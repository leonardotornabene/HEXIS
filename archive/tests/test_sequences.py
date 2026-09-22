"""Sequence construction tests (Spec §7, gate G0; §3.5, §3.7; D10, D52(x)).

Both boundary policies are mandatory G0 coverage (D52(ii)). Signatures per the
ratified G0 API contract
(docs/implementation/specs/2026-08-13-g0-api-contract.md).
"""

import pandas as pd
import pytest

from hexis import manifest, sequences

pytestmark = pytest.mark.g0

BOUNDARY = "#"


def tokens_frame(rows):
    """rows: (doc_id, sent_ord, token_ord, symbol_id, kept)"""
    frame = pd.DataFrame(
        rows, columns=["doc_id", "sent_ord", "token_ord", "symbol_id", "kept"]
    ).assign(language="grc")
    return frame.assign(
        sent_id=frame["doc_id"].astype(str) + "@" + frame["sent_ord"].astype(str)
    )


# doc A: two sentences; the second has a dropped token in the middle (gap closes).
# doc B: one all-dropped sentence between two normal ones.
TOKENS = tokens_frame(
    [
        ("A", 0, 0, 5, True),
        ("A", 0, 1, 3, True),
        ("A", 1, 0, 7, True),
        ("A", 1, 1, -1, False),
        ("A", 1, 2, 2, True),
        ("B", 0, 0, 1, True),
        ("B", 1, 0, -1, False),
        ("B", 2, 0, 4, True),
    ]
)

# Ids 0..7 so that |A| = 8 is a boundary id distinct from every symbol id used
# above; a collision would make the boundary counts below untestable.
ALPHABET = {
    f"UPOS{i}:deprel{i}": i for i in range(8)
}
BOUNDARY_ID = len(ALPHABET)


# --- build_sequences (§3.7) ------------------------------------------------------


def test_build_sequences_keeps_retained_symbols_in_token_order():
    """Deletions close gaps (D05): the dropped token leaves no hole."""
    seqs = sequences.build_sequences(TOKENS)
    by_key = seqs.set_index(["doc_id", "sent_ord"])["symbols"]
    assert by_key[("A", 0)] == [5, 3]
    assert by_key[("A", 1)] == [7, 2]


def test_all_dropped_sentence_remains_an_empty_row():
    """The row survives with symbols == [] — it is not silently deleted, so
    sentence indexing and the P-BOUND boundary count stay faithful."""
    seqs = sequences.build_sequences(TOKENS)
    assert seqs.set_index(["doc_id", "sent_ord"])["symbols"][("B", 1)] == []
    assert len(seqs) == 5


def test_build_sequences_schema_and_deterministic_order():
    seqs = sequences.build_sequences(TOKENS)
    assert list(seqs.columns) == list(sequences.SEQUENCE_COLUMNS)
    assert list(zip(seqs["doc_id"], seqs["sent_ord"])) == [
        ("A", 0), ("A", 1), ("B", 0), ("B", 1), ("B", 2)
    ]


def test_sequences_never_carry_the_boundary_symbol():
    """sequences.parquet is always sentence-based and never contains `#`; P-BOUND
    is produced at run time (D52(x))."""
    seqs = sequences.build_sequences(TOKENS)
    ids = [sid for row in seqs["symbols"] for sid in row]
    assert len(ids) == 6
    assert max(ids) < len(ALPHABET)  # only real symbol ids, never the appended boundary


def test_token_order_is_honoured_not_row_order():
    shuffled = TOKENS.sample(frac=1.0, random_state=0)
    assert sequences.build_sequences(shuffled).equals(sequences.build_sequences(TOKENS))
    assert sequences.build_sequences(shuffled)["symbols"].iloc[0] == [5, 3]


# --- extend_alphabet_bound (D52(x)) ----------------------------------------------


def test_extend_alphabet_bound_appends_at_size_and_keeps_ids_stable():
    extended = sequences.extend_alphabet_bound(ALPHABET)
    assert extended[BOUNDARY] == len(ALPHABET)
    assert all(extended[symbol] == sid for symbol, sid in ALPHABET.items())
    assert len(extended) == len(ALPHABET) + 1


def test_extend_alphabet_bound_does_not_mutate_the_frozen_alphabet():
    """alphabet.json is never rewritten (D52(x))."""
    before = dict(ALPHABET)
    sequences.extend_alphabet_bound(ALPHABET)
    assert ALPHABET == before


def test_extend_alphabet_bound_rejects_an_alphabet_already_carrying_the_boundary():
    with pytest.raises(ValueError) as exc:
        sequences.extend_alphabet_bound({**ALPHABET, BOUNDARY: len(ALPHABET)})
    assert BOUNDARY in str(exc.value)


