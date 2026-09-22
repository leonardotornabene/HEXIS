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
import math
import time
from pathlib import Path

import pandas as pd

from hexis.contracts import compare, digest, load_contracts
from hexis.model import diagnostics
from hexis.pipeline import scientific_run, validation_run
from hexis.protocols import r1, sampling, scores

KEY_COLUMNS = ('cell', 'variant', 'held_block', 'held_block_key', 'seed')
RECORD_FIELDS = (*KEY_COLUMNS, 'q', 'depth', 'm', 'a_per_symbol', 'rho', 'min_available_past',
                 'arms', 'ledger_sha256', 'ledger_rows', 'sample_ledger', 'training', 'fragments', 'shuffle', 'models',
                 'document_sums', 'arm_diagnostics', 'positions')
TABLES = ('document_scores.csv', 'block_pairs.csv', 'aggregation_weights.csv', 'contrasts.csv',
          'seed_summaries.csv', 'sensitivity_pairs.csv', 'model_diagnostics.csv',
          'arm_diagnostics.csv', 'fragment_diagnostics.csv', 'root_distributions.csv',
          'jsd_pairs.csv', 'jsd_centroids.csv', 'jsd_contributions.csv')
REFERENCE_CELL = 'C0'  # §11.5: sensitivities are paired against C0 on the same seeds
UNIT_COLUMNS = ('level', 'unit', 'aggregation', 'past_band')  # a group, block or document profile
NOT_APPLICABLE = 'not_applicable'  # blocks and documents have no weighting choice (§8.2)
SUMMARY_COLUMNS = ('cell', *UNIT_COLUMNS, 'metric', 'mean', 'sd', 'min', 'max', 'S', 'reason')
PAIR_COLUMNS = ('cell', 'reference', *UNIT_COLUMNS, 'seed', 'metric', 'value', 'reference_value',
                'difference')
FOLD_COLUMNS = ('fold_training_tokens', f'fold_share_{scores.HEX}', f'fold_share_{scores.PROSE}',
                'fold_share_own_group')
FRAGMENT_COLUMNS = (*KEY_COLUMNS, 'contributor', 'contributor_key', 'fragment_count',
                    'internal_start_count', 'fragment_tokens', 'direct_context_targets')
CENTROID_COLUMNS = ('variant', 'group_a', 'group_b', 'blocks_a', 'blocks_b', 'jsd')
RESOURCE_COLUMNS = ('fit_seconds', 'evaluation_seconds', 'peak_rss')  # §11.5; measured, never deterministic


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


def check_evidence(evidence, contract, *, scientific=False):
    """Step 2: real reports require V0–V3; V2 toy runs verify only their recorded evidence."""
    required = ('V0', 'V1', 'V2', 'V3') if scientific else scientific_run.EVIDENCE_STEPS
    missing = [step for step in required if step not in evidence]
    if missing:
        raise ValueError(f'evidence: {missing} is not recorded in this manifest; a written PASS '
                         'is not the proof it stands for')
    for step, record in sorted(evidence.items()):
        if record.get('code') != digest(contract['code']):
            raise ValueError(f'evidence {step}: recorded under another code identity')
        if record.get('lock') != contract['lock']:
            raise ValueError(f'evidence {step}: recorded under another environment lock')


def expected_keys(cfg) -> dict:
    """Step 3: the keys the contract asks for, generated from the contract itself.

    `document_band` covers both bands of every primary document of the evaluated
    (held-out) block, for every seed of every cell — the family §14.2 step 3 names
    beside the 490 pair-keys/980 model-keys ones, with expected cardinalities
    `paired_document_band_rows_C0`/`..._sensitivities` in `report_contract_v3.1.json`.
    """
    blocks = scientific_run.block_keys_of(cfg)
    members = scientific_run.blocks_of(cfg)
    pair, model, document_band = [], [], []
    for cell in cfg['cells']:
        for name in sorted(blocks):
            for seed in cell['seeds']:
                key = (cell['id'], blocks[name], int(seed))
                pair.append(key)
                model.extend((*key, arm) for arm in cell['arms'])
                document_band.extend((*key, str(doc), band) for doc in members[name]
                                     for band in scores.BANDS)
    return {'pair': pair, 'model': model, 'document_band': document_band}


