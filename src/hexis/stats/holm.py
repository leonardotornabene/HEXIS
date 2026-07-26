"""Holm-Bonferroni over the confirmatory family {P1, P2} at alpha = 0.05
(thresholds 0.025 / 0.05; valid under arbitrary dependence) (Spec §5.4; D33).

Signature chosen under the P3b authorization (not fixed in §6.2); recorded in
docs/HANDOFF.md. Step-down: sort ascending, reject p_(i) while it clears
alpha / (m - i); stop at the first failure; adjusted p-values are made monotone.
"""

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass
class HolmResult:
    order: list[str]            # names ascending by raw p
    adjusted: dict[str, float]  # monotone Holm-adjusted p-values
    reject: dict[str, bool]     # step-down rejections at alpha


def holm_bonferroni(pvalues: Mapping[str, float], alpha: float = 0.05) -> HolmResult:
    items = sorted(pvalues.items(), key=lambda kv: kv[1])
    m = len(items)
    order = [name for name, _ in items]
    adjusted: dict[str, float] = {}
    reject: dict[str, bool] = {}
    running = 0.0
    still_rejecting = True
    for i, (name, p) in enumerate(items):
        running = max(running, min(1.0, (m - i) * p))  # monotone non-decreasing
        adjusted[name] = running
        if still_rejecting and p <= alpha / (m - i):
            reject[name] = True
        else:
            still_rejecting = False
            reject[name] = False
    return HolmResult(order, adjusted, reject)
