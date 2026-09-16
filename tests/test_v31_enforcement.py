"""Active V0–V1 must collect all required tests and execute real assertions."""
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

import pytest

pytestmark = pytest.mark.v31
ROOT_CONFTEST = Path(__file__).resolve().parents[1]/'conftest.py'

REQUIRED = {'test_gate_inventory_anchor.py': ['test_repository_gate_rejects_a_missing_or_unmarked_inventory'],
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
