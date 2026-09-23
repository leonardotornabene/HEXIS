# HORMATHOS handoff — current state (design HEXIS 3.1)

**V0–V2 completed; V3–V5 not attested; no real fit.** Publication of 2026-09-23: the push of the branch `codex/hexis31-realign` at `2ebb3464b871c1f831d0608edba052ccb4b92be9` and of the tags `archive/pre-realign` and `archive/v2.1`; then the merge into `master` (`73df64d`, a merge commit with neither squash nor rebase) and the deletion of the remote branches `g1/pre-audit` (V3-002, E5) and `codex/hexis31-realign`, whose content is in `master`. Active branch: `master`; the realignment started from `5f1ec06afa192c8d0f006d7f39cdb97df72c2983`. On the same day the project was named HORMATHOS (V3-003); the GitHub repository and the local directory keep the old name until their own go. The detailed chronology of the earlier tranches is not repeated here: it is in the Git history and, in its last pre-realignment form, in [archive/docs/HANDOFF.md](../archive/docs/HANDOFF.md).

## Project name HORMATHOS — 23 September 2026 (V3-003)

**Commits.** `7f3f641`: fixes prepared by Codex, reviewed and committed — the report rechecks the recorded V2 execution context before its first step and again before publication, and a seed-0 run of a single cell leaves V3 pending instead of failing after publishing its pairs; each of the two new tests failed with its fix removed. `4a82f7e`: the package moves from `src/hexis` to `src/hormathos`, tests first. The documents, their English translation and V3-003 are `e086482`; this attestation follows in a commit of its own, which does not cite itself.

**What changed and what stays.** Imports, paths, CLI descriptions, temporary-directory prefixes, the figure footer and the SVG hash salt follow the package. The distribution keeps the name `hexis`: `uv.lock` records it, and the deposited design fixes the lock bytes (`runtime.lock_sha256`), which `corpus_run` and `scientific_run.run_contract` enforce. The contract identifiers, the deposit, the persisted schema names, `results/hexis31/` and `archive/` keep `hexis`. The V3-001 hash now starts at the first V3-001 heading, so the title of the log can change; the act bytes are unchanged. `00_LEGGIMI_INDICE.md` and `03_ROADMAP_OPERATIVA_IT.md` are now `00_INDEX.md` and `03_ROADMAP.md`. The rest is in V3-003.

**Verification of the renamed package, in a separate clone with its own environment.** `uv lock --check` resolves 23 packages and `uv.lock` keeps SHA-256 `33db43b0…`. The V1 corpus `results/hexis31/v1` is still accepted: `load_corpus` and `run_contract` on the deposited configuration give lock `33db43b0…` and 25 code files under `src/hormathos`. `run_audit` and `run_encode` regenerate the nine V1 artifacts byte for byte; in the manifest every `run_contract` field other than `code` equals V1, the input snapshots are identical once their paths are made relative, and the rest is `run_id` and the external fields. Against `7f3f641`, 11 of the 25 sources are byte-identical and 14 carry the changes of `4a82f7e`.

**Review before the push (R1–R4).** An independent review found four residues, each fixed or decided before publication (V3-003, decisions R1–R4). R1: the sdist took every file not ignored by the root `.gitignore` — the five proposal drafts, `scripts/`, and the tools' notes under `.superpowers/` and `.claude/`; it is now a closed list equal to the tracked tree, which `test_the_sdist_ships_exactly_the_tracked_tree` enforces, and an sdist built with those local files present holds exactly the 228 tracked files plus `PKG-INFO`. R2: the pipeline runs from a checkout, and the README says so. R3: the cost of the per-pair revalidation is accepted, see the V3–V5 sequence. R4: Plato's *Ion* is B11, its passage checked against the Greek text, and the Italian left in the docstrings and comments of 17 files is translated; with docstrings set aside, the syntax tree of every changed module is unchanged.

**Attestation.** Measured on `e086482`, with a clean tracked tree before and after:

```text
uv run --frozen pytest -q -p no:cacheprovider
404 passed in 177.61s (0:02:57)

uv run --frozen pytest --collect-only -q          404 tests collected
uv run --frozen pytest -m v31 --collect-only -q   404 tests collected
uv run --frozen pytest . --collect-only -q        404 tests collected
uv lock --check                                   Resolved 23 packages
```