def check_keys(cfg, produced=None, *, docs=None, arm=None):
    """Step 3: set equality against the contract, duplicates detected before the sets.

    `produced` is the manifest's own pair/model key lists, checked as soon as they
    are read. `docs`/`arm` are the document_scores.csv/arm_diagnostics.csv frames:
    they exist only once the partitions are aggregated, so the document/band
    family is checked in a second call once those two frames are built.
    `scores.aggregate` keeps only the documents actually present in the scored
    positions, while `score_streams` pre-seeds a total for every evaluated
    `sent_id` before it ever walks an eligible position — a document contributing
    zero eligible slots silently vanishes from the first table and not the
    second, and nothing else cross-checks them (§14.2 step 3).
    """
    expected = expected_keys(cfg)
    if produced is not None:
        published = scientific_run.key_sets(produced)
        for kind in ('pair', 'model'):
            missing = sorted(set(expected[kind]) - published[kind])
            unexpected = sorted(published[kind] - set(expected[kind]))
            if missing or unexpected:
                raise ValueError(f'{kind} key set differs from the contract: missing {missing[:4]}, '
                                 f'unexpected {unexpected[:4]} ({len(missing)} and {len(unexpected)} '
                                 'in total)')
    if docs is not None:
        band = set(expected['document_band'])
        for name, frame in (('document_scores.csv', docs), ('arm_diagnostics.csv', arm)):
            present = {(row.cell, row.held_block_key, int(row.seed), str(row.doc_id), row.past_band)
                      for row in frame.itertuples()}
            missing = sorted(band - present)
            unexpected = sorted(present - band)
            if missing or unexpected:
                raise ValueError(f'document_band key set differs from the contract in {name}: '
                                 f'missing {missing[:4]}, unexpected {unexpected[:4]} '
                                 f'({len(missing)} and {len(unexpected)} in total)')


def read_partitions(output, manifest) -> list:
    """Step 4: every published pair record, read back and checked against its own key."""
    output, records = Path(output), []
    for key in sorted(tuple(key) for key in manifest['keys']['pair']):
        name = scientific_run.pair_name(*key)
        record = scientific_run._read_json(output / name)
        _schema(record, RECORD_FIELDS, name)
        if (record['cell'], record['held_block_key'], record['seed']) != key:
            raise ValueError(f'{name}: the record names another key')
        records.append(record)
    return records


def _schema(row, fields, where):
    if not isinstance(row, dict) or set(row) != set(fields):
        raise ValueError(f'{where}: fields must be exactly {list(fields)}')


def _number(value, where, *, count=False):
    if (type(value) not in ((int,) if count else (int, float))
            or not math.isfinite(value) or value < 0):
        raise ValueError(f'{where}: expected a finite nonnegative {"integer" if count else "number"}')


def _close(actual, expected, where, *, count=1, tolerance=1e-12):
    if not math.isclose(actual, expected, rel_tol=0, abs_tol=count * tolerance):
        raise ValueError(f'{where}: {actual} differs from reconstructed {expected}')


def _rows(rows, fields, keys, expected, where):
    found = {}
    for row in rows:
        _schema(row, fields, where)
        key = tuple(row[name] for name in keys)
        if key in found:
            raise ValueError(f'{where}: duplicate key {key}')
        found[key] = row
    if set(found) != set(expected):
        raise ValueError(f'{where}: document_band key set differs from the contract: missing {set(expected) - set(found)}, unexpected {set(found) - set(expected)}')
    return found


