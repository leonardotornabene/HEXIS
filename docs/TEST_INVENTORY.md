# Inventario test HEXIS 3.1 — V3-001, V3-002

Accettazione attiva: **ogni test raccolto è `v31`**, con assert eseguito, senza skip,
xfail o xpass. `pytest` e `pytest -m v31` raccolgono gli stessi test: la regola è
imposta in `conftest.py` alla collezione, non letta a occhio dal riepilogo. L'inventario
nominale di `tests/test_v31_enforcement.py` deve coincidere con la raccolta effettiva,
in entrambe le direzioni. Il confronto col contratto depositato non sostituisce i test
del CTW, e le quattro fixture CTW depositate sono identificate, non eseguite.

## Obblighi T01–T30 del §12

| ID | Stato | Copertura / obbligo residuo |
|---|---|---|
| T01 | V1 | Input/hash, sent_id, 18 prefissi/17 documenti |
| T02 | V1 | Conteggi documento/blocco e intero corpus |
| T03 | V1 | Parsing, coordinate, identità, errori localizzati |
| T04 | V1 | Mapping globale, inventari, C0/UPOS, inventory_only |
| T05 | V2 | Esclusione di held-out e `inventory_only` dal training, in tutte le sei celle per sette fold |
| T06 | V2 | q esatto, nessun rimpiazzo, ≤1 frammento per contributore, vuoti e budget impossibili |
| T07 | V2 | Ordine sorgente; campionatore invariante all'ordine dei record e cieco alle etichette; riuso di ledger e permutazione come dichiarato |
| T08 | V2 | Vettore §12.2 e sette `block_key` depositati, scopi separati, ripetibilità, accoppiamento O/R; nessuno scopo di sonda attivo |
| T09 | V2 | Stream/reset e partizione esatta del campione; BOS terminale e partizione dei conteggi in T10–T11 |
| T10 | V2 | Enumerazione indipendente degli alberi ammessi contro evidenza, peso di radice e predizione |
| T11 | V2 | Normalizzazione, supporto raro/ignoto, training vuoto, D=0, m100/105/11, input rigorosi |
| T12 | V2 | Identità prequenziale/integrata pre-update; invarianza all'ordine degli stream |
| T13 | V2 | Conteggi/evidenze/pesi/fingerprint invariati dalla valutazione |
| T14 | V2 | Prior estremo in log, due pesi da δ, saturazione distinta dalle foglie forzate |
| T15 | V2 | 25 sintetici alle soglie §12.1 sul CTW canonico; violazione → exit non zero |
| T16 | V2 | Stress storico m106: esecuzione, normalizzazione, supporti, deficit registrato |
| T17 | V2 | Lunghezza, multinsieme, maschera e conteggi di radice conservati; slot distinto dalla provenienza |
| T18 | V2 | Controesempi di dipendenza interna e di pool eterogeneo al livello del campione e in G/Q: G_R non nullo con due modelli fittati |
| T19 | V2 | Q a quattro termini; controesempio archiviato d'inversione del segno riprodotto sul CTW canonico |
| T20 | V2 | Aggregazioni/due pesi |
| T21 | V2 | Sensibilità accoppiate |
| T22 | V2 | Masse/supporti/L_resolved |
| T23 | V2 | R1 |
| T24 | CODICE pre-V3, ESECUZIONE PENDING V5 | Censimento dei sei inventory_only (V1); il validatore del report rigenera ogni ledger dal contratto RNG, quindi nessun held-out/inventory_only in training, e rifiuta ogni scoring inventory_only: codice e test in `0dc69b5`; esecuzione sulla campagna in V5 |
| T25 | PENDING V4 | Uguaglianza 490/980 chiavi modello/coppia |
| T26 | V2 | Atomicità/interruzione, resume, corruzione, duplicati e chiavi extra: corpus (V1) e stage scientifico (V2) |
| T27 | CODICE V2, ESECUZIONE PENDING V5 | Ricostruzione score/diagnostiche e cinque figure: codice e test su fixture in `559dc40`, correzioni della revisione pre-V3 (campioni, shuffle e provenienza C0 rigenerati; figure leggibili alla cardinalità reale) in `0dc69b5`; esecuzione sui dati reali in V5 |
| T28 | V0–V1 | Pipeline senza candidates/inferenza; accettazione senza skip |
| T29 | PARZIALE V1 | Identità/round-trip corpus; campioni e shuffle rigenerati per ogni coppia (`0dc69b5`); CE/riproduzione modelli PENDING V5 |
| T30 | PENDING V5 | Report scientifico completo |

## Che cosa prova ciascun file attivo

| File | Proprietà |
|---|---|
| `test_v31_config.py` | Deposito e proiezione campo per campo, tipi e valori rifiutati, YAML sicuro e duplicati a ogni profondità, errore che nomina il file originale, isolamento delle configurazioni non 3.1 |
| `test_conllu_reader.py` | Parsing in streaming, identità e ordine, righe MWT ed empty node, errori localizzati, cecità alla rappresentazione |
| `test_v31_corpus.py` | T01–T04: censimento reale esatto, coordinate e ordine numerico, parti e ordinali, mappatura, accorpamento ADV/PART, maschere, target, diagnostiche A/B, corruzioni semantiche |
| `test_v31_persistence.py` | T26/T29: tre input esatti, staging dei byte letti, identità del run, pubblicazione atomica, collisioni e concorrenza, interruzione, corruzione, destinazioni fuori dai raw |
| `test_v31_context_tree.py` | T10–T16: enumerazione indipendente, BOS e partizione, numerica, identità prequenziale, modello congelato, batteria §12.1 e stress m=106 |
| `test_v31_sampling.py` | T05–T09, T17–T18: vettore RNG depositato, ledger, esclusioni, frammenti, stream con reset senza separatori, rimescolamento accoppiato |
| `test_v31_scores.py` | T19–T22: quattro perdite, slot accoppiati, Q a quattro termini, due pesature, diagnostiche e firme pubbliche del §11.1 |
| `test_v31_r1.py` | T23: JSD, simmetria, centroidi e contributi |
| `test_v31_descriptive.py`, `test_v31_completion.py`, `test_v31_report_semantics.py` | Esecutore e report su fixture: partizioni, resume, evidenze, chiavi, rigenerazione, guardie semantiche; assenza dei moduli ritirati |
| `test_v31_validation_run.py` | Evidenze V2/V3 eseguite e ricontrollate; il report rifiuta un contesto V2 cambiato anche durante la generazione; una singola cella a seed 0 resta in attesa di V3 |
| `test_v31_figures.py` | Le cinque figure del §11.6, derivate dalle tabelle verificate |
| `test_v31_docs.py` | Autorità attiva, integrità del deposito, archivio ai byte di `5f1ec06` file per file, identità delle tre copie delle istruzioni, assenza di import ritirati |
| `test_v31_enforcement.py`, `test_gate_inventory_anchor.py` | Il gate stesso: inventario esaustivo nei due versi, rifiuto di skip, xfail, xpass anche non stretto, assert mancante o morto, `.pyc` senza hook, test privo di marker, ancora assente o non marcata, archivio mai raccolto nemmeno dalla radice |

