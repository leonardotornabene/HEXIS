"""Recomputation of a seed-0 run from the deposited contract, without importing hormathos.

Reconstructed for the V3-005 re-attestation (the review's script was lost with its
scratchpad). Sources: plan §4.4, §5.1–§5.3, §6.4, §7, §8.1, §11.4, §12.2 and the
deposited design JSON. Reads the V1 corpus and the run directories; fits nothing.
Every sum runs over sorted keys, so no result depends on set or dict order.
G_R is printed per pair; exact zeros are not counted (R11).

Usage: python indep_check.py REPO RUN_DIR [RUN_DIR ...]
"""
import hashlib, json, math, sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(sys.argv[1]).resolve()
RUNS = [Path(p) for p in sys.argv[2:]]
DESIGN = json.loads((REPO/'docs/contracts/hexis-3.1/HEXIS_allegati_v3.1_2026-09-15/'
                     'hexis_v3.1_design.json').read_text())
RNG = DESIGN['rng']
PROBLEMS = []
ROOT_TOL = 1e-6   # root loss sums recomputed in another summation order (bits)


def check(label, ok, detail=''):
    if not ok:
        PROBLEMS.append(f'{label}: {detail}')
        print(f'  PROBLEM {label}: {detail}')
    return ok


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def block_key(docs):
    return hashlib.sha256(canonical(sorted(docs))).hexdigest()


def derived(purpose, *, seed, held, block, sid='', start=0, end=0):
    payload = {'version': RNG['version'], 'master': RNG['master_seed'], 'seed': seed, 'held': held,
               'block': block, 'purpose': purpose, 'sid': sid, 'start': start, 'end': end}
    return int.from_bytes(hashlib.sha256(canonical(payload)).digest()[:16], 'big')


def rng(seed):
    return np.random.Generator(np.random.PCG64(seed))


def sample_block(rows, q, *, seed, held, block):
    """§5.2 steps 1–5; rows already in canonical order (step 1)."""
    ledger, residual = [], q
    subseed = derived('sample', seed=seed, held=held, block=block)
    for index in rng(subseed).permutation(len(rows)):
        sid, length = rows[int(index)]
        if length == 0:
            continue
        if length <= residual:
            start, end, fragment_subseed = 0, length, ''
        else:
            fragment_subseed = derived('fragment', seed=seed, held=held, block=block, sid=sid)
            start = int(rng(fragment_subseed).integers(0, length - residual + 1))
            end = start + residual
            fragment_subseed = str(fragment_subseed)
        ledger.append({'block_key': block, 'held': held, 'seed': seed, 'sent_id': sid, 'start': start,
                       'end': end, 'fragment': end - start < length,
                       'sample_subseed': str(subseed), 'fragment_subseed': fragment_subseed})
        residual -= end - start
        if residual == 0:
            break
    return ledger, subseed


def fixture():
    """§12.2 artificial vector."""
    f = RNG['sample_fixture']
    held, block = block_key(f['held_members']), block_key(f['block_members'])
    check('fixture held key', held == 'e7b28f6b342cb9fe4fe171f6f02275c1de5349f73462a8709b4e0679a332ab99', held)
    check('fixture block key', block == 'b074a6afd500bbf0891340a1cdda223c1516d7bb52518b820848e1d29d12788a', block)
    seed = derived('sample', seed=f['seed'], held=held, block=block)
    check('fixture derived seed', seed == f['derived_seed'], seed)
    perm = rng(seed).permutation(6).tolist()
    check('fixture permutation(6)', perm == f['permutation_6'], perm)
    rows = [(f'fixture@{i}', n) for i, n in enumerate(f['lengths'], 1)]
    ledger, _ = sample_block(rows, f['q'], seed=f['seed'], held=held, block=block)
    got = [{'sid': r['sent_id'], 'start': r['start'], 'end': r['end']} for r in ledger]
    check('fixture ledger', got == f['ledger'], got)
    check('fixture fragments', [r['fragment'] for r in ledger] == [False, False, False, True])
    check('fixture fragment subseed @2', ledger[-1]['fragment_subseed'] == '46436027119566646866315332695474949224',
          ledger[-1]['fragment_subseed'])
    print(f'fixture §12.2: keys, derived seed {seed}, permutation {perm}, ledger {got} checked')


