"""G1 audit tables, gates and alphabet inventory (Spec §3.4; D05–D09, D35, D50).

Marked `g1`, never `g0`: no D52(ii) mandatory-coverage area names these cases, and
`tests/test_alphabet.py` carries the module-level `pytest.mark.g0` for §3.4's
*mapping* — which is why they live in their own file. The `g1` marker (D55 §xiv,
convention 13; PROPOSED) puts them under the same enforcement as G0: root
`conftest.py` fails the run if any of them is skipped, `xfail`, `xpass`, or
collected without an executed assertion. Canonical command:
`uv run pytest -m g1 --strict-markers`.

Test counts are recorded in one place only (`docs/HANDOFF.md`); they are not
repeated here, because a figure transcribed into a docstring goes stale silently
— as it did at 142.

Never delete or weaken a test to make it pass.
"""

import copy

import pandas as pd
import pytest

from hexis import alphabet
from hexis.config import resolve_config

pytestmark = pytest.mark.g1

C0 = resolve_config()

RAW_COLUMNS = ("language", "doc_id", "sent_id", "token_ord", "upos_raw", "deprel_raw")


def raw_frame(rows):
    """Build a raw token table; `rows` are (doc_id, sent_id, upos_raw, deprel_raw)."""
    records = []
    ordinals: dict = {}
    for doc_id, sent_id, upos_raw, deprel_raw in rows:
        ordinals[sent_id] = ordinals.get(sent_id, 0) + 1
        records.append(
            {
                "language": "grc",
                "doc_id": doc_id,
                "sent_id": sent_id,
                "token_ord": ordinals[sent_id],
                "upos_raw": upos_raw,
                "deprel_raw": deprel_raw,
            }
        )
    return pd.DataFrame(records, columns=list(RAW_COLUMNS))


def repeat(doc_id, sent_id, upos_raw, deprel_raw, n):
    return [(doc_id, sent_id, upos_raw, deprel_raw)] * n


# --- map_tokens: the table-level application of §3.4 ------------------------------


def test_map_tokens_produces_the_spec_columns_and_totality():
    """§3.7 column set (symbol_id excluded: ids exist only after the G1 freeze)."""
    raw = raw_frame(
        [
            ("d1", "d1@1", "NOUN", "nsubj"),
            ("d1", "d1@1", "PUNCT", "punct"),
            ("d1", "d1@1", "NOUN", "vocative"),
        ]
    )
    mapped = alphabet.map_tokens(raw, C0)

    for column in ("upos", "deprel_base", "kept", "symbol", "drop_reason", "available_past"):
        assert column in mapped.columns
    assert len(mapped) == len(raw)
    assert list(mapped["kept"]) == [True, False, False]
    # §3.7 declares symbol/drop_reason nullable; the invariant of MappedToken is
    # kept <=> symbol present <=> drop_reason absent.
    assert list(mapped["symbol"].isna()) == [False, True, True]
    assert mapped["symbol"].iloc[0] == "NOUN:nsubj"
    assert list(mapped["drop_reason"].isna()) == [True, False, False]
    assert list(mapped["drop_reason"].iloc[1:]) == [
        "upos_excluded",
        "deprel_excluded:vocative",
    ]


def test_available_past_counts_retained_predecessors_within_the_sentence():
    """D35 evaluates positions by retained past, and deletions close gaps (D05)."""
    raw = raw_frame(
        [
            ("d1", "d1@1", "NOUN", "nsubj"),
            ("d1", "d1@1", "PUNCT", "punct"),  # dropped: must not advance the count
            ("d1", "d1@1", "VERB", "root"),
            ("d1", "d1@2", "NOUN", "obj"),  # new sentence: P-RESET restarts the past
        ]
    )
    mapped = alphabet.map_tokens(raw, C0)

    retained = mapped[mapped["kept"]]
    assert list(retained["available_past"]) == [0, 1, 0]


# --- observed_alphabet ------------------------------------------------------------


def test_observed_alphabet_orders_ids_by_descending_pooled_frequency():
    """§3.4: integer ids by descending pooled frequency."""
    raw = raw_frame(
        repeat("d1", "d1@1", "NOUN", "nsubj", 3)
        + repeat("d1", "d1@2", "VERB", "root", 5)
        + repeat("d1", "d1@3", "ADV", "advmod", 1)
    )
    ids = alphabet.observed_alphabet(alphabet.map_tokens(raw, C0), C0, language="grc")

    assert ids == {"VERB:root": 0, "NOUN:nsubj": 1, "ADV:advmod": 2}


