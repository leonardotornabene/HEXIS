"""Semantic validation of toy partitions, independent of byte/hash checks."""
import copy
import json

import numpy as np
import pandas as pd
import pytest
import yaml

from hexis.contracts import digest
from hexis.pipeline import run_descriptive, run_report, scientific_run
from hexis.protocols import sampling, scores
from test_v31_descriptive import toy_config, toy_frames

pytestmark = pytest.mark.v31


def build(tmp_path, cell):
    cfg = yaml.safe_load(toy_config(tmp_path).read_text())
    frames = toy_frames()
    record, positions = run_descriptive.run_pair(cfg, frames, cfg['cells'][cell], 'ALPHA', 0)
    ledger = record['sample_ledger']
    record['sample_ledger'] = scientific_run.ledger_name(record['ledger_sha256'])
    (tmp_path / record['sample_ledger']).write_text(json.dumps(ledger))
    key = (record['cell'], record['held_block_key'], record['seed'])
    manifest = {'keys': {'pair': [key], 'model': [(*key, arm) for arm in scores.ARMS]}}
    return tmp_path, cfg, frames, record, positions, manifest


@pytest.fixture
def partition(tmp_path):
    return build(tmp_path, 0)


@pytest.fixture
def sensitivity(tmp_path):
    """The same fold under the second cell: aggregates only, no positional vectors (§11.5)."""
    return build(tmp_path, 1)


def rehash_ledger(case, rows):
    """A consistent forgery: new digest, name, cardinality and training/fragment summaries
    recomputed from it, so only a regeneration from the RNG contract can refuse it."""
    output, cfg, frames, record, _, _ = case
    ledger = pd.DataFrame(rows, columns=list(sampling.LEDGER_COLUMNS))
    record['ledger_sha256'] = digest(rows)
    record['sample_ledger'] = scientific_run.ledger_name(record['ledger_sha256'])
    record['ledger_rows'] = len(rows)
    record['training'] = scientific_run.records(sampling.training_metrics(
        ledger, frames['sequences.parquet'], blocks=scientific_run.blocks_of(cfg), variant=record['variant']))
    record['fragments'] = scientific_run.records(sampling.fragment_metrics(ledger, record['depth']))
    (output / record['sample_ledger']).write_text(json.dumps(rows))


def validate(case):
    output, cfg, frames, record, positions, manifest = case
    (output / scientific_run.pair_name(record['cell'], record['held_block_key'], record['seed'])).write_text(json.dumps(record))
    if positions is not None:
        positions.to_parquet(output / scientific_run.positions_name(record['cell'], record['held_block_key'], record['seed']), index=False)
    return run_report.validate_partitions(output, manifest, cfg, frames)


@pytest.mark.parametrize('fault', ['extra', 'missing_positions', 'duplicate_document', 'duplicate_arm',
    'missing_arm', 'extra_sum', 'denominator', 'fractional_count', 'bool_count', 'nan_sum',
    'negative_sum', 'valid_count', 'mass', 'resolved', 'unseen', 'model_arm', 'variant',
    'position_duplicate', 'position_nan', 'position_symbol', 'model_histogram',
    'training_tokens', 'shuffle_denominator', 'training', 'fragments'])
