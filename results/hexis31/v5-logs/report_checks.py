"""Read-only checks of the V5 report stage in a run directory; imports nothing from hormathos.

Usage: python report_checks.py RUN_DIR
"""
import collections, datetime as dt, hashlib, json, sys
from pathlib import Path

R = Path(sys.argv[1])
raw = (R/'manifest.json').read_bytes()
m = json.loads(raw)
print('manifest_sha256', hashlib.sha256(raw).hexdigest())
print('run_id', m['run_id'], 'stages', m['completed_stages'], 'evidence', sorted(m['evidence']))
rep = m['metadata']['report']
print('report implementation_commit', rep['implementation_commit'], 'tracked_dirty', rep['tracked_dirty'],
      'created_utc', rep['created_utc'], 'wall_seconds', rep['resources']['wall_seconds'])
c = m['checks']
for k in sorted(c):
    if k != 'regeneration':
        print(' ', k, json.dumps(c[k]))
print('regeneration', {k: v for k, v in c['regeneration'].items() if k != 'artifacts'},
      dict(collections.Counter(c['regeneration']['artifacts'].values())))
bad = [n for n, r in m['artifacts'].items()
       if hashlib.sha256((R/n).read_bytes()).hexdigest() != (r['sha256'] if isinstance(r, dict) else r)]
print('artifacts in manifest', len(m['artifacts']), 'hash mismatches', len(bad))
print('files on disk == artifacts + manifest', {p.name for p in R.iterdir()} == set(m['artifacts']) | {'manifest.json'})
cut = dt.datetime(2026, 9, 25).timestamp()
new = sorted(p.name for p in R.iterdir() if p.stat().st_mtime > cut and p.name != 'manifest.json')
print('files modified on 2026-09-25 besides the manifest:', len(new))
for n in new:
    if n.endswith('.csv'):
        with open(R/n) as f:
            print(f'  {n:40s} rows {sum(1 for _ in f) - 1}')
    else:
        print(f'  {n:40s} bytes {(R/n).stat().st_size}')
