# Project HEXIS — standing instructions for Codex (design v2.1, single-instrument)

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
