"""Four losses on coupled slots, sums, G/Q and the two weightings (piano §8.1–§8.2, §9.3, §11.1).

The core is label-free (§11.1): it pairs the two arms on the eligible slot and
returns losses, masses and sums keyed by `sent_id`/`slot_uid`. No regime, group
or display name reaches it — the caller maps a sentence to its document before
aggregating. `annotate_scores` introduces registry labels after scoring.

Q always needs its four terms (§7): the two roots are the same training
distribution but not the same test population, so `CE_CTW_R - CE_CTW_O` is not Q
and can carry the opposite sign. G and Q are never truncated (§8.1).
"""

import math
import time

import numpy as np
import pandas as pd

from hexis.model import diagnostics

MIN_AVAILABLE_PAST = 4  # §4.4: four ordinary predecessors kept in the same sentence
BANDS = ('4_7', 'ge8')
ARMS = ('original', 'shuffled')
HEX, PROSE = 'HEX', 'PROSE_ALL'
AGGREGATIONS = ('equal_block', 'eligible_token_weighted')

POSITION_COLUMNS = ('slot_uid', 'original_symbol_id', 'shuffled_symbol_id',
                    'shuffled_origin_slot_uid', 'loss_ctw_original', 'loss_root_original',
                    'loss_ctw_shuffled', 'loss_root_shuffled', 'unseen_mass_original',
                    'unseen_mass_shuffled', 'resolved_mean_original', 'resolved_mean_shuffled')
SUM_COLUMNS = ('n', 'sum_loss_ctw_original', 'sum_loss_root_original', 'sum_loss_ctw_shuffled',
               'sum_loss_root_shuffled', 'changed_symbol_eligible_slot_count',
               'eligible_slot_count')
COUNT_COLUMNS = ('n', 'changed_symbol_eligible_slot_count', 'eligible_slot_count')
SCORE_COLUMNS = ('ce_ctw_original', 'ce_root_original', 'ce_ctw_shuffled', 'ce_root_shuffled',
                 'g_original', 'g_shuffled', 'q')


def past_band(available_past: int) -> str:
    """§4.4 diagnostic bands, disjoint: 4–7 and >=8 predecessors."""
    return BANDS[0] if available_past < 8 else BANDS[1]


def _require_paired(left, right, index):
    """§7 step 6: the shuffle moves the symbol, never the slot. Verified, not assumed."""
    if left['sent_id'] != right['sent_id']:
        raise ValueError(f'stream {index}: {left["sent_id"]!r} is paired with '
                         f'{right["sent_id"]!r} — the two arms must walk the same sample')
    if 'source_slot_uids' not in right:
        raise ValueError(f'{left["sent_id"]}: the shuffled arm carries no source_slot_uids, so '
                         'the provenance of the moved token is unrecoverable')
    if left['slot_uids'] != right['slot_uids']:
        raise ValueError(f'{left["sent_id"]}: the two arms hold different slot_uids; the shuffle '
                         'permutes symbols inside a stream and leaves every slot in place')
    if len(left['symbols']) != len(right['symbols']):
        raise ValueError(f'{left["sent_id"]}: the shuffle must preserve the stream length, got '
                         f'{len(left["symbols"])} and {len(right["symbols"])}')
    slots, origins = left['slot_uids'], right['source_slot_uids']
    if len(slots) != len(left['symbols']) or len(set(slots)) != len(slots):
        raise ValueError(f'{left["sent_id"]}: slot_uids must be unique and match symbols in length')
    if len(origins) != len(slots) or set(origins) != set(slots):
        raise ValueError(f'{left["sent_id"]}: provenance must permute the slot_uids one-to-one')


