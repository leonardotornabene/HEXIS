"""V2 sampling protocol: exact budget, ledger, RNG identity and the coupled shuffle.

`derive` below is a second, deliberately plain implementation of the §5.3
convention (hashlib and json only) used as the oracle for T08; it shares no code
with ``hormathos.protocols.sampling``. The §12.2 vector and the seven deposited
block keys are reproduced through it before any value of the module is trusted.
"""
import ast
import hashlib
import json
from collections import Counter
from itertools import chain
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from hormathos.config import load_v31_config
from hormathos.contracts import load_contracts
from hormathos.corpus import build_corpus
from hormathos.protocols import sampling

pytestmark = pytest.mark.v31

ROOT = Path(__file__).resolve().parents[1]
DESIGN = load_contracts()['design']
BLOCKS = {block['block']: block['docs'] for block in DESIGN['blocks']}
CELLS = {cell['id']: cell for cell in DESIGN['cells']}
FIXTURE = DESIGN['rng']['sample_fixture']
HELD_KEY = 'e7b28f6b342cb9fe4fe171f6f02275c1de5349f73462a8709b4e0679a332ab99'
FIXTURE_KEY = 'b074a6afd500bbf0891340a1cdda223c1516d7bb52518b820848e1d29d12788a'
PLUTARCH = sampling.block_key(BLOCKS['PLUTARCH'])
COLUMNS = ['variant', 'doc_id', 'sent_id', 'part_order', 'source_ordinal', 'regime', 'role',
           'dependence_block', 'group', 'encoded_length', 'symbols', 'slot_uids']


# --- independent derivator (T08) ----------------------------------------------

def derive(purpose, seed=0, held=HELD_KEY, block=FIXTURE_KEY, sid='', start=0, end=0):
    """§5.3 by hand: nine fields, canonical JSON, first 16 SHA-256 bytes big endian."""
    payload = {'version': 'hexis-v3-rng-1', 'master': 20260706, 'seed': seed, 'held': held,
               'block': block, 'purpose': purpose, 'sid': sid, 'start': start, 'end': end}
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return int.from_bytes(hashlib.sha256(text.encode('utf-8')).digest()[:16], 'big')


def canonical(rows):
    return sorted(rows, key=lambda row: (row['doc_id'], row['part_order'], row['source_ordinal'], row['sent_id']))


def oracle(rows, q, *, held, block, seed=0):
    """§5.2 steps 1–4 transcribed by hand: canonical order, drawn order, fragment offset."""
    ordered, ledger, residual = canonical(rows), [], q
    for index in np.random.Generator(np.random.PCG64(
            derive('sample', seed=seed, held=held, block=block))).permutation(len(ordered)):
        row = ordered[int(index)]
        length = int(row['encoded_length'])
        if length == 0:
            continue
        if length <= residual:
            start, end = 0, length
        else:
            start = int(np.random.Generator(np.random.PCG64(derive(
                'fragment', seed=seed, held=held, block=block, sid=row['sent_id']))
            ).integers(0, length - residual + 1))
            end = start + residual
        ledger.append({'sid': row['sent_id'], 'start': start, 'end': end})
        residual -= end - start
        if residual == 0:
            break
    return ledger


# --- fixtures -----------------------------------------------------------------

def frame(lengths, doc='fixture', role='primary', first_slot=0, first_ordinal=1):
    """A minimal sequences frame: one document, one sentence per length given."""
    rows, slot = [], first_slot
    for ordinal, length in enumerate(lengths, start=first_ordinal):
        rows.append({'variant': 'ud23', 'doc_id': doc, 'sent_id': f'{doc}@{ordinal}', 'part_order': 0,
                     'source_ordinal': ordinal, 'regime': 'HEX', 'role': role, 'dependence_block': doc,
                     'group': 'HEX', 'encoded_length': length,
                     'symbols': [(ordinal * 10 + index) % 100 for index in range(length)],
                     'slot_uids': list(range(slot, slot + length))})
        slot += length
    return pd.DataFrame(rows, columns=COLUMNS)


