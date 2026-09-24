"""Regressions found by the review of the whole package before V4 (V3-006)."""

import math

import pytest

from hormathos.contracts import load_contracts
from hormathos.corpus import verify_sequences
from hormathos.model.context_tree import CTW
from hormathos.protocols import scores
from test_v31_corpus import real_corpus
from test_v31_scores import cycle, model, stream

pytestmark = pytest.mark.v31


def test_sequence_eligibility_follows_the_configured_min_available_past(real_corpus):
    """F1: the validator reads the threshold from the design, as `encode_corpus` does."""
    contracts = load_contracts()
    design = {**contracts['design'],
              'min_available_past': contracts['design']['min_available_past'] + 1}
    with pytest.raises(ValueError, match='eligibility mismatch') as error:
        verify_sequences(real_corpus['coordinates.parquet'], real_corpus['sequences.parquet'],
                         design, contracts['alphabets'])
    assert 'eligibility mismatch' in str(error.value)


def test_scoring_hands_the_model_only_the_last_depth_symbols():
    """F2: only the last D symbols decide the path (§6.4), so the scorer passes that
    window and never the whole prefix; the losses equal the full-prefix prediction."""
    depth, symbols = 2, cycle(12, 3)
    trained = model([symbols], m=3, depth=depth)
    lengths = []
    for name in ('mixture', 'predict_proba'):
        def spy(history, method=getattr(trained, name)):
            lengths.append(len(history))
            return method(history)
        setattr(trained, name, spy)
    positions, _ = scores.pooled_score_core(
        [stream('a@1', symbols)], [stream('a@1', symbols, origin=range(len(symbols)))],
        model_original=trained, model_shuffled=trained)
    assert lengths and max(lengths) == depth
    assert positions['loss_ctw_original'].tolist() == [
        -math.log2(CTW.predict_proba(trained, symbols[:past])[symbols[past]])
        for past in positions['available_past']]
