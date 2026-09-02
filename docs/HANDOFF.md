# Overnight handoff — branch `phase1a/overnight-2026-07-25`

> **Post-review remediation prepared and owner-ratified 2026-07-27.**
> The historical overnight snapshot remains below. The remediation replaces the
> static assertion scan with runtime G0 enforcement, adds the missing D43/input
> domain tests, completes D46 input hashing and atomic overwrite refusal, expands
> the reader contract to 11 intentionally RED cases, and corrects this handoff.
> No Decision Log edit and no reader implementation.

**Pre-commit remediation verification:**
`uv run pytest -m g0 --strict-markers -p no:cacheprovider
--ignore=tests/test_conllu_reader.py` → `46 passed, 23 deselected`;
full suite → `11 failed, 46 passed, 23 skipped`. All 11 failures are confined
to the deliberately unimplemented reader contract. G0 remains open.

Autonomous Phase-1a run (authorized 2026-07-25, executed into 2026-07-26).
Scope P1–P6, reader RED-only. No master edit, no Decision Log edit, no merge,
no force-push. Pre-handoff implementation tip: **`db1dbda`**; historical
handoff commit: **`d82357b`**.

**Suite at handoff:** `6 failed, 38 passed, 23 skipped`. The 6 failures are the
**intended reader RED** (P5); nothing was skipped/weakened to go green.
`uv run pytest` therefore exits non-zero by design — the correct overnight state.

---

## Historical per-unit log at handoff

| Unit | Commit | Outcome |
|---|---|---|
| P1 — G0 enforcement | `7559f66` | GREEN — mechanized D45/D52(iii) |
| P2 — conllu probe | `b5ced54` | done — findings pinned, no D54 contradiction |
| P3a — permutation | `e9e4489` | GREEN — 7 tests |
| P3b — holm + bootstrap | `8e95466` | GREEN — 7 tests |
| P3c — blocks | `8a60ccd` | GREEN — 4 tests |
| P4a — config/seed/hash | `60bf14d` | GREEN — 4 tests |
| P4b — manifest/sidecar | `7794d76` | GREEN — 4 tests |
| P5 — reader (RED only) | `4505c34` | **RED (intended)** — 6 tests fail, impl deferred |
| P6 — corpus acquisition | `db1dbda` | done — grc/la Perseus r2.18 cloned, PROVENANCE committed |

### Per-file test counts at handoff

| file | result |
|---|---|
| test_g0_enforcement.py | 10 passed |
| test_scores.py | 2 passed, 3 skipped (G3 placeholders) |
| test_permutation.py | 7 passed |
| test_bootstrap_holm.py | 7 passed |
| test_blocks.py | 4 passed |
| test_determinism.py | 8 passed |
| **test_conllu_reader.py** | **6 failed (RED, intended)** |
| test_alphabet.py | 6 skipped (G0 coverage NOT yet implemented — see below) |
| test_context_tree.py / test_tree_slices.py / test_null_calibration.py | 14 skipped (G3, out of scope) |

### P1 detail — historical implementation (superseded by 2026-07-27 remediation)
- Enforcement lives in **`./conftest.py` (repo root)**, not `tests/conftest.py`:
  `pytest_plugins` (needed to expose the `pytester` fixture) is honoured only in
  the root conftest. Runtime hooks work identically from either location. See Q1.
- The original assertion-free enforcement was a static AST check. Review found
  bypasses for dead assertions, module/class markers, non-strict XPASS and
  collection-time skips. It is replaced in the remediation by runtime
  `pytest_assertion_pass` accounting plus subprocess regressions, including a
  warm-`.pyc` case.
- `tests/conftest.py` DOES exist now — it holds the P5 synthetic reader fixtures
  (fixtures are allowed in a non-root conftest; only `pytest_plugins` is not).

### P2 detail — conllu probe (full findings: `docs/probe_conllu.md`)
`conllu` **6.0.0**. `newdoc id` → metadata key `'newdoc id'` (with a space);
`token['id']` is `int` for syntactic-word rows and a `tuple` for MWT `(i,'-',j)`
/ empty `(i,'.',k)` rows; a **short row is silent** (reader must validate required
fields) while a **bad `id` raises** `conllu.exceptions.ParseException` (reader
must wrap). **No finding contradicts a D54(ii)–(iii) invariant.**

