"""V2 scores and diagnostics: four losses, coupled slots, aggregations, masses.

Every fixture is synthetic and tiny (piano §12): no Greek corpus row is fitted or
scored here, and no model in this file ever sees a real sequence. The §7
sign-inversion counterexample is the archived one of
`HEXIS_v3_allegati/diagnostics_validation.json`, reproduced through the canonical
CTW instead of the historical prototype.
"""
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from hexis.model import diagnostics
from hexis.model.context_tree import CTW, CTWParams
from hexis.protocols import sampling, scores

pytestmark = pytest.mark.v31

ROOT = Path(__file__).resolve().parents[1]
ARCHIVED = json.loads((ROOT / 'docs/contracts/hexis-3.1/HEXIS_v3_allegati'
                       / 'diagnostics_validation.json').read_text(encoding='utf-8'))
CE_ATOL = 1e-9  # §6.5 CE reconstruction tolerance, bits per symbol


# --- fixtures -----------------------------------------------------------------

def model(streams, m, depth=8, a=0.5):
    return CTW(CTWParams.from_rho(m=m, depth=depth, a=a, rho=0.5)).fit(streams)


def stream(sent_id, symbols, *, block='k' * 64, first_slot=0, origin=None):
    """One reset stream in the shape `sampling` hands to the scorer."""
    slots = list(range(first_slot, first_slot + len(symbols)))
    built = {'sent_id': sent_id, 'block_key': block, 'start': 0, 'end': len(symbols),
             'symbols': list(symbols), 'slot_uids': slots}
    return built if origin is None else built | {'source_slot_uids': list(origin)}


def frame(spec, variant='toy'):
    """A sequences frame: {doc_id: [symbol list, ...]}, one part, ordinals from 1."""
    rows, slot = [], 0
    for doc, sentences in spec.items():
        for ordinal, symbols in enumerate(sentences, start=1):
            rows.append({'variant': variant, 'role': 'primary', 'doc_id': doc,
                         'sent_id': f'{doc}@{ordinal}', 'part_order': 1,
                         'source_ordinal': ordinal, 'encoded_length': len(symbols),
                         'symbols': list(symbols),
                         'slot_uids': list(range(slot, slot + len(symbols)))})
            slot += len(symbols)
    return pd.DataFrame(rows)


def protocol(spec, blocks, held, *, m, q, seed=0, depth=8):
    """§7 steps 1–6 on synthetic data: two fitted arms and the paired test streams."""
    sequences = frame(spec)
    keys = {name: sampling.block_key(docs) for name, docs in blocks.items()}
    ledger = sampling.sample_fold(sequences, variant='toy', blocks=blocks,
                                  held_block=held, q=q, seed=seed)
    train = sampling.sample_streams(ledger, sequences, 'toy')
    train_shuffled = sampling.shuffle_streams(train, seed=seed, held=keys[held],
                                              purpose='shuffle_train')
    test = sampling.evaluation_streams(sequences, variant='toy', docs=blocks[held],
                                       block=keys[held])
    test_shuffled = sampling.shuffle_streams(test, seed=seed, held=keys[held],
                                             purpose='shuffle_eval')
    return (model([s['symbols'] for s in train], m, depth),
            model([s['symbols'] for s in train_shuffled], m, depth),
            test, test_shuffled)


def cycle(length, period, offset=0):
    return [(offset + index) % period for index in range(length)]


def positions_frame(rows):
    """Hand-written position rows: (doc, block, sent, past, four losses)."""
    return pd.DataFrame(
        [{'block': block, 'doc_id': doc, 'sent_id': sent, 'available_past': past,
          'past_band': scores.past_band(past), 'slot_uid': index,
          'original_symbol_id': 0, 'shuffled_symbol_id': 0, 'shuffled_origin_slot_uid': index,
          'loss_ctw_original': o_ctw, 'loss_root_original': o_root,
          'loss_ctw_shuffled': s_ctw, 'loss_root_shuffled': s_root,
          'unseen_mass_original': 0.0, 'unseen_mass_shuffled': 0.0,
          'resolved_mean_original': 0.0, 'resolved_mean_shuffled': 0.0}
         for index, (block, doc, sent, past, o_ctw, o_root, s_ctw, s_root) in enumerate(rows)])


