# HORMATHOS handoff — current state (design HEXIS 3.1)

**V0–V3 completed; V4–V5 not attested; real fits only at seed 0 (V3).** Publication of 2026-09-23: the push of the branch `codex/hexis31-realign` at `2ebb3464b871c1f831d0608edba052ccb4b92be9` and of the tags `archive/pre-realign` and `archive/v2.1`; then the merge into `master` (`73df64d`, a merge commit with neither squash nor rebase) and the deletion of the remote branches `g1/pre-audit` (V3-002, E5) and `codex/hexis31-realign`, whose content is in `master`. At that point the active branch was `master`; the realignment started from `5f1ec06afa192c8d0f006d7f39cdb97df72c2983`. On the same day the project was named HORMATHOS (V3-003), published at `c738c73`, and the GitHub repository became `leonardotornabene/HORMATHOS`; the old address redirects. The detailed chronology of the earlier tranches is not repeated here: it is in the Git history and, in its last pre-realignment form, in [archive/docs/HANDOFF.md](../archive/docs/HANDOFF.md).

## Review of V3 and re-attestation — 24 September 2026 (V3-005)

Three moments, in order: the V3 technical trial of 24 September on `01d1883` (next section, historical evidence, not resumed); its review; the re-attestation below.

The review of V3 found no defect in its results; the details are in V3-005. Three fixes of `2a16a81` had no test that failed without them: the coordinate-order check with a categorical `doc_id` (R4), the rollback that keeps every artifact when the manifest is unreadable (R5), and the `samefile` refusal of a raw alias that `resolve()` misses, exercised only on case-insensitive file systems and closed by `assert True` (R6). Each now has its own test, and the README test that pinned the V2-phase status sentence is replaced by phase-independent properties. `src/hormathos` does not change, so the run ID stays `1563452a…`; the tests do change, so the V2 context of the directories of 24 September no longer matches and they are not resumed. V2 and seed 0 are rerun in `results/hexis31/v3-seed0-r4-r6` and `results/hexis31/v3-seed0-r4-r6-regeneration`.

The comparator's scope (R7) is fixed in V3-005 (d). One residue stays without action (R9): `load_corpus` validates and reads a private copy of the corpus, but `evidence()` and `context()` hash the corpus manifest by rereading the original directory; a change in that window cannot yield a silent wrong result, because `run_contract` detects it at the report.

**Re-attestation.** The suite of `602ff90` first, then the runs on the same commit, with a clean tracked tree (untracked `scripts/` and `docs/proposal/` preserved), Python 3.12.13 through `uv run --no-sync` with `UV_NO_CACHE=1`, `uv.lock` SHA-256 `33db43b0…`, corpus `results/hexis31/v1`. Commands and logs: `results/hexis31/v3-seed0-r4-r6-logs/` (01–06 runs, 07–12 checks, `commands.txt`).

```text
uv run --frozen pytest -q -p no:cacheprovider
429 passed in 197.20s (0:03:17)

uv run --frozen pytest --collect-only -q          429 tests collected
uv run --frozen pytest -m v31 --collect-only -q   429 tests collected
uv run --frozen pytest . --collect-only -q        429 tests collected
uv lock --check                                   Resolved 23 packages
```

The three collections have the same 429 node IDs and none under `archive/`; the count rises from 426 by the three tests of V3-005. Eighteen mutants, numbered afresh N01–N18 without claiming the identity of the lost pre-V3 mutants, each revert or disable one fix of `2a16a81` in a temporary copy of `602ff90`; for each, the target tests pass on the unmutated copy and fail on the mutant, rerun one by one: 18 killed, none survived. They include R4 (N01), R5 (N03) and R6 (N04), each killed by its own new test. The script and its log are outside the repository, in the verification workspace `hexis-verifica-riallineamento/revisione_v3_2026-09-24/`.

`results/hexis31/v3-seed0-r4-r6`: `run_tree_validation` (34 synthetic cases, 429 acceptance cases; 249.6 s wall), then `run_descriptive --seed 0` in the three invocations of 24 September — `--cell C0` (88.6 s), `--cell D12 --resume` (102.6 s), `--cell all --resume` (354.9 s). Manifest SHA-256 `b9c94d7a5dd46befcd50eef53056dd88baec0d7dccbf6cd49f74275d18efb8cf`, run ID `1563452ad4b644d1ec8ea00f38300192f95fad8c4d34761a570a22f5b6a78855`, stages `validation` and `descriptive`, evidence V0–V3, 42 pair and 84 model keys at seed 0, seven pairs per cell. The manifest records the last invocation (56 new fits, 14 reused partitions, 28 published); as on 24 September, the C0 and D12 invocations are documented only by their commands and times in the logs. Resources over the 84 models: fit 61.07 s, evaluation 45.84 s, maximum peak RSS 1 418 235 904 bytes (D12); directory 29 366 010 bytes.

