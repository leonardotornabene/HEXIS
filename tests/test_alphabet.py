"""Alphabet mapping tests (Spec §7, gate G0; §3.4, App. A; D05–D09).

Return shape and configuration coupling per the ratified G0 API contract
(docs/implementation/specs/2026-08-13-g0-api-contract.md; D54(v)).
Never delete or weaken a test to make it pass.
"""

import dataclasses

import pytest

from hexis import alphabet, conllu_reader
from hexis.config import resolve_config

pytestmark = pytest.mark.g0

UD_UPOS = sorted(conllu_reader.UD_UPOS_TAGS)

# The 20 verified Latin subtypes of §3.4 step 1, plus the Greek/proposal cases.
VERIFIED_SUBTYPES = {
    "acl:relcl": "acl",
    "advcl:abs": "advcl",
    "advcl:cmp": "advcl",
    "advcl:pred": "advcl",
    "advmod:neg": "advmod",
    "advmod:emph": "advmod",
    "advmod:lmod": "advmod",
    "advmod:tmod": "advmod",
    "aux:pass": "aux",
    "nsubj:pass": "nsubj",
    "nsubj:outer": "nsubj",
    "obl:arg": "obl",
    "obl:cmp": "obl",
    "ccomp:reported": "ccomp",
    "conj:expl": "conj",
    "det:numgov": "det",
    "nummod:gov": "nummod",
    "flat:name": "flat",
    "flat:redup": "flat",
    "csubj:pass": "csubj",
}


def cfg_for(variant, policy):
    return resolve_config(
        {"alphabet": {"variant": variant, "excluded_deprel_policy": policy}}
    )


UD23 = cfg_for("ud23", "drop")
UD23_OTH = cfg_for("ud23_oth", "oth")
UPOS_ONLY = cfg_for("upos_only", "drop")


# --- §7 catalogue ---------------------------------------------------------------


def test_subtype_stripping_incl_multi_colon():
    """deprel.lower().split(":")[0]; all verified subtypes (§3.4 step 1; D07)."""
    for raw, expected in VERIFIED_SUBTYPES.items():
        assert alphabet.strip_subtype(raw) == expected
    assert alphabet.strip_subtype("root") == "root"          # already bare
    assert alphabet.strip_subtype("ADVMOD:EMPH") == "advmod"  # lowercased
    assert alphabet.strip_subtype("obl:arg:extra") == "obl"   # multi-colon
    assert alphabet.strip_subtype("") == ""                   # total on any string


def test_propn_maps_to_noun():
    """PROPN → NOUN (§3.4 step 2; D08). Config-driven: Greek has no PROPN, so the
    rule is a no-op there and needs no language argument."""
    mapped = alphabet.map_token("PROPN", "nsubj", UD23)
    assert mapped.upos == "NOUN"
    assert mapped.symbol == "NOUN:nsubj"
    assert mapped.kept is True


def test_drop_rules():
    """UPOS {PUNCT, X, INTJ, SYM} dropped with drop_reason upos_excluded (D05)."""
    for upos in ("PUNCT", "X", "INTJ", "SYM"):
        mapped = alphabet.map_token(upos, "punct", UD23)
        assert mapped.kept is False
        assert mapped.drop_reason == "upos_excluded"
        assert mapped.symbol is None


def test_upos_rule_precedes_deprel_rule():
    """Order of operations is normative (§3.4): a dropped UPOS carrying an excluded
    deprel is reported as upos_excluded, never deprel_excluded."""
    mapped = alphabet.map_token("INTJ", "vocative", UD23)
    assert mapped.drop_reason == "upos_excluded"


def test_excluded_deprel_dropped_under_primary_policy():
    """PRIMARY = delete, drop_reason deprel_excluded:<base label> (D06)."""
    mapped = alphabet.map_token("NOUN", "vocative", UD23)
    assert mapped.kept is False
    assert mapped.drop_reason == "deprel_excluded:vocative"
    assert mapped.symbol is None
    # the label recorded is the stripped base, the unit GATE-A audits
    assert alphabet.map_token("NOUN", "flat:name", UD23).drop_reason == (
        "deprel_excluded:flat"
    )