# --- T19: the four terms of Q --------------------------------------------------

def test_public_core_and_annotation_keep_scores_independent_of_labels():
    trained = model([[0, 1] * 8], m=2)
    original = stream('a@1', [0, 1, 0, 1, 0, 1])
    shuffled = stream('a@1', [1, 0, 1, 0, 1, 0], origin=[1, 0, 3, 2, 5, 4])
    before = trained.fingerprint()
    positions, diagnostics = scores.pooled_score_core(
        [original], [shuffled], model_original=trained, model_shuffled=trained)
    registry = pd.DataFrame({'sent_id': ['a@1'], 'regime': ['HEX'], 'group': ['HEX']})
    annotated = scores.annotate_scores(positions, registry, on='sent_id')
    relabelled = registry.assign(regime='PROSE_POST', group='PROSE_ALL')
    changed = scores.annotate_scores(positions, relabelled, on='sent_id')
    assert annotated['group'].tolist() == ['HEX', 'HEX']
    assert changed['group'].tolist() == ['PROSE_ALL', 'PROSE_ALL']
    pd.testing.assert_frame_equal(annotated[positions.columns], positions)
    pd.testing.assert_frame_equal(changed[positions.columns], positions)
    again, again_diagnostics = scores.pooled_score_core(
        [original | {'regime': 'OTHER_VERSE'}], [shuffled | {'group': 'anything'}],
        model_original=trained, model_shuffled=trained)
    assert positions.to_csv(index=False) == again.to_csv(index=False)
    assert diagnostics.to_csv(index=False) == again_diagnostics.to_csv(index=False)
    assert trained.fingerprint() == before
    assert set(positions).isdisjoint({'regime', 'group'})


@pytest.mark.parametrize('fault', ['duplicate', 'missing', 'null', 'overwrite'])
def test_annotation_refuses_ambiguous_missing_or_overwriting_registry(fault):
    fixed = pd.DataFrame({'doc_id': ['a', 'b'], 'q': [0.1, -0.2]})
    registry = pd.DataFrame({'doc_id': ['a', 'b'], 'group': ['HEX', 'PROSE_ALL']})
    if fault == 'duplicate':
        registry = pd.concat([registry, registry.iloc[:1]], ignore_index=True)
    elif fault == 'missing':
        registry = registry.iloc[:1]
    elif fault == 'null':
        registry.loc[1, 'doc_id'] = None
    else:
        registry['q'] = 99.0
    with pytest.raises(ValueError) as exc:
        scores.annotate_scores(fixed, registry)
    assert str(exc.value)
    assert fixed['q'].tolist() == [0.1, -0.2]

def test_four_term_q_reproduces_the_archived_sign_inversion():
    """§7: the shortcut CE_CTW_R − CE_CTW_O can even flip the sign of Q."""
    trained = model([[0] * 6 + [1] * 2], m=2)
    original = stream('fixture@1', [0, 0, 0, 0, 1, 1, 1, 1])
    shuffled = stream('fixture@1', [1, 1, 1, 1, 0, 0, 0, 0], origin=[4, 5, 6, 7, 0, 1, 2, 3])
    positions, _ = scores.score_streams([original], [shuffled],
                                        model_original=trained, model_shuffled=trained)

    block = scores.ce_gain_q(scores.roll_up(scores.aggregate(positions))).iloc[0]
    reference = ARCHIVED['root_non_cancellation']
    assert block['n'] == 4
    assert abs(block['q'] - reference['Q']) < CE_ATOL
    assert abs(block['ce_root_original'] - block['ce_root_shuffled']
               - reference['root_difference']) < CE_ATOL

    shortcut = block['ce_ctw_shuffled'] - block['ce_ctw_original']
    assert abs(shortcut - reference['incorrect_shortcut']) < CE_ATOL
    assert shortcut < 0.0 < block['q']  # the archived sign inversion, not a rounding gap


