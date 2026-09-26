# tests/ — what the code is guaranteed to do

These are the acceptance tests of HORMATHOS: 431 test cases in 18 files, all run on every check, none skipped. They show that the code does what the deposited plan requires. They check the model on cases with known answers and every file of the plan against its recorded hash, and they check that a run refuses corrupted or incomplete input. All model fits in the tests use small synthetic corpora. The real corpus is only read and counted, never fitted.

## How to run them

From the repository root, after `uv sync --frozen` and fetching the corpus as the [README](../README.md#reproduce) shows:

```bash
uv run pytest            # 431 passed
uv run pytest -m v31     # the same 431: every test carries the marker v31
```

The root [`conftest.py`](../conftest.py) enforces the rules of acceptance on every run: each test carries the marker `v31`, none may be skipped or expected to fail, and each must execute at least one `assert`. A test that breaks these rules fails the whole run. `tests/conftest.py` only provides small CoNLL-U samples to the reader tests.

## What is here, by area

| Area | Files |
|---|---|
| reading and encoding the corpus | `test_conllu_reader.py`, `test_v31_corpus.py`, `test_v31_config.py` |
| the prediction model | `test_v31_context_tree.py` |
| sampling, scores and the frequency comparison | `test_v31_sampling.py`, `test_v31_scores.py`, `test_v31_r1.py` |
| runs: identity, atomic publication, resume, report, figures | `test_v31_persistence.py`, `test_v31_descriptive.py`, `test_v31_completion.py`, `test_v31_report_semantics.py`, `test_v31_figures.py`, `test_v31_validation_run.py` |
| the repository: plan and history preserved byte for byte, instructions aligned | `test_v31_docs.py` |
| the acceptance rules themselves | `test_v31_enforcement.py`, `test_gate_inventory_anchor.py` |
| errors found by the reviews before the campaign, kept as regressions | `test_v31_pre_v3_audit.py`, `test_v31_pre_v4_review.py` |

The [test inventory](../docs/TEST_INVENTORY.md#what-each-active-file-proves) says what each file proves and maps every requirement of the plan (T01–T30) to the tests that enforce it. Each file opens with a docstring stating its scope.

## Why the tests must not change

The tests are part of the frozen code of the published runs: a run records the hash of every test file and of its own acceptance run (`v31.junit.xml`, `v31_process.json` in [`results/hexis31/`](../results/hexis31/README.md)). A property that still holds is never weakened. A test is retired only by replacing it with another test that states why. The earlier test suites are kept, not run, in [`archive/tests/`](../archive/tests/).
