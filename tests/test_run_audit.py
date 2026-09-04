"""The G1 audit stage: modes, artifacts, provenance (Spec §3.3, §6.1, §6.4; D46).

Marked `g1`, never `g0` — the attested G0 selection is closed. The `g1` marker
(D55 §xiv, convention 13; ratified 2026-09-04) puts these cases under the same enforcement
as G0: root `conftest.py` fails the run if any is skipped, `xfail`, `xpass`, or
collected without an executed assertion. Canonical command:
`uv run pytest -m g1 --strict-markers`. Hence the `as caught` idiom below —
`pytest.raises` alone executes no Python assert, so a test that only expects an
exception does not, by itself, satisfy the gate.

The stage is driven over a synthetic mini-corpus through `--data-root`, never
over `data/raw/`: these tests must not depend on licensed data being present.

Never delete or weaken a test to make it pass.
"""

import hashlib
import json
import shutil
from pathlib import Path

import pytest
import yaml

from hexis import registry
from hexis.manifest import build_manifest
from hexis.pipeline import run_audit

pytestmark = pytest.mark.g1

ENTRY_POINT_FOR_TEST = "hexis.pipeline.run_audit"

# `--config` is resolved by walking up from the working directory, so the one test
# that changes directory has to name it explicitly.
REPO_CONFIG = Path(__file__).resolve().parents[1] / "config" / "default.yaml"

_T = "\t"


def _row(*cols):
    return _T.join(cols)


def _sentence(sent_id, tokens):
    lines = [f"# sent_id = {sent_id}"]
    for index, (upos, deprel) in enumerate(tokens, start=1):
        lines.append(_row(str(index), "w", "w", upos, "_", "_", "0", deprel, "_", "_"))
    return "\n".join(lines) + "\n"


MINI_GRC = (
    _sentence("alpha.tb.xml@1", [("NOUN", "nsubj"), ("VERB", "root"), ("PUNCT", "punct")])
    + "\n"
    + _sentence("alpha.tb.xml@2", [("ADV", "advmod"), ("VERB", "root")])
    + "\n"
    + _sentence("beta.tb.xml@1", [("NOUN", "nsubj"), ("NOUN", "vocative")])
    + "\n"
)

# `corpus.languages` is [grc, la], and a treebank that is simply absent must not
# yield a complete-looking audit of half the corpus — so the fixture carries both.
MINI_LA = _sentence("gamma.tb.xml@1", [("NOUN", "nsubj"), ("VERB", "root")]) + "\n"

ASSIGNMENTS = {
    "_status": "RATIFIED",
    "alpha.tb.xml": {
        "author": "Alpha",
        "work": "Alpha Work",
        "regime": "HEX",
        "meter": "hexameter",
        "period": "archaic",
    },
    "beta.tb.xml": {
        "author": "Beta",
        "work": "Beta Work",
        "regime": "PROSE_CLASS",
        "meter": "prose",
        "period": "classical",
    },
    "gamma.tb.xml": {
        "author": "Gamma",
        "work": "Gamma Work",
        "regime": "HEX",
        "meter": "hexameter",
        "period": "classical",
    },
}

DOCS = ("alpha.tb.xml", "beta.tb.xml", "gamma.tb.xml")


def assignments_with(**changes):
    """ASSIGNMENTS with per-document edits; a value of None drops the key."""
    out = {key: dict(value) if isinstance(value, dict) else value
           for key, value in ASSIGNMENTS.items()}
    for doc, edits in changes.items():
        if edits is None:
            out.pop(doc, None)
            continue
        for field, value in edits.items():
            if value is None:
                out[doc].pop(field, None)
            else:
                out[doc][field] = value
    return out


def config_with(**corpus_overrides):
    """The repo config with `corpus:` keys replaced — written to a temp file."""
    config = yaml.safe_load(REPO_CONFIG.read_text(encoding="utf-8"))
    config["corpus"].update(corpus_overrides)
    return config


@pytest.fixture
def corpus(tmp_path, monkeypatch):
    """A mini treebank plus an empty and a complete overrides file."""
    data_root = tmp_path / "raw"
    (data_root / "UD_Mini").mkdir(parents=True)
    grc = data_root / "UD_Mini" / "grc_mini-ud-train.conllu"
    la = data_root / "UD_Mini" / "la_mini-ud-train.conllu"
    grc.write_text(MINI_GRC, encoding="utf-8")
    la.write_text(MINI_LA, encoding="utf-8")

    empty = tmp_path / "empty_overrides.yaml"
    empty.write_text("# no assignments yet\n", encoding="utf-8")

    def write(payload, name):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(payload), encoding="utf-8")
        return path

    provenance = tmp_path / "PROVENANCE.md"

    def refresh_provenance():
        provenance.write_text(
            "# Test provenance\n\n"
            "| Field | UD_Mini |\n|---|---|\n"
            "| UD release tag (pinned, D03) | r2.18 |\n\n"
            "| file | sha256 |\n|---|---|\n"
            + "".join(
                f"| {path.name} | `{hashlib.sha256(path.read_bytes()).hexdigest()}` |\n"
                for path in sorted(data_root.rglob("*.conllu"))
            ),
            encoding="utf-8",
        )

    refresh_provenance()
    complete = write(ASSIGNMENTS, "config/registry_overrides.yaml")
    monkeypatch.setattr(run_audit, "CANONICAL_OVERRIDES", complete.resolve(), raising=False)
    monkeypatch.setattr(
        run_audit, "git_state", lambda: {"commit": "a" * 40, "dirty": False}
    )

    return {
        "data_root": data_root,
        "results_root": tmp_path / "results",
        "empty": empty,
        "complete": complete,
        "provenance": provenance,
        "refresh_provenance": refresh_provenance,
        "write_overrides": write,
        "tmp_path": tmp_path,
    }


def invoke(corpus, *extra):
    return run_audit.main(
        [
            "--data-root",
            str(corpus["data_root"]),
            "--results-root",
            str(corpus["results_root"]),
            "--provenance",
            str(corpus["provenance"]),
            *extra,
        ]
    )


def read_report(result):
    return result["report_path"].read_text(encoding="utf-8")


# --- modes ------------------------------------------------------------------------


def test_canonical_mode_fails_loud_on_an_unassigned_sentence(corpus):
    """§3.3: the audit fails on any unassigned sentence. That is the default."""
    with pytest.raises(ValueError, match="alpha.tb.xml"):
        invoke(corpus, "--overrides", str(corpus["empty"]))

    assert not corpus["results_root"].exists()


def test_pre_audit_stamps_the_report_incomplete_and_withholds_every_verdict(corpus):
    result = invoke(corpus, "--pre-audit", "--overrides", str(corpus["empty"]))
    report = read_report(result)

    assert "INCOMPLETE / PENDING_REGISTRY" in report
    assert "GATE-A: NOT EVALUATED" in report
    assert "GATE-B: NOT EVALUATED" in report
    assert "T*: not computed" in report
    assert result["gates_evaluated"] is False


