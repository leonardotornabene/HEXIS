"""G1 guards on document identity in sequence construction (Spec §3.5, §3.7; D10).

Marked `g1`, never `g0`: `tests/test_sequences.py` carries a module-level `g0`
marker, so anything added there would silently join the attested 144-test G0
selection. Canonical command: `uv run pytest -m g1 --strict-markers`.

`sequences.parquet` is keyed `(language, doc_id, sent_ord)`, but `to_model_input`
filtered on `doc_id` alone. The signature is fixed by the ratified G0 API
contract, so the ambiguity is *refused* here rather than resolved by a new
parameter: a doc_id shared by two languages is a registry error, not a call the
model should silently service.

`pytest.raises` executes no Python `assert`, and the repo-root conftest fails any
gated test that runs none — hence the `as caught` idiom throughout.

Never delete or weaken a test to make it pass.
"""

import pandas as pd
import pytest

from hexis import sequences

pytestmark = pytest.mark.g1


def _sequences(rows):
    return pd.DataFrame(rows, columns=list(sequences.SEQUENCE_COLUMNS))


def test_a_doc_id_shared_by_two_languages_is_refused():
    """Filtering on doc_id alone pools two languages into one model input and then
    interleaves them by sent_ord — a cross-language fit nothing downstream could
    detect, since the result is a well-formed list of symbol lists."""
    frame = _sequences(
        [
            {"language": "grc", "doc_id": "shared", "sent_ord": 1, "symbols": [0, 1]},
            {"language": "la", "doc_id": "shared", "sent_ord": 1, "symbols": [2, 3]},
        ]
    )

    with pytest.raises(ValueError) as caught:
        sequences.to_model_input(frame, doc_id="shared", boundary="reset")

    assert "language" in str(caught.value)


def test_a_repeated_sent_ord_within_one_document_is_refused():
    """`sent_ord` is the sentence index within the document (§3.7): two rows
    sharing one means the order is undefined and a sentence is duplicated."""
    frame = _sequences(
        [
            {"language": "grc", "doc_id": "alpha", "sent_ord": 1, "symbols": [0]},
            {"language": "grc", "doc_id": "alpha", "sent_ord": 1, "symbols": [1]},
        ]
    )

    with pytest.raises(ValueError) as caught:
        sequences.to_model_input(frame, doc_id="alpha", boundary="reset")

    assert "sent_ord" in str(caught.value)


def test_two_sentences_colliding_on_one_sent_ord_are_refused_at_construction():
    """The guard above is the second belt, and on its own it was unreachable.

    `build_sequences` groups by `(language, doc_id, sent_ord)` and emits one row
    per key, so two sentences sharing a `sent_ord` are fused — their symbols
    interleaved by `token_ord` — *before* `to_model_input` could see two rows. The
    frame it returns can never trip the downstream check. `sent_ord` derivation
    across the pooled UD split files is settled at checklist item 13, which is
    exactly when this collision becomes reachable on real data.
    """
    tokens = pd.DataFrame(
        [
            # two distinct sentences, both numbered sent_ord 7 in doc alpha
            {"language": "grc", "doc_id": "alpha", "sent_ord": 7, "token_ord": 0,
             "symbol_id": 5, "kept": True},
            {"language": "grc", "doc_id": "alpha", "sent_ord": 7, "token_ord": 0,
             "symbol_id": 9, "kept": True},
        ]
    )

    with pytest.raises(ValueError) as caught:
        sequences.build_sequences(tokens)

    assert "sent_ord" in str(caught.value)
    assert "alpha" in str(caught.value)


def test_a_single_language_document_still_converts():
    """The guards must not disturb the ordinary case: one language, gappy
    ordinals, sorted by sent_ord and not by row order."""
    frame = _sequences(
        [
            {"language": "grc", "doc_id": "alpha", "sent_ord": 7, "symbols": [3]},
            {"language": "grc", "doc_id": "alpha", "sent_ord": 2, "symbols": [0, 1]},
        ]
    )

    assert sequences.to_model_input(frame, doc_id="alpha", boundary="reset") == [
        [0, 1],
        [3],
    ]