def validate_partitions(output, manifest, cfg, frames):
    """Validate each published pair, including a partial campaign, before reuse or reporting.

    Keys/counts are exact; CE reconstruction uses §6.5's 1e-9 bit/target.
    Diagnostic sums allow 1e-12 per contributing position for summation roundoff.
    """
    output = Path(output)
    published = scientific_run.key_sets(manifest['keys'])
    expected = expected_keys(cfg)
    if not published['pair'] <= set(expected['pair']):
        raise ValueError('pair key set contains an undeclared execution')
    if published['model'] != {(*key, arm) for key in published['pair'] for arm in scores.ARMS}:
        raise ValueError('model key set must contain both arms of every pair')
    records = read_partitions(output, manifest)
    cells = {cell['id']: cell for cell in cfg['cells']}
    blocks = scientific_run.blocks_of(cfg)
    coordinates = frames['coordinates.parquet']
    for record in records:
        cell = cells[record['cell']]
        held = record['held_block']
        if held not in blocks or scientific_run.block_keys_of(cfg)[held] != record['held_block_key']:
            raise ValueError('held_block disagrees with its declared key')
        for field, value in {'variant': cell['variant'], 'depth': cell['D'], 'm': cell['m'],
                             'q': cell['q'], 'rho': cell['rho'], 'a_per_symbol': cell['a_per_symbol'],
                             'min_available_past': cfg['min_available_past'], 'arms': list(scores.ARMS)}.items():
            if type(record[field]) is not type(value) or record[field] != value:
                raise ValueError(f'{field}: partition differs from configuration')
        if record['sample_ledger'] != scientific_run.ledger_name(record['ledger_sha256']):
            raise ValueError('sample_ledger: name does not match its digest')
        rows = scientific_run._read_json(output / record['sample_ledger'])
        if digest(rows) != record['ledger_sha256'] or len(rows) != record['ledger_rows']:
            raise ValueError(f"{record['sample_ledger']}: ledger digest or cardinality mismatch")
        ledger = pd.DataFrame(rows, columns=list(sampling.LEDGER_COLUMNS))
        # §11.5: the training and fragment summaries the report reads are recomputed, never trusted.
        compare(record['training'], scientific_run.records(sampling.training_metrics(
            ledger, frames['sequences.parquet'], blocks=blocks, variant=cell['variant'])), 'training')
        compare(record['fragments'], scientific_run.records(
            sampling.fragment_metrics(ledger, record['depth'])), 'fragments')
        positional = scientific_run.positions_name(record['cell'], record['held_block_key'], record['seed'])
        if record['positions'] != (positional if record['cell'] == REFERENCE_CELL else None):
            raise ValueError('positions: mandatory in C0 and forbidden in sensitivities')
        eligible = coordinates[coordinates['variant'].eq(record['variant'])
                               & coordinates['doc_id'].astype(str).isin(blocks[held])
                               & coordinates['eligible'].astype(bool)].copy()
        eligible['doc_id'] = eligible['doc_id'].astype(str)
        eligible['past_band'] = eligible['available_past'].map(scores.past_band)
        counts = eligible.groupby(['doc_id', 'past_band']).size().to_dict()
        if not len(eligible):
            raise ValueError(f'{held}: primary block has no eligible targets')
        keys = [(str(doc), band) for doc in blocks[held] for band in scores.BANDS]
        docs = _rows(record['document_sums'], ('doc_id', 'past_band', *scores.SUM_COLUMNS),
                     ('doc_id', 'past_band'), keys, 'document_scores.csv')
        diag_fields = diagnostics.EvaluationTotals(record['depth']).row()
        arms = _rows(record['arm_diagnostics'], ('doc_id', 'arm', 'past_band', *diag_fields),
                     ('doc_id', 'past_band', 'arm'),
                     [(*key, arm) for key in keys for arm in scores.ARMS], 'arm_diagnostics.csv')
        check_roles(pd.DataFrame(record['document_sums']), frames['documents.csv'])
        for key, row in docs.items():
            n = counts.get(key, 0)
            for field in scores.SUM_COLUMNS:
                _number(row[field], field, count=field in scores.COUNT_COLUMNS)
                if n == 0 and row[field] != 0:
                    raise ValueError(f'{key}: empty bucket has nonzero sums')
            if row['n'] != n or row['eligible_slot_count'] != n or row['changed_symbol_eligible_slot_count'] > n:
                raise ValueError(f'{key}: coordinate denominator differs')
            for arm in scores.ARMS:
                diagnostic = arms[(*key, arm)]
                for field, default in diag_fields.items():
                    _number(diagnostic[field], field, count=type(default) is int)
                    if n == 0 and diagnostic[field] != 0:
                        raise ValueError(f'{key}: empty bucket has nonzero diagnostics')
                valid = diagnostic['resolved_valid_count']
                null = diagnostic[f'resolved_null_count_by_reason_{diagnostics.NO_RESOLVED_MASS}']
                if diagnostic['n'] != n or valid + null != n:
                    raise ValueError(f'{key}: diagnostic denominator differs')
                for field in ('root_unseen_target_count', 'implicit_unseen_branch_encounter_count'):
                    if diagnostic[field] > n:
                        raise ValueError(f'{key}: {field} exceeds its denominator')
                if diagnostic['sum_resolved_valid'] > valid * record['depth'] + n * 1e-12:
                    raise ValueError(f'{key}: resolved sum exceeds depth/valid count')
                if diagnostic['sum_unseen_mass'] > n + n * 1e-12:
                    raise ValueError(f'{key}: unseen mass exceeds denominator')
                mass = math.fsum(diagnostic[field] for field in diag_fields if field.startswith(diagnostics.MASS_PREFIX))
                _close(mass + diagnostic['sum_unseen_mass'], n, 'mass conservation', count=max(n, 1))
        _schema(record['models'], scores.ARMS, 'models')
        training_tokens = (len(blocks) - 1) * cell['q']
        _schema(record['shuffle'], ('training', 'evaluation'), 'shuffle')
        sequences = frames['sequences.parquet']
        evaluated_tokens = int(sequences.loc[sequences['variant'].eq(cell['variant'])
                                             & sequences['doc_id'].astype(str).isin(blocks[held]),
                                             'encoded_length'].sum())
        for population, denominator in (('training', training_tokens), ('evaluation', evaluated_tokens)):
            counts = record['shuffle'][population]
            _schema(counts, ('changed_symbol_slot_count', 'total_slot_count'), 'shuffle counts')
            for value in counts.values():
                _number(value, 'shuffle counts', count=True)
            if counts['total_slot_count'] != denominator or counts['changed_symbol_slot_count'] > denominator:
                raise ValueError('shuffle denominator differs from corpus/budget')
        for arm, model in record['models'].items():
            _schema(model, ('fingerprint', 'training_streams', 'training_tokens', 'nodes',
                           'node_count_by_structural_depth', 'support_histogram_1_2to4_5to9_10plus_by_depth',
                           'root_observed_symbol_count', 'root_unseen_symbol_count', 'root_stop',
                           'delta_root_nats_stop_minus_split', 'delta_root_reason', 'log_evidence'),
                    f'model {arm}')
            for field in ('training_streams', 'training_tokens', 'nodes', 'root_observed_symbol_count',
                          'root_unseen_symbol_count'):
                _number(model[field], field, count=True)
            if model['training_tokens'] != training_tokens or model['training_streams'] != record['ledger_rows']:
                raise ValueError('model training denominator differs from budget/ledger')
            depths = model['node_count_by_structural_depth']
            histograms = model['support_histogram_1_2to4_5to9_10plus_by_depth']
            if len(depths) != len(histograms) or not depths or depths[0] != 1 or len(depths) > record['depth'] + 1:
                raise ValueError('model support depth differs')
            for n, histogram in zip(depths, histograms):
                _number(n, 'node_count_by_structural_depth', count=True)
                _schema(histogram, ('1', '2to4', '5to9', '10plus'), 'support histogram')
                for value in histogram.values(): _number(value, 'support histogram', count=True)
                if sum(histogram.values()) != n:
                    raise ValueError('model support histogram count differs')
            if (sum(depths) != model['nodes'] or model['root_observed_symbol_count']
                    + model['root_unseen_symbol_count'] != record['m']):
                raise ValueError('model support count differs')
            _number(model['root_stop'], 'root_stop')
            if model['root_stop'] > 1:
                raise ValueError('root_stop exceeds one')
            if type(model['log_evidence']) not in (int, float) or not math.isfinite(model['log_evidence']):
                raise ValueError('nonfinite log_evidence')
            if record['depth'] == 0:
                if model['delta_root_nats_stop_minus_split'] is not None or model['delta_root_reason'] != 'forced_leaf' or model['root_stop'] != 1:
                    raise ValueError('invalid forced root')
            elif (type(model['delta_root_nats_stop_minus_split']) not in (int, float)
                  or not math.isfinite(model['delta_root_nats_stop_minus_split'])
                  or model['delta_root_reason'] is not None):
                raise ValueError('invalid delta_root_nats_stop_minus_split')
        if record['positions'] is not None:
            positions, eligible = check_positions(output, record, cfg, coordinates)
            joined = scores.pair_positions(positions, eligible[['slot_uid', 'doc_id', 'available_past']])
            joined['doc_id'] = joined['doc_id'].astype(str)
            joined['past_band'] = joined['available_past'].map(scores.past_band)
            rebuilt = scores.aggregate(joined, keys=['doc_id'], universe=pd.DataFrame({'doc_id': blocks[held]}))
            for row in rebuilt.to_dict('records'):
                persisted = docs[(row['doc_id'], row['past_band'])]
                for field in scores.SUM_COLUMNS:
                    if field in scores.COUNT_COLUMNS:
                        if persisted[field] != row[field]: raise ValueError(f'{field}: reconstructed count differs')
                    else:
                        _close(persisted[field], row[field], field, count=max(row['n'], 1), tolerance=1e-9)
            for key in keys:
                part = joined[joined['doc_id'].eq(key[0]) & joined['past_band'].eq(key[1])]
                for arm in scores.ARMS:
                    row = arms[(*key, arm)]
                    resolved = part[f'resolved_mean_{arm}'].dropna()
                    if row['resolved_valid_count'] != len(resolved):
                        raise ValueError('resolved valid/null count differs from positions')
                    _close(row['sum_resolved_valid'], math.fsum(resolved), 'resolved sum', count=max(len(resolved), 1))
                    _close(row['sum_unseen_mass'], math.fsum(part[f'unseen_mass_{arm}']), 'unseen sum', count=max(len(part), 1))
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
    scores.pair_positions(frame[['slot_uid']], eligible[['slot_uid']])
    integer_columns = ('slot_uid', 'original_symbol_id', 'shuffled_symbol_id', 'shuffled_origin_slot_uid')
    for field in integer_columns:
        if not pd.api.types.is_integer_dtype(frame[field].dtype) or (frame[field] < 0).any():
            raise ValueError(f'{field}: expected nonnegative integer positions')
    for field in ('original_symbol_id', 'shuffled_symbol_id'):
        if (frame[field] >= record['m']).any():
            raise ValueError(f'{field}: symbol outside alphabet')
    for field in scores.POSITION_COLUMNS[4:]:
        values = frame[field]
        nullable = field.startswith('resolved_mean_')
        if not pd.api.types.is_float_dtype(values.dtype) or values.dtype.itemsize != 8:
            raise ValueError(f'{field}: positional diagnostics/losses require float64')
        for value in values:
            if nullable and pd.isna(value):
                continue
            _number(float(value), field)
            if field.startswith('unseen_mass_') and value > 1 + 1e-12:
                raise ValueError(f'{field}: mass exceeds one')
            if nullable and value > record['depth'] + 1e-12:
                raise ValueError(f'{field}: resolved length exceeds depth')
    original = eligible.set_index('slot_uid')['symbol_id']
    if not frame['original_symbol_id'].eq(frame['slot_uid'].map(original)).all():
        raise ValueError('original_symbol_id differs from coordinates')
    origins = coordinates[coordinates['variant'].eq(record['variant'])].set_index('slot_uid')
    if not origins.index.is_unique or not frame['shuffled_origin_slot_uid'].isin(origins.index).all():
        raise ValueError('shuffled provenance is missing or ambiguous')
    if (not frame['shuffled_origin_slot_uid'].is_unique
            or not frame['shuffled_symbol_id'].eq(frame['shuffled_origin_slot_uid'].map(origins['symbol_id'])).all()
            or not frame['slot_uid'].map(origins['sent_id']).eq(frame['shuffled_origin_slot_uid'].map(origins['sent_id'])).all()):
        raise ValueError('shuffled provenance differs from source symbol/sentence')
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