The three collections have the same node IDs and none under `archive/`, and `uv.lock` keeps SHA-256 `33db43b0…`. The count rises from 400 by the three cases of `7f3f641` and by the package guard of `4a82f7e`. Each new test failed before its change: the two tests of `7f3f641` with their source file restored from `d7c8f21`, the package guard while the package was still `src/hexis`, and the new assertions on the documents against the Italian documents.

**Attestation after the review.** Fixes in `348b8da` (sdist, test and docstrings) and `39bb7ec` (documents); measured on `39bb7ec`, with a clean tracked tree before and after:

```text
uv run --frozen pytest -q -p no:cacheprovider
405 passed in 180.00s (0:03:00)

uv run --frozen pytest --collect-only -q          405 tests collected
uv run --frozen pytest -m v31 --collect-only -q   405 tests collected
uv run --frozen pytest . --collect-only -q        405 tests collected
uv lock --check                                   Resolved 23 packages
```

The three collections have the same 405 node IDs and none under `archive/`; the count rises by the sdist test. `uv.lock` keeps SHA-256 `33db43b0…`. The sdist built in this working copy, with the five proposal drafts, `scripts/`, `.superpowers/` and `.claude/` present, holds exactly the 228 tracked files plus `PKG-INFO`. The V1 corpus regenerated at `39bb7ec` reproduces the nine artifacts byte for byte, and every field of its run contract other than the code equals V1.

## Code review of 23 September 2026

Two full reviews of `5f1ec06..a4a8871`, each finding verified on the repository before acting.

**Accepted and fixed.** The archive was collected by `pytest .`: the realignment had removed `norecursedirs`, and the docstring that promised the opposite had no assert. The attestation of the transfer from `legacy_audit` said "without changes", while the message of `verify_inputs_unchanged` had changed. The act gave two licences to the same bytes and did not cover `config/`, the metadata of `data/`, the scripts of the deposit or the code under `archive/`. `LICENSE` did not declare its own scope, and the README repeated the act. `archive/README.md` was a new note in place of the historical README. `.gitignore` no longer ignored `data/interim/` and `data/processed/`, and also ignored `archive/results/`. `CANONICAL_DATA_ROOT` depended on the current directory. A false docstring in `manifest.py`, an orphan comment and leftover blank lines remained. Two new tests bind the archive: `test_the_archive_is_never_collected_even_from_the_root` and `test_every_archived_file_has_its_bytes_at_the_base`.

**Rejected.** Limiting the rule "every collected test is v31" to the repository alone: `test_every_collected_test_is_active_acceptance` verifies it precisely in a synthetic project, and no synthetic project has tests without the marker. Changing the two tests that refuse an importable `hexis.stats` (now `hormathos.stats`): the refusal is correct, and the cause is avoided as "Running the history" says.

**Attestation.** Fixes in `61d4a08` (tests first, then code and configuration) and `2eabcb6` (act and documents); this section did not cite its own commit. Measured on `2eabcb6`, with a clean tracked tree before and after:

```text
uv run --frozen pytest -q -p no:cacheprovider
400 passed in 163.67s (0:02:43)

uv run --frozen pytest --collect-only -q          400 tests collected
uv run --frozen pytest -m v31 --collect-only -q   400 tests collected
uv run --frozen pytest . --collect-only -q        400 tests collected
uv lock --check                                   Resolved 23 packages
```

The three collections have the same node IDs and none under `archive/`. Before the fixes, each of the two new tests failed on its own finding: `archive/tests/test_old.py` collected by `pytest .`, and `archive/README.md` with blob `d8c0353` instead of `d0e062e`. The archive has 102 of 102 files identical to `5f1ec06`, no path lost. Compared with `legacy_audit` at `5f1ec06`, the AST differs only in `verify_inputs_unchanged` and `CANONICAL_DATA_ROOT`, as V3-002 declares. The V1 corpus regenerated with `run_encode` at `2eabcb6`, in an external directory, reproduces the nine artifacts byte for byte; in the manifest only `run_id`, the code identity and the external fields already declared differ.

## Realignment of 22 September 2026 — verification