def test_q_needs_the_four_terms_of_two_independently_fitted_arms():
    """§8.1 on the §7 call sequence; `evaluate` cross-checks the per-slot losses."""
    spec = {'h1': [cycle(14, 3, i) for i in range(4)],
            'p1': [cycle(13, 4, i) + [4] for i in range(4)],
            'p2': [cycle(12, 5, i) for i in range(4)]}
    blocks = {'H': ['h1'], 'P1': ['p1'], 'P2': ['p2']}
    original, shuffled, test, test_shuffled = protocol(spec, blocks, 'H', m=5, q=30)

    positions, _ = scores.score_streams(test, test_shuffled, model_original=original,
                                        model_shuffled=shuffled)
    block = scores.ce_gain_q(scores.roll_up(scores.aggregate(positions))).iloc[0]

    assert block['q'] == pytest.approx(
        (block['ce_root_original'] - block['ce_ctw_original'])
        - (block['ce_root_shuffled'] - block['ce_ctw_shuffled']), abs=1e-12)
    for arm, fitted, streams in (('original', original, test), ('shuffled', shuffled, test_shuffled)):
        reference = fitted.evaluate([s['symbols'] for s in streams], min_available_past=4)
        assert block['n'] == reference.n
        assert abs(block[f'ce_ctw_{arm}'] - reference.ce) < CE_ATOL
        assert abs(block[f'ce_root_{arm}'] - reference.root_ce) < CE_ATOL


def test_slots_are_paired_one_to_one_and_a_mismatch_is_refused():
    """§7 step 6: shuffle moves the symbol, never the slot; the join is verified."""
    spec = {'h1': [cycle(11, 3, i) for i in range(3)], 'p1': [cycle(10, 4, i) for i in range(3)]}
    blocks = {'H': ['h1'], 'P': ['p1']}
    original, shuffled, test, test_shuffled = protocol(spec, blocks, 'H', m=4, q=20)
    assert [s['slot_uids'] for s in test] == [s['slot_uids'] for s in test_shuffled]

    positions, _ = scores.score_streams(test, test_shuffled, model_original=original,
                                        model_shuffled=shuffled)
    assert positions['slot_uid'].is_unique

    broken = [s | {'slot_uids': [slot + 1 for slot in s['slot_uids']]} for s in test_shuffled]
    with pytest.raises(ValueError, match='slot'):
        scores.score_streams(test, broken, model_original=original, model_shuffled=shuffled)
    with pytest.raises(ValueError, match='0 eligible|no eligible'):
        scores.score_streams([stream('short@1', [0, 1, 2])], [stream('short@1', [2, 1, 0], origin=[2, 1, 0])],
                             model_original=original, model_shuffled=shuffled)
    with pytest.raises(ValueError, match='sent_id'):  # never merge two streams into one record
        scores.score_streams(test + test[:1], test_shuffled + test_shuffled[:1],
                             model_original=original, model_shuffled=shuffled)


def test_score_streams_refuses_an_alphabet_size_mismatch():
    """A smaller-alphabet arm paired with a larger one would misindex CE_0/CE_CTW silently."""
    small = model([[0, 1, 0, 1, 0, 1]], m=2, depth=4)
    large = model([[0, 1, 2, 3, 0, 1, 2, 3]], m=4, depth=4)
    original = stream('fixture@1', [0, 1, 0, 1, 0, 1])
    shuffled = stream('fixture@1', [1, 0, 1, 0, 1, 0], origin=[1, 0, 3, 2, 5, 4])
    with pytest.raises(ValueError) as excinfo:
        scores.score_streams([original], [shuffled], model_original=small, model_shuffled=large)
    assert 'alphabet' in str(excinfo.value)


def test_score_streams_refuses_a_negative_min_available_past():
    """Mirrors CTW.evaluate's own guard on the identical parameter (context_tree.py)."""
    trained = model([[0, 1, 0, 1, 0, 1]], m=2, depth=4)
    original = stream('fixture@1', [0, 1, 0, 1, 0, 1])
    shuffled = stream('fixture@1', [1, 0, 1, 0, 1, 0], origin=[1, 0, 3, 2, 5, 4])
    with pytest.raises(ValueError) as excinfo:
        scores.score_streams([original], [shuffled], model_original=trained, model_shuffled=trained,
                             min_available_past=-1)
    assert 'min_available_past' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        scores.score_streams([original], [shuffled], model_original=trained, model_shuffled=trained,
                             min_available_past=2.5)
    assert 'min_available_past' in str(excinfo.value)


