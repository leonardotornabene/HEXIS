"""Evidence execution and preservation; isolated pytest projects and toy fits only."""
import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from hexis.pipeline import corpus_run, run_descriptive, run_report, run_tree_validation, scientific_run
from test_v31_descriptive import campaign, describe, cell, report

pytestmark = pytest.mark.v31
ROOT = Path(__file__).resolve().parents[1]


def test_acceptance_checks_actual_junit_collection_and_process(tmp_path, monkeypatch):
    from hexis.pipeline import validation_run
    (tmp_path/'test_small.py').write_text('import pytest\npytestmark=pytest.mark.v31\ndef test_one(): assert 1 == 1\n')
    (tmp_path/'pyproject.toml').write_text('[tool.pytest.ini_options]\nmarkers=["v31: test"]\nenable_assertion_pass_hook=true\n')
    (tmp_path/'conftest.py').write_bytes((ROOT/'conftest.py').read_bytes())
    monkeypatch.setattr(validation_run, 'ROOT', tmp_path)
    process, xml = validation_run.run_acceptance(tmp_path)
    assert validation_run.check_acceptance(process, xml) == 1
    broken = copy.deepcopy(process)
    broken['execution']['returncode'] = 1  # JUnit can pass while the assert hook fails.
    with pytest.raises(ValueError) as error:
        validation_run.check_acceptance(broken, xml)
    assert str(error.value)
    broken = copy.deepcopy(process)
    broken['collection']['nodeids'].append('test_small.py::test_absent')
    with pytest.raises(ValueError) as error:
        validation_run.check_acceptance(broken, xml)
    assert str(error.value)


@pytest.mark.parametrize('body', ['pass', 'pytest.skip("pending")', 'assert False'])
def test_acceptance_rejects_vacuity_skip_and_failure(tmp_path, monkeypatch, body):
    from hexis.pipeline import validation_run
    (tmp_path/'test_small.py').write_text('import pytest\npytestmark=pytest.mark.v31\ndef test_one(): '+body+'\n')
    (tmp_path/'pyproject.toml').write_text('[tool.pytest.ini_options]\nmarkers=["v31: test"]\nenable_assertion_pass_hook=true\n')
    (tmp_path/'conftest.py').write_bytes((ROOT/'conftest.py').read_bytes())
    monkeypatch.setattr(validation_run, 'ROOT', tmp_path)
    with pytest.raises(ValueError) as error:
        validation_run.run_acceptance(tmp_path)
    assert str(error.value)


def test_validation_cli_requires_both_directories_and_protects_raw(tmp_path):
    for args in (['--corpus-dir', str(tmp_path)], ['--output-dir', str(tmp_path)]):
        with pytest.raises(SystemExit) as error:
            run_tree_validation.main(args)
        assert error.value.code != 0
    alias = tmp_path/'raw'
    alias.symlink_to(ROOT/'data/raw', target_is_directory=True)
    with pytest.raises(ValueError, match='raw') as error:
        run_tree_validation.main(['--config', str(ROOT/'config/default.yaml'), '--corpus-dir',
                                   str(tmp_path/'missing'), '--output-dir', str(alias/'forbidden')])
    assert str(error.value)


def test_new_schema_refuses_old_run_without_rewriting_it(tmp_path):
    config, corpus, output = campaign(tmp_path)
    manifest = describe(config, corpus, output)
    assert manifest['schema_version'] == 'hexis-scientific-manifest-2'
    manifest['schema_version'] = 'hexis-scientific-manifest-1'
    corpus_run.write_artifact(output/'manifest.json', manifest)
    before = (output/'manifest.json').read_bytes()
    with pytest.raises(ValueError, match='schema') as error:
        describe(config, corpus, output, '--resume')
    assert str(error.value)
    assert (output/'manifest.json').read_bytes() == before


def test_seed_zero_technical_keys_are_distinct_from_campaign_keys():
    from hexis.config import load_v31_config
    from hexis.pipeline import validation_run
    cfg = load_v31_config(ROOT/'config/default.yaml')
    technical = validation_run.technical_keys(cfg)
    full = run_report.expected_keys(cfg)
    assert len(technical['pair']) == 42 and len(technical['model']) == 84
    assert len(full['pair']) == 490 and len(full['model']) == 980
    assert {key[2] for key in technical['pair']} == {0}
    with pytest.raises(ValueError, match='key') as error:
        run_report.check_keys(cfg, technical)
    assert str(error.value)


