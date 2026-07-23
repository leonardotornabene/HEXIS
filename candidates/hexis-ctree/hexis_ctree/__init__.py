"""hexis_ctree: Rissanen-style MDL context tree for the HEXIS project.

Single-instrument engine (Decision D32) following Schuermann & Grassberger
(1996), Chaos 6(3):414-427, arXiv:cond-mat/0203436, with the HEXIS-specific
extensions (sentence-level hard reset, frozen evaluation, label-free
P2/S1 score construction) documented in model.py and ASSUMPTIONS.md.
"""

from .alphabet import Alphabet
from .config import ContextTreeConfig
from .model import ContextTreeModel, __version__
from .scores import (
    MIN_AVAILABLE_PAST_FOR_GAIN_AND_DEPTH,
    DocumentScores,
    SentenceScores,
    eligible_position_count,
    mean_codelength_bits,
    mean_context_gain_bits,
    mean_selected_depth,
)
from .stats import (
    DocStatistic,
    document_mean_difference,
    fit_context_tree,
    per_document_depth,
    per_document_gain,
    permutation_test_label_free,
    pooled_document_scores,
    token_weighted_mean_difference,
    transfer_matrix,
)

__all__ = [
    "Alphabet",
    "ContextTreeConfig",
    "ContextTreeModel",
    "MIN_AVAILABLE_PAST_FOR_GAIN_AND_DEPTH",
    "DocumentScores",
    "SentenceScores",
    "DocStatistic",
    "document_mean_difference",
    "eligible_position_count",
    "mean_codelength_bits",
    "mean_context_gain_bits",
    "mean_selected_depth",
    "fit_context_tree",
    "per_document_gain",
    "per_document_depth",
    "permutation_test_label_free",
    "pooled_document_scores",
    "token_weighted_mean_difference",
    "transfer_matrix",
    "__version__",
]
