"""V2 completion regressions; every fitted corpus is synthetic."""
import json
from pathlib import Path

import pandas as pd
import pytest
import yaml

from hormathos.manifest import sha256_file
from hormathos.pipeline import corpus_run, scientific_run
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
    from hormathos.contracts import load_contracts
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


def test_report_summarizes_every_level_and_pairs_sensitivities_per_block_and_seed(tmp_path):
    """§8.2/§10/§5.1/§11.5, each recomputed here from the per-seed tables of the same report."""
    import numpy as np
    from hormathos.protocols import scores
    from test_v31_descriptive import cell
    blocks = {'ALPHA': (['a'], 'HEX'), 'BETA': (['b'], 'PROSE_ALL'), 'GAMMA': (['c'], 'PROSE_ALL')}
    config, corpus, output = campaign(tmp_path, blocks=blocks, lengths={**LENGTHS, 'c': [9, 8, 7]},
                                      cells=[cell('C0', q=12, seeds=(0, 1)), cell('tiny', q=6, seeds=(0, 1))])
    describe(config, corpus, output, '--cell', 'all')
    report(config, corpus, output)
    summaries, pairs = pd.read_csv(output/'seed_summaries.csv'), pd.read_csv(output/'sensitivity_pairs.csv')
    block_rows, docs = pd.read_csv(output/'block_pairs.csv'), pd.read_csv(output/'document_scores.csv')
    assert set(summaries['level']) == {'group', 'block', 'document', 'group_difference', 'block_difference'}

    def summary(**where):
        rows = summaries[np.logical_and.reduce([summaries[key].eq(value) for key, value in where.items()])]
        assert len(rows) == 1
        return rows.iloc[0]

    def block_q(name):
        rows = block_rows[block_rows.cell.eq(name) & block_rows.held_block.eq('ALPHA') & block_rows.past_band.eq('all')]
        return rows.set_index('seed')['q'].sort_index()

    expected = scores.seed_summary(block_q('C0'))
    row = summary(cell='C0', level='block', unit='ALPHA', past_band='all', metric='q')
    assert [row[f] for f in ('mean', 'sd', 'min', 'max', 'S')] == pytest.approx(
        [expected[f] for f in ('mean', 'sd', 'min', 'max', 'S')], abs=1e-12)
    part = docs[docs.cell.eq('C0') & docs.doc_id.eq('b')].groupby('seed')[
        ['n', 'sum_loss_ctw_original', 'sum_loss_root_original', 'sum_loss_ctw_shuffled', 'sum_loss_root_shuffled']].sum()
    q = ((part.sum_loss_root_original - part.sum_loss_ctw_original)
         - (part.sum_loss_root_shuffled - part.sum_loss_ctw_shuffled)) / part.n
    assert summary(cell='C0', level='document', unit='b', past_band='all', metric='q')['mean'] == pytest.approx(q.mean(), abs=1e-12)

    difference = block_q('tiny') - block_q('C0')
    rows = pairs[pairs.cell.eq('tiny') & pairs.level.eq('block') & pairs.unit.eq('ALPHA')
                 & pairs.past_band.eq('all') & pairs.metric.eq('q')].set_index('seed').sort_index()
    assert list(rows.index) == [0, 1] and (rows['reference'] == 'C0').all()
    assert rows['difference'].to_numpy() == pytest.approx(difference.to_numpy(), abs=1e-12)
    assert summary(cell='tiny', level='block_difference', unit='ALPHA', past_band='all',
                   metric='q')['mean'] == pytest.approx(difference.mean(), abs=1e-12)

    weights = pd.read_csv(output/'aggregation_weights.csv').drop_duplicates(['cell', 'seed', 'block']).set_index(
        ['cell', 'seed', 'block'])
    shares = ['fold_share_HEX', 'fold_share_PROSE_ALL', 'fold_share_own_group']
    assert list(weights.loc[('C0', 0, 'ALPHA'), shares]) == [0.0, 1.0, 0.0]  # §5.1: HEX test, prose training
    assert list(weights.loc[('C0', 0, 'BETA'), shares]) == [0.5, 0.5, 0.5]
    assert weights.loc[('C0', 0, 'BETA'), 'fold_training_tokens'] == 24

    fragments = pd.read_csv(output/'fragment_diagnostics.csv')
    assert len(fragments) == 2 * 3 * 2 * 2  # cells x folds x seeds x contributors
    metrics = ['fragment_count', 'internal_start_count', 'fragment_tokens', 'direct_context_targets']
    for path in sorted(output.glob('pair__*.json')):
        record = json.loads(path.read_text())
        rows = fragments[fragments.cell.eq(record['cell']) & fragments.held_block_key.eq(record['held_block_key'])
                         & fragments.seed.eq(record['seed'])]
        assert rows[['contributor', *metrics]].to_dict('records') == [
            {'contributor': row['block'], **{name: row[name] for name in metrics}} for row in record['fragments']]


