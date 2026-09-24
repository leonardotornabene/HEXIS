"""Active V0–V2 must collect all required tests and execute real assertions."""
from collections import Counter, defaultdict
from pathlib import Path
from types import SimpleNamespace

import pytest

pytestmark = pytest.mark.v31
ROOT_CONFTEST = Path(__file__).resolve().parents[1]/'conftest.py'

REQUIRED = {'test_gate_inventory_anchor.py': ['test_repository_gate_rejects_a_missing_or_unmarked_inventory'],
 'test_conllu_reader.py': ['test_malformed_row_raises_parse_error_with_location',
                           'test_missing_sent_id_raises_parse_error',
                           'test_id_order_preserved',
                           'test_out_of_order_integer_ids_raise_parse_error',
                           'test_mwt_range_and_empty_nodes_removed',
                           'test_punct_token_yielded_unchanged',
                           'test_newdoc_id_recoverable_from_metadata',
                           'test_public_type_and_streaming_failure_boundary',
                           'test_invalid_required_labels_raise_parse_error',
                           'test_conllu_parse_exception_is_wrapped',
                           'test_representation_exclusions_are_yielded_unchanged'],
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
                              'test_historical_m106_stress_records_execution_and_oracle_gap',
                              'test_analytic_pass_pins_the_corrected_iid_threshold'],
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
                         'test_module_imports_no_retired_v21_helper',
                         'test_sample_streams_refuses_a_ledger_cut_from_a_shorter_variant',
                         'test_shuffle_records_the_symbol_change_rate_with_an_explicit_denominator'],
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
                        'test_an_empty_band_is_null_with_a_reason_and_never_a_false_zero',
                        'test_pooled_core_refuses_an_alphabet_size_mismatch',
                        'test_pooled_core_refuses_a_negative_min_available_past',
                        'test_roll_up_casts_count_columns_to_int64_in_both_branches',
                        'test_contrasts_refuse_a_q_that_is_not_the_gain_difference',
                        'test_public_core_keeps_the_label_free_signature',
                        'test_annotation_keeps_the_registry_signature'],
 'test_v31_r1.py': ['test_jsd_is_symmetric_zero_on_the_diagonal_and_bounded_by_one_bit',
                    'test_smoothed_counts_of_the_seven_blocks_and_their_matrix',
                    'test_group_centroids_are_not_the_mean_of_the_pairwise_divergences',
                    'test_matrix_orders_blocks_alphabetically_like_pairs_regardless_of_insertion_order'],
 'test_v31_config.py': ['test_deposit_and_application_projection_match',
                        'test_schema_refuses_wrong_numeric_types_and_values',
                        'test_application_contract_rejects_drift',
                        'test_yaml_rejects_duplicate_keys_and_registry_drift',
                        'test_deposit_refuses_altered_missing_extra_contracts',
                        'test_the_alphabet_reads_the_active_projection_only',
                        'test_duplicate_yaml_keys_are_rejected_at_every_depth',
                        'test_a_yaml_error_names_the_original_file_and_keeps_its_snippet'],
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
                         'test_coordinate_schema_does_not_silently_cast_float_ids',
                        'test_subtype_stripping_is_total_and_lowercases_every_colon',
                        'test_propn_is_mapped_to_noun_before_retention',
                        'test_excluded_source_upos_drops_before_any_deprel_rule',
                        'test_excluded_deprel_drops_with_its_base_label_or_is_absorbed_by_oth',
                        'test_the_merge_follows_retention_so_an_excluded_token_keeps_its_source_upos',
                        'test_mapped_token_is_immutable',
                        'test_map_tokens_keeps_a_boolean_mask_on_an_empty_table',
                        'test_an_unknown_alphabet_variant_is_refused'],
 'test_v31_docs.py': ['test_active_authority_and_instructions_are_aligned',
                      'test_the_v3_001_acts_are_never_rewritten',
                      'test_the_package_is_hormathos_and_hexis_names_only_the_design',
                      'test_the_deposit_and_the_lock_are_byte_preserved',
                      'test_the_sdist_ships_exactly_the_tracked_tree',
                      'test_all_preserved_v21_documents_match_the_original_hash_inventory',
                      'test_the_archive_is_a_record_and_never_a_dependency',
                      'test_every_archived_file_has_its_bytes_at_the_base',
                      'test_test_inventory_explicitly_tracks_future_obligations',
                      'test_pipeline_does_not_import_candidates_or_inferential_utilities',
                      'test_the_three_standing_instruction_copies_are_identical'],
 'test_v31_enforcement.py': ['test_v31_actual_collection_covers_required_behaviors',
                             'test_v31_inventory_rejects_missing_test_and_marker',
                             'test_v31_enforcement_rejects_vacuity_skip_and_xfail',
                             'test_v31_enforcement_accepts_executed_assert',
                             'test_v31_inventory_lists_every_collected_active_test',
                             'test_v31_enforcement_rejects_a_static_skip_and_an_xpass_without_strict_xfail',
                             'test_v31_enforcement_invalidates_pyc_compiled_without_the_assertion_hook',
                              'test_every_collected_test_is_active_acceptance',
                              'test_the_archive_is_never_collected_even_from_the_root'],
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
                            'test_retired_stages_do_not_exist',
                            'test_retired_v21_modules_do_not_exist',
                            'test_the_v21_configuration_api_is_gone',
                            'test_the_descriptive_path_imports_no_retired_scientific_module',
                            'test_the_documented_command_lines_run_the_whole_toy_campaign',
                            'test_report_refuses_a_document_silently_dropped_from_document_scores'],
 'test_v31_completion.py': ['test_scientific_identity_verifies_the_present_lock', 'test_model_keys_reject_noninteger_seed_without_coercion', 'test_zero_target_documents_keep_both_bands_and_null_reasons', 'test_per_model_resources_are_measured_and_kept_out_of_deterministic_artifacts', 'test_resume_rejects_invalid_artifact_families_and_model_arms', 'test_resume_rejects_semantically_corrupt_sums_even_after_rehashing', 'test_resource_records_are_complete_valid_and_bound_to_model_keys', 'test_diagnostics_carry_the_report_contract_names',
                           'test_report_summarizes_every_level_and_pairs_sensitivities_per_block_and_seed',
                           'test_empty_document_summaries_stay_null_with_their_reason',
                           'test_seed_zero_regeneration_is_compared_and_recorded_by_the_report',
                           'test_a_scientific_report_requires_the_seed_zero_regeneration'],
 'test_v31_validation_run.py': ['test_acceptance_checks_actual_junit_collection_and_process',
                                'test_acceptance_rejects_vacuity_skip_and_failure',
                                'test_validation_cli_requires_both_directories_and_protects_raw',
                                'test_new_schema_refuses_old_run_without_rewriting_it',
                                'test_seed_zero_technical_keys_are_distinct_from_campaign_keys',
                                'test_validation_evidence_survives_descriptive_progress_and_resume',
                                'test_report_refuses_changed_v2_execution_context',
                                'test_invalid_validation_evidence_blocks_fits',
                                'test_validation_refuses_changed_execution_context_without_publication',
                                'test_technical_completion_is_fixture_only_and_requires_the_exact_seed_zero_set',
                                'test_seed_zero_single_cell_keeps_v3_pending',
                                'test_real_fit_requires_clean_tracked_producers',
                                'test_recorded_v3_evidence_is_recomputed_never_trusted'],
 'test_v31_figures.py': ['test_report_emits_the_five_contract_figures_as_deterministic_svg',
                         'test_plotted_values_are_the_verified_table_values',
                         'test_structured_model_columns_are_canonical_json',
                         'test_figures_read_tables_only',
                         'test_mixture_mass_axis_stops_at_the_reference_depth',
                         'test_profiles_label_documents_by_author_work_and_targets',
                         'test_corpus_figure_orders_documents_by_group_then_block',
                         'test_r1_tables_and_figure_name_every_symbol',
                         'test_sensitivity_figure_follows_the_declared_cell_order',
                         'test_every_figure_keeps_its_text_inside_the_canvas'],
 'test_v31_report_semantics.py': ['test_partition_semantic_corruption_is_rejected', 'test_partial_campaign_validates_and_float_reconstruction_allows_roundoff', 'test_root_distribution_preserves_empirical_and_smoothed_frequencies', 'test_duplicate_json_fields_in_pair_are_rejected',
                                  'test_the_persisted_ledger_is_the_contract_sample_even_after_rehashing',
                                  'test_shuffle_counts_and_c0_provenance_are_the_contract_regeneration',
                                  'test_each_c0_guard_names_its_own_corruption',
                                  'test_sensitivity_partitions_enforce_diagnostic_denominators_and_bounds'],
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
                             'test_manifest_schema_rejects_ambiguous_json',
                             'test_sha256_file_is_the_hash_of_the_bytes_on_disk',
                             'test_a_destination_inside_the_repository_raw_root_is_refused_under_any_data_root']}


