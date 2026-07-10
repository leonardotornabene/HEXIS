"""Score-function tests (Spec §7, gate G3; §4.4; D35, D36).

Fase 0 placeholders: cases enumerated per Spec §7, no assertions yet.
Never delete or weaken a test to make it pass — the label-invariance test in
particular is mandatory and must never be weakened (D36).
"""

import pytest

SKIP = pytest.mark.skip(reason="Fase 0 scaffold — implement at gate G3 per Spec §7")


@SKIP
def test_delta_ce_analytic_markov_chains():
    """ΔCE on two analytic Markov chains matches analytic CE(B‖A) (§7)."""


@SKIP
def test_gain_restriction_respects_available_past():
    """Primary gain/depth use only positions with available_past ≥ 4 (D35)."""


@SKIP
def test_pooled_scores_label_free_byte_identical():
    """pooled_scores output byte-identical under permuted registry regime labels —
    code-level guarantee of D36 (§7)."""
