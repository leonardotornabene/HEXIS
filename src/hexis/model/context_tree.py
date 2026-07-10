"""MDL context tree — the sole statistical instrument (Spec §4.1–4.3; D18, D32).

Prequential add-β trie over reversed contexts; predictive probability with
PRE-update counts; monotone-stop MDL selection on Δ(s) = L_par − L_self > γ.
No separate model-complexity penalty (D18/D32): prequential coding includes it.
All logarithms base 2; all quantities in bits.
"""

from collections.abc import Iterable, Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class TreeParams:
    """Context-tree parameters (Spec §4.1; config context_tree:, §6.3)."""

    d_max: int = 8
    beta: float = 0.5
    k_min: int = 2
    gamma: float = 0.0
    select: str = "monotone"


@dataclass
class EvalResult:
    """Per-position records from frozen-tree evaluation (Spec §4.3, §6.2)."""

    ce: float
    n: int
    depth_selected: np.ndarray
    depth_matched: np.ndarray
    available_past: np.ndarray
    codelen_root: np.ndarray
    codelen_selected: np.ndarray
    unseen_context_rate: float


class ContextTree:
    """Rissanen-style MDL context tree (Spec §4.1; SG96 §V.A–B correspondence, D18)."""

    def __init__(self, n_symbols: int, params: TreeParams):
        raise NotImplementedError

    def fit(self, sent_seqs: Iterable[Sequence[int]]) -> None:
        """Single prequential pass; sets self.h_online (Spec §4.1, §4.5)."""
        raise NotImplementedError

    def evaluate(self, sent_seqs) -> EvalResult:
        """Frozen tree, no updates; per-position records and fallbacks (Spec §4.3)."""
        raise NotImplementedError

    def root_distribution(self) -> np.ndarray:
        """Smoothed (add-β) root distribution (Spec §4.5, §4.6)."""
        raise NotImplementedError

    def node_table(self, depth: int) -> pd.DataFrame:
        """Diagnostics/lexicon support (Spec §4.6)."""
        raise NotImplementedError

    def top_contexts(self, k: int = 20) -> pd.DataFrame:
        """Contexts ranked by Δ(s) — the context lexicon (Spec §4.5; D38)."""
        raise NotImplementedError