def pooled_score_core(original, shuffled, *, model_original, model_shuffled,
                      min_available_past=MIN_AVAILABLE_PAST) -> tuple[pd.DataFrame, pd.DataFrame]:
    """The four losses of §8.1 per eligible slot, with the §9.3 sums per arm and band.

    Returns `(positions, arm_diagnostics)`: one row per eligible slot with the
    §11.4 fields, and one row per (sent_id, band, arm) with the §9.3 record —
    both bands always, so an empty one is a zero row and never an absence.
    """
    is_int = isinstance(min_available_past, (int, np.integer)) and not isinstance(min_available_past, bool)
    if not is_int or min_available_past < 0:
        raise ValueError(f'min_available_past={min_available_past!r}: must be an int >= 0')
    if len(original) != len(shuffled):
        raise ValueError(f'{len(original)} original streams against {len(shuffled)} shuffled: '
                         'the two arms come from one sample and must be paired')
    names = [stream['sent_id'] for stream in original]
    if len(set(names)) != len(names):
        raise ValueError('the scored streams repeat a sent_id: every sentence or fragment is one '
                         'stream, and its diagnostics must not be silently merged')
    depth = model_original.params.depth
    if depth != model_shuffled.params.depth:
        raise ValueError(f'the two arms carry different depths ({depth} and '
                         f'{model_shuffled.params.depth}): one cell fits both')
    m = model_original.params.m
    if m != model_shuffled.params.m:
        raise ValueError(f'the two arms carry different alphabet sizes ({m} and '
                         f'{model_shuffled.params.m}): one cell fits both')
    models = {'original': model_original, 'shuffled': model_shuffled}
    roots = {arm: model.root_distribution() for arm, model in models.items()}
    observed = {arm: set(model.inspect(())['counts']) for arm, model in models.items()}

    rows, totals, seen_slots = [], {}, set()
    evaluation_seconds = dict.fromkeys(ARMS, 0.0)
    for index, (left, right) in enumerate(zip(original, shuffled)):
        _require_paired(left, right, index)
        if seen_slots.intersection(left['slot_uids']):
            raise ValueError('slot_uids repeat across scored streams')
        seen_slots.update(left['slot_uids'])
        sent_id = left['sent_id']
        for arm, stream in (('original', left), ('shuffled', right)):
            models[arm]._validated(stream['symbols'], f'{sent_id} {arm}')
        for band in BANDS:
            for arm in ARMS:
                totals[(sent_id, band, arm)] = diagnostics.EvaluationTotals(depth)
        for position in range(min_available_past, len(left['symbols'])):
            band = past_band(position)
            row = {'sent_id': sent_id, 'available_past': position, 'past_band': band,
                   'slot_uid': left['slot_uids'][position],
                   'original_symbol_id': left['symbols'][position],
                   'shuffled_symbol_id': right['symbols'][position],
                   'shuffled_origin_slot_uid': right['source_slot_uids'][position]}
            for arm, symbols in (('original', left['symbols']), ('shuffled', right['symbols'])):
                started = time.perf_counter()
                model, target, history = models[arm], symbols[position], symbols[:position]
                record = diagnostics.resolved(model.mixture(history))
                row[f'loss_ctw_{arm}'] = -math.log2(model.predict_proba(history)[target])
                row[f'loss_root_{arm}'] = -math.log2(roots[arm][target])
                row[f'unseen_mass_{arm}'] = record['unseen_mass']
                row[f'resolved_mean_{arm}'] = (math.nan if record['resolved_mean'] is None
                                               else record['resolved_mean'])
                totals[(sent_id, band, arm)].add(record, root_unseen=target not in observed[arm])
                evaluation_seconds[arm] += time.perf_counter() - started
            rows.append(row)
    if not rows:
        raise ValueError(f'no eligible target with min_available_past={min_available_past} in '
                         f'{len(original)} streams: a primary block without targets stops the cell')
    positions = pd.DataFrame(rows, columns=['sent_id', 'available_past', 'past_band',
                                            *POSITION_COLUMNS])
    arm_rows = [{'sent_id': sent_id, 'past_band': band, 'arm': arm, **record.row()}
                for (sent_id, band, arm), record in totals.items()]
    arm_frame = pd.DataFrame(arm_rows)
    arm_frame.attrs['evaluation_seconds'] = evaluation_seconds
    return positions, arm_frame


# Existing v3.1 callers use the same implementation, with no second scoring path.


def annotate_scores(scores, registry, *, on='doc_id') -> pd.DataFrame:
    """§11.1: attach registry columns to fixed scores by their explicit identity.

    Document, sentence or block identity can be used; the registry must contain
    exactly one non-null record per key and must never replace a score column.
    """
    for name, frame in (('scores', scores), ('registry', registry)):
        if not frame.columns.is_unique or on not in frame or frame[on].isna().any():
            raise ValueError(f'{name}: unique columns and non-null {on!r} are required')
    if not registry[on].is_unique:
        raise ValueError(f'registry: duplicate {on!r}')
    overlap = (set(scores.columns) & set(registry.columns)) - {on}
    if overlap:
        raise ValueError(f'registry: refusing to overwrite fixed columns {sorted(overlap)}')
    missing = set(scores[on]) - set(registry[on])
    if missing:
        raise ValueError(f'registry: missing {on!r} for {sorted(missing)}')
    return scores.join(registry.set_index(on), on=on, how='left', validate='many_to_one')


def aggregate(positions, keys=(), *, universe=None) -> pd.DataFrame:
    """§8.2 sums per (keys, band); every key keeps both bands, empty ones at zero."""
    keys = list(keys)
    changed = positions['original_symbol_id'].ne(positions['shuffled_symbol_id'])
    frame = positions.assign(n=1, eligible_slot_count=1,
                             changed_symbol_eligible_slot_count=changed.astype('int64'),
                             **{f'sum_loss_{name}': positions[f'loss_{name}'] for name in
                                ('ctw_original', 'root_original', 'ctw_shuffled', 'root_shuffled')})
    grouped = frame.groupby(keys + ['past_band'], sort=True)[list(SUM_COLUMNS)].sum().reset_index()
    bands = pd.DataFrame({'past_band': list(BANDS)})
    members = frame[keys].drop_duplicates() if universe is None else universe[keys]
    complete = (members.sort_values(keys).merge(bands, how='cross')
                if keys else bands)
    filled = complete.merge(grouped, how='left', on=keys + ['past_band'])
    filled[list(SUM_COLUMNS)] = filled[list(SUM_COLUMNS)].fillna(0)
    return filled.astype({column: 'int64' for column in COUNT_COLUMNS})


