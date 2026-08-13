# Phase 1a Contract Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align the Phase-0 scaffold with the frozen D46/D52 contracts and add
the first executable G0 guards without implementing scoring or manifest logic.

**Architecture:** Treat the scoring boundary as a public API contract: pytest
checks the exact label-free core signature before the stub is added. Keep
manifest work documentation-only because no manifest interface is frozen in
Spec §6.2. The two independent changes receive separate review and commit
gates.

**Tech Stack:** Python 3.12, pandas, pytest 9, uv, TOML.

## Global Constraints

- Authoritative requirements: Master Spec §§6.2, 7 and Decision Log D46, D52.
- Use Python `>=3.12,<3.13` through uv; add no dependency.
- Write the failing test before each new scoring stub and observe the expected
  failure before production edits.
- Never weaken or delete an existing test.
- `pooled_score_core` takes no registry and no label-bearing argument.
- Do not implement scoring, sampling, annotation, manifests, seeds, config
  resolution, overwrite protection, or canonical serialization in this plan.
- Do not import anything from `candidates/`.
- Touch no real corpus data and fit no model.
- Do not claim Gate G0 is closed: this plan adds only the first two marked
  structural tests.
- Before every commit, show the complete diff and wait for the owner's explicit
  permission.

---

### Task 1: Establish the D52 Scoring Boundary Contract

**Files:**

- Modify: `pyproject.toml:24-29`
- Modify: `tests/test_scores.py:1-26`
- Modify: `src/hexis/protocols/scores.py:1-47`

**Interfaces:**

- Consumes: the frozen signatures in Master Spec §6.2 and D52(v).
- Produces:
  `pooled_score_core(sequences, alphabet, cfg, rng, doc_ids)
  -> tuple[pd.DataFrame, pd.DataFrame]`;
  `annotate_scores(scores, ledger, registry) -> pd.DataFrame`.
- Preserves:
  `pooled_scores(registry, sequences, alphabet, cfg, rng) -> pd.DataFrame`.

- [ ] **Step 1: Register the G0 marker**

Add the marker declaration inside `[tool.pytest.ini_options]` in
`pyproject.toml`:

```toml
markers = [
    "g0: Gate G0 acceptance tests (D52); incomplete until all mandatory coverage is implemented",
]
```

This registration lets `--strict-markers` distinguish the frozen `g0` marker
from a typo. It does not mark any existing skipped placeholder.

- [ ] **Step 2: Write the failing core-boundary test**

Add `inspect` and the real module import near the top of
`tests/test_scores.py`:

```python
import inspect

import pandas as pd
import pytest

from hexis.protocols import scores
```

Add this unskipped test before the existing `@SKIP` cases:

```python
@pytest.mark.g0
def test_pooled_score_core_has_label_free_signature():
    core = getattr(scores, "pooled_score_core", None)
    assert core is not None

    signature = inspect.signature(core)
    assert tuple(signature.parameters) == (
        "sequences",
        "alphabet",
        "cfg",
        "rng",
        "doc_ids",
    )
    assert set(signature.parameters).isdisjoint(
        {"registry", "regime", "author", "work"}
    )
    assert signature.return_annotation == tuple[pd.DataFrame, pd.DataFrame]
```

Keep the existing three G3 placeholders and their `@SKIP` decorators unchanged.

- [ ] **Step 3: Run the core test and verify RED**

Run:

```bash
uv run pytest \
  tests/test_scores.py::test_pooled_score_core_has_label_free_signature \
  --strict-markers -v
```

Expected result: one test fails at `assert core is not None` because
`hexis.protocols.scores` does not yet expose `pooled_score_core`. A collection
error, unknown-marker error, or different assertion failure is not the
expected RED state and must be corrected before continuing.

- [ ] **Step 4: Add the minimal label-free core stub**

Insert this function between `delta_ce_scores` and `pooled_scores` in
`src/hexis/protocols/scores.py`:

```python
def pooled_score_core(
    sequences, alphabet, cfg, rng, doc_ids
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Protocol-(c) label-free core returning scores and sampling ledger (D52).

    Model-derived score columns, in order: doc_id, gain_mean, gain_sd,
    depth_mean, depth_sd, frac_restricted, coverage. Ledger columns, in order:
    evaluation_doc_id, seed, training_doc_id, sampled_token_count.
    """
    raise NotImplementedError
```

Do not add `registry`, `regime`, `author`, `work`, a helper call, or any
implementation.

- [ ] **Step 5: Run the core test and verify GREEN**

Run the same targeted command:

```bash
uv run pytest \
  tests/test_scores.py::test_pooled_score_core_has_label_free_signature \
  --strict-markers -v
```

Expected result: `1 passed`.

- [ ] **Step 6: Write the failing annotation-boundary test**

Add this second unskipped test immediately after the core test:

```python
@pytest.mark.g0
def test_annotate_scores_has_d52_signature():
    annotate = getattr(scores, "annotate_scores", None)
    assert annotate is not None

    signature = inspect.signature(annotate)
    assert tuple(signature.parameters) == ("scores", "ledger", "registry")
    assert signature.return_annotation is pd.DataFrame
```

- [ ] **Step 7: Run the annotation test and verify RED**

Run:

```bash
uv run pytest \
  tests/test_scores.py::test_annotate_scores_has_d52_signature \
  --strict-markers -v
```

Expected result: one test fails at `assert annotate is not None` because the
function is absent.

- [ ] **Step 8: Add the minimal annotation stub**

Insert this function between `pooled_score_core` and `pooled_scores`:

```python
def annotate_scores(scores, ledger, registry) -> pd.DataFrame:
    """Attach registry fields and own-regime pool fraction to fixed scores (D52).

    This label-aware stage is outside the byte-identity guarantee.
    """
    raise NotImplementedError
```

Do not compute annotations or inspect the registry.

- [ ] **Step 9: Run both structural tests and verify GREEN**

Run:

```bash
uv run pytest \
  tests/test_scores.py::test_pooled_score_core_has_label_free_signature \
  tests/test_scores.py::test_annotate_scores_has_d52_signature \
  --strict-markers -v
```

Expected result: `2 passed`.

- [ ] **Step 10: Align the surrounding scoring documentation**

Replace the module description in `tests/test_scores.py` with:

```python
"""Score-function tests (Spec §7; G0 boundary contract, G3 scoring behavior).

The D52 scoring-boundary signatures are real G0 assertions. The analytic,
restriction, and byte-identity cases remain Phase-0 placeholders for G3 and
must never be deleted or weakened.
"""
```

Replace the module description in `src/hexis/protocols/scores.py` with:

```python
"""Score functions and LODO orchestration (Spec §4.2, §4.4; D35, D36, D52).

pooled_score_core is the label-free protocol-(c) boundary. Registry-derived
fields enter only through annotate_scores; pooled_scores remains the public
composition. The G3 byte-identity tests must never be weakened.
"""
```

Replace the obsolete `pooled_scores` docstring, including the “D52 open” note,
with:

```python
"""Public protocol-(c) scoring contract: label-free core plus annotation.

The eventual implementation is the thin composition required by D52(v).
Scoring behavior remains unimplemented in this scaffold.
"""
```

Keep its body as `raise NotImplementedError`.

- [ ] **Step 11: Verify the Task-1 test surface**

Run the marked subset:

```bash
uv run pytest -m g0 --strict-markers -v
```

Expected interim result: the two new structural tests pass. This command does
not prove G0 completion because the remaining mandatory files are not marked
or implemented yet.

Run the full suite:

```bash
uv run pytest
```

Expected interim result: `2 passed, 35 skipped`, with no failures or collection
warnings.

- [ ] **Step 12: Present the Task-1 diff and stop for commit permission**

Run:

```bash
git diff --check
git status --short
git diff -- pyproject.toml tests/test_scores.py src/hexis/protocols/scores.py
```

Expected scope: exactly those three modified files. Explain the RED and GREEN
results to the owner. Do not stage or commit until the owner explicitly
authorizes it.

- [ ] **Step 13: Commit Task 1 after explicit permission**

Only after permission:

```bash
git add pyproject.toml tests/test_scores.py src/hexis/protocols/scores.py
git commit -m "chore: align scoring scaffold with D52"
```

Then run:

```bash
git status --short --branch
git show --stat --oneline HEAD
```

Expected result: a clean working tree and a commit containing exactly the
three Task-1 files.

---

### Task 2: Align the Manifest Scaffold with D46

**Files:**

- Modify: `src/hexis/manifest.py:1-6`

**Interfaces:**

- Consumes: the frozen D46 run-manifest and minimal-sidecar policy.
- Produces: no executable interface; this task corrects the scaffold contract
  only.

- [ ] **Step 1: Record the stale wording before editing**

Run:

```bash
rg -n "one manifest per artifact" src/hexis/manifest.py
```

Expected result: the obsolete statement is found on line 2. This is a
documentation-only correction, so no executable RED test is appropriate.

- [ ] **Step 2: Replace the module description**

Replace the complete module docstring with:

```python
"""Run-level artifact provenance (Spec §6.4; D26, D46).

One central manifest per run records the git commit, dirty flag,
resolved-config SHA-256, input hashes, package versions, timestamps, seed, and
every produced artifact with its SHA-256. Each artifact carries or is
accompanied by the minimal sidecar {run_id, sha256, entry_point}.

Interface not specified in Spec §6.2; signatures will be proposed for approval
before implementation — no invented contracts.
"""
```

Do not add functions, schemas, file writes, or imports.

- [ ] **Step 3: Verify the corrected contract**

Run:

```bash
! rg -n "one manifest per artifact" src/hexis/manifest.py
sed -n '1,20p' src/hexis/manifest.py
git diff --check
```

Expected result: the stale phrase is absent, the rendered description matches
D46, and no whitespace error is reported.

- [ ] **Step 4: Re-run the complete verification surface**

Run:

```bash
uv run pytest -m g0 --strict-markers -v
uv run pytest
```

Expected interim results: the two marked structural tests pass; the full suite
reports `2 passed, 35 skipped`; neither command has failures or warnings.

- [ ] **Step 5: Present the Task-2 diff and stop for commit permission**

Run:

```bash
git status --short
git diff -- src/hexis/manifest.py
git diff --check
```

Expected scope: only `src/hexis/manifest.py`. Explain that this changes no
runtime behavior. Do not stage or commit until the owner explicitly
authorizes it.

- [ ] **Step 6: Commit Task 2 after explicit permission**

Only after permission:

```bash
git add src/hexis/manifest.py
git commit -m "docs: align manifest scaffold with D46"
```

Then run:

```bash
git status --short --branch
git show --stat --oneline HEAD
git diff --check HEAD~2..HEAD
```

Expected result: clean working tree; the two implementation commits together
touch only the four files authorized by the design; the combined diff has no
whitespace errors.

---

## Final Handoff

At completion, report:

- the two commit hashes;
- the observed RED failure for each new scoring function;
- the final targeted and full-suite counts;
- that Gate G0 remains open;
- that no real data or model was touched;
- that the next increment is the repository-level G0 enforcement plus the
  first real `conllu_reader` test cycle.
