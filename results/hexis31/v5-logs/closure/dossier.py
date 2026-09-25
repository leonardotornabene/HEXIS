"""Editorial selections only: no score or dispersion aggregation."""
import csv
import json
from pathlib import Path

ROOT = Path.cwd()
RUN = ROOT/'results/hexis31/v3-seed0-v3006'
OUT = Path('/tmp/hormathos-v5-review')
tables = {p.name: list(csv.DictReader(p.open())) for p in RUN.glob('*.csv')}
inventory = list(csv.DictReader((ROOT/'results/hexis31/v1/documents.csv').open()))
cells = ['C0', 'a_total1', 'q_half', 'D12', 'oth', 'upos']
blocks = ['HOMERIC_TRADITION', 'HESIODIC_TRADITION', 'HERODOTUS', 'THUCYDIDES', 'ATHENAEUS', 'DIODORUS', 'PLUTARCH']
metrics = ['ce_ctw_original', 'ce_root_original', 'ce_ctw_shuffled', 'ce_root_shuffled', 'g_original', 'g_shuffled', 'q']
metric_labels = ['CE_CTW O', 'CE_0 O', 'CE_CTW R', 'CE_0 R', 'G_O', 'G_R', 'Q']
weights = ['equal_block', 'eligible_token_weighted']
weight_labels = {'equal_block': 'Equal block', 'eligible_token_weighted': 'Eligible target'}
docrows = [r for r in inventory if r['variant'] == 'ud23' and r['role'] == 'primary']
docrows.sort(key=lambda r: (blocks.index(r['dependence_block']), r['doc_id']))
docs = [r['doc_id'] for r in docrows]
labels = {r['doc_id']: r['work'] + (' (Thucydides)' if r['dependence_block'] == 'THUCYDIDES' else ' (Herodotus)' if r['dependence_block'] == 'HERODOTUS' else '') for r in docrows}
assert len(docs) == 11 and len(set(docs)) == 11
summaries = tables['seed_summaries.csv']
summary_keys = ['cell', 'level', 'unit', 'aggregation', 'past_band', 'metric']
lookup = {tuple(r[k] for k in summary_keys): r for r in summaries}
assert len(lookup) == len(summaries) == 3465
assert set(r['unit'] for r in summaries if r['level'] == 'block') == set(blocks)
assert set(r['unit'] for r in summaries if r['level'] == 'document') == set(docs)

def fmt(value):
    if value == '':
        return 'null'
    x = float(value)
    return f'{x:.2e}' if x != 0 and abs(x) < 1e-6 else f'{x:.6f}'

def one(name, **filters):
    rows = [r for r in tables[name] if all(r[k] == str(v) for k, v in filters.items())]
    assert len(rows) == 1, (name, filters, len(rows))
    return rows[0]

def summary(cell, level, unit, metric, band='all', weight='not_applicable'):
    r = lookup[(cell, level, unit, weight, band, metric)]
    assert int(r['S']) == (20 if cell == 'C0' else 10)
    return r

def score_row(cell, level, unit, band='all', weight='not_applicable'):
    return [fmt(summary(cell, level, unit, m, band, weight)['mean']) for m in metrics]

def spread(cell, level, unit, band='all', weight='not_applicable', metric='q'):
    r = summary(cell, level, unit, metric, band, weight)
    return ' / '.join(fmt(r[k]) for k in ['mean', 'sd', 'min', 'max'])

def link(name):
    return f'[{name}](../results/hexis31/v3-seed0-v3006/{name})'

parts = []
def text(value):
    parts.append(value.strip() + '\n\n')

def table(headers, rows):
    rows = list(rows)
    assert all(len(row) == len(headers) for row in rows)
    parts.append('| ' + ' | '.join(headers) + ' |\n')
    parts.append('|' + '|'.join('---' for _ in headers) + '|\n')
    for row in rows:
        parts.append('| ' + ' | '.join(map(str, row)) + ' |\n')
    parts.append('\n')