# --- T18 residual: no universal G_R = 0 ---------------------------------------

def test_shuffled_gain_is_not_automatically_zero_on_a_heterogeneous_pool():
    """§7: G_R null in a pilot is an observation, never an identity.

    Two dialects, {0,1} and {2,3}, never mixed inside a sentence. The within-
    sentence shuffle keeps each multiset, so the shuffled arm still learns which
    dialect a context is in and beats its own root.
    """
    spec = {'h1': [[0, 1] * 7, [1, 0] * 7, [0, 0, 1] * 5], 'p1': [[2, 3] * 7, [3, 2] * 7, [2, 2, 3] * 5],
            'p2': [[0, 1, 1] * 5, [2, 3, 3] * 5, [1, 0] * 7]}
    blocks = {'H': ['h1'], 'P1': ['p1'], 'P2': ['p2']}
    original, shuffled, test, test_shuffled = protocol(spec, blocks, 'P2', m=4, q=24)

    changed = sum(s['changed_count'] for s in test_shuffled)
    total = sum(s['total_count'] for s in test_shuffled)
    assert 0 < changed < total  # §7: an explicit denominator, no resampling for change

    positions, _ = scores.score_streams(test, test_shuffled, model_original=original,
                                        model_shuffled=shuffled)
    block = scores.ce_gain_q(scores.roll_up(scores.aggregate(positions))).iloc[0]
    assert block['g_shuffled'] > 0.05
    assert abs(block['q'] - block['g_original']) > 0.05  # assuming G_R = 0 would misstate Q


# --- T20: losses to documents, blocks, groups; two weightings -----------------

def test_losses_sum_through_documents_blocks_and_groups():
    """§8.2: sum the losses and divide by the targets — never a mean of means."""
    rows = [('HEX', 'h1', 'h1@1', 4, 3.0, 5.0, 4.0, 5.0),
            ('HEX', 'h1', 'h1@1', 9, 1.0, 5.0, 2.0, 5.0),
            ('HEX', 'h2', 'h2@1', 4, 9.0, 5.0, 6.0, 5.0),
            ('PROSE_ALL', 'p1', 'p1@1', 5, 2.0, 4.0, 3.0, 4.0),
            ('PROSE_ALL', 'p1', 'p1@2', 8, 4.0, 4.0, 3.0, 4.0),
            ('PROSE_ALL', 'p1', 'p1@2', 11, 6.0, 4.0, 5.0, 4.0)]
    positions = positions_frame(rows)

    documents = scores.ce_gain_q(scores.roll_up(scores.aggregate(positions, ('block', 'doc_id')),
                                                ('block', 'doc_id'))).set_index('doc_id')
    assert documents.loc['h1', 'n'] == 2
    assert documents.loc['h1', 'ce_ctw_original'] == pytest.approx(2.0)  # (3+1)/2, not (3+1)/2 of means
    assert documents.loc['h2', 'ce_ctw_original'] == pytest.approx(9.0)

    blocks = scores.ce_gain_q(scores.roll_up(scores.aggregate(positions, ('block',)), ('block',))
                              ).set_index('block')
    assert blocks.loc['HEX', 'n'] == 3
    assert blocks.loc['HEX', 'ce_ctw_original'] == pytest.approx(13.0 / 3)  # ≠ (2.0 + 9.0)/2
    assert blocks.loc['HEX', 'g_original'] == pytest.approx(5.0 - 13.0 / 3)

    bands = scores.aggregate(positions, ('block',)).set_index(['block', 'past_band'])
    assert bands.loc[('HEX', '4_7'), 'n'] + bands.loc[('HEX', 'ge8'), 'n'] == blocks.loc['HEX', 'n']
    assert (bands.loc[('HEX', '4_7'), 'sum_loss_ctw_original']
            + bands.loc[('HEX', 'ge8'), 'sum_loss_ctw_original']) == pytest.approx(13.0)


