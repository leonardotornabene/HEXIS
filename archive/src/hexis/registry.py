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

# Every field an assignment may carry. Beyond the required five, `source_urn`,
# `flags` and `canonical_doc_id` are read here; `part_order` is declared in the G1
# ratification package (§viii) and read by nothing yet. It is listed so that
# accepting it is a decision on record rather than the silence of a missing check:
# without the list, a mistyped optional key (`flag:` for `flags:`, `urn:` for
# `source_urn:`) is dropped without a trace and shows up in no artifact.
KNOWN_OVERRIDE_FIELDS = frozenset(
    REQUIRED_OVERRIDE_FIELDS + ("source_urn", "flags", "canonical_doc_id", "part_order")
)

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
    derived prefix, and a `sent_id` repeated in the stream aborts: pooled splits
    make it one sentence counted twice, not a duplicate row to drop.
    """
    n_sentences: Counter = Counter()
    n_tokens: Counter = Counter()
    seen_sent_ids: set[str] = set()

    for sentence in sentences:
        sent_id = sentence.metadata["sent_id"]
        if sent_id in seen_sent_ids:
            raise ValueError(
                f"sent_id {sent_id!r} occurs twice in the {language} stream: D03 "
                "pools the UD splits, so a repeated id is counted twice in "
                "n_sentences and n_tokens_raw (§3.3)"
            )
        seen_sent_ids.add(sent_id)
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


def canonical_targets(prefix_counts: pd.DataFrame, overrides: Mapping) -> dict:
    """Resolve and validate every raw prefix's merge target.

    Public because the audit pipeline needs the raw -> canonical map to fold merged
    prefixes into one document before counting: re-deriving the "default to the raw
    prefix" rule at the call site would give the merge two sources of truth.

    A wrong merge is silent: all sentences stay assigned, so §3.3's "the audit
    fails on any unassigned sentence" never fires, while the resulting document
    count fixes the exact enumeration sizes of D43 and therefore the attainable
    p floors. Two rules reject unshared mistyped targets:

    1. a target may differ from its raw prefix only if **at least two** prefixes
       share it — an unshared target means no merge is happening, so it can only
       be an error (this also rejects unshared invented targets and visually
       identical homoglyphs when they split a group instead of joining it);
    2. a merge target must be a stable root: if A → B then B → B, so no chain or
       cycle can make the intended document ambiguous.

    The target is deliberately *not* required to be an existing raw prefix:
    merging subdivisions `X.1`/`X.2` into `X` must stay legal when a bare `X`
    never occurs, and forcing one subdivision to stand for the whole document
    would be arbitrary.
    """
    canonical_of = {}
    for raw_doc_id in prefix_counts["doc_id"]:
        target = overrides[raw_doc_id].get("canonical_doc_id", raw_doc_id)
        if not isinstance(target, str) or not target.strip():
            raise ValueError(
                f"canonical_doc_id for raw prefix {raw_doc_id!r} must be a "
                "nonempty string"
            )
        canonical_of[raw_doc_id] = target

    group_sizes = Counter(canonical_of.values())
    violations = []
    for raw_doc_id in sorted(canonical_of):
        target = canonical_of[raw_doc_id]
        if target == raw_doc_id:
            continue
        target_of_target = canonical_of.get(target)
        if target_of_target is not None and target_of_target != target:
            violations.append(
                f"{raw_doc_id!r} -> {target!r}, but {target!r} -> "
                f"{target_of_target!r} (chain)"
            )
        elif group_sizes[target] < 2:
            violations.append(f"{raw_doc_id!r} -> {target!r} (no other prefix shares it)")
    if violations:
        raise ValueError(
            "invalid canonical_doc_id target(s): "
            + "; ".join(violations)
            + " — a target may differ from its raw prefix only if at least two "
            "prefixes share it, and a merge target must be a stable root"
        )
    return canonical_of


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

    Fields outside `KNOWN_OVERRIDE_FIELDS` are rejected rather than ignored: the
    required five are caught by their absence, but a mistyped *optional* key is
    caught by nothing and disappears without a trace.
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

    stray = sorted(
        f"{doc_id}: {sorted(set(assignment) - KNOWN_OVERRIDE_FIELDS)}"
        for doc_id, assignment in overrides.items()
        if set(assignment) - KNOWN_OVERRIDE_FIELDS
    )
    if stray:
        raise ValueError(
            "registry assignments carry unknown field(s): "
            + "; ".join(stray)
            + f" — the schema is {sorted(KNOWN_OVERRIDE_FIELDS)} (§2.3). An "
            "unlisted key is a typo, and a dropped optional field is invisible in "
            "every artifact the run produces."
        )

    canonical_of = canonical_targets(prefix_counts, overrides)

    group_sizes = Counter(canonical_of.values())
    missing_merge_sources = []
    for target in sorted(group_sizes):
        if group_sizes[target] < 2:
            continue
        members = sorted(
            raw for raw, canonical in canonical_of.items() if canonical == target
        )
        missing = [raw for raw in members if "source_urn" not in overrides[raw]]
        if missing:
            missing_merge_sources.append(
                f"{target!r} <- {members!r} (missing for {missing!r})"
            )
    if missing_merge_sources:
        raise ValueError(
            "every raw prefix in a multi-prefix merge must define the same "
            "explicit source_urn: " + "; ".join(missing_merge_sources)
        )

    rows_by_doc_id = {}
    first_raw_prefix_by_doc_id = {}
    for record in prefix_counts.to_dict("records"):
        raw_doc_id = record["doc_id"]
        assignment = overrides[raw_doc_id]
        missing = [f for f in REQUIRED_OVERRIDE_FIELDS if f not in assignment]
        if missing:
            raise ValueError(f"registry assignment for {raw_doc_id} is missing {missing}")
        blank = [
            field
            # `source_urn` is optional, so membership is tested; the required five
            # are already caught above by their absence, so one expression covers
            # both. It is published in the registry and carries the work's
            # identity — it is the field the Tacitus conflict lives in.
            for field in (*REQUIRED_OVERRIDE_FIELDS, "source_urn")
            if field in assignment
            and (not isinstance(assignment[field], str) or not assignment[field].strip())
        ]
        if blank:
            raise ValueError(
                f"registry assignment for {raw_doc_id} has blank or non-string "
                f"{blank}: presence is not content, and an empty cell reaches the "
                "frozen registry with nothing left to flag it (§2.3)"
            )
        flags = assignment.get("flags", [])
        if not isinstance(flags, list) or any(
            not isinstance(flag, str) or not flag.strip() for flag in flags
        ):
            raise ValueError(
                f"flags for {raw_doc_id} must be a list of nonempty strings, got "
                f"{flags!r}: list('draft') is five single-character flags nobody wrote"
            )
        if "part_order" in assignment:
            part_order = assignment["part_order"]
            if (
                isinstance(part_order, bool)
                or not isinstance(part_order, int)
                or part_order < 0
            ):
                raise ValueError(
                    f"part_order for {raw_doc_id} must be a non-negative int, got "
                    f"{part_order!r} (booleans are ints in Python and are refused here)"
                )
        if assignment["regime"] not in REGIME_LABELS:
            raise ValueError(
                f"regime {assignment['regime']!r} for {raw_doc_id} is not one of the five "
                f"labels of D04: {sorted(REGIME_LABELS)}"
            )
        canonical_doc_id = canonical_of[raw_doc_id]
        metadata = {
            "language": record["language"],
            "source_urn": assignment.get("source_urn", raw_doc_id),
            **{field: assignment[field] for field in REQUIRED_OVERRIDE_FIELDS},
            "flags": list(assignment.get("flags", [])),
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
