"""Alphabet mapping (piano §4.1): validate the source tags, then merge ADV/PART.

One token in, one decision out. The order is normative: strip the DEPREL subtype,
map PROPN to NOUN before retention, apply the UPOS retention set, apply the DEPREL
retention set under the variant's policy, and only then merge ADV and PART on the
tokens that survived. An unknown source UPOS is an error, not a drop.
"""

from dataclasses import dataclass
from typing import Mapping

import pandas as pd

VARIANTS = ("ud23", "ud23_oth", "upos_only")


@dataclass(frozen=True)
class MappedToken:
    """One token's decision. The coordinates table adds identity columns and the
    frozen `symbol_id`; this object carries the decision alone.

    Invariants: `kept` ⟺ `symbol is not None` ⟺ `drop_reason is None`.
    """

    upos: str
    deprel_base: str
    kept: bool
    symbol: str | None
    drop_reason: str | None


def strip_subtype(deprel: str) -> str:
    """Universal subtype stripping: `deprel.lower().split(":")[0]` (§4.1 step 1)."""
    return deprel.lower().split(":")[0]


def _alphabet_policy(cfg: Mapping, variant=None) -> tuple[Mapping, str, str]:
    if cfg.get("spec_version") != "HEXIS-3.1":
        raise ValueError("the alphabet reads the active HEXIS-3.1 projection only")
    variant = variant or "ud23"
    if variant not in VARIANTS:
        raise ValueError(f"unknown alphabet variant {variant!r}")
    rep = cfg["representation"]
    return ({"upos_map": rep["source_map_before_retention"],
             "upos_keep": rep["source_upos_keep_before_merge"],
             "deprel_keep": rep["deprel_keep"]},
            variant, "oth" if variant == "ud23_oth" else "drop")


def map_token(upos_raw: str, deprel_raw: str, cfg: Mapping, *, variant=None) -> MappedToken:
    """Map one token: subtype, PROPN→NOUN, retention, policy, ADV/PART merge.

    A source UPOS outside the UD set and an empty DEPREL are errors: the corpus is
    pinned by hash, so an unexpected tag means the input is not the corpus, and
    dropping it silently would hide that.

    Under `upos_only` only the symbol changes, so the retained token set — and
    with it the evaluated positions — stays identical to C0.
    """
    section, variant, policy = _alphabet_policy(cfg, variant)
    from hormathos.conllu_reader import UD_UPOS_TAGS
    if not isinstance(upos_raw, str) or upos_raw not in UD_UPOS_TAGS:
        raise ValueError(f"UPOS {upos_raw!r} is not a source UD tag")
    if not isinstance(deprel_raw, str) or not deprel_raw.strip() or deprel_raw == "_":
        raise ValueError(f"DEPREL {deprel_raw!r} is empty")

    deprel_base = strip_subtype(deprel_raw)
    upos = section["upos_map"].get(upos_raw, upos_raw)

    if upos not in section["upos_keep"]:
        return MappedToken(upos, deprel_base, False, None, "upos_excluded")

    if deprel_base in section["deprel_keep"] or policy == "oth":
        upos = cfg["representation"]["map_after_retention"].get(upos, upos)
    if deprel_base in section["deprel_keep"]:
        symbol = upos if variant == "upos_only" else f"{upos}:{deprel_base}"
        return MappedToken(upos, deprel_base, True, symbol, None)

    if policy == "oth":
        # The catch-all shows up only in `symbol`; deprel_base keeps the absorbed
        # category visible to the audit.
        return MappedToken(upos, deprel_base, True, f"{upos}:oth", None)

    return MappedToken(
        upos, deprel_base, False, None, f"deprel_excluded:{deprel_base}"
    )


def map_tokens(tokens, cfg, *, variant=None) -> pd.DataFrame:
    """Apply the mapping to a whole raw token table.

    In: `language, doc_id, sent_id, token_ord, upos_raw, deprel_raw`.
    Out: the same plus `upos, deprel_base, kept, symbol, drop_reason`. The frozen
    `symbol_id` and the available past belong to the coordinates (§11.2), which
    are built from the encoded order, not from this table.

    The decision is memoized over distinct `(upos_raw, deprel_raw)` pairs: it is a
    pure function of that pair, and the corpus has ~10² pairs against ~10⁵ rows.
    """
    frame = tokens.copy()
    decisions = {
        pair: map_token(pair[0], pair[1], cfg, variant=variant)
        for pair in frame[["upos_raw", "deprel_raw"]].drop_duplicates().itertuples(
            index=False, name=None
        )
    }
    resolved = [
        decisions[pair]
        for pair in zip(frame["upos_raw"], frame["deprel_raw"])
    ]
    frame["upos"] = [decision.upos for decision in resolved]
    frame["deprel_base"] = [decision.deprel_base for decision in resolved]
    # Explicit dtype: on an empty table a list comprehension yields an object
    # column, and `kept` is used as a boolean mask.
    frame["kept"] = pd.Series(
        [decision.kept for decision in resolved], dtype=bool, index=frame.index
    )
    # Both are nullable. `string` keeps the null as pd.NA instead of
    # letting the object dtype coerce None to NaN, which would survive neither an
    # equality check nor a parquet round-trip cleanly.
    frame["symbol"] = pd.array([decision.symbol for decision in resolved], dtype="string")
    frame["drop_reason"] = pd.array(
        [decision.drop_reason for decision in resolved], dtype="string"
    )
    return frame
