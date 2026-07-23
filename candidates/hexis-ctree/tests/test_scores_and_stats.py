"""Score aggregation (exact hand values), the available_past >= 4 mask,
the label-free P2/S1 construction, and the P1 transfer matrix."""

from hexis_ctree import (
    Alphabet,
    ContextTreeConfig,
    DocumentScores,
    SentenceScores,
    document_mean_difference,
    eligible_position_count,
    fit_context_tree,
    mean_codelength_bits,
    mean_context_gain_bits,
    mean_selected_depth,
    per_document_gain,
    permutation_test_label_free,
    pooled_document_scores,
    token_weighted_mean_difference,
    transfer_matrix,
)
from hexis_ctree.synthetic import (
    default_symbols,
    markov_document,
    periodic_template_document,
)


# --------------------------------------------------------------------- #
# Aggregators on hand-built scores
# --------------------------------------------------------------------- #
def _hand_doc():
    s = SentenceScores(
        codelen_bits=(1.0, 1.0, 1.0, 1.0, 2.0, 3.0),
        root_codelen_bits=(2.0, 2.0, 2.0, 2.0, 4.0, 4.0),
        selected_depth=(0, 1, 2, 3, 2, 1),
        matched_depth=(0, 1, 2, 3, 4, 5),
        available_past=(0, 1, 2, 3, 4, 5),
    )
    return DocumentScores(sentences=(s,))


def test_aggregators_exact_hand_values():
    doc = _hand_doc()
    # P1 ingredient: over ALL positions.
    assert abs(mean_codelength_bits(doc) - 9.0 / 6.0) < 1e-12
    # P2/S1 ingredients: only available_past >= 4 (positions 4 and 5).
    assert eligible_position_count(doc) == 2
    assert abs(mean_context_gain_bits(doc) - ((4 - 2) + (4 - 3)) / 2.0) < 1e-12
    assert abs(mean_selected_depth(doc) - 1.5) < 1e-12


def test_mask_raises_when_no_eligible_positions():
    s = SentenceScores(
        codelen_bits=(1.0, 1.0),
        root_codelen_bits=(2.0, 2.0),
        selected_depth=(0, 1),
        matched_depth=(0, 1),
        available_past=(0, 1),
    )
    doc = DocumentScores(sentences=(s,))
    try:
        mean_context_gain_bits(doc)  # min_available_past defaults to 4
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError with no eligible positions")


# --------------------------------------------------------------------- #
# Label-free construction (v2.0 correction)
# --------------------------------------------------------------------- #
def _toy_corpus():
    """6 'prose' (order-1 Markov) + 6 'verse' (noisy template) documents."""
    d = 6
    P = [
        [0.45 if j == (i + 1) % d else 0.11 for j in range(d)] for i in range(d)
    ]
    docs = {}
    labels = {}
    for k in range(6):
        docs[f"prose_{k}"] = markov_document(
            P, n_sentences=25, sentence_length=16, seed=100 + k
        )
        labels[f"prose_{k}"] = "PROSE"
    for k in range(6):
        docs[f"verse_{k}"] = periodic_template_document(
            list("abacad"), d, n_sentences=25, sentence_length=16,
            noise=0.03, seed=200 + k,
        )
        labels[f"verse_{k}"] = "HEX"
    return docs, labels


def test_scores_are_label_free_and_reproducible():
    docs, labels = _toy_corpus()
    alph = Alphabet(default_symbols(6))
    pooled = fit_context_tree(list(docs.values()), alph)
    scores1 = pooled_document_scores(pooled, docs)
    scores2 = pooled_document_scores(pooled, docs)  # labels never enter
    for doc_id in docs:
        assert scores1[doc_id] == scores2[doc_id]


def test_permutation_test_detects_regime_difference_and_is_symmetric():
    docs, labels = _toy_corpus()
    alph = Alphabet(default_symbols(6))
    pooled = fit_context_tree(list(docs.values()), alph)
    gains = per_document_gain(pooled_document_scores(pooled, docs))

    # Spec section 4.4 statistic: UNWEIGHTED mean over documents.
    t_doc = document_mean_difference(gains, labels, "HEX", "PROSE")
    t_doc_rev = document_mean_difference(gains, labels, "PROSE", "HEX")
    assert abs(t_doc + t_doc_rev) < 1e-12  # antisymmetry
    assert t_doc > 0.3  # the constrained regime gains far more from context

    # Token-weighted descriptive variant: same properties.
    t_tok = token_weighted_mean_difference(gains, labels, "HEX", "PROSE")
    t_tok_rev = token_weighted_mean_difference(gains, labels, "PROSE", "HEX")
    assert abs(t_tok + t_tok_rev) < 1e-12

    observed, p = permutation_test_label_free(
        gains, labels, "HEX", "PROSE", n_permutations=500, seed=7
    )
    assert observed == t_doc  # default statistic is the spec form
    assert p < 0.05

    observed_tok, _ = permutation_test_label_free(
        gains, labels, "HEX", "PROSE", n_permutations=50, seed=7,
        statistic="token_weighted",
    )
    assert observed_tok == t_tok


def test_permutation_test_null_case_is_not_significant():
    # Same generator for both nominal groups: no real difference.
    d = 6
    P = [
        [0.45 if j == (i + 1) % d else 0.11 for j in range(d)] for i in range(d)
    ]
    docs = {
        f"doc_{k}": markov_document(P, 20, 16, seed=300 + k) for k in range(10)
    }
    labels = {f"doc_{k}": ("A" if k < 5 else "B") for k in range(10)}
    alph = Alphabet(default_symbols(d))
    pooled = fit_context_tree(list(docs.values()), alph)
    gains = per_document_gain(pooled_document_scores(pooled, docs))
    _, p = permutation_test_label_free(
        gains, labels, "A", "B", n_permutations=500, seed=11
    )
    assert p > 0.05


# --------------------------------------------------------------------- #
# P1 transfer matrix
# --------------------------------------------------------------------- #
def test_transfer_matrix_shape_and_asymmetry():
    docs, labels = _toy_corpus()
    groups = {
        "HEX": [docs[k] for k in docs if labels[k] == "HEX"][:3],
        "PROSE": [docs[k] for k in docs if labels[k] == "PROSE"][:3],
    }
    alph = Alphabet(default_symbols(6))
    tm = transfer_matrix(groups, alph, lodo_diagonal=True)
    assert set(tm.keys()) == {
        ("HEX", "HEX"), ("HEX", "PROSE"), ("PROSE", "HEX"), ("PROSE", "PROSE")
    }
    # The strongly constrained regime is much harder to code under the
    # prose model than under its own (LODO) model.
    assert tm[("HEX", "PROSE")] > tm[("HEX", "HEX")] + 0.3
    # And the prose regime is coded worse by the verse model than by its own.
    assert tm[("PROSE", "HEX")] > tm[("PROSE", "PROSE")] + 0.1


def test_transfer_matrix_lodo_requires_two_documents():
    d = 6
    P = [
        [0.45 if j == (i + 1) % d else 0.11 for j in range(d)] for i in range(d)
    ]
    groups = {
        "A": [markov_document(P, 5, 10, seed=1)],
        "B": [markov_document(P, 5, 10, seed=2), markov_document(P, 5, 10, seed=3)],
    }
    alph = Alphabet(default_symbols(d))
    try:
        transfer_matrix(groups, alph, lodo_diagonal=True)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for single-document LODO group")