def aggregation_weights(blocks, training, folds, groups) -> pd.DataFrame:
    """§11.5: the weight each block carries under both weightings, beside its training quota and
    the §5.1 group shares of the training of the fold that evaluates it."""
    rows = []
    registry = pd.DataFrame({'held_block': list(groups), 'group': list(groups.values())})
    annotated = scores.annotate_scores(blocks, registry, on='held_block')
    for aggregation in scores.AGGREGATIONS:
        frame = annotated.assign(aggregation=aggregation)
        frame['weight'] = 1.0 if aggregation == scores.AGGREGATIONS[0] else frame['n'].astype(float)
        shares = frame.groupby(['cell', 'seed', 'group'])['weight'].transform('sum')
        rows.append(frame.assign(share=frame['weight'] / shares))
    weights = pd.concat(rows, ignore_index=True).rename(columns={'held_block': 'block'})
    merged = weights.merge(training, on=['cell', 'block'], how='left', validate='many_to_one').merge(
        folds, on=['cell', 'seed', 'block'], how='left', validate='many_to_one')
    return merged[['cell', 'seed', 'aggregation', 'block', 'held_block_key', 'group', 'n',
                   'weight', 'share', 'training_tokens', 'available_tokens', 'training_share',
                   *FOLD_COLUMNS]]