def test_registry_is_validated_not_merely_indexed(corpus):
    """An invalid regime must reach `build_registry`, which is what rejects it.

    Reading `overrides[doc_id]["regime"]` straight into the aggregates validates
    nothing; the bad label would simply become a grouping key.
    """
    bad = {**ASSIGNMENTS, "beta.tb.xml": {**ASSIGNMENTS["beta.tb.xml"], "regime": "NOT_A_REGIME"}}
    path = corpus["write_overrides"](bad, "bad_regime.yaml")

    with pytest.raises(ValueError, match="NOT_A_REGIME") as caught:
        invoke(corpus, "--overrides", str(path))

    # Asserted, not merely raised (D52(iii)): the message must name the offending
    # label *and* the document, and the refused run must have written nothing.
    assert "beta.tb.xml" in str(caught.value)
    assert not corpus["results_root"].exists()


def test_a_missing_required_field_is_rejected(corpus):
    incomplete = {**ASSIGNMENTS, "beta.tb.xml": {"author": "Beta", "regime": "HEX"}}
    path = corpus["write_overrides"](incomplete, "missing_fields.yaml")

    with pytest.raises(ValueError, match="missing") as caught:
        invoke(corpus, "--overrides", str(path))

    # Every absent required field is named, not just the first one found.
    for field in ("work", "meter", "period"):
        assert field in str(caught.value), field


@pytest.mark.parametrize(
    "broken, expected",
    [
        ({"regime": "NOT_A_REGIME"}, "NOT_A_REGIME"),
        ({"author": None, "regime": None, "meter": None, "period": None}, "missing"),
        ({"canonical_doc_id": "nobody_else_points_here"}, "canonical_doc_id"),
    ],
    ids=["invalid-regime", "missing-field", "invalid-merge"],
)
def test_an_incomplete_registry_still_validates_the_rows_it_has(corpus, broken, expected):
    """`--pre-audit` tolerates absence, never error.

    Returning early on the first missing assignment would let a bad regime label,
    a missing field or a broken merge sit unnoticed in the proposal until the day
    it is ratified.
    """
    assignment = {k: v for k, v in ASSIGNMENTS["alpha.tb.xml"].items()}
    assignment.update({k: v for k, v in broken.items() if v is not None})
    for key, value in broken.items():
        if value is None:
            assignment.pop(key, None)
    partial = {"alpha.tb.xml": assignment}  # beta.tb.xml deliberately unassigned
    path = corpus["write_overrides"](partial, "partial_broken.yaml")

    with pytest.raises(ValueError, match=expected) as caught:
        invoke(corpus, "--pre-audit", "--overrides", str(path))

    # The row that is *absent* must not be what the error is about: the point of
    # this test is that the rows present were validated, not that one is missing.
    assert expected in str(caught.value)
    assert "beta.tb.xml" not in str(caught.value)


ABSENT = object()


@pytest.mark.parametrize(
    "status",
    [ABSENT, None, "PROPOSED", "", "ratified", "UNVERIFIED"],
    ids=["absent", "yaml-null", "PROPOSED", "empty", "wrong-case", "UNVERIFIED"],
)
def test_only_an_explicitly_ratified_file_produces_a_canonical_audit(
    corpus, status, monkeypatch
):
    """Ratification is opt-in. Silence is not consent, and neither is a typo.

    `ABSENT` is the case that matters most — an overrides file with no `_status`
    at all is the default shape — and `None` is the distinct YAML `_status: null`,
    which reads back as a present-but-empty declaration.
    """
    payload = assignments_with()
    if status is ABSENT:
        payload.pop("_status")
    else:
        payload["_status"] = status
    path = corpus["write_overrides"](payload, f"status_{id(status)}.yaml")
    monkeypatch.setattr(run_audit, "CANONICAL_OVERRIDES", path.resolve())
    if status is None:
        assert "_status: null" in path.read_text(encoding="utf-8")

    with pytest.raises(ValueError, match="_status"):
        invoke(corpus, "--overrides", str(path))

    # Every one of them is fine in the mode that declares itself incomplete.
    assert invoke(corpus, "--pre-audit", "--overrides", str(path))["has_registry"] is True


def test_a_ratified_overrides_file_runs_canonically(corpus):
    assert invoke(corpus, "--overrides", str(corpus["complete"]))["gates_evaluated"] is True


def test_canonical_mode_accepts_only_the_authoritative_registry_path(corpus):
    copy = corpus["write_overrides"](ASSIGNMENTS, "self_ratified_copy.yaml")

    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--overrides", str(copy))

    assert "config/registry_overrides.yaml" in str(caught.value)
    assert invoke(corpus, "--pre-audit", "--overrides", str(copy))["has_registry"] is True


def test_canonical_mode_requires_a_clean_repository(corpus, monkeypatch):
    monkeypatch.setattr(
        run_audit, "git_state", lambda: {"commit": "a" * 40, "dirty": True}
    )

    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--overrides", str(corpus["complete"]))

    assert "clean" in str(caught.value).lower()
    assert not corpus["results_root"].exists()


def test_force_is_pre_audit_only(corpus, monkeypatch):
    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--overrides", str(corpus["complete"]), "--force")

    assert "--force" in str(caught.value)
    monkeypatch.setattr(
        run_audit, "git_state", lambda: {"commit": "a" * 40, "dirty": True}
    )
    assert invoke(
        corpus, "--pre-audit", "--overrides", str(corpus["complete"]), "--force"
    )["mode"] == "preaudit"


def test_a_corpus_missing_a_configured_language_is_refused(corpus, tmp_path):
    """A treebank that is simply absent would yield a complete-looking half-audit."""
    (corpus["data_root"] / "UD_Mini" / "la_mini-ud-train.conllu").unlink()
    corpus["refresh_provenance"]()

    for extra in ([], ["--pre-audit"]):
        with pytest.raises(ValueError, match="configured corpus language") as caught:
            invoke(corpus, "--overrides", str(corpus["complete"]), *extra)

        # Named, so the operator knows which treebank is absent — and refused in
        # both modes, since --pre-audit excuses registry gaps, not corpus gaps.
        assert "'la'" in str(caught.value)


def test_a_single_language_audit_is_possible_only_by_configuring_it(corpus, monkeypatch):
    """The escape hatch is explicit configuration, not silent tolerance."""
    (corpus["data_root"] / "UD_Mini" / "la_mini-ud-train.conllu").unlink()
    corpus["refresh_provenance"]()
    config = corpus["write_overrides"](config_with(languages=["grc"]), "grc_only.yaml")
    overrides = corpus["write_overrides"](
        assignments_with(**{"gamma.tb.xml": None}), "grc_only_registry.yaml"
    )
    monkeypatch.setattr(run_audit, "CANONICAL_OVERRIDES", overrides.resolve())

    result = invoke(corpus, "--overrides", str(overrides), "--config", str(config))
    assert result["gates_evaluated"] is True


def test_a_missing_overrides_file_is_not_an_empty_registry(corpus):
    with pytest.raises(FileNotFoundError) as caught:
        invoke(corpus, "--pre-audit", "--overrides", str(corpus["data_root"] / "typo.yaml"))

    # The mistyped path is quoted back, which is the whole point of refusing it
    # instead of reading it as "no assignments yet".
    assert "typo.yaml" in str(caught.value)


