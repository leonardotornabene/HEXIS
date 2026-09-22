"""V2 completion regressions; every fitted corpus is synthetic."""
import json
from pathlib import Path

import pandas as pd
import pytest
import yaml

from hexis.manifest import sha256_file
from hexis.pipeline import corpus_run, scientific_run
from test_v31_descriptive import campaign, describe, report, LENGTHS

pytestmark = pytest.mark.v31


def test_scientific_identity_verifies_the_present_lock(tmp_path):
    config, corpus, _ = campaign(tmp_path)
    cfg = yaml.safe_load(config.read_text())
    manifest = corpus_run.validate_run(corpus)
    manifest['run_contract']['lock'] = sha256_file(scientific_run.ROOT/'uv.lock')
    assert scientific_run.run_contract(cfg, manifest)['lock'] == manifest['run_contract']['lock']
    manifest['run_contract']['lock'] = '0' * 64
    with pytest.raises(ValueError, match='lock') as error:
        scientific_run.run_contract(cfg, manifest)
    assert str(error.value)


@pytest.mark.parametrize('seed', [False, 0.0])
def test_model_keys_reject_noninteger_seed_without_coercion(seed):
    pair = ['C0', 'a' * 64, seed]
    with pytest.raises(ValueError, match='key') as error:
        scientific_run.key_sets({'pair': [pair],
                                 'model': [[*pair, arm] for arm in ('original', 'shuffled')]})
    assert str(error.value)


def test_zero_target_documents_keep_both_bands_and_null_reasons(tmp_path):
    config, corpus, output = campaign(
        tmp_path, blocks={'ALPHA': (['a', 'short'], 'HEX'), 'BETA': (['b'], 'PROSE_ALL')},
        lengths={**LENGTHS, 'short': [0, 3]})
    describe(config, corpus, output)
    report(config, corpus, output)
    docs = pd.read_csv(output/'document_scores.csv')
    empty = docs[docs.doc_id.eq('short')]
    assert len(empty) == 4 and set(empty.past_band) == {'4_7', 'ge8'}
    assert (empty['n'] == 0).all() and (empty.reason == 'empty_bucket').all()
    assert empty.filter(regex='^sum_loss_').eq(0).all().all()
    assert empty[['ce_ctw_original', 'g_original', 'q']].isna().all().all()
    arms = pd.read_csv(output/'arm_diagnostics.csv')
    empty_arms = arms[arms.doc_id.eq('short')]
    assert len(empty_arms) == 8 and (empty_arms['n'] == 0).all()
    assert empty_arms.resolved_mean.isna().all()
    assert (empty_arms.reason == 'empty_bucket').all()


def test_per_model_resources_are_measured_and_kept_out_of_deterministic_artifacts(tmp_path):
    config, corpus, output = campaign(tmp_path)
    first = describe(config, corpus, output, '--cell', 'C0')
    second = describe(config, corpus, output, '--resume')
    measured = second['metadata']['descriptive']['models']
    assert len(first['metadata']['descriptive']['models']) == 4
    assert len(measured) == 8
    assert {tuple(row['key']) for row in measured} == {tuple(key) for key in second['keys']['model']}
    for row in measured:
        assert row['fit_seconds'] >= 0 and row['evaluation_seconds'] > 0
        assert type(row['peak_rss']) is int and row['peak_rss'] > 0
        assert row['rss_method'] == 'resource.getrusage(RUSAGE_SELF).ru_maxrss in bytes; process lifetime high-water mark'
        assert row['timer'] == 'time.perf_counter; seconds'
    assert 'resources' not in second['run_contract']
    for name in second['artifacts']:
        if name.startswith('pair__'):
            assert 'fit_seconds' not in (output/name).read_text()


@pytest.mark.parametrize('fault', ['missing_C0_positions', 'sensitivity_positions', 'unknown_artifact', 'missing_arm'])
def test_resume_rejects_invalid_artifact_families_and_model_arms(tmp_path, fault):
    config, corpus, output = campaign(tmp_path)
    manifest = describe(config, corpus, output)
    if fault == 'missing_arm':
        manifest['keys']['model'].pop()
    elif fault == 'missing_C0_positions':
        name = next(name for name in manifest['artifacts'] if name.startswith('positions__'))
        (output/name).unlink()
        del manifest['artifacts'][name]
    else:
        name = ('unknown.json' if fault == 'unknown_artifact' else
                scientific_run.positions_name(*next(key for key in manifest['keys']['pair'] if key[0] == 'tiny')))
        if fault == 'unknown_artifact':
            corpus_run.write_artifact(output/name, {})
        else:
            source = next(output.glob('positions__C0__*.parquet'))
            (output/name).write_bytes(source.read_bytes())
        manifest['artifacts'][name] = corpus_run.artifact_record(output/name)
    (output/'manifest.json').write_text(json.dumps(manifest))
    with pytest.raises(ValueError) as error:
        describe(config, corpus, output, '--resume')
    assert str(error.value)


def test_resume_rejects_semantically_corrupt_sums_even_after_rehashing(tmp_path):
    config, corpus, output = campaign(tmp_path)
    manifest = describe(config, corpus, output, '--cell', 'tiny')
    name = next(name for name in manifest['artifacts'] if name.startswith('pair__'))
    pair = json.loads((output/name).read_text())
    pair['document_sums'][0]['n'] += 1
    corpus_run.write_artifact(output/name, pair)
    manifest['artifacts'][name] = corpus_run.artifact_record(output/name)
    corpus_run.write_artifact(output/'manifest.json', manifest)
    with pytest.raises(ValueError, match='denominator') as error:
        describe(config, corpus, output, '--resume')
    assert str(error.value)


@pytest.mark.parametrize('fault', ['missing', 'duplicate', 'negative', 'unit'])
def test_resource_records_are_complete_valid_and_bound_to_model_keys(tmp_path, fault):
    config, corpus, output = campaign(tmp_path)
    manifest = describe(config, corpus, output)
    rows = manifest['metadata']['descriptive']['models']
    if fault == 'missing':
        rows.pop()
    elif fault == 'duplicate':
        rows[-1] = rows[0]
    elif fault == 'negative':
        rows[0]['evaluation_seconds'] = -1
    else:
        rows[0]['rss_method'] = 'unknown units'
    corpus_run.write_artifact(output/'manifest.json', manifest)
    with pytest.raises(ValueError, match='resource') as error:
        scientific_run.validate_run(output)
    assert str(error.value)


def test_diagnostics_carry_the_report_contract_names(tmp_path):
    """report_contract_v3.1.json fixes the names; `_by_reason`/`_by_length` name column families."""
    from hexis.contracts import load_contracts
    contract = load_contracts()['report']
    aggregate = contract['paired_aggregate_all_cells']

    def missing(required, fields):
        return [name for name in required if name not in fields and not (
            name.endswith(('_by_reason', '_by_length')) and any(f.startswith(name + '_') for f in fields))]

    config, corpus, output = campaign(tmp_path)
    describe(config, corpus, output, '--cell', 'all')
    manifest = report(config, corpus, output)
    record = json.loads((output/min(n for n in manifest['artifacts'] if n.startswith('pair__'))).read_text())
    docs = set(record['document_sums'][0])
    assert missing(aggregate['fields'], docs) == []
    assert missing(aggregate['per_arm_diagnostics'], set(record['arm_diagnostics'][0])) == []
    for population in ('training', 'evaluation'):
        assert missing(aggregate['shuffle'], set(record['shuffle'][population]) | docs) == []
    assert missing(contract['model_diagnostics'], set(pd.read_csv(output/'model_diagnostics.csv').columns)) == []