FIXTURE_FRAME = frame(FIXTURE['lengths'])
FIXTURE_BLOCKS = {'fixture': ['fixture'], 'held': ['held']}


def fixture_fold(sequences=FIXTURE_FRAME, blocks=FIXTURE_BLOCKS, q=FIXTURE['q'], seed=0):
    return sampling.sample_fold(sequences, variant='ud23', blocks=blocks, held_block='held', q=q, seed=seed)


def stream(symbols, sid='x@1', block=FIXTURE_KEY):
    return {'sent_id': sid, 'block_key': block, 'start': 0, 'end': len(symbols),
            'symbols': list(symbols), 'slot_uids': list(range(len(symbols)))}


@pytest.fixture(scope='module')
def corpus():
    root = ROOT / 'data/raw/UD_Ancient_Greek-Perseus'
    return build_corpus(sorted(root.glob('*.conllu')), load_v31_config(), load_contracts())


@pytest.fixture(scope='module')
def sequences(corpus):
    return corpus['sequences.parquet']


@pytest.fixture(scope='module')
def fold(sequences):
    """C0, seed 0, Plutarch held out — the fold the ledger and stream tests reuse."""
    return sampling.sample_fold(sequences, variant='ud23', blocks=BLOCKS,
                                held_block='PLUTARCH', q=CELLS['C0']['q'], seed=0)


@pytest.fixture(scope='module')
def arms(fold, sequences):
    original = sampling.sample_streams(fold, sequences, 'ud23')
    return original, sampling.shuffle_streams(original, seed=0, held=PLUTARCH, purpose='shuffle_train')


# --- T08: RNG identity --------------------------------------------------------

def test_pinned_rng_vector_and_fixture_ledger_reproduce_the_deposit():
    assert sampling.block_key(['held']) == HELD_KEY
    assert sampling.block_key(['fixture']) == FIXTURE_KEY
    assert sampling.block_key(['b', 'a']) == sampling.block_key(['a', 'b'])  # membership, not order
    assert derive('sample') == FIXTURE['derived_seed']
    assert sampling.derived_seed('sample', seed=0, held=HELD_KEY, block=FIXTURE_KEY) == derive('sample')
    assert sampling.permutation(6, seed=0, held=HELD_KEY, block=FIXTURE_KEY).tolist() == FIXTURE['permutation_6']
    ledger = fixture_fold()
    assert [{'sid': row.sent_id, 'start': row.start, 'end': row.end}
            for row in ledger.itertuples(index=False)] == FIXTURE['ledger']
    assert ledger['fragment'].tolist() == [False, False, False, True]
    assert ledger['sample_subseed'].tolist() == [str(derive('sample'))] * 4
    assert ledger['fragment_subseed'].tolist() == ['', '', '', str(derive('fragment', sid='fixture@2'))]
    assert derive('fragment', sid='fixture@2') == 46436027119566646866315332695474949224


def test_deposited_block_keys_recompute_from_their_member_lists():
    assert len(DESIGN['blocks']) == 7
    for block in DESIGN['blocks']:
        assert sampling.block_key(block['docs']) == block['block_key'], block['block']
        assert hashlib.sha256(json.dumps(sorted(block['docs']), ensure_ascii=False, sort_keys=True,
                                         separators=(',', ':')).encode()).hexdigest() == block['block_key']
    assert {block['block_key'] for block in DESIGN['blocks']} == set(DESIGN['validation']['replication']['held_blocks'])


