"""The single reporter: the six-step validator and one aggregation (§11.5, §14.2).

Nothing here re-implements a formula. Documents, blocks, groups and the two
weightings come from `protocols.scores`, the three R1 quantities from
`protocols.r1`, and the tables are those objects written out. The five figures of
§11.6 are not this stage's work: they derive from these verified tables.

The validator refuses before it emits. A missing cell, a duplicated key, a
corrupted artifact, an inventory_only score or an evidence recorded under another
code identity stops the report — a partial contrast is never written as a result.
"""

import argparse
import itertools
import json
import time
from pathlib import Path

import pandas as pd

from hexis.contracts import compare, digest, load_contracts
from hexis.model import diagnostics
from hexis.pipeline import scientific_run
from hexis.protocols import r1, scores

KEY_COLUMNS = ('cell', 'variant', 'held_block', 'held_block_key', 'seed')
RECORD_FIELDS = (*KEY_COLUMNS, 'q', 'depth', 'm', 'a_per_symbol', 'rho', 'min_available_past',
                 'arms', 'ledger_sha256', 'training', 'fragments', 'shuffle', 'models',
                 'document_sums', 'arm_diagnostics', 'positions')
TABLES = ('document_scores.csv', 'block_pairs.csv', 'aggregation_weights.csv', 'contrasts.csv',
          'seed_summaries.csv', 'sensitivity_pairs.csv', 'model_diagnostics.csv',
          'arm_diagnostics.csv', 'root_distributions.csv', 'jsd_pairs.csv', 'jsd_centroids.csv',
          'jsd_contributions.csv')
REFERENCE_CELL = 'C0'  # §11.5: sensitivities are paired against C0 on the same seeds
SENSITIVITY_COLUMNS = ('cell', 'reference', 'aggregation', 'group', 'metric', 'seeds', 'mean', 'sd',
                       'min', 'max', 'S')
CENTROID_COLUMNS = ('variant', 'group_a', 'group_b', 'blocks_a', 'blocks_b', 'jsd')


# --- the six steps -------------------------------------------------------------

def check_deposit(contract, deposited: bool) -> bool:
    """Step 1: the deposited bytes of the analytical contracts and of the plan named by the lock.

    The configuration is verified before this step and not inside it:
    `scientific_run.load_projection` refuses a configuration that is not the deposited
    analytical projection unless `--fixture` is declared, and `main` compares this run's
    whole `run_contract` — `configuration` digest included — with the published one. A
    comparison here against `contract['configuration']` would only restate the digest this
    same call built from this same configuration, and could never fail.
    """
    contracts = load_contracts()
    if deposited:
        compare(contract['analytical_contracts'], contracts['lock']['contracts'],
                'analytical_contracts')
        compare(contract['plan'], contracts['lock']['plan']['sha256'], 'plan')
    return deposited


def check_evidence(evidence, contract):
    """Step 2: the V0–V1 evidence of this manifest, under the code and lock of this run."""
    missing = [step for step in scientific_run.EVIDENCE_STEPS if step not in evidence]
    if missing:
        raise ValueError(f'evidence: {missing} is not recorded in this manifest; a written PASS '
                         'is not the proof it stands for')
    for step, record in sorted(evidence.items()):
        if record.get('code') != digest(contract['code']):
            raise ValueError(f'evidence {step}: recorded under another code identity')
        if record.get('lock') != contract['lock']:
            raise ValueError(f'evidence {step}: recorded under another environment lock')


def expected_keys(cfg) -> dict:
    """Step 3: the keys the contract asks for, generated from the contract itself."""
    blocks = scientific_run.block_keys_of(cfg)
    pair, model = [], []
    for cell in cfg['cells']:
        for name in sorted(blocks):
            for seed in cell['seeds']:
                key = (cell['id'], blocks[name], int(seed))
                pair.append(key)
                model.extend((*key, arm) for arm in cell['arms'])
    return {'pair': pair, 'model': model}