def test_partition_semantic_corruption_is_rejected(partition, fault):
    _, _, _, record, positions, _ = partition
    sums, arm = record['document_sums'][0], record['arm_diagnostics'][0]
    if fault == 'extra': record['surprise'] = 1
    elif fault == 'missing_positions': record['positions'] = None
    elif fault == 'duplicate_document': record['document_sums'].append(copy.deepcopy(sums))
    elif fault == 'duplicate_arm': record['arm_diagnostics'].append(copy.deepcopy(arm))
    elif fault == 'missing_arm': record['arm_diagnostics'].pop()
    elif fault == 'extra_sum': sums['surprise'] = 1
    elif fault == 'denominator': sums['n'] += 1
    elif fault == 'fractional_count': sums['n'] = float(sums['n'])
    elif fault == 'bool_count': sums['n'] = True
    elif fault == 'nan_sum': sums['sum_loss_ctw_original'] = float('nan')
    elif fault == 'negative_sum': sums['sum_loss_ctw_original'] = -1.
    elif fault == 'valid_count': arm['resolved_valid_count'] -= 1
    elif fault == 'mass': arm['sum_observed_mass_by_length_0'] += .1
    elif fault == 'resolved': arm['sum_resolved_valid'] += .1
    elif fault == 'unseen':
        arm['sum_unseen_mass'] += .01
        arm['sum_observed_mass_by_length_0'] -= .01
    elif fault == 'model_arm': record['models'].pop('shuffled')
    elif fault == 'variant': record['variant'] = 'wrong'
    elif fault == 'position_duplicate': positions.loc[1, 'slot_uid'] = positions.loc[0, 'slot_uid']
    elif fault == 'position_nan': positions.loc[0, 'loss_ctw_original'] = np.nan
    elif fault == 'position_symbol': positions.loc[0, 'original_symbol_id'] = -1
    elif fault == 'model_histogram': record['models']['original']['support_histogram_1_2to4_5to9_10plus_by_depth'][0]['1'] += 1
    elif fault == 'training_tokens': record['models']['original']['training_tokens'] += 1
    elif fault == 'shuffle_denominator': record['shuffle']['evaluation']['total_slot_count'] += 1
    elif fault == 'training': record['training'][0]['tokens'] += 5
    elif fault == 'fragments': record['fragments'][0]['fragment_tokens'] += 1
    with pytest.raises(ValueError) as error: validate(partition)
    assert str(error.value)


@pytest.mark.parametrize('fault', ['held_out', 'inventory_only', 'offset'])
def test_the_persisted_ledger_is_the_contract_sample_even_after_rehashing(partition, fault):
    """T05/T24 on the campaign: held-out or inventory_only sentence, or a moved cut, with every
    count, digest and summary kept consistent — only the regenerated sample can see it."""
    output, _, frames, record, _, _ = partition
    rows = json.loads((output / record['sample_ledger']).read_text())
    if fault == 'offset':
        row = next(row for row in rows if row['fragment'])
        length = int(frames['sequences.parquet'].set_index('sent_id').at[row['sent_id'], 'encoded_length'])
        shift = 1 if row['end'] < length else -1
        row.update(start=row['start'] + shift, end=row['end'] + shift)
    else:
        doc = 'a' if fault == 'held_out' else 'z'  # ALPHA is held out; z is inventory_only
        rows[0].update(sent_id=f'{doc}@1', doc_id=doc, source_ordinal=1)
    rehash_ledger(partition, rows)
    with pytest.raises(ValueError, match='sample_ledger') as error:
        validate(partition)
    assert 'sample_ledger' in str(error.value)


@pytest.mark.parametrize('fault,pattern', [('training_changes', 'shuffle'), ('provenance_swap', 'shuffle_eval')])
def test_shuffle_counts_and_c0_provenance_are_the_contract_regeneration(partition, fault, pattern):
    """§5.3/§7: change counts and moved-token provenance are regenerated, never trusted."""
    _, _, frames, record, positions, _ = partition
    if fault == 'training_changes':  # still under its denominator
        counts = record['shuffle']['training']
        counts['changed_symbol_slot_count'] += -1 if counts['changed_symbol_slot_count'] else 1
    else:  # two slots of one sentence that received the same symbol swap their provenance
        sentence = positions['slot_uid'].map(frames['coordinates.parquet'].set_index('slot_uid')['sent_id'])
        first, second = next((i, j) for i in positions.index for j in positions.index
                             if i < j and sentence[i] == sentence[j]
                             and positions.at[i, 'shuffled_symbol_id'] == positions.at[j, 'shuffled_symbol_id'])
        origins = positions.loc[[first, second], 'shuffled_origin_slot_uid'].to_numpy()
        positions.loc[[first, second], 'shuffled_origin_slot_uid'] = origins[::-1]
    with pytest.raises(ValueError, match=pattern) as error:
        validate(partition)
    assert pattern in str(error.value)


@pytest.mark.parametrize('fault,pattern', [
    ('sum_value', 'reconstructed'), ('original_symbol', 'original_symbol_id differs'),
    ('provenance_sentence', 'source symbol/sentence'), ('ledger_bytes', 'ledger digest')])