### P5 detail — historical reader RED (verbatim failures)
All six fail because `iter_sentences` raises `NotImplementedError` and
`ParseError` is undefined (feature missing):
```
FAILED test_conllu_reader.py::test_malformed_row_raises_parse_error_with_location
FAILED test_conllu_reader.py::test_missing_sent_id_raises_parse_error
FAILED test_conllu_reader.py::test_id_order_preserved
FAILED test_conllu_reader.py::test_mwt_range_and_empty_nodes_removed
FAILED test_conllu_reader.py::test_punct_token_yielded_unchanged
FAILED test_conllu_reader.py::test_newdoc_id_recoverable_from_metadata
```
GREEN-phase note for the implementer: conllu is silent on short rows, so the
reader must itself check ID/FORM/UPOS/HEAD/DEPREL presence AND wrap
`conllu.exceptions.ParseException` for bad-id rows (both paths → `ParseError`).

---

## Questions requiring your ruling (numbered)

1. **RESOLVED — conftest location.** Enforcement remains in `./conftest.py`:
   it is repository-wide and `pytest_plugins` for `pytester` must be declared at
   the root. `tests/conftest.py` remains fixture-only.

2. **RESOLVED — implementation readings ratified.** On 2026-07-27 the owner
   ratified the config, manifest, Holm, bootstrap and blocks signatures below,
   including the manifest's keyword-only `inputs=()`, non-collapsing
   caller-supplied path strings, and fail-loud behavior when Git state is
   unavailable.

3. **RESOLVED — D54-A1 alignment.** The branch base includes master commit
   `5aabc05` ("docs: align D54 governance and handoff references", 2026-07-25),
   added *after* my D54 commit, which deposited **D54-A1** and updated the reader
   docstring. D54-A1 makes `Iterator[conllu.TokenList]` the **binding public
   return type**. The expanded P5 tests now assert `TokenList` explicitly and
   preserve all D54(ii)–(iv) responsibilities. No Decision Log action is needed.

4. **RESOLVED — enforcement proof scope.** Static proof removed. Ten `pytester`
   subprocess cases exercise the canonical `-m g0 --strict-markers` path.

5. **KS uniformity (minor).** `test_null_synthetic_p_uniform` label-permutation
   arm has a fixed-seed KS p-value of 0.10 (> 0.05, deterministic). Acceptable, or
   raise the replication count for more headroom?

---

## RATIFIED implementation readings (unapplied to master)

- **config.py**: `load_config(path=None)->dict`; `resolve_config(overrides=None,
  base=None)->dict` (non-mutating deep merge); `config_hash(cfg)->str` (SHA-256 of
  canonical sorted-key JSON); `derive_seed(analysis_id, global_seed)->int`
  (`global ^ crc32(id.utf-8)`, §6.3). Default config located by walking up from CWD.
- **manifest.py**: `sha256_file(path)->str`; `build_manifest(run_id,
  config_sha256, seed, artifacts, entry_point, *, inputs=())->dict` (D46 fields
  + SHA-256 for every input and artifact, with non-collapsing paths);
  `write_manifest(manifest, results_root, force=False)->Path`
  (`{root}/logs/{run_id}/manifest.json`, atomic FileExistsError without force);
  `sidecar(run_id, sha256, entry_point)->dict`;
  `write_sidecar(artifact_path, run_id, entry_point, force=False)->Path`.
- **holm.py**: `holm_bonferroni(pvalues: Mapping[str,float], alpha=0.05)
  -> HolmResult(order, adjusted, reject)` — step-down, monotone adjusted p.
- **bootstrap.py**: `document_bootstrap(values, labels, B=2000, seed=0,
  alpha=0.05, statistic=None) -> BootResult(observed, replicates, ci)` — within-
  group whole-document resampling, percentile CI, `default_rng(seed)`.
- **blocks.py**: `make_blocks(doc, n_block=1000, min_frac=0.5)` where `doc` is one
  document's sentences (each a sequence of symbols) and the return is a list of
  blocks (each a list of whole sentences). "Never spans documents" is realized by
  per-document invocation.
- **permutation.py** (PermResult signature was already in §6.2; conventions
  chosen): label-perm statistic = mean(group sorted-first) − mean(sorted-second)
  over C(n,k); sign-flip = mean(sign·values) over 2^n; two-sided p is centered at
  the null mean (= 0 for both here). No confirmatory P1 wiring (O7/D44).

The owner ratification is recorded here. No `ASSUMPTIONS.md` or Decision Log
edit was made.

---

## G0 status — CLOSED AFTER PRE-MERGE REVIEW 2026-08-14