def check_keys(cfg, produced):
    """Step 3: set equality against the contract, duplicates detected before the sets."""
    expected = expected_keys(cfg)
    published = scientific_run.key_sets(produced)
    for kind in ('pair', 'model'):
        missing = sorted(set(expected[kind]) - published[kind])
        unexpected = sorted(published[kind] - set(expected[kind]))
        if missing or unexpected:
            raise ValueError(f'{kind} key set differs from the contract: missing {missing[:4]}, '
                             f'unexpected {unexpected[:4]} ({len(missing)} and {len(unexpected)} '
                             'in total)')


def read_partitions(output, manifest) -> list:
    """Step 4: every published pair record, read back and checked against its own key."""
    output, records = Path(output), []
    for key in sorted(tuple(key) for key in manifest['keys']['pair']):
        name = scientific_run.pair_name(*key)
        record = json.loads((output / name).read_bytes())
        missing = [field for field in RECORD_FIELDS if field not in record]
        if missing:
            raise ValueError(f'{name}: the partition is missing field(s) {missing}')
        if (record['cell'], record['held_block_key'], record['seed']) != key:
            raise ValueError(f'{name}: the record names another key')
        records.append(record)
    return records


def check_roles(scored, documents):
    """Step 5: no inventory_only document ever carries a score (§2.3, §14.2)."""
    roles = dict(zip(documents['doc_id'].astype(str), documents['role'].astype(str)))
    scored_ids = sorted(set(scored['doc_id'].astype(str)))
    unknown = [doc for doc in scored_ids if doc not in roles]
    if unknown:
        raise ValueError(f'{unknown}: scored documents absent from the corpus registry')
    refused = [doc for doc in scored_ids if roles[doc] == 'inventory_only']
    if refused:
        raise ValueError(f'{refused}: inventory_only documents are censused, never scored')


def check_positions(output, record, cfg, coordinates):
    """Step 4 for C0: exactly the eligible slots of the evaluated block, and no other column."""
    frame = pd.read_parquet(Path(output) / record['positions'])
    if list(frame.columns) != list(scores.POSITION_COLUMNS):
        raise ValueError(f"{record['positions']}: columns {list(frame.columns)} are not the §11.4 "
                         'fields')
    docs = scientific_run.blocks_of(cfg)[record['held_block']]
    eligible = coordinates[coordinates['variant'].eq(record['variant'])
                           & coordinates['doc_id'].astype(str).isin(docs)
                           & coordinates['eligible'].astype(bool)]
    if len(frame) != len(eligible):
        raise ValueError(f"{record['positions']}: {len(frame)} persisted rows against "
                         f'{len(eligible)} eligible slots of {record["held_block"]}')
    return frame, eligible


def reconstruct(frame, eligible) -> pd.DataFrame:
    """Step 6 for C0: losses -> documents, through the coordinate dictionary (§11.5)."""
    joined = scores.pair_positions(frame, eligible[['slot_uid', 'doc_id', 'available_past']])
    joined = joined.assign(doc_id=joined['doc_id'].astype(str),
                           past_band=joined['available_past'].map(scores.past_band))
    return scores.aggregate(joined, keys=['doc_id'])


# --- one aggregation -----------------------------------------------------------

def document_scores(records) -> pd.DataFrame:
    """§11.5: n and the four unrounded sums per document, seed, cell and band."""
    frames = [pd.DataFrame(record['document_sums']).assign(
        **{column: record[column] for column in KEY_COLUMNS}) for record in records]
    docs = pd.concat(frames, ignore_index=True)[
        [*KEY_COLUMNS, 'doc_id', 'past_band', *scores.SUM_COLUMNS]]
    bands = docs.groupby([*KEY_COLUMNS, 'doc_id'], sort=True)['past_band'].agg(
        lambda values: tuple(sorted(values)))
    incomplete = [key for key, seen in bands.items() if seen != tuple(sorted(scores.BANDS))]
    if incomplete:
        raise ValueError(f'{incomplete[:4]}: every scored document keeps both bands, an empty one '
                         'as a zero row')
    return docs


def block_pairs(docs) -> pd.DataFrame:
    """§11.5: the block rows per band and their total, summed from the document rows."""
    keys = list(KEY_COLUMNS)
    banded = scores.roll_up(docs, keys=[*keys, 'past_band'])
    total = scores.roll_up(docs, keys=keys).assign(past_band='all')
    return scores.ce_gain_q(pd.concat([banded, total[banded.columns]], ignore_index=True))