@pytest.mark.parametrize(
    "body, expected",
    [
        ("- alpha.tb.xml\n- beta.tb.xml\n", "must be a mapping"),
        ("alpha.tb.xml: not-a-mapping\n", "not a mapping of registry fields"),
        ("1: {author: x}\n", "but keys are"),
        ("alpha: [unclosed\n", "not valid YAML"),
    ],
    ids=["top-level-list", "scalar-assignment", "non-string-key", "unparseable"],
)
def test_a_malformed_overrides_file_fails_with_its_path(corpus, body, expected):
    """A YAML list used to reach `.items()` and die on an AttributeError."""
    path = corpus["tmp_path"] / "malformed.yaml"
    path.write_text(body, encoding="utf-8")

    with pytest.raises(ValueError, match=expected) as caught:
        invoke(corpus, "--pre-audit", "--overrides", str(path))
    assert str(path) in str(caught.value)
    # Prefixing the real path is not enough: PyYAML embeds the stream name in
    # every error marker, so an unnamed stream leaves "<unicode string>" inside
    # the message next to the path that contradicts it.
    assert "<unicode string>" not in str(caught.value)


@pytest.mark.parametrize(
    "body",
    [
        "_status: PROPOSED\n_status: RATIFIED\n",
        "alpha.tb.xml:\n  author: Alpha\n  author: Other\n",
    ],
    ids=["top-level", "assignment-field"],
)
def test_duplicate_yaml_keys_are_rejected_at_any_registry_depth(corpus, body):
    path = corpus["tmp_path"] / "duplicate.yaml"
    path.write_text(body, encoding="utf-8")

    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--pre-audit", "--overrides", str(path))

    assert "duplicate" in str(caught.value).lower()
    assert str(path) in str(caught.value)


def test_the_yaml_error_names_the_original_file_and_keeps_the_snippet(corpus):
    """The staged copy is index-prefixed and lives in a temp dir that is gone by
    the time the operator reads the message, so the *original* path is the only
    one worth naming — and PyYAML's line, column and caret have to survive the
    substitution, or the fix trades one kind of blindness for another."""
    path = corpus["tmp_path"] / "unparseable.yaml"
    path.write_text("alpha: [unclosed\n", encoding="utf-8")

    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--pre-audit", "--overrides", str(path))
    message = str(caught.value)
    assert "hexis-audit-" not in message  # never the staging copy
    assert f'in "{path}", line 1, column 8' in message
    assert "alpha: [unclosed" in message and "^" in message


@pytest.mark.parametrize(
    "field", ["flag", "urn", "canonical_docid", "regimes"], ids=lambda f: f
)
def test_an_unknown_override_field_is_rejected_not_dropped(corpus, field):
    """The required five are caught by their absence; a mistyped *optional* key is
    caught by nothing, and a silently dropped `flags:` shows up in no artifact."""
    payload = assignments_with(**{"beta.tb.xml": {field: ["x"]}})
    path = corpus["write_overrides"](payload, f"stray_{field}.yaml")

    for extra in ([], ["--pre-audit"]):
        with pytest.raises(ValueError, match="unknown field") as caught:
            invoke(corpus, "--overrides", str(path), *extra)

        # "unknown field" alone does not tell the operator which key in which
        # document — which is the entire reason the key is refused.
        assert f"'{field}'" in str(caught.value)
        assert "beta.tb.xml" in str(caught.value)


def test_the_declared_schema_fields_are_all_accepted(corpus, monkeypatch):
    """`part_order` is declared in the G1 package (§viii) and read by nothing yet:
    the check must not turn "not implemented" into "not loadable"."""
    payload = assignments_with(
        **{"beta.tb.xml": {"source_urn": "urn:x", "flags": ["f"], "part_order": 12}}
    )
    path = corpus["write_overrides"](payload, "declared_fields.yaml")
    monkeypatch.setattr(run_audit, "CANONICAL_OVERRIDES", path.resolve())

    assert invoke(corpus, "--overrides", str(path))["gates_evaluated"] is True


def test_an_empty_corpus_fails_instead_of_passing_every_gate(tmp_path):
    """Zero sentences would otherwise yield a CANONICAL report with nothing in it."""
    data_root = tmp_path / "raw" / "UD_Empty"
    data_root.mkdir(parents=True)
    (data_root / "grc_empty-ud-train.conllu").write_text("", encoding="utf-8")
    overrides = tmp_path / "empty.yaml"
    overrides.write_text("# nothing\n", encoding="utf-8")

    with pytest.raises(ValueError, match="empty corpus") as caught:
        run_audit.main(
            [
                "--data-root", str(tmp_path / "raw"),
                "--results-root", str(tmp_path / "results"),
                "--overrides", str(overrides),
                "--provenance", str(tmp_path / "missing_PROVENANCE.md"),
                "--pre-audit",
            ]
        )

    assert "no sentences read" in str(caught.value)
    assert not (tmp_path / "results").exists()


def test_a_configuration_that_retains_nothing_fails(corpus, tmp_path):
    """|A| = 0 makes the add-β pseudo-mass vanish; it must not reach a report."""
    config = yaml.safe_load(REPO_CONFIG.read_text(encoding="utf-8"))
    config["alphabet"]["deprel_keep"] = ["there_is_no_such_deprel"]
    path = tmp_path / "retains_nothing.yaml"
    path.write_text(yaml.safe_dump(config), encoding="utf-8")

    with pytest.raises(ValueError, match=r"\|A\| = 0") as caught:
        invoke(corpus, "--pre-audit", "--overrides", str(corpus["empty"]), "--config", str(path))

    # Both configured languages are named, and no report survives the refusal.
    assert "'grc'" in str(caught.value) and "'la'" in str(caught.value)
    assert not corpus["results_root"].exists()


def test_a_stale_override_is_fatal_in_both_modes(corpus):
    """A key naming an absent document means the file describes another corpus."""
    stale = {**ASSIGNMENTS, "ghost.tb.xml": ASSIGNMENTS["alpha.tb.xml"]}
    path = corpus["write_overrides"](stale, "stale.yaml")

    for extra in ([], ["--pre-audit"]):
        with pytest.raises(ValueError, match="ghost.tb.xml") as caught:
            invoke(corpus, "--overrides", str(path), *extra)

        # And the message says so explicitly, so nobody reaches for --pre-audit
        # expecting it to excuse a file describing a different corpus.
        assert "--pre-audit does not excuse this" in str(caught.value)


def test_merged_prefixes_are_folded_before_anything_is_counted(corpus, monkeypatch):
    """GATE-B and the retained-token column must be about documents, not prefixes."""
    merge = {"source_urn": "urn:cts:test:merged", "canonical_doc_id": "merged.tb.xml"}
    merged = assignments_with(
        **{
            "alpha.tb.xml": merge,
            # beta takes alpha's metadata wholesale: a merge requires the traceable
            # fields to agree exactly across the group.
            "beta.tb.xml": {**ASSIGNMENTS["alpha.tb.xml"], **merge},
        }
    )
    path = corpus["write_overrides"](merged, "merged.yaml")
    monkeypatch.setattr(run_audit, "CANONICAL_OVERRIDES", path.resolve())
    report = read_report(invoke(corpus, "--overrides", str(path)))

    assert "merged.tb.xml" in report
    # alpha 4 retained + beta 1 retained (its `vocative` token is dropped under C0).
    assert "| 5 |" in report
    assert "| alpha.tb.xml |" not in report


