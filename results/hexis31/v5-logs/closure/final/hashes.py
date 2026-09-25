"""Final closure check: only the nine planned documents changed; frozen perimeter,
manifests and every artifact hash unchanged. Read-only."""
import hashlib, json, subprocess
from pathlib import Path
root = Path.cwd()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
base = json.loads(Path('/tmp/hormathos-v5-baseline.json').read_text())
changed = sorted(p for p, h in base.items() if sha(root/p) != h)
planned = sorted(['AGENTS.md','CLAUDE.md','README.md','docs/00_INDEX.md','docs/01_MASTER_SPEC.md',
    'docs/03_ROADMAP.md','docs/04_AI_HANDOFF_PROMPT.md','docs/HANDOFF.md','docs/TEST_INVENTORY.md'])
assert changed == planned, changed
tracked = subprocess.run(['git','ls-files'], cwd=root, capture_output=True, text=True, check=True).stdout.split()
assert set(tracked) <= set(base), set(tracked) - set(base)
frozen = [p for p in base if p.startswith(('src/','tests/','config/')) or p in ('conftest.py','pyproject.toml','uv.lock')]
assert all(sha(root/p) == base[p] for p in frozen)
run = root/'results/hexis31/v3-seed0-v3006'
assert sha(run/'manifest.json') == '3243fc329351e45e1d1c2c2f68a5be57fec2ea197ef5a81a170a5c11f4ca6dab'
assert sha(root/'results/hexis31/v3-seed0-v3006-regeneration/manifest.json') == '72b6cdee3220cbea97ba0bfb969bd2f3b871f244e62a8f3da3182d6d84c3790a'
m = json.loads((run/'manifest.json').read_text())
arts = m['artifacts']
items = arts.items() if isinstance(arts, dict) else [(a['path'], a['sha256']) for a in arts]
n = 0
for name, digest in items:
    digest = digest if isinstance(digest, str) else digest['sha256']
    assert sha(run/name) == digest, name; n += 1
print(f'PASS: changed = the {len(planned)} planned documents; {len(frozen)} frozen files unchanged; '
      f'both manifests unchanged; {n} artifact hashes match; run_id {m.get("run_id","?")[:12]}')
