"""Scientific run identity, atomic publication and resume (piano §11.3, §11.7, §14).

The V1 corpus stages publish under `hexis-corpus-manifest-1`, whose completeness
flags describe an audit/encode pair. A descriptive campaign is identified by
cells, folds, seeds and arms instead, so it carries its own schema, its own key
lists and its own checks — and `corpus_run` stays closed, exactly as V1 attested
it. What is format-agnostic there (writing an artifact, recording what came back,
the hardened JSON reader, the destination guard) is imported unchanged: one
implementation of the bytes, two stage vocabularies.

Timestamps, machines, paths and resources are external metadata (§11.3): they
stay out of `run_contract`, so two runs of the same contract on two machines
produce the same `run_id` and byte-identical partitions.
"""

import datetime
import io
import json
import math
import os
import platform
import resource
import subprocess
import tempfile
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa

from hexis.config import load_v31_config, load_yaml
from hexis.contracts import ROOT, compare, digest, load_contracts
from hexis.manifest import sha256_file, _package_versions
from hexis.pipeline import corpus_run
from hexis.pipeline.corpus_run import (_code_identity, _read_json, artifact_record,
                                       check_destination, write_artifact)
from hexis.protocols import sampling

SCHEMA = 'hexis-scientific-manifest-1'
STAGES = ('descriptive', 'report')
CONTRACT_FIELDS = ('spec_version', 'representation_version', 'analytical_contracts', 'source_commit',
                   'plan', 'code', 'data', 'registry', 'alphabets', 'configuration', 'lock',
                   'rng_version')
MANIFEST_FIELDS = {'schema_version': str, 'run_id': str, 'run_contract': dict,
                   'completed_stages': list, 'keys': dict, 'artifacts': dict, 'evidence': dict,
                   'checks': dict, 'metadata': dict}
KEY_WIDTH = {'pair': 3, 'model': 4}  # §11.3: (cell, held_block_key, seed[, arm])
PROJECTION_FIELDS = ('spec_version', 'representation', 'min_available_past', 'rng', 'cells',
                     'blocks', 'registry', 'R1')
EVIDENCE_STEPS = ('V0', 'V1')  # what this run verifies for itself; V2–V3 are added by their stages


# --- the analytical projection -------------------------------------------------

def load_projection(path, fixture: bool):
    """The configuration this run reads, and whether it is the deposited projection.

    A synthetic campaign must never be readable as a result and the deposited
    contract must never be run as a fixture, so the declaration is explicit in
    both directions (§14.2 step 1).
    """
    path = Path(path)
    cfg = load_yaml(path)
    try:
        load_v31_config(path)
        deposited = True
    except ValueError as exc:
        if not fixture:
            raise ValueError(f'{path}: this configuration is not the deposited analytical '
                             f'projection; declare --fixture for a synthetic run — {exc}') from exc
        deposited = False
    if deposited and fixture:
        raise ValueError(f'{path}: --fixture refuses the deposited analytical projection; a '
                         'fixture must not impersonate the scientific configuration')
    missing = [field for field in PROJECTION_FIELDS if field not in cfg]
    if missing:
        raise ValueError(f'{path}: the analytical projection is missing {missing}')
    return cfg, deposited


def blocks_of(cfg) -> dict:
    """Block name -> canonical_doc_id members, the only block identity the sampler reads."""
    return {block['block']: list(block['docs']) for block in cfg['blocks']}


def block_keys_of(cfg) -> dict:
    """Block name -> §5.3 key, recomputed from the members rather than trusted."""
    keys = {}
    for block in cfg['blocks']:
        key = sampling.block_key(block['docs'])
        if 'block_key' in block and block['block_key'] != key:
            raise ValueError(f"block {block['block']}: declared key {block['block_key']!r} is not "
                             f'the key of its members')
        keys[block['block']] = key
    return keys


def groups_of(cfg) -> dict:
    """Block name -> report group; the one label the descriptive core never reads (§11.1)."""
    return {block['block']: block['group'] for block in cfg['blocks']}


def alphabet_sizes(cfg) -> dict:
    """Variant -> m, declared by the cells that fit it (§11.5, R1 needs one per variant)."""
    sizes = {}
    for cell in cfg['cells']:
        m = int(cell['m'])
        if sizes.setdefault(cell['variant'], m) != m:
            raise ValueError(f"variant {cell['variant']!r}: cells declare different alphabet sizes")
    return sizes


