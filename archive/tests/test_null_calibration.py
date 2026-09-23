"""Null-calibration tests for the P1 inference chain (Spec §7, gate G3; O7/D44).

Fase 0 placeholders: cases enumerated per D44(v), no assertions yet.
Never delete or weaken a test to make it pass.
"""

import pytest

SKIP = pytest.mark.skip(reason="Fase 0 scaffold — implement at gate G3 per Spec §7")


@SKIP
def test_pseudo_documents_match_corpus_size_profile():
    """Synthetic H0 material split into 11 pseudo-documents whose token-size
    profile matches the corpus (profile available after G1; D44 v)."""


@SKIP
def test_sign_flip_type_one_error_at_nominal_levels():
    """Empirical type-I error of the full P1 chain (LODO, T*-matching,
    seed-averaging, exact sign-flip) under a true null, at the nominal levels,
    over replications (O7; D44 v)."""


@SKIP
def test_p2_permutation_positive_control_calibrates():
    """P2's document-label permutation must calibrate on the same material;
    failure indicates an implementation bug, not a theoretical problem (D44 v)."""