def test_purposes_fields_repeatability_and_no_active_shuffle_probe():
    assert sampling.PURPOSES == ('sample', 'fragment', 'shuffle_train', 'shuffle_eval')
    with pytest.raises(ValueError, match='purpose'):
        sampling.derived_seed('shuffle_probe', seed=0, held=HELD_KEY, block=FIXTURE_KEY, sid='a@1')
    assert 'shuffle_probe' not in Path(sampling.__file__).read_text(encoding='utf-8')
    base = dict(seed=0, held=HELD_KEY, block=FIXTURE_KEY, sid='fixture@2', start=0, end=5)
    seeds = {purpose: sampling.derived_seed(purpose, **base) for purpose in sampling.PURPOSES}
    assert len(set(seeds.values())) == 4  # the four active purposes never share a stream
    assert all(seeds[purpose] == derive(purpose, **base) for purpose in seeds)
    assert sampling.derived_seed('sample', **base) == seeds['sample']  # repeatable
    for field, other in [('seed', 1), ('held', FIXTURE_KEY), ('block', HELD_KEY),
                         ('sid', 'fixture@3'), ('start', 1), ('end', 6)]:
        assert sampling.derived_seed('shuffle_train', **(base | {field: other})) != seeds['shuffle_train']
    for excluded in ('variant', 'cell', 'q', 'D', 'a', 'rho', 'group', 'regime'):
        with pytest.raises(TypeError):  # §5.3: nothing else may enter the derivation
            sampling.derived_seed('sample', **(base | {excluded: 1}))
    for bad in ('PLUTARCH', '', 'ab' * 31, HELD_KEY.upper()):
        with pytest.raises(ValueError, match='key'):
            sampling.derived_seed('sample', seed=0, held=bad, block=FIXTURE_KEY)
    assert isinstance(sampling.generator('sample', seed=0, held=HELD_KEY,
                                         block=FIXTURE_KEY).bit_generator, np.random.PCG64)


def test_one_sample_feeds_both_arms_and_each_sentence_shuffles_independently(arms, sequences):
    original, shuffled = arms
    assert len(shuffled) == len(original) > 0
    for before, after in zip(original, shuffled):  # both arms share the sampled coordinates
        assert (after['sent_id'], after['start'], after['end']) == (before['sent_id'], before['start'], before['end'])
    repeat = sampling.shuffle_streams(original, seed=0, held=PLUTARCH, purpose='shuffle_train')
    assert [item['symbols'] for item in repeat] == [item['symbols'] for item in shuffled]
    long_enough = [index for index, item in enumerate(original) if len(item['symbols']) > 10]
    for index in (0, long_enough[0], len(original) - 1):  # no shared generator across streams
        alone = sampling.shuffle_streams([original[index]], seed=0, held=PLUTARCH, purpose='shuffle_train')
        assert alone[0]['symbols'] == shuffled[index]['symbols']
    other_seed = sampling.shuffle_streams(original, seed=1, held=PLUTARCH, purpose='shuffle_train')
    assert other_seed[long_enough[0]]['symbols'] != shuffled[long_enough[0]]['symbols']
    evaluation = sampling.evaluation_streams(sequences, variant='ud23', docs=BLOCKS['PLUTARCH'], block=PLUTARCH)
    assert len(evaluation) == 499
    assert sum(len(item['symbols']) for item in evaluation) == 8884
    assert {item['start'] for item in evaluation} == {0}
    assert sampling.shuffle_streams(evaluation, seed=0, held=PLUTARCH, purpose='shuffle_eval')
    with pytest.raises(ValueError, match='shuffle_eval'):  # held and block must be the evaluated block
        sampling.shuffle_streams(original, seed=0, held=PLUTARCH, purpose='shuffle_eval')


# --- T05: exclusion -----------------------------------------------------------

