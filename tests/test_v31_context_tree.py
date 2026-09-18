"""V2 CTW core: independent enumeration, frozen mixture, numerics and the §12.1 battery.

The enumeration helpers below are a second, deliberately naive implementation of
the piano §6.1–§6.4 contract (explicit sum over admissible trees, counts matched
by scanning the streams) used as the oracle for T10; they share no code with
``hexis.model.context_tree``.
"""
import ast
import itertools
import json
import math
from pathlib import Path

import numpy as np
import pytest

from hexis.contracts import load_contracts
from hexis.model.context_tree import BOS, CTW, CTWParams
from hexis.pipeline import run_tree_validation as validation

pytestmark = pytest.mark.v31

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL = ROOT/'docs/contracts/hexis-3.1/fixtures/ctw_validation/verify_synthetic.py'
# §12.1 table — the text governs semantics (§0), so `iid` uses 0.02, not the 0.03
# hardcoded in the historical script. Recomputed here, independently of the stage.
PLAN_TOLERANCE = {'iid': 0.02, 'cycle': 0.02, 'order1': 0.03, 'lag2': 0.03, 'variable': 0.03}


# --- independent oracle (T10) -------------------------------------------------

def visits(streams, context, m):
    """n_c(x) by direct scan of every training target (§6.2 partition)."""
    bos = bool(context) and context[-1] == BOS
    core = context[:-1] if bos else context
    counts = {}
    for stream in streams:
        for i, target in enumerate(stream):
            if (i != len(core)) if bos else (i < len(core)):
                continue
            if all(stream[i-1-j] == core[j] for j in range(len(core))):
                counts[target] = counts.get(target, 0)+1
    return counts


def log_evidence(counts, m, a):
    total = sum(counts.values())
    return (math.lgamma(m*a) - math.lgamma(total+m*a)
            + sum(math.lgamma(n+a) - math.lgamma(a) for n in counts.values()))


def admissible_trees(context, m, depth, log_rho, log_split):
    """Every admissible tree below `context` as (leaves, log prior)."""
    if len(context) == depth or (context and context[-1] == BOS):
        return [((context,), 0.0)]
    trees = [((context,), log_rho)]
    branches = [admissible_trees(context+(sym,), m, depth, log_rho, log_split)
                for sym in (*range(m), BOS)]
    for combination in itertools.product(*branches):
        trees.append((tuple(leaf for leaves, _ in combination for leaf in leaves),
                      log_split + sum(prior for _, prior in combination)))
    return trees


class Oracle:
    """Explicit mixture over admissible trees; no recursion on weights."""

    def __init__(self, streams, m, depth, a, rho):
        self.streams, self.m, self.a = streams, m, a
        self.trees = admissible_trees((), m, depth, math.log(rho), math.log1p(-rho))
        self.evidence = {}
        self.log_posterior = [prior + sum(self._evidence(leaf) for leaf in leaves)
                              for leaves, prior in self.trees]
        top = max(self.log_posterior)
        self.log_w = top + math.log(sum(math.exp(value-top) for value in self.log_posterior))

    def _evidence(self, context):
        if context not in self.evidence:
            self.evidence[context] = log_evidence(visits(self.streams, context, self.m), self.m, self.a)
        return self.evidence[context]

    def weight(self, index):
        return math.exp(self.log_posterior[index] - self.log_w)

    def root_stop(self):
        return sum(self.weight(index) for index, (leaves, _) in enumerate(self.trees) if leaves == ((),))

    def predict(self, history):
        q = np.zeros(self.m)
        for index, (leaves, _) in enumerate(self.trees):
            context = ()
            while context not in leaves:
                depth = len(context)
                context += (history[-1-depth],) if depth < len(history) else (BOS,)
            counts = visits(self.streams, context, self.m)
            total = sum(counts.values())
            q += self.weight(index)*np.array([(counts.get(x, 0)+self.a)/(total+self.m*self.a)
                                              for x in range(self.m)])
        return q


def fitted(streams, m, depth, a=0.5, rho=0.5):
    return CTW(CTWParams.from_rho(m=m, depth=depth, a=a, rho=rho)).fit(streams)