def test_roll_up_casts_count_columns_to_int64_in_both_branches():
    """§11.5: the keyless total and the keyed groupby must agree on dtype, not
    just value, even when handed a sums frame whose counts are not already
    int64 (e.g. one that did not pass through `aggregate`)."""
    sums = pd.DataFrame({
        'block': ['H', 'H', 'P'],
        'n': pd.array([4.0, 5.0, 3.0], dtype='float64'),
        'changed_symbol_eligible_slot_count': pd.array([1.0, 2.0, 0.0], dtype='float64'),
        'eligible_slot_count': pd.array([4.0, 5.0, 3.0], dtype='float64'),
        'sum_loss_ctw_original': [3.0, 1.0, 2.0], 'sum_loss_root_original': [5.0, 5.0, 4.0],
        'sum_loss_ctw_shuffled': [4.0, 2.0, 3.0], 'sum_loss_root_shuffled': [5.0, 5.0, 4.0]})

    totaled = scores.roll_up(sums)
    for column in scores.COUNT_COLUMNS:
        assert totaled[column].dtype == np.int64, column

    by_block = scores.roll_up(sums, ('block',))
    for column in scores.COUNT_COLUMNS:
        assert by_block[column].dtype == np.int64, column


def test_both_weightings_report_four_components_and_agree_on_d_q():
    """§8.2: D_Q^equal and D_Q^target, each with D_Q = D_G_O − D_G_R."""
    blocks = pd.DataFrame(
        [{'block': 'HEX_A', 'n': 40}, {'block': 'HEX_B', 'n': 5},
         {'block': 'P_A', 'n': 30}, {'block': 'P_B', 'n': 20}, {'block': 'P_C', 'n': 2}])
    blocks['ce_ctw_original'] = [3.0, 2.0, 3.5, 3.0, 1.0]
    blocks['ce_root_original'] = [5.0, 5.0, 5.0, 5.0, 5.0]
    blocks['ce_ctw_shuffled'] = [4.0, 4.5, 4.0, 4.2, 2.0]
    blocks['ce_root_shuffled'] = [5.0, 5.0, 5.0, 5.0, 5.0]
    blocks['g_original'] = blocks['ce_root_original'] - blocks['ce_ctw_original']
    blocks['g_shuffled'] = blocks['ce_root_shuffled'] - blocks['ce_ctw_shuffled']
    blocks['q'] = blocks['g_original'] - blocks['g_shuffled']
    groups = {'HEX_A': 'HEX', 'HEX_B': 'HEX', 'P_A': 'PROSE_ALL', 'P_B': 'PROSE_ALL', 'P_C': 'PROSE_ALL'}

    table = scores.contrasts(blocks, groups).set_index(['aggregation', 'group'])
    for aggregation in ('equal_block', 'eligible_token_weighted'):
        row = table.loc[(aggregation, 'contrast')]
        assert row['q'] == pytest.approx(row['g_original'] - row['g_shuffled'], abs=1e-12)
        for arm in ('original', 'shuffled'):
            assert row[f'g_{arm}'] == pytest.approx(
                row[f'ce_root_{arm}'] - row[f'ce_ctw_{arm}'], abs=1e-12)

    equal = table.loc[('equal_block', 'contrast'), 'q']
    weighted = table.loc[('eligible_token_weighted', 'contrast'), 'q']
    assert equal == pytest.approx(blocks['q'][:2].mean() - blocks['q'][2:].mean())
    hex_rows, prose_rows = blocks.iloc[:2], blocks.iloc[2:]
    assert weighted == pytest.approx(
        (hex_rows['n'] * hex_rows['q']).sum() / hex_rows['n'].sum()
        - (prose_rows['n'] * prose_rows['q']).sum() / prose_rows['n'].sum())
    assert abs(equal - weighted) > 1e-3  # unequal denominators: the two weightings differ

    blocks.loc[blocks['block'].eq('P_C'), 'q'] = np.nan
    with pytest.raises(ValueError, match='P_C'):
        scores.contrasts(blocks, groups)