def training_quota(records) -> pd.DataFrame:
    """The tokens each block contributes to a training sample, beside the results (§11.5)."""
    frames = [pd.DataFrame(record['training']).assign(cell=record['cell']) for record in records]
    quota = pd.concat(frames, ignore_index=True).groupby(['cell', 'block'], sort=True,
                                                         as_index=False).agg(
        folds=('tokens', 'size'), training_tokens=('tokens', 'max'),
        available_tokens=('available', 'max'))
    quota['training_share'] = quota['training_tokens'] / quota['available_tokens']
    return quota


def fold_training(records, groups) -> pd.DataFrame:
    """§5.1: per fold, the share of training tokens from each group and from the test's own group."""
    rows = []
    for record in records:
        tokens = pd.DataFrame(record['training'])
        by_group = tokens.groupby(tokens['block'].map(groups))['tokens'].sum()
        total = int(tokens['tokens'].sum())
        rows.append({'cell': record['cell'], 'seed': record['seed'], 'block': record['held_block'],
                     'fold_training_tokens': total,
                     **{f'fold_share_{group}': int(by_group.get(group, 0)) / total
                        for group in (scores.HEX, scores.PROSE)},
                     'fold_share_own_group': int(by_group.get(groups[record['held_block']], 0)) / total})
    return pd.DataFrame(rows, columns=['cell', 'seed', 'block', *FOLD_COLUMNS])


