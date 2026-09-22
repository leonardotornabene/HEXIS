"""Stage run_tree_validation: the frozen synthetic battery of piano §12.1 (T15/T16).

Twenty-five small cases (five sources x five seeds) against the thresholds of the
§12.1 table, then the historical m=106 stress (three variants x three seeds) for
which only execution, normalization, supports and the gap from the declared
oracle are required — not reaching it. The battery reads no corpus; `--corpus-dir/
--output-dir` only re-verifies a published V1 run to bind the V0–V2 evidence into a
new scientific manifest (`validation_run`).

`generate` is the pure fixture of `docs/contracts/hexis-3.1/fixtures/ctw_validation/
verify_synthetic.py` (sha256 e6a55b08d5709d8966c4431b5bfec5d9c1cb64a5d3ba4dbf6e291b3b3c8479f0
in the design contract), extracted verbatim: same seeds, same call order, same
oracles. Its historical `main` is not reused — it fits an obsolete model and its
own pass flags contradict the §12.1 table (see THRESHOLD below).
"""
import argparse
import math
import os
import tempfile
from pathlib import Path

import numpy as np

from hexis.contracts import ROOT, load_contracts
from hexis.config import load_v31_config
from hexis.model.context_tree import CTW, CTWParams
from hexis.pipeline.corpus_run import check_destination, write_artifact

# §12.1 table. The historical script hardcodes 0.03 for iid/order1/lag2/variable
# and 0.02 only for cycle; the plan text, which governs semantics (§0), fixes
# |CE-2| <= 0.02 for iid m=4. The table wins: thresholds are never relaxed after
# results. `cycle` is the only strict inequality of the table (CE < 0.02).
THRESHOLD = {'iid': 0.02, 'cycle': 0.02, 'order1': 0.03, 'lag2': 0.03, 'variable': 0.03}
SMALL = (('iid', 4), ('cycle', 3), ('order1', 2), ('lag2', 2), ('variable', 2))
STRESS = ('iid', 'lag2_full', 'lag2_core')
NORMALIZATION_STRIDE = 2000  # positions between the full-vector normalization checks


def generate(kind,n,seed,m=2):
    r=np.random.default_rng(seed)
    if kind=='iid': return r.integers(m,size=n).tolist(),math.log2(m)
    if kind=='cycle': return (np.arange(n)%m).tolist(),0.
    x=r.integers(m,size=n).tolist(); prob=r.random(n)
    if kind=='order1':
        for i in range(1,n): x[i]=x[i-1] if prob[i]<.8 else 1-x[i-1]
        target=-.8*math.log2(.8)-.2*math.log2(.2)
    elif kind=='lag2':
        for i in range(2,n): x[i]=x[i-2] if prob[i]<.9 else 1-x[i-2]
        target=-.9*math.log2(.9)-.1*math.log2(.1)
    elif kind=='variable':
        # Context 0 -> Bernoulli .2; context 01 -> .1; context 11 -> .9.
        ll=[]
        for i in range(2,n):
            p=.2 if x[i-1]==0 else (.1 if x[i-2]==0 else .9)
            x[i]=int(prob[i]<p); ll.append(-math.log2(p if x[i] else 1-p))
        target=sum(ll)/len(ll)
    elif kind=='lag2_full':
        for i in range(2,n): x[i]=x[i-2] if prob[i]<.9 else x[i]
        p=.9+.1/m; target=-p*math.log2(p)-(m-1)*(.1/m)*math.log2(.1/m)
    elif kind=='lag2_core':
        # 90% frequent binary core; 10% rare independent symbols.
        z=r.integers(2,size=n).tolist()
        for i in range(2,n): z[i]=z[i-2] if prob[i]<.9 else 1-z[i-2]
        rare=r.random(n)<.1
        x=[int(r.integers(2,m)) if rare[i] else z[i] for i in range(n)]
        target=None
    else: raise ValueError(kind)
    return x,target


def analytic_pass(kind, m, ce, target):
    """§12.1 gate for the five small sources; None elsewhere — the stress sets no criterion."""
    if (kind, m) not in SMALL:
        return None
    if kind == 'cycle':
        return ce < THRESHOLD[kind]
    return abs(ce - target) <= THRESHOLD[kind]


def run_case(kind, m, seed, design, cell):
    """One frozen case: fit on the training seed, score the independent test stream."""
    train, _ = generate(kind, design['validation']['synthetic_n_train'], seed, m)
    test, target = generate(kind, design['validation']['synthetic_n_test'],
                            design['validation']['synthetic_test_seed_offset'] + seed, m)
    model = CTW(CTWParams.from_rho(m=m, depth=cell['D'], a=cell['a_per_symbol'], rho=cell['rho'])).fit([train])
    skip = design['min_available_past']
    result = model.evaluate([test], min_available_past=skip)
    error = max(abs(float(model.predict_proba(test[:position]).sum()) - 1.0)
                for position in range(skip, len(test), NORMALIZATION_STRIDE))
    diagnostics = model.diagnostics()
    return {'kind': kind, 'm': m, 'seed': seed, 'cell': cell['id'], 'target': target,
            'n': result.n, 'ce': result.ce, 'root_ce': result.root_ce,
            'deficit': None if target is None else result.ce - target,
            'analytic_pass': analytic_pass(kind, m, result.ce, target),
            'normalization_max_error': error,
            'nodes': diagnostics['nodes'],
            'node_count_by_structural_depth': diagnostics['node_count_by_structural_depth'],
            'support_histogram_1_2to4_5to9_10plus_by_depth':
                diagnostics['support_histogram_1_2to4_5to9_10plus_by_depth'],
            'root_observed_symbol_count': diagnostics['root_observed_symbol_count'],
            'root_stop': diagnostics['root_stop'], 'delta_root_nats_stop_minus_split':
                float(diagnostics['delta_root_nats_stop_minus_split']),
            'delta_root_reason': diagnostics['delta_root_reason'],
            'log_evidence': float(diagnostics['log_evidence'])}