`results/hexis31/v3-seed0-r4-r6-regeneration`, separately executed with the same code: `run_tree_validation` (247.9 s), then one `run_descriptive --seed 0` (551.5 s). Manifest SHA-256 `eba21d35bd6dd8a4086f87b39eaaa47e44fbc50e7a2a9221f3b2462c40694892`, same run ID; fit 62.90 s, evaluation 48.35 s, peak RSS 1 554 911 232 bytes (D12). Its verification in the report remains a V5 obligation.

Checks, each with its own log:

- `validate_run` accepts both manifests; `verify_evidence` with the current context and `verify_technical` pass on both (V3 over 70 artifacts: 42 pairs, 21 ledgers, 7 C0 position files).
- `compare_regeneration(v3-seed0-r4-r6, v3-seed0-r4-r6-regeneration)`: 70 of 70 artifacts byte-identical.
- `compare_regeneration(v3-seed0, v3-seed0-r4-r6)`: 70 of 70 byte-identical. This is an identity check across the two test contexts, same code and run ID, not §12.2 evidence.
- A recomputation from the deposited contract that does not import `hormathos` (`indep_check.py`, rebuilt, summing over sorted keys) finds 0 problems in both directories. It checks the §12.2 fixture, the eligible totals 109 108 / 109 716 / 109 108 by block and variant, the 21 ledgers row by row with their subseeds, training and fragment metrics, shuffle counts, root counts and the root losses q₀ of both arms, the 109 108 C0 position rows with the reconstruction of all four loss sums, and zero probe evaluations. Its first pass flagged every ledger hash, because it hashed the file bytes; the hash is the SHA-256 of the canonical JSON of the rows (deviation 4 of V3-002). The check was corrected and rerun; the first log is kept (`10a`).
- The preconditions of `run_descriptive --resume` for V4 pass on a copy of `v3-seed0-r4-r6`; on a copy of `v3-seed0`, `verify_evidence` refuses the run, because the recorded test context no longer matches (`tests/test_v31_docs.py`).
- `v1`, `v2-pre-v3-audit-2026-09-24`, `v3-seed0` and `v3-seed0-regeneration` keep their manifest SHA-256.

Observation without contrasts (R11): G_R = CE₀ᴿ − CE_CTWᴿ, summed over the document and band records in sorted order, is 0 in the seven C0 folds and about 2.0363×10⁻⁵ bit/target for `upos` held out on PLUTARCH (§7: an observed result, not an identity). Forecast, not measured (R10): V4, with 448 new pairs, about 2–2.5 hours and about 0.3 GB of disk.

Stop for review before V4.

## V3 technical trial — 24 September 2026 (historical, not resumed)

Measured on `01d1883` with a clean tracked tree (untracked `scripts/` and `docs/proposal/` preserved), Python 3.12.13 through `uv run --no-sync` with `UV_NO_CACHE=1`, `uv.lock` SHA-256 `33db43b0…` unchanged, corpus `results/hexis31/v1`. Commands and logs are in `results/hexis31/v3-seed0-logs/`.

`results/hexis31/v3-seed0`: `run_tree_validation` (34 synthetic cases, 426 acceptance cases), then `run_descriptive --seed 0` in three invocations — `--cell C0`, `--cell D12 --resume`, `--cell all --resume`. `validate_run` accepts the manifest (SHA-256 `b48bd60bdebbc20a1dec6b57a5dc10c6a096dd6a9f0afe1d8e38f35c29af28bd`); the run ID `1563452ad4b644d1ec8ea00f38300192f95fad8c4d34761a570a22f5b6a78855` equals that of the V2 evidence in `v2-pre-v3-audit-2026-09-24`, so the code identity did not change. Stages `validation` and `descriptive`, evidence V0–V3, 42 pair and 84 model keys, all at seed 0, seven pairs in each of C0, D12, a_total1, oth, q_half and upos. `verify_technical` recomputes the recorded V3 over its 70 artifacts (42 pairs, 21 ledgers, 7 C0 position files).

Resources over the 84 model measurements: fit 61.26 s, evaluation 43.58 s, maximum peak RSS 1 471 389 696 bytes (D12); directory 29 365 072 bytes. Wall time: validation 249.6 s; descriptive 88.2 s (C0), 103.9 s (D12), 349.1 s (the other 28 pairs). `new_model_fits` counts one invocation (14, 14, 56).