EXPECTED_CASES = {
    ('test_conllu_reader.py', 'test_invalid_required_labels_raise_parse_error'): 2,
    ('test_gate_inventory_anchor.py', 'test_repository_gate_rejects_a_missing_or_unmarked_inventory'): 2,
    ('test_v31_completion.py', 'test_model_keys_reject_noninteger_seed_without_coercion'): 2,
    ('test_v31_completion.py', 'test_resource_records_are_complete_valid_and_bound_to_model_keys'): 4,
    ('test_v31_completion.py', 'test_resume_rejects_invalid_artifact_families_and_model_arms'): 4,
    ('test_v31_config.py', 'test_application_contract_rejects_drift'): 6,
    ('test_v31_config.py', 'test_deposit_refuses_altered_missing_extra_contracts'): 3,
    ('test_v31_config.py', 'test_duplicate_yaml_keys_are_rejected_at_every_depth'): 2,
    ('test_v31_config.py', 'test_schema_refuses_wrong_numeric_types_and_values'): 6,
    ('test_v31_context_tree.py', 'test_battery_gate_rejects_incomplete_or_invalid_recorded_results'): 10,
    ('test_v31_context_tree.py', 'test_core_rejects_invalid_parameters_and_symbols'): 23,
    ('test_v31_context_tree.py', 'test_empty_training_is_a_valid_core_case'): 3,
    ('test_v31_context_tree.py', 'test_independent_enumeration_matches_evidence_and_prediction'): 3,
    ('test_v31_context_tree.py', 'test_normalization_rare_and_unseen_support_across_alphabets'): 3,
    ('test_v31_context_tree.py', 'test_prequential_identity_uses_pre_update_counts'): 3,
    ('test_v31_context_tree.py', 'test_support_histogram_counts_observations_including_bos'): 6,
    ('test_v31_context_tree.py', 'test_validation_output_refuses_raw_including_symlinks'): 2,
    ('test_v31_corpus.py', 'test_ambiguous_identities_fail_with_source'): 5,
    ('test_v31_corpus.py', 'test_excluded_source_upos_drops_before_any_deprel_rule'): 12,
    ('test_v31_corpus.py', 'test_public_mapping_rejects_unknown_source_upos'): 4,
    ('test_v31_corpus.py', 'test_source_parser_rejects_malformed_rows_with_location'): 7,
    ('test_v31_corpus.py', 'test_validator_rejects_semantic_corruption_at_unchanged_cardinality'): 6,
    ('test_v31_descriptive.py', 'test_a_corrupted_partition_is_detected_and_never_reused'): 6,
    ('test_v31_descriptive.py', 'test_retired_stages_do_not_exist'): 6,
    ('test_v31_descriptive.py', 'test_retired_v21_modules_do_not_exist'): 5,
    ('test_v31_descriptive.py', 'test_sensitivity_checks_coordinate_slot_sets_before_discarding_vectors'): 2,
    ('test_v31_descriptive.py', 'test_the_manifest_refuses_duplicate_extra_and_missing_keys'): 8,
    ('test_v31_enforcement.py', 'test_v31_enforcement_rejects_a_static_skip_and_an_xpass_without_strict_xfail'): 3,
    ('test_v31_enforcement.py', 'test_v31_enforcement_rejects_vacuity_skip_and_xfail'): 5,
    ('test_v31_persistence.py', 'test_corruption_prevents_stage_reuse'): 6,
    ('test_v31_persistence.py', 'test_manifest_schema_rejects_ambiguous_json'): 3,
    ('test_v31_pre_v3_audit.py', 'test_acceptance_rejects_junit_failure_even_with_zero_process_status'): 2,
    ('test_v31_pre_v3_audit.py', 'test_manifest_commit_exception_preserves_the_published_state'): 2,
    ('test_v31_pre_v3_audit.py', 'test_scientific_manifest_commit_exception_keeps_a_valid_fixture_run'): 2,
    ('test_v31_report_semantics.py', 'test_each_c0_guard_names_its_own_corruption'): 4,
    ('test_v31_report_semantics.py', 'test_partition_semantic_corruption_is_rejected'): 25,
    ('test_v31_report_semantics.py', 'test_sensitivity_partitions_enforce_diagnostic_denominators_and_bounds'): 2,
    ('test_v31_report_semantics.py', 'test_shuffle_counts_and_c0_provenance_are_the_contract_regeneration'): 2,
    ('test_v31_report_semantics.py', 'test_the_persisted_ledger_is_the_contract_sample_even_after_rehashing'): 3,
    ('test_v31_sampling.py', 'test_canonical_order_and_fragment_offset_match_an_independent_transcription'): 6,
    ('test_v31_sampling.py', 'test_impossible_budgets_fail_explicitly'): 5,
    ('test_v31_scores.py', 'test_annotation_refuses_ambiguous_missing_or_overwriting_registry'): 4,
    ('test_v31_scores.py', 'test_scoring_rejects_invalid_slot_bijections_and_symbols'): 5,
    ('test_v31_validation_run.py', 'test_acceptance_rejects_vacuity_skip_and_failure'): 3,
    ('test_v31_validation_run.py', 'test_invalid_validation_evidence_blocks_fits'): 5,
    ('test_v31_validation_run.py', 'test_recorded_v3_evidence_is_recomputed_never_trusted'): 3,
    ('test_v31_validation_run.py', 'test_report_refuses_changed_v2_execution_context'): 2,
}


