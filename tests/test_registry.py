"""Document registry tests (Spec §7, gate G0; §2.3, §3.3; D03, D04).

Signatures per the ratified G0 API contract
(docs/implementation/specs/2026-08-13-g0-api-contract.md).
All fixtures are synthetic: the corpus enumeration and the human-verified
assignments belong to the G1 audit, strictly after G0 (D45).
"""

import pandas as pd
import pytest
from conllu import TokenList

from hexis import conllu_reader, registry

pytestmark = pytest.mark.g0

REGIME_LABELS = {"HEX", "PROSE_CLASS", "PROSE_POST", "OTHER_VERSE", "EXCLUDED"}

ILIAD = "tlg0012.tlg001.perseus-grc1.tb.xml"
ILIAD_PART = "tlg0012.tlg001.perseus-grc1.1.tb.xml"
THUC = "tlg0003.tlg001.perseus-grc1.1.tb.xml"


def sentence(sent_id, n_tokens, newdoc_id=None):
    metadata = {"sent_id": sent_id}
    if newdoc_id is not None:
        metadata["newdoc id"] = newdoc_id
    tokens = [{"id": i + 1, "form": "x"} for i in range(n_tokens)]
    return TokenList(tokens, metadata)


OVERRIDES = {
    ILIAD: {
        "author": "Homer",
        "work": "Iliad",
        "regime": "HEX",
        "meter": "dactylic_hexameter",
        "period": "archaic",
        "flags": [],
    },
    THUC: {
        "author": "Thucydides",
        "work": "Historiae",
        "regime": "PROSE_CLASS",
        "meter": "prose",
        "period": "classical",
        "flags": [],
    },
}


# --- doc_id derivation (D03) -----------------------------------------------------


def test_doc_id_derived_from_sent_id_prefix():
    """sent_id is <newdoc id>@<ordinal>; doc_id is the part before the last @."""
    counts = registry.enumerate_prefixes(
        [sentence(f"{ILIAD}@1", 5), sentence(f"{THUC}@2", 7)], language="grc"
    )
    assert list(counts["doc_id"]) == sorted([ILIAD, THUC])
    assert set(counts["language"]) == {"grc"}


def test_counts_aggregate_over_gappy_ordinals_and_split_files():
    """UD splits are ignored (D03): sentences of one document arrive in several
    files with non-contiguous ordinals and must aggregate into one row."""
    counts = registry.enumerate_prefixes(
        [
            sentence(f"{ILIAD}@3", 4),
            sentence(f"{ILIAD}@7", 6),
            sentence(f"{ILIAD}@8", 2),
            sentence(f"{THUC}@41", 9),
        ],
        language="grc",
    )
    iliad = counts.set_index("doc_id").loc[ILIAD]
    assert iliad["n_sentences"] == 3
    assert iliad["n_tokens_raw"] == 12
    assert counts.set_index("doc_id").loc[THUC, "n_sentences"] == 1


def test_n_tokens_raw_counts_integer_id_words_before_alphabet(conllu_samples):
    counts = registry.enumerate_prefixes(
        conllu_reader.iter_sentences(conllu_samples["valid"]), language="lat"
    )

    row = counts.set_index("doc_id").loc["alpha"]
    assert row["n_sentences"] == 2
    assert row["n_tokens_raw"] == 6


def test_newdoc_id_disagreement_raises():
    """`newdoc id` is present in both treebanks; when it contradicts the derived
    prefix the document identity is ambiguous and must fail loud (§3.3)."""
    with pytest.raises(ValueError) as exc:
        registry.enumerate_prefixes(
            [sentence(f"{ILIAD}@1", 5, newdoc_id="something.else.xml")], language="grc"
        )
    assert ILIAD in str(exc.value) and "something.else.xml" in str(exc.value)


def test_agreeing_newdoc_id_is_accepted():
    counts = registry.enumerate_prefixes(
        [sentence(f"{ILIAD}@1", 5, newdoc_id=ILIAD)], language="grc"
    )
    assert list(counts["doc_id"]) == [ILIAD]


def test_sent_id_without_separator_raises():
    with pytest.raises(ValueError) as exc:
        registry.enumerate_prefixes([sentence("no-ordinal-here", 3)], language="grc")
    assert "no-ordinal-here" in str(exc.value)


# --- registry construction (§2.3) ------------------------------------------------


def counts_fixture():
    return registry.enumerate_prefixes(
        [sentence(f"{ILIAD}@1", 5), sentence(f"{THUC}@2", 7)], language="grc"
    )


