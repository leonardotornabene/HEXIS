"""Validation against sources with analytically known entropy rates.

Tolerances account for the finite-N positive bias of the online estimator
(S&G Eq. (28)) and for the per-sentence restart cost (the first token of a
sentence is coded at the root by construction).
"""

import math

from hexis_ctree import (
    Alphabet,
    ContextTreeConfig,
    ContextTreeModel,
    mean_context_gain_bits,
    mean_selected_depth,
)
from hexis_ctree.synthetic import (
    default_symbols,
    iid_uniform_document,
    markov_document,
    markov_entropy_rate_bits,
    periodic_template_document,
    template_phase_known_entropy_rate_bits,
)


def test_iid_uniform_entropy_rate():
    d = 4
    train = iid_uniform_document(d, n_sentences=250, sentence_length=200, seed=1)
    alph = Alphabet(default_symbols(d))
    m = ContextTreeModel(alph).fit([train])
    h_true = math.log2(d)  # 2.0 bits
    assert h_true - 0.01 < m.online_entropy_rate < h_true + 0.06

    m.freeze()
    fresh = iid_uniform_document(d, n_sentences=100, sentence_length=200, seed=2)
    ce = m.cross_entropy([fresh])
    assert abs(ce - h_true) < 0.03

    scores = m.score_document(fresh)
    # No genuine context structure: mean gain ~ 0, shallow selection.
    assert abs(mean_context_gain_bits(scores)) < 0.03
    assert mean_selected_depth(scores) < 0.5


def test_markov_order1_entropy_rate_gain_and_depth():
    p_stay = 0.9
    P = [[p_stay, 1 - p_stay], [1 - p_stay, p_stay]]
    h_true = markov_entropy_rate_bits(P)  # ~0.4690 bits
    assert abs(h_true - 0.46899559) < 1e-6

    train = markov_document(P, n_sentences=300, sentence_length=200, seed=3)
    alph = Alphabet(default_symbols(2))
    m = ContextTreeModel(alph).fit([train])
    assert h_true - 0.01 < m.online_entropy_rate < h_true + 0.06

    m.freeze()
    fresh = markov_document(P, n_sentences=100, sentence_length=200, seed=4)
    ce = m.cross_entropy([fresh])
    assert h_true - 0.01 < ce < h_true + 0.04

    scores = m.score_document(fresh)
    # Marginal is uniform (H1 = 1 bit): expected gain ~ H1 - h ~ 0.531.
    gain = mean_context_gain_bits(scores)
    assert 0.47 < gain < 0.59
    depth = mean_selected_depth(scores)
    assert 0.9 < depth < 1.8  # order-1 structure; mild spurious deepening allowed


def test_periodic_template_low_entropy_and_deep_context():
    d = 6
    noise = 0.02
    template = list("abacad")  # after 'a' the phase must be read from depth 2
    train = periodic_template_document(
        template, d, n_sentences=200, sentence_length=120, noise=noise, seed=5
    )
    alph = Alphabet(default_symbols(d))
    m = ContextTreeModel(alph).fit([train])
    h_lower = template_phase_known_entropy_rate_bits(d, noise)  # ~0.188 bits
    marginal_upper = 1.8  # H1 of the template distribution ~1.79 bits
    assert h_lower < m.online_entropy_rate < 0.6 < marginal_upper

    m.freeze()
    fresh = periodic_template_document(
        template, d, n_sentences=80, sentence_length=120, noise=noise, seed=6
    )
    scores = m.score_document(fresh)
    assert mean_context_gain_bits(scores) > 1.0
    assert mean_selected_depth(scores) > 1.3