def select_cells(cfg, selection) -> list:
    """`all` or one declared cell (§14.1); an unknown name stops the run before any write."""
    declared = [cell['id'] for cell in cfg['cells']]
    if len(set(declared)) != len(declared):
        raise ValueError(f'cells: duplicate id(s) in {declared}')
    if any(not isinstance(name, str) or not name or '__' in name for name in declared):
        raise ValueError(f'cells: {declared} — an id is a nonempty name without "__"')
    if selection == 'all':
        return list(cfg['cells'])
    chosen = [cell for cell in cfg['cells'] if cell['id'] == selection]
    if not chosen:
        raise ValueError(f'unknown cell {selection!r}: this configuration declares {declared}')
    return chosen


# --- run identity --------------------------------------------------------------

def run_contract(cfg, corpus) -> dict:
    """§11.3: the corpus identity this run reads, under this configuration and this code.

    Data, registry, alphabets, plan and lock are the published corpus run's own
    fields — changing the corpus changes them. The configuration and the code are
    this run's, so a changed cell or a changed source file is a different run_id
    and can never be resumed into an existing one.
    """
    contract = dict(corpus['run_contract'])
    for field, declared in (('spec_version', cfg['spec_version']),
                            ('representation_version', cfg['representation']['version']),
                            ('rng_version', cfg['rng']['version'])):
        if contract.get(field) != declared:
            raise ValueError(f'{field}: the configuration declares {declared!r} and the corpus was '
                             f'published under {contract.get(field)!r}')
    contract['configuration'] = digest(cfg)
    contract['code'] = _code_identity()
    if sorted(contract) != sorted(CONTRACT_FIELDS):
        raise ValueError(f'run_contract: unknown {sorted(set(contract) - set(CONTRACT_FIELDS))}, '
                         f'missing {sorted(set(CONTRACT_FIELDS) - set(contract))}')
    return contract


def load_corpus(corpus_dir):
    """Re-verify the published corpus and return its frames; this *is* the V1 evidence."""
    corpus_dir = Path(corpus_dir)
    manifest = corpus_run.validate_run(corpus_dir)
    if 'encode' not in manifest['completed_stages']:
        raise ValueError(f'{corpus_dir}: the corpus run stopped at {manifest["completed_stages"]}; '
                         'the descriptive stage needs published sequences and coordinates')
    frames = {name: pd.read_parquet(corpus_dir / name)
              for name in ('sequences.parquet', 'coordinates.parquet')}
    frames['documents.csv'] = pd.read_csv(corpus_dir / 'documents.csv')
    return manifest, frames


def evidence(contract, corpus_dir, corpus) -> dict:
    """§14.2 step 2: the V0/V1 checks this run performed, under its own code and lock.

    Each record names the bytes that were verified in this process — the contract
    bundle and the corpus manifest — never a hand-written PASS.
    """
    contracts = load_contracts()
    common = {'code': digest(contract['code']), 'lock': contract['lock']}
    return {'V0': {**common, 'plan': contracts['lock']['plan']['sha256'],
                   'contracts': digest(contracts['lock']['contracts'])},
            'V1': {**common, 'run_id': corpus['run_id'],
                   'stages': list(corpus['completed_stages']),
                   'manifest_sha256': sha256_file(Path(corpus_dir) / 'manifest.json')}}


# --- artifact names and key sets -----------------------------------------------

def pair_name(cell, block_key, seed) -> str:
    return f'pair__{cell}__{block_key}__s{seed}.json'


def positions_name(cell, block_key, seed) -> str:
    return f'positions__{cell}__{block_key}__s{seed}.parquet'


def key_sets(keys) -> dict:
    """Detect duplicates *before* turning the lists into sets (§14.2 step 3)."""
    if set(keys) != set(KEY_WIDTH):
        raise ValueError(f'keys: {sorted(keys)}, expected {sorted(KEY_WIDTH)}')
    table = {}
    for kind, width in KEY_WIDTH.items():
        rows = [tuple(key) for key in keys[kind]]
        repeated = sorted(key for key, count in Counter(rows).items() if count > 1)
        if repeated:
            raise ValueError(f'keys/{kind}: duplicate key(s) {repeated}; a list is not a set')
        malformed = sorted(key for key in rows if len(key) != width)
        if malformed:
            raise ValueError(f'keys/{kind}: {malformed} do not carry {width} fields')
        table[kind] = set(rows)
    orphan = sorted({key[:3] for key in table['model']} - table['pair'])
    if orphan:
        raise ValueError(f'keys/model: {orphan} name no published pair')
    unfitted = sorted(table['pair'] - {key[:3] for key in table['model']})
    if unfitted:
        raise ValueError(f'keys/pair: {unfitted} carry no model identity')
    return table