## Mappa dei test precedenti (§13.2: mantenuto, sostituito, ritirato)

Ogni funzione di test raccolta a `5f1ec06` e non marcata `v31` ha una destinazione.
«Migrato» significa che la proprietà è ora in un test attivo; «coperto» che un test
attivo già la dimostrava; «sostituito» che la 3.1 richiede un'altra proprietà, indicata;
«archiviato» che la proprietà vale solo per il codice ritirato, conservato in `archive/`
ed eseguibile a `5f1ec06`.

| Test a `5f1ec06` | Destinazione | Nota |
|---|---|---|
| `tests/test_alphabet.py::test_drop_rules` | migrato | test_v31_corpus.py::test_excluded_source_upos_drops_before_any_deprel_rule |
| `tests/test_alphabet.py::test_excluded_deprel_dropped_under_primary_policy` | migrato | test_v31_corpus.py::test_excluded_deprel_drops_with_its_base_label_or_is_absorbed_by_oth |
| `tests/test_alphabet.py::test_inconsistent_alphabet_configuration_raises` | sostituito | la cella variant+policy v2.1 non esiste: test_v31_corpus.py::test_an_unknown_alphabet_variant_is_refused |
| `tests/test_alphabet.py::test_mapped_token_is_immutable` | migrato | test_v31_corpus.py::test_mapped_token_is_immutable |
| `tests/test_alphabet.py::test_oth_arm` | migrato | test_v31_corpus.py::test_excluded_deprel_drops_with_its_base_label_or_is_absorbed_by_oth |
| `tests/test_alphabet.py::test_propn_maps_to_noun` | migrato | test_v31_corpus.py::test_propn_is_mapped_to_noun_before_retention |
| `tests/test_alphabet.py::test_subtype_stripping_incl_multi_colon` | migrato | test_v31_corpus.py::test_subtype_stripping_is_total_and_lowercases_every_colon |
| `tests/test_alphabet.py::test_synthetic_conllu_with_mwt_and_empty_node` | coperto | test_v31_corpus.py::test_mwt_and_empty_nodes_do_not_change_source_word_ids |
| `tests/test_alphabet.py::test_totality_on_any_ud_label` | sostituito | la 3.1 rifiuta un UPOS sorgente ignoto invece di scartarlo (§13.2): test_v31_corpus.py::test_public_mapping_rejects_unknown_source_upos |
| `tests/test_alphabet.py::test_upos_only_alphabet_is_the_twelve_retained_tags` | sostituito | con ADV_PART l'alfabeto upos_only ha 11 simboli: test_v31_corpus.py::test_real_corpus_exact_expected_counts_keys_and_inventories |
| `tests/test_alphabet.py::test_upos_only_keeps_the_retention_rules` | coperto | test_v31_corpus.py::test_global_merge_subtypes_masks_and_frozen_ids |
| `tests/test_alphabet.py::test_upos_rule_precedes_deprel_rule` | migrato | test_v31_corpus.py::test_excluded_source_upos_drops_before_any_deprel_rule |
| `tests/test_blocks.py::test_empty_and_all_dropped_documents_produce_no_blocks` | archiviato con blocks.py | chunk v2.1; il blocco di dipendenza 3.1 è un altro oggetto (§13.2) |
| `tests/test_blocks.py::test_invalid_block_parameters_fail_loud` | archiviato con blocks.py | chunk v2.1; il blocco di dipendenza 3.1 è un altro oggetto (§13.2) |
| `tests/test_blocks.py::test_never_spans_documents` | archiviato con blocks.py | chunk v2.1; il blocco di dipendenza 3.1 è un altro oggetto (§13.2) |
| `tests/test_blocks.py::test_oversized_sentence_is_its_own_block` | archiviato con blocks.py | chunk v2.1; il blocco di dipendenza 3.1 è un altro oggetto (§13.2) |
| `tests/test_blocks.py::test_sentence_aligned_fill` | archiviato con blocks.py | chunk v2.1; il blocco di dipendenza 3.1 è un altro oggetto (§13.2) |
| `tests/test_blocks.py::test_tail_kept_iff_at_least_min_frac` | archiviato con blocks.py | chunk v2.1; il blocco di dipendenza 3.1 è un altro oggetto (§13.2) |
| `tests/test_bootstrap_holm.py::test_bootstrap_fails_loud_on_wrong_group_count` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_bootstrap_holm.py::test_bootstrap_rejects_invalid_input_domain` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_bootstrap_holm.py::test_bootstrap_reproducible_under_fixed_seed` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_bootstrap_holm.py::test_bootstrap_resamples_within_groups_only` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_bootstrap_holm.py::test_bootstrap_supports_unweighted_p1_mean_with_unequal_groups` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_bootstrap_holm.py::test_holm_adjusted_is_monotone_nondecreasing` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_bootstrap_holm.py::test_holm_boundary_and_order_invariance` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_bootstrap_holm.py::test_holm_family_of_two_thresholds` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_bootstrap_holm.py::test_holm_rejects_invalid_probability_domain` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_bootstrap_holm.py::test_holm_step_down_stops_at_first_non_reject` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_conllu_reader.py::test_conllu_parse_exception_is_wrapped` | v31 sul posto | lettore attivo 3.1; marcato v31, nessuna modifica di contenuto |
| `tests/test_conllu_reader.py::test_id_order_preserved` | v31 sul posto | lettore attivo 3.1; marcato v31, nessuna modifica di contenuto |
| `tests/test_conllu_reader.py::test_invalid_required_labels_raise_parse_error` | v31 sul posto | lettore attivo 3.1; marcato v31, nessuna modifica di contenuto |
| `tests/test_conllu_reader.py::test_malformed_row_raises_parse_error_with_location` | v31 sul posto | lettore attivo 3.1; marcato v31, nessuna modifica di contenuto |
| `tests/test_conllu_reader.py::test_missing_sent_id_raises_parse_error` | v31 sul posto | lettore attivo 3.1; marcato v31, nessuna modifica di contenuto |
| `tests/test_conllu_reader.py::test_mwt_range_and_empty_nodes_removed` | v31 sul posto | lettore attivo 3.1; marcato v31, nessuna modifica di contenuto |
| `tests/test_conllu_reader.py::test_newdoc_id_recoverable_from_metadata` | v31 sul posto | lettore attivo 3.1; marcato v31, nessuna modifica di contenuto |
| `tests/test_conllu_reader.py::test_out_of_order_integer_ids_raise_parse_error` | v31 sul posto | lettore attivo 3.1; marcato v31, nessuna modifica di contenuto |
| `tests/test_conllu_reader.py::test_public_type_and_streaming_failure_boundary` | v31 sul posto | lettore attivo 3.1; marcato v31, nessuna modifica di contenuto |
| `tests/test_conllu_reader.py::test_punct_token_yielded_unchanged` | v31 sul posto | lettore attivo 3.1; marcato v31, nessuna modifica di contenuto |
| `tests/test_conllu_reader.py::test_representation_exclusions_are_yielded_unchanged` | v31 sul posto | lettore attivo 3.1; marcato v31, nessuna modifica di contenuto |
| `tests/test_context_tree.py::test_d_max_honored` | archiviato | scaffold del selettore v2.1, sempre skip; la batteria §12.1 copre le stesse sorgenti |
| `tests/test_context_tree.py::test_fallback_to_deepest_ancestor` | archiviato | scaffold del selettore v2.1, sempre skip; la batteria §12.1 copre le stesse sorgenti |
| `tests/test_context_tree.py::test_iid_uniform_m4` | archiviato | scaffold del selettore v2.1, sempre skip; la batteria §12.1 copre le stesse sorgenti |
| `tests/test_context_tree.py::test_k_min_gamma_behavior` | archiviato | scaffold del selettore v2.1, sempre skip; la batteria §12.1 copre le stesse sorgenti |
| `tests/test_context_tree.py::test_order1_markov` | archiviato | scaffold del selettore v2.1, sempre skip; la batteria §12.1 copre le stesse sorgenti |
| `tests/test_context_tree.py::test_order2_xor` | archiviato | scaffold del selettore v2.1, sempre skip; la batteria §12.1 copre le stesse sorgenti |
| `tests/test_context_tree.py::test_period3_cycle` | archiviato | scaffold del selettore v2.1, sempre skip; la batteria §12.1 copre le stesse sorgenti |
| `tests/test_context_tree.py::test_unseen_symbol_never_p_zero` | archiviato | scaffold del selettore v2.1, sempre skip; la batteria §12.1 copre le stesse sorgenti |
| `tests/test_determinism.py::test_build_manifest_carries_d46_fields_and_artifact_hashes` | sostituito | test_v31_persistence.py::test_atomic_roundtrip_and_same_run_in_distinct_directories |
| `tests/test_determinism.py::test_build_manifest_fails_if_git_state_is_unavailable` | sostituito | test_v31_descriptive.py::test_real_fit_requires_clean_tracked_producers |
| `tests/test_determinism.py::test_config_hash_canonical_and_sensitive` | sostituito | l'identità è il digest del contratto: test_v31_persistence.py::test_identity_excludes_locations_and_is_sensitive_to_components |
| `tests/test_determinism.py::test_load_config_reads_frozen_defaults` | sostituito | test_v31_config.py::test_deposit_and_application_projection_match |
| `tests/test_determinism.py::test_resolve_config_deep_merges_without_mutating_base` | ritirato | nessun merge di configurazione in 3.1: un solo file, confrontato campo per campo col deposito |
| `tests/test_determinism.py::test_seed_derivation_matches_spec_formula` | sostituito | RNG SHA-256 del contratto: test_v31_sampling.py::test_pinned_rng_vector_and_fixture_ledger_reproduce_the_deposit |
| `tests/test_determinism.py::test_sha256_file_matches_hashlib` | migrato | test_v31_persistence.py::test_sha256_file_is_the_hash_of_the_bytes_on_disk |
| `tests/test_determinism.py::test_write_manifest_central_path_and_refuses_overwrite` | sostituito | test_v31_persistence.py::test_destinations_with_existing_files_are_preserved |
| `tests/test_determinism.py::test_write_manifest_refusal_is_atomic` | sostituito | test_v31_persistence.py::test_interrupted_write_never_publishes_stage |
| `tests/test_determinism.py::test_write_sidecar_is_minimal_and_refuses_overwrite` | ritirato | niente sidecar in 3.1: un manifest per run (§11.7) |
| `tests/test_docs_consistency.py::test_every_item_is_inside_a_lettered_section` | archiviato | coerenza fra i due documenti G1; l'identità delle istruzioni è migrata |
| `tests/test_docs_consistency.py::test_neither_document_numbers_an_item_twice` | archiviato | coerenza fra i due documenti G1; l'identità delle istruzioni è migrata |
| `tests/test_docs_consistency.py::test_only_the_owner_ratified_technical_items_are_closed` | archiviato | coerenza fra i due documenti G1; l'identità delle istruzioni è migrata |
| `tests/test_docs_consistency.py::test_the_checklist_and_the_record_number_the_same_items` | archiviato | coerenza fra i due documenti G1; l'identità delle istruzioni è migrata |
| `tests/test_docs_consistency.py::test_the_item_numbers_are_a_gapless_run_from_one` | archiviato | coerenza fra i due documenti G1; l'identità delle istruzioni è migrata |
| `tests/test_docs_consistency.py::test_the_three_standing_instruction_copies_are_identical` | migrato | test_v31_docs.py::test_the_three_standing_instruction_copies_are_identical |
| `tests/test_docs_consistency.py::test_the_two_documents_agree_on_which_section_each_item_is_in` | archiviato | coerenza fra i due documenti G1; l'identità delle istruzioni è migrata |
| `tests/test_g0_enforcement.py::test_collection_skip_in_non_g0_module_is_ignored` | sostituito | con E8 un modulo non v31 è esso stesso un errore: test_v31_enforcement.py::test_every_collected_test_is_active_acceptance |
| `tests/test_g0_enforcement.py::test_enforcement_fails_on_collection_time_skip` | coperto | test_v31_enforcement.py::test_v31_enforcement_rejects_vacuity_skip_and_xfail |
| `tests/test_g0_enforcement.py::test_enforcement_fails_on_dynamically_skipped_g0` | coperto | test_v31_enforcement.py::test_v31_enforcement_rejects_vacuity_skip_and_xfail |
| `tests/test_g0_enforcement.py::test_enforcement_fails_on_module_marked_assertion_free_test` | coperto | test_v31_enforcement.py::test_v31_enforcement_rejects_vacuity_skip_and_xfail |
| `tests/test_g0_enforcement.py::test_enforcement_fails_on_nonstrict_xpass` | migrato | test_v31_enforcement.py::test_v31_enforcement_rejects_a_static_skip_and_an_xpass_without_strict_xfail |
| `tests/test_g0_enforcement.py::test_enforcement_fails_on_statically_skipped_g0` | migrato | test_v31_enforcement.py::test_v31_enforcement_rejects_a_static_skip_and_an_xpass_without_strict_xfail |
| `tests/test_g0_enforcement.py::test_enforcement_fails_on_xpass` | migrato | test_v31_enforcement.py::test_v31_enforcement_rejects_a_static_skip_and_an_xpass_without_strict_xfail |
| `tests/test_g0_enforcement.py::test_enforcement_fails_when_assertion_is_dead_code` | coperto | test_v31_enforcement.py::test_v31_enforcement_rejects_vacuity_skip_and_xfail |
| `tests/test_g0_enforcement.py::test_enforcement_invalidates_pyc_created_without_assertion_hook` | migrato | test_v31_enforcement.py::test_v31_enforcement_invalidates_pyc_compiled_without_the_assertion_hook |
| `tests/test_g0_enforcement.py::test_enforcement_passes_a_clean_g0_suite` | coperto | test_v31_enforcement.py::test_v31_enforcement_accepts_executed_assert |
| `tests/test_g0_enforcement.py::test_g0_name_scan_rejects_uncollected_and_non_pytest_markers` | coperto | test_v31_enforcement.py::test_v31_inventory_rejects_missing_test_and_marker |
| `tests/test_g0_enforcement.py::test_g0_set_covers_every_mandatory_area` | archiviato | inventario del gate G0; le meccaniche di enforcement sono migrate o già coperte |
| `tests/test_g0_enforcement.py::test_inventory_rejects_a_shared_file_that_lost_label_permutation` | archiviato | inventario del gate G0; le meccaniche di enforcement sono migrate o già coperte |
| `tests/test_g0_enforcement.py::test_inventory_rejects_a_tree_that_lost_the_p_bound_test` | archiviato | inventario del gate G0; le meccaniche di enforcement sono migrate o già coperte |
| `tests/test_g0_enforcement.py::test_inventory_rejects_an_area_without_named_behaviours` | archiviato | inventario del gate G0; le meccaniche di enforcement sono migrate o già coperte |
| `tests/test_g1_alphabet.py::test_a_config_that_moves_the_gate_a_threshold_is_refused` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_available_past_counts_retained_predecessors_within_the_sentence` | coperto | test_v31_corpus.py::test_numeric_order_raw_coordinates_empty_reset_and_targets |
| `tests/test_g1_alphabet.py::test_contingency_keeps_raw_subtypes_visible` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_contingency_totals_reconcile_with_the_raw_token_count` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_drop_rates_by_rule_are_available_per_regime` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_excluded_deprel_census_is_independent_of_the_drop_or_oth_policy` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_excluded_deprel_shares_use_the_raw_token_denominator` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_freeze_alphabet_remains_a_declared_but_unimplemented_api` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_gate_a_aggregates_over_the_regime_not_the_document` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_gate_a_does_not_fire_at_exactly_two_percent` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_gate_a_fires_above_two_percent_of_raw_tokens_in_a_regime` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_gate_a_fires_from_an_exploratory_regime` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_gate_a_shares_are_per_language_and_the_verdict_is_one_per_run` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_gate_a_still_fires_on_an_analysed_regime_when_excluded_is_present` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_gate_a_verdict_ignores_the_excluded_regime_but_still_reports_it` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_gate_b_flags_a_document_below_seventy_percent_retention` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_gate_b_looks_everywhere_including_the_excluded_regime` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_gates_are_not_evaluated_without_a_registry` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_map_tokens_handles_an_empty_table` | migrato | test_v31_corpus.py::test_map_tokens_keeps_a_boolean_mask_on_an_empty_table |
| `tests/test_g1_alphabet.py::test_map_tokens_produces_the_spec_columns_and_totality` | coperto | test_v31_corpus.py::test_coordinate_schema_does_not_silently_cast_float_ids |
| `tests/test_g1_alphabet.py::test_observed_alphabet_breaks_frequency_ties_by_symbol` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_observed_alphabet_excludes_dropped_tokens` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_observed_alphabet_orders_ids_by_descending_pooled_frequency` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_observed_alphabet_rejects_a_two_language_table` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_observed_alphabet_writes_nothing` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_oth_policy_keeps_the_absorbed_label_visible_to_the_audit` | coperto | test_v31_corpus.py::test_excluded_deprel_drops_with_its_base_label_or_is_absorbed_by_oth |
| `tests/test_g1_alphabet.py::test_restricted_position_fraction_is_reported_per_regime` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_retention_and_drop_by_rule_partition_the_raw_tokens` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_alphabet.py::test_run_audit_rejects_a_regime_map_missing_a_document` | archiviato | audit alfabeto v2.1 (ID per frequenza, GATE-A/B); ritirato col suo codice |
| `tests/test_g1_enforcement.py::test_an_empty_required_tuple_is_rejected` | coperto | test_v31_enforcement.py::test_v31_inventory_rejects_missing_test_and_marker |
| `tests/test_g1_enforcement.py::test_g1_set_covers_every_mandatory_area` | sostituito | test_v31_enforcement.py::test_v31_inventory_lists_every_collected_active_test |
| `tests/test_g1_enforcement.py::test_the_inventory_fails_when_an_area_loses_a_mandatory_test` | coperto | test_v31_enforcement.py::test_v31_inventory_rejects_missing_test_and_marker |
| `tests/test_g1_registry.py::test_a_bare_string_flags_value_is_refused` | archiviato con registry.py | registro v2.1; il registro 3.1 viene dal contratto depositato |
| `tests/test_g1_registry.py::test_a_blank_required_field_is_refused` | archiviato con registry.py | registro v2.1; il registro 3.1 viene dal contratto depositato |
| `tests/test_g1_registry.py::test_a_blank_source_urn_is_refused` | archiviato con registry.py | registro v2.1; il registro 3.1 viene dal contratto depositato |
| `tests/test_g1_registry.py::test_a_non_string_flag_element_is_refused` | archiviato con registry.py | registro v2.1; il registro 3.1 viene dal contratto depositato |
| `tests/test_g1_registry.py::test_a_part_order_that_cannot_order_parts_is_refused` | archiviato con registry.py | registro v2.1; il registro 3.1 viene dal contratto depositato |
| `tests/test_g1_registry.py::test_a_sent_id_repeated_in_the_stream_is_refused` | coperto | test_v31_corpus.py::test_ambiguous_identities_fail_with_source |
| `tests/test_g1_registry.py::test_a_well_formed_assignment_still_builds` | archiviato con registry.py | registro v2.1; il registro 3.1 viene dal contratto depositato |
| `tests/test_g1_sequences.py::test_a_doc_id_shared_by_two_languages_is_refused` | archiviato con sequences.py | sequenze v2.1; gli stream 3.1 sono in test_v31_sampling.py |
| `tests/test_g1_sequences.py::test_a_repeated_sent_ord_within_one_document_is_refused` | coperto | test_v31_corpus.py::test_ambiguous_identities_fail_with_source |
| `tests/test_g1_sequences.py::test_a_single_language_document_still_converts` | archiviato con sequences.py | sequenze v2.1; gli stream 3.1 sono in test_v31_sampling.py |
| `tests/test_g1_sequences.py::test_build_sequences_requires_sentence_identity_evidence` | archiviato con sequences.py | sequenze v2.1; gli stream 3.1 sono in test_v31_sampling.py |
| `tests/test_g1_sequences.py::test_one_sent_id_cannot_map_to_two_sentence_ordinals` | coperto | test_v31_corpus.py::test_ambiguous_identities_fail_with_source |
| `tests/test_g1_sequences.py::test_sentence_identity_and_ordinal_values_cannot_be_missing` | archiviato con sequences.py | sequenze v2.1; gli stream 3.1 sono in test_v31_sampling.py |
| `tests/test_g1_sequences.py::test_two_sentences_colliding_on_one_sent_ord_are_refused_at_construction` | archiviato con sequences.py | sequenze v2.1; gli stream 3.1 sono in test_v31_sampling.py |
| `tests/test_null_calibration.py::test_p2_permutation_positive_control_calibrates` | archiviato | calibrazione di P1/P2, ritirata con l'inferenza |
| `tests/test_null_calibration.py::test_pseudo_documents_match_corpus_size_profile` | archiviato | calibrazione di P1/P2, ritirata con l'inferenza |
| `tests/test_null_calibration.py::test_sign_flip_type_one_error_at_nominal_levels` | archiviato | calibrazione di P1/P2, ritirata con l'inferenza |
| `tests/test_permutation.py::test_d43_two_sided_floors_for_equal_and_unequal_groups` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_permutation.py::test_enumeration_counts` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_permutation.py::test_invalid_inputs_fail_loud` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_permutation.py::test_label_permutation_exact_pvalues` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_permutation.py::test_null_synthetic_p_uniform` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_permutation.py::test_one_two_sided_consistency` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_permutation.py::test_planted_effect_small_p` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_permutation.py::test_sign_flip_exact_pvalues` | archiviato con stats/ | nessuna inferenza in 3.1 (§1.2); utility conservate come storiche |
| `tests/test_registry.py::test_agreeing_newdoc_id_is_accepted` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_build_registry_accepts_every_d04_regime` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_build_registry_accepts_every_declared_optional_field` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_build_registry_assigns_taxonomy_and_schema` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_build_registry_rejects_unknown_fields` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_canonical_doc_id_must_be_a_nonempty_string` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_canonical_target_chain_is_rejected` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_counts_aggregate_over_gappy_ordinals_and_split_files` | coperto | test_v31_corpus.py::test_real_corpus_exact_expected_counts_keys_and_inventories |
| `tests/test_registry.py::test_doc_id_derived_from_sent_id_prefix` | coperto | test_v31_corpus.py::test_ambiguous_identities_fail_with_source |
| `tests/test_registry.py::test_invalid_regime_raises` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_merge_into_a_canonical_that_is_not_itself_a_raw_prefix` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_merge_rejects_inconsistent_metadata` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_merge_requires_explicit_source_urn_on_every_contributor` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_missing_override_field_raises` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_n_tokens_raw_counts_integer_id_words_before_alphabet` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_n_tokens_retained_is_nullable_until_the_alphabet_is_frozen` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_newdoc_id_disagreement_raises` | coperto | test_v31_corpus.py::test_ambiguous_identities_fail_with_source |
| `tests/test_registry.py::test_overrides_merge_raw_prefixes_into_canonical_document` | coperto | test_v31_corpus.py::test_athenaeus_parts_order_before_ordinal |
| `tests/test_registry.py::test_regime_labels_are_exactly_the_five_of_d04` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_registry_does_not_alias_the_overrides_flags_list` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_registry_is_deterministic_in_row_order` | coperto | test_v31_config.py::test_deposit_and_application_projection_match |
| `tests/test_registry.py::test_self_targeting_prefix_without_merge_is_allowed` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_sent_id_without_separator_raises` | coperto | test_v31_corpus.py::test_ambiguous_identities_fail_with_source |
| `tests/test_registry.py::test_source_urn_defaults_to_doc_id` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_typo_in_a_merge_target_splits_the_group_and_is_rejected` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_unassigned_document_raises` | coperto | test_v31_corpus.py::test_ambiguous_identities_fail_with_source |
| `tests/test_registry.py::test_unicode_homoglyph_target_is_rejected` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_unknown_override_raises` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_registry.py::test_unshared_canonical_target_is_rejected` | archiviato con registry.py | registro v2.1; identità e prefissi 3.1 sono in test_v31_corpus.py |
| `tests/test_run_audit.py::test_a_collision_on_any_output_leaves_no_partial_run` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_a_config_missing_a_declared_key_is_rejected` | coperto | test_v31_config.py::test_application_contract_rejects_drift |
| `tests/test_run_audit.py::test_a_config_section_replaced_by_a_scalar_is_rejected` | coperto | test_v31_config.py::test_schema_refuses_wrong_numeric_types_and_values |
| `tests/test_run_audit.py::test_a_configuration_that_retains_nothing_fails` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_a_conllu_appearing_mid_run_publishes_nothing` | migrato | test_v31_persistence.py::test_input_staging_binds_hash_to_processed_bytes_and_detects_changes |
| `tests/test_run_audit.py::test_a_corpus_missing_a_configured_language_is_refused` | coperto | test_v31_persistence.py::test_exact_three_inputs_and_hashes |
| `tests/test_run_audit.py::test_a_deleted_language_keyed_section_is_rejected` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_a_failure_between_writes_rolls_the_whole_run_back` | coperto | test_v31_persistence.py::test_before_publication_input_failure_leaves_prior_stage_intact |
| `tests/test_run_audit.py::test_a_malformed_overrides_file_fails_with_its_path` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_a_missing_overrides_file_is_not_an_empty_registry` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_a_missing_required_field_is_rejected` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_a_mistyped_config_key_is_rejected_not_silently_ignored` | coperto | test_v31_config.py::test_application_contract_rejects_drift |
| `tests/test_run_audit.py::test_a_partially_written_artifact_is_rolled_back` | coperto | test_v31_persistence.py::test_interrupted_write_never_publishes_stage |
| `tests/test_run_audit.py::test_a_pre_audit_over_a_proposed_registry_does_say_it_is_unratified` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_a_pre_audit_over_a_ratified_registry_never_calls_it_unratified` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_a_ratified_overrides_file_runs_canonically` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_a_refused_run_never_deletes_the_artifacts_it_refused_to_overwrite` | coperto | test_v31_persistence.py::test_destinations_with_existing_files_are_preserved |
| `tests/test_run_audit.py::test_a_removed_input_is_caught_too` | migrato | test_v31_persistence.py::test_input_staging_binds_hash_to_processed_bytes_and_detects_changes |
| `tests/test_run_audit.py::test_a_sent_id_repeated_across_split_files_is_refused` | coperto | test_v31_corpus.py::test_ambiguous_identities_fail_with_source |
| `tests/test_run_audit.py::test_a_single_language_audit_is_possible_only_by_configuring_it` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_a_stale_override_is_fatal_in_both_modes` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_alphabet_frames_keep_their_header_when_empty` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_an_edit_that_is_restored_before_verification_cannot_reach_the_report` | migrato | test_v31_persistence.py::test_input_staging_binds_hash_to_processed_bytes_and_detects_changes |
| `tests/test_run_audit.py::test_an_empty_corpus_fails_instead_of_passing_every_gate` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_an_explicit_config_must_be_a_nonempty_mapping` | coperto | test_v31_config.py::test_application_contract_rejects_drift |
| `tests/test_run_audit.py::test_an_incomplete_registry_still_validates_the_rows_it_has` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_an_input_edited_mid_run_publishes_nothing` | migrato | test_v31_persistence.py::test_input_staging_binds_hash_to_processed_bytes_and_detects_changes |
| `tests/test_run_audit.py::test_an_unknown_override_field_is_rejected_not_dropped` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_build_manifest_honours_a_pre_captured_git_state` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_canonical_mode_accepts_only_the_authoritative_registry_path` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_canonical_mode_fails_loud_on_an_unassigned_sentence` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_canonical_mode_refuses_a_provenance_hash_mismatch` | coperto | test_v31_persistence.py::test_exact_three_inputs_and_hashes |
| `tests/test_run_audit.py::test_canonical_mode_requires_a_clean_repository` | coperto | test_v31_descriptive.py::test_real_fit_requires_clean_tracked_producers |
| `tests/test_run_audit.py::test_canonical_mode_with_a_complete_registry_evaluates_the_gates` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_canonical_provenance_requires_the_exact_release_and_file_set` | coperto | test_v31_persistence.py::test_exact_three_inputs_and_hashes |
| `tests/test_run_audit.py::test_declared_readings_do_not_make_a_deictic_empirical_claim` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_drop_rates_by_rule_are_reported_per_regime` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_duplicate_config_keys_are_rejected` | coperto | test_v31_config.py::test_duplicate_yaml_keys_are_rejected_at_every_depth |
| `tests/test_run_audit.py::test_duplicate_provenance_rows_are_not_accepted_as_evidence` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_duplicate_yaml_keys_are_rejected_at_any_registry_depth` | migrato | test_v31_config.py::test_duplicate_yaml_keys_are_rejected_at_every_depth |
| `tests/test_run_audit.py::test_every_csv_declares_its_own_status` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_every_resolved_destination_stays_outside_both_raw_roots` | migrato | test_v31_persistence.py::test_a_destination_inside_the_repository_raw_root_is_refused_under_any_data_root |
| `tests/test_run_audit.py::test_force_is_pre_audit_only` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_force_permits_the_rerun` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_g1_used_config_shapes_are_validated` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_manifest_and_sidecar_record_every_input_hash` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_merged_prefixes_are_folded_before_anything_is_counted` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_missing_provenance_blocks_canonical_but_is_reported_by_pre_audit` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_mode_is_machine_readable_in_the_manifest_and_every_sidecar` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_mwt_and_empty_node_rows_never_reach_the_counts` | coperto | test_v31_corpus.py::test_mwt_and_empty_nodes_do_not_change_source_word_ids |
| `tests/test_run_audit.py::test_non_string_config_keys_are_reported_as_unknown` | coperto | test_v31_config.py::test_application_contract_rejects_drift |
| `tests/test_run_audit.py::test_only_an_explicitly_ratified_file_produces_a_canonical_audit` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_pre_audit_names_the_documents_that_blocked_the_regime_aggregates` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_pre_audit_reports_a_provenance_mismatch_without_claiming_it_is_pinned` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_pre_audit_stamps_the_report_incomplete_and_withholds_every_verdict` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_pre_audit_with_a_complete_proposal_labels_regime_tables_provisional` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_registry_is_validated_not_merely_indexed` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_report_carries_the_retained_token_column_t_star_will_be_derived_from` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_rerunning_without_force_refuses_to_overwrite` | coperto | test_v31_descriptive.py::test_a_second_run_refuses_the_destination_unless_resume_is_asked_for |
| `tests/test_run_audit.py::test_results_root_inside_the_data_root_is_refused` | migrato | test_v31_persistence.py::test_a_destination_inside_the_repository_raw_root_is_refused_under_any_data_root |
| `tests/test_run_audit.py::test_runs_differing_only_in_overrides_get_distinct_artifact_names` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_runs_differing_only_in_provenance_get_distinct_artifact_names` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_the_declared_schema_fields_are_all_accepted` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_the_full_alphabet_inventory_ships_unfrozen` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_the_full_contingency_ships_as_csv_and_is_hashed` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_the_inventory_keeps_the_declared_registry_column_order` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_the_label_free_report_does_not_promise_a_regime_contingency_it_lacks` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_the_loser_of_a_concurrent_race_deletes_nothing` | coperto | test_v31_persistence.py::test_concurrent_reservation_refuses_second_writer |
| `tests/test_run_audit.py::test_the_manifest_records_the_inputs_as_read_not_as_they_end_up` | coperto | test_v31_persistence.py::test_input_staging_binds_hash_to_processed_bytes_and_detects_changes |
| `tests/test_run_audit.py::test_the_report_does_not_claim_prefixes_are_unmerged_when_they_are_merged` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_the_report_states_every_declared_reading_and_points_the_right_way` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_the_reservation_alone_protects_even_with_every_artifact_deleted` | coperto | test_v31_persistence.py::test_concurrent_reservation_refuses_second_writer |
| `tests/test_run_audit.py::test_the_run_id_distinguishes_two_code_revisions` | coperto | test_v31_persistence.py::test_identity_excludes_locations_and_is_sensitive_to_components |
| `tests/test_run_audit.py::test_the_stage_never_writes_a_frozen_alphabet` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_the_stage_samples_git_before_it_writes_anything` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_the_two_modes_never_share_a_run_id` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_run_audit.py::test_the_yaml_error_names_the_original_file_and_keeps_the_snippet` | migrato | test_v31_config.py::test_a_yaml_error_names_the_original_file_and_keeps_its_snippet |
| `tests/test_run_audit.py::test_two_concurrent_identical_runs_cannot_both_publish` | coperto | test_v31_persistence.py::test_concurrent_reservation_refuses_second_writer |
| `tests/test_run_audit.py::test_verified_provenance_is_visible_in_report_and_manifest` | archiviato con legacy_audit.py | audit v2.1 end-to-end; le difese ancora vive sono migrate |
| `tests/test_scores.py::test_delta_ce_analytic_markov_chains` | ritirato | protocollo (b) ritirato; le quattro perdite sono in test_v31_scores.py |
| `tests/test_scores.py::test_gain_restriction_respects_available_past` | sostituito | test_v31_scores.py::test_pooled_core_refuses_a_negative_min_available_past e il target j>=4 in test_v31_corpus.py |
| `tests/test_scores.py::test_pooled_scores_label_free_byte_identical` | sostituito | test_v31_scores.py::test_public_core_and_annotation_keep_scores_independent_of_labels |
| `tests/test_sequences.py::test_all_dropped_sentence_remains_an_empty_row` | coperto | test_v31_corpus.py::test_numeric_order_raw_coordinates_empty_reset_and_targets |
| `tests/test_sequences.py::test_build_sequences_keeps_retained_symbols_in_token_order` | coperto | test_v31_corpus.py::test_numeric_order_raw_coordinates_empty_reset_and_targets |
| `tests/test_sequences.py::test_build_sequences_schema_and_deterministic_order` | archiviato con sequences.py | SEP/P-BOUND ritirati (§13.2); reset senza separatori in test_v31_sampling.py |
| `tests/test_sequences.py::test_extend_alphabet_bound_appends_at_size_and_keeps_ids_stable` | archiviato con sequences.py | SEP/P-BOUND ritirati (§13.2); reset senza separatori in test_v31_sampling.py |
| `tests/test_sequences.py::test_extend_alphabet_bound_does_not_mutate_the_frozen_alphabet` | archiviato con sequences.py | SEP/P-BOUND ritirati (§13.2); reset senza separatori in test_v31_sampling.py |
| `tests/test_sequences.py::test_extend_alphabet_bound_rejects_an_alphabet_already_carrying_the_boundary` | archiviato con sequences.py | SEP/P-BOUND ritirati (§13.2); reset senza separatori in test_v31_sampling.py |
| `tests/test_sequences.py::test_extend_alphabet_bound_rejects_non_contiguous_ids` | archiviato con sequences.py | SEP/P-BOUND ritirati (§13.2); reset senza separatori in test_v31_sampling.py |
| `tests/test_sequences.py::test_manifest_omits_the_key_for_p_reset_runs` | archiviato con sequences.py | SEP/P-BOUND ritirati (§13.2); reset senza separatori in test_v31_sampling.py |
| `tests/test_sequences.py::test_manifest_records_the_runtime_alphabet_extension` | archiviato con sequences.py | SEP/P-BOUND ritirati (§13.2); reset senza separatori in test_v31_sampling.py |
| `tests/test_sequences.py::test_p_bound_produces_adjacent_boundaries_around_an_all_dropped_sentence` | archiviato con sequences.py | SEP/P-BOUND ritirati (§13.2); reset senza separatori in test_v31_sampling.py |
| `tests/test_sequences.py::test_p_bound_returns_one_stream_with_exactly_n_minus_one_boundaries` | archiviato con sequences.py | SEP/P-BOUND ritirati (§13.2); reset senza separatori in test_v31_sampling.py |
| `tests/test_sequences.py::test_p_bound_without_boundary_id_raises` | archiviato con sequences.py | SEP/P-BOUND ritirati (§13.2); reset senza separatori in test_v31_sampling.py |
| `tests/test_sequences.py::test_p_reset_returns_one_sequence_per_sentence` | coperto | test_v31_sampling.py::test_each_sentence_or_fragment_is_one_reset_stream_without_separators |
| `tests/test_sequences.py::test_p_reset_with_boundary_id_raises` | archiviato con sequences.py | SEP/P-BOUND ritirati (§13.2); reset senza separatori in test_v31_sampling.py |
| `tests/test_sequences.py::test_sequences_never_carry_the_boundary_symbol` | coperto | test_v31_sampling.py::test_each_sentence_or_fragment_is_one_reset_stream_without_separators |
| `tests/test_sequences.py::test_single_sentence_document_has_no_boundary` | archiviato con sequences.py | SEP/P-BOUND ritirati (§13.2); reset senza separatori in test_v31_sampling.py |
| `tests/test_sequences.py::test_to_model_input_never_spans_documents` | coperto | test_v31_sampling.py::test_held_out_and_inventory_only_never_enter_any_cell_or_fold |
| `tests/test_sequences.py::test_token_order_is_honoured_not_row_order` | coperto | test_v31_corpus.py::test_input_file_order_does_not_change_corpus |
| `tests/test_sequences.py::test_unknown_boundary_policy_raises` | archiviato con sequences.py | SEP/P-BOUND ritirati (§13.2); reset senza separatori in test_v31_sampling.py |
| `tests/test_sequences.py::test_unknown_doc_id_raises` | archiviato con sequences.py | SEP/P-BOUND ritirati (§13.2); reset senza separatori in test_v31_sampling.py |
| `tests/test_tree_slices.py::test_depth1_nodes_equal_smoothed_bigram` | archiviato | scaffold v2.1, sempre skip; radice e profondità 1 sono in test_v31_context_tree.py |
| `tests/test_tree_slices.py::test_evaluate_on_train_consistency` | archiviato | scaffold v2.1, sempre skip; radice e profondità 1 sono in test_v31_context_tree.py |
| `tests/test_tree_slices.py::test_root_equals_add_beta_unigram` | archiviato | scaffold v2.1, sempre skip; radice e profondità 1 sono in test_v31_context_tree.py |
Riepilogo: 270 funzioni non `v31` a `5f1ec06` — 11 v31 sul posto, 22 migrate, 50 coperte,
14 sostituite, 3 ritirate e 170 archiviate col loro codice.

## Obblighi residui

- **V3**: prova tecnica al seme 0 su sei celle e sette fold (42 coppie / 84 modelli), misure di risorse, congelamento di codice e ambiente; pubblicazione delle evidenze V2/V3 nel manifest.
- **V4**: campagna completa, 490 coppie / 980 identità di modello, tre R1, uguaglianza degli insiemi di chiavi (T25).
- **V5**: report, cinque figure, due pesature, ripresa e rigenerazione prefissata del seme 0 (T24, T27, T29, T30).
- Nessuno di questi obblighi è coperto da fixture: la loro esecuzione richiede fit reali, che iniziano in V3.