The manifest keeps in `metadata` and `checks` only the last of the three invocations (`selection: all`, `resume: true`); the C0 and D12 invocations are documented only by the local logs in `v3-seed0-logs/`, which Git ignores, while the per-model resource list accumulates and is complete (R8). Logs 01–07 capture the pipeline commands and the checks run through the package; `08-independent-check.py` imports `hormathos` and applies its validators, so it is a recomputation through the package, not an independent one.

§12.2 regeneration, separately executed with the same code: `results/hexis31/v3-seed0-regeneration`, `run_tree_validation` then one `run_descriptive --seed 0` (239.7 s and 694.6 s wall). Manifest SHA-256 `3486804df9732ff36770b8dc28ea37b7e0ae5850bdca101dbc8fd22256b87552`, same run ID; `compare_regeneration` finds all 70 artifacts byte-identical. Fit 60.71 s, evaluation 43.34 s, peak RSS 1 500 229 632 bytes. Its verification in the report remains a V5 obligation.

Stop for review before V4.

## Pre-V3 audit closure — 24 September 2026 (V3-004)

Commit `2a16a81` on `pre-v3-audit-closure` closes the findings of the pre-V3 audit before the code freeze. `uv run --python 3.12 --no-sync pytest -q` passed **426 tests** in 212.30 seconds. `pytest --collect-only -q` and `pytest -m v31 --collect-only -q` collected the same 426 node IDs; there were no skips or xfails. `uv lock --check` resolved 23 packages without changing `uv.lock`. A separate `run_audit`/`run_encode` invocation with this final source tree regenerated all nine V1 artifacts byte for byte against `results/hexis31/v1`.

The new V2 evidence is in `results/hexis31/v2-pre-v3-audit-2026-09-24`. `scientific_run.validate_run` accepted its manifest (SHA-256 `98b8341dc7e8a2be85c1abeb35ba11ffb428b9da707ea57ba7528b31fd4e7b8f`), run ID `1563452ad4b644d1ec8ea00f38300192f95fad8c4d34761a570a22f5b6a78855`. It records 34 synthetic battery cases, 426 acceptance cases, only the `validation` stage, and empty pair/model keys. No real fit ran. Stop for review before V3.

**Findings, reconstructed (R1).** The original list of findings is lost, and the commit message of `2a16a81` has no body. The review of V3 recalled fifteen findings — ten code fixes, two procedural, the tolerance fixed by V3-004, gaps in the tests and one reasoned rejection on `peak_rss` — but neither their numbering nor that rejection survives. What follows is reconstructed from the diff of `2a16a81` and its tests; it is not certified to match the original one to one, and no record shows that each test failed before its fix.

| Change in `2a16a81` | Tests |
|---|---|
| A failed manifest replacement no longer removes artifacts that a committed manifest lists (`rollback_uncommitted`, corpus and scientific runs) | `test_manifest_commit_exception_preserves_the_published_state`, `test_scientific_manifest_commit_exception_keeps_a_valid_fixture_run`; unreadable-manifest branch: `test_rollback_keeps_artifacts_when_the_manifest_is_unreadable` (V3-005) |
| Extra files in a run or in the deposit are named in the error | `test_extra_ds_store_is_named_in_v1_and_deposit` |
| Plot spreads accept a mean up to one rounding unit outside min/max and refuse anything beyond | `test_spread_accepts_one_rounding_unit_only` |
| Regeneration tolerance absolute, scaled only for loss sums (V3-004) | `test_regeneration_tolerance_is_absolute_and_scales_only_loss_sums` |
| Parquet numeric dtypes regenerated exactly | `test_regeneration_rejects_changed_integer_identity_in_parquet` |
| An alias of the raw data is refused through `samefile` | `test_raw_alias_is_rejected_even_when_case_differs`; `test_raw_alias_is_rejected_even_when_resolve_misses_it` (V3-005) |
| `--fixture` cannot reuse `spec_version` HEXIS-3.1 | `test_fixture_cannot_reuse_the_deposited_spec_version` |
| A document in two blocks is refused before training | `test_sample_fold_rejects_a_document_in_two_blocks_before_training` |
| `load_corpus` reads the private copy it validated | `test_load_corpus_reads_the_validated_private_copy` |
| Sentence and coordinate order checked on string `doc_id` | `test_category_order_cannot_hide_swapped_document_order`; `test_category_order_cannot_hide_swapped_coordinate_order` (V3-005) |
| Every collection skip fails the gate, with or without a gate marker | `test_collection_skip_without_marker_fails_the_gate`, `test_nested_conftest_collection_skip_fails_the_gate` |
| Reviewed case counts pinned for every parametrized test | `test_parameterized_case_counts_match_the_reviewed_inventory`, `test_parameterized_case_gate_catches_one_removed_case` |
| Procedural: a copied directory is not a regeneration; recovery after SIGTERM/SIGHUP | `compare_regeneration` records `comparison_scope` and `independent_execution` (`test_seed_zero_regeneration_is_compared_and_recorded_by_the_report`); runbook in the V3–V5 sequence |

