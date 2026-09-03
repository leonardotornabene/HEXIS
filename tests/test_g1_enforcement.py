"""Mandatory G1 coverage inventory (D55 §xiv convention 13; PROPOSED).

The repo-root conftest guarantees that no test *carrying* the `g1` marker is
skipped, xfail, xpass or assertion-free. It guarantees nothing about which tests
carry it: delete a file or drop a marker and `-m g1` stays green over a smaller
set, because the marker set is a subset of itself by construction. This file is
the other half — `tests/test_g0_enforcement.py` closed the same hole for G0.

**Running this file alone always fails**, exactly as its G0 counterpart does. The
check reads the *current session's* collected items, and a session holding only
this file has collected no other g1 test. Canonical selection:
`uv run pytest -m g1 --strict-markers`.

The G0 helper is duplicated rather than shared: its marker name is hard-coded and
is itself pinned by `test_g0_name_scan_rejects_uncollected_and_non_pytest_markers`,
a named member of the attested 144-test G0 set, so generalising it would mean
editing attested G0 code in order to serve G1.

Reorganizing g1 tests therefore means editing this map, which is what keeps the
coverage traceable rather than incidental. Empty required-name tuples are
rejected: a file-level count alone lets an area keep twenty tests while losing
the one behaviour its key names.
"""

from collections import defaultdict
from pathlib import Path

import pytest

pytestmark = pytest.mark.g1

AUDIT = "test_run_audit.py"
ALPHABET = "test_g1_alphabet.py"
REGISTRY = "test_g1_registry.py"
SEQUENCES = "test_g1_sequences.py"

SEQUENCES_AREA = "document identity in sequence construction (§3.5, §3.7, D10)"

