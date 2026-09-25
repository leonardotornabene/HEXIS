> **Non-normative companion translation; the Italian original governs** (V3-003, B2).
> Original: `docs/contracts/hexis-3.1/hexis-verifica/evidenze/audit_repository.md`, SHA-256 `7f5457b5c2459e5a45268e9b9cdca16e736b914361bba21eb3dcb6167f436109`.
> Translated on 2026-09-25. Structure, values and identifiers follow the original, including paths and file:line references; numbers use English notation. Any translator's note is marked *[Translator's note: …]* and changes nothing in the original.

# HEXIS — audit of the repository and proposed migration

**Verification of 15 September 2026.** Repository `/Users/leonardoTornabene/Projects/hexis`. Audit without changes to the tracked files, installations, acquisitions or real fits. No import from `candidates/`. The untracked script was only read. The operational package was extracted under `/private/tmp/hexis_repo_audit_package/HEXIS_v3_allegati`.

## 1. Actual evidence

| Check performed | Result |
|---|---|
| Local history and reference of the package | Observed HEAD `852644b`, branch `g1/pre-audit`; full reference of the plan `852644b6917790877c7b2ca5df2e76b17829d87c` |
| State before and after the checks | `?? scripts/`; no tracked difference. The repository is not globally clean |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -p no:cacheprovider -q` | **327 passed, 17 skipped in 10.34s**, exit 0 |
| Actual runtime | Python **3.12.13**, NumPy **2.5.1**, pandas 3.0.3, pyarrow 25.0.0, conllu 6.0.0, scipy 1.18.0, matplotlib 3.11.0, PyYAML 6.0.3, pytest 9.1.1 |
| Lock | 23 packages; the eight versions above coincide with `uv.lock`; SHA-256 `33db43b00bcb21ab12aedf6dcc4257764770bff0115dc0d1dfab6e5ea89876bf` |
| Operational attachments | All **33 hashes** in `SHA256SUMS.json` coincide; the Desktop plan and the included copy are byte-identical |
| Tracked results | Two pre-audit manifests, **7 artifacts in all**; all seven verified hashes coincide |
| CI | No tracked `.github/` workflow file; the verified tests are local |

The complete output of the suite was observed in the tool, not saved beforehand in a log file. The row above is its transcription, not a new execution log. The suite was not re-run to fabricate an attachment. The existing `conftest.py` deletes compiled caches of the tests; no tracked file turns out changed.

The 17 skips are scaffolds without operational assertions: 8 in `tests/test_context_tree.py`, 3 in `tests/test_scores.py`, 3 in `tests/test_tree_slices.py`, 3 in `tests/test_null_calibration.py`. The label-free signature is checked, but the behavioural invariance test of the scores is still a skip (`tests/test_scores.py:18`, `:57`). Green does not mean that a CTW or a scientific pipeline is available.

## 2. Authority and status of the gates

The repository continues to be v2.1: `AGENTS.md:8`, `docs/02_DECISION_LOG.md:3`, `config/default.yaml:16`. `docs/g1_ratification_record.md:3–14` ratifies exclusively the technical items 17–20 and 23–26, without deciding corpus, registry, alphabet or T*. G1 remains open (`docs/HANDOFF.md:151–156`), G2 has not been passed and O7 is not resolved.

The historical manifests correctly declare `mode: preaudit`, `status: PROVISIONAL`, code `fb53084b6d6a12a76639aeab098b81dd7368063c`, `dirty: false`; they are not attestations of v3 or of a scientific freeze. `docs/HANDOFF.md:181–213` distinguishes the attestation at `d024cd5` from the runs produced at `fb53084`.

The attached JSON remains `FINAL_PLAN_NOT_APPLIED`. The documentary lock says `READY_FOR_V0_DEPOSIT_NOT_A_GATE_CERTIFICATE`, with a null V0 deposit. A reduced revision must therefore produce a new contract before the implementation; it cannot present itself as already authorized maintenance of the v2.1 values. Retiring O7 from the new analysis means making it inapplicable, not resolving it retroactively. The exception for the earlier pilots is a statement in the package: I did not independently verify the original consent.

## 3. Technical differences that the reuse must respect

1. **Configuration.** `config.py:106–156` checks unknown and missing keys; `:159–221` validates some types used by G1. Calling it only a presence check is therefore imprecise. It remains insufficient for the model: the check performed accepted `d_max=True`, `d_max=-1`, `beta=NaN`, `k_min=-1`, `select='bogus'`. `config_hash` (`:224–227`) also produces a hash of JSON containing NaN. The new validation must reject non-finite values and wrong types/ranges before identifying the run.
2. **Seeds.** `config.py:230–232` uses XOR/CRC32; the attached contract uses `hexis-v3-rng-1` and distinct identities/purposes. They are not interchangeable.
3. **Mapping.** `alphabet.py:80–99` removes an unknown UPOS; verified with `NOTATAG`. It is the declared v2 contract, not a new bug of the reader: `conllu_reader.py:100` already rejects non-UD tags. The new public API must reject them at the boundary of the mapper too.
4. **Alphabet.** `alphabet.py:171–196` assigns IDs by decreasing frequency, while v3 prescribes lexicographic ordering. `freeze_alphabet` (`:199–215`) is really not implemented. A modified representation requires new inventories/hashes/counts, not the reuse of the numbers 106/112/12 as constants still true.
5. **Identity and coordinates.** `registry.py:12–42` has the five v2 regimes, not `PROSE_ALL`, `role` or `dependence_block`; it validates `part_order` but does not carry it into an operational ordering (`:274–293`). `run_audit.py:179–256` keeps prefix/sent_id and a `token_ord` recreated with `enumerate`, not all the raw IDs and ordinals required by v3. The `raw_token_id`, parts, source order and slots must be preserved before transforming the data.
6. **Boundaries.** `sequences.py:104–198` adds `#` to the alphabet and concatenates the sentences; it does not implement the context-only SEP/BOS of the new CTW. If `bound` is removed, retire this branch from the v3 path; keep the identity, order and duplicate checks of the sequences.
7. **Persistence.** `manifest.py:116–130` writes directly, also with `force`; it is not an atomic write with resumption. `run_audit.py:1115–1162` has reservation, collision checks and rollback on its own outputs, but writes the files directly (`:1122–1125`). Hashes, input snapshots and overwrite protection are reusable; v3 atomicity/resume/schema/cardinality are new work.
8. **Identification.** `run_audit.py:1070–1087` also puts the date into the run_id. The v3 contract excludes date/machine/path from the scientific identity and adds lock, data, registry and alphabets. `manifest.py:71–113` does not yet have that contract nor per-partition states.
9. **README.** `README.md:178–184` still calls the G1 audit a signature without a body: this is false with respect to `run_audit.py`. The README is to be redone only after deciding the new perimeter, distinguishing working tools, development results and final results.