def test_held_out_and_inventory_only_never_enter_any_cell_or_fold(sequences):
    inventory_only = set(sequences.loc[sequences['role'].eq('inventory_only'), 'doc_id'])
    assert len(inventory_only) == 6
    for cell in CELLS.values():
        for held in BLOCKS:
            ledger = sampling.sample_fold(sequences, variant=cell['variant'], blocks=BLOCKS,
                                          held_block=held, q=cell['q'], seed=0)
            assert set(ledger['block']) == set(BLOCKS) - {held}, (cell['id'], held)
            assert not set(ledger['doc_id']) & set(BLOCKS[held]), (cell['id'], held)
            assert not set(ledger['doc_id']) & inventory_only, (cell['id'], held)
            tokens = ledger.assign(n=ledger['end'] - ledger['start']).groupby('block')['n'].sum()
            assert tokens.eq(cell['q']).all(), (cell['id'], held)
    # inventory_only sentences leave the universe before the permutation: same member
    # list, same key, and therefore the pinned ledger unchanged — had they stayed in,
    # the universe would be eight sentences and the drawn order a different one
    pool = pd.concat([FIXTURE_FRAME, frame([9, 4], role='inventory_only', first_slot=99, first_ordinal=7)],
                     ignore_index=True)
    assert fixture_fold(sequences=pool).to_csv(index=False) == fixture_fold().to_csv(index=False)
    # and an inventory_only document contributes nothing even when listed as a member
    pool = pd.concat([FIXTURE_FRAME, frame([9], doc='shadow', role='inventory_only', first_slot=99)],
                     ignore_index=True)
    ledger = fixture_fold(sequences=pool, blocks={'fixture': ['fixture', 'shadow'], 'held': ['held']})
    assert 'shadow' not in set(ledger['doc_id'])
    assert int((ledger['end'] - ledger['start']).sum()) == FIXTURE['q']


# --- T06: budget --------------------------------------------------------------

def test_exact_budget_without_replacement_and_one_fragment_per_contributor(fold):
    assert len(set(fold['sent_id'])) == len(fold)  # no sentence is drawn twice
    assert (fold['end'] > fold['start']).all()
    for block, group in fold.groupby('block'):
        assert int((group['end'] - group['start']).sum()) == 8884, block
        assert int(group['fragment'].sum()) <= 1, block
        assert group['fragment'].tolist()[:-1] == [False] * (len(group) - 1), block
        assert (group.loc[~group['fragment'], 'start'] == 0).all(), block
    metrics = sampling.fragment_metrics(fold, depth=8)
    assert metrics['block'].tolist() == sorted(set(BLOCKS) - {'PLUTARCH'})
    assert metrics['fragment_count'].sum() == int(fold['fragment'].sum())
    assert (metrics['internal_start_count'] <= metrics['fragment_count']).all()
    assert (metrics['direct_context_targets'] <= 8 * metrics['internal_start_count']).all()
    cut = fold.loc[fold['fragment']]
    assert metrics['fragment_tokens'].sum() == int((cut['end'] - cut['start']).sum())


def test_empty_sentences_stay_in_the_universe_without_spending_budget():
    ledger = fixture_fold()
    assert 'fixture@3' not in set(ledger['sent_id'])  # the length-0 sentence is never a stream
    assert int((ledger['end'] - ledger['start']).sum()) == FIXTURE['q']
    without = sampling.sample_fold(frame([5, 8, 2, 7, 6]), variant='ud23', blocks=FIXTURE_BLOCKS,
                                   held_block='held', q=FIXTURE['q'], seed=0)
    assert without['sent_id'].tolist() != ledger['sent_id'].tolist()  # it still holds its place
    single = fixture_fold(sequences=frame([40]), q=17)  # one sentence longer than the whole budget
    assert single['fragment'].tolist() == [True]
    assert int(single.loc[0, 'end'] - single.loc[0, 'start']) == 17
    assert 0 <= int(single.loc[0, 'start']) <= 23
    exact = fixture_fold(q=28)  # a budget that exhausts the block takes everything and cuts nothing
    assert not exact['fragment'].any()
    assert set(exact['sent_id']) == {f'fixture@{ordinal}' for ordinal in (1, 2, 4, 5, 6)}