Commits of the realignment on `codex/hexis31-realign`: act `1294f55`, test migration `90dffc0`, code and gate `f6ffe51`, documents and archive `08ba6cd`, leftovers `1f441ff`. This section is documentary and did not cite its own commit.

**Suite and gate.** Final lines, verbatim:

```text
uv run --frozen pytest -q -p no:cacheprovider
398 passed in 190.31s (0:03:10)

uv run --frozen pytest --collect-only -q          398 tests collected
uv run --frozen pytest -m v31 --collect-only -q   398 tests collected
uv lock --check                                   Resolved 23 packages
```

The two selections coincide, with no skip and nothing deselected. Baseline at `5f1ec06`: 672 passed plus 17 skips in the full suite, 351 in the acceptance.

**No file lost.** Every path existing at `5f1ec06` is today either in the active tree or in `archive/`: 102 archived files, all with the same blob as the original; 34 active files modified; no new active file outside the archive. Until the correction of 23 September this line counted 101 and 30: the hundred-and-second item was a new note in place of the historical README, and the modified files were already 33.

**Invariants.** The 69 tracked files of the deposit, the record, the lock, the configuration, the provenance and `data/raw/PROVENANCE.md` have blobs identical to `5f1ec06`. The 98 local files of `data/raw`, `scripts/` and `results/hexis31` have the same sha256 as the baseline.

**Equivalence of the 3.1 path.** The frozen synthetic battery is identical byte for byte to its run at `5f1ec06`. The regenerated V1 corpus reproduces the nine artifacts byte for byte; in the manifest only `run_id`, the code identity and the four external fields declared in advance differ (`created_utc`, `output_dir`, `implementation_commit`, and `tracked_dirty` when the tree is not clean).

**Coverage.** Line differential between the full suite and `-m v31`, measured on unchanged code with the standard library's `sys.monitoring`: 231 lines were reached only by the non-v31 tests, all of them, and only them, in the v2.1 code later removed. No line of the 3.1 path lost coverage.

**Mutations.** The 40 mutations of the pre-V3 review all still anchor to the current code: **35 killed, 5 survived — M3, M6, M14, A1, P1 — the same as at `0dc69b5`**, dominated by stronger checks.

**Leftovers.** Outside the deposit, the archive and the acts, only mentions of history as history and guards that forbid its return remain. Two relative links inside V3-001 stay broken by choice, because the bytes of an act are not rewritten: V3-002 resolves them with the rule `archive/<path>`. The comment in `config/registry_overrides.yaml` still cites `history/v2.1`: the configuration is an invariant of this realignment and was not touched.

## Identity

| Object | Identity |
|---|---|
| V0 deposit | `e98fb8edde91e821c415e26f33b7bdeb549b50ba`; 63 digests in [V3-001-deposit.json](V3-001-deposit.json) |
| V1 corpus | `7afdd3a4f87341110b0f15a77179febe9075ee9b`; delivered run `results/hexis31/v1`, manifest SHA-256 `154433c772f41e444f86b8787e0ee0003c546d9fb398b6ee0f634ce193f3421f` |
| V2 closure | `0a6f644`; pre-V3 review `0dc69b5`, attested **351 v31 / 672 passed + 17 skips** |
| Realignment base | `5f1ec06`, tag `archive/pre-realign`; v2.1 history at tag `archive/v2.1` = `852644b6917790877c7b2ca5df2e76b17829d87c` |
| Name | HORMATHOS (V3-003); package `src/hormathos`, distribution `hexis` |
| Environment | Python 3.12.13, `uv.lock` `33db43b00bcb21ab12aedf6dcc4257764770bff0115dc0d1dfab6e5ea89876bf`, 23 packages |

## Owner decisions of 22 September 2026 (D1–D4)

- **D1** — no public push until a publication act decides on the derivatives. Superseded by the publication act of V3-002, effective at the first push.
- **D2** — the report validator regenerates ledgers, shuffle counts and C0 provenance (implemented in `0dc69b5`).
- **D3** — the deviation of the CLI from §14.1 is recorded in the V3-001 note of the [Decision Log](02_DECISION_LOG.md).
- **D4** — the five figures are corrected in their defects and readability (implemented in `0dc69b5`).

