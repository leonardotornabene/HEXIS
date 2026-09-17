"""The parameterized executor of the six cells: two arms, one partition per pair (§11.4, §14.1).

One sample feeds both arms of a fold, the two models are fitted from it, the
coupled slots are scored once, and the pair is written before the models are
released. Positional vectors are persisted for C0 alone (§11.4); every cell
persists the document/band sums that documents, blocks and groups are
reconstructed from (§11.5).

`--resume` re-uses a partition only through `scientific_run.validate_run`: same
identity, same bytes, same schema, same cardinality and same keys, under the same
contract and the same code (§11.7).
"""

import argparse
import time
from pathlib import Path

from hexis.contracts import compare, digest
from hexis.model.context_tree import CTW, CTWParams
from hexis.pipeline import scientific_run
from hexis.protocols import sampling, scores

POSITION_CELL = 'C0'  # §11.4: positional persistence in C0 alone


def available_tokens(sequences, blocks, variant) -> dict:
    """Encoded primary tokens each block can contribute to a training sample (§5.2)."""
    frame = sequences[sequences['variant'].eq(variant) & sequences['role'].eq('primary')]
    kept = frame.groupby(frame['doc_id'].astype(str))['encoded_length'].sum()
    return {name: int(sum(int(kept.get(doc, 0)) for doc in docs)) for name, docs in blocks.items()}