def test_pre_audit_names_the_documents_that_blocked_the_regime_aggregates(corpus):
    """A withheld verdict must say what is missing, not merely that it is missing."""
    report = read_report(invoke(corpus, "--pre-audit", "--overrides", str(corpus["empty"])))

    assert "alpha.tb.xml" in report
    assert "beta.tb.xml" in report


def test_pre_audit_with_a_complete_proposal_labels_regime_tables_provisional(corpus):
    """The registry is unratified, so aggregates may be shown but never as verdicts."""
    result = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))
    report = read_report(result)

    assert "PROVISIONAL" in report
    assert "HEX" in report
    assert "GATE-A: NOT EVALUATED" in report
    assert "T*: not computed" in report
    assert result["gates_evaluated"] is False


def test_the_report_states_every_declared_reading_and_points_the_right_way(corpus):
    """The readings are the stage's contract with the reader, so their count and
    their direction are asserted, not left to a proofread.

    The "points the right way" half is a real regression: the withheld-verdict
    reason promised shares *below* it while the only share table in the report is
    the one above it, in Regime aggregates.
    """
    # A *proposed* registry: that is the branch whose withheld-verdict reason
    # points at the share table, and the branch the ratification will be read from.
    proposed = corpus["write_overrides"](
        {**ASSIGNMENTS, "_status": "PROPOSED"}, "proposed_for_readings.yaml"
    )
    report = read_report(invoke(corpus, "--pre-audit", "--overrides", str(proposed)))

    assert "Five points of §3.4 admit more than one reading" in report
    for numbered in ("1. **GATE-A denominator", "2. **GATE-A scope",
                     "3. **Which regimes carry", "4. **Exploratory regimes keep",
                     "5. **Language scope"):
        assert numbered in report, numbered
    assert "shares below are provisional" not in report
    assert "*Regime aggregates* above are provisional" in report


def test_canonical_mode_with_a_complete_registry_evaluates_the_gates(corpus):
    """The same entry point becomes the canonical audit once the registry is ratified."""
    result = invoke(corpus, "--overrides", str(corpus["complete"]))
    report = read_report(result)

    assert "INCOMPLETE / PENDING_REGISTRY" not in report
    assert "NOT EVALUATED" not in report
    assert result["gates_evaluated"] is True


# --- counts -----------------------------------------------------------------------


def test_report_carries_the_retained_token_column_t_star_will_be_derived_from(corpus):
    """D55's T* must be recomputable by hand from the report (owner requirement)."""
    report = read_report(invoke(corpus, "--pre-audit", "--overrides", str(corpus["empty"])))

    assert "n_tokens_retained" in report
    # alpha: NOUN:nsubj, VERB:root, ADV:advmod, VERB:root kept; PUNCT dropped.
    assert "| 4 |" in report


def test_a_mistyped_config_key_is_rejected_not_silently_ignored(corpus):
    """`dmax` is not `d_max`: the merge accepts it, the pipeline reads it nowhere,
    and `config_hash` changes anyway — so the run is misparameterised and its own
    identity says nothing about it (§6.3)."""
    config = yaml.safe_load(REPO_CONFIG.read_text(encoding="utf-8"))
    config["context_tree"]["dmax"] = 8
    bad = corpus["write_overrides"](config, "typo_config.yaml")

    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--config", str(bad), "--overrides", str(corpus["complete"]))

    assert "context_tree.dmax" in str(caught.value)


@pytest.mark.parametrize("location", ["top-level", "section", "contrast"])
def test_non_string_config_keys_are_reported_as_unknown(corpus, location):
    config = yaml.safe_load(REPO_CONFIG.read_text(encoding="utf-8"))
    target = {
        "top-level": config,
        "section": config["alphabet"],
        "contrast": config["corpus"]["primary_contrast"],
    }[location]
    target[1] = "unexpected"
    bad = corpus["write_overrides"](config, "numeric_key_config.yaml")

    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--config", str(bad), "--overrides", str(corpus["complete"]))

    assert "unknown" in str(caught.value)
    assert "1" in str(caught.value)


def test_a_config_missing_a_declared_key_is_rejected(corpus):
    """The converse: a key the default declares and the file omits leaves the run
    taking a value the operator never saw in their own config."""
    config = yaml.safe_load(REPO_CONFIG.read_text(encoding="utf-8"))
    del config["context_tree"]["d_max"]
    bad = corpus["write_overrides"](config, "short_config.yaml")

    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--config", str(bad), "--overrides", str(corpus["complete"]))

    assert "context_tree.d_max" in str(caught.value)


def test_a_config_section_replaced_by_a_scalar_is_rejected(corpus):
    """A declared section that is no longer a mapping has no keys to compare, and
    the check used to skip it — accepting silently the misparameterisation it
    exists to refuse, with `config_hash` moved and nothing saying so."""
    config = yaml.safe_load(REPO_CONFIG.read_text(encoding="utf-8"))
    config["context_tree"] = 5
    bad = corpus["write_overrides"](config, "scalar_section_config.yaml")

    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--config", str(bad), "--overrides", str(corpus["complete"]))

    assert "context_tree.d_max" in str(caught.value)


def test_a_deleted_language_keyed_section_is_rejected(corpus):
    """`corpus.primary_contrast` was exempt by name so that its language keys
    would not be schema-checked — but the check never descends that far, so the
    exemption only made the key itself optional."""
    config = yaml.safe_load(REPO_CONFIG.read_text(encoding="utf-8"))
    del config["corpus"]["primary_contrast"]
    bad = corpus["write_overrides"](config, "no_contrast_config.yaml")

    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--config", str(bad), "--overrides", str(corpus["complete"]))

    assert "corpus.primary_contrast" in str(caught.value)


@pytest.mark.parametrize("body", ["", "null\n", "[]\n"], ids=["empty", "null", "list"])
def test_an_explicit_config_must_be_a_nonempty_mapping(corpus, body):
    path = corpus["tmp_path"] / "explicit_config.yaml"
    path.write_text(body, encoding="utf-8")

    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--config", str(path), "--overrides", str(corpus["complete"]))

    assert str(path) in str(caught.value)
    assert "mapping" in str(caught.value)


def test_duplicate_config_keys_are_rejected(corpus):
    path = corpus["tmp_path"] / "duplicate_config.yaml"
    path.write_text("seeds: {global: 1}\nseeds: {global: 2}\n", encoding="utf-8")

    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--config", str(path), "--overrides", str(corpus["complete"]))

    assert "duplicate" in str(caught.value).lower()
    assert str(path) in str(caught.value)


