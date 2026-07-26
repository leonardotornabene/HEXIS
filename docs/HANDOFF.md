# Overnight handoff — branch `phase1a/overnight-2026-07-25`

Autonomous Phase-1a run (authorized 2026-07-25, executed into 2026-07-26).
Scope P1–P6, reader RED-only. No master edit, no Decision Log edit, no merge,
no force-push. Branch tip: **`db1dbda`**. This file is the final commit.

**Suite at handoff:** `6 failed, 38 passed, 23 skipped`. The 6 failures are the
**intended reader RED** (P5); nothing was skipped/weakened to go green.
`uv run pytest` therefore exits non-zero by design — the correct overnight state.

---

## Per-unit log

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

### P1 detail — DEVIATIONS (flagged)
- Enforcement lives in **`./conftest.py` (repo root)**, not `tests/conftest.py`:
  `pytest_plugins` (needed to expose the `pytester` fixture) is honoured only in
  the root conftest. Runtime hooks work identically from either location. See Q1.
- Assertion-free enforcement is a **static AST** check (predicate + meta-test),
  proven by direct/meta unit tests; **skip and xpass** (session-runtime) are
  proven via `pytester` subprocess. A pytester run of the whole meta-test file
  would recurse, so the assertion-free case is not re-proven in a subprocess. See Q5.
- `tests/conftest.py` DOES exist now — it holds the P5 synthetic reader fixtures
  (fixtures are allowed in a non-root conftest; only `pytest_plugins` is not).

### P2 detail — conllu probe (full findings: `docs/probe_conllu.md`)
`conllu` **6.0.0**. `newdoc id` → metadata key `'newdoc id'` (with a space);
`token['id']` is `int` for syntactic-word rows and a `tuple` for MWT `(i,'-',j)`
/ empty `(i,'.',k)` rows; a **short row is silent** (reader must validate required
fields) while a **bad `id` raises** `conllu.exceptions.ParseException` (reader
must wrap). **No finding contradicts a D54(ii)–(iii) invariant.**

### P5 detail — reader RED (verbatim failures)
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

1. **Conftest location.** Enforcement is in `./conftest.py` (root), not
   `tests/conftest.py`, forced by the `pytester` `pytest_plugins` root rule. OK
   as-is, or split (pytest_plugins at root, hooks in `tests/conftest.py`)?

2. **Ratify the PROPOSED signatures** below (config, manifest, holm, bootstrap,
   blocks). These modules carried "Interface not specified in §6.2 … no invented
   contracts"; I implemented them under the P3/P4 authorization and chose the
   signatures. Nothing is on master; ratify or adjust before any merge.

3. **D54-A1 (awareness + confirm).** The branch base includes master commit
   `5aabc05` ("docs: align D54 governance and handoff references", 2026-07-25),
   added *after* my D54 commit, which deposited **D54-A1** and updated the reader
   docstring. D54-A1 makes `Iterator[conllu.TokenList]` the **binding public
   return type**. My P5 tests conform (they use the `TokenList` API: `.metadata`,
   `tok['id']`, iteration). Confirm this reading; no action was taken on it.

4. **Enforcement proof scope (minor).** Accept the static-AST proof of the
   assertion-free case (Q5/P1 deviation), or require a pytester subprocess too?

5. **KS uniformity (minor).** `test_null_synthetic_p_uniform` label-permutation
   arm has a fixed-seed KS p-value of 0.10 (> 0.05, deterministic). Acceptable, or
   raise the replication count for more headroom?

---

## PROPOSED readings (implemented under P3/P4 authorization, unapplied to master)

- **config.py**: `load_config(path=None)->dict`; `resolve_config(overrides=None,
  base=None)->dict` (non-mutating deep merge); `config_hash(cfg)->str` (SHA-256 of
  canonical sorted-key JSON); `derive_seed(analysis_id, global_seed)->int`
  (`global ^ crc32(id.utf-8)`, §6.3). Default config located by walking up from CWD.
- **manifest.py**: `sha256_file(path)->str`; `build_manifest(run_id,
  config_sha256, seed, artifacts, entry_point)->dict` (D46 fields + per-artifact
  sha256); `write_manifest(manifest, results_root, force=False)->Path`
  (`{root}/logs/{run_id}/manifest.json`, FileExistsError without force);
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

No `ASSUMPTIONS.md` ratification and no Decision Log edit were made.

---

## G0 status — NOT closed; what remains

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

```
git log --oneline master..HEAD      # 9 commits, listed below
```
```
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
Branch tip `db1dbda` (+ this HANDOFF commit). Nothing merged to master.