def test_observed_alphabet_breaks_frequency_ties_by_symbol():
    """Declared tie-break (-frequency, symbol): equal counts must not order by chance."""
    raw = raw_frame(
        repeat("d1", "d1@1", "VERB", "root", 2)
        + repeat("d1", "d1@2", "ADV", "advmod", 2)
        + repeat("d1", "d1@3", "NOUN", "nsubj", 2)
    )
    ids = alphabet.observed_alphabet(alphabet.map_tokens(raw, C0), C0, language="grc")

    assert ids == {"ADV:advmod": 0, "NOUN:nsubj": 1, "VERB:root": 2}


def test_observed_alphabet_excludes_dropped_tokens():
    raw = raw_frame(
        [
            ("d1", "d1@1", "NOUN", "nsubj"),
            ("d1", "d1@1", "PUNCT", "punct"),
            ("d1", "d1@1", "NOUN", "vocative"),
        ]
    )
    ids = alphabet.observed_alphabet(alphabet.map_tokens(raw, C0), C0, language="grc")

    assert ids == {"NOUN:nsubj": 0}


def test_observed_alphabet_rejects_a_two_language_table():
    """§4.1: |A| is the alphabet size for the (language, variant) pair — never pooled."""
    raw = raw_frame([("d1", "d1@1", "NOUN", "nsubj")])
    latin = raw_frame([("d2", "d2@1", "VERB", "root")])
    latin["language"] = "la"
    mixed = alphabet.map_tokens(pd.concat([raw, latin], ignore_index=True), C0)

    with pytest.raises(ValueError, match="language") as caught:
        alphabet.observed_alphabet(mixed, C0, language="grc")

    # Asserted, not merely raised: `pytest.raises` executes no Python assert, so
    # the gate would count this test as assertion-free (D52(iii)). The message
    # must name the foreign language, or the operator cannot act on it.
    assert "'la'" in str(caught.value)
    assert "'grc'" in str(caught.value)


def test_observed_alphabet_writes_nothing(tmp_path, monkeypatch):
    """The inventory is read at the pre-audit; the freeze is a separate, later act."""
    monkeypatch.chdir(tmp_path)
    raw = raw_frame([("d1", "d1@1", "NOUN", "nsubj")])

    alphabet.observed_alphabet(alphabet.map_tokens(raw, C0), C0, language="grc")

    assert list(tmp_path.iterdir()) == []


# --- run_audit: tables ------------------------------------------------------------


def test_contingency_totals_reconcile_with_the_raw_token_count():
    """§3.4: the contingency is over *raw* UPOS×DEPREL — every row is counted once."""
    raw = raw_frame(
        repeat("d1", "d1@1", "NOUN", "nsubj", 4)
        + repeat("d1", "d1@2", "PUNCT", "punct", 3)
        + repeat("d2", "d2@1", "VERB", "root", 5)
    )
    audit = alphabet.run_audit(alphabet.map_tokens(raw, C0), C0)

    assert audit["contingency"]["n"].sum() == len(raw)
    per_doc = audit["contingency"].groupby("doc_id")["n"].sum().to_dict()
    assert per_doc == {"d1": 7, "d2": 5}


def test_contingency_keeps_raw_subtypes_visible():
    """Step 1 strips subtypes for the symbol; the audit must still show the raw label."""
    raw = raw_frame([("d1", "d1@1", "NOUN", "nsubj:pass")])
    audit = alphabet.run_audit(alphabet.map_tokens(raw, C0), C0)

    row = audit["contingency"].iloc[0]
    assert row["deprel_raw"] == "nsubj:pass"
    assert row["deprel_base"] == "nsubj"


def test_retention_and_drop_by_rule_partition_the_raw_tokens():
    raw = raw_frame(
        repeat("d1", "d1@1", "NOUN", "nsubj", 6)
        + repeat("d1", "d1@2", "PUNCT", "punct", 3)
        + repeat("d1", "d1@3", "NOUN", "vocative", 1)
    )
    audit = alphabet.run_audit(alphabet.map_tokens(raw, C0), C0)
    row = audit["retention"].set_index("doc_id").loc["d1"]

    assert row["n_raw"] == 10
    assert row["n_kept"] == 6
    assert row["n_upos_excluded"] == 3
    assert row["n_deprel_excluded"] == 1
    assert row["retention"] == pytest.approx(0.6)


