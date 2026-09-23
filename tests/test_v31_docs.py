"""V0 authority, preserved history and declared operational limits."""
import hashlib
import json
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.v31
ROOT = Path(__file__).resolve().parents[1]

# The three V3-001 blocks are the acts of 16, 17 and 22 September: V3-002 supersedes
# sentences of theirs, it never rewrites their bytes.
V3_001_SHA256 = 'df5ca735f4d9f0f450c147518d138e994a2818e0119e3fec95827c9e81760e6f'
LOCK_SHA256 = '33db43b00bcb21ab12aedf6dcc4257764770bff0115dc0d1dfab6e5ea89876bf'
REALIGNMENT_BASE = '5f1ec06afa192c8d0f006d7f39cdb97df72c2983'


def test_active_authority_and_instructions_are_aligned():
    for name in ['README.md', 'AGENTS.md', 'CLAUDE.md', 'docs/01_MASTER_SPEC.md',
                 'docs/02_DECISION_LOG.md', 'docs/03_ROADMAP_OPERATIVA_IT.md',
                 'docs/00_LEGGIMI_INDICE.md', 'docs/HANDOFF.md']:
        text = (ROOT/name).read_text()
        assert 'V3-001' in text and 'V3-002' in text, name
        assert '3.1' in text, name
    readme = (ROOT/'README.md').read_text()
    assert '**V0–V2 completed; V3–V5 not attested; no real fit has ever been run.**' in readme
    assert 'archive/' in readme
    assert 'Arresto per revisione prima di V3.' in (ROOT/'docs/HANDOFF.md').read_text()


def test_the_v3_001_acts_are_never_rewritten():
    log = (ROOT/'docs/02_DECISION_LOG.md').read_text()
    acts = log[:log.index('## V3-002 —')]
    assert hashlib.sha256(acts.encode()).hexdigest() == V3_001_SHA256
    assert 'V3-002 — Riallineamento della repository' in log


def test_the_deposit_and_the_lock_are_byte_preserved():
    record = json.loads((ROOT/'docs/V3-001-deposit.json').read_text())
    for name, sha in record['files'].items():
        assert hashlib.sha256((ROOT/record['root']/name).read_bytes()).hexdigest() == sha, name
    assert hashlib.sha256((ROOT/'uv.lock').read_bytes()).hexdigest() == LOCK_SHA256


def test_all_preserved_v21_documents_match_the_original_hash_inventory():
    history = ROOT/'archive/docs/history/v2.1'
    records = json.loads((history/'SHA256SUMS.json').read_text())
    assert len(records) == 10
    for name, record in records.items():
        assert hashlib.sha256((history/name).read_bytes()).hexdigest() == record['sha256'], name


def test_the_archive_is_a_record_and_never_a_dependency():
    """`archive/` keeps the history at its own paths; nothing active imports it and
    no archived test is collected (piano §13.1 p.4–5; V3-002)."""
    archive = ROOT/'archive'
    assert (archive/'README.md').is_file()
    for expected in ['src/hexis/stats/permutation.py', 'src/hexis/registry.py',
                     'src/hexis/pipeline/legacy_audit.py', 'tests/test_run_audit.py',
                     'docs/history/v2.1/02_DECISION_LOG.md', 'candidates/README.md']:
        assert (archive/expected).is_file(), expected
    assert not (ROOT/'src/hexis/stats').exists()


def test_every_archived_file_has_its_bytes_at_the_base():
    """Rule `archive/P` (V3-002): every archived file holds the bytes `P` had at the
    base, so nothing new can sit in the archive under a historical name."""
    def git(*argv, stdin=None):
        return subprocess.run(['git', *argv], cwd=ROOT, input=stdin, check=True,
                              capture_output=True, text=True).stdout
    base = {}
    for entry in git('ls-tree', '-r', '-z', REALIGNMENT_BASE).split('\0'):
        if entry:
            meta, path = entry.split('\t', 1)
            base[path] = meta.split()[2]
    archived = [path for path in git('ls-files', '-z', 'archive').split('\0') if path]
    blobs = git('hash-object', '--stdin-paths', stdin='\n'.join(archived)).split()
    assert archived and len(blobs) == len(archived)
    for path, blob in zip(archived, blobs):
        assert base.get(path.removeprefix('archive/')) == blob, path


def test_test_inventory_explicitly_tracks_future_obligations():
    text = (ROOT/'docs/TEST_INVENTORY.md').read_text()
    for index in range(1, 31):
        assert f'T{index:02d}' in text
    assert 'PENDING' in text
    assert 'inventory_only' in text
    assert 'test_bootstrap_holm.py' in text


def test_pipeline_does_not_import_candidates_or_inferential_utilities():
    import ast
    for path in (ROOT/'src/hexis').rglob('*.py'):
        tree = ast.parse(path.read_text())
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or '')
        assert not any(name.startswith(('candidates', 'archive', 'hexis.stats'))
                       for name in imports), path


def test_the_three_standing_instruction_copies_are_identical():
    """The template in 04 is the source; CLAUDE.md and AGENTS.md are its copies,
    and AGENTS.md may differ only in its first line."""
    template = (ROOT/'docs/04_AI_HANDOFF_PROMPT.md').read_text()
    fenced = template.partition('````markdown\n')[2].partition('\n````')[0] + '\n'
    claude = (ROOT/'CLAUDE.md').read_text()
    agents = (ROOT/'AGENTS.md').read_text()
    assert fenced == claude
    assert agents.splitlines(keepends=True)[1:] == claude.splitlines(keepends=True)[1:]
