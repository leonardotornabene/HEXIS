"""V0–V2 execution evidence in the scientific manifest; no real model fits."""
import math
import os
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pandas as pd

from hormathos.contracts import ROOT, compare, digest
from hormathos.manifest import sha256_file
from hormathos.pipeline import scientific_run, run_tree_validation

BATTERY = 'tree_validation.json'
PROCESS = 'v31_process.json'
JUNIT = 'v31.junit.xml'
ARTIFACTS = {BATTERY, PROCESS, JUNIT}
REGENERATION_TOLERANCE = 1e-8  # §6.5 reproduction between platforms; identities, counts and keys exact


def context(config, corpus_dir, contract):
    """Read the effective code/tests/configuration/lock, including pytest's enforcement."""
    tests = sorted((ROOT/'tests').rglob('*.py')) + [ROOT/'conftest.py', ROOT/'pyproject.toml']
    return {'code': digest(scientific_run._code_identity()),
            'tests': {str(path.relative_to(ROOT)): sha256_file(path) for path in tests},
            'configuration': sha256_file(Path(config)), 'lock': sha256_file(ROOT/'uv.lock'),
            'run_contract': digest(contract),
            'corpus_manifest': sha256_file(Path(corpus_dir)/'manifest.json')}


def _junit_key(nodeid):
    path, *parts = nodeid.split('::')
    return ('.'.join([path.removesuffix('.py').replace('/', '.'), *parts[:-1]]), parts[-1])


def check_acceptance(process, xml):
    """JUnit proves cases/outcomes; process status also carries the executed-assert gate."""
    try:
        collection, execution = process['collection'], process['execution']
        if collection['returncode'] != 0 or execution['returncode'] != 0:
            raise ValueError('acceptance: pytest process failed')
        nodeids = collection['nodeids']
        if not nodeids or len(set(nodeids)) != len(nodeids):
            raise ValueError('acceptance: empty or duplicate collection')
        root = ET.fromstring(xml)
        suites = list(root.iter('testsuite'))
        cases = list(root.iter('testcase'))
        found = [(case.attrib['classname'], case.attrib['name']) for case in cases]
        if (not suites or len(found) != len(nodeids) or len(set(found)) != len(found)
                or set(found) != {_junit_key(node) for node in nodeids}
                or sum(int(suite.attrib['tests']) for suite in suites) != len(cases)):
            raise ValueError('acceptance: JUnit cases differ from actual collection')
        if any(list(root.iter(tag)) for tag in ('failure', 'error', 'skipped')):
            raise ValueError('acceptance: failure/error/skip in JUnit')
        if any(int(suite.attrib.get(field, '0')) != 0 for suite in suites
               for field in ('failures', 'errors', 'skipped')):
            raise ValueError('acceptance: nonzero JUnit failure counts')
        return len(cases)
    except (KeyError, TypeError, IndexError, ET.ParseError) as exc:
        raise ValueError(f'acceptance: malformed execution evidence: {exc}') from exc


def run_acceptance(directory):
    """Run the entire active selection with the same interpreter, then read pytest's JUnit."""
    directory = Path(directory)
    env = dict(os.environ)
    env.pop('PYTEST_ADDOPTS', None)
    command = [sys.executable, '-m', 'pytest', '-m', 'v31', '-q', '--color=no']
    collect_command = [*command, '--collect-only']
    collected = subprocess.run(collect_command, cwd=ROOT, env=env, capture_output=True, text=True)
    nodeids = [line.strip() for line in collected.stdout.splitlines()
               if '.py::' in line and not line.startswith((' ', '=', '<'))]
    execute_command = [*command, f'--junitxml={directory/JUNIT}']
    executed = subprocess.run(execute_command, cwd=ROOT, env=env, capture_output=True, text=True)
    process = {'collection': {'command': collect_command, 'returncode': collected.returncode,
                              'nodeids': nodeids, 'stdout': collected.stdout, 'stderr': collected.stderr},
               'execution': {'command': execute_command, 'returncode': executed.returncode,
                             'stdout': executed.stdout, 'stderr': executed.stderr}}
    xml = (directory/JUNIT).read_bytes() if (directory/JUNIT).is_file() else b''
    check_acceptance(process, xml)
    return process, xml


def verify_evidence(output, manifest, *, current=None):
    """Verify referenced artifacts and their effective execution context, never a PASS field."""
    output = Path(output)
    evidence = manifest['evidence'].get('V2')
    if not isinstance(evidence, dict) or set(evidence) != {'code', 'lock', 'context', 'artifacts'}:
        raise ValueError('evidence V2: missing execution evidence')
    if set(evidence['artifacts']) != ARTIFACTS:
        raise ValueError('evidence V2: incomplete artifact references')
    for name, expected in evidence['artifacts'].items():
        if name not in manifest['artifacts'] or sha256_file(output/name) != expected:
            raise ValueError(f'evidence V2: missing or altered {name}')
    contract = manifest['run_contract']
    if (evidence['code'] != digest(contract['code']) or evidence['lock'] != contract['lock']
            or evidence['context']['code'] != evidence['code']
            or evidence['context']['lock'] != evidence['lock']
            or evidence['context']['run_contract'] != digest(contract)):
        raise ValueError('evidence V2: code/lock/contract context differs')
    if current is not None:
        compare(evidence['context'], current, 'evidence V2 context')
    battery = scientific_run._read_json(output/BATTERY)
    if set(battery) != {'rows'} or run_tree_validation.exit_code(battery['rows']) != 0:
        raise ValueError('evidence V2: incomplete or invalid synthetic battery')
    return check_acceptance(scientific_run._read_json(output/PROCESS), (output/JUNIT).read_bytes())


