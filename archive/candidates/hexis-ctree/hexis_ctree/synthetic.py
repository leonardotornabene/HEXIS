"""Synthetic sources with known ground truth, for validation only.

These generators exist so that every estimator in the package can be checked
against analytically known entropy rates BEFORE touching corpus data
(Phase 0 has not started; no claim in this package concerns the Perseus
treebanks). All randomness is seeded and reproducible.
"""

from __future__ import annotations

import math
import random
from typing import List, Sequence

Document = List[List[str]]

_LOG2 = math.log(2.0)


def default_symbols(d: int) -> List[str]:
    """Deterministic symbol names: 'a', 'b', ... (d <= 26 for readability)."""
    if not (2 <= d <= 26):
        raise ValueError("d must be between 2 and 26 for the default symbols.")
    return [chr(ord("a") + i) for i in range(d)]


# ---------------------------------------------------------------------- #
# IID uniform source: h = log2(d)
# ---------------------------------------------------------------------- #
def iid_uniform_document(
    d: int, n_sentences: int, sentence_length: int, seed: int
) -> Document:
    symbols = default_symbols(d)
    rng = random.Random(seed)
    return [
        [rng.choice(symbols) for _ in range(sentence_length)]
        for _ in range(n_sentences)
    ]


# ---------------------------------------------------------------------- #
# First-order Markov source: h = -sum_i pi_i sum_j P_ij log2 P_ij
# ---------------------------------------------------------------------- #
def stationary_distribution(P: Sequence[Sequence[float]], n_iter: int = 10_000) -> List[float]:
    d = len(P)
    for row in P:
        if len(row) != d or abs(sum(row) - 1.0) > 1e-9:
            raise ValueError("P must be a square row-stochastic matrix.")
    pi = [1.0 / d] * d
    for _ in range(n_iter):
        nxt = [sum(pi[i] * P[i][j] for i in range(d)) for j in range(d)]
        if max(abs(a - b) for a, b in zip(pi, nxt)) < 1e-14:
            pi = nxt
            break
        pi = nxt
    return pi


def markov_entropy_rate_bits(P: Sequence[Sequence[float]]) -> float:
    pi = stationary_distribution(P)
    h = 0.0
    for i, row in enumerate(P):
        for p in row:
            if p > 0.0:
                h -= pi[i] * p * math.log(p) / _LOG2
    return h


def markov_document(
    P: Sequence[Sequence[float]],
    n_sentences: int,
    sentence_length: int,
    seed: int,
) -> Document:
    """Sentences drawn from the chain; each sentence starts from the
    stationary distribution (the hard reset makes sentences independent)."""
    d = len(P)
    symbols = default_symbols(d)
    pi = stationary_distribution(P)
    rng = random.Random(seed)
    doc: Document = []
    for _ in range(n_sentences):
        sentence: List[str] = []
        state = rng.choices(range(d), weights=pi, k=1)[0]
        sentence.append(symbols[state])
        for _ in range(sentence_length - 1):
            state = rng.choices(range(d), weights=P[state], k=1)[0]
            sentence.append(symbols[state])
        doc.append(sentence)
    return doc


# ---------------------------------------------------------------------- #
# Noisy periodic template: a toy analogue of a strong formal constraint.
# ---------------------------------------------------------------------- #
def periodic_template_document(
    template: Sequence[str],
    d: int,
    n_sentences: int,
    sentence_length: int,
    noise: float,
    seed: int,
) -> Document:
    """Cyclic template with substitution noise and a random initial phase
    per sentence.

    With probability (1 - noise) the template symbol is emitted, otherwise a
    uniformly random *other* symbol from the d-symbol alphabet. The random
    phase forces the model to infer the position in the cycle from the
    context alone (the sentence reset gives no positional cue), which is the
    behaviour the S1/P2 statistics are designed to detect.
    """
    if not (0.0 <= noise < 1.0):
        raise ValueError("noise must be in [0, 1).")
    symbols = default_symbols(d)
    if any(t not in symbols for t in template):
        raise ValueError("template symbols must belong to the d-symbol alphabet.")
    rng = random.Random(seed)
    L = len(template)
    doc: Document = []
    for _ in range(n_sentences):
        phase = rng.randrange(L)
        sentence: List[str] = []
        for k in range(sentence_length):
            intended = template[(phase + k) % L]
            if rng.random() < noise:
                others = [s for s in symbols if s != intended]
                sentence.append(rng.choice(others))
            else:
                sentence.append(intended)
        doc.append(sentence)
    return doc


def template_phase_known_entropy_rate_bits(d: int, noise: float) -> float:
    """Entropy rate of the template source GIVEN the phase (lower bound on h).

    h = -(1-e) log2(1-e) - e log2(e / (d-1)),  e = noise.
    The phase-inference cost at the start of each sentence is not included,
    so the online estimate at finite N must exceed this value.
    """
    if noise == 0.0:
        return 0.0
    e = noise
    return -(1 - e) * math.log(1 - e) / _LOG2 - e * math.log(e / (d - 1)) / _LOG2