## 4. Complete map of the application path

| File or group | Minimum future action |
|---|---|
| `src/hexis/conllu_reader.py` | Reuse parsing and validations; preserve the coordinates required in the next layer |
| `src/hexis/registry.py` | Reuse identity/merge/errors; update schema, roles and blocks; really consume `part_order` |
| `src/hexis/alphabet.py` | Reuse mapping/audit with the declared corrections; implement freeze and the new ID order |
| `src/hexis/sequences.py` | Reuse order/duplication checks and reset; add coordinates; retire the old `#` |
| `src/hexis/config.py` | Keep the YAML reader with duplicate rejection and hash; single strict v3 schema, new seed derivation |
| `src/hexis/manifest.py` | Extend only for an identified contract, atomic writing, content/key checks and resumption |
| `src/hexis/pipeline/run_audit.py` | Reuse reading, snapshot/hash, census and checks; remove the old scientific ratification machinery, T* and the dual language |
| `src/hexis/model/context_tree.py` | Replace the v2 dataclass/API and all the stubs with CTW; there is no old canonical implementation to refactor |
| `src/hexis/model/diagnostics.py` | Implement the prescribed diagnostics; today it is only a docstring |
| `src/hexis/protocols/sampling.py` | Implement; today it is only a docstring |
| `src/hexis/protocols/scores.py` | Replace the P1/P2/curve stubs with losses, G, Q and declared aggregation, keeping the core label-free |
| `src/hexis/viz/plots.py` | Implement only the figures still required; today it is only a docstring |
| `run_encode.py`, `run_tree_validation.py`, `run_sensitivity.py` | Implement; today all stubs |
| New `run_descriptive.py`, `run_report.py` | Orchestration of the pairs and single reporter; no framework or service needed |
| `run_confirmatory.py`, `run_null_calibration.py`, `run_reference.py`, `run_latin.py` | Retire from the application tree/CLI; they are stubs. Historical trace in Git, without keeping them as apparently usable commands |
| `src/hexis/model/lexicon.py`, `src/hexis/blocks.py` | Retire from the scientific path; the first is only a docstring, the second is working code for chunks, not dependency blocks |
| `src/hexis/stats/{permutation,bootstrap,holm}.py` | Keep working utilities and valid tests as history; no import in the v3 scientific path. They are 94/74/44 lines, not stubs |
| `src/hexis/**/__init__.py` | Keep the empty package files; no new abstractions |
| `config/default.yaml`, `config/registry_overrides.yaml` | Replace together with the contract: today the canonical registry contains only comments |
| `tests/test_conllu_reader.py`, alphabet/registry/sequences and corresponding `test_g1_*` | Keep compatible properties; explicitly replace incompatible v2 expectations |
| `tests/test_run_audit.py`, `tests/test_determinism.py` | Reuse integrity/inputs/collisions; adapt format, identity, schema and resume |
| `tests/test_context_tree.py`, `test_tree_slices.py`, `test_scores.py` | Bring independent proofs and executable assertions; retire only the selector/P1 properties really replaced |
| `tests/test_null_calibration.py`, `tests/test_blocks.py` | Retire from the v3 scientific gate; no need to implement an abandoned analysis |
| `tests/test_permutation.py`, `test_bootstrap_holm.py` | Keep with the utilities, without certifying v3 on them |
| `conftest.py`, `tests/test_g0_enforcement.py`, `test_g1_enforcement.py`, `test_gate_inventory_anchor.py`, `test_docs_consistency.py` | Rebuild a compact v3 inventory. Keep no-skip and real assertions; retire obsolete counters, signatures, taxonomies and ratifications, with an explicit map of the replacement |
| `tests/conftest.py`, `pyproject.toml`, `uv.lock` | Reuse fixtures/dependency stack; update description and markers. No new CTW dependency or NumPy change needed |
| MASTER_SPEC, Decision Log, roadmap, index, HANDOFF, README, AGENTS, CLAUDE | One consistent migration act and one new authoritative source; avoid divergent copies of the design |
| `docs/g1_*`, `docs/implementation/`, `docs/audit/`, old PDFs, `README_backup.md`, `README_v1_backup.md`, PDF proposal | Keep as history with an explicit status; remove them from the operational path and from the constraints of the new gate |
| `candidates/` | Quarantine unchanged, never import nor collect in pytest |
| `results/`, `data/raw/PROVENANCE.md`, ignored raw files | Keep history and provenance; no renaming of pre-audits/pilots into final results |
| `.gitignore`, `LICENSE`, licence section | Separate large working outputs from publishable results and declare which are distributed; do not let the new score directory end up entirely and automatically in Git |
| untracked `scripts/reacquire_raw_data.sh` | Preserve; verify/correct in a later assignment before any adoption |