@pytest.mark.parametrize(
    "section,key,value,expected",
    [
        ("corpus", "languages", [], "languages"),
        ("corpus", "languages", ["grc", "grc"], "unique"),
        ("corpus", "languages", ["grc", 3], "strings"),
        ("corpus", "primary_contrast", {"la": ["HEX", "PROSE_ALL"]}, "grc"),
        ("corpus", "primary_contrast", {"grc": ["HEX"], "la": ["HEX", "PROSE_ALL"]}, "two"),
        ("alphabet", "upos_keep", ["NOUN", 3], "strings"),
        ("alphabet", "upos_drop", ["PUNCT", None], "strings"),
        ("alphabet", "deprel_keep", ["root", False], "strings"),
        ("stats", "family", ["P1", 2], "strings"),
        ("alphabet", "gate_a_threshold", "0.02", "numeric"),
        ("seeds", "global", True, "integer"),
        ("scores", "min_available_past", -1, "non-negative"),
        ("scores", "learning_curve_T", [5000, "10000"], "integers"),
    ],
)
def test_g1_used_config_shapes_are_validated(
    corpus, section, key, value, expected
):
    config = yaml.safe_load(REPO_CONFIG.read_text(encoding="utf-8"))
    config[section][key] = value
    path = corpus["write_overrides"](config, f"bad_{section}_{key}.yaml")

    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--config", str(path), "--overrides", str(corpus["complete"]))

    assert expected in str(caught.value)


def test_mwt_and_empty_node_rows_never_reach_the_counts(tmp_path):
    """§3.2: sequences are syntactic words; the reader's filtering must hold here too."""
    data_root = tmp_path / "raw" / "UD_Mwt"
    data_root.mkdir(parents=True)
    (data_root / "la_mwt-ud-train.conllu").write_text(
        "# sent_id = gamma.tb.xml@1\n"
        + _row("1-2", "quoque", "_", "_", "_", "_", "_", "_", "_", "_")
        + "\n"
        + _row("1", "quo", "quo", "ADV", "_", "_", "3", "advmod", "_", "_")
        + "\n"
        + _row("2", "que", "que", "CCONJ", "_", "_", "3", "cc", "_", "_")
        + "\n"
        + _row("3", "canit", "cano", "VERB", "_", "_", "0", "root", "_", "_")
        + "\n"
        + _row("3.1", "_", "_", "X", "_", "_", "_", "_", "_", "_")
        + "\n\n",
        encoding="utf-8",
    )
    config = tmp_path / "la_only.yaml"
    config.write_text(yaml.safe_dump(config_with(languages=["la"])), encoding="utf-8")
    overrides = tmp_path / "none.yaml"
    overrides.write_text("# unassigned\n", encoding="utf-8")
    result = run_audit.main(
        [
            "--data-root", str(tmp_path / "raw"),
            "--results-root", str(tmp_path / "results"),
            "--config", str(config),
            "--overrides", str(overrides),
            "--pre-audit",
        ]
    )

    assert result["n_tokens_raw"] == 3


# --- provenance and overwrite -----------------------------------------------------


def test_a_sent_id_repeated_across_split_files_is_refused(corpus):
    """D03 pools train/dev/test, so a sent_id occurring in two files would be
    counted twice in n_sentences and n_tokens_raw and inflate every figure
    derived from them. `read_tokens` is the only place that sees every file of
    every language at once."""
    (corpus["data_root"] / "UD_Mini" / "grc_mini-ud-dev.conllu").write_text(
        _sentence("alpha.tb.xml@1", [("NOUN", "nsubj")]) + "\n", encoding="utf-8"
    )
    corpus["refresh_provenance"]()

    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--overrides", str(corpus["complete"]))

    assert "alpha.tb.xml@1" in str(caught.value)


def test_results_root_inside_the_data_root_is_refused(corpus):
    """`data/raw` is immutable (CC BY-NC-SA 2.5) and every input is hashed into
    the run's identity, so artifacts landing inside it corrupt both the corpus and
    the next run's fingerprint. The guard compares against `--data-root`, not a
    literal path: the whole suite drives a synthetic corpus."""
    with pytest.raises(ValueError) as caught:
        invoke(
            corpus,
            "--results-root",
            str(corpus["data_root"] / "results"),
            "--overrides",
            str(corpus["complete"]),
        )

    assert "data root" in str(caught.value)

    link = corpus["tmp_path"] / "link"
    link.symlink_to(corpus["data_root"] / "sneaky", target_is_directory=True)
    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--results-root", str(link), "--overrides", str(corpus["complete"]))

    assert "data root" in str(caught.value)


def test_every_resolved_destination_stays_outside_both_raw_roots(corpus, monkeypatch):
    inside_selected = corpus["data_root"] / "sneaky"
    inside_selected.mkdir()
    corpus["results_root"].mkdir()
    (corpus["results_root"] / "tables").symlink_to(
        inside_selected, target_is_directory=True
    )

    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))

    assert "destination" in str(caught.value)
    assert list(inside_selected.iterdir()) == []

    shutil.rmtree(corpus["results_root"])
    canonical_raw = corpus["tmp_path"] / "canonical_raw"
    canonical_raw.mkdir()
    monkeypatch.setattr(run_audit, "CANONICAL_DATA_ROOT", canonical_raw)
    with pytest.raises(ValueError) as caught:
        invoke(
            corpus,
            "--pre-audit",
            "--results-root",
            str(canonical_raw / "results"),
            "--overrides",
            str(corpus["complete"]),
        )

    assert "canonical data root" in str(caught.value)


def test_manifest_and_sidecar_record_every_input_hash(corpus):
    result = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))
    manifest = json.loads(result["manifest_path"].read_text(encoding="utf-8"))
    sidecar = json.loads(
        (result["report_path"].parent / (result["report_path"].name + ".sidecar.json")).read_text(
            encoding="utf-8"
        )
    )

    inputs = {record["path"] for record in manifest["inputs"]}
    assert str(corpus["complete"]) in inputs
    assert str(corpus["provenance"]) in inputs
    assert any(path.endswith("grc_mini-ud-train.conllu") for path in inputs)
    assert all(len(record["sha256"]) == 64 for record in manifest["inputs"])
    assert sidecar["run_id"] == manifest["run_id"]
    assert sidecar["entry_point"] == manifest["entry_point"]


def test_verified_provenance_is_visible_in_report_and_manifest(corpus):
    result = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))
    manifest = json.loads(result["manifest_path"].read_text(encoding="utf-8"))

    assert manifest["provenance"]["status"] == "verified"
    assert "Raw provenance: **VERIFIED**" in read_report(result)


def test_canonical_mode_refuses_a_provenance_hash_mismatch(corpus):
    text = corpus["provenance"].read_text(encoding="utf-8")
    source = sorted(corpus["data_root"].rglob("*.conllu"))[0]
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    other = ("0" if digest[0] != "0" else "1") + digest[1:]
    corpus["provenance"].write_text(text.replace(digest, other), encoding="utf-8")

    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--overrides", str(corpus["complete"]))

    assert "provenance" in str(caught.value).lower()
    assert "grc_mini-ud-train.conllu" in str(caught.value)
    assert not corpus["results_root"].exists()


@pytest.mark.parametrize(
    "defect", ["release", "release-label", "missing", "extra", "invalid-sha"]
)
def test_canonical_provenance_requires_the_exact_release_and_file_set(corpus, defect):
    path = corpus["provenance"]
    text = path.read_text(encoding="utf-8")
    row = next(line for line in text.splitlines() if "grc_mini" in line)
    if defect == "release":
        text = text.replace("r2.18", "r9.99")
    elif defect == "release-label":
        text = text.replace("UD release tag (pinned, D03)", "UD release tag (copy)")
    elif defect == "missing":
        text = text.replace(row + "\n", "")
    elif defect == "extra":
        text += f"| absent-ud-train.conllu | `{'0' * 64}` |\n"
    else:
        text = text.replace(row, row.replace("`", "`not-a-digest`", 1))
    path.write_text(text, encoding="utf-8")

    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--overrides", str(corpus["complete"]))

    assert "provenance" in str(caught.value).lower()
    assert not corpus["results_root"].exists()