@pytest.fixture(scope='module')
def executed_validation(tmp_path_factory):
    """Real battery and real pytest output from a tiny project, never scientific evidence."""
    from hexis.pipeline import validation_run
    directory = tmp_path_factory.mktemp('evidence-source')
    (directory/'test_one.py').write_text('import pytest\npytestmark=pytest.mark.v31\ndef test_one(): assert True\n')
    (directory/'pyproject.toml').write_text('[tool.pytest.ini_options]\nmarkers=["v31: fixture"]\nenable_assertion_pass_hook=true\n')
    (directory/'conftest.py').write_bytes((ROOT/'conftest.py').read_bytes())
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(validation_run, 'ROOT', directory)
        process, xml = validation_run.run_acceptance(directory)
    return run_tree_validation.run_battery(), process, xml


def validation_fixture(monkeypatch, executed_validation):
    from hexis.pipeline import validation_run
    rows, process, xml = executed_validation
    monkeypatch.setattr(run_tree_validation, 'run_battery', lambda: copy.deepcopy(rows))
    monkeypatch.setattr(validation_run, 'run_acceptance', lambda directory: (copy.deepcopy(process), xml))
    return validation_run


def test_validation_evidence_survives_descriptive_progress_and_resume(tmp_path, monkeypatch, executed_validation):
    validation = validation_fixture(monkeypatch, executed_validation)
    config, corpus, output = campaign(tmp_path)
    first = validation.publish_validation(config, corpus, output, fixture=True)
    assert first['completed_stages'] == ['validation'] and not first['keys']['model']
    assert set(first['evidence']) == {'V0', 'V1', 'V2'}
    before = {name: (output/name).read_bytes() for name in first['artifacts']}
    second = describe(config, corpus, output, '--cell', 'C0')
    third = describe(config, corpus, output, '--resume')
    assert second['completed_stages'] == third['completed_stages'] == ['validation', 'descriptive']
    assert first['evidence']['V2'] == third['evidence']['V2']
    assert first['run_id'] == third['run_id']
    assert all((output/name).read_bytes() == value for name, value in before.items())


@pytest.mark.parametrize('during_report', [False, True])
def test_report_refuses_changed_v2_execution_context(tmp_path, monkeypatch, executed_validation,
                                                     during_report):
    validation = validation_fixture(monkeypatch, executed_validation)
    config, corpus, output = campaign(tmp_path)
    validation.publish_validation(config, corpus, output, fixture=True)
    describe(config, corpus, output)
    original_context = validation.context
    changed = not during_report

    if during_report:
        original_render = run_report.plots.render

        def render(*args, **kwargs):
            nonlocal changed
            figures = original_render(*args, **kwargs)
            changed = True
            return figures

        monkeypatch.setattr(run_report.plots, 'render', render)

    def changed_context(*args):
        current = original_context(*args)
        if changed:
            current['tests'] = {**current['tests'], 'tests/changed.py': '0' * 64}
        return current

    monkeypatch.setattr(validation, 'context', changed_context)
    expected = 'report execution context changed' if during_report else 'evidence V2 context'
    with pytest.raises(ValueError, match=expected):
        report(config, corpus, output)
    assert not (output/'contrasts.csv').exists()


@pytest.mark.parametrize('fault', ['missing', 'pass_only', 'context', 'junit', 'process'])
def test_invalid_validation_evidence_blocks_fits(tmp_path, monkeypatch, executed_validation, fault):
    validation = validation_fixture(monkeypatch, executed_validation)
    config, corpus, output = campaign(tmp_path)
    manifest = validation.publish_validation(config, corpus, output, fixture=True)
    if fault == 'missing': manifest['evidence'].pop('V2')
    elif fault == 'pass_only': manifest['evidence']['V2'] = {'status': 'PASS'}
    elif fault == 'context': manifest['evidence']['V2']['context']['tests'] = {}
    else:
        name = validation.JUNIT if fault == 'junit' else validation.PROCESS
        if fault == 'junit': (output/name).write_bytes(b'<testsuites/>')
        else:
            payload = json.loads((output/name).read_text())
            payload['execution']['returncode'] = 1
            corpus_run.write_artifact(output/name, payload)
        manifest['artifacts'][name] = scientific_run.artifact_record(output/name)
        manifest['evidence']['V2']['artifacts'][name] = manifest['artifacts'][name]['sha256']
    corpus_run.write_artifact(output/'manifest.json', manifest)
    monkeypatch.setattr(run_descriptive, 'run_pair', lambda *a, **k: pytest.fail('invalid evidence reached fitting'))
    with pytest.raises(ValueError) as error:
        describe(config, corpus, output)
    assert str(error.value)


def test_validation_refuses_changed_execution_context_without_publication(tmp_path, monkeypatch, executed_validation):
    validation = validation_fixture(monkeypatch, executed_validation)
    config, corpus, output = campaign(tmp_path)
    _, process, xml = executed_validation
    def drift(directory):
        config.write_text(config.read_text()+'\n# changed during acceptance\n')
        return process, xml
    monkeypatch.setattr(validation, 'run_acceptance', drift)
    with pytest.raises(ValueError, match='context') as error:
        validation.publish_validation(config, corpus, output, fixture=True)
    assert str(error.value) and not output.exists()


