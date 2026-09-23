"""Byte-identified HEXIS 3.1 contracts. Expected values are never regenerated."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUNDLE = ROOT / 'docs/contracts/hexis-3.1/HEXIS_allegati_v3.1_2026-09-15'
LOCK_SHA256 = '56525a959ebff5e02117dcc77e1bd20943ce9c9f2b386aa1803a91d172d851a0'
PROJECTION = (
    'spec_version', 'languages', 'scientific_scope', 'inference', 'representation',
    'min_available_past', 'past_bands', 'rng', 'cells', 'blocks', 'registry',
    'sampling', 'shuffle', 'model', 'R1', 'aggregation', 'expected', 'runtime',
    'validation', 'governance',
)


def canonical_json(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(canonical_json(value)).hexdigest()


def compare(actual, expected, path='contract'):
    """Compare every value and its type, including bool/int and int/float."""
    if type(actual) is not type(expected):
        raise ValueError(f'{path}: expected {type(expected).__name__}, got {type(actual).__name__}')
    if isinstance(actual, dict):
        if actual.keys() != expected.keys():
            raise ValueError(f'{path}: unknown keys {set(actual)-set(expected)}, missing keys {set(expected)-set(actual)}')
        for key in expected:
            compare(actual[key], expected[key], f'{path}.{key}')
    elif isinstance(actual, list):
        if len(actual) != len(expected):
            raise ValueError(f'{path}: length {len(actual)}, expected {len(expected)}')
        for index, (a, e) in enumerate(zip(actual, expected)):
            compare(a, e, f'{path}[{index}]')
    elif (isinstance(actual, float) and not math.isfinite(actual)) or actual != expected:
        raise ValueError(f'{path}: {actual!r}, expected {expected!r}')


def analytical_projection(design):
    return {key: design[key] for key in PROJECTION}


def validate_projection(cfg, design):
    compare(cfg, analytical_projection(design), 'config')


def load_contracts(root=None):
    root = Path(root) if root is not None else BUNDLE
    try:
        lock_bytes = (root / 'design_lock.json').read_bytes()
        if hashlib.sha256(lock_bytes).hexdigest() != LOCK_SHA256:
            raise ValueError(f'{root}/design_lock.json: digest mismatch')
        lock = json.loads(lock_bytes)
        sums = json.loads((root / 'SHA256SUMS.json').read_bytes())
        # The delivery has exactly these files; no unreviewed second contract.
        names = {Path(name).name for name in sums if not name.startswith('../')} | {'SHA256SUMS.json'}
        if {p.name for p in root.iterdir()} != names:
            raise ValueError(f'{root}: missing or extra contract files')
        for name, sha in {**sums, **lock['contracts'], lock['plan']['path']: lock['plan']['sha256']}.items():
            if hashlib.sha256((root / name).read_bytes()).hexdigest() != sha:
                raise ValueError(f'{root / name}: digest mismatch')
        files = {'design': 'hexis_v3.1_design.json', 'expected': 'corpus_atteso_v3.1.json',
                 'alphabets': 'alphabets_v3.1.json', 'report': 'report_contract_v3.1.json'}
        result = {key: json.loads((root / name).read_bytes()) for key, name in files.items()}
        result['lock'] = lock
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f'{root}: unreadable deposited contract: {exc}') from exc
    d, e, a, r = (result[key] for key in ('design', 'expected', 'alphabets', 'report'))
    compare(e['expected'], d['expected'], 'corpus.expected')
    compare(r['expected'], d['expected'], 'report.expected')
    compare(e['blocks'], d['blocks'], 'corpus.blocks')
    compare(e['source_hashes'], d['source_hashes'], 'corpus.source_hashes')
    compare(a['representation_version'], d['representation']['version'], 'alphabet.version')
    for variant, alphabet in a['alphabets'].items():
        compare(alphabet['m'], d['expected']['alphabet_sizes'][variant], f'{variant}.m')
        if alphabet['symbols'] != sorted(set(alphabet['symbols'])) or len(alphabet['symbols']) != alphabet['m']:
            raise ValueError(f'{variant}: invalid frozen alphabet')
    docs = {row['canonical_doc_id']: row for row in d['registry']}
    members = [doc for b in d['blocks'] for doc in b['docs']]
    if len(members) != len(set(members)) or set(members) != {doc for doc, row in docs.items() if row['role'] == 'primary'}:
        raise ValueError('registry: inconsistent block membership')
    for block in d['blocks']:
        compare(block['block_key'], digest(sorted(block['docs'])), 'block_key')
        for doc in block['docs']:
            compare(docs[doc]['dependence_block'], block['block'], f'registry.{doc}')
    return result