@pytest.mark.parametrize('m,depth,rho', [(2, 2, 0.5), (2, 3, 0.25), (3, 2, 0.5)])
def test_independent_enumeration_matches_evidence_and_prediction(m, depth, rho):
    streams = [[x % m for x in (0, 1, 1, 2, 0, 0, 1)], [(x*2) % m for x in (1, 1, 0, 2, 2)], [0]]
    model, oracle = fitted(streams, m, depth, rho=rho), Oracle(streams, m, depth, 0.5, rho)
    assert abs(model.log_evidence - oracle.log_w) <= 1e-10
    assert abs(model.diagnostics()['root_stop'] - oracle.root_stop()) <= 1e-12
    for history in [[], [0], [1, 0], [0, 0, 1, 1], [m-1]*(depth+2)]:
        assert max(abs(model.predict_proba(history) - oracle.predict(history))) <= 1e-12


def test_counts_partition_over_children_with_terminal_bos():
    streams = [[0, 1, 1, 0, 1], [1, 0]]
    model = fitted(streams, m=2, depth=3)
    assert model.inspect(())['total'] == 7
    for context in [(), (0,), (1,), (1, 1), (0, BOS)]:
        node = model.inspect(context)
        assert node['counts'] == visits(streams, context, 2)
    for context in [(), (0,), (1, 1)]:
        children = [model.inspect(context+(sym,)) for sym in (0, 1, BOS)]
        parts = [child['counts'] for child in children if child is not None]
        assert model.inspect(context)['counts'] == {
            symbol: total for symbol in (0, 1)
            if (total := sum(part.get(symbol, 0) for part in parts))}
    assert model.inspect((0, BOS))['forced'] and model.inspect((0, BOS, 0)) is None
    assert model.inspect((1, 1, 0))['forced']


@pytest.mark.parametrize('count,bucket', [(1, '1'), (2, '2to4'), (4, '2to4'),
                                        (5, '5to9'), (9, '5to9'), (10, '10plus')])
def test_support_histogram_counts_observations_including_bos(count, bucket):
    trained = fitted([[0]] * count, m=2, depth=2)
    expected = dict.fromkeys(('1', '2to4', '5to9', '10plus'), 0)
    expected[bucket] = 1  # root and terminal BOS each have count observations
    assert trained.diagnostics()['support_histogram_1_2to4_5to9_10plus_by_depth'] == [expected, expected]
    empty = fitted([], m=2, depth=2).diagnostics()
    assert empty['support_histogram_1_2to4_5to9_10plus_by_depth'] == [dict.fromkeys(expected, 0)]


# --- T11: normalization, support, empty training, D=0, strict input -----------

@pytest.mark.parametrize('m', [100, 105, 11])
def test_normalization_rare_and_unseen_support_across_alphabets(m):
    rng = np.random.default_rng(7)
    streams = [rng.integers(0, m-3, size=size).tolist() for size in (200, 40, 1)]
    model = fitted(streams, m=m, depth=8)
    seen = {symbol for stream in streams for symbol in stream}
    rare = min(seen, key=lambda symbol: sum(stream.count(symbol) for stream in streams))
    for history in [[], [0], streams[0][:12], [m-1, m-2, m-3]*4]:
        q = model.predict_proba(history)
        assert q.shape == (m,) and q.dtype == np.float64
        assert abs(q.sum() - 1.0) <= 1e-12
        assert q.min() > 0.0
        assert q[m-1] > 0.0 and q[rare] > 0.0
    assert set(range(m-3, m)).isdisjoint(seen)
    unseen_context = model.mixture([m-1, m-2, m-3]*4)
    assert unseen_context.unseen_mass > 0.0
    assert abs(sum(weight for _, weight in unseen_context.weights) + unseen_context.unseen_mass - 1.0) <= 1e-12
    assert abs(model.root_distribution().sum() - 1.0) <= 1e-12


@pytest.mark.parametrize('streams', [[], [[]], [[], []]])
def test_empty_training_is_a_valid_core_case(streams):
    model = fitted(streams, m=11, depth=8)
    uniform = np.full(11, 1/11)
    assert max(abs(model.predict_proba([3, 4]) - uniform)) <= 1e-12
    assert max(abs(model.root_distribution() - uniform)) <= 1e-12
    mixture = model.mixture([3, 4])
    assert mixture.weights == () and mixture.unseen_mass == 1.0
    assert model.diagnostics()['nodes'] == 1