def test_empty_document_summaries_stay_null_with_their_reason(tmp_path):
    config, corpus, output = campaign(
        tmp_path, blocks={'ALPHA': (['a', 'short'], 'HEX'), 'BETA': (['b'], 'PROSE_ALL')},
        lengths={**LENGTHS, 'short': [0, 3]})
    describe(config, corpus, output)
    report(config, corpus, output)
    summaries = pd.read_csv(output/'seed_summaries.csv')
    empty = summaries[summaries.level.eq('document') & summaries.unit.eq('short')]
    assert len(empty) == 2 * 3 * 7  # cells x (two bands and the total) x metrics
    assert (empty['reason'] == 'empty_bucket').all() and empty[['mean', 'min', 'max']].isna().all().all()


def test_seed_zero_regeneration_is_compared_and_recorded_by_the_report(tmp_path):
    from hormathos.pipeline import validation_run
    from test_v31_descriptive import cell
    config, corpus, output = campaign(tmp_path, cells=[cell('C0', q=12, seeds=(0, 1)), cell('tiny', q=6, seeds=(0, 1))])
    describe(config, corpus, output, '--cell', 'all')
    regenerated = tmp_path/'regenerated'
    describe(config, corpus, regenerated, '--seed', '0')
    cfg, frames = yaml.safe_load(config.read_text()), scientific_run.load_corpus(corpus)[1]
    result = validation_run.compare_regeneration(output, regenerated, cfg, frames)
    assert result['pair_count'] == 4 and result['model_count'] == 8
    assert result['comparison_scope'] == 'identity_and_values'
    assert result['independent_execution'] == 'record_command_and_log_evidence'
    assert set(result['artifacts'].values()) == {'identical'}
    assert {name.split('__')[0] for name in result['artifacts']} == {'pair', 'sample_ledger', 'positions'}
    with pytest.raises(ValueError, match='distinct') as error:
        validation_run.compare_regeneration(output, output, cfg, frames)
    assert str(error.value)

    name = min(name for name in result['artifacts'] if name.startswith('pair__'))
    manifest = json.loads((regenerated/'manifest.json').read_text())

    def rewrite(delta):  # a float the validator cannot reconstruct, moved from the campaign bytes
        record = json.loads((output/name).read_text())
        record['models']['original']['log_evidence'] += delta
        corpus_run.write_artifact(regenerated/name, record)
        manifest['artifacts'][name] = scientific_run.artifact_record(regenerated/name)
        corpus_run.write_artifact(regenerated/'manifest.json', manifest)

    rewrite(1e-12)
    assert validation_run.compare_regeneration(output, regenerated, cfg, frames)['artifacts'][name] == 'within_tolerance'
    rewrite(1e-6)
    with pytest.raises(ValueError, match='log_evidence') as error:
        validation_run.compare_regeneration(output, regenerated, cfg, frames)
    assert str(error.value)
    rewrite(0.0)
    recorded = report(config, corpus, output, '--regenerated-dir', str(regenerated))['checks']['regeneration']
    assert recorded == validation_run.compare_regeneration(output, regenerated, cfg, frames)


def test_a_scientific_report_requires_the_seed_zero_regeneration(tmp_path, monkeypatch):
    from hormathos.pipeline import run_report
    config, corpus, output = campaign(tmp_path)
    cfg = yaml.safe_load(config.read_text())
    monkeypatch.setattr(scientific_run, 'load_projection', lambda path, fixture: (cfg, True))
    monkeypatch.setattr(scientific_run, 'load_corpus', lambda path: pytest.fail('the guard must come first'))
    with pytest.raises(ValueError, match='regenerat') as error:
        run_report.main(['--config', str(config), '--corpus-dir', str(corpus), '--output-dir', str(output)])
    assert '--regenerated-dir' in str(error.value)
