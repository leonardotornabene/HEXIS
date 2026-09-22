# PROPOSTA — Spec amendments mandated by D52

**Status: EXECUTED / ARCHIVED.** The two replacements below were applied to
`docs/01_MASTER_SPEC.md` in commit `97c1ce9` (2026-07-23). This file is preserved as
the pre-application audit record; do not reapply it. The same commit also documented
the D52(vi) sampling-ledger format in §3.7.

**How to read.** Each site is a three-column table — **anchor** (exact current text),
**proposed replacement**, **D52 clause that mandates it**. Where the anchor or the
replacement is multi-line (a fixed-width code block, or a markdown table row that itself
contains `|`), the cell references a labelled verbatim block (`A1`, `B1`, …) reproduced
below the table. This indirection is deliberate: §6.2 is a fixed-width block restored
deterministically under D48, so its anchor MUST be lifted byte-exactly for find-and-replace
— reproducing it inside a table cell would require inserting `<br>`/escapes and would
normalize characters the mandate forbids. The verbatim blocks below are byte-exact; the
tables carry the mapping.

---

## Site 1 — §6.2, the `pooled_scores` contract

Scope: the anchor is a **sub-region** of the existing `# protocols/scores.py` code block in
§6.2 (lines defining `pooled_scores`). The neighbouring lines in that block —
`delta_ce_scores(...)` and `learning_curves(...)` — are **unchanged** and are not part of
this edit.

| Anchor (current §6.2 text, byte-exact) | Proposed replacement | D52 clause |
| --- | --- | --- |
| block **A1** below | block **B1** below | **D52(v)** — three-function form (`pooled_score_core` / `annotate_scores` / `pooled_scores` as thin composition) + canonical score column order; **D52(vi)** — sampling-ledger contract; **D52(vii)–(viii)** — label-derived columns move to the annotation stage, outside the byte-identity guarantee |

**A1 — anchor (reproduce verbatim; byte-exact — do not reflow, re-indent, or normalize):**

```text
def pooled_scores(registry, sequences, alphabet, cfg, rng) -> pd.DataFrame
    # rows: doc_id, regime, gain_mean(mean,sd), depth_mean(mean,sd), frac_restricted,
    #       own_regime_pool_fraction (D44), coverage   [protocol (c); LABEL-FREE]
```

**B1 — proposed replacement:**

```text
def pooled_score_core(sequences, alphabet, cfg, rng, doc_ids)
        -> tuple[pd.DataFrame, pd.DataFrame]      # (scores, sampling ledger); LABEL-FREE core [D52(v)]
    # takes NO registry; no regime/author/work access by any route [D52(v),(viii)]
    # fits + evaluates protocol-(c) pooled LODO models; returns model-derived quantities + the ledger
    # scores columns, IN THIS ORDER: doc_id, gain_mean, gain_sd, depth_mean, depth_sd,
    #                                frac_restricted, coverage
    # ledger columns, IN THIS ORDER: evaluation_doc_id, seed, training_doc_id, sampled_token_count
    #                                — ACTUAL sampled token counts, never nominal membership [D52(vi)]
def annotate_scores(scores, ledger, registry) -> pd.DataFrame
    # attaches regime, author, work, own_regime_pool_fraction (seed-mean of seed-level fractions) [D44; D52(vii)]
    # expected to change under permuted labels — OUTSIDE the byte-identity guarantee [D52(vii),(viii)]
def pooled_scores(registry, sequences, alphabet, cfg, rng) -> pd.DataFrame
        # thin composition = annotate_scores(*pooled_score_core(...), registry); §6.2 public contract preserved [D52(v)]
```

Notes (informative, not part of the byte edit):
- The two columns removed from the core relative to A1 — `regime` and
  `own_regime_pool_fraction (D44)` — are **not deleted**; they reappear in
  `annotate_scores` (B1), which is where labels are allowed to enter (D52(vii)).
- Byte-identity under permuted registry labels is asserted on a **canonical serialization
  SHA-256** of the score table and of the ledger (declared column order; ledger rows sorted
  by `(evaluation_doc_id, seed, training_doc_id)`, score rows by `doc_id`; fixed float
  formatting) — in-memory frame equality is not an acceptable substitute (D52(vi)).

---

## Site 2 — §7, the test table

All references are to the current §7 table (`## 7. TEST SUITE (pytest; all green at the
stated gates)`).