@pytest.mark.parametrize('block', sorted(set(BLOCKS) - {'PLUTARCH'}))
def test_canonical_order_and_fragment_offset_match_an_independent_transcription(sequences, fold, block):
    rows = sequences[sequences['variant'].eq('ud23') & sequences['role'].eq('primary')
                     & sequences['doc_id'].isin(BLOCKS[block])].to_dict('records')
    expected = oracle(rows, 8884, held=PLUTARCH, block=sampling.block_key(BLOCKS[block]))
    drawn = fold[fold['block'].eq(block)]
    assert [{'sid': row.sent_id, 'start': row.start, 'end': row.end}
            for row in drawn.itertuples(index=False)] == expected


def test_the_fragment_offset_can_reach_every_contiguous_segment():
    starts = {int(fixture_fold(sequences=frame([12]), q=5, seed=seed).loc[0, 'start']) for seed in range(60)}
    assert starts == set(range(8))  # 0..length-residual inclusive: the final suffix is reachable too


@pytest.mark.parametrize('case,q,lengths,docs,message', [
    ('over budget', 29, (5, 8, 0, 2, 7, 6), ['fixture'], 'exceeds'),
    ('only empty sentences', 1, (0, 0, 0), ['fixture'], 'exceeds'),
    ('no member sentence', 1, (5, 8), ['absent'], 'exceeds'),
    ('zero budget', 0, (5, 8), ['fixture'], 'positive'),
    ('negative budget', -1, (5, 8), ['fixture'], 'positive'),
])
def test_impossible_budgets_fail_explicitly(case, q, lengths, docs, message):
    with pytest.raises(ValueError, match=message) as error:
        fixture_fold(sequences=frame(lengths), blocks={'fixture': docs, 'held': ['held']}, q=q)
    assert str(q) in str(error.value), case


# --- T07: invariance ----------------------------------------------------------

def test_record_order_and_labels_do_not_change_the_ledger(sequences, fold):
    def ledger(frame):
        return sampling.sample_fold(frame, variant='ud23', blocks=BLOCKS, held_block='PLUTARCH',
                                    q=8884, seed=0).to_csv(index=False)

    reference = fold.to_csv(index=False)
    reordered = sequences.sample(frac=1.0, random_state=7)
    assert not reordered.index.equals(sequences.index)
    assert ledger(reordered) == reference
    # the canonical key of §5.2 step 1 is not the sentence identity: '@10' precedes
    # '@2' lexicographically, and one canonical document can carry several parts
    rows = sequences[sequences['variant'].eq('ud23') & sequences['role'].eq('primary')].to_dict('records')
    assert [row['sent_id'] for row in sorted(rows, key=lambda row: row['sent_id'])] != \
        [row['sent_id'] for row in canonical(rows)]
    # the sampler reads no regime, group or display label: drop them entirely
    assert ledger(sequences.drop(columns=['regime', 'group', 'dependence_block', 'source_prefix'])) == reference
    assert ledger(sequences.assign(regime='OTHER_VERSE', group='PROSE_ALL')) == reference
    with pytest.raises(ValueError, match='role'):  # but role and the coordinates are required
        ledger(sequences.drop(columns=['role']))


def test_declared_ledger_and_permutation_reuse_between_cells(sequences, fold):
    def ledger(cell):
        return sampling.sample_fold(sequences, variant=CELLS[cell]['variant'], blocks=BLOCKS,
                                    held_block='PLUTARCH', q=CELLS[cell]['q'], seed=0)

    reference = fold.to_csv(index=False)
    for cell in DESIGN['sampling']['ledger_reuse_C0']:  # same ledger, byte for byte
        assert ledger(cell).to_csv(index=False) == reference, cell
    for cell in DESIGN['sampling']['permutation_reuse_C0']:  # same order, own stop and own cut
        other = ledger(cell)
        assert other.to_csv(index=False) != reference, cell
        tokens = other.assign(n=other['end'] - other['start']).groupby('block')['n'].sum()
        assert tokens.eq(CELLS[cell]['q']).all(), cell
        for block, group in other.groupby('block'):
            shared = group['sent_id'].tolist()[:-1]
            assert shared == fold.loc[fold['block'].eq(block), 'sent_id'].tolist()[:len(shared)], (cell, block)
    # the shared order comes from the `sample` subseed alone; no cell parameter enters it
    key = sampling.block_key(BLOCKS['HERODOTUS'])
    assert sampling.permutation(1092, seed=0, held=PLUTARCH, block=key).tolist() == \
        sampling.permutation(1092, seed=0, held=PLUTARCH, block=key).tolist()