# --- T21: paired sensitivities over the first ten seeds -----------------------

def test_paired_sensitivities_over_the_first_ten_seeds_detect_a_population_mismatch():
    """§8.2/§11.5: aggregate per seed first, then mean/SD/min/max/S on the seeds."""
    spec = {'h1': [cycle(12, 3, i) for i in range(5)], 'p1': [cycle(11, 4, i) for i in range(5)],
            'p2': [cycle(13, 5, i) for i in range(5)]}
    blocks = {'H': ['h1'], 'P1': ['p1'], 'P2': ['p2']}

    per_seed = {}
    for cell, depth in (('C0', 8), ('D12', 12)):
        values = []
        for seed in range(10):
            original, shuffled, test, test_shuffled = protocol(
                spec, blocks, 'H', m=5, q=24, seed=seed, depth=depth)
            positions, _ = scores.score_streams(test, test_shuffled, model_original=original,
                                                model_shuffled=shuffled)
            values.append(float(scores.ce_gain_q(
                scores.roll_up(scores.aggregate(positions))).iloc[0]['q']))
        per_seed[cell] = values

    summary = scores.seed_summary(per_seed['C0'])
    assert summary['S'] == 10
    assert summary['mean'] == pytest.approx(float(np.mean(per_seed['C0'])))
    assert summary['sd'] == pytest.approx(float(np.std(per_seed['C0'], ddof=1)))
    assert summary['min'] == min(per_seed['C0']) and summary['max'] == max(per_seed['C0'])
    assert scores.seed_summary([1.5])['sd'] is None  # S = 1: no S−1 denominator

    differences = [d12 - c0 for c0, d12 in zip(per_seed['C0'], per_seed['D12'])]
    assert scores.seed_summary(differences)['mean'] == pytest.approx(
        scores.seed_summary(per_seed['D12'])['mean'] - summary['mean'])
    assert scores.seed_summary(differences)['S'] == 10

    # OTH changes the target population: the join must refuse, not line rows up.
    original, shuffled, test, test_shuffled = protocol(spec, blocks, 'H', m=5, q=24)
    positions, _ = scores.score_streams(test, test_shuffled, model_original=original,
                                        model_shuffled=shuffled)
    paired = scores.pair_positions(positions, positions.copy())
    assert len(paired) == len(positions)
    wider = pd.concat([positions, positions.tail(1).assign(slot_uid=10 ** 6)], ignore_index=True)
    with pytest.raises(ValueError, match='slot'):
        scores.pair_positions(positions, wider)
    with pytest.raises(ValueError, match='unique|duplicate'):
        scores.pair_positions(positions, pd.concat([positions, positions.tail(1)], ignore_index=True))


# --- T22: masses, supports and L_resolved -------------------------------------

def test_mixture_masses_and_resolved_length_follow_the_direct_sum():
    """§9.2: R is the direct sum of the observed masses, never 1 − unseen_mass."""
    trained = model([[0, 1, 2, 0, 1, 2, 0, 1, 2, 0]], m=3)
    record = diagnostics.resolved(trained.mixture([0, 1, 2, 0, 1]))
    mass = record['mass_by_length']
    assert math.isclose(sum(mass.values()) + record['unseen_mass'], 1.0, abs_tol=1e-12)
    assert record['resolved_mean'] == pytest.approx(
        sum(length * weight for length, weight in mass.items()) / sum(mass.values()))
    assert record['reason'] is None

    flat = diagnostics.resolved(model([[0, 1, 2, 0]], m=3, depth=0).mixture([0, 1]))
    assert flat['mass_by_length'] == {0: pytest.approx(1.0)} and flat['unseen_mass'] == 0.0
    assert flat['resolved_mean'] == 0.0  # a forced root leaf resolves at lexical length 0

    empty = diagnostics.resolved(model([], m=3).mixture([0, 1]))
    assert empty['unseen_mass'] == 1.0 and empty['mass_by_length'] == {}
    assert empty['resolved_mean'] is None and empty['reason'] == 'no_resolved_mass'


