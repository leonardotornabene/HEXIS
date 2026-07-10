"""Alphabet mapping tests (Spec §7, gate G0; §3.4, App. A; D05–D09).

Fase 0 placeholders: cases enumerated per Spec §7, no assertions yet.
Never delete or weaken a test to make it pass.
"""

import pytest

SKIP = pytest.mark.skip(reason="Fase 0 scaffold — implement at gate G0 per Spec §7")


@SKIP
def test_subtype_stripping_incl_multi_colon():
    """deprel.lower().split(":")[0]; all 20 verified Latin subtypes (§3.4 step 1; D07)."""


@SKIP
def test_propn_maps_to_noun():
    """PROPN → NOUN, Latin only (§3.4 step 2; D08)."""


@SKIP
def test_drop_rules():
    """UPOS {PUNCT, X, INTJ, SYM} dropped with drop_reason upos_excluded (D05)."""


@SKIP
def test_oth_arm():
    """Excluded-deprel sensitivity policy: map to UPOS:oth (D06)."""


@SKIP
def test_totality_on_any_ud_label():
    """Mapping is a total function over any raw (UPOS, DEPREL) (§3.4; D09)."""


@SKIP
def test_synthetic_conllu_with_mwt_and_empty_node():
    """Synthetic CoNLL-U with MWT range line + empty node handled end to end (§3.2)."""