def union_keys(prior, keys) -> dict:
    """A resume extends the published key set and never drops part of it (§11.7)."""
    merged = {}
    for kind in KEY_WIDTH:
        rows = {tuple(key) for key in keys[kind]}
        rows |= {tuple(key) for key in prior['keys'][kind]} if prior else set()
        merged[kind] = [list(key) for key in sorted(rows)]
    return merged


# --- reading, writing and publishing -------------------------------------------

def plain(value):
    """Plain JSON: a numpy scalar becomes Python and a non-finite float becomes null."""
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, dict):
        return {str(key): plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def records(frame) -> list:
    """The rows of a frame as plain JSON, in the frame's own order."""
    return [plain(row) for row in frame.to_dict('records')]


def _verify_roundtrip(path, value):
    """§11.7: every temporary is read back before anything is published."""
    if path.suffix == '.parquet':
        pd.testing.assert_frame_equal(pd.read_parquet(path), value.reset_index(drop=True),
                                      check_dtype=False, check_categorical=False)
    elif path.suffix == '.json':
        compare(json.loads(path.read_bytes()), value, f'roundtrip/{path.name}')
    elif path.suffix == '.csv':
        written = pd.read_csv(path).to_csv(index=False)
        if written != pd.read_csv(io.StringIO(value.to_csv(index=False))).to_csv(index=False):
            raise ValueError(f'{path.name}: CSV round-trip mismatch')


def validate_run(output, *, locked=False) -> dict:
    """§11.7: one manifest, the exact artifacts, verified bytes, schema and cardinality."""
    output = Path(output)
    try:
        manifest = _read_json(output / 'manifest.json')
        if set(manifest) != set(MANIFEST_FIELDS):
            raise ValueError(f'manifest: unknown field(s) {sorted(set(manifest) - set(MANIFEST_FIELDS))}, '
                             f'missing {sorted(set(MANIFEST_FIELDS) - set(manifest))}')
        if any(type(manifest[name]) is not kind for name, kind in MANIFEST_FIELDS.items()):
            raise ValueError('manifest: incorrect field types')
        if manifest['schema_version'] != SCHEMA:
            raise ValueError(f'manifest: schema {manifest["schema_version"]!r}, expected {SCHEMA!r}')
        if sorted(manifest['run_contract']) != sorted(CONTRACT_FIELDS):
            raise ValueError('manifest: run_contract does not carry exactly the §11.3 fields')
        if manifest['run_id'] != digest(manifest['run_contract']):
            raise ValueError('manifest: run identity does not match its own run_contract')
        stages = manifest['completed_stages']
        if not stages or stages != list(STAGES[:len(stages)]):
            raise ValueError(f'manifest: {stages} is not an ordered prefix of {list(STAGES)}')
        keys = key_sets(manifest['keys'])
        expected = {pair_name(*key) for key in keys['pair']}
        listed = {name for name in manifest['artifacts'] if name.startswith('pair__')}
        if listed != expected:
            raise ValueError(f'manifest: pair artifacts {sorted(listed ^ expected)} do not match '
                             'the published pair keys')
        stray = ({name for name in manifest['artifacts'] if name.startswith('positions__')}
                 - {positions_name(*key) for key in keys['pair']})
        if stray:
            raise ValueError(f'manifest: positional artifacts {sorted(stray)} name no pair key')
        names = set(manifest['artifacts']) | {'manifest.json'} | ({'.lock'} if locked else set())
        present = {path.name for path in output.iterdir()}
        if present != names:
            raise ValueError(f'{output}: extra {sorted(present - names)}, missing '
                             f'{sorted(names - present)} — an interrupted or hand-edited run is '
                             'never a completed stage and is never reused')
        for name, record in manifest['artifacts'].items():
            if Path(name).name != name or (output / name).is_symlink():
                raise ValueError(f'{name}: unsafe artifact name or symlink')
            compare(artifact_record(output / name), record, f'artifact/{name}')
        return manifest
    except (OSError, KeyError, TypeError, json.JSONDecodeError, pd.errors.ParserError,
            pa.ArrowException) as exc:
        raise ValueError(f'{output}: unreadable or corrupt run: {exc}') from exc


def read_prior(output):
    """The published run at this destination, fully validated, or None."""
    output = Path(output)
    return validate_run(output) if (output / 'manifest.json').exists() else None


def check_stage_open(output, stage, prior, resume: bool):
    """§11.7: a completed stage is immutable and the report closes the run."""
    if not prior:
        return
    stages = prior['completed_stages']
    if STAGES[-1] in stages:
        raise FileExistsError(f'{output}: the report stage is emitted and this run is closed; a '
                              'correction needs a new identity, not a second publication')
    if stage in stages and not resume:
        raise FileExistsError(f'{output}: {stage} already complete; outputs stay immutable unless '
                              '--resume extends the same identity')


def publish_stage(output, stage, artifacts, contract, body, *, resume=False, corpus_dir=None):
    """Reserve the destination, verify every temporary, link, replace the manifest last.

    Atomic hard-link publication refuses a collision even between the preflight
    and the publication; only the manifest is replaced, and it is replaced last,
    so a killed process leaves an invalid run and never a completed stage.
    """
    output = Path(output)
    check_destination(output, corpus_dir if corpus_dir is not None else ROOT / 'data/raw')
    if stage not in STAGES:
        raise ValueError(f'unknown stage {stage!r}: the scientific stages are {list(STAGES)}')
    if set(body) != {'keys', 'checks', 'evidence', 'metadata'}:
        raise ValueError(f'manifest body: {sorted(body)}, expected keys/checks/evidence/metadata')
    if any(Path(name).name != name or name in ('manifest.json', '.lock') for name in artifacts):
        raise ValueError('unsafe or reserved artifact name')
    output.parent.mkdir(parents=True, exist_ok=True)
    created = False
    try:
        output.mkdir()
        created = True
    except FileExistsError:
        pass
    lock = output / '.lock'
    with lock.open('x'):
        pass
    published = []
    try:
        prior = validate_run(output, locked=True) if not created else None
        stages = list(prior['completed_stages']) if prior else []
        if prior:
            compare(contract, prior['run_contract'], 'run_contract')
            check_stage_open(output, stage, prior, resume)
            dropped = {kind: sorted({tuple(key) for key in prior['keys'][kind]}
                                    - {tuple(key) for key in body['keys'][kind]})
                       for kind in KEY_WIDTH}
            if any(dropped.values()):
                raise ValueError(f'keys: this publication drops published key(s) {dropped}')
        if stage == STAGES[1] and STAGES[0] not in stages:
            raise ValueError(f'{output}: the report needs a published descriptive stage')
        old = dict(prior['artifacts']) if prior else {}
        artifact_records = dict(old)
        with tempfile.TemporaryDirectory(prefix='.stage-', dir=output) as tmp:
            tmp = Path(tmp)
            for name, value in artifacts.items():
                path = tmp / name
                write_artifact(path, value)
                artifact_records[name] = artifact_record(path)
                if name in old:
                    compare(artifact_records[name], old[name], f'existing/{name}')
                _verify_roundtrip(path, value)
            manifest = {'schema_version': SCHEMA, 'run_id': digest(contract),
                        'run_contract': contract,
                        'completed_stages': stages if stage in stages else [*stages, stage],
                        'keys': body['keys'], 'artifacts': artifact_records,
                        'evidence': body['evidence'],
                        'checks': {**(prior['checks'] if prior else {}), **body['checks']},
                        'metadata': {**(prior['metadata'] if prior else {}), **body['metadata']}}
            write_artifact(tmp / 'manifest.json', manifest)
            for name in artifacts:
                if name not in old:
                    os.link(tmp / name, output / name)
                    published.append(output / name)
            os.replace(tmp / 'manifest.json', output / 'manifest.json')
        return manifest
    except BaseException:
        for path in published:
            path.unlink(missing_ok=True)
        raise
    finally:
        lock.unlink(missing_ok=True)
        if created and not any(output.iterdir()):
            output.rmdir()


def stage_metadata(stage, *, corpus_dir, output_dir, started, **extra) -> dict:
    """External metadata (§11.3): never part of the identity, never inside an artifact."""
    def git(*argv):
        return subprocess.run(['git', *argv], cwd=ROOT, check=True, capture_output=True,
                              text=True).stdout.strip()
    return {stage: {'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    'machine': platform.platform(), 'python': platform.python_version(),
                    'package_versions': _package_versions(),
                    'corpus_dir': str(Path(corpus_dir).resolve()),
                    'output_dir': str(Path(output_dir).resolve()),
                    'implementation_commit': git('rev-parse', 'HEAD'),
                    'tracked_dirty': bool(git('status', '--porcelain', '--untracked-files=no')),
                    'resources': {'wall_seconds': time.perf_counter() - started,
                                  'ru_maxrss': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
                    **extra}}
