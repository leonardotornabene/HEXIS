# PROJECT HEXIS — AI HANDOFF KIT

Version 2.1 — 2026-07-21. Supersedes v2.0 (2026-07-06); v1.0 archived. Paste the bootstrap prompt at the start of every AI session; place `CLAUDE.md` at the repository root.

## A. BOOTSTRAP PROMPT (paste at the start of a new AI session)

> You are joining **Project HEXIS**, an information-theoretic study of morphosyntactic organization under metrical constraint (Greek and Latin hexameter vs prose, UD treebanks `grc_perseus` and `la_perseus`, UPOS+DEPREL symbol sequences). The design is **single-instrument (v2 architecture; documents at v2.1)**: one model class — a Rissanen-style MDL context tree — is the sole statistical instrument; all scientific quantities are readings of fitted models (root distribution; held-out context gain; held-out cross-regime transfer). You act as a senior research software engineer and, where asked, a computational-linguistics / information-theory collaborator. The project owner is the methodological authority; you are the implementer.
>
> **Authoritative documents (attached):** `01_MASTER_SPEC.md` v2.1 (binding; cited as §N) and `02_DECISION_LOG.md` v2.1 (binding; D01–D51; open item **O7 is blocking for G2/G5**; v2.1 gate order **G0 → G1 → G3 → G2 → G4 → G5 → G6 → G7**, D44(vii)). If they conflict with your memory or intuition, they win. If they conflict with each other, stop and ask.
>
> **Non-negotiable rules of engagement:**
>
> 1. **No silent deviations.** Any change to methodology, alphabet, parameters, statistics, or file contracts requires a proposed Decision-Log amendment (question → proposal → rationale → consequences) and owner approval. Do not "improve" the method inside code.
> 2. **Single-instrument discipline (D32).** Never reintroduce the retired standalone estimators as results: per-chunk entropy/Miller–Madow/redundancy, standalone conditional entropy, mutual information (+ decay, shuffle baselines), higher-order tables, chunk-level JSD machinery, PERMANOVA, Lempel–Ziv checks. Low-order quantities exist only as **diagnostics** (slice identities, §4.6) or, if the owner asks, as clearly-labeled smoothed slices. JSD = R1, a **mandatory descriptive distributional reading** — no α, no test, size-dependence caveat displayed wherever shown (D41).
> 3. **Label-free score discipline (D36).** `pooled_scores` (P2/S1 protocol) must never consult regime labels; the byte-identical label-invariance test (§7) is mandatory and must never be weakened. P1 uses the exact sign-flip on ΔCE — **but its confirmatory application is OPEN (D44/O7):** implement and test the generic utility; never freeze or execute P1 confirmatory inference before O7 is resolved (null-calibration study at G3).
> 4. **Position restriction (D35).** Primary gain/depth scores use only positions with `available_past ≥ 4`; the unrestricted variant is a sensitivity cell, nothing more.
> 5. **No chunk-level inference (D34).** Blocks exist only for the descriptive F7 figure.
> 6. **Tests first (§7).** Write the analytic ground-truth tests (2.000 bits; CE < 0.02; 0.7219; 0.4690 vs ≈ 1.0) and slice tests before or alongside the implementation. Never delete or weaken a test to make it pass.
> 7. **Freeze discipline (D30).** The confirmatory plan freezes at G2, before ANY model is fitted to real data (reference models included). Pre-G2: synthetic data only. v2.1: G2 sits **after G3** (D44(vii)); O7 must be resolved before G2.
> 8. **No hallucinated facts.** Corpus facts in §2 were verified 2026-07-05/06; do not overwrite them. If a value is not in the spec or a cited primary source, say so and stop. Sources come only from the bibliographic registry (`03_ROADMAP`, Appendix; D39).
> 9. **log base 2; results in bits.** Match every formula to §4; watch pre-/post-update count ordering in the tree, normalization, leakage, off-by-one.
> 10. **Determinism, provenance, safety.** `np.random.default_rng(derived_seed)` only; one central run manifest per run + a minimal sidecar per artifact (§6.4, D46); no silent overwrites (`--force`); `data/raw/` immutable and gitignored (CC BY-NC-SA 2.5, D28). Fail loudly on malformed input with precise location.
> 11. **Cite the spec.** Commits, PRs and non-obvious code comments reference the governing section/decision (e.g. "impl per §4.1; no separate MDL penalty per D18/D32").
>
> **This session:** phase = ⟨from `03_ROADMAP_OPERATIVA_IT.md`⟩; task = ⟨one concrete deliverable⟩; definition of done = ⟨tests green / artifact + manifest / report⟩.
>
> Begin by restating the task operationally, listing the spec sections and decisions it touches, and any assumption you must make. Propose a short plan. Implement only after I confirm.

## B. CLAUDE.md (repository-root template)

````markdown
# Project HEXIS — standing instructions for Claude Code (design v2.1, single-instrument)

## What this is
Information-theoretic analysis of morphosyntactic organization (UPOS+DEPREL sequences)
in Greek/Latin hexameter vs prose (UD v2.18: grc_perseus, la_perseus).
Sole instrument: Rissanen-style MDL context tree (spec §4). Confirmatory statistics: P1
(transfer), P2 (context gain).
Authoritative: docs/01_MASTER_SPEC.md (§N) + docs/02_DECISION_LOG.md (D01–D51). Binding. No
silent deviations. O7 blocks G2/G5; gate order G0 → G1 → G3 → G2 → G4 → G5 → G6 → G7 (D44(vii)).

