"""Active V0–V1 must collect all required tests and execute real assertions."""
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

import pytest

pytestmark = pytest.mark.v31
ROOT_CONFTEST = Path(__file__).resolve().parents[1]/'conftest.py'

REQUIRED = {'test_gate_inventory_anchor.py': ['test_repository_gate_rejects_a_missing_or_unmarked_inventory'],
 'test_v31_context_tree.py': ['test_independent_enumeration_matches_evidence_and_prediction',
                              'test_counts_partition_over_children_with_terminal_bos',
                              'test_support_histogram_counts_observations_including_bos',
                              'test_battery_gate_rejects_incomplete_or_invalid_recorded_results',
                              'test_normalization_rare_and_unseen_support_across_alphabets',
                              'test_empty_training_is_a_valid_core_case',
                              'test_zero_depth_is_a_forced_root_leaf',
                              'test_core_rejects_invalid_parameters_and_symbols',
                              'test_prequential_identity_uses_pre_update_counts',
                              'test_stream_order_does_not_change_the_frozen_model',
                              'test_evaluation_never_mutates_the_frozen_model',
                              'test_extreme_log_prior_keeps_both_weights',
                              'test_stop_saturation_keeps_a_finite_split_weight',
                              'test_saturation_is_distinct_from_a_forced_leaf',
                              'test_generator_fixture_matches_the_historical_script',
                              'test_small_synthetic_battery_meets_plan_thresholds',
                              'test_validation_stage_exits_non_zero_when_a_threshold_fails',
                              'test_validation_cli_rejects_configuration_drift_before_running',
                              'test_validation_output_refuses_raw_including_symlinks',
                              'test_validation_publication_refuses_a_racing_writer',
                              'test_validation_forced_publication_is_atomic_on_write_failure',
                              'test_historical_m106_stress_records_execution_and_oracle_gap'],
 'test_v31_sampling.py': ['test_pinned_rng_vector_and_fixture_ledger_reproduce_the_deposit',
                         'test_deposited_block_keys_recompute_from_their_member_lists',
                         'test_purposes_fields_repeatability_and_no_active_shuffle_probe',
                         'test_one_sample_feeds_both_arms_and_each_sentence_shuffles_independently',
                         'test_held_out_and_inventory_only_never_enter_any_cell_or_fold',
                         'test_exact_budget_without_replacement_and_one_fragment_per_contributor',
                         'test_empty_sentences_stay_in_the_universe_without_spending_budget',
                         'test_canonical_order_and_fragment_offset_match_an_independent_transcription',
                         'test_the_fragment_offset_can_reach_every_contiguous_segment',
                         'test_impossible_budgets_fail_explicitly',
                         'test_record_order_and_labels_do_not_change_the_ledger',
                         'test_declared_ledger_and_permutation_reuse_between_cells',
                         'test_streams_survive_the_parquet_round_trip_of_the_corpus_artifact',
                         'test_each_sentence_or_fragment_is_one_reset_stream_without_separators',
                         'test_shuffle_preserves_length_multiset_mask_and_root_counts',
                         'test_slot_identity_is_distinct_from_the_provenance_of_the_moved_token',
                         'test_shuffled_control_is_not_iid_within_a_stream',
                         'test_heterogeneous_pool_keeps_local_dependence_after_shuffling',
                         'test_module_imports_no_retired_v21_helper'],
 'test_scores.py': ['test_pooled_score_core_has_label_free_signature',
                    'test_annotate_scores_has_d52_signature'],
 'test_v31_scores.py': ['test_public_core_and_annotation_keep_scores_independent_of_labels',
                        'test_annotation_refuses_ambiguous_missing_or_overwriting_registry',
                        'test_four_term_q_reproduces_the_archived_sign_inversion',
                        'test_scoring_rejects_invalid_slot_bijections_and_symbols',
                        'test_unseen_branch_encounter_survives_weight_underflow',
                        'test_q_needs_the_four_terms_of_two_independently_fitted_arms',
                        'test_slots_are_paired_one_to_one_and_a_mismatch_is_refused',
                        'test_shuffled_gain_is_not_automatically_zero_on_a_heterogeneous_pool',
                        'test_losses_sum_through_documents_blocks_and_groups',
                        'test_both_weightings_report_four_components_and_agree_on_d_q',
                        'test_paired_sensitivities_over_the_first_ten_seeds_detect_a_population_mismatch',
                        'test_mixture_masses_and_resolved_length_follow_the_direct_sum',
                        'test_evaluation_diagnostics_count_valid_and_null_resolved_means',
                        'test_an_empty_band_is_null_with_a_reason_and_never_a_false_zero'],
 'test_v31_r1.py': ['test_jsd_is_symmetric_zero_on_the_diagonal_and_bounded_by_one_bit',
                    'test_smoothed_counts_of_the_seven_blocks_and_their_matrix',
                    'test_group_centroids_are_not_the_mean_of_the_pairwise_divergences'],
 'test_v31_config.py': ['test_deposit_and_application_projection_match',
                        'test_schema_refuses_wrong_numeric_types_and_values',
                        'test_application_contract_rejects_drift',
                        'test_yaml_rejects_duplicate_keys_and_registry_drift',
                        'test_deposit_refuses_altered_missing_extra_contracts',
                        'test_legacy_executors_refuse_active_config'],
 'test_v31_corpus.py': ['test_numeric_order_raw_coordinates_empty_reset_and_targets',
                        'test_athenaeus_parts_order_before_ordinal',
                        'test_ambiguous_identities_fail_with_source',
                        'test_public_mapping_rejects_unknown_source_upos',
                        'test_global_merge_subtypes_masks_and_frozen_ids',
                        'test_input_file_order_does_not_change_corpus',
                        'test_diagnostic_a_uses_allowed_upos_per_relation_and_raw_denominator',
                        'test_real_corpus_exact_expected_counts_keys_and_inventories',
                        'test_exact_validator_detects_equal_length_content_and_key_corruption',
                        'test_source_parser_rejects_malformed_rows_with_location',
                        'test_mwt_and_empty_nodes_do_not_change_source_word_ids',
                        'test_validator_rejects_semantic_corruption_at_unchanged_cardinality',
                        'test_b_is_diagnostic_and_keeps_low_retention_documents',
                         'test_coordinate_schema_does_not_silently_cast_float_ids'],
 'test_v31_docs.py': ['test_active_authority_and_instructions_are_aligned',
                      'test_history_and_deposit_are_byte_preserved',
                      'test_test_inventory_explicitly_tracks_future_obligations',
                      'test_all_preserved_v21_documents_match_the_original_hash_inventory',
                      'test_pipeline_does_not_import_candidates_or_inferential_utilities'],
 'test_v31_enforcement.py': ['test_v31_actual_collection_covers_required_behaviors',
                             'test_v31_inventory_rejects_missing_test_and_marker',
                             'test_v31_enforcement_rejects_vacuity_skip_and_xfail',
                             'test_v31_enforcement_accepts_executed_assert'],
 'test_v31_descriptive.py': ['test_cli_runs_every_cell_and_publishes_one_partition_per_pair',
                            'test_every_pair_persists_its_exact_sampling_ledger',
                            'test_sensitivity_checks_coordinate_slot_sets_before_discarding_vectors',
                            'test_seed_zero_trial_resumes_to_full_campaign_without_changing_identity',
                            'test_seed_selection_refuses_undeclared_seed_before_loading_corpus',
                            'test_interrupted_fit_keeps_completed_pairs_and_resume_matches_fresh_run',
                            'test_real_report_requires_v2_and_v3_evidence_as_well_as_corpus',
                            'test_persisted_positions_carry_exactly_the_plan_columns_and_every_eligible_slot',
                            'test_a_cell_selection_leaves_the_other_cells_unpublished',
                            'test_the_fixture_declaration_is_required_and_refused_for_the_deposit',
                            'test_a_second_run_refuses_the_destination_unless_resume_is_asked_for',
                            'test_resume_reuses_validated_partitions_byte_for_byte_and_finishes_the_rest',
                            'test_resume_refuses_a_changed_contract_or_a_changed_corpus',
                            'test_a_corrupted_partition_is_detected_and_never_reused',
                            'test_an_interrupted_write_publishes_nothing_and_leaves_the_prior_state_intact',
                            'test_a_kill_between_the_hard_link_and_the_manifest_blocks_resume_by_name',
                            'test_the_manifest_refuses_duplicate_extra_and_missing_keys',
                            'test_two_destinations_publish_the_same_partitions_byte_for_byte',
                            'test_report_cli_emits_every_declared_table_from_a_complete_campaign',
                            'test_report_reconstructs_documents_blocks_and_groups_from_the_persisted_positions',
                            'test_arm_diagnostics_keep_the_document_dimension_the_loss_sums_carry',
                            'test_report_refuses_an_incomplete_campaign_and_any_inventory_only_score',
                            'test_report_refuses_a_run_that_is_not_the_deposited_configuration',
                            'test_report_refuses_a_second_emission_and_a_partition_added_after_it',
                            'test_evidence_must_be_recorded_under_the_code_and_lock_of_this_run',
                            'test_retired_stages_declare_their_retirement_and_refuse_to_run',
                            'test_the_descriptive_path_imports_no_retired_scientific_module',
                            'test_the_documented_command_lines_run_the_whole_toy_campaign'],
 'test_v31_completion.py': ['test_scientific_identity_verifies_the_present_lock', 'test_model_keys_reject_noninteger_seed_without_coercion', 'test_zero_target_documents_keep_both_bands_and_null_reasons', 'test_per_model_resources_are_measured_and_kept_out_of_deterministic_artifacts', 'test_resume_rejects_invalid_artifact_families_and_model_arms', 'test_resume_rejects_semantically_corrupt_sums_even_after_rehashing', 'test_resource_records_are_complete_valid_and_bound_to_model_keys'],
 'test_v31_report_semantics.py': ['test_partition_semantic_corruption_is_rejected', 'test_partial_campaign_validates_and_float_reconstruction_allows_roundoff', 'test_root_distribution_preserves_empirical_and_smoothed_frequencies', 'test_duplicate_json_fields_in_pair_are_rejected'],
 'test_v31_persistence.py': ['test_exact_three_inputs_and_hashes',
                             'test_identity_excludes_locations_and_is_sensitive_to_components',
                             'test_atomic_roundtrip_and_same_run_in_distinct_directories',
                             'test_encode_updates_one_manifest_without_overwriting_audit',
                             'test_corruption_prevents_stage_reuse',
                             'test_interrupted_write_never_publishes_stage',
                             'test_destinations_with_existing_files_are_preserved',
                             'test_output_raw_and_symlink_rejected',
                             'test_input_staging_binds_hash_to_processed_bytes_and_detects_changes',
                             'test_before_publication_input_failure_leaves_prior_stage_intact',
                             'test_concurrent_reservation_refuses_second_writer',
                             'test_manifest_schema_rejects_ambiguous_json']}


