"""Mechanics of the context tree, checked against hand-computed examples
and against the exact formulas of Schuermann & Grassberger (1996)."""

import math
import pickle

from hexis_ctree import Alphabet, ContextTreeConfig, ContextTreeModel


def _model(symbols, **cfg):
    return ContextTreeModel(Alphabet(symbols), ContextTreeConfig(**cfg))


# --------------------------------------------------------------------- #
# S&G Eq. (21) and Eq. (30)
# --------------------------------------------------------------------- #
def test_probabilities_match_eq21_and_sum_to_one():
    m = _model(list("abcd"), beta=0.5)  # Krichevsky-Trofimov
    m.fit([[list("aabca")]])
    root = m.root
    d = 4
    beta = 0.5
    for sym_id in range(d):
        k = root.counts.get(sym_id, 0)
        expected = (k + beta) / (root.total + beta * d)
        got = 2.0 ** m._log2_prob(root, sym_id)
        assert abs(got - expected) < 1e-12
    total_p = sum(2.0 ** m._log2_prob(root, s) for s in range(d))
    assert abs(total_p - 1.0) < 1e-12


def test_default_config_is_frozen_hexis_c0():
    cfg = ContextTreeConfig()
    assert cfg == ContextTreeConfig.hexis_c0()
    assert cfg.beta == 0.5          # D18: add-beta, KT-style
    assert cfg.k_min == 2           # D18
    assert cfg.delta_threshold == 0.0  # D18: gamma = 0
    assert cfg.max_depth == 8       # D18: d_max = 8
    assert cfg.growth == "eager"    # Spec 4.1 pseudocode: grow on first visit
    # Latin arm: same C0 values with d_max = 6 (D24).
    assert ContextTreeConfig.hexis_c0(max_depth=6).max_depth == 6


def test_sg96_preset_beta_is_one_over_d_eq30():
    cfg = ContextTreeConfig.sg96_published()
    assert cfg.beta is None and cfg.k_min == 1 and cfg.growth == "rissanen"
    m = ContextTreeModel(Alphabet(list("abcdef")), cfg)  # beta=None -> 1/d
    assert abs(m.beta - 1.0 / 6.0) < 1e-15
    # Eq. (30) closed form: p_hat = (k + 1/d) / (n + 1)
    m.fit([[list("abacab")]])
    root = m.root
    a_id = m.alphabet.id_of("a")
    k = root.counts[a_id]
    n = root.total
    assert abs(2.0 ** m._log2_prob(root, a_id) - (k + 1.0 / 6.0) / (n + 1.0)) < 1e-12
    # On an empty model the root prediction is uniform: p = 1/d.
    fresh = ContextTreeModel(Alphabet(list("abcdef")), cfg)
    assert abs(2.0 ** fresh._log2_prob(fresh.root, 0) - 1.0 / 6.0) < 1e-15


# --------------------------------------------------------------------- #
# Rissanen growth rule (S&G Sec. IV), hand-traced on "a b a b"
# --------------------------------------------------------------------- #
def test_rissanen_growth_rule_hand_example():
    m = _model(["a", "b"], growth="rissanen")
    m.fit([[["a", "b", "a", "b"]]])
    a, b = m.alphabet.id_of("a"), m.alphabet.id_of("b")
    root = m.root
    # Root saw every token.
    assert root.counts == {a: 2, b: 2} and root.total == 4
    # Children are created only when the (deepest matched, symbol) count
    # reaches 2: at t=2 (s='a', root count of 'a' becomes 2) the child for
    # previous symbol 'b' is created with counts {'a': 1}; at t=3 (s='b')
    # the child for previous symbol 'a' is created with counts {'b': 1}.
    assert set(root.children.keys()) == {a, b}
    assert root.children[b].counts == {a: 1} and root.children[b].total == 1
    assert root.children[a].counts == {b: 1} and root.children[a].total == 1
    assert m.node_count() == 3


def test_eager_growth_creates_on_first_occurrence():
    m = _model(["a", "b"], growth="eager")
    m.fit([[["a", "b"]]])
    a = m.alphabet.id_of("a")
    b = m.alphabet.id_of("b")
    # At t=1 (s='b', past=['a']) the eager policy creates the depth-1 node
    # for previous symbol 'a' immediately.
    assert set(m.root.children.keys()) == {a}
    assert m.root.children[a].counts == {b: 1}


def test_max_depth_is_respected():
    m = _model(["a", "b"], max_depth=2, growth="eager")
    m.fit([[list("abababababababab")]])

    def max_depth(node):
        if not node.children:
            return node.depth
        return max(max_depth(c) for c in node.children.values())

    assert max_depth(m.root) <= 2


