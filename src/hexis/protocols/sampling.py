"""Sampling, RNG identity and the coupled order control (piano §5.1–§5.3, §7, §11.1).

The sampler is given block membership, the budget q, the held-out block and the
seed; it never reads a regime, a group or any display label (§11.1). No cell
parameter, variant name, alphabet size or configuration hash ever enters a
derivation (§5.3): that is exactly what keeps the two arms coupled.

One convention, `hexis-v3-rng-1`: nine fields in canonical JSON, the first 16
SHA-256 bytes read big endian as a 128-bit seed, and
`Generator(PCG64(derived_seed))`. Four purposes are active; the historical probe
purpose is retired from the contract and has no code here.

Nothing in this module fits or evaluates a model: it produces integer streams and
the ledger that says where each one was cut from.
"""

import hashlib

import numpy as np
import pandas as pd

from hexis.contracts import canonical_json
from hexis.corpus import SENTENCE_KEY

VERSION = 'hexis-v3-rng-1'
MASTER = 20260706
PURPOSES = ('sample', 'fragment', 'shuffle_train', 'shuffle_eval')
SENTENCE_COLUMNS = ('variant', 'role', 'doc_id', 'sent_id', 'part_order', 'source_ordinal',
                    'encoded_length')
LEDGER_COLUMNS = ('block', 'block_key', 'held', 'seed', 'sent_id', 'doc_id', 'part_order',
                  'source_ordinal', 'start', 'end', 'fragment', 'sample_subseed', 'fragment_subseed')
METRIC_COLUMNS = ('block', 'block_key', 'fragment_count', 'internal_start_count', 'fragment_tokens',
                  'direct_context_targets')


def _index(value, name, *, minimum=0) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)) or value < minimum:
        raise ValueError(f'{name}={value!r}: must be an int >= {minimum}')
    return int(value)


def _key(value, name) -> str:
    """Refuse a block name where a block key belongs: both are strings (§5.3)."""
    if not isinstance(value, str) or len(value) != 64 or set(value) - set('0123456789abcdef'):
        raise ValueError(f'{name}={value!r}: expected a 64-hex block key, not a name')
    return value


def _rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def _canonical(sentences) -> pd.DataFrame:
    """§5.2 step 1, sorted on the values of the key, not on a dtype artefact.

    `doc_id` and `sent_id` come back from a parquet round trip as categoricals,
    and a categorical sorts by its category order — which the dictionary of the
    file does not guarantee to be the lexicographic one. Getting this wrong
    would reorder the permutation universe and silently change every sample.
    """
    keys = sentences[list(SENTENCE_KEY)].astype({'doc_id': str, 'sent_id': str}).reset_index(drop=True)
    return sentences.iloc[keys.sort_values(list(SENTENCE_KEY)).index]


def block_key(docs) -> str:
    """SHA-256 of the canonical JSON of the sorted member list (§5.3).

    Author, period, group and display name of the block stay outside: changing
    the members changes the key, and that requires a new version.
    """
    members = list(docs)
    if not members or len(set(members)) != len(members) or any(
            not isinstance(doc, str) or not doc for doc in members):
        raise ValueError(f'block members must be distinct nonempty ids, got {members!r}')
    return hashlib.sha256(canonical_json(sorted(members))).hexdigest()


def derived_seed(purpose, *, seed, held, block, sid='', start=0, end=0) -> int:
    """The 128-bit seed of one draw: these nine fields and nothing else (§5.3)."""
    if purpose not in PURPOSES:
        raise ValueError(f'purpose={purpose!r}: the active purposes are {PURPOSES}')
    if not isinstance(sid, str):
        raise ValueError(f'sid={sid!r}: the sentence identity must be a string')
    fields = {'version': VERSION, 'master': MASTER, 'seed': _index(seed, 'seed'),
              'held': _key(held, 'held'), 'block': _key(block, 'block'), 'purpose': purpose,
              'sid': sid, 'start': _index(start, 'start'), 'end': _index(end, 'end')}
    return int.from_bytes(hashlib.sha256(canonical_json(fields)).digest()[:16], 'big')


