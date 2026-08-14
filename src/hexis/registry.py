"""Document registry: doc_id derivation and regime assignment (Spec §2.3, §3.3; D03, D04).

Signatures per the ratified G0 API contract
(docs/implementation/specs/2026-08-13-g0-api-contract.md).
"""

from collections import Counter
from typing import Iterable, Mapping

import pandas as pd

REGIME_LABELS = frozenset(
    {"HEX", "PROSE_CLASS", "PROSE_POST", "OTHER_VERSE", "EXCLUDED"}
)

# Per-document schema of Spec §2.3, in declared order.
REGISTRY_COLUMNS = (
    "language",
    "doc_id",
    "source_urn",
    "author",
    "work",
    "regime",
    "meter",
    "period",
    "n_sentences",
    "n_tokens_raw",
    "n_tokens_retained",
    "flags",
)

REQUIRED_OVERRIDE_FIELDS = ("author", "work", "regime", "meter", "period")
MERGE_METADATA_FIELDS = (
    "language",
    "source_urn",
    *REQUIRED_OVERRIDE_FIELDS,
    "flags",
)

PREFIX_COLUMNS = ("language", "doc_id", "n_sentences", "n_tokens_raw")

_SEPARATOR = "@"


def doc_id_from_sent_id(sent_id: str) -> str:
    """`sent_id` is `<newdoc id>@<ordinal>` in both treebanks (verified 2026-08-13):
    `doc_id` is everything before the last separator (D03, §3.3)."""
    if _SEPARATOR not in sent_id:
        raise ValueError(
            f"sent_id {sent_id!r} has no {_SEPARATOR!r} separator: cannot derive doc_id "
            "(Spec §3.3, D03)"
        )
    return sent_id.rsplit(_SEPARATOR, 1)[0]


def enumerate_prefixes(sentences: Iterable, *, language: str) -> pd.DataFrame:
    """Aggregate sentence and raw-token counts per derived `doc_id` (§3.3).

    `n_tokens_raw` counts integer-ID syntactic words yielded by the D54 reader,
    before alphabet retention; MWT ranges and empty nodes are already absent
    (owner-ratified G0 API reading, 2026-08-14).

    Streams over the reader's sentences. UD splits are ignored (D03), so one
    document's sentences arrive across several files with non-contiguous
    ordinals; the aggregation is by `doc_id` alone and never by file or by
    ordinal contiguity. Where `newdoc id` is present it must agree with the
    derived prefix.
    """
    n_sentences: Counter = Counter()
    n_tokens: Counter = Counter()

    for sentence in sentences:
        sent_id = sentence.metadata["sent_id"]
        doc_id = doc_id_from_sent_id(sent_id)
        declared = sentence.metadata.get("newdoc id")
        if declared is not None and declared != doc_id:
            raise ValueError(
                f"newdoc id {declared!r} contradicts the doc_id {doc_id!r} derived from "
                f"sent_id {sent_id!r}: document identity is ambiguous (Spec §3.3)"
            )
        n_sentences[doc_id] += 1
        n_tokens[doc_id] += len(sentence)

    return pd.DataFrame(
        [
            {
                "language": language,
                "doc_id": doc_id,
                "n_sentences": n_sentences[doc_id],
                "n_tokens_raw": n_tokens[doc_id],
            }
            for doc_id in sorted(n_sentences)
        ],
        columns=list(PREFIX_COLUMNS),
    )


def build_registry(prefix_counts: pd.DataFrame, overrides: Mapping) -> pd.DataFrame:
    """Build the document registry from enumerated prefixes + human-verified overrides.

    Fails loud on any document without an assignment (the G1 audit fails on any
    unassigned sentence, §3.3) and on any override naming a document absent from
    the corpus (a stale registry). Nothing here may be guessed.

    `n_tokens_retained` stays null until the alphabet is frozen at G1 (§3.4); it
    must be complete before the G1 freeze.

    An optional nonempty `canonical_doc_id` in each raw-prefix assignment merges
    prefixes into one registry row. Counts are summed; traceability metadata must
    agree exactly across the group (owner-ratified G0 API reading, 2026-08-14).
    """
    present = set(prefix_counts["doc_id"])
    unassigned = sorted(present - set(overrides))
    if unassigned:
        raise ValueError(
            f"no registry assignment for {unassigned}: populate "
            "config/registry_overrides.yaml (Spec §3.3, D04)"
        )
    unknown = sorted(set(overrides) - present)
    if unknown:
        raise ValueError(
            f"registry overrides name documents absent from the corpus: {unknown}"
        )

    rows_by_doc_id = {}
    first_raw_prefix_by_doc_id = {}
    for record in prefix_counts.to_dict("records"):
        raw_doc_id = record["doc_id"]
        assignment = overrides[raw_doc_id]
        missing = [f for f in REQUIRED_OVERRIDE_FIELDS if f not in assignment]
        if missing:
            raise ValueError(f"registry assignment for {raw_doc_id} is missing {missing}")
        if assignment["regime"] not in REGIME_LABELS:
            raise ValueError(
                f"regime {assignment['regime']!r} for {raw_doc_id} is not one of the five "
                f"labels of D04: {sorted(REGIME_LABELS)}"
            )
        canonical_doc_id = assignment.get("canonical_doc_id", raw_doc_id)
        if not isinstance(canonical_doc_id, str) or not canonical_doc_id.strip():
            raise ValueError(
                f"canonical_doc_id for raw prefix {raw_doc_id!r} must be a "
                "nonempty string"
            )
        metadata = {
            "language": record["language"],
            "source_urn": assignment.get("source_urn", raw_doc_id),
            **{field: assignment[field] for field in REQUIRED_OVERRIDE_FIELDS},
            "flags": assignment.get("flags", []),
        }
        if canonical_doc_id not in rows_by_doc_id:
            first_raw_prefix_by_doc_id[canonical_doc_id] = raw_doc_id
            rows_by_doc_id[canonical_doc_id] = {
                **metadata,
                "doc_id": canonical_doc_id,
                "n_sentences": 0,
                "n_tokens_raw": 0,
                "n_tokens_retained": pd.NA,
            }
        else:
            existing = rows_by_doc_id[canonical_doc_id]
            for field in MERGE_METADATA_FIELDS:
                if existing[field] != metadata[field]:
                    raise ValueError(
                        f"conflicting {field} for raw prefixes "
                        f"{first_raw_prefix_by_doc_id[canonical_doc_id]!r} and "
                        f"{raw_doc_id!r} merged into canonical doc_id "
                        f"{canonical_doc_id!r}"
                    )
        rows_by_doc_id[canonical_doc_id]["n_sentences"] += record["n_sentences"]
        rows_by_doc_id[canonical_doc_id]["n_tokens_raw"] += record["n_tokens_raw"]

    rows = [rows_by_doc_id[doc_id] for doc_id in sorted(rows_by_doc_id)]
    frame = pd.DataFrame(rows, columns=list(REGISTRY_COLUMNS))
    frame["n_tokens_retained"] = frame["n_tokens_retained"].astype("Int64")
    return frame
