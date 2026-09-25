"""Mutation check of the 2a16a81 fixes at the current HEAD (V3-005 review closure).

Each mutant reverts or disables one fix in a temporary copy of HEAD (git archive +
git init), runs its target tests before and after, and records both outcomes. The
numbering N01… is new; it does not claim the identity of the lost pre-V3 mutants.
Usage: python mutate.py /path/to/hormathos > mutate.log
"""
import os, subprocess, sys, tempfile
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
A = 'tests/test_v31_pre_v3_audit.py::'
MUTANTS = [
    ('N01 R4 coordinate order via categorical .equals', 'src/hormathos/corpus.py',
     "        if c.assign(doc_id=c['doc_id'].astype(str)).sort_values(\n"
     "                SENTENCE_KEY+['encoded_index']).index.tolist()!=list(range(len(c))):",
     "        if not c.equals(c.sort_values(SENTENCE_KEY+['encoded_index']).reset_index(drop=True)):",
     [A+'test_category_order_cannot_hide_swapped_coordinate_order']),
    ('N02 sentence order via categorical .equals', 'src/hormathos/corpus.py',
     "        if s.assign(doc_id=s['doc_id'].astype(str)).sort_values(\n"
     "                SENTENCE_KEY).index.tolist()!=list(range(len(s))):",
     "        if not s.equals(s.sort_values(SENTENCE_KEY).reset_index(drop=True)):",
     [A+'test_category_order_cannot_hide_swapped_document_order']),
    ('N03 R5 unreadable manifest deletes everything', 'src/hormathos/pipeline/corpus_run.py',
     "        return  # An unreadable manifest",
     "        listed = set()  # An unreadable manifest",
     [A+'test_rollback_keeps_artifacts_when_the_manifest_is_unreadable']),
    ('N04 R6 samefile disabled', 'src/hormathos/pipeline/corpus_run.py',
     "ancestor.samefile(root)", "False",
     [A+'test_raw_alias_is_rejected_even_when_resolve_misses_it']),
    ('N05 corpus rollback unlinks all published', 'src/hormathos/pipeline/corpus_run.py',
     "        rollback_uncommitted(output, published)",
     "        [path.unlink(missing_ok=True) for path in published]",
     [A+'test_manifest_commit_exception_preserves_the_published_state']),
    ('N06 scientific rollback unlinks all published', 'src/hormathos/pipeline/scientific_run.py',
     "        corpus_run.rollback_uncommitted(output, published)",
     "        [path.unlink(missing_ok=True) for path in published]",
     [A+'test_scientific_manifest_commit_exception_keeps_a_valid_fixture_run']),
    ('N07 run extras unnamed', 'src/hormathos/pipeline/corpus_run.py',
     "            raise ValueError(f'run: extra {sorted(present-names)}, missing {sorted(names-present)} '\n"
     "                             'artifacts or interrupted temporary stage')",
     "            raise ValueError('run: missing/extra artifacts or interrupted temporary stage')",
     [A+'test_extra_ds_store_is_named_in_v1_and_deposit']),
    ('N08 deposit extras unnamed', 'src/hormathos/contracts.py',
     "            raise ValueError(f'{root}: extra {sorted(present - names)}, missing '\n"
     "                             f'{sorted(names - present)} contract files')",
     "            raise ValueError(f'{root}: missing or extra contract files')",
     [A+'test_extra_ds_store_is_named_in_v1_and_deposit']),
    ('N09 spread without rounding tolerance', 'src/hormathos/viz/plots.py',
     "    if np.any(low < -tolerance) or np.any(high < -tolerance):",
     "    if np.any(low < 0) or np.any(high < 0):",
     [A+'test_spread_accepts_one_rounding_unit_only']),
    ('N10 JSON relative tolerance restored', 'src/hormathos/pipeline/validation_run.py',
     "math.isclose(left, right, rel_tol=0, abs_tol=tolerance)",
     "math.isclose(left, right, rel_tol=REGENERATION_TOLERANCE, abs_tol=tolerance)",
     [A+'test_regeneration_tolerance_is_absolute_and_scales_only_loss_sums']),
    ('N11 loss sums not scaled by n', 'src/hormathos/pipeline/validation_run.py',
     "scale = left.get('n', 1) if key.startswith('sum_loss_') else 1",
     "scale = 1",
     [A+'test_regeneration_tolerance_is_absolute_and_scales_only_loss_sums']),
    ('N12 Parquet relative tolerance restored', 'src/hormathos/pipeline/validation_run.py',
     "np.allclose(a, b, rtol=0, atol=REGENERATION_TOLERANCE, equal_nan=True)",
     "np.allclose(a, b, rtol=REGENERATION_TOLERANCE, atol=REGENERATION_TOLERANCE, equal_nan=True)",
     [A+'test_regeneration_tolerance_is_absolute_and_scales_only_loss_sums']),
    ('N13 Parquet numeric dtype not checked', 'src/hormathos/pipeline/validation_run.py',
     "                raise ValueError(f'{original.name}.{column}: regenerated numeric type differs')",
     "                pass",
     [A+'test_regeneration_rejects_changed_integer_identity_in_parquet']),
    ('N14 fixture may reuse HEXIS-3.1', 'src/hormathos/pipeline/scientific_run.py',
     "    if fixture and cfg.get('spec_version') == 'HEXIS-3.1':",
     "    if False:",
     [A+'test_fixture_cannot_reuse_the_deposited_spec_version']),
    ('N15 block overlap not refused', 'src/hormathos/protocols/sampling.py',
     "    if len(members) != len(set(members)):",
     "    if False:",
     [A+'test_sample_fold_rejects_a_document_in_two_blocks_before_training']),
    ('N16 load_corpus reads the original directory', 'src/hormathos/pipeline/scientific_run.py',
     "        frames = {name: pd.read_parquet(private / name)",
     "        frames = {name: pd.read_parquet(corpus_dir / name)",
     [A+'test_load_corpus_reads_the_validated_private_copy']),
    ('N17 collection gate not registered', 'conftest.py',
     '    config.pluginmanager.register(_CollectionGate(), name="hormathos-collection-gate")',
     '    pass',
     ['tests/test_v31_enforcement.py::test_collection_skip_without_marker_fails_the_gate',
      'tests/test_v31_enforcement.py::test_nested_conftest_collection_skip_fails_the_gate']),
    ('N18 regeneration scope not recorded', 'src/hormathos/pipeline/validation_run.py',
     "            'comparison_scope': 'identity_and_values',", "",
     ['tests/test_v31_completion.py::test_seed_zero_regeneration_is_compared_and_recorded_by_the_report']),
]