| Anchor (current §7 text) | Proposed replacement | D52 clause |
| --- | --- | --- |
| after the row `` | `test_conllu_reader.py` | Malformed row → `ParseError` with location; `sent_id` required; ID order preserved | G0 | `` | insert rows **B1** and **B2** below | **D52(ii)** (mandatory G0 coverage: registry; sequences under both policies); **D52(x)** (P-BOUND boundary symbol) |
| after the row `` | `test_bootstrap_holm.py` | Holm ordering on fixed p-vector (family of 2: 0.025/0.05); bootstrap reproducibility under fixed seed | G0 | `` (end of table) | insert row **B3** below | **D52(ii)** (mandatory G0 coverage: seed derivation, config hashing, manifest/sidecar, overwrite protection) |
| the Cases cell of the row `` | `test_scores.py` | `ΔCE` … label-free test: `pooled_scores` output byte-identical under permuted registry labels | G3 | `` | expand with the six scoring-boundary cases of table **B4** below (per-case gates; case 1 carries `@pytest.mark.g0` even though the file is predominantly G3). Cases 2–3 refine the existing label-free clause: byte-identity is asserted on a canonical-serialization SHA-256 of the **score table** and, separately, the **ledger** — not in-memory equality (D52(vi)) | **D52(ix)** (mandatory tests, with gates) |
| after the line `Edge cases throughout: empty sequences, single-symbol alphabet, sentences shorter than restriction, all-dropped sentences.` | append prose **B5** below | **D52(ii)** (`@pytest.mark.g0` convention); **D52(iii)** (canonical command + no-skip enforcement) |

**B1 — new §7 row (insert after `test_conllu_reader.py`), G0:**

```markdown
| `test_registry.py` | `build_registry` over synthetic `sent_id`s: document identity from `sent_id` (D03); regime/taxonomy assignment per §2.3 (HEX, PROSE_CLASS, PROSE_POST, OTHER_VERSE, EXCLUDED); fail-loud validation on unknown or missing document | G0 |
```

**B2 — new §7 row (insert after B1), G0 — covers both P-RESET and P-BOUND:**

```markdown
| `test_sequences.py` | Sentence sequence construction under **both** boundary policies (§3.5). P-RESET: context reset at each sentence boundary (no cross-sentence past). P-BOUND: deterministic extension A⁺ = A ∪ {`#`} with `#` appended at id = |A| (all existing ids stable), |A⁺| = |A| + 1 used wherever |A| enters; `alphabet.json` unmodified; extension built at run time by a documented function and recorded in the run manifest (D52(x)) | G0 |
```

**B3 — new §7 row (insert after `test_bootstrap_holm.py`, end of table), G0:**

```markdown
| `test_determinism.py` | Seed derivation `global XOR crc32(analysis_id)` (§6.3); resolved-config canonicalization + SHA-256; central run-manifest generation (§6.4/D46); minimal per-artifact sidecar `{run_id, sha256, entry_point}`; overwrite refusal absent `--force` | G0 |
```

**B4 — scoring-boundary cases (D52(ix)); in `test_scores.py` unless noted; per-case gate:**

| # | Case (ground truth) | Gate |
| --- | --- | --- |
| 1 | The core has no `registry` argument and cannot reach labels through another object (static/signature check) | **G0** |
| 2 | Score table byte-identical under registry-label permutation | **G3** |
| 3 | Sampling ledger byte-identical under registry-label permutation | **G3** |
| 4 | Annotated output changes as expected under permutation | **G3** |
| 5 | `own_regime_pool_fraction` exact on a synthetic ledger with analytically known sampled-token counts | **G3** |
| 6 | P2 and S1 computed from fixed model-derived scores, labels forming only the permuted contrast | **G3** |

**B5 — prose to append after the `Edge cases throughout: …` line (D52(ii)–(iii)):**

```markdown
**G0 selection (D52(ii)–(iii)).** The G0 set is every test carrying `@pytest.mark.g0`; the
table above states the *minimum* mandatory coverage and does not restrict additional tests.
Canonical command: `uv run pytest -m g0 --strict-markers`. No test in the G0 selection may be
skipped, `xfail`, `xpass`, or collected without an effective assertion; a repository-local
pytest hook (or a dedicated gate runner) enforces a non-zero exit on any such case, and this
enforcement must not depend on reading the pytest summary by eye.
```

---

*End of archived proposal. The two reviewed replacements (§6.2 `pooled_scores`
contract; §7 test table) were applied in commit `97c1ce9`; that commit also documented
the D52(vi) sampling-ledger format in §3.7. Do not reapply.*