## 5. Acquisition script: static reading, no execution

The 76-line script is not included in the Git snapshot. It cannot be qualified as an artifact attested at the reference commit.

- `:73–74` always acquires Greek **and Latin**: the second download does not serve the new scope.
- `:42–47` skips the checkout if the directory exists; it does not verify the HEAD commit in that case. The hashes validate the checked content, they do not attest HEAD.
- `:52–66` iterates over the files present: it does not compare the set of expected files with those found. If one of the three Greek files is missing and the others coincide, that missing file is not verified.
- `:31`, `:40` extract values from Markdown text with regular expressions and do not explicitly validate uniqueness/format of the extracted record.
- `:54–58` contains a handling of files without hash apparently based on `SKIP`, but with `set -euo pipefail` the failed `grep` search can already terminate the assignment `expected=...`. Do not describe it as a designed and tested rejection with a precise error.

Possible reuse: Greek only, exact set of the three expected names, precise hashes, error on missing/extra/ambiguous record; no automatic modification of a pre-existing clone. Preferably reuse the provenance verification primitives already present, without creating a second system of truth. None of these changes has been executed.

## 6. Output reduction and recommended governance

**Detailed C0, aggregated sensitivities is a sensible reduction**, provided that the new contract declares the lower granularity of the audit. Without probes, C0 contains 2,182,160 paired rows with the original counts; about 158 MiB is only the theoretical payload at 76 bytes/row, not measured disk/RAM. The numbers must be recomputed if the representation or the retention changes.

