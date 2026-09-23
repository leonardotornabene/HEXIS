"""Reference implementation of the HEXIS statistic layer.

STATUS: reference implementation. The engine below (model fitting, frozen
scoring, label-free construction) is the load-bearing part; the exact
aggregation formulas and the full protocol orchestration (gates G0-G7,
protocols (a)/(b)/(c), configuration C0, 13-cell sensitivity plan) are
defined in the HEXIS master specification and MUST be wired against it
before any confirmatory use. Deviations discovered during that wiring are
Decision Log material.

Mapping to the HEXIS statistics family
--------------------------------------
P1 (transfer):      ``transfer_matrix`` -- frozen cross-entropy of each
                    regime's documents under each regime's model, with
                    leave-one-document-out (LODO) on the diagonal.
P2 (context gain):  per-document mean context gain from ONE pooled model
                    fitted without label information, positions restricted
                    to available_past >= 4; label permutation over documents
                    regroups the *fixed* per-document values.
S1 (depth):         same construction with the MDL-selected depth.

Label-free validity: because the pooled model and all per-position scores
are computed once, without reference to regime labels, permuting the labels
does not require refitting anything -- this implements the v2.0 correction
of the v1 flaw (regime-dependent profiles permuted under label-dependent
fits).
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from .alphabet import Alphabet, Document
from .config import ContextTreeConfig
from .model import ContextTreeModel
from .scores import (
    MIN_AVAILABLE_PAST_FOR_GAIN_AND_DEPTH,
    DocumentScores,
    eligible_position_count,
    mean_context_gain_bits,
    mean_selected_depth,
)


# ---------------------------------------------------------------------- #
# Model construction helpers
# ---------------------------------------------------------------------- #
def fit_context_tree(
    documents: Sequence[Document],
    alphabet: Alphabet,
    config: Optional[ContextTreeConfig] = None,
    freeze: bool = True,
) -> ContextTreeModel:
    """Fit (and by default freeze) a context tree on ``documents``."""
    model = ContextTreeModel(alphabet, config).fit(documents)
    return model.freeze() if freeze else model


# ---------------------------------------------------------------------- #
# P1: transfer / cross-entropy matrix with LODO diagonal
# ---------------------------------------------------------------------- #
def transfer_matrix(
    groups: Mapping[str, Sequence[Document]],
    alphabet: Alphabet,
    config: Optional[ContextTreeConfig] = None,
    lodo_diagonal: bool = True,
) -> Dict[Tuple[str, str], float]:
    """Frozen cross-entropy CE(row-group data | column-group model), bits/token.

    Off-diagonal (a != b): one model per group b, fitted on all of group b's
    documents, evaluated on all of group a's documents.

    Diagonal (a == a): if ``lodo_diagonal``, leave-one-document-out --
    for each held-out document, a model is fitted on the remaining documents
    of the group and evaluated on the held-out one; the entries are pooled
    token-weighted (total held-out bits / total held-out tokens). This keeps
    the diagonal out-of-sample and comparable to the off-diagonal entries.
    Requires >= 2 documents per group.

    NOTE (assumption to ratify): pooling of LODO folds is token-weighted;
    a document-weighted alternative is trivial to switch to if the master
    specification prescribes it.
    """
    result: Dict[Tuple[str, str], float] = {}
    full_models: Dict[str, ContextTreeModel] = {
        name: fit_context_tree(docs, alphabet, config)
        for name, docs in groups.items()
    }
    for eval_name, eval_docs in groups.items():
        for model_name, model in full_models.items():
            if eval_name != model_name:
                result[(eval_name, model_name)] = model.cross_entropy(eval_docs)
        # diagonal
        docs = list(groups[eval_name])
        if not lodo_diagonal:
            result[(eval_name, eval_name)] = full_models[
                eval_name
            ].cross_entropy(docs)
            continue
        if len(docs) < 2:
            raise ValueError(
                f"LODO diagonal for group {eval_name!r} requires >= 2 documents."
            )
        total_bits = 0.0
        total_tokens = 0
        for i, held_out in enumerate(docs):
            rest = docs[:i] + docs[i + 1 :]
            fold_model = fit_context_tree(rest, alphabet, config)
            n_tok = sum(len(sentence) for sentence in held_out)
            total_bits += fold_model.cross_entropy([held_out]) * n_tok
            total_tokens += n_tok
        result[(eval_name, eval_name)] = total_bits / total_tokens
    return result


# ---------------------------------------------------------------------- #
# P2 / S1: pooled, label-free per-document statistics
# ---------------------------------------------------------------------- #
@dataclass(frozen=True)
class DocStatistic:
    """A per-document scalar with its token weight (n eligible positions)."""

    value: float
    weight: int


def pooled_document_scores(
    pooled_model: ContextTreeModel,
    documents_by_id: Mapping[str, Document],
) -> Dict[str, DocumentScores]:
    """Frozen per-position scores of every document under ONE pooled model.

    The pooled model must have been fitted without label information (e.g. on
    the union of all documents, or on the LODO-fold union prescribed by
    protocol (c)); this function itself never sees labels.
    """
    return {
        doc_id: pooled_model.score_document(doc)
        for doc_id, doc in documents_by_id.items()
    }


def per_document_gain(
    scores_by_id: Mapping[str, DocumentScores],
    min_available_past: int = MIN_AVAILABLE_PAST_FOR_GAIN_AND_DEPTH,
) -> Dict[str, DocStatistic]:
    return {
        doc_id: DocStatistic(
            value=mean_context_gain_bits(sc, min_available_past),
            weight=eligible_position_count(sc, min_available_past),
        )
        for doc_id, sc in scores_by_id.items()
    }


def per_document_depth(
    scores_by_id: Mapping[str, DocumentScores],
    min_available_past: int = MIN_AVAILABLE_PAST_FOR_GAIN_AND_DEPTH,
) -> Dict[str, DocStatistic]:
    return {
        doc_id: DocStatistic(
            value=mean_selected_depth(sc, min_available_past),
            weight=eligible_position_count(sc, min_available_past),
        )
        for doc_id, sc in scores_by_id.items()
    }


def document_mean_difference(
    stats_by_id: Mapping[str, DocStatistic],
    labels: Mapping[str, str],
    group_a: str,
    group_b: str,
) -> float:
    """T = mean_d(group_a) - mean_d(group_b), UNWEIGHTED over documents.

    This is the Master Spec section 4.4 form of P2/S1: the document is the
    unit of inference, so every document contributes with equal weight
    regardless of its length (consistent with the document-level
    randomization of D21).
    """
    def _dmean(group: str) -> float:
        values = [
            stat.value
            for doc_id, stat in stats_by_id.items()
            if labels[doc_id] == group
        ]
        if not values:
            raise ValueError(f"No documents for group {group!r}.")
        return sum(values) / len(values)

    return _dmean(group_a) - _dmean(group_b)


def token_weighted_mean_difference(
    stats_by_id: Mapping[str, DocStatistic],
    labels: Mapping[str, str],
    group_a: str,
    group_b: str,
) -> float:
    """T = weighted_mean(group_a) - weighted_mean(group_b), token-weighted.

    NOT the spec section 4.4 form (which is the unweighted
    :func:`document_mean_difference`); retained as a labeled descriptive
    alternative because it answers a different question (per-token rather
    than per-document effect). Any confirmatory use would require a
    Decision Log amendment.
    """
    def _wmean(group: str) -> float:
        num = 0.0
        den = 0
        for doc_id, stat in stats_by_id.items():
            if labels[doc_id] == group:
                num += stat.value * stat.weight
                den += stat.weight
        if den == 0:
            raise ValueError(f"No eligible positions for group {group!r}.")
        return num / den

    return _wmean(group_a) - _wmean(group_b)


def permutation_test_label_free(
    stats_by_id: Mapping[str, DocStatistic],
    labels: Mapping[str, str],
    group_a: str,
    group_b: str,
    n_permutations: int = 10_000,
    seed: int = 0,
    two_sided: bool = True,
    statistic: str = "document_mean",
) -> Tuple[float, float]:
    """Label-free permutation test at the document level.

    The per-document statistics are computed ONCE from the pooled model and
    then held fixed; each permutation reassigns the multiset of labels over
    the same document ids and recomputes only the group aggregation. This is
    the v2.0-corrected construction: no quantity entering the null
    distribution depends on the permuted labels through a refit.

    ``statistic`` selects the aggregation: ``"document_mean"`` (default;
    the Master Spec section 4.4 form -- unweighted mean over documents,
    matching the document-level randomization unit of D21) or
    ``"token_weighted"`` (labeled descriptive alternative).

    NOTE: this Monte Carlo shuffle is the engine-validation stand-in; the
    confirmatory Greek analysis prescribes EXACT enumeration of the C(11,5)
    label assignments (Spec section 5.1), to be implemented in the
    protocols/stats phase together with the exact sign-flip for P1.

    Returns
    -------
    (observed_statistic, p_value) with the add-one estimator
    p = (1 + #{|T*| >= |T|}) / (1 + n_permutations)  (two-sided), or the
    one-sided analogue on T* >= T.
    """
    stat_fns = {
        "document_mean": document_mean_difference,
        "token_weighted": token_weighted_mean_difference,
    }
    if statistic not in stat_fns:
        raise ValueError(
            f"statistic must be one of {sorted(stat_fns)} (got {statistic!r})"
        )
    stat_fn = stat_fns[statistic]
    doc_ids = sorted(stats_by_id.keys())
    if set(doc_ids) != set(labels.keys()):
        raise ValueError("stats_by_id and labels must cover the same document ids.")
    observed = stat_fn(stats_by_id, labels, group_a, group_b)
    label_pool: List[str] = [labels[doc_id] for doc_id in doc_ids]
    rng = random.Random(seed)
    exceed = 0
    for _ in range(n_permutations):
        shuffled = label_pool[:]
        rng.shuffle(shuffled)
        perm_labels = dict(zip(doc_ids, shuffled))
        t_star = stat_fn(stats_by_id, perm_labels, group_a, group_b)
        if two_sided:
            if abs(t_star) >= abs(observed):
                exceed += 1
        else:
            if t_star >= observed:
                exceed += 1
    p_value = (1 + exceed) / (1 + n_permutations)
    return observed, p_value