def test_oth_arm():
    """SENSITIVITY = map to catch-all UPOS:oth (D06). The substitution appears only
    in `symbol`; deprel_base keeps the absorbed category visible to GATE-A."""
    mapped = alphabet.map_token("NOUN", "vocative", UD23_OTH)
    assert mapped.kept is True
    assert mapped.deprel_base == "vocative"
    assert mapped.symbol == "NOUN:oth"
    assert mapped.drop_reason is None
    # a retained deprel is unaffected by the policy
    assert alphabet.map_token("NOUN", "nsubj", UD23_OTH).symbol == "NOUN:nsubj"


def test_totality_on_any_ud_label():
    """Total function over any raw (UPOS, DEPREL) (§3.4; D09): never None, never
    raises, invariants hold on every pair."""
    deprels = sorted(UD23["alphabet"]["deprel_keep"]) + [
        "punct", "discourse", "vocative", "orphan", "flat", "dep", "goeswith",
        "reparandum", "list", "compound", "expl", "fixed", "obl:agent", "", "WeIrD:x",
    ]
    for cfg in (UD23, UD23_OTH, UPOS_ONLY):
        for upos in UD_UPOS:
            for deprel in deprels:
                mapped = alphabet.map_token(upos, deprel, cfg)
                assert isinstance(mapped, alphabet.MappedToken)
                if mapped.kept:
                    assert mapped.symbol is not None and mapped.drop_reason is None
                else:
                    assert mapped.symbol is None and mapped.drop_reason is not None


def test_mapped_token_is_immutable():
    mapped = alphabet.map_token("NOUN", "nsubj", UD23)
    with pytest.raises(dataclasses.FrozenInstanceError):
        mapped.symbol = "VERB:root"
    assert mapped.symbol == "NOUN:nsubj"


# --- configuration coupling ------------------------------------------------------


def test_upos_only_keeps_the_retention_rules():
    """D31/D42(ii): only step 5 changes. The token set stays identical to C0, so the
    alphabet cell localizes the DEPREL information instead of changing the positions."""
    assert alphabet.map_token("NOUN", "nsubj", UPOS_ONLY).symbol == "NOUN"
    assert alphabet.map_token("PROPN", "nsubj", UPOS_ONLY).symbol == "NOUN"
    assert alphabet.map_token("PUNCT", "punct", UPOS_ONLY).kept is False
    excluded = alphabet.map_token("NOUN", "vocative", UPOS_ONLY)
    assert excluded.kept is False
    assert excluded.drop_reason == "deprel_excluded:vocative"


def test_upos_only_alphabet_is_the_twelve_retained_tags():
    symbols = {
        alphabet.map_token(upos, "nsubj", UPOS_ONLY).symbol
        for upos in UD_UPOS
    } - {None}
    assert symbols == set(UPOS_ONLY["alphabet"]["upos_keep"])
    assert len(symbols) == 12


@pytest.mark.parametrize(
    "variant,policy",
    [("ud23", "oth"), ("ud23_oth", "drop"), ("upos_only", "oth"), ("nope", "drop")],
)
def test_inconsistent_alphabet_configuration_raises(variant, policy):
    """variant and excluded_deprel_policy encode the same choice twice; D37 declares
    exactly three cells. Silent acceptance would let a run claim a cell it never
    computed."""
    with pytest.raises(ValueError) as exc:
        alphabet.map_token("NOUN", "nsubj", cfg_for(variant, policy))
    assert variant in str(exc.value) and policy in str(exc.value)


# --- end to end through the reader -----------------------------------------------


def test_synthetic_conllu_with_mwt_and_empty_node(conllu_samples):
    """MWT range + empty node handled end to end (§3.2 → §3.4): the reader removes
    the non-integer-ID rows, the alphabet drops PUNCT, retained symbols survive."""
    sentence = next(iter(conllu_reader.iter_sentences(conllu_samples["valid"])))
    mapped = [alphabet.map_token(t["upos"], t["deprel"], UD23) for t in sentence]

    assert len(mapped) == 4  # 1-2 range row and 4.1 empty node already gone
    assert [m.symbol for m in mapped] == ["ADV:advmod", "CCONJ:cc", "VERB:root", None]
    assert [m.kept for m in mapped] == [True, True, True, False]
    assert mapped[-1].drop_reason == "upos_excluded"