def publish_validation(config, corpus_dir, output, *, fixture=False):
    """Validate V1, execute battery and pytest, then atomically publish V0–V2 together."""
    started = time.perf_counter()
    output = Path(output)
    scientific_run.check_destination(output, corpus_dir)
    if output.exists():
        raise FileExistsError(f'{output}: validation requires a new destination')
    cfg, deposited = scientific_run.load_projection(config, fixture)
    corpus, _ = scientific_run.load_corpus(corpus_dir)
    contract = scientific_run.run_contract(cfg, corpus)
    before = context(config, corpus_dir, contract)
    rows = run_tree_validation.run_battery()
    if run_tree_validation.exit_code(rows):
        raise ValueError('V2 synthetic battery failed; no validation stage published')
    with tempfile.TemporaryDirectory(prefix='hormathos-v31-') as directory:
        process, xml = run_acceptance(directory)
    # Re-read source/corpus/configuration and lock before publishing any acceptance.
    latest_corpus, _ = scientific_run.load_corpus(corpus_dir)
    latest_cfg, _ = scientific_run.load_projection(config, fixture)
    latest_contract = scientific_run.run_contract(latest_cfg, latest_corpus)
    compare(before, context(config, corpus_dir, latest_contract), 'validation context changed')
    artifacts = {BATTERY: {'rows': rows}, PROCESS: process, JUNIT: xml}
    evidence = scientific_run.evidence(contract, corpus_dir, corpus)
    evidence['V2'] = {'code': before['code'], 'lock': before['lock'], 'context': before,
                      'artifacts': {}}
    # Hash exactly the representation the shared publisher will write.
    with tempfile.TemporaryDirectory(prefix='hormathos-evidence-') as directory:
        for name, value in artifacts.items():
            path = Path(directory)/name
            scientific_run.write_artifact(path, value)
            evidence['V2']['artifacts'][name] = sha256_file(path)
    body = {'keys': {'pair': [], 'model': []}, 'evidence': evidence,
            'checks': {'validation_cases': len(rows), 'acceptance_cases': check_acceptance(process, xml),
                       'scientific': False, 'deposited_configuration': deposited},
            'metadata': scientific_run.stage_metadata(
                'validation', corpus_dir=corpus_dir, output_dir=output, started=started,
                environment_artifacts=[PROCESS, JUNIT])}
    def unchanged():
        compare(before, context(config, corpus_dir, scientific_run.run_contract(
            scientific_run.load_projection(config, fixture)[0], scientific_run.load_corpus(corpus_dir)[0])),
                'validation context changed')
    manifest = scientific_run.publish_stage(output, 'validation', artifacts, contract, body,
                                            corpus_dir=corpus_dir, before_publish=unchanged)
    scientific_run.validate_run(output)
    return manifest


def technical_keys(cfg):
    """The predefined seed-zero integration set, distinct from full-campaign acceptance."""
    from hormathos.pipeline.run_report import expected_keys
    keys = expected_keys(cfg)
    return {kind: [list(key) for key in keys[kind] if key[2] == 0] for kind in ('pair', 'model')}


def check_technical(output, manifest, cfg, frames, *, scientific):
    """Verify seed zero without confusing 42/84 technical fits with the 490/980 campaign."""
    from hormathos.config import load_v31_config
    from hormathos.pipeline import run_report
    expected = scientific_run.key_sets(technical_keys(cfg))
    published = scientific_run.key_sets(manifest['keys'])
    complete = run_report.expected_keys(cfg)
    for kind in ('pair', 'model'):
        if ({key for key in published[kind] if key[2] == 0} != expected[kind]
                or not published[kind] <= set(complete[kind])):
            raise ValueError('technical key set is not the exact seed-zero integration set')
    if scientific:
        compare(cfg, load_v31_config(), 'V3 deposited configuration')
        if len(expected['pair']) != 42 or len(expected['model']) != 84:
            raise ValueError('V3 requires exactly 42 pairs / 84 models')
        if manifest['run_contract']['spec_version'] != 'HEXIS-3.1':
            raise ValueError('fixture cannot attest scientific V3')
        verify_evidence(output, manifest)
    run_report.validate_partitions(output, manifest, cfg, frames)
    names = set()
    for key in expected['pair']:
        name = scientific_run.pair_name(*key)
        record = scientific_run._read_json(Path(output)/name)
        names.update((name, record['sample_ledger']))
        if record['positions'] is not None:
            names.add(record['positions'])
    return {'code': digest(manifest['run_contract']['code']), 'lock': manifest['run_contract']['lock'],
            'scientific': scientific, 'pair_count': len(expected['pair']),
            'model_count': len(expected['model']), 'keys': technical_keys(cfg),
            'artifacts': {name: sha256_file(Path(output)/name) for name in sorted(names)}}


