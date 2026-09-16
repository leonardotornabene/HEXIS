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
