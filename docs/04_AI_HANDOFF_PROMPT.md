# HORMATHOS standing instructions — V3-001, V3-002, V3-003

````markdown
# Project HORMATHOS — standing instructions (design HEXIS 3.1)

Active authority: docs/01_MASTER_SPEC.md, V3-001, V3-002 and V3-003 in
docs/02_DECISION_LOG.md. V3-001 adopts
docs/contracts/hexis-3.1/HEXIS_piano_definitivo_v3.1_2026-09-15.md and its
byte-identified JSON contracts. Text governs semantics; JSON fixes values.
Do not silently deviate or regenerate expectations to make tests pass.

V0–V2 are completed; V3–V5 are not attested and no real fit has ever run.
V3-002 realigned the repository on 2026-09-22: the active tree is 3.1 only and
every historical material is preserved byte for byte under archive/, at the
path it had at 5f1ec06. archive/ is a record: never imported, never collected,
outside the code identity; it runs at that commit, not here. Retired design
elements — v2.1 inference, Latin, gates G0–G7, permutation constants,
sign-stability, D01–D55 — are listed in V3-001 and must never be reintroduced.

V3-003 named the project HORMATHOS on 2026-09-23. It implements the deposited
HEXIS 3.1 design: hexis survives only in the deposit, the contract identifiers,
the distribution name that the contract-fixed uv.lock records, results/hexis31
and archive/. The package is src/hormathos. Every artifact is in English; the
Italian originals of the deposit and of V3-001 and V3-002 govern and are never
rewritten.

Stop for review before V3; no new real model fits in this tranche. The freeze
perimeter is code identity over all of src/hormathos plus tests, conftest.py,
pyproject.toml, config and uv.lock: once V2/V3 evidence is published, changing
any of them forces a new directory and a new run.

Tests first; never weaken a still-valid property; retiring one means replacing
its test with a reason, not deleting the check. Active acceptance: pytest and
pytest -m v31 collect the same tests, all marked v31, with no skip or xfail and
an executed assert each. Obligations are tracked in docs/TEST_INVENTORY.md.
Use Python 3.12 via uv; keep dependencies and uv.lock. No print in library code.

Three pinned Greek CoNLL-U only; recombine numeric source coordinates, not splits.
18 prefixes, 17 documents, 11 primary in seven blocks; six inventory_only enter
census/alphabet only, never training/scoring. Regime and report group are distinct.
Validate source UPOS, PROPN→NOUN, retention/DEPREL policy, global ADV/PART→ADV_PART,
then frozen lexicographic IDs: ud23/ud23_oth/upos_only = 100/105/11.
UPOS shares the exact C0 mask; OTH has its own population. Sentence streams reset,
including empty streams; target j≥4. No SEP, EOS, UNK or cross-sentence history.

Implemented instrument: frozen CTW, four losses, Q and G in bits, two declared
weights, R1 descriptive only. No inference. Core label-free; labels via
annotate_scores. No extra model-complexity penalty. RNG per the deposited
SHA-256 contract.

One manifest per run: deterministic identity from contract/code/data/registry/
alphabets/config/lock; timestamps, machine and paths external. Atomic publication,
no implicit overwrite; preserve local scripts and every historical result.
data/raw is immutable and gitignored; reject output inside raw even through symlinks.
Raw licensing remains CC BY-NC-SA 2.5; what the publication act of V3-002 covers,
and under which licence, is decided there and nowhere else.
Sources only from the active registry in docs/BIBLIOGRAPHY.md.

When scientifically uncertain: stop the affected passage, state the discrepancy,
propose an explicit contract/Decision-Log amendment rather than guessing.
````
