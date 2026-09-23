"""Per-position scores and their aggregation.

Score semantics (frozen evaluation; see model.ContextTreeModel.score_document):

- ``codelen_bits[i]``      = -log2 p_hat(s_i | selected context)   (frozen model)
- ``root_codelen_bits[i]`` = -log2 p_hat(s_i | empty context)      (same model)
- ``context_gain_bits[i]`` = root_codelen_bits[i] - codelen_bits[i]
- ``selected_depth[i]``    = depth of the MDL-selected context node
- ``available_past[i]``    = i, the number of same-sentence tokens preceding
                             position i (0-based). Contexts never cross
                             sentence boundaries, so this is the maximum
                             usable context length at that position.

Locked HEXIS decision implemented here: the P2 (context gain) and S1 (depth)
statistics are computed only at positions with available_past >= 4
(``MIN_AVAILABLE_PAST_FOR_GAIN_AND_DEPTH``). The P1 ingredient
(cross-entropy / mean code length) uses *all* real-token positions, averaged
over real tokens only (no BOS symbol exists anywhere in the pipeline).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, List, Tuple

# Locked HEXIS decision (position restriction for gain and depth scores).
MIN_AVAILABLE_PAST_FOR_GAIN_AND_DEPTH: int = 4


@dataclass(frozen=True)
class SentenceScores:
    """Parallel per-position score arrays for one sentence.

    ``matched_depth[i]`` is the depth of the deepest *existing* tree node
    along the past at position i (>= selected_depth[i]); together with
    ``available_past`` it supports the coverage statistics of Spec
    section 4.3 (e.g. the depth_matched vs depth_selected distribution).
    """

    codelen_bits: Tuple[float, ...]
    root_codelen_bits: Tuple[float, ...]
    selected_depth: Tuple[int, ...]
    matched_depth: Tuple[int, ...]
    available_past: Tuple[int, ...]

    def __post_init__(self) -> None:
        n = len(self.codelen_bits)
        if not (
            len(self.root_codelen_bits) == n
            and len(self.selected_depth) == n
            and len(self.matched_depth) == n
            and len(self.available_past) == n
        ):
            raise ValueError("SentenceScores arrays must have equal length.")

    def __len__(self) -> int:
        return len(self.codelen_bits)

    def context_gain_bits(self) -> Tuple[float, ...]:
        return tuple(
            r - c for r, c in zip(self.root_codelen_bits, self.codelen_bits)
        )


@dataclass(frozen=True)
class DocumentScores:
    """Scores for one document (a sequence of sentences)."""

    sentences: Tuple[SentenceScores, ...]

    def n_positions(self) -> int:
        return sum(len(s) for s in self.sentences)

    def iter_positions(self) -> Iterator[Tuple[float, float, int, int]]:
        """Yield (codelen, root_codelen, depth, available_past) per token."""
        for s in self.sentences:
            yield from zip(
                s.codelen_bits,
                s.root_codelen_bits,
                s.selected_depth,
                s.available_past,
            )


# ---------------------------------------------------------------------- #
# Aggregators. All means are token-weighted over the eligible positions.
# ---------------------------------------------------------------------- #
def _as_list(scores: "DocumentScores | Iterable[DocumentScores]") -> List[DocumentScores]:
    if isinstance(scores, DocumentScores):
        return [scores]
    return list(scores)


def mean_codelength_bits(scores: "DocumentScores | Iterable[DocumentScores]") -> float:
    """Mean code length in bits per token over ALL real-token positions.

    This is the cross-entropy-rate ingredient of the P1 (transfer) statistic:
    positions at every available_past (including sentence-initial tokens,
    which are coded at the root) contribute; the average runs over real
    tokens only.
    """
    total = 0.0
    n = 0
    for doc in _as_list(scores):
        for codelen, _root, _depth, _avail in doc.iter_positions():
            total += codelen
            n += 1
    if n == 0:
        raise ValueError("No positions to aggregate.")
    return total / n


def mean_context_gain_bits(
    scores: "DocumentScores | Iterable[DocumentScores]",
    min_available_past: int = MIN_AVAILABLE_PAST_FOR_GAIN_AND_DEPTH,
) -> float:
    """Mean context gain (bits) over positions with available_past >= threshold (P2 ingredient)."""
    total = 0.0
    n = 0
    for doc in _as_list(scores):
        for codelen, root, _depth, avail in doc.iter_positions():
            if avail >= min_available_past:
                total += root - codelen
                n += 1
    if n == 0:
        raise ValueError(
            f"No positions with available_past >= {min_available_past}; "
            "sentences may be too short for the position restriction."
        )
    return total / n


def mean_selected_depth(
    scores: "DocumentScores | Iterable[DocumentScores]",
    min_available_past: int = MIN_AVAILABLE_PAST_FOR_GAIN_AND_DEPTH,
) -> float:
    """Mean MDL-selected context depth over eligible positions (S1 ingredient)."""
    total = 0
    n = 0
    for doc in _as_list(scores):
        for _codelen, _root, depth, avail in doc.iter_positions():
            if avail >= min_available_past:
                total += depth
                n += 1
    if n == 0:
        raise ValueError(
            f"No positions with available_past >= {min_available_past}."
        )
    return total / n


def eligible_position_count(
    scores: "DocumentScores | Iterable[DocumentScores]",
    min_available_past: int = MIN_AVAILABLE_PAST_FOR_GAIN_AND_DEPTH,
) -> int:
    """Number of positions passing the available_past restriction."""
    n = 0
    for doc in _as_list(scores):
        for _c, _r, _d, avail in doc.iter_positions():
            if avail >= min_available_past:
                n += 1
    return n