def test_pre_audit_reports_a_provenance_mismatch_without_claiming_it_is_pinned(corpus):
    text = corpus["provenance"].read_text(encoding="utf-8")
    corpus["provenance"].write_text(text.replace("r2.18", "r9.99"), encoding="utf-8")
    result = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))
    manifest = json.loads(result["manifest_path"].read_text(encoding="utf-8"))
    report = read_report(result)

    assert manifest["provenance"]["status"] == "mismatch"
    assert "MISMATCH" in report
    assert "UD release (pinned" not in report


def test_missing_provenance_blocks_canonical_but_is_reported_by_pre_audit(corpus):
    missing = corpus["tmp_path"] / "missing_PROVENANCE.md"

    with pytest.raises(FileNotFoundError) as caught:
        invoke(
            corpus, "--provenance", str(missing), "--overrides", str(corpus["complete"])
        )
    assert "PROVENANCE" in str(caught.value)

    result = invoke(
        corpus,
        "--pre-audit",
        "--provenance",
        str(missing),
        "--overrides",
        str(corpus["complete"]),
    )
    assert "MISSING" in read_report(result)


def test_duplicate_provenance_rows_are_not_accepted_as_evidence(corpus):
    text = corpus["provenance"].read_text(encoding="utf-8")
    row = next(line for line in text.splitlines() if "grc_mini" in line)
    corpus["provenance"].write_text(text + row + "\n", encoding="utf-8")

    with pytest.raises(ValueError) as caught:
        invoke(corpus, "--overrides", str(corpus["complete"]))

    assert "duplicate" in str(caught.value).lower()


def test_rerunning_without_force_refuses_to_overwrite(corpus):
    invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))

    with pytest.raises(FileExistsError) as caught:
        invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))

    # The refusal names its remedy, or §6.4's "no silent overwrites" is a dead
    # end for the operator.
    assert "--force" in str(caught.value)


def test_force_permits_the_rerun(corpus):
    first = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))
    second = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]), "--force")

    assert first["report_path"] == second["report_path"]


def test_runs_differing_only_in_overrides_get_distinct_artifact_names(corpus):
    """§6.1's {stage}_{config-hash}_{date} collides here; the input fingerprint separates them."""
    label_free = invoke(corpus, "--pre-audit", "--overrides", str(corpus["empty"]))
    provisional = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))

    assert label_free["report_path"] != provisional["report_path"]
    assert label_free["run_id"] != provisional["run_id"]
    assert label_free["report_path"].exists()
    assert provisional["report_path"].exists()


def test_runs_differing_only_in_provenance_get_distinct_artifact_names(corpus):
    first = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))
    provenance = corpus["provenance"]
    provenance.write_text(
        provenance.read_text(encoding="utf-8") + "\n<!-- audit note -->\n",
        encoding="utf-8",
    )
    second = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))

    assert first["run_id"] != second["run_id"]
    assert first["report_path"].exists() and second["report_path"].exists()


def test_the_two_modes_never_share_a_run_id(corpus):
    """Same data, config and overrides — different meaning, so different identity."""
    pre = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))
    canonical = invoke(corpus, "--overrides", str(corpus["complete"]))

    assert pre["run_id"] != canonical["run_id"]
    assert pre["report_path"] != canonical["report_path"]
    assert set(pre["csv_files"]).isdisjoint(canonical["csv_files"])
    assert "preaudit" in pre["run_id"] and "canonical" in canonical["run_id"]
    assert pre["report_path"].exists() and canonical["report_path"].exists()


def test_a_collision_on_any_output_leaves_no_partial_run(corpus):
    """Progressive writing would let a failed run replace an earlier run's CSVs."""
    first = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))
    csvs = {path: path.read_bytes() for path in first["csv_files"]}
    first["report_path"].unlink()  # only the late output is missing now

    with pytest.raises(FileExistsError):
        invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))

    assert not first["report_path"].exists()
    assert {path: path.read_bytes() for path in first["csv_files"]} == csvs


def test_the_full_alphabet_inventory_ships_unfrozen(corpus):
    """Top-20 in the report cannot show the tie-break; the freeze will use these ids."""
    result = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))
    inventory = next(p for p in result["csv_files"] if "alphabet_inventory" in p.name)
    rows = inventory.read_text(encoding="utf-8").splitlines()

    assert rows[0].split(",") == [
        "language", "variant", "excluded_deprel_policy", "symbol_id", "symbol", "n",
        "frozen", "status",
    ]
    assert all(",False,PROVISIONAL" in row for row in rows[1:])
    # Ids restart per language (§4.1: |A| is per (language, variant)). Greek:
    # NOUN:nsubj (2), VERB:root (2), ADV:advmod (1) — the first two tie and are
    # ordered by symbol. beta's `vocative` token is dropped under C0.
    assert [tuple(row.split(",")[i] for i in (0, 3, 4)) for row in rows[1:]] == [
        ("grc", "0", "NOUN:nsubj"),
        ("grc", "1", "VERB:root"),
        ("grc", "2", "ADV:advmod"),
        ("la", "0", "NOUN:nsubj"),
        ("la", "1", "VERB:root"),
    ]


def test_mode_is_machine_readable_in_the_manifest_and_every_sidecar(corpus):
    """Reading the mode should not require parsing it back out of the run_id."""
    result = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))
    manifest = json.loads(result["manifest_path"].read_text(encoding="utf-8"))

    assert manifest["mode"] == "preaudit"
    assert manifest["status"] == "PROVISIONAL"
    assert manifest["entry_point"].endswith("--pre-audit")

    sidecars = [result["report_path"], *result["csv_files"]]
    assert len(sidecars) == 4
    for artifact in sidecars:
        payload = json.loads(
            Path(str(artifact) + ".sidecar.json").read_text(encoding="utf-8")
        )
        assert payload["entry_point"].endswith("--pre-audit")
        assert payload["run_id"] == manifest["run_id"]


UNRATIFIED_PHRASINGS = (
    "is not ratified",
    "unratified registry",
    "has not been ratified",
    "not the merge but the ratification",
    "*proposed* registry",
)


