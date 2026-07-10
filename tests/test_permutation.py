"""Exact randomization-test tests (Spec §7, gate G0; §5.1–5.2; D21, D36).

Fase 0 placeholders: cases enumerated per Spec §7, no assertions yet.
Never delete or weaken a test to make it pass.
"""

import pytest

SKIP = pytest.mark.skip(reason="Fase 0 scaffold — implement at gate G0 per Spec §7")


@SKIP
def test_enumeration_counts():
    """Exact enumeration counts = C(n, k) for label permutation and 2^n for
    sign-flip (§5.1)."""


@SKIP
def test_null_synthetic_p_uniform():
    """Null synthetic data → p ~ Uniform (KS over repetitions) (§7)."""


@SKIP
def test_planted_effect_small_p():
    """Planted effect → small p (§7)."""


@SKIP
def test_one_two_sided_consistency():
    """One-/two-sided consistency (§7; D33 sidedness)."""