Three tests of `2a16a81` guard properties that its diff does not change in `src`: `test_parser_consumes_the_copied_v1_input`, `test_descriptive_context_change_cannot_publish_a_pair` and `test_acceptance_rejects_junit_failure_even_with_zero_process_status`.

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

`_code_identity()` covers all of `src/hormathos`; the V2 evidence (`validation_run.context`) also binds `tests/*.py`, `conftest.py`, `pyproject.toml`, the configuration file, `uv.lock` and the manifest of the corpus used. After a validation is published, changing any of these prevents resuming and forces a new directory with V2 and V3 redone. The documents stay outside the perimeter and can be changed; `archive/` is outside the perimeter but bound to the bytes of `5f1ec06` by `test_every_archived_file_has_its_bytes_at_the_base`. The realignment and the rename changed the code identity **before** any V2 or V3 evidence was published: at that time, under `results/hexis31/` there were only the V1 runs. The tests added by V3-005 are such a change after publication: the directories of 24 September are not resumed, and V2 and seed 0 are rerun in new ones.

## Running the history

The history runs only in a separate worktree: `git worktree add ../hexis-pre-realign archive/pre-realign`. A checkout of `5f1ec06` in the main copy would leave ignored files that switching back does not remove. A leftover `src/hexis/…/__pycache__/` would make `hexis` importable as a namespace package, and `test_the_package_is_hormathos_and_hexis_names_only_the_design` refuses it, rightly. The v2.1 outputs in `data/interim/` and `data/processed/` are corpus derivatives, and are therefore ignored.

## Sequence for V3–V5; V3 executed on 24 September 2026, rerun under V3-005

Clean tracked tree (untracked `scripts/` and `docs/proposal/` are allowed), corpus `results/hexis31/v1`, new destinations under `results/hexis31/`. Under V3-005, `<run>` is `results/hexis31/v3-seed0-r4-r6` and `<regen>` is `results/hexis31/v3-seed0-r4-r6-regeneration`, both executed on 24 September 2026; V4 and V5 use them, never the directories of the first trial:

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

**§12.2 evidence.** The comparison checks run identity, keys and values within V3-004's absolute tolerance. Two local directories do not establish independent execution: `cp -R` is indistinguishable from a genuine rerun by inspection of those directories. Record the separately executed commands and their logs as procedural campaign evidence.

**Recovery after SIGTERM/SIGHUP.** First confirm the process has exited (`ps -p <pid>`). Compare the directory entries with `manifest.json`'s artifact list; keep every artifact listed by a valid manifest. Remove only `.lock`, `.stage-*`, and artifacts absent from that list, after identifying them as interrupted output. Then run `scientific_run.validate_run` on the directory; use `--resume` only if it validates. If no valid manifest remains, reconcile the directory manually before starting a new run. Do not remove a listed artifact merely because the process reported an exception after publication.

**Accepted cost (V3-003, R3).** Each published pair revalidates the V1 corpus before publication (`unchanged` in `run_descriptive`, 6.8 s per call measured on 23 September) and the whole run: about 5 minutes for the 42 pairs of V3 and about 55 minutes for the 490 of V4, plus the revalidation of the run, which grows with it (the comment in the code estimates about 2 hours in all). It stays as it is: after V3, a change would be a new code identity and V3 would be redone.

## Open obligations

1. **Full code review**: carried out on 23 September 2026, with two reviews; outcomes and fixes in the code-review section. The conformity check against the plan on the same day finds no substantive divergence; the two readings of V2 not yet declared in the active tree are now deviations 4 and 5 of V3-002.
2. **Licences**: decided in the publication act of V3-002, and only there. The publication venue cannot be determined: the act records the publication without a venue (E9).
3. **Research proposal 3.1 (§17.1)**: not deposited yet. Untracked local files exist in `docs/proposal/`, in Italian; tracking them is a separate decision, because they would enter the perimeter of the publication, and their English version comes with that decision (V3-003).
4. **Rename outside the repository (V3-003)**: done on 23 September 2026 — the GitHub repository is `leonardotornabene/HORMATHOS`, with the description "Project HORMATHOS", and `origin` points to it.
5. **English companions (V3-003)**: non-normative translations of the deposited plan, of the V3-001 and V3-002 acts and of the other Italian texts of the deposit, in a separate tranche; the Italian originals govern.
6. **V4–V5**: campaign, report and figures, in the order of §14; V3 executed on 24 September 2026, reviewed, and re-attested under V3-005 in `results/hexis31/v3-seed0-r4-r6`.

Stop for review before V4.