text('''## V5 results and limitations — draft

**25 September 2026 — numerical dossier for the first owner review. V5 remains EXECUTED.**
This is the numerical basis requested for review, not the final scientific statement.
Interpretative writing starts after the first review; a second review of the complete
scientific draft precedes closure. No new fit, analytical cell or aggregation is introduced.
The historical sections below retain their original wording and status in their dated context.

### Evidence identity and scope

The campaign is [v3-seed0-v3006](../results/hexis31/v3-seed0-v3006/manifest.json),
run ID `6aa1b719e274116c5660790cf9b2ad73c7e1853cec672688e1dc27d6b7d60e05`.
Its manifest SHA-256 is `3243fc329351e45e1d1c2c2f68a5be57fec2ea197ef5a81a170a5c11f4ca6dab`.
The prescribed, separately executed seed-0 regeneration is
[v3-seed0-v3006-regeneration](../results/hexis31/v3-seed0-v3006-regeneration/manifest.json),
manifest SHA-256 `72b6cdee3220cbea97ba0bfb969bd2f3b871f244e62a8f3da3182d6d84c3790a`.
Both have the same scientific run identity. The lock SHA-256 is
`33db43b00bcb21ab12aedf6dcc4257764770bff0115dc0d1dfab6e5ea89876bf`.

Read-only checks for this dossier, from `05ece9cf29c8976f9c059155ea2eb43a7c863335`,
matched the deposited contract, current code/configuration/test/lock context and corpus
manifest against V2 evidence; `verify_evidence` accepted its 431 recorded passing cases.
`validate_run` accepted all 931 artifact hashes, and `check_keys` accepted the exact
490 pair / 980 model identities. Direct byte comparisons of the 70 artifacts named in
the report's regeneration record passed. The 431-case suite was not rerun for this
preliminary dossier; the final complete acceptance run is reserved for closure after
the second review.

The preparation plan recalled a byte reconstruction of 13 tables and five figures;
the accessible [V5 check log](../results/hexis31/v5-logs/02-report-checks.log) records
their hashes but not that reconstruction. This evidence gap was closed by calling the
existing frozen report functions on the published partitions and corpus, writing only
to `/tmp/hormathos-v5-review`: all 13 tables and five figures reproduced byte for byte.
No fit ran and no campaign artifact was overwritten. That temporary script/log is a
local checking aid, not a deposited or published artifact.

The [V4 verification record](../results/hexis31/v4-logs/commands.txt) covers the entire
campaign's keys, ledgers, denominators, shuffle/root checks and C0 loss-sum reconstruction.
It does not regenerate CTW fits for seeds 1–19. The separately executed regeneration
covers only the prescribed seed 0: 42 pairs / 84 models, 70 compared artifacts.
**The V4 terminal log and Python exit status remain lost**; the completion evidence is
the manifest and subsequent checks, as recorded in the dated campaign section below.

All result links in this dossier refer to local, Git-ignored artifacts. They are available
in this workspace; a repository clone alone does not contain them. The dossier does
not publish the raw data or C0 position vectors. Proposal, companion translations and
data publication remain separate activities.

### Reading the numerical tables

Scores are in **bits per eligible target**; R1 divergences and contributions are in
**bits**. O means original order; R means the prescribed within-sentence shuffle.
`G_O = CE_0 O − CE_CTW O`, `G_R = CE_0 R − CE_CTW R`, and `Q = G_O − G_R`.
All contrasts are **HEX − PROSE_ALL**; all sensitivity differences are **cell − C0**
on the same seed. Four CE terms remain necessary because the scored symbol population
can differ between arms despite identical eligible slots.

Every printed score uses six decimals, except nonzero magnitudes below 10⁻⁶, shown in
scientific notation with three significant digits. Rounding is presentation only:
coincident printed numbers are not mathematical identities. `null` is not zero.
The report's `mean`, sample `sd` (denominator S−1), `min`, `max` and `S` describe
computational variation over seeds, not uncertainty about ancient texts.
Tables labelled means select the `mean` field; no statistics are recomputed here.

The hierarchy remains seven block profiles and eleven documents, followed by two
subordinate group summaries. This is a finite corpus with two HEX and five PROSE_ALL
blocks, different training for each held-out block, chronological and annotation
confounding, offline annotations, a control conditioned on sentence composition,
and already observed pilots. The Iliad supplies about 97.5% of the retained C0 tokens
of HOMERIC_TRADITION (§3.3); the block conventions do not establish independent authors.
The six `inventory_only` documents contribute only to census/alphabet, never these scores.

### Population and denominator register

C0, a_total1, q_half and D12 use ud23 (m=100); upos uses upos_only (m=11) with the
**exact C0 retention and target mask**. OTH uses ud23_oth (m=105) and its own population.
`4_7` and `ge8` mean 4–7 and ≥8 retained predecessors in the same sentence. `all` is
their total, not a third disjoint population. C0 uses seeds 0–19; each perturbation 0–9.
Counts below are per seed and are not multiplied by S.
''')
text('**Table N1 — block denominators.** Source: '+link('block_pairs.csv')+
     '; filters `seed=0`, `cell=C0|oth`; keys `(cell, held_block_key, seed, past_band)`, with `held_block` as label. Columns select `n`; units: eligible targets. The C0 columns also apply to upos and the three other ud23 cells, checked against every source row.')