def test_zero_depth_is_a_forced_root_leaf():
    model = fitted([[0, 1, 1, 2]], m=3, depth=0)
    diagnostics = model.diagnostics()
    assert diagnostics['root_stop'] == 1.0
    assert diagnostics['delta_root'] is None
    assert diagnostics['delta_root_reason'] == 'forced_leaf'
    assert model.mixture([0, 1]).weights == ((0, 1.0),)
    assert model.mixture([0, 1]).unseen_mass == 0.0
    assert max(abs(model.predict_proba([0, 1]) - model.root_distribution())) <= 1e-12
    assert model.inspect(())['forced'] and model.inspect((0,)) is None


@pytest.mark.parametrize('case,token', [
    (lambda: CTWParams.from_rho(m=1, depth=2, a=0.5, rho=0.5), 'alphabet size'),
    (lambda: CTWParams.from_rho(m=2.0, depth=2, a=0.5, rho=0.5), 'alphabet size'),
    (lambda: CTWParams.from_rho(m=True, depth=2, a=0.5, rho=0.5), 'alphabet size'),
    (lambda: CTWParams.from_rho(m=4, depth=-1, a=0.5, rho=0.5), 'depth='),
    (lambda: CTWParams.from_rho(m=4, depth=2.0, a=0.5, rho=0.5), 'depth='),
    (lambda: CTWParams.from_rho(m=4, depth=2, a=0.0, rho=0.5), 'Dirichlet'),
    (lambda: CTWParams.from_rho(m=4, depth=2, a=-0.5, rho=0.5), 'Dirichlet'),
    (lambda: CTWParams.from_rho(m=4, depth=2, a=float('inf'), rho=0.5), 'Dirichlet'),
    (lambda: CTWParams.from_rho(m=4, depth=2, a=True, rho=0.5), 'Dirichlet'),
    (lambda: CTWParams.from_rho(m=4, depth=2, a=0.5, rho=0.0), 'stop prior'),
    (lambda: CTWParams.from_rho(m=4, depth=2, a=0.5, rho=1.0), 'stop prior'),
    (lambda: CTWParams.from_rho(m=4, depth=2, a=0.5, rho=float('nan')), 'stop prior'),
    (lambda: CTWParams.from_log_split_prior(m=4, depth=2, a=0.5, log_one_minus_rho=0.0), 'split log-prior'),
    (lambda: CTWParams.from_log_split_prior(m=4, depth=2, a=0.5, log_one_minus_rho=1.0), 'split log-prior'),
    (lambda: fitted([[0, 4]], m=4, depth=2), 'stream 0 position 1'),
    (lambda: fitted([[0], [1, -1]], m=4, depth=2), 'stream 1 position 1'),
    (lambda: fitted([[0, 1.0]], m=4, depth=2), 'stream 0 position 1'),
    (lambda: fitted([[0, True]], m=4, depth=2), 'stream 0 position 1'),
    (lambda: fitted([[0, 1]], m=4, depth=2).predict_proba([2, 9]),
     'history (within the last 2 symbols) position 1'),
    # tail-only validation is intentional (kept unchanged); the leading 5s sit outside the
    # last-2-symbols window and are never checked, but the reported position of the symbol
    # that IS checked must be absolute in the full history (3), not relative to the tail (1).
    (lambda: fitted([[0, 1]], m=4, depth=2).predict_proba([5, 5, 2, 9]),
     'history (within the last 2 symbols) position 3'),
    (lambda: fitted([[0, 1]], m=4, depth=2).evaluate([[0, 1]], min_available_past=-1), 'min_available_past'),
    (lambda: CTW(CTWParams.from_rho(m=4, depth=2, a=0.5, rho=0.5)).predict_proba([0]), 'fit'),
    (lambda: fitted([[0, 1]], m=4, depth=2).fit([[0]]), 'frozen'),
])
def test_core_rejects_invalid_parameters_and_symbols(case, token):
    with pytest.raises(ValueError) as error:
        case()
    assert token in str(error.value)


# --- T12: prequential/integrated identity and stream order --------------------

@pytest.mark.parametrize('depth', [0, 2, 4])
def test_prequential_identity_uses_pre_update_counts(depth):
    streams = [[0, 1, 1, 0, 2, 2, 1, 0], [2, 0, 0, 1]]
    prequential = 0.0
    for index, stream in enumerate(streams):
        for position, target in enumerate(stream):
            seen = [*streams[:index], stream[:position]]
            prequential += math.log(fitted(seen, m=3, depth=depth).predict_proba(stream[:position])[target])
    assert abs(prequential - fitted(streams, m=3, depth=depth).log_evidence) <= 1e-10


