"""Regressions found by the audit before the V3 freeze."""

import os
import shutil

import pandas as pd
import pytest
import yaml

from hormathos.contracts import BUNDLE, ROOT, load_contracts
from hormathos.pipeline import corpus_run, scientific_run
from hormathos.pipeline import validation_run
from hormathos.protocols.sampling import sample_fold
from hormathos.viz.plots import _spread
from test_v31_descriptive import toy_corpus, toy_config, campaign, describe
from test_v31_corpus import mini, real_corpus

pytestmark = pytest.mark.v31


@pytest.mark.parametrize('committed', [False, True])
def test_manifest_commit_exception_preserves_the_published_state(tmp_path, monkeypatch, committed):
    output = tmp_path / 'run'
    artifact = {'new.json': {'value': 1}}
    publish = lambda: corpus_run.publish_stage(output, 'audit', artifact, {'fixture': 'v1'}, {})
    real_replace = os.replace

    def interrupted(source, target):
        if committed:
            real_replace(source, target)
        raise RuntimeError('injected manifest replacement failure')

    monkeypatch.setattr(os, 'replace', interrupted)
    with pytest.raises(RuntimeError, match='injected manifest'):
        publish()
    assert (output / 'manifest.json').exists() is committed
    assert (output / 'new.json').exists() is committed
    if committed:
        manifest = corpus_run.validate_run(output)
        assert manifest['artifacts']['new.json'] == corpus_run.artifact_record(output / 'new.json')


@pytest.mark.parametrize('committed', [False, True])
def test_scientific_manifest_commit_exception_keeps_a_valid_fixture_run(tmp_path, monkeypatch, committed):
    config, corpus, output = campaign(tmp_path)
    real_replace = os.replace

    def interrupted(source, target):
        if target == output/'manifest.json':
            if committed:
                real_replace(source, target)
            raise RuntimeError('injected manifest replacement failure')
        return real_replace(source, target)

    monkeypatch.setattr(os, 'replace', interrupted)
    with pytest.raises(RuntimeError, match='injected manifest'):
        describe(config, corpus, output, '--cell', 'C0')
    assert (output/'manifest.json').exists() is committed
    if committed:
        manifest = scientific_run.validate_run(output)
        assert manifest['completed_stages'] == ['descriptive']
        assert all((output/name).exists() for name in manifest['artifacts'])
    else:
        assert not list(output.glob('pair__*'))


def test_extra_ds_store_is_named_in_v1_and_deposit(tmp_path):
    output = tmp_path / 'run'
    corpus_run.publish_stage(output, 'audit', {'one.json': {}}, {'fixture': 'v1'}, {})
    (output / '.DS_Store').write_bytes(b'finder')
    with pytest.raises(ValueError, match=r'\.DS_Store') as error:
        corpus_run.validate_run(output)
    assert '.DS_Store' in str(error.value)
    deposit = tmp_path / 'deposit'
    shutil.copytree(BUNDLE, deposit)
    (deposit / '.DS_Store').write_bytes(b'finder')
    with pytest.raises(ValueError, match=r'\.DS_Store') as error:
        load_contracts(deposit)
    assert '.DS_Store' in str(error.value)


def test_spread_accepts_one_rounding_unit_only():
    from matplotlib.figure import Figure
    axis = Figure().subplots()
    _spread(axis, [0], pd.DataFrame({'min': [0.1], 'mean': [0.10000000000000002], 'max': [0.1]}))
    assert len(axis.lines) > 0
    with pytest.raises(ValueError, match='mean|range|inconsistent'):
        _spread(axis, [0], pd.DataFrame({'min': [0.1], 'mean': [0.2], 'max': [0.1]}))