def run_battery():
    """The whole §12.1 battery: 25 small cases then the historical m=106 stress."""
    design = load_contracts()['design']
    cell = next(entry for entry in design['cells'] if entry['id'] == 'C0')
    seeds = design['validation']['synthetic_training_seeds']
    stress_m = design['validation']['historical_stress_alphabet']
    rows = [run_case(kind, m, seed, design, cell) for kind, m in SMALL for seed in seeds]
    rows += [run_case(kind, stress_m, seed, design, cell) for kind in STRESS for seed in seeds[:3]]
    return rows


def exit_code(rows):
    """Accept the complete frozen battery, recomputing its checks rather than trusting flags."""
    design = load_contracts()['design']
    validation = design['validation']
    seeds = validation['synthetic_training_seeds']
    expected = {(kind, m, seed) for kind, m in SMALL for seed in seeds}
    expected |= {(kind, validation['historical_stress_alphabet'], seed)
                 for kind in STRESS for seed in seeds[:3]}
    try:
        keys = [(row['kind'], row['m'], row['seed']) for row in rows]
        if len(keys) != len(expected) or set(keys) != expected:
            return 1
        for row in rows:
            kind, m = row['kind'], row['m']
            if (type(m) is not int or type(row['seed']) is not int
                    or type(row['n']) is not int
                    or row['n'] != validation['synthetic_n_test'] - design['min_available_past']
                    or row['cell'] != 'C0'):
                return 1
            for field in ('ce', 'root_ce', 'normalization_max_error', 'root_stop',
                          'delta_root_nats_stop_minus_split', 'log_evidence'):
                if type(row[field]) not in (int, float) or not math.isfinite(row[field]):
                    return 1
            if (min(row['ce'], row['root_ce']) < 0
                    or not 0 <= row['normalization_max_error'] <= 1e-12
                    or not 0 <= row['root_stop'] <= 1 or row['delta_root_reason'] is not None
                    or type(row['root_observed_symbol_count']) is not int
                    or not 0 < row['root_observed_symbol_count'] <= m):
                return 1
            depths = row['node_count_by_structural_depth']
            histograms = row['support_histogram_1_2to4_5to9_10plus_by_depth']
            if (not depths or any(type(n) is not int or n <= 0 for n in depths)
                    or type(row['nodes']) is not int or row['nodes'] != sum(depths)
                    or len(histograms) != len(depths)):
                return 1
            for count, histogram in zip(depths, histograms):
                if (set(histogram) != {'1', '2to4', '5to9', '10plus'}
                        or any(type(n) is not int or n < 0 for n in histogram.values())
                        or sum(histogram.values()) != count):
                    return 1
            _, oracle = generate(kind, validation['synthetic_n_test'],
                                 validation['synthetic_test_seed_offset'] + row['seed'], m)
            if row['target'] != oracle:
                return 1
            if kind == 'lag2_core':
                if row['target'] is not None or row['deficit'] is not None:
                    return 1
            elif (type(row['target']) not in (int, float) or not math.isfinite(row['target'])
                  or type(row['deficit']) not in (int, float) or not math.isfinite(row['deficit'])
                  or abs(row['deficit'] - (row['ce'] - row['target'])) > 1e-12):
                return 1
            passed = analytic_pass(kind, m, row['ce'], row['target'])
            if passed is False or row['analytic_pass'] is not passed:
                return 1
    except (KeyError, TypeError, ValueError):
        return 1
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='HEXIS 3.1 frozen synthetic CTW battery (§12.1)')
    parser.add_argument('--config', type=Path, help='validate the deposited analytical projection')
    parser.add_argument('--out', type=Path, help='write the battery results as JSON')
    parser.add_argument('--force', action='store_true', help='overwrite an existing --out')
    parser.add_argument('--corpus-dir', type=Path, help='verify a V1 corpus for V0–V2 publication')
    parser.add_argument('--output-dir', type=Path, help='publish V0–V2 in a new scientific run')
    parser.add_argument('--fixture', action='store_true', help='explicitly synthetic corpus/configuration')
    args = parser.parse_args(argv)
    if (args.corpus_dir is None) != (args.output_dir is None):
        parser.error('--corpus-dir and --output-dir are required together')
    if args.corpus_dir is not None:
        if args.out is not None or args.force:
            parser.error('--out/--force belong to battery-only mode')
        from hexis.pipeline.validation_run import publish_validation
        publish_validation(args.config or ROOT/'config/default.yaml', args.corpus_dir,
                           args.output_dir, fixture=args.fixture)
        return 0
    if args.fixture:
        parser.error('--fixture requires --corpus-dir/--output-dir')
    load_v31_config(args.config)
    if args.out is not None:
        check_destination(args.out, ROOT/'data/raw')
    if args.out is not None and args.out.exists() and not args.force:
        raise ValueError(f'{args.out}: exists; pass --force to overwrite')
    rows = run_battery()
    code = exit_code(rows)
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.validation-', dir=args.out.parent) as temporary:
            path = Path(temporary)/'result.json'
            write_artifact(path, {'rows': rows, 'analytic_pass': code == 0})
            if args.force:
                os.replace(path, args.out)
            else:
                os.link(path, args.out)
    return code


if __name__ == '__main__':
    raise SystemExit(main())
