"""Slice-identity diagnostics tests (Spec §7, gate G3; §4.6; D32 — diagnostics, not results).

Fase 0 placeholders: cases enumerated per Spec §4.6/§7, no assertions yet.
Never delete or weaken a test to make it pass.
"""

import pytest

SKIP = pytest.mark.skip(reason="Fase 0 scaffold — implement at gate G3 per Spec §7")


@SKIP
def test_root_equals_add_beta_unigram():
    """Root distribution = add-β-smoothed unigram of training sample; max abs
    deviation < 1e-12 (§4.6 i)."""


@SKIP
def test_depth1_nodes_equal_smoothed_bigram():
    """Each depth-1 node's distribution = smoothed conditional bigram table for
    its context symbol (§4.6 ii)."""


@SKIP
def test_evaluate_on_train_consistency():
    """evaluate() on training material (updates disabled) reproduces per-position
    code lengths consistent with stored L_self totals at the root (§4.6 iii)."""
