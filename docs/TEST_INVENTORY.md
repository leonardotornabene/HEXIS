# HORMATHOS test inventory — design HEXIS 3.1, V3-001, V3-002, V3-003

Active acceptance: **every collected test is `v31`**, with an executed assert and no skip,
xfail or xpass. `pytest` and `pytest -m v31` collect the same tests: the rule is enforced
in `conftest.py` at collection, not read off the summary by eye. The named inventory in
`tests/test_v31_enforcement.py` must match the actual collection in both directions.
The comparison with the deposited contract does not replace the CTW tests, and the four
deposited CTW fixtures are identified, not executed.
The named inventory also pins reviewed case counts for every parametrized test; removing one
parameter case fails acceptance.

## Obligations T01–T30 of §12

| ID | Status | Coverage / remaining obligation |
|---|---|---|
| T01 | V1 | Inputs/hashes, sent_id, 18 prefixes/17 documents |
| T02 | V1 | Document/block counts and whole corpus |
| T03 | V1 | Parsing, coordinates, identity, located errors |
| T04 | V1 | Global mapping, inventories, C0/UPOS, inventory_only |
| T05 | V2 | Held-out and `inventory_only` excluded from training, in all six cells for seven folds |
| T06 | V2 | Exact q, no replacement, ≤1 fragment per contributor, empty and impossible budgets |
| T07 | V2 | Source order; sampler invariant to record order and blind to labels; reuse of ledger and permutation as declared |
| T08 | V2 | §12.2 vector and seven deposited `block_key`s, separate purposes, repeatability, O/R pairing; no probe purpose active |
| T09 | V2 | Streams/reset and exact partition of the sample; terminal BOS and partition of counts in T10–T11 |
| T10 | V2 | Independent enumeration of the admissible trees against evidence, root weight and prediction |
| T11 | V2 | Normalisation, rare/unseen support, empty training, D=0, m100/105/11, strict inputs |
| T12 | V2 | Prequential/integrated identity before update; invariance to stream order |
| T13 | V2 | Counts/evidence/weights/fingerprint unchanged by evaluation |
| T14 | V2 | Extreme prior in log space, two weights from δ, saturation distinct from forced leaves |
| T15 | V2 | 25 synthetic sources at the §12.1 thresholds on the canonical CTW; violation → non-zero exit |
| T16 | V2 | Historical m106 stress: execution, normalisation, supports, recorded deficit |
| T17 | V2 | Length, multiset, mask and root counts preserved; slot distinct from provenance |
| T18 | V2 | Counterexamples of internal dependence and of a heterogeneous pool at sample level and in G/Q: non-null G_R with two fitted models |
| T19 | V2 | Four-term Q; archived sign-inversion counterexample reproduced on the canonical CTW |
| T20 | V2 | Aggregations/two weights |
| T21 | V2 | Paired sensitivities |
| T22 | V2 | Masses/supports/L_resolved |
| T23 | V2 | R1 |
| T24 | CODE pre-V3, EXECUTION PENDING V5 | Census of the six inventory_only (V1); the report validator regenerates every ledger from the RNG contract, so no held-out/inventory_only in training, and refuses any inventory_only scoring: code and tests in `0dc69b5`; execution on the campaign in V5 |
| T25 | PENDING V4 | Equality of the 490/980 model/pair keys |
| T26 | V2 | Atomicity/interruption, resume, corruption, duplicates and extra keys: corpus (V1) and scientific stage (V2) |
| T27 | CODE V2, EXECUTION PENDING V5 | Reconstruction of scores/diagnostics and five figures: code and fixture tests in `559dc40`, fixes from the pre-V3 review (samples, shuffle and C0 provenance regenerated; figures readable at real cardinality) in `0dc69b5`; execution on real data in V5 |
| T28 | V0–V1 | Pipeline without candidates/inference; acceptance without skip |
| T29 | PARTIAL V1 | Corpus identity/round trip; samples and shuffle regenerated for every pair (`0dc69b5`); CE/model reproduction PENDING V5 |
| T30 | PENDING V5 | Complete scientific report |

## What each active file proves

| File | Properties |
|---|---|
| `test_v31_config.py` | Deposit and projection field by field, refused types and values, safe YAML and duplicates at every depth, error naming the original file, isolation of non-3.1 configurations |
| `test_conllu_reader.py` | Streaming parsing, identity and order, MWT and empty-node rows, located errors, blindness to the representation |
| `test_v31_corpus.py` | T01–T04: exact real census, coordinates and numeric order, parts and ordinals, mapping, ADV/PART merge, masks, targets, A/B diagnostics, semantic corruptions |
| `test_v31_persistence.py` | T26/T29: three exact inputs, staging of the bytes read, run identity, atomic publication, collisions and concurrency, interruption, corruption, destinations outside the raw data |
| `test_v31_context_tree.py` | T10–T16: independent enumeration, BOS and partition, numerics, prequential identity, frozen model, §12.1 battery and m=106 stress |
| `test_v31_sampling.py` | T05–T09, T17–T18: deposited RNG vector, ledger, exclusions, fragments, reset streams without separators, paired shuffle |
| `test_v31_scores.py` | T19–T22: four losses, paired slots, four-term Q, two weightings, diagnostics and the public signatures of §11.1 |
| `test_v31_r1.py` | T23: JSD, symmetry, centroids and contributions |
| `test_v31_descriptive.py`, `test_v31_completion.py`, `test_v31_report_semantics.py` | Runner and report on fixtures: partitions, resume, evidence, keys, regeneration, semantic guards; absence of the retired modules |
| `test_v31_validation_run.py` | V2/V3 evidence executed and rechecked; the report refuses a changed V2 context, also during generation; a single cell at seed 0 leaves V3 pending; real fits require clean tracked producers |
| `test_v31_figures.py` | The five figures of §11.6, derived from the verified tables |
| `test_v31_docs.py` | Active authority, deposit integrity, archive at the bytes of `5f1ec06` file by file, identity of the three instruction copies, absence of retired imports; the package is `hormathos` and `hexis` is not importable, and the sdist is exactly the tracked tree (V3-003) |
| `test_v31_enforcement.py`, `test_gate_inventory_anchor.py` | The gate itself: exhaustive inventory in both directions, refusal of skip, xfail, xpass even when not strict, missing or dead assert, `.pyc` without the hook, test without marker, missing or unmarked anchor, archive never collected, not even from the root |
| `test_v31_pre_v3_audit.py` | Pre-V3 audit regressions: publication commit, named extras, plotting rounding, regeneration tolerance and exact Parquet identities, raw aliases, fixtures, block overlap, private corpus read, lexical order, staged parser input, descriptive context and JUnit outcomes |