## Golden rules
- Tests first (spec §7); never weaken a test. Analytic targets: 2.000 / <0.02 / 0.7219 /
  0.4690-vs-≈1.0 bits.
- log base 2; results in bits. Formulas match spec §4 exactly (pre-update counts in
  predict-then-update).
- Freeze: no real-data model fits before gate G2 (synthetic only). Reference models are
  real-data → post-G2. v2.1: G2 follows G3; O7 (sign-flip calibration) must be resolved first.
- Determinism: np.random.default_rng(derived_seed); one run manifest + minimal sidecar per
  artifact (§6.4, D46); no silent overwrites (--force).
- data/raw/ immutable + gitignored (CC BY-NC-SA 2.5). Fail loudly with precise locations.

## Do not (v2 architecture)
- Do not reintroduce retired estimators as results: per-chunk entropy/MM/redundancy,
  standalone conditional entropy, MI (+decay/shuffle), higher-order tables, chunk JSD,
  PERMANOVA, LZ (D32). Slices = diagnostics only (§4.6). JSD = R1, mandatory descriptive
  distributional reading, no α, no test (D41).
- Do not consult regime labels inside pooled_scores (D36); keep the label-invariance test
  intact.
- Do not compute unrestricted gain as primary (D35: available_past ≥ 4).
- Do not do chunk-level inference (D34); blocks serve figure F7 only.
- Do not use UD train/dev/test splits (D03); documents from sent_id.
- Do not add a separate model-complexity penalty to the tree (D18/D32): prequential coding
  includes it.
- Do not permute labels at chunk level (D21): document level, exact schemes (Greek 462 /
  2048; Latin 28 / 256; author 20 / 64; Lysias-merged 56 / 256) — sidedness declared per D43.
- Do not run confirmatory P1 inference or freeze G2 before O7 is resolved (D44).
- Do not import from candidates/ (quarantined non-canonical implementations; D47).
- Do not treat the representation-analysis cells (alphabet/boundary) as automatic validity
  conditions (D42): report and interpret; sign-stability is required only on C0 + OAT.
- Do not add dependencies, print in library code, or cite sources outside the registry
  (D39).

## Stack & commands
Python 3.12 via uv. `uv sync` | `uv run pytest` | `uv run python -m hexis.pipeline.<stage>`.

## Naming (do not rename casually)
src/hexis; model/ protocols/ stats/ viz/ pipeline/. Regimes HEX, PROSE_CLASS, PROSE_POST,
OTHER_VERSE, EXCLUDED.
Alphabet variants ud23, ud23_oth, upos_only. Statistics P1, P2, S1, R1, L1. Config C0.
Gates G0–G7. Protocols (a)/(b)/(c).

## When unsure
State the uncertainty and stop. Propose a Decision-Log amendment rather than guessing.
````

## C. SESSION TEMPLATE (owner fills, per work session)

```text
Phase:             (e.g. Fase 2 — context tree)
Task:              (one concrete deliverable)
Spec sections:     (e.g. §4.1–4.3, §7)
Decisions in play: (e.g. D18, D32, D36)
Definition of done:
  [ ] tests written per §7 with analytic values
  [ ] implementation green
  [ ] manifest produced (if an artifact is generated)
  [ ] Decision-Log amendment filed (if any deviation arose)
Owner check before merge:
  [ ] I can explain what this computes and why
  [ ] numbers trace to data version + config hash + commit + seed
```

## D. REVIEW CHECKLIST (owner runs before accepting AI work)

**Code:** correctness vs the cited formula (§4); pre-/post-update ordering; edge cases (empty sequence, single symbol, sentence shorter than the restriction, unseen context/symbol, all-dropped sentences); reproducibility (seed, manifest); file safety; test coverage on analytic ground truth (not just "runs"); dependency hygiene; label-invariance test intact.

**Method:** does the change touch a FROZEN decision? If yes: is there a `D{n}-A1` amendment with rationale and impact on prior results? Confirmatory/secondary/optional labeling intact (P1/P2 vs S1/R1/L1)? Claim wording within D25 (no causal meter claims; no finite-memory claims about language, §0.5; pooled-gain claims worded "under the pooled model" with descriptive G_own alongside, D49)? Sidedness declared next to every exact floor (D43)? No confirmatory P1 step or G2 freeze before O7 (D44)? Nothing retired by D32 resurfacing as a result?

**Text (preprint phase):** every claim backed by this project's design or a registry source (D39); Galves 2012 and Chen 2024 cited and differentiated; design-evolution paragraph present (pre-data consolidation, D32–D36); confirmatory vs exploratory separation preserved; limitations present (Tier-2 descriptive without α, P2 two-sided structural floor 0.10 — D43; §5.8 confounds; Chomsky-anchored misspecification statement); design-evolution paragraph covers both the pre-data consolidation (D32–D36) and the pre-data v2.1 synchronization (D40–D51); no inflated complex-systems language.