def generator(purpose, **identity) -> np.random.Generator:
    """`Generator(PCG64(derived_seed))`, the constructor the plan names (§5.3)."""
    return _rng(derived_seed(purpose, **identity))


def permutation(n, *, seed, held, block) -> np.ndarray:
    """Step 2 of §5.2: the uniform order of a block's sentences under `sample`.

    It depends on the member key, the held-out key and the seed only, so every
    cell of a fold shares it — the cells that do not share a ledger still walk
    the sentences in this order (§5.2, `permutation_reuse_C0`).
    """
    return generator('sample', seed=seed, held=held, block=block).permutation(_index(n, 'n'))


def sample_block(sentences, q, *, seed, held, block) -> list:
    """§5.2 steps 1–5 for one contributing block; returns its ledger rows.

    `sentences` must hold every sentence of the block, empty encoded ones
    included: they stay in the permutation universe and consume no budget, so
    they shift the order without ever becoming a stream. Whole sentences are
    consumed while the next one fits the positive residual; the one that exceeds
    it gives a contiguous segment of exactly the residual, its offset drawn with
    that sentence's own `fragment` subseed. Hence at most one fragment per
    contributor and no sentence twice.
    """
    if isinstance(q, bool) or not isinstance(q, (int, np.integer)) or q < 1:
        raise ValueError(f'q={q}: the token budget must be a positive integer')
    rows = _canonical(sentences)
    lengths = [int(value) for value in rows['encoded_length']]
    if sum(lengths) < q:
        raise ValueError(f'block {block}: q={q} exceeds the {sum(lengths)} encoded tokens '
                         f'available in the {len(lengths)} sentences of this contributor')
    sids = [str(value) for value in rows['sent_id']]
    docs = [str(value) for value in rows['doc_id']]
    parts = [int(value) for value in rows['part_order']]
    ordinals = [int(value) for value in rows['source_ordinal']]
    sample_subseed = derived_seed('sample', seed=seed, held=held, block=block)
    ledger, residual = [], int(q)
    for drawn in _rng(sample_subseed).permutation(len(lengths)):
        index = int(drawn)
        length = lengths[index]
        if length == 0:
            continue
        if length <= residual:
            start, end, subseed = 0, length, ''
        else:
            fragment_subseed = derived_seed('fragment', seed=seed, held=held, block=block, sid=sids[index])
            start = int(_rng(fragment_subseed).integers(0, length - residual + 1))
            end, subseed = start + residual, str(fragment_subseed)
        ledger.append({'block_key': block, 'held': held, 'seed': int(seed), 'sent_id': sids[index],
                       'doc_id': docs[index], 'part_order': parts[index],
                       'source_ordinal': ordinals[index], 'start': start, 'end': end,
                       'fragment': end - start < length, 'sample_subseed': str(sample_subseed),
                       'fragment_subseed': subseed})
        residual -= end - start
        if residual == 0:
            break
    return ledger


def sample_fold(sequences, *, variant, blocks, held_block, q, seed) -> pd.DataFrame:
    """One (cell, fold, seed) training ledger: every block but the held-out one gives q (§5.1).

    `blocks` maps each block to its canonical_doc_id members — the only block
    identity the sampler is given, and the one its key is taken on. Held-out
    members and every `inventory_only` document are excluded before the draw.
    The record order of `sequences` is irrelevant: §5.2 step 1 sorts.
    """
    keys = {name: block_key(docs) for name, docs in blocks.items()}
    if held_block not in keys:
        raise ValueError(f'held_block={held_block!r}: not one of {sorted(keys)}')
    missing = [column for column in SENTENCE_COLUMNS if column not in sequences.columns]
    if missing:
        raise ValueError(f'sequences: missing column(s) {missing}')
    if variant not in set(sequences['variant']):
        raise ValueError(f'variant={variant!r}: absent from this sequences frame')
    primary = sequences[sequences['variant'].eq(variant) & sequences['role'].eq('primary')]
    ledger = []
    for name in sorted(keys):
        if name == held_block:
            continue
        members = primary[primary['doc_id'].isin(blocks[name])]
        ledger.extend({'block': name, **row} for row in
                      sample_block(members, q, seed=seed, held=keys[held_block], block=keys[name]))
    return pd.DataFrame(ledger, columns=list(LEDGER_COLUMNS))


