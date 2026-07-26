"""Exact randomization tests at document level (Spec §5.1-5.2; D21, D33, D36).

Exact enumeration (not sampling): appropriate for this corpus's document counts
(Greek 2^11 = 2048 sign flips / C(n,k) label splits; Latin 2^8 = 256; D43).
Generic utilities only — the confirmatory application of the sign-flip to P1 is
gated by O7 (D44) and must be wired elsewhere.
"""

import itertools
from dataclasses import dataclass

import numpy as np

_SIDES = ("greater", "less", "two-sided")


@dataclass
class PermResult:
    """Result of an exact randomization test (Spec §6.2)."""

    p_exact: float
    observed: float
    null_distribution: np.ndarray
    n_enumerated: int


def _p_value(null: np.ndarray, observed: float, sided: str) -> float:
    if sided == "greater":
        return float(np.mean(null >= observed))
    if sided == "less":
        return float(np.mean(null <= observed))
    if sided == "two-sided":
        mu = float(null.mean())
        return float(np.mean(np.abs(null - mu) >= np.abs(observed - mu) - 1e-12))
    raise ValueError(f"sided must be one of {_SIDES}, got {sided!r}")


def exact_label_permutation(scores: np.ndarray, labels: np.ndarray, sided: str) -> PermResult:
    """Exact document-label permutation; enumerates C(n, k) (Spec §5.1-5.2; D21, D36).

    Statistic: mean(group sorted-first) - mean(group sorted-second). Requires
    exactly two label groups; the observed labelling is one of the enumerated
    splits, so ``p_exact >= 1 / C(n, k)`` (never 0).
    """
    scores = np.asarray(scores, dtype=float)
    labels = np.asarray(labels)
    uniq = np.unique(labels)
    if uniq.size != 2:
        raise ValueError(f"exactly two label groups required, got {uniq.size}")
    n = scores.size
    a_positions = np.flatnonzero(labels == uniq[0])
    k = a_positions.size
    grand = scores.sum()

    def _stat(sum_a: float) -> float:
        return sum_a / k - (grand - sum_a) / (n - k)

    null = np.array(
        [_stat(scores[list(combo)].sum()) for combo in itertools.combinations(range(n), k)]
    )
    observed = _stat(scores[a_positions].sum())
    return PermResult(_p_value(null, observed, sided), float(observed), null, int(null.size))


def exact_sign_flip(values: np.ndarray, sided: str) -> PermResult:
    """Exact sign-flip over documents; enumerates 2^n (Spec §5.1-5.2; D21, D36).

    Statistic: mean(sign .* values) over all 2^n sign vectors; observed = all +1.
    The null is symmetric about 0, so ``p_exact >= 1 / 2^n`` (never 0).
    """
    values = np.asarray(values, dtype=float)
    n = values.size
    signs = np.array(list(itertools.product((-1.0, 1.0), repeat=n)))
    null = (signs * values).mean(axis=1)
    observed = float(values.mean())
    return PermResult(_p_value(null, observed, sided), observed, null, int(null.size))