def test_a_pre_audit_over_a_ratified_registry_never_calls_it_unratified(corpus):
    """--pre-audit on a ratified registry is a legitimate rehearsal; every way of
    saying "unratified" would be a false statement in the report.

    Asserted over all the phrasings the renderer can emit, not one of them: an
    earlier version of this test checked a single exact string and passed while
    the report said "unratified registry" three lines away.
    """
    report = read_report(invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"])))

    for phrase in UNRATIFIED_PHRASINGS:
        assert phrase not in report, phrase
    assert "PROVISIONAL for one reason only" in report
    assert "`_status: RATIFIED`" in report


def test_a_pre_audit_over_a_proposed_registry_does_say_it_is_unratified(corpus):
    """The converse: the honest wording must still appear when it is true."""
    proposed = corpus["write_overrides"](
        {**ASSIGNMENTS, "_status": "PROPOSED"}, "proposed_for_wording.yaml"
    )
    report = read_report(invoke(corpus, "--pre-audit", "--overrides", str(proposed)))

    assert any(phrase in report for phrase in UNRATIFIED_PHRASINGS)
    assert "PROVISIONAL for one reason only" not in report


def test_two_concurrent_identical_runs_cannot_both_publish(corpus):
    """`_preflight` alone is check-then-act; the run_id reservation is the atom."""
    from concurrent.futures import ThreadPoolExecutor

    def run():
        try:
            return invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))
        except FileExistsError as exc:
            return exc

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = [future.result() for future in [pool.submit(run), pool.submit(run)]]

    published = [o for o in outcomes if isinstance(o, dict)]
    refused = [o for o in outcomes if isinstance(o, FileExistsError)]
    assert len(published) == 1 and len(refused) == 1


def test_the_reservation_alone_protects_even_with_every_artifact_deleted(corpus):
    """Protection must not depend on the artifacts still being on disk."""
    first = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))
    for path in [first["report_path"], *first["csv_files"]]:
        path.unlink()
        Path(str(path) + ".sidecar.json").unlink()
    # Free every destination the preflight checks, leaving only the empty log
    # directory — so the refusal below can come from the reservation alone.
    first["manifest_path"].unlink()

    with pytest.raises(FileExistsError, match="already claimed") as caught:
        invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))

    # The reservation names the directory that holds the identity, so the refusal
    # is actionable without guessing which run_id collided.
    assert first["run_id"] in str(caught.value)


def test_a_conllu_appearing_mid_run_publishes_nothing(corpus, monkeypatch):
    """A digest comparison cannot see a file that was never in the snapshot; the
    data root has to be re-globbed, or the new file sits outside report and manifest."""
    real = run_audit.build_context

    def add_a_file(*args, **kwargs):
        out = real(*args, **kwargs)
        (corpus["data_root"] / "UD_Mini" / "grc_extra-ud-train.conllu").write_text(
            MINI_GRC, encoding="utf-8"
        )
        return out

    monkeypatch.setattr(run_audit, "build_context", add_a_file)

    with pytest.raises(RuntimeError, match="appeared"):
        invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))

    assert not corpus["results_root"].exists()


def test_a_removed_input_is_caught_too(corpus, monkeypatch):
    real = run_audit.build_context

    def remove_a_file(*args, **kwargs):
        out = real(*args, **kwargs)
        (corpus["data_root"] / "UD_Mini" / "la_mini-ud-train.conllu").unlink()
        return out

    monkeypatch.setattr(run_audit, "build_context", remove_a_file)

    with pytest.raises(RuntimeError, match="removed") as caught:
        invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))

    # The vanished file is named, and nothing was published from a corpus state
    # that no longer exists.
    assert "la_mini-ud-train.conllu" in str(caught.value)
    assert not corpus["results_root"].exists()


def test_a_refused_run_never_deletes_the_artifacts_it_refused_to_overwrite(corpus):
    """The rollback must not fire on the preflight's own refusal.

    With `_preflight` inside the try, its FileExistsError fell into the rollback,
    which deleted the pre-existing artifacts the refusal exists to protect.
    """
    first = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))
    victim = first["csv_files"][0]
    shutil.rmtree(corpus["results_root"] / "logs")  # free the reservation only
    victim.write_text("KEEP\n", encoding="utf-8")

    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))

    assert victim.exists()
    assert victim.read_text(encoding="utf-8") == "KEEP\n"
    assert first["report_path"].exists()


def test_the_loser_of_a_concurrent_race_deletes_nothing(corpus):
    """A reservation refusal must not roll back the winner's output either."""
    first = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))
    artifacts = [first["report_path"], *first["csv_files"]]
    contents = {path: path.read_bytes() for path in artifacts}

    with pytest.raises(FileExistsError):
        invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))

    assert {path: path.read_bytes() for path in artifacts} == contents


def test_a_partially_written_artifact_is_rolled_back(corpus, monkeypatch):
    """Rollback runs over the predetermined destinations, not over a record of what
    succeeded: a write that fails partway never reaches the line that would record it."""
    # Learn the destinations from a good run, then clear them so the retry is clean.
    report_path = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))[
        "report_path"
    ]
    shutil.rmtree(corpus["results_root"])

    def truncated_write(context):
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text("half a report", encoding="utf-8")
        raise RuntimeError("truncated")

    monkeypatch.setattr(run_audit, "render_report", truncated_write)
    with pytest.raises(RuntimeError, match="truncated"):
        invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))

    assert not report_path.exists()
    assert [path for path in corpus["results_root"].rglob("*") if path.is_file()] == []


def test_a_failure_between_writes_rolls_the_whole_run_back(corpus, monkeypatch):
    """All-or-nothing has to survive a failure *between* writes, not only before
    the first one: the CSVs are written before the report."""
    monkeypatch.setattr(
        run_audit, "render_report", lambda ctx: (_ for _ in ()).throw(RuntimeError("boom"))
    )
    with pytest.raises(RuntimeError, match="boom"):
        invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))

    assert list(corpus["results_root"].rglob("*.csv")) == []
    assert list(corpus["results_root"].rglob("*.json")) == []

    # And the reservation is released, so the corrected rerun is not locked out.
    monkeypatch.undo()
    assert invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))["run_id"]


def test_the_run_id_distinguishes_two_code_revisions(corpus, monkeypatch):
    """Same day, same data, same config, different software: without the code
    revision the second run either refuses to write or, under --force, replaces
    evidence that a different program produced."""
    run_ids = []
    for commit in ("a" * 40, "b" * 40):
        monkeypatch.setattr(
            run_audit,
            "git_state",
            lambda commit=commit: {"commit": commit, "dirty": False},
        )
        run_ids.append(
            invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))["run_id"]
        )

    assert run_ids[0] != run_ids[1]


def test_build_manifest_honours_a_pre_captured_git_state():
    captured = {"commit": "0" * 40, "dirty": False}
    manifest = build_manifest(
        "run", "cfg", 0, [], ENTRY_POINT_FOR_TEST, inputs=(), git=captured
    )

    assert manifest["git"] is captured
    # The default still samples, so no other caller's behaviour changed.
    assert build_manifest("run", "cfg", 0, [], ENTRY_POINT_FOR_TEST)["git"]["commit"] != "0" * 40


def test_the_stage_samples_git_before_it_writes_anything(corpus, monkeypatch):
    """Timing, not just plumbing: the stage's own outputs land in the worktree, so
    a sample taken afterwards would report a dirtiness the run itself created."""
    observed = {}
    real = run_audit.git_state

    def spy():
        observed["results_root_existed"] = corpus["results_root"].exists()
        return real()

    monkeypatch.setattr(run_audit, "git_state", spy)
    invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))

    assert observed["results_root_existed"] is False