table(['Block', 'C0 all', 'C0 4–7', 'C0 ≥8', 'OTH all', 'OTH 4–7', 'OTH ≥8'],
      ([b]+[one('block_pairs.csv',cell=c,seed=0,held_block=b,past_band=band)['n'] for c in ['C0','oth'] for band in ['all','4_7','ge8']] for b in blocks))
text('**Table N2 — document identities and denominators.** Source: '+link('document_scores.csv')+
     '; filters `seed=0`, `cell=C0|oth`; keys `(cell, held_block_key, seed, doc_id, past_band)`; `n` is the denominator. Work names and complete retained-token counts are selected from [V1 documents.csv](../results/hexis31/v1/documents.csv), `role=primary`, `variant=ud23`, keyed by `(variant, doc_id)`. C0 all-target denominators for the total document profiles are its `eligible` column; total profiles themselves come from `seed_summaries.csv`.')
table(['Document key (`doc_id`)', 'Work', 'Block', 'C0 retained', 'C0 all', 'C0 4–7', 'C0 ≥8', 'OTH 4–7', 'OTH ≥8'],
      ([d,labels[d],r['dependence_block'],r['kept'],r['eligible']]+[one('document_scores.csv',cell=c,seed=0,doc_id=d,past_band=band)['n'] for c in ['C0','oth'] for band in ['4_7','ge8']] for r in docrows for d in [r['doc_id']]))

text('### Primary profiles and computational dispersion')
text('**Tables P1–P3 — C0 means for every block and document, total and both bands.** Source: '+link('seed_summaries.csv')+
     '; filters `cell=C0`, `level=block|document`, `aggregation=not_applicable`, `past_band` as named by each table; keys `(cell, level, unit, aggregation, past_band, metric)`. Each column selects `mean` for the metric in the legend, S=20. Units: bits/target, using N1/N2 for the corresponding unit and band. Document titles below map to the exact keys in N2. All seven metrics, all three bands, all six cells and their full `mean/sd/min/max/S/reason` records are available at that source; this is the extended profile table, including every perturbation document profile.')
for i, band in enumerate(['all','4_7','ge8'],1):
    text(f'**P{i}: {dict(all="all eligible targets", **{"4_7":"4–7 predecessors", "ge8":"≥8 predecessors"})[band]}.**')
    table(['Level / unit']+metric_labels,
          ([level+' / '+labels.get(unit,unit)]+score_row('C0',level,unit,band) for level, units in [('block',blocks),('document',docs)] for unit in units))
text('**Table P4 — Q dispersion for the same C0 profiles.** Same source and keys as P1–P3, `metric=q`. Each entry is **mean / sample SD / min / max**, S=20, in bits/target; denominator follows the column band in N1/N2. Dispersion of each of the other six metrics is retained in the extended source with identical keys and fields; no SD or extreme is averaged across lower-level units.')
table(['Level / unit', 'All: mean / SD / min / max', '4–7: mean / SD / min / max', '≥8: mean / SD / min / max'],
      ([level+' / '+labels.get(unit,unit)]+[spread('C0',level,unit,band) for band in ['all','4_7','ge8']] for level, units in [('block',blocks),('document',docs)] for unit in units))