def verify_technical(output, manifest, cfg, frames, *, scientific):
    """§14.2 step 2: a recorded V3 is recomputed from the published run, never trusted."""
    if 'V3' not in manifest['evidence']:
        raise ValueError('evidence V3: the seed-zero integration is not recorded')
    compare(manifest['evidence']['V3'],
            check_technical(output, manifest, cfg, frames, scientific=scientific), 'evidence V3')


def _same(left, right, where):
    """Exact on every identity, count, key and string; floats within the §6.5 tolerance."""
    if type(left) is not type(right):
        raise ValueError(f'{where}: {type(left).__name__} regenerated as {type(right).__name__}')
    if isinstance(left, dict):
        if left.keys() != right.keys():
            raise ValueError(f'{where}: fields differ')
        for key in left:
            if key != 'fingerprint':  # hashes float bits: compared through the values it hashes
                _same(left[key], right[key], f'{where}.{key}')
    elif isinstance(left, list):
        if len(left) != len(right):
            raise ValueError(f'{where}: length differs')
        for index, (a, b) in enumerate(zip(left, right)):
            _same(a, b, f'{where}[{index}]')
    elif isinstance(left, float):
        if not math.isclose(left, right, rel_tol=REGENERATION_TOLERANCE, abs_tol=REGENERATION_TOLERANCE):
            raise ValueError(f'{where}: {left!r} regenerated as {right!r}')
    elif left != right:
        raise ValueError(f'{where}: {left!r} regenerated as {right!r}')


def _regenerated(original, regenerated) -> str:
    """One partition artifact: byte-identical, or equal within tolerance, or refused."""
    if original.read_bytes() == regenerated.read_bytes():
        return 'identical'
    if original.suffix == '.parquet':
        left, right = pd.read_parquet(original), pd.read_parquet(regenerated)
        if list(left.columns) != list(right.columns) or len(left) != len(right):
            raise ValueError(f'{original.name}: regenerated schema or cardinality differs')
        for column in left.columns:
            a, b = left[column].to_numpy(), right[column].to_numpy()
            if (not np.allclose(a, b, rtol=REGENERATION_TOLERANCE, atol=REGENERATION_TOLERANCE, equal_nan=True)
                    if pd.api.types.is_float_dtype(left[column]) else not (a == b).all()):
                raise ValueError(f'{original.name}.{column}: regenerated values differ')
    else:
        _same(scientific_run._read_json(original), scientific_run._read_json(regenerated), original.name)
    return 'within_tolerance'


def compare_regeneration(campaign, regenerated, cfg, frames) -> dict:
    """§12.2 (T27/T29): the seed-0 pairs regenerated in a distinct directory against the campaign.

    Both runs are validated whole and share the run identity; the regenerated keys are exactly
    the predefined seed-0 set. Every pair record, ledger and C0 positional partition is
    byte-identical to the campaign's, or equal within the §6.5 reproduction tolerance with every
    identity, count and key exact — a fingerprint hashes float bits, so it is then reported
    through the values it hashes rather than required. Nothing here fits a model.
    """
    from hormathos.pipeline import run_report
    campaign, regenerated = Path(campaign), Path(regenerated)
    if campaign.resolve() == regenerated.resolve():
        raise ValueError('regeneration requires a distinct directory')
    left, right = scientific_run.validate_run(campaign), scientific_run.validate_run(regenerated)
    if left['run_id'] != right['run_id']:
        raise ValueError('regeneration ran under another run identity')
    expected = scientific_run.key_sets(technical_keys(cfg))
    produced, published = scientific_run.key_sets(right['keys']), scientific_run.key_sets(left['keys'])
    for kind in ('pair', 'model'):
        if produced[kind] != expected[kind] or not expected[kind] <= published[kind]:
            raise ValueError(f'regeneration: {kind} keys are not the seed-0 set of the campaign')
    run_report.validate_partitions(regenerated, right, cfg, frames)
    artifacts = {}
    for key in sorted(expected['pair']):
        name = scientific_run.pair_name(*key)
        record = scientific_run._read_json(regenerated/name)
        for artifact in (name, record['sample_ledger'], *([record['positions']] if record['positions'] else [])):
            artifacts[artifact] = _regenerated(campaign/artifact, regenerated/artifact)
    return {'run_id': left['run_id'], 'pair_count': len(expected['pair']),
            'model_count': len(expected['model']), 'tolerance': REGENERATION_TOLERANCE,
            'artifacts': artifacts}
