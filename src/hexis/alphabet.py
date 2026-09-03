"""Alphabet mapping: total function over raw (UPOS, DEPREL) (Spec §3.4, App. A; D05–D09).

Return shape and configuration coupling per the ratified G0 API contract
(docs/implementation/specs/2026-08-13-g0-api-contract.md), which closes the
reading D54(v) deferred to separate ratification.
"""

from dataclasses import dataclass
from typing import Mapping

import pandas as pd

# §3.4: "any document with < 70% retention flagged for inspection" (GATE-B). Not a
# config knob — no §5.6 cell varies it, and a threshold that can drift silently is
# not a gate.
GATE_B_RETENTION = 0.70

# §3.4/D06: "> 2% of a regime's raw tokens" (GATE-A). A constant for exactly the
# reason above, which until 2026-09-03 was applied to GATE-B and not to its
# sibling: GATE-A was read from config, and `config.check_against_default`
# inspects key presence only, so `gate_a_threshold: 0.9` disarmed the gate in
# silence and the run reported `fired: False`.
# `config/default.yaml` still declares the key, because `config/` is untouched
# until the ratification package is deposited as one act (D55 checklist item 18).
# A config that disagrees is therefore refused, not silently ignored — a dead
# declared key would be the same defect wearing the other face.
GATE_A_THRESHOLD = 0.02

# D04's fifth label is the disposal label, not a regime under study: an EXCLUDED
# document enters no estimand — not P1, P2, S1, R1 or L1, not a regime aggregate,
# not T*. D06 reads "in any regime" and D04 does list EXCLUDED among the five, so
# the scope is a genuine second reading and is declared rather than assumed.
GATE_A_VERDICT_EXCLUDES = ("EXCLUDED",)

# One sentence = one (language, doc_id, sent_id) group; `available_past` and every
# P-RESET context truncate at its start (D10).
_SENTENCE_KEY = ("language", "doc_id", "sent_id")

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