def load_corpus():
    manifest = json.loads((REPO/'results/hexis31/v1/manifest.json').read_text())
    for name in ('sequences.parquet',):
        sha = hashlib.sha256((REPO/'results/hexis31/v1'/name).read_bytes()).hexdigest()
        check(f'V1 {name} sha256', sha == manifest['artifacts'][name]['sha256'], sha)
    seq = pd.read_parquet(REPO/'results/hexis31/v1/sequences.parquet')
    for column in ('variant', 'role', 'doc_id', 'sent_id'):
        seq[column] = seq[column].astype(str)
    seq = seq[seq['role'] == 'primary']
    corpus = {}
    for variant, frame in seq.groupby('variant'):
        frame = frame.sort_values(['doc_id', 'part_order', 'source_ordinal', 'sent_id'])
        corpus[variant] = {row.sent_id: {'doc': row.doc_id, 'symbols': [int(x) for x in row.symbols],
                                         'slots': [int(x) for x in row.slot_uids],
                                         'length': int(row.encoded_length)}
                           for row in frame.itertuples(index=False)}
        order = defaultdict(list)
        for row in frame.itertuples(index=False):
            order[row.doc_id].append(row.sent_id)
        corpus[variant]['__order__'] = order
    return corpus


def block_rows(corpus, variant, docs):
    """Canonical order across the block's documents (§5.2 step 1)."""
    order = corpus[variant]['__order__']
    sids = [sid for doc in sorted(docs) for sid in order.get(doc, [])]
    return [(sid, corpus[variant][sid]['length']) for sid in sids]


def band(j):
    return '4_7' if j < 8 else 'ge8'


def eligible_totals(corpus):
    minimum = DESIGN['min_available_past']
    for variant in ('ud23', 'ud23_oth', 'upos_only'):
        total = 0
        for block in DESIGN['blocks']:
            n = sum(max(0, length - minimum) for _, length in block_rows(corpus, variant, block['docs']))
            check(f'eligible {block["block"]}/{variant}', n == block['eligible'][variant], n)
            total += n
        expected = DESIGN['expected']['primary_eligible'][variant]
        check(f'eligible total {variant}', total == expected, total)
        print(f'eligible {variant}: {total} (design {expected})')


def recompute_pair(corpus, cell, held_name, seed):
    variant, q, D, m, a = cell['variant'], cell['q'], cell['D'], cell['m'], cell['a_per_symbol']
    sample_variant = 'ud23_oth' if variant == 'ud23_oth' else 'ud23'
    blocks = {b['block']: b for b in DESIGN['blocks']}
    held = block_key(blocks[held_name]['docs'])
    ledger = []
    for name in sorted(blocks):
        if name == held_name:
            continue
        key = block_key(blocks[name]['docs'])
        check(f'block key {name}', key == blocks[name]['block_key'], key)
        rows, _ = sample_block(block_rows(corpus, sample_variant, blocks[name]['docs']), q,
                               seed=seed, held=held, block=key)
        ledger.extend({'block': name, **row} for row in rows)
    data = corpus[variant]
    counts, train_changed, train_total = Counter(), 0, 0
    training = defaultdict(lambda: {'streams': 0, 'tokens': 0})
    for row in ledger:
        symbols = data[row['sent_id']]['symbols'][row['start']:row['end']]
        counts.update(symbols)
        training[row['block']]['streams'] += 1
        training[row['block']]['tokens'] += len(symbols)
        order = rng(derived('shuffle_train', seed=seed, held=held, block=row['block_key'],
                            sid=row['sent_id'], start=row['start'], end=row['end'])).permutation(len(symbols))
        train_changed += sum(symbols[int(i)] != s for i, s in zip(order, symbols))
        train_total += len(symbols)
    N = sum(counts.values())
    q0 = lambda x: (counts.get(x, 0) + a) / (N + m * a)
    docs = defaultdict(lambda: {'n': 0, 'root_o': [], 'root_r': [], 'changed': 0})
    positions, eval_changed, eval_total = [], 0, 0
    for sid in [s for doc in sorted(blocks[held_name]['docs']) for s in data['__order__'].get(doc, [])]:
        sentence = data[sid]
        symbols, slots = sentence['symbols'], sentence['slots']
        order = rng(derived('shuffle_eval', seed=seed, held=held, block=held, sid=sid, start=0,
                            end=len(symbols))).permutation(len(symbols))
        moved = [symbols[int(i)] for i in order]
        origin = [slots[int(i)] for i in order]
        eval_changed += sum(x != y for x, y in zip(symbols, moved))
        eval_total += len(symbols)
        for j in range(DESIGN['min_available_past'], len(symbols)):
            d = docs[(sentence['doc'], band(j))]
            d['n'] += 1
            d['root_o'].append(-math.log2(q0(symbols[j])))
            d['root_r'].append(-math.log2(q0(moved[j])))
            d['changed'] += symbols[j] != moved[j]
            positions.append((slots[j], symbols[j], moved[j], origin[j], sentence['doc'], band(j),
                              -math.log2(q0(symbols[j])), -math.log2(q0(moved[j]))))
    fragments = {}
    for name in sorted(training):
        cut = [r for r in ledger if r['block'] == name and r['fragment']]
        internal = [r['end'] - r['start'] for r in cut if r['start'] > 0]
        fragments[name] = {'fragment_count': len(cut), 'internal_start_count': len(internal),
                           'fragment_tokens': sum(r['end'] - r['start'] for r in cut),
                           'direct_context_targets': sum(min(D, n) for n in internal)}
    available = {name: sum(n for _, n in block_rows(corpus, variant, blocks[name]['docs']))
                 for name in training}
    return {'ledger': ledger, 'counts': counts, 'N': N, 'training': training, 'available': available,
            'fragments': fragments, 'docs': docs, 'positions': positions,
            'shuffle': {'training': (train_changed, train_total), 'evaluation': (eval_changed, eval_total)},
            'held': held}