def test_excluded_deprel_shares_use_the_raw_token_denominator():
    """GATE-A's denominator is all raw syntactic words, not the excluded subtotal."""
    raw = raw_frame(
        repeat("d1", "d1@1", "NOUN", "nsubj", 96)
        + repeat("d1", "d1@2", "NOUN", "vocative", 3)
        + repeat("d1", "d1@3", "NOUN", "flat", 1)
    )
    audit = alphabet.run_audit(alphabet.map_tokens(raw, C0), C0)
    shares = (
        audit["excluded_deprel_by_label"].set_index("deprel_base")["share_of_raw"].to_dict()
    )

    assert shares["vocative"] == pytest.approx(0.03)
    assert shares["flat"] == pytest.approx(0.01)


def test_excluded_deprel_census_is_independent_of_the_drop_or_oth_policy():
    """GATE-A sizes the affected category; D06 chooses what to *do* with it.

    Under `oth` the tokens are retained, so counting drops would make the gate
    unable to fire in exactly the cells D50 makes mandatory to interpret.
    """
    oth = resolve_config(
        {"alphabet": {"variant": "ud23_oth", "excluded_deprel_policy": "oth"}}
    )
    raw = raw_frame(
        repeat("d1", "d1@1", "NOUN", "nsubj", 97) + repeat("d1", "d1@2", "NOUN", "vocative", 3)
    )

    drop_share = alphabet.run_audit(alphabet.map_tokens(raw, C0), C0)[
        "excluded_deprel_by_label"
    ]["share_of_raw"].iloc[0]
    oth_share = alphabet.run_audit(alphabet.map_tokens(raw, oth), oth)[
        "excluded_deprel_by_label"
    ]["share_of_raw"].iloc[0]

    assert drop_share == pytest.approx(oth_share) == pytest.approx(0.03)


# --- run_audit: gates -------------------------------------------------------------


def regimes_for(mapping):
    return dict(mapping)


def test_gate_a_fires_above_two_percent_of_raw_tokens_in_a_regime():
    raw = raw_frame(
        repeat("hex1", "hex1@1", "NOUN", "nsubj", 97)
        + repeat("hex1", "hex1@2", "NOUN", "vocative", 3)
        + repeat("pro1", "pro1@1", "NOUN", "nsubj", 100)
    )
    audit = alphabet.run_audit(
        alphabet.map_tokens(raw, C0),
        C0,
        regimes=regimes_for({"hex1": "HEX", "pro1": "PROSE_CLASS"}),
    )

    assert audit["gate_a"]["status"] == "evaluated"
    assert audit["gate_a"]["fired"] is True
    triggers = audit["gate_a"]["triggers"]
    assert list(triggers["regime"]) == ["HEX"]
    assert list(triggers["deprel_base"]) == ["vocative"]
    assert triggers["share_of_raw"].iloc[0] == pytest.approx(0.03)


def test_gate_a_does_not_fire_at_exactly_two_percent():
    """D06 escalates on *strictly* more than 2%; the boundary must not escalate."""
    raw = raw_frame(
        repeat("hex1", "hex1@1", "NOUN", "nsubj", 98)
        + repeat("hex1", "hex1@2", "NOUN", "vocative", 2)
    )
    audit = alphabet.run_audit(
        alphabet.map_tokens(raw, C0), C0, regimes=regimes_for({"hex1": "HEX"})
    )

    assert audit["gate_a"]["status"] == "evaluated"
    assert audit["gate_a"]["fired"] is False
    assert audit["gate_a"]["triggers"].empty


