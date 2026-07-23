# Phase 1a Contract Bootstrap Design

**Status:** draft for owner review  
**Authoritative sources:** Master Spec §§6.2, 7; Decision Log D46, D52  
**Goal:** align the Phase-0 scaffold with the frozen D46/D52 contracts and leave
an executable G0 guard on the label-free scoring boundary, without implementing
scoring or manifest behavior.

## Scope

This increment changes four existing files:

- `pyproject.toml`: register the `g0` pytest marker.
- `tests/test_scores.py`: add the D52(ix)(1) structural contract tests.
- `src/hexis/protocols/scores.py`: add the D52 scoring-boundary stubs and remove
  the obsolete “D52 open” note.
- `src/hexis/manifest.py`: replace the obsolete per-artifact-manifest wording
  with the D46 central-run-manifest plus minimal-sidecar policy.

It adds no dependencies and touches no corpus data, model fitting, statistical
inference, serialization format, or context-tree growth decision.

## Scoring API

`src/hexis/protocols/scores.py` will expose the binding §6.2 signatures:

```python
def pooled_score_core(
    sequences, alphabet, cfg, rng, doc_ids
) -> tuple[pd.DataFrame, pd.DataFrame]:
    raise NotImplementedError


def annotate_scores(scores, ledger, registry) -> pd.DataFrame:
    raise NotImplementedError
```

The existing public `pooled_scores(registry, sequences, alphabet, cfg, rng)`
signature stays unchanged. Its body also remains `raise NotImplementedError`:
the thin composition is the eventual implementation contract, not behavior to
invent during scaffold alignment.

The core has no `registry`, `regime`, `author`, or `work` parameter. The
annotation function is the only new boundary allowed to receive the registry.

## Test-First Sequence

The marker registration and first test are written before the corresponding
stub. The test imports the existing `hexis.protocols.scores` module, asserts
that `pooled_score_core` exists, and checks the exact ordered parameter tuple:

```python
("sequences", "alphabet", "cfg", "rng", "doc_ids")
```

The first run must fail because the function is absent. Only then is the
minimal stub added. The same RED→GREEN cycle is repeated for
`annotate_scores(scores, ledger, registry)`.

Both tests carry `@pytest.mark.g0`. The core test establishes D52(ix)(1) for
the current stub: the exact public boundary has no label-bearing argument and
the body has no call graph through which labels could enter. When a real core
body is introduced, this G0 test must be extended with its static call-graph
check; the G3 byte-identity tests remain independently mandatory. The
annotation test protects the companion §6.2 signature. Neither test claims
that the complete mandatory G0 catalogue exists or that Gate G0 is closed.

## Manifest Contract

`src/hexis/manifest.py` remains an unimplemented module. Only its module
description changes to match D46:

- one central manifest for each run;
- every produced artifact listed with its SHA-256 in that manifest;
- one minimal sidecar `{run_id, sha256, entry_point}` per artifact.

No manifest interface is invented in this increment because §6.2 does not
define one.

## Verification and Acceptance

The increment is acceptable when:

1. each new structural test has been observed failing for the expected missing
   function;
2. both structural tests pass after the minimal stubs are added;
3. the full suite remains collectable with no failures;
4. `git diff --check` reports no whitespace errors;
5. after this design document is committed separately, the implementation diff
   contains only the four files listed in Scope.

The expected interim suite still contains the Phase-0 skipped tests. Passing
the two new G0 tests is not evidence that G0 as a whole has been reached.

## Explicitly Deferred

- enforcement against skipped, xfail, xpass, or assertion-free G0 tests;
- the remaining mandatory G0 files and real assertions;
- scoring, sampling-ledger, annotation, and canonical-serialization behavior;
- manifest/config/seed/overwrite implementation;
- D18-A1, O6, and O7.

These remain assigned to their existing roadmap phases and decisions.