text('### Both subordinate summaries in all six cells')
text('**Table S1 — HEX, PROSE_ALL and HEX − PROSE_ALL, both weightings adjacent.** Source: '+link('seed_summaries.csv')+
     '; filters `level=group`, `past_band=all`; keys `(cell, level, unit, aggregation, past_band, metric)`, where `unit=contrast` is HEX − PROSE_ALL. Entries select `mean`; all seven columns are bits/target. S=20 for C0 and 10 elsewhere. '+link('contrasts.csv')+
     ' retains every seed under `(cell, seed, aggregation, group)` and its `n`; group `n` is the total eligible population under either weighting, while contrast `n` is not a loss denominator. Equal-block means use 2 HEX / 5 PROSE_ALL blocks; target-weighted means use their respective eligible totals. No pooled denominator is assigned to the difference of groups.')
table(['Cell', 'Group or contrast', 'Weight']+metric_labels,
      ([c,u,weight_labels[w]]+score_row(c,'group',u,weight=w) for c in cells for u in ['HEX','PROSE_ALL','contrast'] for w in weights))
text('**Table S2 — computational Q dispersion, both weightings side by side.** Same source, filters and units as S1, `metric=q`. Each entry is **mean / sample SD / min / max**. Full seven-metric dispersion is in the same source rows, selected by `metric`; S is printed explicitly.')
table(['Cell', 'Group or contrast', 'S', 'Equal block: mean / SD / min / max', 'Eligible target: mean / SD / min / max'],
      ([c,u,20 if c=='C0' else 10]+[spread(c,'group',u,weight=w) for w in weights] for c in cells for u in ['HEX','PROSE_ALL','contrast']))
text('**Table S3 — populations and weights.** Source: '+link('aggregation_weights.csv')+
     '; filters `seed=0`, cells C0/oth/q_half, both aggregations; key `(cell, seed, aggregation, held_block_key)`. `n` is eligible targets per held-out block; `share` is its within-group summary weight. `training_tokens/available_tokens` is the block\'s sampling quota when it contributes, not the held-out population. `training_share` uses available retained tokens as denominator. `fold_training_tokens` and `fold_share_HEX/PROSE_ALL` refer to the training of the fold holding out the named block. Shares are fractions, not percentages. The complete 980-row source includes all seeds/cells. a_total1/D12/upos share these C0 count/weight/quota fields; OTH changes populations and q_half changes the quota.')
table(['Cell / block', 'n', 'Equal share', 'Target share', 'Contributor quota / available', 'Sample fraction', 'Fold training', 'Fold HEX share', 'Fold PROSE share'],
      ([c+' / '+b, r['n'], fmt(one('aggregation_weights.csv',cell=c,seed=0,block=b,aggregation='equal_block')['share']),fmt(r['share']),r['training_tokens']+' / '+r['available_tokens'],fmt(r['training_share']),r['fold_training_tokens'],fmt(r['fold_share_HEX']),fmt(r['fold_share_PROSE_ALL'])] for c in ['C0','oth','q_half'] for b in blocks for r in [one('aggregation_weights.csv',cell=c,seed=0,block=b,aggregation='eligible_token_weighted')]))

text('### Paired sensitivity register')
text('**Tables D1–D2 — paired Q differences.** Sources: '+link('sensitivity_pairs.csv')+' and '+link('seed_summaries.csv')+
     '. D1 selects `level=block_difference`, D2 `level=group_difference`, both `past_band=all`, `metric=q`, all five non-C0 cells. Keys are `(cell, level, unit, aggregation, past_band, metric)` in the summaries; each underlying paired row additionally has `seed`, `reference=C0`, `value`, `reference_value`, `difference`. Every entry is **mean / sample SD / min / max** of `cell − C0` on seeds **0–9**, S=10. Units: bits/target; each operand uses its own N1/N2/S1 population. In particular OTH changes the target population; the paired seed does not equate the two tasks. These rows never subtract C0\'s 20-seed mean. All seven metrics and both block history bands are available under the same keys in the linked sources (there is no document-difference level or group-band contrast).')