def roll_up(sums, keys=()) -> pd.DataFrame:
    """§11.5: a total is the sum of the disjoint band rows, not a third population."""
    columns = [column for column in SUM_COLUMNS if column in sums.columns]
    counts = {column: 'int64' for column in COUNT_COLUMNS if column in columns}
    if not keys:
        return sums[columns].sum().to_frame().T.astype(counts)
    return sums.groupby(list(keys), sort=True, as_index=False)[columns].sum().astype(counts)


def ce_gain_q(sums) -> pd.DataFrame:
    """§8.1 CE, G and Q per row; an empty bucket is null with a reason (§9.3)."""
    scored = sums.copy()
    n = scored['n'].to_numpy(dtype='float64')
    targets = np.where(n > 0, n, np.nan)
    for arm in ARMS:
        scored[f'ce_ctw_{arm}'] = scored[f'sum_loss_ctw_{arm}'] / targets
        scored[f'ce_root_{arm}'] = scored[f'sum_loss_root_{arm}'] / targets
        scored[f'g_{arm}'] = scored[f'ce_root_{arm}'] - scored[f'ce_ctw_{arm}']
    scored['q'] = scored['g_original'] - scored['g_shuffled']
    # object dtype on purpose: pandas turns a None inside an inferred string column into NaN
    scored['reason'] = pd.Series([None if count > 0 else diagnostics.EMPTY_BUCKET for count in n],
                                 index=scored.index, dtype=object)
    return scored


def contrasts(blocks, groups) -> pd.DataFrame:
    """§8.2: group means and the HEX - PROSE_ALL contrast under both weightings.

    Labels enter through annotate_scores (§11.1). Weights are eligible targets of the
    variant, never raw or kept tokens; `D_Q = D_G_O - D_G_R` is verified here.
    """
    frame = blocks.set_index('block') if 'block' in blocks.columns else blocks
    columns = list(SCORE_COLUMNS)
    unknown = [block for block in frame.index if block not in groups]
    if unknown:
        raise ValueError(f'{sorted(unknown)}: no group declared for these blocks')
    invalid = [block for block in frame.index[frame[columns].isna().any(axis=1)]]
    if invalid:
        raise ValueError(f'{sorted(invalid)}: a block without a score cannot enter a contrast')
    registry = pd.DataFrame({'block': list(groups), 'group': list(groups.values())})
    frame = annotate_scores(frame.rename_axis('block').reset_index(), registry,
                            on='block').set_index('block')
    label = frame['group'].to_numpy()
    rows = []
    for aggregation in AGGREGATIONS:
        weights = (pd.Series(1.0, index=frame.index) if aggregation == AGGREGATIONS[0]
                   else frame['n'].astype('float64'))
        means = {}
        for group in (HEX, PROSE):
            part = frame[label == group]
            if part.empty or weights[part.index].sum() <= 0:
                raise ValueError(f'group {group!r} has no weighted block in this contrast')
            share = weights[part.index]
            means[group] = part[columns].mul(share, axis=0).sum() / share.sum()
            rows.append({'aggregation': aggregation, 'group': group,
                         'n': int(part['n'].sum()), **means[group]})
        contrast = means[HEX] - means[PROSE]
        if abs(contrast['q'] - (contrast['g_original'] - contrast['g_shuffled'])) > 1e-12:
            raise ValueError(f'{aggregation}: D_Q does not match D_G_O - D_G_R')
        rows.append({'aggregation': aggregation, 'group': 'contrast', 'n': np.nan, **contrast})
    return pd.DataFrame(rows)


def seed_summary(values) -> dict:
    """§8.2: aggregate per seed first, then mean, SD with S-1, min, max and S."""
    numbers = [float(value) for value in values]
    if not numbers:
        raise ValueError('seed_summary: no per-seed value to summarize')
    return {'mean': float(np.mean(numbers)),
            'sd': float(np.std(numbers, ddof=1)) if len(numbers) > 1 else None,
            'min': min(numbers), 'max': max(numbers), 'S': len(numbers)}


def pair_positions(left, right, *, on='slot_uid', suffixes=('_left', '_right')) -> pd.DataFrame:
    """§11.5: one-to-one on the slot before aggregating; equal length is not enough."""
    for side, frame in (('left', left), ('right', right)):
        if not frame[on].is_unique:
            raise ValueError(f'{side}: {on} holds duplicates, so it is not unique enough to pair')
    only_left, only_right = set(left[on]) - set(right[on]), set(right[on]) - set(left[on])
    if only_left or only_right:
        raise ValueError(f'the two {on} sets differ: {len(only_left)} only on the left and '
                         f'{len(only_right)} only on the right — a changed target population '
                         'is not a paired comparison')
    return left.merge(right, on=on, suffixes=suffixes, validate='one_to_one')
