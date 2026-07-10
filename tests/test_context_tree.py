"""Context-tree analytic ground-truth tests (Spec §7, gate G3; §4.1–4.3, §4.7; D18).

Fase 0 placeholders: cases and tolerances enumerated per Spec §4.7/§7, no
assertions yet. Never delete or weaken a test to make it pass.
"""

import pytest

SKIP = pytest.mark.skip(reason="Fase 0 scaffold — implement at gate G3 per Spec §7")


@SKIP
def test_iid_uniform_m4():
    """(a) i.i.d. uniform, m = 4, N = 2e5: h_online → 2.000 bits (tol 0.02);
    mean selected depth < 0.2 (§4.7a)."""


@SKIP
def test_period3_cycle():
    """(b) deterministic ABCABC…: held-out CE < 0.02 bits; depths at 1 (§4.7b)."""


@SKIP
def test_order1_markov():
    """(c) order-1 binary chain, P(stay) = 0.8: rate H_b(0.2) = 0.7219 bits;
    held-out CE within 0.03 (§4.7c)."""


@SKIP
def test_order2_xor():
    """(d) X_t = X_{t-2} XOR Z_t, Z ~ Bern(0.1): true rate H_b(0.1) = 0.4690 bits
    vs ≈ 1.0 for any order-1 model; tree must reach depth 2, held-out CE within
    0.03 of 0.4690 (§4.7d)."""


@SKIP
def test_d_max_honored():
    """No selected or grown context deeper than d_max (§4.1)."""


@SKIP
def test_k_min_gamma_behavior():
    """Selection requires total(s_i) ≥ k_min and Δ(s_i) > γ along the path (§4.1)."""


@SKIP
def test_fallback_to_deepest_ancestor():
    """Context prefix absent at evaluation → deepest existing ancestor; root
    always exists (§4.3)."""


@SKIP
def test_unseen_symbol_never_p_zero():
    """β-smoothing: unseen symbols never get probability 0 (§4.1, §4.3)."""
