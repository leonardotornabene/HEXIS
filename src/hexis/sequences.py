"""Sequence construction: retained symbols per sentence, boundary policy (Spec §3.5, §3.7; D10).

Signatures per the ratified G0 API contract
(docs/implementation/specs/2026-08-13-g0-api-contract.md); §6.2 assigns none.
"""

from typing import Mapping

import pandas as pd

BOUNDARY_SYMBOL = "#"

# §3.7 sequences.parquet, in declared order. `symbols` holds Python ints in
# memory; the int16 storage type is applied by the parquet writer.
SEQUENCE_COLUMNS = ("language", "doc_id", "sent_ord", "symbols")


def build_sequences(tokens_with_sent_ord: pd.DataFrame) -> pd.DataFrame:
    """Group retained symbols into one row per sentence (§3.5, §3.7).

    Retained symbols only, in `token_ord` order; deletions close gaps (D05).
    A sentence whose tokens are all dropped keeps its row with an empty list, so
    sentence indexing and the P-BOUND boundary count stay faithful to the source.

    `sent_ord` is an input column, never derived here: sorting `sent_id` strings
    would put `…@10` before `…@3` and silently scramble document order. How it is
    computed across the UD split files (which D03 ignores) is settled at G1.
    """
    ordered = tokens_with_sent_ord.sort_values(["doc_id", "sent_ord", "token_ord"])
    rows = []
    for (language, doc_id, sent_ord), group in ordered.groupby(
        ["language", "doc_id", "sent_ord"], sort=True
    ):
        kept = group[group["kept"]]
        rows.append(
            {
                "language": language,
                "doc_id": doc_id,
                "sent_ord": sent_ord,
                "symbols": [int(sid) for sid in kept["symbol_id"]],
            }
        )
    return pd.DataFrame(rows, columns=list(SEQUENCE_COLUMNS))


def extend_alphabet_bound(alphabet: Mapping[str, int]) -> dict[str, int]:
    """Deterministic run-time extension A⁺ = A ∪ {`#`} with `#` at id |A| (D52(x)).

    Returns a new mapping; the frozen alphabet is not mutated and
    `alphabet.json` is never rewritten. |A⁺| = |A| + 1 is what must be used
    wherever |A| enters, including the β = 1/|A| sensitivity cell (§5.6).
    """
    if BOUNDARY_SYMBOL in alphabet:
        raise ValueError(
            f"alphabet already contains {BOUNDARY_SYMBOL!r}: the P-BOUND extension "
            "would collide (D52(x))"
        )
    ids = sorted(alphabet.values())
    if ids != list(range(len(alphabet))):
        raise ValueError(
            f"alphabet ids are not contiguous 0..{len(alphabet) - 1}; "
            f"{BOUNDARY_SYMBOL!r} takes id |A| and would collide (D52(x))"
        )
    return {**alphabet, BOUNDARY_SYMBOL: len(alphabet)}


def alphabet_extension_record(
    alphabet: Mapping[str, int], extended: Mapping[str, int]
) -> dict:
    """The run-manifest record of the run-time extension (D52(x), §6.4/D46)."""
    return {
        "base_size": len(alphabet),
        "added_symbols": {
            symbol: sid for symbol, sid in extended.items() if symbol not in alphabet
        },
        "runtime_size": len(extended),
    }


def to_model_input(
    sequences: pd.DataFrame,
    *,
    doc_id: str,
    boundary: str,
    boundary_id: int | None = None,
) -> list[list[int]]:
    """One document's sequences in the form `ContextTree.fit(sent_seqs)` accepts (§6.2).

    P-RESET (primary, D10): one sequence per sentence — contexts truncate at
    sentence start, no cross-sentence statistics. P-BOUND (sensitivity): a single
    stream per document with exactly `n_sentences - 1` boundary symbols and no
    reset.

    `doc_id` is required and keyword-only, so "blocks never span documents"
    (§3.6) holds structurally rather than by convention.
    """
    if boundary not in ("reset", "bound"):
        raise ValueError(f"boundary policy {boundary!r} is not 'reset' or 'bound' (§3.5)")
    if boundary == "bound" and boundary_id is None:
        raise ValueError("P-BOUND requires boundary_id = |A| from extend_alphabet_bound (D52(x))")
    if boundary == "reset" and boundary_id is not None:
        raise ValueError("P-RESET takes no boundary_id: no boundary symbol is inserted (D10)")

    doc = sequences[sequences["doc_id"] == doc_id].sort_values("sent_ord")
    if doc.empty:
        raise ValueError(f"no sequences for doc_id {doc_id!r}")

    sentence_symbols = [list(row) for row in doc["symbols"]]
    if boundary == "reset":
        return sentence_symbols

    stream: list[int] = []
    for position, symbols in enumerate(sentence_symbols):
        if position:
            stream.append(boundary_id)
        stream.extend(symbols)
    return [stream]