G1_REQUIRED_COVERAGE = {
    "audit modes: pre-audit withholds every verdict, canonical decides (§3.3)": (
        AUDIT,
        (
            "test_canonical_mode_fails_loud_on_an_unassigned_sentence",
            "test_pre_audit_stamps_the_report_incomplete_and_withholds_every_verdict",
            "test_only_an_explicitly_ratified_file_produces_a_canonical_audit",
            "test_a_ratified_overrides_file_runs_canonically",
            "test_pre_audit_names_the_documents_that_blocked_the_regime_aggregates",
            "test_pre_audit_with_a_complete_proposal_labels_regime_tables_provisional",
            "test_canonical_mode_with_a_complete_registry_evaluates_the_gates",
            "test_mode_is_machine_readable_in_the_manifest_and_every_sidecar",
            "test_a_pre_audit_over_a_ratified_registry_never_calls_it_unratified",
            "test_a_pre_audit_over_a_proposed_registry_does_say_it_is_unratified",
        ),
    ),
    "overrides file well-formedness and registry validation (§2.3)": (
        AUDIT,
        (
            "test_registry_is_validated_not_merely_indexed",
            "test_a_missing_required_field_is_rejected",
            "test_an_incomplete_registry_still_validates_the_rows_it_has",
            "test_a_missing_overrides_file_is_not_an_empty_registry",
            "test_a_malformed_overrides_file_fails_with_its_path",
            "test_the_yaml_error_names_the_original_file_and_keeps_the_snippet",
            "test_an_unknown_override_field_is_rejected_not_dropped",
            "test_the_declared_schema_fields_are_all_accepted",
            "test_a_stale_override_is_fatal_in_both_modes",
            "test_merged_prefixes_are_folded_before_anything_is_counted",
        ),
    ),
    "corpus discovery, configuration and raw token counting (D03, §3.3)": (
        AUDIT,
        (
            "test_a_corpus_missing_a_configured_language_is_refused",
            "test_a_single_language_audit_is_possible_only_by_configuring_it",
            "test_an_empty_corpus_fails_instead_of_passing_every_gate",
            "test_a_configuration_that_retains_nothing_fails",
            "test_mwt_and_empty_node_rows_never_reach_the_counts",
            "test_a_sent_id_repeated_across_split_files_is_refused",
            "test_a_mistyped_config_key_is_rejected_not_silently_ignored",
            "test_a_config_missing_a_declared_key_is_rejected",
            "test_results_root_inside_the_data_root_is_refused",
        ),
    ),
    "run identity, overwrite refusal and concurrent publication (§6.4, D46)": (
        AUDIT,
        (
            "test_rerunning_without_force_refuses_to_overwrite",
            "test_force_permits_the_rerun",
            "test_runs_differing_only_in_overrides_get_distinct_artifact_names",
            "test_the_two_modes_never_share_a_run_id",
            "test_the_run_id_distinguishes_two_code_revisions",
            "test_a_collision_on_any_output_leaves_no_partial_run",
            "test_two_concurrent_identical_runs_cannot_both_publish",
            "test_the_reservation_alone_protects_even_with_every_artifact_deleted",
            "test_a_refused_run_never_deletes_the_artifacts_it_refused_to_overwrite",
            "test_the_loser_of_a_concurrent_race_deletes_nothing",
        ),
    ),
    "input staging, mid-run mutation, rollback and git state (§6.4, D46)": (
        AUDIT,
        (
            "test_manifest_and_sidecar_record_every_input_hash",
            "test_a_conllu_appearing_mid_run_publishes_nothing",
            "test_a_removed_input_is_caught_too",
            "test_a_partially_written_artifact_is_rolled_back",
            "test_a_failure_between_writes_rolls_the_whole_run_back",
            "test_build_manifest_honours_a_pre_captured_git_state",
            "test_the_stage_samples_git_before_it_writes_anything",
            "test_the_manifest_records_the_inputs_as_read_not_as_they_end_up",
            "test_an_edit_that_is_restored_before_verification_cannot_reach_the_report",
            "test_an_input_edited_mid_run_publishes_nothing",
        ),
    ),
    "report and CSV contract, including the declared readings (§6.4)": (
        AUDIT,
        (
            "test_the_report_states_every_declared_reading_and_points_the_right_way",
            "test_report_carries_the_retained_token_column_t_star_will_be_derived_from",
            "test_the_full_alphabet_inventory_ships_unfrozen",
            "test_every_csv_declares_its_own_status",
            "test_the_report_does_not_claim_prefixes_are_unmerged_when_they_are_merged",
            "test_the_label_free_report_does_not_promise_a_regime_contingency_it_lacks",
            "test_alphabet_frames_keep_their_header_when_empty",
            "test_drop_rates_by_rule_are_reported_per_regime",
            "test_the_stage_never_writes_a_frozen_alphabet",
            "test_the_full_contingency_ships_as_csv_and_is_hashed",
            "test_the_inventory_keeps_the_declared_registry_column_order",
        ),
    ),
    "§3.4 mapping, available_past and the drop/retention census": (
        ALPHABET,
        (
            "test_map_tokens_produces_the_spec_columns_and_totality",
            "test_available_past_counts_retained_predecessors_within_the_sentence",
            "test_map_tokens_handles_an_empty_table",
            "test_contingency_totals_reconcile_with_the_raw_token_count",
            "test_contingency_keeps_raw_subtypes_visible",
            "test_retention_and_drop_by_rule_partition_the_raw_tokens",
            "test_excluded_deprel_shares_use_the_raw_token_denominator",
            "test_excluded_deprel_census_is_independent_of_the_drop_or_oth_policy",
            "test_oth_policy_keeps_the_absorbed_label_visible_to_the_audit",
            "test_drop_rates_by_rule_are_available_per_regime",
            "test_restricted_position_fraction_is_reported_per_regime",
        ),
    ),
    "observed alphabet ordering and the refusal to freeze (§3.4, §3.7)": (
        ALPHABET,
        (
            "test_observed_alphabet_orders_ids_by_descending_pooled_frequency",
            "test_observed_alphabet_breaks_frequency_ties_by_symbol",
            "test_observed_alphabet_excludes_dropped_tokens",
            "test_observed_alphabet_rejects_a_two_language_table",
            "test_observed_alphabet_writes_nothing",
            "test_freeze_alphabet_remains_a_declared_but_unimplemented_api",
            "test_run_audit_rejects_a_regime_map_missing_a_document",
        ),
    ),
    "GATE-A and GATE-B, with the declared regime and language scope (D06)": (
        ALPHABET,
        (
            "test_gate_a_fires_above_two_percent_of_raw_tokens_in_a_regime",
            "test_gate_a_does_not_fire_at_exactly_two_percent",
            "test_gate_a_aggregates_over_the_regime_not_the_document",
            "test_gate_a_verdict_ignores_the_excluded_regime_but_still_reports_it",
            "test_gate_a_still_fires_on_an_analysed_regime_when_excluded_is_present",
            "test_gate_a_fires_from_an_exploratory_regime",
            "test_gate_a_shares_are_per_language_and_the_verdict_is_one_per_run",
            "test_gate_b_looks_everywhere_including_the_excluded_regime",
            "test_gate_b_flags_a_document_below_seventy_percent_retention",
            "test_gates_are_not_evaluated_without_a_registry",
        ),
    ),
    "registry field-value guards (§2.3, D04)": (
        REGISTRY,
        (
            "test_a_blank_required_field_is_refused",
            "test_a_bare_string_flags_value_is_refused",
            "test_a_non_string_flag_element_is_refused",
            "test_a_part_order_that_cannot_order_parts_is_refused",
            "test_a_well_formed_assignment_still_builds",
        ),
    ),
    SEQUENCES_AREA: (
        SEQUENCES,
        (
            "test_a_doc_id_shared_by_two_languages_is_refused",
            "test_a_repeated_sent_ord_within_one_document_is_refused",
            "test_a_single_language_document_still_converts",
        ),
    ),
}


