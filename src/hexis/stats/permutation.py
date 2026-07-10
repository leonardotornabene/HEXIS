"""Exact randomization tests at document level (Spec §5.1–5.2; D21, D33, D36)."""

from dataclasses import dataclass

import numpy as np


@dataclass
class PermResult:
    """Result of an exact randomization test (Spec §6.2)."""

    p_exact: float
    observed: float
    null_distribution: np.ndarray
    n_enumerated: int


def exact_label_permutation(scores: np.ndarray, labels: np.ndarray, sided: str) -> PermResult:
    """Exact document-label permutation; enumerates C(n, k) (Spec §5.1–5.2; D21, D36)."""
    raise NotImplementedError


def exact_sign_flip(values: np.ndarray, sided: str) -> PermResult:
    """Exact sign-flip over documents; enumerates 2^n (Spec §5.1–5.2; D21, D36)."""
    raise NotImplementedError