table(['Cell', 'Block', 'ΔQ: mean / SD / min / max (S=10)'],
      ([c,b,spread(c,'block_difference',b)] for c in cells[1:] for b in blocks))
table(['Cell', 'Group or contrast', 'Equal block ΔQ: mean / SD / min / max', 'Eligible target ΔQ: mean / SD / min / max'],
      ([c,u]+[spread(c,'group_difference',u,weight=w) for w in weights] for c in cells[1:] for u in ['HEX','PROSE_ALL','contrast']))
text('**Table D3 — all seven components of the paired contrast differences.** Same sources and units, `level=group_difference`, `unit=contrast`, `past_band=all`; entries select `mean`, S=10. This retains the direction of each loss and gain change beside ΔQ. The complete dispersion and HEX/PROSE_ALL component means are in the linked summaries, without selection by sign.')
table(['Cell', 'Weight']+['Δ'+x for x in metric_labels],
      ([c,weight_labels[w]]+score_row(c,'group_difference','contrast',weight=w) for c in cells[1:] for w in weights))

text('### R1: all three marginal comparisons')
text('''R1 uses complete original retained tokens, **including sentence-initial tokens**,
from the seven primary blocks, not only eligible targets, sampled training roots or
inventory-only texts. It has no seed dimension. '''+link('root_distributions.csv')+
     ''' holds 1,512 rows keyed by `(variant, block, symbol_id)`, with unsmoothed `count`,
`empirical_frequency=count/N_all` and `smoothed_frequency=(count+0.5)/(N_all+0.5m)`.
Complete block token counts come from the deposited §3.3 table (C0/UPOS 154,300,
OTH 154,947 across primary blocks); per-document counts are in V1 `documents.csv`.
R1 describes marginal distributions and neither corrects nor validates Q.''')
text('**Table R1a — all 21 unordered pairs, three representations.** Source: '+link('jsd_pairs.csv')+
     '; no row excluded; keys `(variant, block_a, block_b)`, value `jsd` in bits. Each column reconstructs its full 7×7 matrix by reflection, with diagonal zero; no averaging or new JSD computation is involved. Variant alphabets m=100/105/11 and denominators are the smoothed full-block distributions above.')
pairs = [(r['block_a'],r['block_b']) for r in tables['jsd_pairs.csv'] if r['variant']=='ud23']
assert len(pairs)==21
table(['Block a', 'Block b', 'ud23', 'ud23_oth', 'upos_only'],
      ([a,b]+[fmt(one('jsd_pairs.csv',variant=v,block_a=a,block_b=b)['jsd']) for v in ['ud23','ud23_oth','upos_only']] for a,b in pairs))
text('**Table R1b — centroid divergences.** Source: '+link('jsd_centroids.csv')+
     '; all rows, key `(variant, group_a, group_b)`, value `jsd` in bits. Each HEX centroid is the uniform mean of its two smoothed block distributions; PROSE_ALL uses five. These are neither target-weighted centroids nor averages of pair divergences.')
table(['Variant', 'HEX blocks', 'PROSE_ALL blocks', 'Centroid JSD (bits)'],
      ([r['variant'],r['blocks_a'],r['blocks_b'],fmt(r['jsd'])] for r in tables['jsd_centroids.csv']))
text('**R1c — complete contributions, available locally.** '+link('jsd_contributions.csv')+
     ''' retains all **4,752** symbol contributions: keys `(variant, scope, a, b, symbol_id)`,
`scope=block_pair|group_centroid`, value `contribution` in bits. All symbols, including
zero contributions, are retained for all 21 pairs and each centroid comparison in
each representation: (21+1)×(100+105+11). `symbol` maps the frozen lexicographic ID.
There is no top-contributor selection. The numerical check compares every contribution
sum with the corresponding published JSD. Full centroid vectors are reconstructible
from the linked smoothed block frequencies with the uniform 2/5 weights.''')