def parameterized_counts(items):
    counts = Counter((Path(item.path).name,
                      getattr(item, 'originalname', None) or item.name.split('[', 1)[0])
                     for item in items if hasattr(item, 'callspec'))
    return dict(counts)


REQUIRED['test_v31_pre_v3_audit.py'] = [
    'test_manifest_commit_exception_preserves_the_published_state',
    'test_scientific_manifest_commit_exception_keeps_a_valid_fixture_run',
    'test_extra_ds_store_is_named_in_v1_and_deposit',
    'test_spread_accepts_one_rounding_unit_only',
    'test_regeneration_tolerance_is_absolute_and_scales_only_loss_sums',
    'test_regeneration_rejects_changed_integer_identity_in_parquet',
    'test_raw_alias_is_rejected_even_when_case_differs',
    'test_fixture_cannot_reuse_the_deposited_spec_version',
    'test_sample_fold_rejects_a_document_in_two_blocks_before_training',
    'test_load_corpus_reads_the_validated_private_copy',
    'test_category_order_cannot_hide_swapped_document_order',
    'test_parser_consumes_the_copied_v1_input',
    'test_descriptive_context_change_cannot_publish_a_pair',
    'test_acceptance_rejects_junit_failure_even_with_zero_process_status',
]
REQUIRED['test_v31_enforcement.py'] += [
    'test_collection_skip_without_marker_fails_the_gate',
    'test_nested_conftest_collection_skip_fails_the_gate',
    'test_parameterized_case_counts_match_the_reviewed_inventory',
    'test_parameterized_case_gate_catches_one_removed_case',
]