def test_technical_completion_is_fixture_only_and_requires_the_exact_seed_zero_set(tmp_path):
    from hexis.pipeline import validation_run
    config, corpus, output = campaign(tmp_path, cells=[cell('C0', q=12, seeds=(0, 1)), cell('tiny', q=6, seeds=(0, 1))])
    cfg = yaml.safe_load(config.read_text())
    manifest = describe(config, corpus, output, '--seed', '0')
    frames = scientific_run.load_corpus(corpus)[1]
    result = validation_run.check_technical(output, manifest, cfg, frames, scientific=False)
    assert result['scientific'] is False and result['pair_count'] == 4 and result['model_count'] == 8
    assert 'V3' not in manifest['evidence']
    malformed = copy.deepcopy(manifest)
    malformed['keys']['pair'].pop()
    with pytest.raises(ValueError) as error:
        validation_run.check_technical(output, malformed, cfg, frames, scientific=False)
    assert str(error.value)

    with pytest.raises(ValueError) as error:
        validation_run.check_technical(output, manifest, cfg, frames, scientific=True)
    assert str(error.value)


def test_seed_zero_single_cell_keeps_v3_pending(tmp_path, monkeypatch, executed_validation):
    validation = validation_fixture(monkeypatch, executed_validation)
    config, corpus, output = campaign(tmp_path)
    validation.publish_validation(config, corpus, output, fixture=True)
    cfg = yaml.safe_load(config.read_text())
    monkeypatch.setattr(scientific_run, 'load_projection', lambda path, fixture: (cfg, True))
    monkeypatch.setattr(scientific_run, 'require_clean_producers', lambda: None)
    manifest = describe(config, corpus, output, '--cell', 'C0', '--seed', '0')
    assert len(manifest['keys']['pair']) == 2
    assert 'V3' not in manifest['evidence']
    assert manifest['completed_stages'] == ['validation', 'descriptive']


def test_real_fit_requires_clean_tracked_producers(tmp_path, monkeypatch):
    source = tmp_path/'src/hexis/core.py'
    source.parent.mkdir(parents=True)
    source.write_text('value = 1\n')
    def git(*args):
        return subprocess.run(['git', *args], cwd=tmp_path, capture_output=True, text=True, check=True)
    git('init')
    git('add', 'src')
    git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-m', 'fixture')
    monkeypatch.setattr(scientific_run, 'ROOT', tmp_path)
    scientific_run.require_clean_producers()
    assert source.read_text() == 'value = 1\n'
    (source.parent/'untracked.py').write_text('value = 2\n')
    with pytest.raises(ValueError, match='untracked') as error:
        scientific_run.require_clean_producers()
    assert str(error.value)
    (source.parent/'untracked.py').unlink()
    source.write_text('value = 3\n')
    with pytest.raises(ValueError, match='clean') as error:
        scientific_run.require_clean_producers()
    assert str(error.value)


@pytest.mark.parametrize('fault', [None, 'handwritten', 'artifact'])
def test_recorded_v3_evidence_is_recomputed_never_trusted(tmp_path, monkeypatch, executed_validation, fault):
    validation = validation_fixture(monkeypatch, executed_validation)
    config, corpus, output = campaign(tmp_path, cells=[cell('C0', q=12, seeds=(0, 1)),
                                                       cell('tiny', q=6, seeds=(0, 1))])
    validation.publish_validation(config, corpus, output, fixture=True)
    manifest = describe(config, corpus, output, '--seed', '0')
    cfg, frames = yaml.safe_load(config.read_text()), scientific_run.load_corpus(corpus)[1]
    record = validation.check_technical(output, manifest, cfg, frames, scientific=False)
    if fault == 'handwritten':  # code and lock right, no proof: the probe of the review
        record = {'code': record['code'], 'lock': record['lock'], 'status': 'PASS'}
    elif fault == 'artifact':
        record['artifacts'][sorted(record['artifacts'])[0]] = '0' * 64
    manifest['evidence']['V3'] = record
    corpus_run.write_artifact(output/'manifest.json', manifest)
    if fault is None:
        assert describe(config, corpus, output, '--resume')['evidence']['V3'] == record
        assert report(config, corpus, output)['checks']['scientific'] is False
        return
    monkeypatch.setattr(run_descriptive, 'run_pair', lambda *a, **k: pytest.fail('untrusted V3 reached fitting'))
    for stage, argv in ((describe, ['--resume']), (report, [])):
        with pytest.raises(ValueError, match='evidence V3') as error:
            stage(config, corpus, output, *argv)
        assert str(error.value)
    assert not (output/'contrasts.csv').exists()