def test_the_manifest_records_the_inputs_as_read_not_as_they_end_up(corpus):
    """Inputs are read twice — once to compute, once to identify. If the overrides
    file is edited in between, the report and the manifest describe different bytes."""
    sentinel = corpus["write_overrides"](assignments_with(), "racy.yaml")
    with run_audit.staged_inputs([sentinel]) as (snapshot, _):
        digest_before = snapshot[sentinel]

    result = invoke(corpus, "--pre-audit", "--overrides", str(sentinel))
    sentinel.write_text("_status: TAMPERED\n", encoding="utf-8")
    manifest = json.loads(result["manifest_path"].read_text(encoding="utf-8"))

    recorded = {r["path"]: r["sha256"] for r in manifest["inputs"]}
    assert recorded[str(sentinel)] == digest_before


def test_an_edit_that_is_restored_before_verification_cannot_reach_the_report(
    corpus, monkeypatch
):
    """The sequence a before/after digest comparison cannot catch: edit → parse →
    restore. Both digests match the original while the parse consumed something
    else, and there is nothing left to compare. Only parsing the same bytes the
    digest covers closes it."""
    target = corpus["data_root"] / "UD_Mini" / "grc_mini-ud-train.conllu"
    original = target.read_text(encoding="utf-8")
    smuggled = original + _sentence("smuggled.tb.xml@1", [("NOUN", "nsubj")]) + "\n"

    real = run_audit.read_tokens

    def edit_then_restore(*args, **kwargs):
        target.write_text(smuggled, encoding="utf-8")
        try:
            return real(*args, **kwargs)
        finally:
            target.write_text(original, encoding="utf-8")

    monkeypatch.setattr(run_audit, "read_tokens", edit_then_restore)
    result = invoke(corpus, "--pre-audit", "--overrides", str(corpus["empty"]))

    # alpha 3 + 2, beta 2, gamma 2 = 9 raw tokens; the smuggled sentence is absent.
    assert result["n_tokens_raw"] == 9
    assert "smuggled.tb.xml" not in read_report(result)


def test_an_input_edited_mid_run_publishes_nothing(corpus, monkeypatch):
    """The check has to happen before the first write, or the damage is already done."""
    overrides = corpus["write_overrides"](assignments_with(), "mutating.yaml")
    real = run_audit.build_context

    def tamper(*args, **kwargs):
        out = real(*args, **kwargs)
        overrides.write_text("_status: SWAPPED\n", encoding="utf-8")
        return out

    monkeypatch.setattr(run_audit, "build_context", tamper)

    with pytest.raises(RuntimeError, match="changed while the audit was running"):
        invoke(corpus, "--pre-audit", "--overrides", str(overrides))

    assert not corpus["results_root"].exists()


def test_every_csv_declares_its_own_status(corpus):
    """Detached from filename and sidecar, a provisional table must still say so."""
    result = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))

    for path in result["csv_files"]:
        rows = path.read_text(encoding="utf-8").splitlines()
        assert rows[0].split(",")[-1] == "status"
        assert all(row.endswith(",PROVISIONAL") for row in rows[1:])


def test_the_report_does_not_claim_prefixes_are_unmerged_when_they_are_merged(corpus):
    """The GATE-B note must follow the registry, not assume there is none."""
    with_registry = read_report(invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"])))
    without = read_report(invoke(corpus, "--pre-audit", "--overrides", str(corpus["empty"])))

    assert "is** computed over canonical documents" in with_registry
    assert "still counted apart" not in with_registry
    assert "still counted apart" in without


def test_the_label_free_report_does_not_promise_a_regime_contingency_it_lacks(corpus):
    report = read_report(invoke(corpus, "--pre-audit", "--overrides", str(corpus["empty"])))

    assert "cannot be produced: regimes come from the registry" in report
    assert "contingency_by_regime" not in report


def test_declared_readings_do_not_make_a_deictic_empirical_claim(corpus):
    report = read_report(invoke(corpus, "--pre-audit", "--overrides", str(corpus["empty"])))

    assert "largest share anywhere below" not in report
    assert "Exploratory regimes keep their firing power" in report


def test_alphabet_frames_keep_their_header_when_empty():
    """A column-less frame writes a CSV with no header row at all."""
    empty = run_audit._alphabet_full(None, {}, {"alphabet": {"variant": "ud23", "excluded_deprel_policy": "drop"}})

    assert list(empty.columns) == [
        "language", "variant", "excluded_deprel_policy", "symbol_id", "symbol", "n", "frozen"
    ]
    assert empty.to_csv(index=False).startswith("language,variant")


def test_drop_rates_by_rule_are_reported_per_regime(corpus):
    """T2 (§8) asks for drop rates by rule *and regime*, not by rule and document."""
    report = read_report(invoke(corpus, "--overrides", str(corpus["complete"])))

    assert "Drop rates by rule, per regime" in report
    assert "upos_excluded_rate" in report
    assert "deprel_excluded_rate" in report


def test_the_stage_never_writes_a_frozen_alphabet(corpus, tmp_path):
    """No freeze in this stage: alphabet.json is an outcome of the ratified G1 audit."""
    result = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))

    assert not list(tmp_path.rglob("alphabet.json"))
    assert not (REPO_CONFIG.parents[1] / "data" / "processed" / "alphabet.json").exists()
    written = {path.name for path in corpus["results_root"].rglob("*") if path.is_file()}
    stem = result["report_path"].name.removeprefix("audit_report_").removesuffix(".md")
    assert written == {
        f"audit_report_{stem}.md",
        f"audit_report_{stem}.md.sidecar.json",
        f"alphabet_inventory_{stem}.csv",
        f"alphabet_inventory_{stem}.csv.sidecar.json",
        f"contingency_by_document_{stem}.csv",
        f"contingency_by_document_{stem}.csv.sidecar.json",
        f"contingency_by_regime_{stem}.csv",
        f"contingency_by_regime_{stem}.csv.sidecar.json",
        "manifest.json",
    }


def test_the_full_contingency_ships_as_csv_and_is_hashed(corpus):
    """§3.4 pre-registers the *full* contingency; a truncated table would not be it."""
    result = invoke(corpus, "--pre-audit", "--overrides", str(corpus["complete"]))
    manifest = json.loads(result["manifest_path"].read_text(encoding="utf-8"))
    artifacts = {Path(record["path"]).name for record in manifest["artifacts"]}

    csvs = sorted(name for name in artifacts if name.endswith(".csv"))
    assert [name.split("_preaudit_")[0] for name in csvs] == [
        "alphabet_inventory",
        "contingency_by_document",
        "contingency_by_regime",
    ]
    for name in csvs:
        assert name in read_report(result)
    assert all(len(record["sha256"]) == 64 for record in manifest["artifacts"])


def test_the_inventory_keeps_the_declared_registry_column_order(corpus):
    """§2.3 declares the schema order and `build_registry` honours it; the table
    the report publishes must not silently reorder it. `_inventory` drops
    `n_tokens_retained` and re-merges it, which appends it last unless the
    declared order is restored."""
    report = read_report(invoke(corpus, "--overrides", str(corpus["complete"])))
    after = report.split("## Document inventory", 1)[1].splitlines()
    header = next(line for line in after if line.startswith("|"))

    assert tuple(cell.strip() for cell in header.strip("|").split("|")) == (
        registry.REGISTRY_COLUMNS
    )
