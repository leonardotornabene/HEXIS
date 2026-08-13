"""Alphabet mapping: total function over raw (UPOS, DEPREL) (Spec §3.4, App. A; D05–D09).

Return shape and configuration coupling per the ratified G0 API contract
(docs/implementation/specs/2026-08-13-g0-api-contract.md), which closes the
reading D54(v) deferred to separate ratification.
"""

from dataclasses import dataclass
from typing import Mapping

# The three alphabet-policy cells of D37/§5.6. `variant` and
# `excluded_deprel_policy` encode the same choice twice, so any other pairing is
# a configuration error: accepting it silently would let a run claim a
# sensitivity cell it never computed.
CANONICAL_ALPHABET_CELLS = frozenset(
    {("ud23", "drop"), ("ud23_oth", "oth"), ("upos_only", "drop")}
)


@dataclass(frozen=True)
class MappedToken:
    """The result of §3.4 on one raw token — not a `tokens.parquet` row (§3.7),
    which adds the caller's identity columns and stores `symbol_id` rather than
    `symbol` (ids exist only after `freeze_alphabet` at G1).

    Invariants: `kept` ⟺ `symbol is not None` ⟺ `drop_reason is None`.
    """

    upos: str
    deprel_base: str
    kept: bool
    symbol: str | None
    drop_reason: str | None


def strip_subtype(deprel: str) -> str:
    """Universal subtype stripping: deprel.lower().split(":")[0] (Spec §3.4 step 1; D07)."""
    return deprel.lower().split(":")[0]


def _alphabet_policy(cfg: Mapping) -> tuple[Mapping, str, str]:
    section = cfg["alphabet"]
    cell = (section["variant"], section["excluded_deprel_policy"])
    if cell not in CANONICAL_ALPHABET_CELLS:
        raise ValueError(
            f"alphabet variant/excluded_deprel_policy {cell} is not one of the three "
            f"cells declared in D37: {sorted(CANONICAL_ALPHABET_CELLS)}"
        )
    return section, *cell


def map_token(upos_raw: str, deprel_raw: str, cfg: Mapping) -> MappedToken:
    """Total mapping of one raw token to a symbol or a drop decision (Spec §3.4 steps 1–5).

    Order of operations is normative: strip subtype (D07); PROPN→NOUN (D08); UPOS
    retain/drop (D05); deprel_base retain / excluded-deprel policy drop|oth
    (D06/D09); symbol. Total over any pair of strings — an unexpected label is a
    drop decision, never an exception (D09). An inconsistent *configuration* is a
    different matter and raises.

    Under `upos_only` (D31) steps 1–4 are unchanged and only step 5 differs, so
    the observed token set — and therefore the evaluated positions — stays
    identical to C0 and the cell localizes the DEPREL information (D42(ii)).
    """
    section, variant, policy = _alphabet_policy(cfg)

    deprel_base = strip_subtype(deprel_raw)
    upos = section["upos_map"].get(upos_raw, upos_raw)

    if upos not in section["upos_keep"]:
        return MappedToken(upos, deprel_base, False, None, "upos_excluded")

    if deprel_base in section["deprel_keep"]:
        symbol = upos if variant == "upos_only" else f"{upos}:{deprel_base}"
        return MappedToken(upos, deprel_base, True, symbol, None)

    if policy == "oth":
        # The catch-all shows up only in `symbol`; deprel_base keeps the absorbed
        # category visible to the G1 audit and GATE-A.
        return MappedToken(upos, deprel_base, True, f"{upos}:oth", None)

    return MappedToken(
        upos, deprel_base, False, None, f"deprel_excluded:{deprel_base}"
    )


def run_audit(tokens, cfg):
    """G1 alphabet audit: UPOS×DEPREL contingency per document and regime, drop-rate
    tables by rule and label, GATE-A/GATE-B outcomes (Spec §3.4; D06, D09).

    GATED:G1 — the audit runs on real data strictly after G0 (D45).
    """
    raise NotImplementedError


def freeze_alphabet(tokens, cfg):
    """Freeze alphabet = symbols observed at G1; integer ids by descending pooled
    frequency; persist to data/processed/alphabet.json (Spec §3.4, §3.7).

    GATED:G1 — the frozen alphabet is an outcome of the G1 audit (D45).
    """
    raise NotImplementedError