def test_stream_order_does_not_change_the_frozen_model():
    first, second, third = [0, 1, 1, 0, 2], [2, 2, 0], [1]
    forward = fitted([first, second, third], m=3, depth=3)
    backward = fitted([third, second, first], m=3, depth=3)
    assert forward.fingerprint() == backward.fingerprint()
    assert forward.diagnostics() == backward.diagnostics()
    assert abs(forward.log_evidence - backward.log_evidence) == 0.0
    assert forward.evaluate([[0, 1, 2, 0]], min_available_past=0).ce == \
        backward.evaluate([[0, 1, 2, 0]], min_available_past=0).ce


# --- T13: the frozen model is unchanged by evaluation -------------------------

def test_evaluation_never_mutates_the_frozen_model():
    rng = np.random.default_rng(3)
    train = [rng.integers(0, 4, size=size).tolist() for size in (120, 40)]
    test = [rng.integers(0, 4, size=60).tolist(), [3, 3, 3, 3, 3, 3]]
    model = fitted(train, m=4, depth=4)
    contexts = [(), (0,), (1, 2), (0, BOS), (3, 3, 3, 3)]
    before = (model.fingerprint(), model.diagnostics(), [model.inspect(c) for c in contexts],
              model.log_evidence, model.root_distribution().tolist())
    result = model.evaluate(test, min_available_past=4)
    model.predict_proba([1, 2, 3])
    model.mixture([1, 2, 3])
    after = (model.fingerprint(), model.diagnostics(), [model.inspect(c) for c in contexts],
             model.log_evidence, model.root_distribution().tolist())
    assert before == after
    assert result.n == 56+2 and math.isfinite(result.ce)
    # the scalar path of `evaluate` and the vector of `predict_proba` read one mixture
    single = model.evaluate([[3, 3, 3, 3, 3, 2]], min_available_past=5)
    assert single.n == 1
    assert abs(single.ce + math.log2(model.predict_proba([3, 3, 3, 3, 3])[2])) <= 1e-12
    probabilities = model.predict_proba([1, 2, 3])
    probabilities[0] = 99.0
    assert model.predict_proba([1, 2, 3])[0] != 99.0
    assert model.inspect((0,))['counts'] is not model.inspect((0,))['counts']


# --- T14: log priors, two weights, saturation vs forced leaves ----------------

def stop_and_split(delta):
    """§6.5 both weights from δ, overflow-safe and independent of the module."""
    return -np.logaddexp(0.0, -delta), -np.logaddexp(0.0, delta)


def test_extreme_log_prior_keeps_both_weights():
    m = 106
    log_split = -(m-1)*math.log(2)
    params = CTWParams.from_log_split_prior(m=m, depth=3, a=0.5, log_one_minus_rho=log_split)
    assert math.log(1-2**-(m-1)) == 0.0  # the float route the plan forbids loses the mass
    assert params.log_rho < 0.0
    assert abs(params.log_rho/-(2.0**-(m-1)) - 1.0) <= 1e-9
    assert params.log_one_minus_rho == log_split
    model = CTW(params).fit([[0, 1, 2, 3]*40])
    root = model.inspect(())
    assert root['log_stop'] < 0.0 and root['log_split'] < 0.0
    assert math.isfinite(root['log_stop']) and math.isfinite(root['log_split'])
    assert abs(math.exp(root['log_stop']) + math.exp(root['log_split']) - 1.0) <= 1e-12
    expected_stop, expected_split = stop_and_split(root['delta'])
    assert abs(root['log_stop'] - expected_stop) <= 1e-12
    assert abs(root['log_split'] - expected_split) <= 1e-12


def test_stop_saturation_keeps_a_finite_split_weight():
    """§6.5: past ~37 nats the stop weight rounds to 1 and `1 - stop` loses the other weight."""
    rng = np.random.default_rng(11)
    model = fitted([rng.integers(0, 11, size=2000).tolist()], m=11, depth=4)
    root = model.inspect(())
    assert root['delta'] > 37.0
    assert math.exp(root['log_stop']) == 1.0 and 1.0 - math.exp(root['log_stop']) == 0.0
    assert math.isfinite(root['log_split']) and root['log_split'] < -37.0
    assert abs(root['log_split'] - stop_and_split(root['delta'])[1]) <= 1e-12
    mixture = model.mixture([1, 2, 3, 4])
    assert mixture.weights[0][1] == 1.0
    assert abs(sum(weight for _, weight in mixture.weights) + mixture.unseen_mass - 1.0) <= 1e-12