def missing_coverage(items, required):
    collected=defaultdict(set)
    for item in items:
        if item.get_closest_marker('v31') is not None:
            collected[Path(item.path).name].add(getattr(item,'originalname',None) or item.name.split('[',1)[0])
    return {file:sorted(set(names)-collected[file]) or ['empty inventory']
            for file,names in required.items() if not names or set(names)-collected[file]}


def unlisted_tests(items, required):
    return sorted({(Path(item.path).name, getattr(item, 'originalname', None) or item.name.split('[', 1)[0])
                   for item in items if item.get_closest_marker('v31') is not None}
                  - {(file, name) for file, names in required.items() for name in names})


def test_v31_actual_collection_covers_required_behaviors(request):
    assert REQUIRED
    assert not missing_coverage(request.session.items,REQUIRED)


def test_v31_inventory_lists_every_collected_active_test(request):
    """Exhaustive inventory: an active test outside REQUIRED could be deleted unnoticed."""
    assert not unlisted_tests(request.session.items, REQUIRED)


def test_parameterized_case_counts_match_the_reviewed_inventory(request):
    assert parameterized_counts(request.session.items) == EXPECTED_CASES


def test_parameterized_case_gate_catches_one_removed_case(request):
    items = request.session.items
    target = next(item for item in items if item.nodeid.startswith(
        'tests/test_v31_context_tree.py::test_core_rejects_invalid_parameters_and_symbols['))
    assert parameterized_counts([item for item in items if item is not target]) != EXPECTED_CASES


def test_v31_inventory_rejects_missing_test_and_marker():
    item=SimpleNamespace(path=Path('test_a.py'),name='test_a',get_closest_marker=lambda marker:None)
    assert missing_coverage([item],{'test_a.py':['test_a']})=={'test_a.py':['test_a']}
    assert missing_coverage([],{'test_a.py':[]})=={'test_a.py':['empty inventory']}
    marked = SimpleNamespace(path=Path('test_b.py'), name='test_b[x]', originalname='test_b',
                             get_closest_marker=lambda marker: object())
    assert unlisted_tests([marked], {}) == [('test_b.py', 'test_b')]


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


