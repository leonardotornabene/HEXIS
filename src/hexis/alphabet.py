"""Alphabet mapping: total function over raw (UPOS, DEPREL) (Spec §3.4, App. A; D05–D09)."""


def strip_subtype(deprel: str) -> str:
    """Universal subtype stripping: deprel.lower().split(":")[0] (Spec §3.4 step 1; D07)."""
    raise NotImplementedError


def map_token(upos_raw: str, deprel_raw: str, cfg):
    """Total mapping of one raw token to a symbol or a drop decision (Spec §3.4 steps 1–5).

    Order of operations is normative: strip subtype; PROPN→NOUN (D08); UPOS
    retain/drop (D05); deprel_base retain / excluded-deprel policy drop|oth
    (D06/D09); symbol = f"{UPOS}:{deprel_base}". Exact signature finalized at
    implementation (Fase 1).
    """
    raise NotImplementedError


def run_audit(tokens, cfg):
    """G1 alphabet audit: UPOS×DEPREL contingency per document and regime, drop-rate
    tables by rule and label, GATE-A/GATE-B outcomes (Spec §3.4; D06, D09).

    Exact signature finalized at implementation (Fase 1).
    """
    raise NotImplementedError


def freeze_alphabet(tokens, cfg):
    """Freeze alphabet = symbols observed at G1; integer ids by descending pooled
    frequency; persist to data/processed/alphabet.json (Spec §3.4, §3.7).

    Exact signature finalized at implementation (Fase 1).
    """
    raise NotImplementedError