def group_contrasts(blocks, groups) -> pd.DataFrame:
    """§8.2: group means and the HEX - PROSE_ALL contrast, per cell and seed."""
    rows = []
    for (cell, seed), part in blocks.groupby(['cell', 'seed'], sort=True):
        frame = part.rename(columns={'held_block': 'block'})[
            ['block', 'n', *scores.SCORE_COLUMNS]]
        rows.append(scores.contrasts(frame, groups).assign(cell=cell, seed=seed))
    return pd.concat(rows, ignore_index=True)[
        ['cell', 'seed', 'aggregation', 'group', 'n', *scores.SCORE_COLUMNS]]


def aggregation_weights(blocks, training, groups) -> pd.DataFrame:
    """§11.5: the weight each block carries under both weightings, with its training quota."""
    rows = []
    for aggregation in scores.AGGREGATIONS:
        frame = blocks.assign(aggregation=aggregation, group=blocks['held_block'].map(groups))
        frame['weight'] = 1.0 if aggregation == scores.AGGREGATIONS[0] else frame['n'].astype(float)
        shares = frame.groupby(['cell', 'seed', 'group'])['weight'].transform('sum')
        rows.append(frame.assign(share=frame['weight'] / shares))
    weights = pd.concat(rows, ignore_index=True).rename(columns={'held_block': 'block'})
    merged = weights.merge(training, on=['cell', 'block'], how='left', validate='many_to_one')
    return merged[['cell', 'seed', 'aggregation', 'block', 'held_block_key', 'group', 'n',
                   'weight', 'share', 'training_tokens', 'available_tokens', 'training_share']]


def training_quota(records) -> pd.DataFrame:
    """The tokens each block contributes to a training sample, beside the results (§11.5)."""
    frames = [pd.DataFrame(record['training']).assign(cell=record['cell']) for record in records]
    quota = pd.concat(frames, ignore_index=True).groupby(['cell', 'block'], sort=True,
                                                         as_index=False).agg(
        folds=('tokens', 'size'), training_tokens=('tokens', 'max'),
        available_tokens=('available', 'max'))
    quota['training_share'] = quota['training_tokens'] / quota['available_tokens']
    return quota


def seed_summaries(contrasts) -> pd.DataFrame:
    """§8.2: aggregate per seed first, then mean, SD with S-1, min, max and S."""
    melted = contrasts.melt(id_vars=['cell', 'seed', 'aggregation', 'group'],
                            value_vars=list(scores.SCORE_COLUMNS), var_name='metric',
                            value_name='value')
    rows = [{'cell': cell, 'aggregation': aggregation, 'group': group, 'metric': metric,
             **scores.seed_summary(part['value'])}
            for (cell, aggregation, group, metric), part in
            melted.groupby(['cell', 'aggregation', 'group', 'metric'], sort=True)]
    return pd.DataFrame(rows)


def sensitivity_pairs(contrasts) -> pd.DataFrame:
    """§11.5: paired differences against C0 on the very same seeds, never on a changed set."""
    melted = contrasts.melt(id_vars=['cell', 'seed', 'aggregation', 'group'],
                            value_vars=list(scores.SCORE_COLUMNS), var_name='metric',
                            value_name='value')
    on = ['seed', 'aggregation', 'group', 'metric']
    reference = melted[melted['cell'].eq(REFERENCE_CELL)].drop(columns='cell')
    rows = []
    for cell, part in melted[melted['cell'].ne(REFERENCE_CELL)].groupby('cell', sort=True):
        paired = part.drop(columns='cell').merge(reference, on=on, suffixes=('', '_reference'),
                                                 validate='one_to_one')
        if len(paired) != len(part):
            raise ValueError(f'{cell}: {len(part) - len(paired)} rows have no {REFERENCE_CELL} '
                             'value on the same seed; a changed population is not a paired '
                             'comparison')
        paired = paired.assign(difference=paired['value'] - paired['value_reference'])
        for (aggregation, group, metric), block in paired.groupby(
                ['aggregation', 'group', 'metric'], sort=True):
            rows.append({'cell': cell, 'reference': REFERENCE_CELL, 'aggregation': aggregation,
                         'group': group, 'metric': metric,
                         'seeds': sorted(int(seed) for seed in block['seed']),
                         **scores.seed_summary(block['difference'])})
    frame = pd.DataFrame(rows, columns=list(SENSITIVITY_COLUMNS))
    frame['seeds'] = frame['seeds'].map(lambda seeds: ' '.join(str(seed) for seed in seeds))
    return frame