def sample_streams(ledger, sequences, variant) -> list:
    """One autonomous reset stream per ledger row: symbols[start:end] with their slots (§5.2).

    Streams are never concatenated and there is no separator outcome: the
    excluded part of a cut sentence supplies no history (§6.2). Materialising a
    ledger against sentences it was not cut from is refused, not truncated —
    including a ledger cut from a shorter variant (the ledger carries no
    `variant` field by design, §5.2, so an overrun check alone cannot catch a
    `ud23` ledger silently applied to `ud23_oth`, whose sentences are never
    shorter: a non-fragment row must span the whole encoded sentence, not a
    truncated prefix of a longer one).
    """
    frame = sequences[sequences['variant'].eq(variant)]
    symbols = dict(zip(frame['sent_id'], frame['symbols']))
    slots = dict(zip(frame['sent_id'], frame['slot_uids']))
    streams = []
    for row in ledger.itertuples(index=False):
        if row.sent_id not in symbols:
            raise ValueError(f'{row.sent_id}: absent from the {variant!r} sentences of this frame')
        encoded = list(symbols[row.sent_id])
        if row.end > len(encoded):
            raise ValueError(f'{row.sent_id}: the ledger interval [{row.start},{row.end}) exceeds '
                             f'the {len(encoded)} encoded symbols of variant {variant!r}')
        if not row.fragment and (row.start != 0 or row.end - row.start != len(encoded)):
            raise ValueError(f'{row.sent_id}: a non-fragment ledger row must span the whole '
                             f'{len(encoded)}-symbol encoded sentence of variant {variant!r}, got '
                             f'[{row.start},{row.end}) — this ledger looks cut from a different variant')
        streams.append({'sent_id': row.sent_id, 'block_key': row.block_key, 'start': int(row.start),
                        'end': int(row.end),
                        'symbols': [int(symbol) for symbol in encoded[row.start:row.end]],
                        'slot_uids': [int(slot) for slot in list(slots[row.sent_id])[row.start:row.end]]})
    return streams


def evaluation_streams(sequences, *, variant, docs, block) -> list:
    """Every sentence of the evaluated block, whole and in canonical order (§4.4).

    Test sentences are never subsampled, so the interval is 0/length — the one
    `shuffle_eval` derives from (§5.3).
    """
    frame = _canonical(sequences[sequences['variant'].eq(variant) & sequences['role'].eq('primary')
                                 & sequences['doc_id'].isin(list(docs))])
    return [{'sent_id': str(row.sent_id), 'block_key': _key(block, 'block'), 'start': 0,
             'end': int(row.encoded_length), 'symbols': [int(symbol) for symbol in row.symbols],
             'slot_uids': [int(slot) for slot in row.slot_uids]}
            for row in frame.itertuples(index=False)]