def test_evaluation_diagnostics_count_valid_and_null_resolved_means():
    """§9.3: mean L = sum of valid values / valid count; nulls are counted, not zeroed."""
    trained = model([[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]], m=3)
    untrained = model([], m=3)
    original = stream('toy@1', [0, 1, 2, 0, 1, 2, 0, 1, 2, 0])
    shuffled = stream('toy@1', [2, 1, 0, 2, 1, 0, 2, 1, 0, 2], origin=list(range(10)))

    positions, per_arm = scores.score_streams([original], [shuffled],
                                              model_original=trained, model_shuffled=untrained)
    assert len(positions) == 6
    assert np.allclose(positions['loss_ctw_shuffled'], math.log2(3))  # empty training: uniform
    assert positions['resolved_mean_shuffled'].isna().all()
    assert positions['resolved_mean_original'].notna().all()

    totals = per_arm.groupby('arm').sum(numeric_only=True)
    assert totals.loc['shuffled', 'resolved_valid_count'] == 0
    assert totals.loc['shuffled', 'resolved_null_count_no_resolved_mass'] == 6
    assert totals.loc['shuffled', 'sum_unseen_mass'] == pytest.approx(6.0)
    assert totals.loc['shuffled', 'root_unseen_target_count'] == 6  # empty training observes nothing
    assert totals.loc['original', 'resolved_valid_count'] == 6
    assert totals.loc['original', 'sum_resolved_valid'] == pytest.approx(
        positions['resolved_mean_original'].sum())

    valid = diagnostics.means(per_arm[per_arm['arm'].eq('original')].sum(numeric_only=True))
    assert valid['L'] == pytest.approx(positions['resolved_mean_original'].mean())
    assert valid['reason'] is None
    null = diagnostics.means(per_arm[per_arm['arm'].eq('shuffled')].sum(numeric_only=True))
    assert null['L'] is None and null['reason'] == 'no_resolved_mass'
    assert null['unseen'] == pytest.approx(1.0)

    observed = [column for column in per_arm.columns if column.startswith('observed_mass_')]
    assert len(observed) == 9  # ℓ = 0..D
    assert per_arm[per_arm['arm'].eq('original')][observed].to_numpy().sum() \
        + totals.loc['original', 'sum_unseen_mass'] == pytest.approx(6.0, abs=1e-12)
    assert totals.loc['original', 'implicit_unseen_branch_encounter_count'] >= 0


def test_an_empty_band_is_null_with_a_reason_and_never_a_false_zero():
    """§9.3: n = 0, additive sums 0, CE/G/Q null with reason empty_bucket."""
    trained = model([[0, 1, 2, 3] * 3], m=4)
    original = stream('short@1', [0, 1, 2, 3, 0, 1])
    shuffled = stream('short@1', [1, 0, 3, 2, 1, 0], origin=[1, 0, 3, 2, 5, 4])
    positions, per_arm = scores.score_streams([original], [shuffled],
                                              model_original=trained, model_shuffled=trained)
    assert set(positions['past_band']) == {'4_7'}

    banded = scores.ce_gain_q(scores.aggregate(positions)).set_index('past_band')
    assert list(banded.index) == ['4_7', 'ge8']  # the empty band is a row, not an absence
    empty = banded.loc['ge8']
    assert empty['n'] == 0
    assert empty[[column for column in banded.columns if column.startswith('sum_')]].eq(0).all()
    assert all(pd.isna(empty[column]) for column in
               ('ce_ctw_original', 'ce_root_original', 'ce_ctw_shuffled', 'ce_root_shuffled',
                'g_original', 'g_shuffled', 'q'))
    assert empty['reason'] == 'empty_bucket'
    assert banded.loc['4_7', 'reason'] is None
    assert set(per_arm['past_band']) == {'4_7', 'ge8'}
    empty_arm = diagnostics.means(per_arm[per_arm['past_band'].eq('ge8')].sum(numeric_only=True))
    assert empty_arm == {'L': None, 'unseen': None, 'mass': None, 'reason': 'empty_bucket'}