def test_each_c0_guard_names_its_own_corruption(partition, fault, pattern):
    """Each §14.2 step-4 guard is exercised by the corruption it exists for (mutation-verified gap)."""
    output, _, frames, record, positions, _ = partition
    coordinates = frames['coordinates.parquet']
    if fault == 'sum_value':  # finite and positive: only the C0 reconstruction sees it
        record['document_sums'][0]['sum_loss_ctw_original'] += 0.5
    elif fault == 'original_symbol':  # another valid id: only the coordinate map sees it
        positions.loc[0, 'original_symbol_id'] = (positions.loc[0, 'original_symbol_id'] + 1) % record['m']
    elif fault == 'provenance_sentence':  # same symbol, another sentence, still unique
        sentence = coordinates.set_index('slot_uid').at[int(positions.loc[0, 'slot_uid']), 'sent_id']
        elsewhere = coordinates[coordinates['sent_id'].ne(sentence)
                                & coordinates['symbol_id'].eq(positions.loc[0, 'shuffled_symbol_id'])
                                & ~coordinates['slot_uid'].isin(positions['shuffled_origin_slot_uid'])]
        positions.loc[0, 'shuffled_origin_slot_uid'] = int(elsewhere['slot_uid'].iloc[0])
    else:  # the file changes, its recorded digest does not
        path = output / record['sample_ledger']
        rows = json.loads(path.read_text())
        rows[0]['sample_subseed'] = '0'
        path.write_text(json.dumps(rows))
    with pytest.raises(ValueError, match=pattern) as error:
        validate(partition)
    assert pattern in str(error.value)


@pytest.mark.parametrize('fault,pattern', [('valid_count', 'diagnostic denominator'),
                                           ('resolved_bound', 'resolved sum exceeds')])
def test_sensitivity_partitions_enforce_diagnostic_denominators_and_bounds(sensitivity, fault, pattern):
    """Without positional vectors (§11.4) these bounds are a sensitivity's only diagnostic check."""
    _, _, _, record, positions, _ = sensitivity
    assert positions is None and record['positions'] is None
    arm = record['arm_diagnostics'][0]
    if fault == 'valid_count':
        arm['resolved_valid_count'] -= 1
    else:
        arm['sum_resolved_valid'] = arm['resolved_valid_count'] * record['depth'] + 1.0
    with pytest.raises(ValueError, match=pattern) as error:
        validate(sensitivity)
    assert pattern in str(error.value)


def test_duplicate_json_fields_in_pair_are_rejected(partition):
    assert len(validate(partition)) == 1
    output, cfg, frames, record, _, manifest = partition
    path = output/scientific_run.pair_name(record['cell'], record['held_block_key'], record['seed'])
    path.write_text(path.read_text().replace('"seed": 0', '"seed": 1, "seed": 0'))
    with pytest.raises(ValueError, match='duplicate') as error:
        run_report.validate_partitions(output, manifest, cfg, frames)
    assert str(error.value)


def test_partial_campaign_validates_and_float_reconstruction_allows_roundoff(partition):
    partition[3]['document_sums'][0]['sum_loss_ctw_original'] += 1e-10
    partition[3]['arm_diagnostics'][0]['sum_resolved_valid'] += 1e-13
    assert len(validate(partition)) == 1


def test_root_distribution_preserves_empirical_and_smoothed_frequencies(tmp_path):
    cfg = yaml.safe_load(toy_config(tmp_path).read_text())
    frames = toy_frames()
    table = run_report.r1_tables(cfg, frames['coordinates.parquet'], frames['alphabets.json'])['root_distributions.csv']
    names = frames['alphabets.json']['toy']['symbols']
    assert table['symbol'].tolist() == [names[index] for index in table['symbol_id']]
    assert {'empirical_frequency', 'smoothed_frequency'} <= set(table)
    for _, part in table.groupby('block'):
        assert np.allclose(part['empirical_frequency'], part['count'] / part['count'].sum(), rtol=0, atol=1e-15)
        assert np.allclose(part['smoothed_frequency'], (part['count'] + .5) / (part['count'].sum() + 2.5), rtol=0, atol=1e-15)