For each sensitivity keep at least complete identities of the pair, model/ledger hashes, number of targets and four sums of the losses per document and history band, plus aggregates sufficient to reconstruct exactly the diagnostics still required. For the conditional depth a generic mean is not enough: keep its numerators and denominators. Raw R1 counts, distributions and contributions remain necessary. Ledgers, coordinates and seeds allow the regeneration of a fit.

Figures and tables are reconstructed from these outputs; one **cannot** claim to recheck every sum of the sensitivities from per-position losses that are no longer kept. Detailed numerical verification of the sensitivities requires targeted regeneration of predetermined cases. Do not automatically omit the losses or the shuffled fits on the basis of the collapse observed in the pilot: it is not a universal identity of the protocol.

A short manifest can contain contract/commit/lock/inputs, status of the steps, proofs performed, list of files with hash/schema/cardinality and the set of scientific keys. Use the same reporter to verify them and reject the incomplete official result. Keep atomic writing, duplicate detection, hashes, denominators, slot joins, consistent resume and interruption/corruption tests. No framework of signed certificates is needed: the plan does not really require cryptographic signatures, and the attached certificates are simple records.

`report_contract.py:1–3` explicitly declares that the reference does **not** yet validate the schema of the scores, slots, numerical invariants and attestations of the pipeline. The about 40 lines of the function are a useful basis for the set comparison, not a complete, already integrated verification. Replacing four certificate objects with evidence rows in the same manifest does not authorize eliminating those checks.

I would not now optimize the number of CTW constructions by reusing deep trees and reweighting the priors: it can be correct after equivalence proofs, but the saving in computation does not address the dominant cost of integration and adds mutable state. First reduce questions/cells and outputs; always distinguish evaluated scientific models from computational reconstructions.

Licences: the repository distinguishes MIT code, CC BY 4.0 documents and future CC BY-NC-SA 4.0 statistics (`README.md:251–261`), while the raw files are CC BY-NC-SA 2.5 (`data/raw/PROVENANCE.md:35`). The plan speaks of the raw files but does not clearly assign a public/local destination to the new coordinates and per-position symbols. It must be declared in the migration, without automatically giving all files the licence of the code. This finding concerns the consistency of the contract and of the outputs, not a legal assessment of the derivation.

## 7. Existing attachable artifacts, without new executions

- This report: `/private/tmp/hexis_repo_audit.md`.
- Original package: `/Users/leonardoTornabene/Desktop/HEXIS_allegati_operativi_v3_2026-09-11.zip`.
- Verified copy: `/private/tmp/hexis_repo_audit_package/HEXIS_v3_allegati/`, in particular `SHA256SUMS.json`, `design_lock.json`, `package_validation.json`, `contract_validation.json`, `diagnostics_validation.json`, `scores_validation.json`, `report_validation.json`, `numpy_comparison.json`, `authorization_and_experiments.json`. They are **evidence earlier than the present audit**, not results just reproduced.
- Verified historical manifests: `results/logs/audit_preaudit_53f76d297774_1096e1d24582_fb53084b6d6a_2026-09-04/manifest.json` and `results/logs/audit_preaudit_53f76d297774_cbeffa78b04e_fb53084b6d6a_2026-09-04/manifest.json`; the corresponding files are in `results/tables/`.
- Documented historical test: `docs/HANDOFF.md:181–213`; runtime and command just verified are reported in §1 of this report.

**Conclusion:** the infrastructure base is concrete and passes its own tests. The model and the v3 pipeline have yet to be integrated. The minimum useful work is a reduced and consistent contract, selective reuse of the existing protections, verified CTW/protocol, detailed C0 outputs and sufficient aggregates elsewhere, a single reporter with complete checking. Nothing has been applied to the repository.