> The first pre-merge review reopened G0 after finding three uncovered contract
> defects: out-of-order integer token IDs were accepted; registry overrides could
> not merge prefixes; and `n_tokens_raw` had no ratified meaning. The reader fix
> is commit `73f70e3`; the owner ratified both registry readings on 2026-08-14 and
> their tests-first implementation is commit `eea3b3e`. A second independent
> review found no Critical or Important issue and confirmed that every previous
> blocker was resolved.
>
> **Attestation of record — commit
> `8fd72becbc4359dd6c7af49b98d0897e4f0f9ffd`, working tree clean:**
>
> ```
> uv run pytest -m g0 --strict-markers -q  →  144 passed, 112 deselected  (exit 0)
> uv run pytest -m g1 --strict-markers -q  →   95 passed, 161 deselected  (exit 0)
> uv run pytest -q                         →  239 passed,  17 skipped     (exit 0)
> uv lock --check                          →  Resolved 23 packages        (clean)
> ```
>
> Re-attested 2026-09-02. The delta from `1271d57` is twelve commits and no test:
> the previous attestation itself (`1680d3a`), the two pre-audit artifact sets
> under `results/` (`84a9319`, `dc4cf43`), D55's revision and the opening of the
> ratification record (`61d6496`, `15352a5`), and the post-review pass —
> `eec419f` and `d8b8052` (D55's two false `git.dirty: true` claims, its
> untracked-vs-ignored error, the stale 142/17 in its commit recipe, and the
> template/live `CLAUDE.md` drift), `729679f` and `8fd72be` (the open-finding
> pointer into `00`/`03`/`04` and into `README.md`), `4766f35` (one overclaiming
> docstring in `sequences.py`) and the two intermediate re-attestations this block
> replaces (`025f236`, `22c6c4f`).
> **Every count is unchanged** — prose and artifacts only, no test and no library
> behaviour — and it is re-run rather than transcribed because a figure carried
> over untested is a figure nobody measured. Superseded attestations, same counts,
> kept for the trail: `d8b805251b261d116251fed31c82bfc2ad5f5610`,
> `4766f355a0dfbf09ec70d7b07ba99b81d62e8e43` and
> `1271d57e2c1b112d46f59e27f56f5bdd7f0a8c68`.
>
> Earlier still, and the one that did move: commit
> `180e05cf83985be08a5d4dd27ba843a680d826a8` at 142 passed / 17 deselected (G0)
> and 142 / 17 (full suite). **G0 itself did not reopen.** The selection moved
> 142 → 144 because convention 12 of the D55 proposal (unknown override fields
> rejected) changes `registry.build_registry`, whose mandatory-coverage area is
> "registry construction and validation" in the D52(ii) inventory: testing it only
> in an unmarked file would have left `-m g0` green while the rule went
> unexercised. The suite moved 142 → 239 because this branch adds the G1 audit
> tests, which carry `g1` and never `g0`.
>
> This is the **only** place the counts are recorded; README, the roadmap and the
> index point here instead of repeating them. Any test added later moves the
> number, and a figure transcribed into four documents goes stale silently — as
> it did at 124, when PR #2 added seven registry tests and the hardening pass
> below added eleven more. Re-attesting means rerunning the commands on a clean
> tree and replacing the block above together with its commit.
>
> The 17 are G3 scaffolds (`context_tree`, `tree_slices`, `null_calibration`,
> the G3 scoring-boundary cases); none carries a gate marker. D52(i)'s three
> conditions hold: environment locked (Python 3.12.13, `uv lock --check` clean,
> 23 packages); every G0 test passes with an executed assertion; the D45/D46
> deterministic infrastructure is verified.
>
> **`-m g1` is new here** (D55 §xiv, convention 13; owner-authorized 2026-08-17,
> PROPOSED with the rest of the package). It puts the G1 audit tests under the
> same enforcement as G0 — `conftest.GATE_MARKERS` — because they previously ran
> only inside the full suite, where one skipped test moves `239 passed / 17
> skipped` to `238 / 18` and stays green: the failure mode D52(iii) forbids for G0
> and left open for G1. Its first run found nineteen G1 tests passing while
> executing no Python assert, relying on `pytest.raises(match=…)` alone; each now
> asserts on the exception's content. Mutation-verified in both directions.
> It attests no gate: **G1 is not closed** — nothing is frozen, the registry is
> unratified, and the evidence for its ratification is in
> `docs/g1_D55_proposal.md` and `docs/g1_registry_proposal.md` (both PROPOSED).
>
> Two gaps in the enforcement were closed in the process, each one level finer
> than the last. First: `-m g0` selects only marked tests, so an incomplete
> marker set exited 0 — the gate command reported a green G0 the moment the
> reader went green, with three mandatory areas at zero coverage.
> `tests/test_g0_enforcement.py` now also asserts the D52(ii) inventory. Second
> (post-merge review, commits `d015b98`–`180e05c`): that inventory guarded areas
> at *file* granularity while its keys name behaviours, so deleting every P-BOUND
> test kept the gate green — and, symmetrically, §7's five-label taxonomy row was
> covered by a subset assertion that two labels satisfied. The inventory now
> requires named tests by exact name for every mandatory behaviour, and the
> canonical gate compares them with the module-level G0 items actually collected
> by the current pytest session. The AST scanner remains only in isolated
> synthetic probes; it is not closure evidence.
> `registry.REGIME_LABELS` is pinned by equality with all five labels exercised
> through `build_registry`. A green gate now implies that every mandatory area is
> represented, that its named behaviours are still selected by `-m g0`, and that
> those tests really assert.
>
> Still assigned to G1: `sent_ord`, the empirical Greek prefix granularity and
> the O2/O8 decision about which prefixes to merge. The mechanism itself and the
> `n_tokens_raw` denominator are now ratified. The KS-headroom question below
> (Q5) also remains open.
>
> **State of those items at this attestation.** The G1 enumeration has been run
> on the pinned data: the Greek prefix granularity is empirical (18 raw prefixes,
> 17 canonical if Athenaeus 12+13 merge) and **O2 is resolved at document level**
> — one Hymn prefix, no duplication — while **O8 remains open** and `sent_ord` is
> proposed, not implemented. The enumeration also contradicts §2.3: Greek
> PROSE_CLASS holds 2 documents, not 6, so 𝔻 is 7 (or 11 only under the union
> option) and the constants of D21/D24/D33/D43 do not describe this corpus. That
> finding, both options and every recomputed constant are in
> `docs/g1_D55_proposal.md` — **PROPOSED, applied to nothing**.