def test_collection_skip_without_marker_fails_the_gate(pytester):
    run = _project(pytester)
    pytester.makepyfile(test_good='import pytest\npytestmark=pytest.mark.v31\ndef test_good(): assert True',
                        test_skipped='import pytest\npytest.skip("module skip", allow_module_level=True)')
    result = run()
    assert result.ret != 0
    result.stdout.fnmatch_lines(['*GATE FAILURE*collection skip*'])


def test_nested_conftest_collection_skip_fails_the_gate(pytester):
    run = _project(pytester)
    pytester.makepyfile(test_good='import pytest\npytestmark=pytest.mark.v31\ndef test_good(): assert True')
    nested = pytester.path/'nested'
    nested.mkdir()
    (nested/'conftest.py').write_text('import pytest\npytest.skip("nested skip", allow_module_level=True)')
    (nested/'test_nested.py').write_text('import pytest\npytestmark=pytest.mark.v31\ndef test_nested(): assert True')
    result = run()
    assert result.ret != 0
    result.stdout.fnmatch_lines(['*GATE FAILURE*collection skip*'])


# --- enforcement mechanics carried over from the v2.1 gate suite -----------------


def _project(pytester, *, assertion_pass=True, xfail_strict=False):
    pytester.makeconftest(ROOT_CONFTEST.read_text())
    pytester.makepyprojecttoml(
        '[tool.pytest.ini_options]\nmarkers=["v31: active"]\n'
        f'enable_assertion_pass_hook={str(assertion_pass).lower()}\n'
        + ('xfail_strict=true\n' if xfail_strict else ''))
    return lambda: pytester.runpytest_subprocess('-m', 'v31', '--strict-markers')


@pytest.mark.parametrize('body', [
    '@pytest.mark.skip("static")\ndef test_bad(): assert True',
    '@pytest.mark.xfail(reason="but passes")\ndef test_bad(): assert True',
    '@pytest.mark.xfail(reason="but passes", strict=False)\ndef test_bad(): assert True',
])
def test_v31_enforcement_rejects_a_static_skip_and_an_xpass_without_strict_xfail(pytester, body):
    """The gate must not depend on `xfail_strict`: a non-strict xpass is green to
    pytest and still has to fail the acceptance."""
    run = _project(pytester)
    pytester.makepyfile('import pytest\npytestmark=pytest.mark.v31\n' + body)
    assert run().ret != 0


def test_v31_enforcement_invalidates_pyc_compiled_without_the_assertion_hook(pytester):
    """A cached .pyc compiled without the assertion-pass hook would make every
    assert invisible, so the gate would read a real test as assertion-free."""
    run = _project(pytester, assertion_pass=False)
    pytester.makepyfile('import pytest\npytestmark=pytest.mark.v31\ndef test_ok(): assert 1 == 1')
    assert run().ret != 0
    run = _project(pytester, assertion_pass=True)
    assert run().ret == 0


def test_every_collected_test_is_active_acceptance(pytester):
    """A test without the marker is refused at collection, so `pytest` and
    `pytest -m v31` cannot drift apart."""
    run = _project(pytester)
    pytester.makepyfile(test_unmarked='def test_outside(): assert True')
    result = run()
    assert result.ret != 0
    result.stderr.fnmatch_lines(['*every collected test must carry pytest.mark.v31*'])


def test_the_archive_is_never_collected_even_from_the_root(pytester):
    """`archive/` is a record (V3-002): the real configuration keeps its suites out of
    collection whether pytest starts from `testpaths` or from the root."""
    pytester.makeconftest(ROOT_CONFTEST.read_text())
    pytester.makepyprojecttoml((ROOT_CONFTEST.parent/'pyproject.toml').read_text())
    for directory in ('tests', 'archive/tests'):
        (pytester.path/directory).mkdir(parents=True)
    (pytester.path/'tests/test_ok.py').write_text(
        'import pytest\npytestmark = pytest.mark.v31\ndef test_ok(): assert 1 == 1\n')
    (pytester.path/'archive/tests/test_old.py').write_text(
        'import hexis_retired_module\ndef test_old(): assert True\n')
    for args in ((), ('.',)):
        result = pytester.runpytest_subprocess(*args)
        assert result.ret == 0, args
        result.assert_outcomes(passed=1)