# --- T09: streams -------------------------------------------------------------

def test_streams_survive_the_parquet_round_trip_of_the_corpus_artifact(tmp_path):
    path = tmp_path / 'sequences.parquet'
    FIXTURE_FRAME.to_parquet(path)
    restored = pd.read_parquet(path)  # lists come back as arrays; the cut must not care
    assert not isinstance(restored['symbols'].iloc[0], list)
    assert sampling.sample_fold(restored, variant='ud23', blocks=FIXTURE_BLOCKS, held_block='held',
                                q=FIXTURE['q'], seed=0).to_csv(index=False) == fixture_fold().to_csv(index=False)
    # a categorical sorts by its category order, which the file's dictionary does
    # not have to agree with: the universe must follow the values regardless
    pool = pd.concat([frame([5, 8], doc='a'), frame([4, 7], doc='b', first_slot=13)], ignore_index=True)
    blocks = {'ab': ['a', 'b'], 'held': ['held']}
    reversed_categories = pool.astype({'doc_id': pd.CategoricalDtype(['b', 'a']), 'sent_id': 'category'})
    assert list(reversed_categories['doc_id'].cat.categories) == ['b', 'a']
    assert fixture_fold(sequences=reversed_categories, blocks=blocks, q=12).to_csv(index=False) == \
        fixture_fold(sequences=pool, blocks=blocks, q=12).to_csv(index=False)
    streams = sampling.sample_streams(fixture_fold(), restored, 'ud23')
    assert streams == sampling.sample_streams(fixture_fold(), FIXTURE_FRAME, 'ud23')
    assert [item['symbols'] for item in streams] == [[10, 11, 12, 13, 14], [50, 51, 52, 53, 54, 55, 56],
                                                     [40, 41], [23, 24, 25]]  # @2 is cut at [3,6)
    assert sampling.evaluation_streams(restored, variant='ud23', docs=['fixture'], block=FIXTURE_KEY) == \
        sampling.evaluation_streams(FIXTURE_FRAME, variant='ud23', docs=['fixture'], block=FIXTURE_KEY)


def test_each_sentence_or_fragment_is_one_reset_stream_without_separators(fold, arms, corpus, sequences):
    original, _ = arms
    assert len(original) == len(fold)
    assert sum(len(item['symbols']) for item in original) == 6 * 8884
    ud23 = sequences[sequences['variant'].eq('ud23')]
    symbols = dict(zip(ud23['sent_id'], ud23['symbols']))
    slots = dict(zip(ud23['sent_id'], ud23['slot_uids']))
    for row, item in zip(fold.itertuples(index=False), original):
        assert item['symbols'] == list(symbols[row.sent_id])[row.start:row.end]
        assert item['slot_uids'] == list(slots[row.sent_id])[row.start:row.end]
        assert isinstance(item['symbols'], list)  # one stream per sentence, never concatenated
    internal = [item for item, row in zip(original, fold.itertuples(index=False))
                if row.fragment and row.start > 0]
    assert internal, 'the fold must exercise at least one internal fragment'
    for item in internal:  # the excluded part of the sentence supplies no history
        assert len(symbols[item['sent_id']]) > len(item['symbols'])
    m = len(corpus['alphabets.json']['ud23']['symbols'])
    assert all(0 <= symbol < m for item in original for symbol in item['symbols'])
    # a ledger materialised against sentences that are not the ones it was cut from must fail
    short = frame([5, 4, 0, 2, 7, 6])
    with pytest.raises(ValueError, match='fixture@2'):
        sampling.sample_streams(fixture_fold(), short, 'ud23')
    with pytest.raises(ValueError, match='fixture@5'):
        sampling.sample_streams(fixture_fold(), FIXTURE_FRAME.iloc[:4], 'ud23')