def merge_fixture():
    counts = registry.enumerate_prefixes(
        [
            sentence(f"{ILIAD}@1", 5),
            sentence(f"{ILIAD_PART}@1", 7),
            sentence(f"{ILIAD_PART}@2", 3),
        ],
        language="grc",
    )
    source_urn = "urn:cts:greekLit:tlg0012.tlg001"
    overrides = {
        ILIAD: dict(OVERRIDES[ILIAD], source_urn=source_urn),
        ILIAD_PART: dict(
            OVERRIDES[ILIAD],
            canonical_doc_id=ILIAD,
            source_urn=source_urn,
        ),
    }
    return counts, overrides


def test_build_registry_assigns_taxonomy_and_schema():
    reg = registry.build_registry(counts_fixture(), OVERRIDES)
    assert list(reg.columns) == list(registry.REGISTRY_COLUMNS)
    row = reg.set_index("doc_id").loc[ILIAD]
    assert row["author"] == "Homer"
    assert row["work"] == "Iliad"
    assert row["regime"] == "HEX"
    assert row["meter"] == "dactylic_hexameter"
    assert row["period"] == "archaic"
    assert row["n_sentences"] == 1
    assert row["n_tokens_raw"] == 5
    assert set(reg["regime"]) <= REGIME_LABELS


def test_source_urn_defaults_to_doc_id():
    reg = registry.build_registry(counts_fixture(), OVERRIDES)
    assert reg.set_index("doc_id").loc[THUC, "source_urn"] == THUC


def test_overrides_merge_raw_prefixes_into_canonical_document():
    counts, overrides = merge_fixture()

    reg = registry.build_registry(counts, overrides)

    assert list(reg["doc_id"]) == [ILIAD]
    row = reg.iloc[0]
    assert row["source_urn"] == "urn:cts:greekLit:tlg0012.tlg001"
    assert row["n_sentences"] == 3
    assert row["n_tokens_raw"] == 15

    reversed_reg = registry.build_registry(
        counts.iloc[::-1].reset_index(drop=True),
        dict(reversed(list(overrides.items()))),
    )
    pd.testing.assert_frame_equal(reg, reversed_reg)


@pytest.mark.parametrize(
    ("field", "conflicting_value"),
    [
        ("language", "lat"),
        ("source_urn", "urn:cts:greekLit:tlg0012.tlg999"),
        ("author", "Pseudo-Homer"),
        ("work", "Iliad subdivision"),
        ("regime", "OTHER_VERSE"),
        ("meter", "mixed"),
        ("period", "classical"),
        ("flags", ["duplicate_source"]),
    ],
)
def test_merge_rejects_inconsistent_metadata(field, conflicting_value):
    counts, overrides = merge_fixture()
    if field == "language":
        counts.loc[counts["doc_id"] == ILIAD_PART, field] = conflicting_value
    else:
        overrides[ILIAD_PART][field] = conflicting_value

    with pytest.raises(ValueError) as exc:
        registry.build_registry(counts, overrides)

    assert field in str(exc.value)
    assert ILIAD in str(exc.value)
    assert ILIAD_PART in str(exc.value)


@pytest.mark.parametrize("invalid_target", [None, "", 7])
def test_canonical_doc_id_must_be_a_nonempty_string(invalid_target):
    counts, overrides = merge_fixture()
    overrides[ILIAD_PART]["canonical_doc_id"] = invalid_target

    with pytest.raises(ValueError) as exc:
        registry.build_registry(counts, overrides)

    assert "canonical_doc_id" in str(exc.value)
    assert ILIAD_PART in str(exc.value)


# --- canonical target validation -------------------------------------------------
#
# A merge target that nothing else shares is indistinguishable from a typo, and a
# wrong merge is silent: every sentence stays assigned, so the §3.3 "fails on any
# unassigned sentence" rule never fires. Since the document count fixes the exact
# enumeration sizes of D43, a silent split or merge changes the attainable p
# floors. The rule: a target may differ from its raw prefix ONLY if at least two
# raw prefixes share it.


def merged_counts(*doc_ids):
    return registry.enumerate_prefixes(
        [sentence(f"{doc_id}@1", 5) for doc_id in doc_ids], language="grc"
    )


def assignment(canonical=None, urn="urn:cts:greekLit:tlg0012.tlg001"):
    extra = {"source_urn": urn}
    if canonical is not None:
        extra["canonical_doc_id"] = canonical
    return dict(OVERRIDES[ILIAD], **extra)


def test_merge_into_a_canonical_that_is_not_itself_a_raw_prefix():
    """Legitimate and must stay legal: subdivisions `X.1`/`X.2` merge into `X`
    even though a bare `X` prefix never occurs in the corpus. Requiring the target
    to be an existing raw prefix would force an arbitrary choice between them."""
    reg = registry.build_registry(
        merged_counts("X.1", "X.2"),
        {"X.1": assignment("X"), "X.2": assignment("X")},
    )
    assert list(reg["doc_id"]) == ["X"]
    assert reg.iloc[0]["n_sentences"] == 2