def model_diagnostics(records) -> pd.DataFrame:
    """§11.5: supports, masses, root record and fingerprint of every fitted model."""
    rows = []
    for record in records:
        for arm, model in sorted(record['models'].items()):
            row = {column: record[column] for column in KEY_COLUMNS}
            row.update(arm=arm, depth=record['depth'], m=record['m'],
                       a_per_symbol=record['a_per_symbol'], q=record['q'],
                       ledger_sha256=record['ledger_sha256'],
                       **{f'{population}_{name}': value
                          for population, counts in sorted(record['shuffle'].items())
                          for name, value in sorted(counts.items())},
                       **{name: value for name, value in sorted(model.items())
                          if name != 'nodes_by_depth'},
                       nodes_by_depth=' '.join(str(count) for count in model['nodes_by_depth']))
            rows.append(row)
    return pd.DataFrame(rows)


def arm_diagnostics(records) -> pd.DataFrame:
    """§9.3 per document, arm and band: the sums, each mean over its own denominator.

    The document dimension is the one the loss sums carry (§11.5), so step 4 reads
    `entrambe le fasce per documento` from these rows directly.
    """
    frames = []
    for record in records:
        frame = pd.DataFrame(record['arm_diagnostics']).assign(
            **{column: record[column] for column in KEY_COLUMNS})
        means = [diagnostics.means(row) for row in frame.to_dict('records')]
        frames.append(frame.assign(resolved_mean=[value['L'] for value in means],
                                   unseen_mass_mean=[value['unseen'] for value in means],
                                   reason=[value['reason'] for value in means]))
    frame = pd.concat(frames, ignore_index=True)
    leading = [*KEY_COLUMNS, 'doc_id', 'arm', 'past_band']
    return frame[[*leading, *[name for name in frame.columns if name not in leading]]]