def test_sample_streams_refuses_a_ledger_cut_from_a_shorter_variant():
    """A ledger carries no `variant` field by design (`upos_only` legitimately reuses C0's ledger
    byte for byte, §5.2). The overrun check alone cannot catch a `ud23` ledger silently applied to
    `ud23_oth`, whose sentences are never shorter (`oth` keeps every relation instead of dropping
    the unlisted ones): a non-fragment row must span the whole encoded sentence, not a shorter
    prefix of a longer one."""
    ledger = pd.DataFrame([{'block': 'fixture', 'block_key': FIXTURE_KEY, 'held': HELD_KEY, 'seed': 0,
                            'sent_id': 'fixture@1', 'doc_id': 'fixture', 'part_order': 0, 'source_ordinal': 1,
                            'start': 0, 'end': 5, 'fragment': False, 'sample_subseed': '0', 'fragment_subseed': ''}],
                          columns=list(sampling.LEDGER_COLUMNS))
    ud23 = frame([5])  # fixture@1: 5 encoded symbols in ud23, the row this ledger was cut from
    oth = ud23.assign(variant='ud23_oth', encoded_length=7, symbols=[list(range(7))],
                      slot_uids=[list(range(7))])  # ud23_oth keeps 2 more tokens for this sentence
    with pytest.raises(ValueError, match='fixture@1'):
        sampling.sample_streams(ledger, oth, 'ud23_oth')
    # the legitimate reuse — identical lengths, e.g. a C0 ledger against upos_only — still works
    same = ud23.assign(variant='upos_only')
    streams = sampling.sample_streams(ledger, same, 'upos_only')
    assert streams[0]['symbols'] == ud23.loc[0, 'symbols']


# --- T17: what the shuffle preserves ------------------------------------------

def test_shuffle_preserves_length_multiset_mask_and_root_counts(arms):
    original, shuffled = arms
    for before, after in zip(original, shuffled):
        assert len(after['symbols']) == len(before['symbols'])  # length fixes the mask too: same eligible count
        assert Counter(after['symbols']) == Counter(before['symbols'])
    assert Counter(chain.from_iterable(item['symbols'] for item in shuffled)) == \
        Counter(chain.from_iterable(item['symbols'] for item in original))  # identical root counts
    assert [item['symbols'] for item in shuffled] != [item['symbols'] for item in original]


def test_slot_identity_is_distinct_from_the_provenance_of_the_moved_token(arms):
    original, shuffled = arms
    moved = 0
    for before, after in zip(original, shuffled):
        assert after['slot_uids'] == before['slot_uids']  # the slot stays with its position
        assert sorted(after['source_slot_uids']) == sorted(before['slot_uids'])  # one to one
        assert dict(zip(after['source_slot_uids'], after['symbols'])) == \
            dict(zip(before['slot_uids'], before['symbols']))  # the symbol travels with its origin
        moved += sum(1 for slot, source in zip(after['slot_uids'], after['source_slot_uids']) if slot != source)
    assert moved > 0
    assert all('source_slot_uids' not in item for item in original)  # the original arm is untouched