def run(argv, cwd, env=None):
    return subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True)


def main():
    head = run(['git', 'rev-parse', 'HEAD'], REPO).stdout.strip()
    python = REPO/'.venv/bin/python'
    with tempfile.TemporaryDirectory(prefix='hormathos-mutate-') as tmp:
        copy = Path(tmp)/'repo'
        copy.mkdir()
        archive = run(['git', 'archive', '-o', str(Path(tmp)/'head.tar'), 'HEAD'], REPO)
        assert archive.returncode == 0, archive.stderr
        assert run(['tar', '-xf', str(Path(tmp)/'head.tar'), '-C', str(copy)], tmp).returncode == 0
        for argv in (['git', 'init', '-q'], ['git', 'add', '-A'],
                     ['git', '-c', 'user.name=m', '-c', 'user.email=m@m', 'commit', '-qm', 'HEAD copy']):
            assert run(argv, copy).returncode == 0, argv
        for entry in (REPO/'data/raw').iterdir():
            if entry.is_dir():
                (copy/'data/raw'/entry.name).symlink_to(entry, target_is_directory=True)
        (copy/'results').mkdir()
        (copy/'results/hexis31').symlink_to(REPO/'results/hexis31', target_is_directory=True)
        env = {**os.environ, 'PYTHONPATH': str(copy/'src'), 'MPLCONFIGDIR': str(Path(tmp)/'mpl')}
        print(f'HEAD {head}; copy {copy}; python {python}')
        killed = 0
        for name, rel, old, new, targets in MUTANTS:
            path = copy/rel
            source = path.read_text()
            assert source.count(old) == 1, (name, 'anchor not unique')
            pytest = [str(python), '-m', 'pytest', '-q', '-p', 'no:cacheprovider', *targets]
            base = run(pytest, copy, env)
            path.write_text(source.replace(old, new))
            try:
                mutated = run(pytest, copy, env)
            finally:
                path.write_text(source)
            last = lambda r: (r.stdout.strip().splitlines() or [''])[-1]
            dead = base.returncode == 0 and mutated.returncode != 0
            killed += dead
            print(f'{name}\n  file {rel}; targets {targets}\n  baseline rc={base.returncode} {last(base)}'
                  f'\n  mutant   rc={mutated.returncode} {last(mutated)}\n  => {"KILLED" if dead else "SURVIVED"}')
        print(f'TOTAL {len(MUTANTS)} mutants: {killed} killed, {len(MUTANTS) - killed} survived')
        return 0 if killed == len(MUTANTS) else 1


if __name__ == '__main__':
    sys.exit(main())