def test_extend_alphabet_bound_rejects_non_contiguous_ids():
    """`#` takes id |A|; if the ids are not 0..|A|-1 that id would collide."""
    with pytest.raises(ValueError) as exc:
        sequences.extend_alphabet_bound({"NOUN:root": 0, "VERB:root": 7})
    assert "contiguous" in str(exc.value)


# --- to_model_input: both boundary policies (§3.5, D10) --------------------------


def test_p_reset_returns_one_sequence_per_sentence():
    """Contexts truncate at sentence start: no cross-sentence past (D10)."""
    seqs = sequences.build_sequences(TOKENS)
    assert sequences.to_model_input(seqs, doc_id="A", boundary="reset") == [[5, 3], [7, 2]]


def test_p_bound_returns_one_stream_with_exactly_n_minus_one_boundaries():
    seqs = sequences.build_sequences(TOKENS)
    stream = sequences.to_model_input(
        seqs, doc_id="A", boundary="bound", boundary_id=BOUNDARY_ID
    )
    assert stream == [[5, 3, BOUNDARY_ID, 7, 2]]
    assert stream[0].count(BOUNDARY_ID) == 1  # n_sentences - 1


def test_p_bound_produces_adjacent_boundaries_around_an_all_dropped_sentence():
    """Correct and deliberately not special-cased: the empty sentence still
    contributes its separators."""
    seqs = sequences.build_sequences(TOKENS)
    stream = sequences.to_model_input(
        seqs, doc_id="B", boundary="bound", boundary_id=BOUNDARY_ID
    )
    assert stream == [[1, BOUNDARY_ID, BOUNDARY_ID, 4]]
    assert stream[0].count(BOUNDARY_ID) == 2


def test_single_sentence_document_has_no_boundary():
    seqs = sequences.build_sequences(tokens_frame([("C", 0, 0, 1, True)]))
    assert sequences.to_model_input(
        seqs, doc_id="C", boundary="bound", boundary_id=BOUNDARY_ID
    ) == [[1]]


def test_to_model_input_never_spans_documents():
    """doc_id is required and keyword-only, so the constraint is structural."""
    seqs = sequences.build_sequences(TOKENS)
    every = [
        sid
        for doc in ("A", "B")
        for stream in sequences.to_model_input(seqs, doc_id=doc, boundary="reset")
        for sid in stream
    ]
    assert every == [5, 3, 7, 2, 1, 4]


def test_unknown_doc_id_raises():
    seqs = sequences.build_sequences(TOKENS)
    with pytest.raises(ValueError) as exc:
        sequences.to_model_input(seqs, doc_id="Z", boundary="reset")
    assert "Z" in str(exc.value)


def test_unknown_boundary_policy_raises():
    seqs = sequences.build_sequences(TOKENS)
    with pytest.raises(ValueError) as exc:
        sequences.to_model_input(seqs, doc_id="A", boundary="concat")
    assert "concat" in str(exc.value)


def test_p_bound_without_boundary_id_raises():
    seqs = sequences.build_sequences(TOKENS)
    with pytest.raises(ValueError) as exc:
        sequences.to_model_input(seqs, doc_id="A", boundary="bound")
    assert "boundary_id" in str(exc.value)


def test_p_reset_with_boundary_id_raises():
    """A boundary id under P-RESET signals a mixed-up run configuration."""
    seqs = sequences.build_sequences(TOKENS)
    with pytest.raises(ValueError) as exc:
        sequences.to_model_input(seqs, doc_id="A", boundary="reset", boundary_id=9)
    assert "boundary_id" in str(exc.value)


# --- the extension is recorded in the run manifest (D52(x), §7 test_sequences row) ---


def test_manifest_records_the_runtime_alphabet_extension():
    extended = sequences.extend_alphabet_bound(ALPHABET)
    record = manifest.build_manifest(
        "run-x",
        "0" * 64,
        seed=1,
        artifacts=(),
        entry_point="pipeline.run_encode",
        alphabet_extension=sequences.alphabet_extension_record(ALPHABET, extended),
    )
    assert record["alphabet_extension"] == {
        "base_size": 8,
        "added_symbols": {BOUNDARY: 8},
        "runtime_size": 9,
    }


def test_manifest_omits_the_key_for_p_reset_runs():
    record = manifest.build_manifest(
        "run-y", "0" * 64, seed=1, artifacts=(), entry_point="pipeline.run_encode"
    )
    assert "alphabet_extension" not in record