def profiles(contrasts, blocks, docs) -> pd.DataFrame:
    """§8.2: the per-seed value of every reported unit — group, block and document — in one frame.

    Documents carry their two bands and their total, summed as the blocks' are (§11.5).
    """
    totals = scores.roll_up(docs, keys=[*KEY_COLUMNS, 'doc_id']).assign(past_band='all')
    documents = scores.ce_gain_q(pd.concat([docs, totals[docs.columns]], ignore_index=True))
    levels = (contrasts.assign(level='group', past_band='all').rename(columns={'group': 'unit'}),
              blocks.assign(level='block', aggregation=NOT_APPLICABLE)
              .rename(columns={'held_block': 'unit'}),
              documents.assign(level='document', aggregation=NOT_APPLICABLE)
              .rename(columns={'doc_id': 'unit'}))
    return pd.concat([frame[['cell', 'seed', *UNIT_COLUMNS, *scores.SCORE_COLUMNS]]
                      for frame in levels], ignore_index=True).melt(
        id_vars=['cell', 'seed', *UNIT_COLUMNS], var_name='metric', value_name='value')


def _summary(values) -> dict:
    """§8.2 across seeds; a bucket empty in every seed stays null with its reason (§9.3)."""
    values = pd.Series(values, dtype='float64')
    if values.isna().all():
        return {'mean': None, 'sd': None, 'min': None, 'max': None, 'S': len(values),
                'reason': diagnostics.EMPTY_BUCKET}
    if values.isna().any():
        raise ValueError('a bucket is empty in some seeds only; the evaluated population is fixed')
    return {**scores.seed_summary(values), 'reason': None}