def r1_tables(cfg, coordinates) -> dict:
    """R1 in full: raw counts, frequencies, the C(n,2) pairs, centroids and contributions."""
    blocks, groups = scientific_run.blocks_of(cfg), scientific_run.groups_of(cfg)
    sizes = scientific_run.alphabet_sizes(cfg)
    distributions, pairs, centroids, contributions = [], [], [], []
    for variant in cfg['R1']['variants']:
        if variant not in sizes:
            raise ValueError(f'R1 variant {variant!r}: no cell declares its alphabet size')
        counts = r1.block_counts(coordinates, blocks, variant=variant, m=sizes[variant])
        smoothed = {name: r1.smoothed(vector, a=cfg['R1']['a_per_symbol'])
                    for name, vector in counts.items()}
        distributions.extend(
            {'variant': variant, 'block': name, 'symbol_id': symbol,
             'count': int(counts[name][symbol]), 'frequency': float(smoothed[name][symbol])}
            for name in sorted(counts) for symbol in range(sizes[variant]))
        pairs.append(r1.pairs(smoothed).assign(variant=variant))
        contributions.extend(
            {'variant': variant, 'scope': 'block_pair', 'a': left, 'b': right,
             'symbol_id': symbol, 'contribution': float(value)}
            for left, right in itertools.combinations(sorted(smoothed), 2)
            for symbol, value in enumerate(r1.contributions(smoothed[left], smoothed[right])))
        members = {group: [smoothed[name] for name in sorted(smoothed) if groups[name] == group]
                   for group in sorted(set(groups.values()))}
        means = {group: r1.centroid(vectors) for group, vectors in members.items()}
        for left, right in itertools.combinations(sorted(means), 2):
            centroids.append({'variant': variant, 'group_a': left, 'group_b': right,
                              'blocks_a': len(members[left]), 'blocks_b': len(members[right]),
                              'jsd': r1.jsd(means[left], means[right])})
            contributions.extend(
                {'variant': variant, 'scope': 'group_centroid', 'a': left, 'b': right,
                 'symbol_id': symbol, 'contribution': float(value)}
                for symbol, value in enumerate(r1.contributions(means[left], means[right])))
    return {'root_distributions.csv': pd.DataFrame(distributions),
            'jsd_pairs.csv': pd.concat(pairs, ignore_index=True)[
                ['variant', 'block_a', 'block_b', 'jsd']],
            'jsd_centroids.csv': pd.DataFrame(centroids, columns=list(CENTROID_COLUMNS)),
            'jsd_contributions.csv': pd.DataFrame(contributions)}


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='HEXIS 3.1 report: six-step validator, one aggregation, no figures')
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--corpus-dir', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--fixture', action='store_true',
                        help='declare a synthetic configuration; the report is not scientific')
    args = parser.parse_args(argv)
    started = time.perf_counter()
    cfg, deposited = scientific_run.load_projection(args.config, args.fixture)
    corpus, frames = scientific_run.load_corpus(args.corpus_dir)
    contract = scientific_run.run_contract(cfg, corpus)
    prior = scientific_run.read_prior(args.output_dir)
    if prior is None:
        raise ValueError(f'{args.output_dir}: no published descriptive run to report on')
    scientific_run.check_stage_open(args.output_dir, 'report', prior, resume=False)
    compare(contract, prior['run_contract'], 'run_contract')
    steps = []
    scientific = check_deposit(contract, deposited)
    steps.append(1)
    check_evidence(prior['evidence'], contract)
    steps.append(2)
    check_keys(cfg, prior['keys'])
    steps.append(3)
    records = read_partitions(args.output_dir, prior)
    coordinates = frames['coordinates.parquet']
    positional = [record for record in records if record['positions'] is not None]
    for record in positional:  # one partition in memory at a time (§11.4)
        check_positions(args.output_dir, record, cfg, coordinates)
    steps.append(4)
    docs = document_scores(records)
    check_roles(docs, frames['documents.csv'])
    tables = r1_tables(cfg, coordinates)
    steps.append(5)
    for record in positional:
        rebuilt = reconstruct(*check_positions(args.output_dir, record, cfg, coordinates))
        persisted = pd.DataFrame(record['document_sums'])
        if not rebuilt.reset_index(drop=True).equals(persisted[rebuilt.columns]):
            raise ValueError(f"{record['positions']}: the persisted sums are not the sums of the "
                             'persisted positions')
    blocks = block_pairs(docs)
    totals = blocks[blocks['past_band'].eq('all')]
    contrasts = group_contrasts(totals, scientific_run.groups_of(cfg))
    tables.update({'document_scores.csv': scores.ce_gain_q(docs), 'block_pairs.csv': blocks,
                   'aggregation_weights.csv': aggregation_weights(
                       totals, training_quota(records), scientific_run.groups_of(cfg)),
                   'contrasts.csv': contrasts, 'seed_summaries.csv': seed_summaries(contrasts),
                   'sensitivity_pairs.csv': sensitivity_pairs(contrasts),
                   'model_diagnostics.csv': model_diagnostics(records),
                   'arm_diagnostics.csv': arm_diagnostics(records)})
    steps.append(6)
    if sorted(tables) != sorted(TABLES):
        raise ValueError(f'report: {sorted(set(tables) ^ set(TABLES))} is not a declared table')
    checks = {'steps': steps, 'scientific': scientific, 'reported_partitions': len(records),
              'positional_partitions': len(positional),
              'r1_pairs': int(len(tables['jsd_pairs.csv']))}
    body = {'keys': prior['keys'], 'checks': checks, 'evidence': prior['evidence'],
            'metadata': scientific_run.stage_metadata('report', corpus_dir=args.corpus_dir,
                                                      output_dir=args.output_dir, started=started)}
    manifest = scientific_run.publish_stage(args.output_dir, 'report', tables, contract, body,
                                            corpus_dir=args.corpus_dir)
    scientific_run.validate_run(args.output_dir)
    return manifest


if __name__ == '__main__':
    main()
