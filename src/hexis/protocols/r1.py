"""R1: JSD of the complete retained counts (piano §8.3, §11.1).

The population is every retained original token of the seven primary blocks,
initial slots included — not the leave-one-block-out training roots and not the
eligible targets. So R1 needs no CTW, no sample and no seed.

It is descriptive: a divergence, not a metric distance. It neither corrects nor
validates Q, and it carries no clustering, no test, no target-weighted centroid.
"""

import itertools
import math

import numpy as np
import pandas as pd

SMOOTHING = 0.5  # §8.3: r_b(x) = (n_b(x) + 0.5) / (N_b + 0.5 m)
NORMALIZATION_ATOL = 1e-9


def block_counts(coordinates, blocks, *, variant, m) -> dict:
    """Retained-token counts per block, from the coordinates of one variant (§8.3)."""
    frame = coordinates[coordinates['variant'].eq(variant)]
    counts = {}
    for block, docs in blocks.items():
        symbols = frame.loc[frame['doc_id'].isin(list(docs)), 'symbol_id'].to_numpy(dtype='int64')
        if not symbols.size:
            raise ValueError(f'block {block!r}: {sorted(docs)} absent from the retained tokens '
                             f'of variant {variant!r}')
        if symbols.min() < 0 or symbols.max() >= m:
            raise ValueError(f'block {block!r}: symbol ids outside [0, {m}) in variant {variant!r}')
        counts[block] = np.bincount(symbols, minlength=m)
    return counts


def smoothed(counts, *, a=SMOOTHING) -> np.ndarray:
    """§8.3: the smoothed block frequencies; the raw counts stay with the caller."""
    values = np.asarray(counts, dtype='float64')
    if values.ndim != 1 or (values < 0).any():
        raise ValueError('smoothed: a one-dimensional vector of non-negative counts is required')
    return (values + a) / (values.sum() + a * values.size)


def contributions(p, q) -> np.ndarray:
    """The per-symbol contributions of JSD in bits, with 0 log 0 = 0 (§8.3)."""
    left, right = _distribution(p, 'p'), _distribution(q, 'q')
    if left.size != right.size:
        raise ValueError(f'p and q have lengths {left.size} and {right.size}: JSD compares two '
                         'distributions over the same alphabet')
    mean = 0.5 * (left + right)
    return 0.5 * (_divergence(left, mean) + _divergence(right, mean))


def jsd(p, q) -> float:
    """§8.3: the symmetric divergence in bits, the sum of its own contributions."""
    return math.fsum(contributions(p, q))


def matrix(distributions) -> pd.DataFrame:
    """The block matrix of one variant: symmetric, zero on the diagonal (§8.3)."""
    names = list(distributions)
    values = np.zeros((len(names), len(names)), dtype='float64')
    for left, right in itertools.combinations(range(len(names)), 2):
        values[left, right] = values[right, left] = jsd(distributions[names[left]],
                                                        distributions[names[right]])
    return pd.DataFrame(values, index=names, columns=names)


def pairs(distributions) -> pd.DataFrame:
    """The C(n,2) distinct pairs of one variant: 21 rows for the seven blocks (§8.3)."""
    names = sorted(distributions)
    return pd.DataFrame([{'block_a': left, 'block_b': right,
                          'jsd': jsd(distributions[left], distributions[right])}
                         for left, right in itertools.combinations(names, 2)],
                        columns=['block_a', 'block_b', 'jsd'])


def centroid(distributions) -> np.ndarray:
    """§8.3: the uniform mean of a group's block distributions — averaged before the JSD."""
    members = [_distribution(member, 'centroid member') for member in distributions]
    if not members:
        raise ValueError('centroid: no block distribution to average')
    return np.mean(members, axis=0)


def _distribution(values, name) -> np.ndarray:
    array = np.asarray(values, dtype='float64')
    if array.ndim != 1 or (array < 0).any() or not np.isfinite(array).all():
        raise ValueError(f'{name}: a one-dimensional finite non-negative vector is required')
    if abs(array.sum() - 1.0) > NORMALIZATION_ATOL:
        raise ValueError(f'{name}: does not sum to 1 ({array.sum()!r}); JSD takes distributions, '
                         'not counts')
    return array


def _divergence(p, u) -> np.ndarray:
    """p log2(p/u) per symbol, reading 0 log 0 as 0; u >= p/2 > 0 wherever p > 0."""
    out = np.zeros_like(p)
    seen = p > 0.0
    out[seen] = p[seen] * np.log2(p[seen] / u[seen])
    return out