## Map of the previous tests (§13.2: kept, replaced, retired)

Every test function collected at `5f1ec06` and not marked `v31` has a destination.
"Migrated" means the property is now in an active test; "covered" that an active test
already proved it; "replaced" that 3.1 requires another property, named here; "archived"
that the property holds only for the retired code, preserved in `archive/` and executable
at `5f1ec06`. Test paths are those of `5f1ec06`; the package of that commit is `hexis`.

| Test at `5f1ec06` | Destination | Note |
|---|---|---|
| `tests/test_alphabet.py::test_drop_rules` | migrated | test_v31_corpus.py::test_excluded_source_upos_drops_before_any_deprel_rule |
| `tests/test_alphabet.py::test_excluded_deprel_dropped_under_primary_policy` | migrated | test_v31_corpus.py::test_excluded_deprel_drops_with_its_base_label_or_is_absorbed_by_oth |
| `tests/test_alphabet.py::test_inconsistent_alphabet_configuration_raises` | replaced | the v2.1 variant+policy cell does not exist: test_v31_corpus.py::test_an_unknown_alphabet_variant_is_refused |
| `tests/test_alphabet.py::test_mapped_token_is_immutable` | migrated | test_v31_corpus.py::test_mapped_token_is_immutable |
| `tests/test_alphabet.py::test_oth_arm` | migrated | test_v31_corpus.py::test_excluded_deprel_drops_with_its_base_label_or_is_absorbed_by_oth |
| `tests/test_alphabet.py::test_propn_maps_to_noun` | migrated | test_v31_corpus.py::test_propn_is_mapped_to_noun_before_retention |
| `tests/test_alphabet.py::test_subtype_stripping_incl_multi_colon` | migrated | test_v31_corpus.py::test_subtype_stripping_is_total_and_lowercases_every_colon |
| `tests/test_alphabet.py::test_synthetic_conllu_with_mwt_and_empty_node` | covered | test_v31_corpus.py::test_mwt_and_empty_nodes_do_not_change_source_word_ids |
| `tests/test_alphabet.py::test_totality_on_any_ud_label` | replaced | 3.1 refuses an unknown source UPOS instead of dropping it (§13.2): test_v31_corpus.py::test_public_mapping_rejects_unknown_source_upos |
| `tests/test_alphabet.py::test_upos_only_alphabet_is_the_twelve_retained_tags` | replaced | with ADV_PART the upos_only alphabet has 11 symbols: test_v31_corpus.py::test_real_corpus_exact_expected_counts_keys_and_inventories |
| `tests/test_alphabet.py::test_upos_only_keeps_the_retention_rules` | covered | test_v31_corpus.py::test_global_merge_subtypes_masks_and_frozen_ids |
| `tests/test_alphabet.py::test_upos_rule_precedes_deprel_rule` | migrated | test_v31_corpus.py::test_excluded_source_upos_drops_before_any_deprel_rule |
| `tests/test_blocks.py::test_empty_and_all_dropped_documents_produce_no_blocks` | archived with blocks.py | v2.1 chunks; the 3.1 dependency block is a different object (§13.2) |
| `tests/test_blocks.py::test_invalid_block_parameters_fail_loud` | archived with blocks.py | v2.1 chunks; the 3.1 dependency block is a different object (§13.2) |
| `tests/test_blocks.py::test_never_spans_documents` | archived with blocks.py | v2.1 chunks; the 3.1 dependency block is a different object (§13.2) |
| `tests/test_blocks.py::test_oversized_sentence_is_its_own_block` | archived with blocks.py | v2.1 chunks; the 3.1 dependency block is a different object (§13.2) |
| `tests/test_blocks.py::test_sentence_aligned_fill` | archived with blocks.py | v2.1 chunks; the 3.1 dependency block is a different object (§13.2) |
| `tests/test_blocks.py::test_tail_kept_iff_at_least_min_frac` | archived with blocks.py | v2.1 chunks; the 3.1 dependency block is a different object (§13.2) |
| `tests/test_bootstrap_holm.py::test_bootstrap_fails_loud_on_wrong_group_count` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_bootstrap_holm.py::test_bootstrap_rejects_invalid_input_domain` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_bootstrap_holm.py::test_bootstrap_reproducible_under_fixed_seed` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_bootstrap_holm.py::test_bootstrap_resamples_within_groups_only` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_bootstrap_holm.py::test_bootstrap_supports_unweighted_p1_mean_with_unequal_groups` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_bootstrap_holm.py::test_holm_adjusted_is_monotone_nondecreasing` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_bootstrap_holm.py::test_holm_boundary_and_order_invariance` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_bootstrap_holm.py::test_holm_family_of_two_thresholds` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_bootstrap_holm.py::test_holm_rejects_invalid_probability_domain` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_bootstrap_holm.py::test_holm_step_down_stops_at_first_non_reject` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_conllu_reader.py::test_conllu_parse_exception_is_wrapped` | v31 in place | active 3.1 reader; marked v31, no change of content |
| `tests/test_conllu_reader.py::test_id_order_preserved` | v31 in place | active 3.1 reader; marked v31, no change of content |
| `tests/test_conllu_reader.py::test_invalid_required_labels_raise_parse_error` | v31 in place | active 3.1 reader; marked v31, no change of content |
| `tests/test_conllu_reader.py::test_malformed_row_raises_parse_error_with_location` | v31 in place | active 3.1 reader; marked v31, no change of content |
| `tests/test_conllu_reader.py::test_missing_sent_id_raises_parse_error` | v31 in place | active 3.1 reader; marked v31, no change of content |
| `tests/test_conllu_reader.py::test_mwt_range_and_empty_nodes_removed` | v31 in place | active 3.1 reader; marked v31, no change of content |
| `tests/test_conllu_reader.py::test_newdoc_id_recoverable_from_metadata` | v31 in place | active 3.1 reader; marked v31, no change of content |
| `tests/test_conllu_reader.py::test_out_of_order_integer_ids_raise_parse_error` | v31 in place | active 3.1 reader; marked v31, no change of content |
| `tests/test_conllu_reader.py::test_public_type_and_streaming_failure_boundary` | v31 in place | active 3.1 reader; marked v31, no change of content |
| `tests/test_conllu_reader.py::test_punct_token_yielded_unchanged` | v31 in place | active 3.1 reader; marked v31, no change of content |
| `tests/test_conllu_reader.py::test_representation_exclusions_are_yielded_unchanged` | v31 in place | active 3.1 reader; marked v31, no change of content |
| `tests/test_context_tree.py::test_d_max_honored` | archived | v2.1 selector scaffold, always skipped; the §12.1 battery covers the same sources |
| `tests/test_context_tree.py::test_fallback_to_deepest_ancestor` | archived | v2.1 selector scaffold, always skipped; the §12.1 battery covers the same sources |
| `tests/test_context_tree.py::test_iid_uniform_m4` | archived | v2.1 selector scaffold, always skipped; the §12.1 battery covers the same sources |
| `tests/test_context_tree.py::test_k_min_gamma_behavior` | archived | v2.1 selector scaffold, always skipped; the §12.1 battery covers the same sources |
| `tests/test_context_tree.py::test_order1_markov` | archived | v2.1 selector scaffold, always skipped; the §12.1 battery covers the same sources |
| `tests/test_context_tree.py::test_order2_xor` | archived | v2.1 selector scaffold, always skipped; the §12.1 battery covers the same sources |
| `tests/test_context_tree.py::test_period3_cycle` | archived | v2.1 selector scaffold, always skipped; the §12.1 battery covers the same sources |
| `tests/test_context_tree.py::test_unseen_symbol_never_p_zero` | archived | v2.1 selector scaffold, always skipped; the §12.1 battery covers the same sources |
| `tests/test_determinism.py::test_build_manifest_carries_d46_fields_and_artifact_hashes` | replaced | test_v31_persistence.py::test_atomic_roundtrip_and_same_run_in_distinct_directories |
| `tests/test_determinism.py::test_build_manifest_fails_if_git_state_is_unavailable` | replaced | test_v31_validation_run.py::test_real_fit_requires_clean_tracked_producers |
| `tests/test_determinism.py::test_config_hash_canonical_and_sensitive` | replaced | the identity is the digest of the contract: test_v31_persistence.py::test_identity_excludes_locations_and_is_sensitive_to_components |
| `tests/test_determinism.py::test_load_config_reads_frozen_defaults` | replaced | test_v31_config.py::test_deposit_and_application_projection_match |
| `tests/test_determinism.py::test_resolve_config_deep_merges_without_mutating_base` | retired | no configuration merge in 3.1: one file, compared field by field with the deposit |
| `tests/test_determinism.py::test_seed_derivation_matches_spec_formula` | replaced | the contract's SHA-256 RNG: test_v31_sampling.py::test_pinned_rng_vector_and_fixture_ledger_reproduce_the_deposit |
| `tests/test_determinism.py::test_sha256_file_matches_hashlib` | migrated | test_v31_persistence.py::test_sha256_file_is_the_hash_of_the_bytes_on_disk |
| `tests/test_determinism.py::test_write_manifest_central_path_and_refuses_overwrite` | replaced | test_v31_persistence.py::test_destinations_with_existing_files_are_preserved |
| `tests/test_determinism.py::test_write_manifest_refusal_is_atomic` | replaced | test_v31_persistence.py::test_interrupted_write_never_publishes_stage |
| `tests/test_determinism.py::test_write_sidecar_is_minimal_and_refuses_overwrite` | retired | no sidecars in 3.1: one manifest per run (§11.7) |
| `tests/test_docs_consistency.py::test_every_item_is_inside_a_lettered_section` | archived | consistency between the two G1 documents; the identity of the instructions is migrated |
| `tests/test_docs_consistency.py::test_neither_document_numbers_an_item_twice` | archived | consistency between the two G1 documents; the identity of the instructions is migrated |
| `tests/test_docs_consistency.py::test_only_the_owner_ratified_technical_items_are_closed` | archived | consistency between the two G1 documents; the identity of the instructions is migrated |
| `tests/test_docs_consistency.py::test_the_checklist_and_the_record_number_the_same_items` | archived | consistency between the two G1 documents; the identity of the instructions is migrated |
| `tests/test_docs_consistency.py::test_the_item_numbers_are_a_gapless_run_from_one` | archived | consistency between the two G1 documents; the identity of the instructions is migrated |
| `tests/test_docs_consistency.py::test_the_three_standing_instruction_copies_are_identical` | migrated | test_v31_docs.py::test_the_three_standing_instruction_copies_are_identical |
| `tests/test_docs_consistency.py::test_the_two_documents_agree_on_which_section_each_item_is_in` | archived | consistency between the two G1 documents; the identity of the instructions is migrated |
| `tests/test_g0_enforcement.py::test_collection_skip_in_non_g0_module_is_ignored` | replaced | under E8 a non-v31 module is itself an error: test_v31_enforcement.py::test_every_collected_test_is_active_acceptance |
| `tests/test_g0_enforcement.py::test_enforcement_fails_on_collection_time_skip` | covered | test_v31_enforcement.py::test_v31_enforcement_rejects_vacuity_skip_and_xfail |
| `tests/test_g0_enforcement.py::test_enforcement_fails_on_dynamically_skipped_g0` | covered | test_v31_enforcement.py::test_v31_enforcement_rejects_vacuity_skip_and_xfail |
| `tests/test_g0_enforcement.py::test_enforcement_fails_on_module_marked_assertion_free_test` | covered | test_v31_enforcement.py::test_v31_enforcement_rejects_vacuity_skip_and_xfail |
| `tests/test_g0_enforcement.py::test_enforcement_fails_on_nonstrict_xpass` | migrated | test_v31_enforcement.py::test_v31_enforcement_rejects_a_static_skip_and_an_xpass_without_strict_xfail |
| `tests/test_g0_enforcement.py::test_enforcement_fails_on_statically_skipped_g0` | migrated | test_v31_enforcement.py::test_v31_enforcement_rejects_a_static_skip_and_an_xpass_without_strict_xfail |
| `tests/test_g0_enforcement.py::test_enforcement_fails_on_xpass` | migrated | test_v31_enforcement.py::test_v31_enforcement_rejects_a_static_skip_and_an_xpass_without_strict_xfail |
| `tests/test_g0_enforcement.py::test_enforcement_fails_when_assertion_is_dead_code` | covered | test_v31_enforcement.py::test_v31_enforcement_rejects_vacuity_skip_and_xfail |
| `tests/test_g0_enforcement.py::test_enforcement_invalidates_pyc_created_without_assertion_hook` | migrated | test_v31_enforcement.py::test_v31_enforcement_invalidates_pyc_compiled_without_the_assertion_hook |
| `tests/test_g0_enforcement.py::test_enforcement_passes_a_clean_g0_suite` | covered | test_v31_enforcement.py::test_v31_enforcement_accepts_executed_assert |
| `tests/test_g0_enforcement.py::test_g0_name_scan_rejects_uncollected_and_non_pytest_markers` | covered | test_v31_enforcement.py::test_v31_inventory_rejects_missing_test_and_marker |
| `tests/test_g0_enforcement.py::test_g0_set_covers_every_mandatory_area` | archived | G0 gate inventory; the enforcement mechanics are migrated or already covered |
| `tests/test_g0_enforcement.py::test_inventory_rejects_a_shared_file_that_lost_label_permutation` | archived | G0 gate inventory; the enforcement mechanics are migrated or already covered |
| `tests/test_g0_enforcement.py::test_inventory_rejects_a_tree_that_lost_the_p_bound_test` | archived | G0 gate inventory; the enforcement mechanics are migrated or already covered |
| `tests/test_g0_enforcement.py::test_inventory_rejects_an_area_without_named_behaviours` | archived | G0 gate inventory; the enforcement mechanics are migrated or already covered |
| `tests/test_g1_alphabet.py::test_a_config_that_moves_the_gate_a_threshold_is_refused` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_available_past_counts_retained_predecessors_within_the_sentence` | covered | test_v31_corpus.py::test_numeric_order_raw_coordinates_empty_reset_and_targets |
| `tests/test_g1_alphabet.py::test_contingency_keeps_raw_subtypes_visible` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_contingency_totals_reconcile_with_the_raw_token_count` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_drop_rates_by_rule_are_available_per_regime` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_excluded_deprel_census_is_independent_of_the_drop_or_oth_policy` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_excluded_deprel_shares_use_the_raw_token_denominator` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_freeze_alphabet_remains_a_declared_but_unimplemented_api` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_gate_a_aggregates_over_the_regime_not_the_document` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_gate_a_does_not_fire_at_exactly_two_percent` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_gate_a_fires_above_two_percent_of_raw_tokens_in_a_regime` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_gate_a_fires_from_an_exploratory_regime` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_gate_a_shares_are_per_language_and_the_verdict_is_one_per_run` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_gate_a_still_fires_on_an_analysed_regime_when_excluded_is_present` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_gate_a_verdict_ignores_the_excluded_regime_but_still_reports_it` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_gate_b_flags_a_document_below_seventy_percent_retention` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_gate_b_looks_everywhere_including_the_excluded_regime` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_gates_are_not_evaluated_without_a_registry` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_map_tokens_handles_an_empty_table` | migrated | test_v31_corpus.py::test_map_tokens_keeps_a_boolean_mask_on_an_empty_table |
| `tests/test_g1_alphabet.py::test_map_tokens_produces_the_spec_columns_and_totality` | covered | test_v31_corpus.py::test_coordinate_schema_does_not_silently_cast_float_ids |
| `tests/test_g1_alphabet.py::test_observed_alphabet_breaks_frequency_ties_by_symbol` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_observed_alphabet_excludes_dropped_tokens` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_observed_alphabet_orders_ids_by_descending_pooled_frequency` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_observed_alphabet_rejects_a_two_language_table` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_observed_alphabet_writes_nothing` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_oth_policy_keeps_the_absorbed_label_visible_to_the_audit` | covered | test_v31_corpus.py::test_excluded_deprel_drops_with_its_base_label_or_is_absorbed_by_oth |
| `tests/test_g1_alphabet.py::test_restricted_position_fraction_is_reported_per_regime` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_retention_and_drop_by_rule_partition_the_raw_tokens` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_alphabet.py::test_run_audit_rejects_a_regime_map_missing_a_document` | archived | v2.1 alphabet audit (IDs by frequency, GATE-A/B); retired with its code |
| `tests/test_g1_enforcement.py::test_an_empty_required_tuple_is_rejected` | covered | test_v31_enforcement.py::test_v31_inventory_rejects_missing_test_and_marker |
| `tests/test_g1_enforcement.py::test_g1_set_covers_every_mandatory_area` | replaced | test_v31_enforcement.py::test_v31_inventory_lists_every_collected_active_test |
| `tests/test_g1_enforcement.py::test_the_inventory_fails_when_an_area_loses_a_mandatory_test` | covered | test_v31_enforcement.py::test_v31_inventory_rejects_missing_test_and_marker |
| `tests/test_g1_registry.py::test_a_bare_string_flags_value_is_refused` | archived with registry.py | v2.1 registry; the 3.1 registry comes from the deposited contract |
| `tests/test_g1_registry.py::test_a_blank_required_field_is_refused` | archived with registry.py | v2.1 registry; the 3.1 registry comes from the deposited contract |
| `tests/test_g1_registry.py::test_a_blank_source_urn_is_refused` | archived with registry.py | v2.1 registry; the 3.1 registry comes from the deposited contract |
| `tests/test_g1_registry.py::test_a_non_string_flag_element_is_refused` | archived with registry.py | v2.1 registry; the 3.1 registry comes from the deposited contract |
| `tests/test_g1_registry.py::test_a_part_order_that_cannot_order_parts_is_refused` | archived with registry.py | v2.1 registry; the 3.1 registry comes from the deposited contract |
| `tests/test_g1_registry.py::test_a_sent_id_repeated_in_the_stream_is_refused` | covered | test_v31_corpus.py::test_ambiguous_identities_fail_with_source |
| `tests/test_g1_registry.py::test_a_well_formed_assignment_still_builds` | archived with registry.py | v2.1 registry; the 3.1 registry comes from the deposited contract |
| `tests/test_g1_sequences.py::test_a_doc_id_shared_by_two_languages_is_refused` | archived with sequences.py | v2.1 sequences; the 3.1 streams are in test_v31_sampling.py |
| `tests/test_g1_sequences.py::test_a_repeated_sent_ord_within_one_document_is_refused` | covered | test_v31_corpus.py::test_ambiguous_identities_fail_with_source |
| `tests/test_g1_sequences.py::test_a_single_language_document_still_converts` | archived with sequences.py | v2.1 sequences; the 3.1 streams are in test_v31_sampling.py |
| `tests/test_g1_sequences.py::test_build_sequences_requires_sentence_identity_evidence` | archived with sequences.py | v2.1 sequences; the 3.1 streams are in test_v31_sampling.py |
| `tests/test_g1_sequences.py::test_one_sent_id_cannot_map_to_two_sentence_ordinals` | covered | test_v31_corpus.py::test_ambiguous_identities_fail_with_source |
| `tests/test_g1_sequences.py::test_sentence_identity_and_ordinal_values_cannot_be_missing` | archived with sequences.py | v2.1 sequences; the 3.1 streams are in test_v31_sampling.py |
| `tests/test_g1_sequences.py::test_two_sentences_colliding_on_one_sent_ord_are_refused_at_construction` | archived with sequences.py | v2.1 sequences; the 3.1 streams are in test_v31_sampling.py |
| `tests/test_null_calibration.py::test_p2_permutation_positive_control_calibrates` | archived | P1/P2 calibration, retired with inference |
| `tests/test_null_calibration.py::test_pseudo_documents_match_corpus_size_profile` | archived | P1/P2 calibration, retired with inference |
| `tests/test_null_calibration.py::test_sign_flip_type_one_error_at_nominal_levels` | archived | P1/P2 calibration, retired with inference |
| `tests/test_permutation.py::test_d43_two_sided_floors_for_equal_and_unequal_groups` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_permutation.py::test_enumeration_counts` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_permutation.py::test_invalid_inputs_fail_loud` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_permutation.py::test_label_permutation_exact_pvalues` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_permutation.py::test_null_synthetic_p_uniform` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_permutation.py::test_one_two_sided_consistency` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_permutation.py::test_planted_effect_small_p` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_permutation.py::test_sign_flip_exact_pvalues` | archived with stats/ | no inference in 3.1 (§1.2); utilities preserved as historical |
| `tests/test_registry.py::test_agreeing_newdoc_id_is_accepted` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_build_registry_accepts_every_d04_regime` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_build_registry_accepts_every_declared_optional_field` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_build_registry_assigns_taxonomy_and_schema` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_build_registry_rejects_unknown_fields` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_canonical_doc_id_must_be_a_nonempty_string` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_canonical_target_chain_is_rejected` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_counts_aggregate_over_gappy_ordinals_and_split_files` | covered | test_v31_corpus.py::test_real_corpus_exact_expected_counts_keys_and_inventories |
| `tests/test_registry.py::test_doc_id_derived_from_sent_id_prefix` | covered | test_v31_corpus.py::test_ambiguous_identities_fail_with_source |
| `tests/test_registry.py::test_invalid_regime_raises` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_merge_into_a_canonical_that_is_not_itself_a_raw_prefix` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_merge_rejects_inconsistent_metadata` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_merge_requires_explicit_source_urn_on_every_contributor` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_missing_override_field_raises` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_n_tokens_raw_counts_integer_id_words_before_alphabet` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_n_tokens_retained_is_nullable_until_the_alphabet_is_frozen` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_newdoc_id_disagreement_raises` | covered | test_v31_corpus.py::test_ambiguous_identities_fail_with_source |
| `tests/test_registry.py::test_overrides_merge_raw_prefixes_into_canonical_document` | covered | test_v31_corpus.py::test_athenaeus_parts_order_before_ordinal |
| `tests/test_registry.py::test_regime_labels_are_exactly_the_five_of_d04` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_registry_does_not_alias_the_overrides_flags_list` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_registry_is_deterministic_in_row_order` | covered | test_v31_config.py::test_deposit_and_application_projection_match |
| `tests/test_registry.py::test_self_targeting_prefix_without_merge_is_allowed` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_sent_id_without_separator_raises` | covered | test_v31_corpus.py::test_ambiguous_identities_fail_with_source |
| `tests/test_registry.py::test_source_urn_defaults_to_doc_id` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_typo_in_a_merge_target_splits_the_group_and_is_rejected` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_unassigned_document_raises` | covered | test_v31_corpus.py::test_ambiguous_identities_fail_with_source |
| `tests/test_registry.py::test_unicode_homoglyph_target_is_rejected` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_unknown_override_raises` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_registry.py::test_unshared_canonical_target_is_rejected` | archived with registry.py | v2.1 registry; 3.1 identities and prefixes are in test_v31_corpus.py |
| `tests/test_run_audit.py::test_a_collision_on_any_output_leaves_no_partial_run` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_a_config_missing_a_declared_key_is_rejected` | covered | test_v31_config.py::test_application_contract_rejects_drift |
| `tests/test_run_audit.py::test_a_config_section_replaced_by_a_scalar_is_rejected` | covered | test_v31_config.py::test_schema_refuses_wrong_numeric_types_and_values |
| `tests/test_run_audit.py::test_a_configuration_that_retains_nothing_fails` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_a_conllu_appearing_mid_run_publishes_nothing` | migrated | test_v31_persistence.py::test_input_staging_binds_hash_to_processed_bytes_and_detects_changes |
| `tests/test_run_audit.py::test_a_corpus_missing_a_configured_language_is_refused` | covered | test_v31_persistence.py::test_exact_three_inputs_and_hashes |
| `tests/test_run_audit.py::test_a_deleted_language_keyed_section_is_rejected` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_a_failure_between_writes_rolls_the_whole_run_back` | covered | test_v31_persistence.py::test_before_publication_input_failure_leaves_prior_stage_intact |
| `tests/test_run_audit.py::test_a_malformed_overrides_file_fails_with_its_path` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_a_missing_overrides_file_is_not_an_empty_registry` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_a_missing_required_field_is_rejected` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_a_mistyped_config_key_is_rejected_not_silently_ignored` | covered | test_v31_config.py::test_application_contract_rejects_drift |
| `tests/test_run_audit.py::test_a_partially_written_artifact_is_rolled_back` | covered | test_v31_persistence.py::test_interrupted_write_never_publishes_stage |
| `tests/test_run_audit.py::test_a_pre_audit_over_a_proposed_registry_does_say_it_is_unratified` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_a_pre_audit_over_a_ratified_registry_never_calls_it_unratified` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_a_ratified_overrides_file_runs_canonically` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_a_refused_run_never_deletes_the_artifacts_it_refused_to_overwrite` | covered | test_v31_persistence.py::test_destinations_with_existing_files_are_preserved |
| `tests/test_run_audit.py::test_a_removed_input_is_caught_too` | migrated | test_v31_persistence.py::test_input_staging_binds_hash_to_processed_bytes_and_detects_changes |
| `tests/test_run_audit.py::test_a_sent_id_repeated_across_split_files_is_refused` | covered | test_v31_corpus.py::test_ambiguous_identities_fail_with_source |
| `tests/test_run_audit.py::test_a_single_language_audit_is_possible_only_by_configuring_it` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_a_stale_override_is_fatal_in_both_modes` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_alphabet_frames_keep_their_header_when_empty` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_an_edit_that_is_restored_before_verification_cannot_reach_the_report` | migrated | test_v31_persistence.py::test_input_staging_binds_hash_to_processed_bytes_and_detects_changes |
| `tests/test_run_audit.py::test_an_empty_corpus_fails_instead_of_passing_every_gate` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_an_explicit_config_must_be_a_nonempty_mapping` | covered | test_v31_config.py::test_application_contract_rejects_drift |
| `tests/test_run_audit.py::test_an_incomplete_registry_still_validates_the_rows_it_has` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_an_input_edited_mid_run_publishes_nothing` | migrated | test_v31_persistence.py::test_input_staging_binds_hash_to_processed_bytes_and_detects_changes |
| `tests/test_run_audit.py::test_an_unknown_override_field_is_rejected_not_dropped` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_build_manifest_honours_a_pre_captured_git_state` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_canonical_mode_accepts_only_the_authoritative_registry_path` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_canonical_mode_fails_loud_on_an_unassigned_sentence` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_canonical_mode_refuses_a_provenance_hash_mismatch` | covered | test_v31_persistence.py::test_exact_three_inputs_and_hashes |
| `tests/test_run_audit.py::test_canonical_mode_requires_a_clean_repository` | covered | test_v31_validation_run.py::test_real_fit_requires_clean_tracked_producers |
| `tests/test_run_audit.py::test_canonical_mode_with_a_complete_registry_evaluates_the_gates` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_canonical_provenance_requires_the_exact_release_and_file_set` | covered | test_v31_persistence.py::test_exact_three_inputs_and_hashes |
| `tests/test_run_audit.py::test_declared_readings_do_not_make_a_deictic_empirical_claim` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_drop_rates_by_rule_are_reported_per_regime` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_duplicate_config_keys_are_rejected` | covered | test_v31_config.py::test_duplicate_yaml_keys_are_rejected_at_every_depth |
| `tests/test_run_audit.py::test_duplicate_provenance_rows_are_not_accepted_as_evidence` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_duplicate_yaml_keys_are_rejected_at_any_registry_depth` | migrated | test_v31_config.py::test_duplicate_yaml_keys_are_rejected_at_every_depth |
| `tests/test_run_audit.py::test_every_csv_declares_its_own_status` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_every_resolved_destination_stays_outside_both_raw_roots` | migrated | test_v31_persistence.py::test_a_destination_inside_the_repository_raw_root_is_refused_under_any_data_root |
| `tests/test_run_audit.py::test_force_is_pre_audit_only` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_force_permits_the_rerun` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_g1_used_config_shapes_are_validated` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_manifest_and_sidecar_record_every_input_hash` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_merged_prefixes_are_folded_before_anything_is_counted` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_missing_provenance_blocks_canonical_but_is_reported_by_pre_audit` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_mode_is_machine_readable_in_the_manifest_and_every_sidecar` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_mwt_and_empty_node_rows_never_reach_the_counts` | covered | test_v31_corpus.py::test_mwt_and_empty_nodes_do_not_change_source_word_ids |
| `tests/test_run_audit.py::test_non_string_config_keys_are_reported_as_unknown` | covered | test_v31_config.py::test_application_contract_rejects_drift |
| `tests/test_run_audit.py::test_only_an_explicitly_ratified_file_produces_a_canonical_audit` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_pre_audit_names_the_documents_that_blocked_the_regime_aggregates` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_pre_audit_reports_a_provenance_mismatch_without_claiming_it_is_pinned` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_pre_audit_stamps_the_report_incomplete_and_withholds_every_verdict` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_pre_audit_with_a_complete_proposal_labels_regime_tables_provisional` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_registry_is_validated_not_merely_indexed` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_report_carries_the_retained_token_column_t_star_will_be_derived_from` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_rerunning_without_force_refuses_to_overwrite` | covered | test_v31_descriptive.py::test_a_second_run_refuses_the_destination_unless_resume_is_asked_for |
| `tests/test_run_audit.py::test_results_root_inside_the_data_root_is_refused` | migrated | test_v31_persistence.py::test_a_destination_inside_the_repository_raw_root_is_refused_under_any_data_root |
| `tests/test_run_audit.py::test_runs_differing_only_in_overrides_get_distinct_artifact_names` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_runs_differing_only_in_provenance_get_distinct_artifact_names` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_the_declared_schema_fields_are_all_accepted` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_the_full_alphabet_inventory_ships_unfrozen` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_the_full_contingency_ships_as_csv_and_is_hashed` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_the_inventory_keeps_the_declared_registry_column_order` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_the_label_free_report_does_not_promise_a_regime_contingency_it_lacks` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_the_loser_of_a_concurrent_race_deletes_nothing` | covered | test_v31_persistence.py::test_concurrent_reservation_refuses_second_writer |
| `tests/test_run_audit.py::test_the_manifest_records_the_inputs_as_read_not_as_they_end_up` | covered | test_v31_persistence.py::test_input_staging_binds_hash_to_processed_bytes_and_detects_changes |
| `tests/test_run_audit.py::test_the_report_does_not_claim_prefixes_are_unmerged_when_they_are_merged` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_the_report_states_every_declared_reading_and_points_the_right_way` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_the_reservation_alone_protects_even_with_every_artifact_deleted` | covered | test_v31_persistence.py::test_concurrent_reservation_refuses_second_writer |
| `tests/test_run_audit.py::test_the_run_id_distinguishes_two_code_revisions` | covered | test_v31_persistence.py::test_identity_excludes_locations_and_is_sensitive_to_components |
| `tests/test_run_audit.py::test_the_stage_never_writes_a_frozen_alphabet` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_the_stage_samples_git_before_it_writes_anything` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_the_two_modes_never_share_a_run_id` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_run_audit.py::test_the_yaml_error_names_the_original_file_and_keeps_the_snippet` | migrated | test_v31_config.py::test_a_yaml_error_names_the_original_file_and_keeps_its_snippet |
| `tests/test_run_audit.py::test_two_concurrent_identical_runs_cannot_both_publish` | covered | test_v31_persistence.py::test_concurrent_reservation_refuses_second_writer |
| `tests/test_run_audit.py::test_verified_provenance_is_visible_in_report_and_manifest` | archived with legacy_audit.py | v2.1 end-to-end audit; the defences still alive are migrated |
| `tests/test_scores.py::test_delta_ce_analytic_markov_chains` | retired | protocol (b) retired; the four losses are in test_v31_scores.py |
| `tests/test_scores.py::test_gain_restriction_respects_available_past` | replaced | test_v31_scores.py::test_pooled_core_refuses_a_negative_min_available_past and the target j>=4 in test_v31_corpus.py |
| `tests/test_scores.py::test_pooled_scores_label_free_byte_identical` | replaced | test_v31_scores.py::test_public_core_and_annotation_keep_scores_independent_of_labels |
| `tests/test_sequences.py::test_all_dropped_sentence_remains_an_empty_row` | covered | test_v31_corpus.py::test_numeric_order_raw_coordinates_empty_reset_and_targets |
| `tests/test_sequences.py::test_build_sequences_keeps_retained_symbols_in_token_order` | covered | test_v31_corpus.py::test_numeric_order_raw_coordinates_empty_reset_and_targets |
| `tests/test_sequences.py::test_build_sequences_schema_and_deterministic_order` | archived with sequences.py | SEP/P-BOUND retired (§13.2); reset without separators in test_v31_sampling.py |
| `tests/test_sequences.py::test_extend_alphabet_bound_appends_at_size_and_keeps_ids_stable` | archived with sequences.py | SEP/P-BOUND retired (§13.2); reset without separators in test_v31_sampling.py |
| `tests/test_sequences.py::test_extend_alphabet_bound_does_not_mutate_the_frozen_alphabet` | archived with sequences.py | SEP/P-BOUND retired (§13.2); reset without separators in test_v31_sampling.py |
| `tests/test_sequences.py::test_extend_alphabet_bound_rejects_an_alphabet_already_carrying_the_boundary` | archived with sequences.py | SEP/P-BOUND retired (§13.2); reset without separators in test_v31_sampling.py |
| `tests/test_sequences.py::test_extend_alphabet_bound_rejects_non_contiguous_ids` | archived with sequences.py | SEP/P-BOUND retired (§13.2); reset without separators in test_v31_sampling.py |
| `tests/test_sequences.py::test_manifest_omits_the_key_for_p_reset_runs` | archived with sequences.py | SEP/P-BOUND retired (§13.2); reset without separators in test_v31_sampling.py |
| `tests/test_sequences.py::test_manifest_records_the_runtime_alphabet_extension` | archived with sequences.py | SEP/P-BOUND retired (§13.2); reset without separators in test_v31_sampling.py |
| `tests/test_sequences.py::test_p_bound_produces_adjacent_boundaries_around_an_all_dropped_sentence` | archived with sequences.py | SEP/P-BOUND retired (§13.2); reset without separators in test_v31_sampling.py |
| `tests/test_sequences.py::test_p_bound_returns_one_stream_with_exactly_n_minus_one_boundaries` | archived with sequences.py | SEP/P-BOUND retired (§13.2); reset without separators in test_v31_sampling.py |
| `tests/test_sequences.py::test_p_bound_without_boundary_id_raises` | archived with sequences.py | SEP/P-BOUND retired (§13.2); reset without separators in test_v31_sampling.py |
| `tests/test_sequences.py::test_p_reset_returns_one_sequence_per_sentence` | covered | test_v31_sampling.py::test_each_sentence_or_fragment_is_one_reset_stream_without_separators |
| `tests/test_sequences.py::test_p_reset_with_boundary_id_raises` | archived with sequences.py | SEP/P-BOUND retired (§13.2); reset without separators in test_v31_sampling.py |
| `tests/test_sequences.py::test_sequences_never_carry_the_boundary_symbol` | covered | test_v31_sampling.py::test_each_sentence_or_fragment_is_one_reset_stream_without_separators |
| `tests/test_sequences.py::test_single_sentence_document_has_no_boundary` | archived with sequences.py | SEP/P-BOUND retired (§13.2); reset without separators in test_v31_sampling.py |
| `tests/test_sequences.py::test_to_model_input_never_spans_documents` | covered | test_v31_sampling.py::test_held_out_and_inventory_only_never_enter_any_cell_or_fold |
| `tests/test_sequences.py::test_token_order_is_honoured_not_row_order` | covered | test_v31_corpus.py::test_input_file_order_does_not_change_corpus |
| `tests/test_sequences.py::test_unknown_boundary_policy_raises` | archived with sequences.py | SEP/P-BOUND retired (§13.2); reset without separators in test_v31_sampling.py |
| `tests/test_sequences.py::test_unknown_doc_id_raises` | archived with sequences.py | SEP/P-BOUND retired (§13.2); reset without separators in test_v31_sampling.py |
| `tests/test_tree_slices.py::test_depth1_nodes_equal_smoothed_bigram` | archived | v2.1 scaffold, always skipped; root and depth 1 are in test_v31_context_tree.py |
| `tests/test_tree_slices.py::test_evaluate_on_train_consistency` | archived | v2.1 scaffold, always skipped; root and depth 1 are in test_v31_context_tree.py |
| `tests/test_tree_slices.py::test_root_equals_add_beta_unigram` | archived | v2.1 scaffold, always skipped; root and depth 1 are in test_v31_context_tree.py |

Summary: 270 non-`v31` functions at `5f1ec06` — 11 v31 in place, 22 migrated, 50 covered,
14 replaced, 3 retired and 170 archived with their code.

## Remaining obligations

- **V3**: technical trial at seed 0 on six cells and seven folds (42 pairs / 84 models), resource measurements, freeze of code and environment; publication of the V2/V3 evidence in the manifest.
- **V4**: full campaign, 490 pairs / 980 model identities, three R1, equality of the key sets (T25).
- **V5**: report, five figures, two weightings, resume and the prescribed regeneration of seed 0 (T24, T27, T29, T30).
- None of these obligations is covered by fixtures: executing them requires real fits, which start in V3.