def map_tokens(tokens, cfg) -> pd.DataFrame:
    """Apply §3.4 to a whole raw token table, adding the §3.7 derived columns.

    In: `language, doc_id, sent_id, token_ord, upos_raw, deprel_raw`.
    Out: the same plus `upos, deprel_base, kept, symbol, drop_reason,
    available_past`. `symbol_id` is absent by construction — ids exist only after
    the alphabet is frozen at G1 (§3.7), and this table is what the freeze reads.

    `available_past` is the number of *retained* tokens preceding the token in its
    sentence, so deletions close gaps (D05) and the count restarts at every
    sentence under P-RESET (D10). It is `pd.NA` on dropped tokens, which are never
    evaluated positions. This is the quantity D35 restricts on (`>= 4`).

    The decision is memoized over distinct `(upos_raw, deprel_raw)` pairs: §3.4 is
    a pure function of that pair, and the corpus has ~10² pairs against ~10⁵ rows.
    """
    frame = tokens.copy()
    decisions = {
        pair: map_token(pair[0], pair[1], cfg)
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
    # column, and `kept` is used as a boolean mask (§7 lists the empty case).
    frame["kept"] = pd.Series(
        [decision.kept for decision in resolved], dtype=bool, index=frame.index
    )
    # §3.7 declares both nullable. `string` keeps the null as pd.NA instead of
    # letting the object dtype coerce None to NaN, which would survive neither an
    # equality check nor a parquet round-trip cleanly.
    frame["symbol"] = pd.array([decision.symbol for decision in resolved], dtype="string")
    frame["drop_reason"] = pd.array(
        [decision.drop_reason for decision in resolved], dtype="string"
    )
    frame["available_past"] = _available_past(frame)
    return frame


def _available_past(frame: pd.DataFrame) -> pd.Series:
    ordered = frame.sort_values(list(_SENTENCE_KEY) + ["token_ord"])
    kept = ordered["kept"].to_numpy()
    ranks = ordered["kept"].groupby(
        [ordered[column] for column in _SENTENCE_KEY], sort=False
    ).cumsum() - 1
    out = pd.Series(pd.NA, index=frame.index, dtype="Int64")
    out.loc[ordered.index[kept]] = ranks.to_numpy()[kept]
    return out


def observed_alphabet(tokens, cfg, *, language: str) -> dict[str, int]:
    """The alphabet observed in a mapped token table: `{symbol: id}` (§3.4).

    Ids run 0..|A|-1 by **descending pooled frequency**, ties broken by the symbol
    string so the mapping is a function of the data alone and not of row order.

    §4.1 defines |A| as the frozen alphabet size for the **(language, variant)**
    pair, so a table carrying more than the requested language is rejected rather
    than silently pooled — a pooled alphabet would change β·|A| for both languages
    and quietly alter every smoothed probability.

    Pure: computes the inventory and writes nothing. Persisting it as
    `alphabet.json` is the separate act of freezing, which happens at G1 only
    after the registry is ratified.
    """
    _alphabet_policy(cfg)
    foreign = sorted(set(tokens["language"].unique()) - {language})
    if foreign:
        raise ValueError(
            f"token table carries language(s) {foreign} but observed_alphabet was "
            f"called for language {language!r}: |A| is per (language, variant) and "
            "alphabets are never pooled (§4.1)"
        )
    counts = tokens.loc[tokens["kept"], "symbol"].value_counts()
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return {symbol: index for index, (symbol, _) in enumerate(ranked)}


def freeze_alphabet(tokens, cfg):
    """Freeze alphabet = symbols observed at G1; integer ids by descending pooled
    frequency; persist to data/processed/alphabet.json (Spec §3.4, §3.7).

    GATED:G1 — the frozen alphabet is an outcome of the G1 audit (D45), and the
    G1 audit is not ratified. Deliberately unimplemented at the pre-audit, for a
    reason beyond sequencing: §3.7 gives `alphabet.json` **one** variant tag and no
    language field, while §4.1 defines |A| per **(language, variant)**. The shape
    of a two-language artifact is therefore an open question, and guessing it here
    would freeze a format nobody ratified.

    `observed_alphabet` computes the same inventory without persisting it, which is
    all the audit needs.
    """
    raise NotImplementedError(
        "freeze_alphabet is gated on the ratified G1 audit; use observed_alphabet "
        "for the un-frozen inventory (§3.4, D45)"
    )


def run_audit(tokens, cfg, *, regimes: Mapping[str, str] | None = None) -> dict:
    """G1 alphabet audit: UPOS×DEPREL contingency per document and regime, drop-rate
    tables by rule and label, GATE-A/GATE-B outcomes (Spec §3.4; D06, D09).

    `tokens` is a mapped table from `map_tokens`. `regimes` maps `doc_id` to one of
    D04's five labels; it is the ratified registry's contribution and the audit
    fails loudly on any document it does not cover (§3.3).

    Without `regimes` the audit is **incomplete by construction**: no regime
    aggregate exists, so neither gate can be decided and both are returned as
    `not_evaluated` with the reason recorded. That is the pre-audit shape — it
    reports what counts alone can support and refuses to imply a verdict.

    GATED:G1 — the audit runs on real data strictly after G0 (D45).
    """
    section, _, _ = _alphabet_policy(cfg)
    audit = {
        "contingency": _contingency(tokens),
        "retention": _retention(tokens),
        "excluded_upos_by_label": _excluded_upos_by_label(tokens),
        "excluded_deprel_by_label": _excluded_deprel_by_label(tokens, section),
    }
    if regimes is None:
        reason = "no registry: regime aggregates require ratified doc_id -> regime assignments (§3.3)"
        audit["gate_a"] = {"status": "not_evaluated", "reason": reason}
        audit["gate_b"] = {"status": "not_evaluated", "reason": reason}
        return audit

    unassigned = sorted(set(tokens["doc_id"].unique()) - set(regimes))
    if unassigned:
        raise ValueError(
            f"no regime assignment for {unassigned}: the audit fails on any "
            "unassigned sentence (Spec §3.3, D04)"
        )
    labelled = tokens.assign(regime=tokens["doc_id"].map(regimes))
    audit["by_regime"] = _contingency(labelled, key="regime")
    # T2 (§8) asks for drop rates by rule **and regime**, not by rule and document.
    audit["retention_by_regime"] = _retention(labelled, key="regime")
    audit["restricted_fraction"] = _restricted_fraction(labelled, cfg)
    audit["gate_a"] = _gate_a(labelled, section)
    audit["gate_b"] = _gate_b(audit["retention"])
    return audit


def _contingency(tokens: pd.DataFrame, key: str = "doc_id") -> pd.DataFrame:
    """Raw UPOS×DEPREL counts; `deprel_base` rides along so §3.4 step 1 stays auditable."""
    columns = ["language", key, "upos_raw", "deprel_raw", "upos", "deprel_base"]
    return (
        tokens.groupby(columns, sort=True, dropna=False)
        .size()
        .reset_index(name="n")
    )


def _retention(tokens: pd.DataFrame, key: str = "doc_id") -> pd.DataFrame:
    """Drop rates **by rule**, grouped by `key` (§3.4; T2 wants both doc and regime)."""
    drop_reason = tokens["drop_reason"].fillna("")
    frame = tokens.assign(
        _upos_excluded=drop_reason.eq("upos_excluded"),
        _deprel_excluded=drop_reason.str.startswith("deprel_excluded:"),
    )
    out = (
        frame.groupby(["language", key], sort=True)
        .agg(
            n_raw=("kept", "size"),
            n_kept=("kept", "sum"),
            n_upos_excluded=("_upos_excluded", "sum"),
            n_deprel_excluded=("_deprel_excluded", "sum"),
        )
        .reset_index()
    )
    out["retention"] = out["n_kept"] / out["n_raw"]
    out["upos_excluded_rate"] = out["n_upos_excluded"] / out["n_raw"]
    out["deprel_excluded_rate"] = out["n_deprel_excluded"] / out["n_raw"]
    return out


def _excluded_upos_by_label(tokens: pd.DataFrame) -> pd.DataFrame:
    """Per-document census of the D05 deletions, by the UPOS tag that caused them."""
    excluded = tokens[tokens["drop_reason"].fillna("").eq("upos_excluded")]
    return _label_shares(tokens, excluded, "upos")


def _excluded_deprel_rows(tokens: pd.DataFrame, section: Mapping) -> pd.DataFrame:
    return tokens[
        tokens["upos"].isin(section["upos_keep"])
        & ~tokens["deprel_base"].isin(section["deprel_keep"])
    ]


def _excluded_deprel_by_label(tokens: pd.DataFrame, section: Mapping) -> pd.DataFrame:
    """Per-document census of the excluded-deprel category, by label.

    Counts **retained-UPOS tokens whose `deprel_base` is outside the 23**, not the
    tokens that were dropped. The two coincide under the primary `drop` policy but
    not under `oth`, where the same tokens are kept as `UPOS:oth`. GATE-A sizes the
    affected category so that D06 can decide what to do with it, so it must read
    the same in both cells — otherwise the gate could never fire in precisely the
    `(ud23_oth, ·)` cells D50 makes mandatory to interpret.
    """
    return _label_shares(tokens, _excluded_deprel_rows(tokens, section), "deprel_base")


def _label_shares(
    tokens: pd.DataFrame, subset: pd.DataFrame, label: str, key: str = "doc_id"
) -> pd.DataFrame:
    """Counts per (`key`, label) with the share of **all raw tokens** under that key."""
    raw_totals = tokens.groupby(["language", key], sort=True).size()
    out = (
        subset.groupby(["language", key, label], sort=True)
        .size()
        .reset_index(name="n")
    )
    denominators = out.set_index(["language", key]).index.map(raw_totals)
    out["share_of_raw"] = out["n"].to_numpy() / denominators.to_numpy()
    return out


def _restricted_fraction(labelled: pd.DataFrame, cfg: Mapping) -> pd.DataFrame:
    """Fraction of evaluated positions meeting D35's `available_past >= 4`, per regime."""
    minimum = cfg["scores"]["min_available_past"]
    evaluated = labelled[labelled["kept"]]
    qualifying = evaluated.assign(
        _qualifies=evaluated["available_past"] >= minimum
    )
    out = (
        qualifying.groupby(["language", "regime"], sort=True)
        .agg(n_evaluated=("_qualifies", "size"), n_restricted=("_qualifies", "sum"))
        .reset_index()
    )
    out["fraction"] = out["n_restricted"] / out["n_evaluated"]
    out["min_available_past"] = minimum
    return out


def _gate_a(labelled: pd.DataFrame, section: Mapping) -> dict:
    """GATE-A (D06/D50): any excluded-deprel label above the threshold **in a regime**.

    Denominator: every raw syntactic word of the regime. Evaluated per label, not
    on the summed excluded total — D06's escalation names a category, and the
    drop-vs-`oth` alternative it offers exists only for excluded deprels, so the
    D05 UPOS deletions (which have no alternative policy) are outside the gate.

    **Regime scope.** The census (`shares`) covers every regime, EXCLUDED among
    them; the **verdict** (`fired`/`triggers`) is read over the analysed regimes
    only. The two differ because they answer different questions: publishing the
    evidence costs nothing and hiding it would be its own distortion, whereas
    firing GATE-A binds the whole design — D50 gives the `(ud23_oth, ·)` cells
    mandatory-interpretation status and puts a declared caveat on *every primary
    conclusion*. Deriving that from a document assigned EXCLUDED, which enters no
    conclusion, would make the report less accurate rather than more cautious.
    `excluded_regimes` records the scope in the returned dict so the report can
    state it instead of leaving a reader to infer it from a row count.

    **Exploratory regimes keep their firing power — by decision, not by omission.**
    The narrowing stops at D04's disposal label. OTHER_VERSE and PROSE_POST are
    *analysed* (§1.4: specificity check, chronological-robustness set), so an
    imbalance there is evidence about the mapping the primary contrast also uses,
    and D06's category is a property of the annotation, not of one regime's role.
    This is the reading that can actually bind: at the pre-audit the largest share
    anywhere is OTHER_VERSE `vocative` at 1.28% — against HEX 0.52% and
    PROSE_CLASS 0.18% — so tragedy, not the epic invocations D06 anticipated, is
    what sits nearest the 2% threshold. Under a primary contrast that excludes
    them (D55 option A) a trigger there would still put D50's caveat on every
    primary conclusion; that consequence is accepted deliberately, and the scope
    is a ratification question (D55 §xiii), never something to change in code.

    **Language scope.** Shares are per `(language, regime)`: the denominators are
    per language because |A|, T* and the inferential families are (§4.1, §4.2,
    §5.7), and pooling would dilute a Latin excess against the far larger Greek
    tally. The verdict, however, is **one per run** — a trigger in either language
    fires the gate for the whole design, since D06 escalates the excluded-deprel
    *policy*, which is shared by both languages and by every cell of §5.6.
    """
    declared = section["gate_a_threshold"]
    if declared != GATE_A_THRESHOLD:
        raise ValueError(
            f"alphabet.gate_a_threshold is {declared!r}, not {GATE_A_THRESHOLD}: the "
            "GATE-A threshold is a constant (§3.4, D06) like GATE_B_RETENTION, and a "
            "config that moved it would change a gate verdict without changing the "
            "gate. The key survives in config/default.yaml only because config/ is "
            "frozen until the ratification act (D55 checklist item 18)"
        )
    threshold = GATE_A_THRESHOLD
    shares = _label_shares(
        labelled, _excluded_deprel_rows(labelled, section), "deprel_base", key="regime"
    )
    in_scope = ~shares["regime"].isin(GATE_A_VERDICT_EXCLUDES)
    triggers = shares[in_scope & (shares["share_of_raw"] > threshold)].reset_index(
        drop=True
    )
    return {
        "status": "evaluated",
        "threshold": threshold,
        "fired": not triggers.empty,
        "shares": shares,
        "triggers": triggers,
        "excluded_regimes": list(GATE_A_VERDICT_EXCLUDES),
    }


def _gate_b(retention: pd.DataFrame) -> dict:
    """GATE-B (§3.4): any document below `GATE_B_RETENTION` is flagged for inspection.

    Scope is deliberately **not** narrowed the way GATE-A's verdict is: §3.4 asks
    for a flag, not an escalation, and the flag names the document it is about. An
    EXCLUDED document with implausible retention is evidence about the *mapping*,
    which is worth a human's attention wherever it occurs; the cost of looking is
    one inspection, not a change to the design. The distinguishing principle: a
    gate whose firing changes the study is read over the material the study
    analyses; a gate that only asks someone to look may look everywhere.
    """
    flagged = retention[retention["retention"] < GATE_B_RETENTION].reset_index(drop=True)
    return {
        "status": "evaluated",
        "threshold": GATE_B_RETENTION,
        "fired": not flagged.empty,
        "flagged": flagged,
    }
