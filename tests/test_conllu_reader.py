"""CoNLL-U reader tests (Spec §7, gate G0; §3.2; D54).

RED-only in the overnight run: these encode the D54(ii)-(iv) contract before
`conllu_reader.iter_sentences` / `ParseError` exist, so they must FAIL. The
implementation is deliberately deferred (owner's RED checkpoint).

Beyond the §7 minimum (malformed→ParseError; sent_id required; ID order), the
last three are declared additions permitted by "edge cases throughout":
MWT/empty-node removal, PUNCT passthrough, and newdoc-id recovery.
"""

import pytest

from hexis import conllu_reader


# --- the three §7 cases ---------------------------------------------------------


@pytest.mark.g0
def test_malformed_row_raises_parse_error_with_location(conllu_samples):
    with pytest.raises(conllu_reader.ParseError) as exc:
        list(conllu_reader.iter_sentences(conllu_samples["malformed"]))
    err = exc.value
    assert err.path == conllu_samples["malformed"]
    assert err.sent_id == "gamma@1"
    assert err.token_id == 2
    assert err.reason  # populated, non-empty


@pytest.mark.g0
def test_missing_sent_id_raises_parse_error(conllu_samples):
    with pytest.raises(conllu_reader.ParseError) as exc:
        list(conllu_reader.iter_sentences(conllu_samples["missing_sent_id"]))
    assert exc.value.sent_id is None  # violation precedes sent_id availability (D54 iv)


@pytest.mark.g0
def test_id_order_preserved(conllu_samples):
    sentences = list(conllu_reader.iter_sentences(conllu_samples["valid"]))
    first = sentences[0]
    assert [tok["id"] for tok in first] == [1, 2, 3, 4]  # surface CoNLL-U ID order


# --- declared additions (edge cases) --------------------------------------------


@pytest.mark.g0
def test_mwt_range_and_empty_nodes_removed(conllu_samples):
    first = next(iter(conllu_reader.iter_sentences(conllu_samples["valid"])))
    assert all(isinstance(tok["id"], int) for tok in first)  # no (i,'-',j) / (i,'.',k)
    assert len(first) == 4


@pytest.mark.g0
def test_punct_token_yielded_unchanged(conllu_samples):
    first = next(iter(conllu_reader.iter_sentences(conllu_samples["valid"])))
    puncts = [tok for tok in first if tok["upos"] == "PUNCT"]
    assert len(puncts) == 1 and puncts[0]["form"] == "."  # representation blindness (D54 iii)


@pytest.mark.g0
def test_newdoc_id_recoverable_from_metadata(conllu_samples):
    first = next(iter(conllu_reader.iter_sentences(conllu_samples["valid"])))
    assert first.metadata["newdoc id"] == "alpha"  # key pinned by the probe
