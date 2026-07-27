"""CoNLL-U reader tests (Spec §7, gate G0; §3.2; D54).

RED-only in the overnight run: these encode the D54(ii)-(iv) contract before
`conllu_reader.iter_sentences` / `ParseError` exist, so they must FAIL. The
implementation is deliberately deferred (owner's RED checkpoint).

Beyond the §7 minimum (malformed→ParseError; sent_id required; ID order), the
last three are declared additions permitted by "edge cases throughout":
MWT/empty-node removal, PUNCT passthrough, and newdoc-id recovery.
"""

import pytest
from conllu import TokenList

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
    assert isinstance(err, ValueError)
    rendered = str(err)
    values = (str(err.path), err.sent_id, "2", err.reason)
    assert all(value in rendered for value in values)
    assert "\n" not in rendered


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
    assert first.metadata["sent_id"] == "alpha@1"


@pytest.mark.g0
def test_public_type_and_streaming_failure_boundary(conllu_samples):
    sentences = conllu_reader.iter_sentences(conllu_samples["lazy"])
    assert iter(sentences) is sentences
    first = next(sentences)
    assert isinstance(first, TokenList)
    assert first.metadata["sent_id"] == "theta@1"
    with pytest.raises(conllu_reader.ParseError) as exc:
        next(sentences)
    assert exc.value.path == conllu_samples["lazy"]


@pytest.mark.g0
@pytest.mark.parametrize("sample", ["invalid_upos", "empty_deprel"])
def test_invalid_required_labels_raise_parse_error(conllu_samples, sample):
    with pytest.raises(conllu_reader.ParseError) as exc:
        list(conllu_reader.iter_sentences(conllu_samples[sample]))
    assert exc.value.path == conllu_samples[sample]
    assert exc.value.token_id == 1
    assert exc.value.reason


@pytest.mark.g0
def test_conllu_parse_exception_is_wrapped(conllu_samples):
    with pytest.raises(conllu_reader.ParseError) as exc:
        list(conllu_reader.iter_sentences(conllu_samples["invalid_id"]))
    assert exc.value.path == conllu_samples["invalid_id"]
    assert exc.value.reason


@pytest.mark.g0
def test_representation_exclusions_are_yielded_unchanged(conllu_samples):
    sentence = next(
        iter(conllu_reader.iter_sentences(conllu_samples["representation_blind"]))
    )
    assert [(token["upos"], token["deprel"]) for token in sentence] == [
        ("PUNCT", "punct"),
        ("X", "discourse"),
        ("INTJ", "vocative"),
        ("SYM", "dep"),
    ]
