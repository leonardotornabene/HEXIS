"""V3-006 (d): a run on the new code against the V3-005 run on the old one.

The two runs carry different run identities, so compare_regeneration refuses them by design.
Here the 70 V3 artifacts (pairs, ledgers, C0 positions) must be byte-identical or equal within
the V3-004 tolerance (validation_run._regenerated); tree_validation.json is compared the same
way; the JUnit record and process record of V2 differ by construction (431 tests against 429)
and are only listed; the manifests must agree on keys and stages, and
their run contracts may differ only in the code identity, in exactly the files V3-006 changed.

Usage: uv run --no-sync python cross_check.py OLD NEW
"""
import sys
from collections import Counter
from pathlib import Path

from hormathos.pipeline import scientific_run as sr, validation_run as vr

CHANGED = {'src/hormathos/corpus.py', 'src/hormathos/protocols/scores.py',
           'src/hormathos/pipeline/run_report.py', 'src/hormathos/pipeline/corpus_run.py',
           'src/hormathos/pipeline/scientific_run.py'}

old, new = map(Path, sys.argv[1:3])
left, right = sr.validate_run(old), sr.validate_run(new)
assert set(left['artifacts']) == set(right['artifacts']), sorted(set(left['artifacts']) ^ set(right['artifacts']))
names = set(left['evidence']['V3']['artifacts']) | {'tree_validation.json'}
assert names == set(right['evidence']['V3']['artifacts']) | {'tree_validation.json'}
assert sr.key_sets(left['keys']) == sr.key_sets(right['keys']), 'keys differ'
assert left['completed_stages'] == right['completed_stages'], 'stages differ'
contract = [field for field in left['run_contract']
            if left['run_contract'][field] != right['run_contract'][field]]
assert contract == ['code'], contract
code_old, code_new = left['run_contract']['code'], right['run_contract']['code']
files = {path for path in code_old.keys() | code_new.keys() if code_old.get(path) != code_new.get(path)}
assert files == CHANGED, sorted(files ^ CHANGED)
outcomes = {name: vr._regenerated(old / name, new / name) for name in sorted(names)}
print('old run_id', left['run_id'])
print('new run_id', right['run_id'])
print('run_contract differs only in: code, files', sorted(files))
print('keys and stages equal:', right['completed_stages'],
      {kind: len(keys) for kind, keys in sr.key_sets(right['keys']).items()})
print('artifacts', len(names), dict(Counter(outcomes.values())),
      'not compared (V2 context):', sorted(set(left['artifacts']) - names))
for name, outcome in outcomes.items():
    if outcome != 'identical':
        print(' ', outcome, name)