### Historical: what remained at the overnight handoff

Tonight delivered the enforcement mechanics + these mandatory-coverage areas
(D52(ii)): permutation, sign-flip, Holm, bootstrap, blocks, seed derivation,
config canonicalization+hash, central run-manifest, minimal sidecar, overwrite
refusal. **Still open in the G0 set:**

- **conllu_reader** — tests RED (P5); implementation is the next GREEN step
  (RED checkpoint honoured; not written tonight).
- **total alphabet mapping (§3.4)** — `test_alphabet.py` placeholders still
  `@SKIP`; `alphabet.py` is a stub. Not in tonight's scope.
- **registry build + validation** — `test_registry.py` does not exist yet;
  `registry.py` is a stub. Not in tonight's scope.
- **sequences P-RESET / P-BOUND (§3.5, D52(x))** — `test_sequences.py` does not
  exist yet; `sequences.py` is a stub. Not in tonight's scope.

The `@pytest.mark.g0` set is therefore still a subset, exactly as D52(ii)'s marker
description ("incomplete until all mandatory coverage is implemented") anticipates.

## Skipped / not done (with reasons)
- Reader implementation — deliberate RED-only (your checkpoint).
- alphabet / registry / sequences G0 modules — outside the P1–P6 priority list.
- G3 suites (context_tree, tree_slices, scores byte-identity, null_calibration)
  — out of scope; remain skipped.
- No mirror was improvised for P6 (network was available, so both repos were
  cloned at r2.18 directly).

---

## Reproduce

At the historical handoff:

```
git log --oneline master..d82357b      # 10 commits, listed below
```
```
d82357b docs(handoff): overnight Phase-1a run report (P1-P6)
db1dbda data(provenance): record UD grc/la Perseus r2.18 acquisition (P6)
4505c34 test(reader): RED-only G0 contract for iter_sentences/ParseError (D54/D54-A1)
7794d76 feat(manifest): central run manifest, minimal sidecar, overwrite refusal (G0)
60bf14d feat(config): seed derivation + canonical config hashing (G0)
8a60ccd feat(blocks): sentence-aligned block segmentation, descriptive only (G0)
8e95466 feat(stats): Holm step-down and hierarchical document bootstrap (G0)
e9e4489 feat(stats): exact label-permutation and sign-flip utilities (G0)
b5ced54 docs(probe): pin conllu 6.0.0 runtime facts for the reader contract
7559f66 chore(g0): mechanize the D45/D52(iii) G0 enforcement criterion
```
Historical branch tip `d82357b`. The owner ratified the implementation readings
and authorized the remediation commit on 2026-07-27. Nothing merged to master.
