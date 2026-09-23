"""R1: JSD of the complete retained counts (plan §8.3), with its own fixtures.

R1 needs no CTW, no seed and no sample, so nothing here is shared with the score
tests: toy blocks of invented counts over a five-symbol alphabet. No Greek corpus
row is read.
"""
import itertools
import math

import numpy as np
import pandas as pd
import pytest

from hormathos.protocols import r1

pytestmark = pytest.mark.v31

BLOCKS = {'HEX_A': ['a1', 'a2'], 'HEX_B': ['b1'], 'P_A': ['c1'], 'P_B': ['d1'],
          'P_C': ['e1'], 'P_D': ['f1'], 'P_E': ['g1']}
GROUPS = {'HEX_A': 'HEX', 'HEX_B': 'HEX', 'P_A': 'PROSE_ALL', 'P_B': 'PROSE_ALL',
          'P_C': 'PROSE_ALL', 'P_D': 'PROSE_ALL', 'P_E': 'PROSE_ALL'}
COUNTS = {'HEX_A': [40, 30, 20, 10, 0], 'HEX_B': [38, 31, 18, 12, 1],
          'P_A': [10, 10, 30, 40, 10], 'P_B': [12, 9, 28, 42, 9], 'P_C': [11, 11, 29, 39, 10],
          'P_D': [9, 12, 31, 38, 10], 'P_E': [10, 10, 30, 40, 10]}
M = 5


def distributions():
    return {block: r1.smoothed(counts) for block, counts in COUNTS.items()}


def coordinates():
    """A coordinates frame in the shape `corpus` writes: retained tokens only."""
    rows = []
    for block, docs in BLOCKS.items():
        for index, doc in enumerate(docs):
            for symbol, count in enumerate(COUNTS[block]):
                share = count // len(docs) + (count % len(docs) if index == 0 else 0)
                rows.extend({'variant': 'toy', 'doc_id': doc, 'symbol_id': symbol,
                             'available_past': position, 'eligible': position >= 4}
                            for position in range(share))
    frame = pd.DataFrame(rows)
    return pd.concat([frame, frame.assign(variant='other', symbol_id=0)], ignore_index=True)


def test_jsd_is_symmetric_zero_on_the_diagonal_and_bounded_by_one_bit():
    """§8.3: 0 log 0 = 0, symmetry, [0,1] bits, and the contributions sum to the total."""
    disjoint = (np.array([1.0, 0.0, 0.0]), np.array([0.0, 0.5, 0.5]))
    assert r1.jsd(*disjoint) == 1.0  # the bound is attained, and no zero produces a nan
    assert r1.jsd(*reversed(disjoint)) == r1.jsd(*disjoint)

    blocks = distributions()
    for left, right in itertools.combinations(blocks, 2):
        value = r1.jsd(blocks[left], blocks[right])
        assert 0.0 <= value <= 1.0
        assert value == pytest.approx(r1.jsd(blocks[right], blocks[left]), abs=1e-15)
        parts = r1.contributions(blocks[left], blocks[right])
        assert len(parts) == M and (parts >= 0.0).all()
        assert math.fsum(parts) == pytest.approx(value, abs=1e-15)

    for block, distribution in blocks.items():
        assert r1.jsd(distribution, distribution) == 0.0
        assert r1.contributions(distribution, distribution).tolist() == [0.0] * M
    assert r1.jsd(np.array([0.5, 0.5]), np.array([0.5, 0.5])) == 0.0

    with pytest.raises(ValueError, match='length|sum'):
        r1.jsd(np.array([0.5, 0.5]), np.array([0.5, 0.25, 0.25]))


def test_smoothed_counts_of_the_seven_blocks_and_their_matrix():
    """§8.3: r_b = (n+0.5)/(N+0.5m) on every retained token, initial ones included."""
    counts = r1.block_counts(coordinates(), BLOCKS, variant='toy', m=M)
    assert set(counts) == set(BLOCKS)
    for block, expected in COUNTS.items():
        assert counts[block].tolist() == expected  # both documents of HEX_A, all positions

    frequencies = r1.smoothed(counts['HEX_A'])
    total = sum(COUNTS['HEX_A'])
    assert frequencies.tolist() == [(n + 0.5) / (total + 0.5 * M) for n in COUNTS['HEX_A']]
    assert frequencies.sum() == pytest.approx(1.0, abs=1e-15)
    assert frequencies[4] > 0.0  # a symbol never seen in the block keeps positive mass

    blocks = {block: r1.smoothed(value) for block, value in counts.items()}
    matrix = r1.matrix(blocks)
    assert matrix.shape == (7, 7)
    assert np.allclose(matrix.to_numpy(), matrix.to_numpy().T, atol=1e-15)
    assert np.diag(matrix.to_numpy()).tolist() == [0.0] * 7
    assert ((matrix.to_numpy() >= 0.0) & (matrix.to_numpy() <= 1.0)).all()
    assert matrix.loc['P_A', 'P_E'] == 0.0  # identical counts, identical distributions

    pairs = r1.pairs(blocks)
    assert len(pairs) == 21 and pairs['jsd'].between(0.0, 1.0).all()
    assert list(pairs.columns) == ['block_a', 'block_b', 'jsd']
    for row in pairs.itertuples(index=False):
        assert row.block_a < row.block_b
        assert matrix.loc[row.block_a, row.block_b] == pytest.approx(row.jsd, abs=1e-15)

    with pytest.raises(ValueError, match='absent|empty'):
        r1.block_counts(coordinates(), BLOCKS | {'GHOST': ['nowhere']}, variant='toy', m=M)


def test_matrix_orders_blocks_alphabetically_like_pairs_regardless_of_insertion_order():
    """§8.3: the 7x7 matrix and the 21-pair list must agree on block order by construction."""
    blocks = distributions()
    insertion_order = list(reversed(blocks))
    assert insertion_order != sorted(blocks)  # the fixture is deliberately not alphabetical

    reordered = {name: blocks[name] for name in insertion_order}
    matrix = r1.matrix(reordered)
    assert list(matrix.index) == sorted(blocks)
    assert list(matrix.columns) == sorted(blocks)


def test_group_centroids_are_not_the_mean_of_the_pairwise_divergences():
    """§8.3: uniform block means first, then one JSD of the two centroids."""
    blocks = distributions()
    members = {group: [block for block, label in GROUPS.items() if label == group]
               for group in ('HEX', 'PROSE_ALL')}
    centroids = {group: r1.centroid([blocks[block] for block in names])
                 for group, names in members.items()}

    assert np.allclose(centroids['HEX'], np.mean([blocks['HEX_A'], blocks['HEX_B']], axis=0))
    for centroid in centroids.values():
        assert centroid.sum() == pytest.approx(1.0, abs=1e-15)

    between = r1.jsd(centroids['HEX'], centroids['PROSE_ALL'])
    crossing = [r1.jsd(blocks[left], blocks[right])
                for left in members['HEX'] for right in members['PROSE_ALL']]
    assert 0.0 < between <= 1.0
    assert abs(between - float(np.mean(crossing))) > 1e-4  # a mean of pair JSDs is a different number
    assert math.fsum(r1.contributions(centroids['HEX'], centroids['PROSE_ALL'])) \
        == pytest.approx(between, abs=1e-15)

    single = r1.centroid([blocks['HEX_A']])
    assert single.tolist() == blocks['HEX_A'].tolist()
    with pytest.raises(ValueError, match='centroid'):
        r1.centroid([])