def _missing_collected_coverage(items, inventory: dict) -> dict:
    """Compare the inventory with the g1 functions pytest actually collected.

    Any collected item carrying the marker counts, whatever its parent: every g1
    test is a module-level function today, and a class-nested one would still be
    g1 coverage of the file it lives in. Parametrized ids collapse to the
    function name, so the inventory names behaviours and not case counts.
    """
    collected = defaultdict(set)
    for item in items:
        if item.get_closest_marker("g1") is None:
            continue
        name = getattr(item, "originalname", None) or item.name.split("[", 1)[0]
        collected[Path(item.path).name].add(name)

    missing = {}
    for area, (filename, required) in inventory.items():
        if not required:
            missing[area] = f"tests/{filename} has no mandatory test names in inventory"
            continue
        present = collected.get(filename, set())
        if not present:
            missing[area] = f"tests/{filename} has no collected g1 test"
            continue
        absent = sorted(set(required) - present)
        if absent:
            missing[area] = (
                f"tests/{filename} is missing {absent} from collected g1 tests"
            )
    return missing


class _StandInItem:
    """The minimum of pytest's item interface `_missing_collected_coverage` reads.

    The self-tests below need a collection that can *lose* a test, which a real
    session cannot supply without deleting one.
    """

    def __init__(self, name, filename):
        self.name = name
        self.originalname = name
        self.path = Path("tests") / filename

    def get_closest_marker(self, marker):
        return object() if marker == "g1" else None


def test_g1_set_covers_every_mandatory_area(request):
    """G1 cannot close on a subset. Evidence is the current pytest session, not an
    approximation of collection from source text.

    Running this file on its own always fails: the session has then collected no
    other g1 test. That is the documented behaviour, not a defect.
    """
    missing = _missing_collected_coverage(request.session.items, G1_REQUIRED_COVERAGE)
    assert not missing, "incomplete mandatory G1 coverage: " + "; ".join(
        f"{area}: {reason}" for area, reason in sorted(missing.items())
    )


def test_the_inventory_fails_when_an_area_loses_a_mandatory_test():
    """The inventory must be able to go red, or it certifies nothing: the file
    keeps its other g1 tests and loses exactly one named behaviour."""
    filename, required = G1_REQUIRED_COVERAGE[SEQUENCES_AREA]
    dropped = "test_a_doc_id_shared_by_two_languages_is_refused"
    assert dropped in required
    items = [_StandInItem(name, filename) for name in required if name != dropped]

    missing = _missing_collected_coverage(
        items, {SEQUENCES_AREA: (filename, required)}
    )

    assert dropped in missing[SEQUENCES_AREA]


def test_an_empty_required_tuple_is_rejected():
    """A file-level count alone left the G0 inventory decorative: an area could
    keep twenty tests and lose the one behaviour its key names."""
    missing = _missing_collected_coverage([], {"area": ("test_nothing.py", ())})

    assert "no mandatory test names" in missing["area"]
