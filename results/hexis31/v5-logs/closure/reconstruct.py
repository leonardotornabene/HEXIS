"""Read-only reconstruction with the frozen report implementation; no fits."""
import json
from pathlib import Path
import pandas as pd
from hormathos.contracts import digest
from hormathos.pipeline import scientific_run as s, run_report as r
from hormathos.protocols import scores

p = Path('results/hexis31/v3-seed0-v3006')
out = Path('/tmp/hormathos-v5-review')
m = json.loads((p/'manifest.json').read_text())
cfg, _ = s.load_projection('config/default.yaml', False)
_, frames = s.load_corpus('results/hexis31/v1')
records = r.read_partitions(p, m)
docs = r.document_scores(records)
blocks = r.block_pairs(docs)
totals = blocks[blocks.past_band.eq('all')]
groups = s.groups_of(cfg)
contrasts = r.group_contrasts(totals, groups)
long = r.profiles(contrasts, blocks, docs)
pairs = r.sensitivity_pairs(long)
differences = pairs.assign(level=pairs.level + '_difference', value=pairs.difference)
tables = r.r1_tables(cfg, frames['coordinates.parquet'], frames['alphabets.json'])
tables.update({
    'document_scores.csv': scores.ce_gain_q(docs), 'block_pairs.csv': blocks,
    'aggregation_weights.csv': r.aggregation_weights(
        totals, r.training_quota(records), r.fold_training(records, groups), groups),
    'contrasts.csv': contrasts,
    'seed_summaries.csv': r.seed_summaries(pd.concat([long, differences[long.columns]], ignore_index=True)),
    'sensitivity_pairs.csv': pairs,
    'fragment_diagnostics.csv': r.fragment_diagnostics(records),
    'model_diagnostics.csv': r.model_diagnostics(records, {
        tuple(row['key']): row for row in m['metadata']['descriptive']['models']}),
    'arm_diagnostics.csv': r.arm_diagnostics(records),
})
figures = r.plots.render(tables, frames['documents.csv'],
    pd.read_csv('results/hexis31/v1/audit_contingency.csv'), digest(m['run_contract']),
    cells=[cell['id'] for cell in cfg['cells']])
assert set(tables) == set(r.TABLES)
assert len(tables) == 13 and len(figures) == 5
for name, value in {**tables, **figures}.items():
    s.write_artifact(out/name, value)
    assert (out/name).read_bytes() == (p/name).read_bytes(), name
    print('byte-identical', name)
print('PASS: 13 tables and 5 figures reconstructed byte for byte; no fits')