def seed_summaries(long) -> pd.DataFrame:
    """§8.2 at every level: per seed first, then mean, SD with S-1, min, max and S — never an
    SD or an extreme of a lower level."""
    keys = ['cell', *UNIT_COLUMNS, 'metric']
    rows = [{**dict(zip(keys, key)), **_summary(part['value'])}
            for key, part in long.groupby(keys, sort=True)]
    return pd.DataFrame(rows, columns=list(SUMMARY_COLUMNS))


def sensitivity_pairs(long) -> pd.DataFrame:
    """§10: paired differences per block/seed and per group/seed, against C0 on the very same
    seeds — never on a changed set. Their summaries are rows of `seed_summaries`."""
    paired = long[long['level'].isin(('group', 'block'))]
    on = ['seed', *UNIT_COLUMNS, 'metric']
    reference = paired[paired['cell'].eq(REFERENCE_CELL)].drop(columns='cell')
    frames = []
    for cell, part in paired[paired['cell'].ne(REFERENCE_CELL)].groupby('cell', sort=True):
        joined = part.merge(reference, on=on, suffixes=('', '_reference'), validate='one_to_one')
        if len(joined) != len(part):
            raise ValueError(f'{cell}: {len(part) - len(joined)} rows have no {REFERENCE_CELL} '
                             'value on the same seed; a changed population is not a paired '
                             'comparison')
        frames.append(joined.assign(reference=REFERENCE_CELL, reference_value=joined['value_reference'],
                                    difference=joined['value'] - joined['value_reference']))
    if not frames:
        return pd.DataFrame(columns=list(PAIR_COLUMNS))
    return pd.concat(frames, ignore_index=True)[list(PAIR_COLUMNS)]


def fragment_diagnostics(records) -> pd.DataFrame:
    """§5.2/§11.5: the cut quantities of every contributor of every pair, shared by both arms."""
    frames = [pd.DataFrame(record['fragments'])
              .rename(columns={'block': 'contributor', 'block_key': 'contributor_key'})
              .assign(**{column: record[column] for column in KEY_COLUMNS}) for record in records]
    return pd.concat(frames, ignore_index=True)[list(FRAGMENT_COLUMNS)]


