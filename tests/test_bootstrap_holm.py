"""Bootstrap and Holm tests (Spec §7, gate G0; §5.3–5.4; D22, D33).

Fase 0 placeholders: cases enumerated per Spec §7, no assertions yet.
Never delete or weaken a test to make it pass.
"""

import pytest

SKIP = pytest.mark.skip(reason="Fase 0 scaffold — implement at gate G0 per Spec §7")


@SKIP
def test_holm_ordering_fixed_p_vector():
    """Holm ordering on a fixed p-vector; family of 2 → thresholds 0.025 / 0.05
    (§5.4; D33)."""


@SKIP
def test_bootstrap_reproducibility_fixed_seed():
    """Hierarchical document bootstrap reproducible under fixed seed (§5.3; D26)."""