@pytest.mark.parametrize("moved", [0.9, 0.002])
def test_a_config_that_moves_the_gate_a_threshold_is_refused(moved):
    """The threshold is a constant (§3.4, D06), as `GATE_B_RETENTION` always was.

    It used to be read straight from config, and `config.check_against_default`
    inspects key presence only — never a value — so `gate_a_threshold: 0.9`
    disarmed the gate and the run reported `fired: False` on the same corpus that
    fires it at 0.02. Both directions are refused: 0.002 fabricates a trigger just
    as silently as 0.9 suppresses one.
    """
    config = copy.deepcopy(C0)
    config["alphabet"]["gate_a_threshold"] = moved
    raw = raw_frame(
        repeat("hex1", "hex1@1", "NOUN", "nsubj", 97)
        + repeat("hex1", "hex1@2", "NOUN", "vocative", 3)
    )

    with pytest.raises(ValueError) as caught:
        alphabet.run_audit(
            alphabet.map_tokens(raw, config),
            config,
            regimes=regimes_for({"hex1": "HEX"}),
        )

    assert "gate_a_threshold" in str(caught.value)
    assert str(moved) in str(caught.value)


def test_gate_a_aggregates_over_the_regime_not_the_document():
    """Two documents each below 2% can still put their regime above it."""
    raw = raw_frame(
        repeat("hex1", "hex1@1", "NOUN", "nsubj", 97)
        + repeat("hex1", "hex1@2", "NOUN", "vocative", 3)
        + repeat("hex2", "hex2@1", "NOUN", "nsubj", 97)
        + repeat("hex2", "hex2@2", "NOUN", "vocative", 3)
    )
    mapped = alphabet.map_tokens(raw, C0)
    audit = alphabet.run_audit(
        mapped, C0, regimes=regimes_for({"hex1": "HEX", "hex2": "HEX"})
    )

    assert audit["gate_a"]["fired"] is True
    assert audit["gate_a"]["triggers"]["share_of_raw"].iloc[0] == pytest.approx(0.03)


def test_gate_a_verdict_ignores_the_excluded_regime_but_still_reports_it():
    """Declared reading 3. An EXCLUDED document enters no estimand, and firing
    GATE-A is not a precaution but a binding change (D50: mandatory-interpretation
    status for the `oth` cells, a caveat on every primary conclusion). Deriving
    that from material the study does not analyse would make the report wrong.

    The census must still carry the row: withholding a verdict is not a licence to
    hide the evidence it was withheld from."""
    raw = raw_frame(
        repeat("vulg", "vulg@1", "NOUN", "nsubj", 90)
        + repeat("vulg", "vulg@2", "NOUN", "vocative", 10)  # 10% — far above 2%
        + repeat("hex1", "hex1@1", "NOUN", "nsubj", 100)
    )
    audit = alphabet.run_audit(
        alphabet.map_tokens(raw, C0),
        C0,
        regimes=regimes_for({"vulg": "EXCLUDED", "hex1": "HEX"}),
    )

    assert audit["gate_a"]["fired"] is False
    assert audit["gate_a"]["triggers"].empty
    assert audit["gate_a"]["excluded_regimes"] == ["EXCLUDED"]
    census = audit["gate_a"]["shares"]
    row = census[census["regime"] == "EXCLUDED"]
    assert list(row["deprel_base"]) == ["vocative"]
    assert row["share_of_raw"].iloc[0] == pytest.approx(0.10)


def test_gate_a_still_fires_on_an_analysed_regime_when_excluded_is_present():
    """The converse guard: narrowing the verdict must not disarm the gate itself."""
    raw = raw_frame(
        repeat("vulg", "vulg@1", "NOUN", "vocative", 100)
        + repeat("hex1", "hex1@1", "NOUN", "nsubj", 97)
        + repeat("hex1", "hex1@2", "NOUN", "vocative", 3)
    )
    audit = alphabet.run_audit(
        alphabet.map_tokens(raw, C0),
        C0,
        regimes=regimes_for({"vulg": "EXCLUDED", "hex1": "HEX"}),
    )

    assert audit["gate_a"]["fired"] is True
    assert list(audit["gate_a"]["triggers"]["regime"]) == ["HEX"]


