# Project HEXIS — standing instructions (design 3.1)

Active authority: docs/01_MASTER_SPEC.md and V3-001 in docs/02_DECISION_LOG.md,
which adopt docs/contracts/hexis-3.1/HEXIS_piano_definitivo_v3.1_2026-09-15.md
and its byte-identified JSON contracts. Text governs semantics; JSON fixes values.
Do not silently deviate or regenerate expectations to make tests pass.

V0–V1 are completed. V2 is extensively implemented; closure must be reconciled
and verified, preserving prior synthetic evidence. V3–V5 are not attested.
Stop for review before V3; no new real model fits in this tranche.
The old v2.1 P1/P2 inference, Latin, O7 blocker, permutation constants, sign-stability,
old sensitivities and gates G0–G7 are historical, not resolved retroactively.
D01–D54, proposed D55 and technical G1 ratifications retain their historical status.

Tests first; never weaken a still-valid property. Active acceptance: pytest -m v31,
actual collection coverage, executed asserts, no skip/xfail. The remaining
V3–V5 obligations are tracked in docs/TEST_INVENTORY.md. Use Python 3.12 via uv;
keep dependencies and uv.lock. No print in library code or candidates imports.

Three pinned Greek CoNLL-U only; recombine numeric source coordinates, not splits.
18 prefixes, 17 documents, 11 primary in seven blocks; six inventory_only enter
census/alphabet only, never training/scoring. Regime and report group are distinct.
Validate source UPOS, PROPN→NOUN, retention/DEPREL policy, global ADV/PART→ADV_PART,
then frozen lexicographic IDs: ud23/ud23_oth/upos_only = 100/105/11.
UPOS shares the exact C0 mask; OTH has its own population. Sentence streams reset,
including empty streams; target j≥4. No SEP, EOS, UNK or cross-sentence history.

Implemented instrument: frozen CTW, four losses, Q and G in bits, two declared weights,
R1 descriptive only. No inference. Core label-free; labels via annotate_scores.
No extra model-complexity penalty. RNG per deposited SHA-256 contract, not old CRC32.

One manifest per run: deterministic identity from contract/code/data/registry/
alphabets/config/lock; timestamps, machine and paths external. Atomic publication,
no implicit overwrite; preserve local scripts and all historical results.
data/raw is immutable and gitignored; reject output inside raw even through symlinks.
Raw licensing remains CC BY-NC-SA 2.5; no data publication in this tranche.
Sources only from the active registry in docs/BIBLIOGRAPHY.md.

When scientifically uncertain: stop the affected passage, state the discrepancy,
propose an explicit contract/Decision-Log amendment rather than guessing.