def model_diagnostics(records, resources) -> pd.DataFrame:
    """§11.5: supports, masses, root record, fingerprint and measured resources of every model."""
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
                          if name != 'node_count_by_structural_depth'},
                       node_count_by_structural_depth=' '.join(
                           str(count) for count in model['node_count_by_structural_depth']),
                       **{field: resources[(record['cell'], record['held_block_key'], record['seed'], arm)][field]
                          for field in RESOURCE_COLUMNS})
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
             'count': int(counts[name][symbol]),
             'empirical_frequency': float(counts[name][symbol] / counts[name].sum()),
             'smoothed_frequency': float(smoothed[name][symbol])}
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
    parser.add_argument('--regenerated-dir', type=Path,
                        help='the distinct seed-0 regeneration of §12.2; required for a scientific report')
    args = parser.parse_args(argv)
    started = time.perf_counter()
    cfg, deposited = scientific_run.load_projection(args.config, args.fixture)
    if deposited and args.regenerated_dir is None:
        raise ValueError('a scientific report verifies the §12.2 seed-0 regeneration (§14.2 step 6): '
                         '--regenerated-dir is required')
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
    check_evidence(prior['evidence'], contract, scientific=scientific)
    if scientific or 'V3' in prior['evidence']:
        validation_run.verify_technical(args.output_dir, prior, cfg, frames, scientific=scientific)
    steps.append(2)
    check_keys(cfg, prior['keys'])
    steps.append(3)
    records = validate_partitions(args.output_dir, prior, cfg, frames)
    coordinates = frames['coordinates.parquet']
    positional = [record for record in records if record['positions'] is not None]
    for record in positional:  # one partition in memory at a time (§11.4)
        check_positions(args.output_dir, record, cfg, coordinates)
    steps.append(4)
    docs = document_scores(records)
    check_roles(docs, frames['documents.csv'])
    arm = arm_diagnostics(records)
    check_keys(cfg, docs=docs, arm=arm)
    tables = r1_tables(cfg, coordinates)
    steps.append(5)
    blocks = block_pairs(docs)
    totals = blocks[blocks['past_band'].eq('all')]
    groups = scientific_run.groups_of(cfg)
    contrasts = group_contrasts(totals, groups)
    long = profiles(contrasts, blocks, docs)
    pairs = sensitivity_pairs(long)
    differences = pairs.assign(level=pairs['level'] + '_difference', value=pairs['difference'])
    tables.update({'document_scores.csv': scores.ce_gain_q(docs), 'block_pairs.csv': blocks,
                   'aggregation_weights.csv': aggregation_weights(
                       totals, training_quota(records), fold_training(records, groups), groups),
                   'contrasts.csv': contrasts,
                   'seed_summaries.csv': seed_summaries(
                       pd.concat([long, differences[long.columns]], ignore_index=True)),
                   'sensitivity_pairs.csv': pairs,
                   'fragment_diagnostics.csv': fragment_diagnostics(records),
                   'model_diagnostics.csv': model_diagnostics(records, {
                       tuple(row['key']): row for row in prior['metadata']['descriptive']['models']}),
                   'arm_diagnostics.csv': arm})
    regeneration = (None if args.regenerated_dir is None else validation_run.compare_regeneration(
        args.output_dir, args.regenerated_dir, cfg, frames))
    steps.append(6)
    if sorted(tables) != sorted(TABLES):
        raise ValueError(f'report: {sorted(set(tables) ^ set(TABLES))} is not a declared table')
    checks = {'steps': steps, 'scientific': scientific, 'reported_partitions': len(records),
              'positional_partitions': len(positional),
              'r1_pairs': int(len(tables['jsd_pairs.csv'])), 'regeneration': regeneration}
    body = {'keys': prior['keys'], 'checks': checks, 'evidence': prior['evidence'],
            'metadata': scientific_run.stage_metadata('report', corpus_dir=args.corpus_dir,
                                                      output_dir=args.output_dir, started=started)}
    manifest = scientific_run.publish_stage(args.output_dir, 'report', tables, contract, body,
                                            corpus_dir=args.corpus_dir)
    scientific_run.validate_run(args.output_dir)
    return manifest


if __name__ == '__main__':
    main()