def missing_coverage(items, required):
    collected=defaultdict(set)
    for item in items:
        if item.get_closest_marker('v31') is not None:
            collected[Path(item.path).name].add(getattr(item,'originalname',None) or item.name.split('[',1)[0])
    return {file:sorted(set(names)-collected[file]) or ['empty inventory']
            for file,names in required.items() if not names or set(names)-collected[file]}


def test_v31_actual_collection_covers_required_behaviors(request):
    assert REQUIRED
    assert not missing_coverage(request.session.items,REQUIRED)


def test_v31_inventory_rejects_missing_test_and_marker():
    item=SimpleNamespace(path=Path('test_a.py'),name='test_a',get_closest_marker=lambda marker:None)
    assert missing_coverage([item],{'test_a.py':['test_a']})=={'test_a.py':['test_a']}
    assert missing_coverage([],{'test_a.py':[]})=={'test_a.py':['empty inventory']}


@pytest.mark.parametrize('body',[
    'def test_bad(): pass',
    'def test_bad():\n    if False: assert True',
    'def test_bad(): pytest.skip("no")',
    '@pytest.mark.xfail\ndef test_bad(): assert False',
    'pytest.skip("no", allow_module_level=True)\ndef test_bad(): assert True',
])
def test_v31_enforcement_rejects_vacuity_skip_and_xfail(pytester,body):
    pytester.makeconftest(ROOT_CONFTEST.read_text())
    pytester.makepyprojecttoml('[tool.pytest.ini_options]\nmarkers=["v31: active"]\nenable_assertion_pass_hook=true\n')
    pytester.makepyfile('import pytest\npytestmark=pytest.mark.v31\n'+body)
    result=pytester.runpytest_subprocess('-m','v31','--strict-markers')
    assert result.ret!=0


def test_v31_enforcement_accepts_executed_assert(pytester):
    pytester.makeconftest(ROOT_CONFTEST.read_text())
    pytester.makepyprojecttoml('[tool.pytest.ini_options]\nmarkers=["v31: active"]\nenable_assertion_pass_hook=true\n')
    pytester.makepyfile('import pytest\npytestmark=pytest.mark.v31\ndef test_good(): assert 2+2==4')
    result=pytester.runpytest_subprocess('-m','v31','--strict-markers')
    assert result.ret==0