text('### Diagnostics and resources: exact access paths')
text('**Table X1 — diagnostic source register, all cells/seeds included.** Each linked source is part of the same hash-verified manifest. The table specifies complete selections and denominators; nested histogram fields are JSON cells in the CSV, not missing supplementary files. No new cross-seed diagnostic aggregation is introduced.')
table(['Source / rows', 'Selection and keys', 'Fields, units and denominator'], [
    [link('model_diagnostics.csv')+' / 980', 'All; (cell, held_block_key, seed, arm)', '`nodes`, `node_count_by_structural_depth`, `support_histogram_1_2to4_5to9_10plus_by_depth`: node counts per model/depth, support bins 1, 2–4, 5–9, ≥10; do not multiply by document count. `root_observed_symbol_count`, `root_unseen_symbol_count`: alphabet types. `root_stop`: probability; `delta_root_nats_stop_minus_split`: nats, with `delta_root_reason`. `fit_seconds`, `evaluation_seconds`: seconds; `peak_rss`: bytes, process high-water mark, not additive RAM.'],
    [link('arm_diagnostics.csv')+' / 3,080', 'All; (cell, held_block_key, seed, doc_id, arm, past_band)', '`n`: targets. `resolved_mean=sum_resolved_valid/resolved_valid_count`; zero valid mass is null with reason, never a length zero. `resolved_null_count_by_reason_no_resolved_mass`: null count. `unseen_mass_mean=sum_unseen_mass/n`; `sum_observed_mass_by_length_ℓ/n`: mass at ℓ ordinary edges, BOS excluded. `root_unseen_target_count/n`: fraction of targets unseen at root. `implicit_unseen_branch_encounter_count`: encounters with support 0, not materialized nodes.'],
    [link('fragment_diagnostics.csv')+' / 2,940', 'All; (cell, held_block_key, seed, contributor_key)', '`fragment_count`, `internal_start_count`: fragment counts; `fragment_tokens`: retained tokens in cut fragments; `direct_context_targets`: eligible positions within those fragments. Six contributors per pair; shared by both arms, not two independent samples. The named sample ledger records coordinates and subseeds.'],
    [link('aggregation_weights.csv')+' / 980', 'All; (cell, seed, aggregation, held_block_key)', '`n`, `weight`, `share`: held-out populations and within-group weights. `training_tokens/available_tokens`: contributor quota/retained supply. `fold_training_tokens`: tokens after excluding the held-out block; `fold_share_*` uses that denominator.'],
    [link('document_scores.csv')+' / 1,540; '+link('block_pairs.csv')+' / 1,470', 'All; (cell, held_block_key, seed[, doc_id], past_band)', '`n`, four `sum_loss_*` (bits), CE/G/Q (bits/target), `reason`; `changed_symbol_eligible_slot_count/eligible_slot_count` measures changed symbols only on eligible slots. Both bands are retained even if empty.'],
])
text('''The means of L_resolved are means of valid position values, not ratios of aggregated
mass moments. L_resolved is an assigned context length conditional on observed mass,
not reliability, grammatical depth or a maximum recoverable order. Masses by length and
unseen mass use all targets, and sum to one within tolerance after division by `n`.
Columns for lengths 9–12 are populated for D12; blank cells in the other depth-8 models
mean those lengths are outside the model, not `no_resolved_mass`. Empty scored buckets
retain n=0, additive sums=0 and null means/scores with reason `empty_bucket`.
`root_stop` saturation and tiny G_R values must remain recorded numerical behavior,
not a theorem that the shuffled CTW equals its root.''')
text('**Table X2 — model records at a fixed reference slice.** Source: '+link('model_diagnostics.csv')+
     '; filter `cell=C0, seed=0`, all seven held-out blocks and both arms. Key `(cell, held_block_key, seed, arm)`; counts per model, delta in nats, times in seconds, RSS in bytes. This is a reference slice, not a campaign mean or a selected extreme; X1 links all remaining models and their complete support histograms.')
table(['Block / arm', 'Nodes', 'Root seen / unseen types', 'root_stop', 'delta_root (nats)', 'Fit s', 'Eval s', 'Peak RSS bytes'],
      ([b+' / '+a,r['nodes'],r['root_observed_symbol_count']+' / '+r['root_unseen_symbol_count'],fmt(r['root_stop']),fmt(r['delta_root_nats_stop_minus_split']),fmt(r['fit_seconds']),fmt(r['evaluation_seconds']),r['peak_rss']] for b in blocks for a in ['original','shuffled'] for r in [one('model_diagnostics.csv',cell='C0',seed=0,held_block=b,arm=a)]))
