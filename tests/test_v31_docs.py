"""V0 authority, preserved history and declared operational limits."""
import hashlib
import json
from pathlib import Path

import pytest

pytestmark = pytest.mark.v31
ROOT = Path(__file__).resolve().parents[1]


def test_active_authority_and_instructions_are_aligned():
    for name in ['README.md', 'AGENTS.md', 'CLAUDE.md', 'docs/01_MASTER_SPEC.md',
                 'docs/02_DECISION_LOG.md', 'docs/03_ROADMAP_OPERATIVA_IT.md',
                 'docs/00_LEGGIMI_INDICE.md', 'docs/HANDOFF.md']:
        text = (ROOT/name).read_text()
        assert 'V3-001' in text, name
        assert '3.1' in text, name
    assert (ROOT/'AGENTS.md').read_bytes() == (ROOT/'CLAUDE.md').read_bytes()
    assert 'V2–V5' in (ROOT/'README.md').read_text()


def test_history_and_deposit_are_byte_preserved():
    record = json.loads((ROOT/'docs/V3-001-deposit.json').read_text())
    for name, sha in record['files'].items():
        assert hashlib.sha256((ROOT/record['root']/name).read_bytes()).hexdigest() == sha, name
    old = (ROOT/'docs/history/v2.1/02_DECISION_LOG.md').read_bytes()
    assert (ROOT/'docs/02_DECISION_LOG.md').read_bytes().endswith(old)
    assert (ROOT/'uv.lock').read_bytes() == (ROOT/'docs/history/v2.1/uv.lock').read_bytes()


def test_test_inventory_explicitly_tracks_future_obligations():
    text = (ROOT/'docs/TEST_INVENTORY.md').read_text()
    for index in range(1,31):
        assert f'T{index:02d}' in text
    assert 'PENDING' in text
    assert 'inventory_only' in text
    assert 'test_bootstrap_holm.py' in text


def test_all_preserved_v21_documents_match_the_original_hash_inventory():
    history=ROOT/'docs/history/v2.1'
    records=json.loads((history/'SHA256SUMS.json').read_text())
    assert len(records)==10
    for name,record in records.items():
        assert hashlib.sha256((history/name).read_bytes()).hexdigest()==record['sha256'],name


def test_pipeline_does_not_import_candidates_or_inferential_utilities():
    import ast
    for path in (ROOT/'src/hexis/pipeline').glob('*.py'):
        tree=ast.parse(path.read_text())
        imports=[]
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):imports.extend(a.name for a in node.names)
            elif isinstance(node,ast.ImportFrom):imports.append(node.module or '')
        assert not any(name.startswith(('candidates','hexis.stats')) for name in imports),path
