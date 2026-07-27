"""Bootstrap and Holm tests (Spec §7, gate G0; §5.3-5.4; D22, D33).

Signatures were not fixed in §6.2 ("proposed before implementation"); chosen here
under the P3b authorization and recorded in docs/HANDOFF.md:
  holm_bonferroni(pvalues: Mapping[str, float], alpha=0.05) -> HolmResult
  document_bootstrap(values, labels, B=2000, seed=0, alpha=0.05, statistic=None) -> BootResult
"""

import numpy as np
import pytest

from hexis.stats.bootstrap import BootResult, document_bootstrap
from hexis.stats.holm import HolmResult, holm_bonferroni


# --- Holm (§5.4; family {P1, P2} → thresholds 0.025 / 0.05) ---------------------


@pytest.mark.g0
def test_holm_family_of_two_thresholds():
    # smallest p must clear alpha/2 = 0.025; the next clears alpha/1 = 0.05.
    both = holm_bonferroni({"P1": 0.01, "P2": 0.03})
    assert isinstance(both, HolmResult)
    assert both.reject == {"P1": True, "P2": True}
    assert both.adjusted["P1"] == pytest.approx(0.02)  # min(1, 2*0.01)
    assert both.adjusted["P2"] == pytest.approx(0.03)  # max(0.02, 1*0.03)


@pytest.mark.g0
def test_holm_step_down_stops_at_first_non_reject():
    res = holm_bonferroni({"P1": 0.03, "P2": 0.001})  # sorted: P2=0.001, P1=0.03
    # P2 clears 0.025; P1 = 0.03 does NOT clear 0.05/1 = 0.05? it does (0.03<=0.05) → reject.
    assert res.reject == {"P1": True, "P2": True}
    # but if the smallest fails its 0.025 gate, nothing is rejected (step-down):
    none = holm_bonferroni({"P1": 0.03, "P2": 0.04})
    assert none.reject == {"P1": False, "P2": False}
    assert none.adjusted["P1"] == pytest.approx(0.06)  # 2*0.03, capped at 1
    assert none.adjusted["P2"] == pytest.approx(0.06)  # monotone: max(0.06, 0.04)


@pytest.mark.g0
def test_holm_boundary_and_order_invariance():
    assert holm_bonferroni({"P1": 0.025, "P2": 0.05}).reject == {"P1": True, "P2": True}
    a = holm_bonferroni({"P1": 0.02, "P2": 0.20})
    b = holm_bonferroni({"P2": 0.20, "P1": 0.02})
    assert a.adjusted == b.adjusted and a.reject == b.reject
    assert a.reject == {"P1": True, "P2": False}
    assert a.order == ["P1", "P2"]  # ascending by p


@pytest.mark.g0
def test_holm_adjusted_is_monotone_nondecreasing():
    res = holm_bonferroni({"a": 0.001, "b": 0.2, "c": 0.02, "d": 0.9})
    ordered = [res.adjusted[name] for name in res.order]
    assert ordered == sorted(ordered)
    assert all(0.0 <= p <= 1.0 for p in ordered)


@pytest.mark.g0
def test_holm_rejects_invalid_probability_domain():
    invalid_cases = (
        ({"P1": -0.1, "P2": 0.2}, 0.05),
        ({"P1": 0.1, "P2": 1.1}, 0.05),
        ({"P1": np.nan, "P2": 0.2}, 0.05),
        ({}, 0.05),
        ({"P1": 0.1, "P2": 0.2}, 0.0),
        ({"P1": 0.1, "P2": 0.2}, 1.1),
    )
    errors = []
    for pvalues, alpha in invalid_cases:
        with pytest.raises(ValueError) as exc:
            holm_bonferroni(pvalues, alpha=alpha)
        errors.append(exc.value)
    assert all(error.args for error in errors)


# --- Hierarchical document bootstrap (§5.3; D22) --------------------------------


@pytest.mark.g0
def test_bootstrap_reproducible_under_fixed_seed():
    v = np.array([3.0, 1.0, 4.0, 0.0, 2.0, 5.0])
    lab = np.array(["H", "H", "H", "P", "P", "P"])
    r1 = document_bootstrap(v, lab, B=500, seed=20260706)
    r2 = document_bootstrap(v, lab, B=500, seed=20260706)
    assert isinstance(r1, BootResult)
    assert np.array_equal(r1.replicates, r2.replicates)
    assert r1.ci == r2.ci
    r3 = document_bootstrap(v, lab, B=500, seed=1)
    assert not np.array_equal(r1.replicates, r3.replicates)


@pytest.mark.g0
def test_bootstrap_resamples_within_groups_only():
    # group H is constant → mean_H is invariant → all variation is from P only.
    v = np.array([5.0, 5.0, 5.0, 0.0, 2.0, 4.0])
    lab = np.array(["H", "H", "H", "P", "P", "P"])
    res = document_bootstrap(v, lab, B=800, seed=7)
    assert res.observed == pytest.approx(5.0 - 2.0)  # mean_H - mean_P
    assert res.replicates.shape == (800,)
    # statistic = 5 - mean(resampled P); P resamples of {0,2,4} give means in [0,4]
    assert np.all(res.replicates >= 1.0 - 1e-9)
    assert np.all(res.replicates <= 5.0 + 1e-9)
    lo, hi = res.ci
    assert lo <= hi


@pytest.mark.g0
def test_bootstrap_fails_loud_on_wrong_group_count():
    with pytest.raises(ValueError) as exc:
        document_bootstrap(np.array([1.0, 2.0, 3.0]), np.array(["A", "B", "C"]), B=10, seed=0)
    assert exc.value.args


@pytest.mark.g0
def test_bootstrap_rejects_invalid_input_domain():
    cases = (
        ([1.0, 2.0, 3.0], ["A", "B"], 10, 0.05),
        ([], [], 10, 0.05),
        ([1.0, np.nan], ["A", "B"], 10, 0.05),
        ([[1.0, 2.0]], [["A", "B"]], 10, 0.05),
        ([1.0, 2.0], ["A", "B"], 0, 0.05),
        ([1.0, 2.0], ["A", "B"], 10, 0.0),
        ([1.0, 2.0], ["A", "B"], 10, 1.0),
    )
    errors = []
    for values, labels, B, alpha in cases:
        with pytest.raises(ValueError) as exc:
            document_bootstrap(values, labels, B=B, seed=0, alpha=alpha)
        errors.append(exc.value)
    assert all(error.args for error in errors)


@pytest.mark.g0
def test_bootstrap_supports_unweighted_p1_mean_with_unequal_groups():
    values = np.arange(11, dtype=float)
    labels = np.array(["HEX"] * 5 + ["PROSE"] * 6)

    def p1_mean(sample, sample_labels):
        assert sample.shape == sample_labels.shape
        return float(sample.mean())

    result = document_bootstrap(values, labels, B=20, seed=19, statistic=p1_mean)
    assert result.observed == pytest.approx(values.mean())
    assert result.replicates.shape == (20,)
    assert np.isfinite(result.replicates).all()