def test_saturation_is_distinct_from_a_forced_leaf():
    model = fitted([[0, 1, 2, 3]*400], m=4, depth=3)
    root = model.inspect(())
    assert not root['forced']
    assert root['log_stop'] < -745.0 and math.isfinite(root['log_stop'])
    assert math.exp(root['log_stop']) == 0.0  # numerical saturation, not a discrete choice
    assert -1e-300 < root['log_split'] <= 0.0
    leaf = model.inspect((3, 2, 1))
    assert leaf['forced'] and leaf['log_split'] == -math.inf and leaf['log_stop'] == 0.0
    assert leaf['delta'] is None
    assert model.diagnostics()['delta_root'] == root['delta']
    assert model.diagnostics()['delta_root_reason'] is None
    mixture = model.mixture([1, 2, 3])
    assert mixture.weights[0][1] == 0.0 and mixture.unseen_mass == 0.0
    assert abs(sum(weight for _, weight in mixture.weights) - 1.0) <= 1e-12


# --- T15/T16: the frozen §12.1 battery ---------------------------------------

def test_generator_fixture_matches_the_historical_script():
    def functions(path):
        return {node.name: node for node in ast.parse(path.read_text()).body
                if isinstance(node, ast.FunctionDef)}

    historical, ours = functions(HISTORICAL), functions(Path(validation.__file__))
    assert ast.dump(ours['generate']) == ast.dump(historical['generate'])
    assert validation.generate('lag2', 12, 3, 2)[0] == [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1]
    assert validation.generate('lag2', 12, 3, 2)[1] == 0.4689955935892812


def test_analytic_pass_pins_the_corrected_iid_threshold():
    """§12.1 fixes |CE-2| <= 0.02 for iid; the historical script's 0.03 must not silently
    come back (a 0.025 deviation passes at 0.03 but must fail at the plan's 0.02)."""
    assert validation.analytic_pass('iid', 4, 2.025, 2.0) is False
    assert validation.analytic_pass('iid', 4, 2.019, 2.0) is True


@pytest.fixture(scope='module')
def battery(tmp_path_factory):
    path = tmp_path_factory.mktemp('battery')/'synthetic_results.json'
    code = validation.main(['--config', str(ROOT/'config/default.yaml'), '--out', str(path)])
    return code, json.loads(path.read_text())


def plan_pass(row):
    """§12.1 table, recomputed independently of the stage."""
    if row['kind'] == 'cycle':
        return row['ce'] < 0.02
    return abs(row['ce'] - row['target']) <= PLAN_TOLERANCE[row['kind']]


def test_small_synthetic_battery_meets_plan_thresholds(battery):
    code, results = battery
    design = load_contracts()['design']['validation']
    small = [row for row in results['rows'] if row['m'] < 106]
    assert code == 0
    assert len(small) == design['small_synthetic_cases'] == 25
    assert sorted({(row['kind'], row['m']) for row in small}) == \
        [('cycle', 3), ('iid', 4), ('lag2', 2), ('order1', 2), ('variable', 2)]
    assert sorted({row['seed'] for row in small}) == design['synthetic_training_seeds']
    assert [row for row in small if not plan_pass(row)] == []
    assert all(row['analytic_pass'] is True for row in small)
    assert all(row['n'] == design['synthetic_n_test']-4 for row in small)
    assert all(row['normalization_max_error'] <= 1e-12 for row in small)
    # §12.1: the recovered lag-2 rate against the ≈1 bit of the historical local selector.
    lag2 = [row for row in small if row['kind'] == 'lag2']
    assert all(abs(row['ce']-0.468996) <= 0.03 and row['root_ce'] > 0.99 for row in lag2)


def test_validation_stage_exits_non_zero_when_a_threshold_fails(monkeypatch, tmp_path):
    rows = [{'kind': 'iid', 'm': 4, 'seed': 0, 'ce': 2.5, 'target': 2.0, 'analytic_pass': False}]
    monkeypatch.setattr(validation, 'run_battery', lambda: rows)
    path = tmp_path/'failed.json'
    assert validation.main(['--out', str(path)]) != 0
    assert json.loads(path.read_text())['analytic_pass'] is False
    assert validation.exit_code(rows) == 1
    assert validation.exit_code([{**rows[0], 'ce': 2.0, 'analytic_pass': True}]) == 1  # incomplete


