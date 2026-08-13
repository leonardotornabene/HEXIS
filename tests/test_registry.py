"""Document registry tests (Spec §7, gate G0; §2.3, §3.3; D03, D04).

Signatures per the ratified G0 API contract
(docs/implementation/specs/2026-08-13-g0-api-contract.md).
All fixtures are synthetic: the corpus enumeration and the human-verified
assignments belong to the G1 audit, strictly after G0 (D45).
"""

import pandas as pd
import pytest
from conllu import TokenList

from hexis import registry

pytestmark = pytest.mark.g0

REGIME_LABELS = {"HEX", "PROSE_CLASS", "PROSE_POST", "OTHER_VERSE", "EXCLUDED"}

ILIAD = "tlg0012.tlg001.perseus-grc1.tb.xml"
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