def test_regeneration_tolerance_is_absolute_and_scales_only_loss_sums(tmp_path):
    validation_run._same({'value': 1.0}, {'value': 1.0 + 9e-9}, 'pair')
    with pytest.raises(ValueError, match='value'):
        validation_run._same({'value': 1.0}, {'value': 1.0 + 1.1e-8}, 'pair')
    validation_run._same({'n': 1000, 'sum_loss_ctw_original': 5.0},
                         {'n': 1000, 'sum_loss_ctw_original': 5.0 + 9e-6}, 'pair')
    with pytest.raises(ValueError, match='sum_loss') as error:
        validation_run._same({'n': 1000, 'sum_loss_ctw_original': 5.0},
                             {'n': 1000, 'sum_loss_ctw_original': 5.0 + 1.1e-5}, 'pair')
    assert 'sum_loss' in str(error.value)
    with pytest.raises(ValueError, match='value'):
        validation_run._same({'value': 1e8}, {'value': 1e8 + 0.1}, 'pair')
    first, second = tmp_path/'a.parquet', tmp_path/'b.parquet'
    pd.DataFrame({'loss_ctw_original': [1.0]}).to_parquet(first)
    pd.DataFrame({'loss_ctw_original': [1.0 + 9e-9]}).to_parquet(second)
    assert validation_run._regenerated(first, second) == 'within_tolerance'
    pd.DataFrame({'loss_ctw_original': [1e8]}).to_parquet(first)
    pd.DataFrame({'loss_ctw_original': [1e8 + 0.1]}).to_parquet(second)
    with pytest.raises(ValueError, match='loss_ctw_original'):
        validation_run._regenerated(first, second)


def test_regeneration_rejects_changed_integer_identity_in_parquet(tmp_path):
    original, regenerated = tmp_path/'original.parquet', tmp_path/'regenerated.parquet'
    pd.DataFrame({'slot_uid': [2**53 + 1]}).to_parquet(original)
    pd.DataFrame({'slot_uid': [float(2**53)]}).to_parquet(regenerated)
    with pytest.raises(ValueError, match='slot_uid') as error:
        validation_run._regenerated(original, regenerated)
    assert 'slot_uid' in str(error.value)


def test_raw_alias_is_rejected_even_when_case_differs(tmp_path):
    raw = tmp_path/'data'/'raw'
    raw.mkdir(parents=True)
    alias = tmp_path/'alias'
    alias.symlink_to(raw, target_is_directory=True)
    with pytest.raises(ValueError, match='raw'):
        corpus_run.check_output_locations([alias/'run'], data_root=raw)
    if (tmp_path/'data'/'RAW').exists():  # APFS case-insensitive volumes
        with pytest.raises(ValueError, match='raw'):
            corpus_run.check_output_locations([tmp_path/'data'/'RAW'/'run'], data_root=raw)
    assert True


def test_fixture_cannot_reuse_the_deposited_spec_version(tmp_path):
    config = tmp_path/'fixture.yaml'
    cfg = yaml.safe_load((ROOT/'config/default.yaml').read_text())
    cfg['cells'][0]['D'] = 99
    config.write_text(yaml.safe_dump(cfg))
    with pytest.raises(ValueError, match='spec_version|fixture') as error:
        scientific_run.load_projection(config, fixture=True)
    assert 'HEXIS-3.1' in str(error.value)
    corpus = corpus_run.validate_run(ROOT/'results/hexis31/v1')
    toy = yaml.safe_load(toy_config(tmp_path, name='toy.yaml').read_text())
    with pytest.raises(ValueError, match='spec_version'):
        scientific_run.run_contract(toy, corpus)


def test_sample_fold_rejects_a_document_in_two_blocks_before_training():
    sequences = pd.DataFrame({'variant': ['toy'], 'role': ['primary'], 'doc_id': ['held'],
                              'sent_id': ['held@1'], 'part_order': [0], 'source_ordinal': [1],
                              'encoded_length': [5], 'symbols': [[0]*5], 'slot_uids': [[0,1,2,3,4]]})
    with pytest.raises(ValueError, match='held|multiple|duplicate') as error:
        sample_fold(sequences, variant='toy', blocks={'A': ['held'], 'B': ['held']},
                    held_block='A', q=1, seed=0)
    assert 'multiple blocks' in str(error.value)


