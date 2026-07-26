"""Hierarchical document bootstrap: resample documents with replacement within each
label group (B = 2000, seeded) on fixed per-document score tables (Spec §5.3; D22).

CI semantics: between-document, conditional on the fitted per-document scores
(§5.3). Signature chosen under the P3b authorization (not fixed in §6.2);
recorded in docs/HANDOFF.md. Determinism via np.random.default_rng(seed) (D26).
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class BootResult:
    observed: float
    replicates: np.ndarray
    ci: tuple[float, float]


def document_bootstrap(values, labels, B: int = 2000, seed: int = 0, alpha: float = 0.05, statistic=None) -> BootResult:
    """Percentile CI of a two-group statistic under within-group document resampling.

    Default statistic: mean(group sorted-first) - mean(group sorted-second).
    Resampling is stratified by label group (whole-document draws with
    replacement), so group membership is preserved in every replicate.
    """
    values = np.asarray(values, dtype=float)
    labels = np.asarray(labels)
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