def test_gate_a_fires_from_an_exploratory_regime():
    """Declared reading 4. The narrowing of reading 3 stops at the disposal label:
    OTHER_VERSE and PROSE_POST are analysed (§1.4), so they keep their firing power
    even where the primary contrast excludes them. Not hypothetical — at the
    pre-audit the largest share anywhere is OTHER_VERSE `vocative` (1.28%), above
    both primary regimes, so this is the reading that can actually bind."""
    raw = raw_frame(
        repeat("trag", "trag@1", "NOUN", "nsubj", 97)
        + repeat("trag", "trag@2", "NOUN", "vocative", 3)
        + repeat("hex1", "hex1@1", "NOUN", "nsubj", 100)
    )
    audit = alphabet.run_audit(
        alphabet.map_tokens(raw, C0),
        C0,
        regimes=regimes_for({"trag": "OTHER_VERSE", "hex1": "HEX"}),
    )

    assert audit["gate_a"]["fired"] is True
    assert list(audit["gate_a"]["triggers"]["regime"]) == ["OTHER_VERSE"]
    assert "OTHER_VERSE" not in alphabet.GATE_A_VERDICT_EXCLUDES


def test_gate_a_shares_are_per_language_and_the_verdict_is_one_per_run():
    """Declared reading 5. Denominators are per (language, regime) — pooling would
    dilute a Latin excess against the far larger Greek tally — while the verdict is
    single, because D06 escalates the excluded-deprel *policy*, which both
    languages share. Here Latin alone is over the threshold and Greek alone is
    under it: pooled, the row would vanish; scoped per language, it fires."""
    grc = raw_frame(repeat("hex1", "hex1@1", "NOUN", "nsubj", 1000))
    la = raw_frame(
        repeat("lat1", "lat1@1", "NOUN", "nsubj", 97)
        + repeat("lat1", "lat1@2", "NOUN", "vocative", 3)
    )
    la["language"] = "la"
    mapped = alphabet.map_tokens(pd.concat([grc, la], ignore_index=True), C0)

    audit = alphabet.run_audit(
        mapped, C0, regimes=regimes_for({"hex1": "HEX", "lat1": "HEX"})
    )

    shares = audit["gate_a"]["shares"]
    assert set(shares["language"]) == {"la"}  # only Latin has an excluded deprel
    triggers = audit["gate_a"]["triggers"]
    assert list(triggers["language"]) == ["la"]
    assert triggers["share_of_raw"].iloc[0] == pytest.approx(0.03)
    # 3 / 1100 pooled is 0.27%, far below the threshold: the verdict below exists
    # only because the denominator is the Latin regime, not both languages.
    assert audit["gate_a"]["fired"] is True


def test_gate_b_looks_everywhere_including_the_excluded_regime():
    """GATE-B is scoped deliberately *differently* from GATE-A's verdict: §3.4 asks
    it to flag a document for inspection, and a flag naming its own document
    misleads no one. Implausible retention on an excluded text is evidence about
    the mapping, which is worth a look wherever it occurs."""
    raw = raw_frame(
        repeat("vulg", "vulg@1", "NOUN", "nsubj", 60)
        + repeat("vulg", "vulg@2", "PUNCT", "punct", 40)
    )
    audit = alphabet.run_audit(
        alphabet.map_tokens(raw, C0), C0, regimes=regimes_for({"vulg": "EXCLUDED"})
    )

    assert audit["gate_b"]["fired"] is True
    assert list(audit["gate_b"]["flagged"]["doc_id"]) == ["vulg"]


def test_gate_b_flags_a_document_below_seventy_percent_retention():
    raw = raw_frame(
        repeat("d1", "d1@1", "NOUN", "nsubj", 69)
        + repeat("d1", "d1@2", "PUNCT", "punct", 31)
        + repeat("d2", "d2@1", "NOUN", "nsubj", 70)
        + repeat("d2", "d2@2", "PUNCT", "punct", 30)
    )
    audit = alphabet.run_audit(
        alphabet.map_tokens(raw, C0),
        C0,
        regimes=regimes_for({"d1": "HEX", "d2": "HEX"}),
    )

    assert audit["gate_b"]["status"] == "evaluated"
    assert audit["gate_b"]["fired"] is True
    assert list(audit["gate_b"]["flagged"]["doc_id"]) == ["d1"]


def test_gates_are_not_evaluated_without_a_registry():
    """Pre-audit: no regime map means no gate verdict, and the reason is recorded."""
    raw = raw_frame(repeat("d1", "d1@1", "NOUN", "vocative", 100))
    audit = alphabet.run_audit(alphabet.map_tokens(raw, C0), C0)

    for gate in ("gate_a", "gate_b"):
        assert audit[gate]["status"] == "not_evaluated"
        assert "fired" not in audit[gate]
        assert audit[gate]["reason"]
    assert "by_regime" not in audit
    assert "restricted_fraction" not in audit