def test_load_corpus_reads_the_validated_private_copy(tmp_path, monkeypatch):
    corpus = toy_corpus(tmp_path)
    original = corpus/'sequences.parquet'
    expected = pd.read_parquet(original)
    real_validate = corpus_run.validate_run
    saved = original.read_bytes()

    def changed_after_validation(path, **kwargs):
        manifest = real_validate(path, **kwargs)
        modified = expected.copy()
        modified.at[0, 'symbols'] = [9] * len(modified.at[0, 'symbols'])
        modified.to_parquet(original, index=False)
        return manifest

    monkeypatch.setattr(corpus_run, 'validate_run', changed_after_validation)
    try:
        _, frames = scientific_run.load_corpus(corpus)
    finally:
        original.write_bytes(saved)
    pd.testing.assert_frame_equal(frames['sequences.parquet'], expected)
    assert list(frames['sequences.parquet'].iloc[0]['symbols']) == list(expected.iloc[0]['symbols'])


def test_category_order_cannot_hide_swapped_document_order(real_corpus):
    from hormathos.corpus import verify_sequences
    artifacts = real_corpus.copy()
    sequences = real_corpus['sequences.parquet'].copy()
    docs = list(dict.fromkeys(sequences['doc_id'].astype(str)))
    categories = [docs[1], docs[0], *docs[2:]]
    sequences['doc_id'] = pd.Categorical(sequences['doc_id'].astype(str), categories=categories,
                                          ordered=True)
    sequences = sequences.sort_values(['variant', 'doc_id', 'part_order', 'source_ordinal',
                                       'sent_id']).reset_index(drop=True)
    artifacts['sequences.parquet'] = sequences
    with pytest.raises(ValueError, match='noncanonical sentence order') as error:
        verify_sequences(artifacts['coordinates.parquet'], sequences, load_contracts()['design'],
                         load_contracts()['alphabets'])
    assert 'noncanonical' in str(error.value)


def test_parser_consumes_the_copied_v1_input(tmp_path):
    from hormathos.corpus import read_corpus
    cfg, path, prefix = mini(tmp_path)
    with corpus_run.staged_inputs([path]) as (_, staged):
        saved = path.read_bytes()
        path.write_bytes(saved.replace(b'NOUN', b'VERB'))
        try:
            tokens, _ = read_corpus([path], cfg['registry'], staged=staged)
        finally:
            path.write_bytes(saved)
    assert 'NOUN' in set(tokens['upos_raw'])
    assert 'VERB' not in set(tokens['upos_raw'])


def test_descriptive_context_change_cannot_publish_a_pair(tmp_path, monkeypatch):
    from hormathos.pipeline import run_descriptive
    config, corpus, output = campaign(tmp_path)
    original = config.read_bytes()
    real_pair = run_descriptive.run_pair

    def changed_context(*args, **kwargs):
        result = real_pair(*args, **kwargs)
        modified = yaml.safe_load(original)
        modified['cells'][0]['q'] += 1
        config.write_text(yaml.safe_dump(modified))
        return result

    monkeypatch.setattr(run_descriptive, 'run_pair', changed_context)
    try:
        with pytest.raises(ValueError, match='context changed') as error:
            run_descriptive.main(['--config', str(config), '--corpus-dir', str(corpus),
                                  '--output-dir', str(output), '--fixture'])
    finally:
        config.write_bytes(original)
    assert 'context changed' in str(error.value)
    assert not list(output.glob('pair__*')) if output.exists() else True


@pytest.mark.parametrize('tag', ['skipped', 'failure'])
def test_acceptance_rejects_junit_failure_even_with_zero_process_status(tag):
    process = {'collection': {'returncode': 0, 'nodeids': ['test_one.py::test_one']},
               'execution': {'returncode': 0}}
    xml = (f'<testsuite tests="1" failures="0" skipped="0">'
           f'<testcase classname="test_one" name="test_one"><{tag}/></testcase></testsuite>').encode()
    with pytest.raises(ValueError, match='JUnit') as error:
        validation_run.check_acceptance(process, xml)
    assert tag in str(error.value) or 'JUnit' in str(error.value)