The note on the `.DS_Store` that entered and left the deposit is now in V3-002, which records it as part of the act.

## Freeze perimeter

`_code_identity()` covers all of `src/hormathos`; the V2 evidence (`validation_run.context`) also binds `tests/*.py`, `conftest.py`, `pyproject.toml`, the configuration file, `uv.lock` and the manifest of the corpus used. After a validation is published, changing any of these prevents resuming and forces a new directory with V2 and V3 redone. The documents stay outside the perimeter and can be changed; `archive/` is outside the perimeter but bound to the bytes of `5f1ec06` by `test_every_archived_file_has_its_bytes_at_the_base`. The realignment and the rename changed the code identity **before** any V2 or V3 evidence was published: under `results/hexis31/` there are only the V1 runs.

## Running the history

The history runs only in a separate worktree: `git worktree add ../hexis-pre-realign archive/pre-realign`. A checkout of `5f1ec06` in the main copy would leave ignored files that switching back does not remove. A leftover `src/hexis/…/__pycache__/` would make `hexis` importable as a namespace package, and `test_the_package_is_hormathos_and_hexis_names_only_the_design` refuses it, rightly. The v2.1 outputs in `data/interim/` and `data/processed/` are corpus derivatives, and are therefore ignored.

## Planned sequence for V3–V5, not executed

Clean tracked tree (untracked `scripts/` and `docs/proposal/` are allowed), corpus `results/hexis31/v1`, new destinations under `results/hexis31/`:

```bash
uv sync --frozen
uv run python -m hormathos.pipeline.run_tree_validation --config config/default.yaml --corpus-dir results/hexis31/v1 --output-dir results/hexis31/<run>
uv run python -m hormathos.pipeline.run_descriptive --config config/default.yaml --corpus-dir results/hexis31/v1 --output-dir results/hexis31/<run> --seed 0
# §12.2: the same pair of commands in a distinct directory, same code
uv run python -m hormathos.pipeline.run_tree_validation --config config/default.yaml --corpus-dir results/hexis31/v1 --output-dir results/hexis31/<regen>
uv run python -m hormathos.pipeline.run_descriptive --config config/default.yaml --corpus-dir results/hexis31/v1 --output-dir results/hexis31/<regen> --seed 0
# V4, after the review of V3
uv run python -m hormathos.pipeline.run_descriptive --config config/default.yaml --corpus-dir results/hexis31/v1 --output-dir results/hexis31/<run> --resume
# V5
uv run python -m hormathos.pipeline.run_report --config config/default.yaml --corpus-dir results/hexis31/v1 --output-dir results/hexis31/<run> --regenerated-dir results/hexis31/<regen>
```

**Accepted cost (V3-003, R3).** Each published pair revalidates the V1 corpus before publication (`unchanged` in `run_descriptive`, 6.8 s per call measured on 23 September) and the whole run: about 5 minutes for the 42 pairs of V3 and about 55 minutes for the 490 of V4, plus the revalidation of the run, which grows with it (the comment in the code estimates about 2 hours in all). It stays as it is: after V3, a change would be a new code identity and V3 would be redone.

## Open obligations

1. **Full code review**: carried out on 23 September 2026, with two reviews; outcomes and fixes in the code-review section. The conformity check against the plan on the same day finds no substantive divergence; the two readings of V2 not yet declared in the active tree are now deviations 4 and 5 of V3-002.
2. **Licences**: decided in the publication act of V3-002, and only there. The publication venue cannot be determined: the act records the publication without a venue (E9).
3. **Research proposal 3.1 (§17.1)**: not deposited yet. Untracked local files exist in `docs/proposal/`, in Italian; tracking them is a separate decision, because they would enter the perimeter of the publication, and their English version comes with that decision (V3-003).
4. **Rename outside the repository (V3-003)**: the GitHub repository HEXIS becomes HORMATHOS, with its description and the local remote URL; then the local directory, with the virtual environment rebuilt. Each step needs the owner's explicit go.
5. **English companions (V3-003)**: non-normative translations of the deposited plan, of the V3-001 and V3-002 acts and of the other Italian texts of the deposit, in a separate tranche; the Italian originals govern.
6. **V3–V5**: technical trial, campaign, report and figures, in the order of §14.

Stop for review before V3.