text('**Table X3 — evaluation records at the same fixed reference seed.** Source: '+link('arm_diagnostics.csv')+
     '; filters `cell=C0, seed=0`, all documents, arms and bands; key `(cell, held_block_key, seed, doc_id, arm, past_band)`. Counts: `n`, valid `resolved_valid_count`, null `resolved_null_count_by_reason_no_resolved_mass`, `root_unseen_target_count`, `implicit_unseen_branch_encounter_count`. L selects `resolved_mean` (ordinary context length); unseen mass selects `unseen_mass_mean` (fraction over n). Full sums and every mass-by-length component are in X1, including all other cells/seeds.')
table(['Document / arm / band', 'n', 'Valid / null L', 'Mean L', 'Mean unseen mass', 'Root-unseen targets', 'Implicit encounters'],
      ([labels[d]+' / '+a+' / '+band,r['n'],r['resolved_valid_count']+' / '+r['resolved_null_count_by_reason_no_resolved_mass'],fmt(r['resolved_mean']),fmt(r['unseen_mass_mean']),r['root_unseen_target_count'],r['implicit_unseen_branch_encounter_count']] for d in docs for a in ['original','shuffled'] for band in ['4_7','ge8'] for r in [one('arm_diagnostics.csv',cell='C0',seed=0,doc_id=d,arm=a,past_band=band)]))
text('''Campaign resource totals remain the measured records in the dated V4/V5 section:
713.32 s summed fit time and 535.60 s summed evaluation time over 980 models, peak RSS
1,654,919,168 bytes; the V4 resume wall time in the manifest is 7,450.8 s. These are
historical measurements, not forecasts or performance guarantees. Per-model values are
in X1; the report manifest has separate report-stage resources. No resource sum is used
as a score or complexity penalty.''')

text('### Existing figures and review boundary')
table(['Figure', 'Numerical companion / scope'], [
    [link('figure__corpus_annotation.svg'), 'V1 documents.csv and audit_contingency.csv: quantities, retention and annotation census, including inventory_only.'],
    [link('figure__block_document_profiles.svg'), 'P1–P4; the linked extended seed summaries contain all profile components and bands.'],
    [link('figure__sensitivities_two_weights.svg'), 'S1–S3, D1–D3; both weights and paired first-ten-seed differences.'],
    [link('figure__R1.svg'), 'R1a–R1c: three complete pair tables and centroid/contribution records.'],
    [link('figure__supports_mixture_masses.svg'), 'X1–X3: model supports, assigned masses and resolved lengths with their own denominators.'],
])
text('''Byte identity of the five figures was checked during preparation. Visual readability
and caption/interpretation checks remain part of the complete scientific draft review.
No frozen figure has been edited.

**First-review checkpoint.** The numerical checks found no discrepancy in the source
identities, displayed selections, denominator coverage, contrast direction or paired
seed sets. The missing reconstruction record was addressed as documented above;
the lost V4 terminal log remains an explicit procedural limitation. This dossier awaits
the owner\'s numerical review. No conclusion is yet adopted from these values.

After that review, the scientific account must apply §16 beside the relevant results:
numerically null G_R is observed behavior; D8/D12 similarity cannot exclude longer
dependencies; UPOS is a different task and cannot isolate DEPREL by subtraction; R1
does not validate Q. It must retain the corpus/training/annotation/pilot limitations,
both weights and every sign, and the explicit design omissions (no final stop/split
prior sensitivity, cross-boundary evaluation or specificity comparison with other
meters). The second owner review precedes any V5 COMPLETED status or README summary.''')

section=''.join(parts)
path=ROOT/'docs/HANDOFF.md'
original=path.read_text()
marker='## Campaign V4 and report V5 — 24 and 25 September 2026'
assert '## V5 results and limitations — draft' not in original
assert original.count(marker)==1
path.write_text(original.replace(marker,section+marker))
(OUT/'section.md').write_text(section)
print('Inserted numerical dossier:', len(section.splitlines()), 'lines;',len(section),'characters')