def test_map_tokens_handles_an_empty_table():
    """§7 lists the empty case; `kept` must stay a boolean mask, not become object."""
    mapped = alphabet.map_tokens(raw_frame([]), C0)

    assert len(mapped) == 0
    assert mapped["kept"].dtype == bool
    assert alphabet.observed_alphabet(mapped, C0, language="grc") == {}


def test_freeze_alphabet_remains_a_declared_but_unimplemented_api():
    """§6.2 binds `alphabet.freeze_alphabet`. Not implementing it is a choice;
    deleting it would be a silent deviation from the carried-unchanged API list."""
    assert callable(alphabet.freeze_alphabet)

    with pytest.raises(NotImplementedError, match="G1"):
        alphabet.freeze_alphabet(alphabet.map_tokens(raw_frame([]), C0), C0)


def test_drop_rates_by_rule_are_available_per_regime():
    """T2 (§8) asks for drop rates by rule *and regime*."""
    raw = raw_frame(
        repeat("hex1", "hex1@1", "NOUN", "nsubj", 8)
        + repeat("hex1", "hex1@2", "PUNCT", "punct", 1)
        + repeat("hex1", "hex1@3", "NOUN", "vocative", 1)
        + repeat("pro1", "pro1@1", "NOUN", "nsubj", 10)
    )
    audit = alphabet.run_audit(
        alphabet.map_tokens(raw, C0),
        C0,
        regimes=regimes_for({"hex1": "HEX", "pro1": "PROSE_CLASS"}),
    )
    row = audit["retention_by_regime"].set_index("regime").loc["HEX"]

    assert row["n_raw"] == 10
    assert row["n_kept"] == 8
    assert row["upos_excluded_rate"] == pytest.approx(0.1)
    assert row["deprel_excluded_rate"] == pytest.approx(0.1)
    assert row["retention"] == pytest.approx(0.8)


def test_restricted_position_fraction_is_reported_per_regime():
    """D35: the fraction of positions with available_past >= 4, per regime."""
    raw = raw_frame(
        repeat("hex1", "hex1@1", "NOUN", "nsubj", 10)  # positions 0..9 → 6 qualify
        + repeat("pro1", "pro1@1", "NOUN", "nsubj", 4)  # positions 0..3 → none qualify
    )
    audit = alphabet.run_audit(
        alphabet.map_tokens(raw, C0),
        C0,
        regimes=regimes_for({"hex1": "HEX", "pro1": "PROSE_CLASS"}),
    )
    fractions = audit["restricted_fraction"].set_index("regime")["fraction"].to_dict()

    assert fractions["HEX"] == pytest.approx(0.6)
    assert fractions["PROSE_CLASS"] == pytest.approx(0.0)


def test_run_audit_rejects_a_regime_map_missing_a_document():
    """§3.3: the audit fails on any unassigned sentence — never silently drops one."""
    raw = raw_frame(
        [("d1", "d1@1", "NOUN", "nsubj"), ("d2", "d2@1", "NOUN", "nsubj")]
    )

    with pytest.raises(ValueError, match="d2") as caught:
        alphabet.run_audit(
            alphabet.map_tokens(raw, C0), C0, regimes=regimes_for({"d1": "HEX"})
        )

    # The message names the document that is missing, and only that one.
    assert "d2" in str(caught.value)
    assert "'d1'" not in str(caught.value)


def test_oth_policy_keeps_the_absorbed_label_visible_to_the_audit():
    """D06 sensitivity arm: `oth` retains the token, and the audit still sees why."""
    oth = resolve_config(
        {"alphabet": {"variant": "ud23_oth", "excluded_deprel_policy": "oth"}}
    )
    raw = raw_frame(
        repeat("d1", "d1@1", "NOUN", "nsubj", 8) + repeat("d1", "d1@2", "NOUN", "vocative", 2)
    )
    audit = alphabet.run_audit(alphabet.map_tokens(raw, oth), oth)
    row = audit["retention"].set_index("doc_id").loc["d1"]

    assert row["n_kept"] == 10
    assert row["n_deprel_excluded"] == 0
    assert "NOUN:oth" in alphabet.observed_alphabet(
        alphabet.map_tokens(raw, oth), oth, language="grc"
    )
