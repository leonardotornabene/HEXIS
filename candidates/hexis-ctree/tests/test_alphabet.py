"""Alphabet: fixed ex ante, deterministic, fail-loud on unseen symbols."""

from hexis_ctree import Alphabet


def test_alphabet_is_sorted_and_deterministic():
    a1 = Alphabet(["NOUN+nsubj", "VERB+root", "ADJ+amod"])
    a2 = Alphabet(["VERB+root", "ADJ+amod", "NOUN+nsubj"])  # different order
    assert a1.symbols == a2.symbols == ("ADJ+amod", "NOUN+nsubj", "VERB+root")
    assert a1.id_of("NOUN+nsubj") == a2.id_of("NOUN+nsubj")


def test_from_documents_collects_all_symbols():
    docs = [[["a", "b"], ["c"]], [["b", "d"]]]
    alph = Alphabet.from_documents(docs)
    assert alph.symbols == ("a", "b", "c", "d")
    assert len(alph) == 4


def test_unknown_symbol_raises():
    alph = Alphabet(["a", "b"])
    try:
        alph.encode_sentence(["a", "z"])
    except ValueError as e:
        assert "z" in str(e)
    else:
        raise AssertionError("expected ValueError for out-of-alphabet symbol")


def test_empty_sentence_raises():
    alph = Alphabet(["a", "b"])
    try:
        alph.encode_sentence([])
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for empty sentence")


def test_alphabet_requires_two_symbols():
    for bad in ([], ["only"]):
        try:
            Alphabet(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for degenerate alphabet")