def shuffle_streams(streams, *, seed, held, purpose) -> list:
    """§7 steps 3 and 5: permute the whole composite symbol inside each stream.

    The slot keeps its position — that is what the score pairs on — while the
    provenance of the moved token is the separate `source_slot_uids` field (§7
    step 6). UPOS and DEPREL are never separated: a symbol is one integer here
    and nothing in this module decodes it. Each stream derives its own
    generator, so reordering the streams cannot change any of them (§5.3).

    `changed_symbol_slot_count`/`total_slot_count` record §7's "quota di slot con simbolo
    diverso, con denominatore esplicito": how many slots hold a different
    symbol after the shuffle, out of the stream's length. A constant
    sentence can come back identical (`changed_symbol_slot_count == 0`) even though every
    slot's provenance still moved.
    """
    if purpose not in ('shuffle_train', 'shuffle_eval'):
        raise ValueError(f'purpose={purpose!r}: the order control is shuffle_train or shuffle_eval')
    shuffled = []
    for stream in streams:
        if purpose == 'shuffle_eval' and stream['block_key'] != held:
            raise ValueError(f"{stream['sent_id']}: shuffle_eval takes held and block from the "
                             'evaluated block itself')
        order = generator(purpose, seed=seed, held=held, block=stream['block_key'],
                          sid=stream['sent_id'], start=stream['start'],
                          end=stream['end']).permutation(len(stream['symbols']))
        moved = [stream['symbols'][index] for index in order]
        changed = sum(1 for before, after in zip(stream['symbols'], moved) if before != after)
        shuffled.append(stream | {'symbols': moved,
                                  'source_slot_uids': [stream['slot_uids'][index] for index in order],
                                  'changed_symbol_slot_count': changed, 'total_slot_count': len(moved)})
    return shuffled


def training_metrics(ledger, sequences, *, blocks, variant) -> pd.DataFrame:
    """Streams and tokens per contributor, beside the primary tokens it could give (§5.1)."""
    frame = sequences[sequences['variant'].eq(variant) & sequences['role'].eq('primary')]
    kept = frame.groupby(frame['doc_id'].astype(str))['encoded_length'].sum()
    training = ledger.assign(tokens=ledger['end'] - ledger['start']).groupby(
        ['block', 'block_key'], sort=True, as_index=False).agg(
        streams=('sent_id', 'size'), tokens=('tokens', 'sum'))
    training['available'] = [int(sum(int(kept.get(doc, 0)) for doc in blocks[name]))
                             for name in training['block']]
    return training


def fragment_metrics(ledger, depth) -> pd.DataFrame:
    """The four cut quantities §5.2 requires per contributor, shared by both arms."""
    depth = _index(depth, 'depth', minimum=1)
    rows = []
    for (name, key), group in ledger.groupby(['block', 'block_key'], sort=True):
        cut = group[group['fragment']]
        lengths = (cut['end'] - cut['start']).astype(int)
        internal = lengths[cut['start'] > 0]
        rows.append({'block': name, 'block_key': key, 'fragment_count': len(cut),
                     'internal_start_count': len(internal), 'fragment_tokens': int(lengths.sum()),
                     'direct_context_targets': int(internal.clip(upper=depth).sum())})
    return pd.DataFrame(rows, columns=list(METRIC_COLUMNS))


def pair_streams(sequences, *, variant, blocks, held_block, q, seed):
    """§7 steps 1–3 and 5 for one (cell, fold, seed), from the RNG contract alone: the ledger,
    both training arms and both evaluated arms — what the executor fits and the report regenerates."""
    ledger = sample_fold(sequences, variant=variant, blocks=blocks, held_block=held_block, q=q, seed=seed)
    held = block_key(blocks[held_block])
    train = {'original': sample_streams(ledger, sequences, variant)}
    train['shuffled'] = shuffle_streams(train['original'], seed=seed, held=held, purpose='shuffle_train')
    evaluated = {'original': evaluation_streams(sequences, variant=variant, docs=blocks[held_block], block=held)}
    evaluated['shuffled'] = shuffle_streams(evaluated['original'], seed=seed, held=held, purpose='shuffle_eval')
    return ledger, train, evaluated


def change_counts(train, evaluated):
    """§7: slots holding another symbol after the shuffle, over an explicit denominator."""
    return {population: {name: sum(stream[name] for stream in streams['shuffled'])
                         for name in ('changed_symbol_slot_count', 'total_slot_count')}
            for population, streams in (('training', train), ('evaluation', evaluated))}