def run_pair(cfg, frames, cell, held, seed):
    """One (cell, fold, seed): sample once, fit both arms, score the coupled slots.

    Returns the pair record of §11.4–§11.5 and, for C0, the positional frame.
    """
    if list(cell['arms']) != list(scores.ARMS):
        raise ValueError(f"cell {cell['id']}: arms {list(cell['arms'])} — the design fits "
                         f'{list(scores.ARMS)}')
    blocks, keys = scientific_run.blocks_of(cfg), scientific_run.block_keys_of(cfg)
    variant, depth, held_key = cell['variant'], int(cell['D']), keys[held]
    sequences = frames['sequences.parquet']
    ledger = sampling.sample_fold(sequences, variant=variant, blocks=blocks, held_block=held,
                                  q=cell['q'], seed=seed)
    train = {'original': sampling.sample_streams(ledger, sequences, variant)}
    train['shuffled'] = sampling.shuffle_streams(train['original'], seed=seed, held=held_key,
                                                 purpose='shuffle_train')
    evaluated = {'original': sampling.evaluation_streams(sequences, variant=variant,
                                                         docs=blocks[held], block=held_key)}
    evaluated['shuffled'] = sampling.shuffle_streams(evaluated['original'], seed=seed,
                                                     held=held_key, purpose='shuffle_eval')
    params = CTWParams.from_rho(m=int(cell['m']), depth=depth, a=cell['a_per_symbol'],
                                rho=cell['rho'])
    models = {arm: CTW(params).fit([stream['symbols'] for stream in train[arm]])
              for arm in scores.ARMS}
    positions, arms = scores.pooled_score_core(evaluated['original'], evaluated['shuffled'],
                                           model_original=models['original'],
                                           model_shuffled=models['shuffled'],
                                           min_available_past=cfg['min_available_past'])
    coordinates = frames['coordinates.parquet']
    eligible = coordinates[coordinates['variant'].eq(variant)
                           & coordinates['doc_id'].astype(str).isin(blocks[held])
                           & coordinates['eligible'].astype(bool)]
    # §11.5 applies to every cell before the sensitivity vectors are discarded.
    scores.pair_positions(positions[['slot_uid']], eligible[['slot_uid']])
    frame = sequences[sequences['variant'].eq(variant)]
    documents = dict(zip(frame['sent_id'].astype(str), frame['doc_id'].astype(str)))
    positions = positions.assign(doc_id=positions['sent_id'].map(documents))
    arms = arms.assign(doc_id=arms['sent_id'].map(documents))
    if positions['doc_id'].isna().any() or arms['doc_id'].isna().any():
        raise ValueError(f'{held}: a scored sentence has no document in variant {variant!r}')
    sums = scores.aggregate(positions, keys=['doc_id'])
    # §11.5: the §9.3 summaries are kept per document, like the loss sums beside them — summing
    # the document dimension away here would lose it for good (§14.3, 1.540 logical rows).
    arm_sums = (arms.drop(columns=['sent_id']).groupby(['doc_id', 'arm', 'past_band'], sort=True,
                                                       as_index=False).sum())
    lengths = ledger.assign(tokens=ledger['end'] - ledger['start'])
    training = lengths.groupby(['block', 'block_key'], sort=True, as_index=False).agg(
        streams=('sent_id', 'size'), tokens=('tokens', 'sum'))
    pool = available_tokens(sequences, blocks, variant)
    training['available'] = [pool[name] for name in training['block']]
    sample_ledger = scientific_run.records(ledger)
    record = {
        'cell': cell['id'], 'variant': variant, 'held_block': held, 'held_block_key': held_key,
        'seed': int(seed), 'q': int(cell['q']), 'depth': depth, 'm': int(cell['m']),
        'a_per_symbol': float(cell['a_per_symbol']), 'rho': float(cell['rho']),
        'min_available_past': int(cfg['min_available_past']), 'arms': list(scores.ARMS),
        'ledger_sha256': digest(sample_ledger), 'sample_ledger': sample_ledger,
        'ledger_rows': int(len(ledger)),
        'training': scientific_run.records(training),
        'fragments': scientific_run.records(sampling.fragment_metrics(ledger, depth)),
        'shuffle': {population: {'changed_count': sum(s['changed_count'] for s in streams),
                                 'total_count': sum(s['total_count'] for s in streams)}
                    for population, streams in (('training', train['shuffled']),
                                                ('evaluation', evaluated['shuffled']))},
        'models': {arm: {'fingerprint': models[arm].fingerprint(),
                         'training_streams': len(train[arm]),
                         'training_tokens': sum(len(s['symbols']) for s in train[arm]),
                         **models[arm].diagnostics()} for arm in scores.ARMS},
        'document_sums': scientific_run.records(sums),
        'arm_diagnostics': scientific_run.records(arm_sums),
        'positions': (scientific_run.positions_name(cell['id'], held_key, int(seed))
                      if cell['id'] == POSITION_CELL else None)}
    vectors = (positions[list(scores.POSITION_COLUMNS)].reset_index(drop=True)
               if cell['id'] == POSITION_CELL else None)
    return scientific_run.plain(record), vectors


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='HEXIS 3.1 descriptive campaign: six cells, two arms, one partition per pair')
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--corpus-dir', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--cell', default='all', help="'all' or one declared cell id")
    parser.add_argument('--seed', type=int, choices=(0,),
                        help='select only the declared seed 0 for the incomplete V3 trial')
    parser.add_argument('--resume', action='store_true',
                        help='re-use validated partitions of the same identity (§11.7)')
    parser.add_argument('--fixture', action='store_true',
                        help='declare a synthetic configuration; refuses the deposited projection')
    args = parser.parse_args(argv)
    started = time.perf_counter()
    cfg, _ = scientific_run.load_projection(args.config, args.fixture)
    cells = scientific_run.select_cells(cfg, args.cell)
    if args.seed is not None:
        missing = [cell['id'] for cell in cells if args.seed not in cell['seeds']]
        if missing:
            raise ValueError(f'seed {args.seed} is not declared for cells {missing}')
    scientific_run.check_destination(args.output_dir, args.corpus_dir)
    corpus, frames = scientific_run.load_corpus(args.corpus_dir)
    contract = scientific_run.run_contract(cfg, corpus)
    evidence = scientific_run.evidence(contract, args.corpus_dir, corpus)
    prior = scientific_run.read_prior(args.output_dir)
    scientific_run.check_stage_open(args.output_dir, 'descriptive', prior, args.resume)
    if prior:
        compare(contract, prior['run_contract'], 'run_contract')
        compare(evidence, prior['evidence'], 'evidence')
    resumable = {tuple(key) for key in prior['keys']['pair']} if prior else set()
    blocks = scientific_run.block_keys_of(cfg)
    keys = {'pair': [], 'model': []}
    selected = [(cell, held, seed) for cell in cells for held in sorted(blocks)
                for seed in cell['seeds'] if args.seed is None or seed == args.seed]
    reused = sum((cell['id'], blocks[held], int(seed)) in resumable
                 for cell, held, seed in selected)
    checks = {'reused_partitions': reused, 'published_partitions': 0, 'new_model_fits': 0,
              'positions_cell': POSITION_CELL,
              'cells': sorted({cell['id'] for cell in cells} | set(
                  prior['checks'].get('cells', []) if prior else []))}
    manifest = prior

    def publish(artifacts):
        body = {'keys': scientific_run.union_keys(manifest, keys), 'checks': checks,
                'evidence': evidence,
                'metadata': scientific_run.stage_metadata(
                    'descriptive', corpus_dir=args.corpus_dir, output_dir=args.output_dir,
                    started=started, selection=args.cell, seed=args.seed, resume=args.resume)}
        return scientific_run.publish_stage(
            args.output_dir, 'descriptive', artifacts, contract, body,
            resume=args.resume or manifest is not None, corpus_dir=args.corpus_dir)

    for cell, held, seed in selected:
        key = [cell['id'], blocks[held], int(seed)]
        if tuple(key) in resumable:
            continue
        record, vectors = run_pair(cfg, frames, cell, held, seed)
        ledger = record['sample_ledger']
        record['sample_ledger'] = scientific_run.ledger_name(record['ledger_sha256'])
        artifacts = {scientific_run.pair_name(*key): record, record['sample_ledger']: ledger}
        if vectors is not None:
            artifacts[scientific_run.positions_name(*key)] = vectors
        keys['pair'].append(key)
        keys['model'].extend([*key, arm] for arm in cell['arms'])
        checks['published_partitions'] += 1
        checks['new_model_fits'] += len(cell['arms'])
        # §11.4: publish each pair before fitting the next; keep only one vector in memory.
        # ponytail: publication revalidates prior artifacts; optimize only after V3 measurements.
        manifest = publish(artifacts)
        del artifacts, record, vectors, ledger
    if not checks['published_partitions']:
        manifest = publish({})
    scientific_run.validate_run(args.output_dir)
    return manifest


if __name__ == '__main__':
    main()
