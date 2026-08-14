"""Hierarchical document bootstrap: resample documents with replacement within each
label group (B = 2000, seeded) on fixed per-document score tables (Spec §5.3; D22).

CI semantics: between-document, conditional on the fitted per-document scores
(§5.3). Signature chosen under the P3b authorization (not fixed in §6.2);
ratified by the owner on 2026-07-27 and recorded in docs/HANDOFF.md.
Determinism via np.random.default_rng(seed) (D26).
"""

import operator
from dataclasses import dataclass

import numpy as np


@dataclass
class BootResult:
    observed: float
    replicates: np.ndarray
    ci: tuple[float, float]


def document_bootstrap(
    values,
    labels,
    B: int = 2000,
    seed: int = 0,
    alpha: float = 0.05,
    statistic=None,
) -> BootResult:
    """Percentile CI of a two-group statistic under within-group document resampling.

    Default statistic: mean(group sorted-first) - mean(group sorted-second).
    Resampling is stratified by label group (whole-document draws with
    replacement), so group membership is preserved in every replicate.
    """
    values = np.asarray(values, dtype=float)
    labels = np.asarray(labels)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("values must be a non-empty one-dimensional array")
    if labels.ndim != 1 or labels.size != values.size:
        raise ValueError("labels must be one-dimensional and match values length")
    if not np.isfinite(values).all():
        raise ValueError("values must contain only finite values")
    try:
        B = operator.index(B)
    except TypeError as exc:
        raise ValueError("B must be a positive integer") from exc
    if B <= 0:
        raise ValueError("B must be a positive integer")
    if not np.isfinite(alpha) or not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be finite and in (0, 1)")
    if statistic is not None and not callable(statistic):
        raise ValueError("statistic must be callable")
    uniq = np.unique(labels)
    if uniq.size != 2:
        raise ValueError(f"exactly two label groups required, got {uniq.size}")

    if statistic is None:
        def statistic(v, lab):
            return float(v[lab == uniq[0]].mean() - v[lab == uniq[1]].mean())

    rng = np.random.default_rng(seed)
    group_idx = {u: np.flatnonzero(labels == u) for u in uniq}
    replicates = np.empty(B, dtype=float)
    for b in range(B):
        idx = np.concatenate(
            [rng.choice(group_idx[u], size=group_idx[u].size, replace=True) for u in uniq]
        )
        replicates[b] = statistic(values[idx], labels[idx])

    observed = statistic(values, labels)
    lo, hi = np.quantile(replicates, [alpha / 2, 1.0 - alpha / 2])
    return BootResult(float(observed), replicates, (float(lo), float(hi)))
