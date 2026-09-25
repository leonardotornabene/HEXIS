"""Package-level checks of the V3-005 rerun, reused unchanged for V3-006 (these import hormathos; see indep_check.py for
the recomputation that does not). Run from the repository root with uv run --no-sync.

  checks.py validate RUN [RUN ...]    validate_run, manifest SHA, run ID, evidence V0–V3,
                                      42/84 keys, verify_technical, verify_evidence(current)
  checks.py compare ORIGINAL REGEN    compare_regeneration
  checks.py resume RUN SCRATCH        V4 --resume preconditions on a copy of RUN
"""
import hashlib, shutil, sys
from collections import Counter
from pathlib import Path

from hormathos.contracts import compare as same
from hormathos.pipeline import corpus_run, scientific_run as sr, validation_run as vr

CONFIG, CORPUS = Path('config/default.yaml'), Path('results/hexis31/v1')


def setup():
    cfg = sr.load_projection(CONFIG, False)[0]
    corpus, frames = sr.load_corpus(CORPUS)
    return cfg, corpus, frames


def validate(runs):
    cfg, corpus, frames = setup()
    contract = sr.run_contract(cfg, corpus)
    current = vr.context(CONFIG, CORPUS, contract)
    print('current run_id', corpus_run.run_identity(contract))
    for run in map(Path, runs):
        m = sr.validate_run(run)
        k = sr.key_sets(m['keys'])
        vr.verify_evidence(run, m, current=current)
        vr.verify_technical(run, m, cfg, frames, scientific=True)
        desc = m['metadata']['descriptive']
        rows = desc['models']
        print(run)
        print(' manifest_sha256', hashlib.sha256((run/'manifest.json').read_bytes()).hexdigest())
        print(' run_id', m['run_id'], 'stages', m['completed_stages'], 'evidence', sorted(m['evidence']))
        print(' pairs', len(k['pair']), 'models', len(k['model']), 'seeds', sorted({x[2] for x in k['pair']}),
              'cells', dict(sorted(Counter(x[0] for x in k['pair']).items())))
        v3 = m['evidence']['V3']
        print(' V3 pair_count', v3['pair_count'], 'model_count', v3['model_count'],
              'artifacts', len(v3['artifacts']), 'scientific', v3['scientific'])
        print(' verify_evidence(current context) OK; verify_technical OK')
        print(' checks', {key: m['checks'][key] for key in sorted(m['checks']) if key != 'cells'})
        print(' metadata selection', desc.get('selection'), 'resume', desc.get('resume'),
              'tracked_dirty', desc.get('tracked_dirty'), 'implementation_commit', desc.get('implementation_commit'))
        print(' fit_s %.2f eval_s %.2f max_peak_rss %d (%s)' % (
            sum(r['fit_seconds'] for r in rows), sum(r['evaluation_seconds'] for r in rows),
            max(r['peak_rss'] for r in rows), max(rows, key=lambda r: r['peak_rss']).get('cell')))
        print(' disk_bytes', sum(p.stat().st_size for p in run.iterdir()), 'files', len(list(run.iterdir())))


def compare(original, regenerated):
    cfg, _, frames = setup()
    for run in (original, regenerated):
        print(run, 'manifest_sha256', hashlib.sha256((Path(run)/'manifest.json').read_bytes()).hexdigest())
    c = vr.compare_regeneration(Path(original), Path(regenerated), cfg, frames)
    print({key: value for key, value in c.items() if key != 'artifacts'})
    print('artifact_comparisons', dict(Counter(c['artifacts'].values())), 'of', len(c['artifacts']))


def resume(run, scratch):
    """run_descriptive.main up to the first fit, on a copy: nothing is fitted or published."""
    from hormathos.pipeline.run_report import validate_partitions
    run, copy = Path(run), Path(scratch)/Path(run).name
    assert not copy.exists(), copy
    shutil.copytree(run, copy)
    cfg, corpus, frames = setup()
    sr.check_destination(copy, CORPUS)
    contract = sr.run_contract(cfg, corpus)
    evidence = sr.evidence(contract, CORPUS, corpus)
    prior = sr.read_prior(copy)
    sr.check_stage_open(copy, 'descriptive', prior, True)
    same(contract, prior['run_contract'], 'run_contract')
    same(evidence, {step: prior['evidence'].get(step) for step in evidence}, 'evidence')
    vr.verify_evidence(copy, prior, current=vr.context(CONFIG, CORPUS, contract))
    validate_partitions(copy, prior, cfg, frames)
    vr.verify_technical(copy, prior, cfg, frames, scientific=True)
    sr.require_clean_producers()
    print(copy, 'V4 --resume preconditions: all pass (no fit run)')
    shutil.rmtree(copy)


if __name__ == '__main__':
    {'validate': lambda: validate(sys.argv[2:]), 'compare': lambda: compare(*sys.argv[2:4]),
     'resume': lambda: resume(*sys.argv[2:4])}[sys.argv[1]]()
