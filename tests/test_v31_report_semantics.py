"""Semantic validation of toy partitions, independent of byte/hash checks."""
import copy
import json

import numpy as np
import pandas as pd
import pytest
import yaml

from hexis.pipeline import run_descriptive, run_report, scientific_run
from hexis.protocols import scores
from test_v31_descriptive import toy_config, toy_frames

pytestmark = pytest.mark.v31


@pytest.fixture
def partition(tmp_path):
    cfg = yaml.safe_load(toy_config(tmp_path).read_text())
    frames = toy_frames()
    record, positions = run_descriptive.run_pair(cfg, frames, cfg['cells'][0], 'ALPHA', 0)
    key = (record['cell'], record['held_block_key'], record['seed'])
    manifest = {'keys': {'pair': [key], 'model': [(*key, arm) for arm in scores.ARMS]}}
    return tmp_path, cfg, frames, record, positions, manifest


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
    'training_tokens', 'shuffle_denominator'])
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
    elif fault == 'mass': arm['observed_mass_0'] += .1
    elif fault == 'resolved': arm['sum_resolved_valid'] += .1
    elif fault == 'unseen':
        arm['sum_unseen_mass'] += .01
        arm['observed_mass_0'] -= .01
    elif fault == 'model_arm': record['models'].pop('shuffled')
    elif fault == 'variant': record['variant'] = 'wrong'
    elif fault == 'position_duplicate': positions.loc[1, 'slot_uid'] = positions.loc[0, 'slot_uid']
    elif fault == 'position_nan': positions.loc[0, 'loss_ctw_original'] = np.nan
    elif fault == 'position_symbol': positions.loc[0, 'original_symbol_id'] = -1
    elif fault == 'model_histogram': record['models']['original']['support_histogram_1_2to4_5to9_10plus_by_depth'][0]['1'] += 1
    elif fault == 'training_tokens': record['models']['original']['training_tokens'] += 1
    elif fault == 'shuffle_denominator': record['shuffle']['evaluation']['total_count'] += 1
    with pytest.raises(ValueError) as error: validate(partition)
    assert str(error.value)


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
    table = run_report.r1_tables(cfg, toy_frames()['coordinates.parquet'])['root_distributions.csv']
    assert {'empirical_frequency', 'smoothed_frequency'} <= set(table)
    for _, part in table.groupby('block'):
        assert np.allclose(part['empirical_frequency'], part['count'] / part['count'].sum(), rtol=0, atol=1e-15)
        assert np.allclose(part['smoothed_frequency'], (part['count'] + .5) / (part['count'].sum() + 2.5), rtol=0, atol=1e-15)