# --------------------------------------------------------------------- #
# Delta semantics (S&G Eqs. (22)-(24))
# --------------------------------------------------------------------- #
def test_delta_negative_for_genuinely_informative_context():
    # Deterministic alternation: the depth-1 contexts are maximally
    # informative, so their accumulated code-length difference vs the root
    # must be strongly negative (child codes better).
    m = _model(["a", "b"])
    m.fit([[list("ab" * 200)]])
    a, b = m.alphabet.id_of("a"), m.alphabet.id_of("b")
    assert m.root.children[a].delta < -10.0
    assert m.root.children[b].delta < -10.0


def test_delta_update_is_prequential_first_visit_is_neutral_in_expectation():
    # A freshly created node starts with delta == 0 by construction.
    m = _model(["a", "b"])
    m.fit([[["a", "b", "a"]]])  # creates child for context 'b' at t=2
    b = m.alphabet.id_of("b")
    assert m.root.children[b].delta == 0.0


def test_k_min_gates_selection_hand_example():
    # Fit "a b a b" under C0-eager growth, beta = 0.5, d = 2. Hand trace:
    # the depth-1 node for context 'a' receives exactly one prequential
    # update, at t=3 (s='b'): pre-update p_root(b) = 1.5/4 = 0.375 and
    # p_node(b) = 1.5/2 = 0.75, so delta = log2(0.375) - log2(0.75) = -1.0
    # exactly, and its final training count is total = 2.
    doc = [["a", "b", "a", "b"]]
    for k_min, expected_depth in ((2, 1), (3, 0)):
        m = _model(["a", "b"], k_min=k_min)
        m.fit([doc]).freeze()
        child = m.root.children[m.alphabet.id_of("a")]
        assert abs(child.delta - (-1.0)) < 1e-12 and child.total == 2
        s = m.score_document(doc).sentences[0]
        # Position 1 (symbol 'b', past ['a']): the node saves bits
        # (delta < 0) but is selectable only if total >= k_min.
        assert s.selected_depth[1] == expected_depth
        assert s.matched_depth[1] == 1  # the node exists in both cases


# --------------------------------------------------------------------- #
# Sentence-level hard reset (locked HEXIS decision)
# --------------------------------------------------------------------- #
def test_context_never_crosses_sentence_boundary():
    # Two sentences with disjoint bigram structure. If contexts leaked
    # across the boundary, a context node keyed by 'b' would acquire counts
    # for 'c' (the first symbol of the second sentence).
    m = _model(list("abcd"), growth="eager")
    m.fit([[list("abab"), list("cdcd")]])
    b, c = m.alphabet.id_of("b"), m.alphabet.id_of("c")
    node_after_b = m.root.children.get(b)
    assert node_after_b is not None
    assert c not in node_after_b.counts  # no cross-boundary evidence
    # And scoring: the first position of every sentence has depth 0 and
    # available_past 0.
    scores = m.score_document([list("abab"), list("cdcd")])
    for s in scores.sentences:
        assert s.selected_depth[0] == 0
        assert s.matched_depth[0] == 0
        assert s.available_past[0] == 0
        assert s.available_past == tuple(range(len(s)))
        # Structural invariants of the per-position record (Spec 4.3):
        assert all(
            sel <= mat <= avail
            for sel, mat, avail in zip(
                s.selected_depth, s.matched_depth, s.available_past
            )
        )


# --------------------------------------------------------------------- #
# Frozen evaluation purity and lifecycle
# --------------------------------------------------------------------- #
def test_scoring_never_mutates_the_model():
    m = _model(list("ab"))
    m.fit([[list("abab" * 10)]]).freeze()
    before = pickle.dumps(
        (m.root.counts, m.root.total, m.node_count(), m.n_tokens_trained,
         m._online_codelen_sum_bits)
    )
    _ = m.score_document([list("abba"), list("aaab")])
    _ = m.cross_entropy([[list("abab")]])
    after = pickle.dumps(
        (m.root.counts, m.root.total, m.node_count(), m.n_tokens_trained,
         m._online_codelen_sum_bits)
    )
    assert before == after


def test_fit_after_freeze_raises():
    m = _model(["a", "b"])
    m.fit([[["a", "b"]]]).freeze()
    try:
        m.fit([[["a", "b"]]])
    except RuntimeError:
        pass
    else:
        raise AssertionError("expected RuntimeError after freeze")


def test_fit_is_deterministic():
    doc = [list("abbaba"), list("babab")]
    m1 = _model(["a", "b"]).fit([doc])
    m2 = _model(["a", "b"]).fit([doc])
    assert m1.online_entropy_rate == m2.online_entropy_rate
    assert m1.node_count() == m2.node_count()


def test_save_load_roundtrip(tmp_path=None):
    import os
    import tempfile

    m = _model(["a", "b"]).fit([[list("ababab")]]).freeze()
    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "model.pkl")
        m.save(path)
        m2 = ContextTreeModel.load(path)
    assert m2.online_entropy_rate == m.online_entropy_rate
    assert m2.node_count() == m.node_count()
    assert m2.summary()["config"] == m.summary()["config"]