@pytest.mark.parametrize('fault', ['missing', 'duplicate', 'extra', 'nan', 'normalization',
                                  'count', 'support', 'deficit', 'false_flag', 'oracle_drift'])
def test_battery_gate_rejects_incomplete_or_invalid_recorded_results(battery, fault):
    rows = [dict(row) for row in battery[1]['rows']]
    if fault == 'missing':
        rows.pop()
    elif fault == 'duplicate':
        rows[-1] = dict(rows[-2])
    elif fault == 'extra':
        rows.append(dict(rows[-1], seed=99))
    elif fault == 'oracle_drift':
        rows[0].update(ce=.1, target=.1, deficit=0., analytic_pass=True)
    elif fault == 'false_flag':
        rows[0]['ce'] = rows[0]['target'] + .5
    else:
        key, value = {'nan': ('ce', float('nan')), 'normalization': ('normalization_max_error', .1),
                      'count': ('n', 1), 'support': ('root_support', 0),
                      'deficit': ('deficit', None)}[fault]
        next(row for row in rows if row['kind'] == 'lag2_full')[key] = value
    assert validation.exit_code(rows) == 1


def test_validation_cli_rejects_configuration_drift_before_running(tmp_path):
    import yaml
    cfg = yaml.safe_load((ROOT/'config/default.yaml').read_text())
    cfg['cells'][0]['D'] = 9
    path = tmp_path/'invalid.yaml'
    path.write_text(yaml.safe_dump(cfg))
    with pytest.raises(ValueError) as exc:
        validation.main(['--config', str(path), '--out', str(tmp_path/'results.json')])
    assert str(exc.value)
    assert not (tmp_path/'results.json').exists()


@pytest.mark.parametrize('alias', [False, True])
def test_validation_output_refuses_raw_including_symlinks(tmp_path, monkeypatch, alias):
    directory = ROOT/'data/raw'
    if alias:
        link = tmp_path/'raw-alias'
        link.symlink_to(directory, target_is_directory=True)
        directory = link
    monkeypatch.setattr(validation, 'run_battery', lambda: pytest.fail('raw accepted before fit'))
    with pytest.raises(ValueError) as exc:
        validation.main(['--out', str(directory/'validation-fixture.json'), '--force'])
    assert 'raw' in str(exc.value)
    assert not (directory/'validation-fixture.json').exists()


def test_validation_publication_refuses_a_racing_writer(tmp_path, monkeypatch):
    path = tmp_path/'result.json'

    def raced():
        path.write_bytes(b'other writer\n')
        return []

    monkeypatch.setattr(validation, 'run_battery', raced)
    with pytest.raises(FileExistsError) as exc:
        validation.main(['--out', str(path)])
    assert str(exc.value)
    assert path.read_bytes() == b'other writer\n'


def test_validation_forced_publication_is_atomic_on_write_failure(tmp_path, monkeypatch):
    path = tmp_path/'result.json'
    path.write_bytes(b'previous validation\n')
    monkeypatch.setattr(validation, 'run_battery', lambda: [])

    def interrupted(*args):
        raise OSError('interrupted writing validation')

    monkeypatch.setattr(validation, 'write_artifact', interrupted, raising=False)
    with pytest.raises(OSError, match='interrupted') as exc:
        validation.main(['--out', str(path), '--force'])
    assert str(exc.value)
    assert path.read_bytes() == b'previous validation\n'
    assert list(tmp_path.iterdir()) == [path]


def test_historical_m106_stress_records_execution_and_oracle_gap(battery):
    code, results = battery
    stress = [row for row in results['rows'] if row['m'] == 106]
    assert code == 0 and len(stress) == 9
    assert sorted({row['kind'] for row in stress}) == ['iid', 'lag2_core', 'lag2_full']
    assert all(math.isfinite(row['ce']) and row['n'] > 0 for row in stress)
    assert all(row['normalization_max_error'] <= 1e-12 for row in stress)
    assert all(0 < row['root_support'] <= 106 and row['nodes'] > 1 for row in stress)
    assert all(row['analytic_pass'] is None for row in stress)
    core = [row for row in stress if row['kind'] == 'lag2_core']
    assert len(core) == 3 and all(row['target'] is None and row['deficit'] is None for row in core)
    lag2 = [row for row in stress if row['kind'] == 'lag2_full']
    assert all(abs(row['target']-1.13109) <= 1e-4 and row['deficit'] > 0.0 for row in lag2)
    assert all(row['deficit'] is not None for row in stress if row['kind'] == 'iid')