def check_run(run, corpus):
    print(f'== {run}')
    manifest_bytes = (run/'manifest.json').read_bytes()
    print(f' manifest_sha256 {hashlib.sha256(manifest_bytes).hexdigest()}')
    manifest = json.loads(manifest_bytes)
    print(f' run_id {manifest["run_id"]}')
    for name, record in sorted(manifest['artifacts'].items()):
        sha = hashlib.sha256((run/name).read_bytes()).hexdigest()
        got = record['sha256'] if isinstance(record, dict) else record
        check(f'artifact sha {name}', sha == got, sha)
    cells = {c['id']: c for c in DESIGN['cells']}
    pairs = sorted(run.glob('pair__*__s0.json'))
    check('pair count', len(pairs) == DESIGN['expected']['technical_pairs'], len(pairs))
    probes = sum(1 for p in pairs + [run/'manifest.json'] if 'probe' in p.read_text())
    check('zero probe', probes == 0, probes)
    ledgers_seen, c0_rows, gr = set(), 0, []
    per_cell = Counter()
    eligible_by_cell = defaultdict(int)
    for path in pairs:
        pair = json.loads(path.read_text())
        cell = cells[pair['cell']]
        per_cell[pair['cell']] += 1
        label = f'{pair["cell"]}/{pair["held_block"]}'
        for field in ('variant', 'q', 'm', 'a_per_symbol', 'rho'):
            check(f'{label} {field}', pair[field] == cell[field], pair[field])
        check(f'{label} depth', pair['depth'] == cell['D'], pair['depth'])
        r = recompute_pair(corpus, cell, pair['held_block'], pair['seed'])
        check(f'{label} held key', pair['held_block_key'] == r['held'], pair['held_block_key'])
        # ledger (§5.2): same rows, compared by key; order across blocks is not contractual
        persisted = json.loads((run/pair['sample_ledger']).read_text())
        # the ledger hash is SHA-256 of the canonical JSON of its rows, and names the file
        # (V3-002 deviation 4); not the hash of the file bytes
        sha = hashlib.sha256(canonical(persisted)).hexdigest()
        check(f'{label} ledger sha', sha == pair['ledger_sha256'] and
              pair['sample_ledger'] == f'sample_ledger__{sha}.json', sha)
        fields = ('block', 'block_key', 'held', 'seed', 'sent_id', 'start', 'end', 'fragment',
                  'sample_subseed', 'fragment_subseed')
        key = lambda row: (row['block_key'], row['sent_id'])
        mine = sorted((tuple(row[f] for f in fields) for row in r['ledger']))
        theirs = sorted((tuple(row[f] for f in fields) for row in persisted))
        check(f'{label} ledger rows', mine == theirs, f'{len(mine)} vs {len(theirs)}')
        check(f'{label} ledger_rows', pair['ledger_rows'] == len(mine), pair['ledger_rows'])
        ledgers_seen.add(pair['sample_ledger'])
        # training and fragment metrics (§5.1, §5.2)
        for row in pair['training']:
            t = r['training'][row['block']]
            check(f'{label} training {row["block"]}',
                  (row['streams'], row['tokens'], row['available']) ==
                  (t['streams'], t['tokens'], r['available'][row['block']]), row)
            check(f'{label} tokens q', row['tokens'] == cell['q'], row['tokens'])
        check(f'{label} training blocks', sorted(x['block'] for x in pair['training']) == sorted(r['training']))
        for row in pair['fragments']:
            want = r['fragments'][row['block']]
            check(f'{label} fragments {row["block"]}', all(row[k] == v for k, v in want.items()), (row, want))
        # shuffle counts (§7)
        for population in ('training', 'evaluation'):
            got = (pair['shuffle'][population]['changed_symbol_slot_count'],
                   pair['shuffle'][population]['total_slot_count'])
            check(f'{label} shuffle {population}', got == r['shuffle'][population], (got, r['shuffle'][population]))
        # root q0 from training counts (§6.4), both arms
        observed = len(r['counts'])
        for arm in ('original', 'shuffled'):
            model = pair['models'][arm]
            check(f'{label} {arm} root observed', model['root_observed_symbol_count'] == observed,
                  model['root_observed_symbol_count'])
            check(f'{label} {arm} root unseen', model['root_unseen_symbol_count'] == cell['m'] - observed)
            check(f'{label} {arm} training tokens', model['training_tokens'] == r['N'], model['training_tokens'])
            check(f'{label} {arm} training streams', model['training_streams'] == len(r['ledger']))
        sums = {(row['doc_id'], row['past_band']): row for row in pair['document_sums']}
        check(f'{label} doc/band keys', sorted(sums) == sorted(r['docs']), sorted(sums))
        n_total = s_root_r = s_ctw_r = 0.0
        for k in sorted(r['docs']):
            want, row = r['docs'][k], sums.get(k)
            if row is None:
                continue
            check(f'{label} {k} n', row['n'] == want['n'] == row['eligible_slot_count'], row['n'])
            check(f'{label} {k} changed', row['changed_symbol_eligible_slot_count'] == want['changed'])
            for field, values in (('sum_loss_root_original', want['root_o']), ('sum_loss_root_shuffled', want['root_r'])):
                total = math.fsum(values)
                check(f'{label} {k} {field}', abs(row[field] - total) <= ROOT_TOL, (row[field], total))
            n_total += row['n']
            s_root_r += row['sum_loss_root_shuffled']
            s_ctw_r += row['sum_loss_ctw_shuffled']
        eligible_by_cell[pair['cell']] += int(n_total)
        gr.append((pair['cell'], pair['held_block'], (s_root_r - s_ctw_r) / n_total))
        # C0 positions (§11.4)
        if pair['cell'] == 'C0':
            frame = pd.read_parquet(run/pair['positions'])
            c0_rows += len(frame)
            want = sorted(r['positions'])
            got = frame.sort_values('slot_uid')
            check(f'{label} positions slots', got['slot_uid'].tolist() == [p[0] for p in want])
            for column, index in (('original_symbol_id', 1), ('shuffled_symbol_id', 2),
                                  ('shuffled_origin_slot_uid', 3)):
                check(f'{label} positions {column}', got[column].tolist() == [p[index] for p in want])
            for column, index in (('loss_root_original', 6), ('loss_root_shuffled', 7)):
                diff = float(np.max(np.abs(got[column].to_numpy() - np.array([p[index] for p in want]))))
                check(f'{label} positions {column}', diff <= 1e-9, diff)
            # the partition reconstructs the persisted document sums, all four losses
            by_key = defaultdict(lambda: defaultdict(list))
            losses = got.set_index('slot_uid')
            for p in want:
                for column in ('loss_ctw_original', 'loss_root_original', 'loss_ctw_shuffled', 'loss_root_shuffled'):
                    by_key[(p[4], p[5])][column].append(float(losses.at[p[0], column]))
            for k in sorted(by_key):
                for column, values in sorted(by_key[k].items()):
                    total = math.fsum(values)
                    check(f'{label} {k} positions→{column}', abs(sums[k]['sum_' + column] - total) <= 1e-6,
                          (sums[k]['sum_' + column], total))
    check('cells', dict(per_cell) == {c: 7 for c in cells}, dict(per_cell))
    check('ledger files', len(ledgers_seen) == 21 and len(list(run.glob('sample_ledger__*.json'))) == 21,
          len(ledgers_seen))
    check('C0 position rows', c0_rows == DESIGN['expected']['primary_eligible']['ud23'], c0_rows)
    for cell in sorted(eligible_by_cell):
        variant = cells[cell]['variant']
        check(f'eligible pairs {cell}', eligible_by_cell[cell] == DESIGN['expected']['primary_eligible'][variant],
              eligible_by_cell[cell])
    print(f' pairs {len(pairs)} cells {dict(sorted(per_cell.items()))} ledgers {len(ledgers_seen)} '
          f'C0 position rows {c0_rows}')
    print(f' eligible per cell over 7 folds {dict(sorted(eligible_by_cell.items()))}; probe evaluations {probes}')
    print(' G_R = CE_0^R - CE_CTW^R per pair (bits/target):')
    for cell, held, value in sorted(gr):
        print(f'  {cell:9s} {held:20s} {value:.6e}')


def main():
    fixture()
    corpus = load_corpus()
    eligible_totals(corpus)
    for run in RUNS:
        check_run(run, corpus)
    check('hormathos not imported', 'hormathos' not in sys.modules)
    print(f'PROBLEMS {len(PROBLEMS)}')
    return 1 if PROBLEMS else 0


if __name__ == '__main__':
    sys.exit(main())