def test_shuffle_records_the_symbol_change_rate_with_an_explicit_denominator():
    """§7: "Record the share of slots with a different symbol, with an explicit denominator;
    constant sentences may stay identical." Both small cases are hand-verifiable without knowing the
    drawn permutation: a constant stream can only ever come back identical, and with a single odd
    symbol among constants, only that symbol's own slot and the slot it lands on can ever change."""
    constant = stream([5, 5, 5, 5])
    after = sampling.shuffle_streams([constant], seed=0, held=HELD_KEY, purpose='shuffle_train')[0]
    assert after['symbols'] == constant['symbols']  # permuting equal values changes no slot
    assert (after['changed_symbol_slot_count'], after['total_slot_count']) == (0, 4)

    one_odd = stream([0, 0, 0, 1], sid='x@2')
    after = sampling.shuffle_streams([one_odd], seed=0, held=HELD_KEY, purpose='shuffle_train')[0]
    assert after['total_slot_count'] == 4
    assert after['changed_symbol_slot_count'] == sum(1 for before, moved in zip(one_odd['symbols'], after['symbols'])
                                         if before != moved)  # independently recomputed from the two arrays
    assert after['changed_symbol_slot_count'] in (0, 2)  # the lone 1 either lands back home, or swaps with one 0


# --- T18: the control is not innocuous ----------------------------------------

def test_shuffled_control_is_not_iid_within_a_stream():
    """Prefixed counterexample: identical multiset, different local dependence."""
    alternating = stream([0, 1] * 6)
    after = sampling.shuffle_streams([alternating], seed=0, held=HELD_KEY, purpose='shuffle_train')[0]
    assert Counter(after['symbols']) == Counter(alternating['symbols'])
    bigrams = Counter(zip(after['symbols'], after['symbols'][1:]))
    assert bigrams != Counter(zip(alternating['symbols'], alternating['symbols'][1:]))
    assert bigrams[(0, 0)] + bigrams[(1, 1)] > 0  # the original had none of either
    # permutation without replacement induces finite-composition dependence
    draws = [sampling.shuffle_streams([stream([0, 0, 1, 1], sid=f'x@{index}')], seed=0, held=HELD_KEY,
                                      purpose='shuffle_train')[0]['symbols'] for index in range(600)]
    assert all(sum(draw) == 2 for draw in draws)  # the last symbol is fixed by the first three
    after_one = [draw[1] for draw in draws if draw[0] == 1]
    conditional = sum(after_one) / len(after_one)
    marginal = sum(draw[1] for draw in draws) / len(draws)
    assert conditional + 0.08 < marginal, (conditional, marginal)  # i.i.d. would make them equal


def test_heterogeneous_pool_keeps_local_dependence_after_shuffling():
    """Blocks of unequal composition: the shuffled pool is not an order-free control."""
    pool = pd.concat([frame([8] * 10, doc='a'), frame([8] * 10, doc='b', first_slot=80)], ignore_index=True)
    composition = {'a': [0] * 7 + [1], 'b': [1] * 7 + [0]}
    pool['symbols'] = [composition[row.doc_id] for row in pool.itertuples(index=False)]
    blocks = {'a': ['a'], 'b': ['b'], 'held': ['held']}
    ledger = sampling.sample_fold(pool, variant='ud23', blocks=blocks, held_block='held', q=40, seed=0)
    streams = sampling.shuffle_streams(sampling.sample_streams(ledger, pool, 'ud23'),
                                       seed=0, held=sampling.block_key(['held']), purpose='shuffle_train')
    flat = list(chain.from_iterable(item['symbols'] for item in streams))
    assert Counter(flat) == Counter([0] * 40 + [1] * 40)  # the pooled composition is balanced
    pairs = Counter(chain.from_iterable(zip(item['symbols'], item['symbols'][1:]) for item in streams))
    conditional = pairs[(0, 0)] / (pairs[(0, 0)] + pairs[(0, 1)])
    assert conditional - flat.count(0) / len(flat) > 0.2, (conditional, pairs)


def test_module_imports_no_retired_v21_helper():
    """The sampler reads the corpus and the contract, nothing else: the retired
    registry and sequence helpers are in the archive and must not come back."""
    tree = ast.parse(Path(sampling.__file__).read_text(encoding='utf-8'))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module or '')
    assert imported == {'hashlib', 'numpy', 'pandas', 'hormathos.contracts', 'hormathos.corpus'}
    assert 'print(' not in Path(sampling.__file__).read_text(encoding='utf-8')
