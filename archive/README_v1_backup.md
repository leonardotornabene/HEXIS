# HEXIS — Hexameter Information Signature

An information-theoretic study of morphosyntactic organization under metrical
constraint: Greek and Latin hexameter versus prose, using UD v2.18 treebanks
(`grc_perseus`, `la_perseus`) as UPOS+DEPREL symbol sequences, measured by a
single Rissanen-style MDL context-tree instrument (Spec §4, D32).

Confirmatory statistics: **P1** (cross-regime transfer) and **P2** (held-out
context gain), tested by exact randomization under Holm–Bonferroni correction.
Latin serves as a qualitative replication.

Full proposal: [HEXIS_research_proposal.pdf](HEXIS_research_proposal.pdf)

## Status

**Phase 1a — implementation. The design is frozen; no model has been fitted to
real data.**

Gate order: G0, G1, G3, G2, G4, G5, G6, G7. The first fits to real data occur
at G4, after the design freeze at G2. The analysis plan was specified before
any data were examined, and the commit history of this repository records that
ordering.

One methodological question is open and currently blocks G2: **D44 / O7**, the
validity of the sign-flip randomization for P1.

## Authoritative documents

Binding, cited as §N and D##. No silent deviations.

- [`docs/01_MASTER_SPEC.md`](docs/01_MASTER_SPEC.md) — specification v2.1
- [`docs/02_DECISION_LOG.md`](docs/02_DECISION_LOG.md) — decisions D01–D54, append-only

## Stack

Python 3.12 via `uv`. Dependencies (Spec §3.1/§6.3, D27): numpy, pandas,
pyarrow, conllu, scipy, matplotlib, pyyaml, pytest.

uv sync # install environment
uv run pytest # test suite (Spec §7)


Pipeline stages (`uv run python -m hexis.pipeline.<stage>`, Spec §6.1) are not
yet runnable: implementation is in progress and proceeds tests-first.

## Data

Raw UD treebanks are CC BY-NC-SA 2.5 and are never redistributed (D28):
`data/raw/` is gitignored and immutable; only
[`data/raw/PROVENANCE.md`](data/raw/PROVENANCE.md) is committed (Spec §2.5).

## Author

Leonardo Tornabene. Independent work, carried out outside any institution.
AI assistants were used for implementation and methodological review; the
research design, the methodological decisions and the contents of the Decision
Log are my own.
