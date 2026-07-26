"""Exact randomization-test tests (Spec §7, gate G0; §5.1-5.2; D21, D36).

Generic utilities only — the confirmatory application of the sign-flip to P1 is
gated by O7 (D44) and is not exercised here. Statistic conventions:
  * label permutation: mean(group sorted-first) - mean(group sorted-second),
    enumerated over all C(n, k) assignments of the k first-group positions;
  * sign flip: mean(sign .* values) over all 2^n sign vectors; observed = all +1.
Ground-truth p-values below are computed by hand from those definitions.
"""

import math

import numpy as np
import pytest
from scipy import stats

from hexis.stats.permutation import PermResult, exact_label_permutation, exact_sign_flip

_LABELS5 = ["A", "A", "B", "B", "B"]
_SCORES5 = [4.0, 3.0, 2.0, 1.0, 0.0]  # observed T = mean(4,3) - mean(2,1,0) = 2.5, the max


@pytest.mark.g0
def test_enumeration_counts():
    r = exact_label_permutation(_SCORES5, _LABELS5, "greater")
    assert r.n_enumerated == math.comb(5, 2)  # 10
    assert r.null_distribution.shape == (10,)
    assert isinstance(r, PermResult)

    s = exact_sign_flip([1, 2, 3, 4, 5, 6], "greater")
    assert s.n_enumerated == 2**6  # 64
    assert s.null_distribution.shape == (64,)


@pytest.mark.g0
def test_label_permutation_exact_pvalues():
    assert exact_label_permutation(_SCORES5, _LABELS5, "greater").observed == pytest.approx(2.5)
    assert exact_label_permutation(_SCORES5, _LABELS5, "greater").p_exact == pytest.approx(0.1)
    assert exact_label_permutation(_SCORES5, _LABELS5, "less").p_exact == pytest.approx(1.0)
    assert exact_label_permutation(_SCORES5, _LABELS5, "two-sided").p_exact == pytest.approx(0.2)


@pytest.mark.g0
def test_sign_flip_exact_pvalues():
    v = [1.0, 2.0, 3.0]  # null {±2, ±4/3, ±2/3, 0, 0}/... observed = 2.0 (the max)
    assert exact_sign_flip(v, "greater").observed == pytest.approx(2.0)
    assert exact_sign_flip(v, "greater").p_exact == pytest.approx(1 / 8)
    assert exact_sign_flip(v, "less").p_exact == pytest.approx(1.0)
    assert exact_sign_flip(v, "two-sided").p_exact == pytest.approx(2 / 8)


@pytest.mark.g0
def test_null_synthetic_p_uniform():
    rng = np.random.default_rng(20260706)
    ps = [exact_sign_flip(rng.standard_normal(8), "greater").p_exact for _ in range(400)]
    assert stats.kstest(ps, "uniform").pvalue > 0.05

    labels = np.array(["A"] * 4 + ["B"] * 4)
    pl = [
        exact_label_permutation(rng.standard_normal(8), labels, "greater").p_exact
        for _ in range(400)
    ]
    assert stats.kstest(pl, "uniform").pvalue > 0.05


@pytest.mark.g0
def test_planted_effect_small_p():
    s = exact_sign_flip([5, 6, 7, 8, 9, 10, 11, 12], "greater")
    assert s.p_exact == pytest.approx(1 / 256)  # all positive → observed is the unique max

    r = exact_label_permutation([100, 101, 102, 0, 1, 2], ["A", "A", "A", "B", "B", "B"], "greater")
    assert r.p_exact == pytest.approx(1 / math.comb(6, 3))  # perfectly separated → unique max


@pytest.mark.g0
def test_one_two_sided_consistency():
    v = [1.0, 2.0, 3.0]
    g = exact_sign_flip(v, "greater").p_exact
    lo = exact_sign_flip(v, "less").p_exact
    t = exact_sign_flip(v, "two-sided").p_exact
    assert g + lo >= 1.0  # both tails include the observed value
    assert t == pytest.approx(2 * min(g, lo))  # sign-flip null is symmetric about 0
    mirrored = exact_sign_flip([-x for x in v], "greater").p_exact
    assert mirrored == pytest.approx(lo)  # flipping the data swaps greater<->less


@pytest.mark.g0
def test_invalid_inputs_fail_loud():
    with pytest.raises(ValueError):
        exact_label_permutation(_SCORES5, ["A", "B", "C", "A", "B"], "greater")  # 3 groups
    with pytest.raises(ValueError):
        exact_sign_flip([1.0, 2.0], "sideways")  # bad sidedness
