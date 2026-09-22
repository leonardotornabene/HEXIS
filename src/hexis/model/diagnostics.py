"""Mixture masses, L_resolved and the §9.3 evaluation sums (piano §9.1–§9.3).

Nothing here selects a depth. L_resolved describes the observed lengths the
mixture puts weight on, conditioned on the observed mass R — and R is always the
direct sum of those masses, never `1 - unseen_mass`. A history whose mass is
entirely unseen has no L_resolved: it is null with a reason, not a zero.

The totals are sums and counts only. Means arrive at the end, through `means`,
each with its own declared denominator (§9.3).
"""

import math

NO_RESOLVED_MASS = 'no_resolved_mass'
EMPTY_BUCKET = 'empty_bucket'
MASS_PREFIX = 'sum_observed_mass_by_length_'


def resolved(mixture) -> dict:
    """§9.2 for one history: observed mass per lexical length, R and L_resolved."""
    mass = {}
    for length, weight in mixture.weights:  # a BOS leaf repeats its parent's length
        mass[length] = mass.get(length, 0.0) + weight
    total = math.fsum(mass.values())
    if total <= 0.0:
        return {'mass_by_length': mass, 'unseen_mass': mixture.unseen_mass,
                'unseen_branch_encountered': mixture.unseen_branch_encountered,
                'resolved_mean': None, 'reason': NO_RESOLVED_MASS}
    return {'mass_by_length': mass, 'unseen_mass': mixture.unseen_mass,
            'unseen_branch_encountered': mixture.unseen_branch_encountered,
            'resolved_mean': math.fsum(length * weight for length, weight in mass.items()) / total,
            'reason': None}


class EvaluationTotals:
    """§9.3 running record of one (population, arm, band): the sums, never a mean."""

    __slots__ = ('n', 'sum_resolved_valid', 'resolved_valid_count', 'resolved_null_count',
                 'sum_unseen_mass', 'root_unseen_target_count', 'unseen_branch_encounters', 'mass')

    def __init__(self, depth: int):
        self.n = 0
        self.sum_resolved_valid = 0.0
        self.resolved_valid_count = 0
        self.resolved_null_count = 0
        self.sum_unseen_mass = 0.0
        self.root_unseen_target_count = 0
        self.unseen_branch_encounters = 0
        self.mass = [0.0] * (depth + 1)

    def add(self, record, *, root_unseen: bool):
        """One scored target: its §9.2 record and whether the root had ever seen it."""
        self.n += 1
        if record['resolved_mean'] is None:
            self.resolved_null_count += 1
        else:
            self.sum_resolved_valid += record['resolved_mean']
            self.resolved_valid_count += 1
        self.sum_unseen_mass += record['unseen_mass']
        self.root_unseen_target_count += int(root_unseen)
        self.unseen_branch_encounters += int(record['unseen_branch_encountered'])
        for length, weight in record['mass_by_length'].items():
            self.mass[length] += weight

    def row(self) -> dict:
        """The report-contract fields of one `per_arm_diagnostics` row."""
        return {'n': self.n, 'sum_resolved_valid': self.sum_resolved_valid,
                'resolved_valid_count': self.resolved_valid_count,
                f'resolved_null_count_by_reason_{NO_RESOLVED_MASS}': self.resolved_null_count,
                'sum_unseen_mass': self.sum_unseen_mass,
                'root_unseen_target_count': self.root_unseen_target_count,
                'implicit_unseen_branch_encounter_count': self.unseen_branch_encounters,
                **{f'{MASS_PREFIX}{length}': weight for length, weight in enumerate(self.mass)}}


def means(totals) -> dict:
    """§9.3: L over the valid count, unseen and per-length mass over all targets.

    Never the ratio of aggregated mass moments — that is a different quantity.
    """
    n = int(totals['n'])
    if n == 0:
        return {'L': None, 'unseen': None, 'mass': None, 'reason': EMPTY_BUCKET}
    valid = int(totals['resolved_valid_count'])
    lengths = sorted(int(key[len(MASS_PREFIX):]) for key in totals.keys()
                     if str(key).startswith(MASS_PREFIX))
    return {'L': totals['sum_resolved_valid'] / valid if valid else None,
            'unseen': totals['sum_unseen_mass'] / n,
            'mass': [totals[f'{MASS_PREFIX}{length}'] / n for length in lengths],
            'reason': None if valid else NO_RESOLVED_MASS}
