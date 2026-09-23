"""Score-function tests (Spec §7; G0 boundary contract, G3 scoring behavior).

The D52 label-free/annotation boundary is retained under the active v3.1 API
(V3-001, §11.1); the retired protocol-(c) argument vocabulary is superseded.
The analytic,
restriction, and byte-identity cases remain Phase-0 placeholders for G3 and
must never be deleted or weakened.
"""

import inspect

import pandas as pd
import pytest

from hexis.protocols import scores

SKIP = pytest.mark.skip(reason="Fase 0 scaffold — implement at gate G3 per Spec §7")


@pytest.mark.g0
@pytest.mark.v31
def test_pooled_score_core_has_label_free_signature():
    core = getattr(scores, "pooled_score_core", None)
    assert core is not None

    signature = inspect.signature(core)
    assert tuple(signature.parameters) == (
        "original",
        "shuffled",
        "model_original",
        "model_shuffled",
        "min_available_past",
    )
    assert set(signature.parameters).isdisjoint(
        {"registry", "regime", "author", "work"}
    )
    assert signature.return_annotation == tuple[pd.DataFrame, pd.DataFrame]


@pytest.mark.g0
@pytest.mark.v31
def test_annotate_scores_has_d52_signature():
    annotate = getattr(scores, "annotate_scores", None)
    assert annotate is not None

    signature = inspect.signature(annotate)
    assert tuple(signature.parameters) == ("scores", "registry", "on")
    assert signature.return_annotation is pd.DataFrame


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
