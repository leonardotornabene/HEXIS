"""V2 persistence: the descriptive/report CLIs, their manifest, atomicity and resume.

Every fixture here is a toy campaign — three documents, a five-symbol alphabet,
two blocks, two cells, one seed — written to a temporary corpus run and driven
through the real entry points. No Greek sentence is sampled, fitted or scored in
this file: real fits belong to V3 (piano §14), and this module must stay runnable
without `data/raw`.

The toy contract is deliberately *not* the deposited analytical projection, so
both CLIs require the explicit `--fixture` declaration and `run_report` records
the campaign as non-scientific. That refusal is itself under test: it is what
stops a fixture run from ever being read as a result.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

from hexis.contracts import digest
from hexis.manifest import sha256_file
from hexis.pipeline import corpus_run, run_descriptive, run_report, scientific_run
from hexis.protocols import sampling, scores

pytestmark = pytest.mark.v31

ROOT = Path(__file__).resolve().parents[1]
VARIANT = 'toy'
M = 5
LENGTHS = {'a': [9, 9, 9, 9], 'b': [9, 7, 6, 9], 'z': [8, 8]}
BLOCKS = {'ALPHA': (['a'], 'HEX'), 'BETA': (['b'], 'PROSE_ALL')}
TABLES = ('document_scores.csv', 'block_pairs.csv', 'aggregation_weights.csv', 'contrasts.csv',
          'seed_summaries.csv', 'sensitivity_pairs.csv', 'model_diagnostics.csv',
          'arm_diagnostics.csv', 'fragment_diagnostics.csv', 'root_distributions.csv',
          'jsd_pairs.csv', 'jsd_centroids.csv', 'jsd_contributions.csv')


# --- toy corpus and toy contract ---------------------------------------------

def cell(identifier, *, q, D=2, a=0.5, seeds=(0,)):
    return {'id': identifier, 'variant': VARIANT, 'D': D, 'rho': 0.5, 'q': q, 'boundary': 'reset',
            'seeds': list(seeds), 'arms': ['original', 'shuffled'], 'a_per_symbol': a, 'm': M}


def toy_config(tmp_path, *, cells=None, blocks=None, name='fixture.yaml'):
    """A minuscule analytical projection: two cells, two blocks, one seed, two arms."""
    blocks = BLOCKS if blocks is None else blocks
    declared = [{'block': name_, 'docs': docs, 'group': group,
                 'block_key': sampling.block_key(docs)}
                for name_, (docs, group) in sorted(blocks.items())]
    registry = [{'canonical_doc_id': doc, 'role': 'primary', 'dependence_block': name_}
                for name_, (docs, _) in sorted(blocks.items()) for doc in docs]
    cfg = {'spec_version': 'HEXIS-3.1-fixture',
           'representation': {'version': 'toy-1'},
           'min_available_past': 4,
           'rng': {'version': 'hexis-v3-rng-1'},
           'cells': cells if cells is not None else [cell('C0', q=12), cell('tiny', q=6)],
           'blocks': declared,
           'registry': [*registry, {'canonical_doc_id': 'z', 'role': 'inventory_only',
                                    'dependence_block': None}],
           'R1': {'variants': [VARIANT], 'a_per_symbol': 0.5}}
    path = tmp_path / name
    path.write_text(yaml.safe_dump(cfg, sort_keys=True), encoding='utf-8')
    return path


def toy_frames(lengths=None):
    rng = np.random.default_rng(7)
    sentences, coordinates, slot = [], [], 0
    for doc, sizes in (lengths or LENGTHS).items():
        role = 'inventory_only' if doc == 'z' else 'primary'
        for ordinal, length in enumerate(sizes, start=1):
            symbols = [int(value) for value in rng.integers(M, size=length)]
            slots = list(range(slot, slot + length))
            slot += length
            sentences.append({'variant': VARIANT, 'role': role, 'doc_id': doc,
                              'sent_id': f'{doc}@{ordinal}', 'part_order': 0,
                              'source_ordinal': ordinal, 'encoded_length': length,
                              'symbols': symbols, 'slot_uids': slots})
            coordinates.extend({'variant': VARIANT, 'doc_id': doc, 'sent_id': f'{doc}@{ordinal}',
                                'slot_uid': uid, 'symbol_id': symbol, 'role': role,
                                'available_past': index, 'eligible': index >= 4}
                               for index, (uid, symbol) in enumerate(zip(slots, symbols)))
    sequences = pd.DataFrame(sentences)
    documents = pd.DataFrame([{'variant': VARIANT, 'doc_id': doc, 'role': group['role'].iloc[0],
                               'kept': int(group['encoded_length'].sum()),
                               'sentences': len(group)}
                              for doc, group in sequences.groupby('doc_id', sort=True)])
    return {'documents.csv': documents, 'sequences.parquet': sequences,
            'coordinates.parquet': pd.DataFrame(coordinates)}


def toy_corpus(tmp_path, *, lengths=None, alphabets='1' * 64):
    """A published V1-shaped corpus run holding the toy artifacts."""
    contract = {'spec_version': 'HEXIS-3.1-fixture', 'representation_version': 'toy-1',
                'analytical_contracts': {}, 'source_commit': '0' * 40, 'plan': '0' * 64,
                'code': {}, 'data': {'toy.conllu': '0' * 64}, 'registry': '4' * 64,
                'alphabets': alphabets, 'configuration': '2' * 64,
                'lock': sha256_file(ROOT / 'uv.lock'),
                'rng_version': 'hexis-v3-rng-1'}
    artifacts = toy_frames(lengths)
    directory = tmp_path / 'corpus'
    corpus_run.publish_stage(directory, 'audit', {'documents.csv': artifacts['documents.csv']},
                             contract, {})
    corpus_run.publish_stage(directory, 'encode', artifacts, contract, {})
    return directory


def campaign(tmp_path, *, cells=None, blocks=None, lengths=None, alphabets='1' * 64, out='run'):
    corpus = toy_corpus(tmp_path, lengths=lengths, alphabets=alphabets)
    config = toy_config(tmp_path, cells=cells, blocks=blocks)
    return config, corpus, tmp_path / out


def describe(config, corpus, output, *argv):
    return run_descriptive.main(['--config', str(config), '--corpus-dir', str(corpus),
                                 '--output-dir', str(output), '--fixture', *argv])


def report(config, corpus, output, *argv):
    return run_report.main(['--config', str(config), '--corpus-dir', str(corpus),
                            '--output-dir', str(output), '--fixture', *argv])


# --- the descriptive campaign -------------------------------------------------

def test_cli_runs_every_cell_and_publishes_one_partition_per_pair(tmp_path):
    config, corpus, output = campaign(tmp_path)
    manifest = describe(config, corpus, output, '--cell', 'all')
    assert manifest['schema_version'] == 'hexis-scientific-manifest-2'
    assert manifest['completed_stages'] == ['descriptive']
    assert manifest['run_id'] == digest(manifest['run_contract'])
    assert sorted(manifest['run_contract']) == sorted(
        ['spec_version', 'representation_version', 'analytical_contracts', 'source_commit',
         'plan', 'code', 'data', 'registry', 'alphabets', 'configuration', 'lock', 'rng_version'])
    pairs = {tuple(key) for key in manifest['keys']['pair']}
    models = {tuple(key) for key in manifest['keys']['model']}
    keys = {sampling.block_key(docs) for docs, _ in BLOCKS.values()}
    assert pairs == {(cell_id, key, 0) for cell_id in ('C0', 'tiny') for key in keys}
    assert models == {(*pair, arm) for pair in pairs for arm in ('original', 'shuffled')}
    assert len(manifest['keys']['model']) == 8 and len(manifest['keys']['pair']) == 4
    # One record per pair, positional persistence in C0 alone (§11.4).
    records = sorted(name for name in manifest['artifacts'] if name.startswith('pair__'))
    positions = sorted(name for name in manifest['artifacts'] if name.startswith('positions__'))
    assert len(records) == 4
    assert len(positions) == 2 and all('__C0__' in name for name in positions)
    assert scientific_run.validate_run(output)['run_id'] == manifest['run_id']


def test_persisted_positions_carry_exactly_the_plan_columns_and_every_eligible_slot(tmp_path):
    config, corpus, output = campaign(tmp_path)
    manifest = describe(config, corpus, output, '--cell', 'C0')
    name = next(name for name in manifest['artifacts'] if name.startswith('positions__'))
    frame = pd.read_parquet(output / name)
    assert list(frame.columns) == list(scores.POSITION_COLUMNS)
    assert all(str(frame[column].dtype) == 'float64' for column in
               [c for c in scores.POSITION_COLUMNS if c.startswith(('loss_', 'unseen_', 'resolved_'))])
    block = name.split('__')[2]
    docs = next(docs for docs, _ in BLOCKS.values() if sampling.block_key(docs) == block)
    coordinates = pd.read_parquet(corpus / 'coordinates.parquet')
    eligible = coordinates[coordinates['doc_id'].isin(docs) & coordinates['eligible']]
    assert len(frame) == len(eligible)
    assert set(frame['slot_uid']) == set(eligible['slot_uid'])


def test_every_pair_persists_its_exact_sampling_ledger(tmp_path):
    config, corpus, output = campaign(tmp_path)
    manifest = describe(config, corpus, output)
    sequences = pd.read_parquet(corpus/'sequences.parquet')
    for name in manifest['artifacts']:
        if not name.startswith('pair__'):
            continue
        record = json.loads((output/name).read_text())
        ledger_path = output/record['sample_ledger']
        ledger_rows = json.loads(ledger_path.read_text())
        assert digest(ledger_rows) == record['ledger_sha256']
        assert len(ledger_rows) == record['ledger_rows']
        ledger = pd.DataFrame(ledger_rows)
        assert int((ledger['end'] - ledger['start']).sum()) == record['q']
        streams = sampling.sample_streams(ledger, sequences, record['variant'])
        from hexis.model.context_tree import CTW, CTWParams
        rebuilt = CTW(CTWParams.from_rho(m=record['m'], depth=record['depth'],
                                          a=record['a_per_symbol'], rho=record['rho'])).fit(
                                              [stream['symbols'] for stream in streams])
        assert rebuilt.fingerprint() == record['models']['original']['fingerprint']


@pytest.mark.parametrize('fault', ['changed_key', 'duplicate_key'])
def test_sensitivity_checks_coordinate_slot_sets_before_discarding_vectors(tmp_path, fault):
    config = yaml.safe_load(toy_config(tmp_path).read_text())
    frames = toy_frames()
    coords = frames['coordinates.parquet']
    rows = coords.index[coords['doc_id'].eq('a') & coords['eligible']]
    coords.loc[rows[-1], 'slot_uid'] = (99999 if fault == 'changed_key'
                                       else coords.loc[rows[0], 'slot_uid'])
    with pytest.raises(ValueError, match='slot') as exc:
        run_descriptive.run_pair(config, frames, config['cells'][1], 'ALPHA', 0)
    assert str(exc.value)


def test_a_cell_selection_leaves_the_other_cells_unpublished(tmp_path):
    config, corpus, output = campaign(tmp_path)
    manifest = describe(config, corpus, output, '--cell', 'tiny')
    assert {key[0] for key in manifest['keys']['pair']} == {'tiny'}
    with pytest.raises(ValueError, match='unknown cell') as exc:
        describe(config, corpus, tmp_path / 'other', '--cell', 'q_half')
    assert 'q_half' in str(exc.value)


def test_seed_zero_trial_resumes_to_full_campaign_without_changing_identity(tmp_path):
    config, corpus, output = campaign(tmp_path, cells=[cell('C0', q=12, seeds=(0, 1)),
                                                       cell('tiny', q=6, seeds=(0, 1))])
    first = describe(config, corpus, output, '--cell', 'all', '--seed', '0')
    assert len(first['keys']['pair']) == 4
    assert {key[2] for key in first['keys']['pair']} == {0}
    before = {name: (output / name).read_bytes() for name in first['artifacts']}
    with pytest.raises(ValueError, match='key') as exc:
        report(config, corpus, output)
    assert str(exc.value)
    complete = describe(config, corpus, output, '--resume')
    assert len(complete['keys']['pair']) == 8 and len(complete['keys']['model']) == 16
    assert complete['run_id'] == first['run_id']
    assert complete['checks']['reused_partitions'] == 4
    assert complete['checks']['new_model_fits'] == 8
    assert all((output / name).read_bytes() == data for name, data in before.items())
    assert report(config, corpus, output)['checks']['scientific'] is False


def test_seed_selection_refuses_undeclared_seed_before_loading_corpus(tmp_path):
    config = toy_config(tmp_path, cells=[cell('C0', q=12, seeds=(1,))])
    with pytest.raises(ValueError, match='seed') as exc:
        describe(config, tmp_path / 'absent-corpus', tmp_path / 'output', '--seed', '0')
    assert 'C0' in str(exc.value)
    assert not (tmp_path / 'output').exists()


def test_interrupted_fit_keeps_completed_pairs_and_resume_matches_fresh_run(tmp_path, monkeypatch):
    config, corpus, output = campaign(tmp_path)
    real_pair = run_descriptive.run_pair
    completed = []

    def interrupted(*args, **kwargs):
        if completed:
            raise RuntimeError('interrupted between pairs')
        result = real_pair(*args, **kwargs)
        completed.append(result[0])
        return result

    monkeypatch.setattr(run_descriptive, 'run_pair', interrupted)
    with pytest.raises(RuntimeError, match='between pairs') as exc:
        describe(config, corpus, output)
    assert str(exc.value)
    partial = scientific_run.validate_run(output)
    assert len(partial['keys']['pair']) == 1 and len(partial['keys']['model']) == 2
    before = {name: (output / name).read_bytes() for name in partial['artifacts']}
    monkeypatch.setattr(run_descriptive, 'run_pair', real_pair)
    resumed = describe(config, corpus, output, '--resume')
    assert resumed['checks']['reused_partitions'] == 1
    assert resumed['checks']['new_model_fits'] == 6
    assert all((output / name).read_bytes() == data for name, data in before.items())
    fresh_dir = tmp_path / 'fresh'
    fresh = describe(config, corpus, fresh_dir)
    assert resumed['run_id'] == fresh['run_id']
    assert resumed['artifacts'] == fresh['artifacts']
    assert all((output / name).read_bytes() == (fresh_dir / name).read_bytes()
               for name in fresh['artifacts'])


def test_the_fixture_declaration_is_required_and_refused_for_the_deposit(tmp_path):
    config, corpus, output = campaign(tmp_path)
    with pytest.raises(ValueError) as exc:
        run_descriptive.main(['--config', str(config), '--corpus-dir', str(corpus),
                              '--output-dir', str(output), '--cell', 'all'])
    assert 'config' in str(exc.value)
    with pytest.raises(ValueError, match='--fixture') as exc:
        run_descriptive.main(['--config', str(ROOT / 'config/default.yaml'), '--corpus-dir',
                              str(corpus), '--output-dir', str(output), '--fixture'])
    assert 'deposited' in str(exc.value)


# --- T26: atomicity, interruption, resume, corruption, keys -------------------

def test_a_second_run_refuses_the_destination_unless_resume_is_asked_for(tmp_path):
    config, corpus, output = campaign(tmp_path)
    first = describe(config, corpus, output, '--cell', 'C0')
    before = (output / 'manifest.json').read_bytes()
    with pytest.raises(FileExistsError) as exc:
        describe(config, corpus, output, '--cell', 'tiny')
    assert str(output) in str(exc.value)
    assert (output / 'manifest.json').read_bytes() == before
    assert scientific_run.validate_run(output)['run_id'] == first['run_id']


def test_resume_reuses_validated_partitions_byte_for_byte_and_finishes_the_rest(tmp_path):
    config, corpus, output = campaign(tmp_path)
    first = describe(config, corpus, output, '--cell', 'C0')
    reused = {name: sha256_file(output / name) for name in first['artifacts']}
    second = describe(config, corpus, output, '--cell', 'all', '--resume')
    assert set(first['artifacts']) < set(second['artifacts'])
    assert all(sha256_file(output / name) == sha for name, sha in reused.items())
    assert second['run_id'] == first['run_id']
    assert len(second['keys']['pair']) == 4
    assert second['checks']['reused_partitions'] == 2
    # A resume with nothing left to do is a no-op, not a second publication.
    third = describe(config, corpus, output, '--cell', 'all', '--resume')
    assert third['artifacts'] == second['artifacts']
    assert third['checks']['reused_partitions'] == 4


def test_resume_refuses_a_changed_contract_or_a_changed_corpus(tmp_path, monkeypatch):
    config, corpus, output = campaign(tmp_path)
    describe(config, corpus, output, '--cell', 'C0')
    changed = toy_config(tmp_path, cells=[cell('C0', q=11), cell('tiny', q=6)], name='changed.yaml')
    with pytest.raises(ValueError, match='run_contract') as exc:
        describe(changed, corpus, output, '--cell', 'all', '--resume')
    assert 'configuration' in str(exc.value)
    other = toy_corpus(tmp_path / 'second', alphabets='9' * 64)
    with pytest.raises(ValueError, match='run_contract') as exc:
        describe(config, other, output, '--cell', 'all', '--resume')
    assert 'alphabets' in str(exc.value)
    # Changed code under an unchanged configuration is a different run, never a resume.
    monkeypatch.setattr(scientific_run, '_code_identity', lambda: {'src/hexis/ghost.py': '0' * 64})
    with pytest.raises(ValueError, match='run_contract') as rewritten:
        describe(config, corpus, output, '--cell', 'all', '--resume')
    assert 'code' in str(rewritten.value)


@pytest.mark.parametrize('fault', ['bytes', 'truncated', 'missing', 'rows', 'identity',
                                   'ledger_reference'])
def test_a_corrupted_partition_is_detected_and_never_reused(tmp_path, fault):
    config, corpus, output = campaign(tmp_path)
    manifest = describe(config, corpus, output, '--cell', 'C0')
    record = next(name for name in manifest['artifacts'] if name.startswith('pair__'))
    positions = next(name for name in manifest['artifacts'] if name.startswith('positions__'))
    if fault == 'bytes':
        (output / record).write_text('{}')
    if fault == 'truncated':
        (output / positions).write_bytes((output / positions).read_bytes()[:-64])
    if fault == 'missing':
        (output / record).unlink()
    if fault in ('rows', 'identity'):
        broken = json.loads((output / 'manifest.json').read_text())
        if fault == 'identity':
            broken['run_id'] = 'incorrect'
        else:
            broken['artifacts'][record]['rows'] = 99
        (output / 'manifest.json').write_text(json.dumps(broken))
    if fault == 'ledger_reference':
        pair = json.loads((output / record).read_text())
        pair['ledger_sha256'] = '0' * 64
        (output / record).write_text(json.dumps(pair))
        manifest['artifacts'][record] = corpus_run.artifact_record(output / record)
        (output / 'manifest.json').write_text(json.dumps(manifest))
    with pytest.raises(ValueError) as exc:
        scientific_run.validate_run(output)
    assert str(exc.value)
    with pytest.raises(ValueError) as resumed:
        describe(config, corpus, output, '--cell', 'all', '--resume')
    assert str(resumed.value)


def test_an_interrupted_write_publishes_nothing_and_leaves_the_prior_state_intact(tmp_path,
                                                                                 monkeypatch):
    config, corpus, output = campaign(tmp_path)
    first = describe(config, corpus, output, '--cell', 'C0')
    before = (output / 'manifest.json').read_bytes()
    real = scientific_run.write_artifact

    def interrupt(path, value):
        real(path, value)
        raise RuntimeError('interrupted')

    monkeypatch.setattr(scientific_run, 'write_artifact', interrupt)
    with pytest.raises(RuntimeError, match='interrupted') as exc:
        describe(config, corpus, output, '--cell', 'all', '--resume')
    assert str(exc.value)
    assert (output / 'manifest.json').read_bytes() == before
    assert set(scientific_run.validate_run(output)['artifacts']) == set(first['artifacts'])


def test_a_kill_between_the_hard_link_and_the_manifest_blocks_resume_by_name(tmp_path):
    config, corpus, output = campaign(tmp_path)
    describe(config, corpus, output, '--cell', 'C0')
    orphan = output / 'pair__tiny__killed__s0.json'
    os.link(next(output.glob('pair__C0__*.json')), orphan)
    with pytest.raises(ValueError) as exc:
        scientific_run.validate_run(output)
    assert orphan.name in str(exc.value)
    with pytest.raises(ValueError) as resumed:
        describe(config, corpus, output, '--cell', 'all', '--resume')
    assert orphan.name in str(resumed.value)
    orphan.unlink()
    assert len(describe(config, corpus, output, '--cell', 'all', '--resume')['keys']['pair']) == 4


def test_two_destinations_publish_the_same_partitions_byte_for_byte(tmp_path):
    # Identity excludes paths, timestamps and resources (§11.3), so the whole campaign is
    # the bytes of the contract alone: a second destination is the same run, not a second
    # result. Both stages run, so the report tables are under the same claim.
    config, corpus, output = campaign(tmp_path)
    second = tmp_path / 'second'
    describe(config, corpus, output, '--cell', 'all')
    describe(config, corpus, second, '--cell', 'all')
    left, right = report(config, corpus, output), report(config, corpus, second)
    assert left['run_id'] == right['run_id']
    measured = 'model_diagnostics.csv'  # §11.5 resources are measured, never byte-identical
    assert all(sha256_file(output / name) == sha256_file(second / name)
               for name in left['artifacts'] if name != measured)
    pd.testing.assert_frame_equal(
        pd.read_csv(output / measured).drop(columns=list(run_report.RESOURCE_COLUMNS)),
        pd.read_csv(second / measured).drop(columns=list(run_report.RESOURCE_COLUMNS)))
    for manifest in (left, right):
        manifest['artifacts'].pop(measured)
    assert ({name: value for name, value in left.items() if name != 'metadata'}
            == {name: value for name, value in right.items() if name != 'metadata'})
    assert left['metadata']['report']['output_dir'] != right['metadata']['report']['output_dir']


@pytest.mark.parametrize('fault', ['duplicate_json_key', 'nonfinite_json', 'unknown_field',
                                   'missing_field', 'duplicate_model_key', 'extra_model_key',
                                   'extra_artifact', 'unknown_stage'])
def test_the_manifest_refuses_duplicate_extra_and_missing_keys(tmp_path, fault):
    config, corpus, output = campaign(tmp_path)
    describe(config, corpus, output, '--cell', 'C0')
    path = output / 'manifest.json'
    content = path.read_text()
    if fault == 'duplicate_json_key':
        content = content.replace('"completed_stages"', '"completed_stages":["descriptive"],"completed_stages"')
    if fault == 'nonfinite_json':
        content = content.replace('"metadata":{', '"metadata":{"bad":NaN,')
    if fault == 'unknown_field':
        content = content.replace('"metadata":{', '"unknown":0,"metadata":{')
    if fault in ('missing_field', 'duplicate_model_key', 'extra_model_key', 'unknown_stage'):
        broken = json.loads(content)
        if fault == 'missing_field':
            broken.pop('evidence')
        if fault == 'duplicate_model_key':
            broken['keys']['model'].append(list(broken['keys']['model'][0]))
        if fault == 'extra_model_key':
            broken['keys']['model'].append(['ghost', '0' * 64, 0, 'original'])
        if fault == 'unknown_stage':
            broken['completed_stages'] = ['descriptive', 'confirmatory']
        content = json.dumps(broken)
    if fault == 'extra_artifact':
        (output / 'pair__ghost.json').write_text('{}')
    path.write_text(content)
    with pytest.raises(ValueError) as exc:
        scientific_run.validate_run(output)
    assert str(exc.value)


# --- the report and its six-step validator ------------------------------------

def test_report_cli_emits_every_declared_table_from_a_complete_campaign(tmp_path):
    config, corpus, output = campaign(tmp_path)
    describe(config, corpus, output, '--cell', 'all')
    manifest = report(config, corpus, output)
    assert manifest['completed_stages'] == ['descriptive', 'report']
    assert set(TABLES) <= set(manifest['artifacts'])
    assert manifest['checks']['scientific'] is False
    assert manifest['checks']['steps'] == [1, 2, 3, 4, 5, 6]
    contrasts = pd.read_csv(output / 'contrasts.csv')
    assert set(contrasts['aggregation']) == {'equal_block', 'eligible_token_weighted'}
    assert set(contrasts['group']) == {'HEX', 'PROSE_ALL', 'contrast'}
    rows = contrasts[contrasts['group'].eq('contrast')]
    assert len(rows) == 4  # two cells x two weightings
    assert np.allclose(rows['q'], rows['g_original'] - rows['g_shuffled'], atol=1e-12)
    documents = pd.read_csv(output / 'document_scores.csv')
    assert set(documents['past_band']) == {'4_7', 'ge8'}
    assert set(documents['doc_id']) == {'a', 'b'}
    jsd = pd.read_csv(output / 'jsd_pairs.csv')
    assert len(jsd) == 1 and jsd['jsd'].iloc[0] >= 0.0
    assert not (output / 'figures').exists()


def test_report_reconstructs_documents_blocks_and_groups_from_the_persisted_positions(tmp_path):
    config, corpus, output = campaign(tmp_path)
    describe(config, corpus, output, '--cell', 'all')
    report(config, corpus, output)
    documents = pd.read_csv(output / 'document_scores.csv')
    coordinates = pd.read_parquet(corpus / 'coordinates.parquet')
    frames = [pd.read_parquet(path) for path in sorted(output.glob('positions__C0__*.parquet'))]
    positions = pd.concat(frames, ignore_index=True).merge(
        coordinates[['slot_uid', 'doc_id', 'available_past']], on='slot_uid', validate='one_to_one')
    positions['past_band'] = positions['available_past'].map(scores.past_band)
    rebuilt = scores.aggregate(positions, keys=['doc_id']).set_index(['doc_id', 'past_band'])
    kept = documents[documents['cell'].eq('C0')].set_index(['doc_id', 'past_band'])
    assert set(rebuilt.index) == set(kept.index)
    for column in ('n', 'sum_loss_ctw_original', 'sum_loss_root_shuffled'):
        assert np.allclose(kept[column], rebuilt.loc[kept.index, column], atol=0, rtol=0)
    blocks = pd.read_csv(output / 'block_pairs.csv')
    total = blocks[blocks['cell'].eq('C0') & blocks['past_band'].eq('all')]
    assert int(total['n'].sum()) == int(rebuilt['n'].sum())


def test_arm_diagnostics_keep_the_document_dimension_the_loss_sums_carry(tmp_path):
    # §11.5 keeps the §9.3 summaries beside the document/band loss sums, and §14.3 counts
    # 1.540 logical rows = documents x (cell,seed) x arms, before the bands. A block holding
    # two documents is what tells the two granularities apart: summing the document dimension
    # away here would be irreversible for the five cells that persist no positions.
    blocks = {'ALPHA': (['a', 'c'], 'HEX'), 'BETA': (['b'], 'PROSE_ALL')}
    config, corpus, output = campaign(tmp_path, blocks=blocks, lengths={**LENGTHS, 'c': [9, 8]})
    describe(config, corpus, output, '--cell', 'all')
    report(config, corpus, output)
    frame = pd.read_csv(output / 'arm_diagnostics.csv')
    keys = ['cell', 'held_block_key', 'seed', 'doc_id', 'arm', 'past_band']
    assert not frame.duplicated(subset=keys).any()
    cells, seeds = 2, 1
    evaluated = sum(len(docs) for docs, _ in blocks.values())  # each block is held once
    assert len(frame) == cells * seeds * evaluated * len(scores.ARMS) * len(scores.BANDS) == 24
    alpha = frame[frame['held_block'].eq('ALPHA')]
    assert set(alpha['doc_id']) == {'a', 'c'}
    # The two documents of the held block carry their own targets, not one shared block row.
    counts = alpha[alpha['cell'].eq('C0') & alpha['arm'].eq('original')].set_index(
        ['doc_id', 'past_band'])['n']
    assert counts.loc[('a', '4_7')] == 16 and counts.loc[('c', '4_7')] == 8
    assert counts.loc[('a', 'ge8')] == 4 and counts.loc[('c', 'ge8')] == 1
    # Every summary lines up with the document/band row of the same key, one arm at a time.
    documents = pd.read_csv(output / 'document_scores.csv')
    merged = frame.merge(documents[[*run_report.KEY_COLUMNS, 'doc_id', 'past_band', 'n']],
                         on=[*run_report.KEY_COLUMNS, 'doc_id', 'past_band'],
                         suffixes=('', '_document'), validate='many_to_one')
    assert len(merged) == len(frame)
    assert (merged['n'] == merged['n_document']).all()


def test_report_refuses_a_document_silently_dropped_from_document_scores(tmp_path):
    # Explicit corruption: a zero-target document must still have both rows.
    blocks = {'ALPHA': (['a', 'short'], 'HEX'), 'BETA': (['b'], 'PROSE_ALL')}
    lengths = {**LENGTHS, 'short': [3, 3]}  # both sentences shorter than min_available_past
    config, corpus, output = campaign(tmp_path, blocks=blocks, lengths=lengths)
    manifest = describe(config, corpus, output, '--cell', 'all')
    for name in manifest['artifacts']:
        if name.startswith('pair__'):
            record = json.loads((output/name).read_text())
            record['document_sums'] = [row for row in record['document_sums'] if row['doc_id'] != 'short']
            corpus_run.write_artifact(output/name, record)
            manifest['artifacts'][name] = corpus_run.artifact_record(output/name)
    corpus_run.write_artifact(output/'manifest.json', manifest)
    with pytest.raises(ValueError, match='document_band') as exc:
        report(config, corpus, output)
    assert 'short' in str(exc.value) and 'document_scores.csv' in str(exc.value)
    # expected_keys() itself: both bands, str doc_id, one entry per (cell, seed, doc).
    expected = run_report.expected_keys(yaml.safe_load(config.read_text()))['document_band']
    key = sampling.block_key(['a', 'short'])
    assert {('C0', key, 0, 'short', '4_7'), ('C0', key, 0, 'short', 'ge8'),
           ('tiny', key, 0, 'short', '4_7'), ('tiny', key, 0, 'short', 'ge8')} <= set(expected)


def test_report_refuses_an_incomplete_campaign_and_any_inventory_only_score(tmp_path):
    config, corpus, output = campaign(tmp_path)
    describe(config, corpus, output, '--cell', 'C0')
    with pytest.raises(ValueError, match='key') as exc:
        report(config, corpus, output)
    assert 'tiny' in str(exc.value)
    scored = pd.DataFrame([{'doc_id': 'z'}, {'doc_id': 'a'}])
    with pytest.raises(ValueError, match='inventory_only') as refused:
        run_report.check_roles(scored, pd.read_csv(corpus / 'documents.csv'))
    assert 'z' in str(refused.value)


def test_report_refuses_a_run_that_is_not_the_deposited_configuration(tmp_path):
    config, corpus, output = campaign(tmp_path)
    describe(config, corpus, output, '--cell', 'all')
    with pytest.raises(ValueError, match='deposited') as exc:
        run_report.main(['--config', str(config), '--corpus-dir', str(corpus),
                         '--output-dir', str(output)])
    assert 'configuration' in str(exc.value)
    assert not (output / 'contrasts.csv').exists()


def test_report_refuses_a_second_emission_and_a_partition_added_after_it(tmp_path):
    config, corpus, output = campaign(tmp_path)
    describe(config, corpus, output, '--cell', 'all')
    report(config, corpus, output)
    with pytest.raises(FileExistsError) as exc:
        report(config, corpus, output)
    assert 'report' in str(exc.value)
    with pytest.raises(FileExistsError) as closed:
        describe(config, corpus, output, '--cell', 'all', '--resume')
    assert 'report' in str(closed.value)


def test_evidence_must_be_recorded_under_the_code_and_lock_of_this_run(tmp_path):
    config, corpus, output = campaign(tmp_path)
    manifest = describe(config, corpus, output, '--cell', 'all')
    # §14.2 step 2 names V0-V3; the descriptive stage records V0/V1 for itself, while V2/V3
    # come from `validation_run` and are recomputed wherever they are read.
    assert scientific_run.EVIDENCE_STEPS == ('V0', 'V1')
    assert set(manifest['evidence']) == set(scientific_run.EVIDENCE_STEPS)
    assert manifest['evidence']['V1']['code'] == digest(manifest['run_contract']['code'])
    with pytest.raises(ValueError, match='evidence') as exc:
        run_report.check_evidence({'V0': manifest['evidence']['V0']}, manifest['run_contract'])
    assert 'V1' in str(exc.value)
    stale = {key: dict(value, code='stale') for key, value in manifest['evidence'].items()}
    with pytest.raises(ValueError, match='evidence') as drifted:
        run_report.check_evidence(stale, manifest['run_contract'])
    assert 'code' in str(drifted.value)


def test_real_report_requires_v2_and_v3_evidence_as_well_as_corpus(tmp_path):
    config, corpus, output = campaign(tmp_path)
    manifest = describe(config, corpus, output)
    with pytest.raises(ValueError, match='V2.*V3') as exc:
        run_report.check_evidence(manifest['evidence'], manifest['run_contract'], scientific=True)
    assert 'evidence' in str(exc.value)
    assert not (output/'contrasts.csv').exists()


# --- the retired v2.1 entry points --------------------------------------------

@pytest.mark.parametrize('module', ['run_confirmatory', 'run_null_calibration', 'run_reference',
                                    'run_latin', 'run_sensitivity'])
def test_retired_stages_declare_their_retirement_and_refuse_to_run(module):
    import importlib
    stage = importlib.import_module(f'hexis.pipeline.{module}')
    assert 'retired' in (stage.__doc__ or '').lower()
    assert '3.1' in (stage.__doc__ or '')
    with pytest.raises(SystemExit) as exc:
        stage.main()
    assert module in str(exc.value)


def test_the_descriptive_path_imports_no_retired_scientific_module():
    import ast

    def imported(source):
        """Every module a source names, `from package import module` included."""
        modules = []
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Import):
                modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                modules.append(node.module or '')
                modules.extend(f'{node.module or ""}.{alias.name}' for alias in node.names)
        return modules

    # The detector first: `from hexis.model import blocks` names the module in the alias,
    # not in `node.module`, so reading `node.module` alone would miss the import it forbids.
    assert any('blocks' in module for module in imported('from hexis.model import blocks'))
    for name in ('run_descriptive.py', 'run_report.py', 'scientific_run.py'):
        modules = imported((ROOT / 'src/hexis/pipeline' / name).read_text(encoding='utf-8'))
        assert not any('lexicon' in module or 'blocks' in module for module in modules), name


# --- the entry points as the plan publishes them ------------------------------

def test_the_documented_command_lines_run_the_whole_toy_campaign(tmp_path):
    config, corpus, output = campaign(tmp_path)
    common = ['--config', str(config), '--corpus-dir', str(corpus), '--output-dir', str(output),
              '--fixture']
    for argv in ([sys.executable, '-m', 'hexis.pipeline.run_descriptive', *common, '--cell', 'all'],
                 [sys.executable, '-m', 'hexis.pipeline.run_report', *common]):
        done = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
        assert done.returncode == 0, done.stderr
    manifest = scientific_run.validate_run(output)
    assert manifest['completed_stages'] == ['descriptive', 'report']
    assert set(TABLES) <= set(manifest['artifacts'])
