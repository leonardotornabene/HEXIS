"""Audit sintetico: nessun accesso a dati reali e nessuna modifica agli allegati."""
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from verify_synthetic import generate
from ctw import CTW

rows = []
for kind, m in [('iid', 4), ('cycle', 3), ('order1', 2), ('lag2', 2), ('variable', 2)]:
    for seed in range(5):
        training, _ = generate(kind, 53304, seed, m)
        evaluation, target = generate(kind, 100000, 10000 + seed, m)
        model = CTW(m).fit([training])
        before = model.fingerprint()
        score = model.evaluate([evaluation])
        assert before == model.fingerprint()
        tolerance = .02 if kind in ('iid', 'cycle') else .03
        error = abs(score['ce'] - target)
        assert (error < tolerance if kind == 'cycle' else error <= tolerance), (kind, seed, score, target)
        rows.append({'kind': kind, 'm': m, 'seed': seed, 'ce': score['ce'],
                     'target': target, 'tolerance': tolerance})
    print(kind, 'PASS', flush=True)
path = Path(sys.argv[2])
with path.open('x') as f:
    json.dump({'status': 'PASS', 'cases': rows}, f, indent=2)