def test_merge_requires_explicit_source_urn_on_every_contributor():
    """A root prefix's default can equal another prefix's explicit value; that
    must not satisfy the explicit traceability contract for a real merge."""
    root = assignment("X")
    del root["source_urn"]

    with pytest.raises(ValueError) as exc:
        registry.build_registry(
            merged_counts("X", "X.1"),
            {"X": root, "X.1": assignment("X", urn="X")},
        )

    message = str(exc.value)
    assert "source_urn" in message and "X" in message and "X.1" in message


def test_unshared_canonical_target_is_rejected():
    """A single prefix pointing at an invented target: no merge is happening, so
    the target can only be a mistake."""
    with pytest.raises(ValueError) as exc:
        registry.build_registry(
            merged_counts("X.1"), {"X.1": assignment("COMPLETELY_INVENTED")}
        )
    assert "COMPLETELY_INVENTED" in str(exc.value) and "X.1" in str(exc.value)


def test_typo_in_a_merge_target_splits_the_group_and_is_rejected():
    """`X.1 -> X` and `X.2 -> Xx` used to yield two documents where one was meant."""
    with pytest.raises(ValueError) as exc:
        registry.build_registry(
            merged_counts("X.1", "X.2"),
            {"X.1": assignment("X"), "X.2": assignment("Xx")},
        )
    assert "Xx" in str(exc.value)


def test_unicode_homoglyph_target_is_rejected():
    """`HYMN` and `HYMN` differ only in the final character (Latin N vs Greek Nu):
    visually identical, and previously two silent documents."""
    latin_n, greek_nu = "HYMN", "HYMΝ"
    assert latin_n != greek_nu
    with pytest.raises(ValueError) as exc:
        registry.build_registry(
            merged_counts("H.1", "H.2"),
            {"H.1": assignment(latin_n), "H.2": assignment(greek_nu)},
        )
    assert "H.2" in str(exc.value)


def test_canonical_target_chain_is_rejected():
    """A -> B while B -> C: the intended document is ambiguous."""
    with pytest.raises(ValueError) as exc:
        registry.build_registry(
            merged_counts("A", "B", "C"),
            {
                "A": assignment("B"),
                "B": assignment("C"),
                "C": assignment("C"),
            },
        )
    message = str(exc.value)
    assert "B" in message and "C" in message


def test_self_targeting_prefix_without_merge_is_allowed():
    """Writing `canonical_doc_id` equal to the raw prefix is redundant, not wrong."""
    reg = registry.build_registry(
        merged_counts("X.1"), {"X.1": assignment("X.1")}
    )
    assert list(reg["doc_id"]) == ["X.1"]


def test_n_tokens_retained_is_nullable_until_the_alphabet_is_frozen():
    """It depends on the frozen alphabet (§3.4), which is a G1 outcome; the column
    exists and is null, and must be complete before the G1 freeze."""
    reg = registry.build_registry(counts_fixture(), OVERRIDES)
    assert reg["n_tokens_retained"].isna().all()
    assert str(reg["n_tokens_retained"].dtype) == "Int64"


def test_unassigned_document_raises():
    """The G1 audit fails on any unassigned sentence (§3.3) — nothing is guessed."""
    with pytest.raises(ValueError) as exc:
        registry.build_registry(counts_fixture(), {ILIAD: OVERRIDES[ILIAD]})
    assert THUC in str(exc.value)


def test_unknown_override_raises():
    """An override naming a document absent from the corpus is a stale registry."""
    extra = dict(OVERRIDES, **{"ghost.tb.xml": OVERRIDES[ILIAD]})
    with pytest.raises(ValueError) as exc:
        registry.build_registry(counts_fixture(), extra)
    assert "ghost.tb.xml" in str(exc.value)


def test_invalid_regime_raises():
    bad = dict(OVERRIDES, **{THUC: dict(OVERRIDES[THUC], regime="PROSE")})
    with pytest.raises(ValueError) as exc:
        registry.build_registry(counts_fixture(), bad)
    assert "PROSE" in str(exc.value)


@pytest.mark.parametrize("field", ["author", "work", "regime", "meter", "period"])
def test_missing_override_field_raises(field):
    incomplete = {k: dict(v) for k, v in OVERRIDES.items()}
    del incomplete[THUC][field]
    with pytest.raises(ValueError) as exc:
        registry.build_registry(counts_fixture(), incomplete)
    assert field in str(exc.value)


def test_registry_is_deterministic_in_row_order():
    first = registry.build_registry(counts_fixture(), OVERRIDES)
    second = registry.build_registry(counts_fixture(), dict(reversed(list(OVERRIDES.items()))))
    pd.testing.assert_frame_equal(first, second)
    assert list(first["doc_id"]) == sorted([ILIAD, THUC])  # order follows doc_id, not insertion
