# HEXIS

Hexameter Information Signature: an information-theoretic study of morphosyntactic
organization under metrical constraint — Greek and Latin hexameter vs prose
(UD v2.18 treebanks grc_perseus, la_perseus; UPOS+DEPREL symbol sequences),
measured by a single Rissanen-style MDL context-tree instrument (design v2.0,
single-instrument; Spec §4, D32). Confirmatory statistics: P1 (cross-regime
transfer), P2 (held-out context gain).

Authoritative documents: docs/01_MASTER_SPEC.pdf (binding; cited as §N) and
docs/02_DECISION_LOG.pdf (binding decisions D01–D39). No silent deviations.

## Stack

Python 3.12 via uv. Dependencies (Spec §3.1/§6.3, D27): numpy, pandas, pyarrow,
conllu, scipy, matplotlib, pyyaml, pytest.

## Commands

    uv sync                                  # install environment
    uv run pytest                            # test suite (Spec §7)
    uv run python -m hexis.pipeline.<stage>  # pipeline stages (Spec §6.1)

## Data

Raw UD treebanks are CC BY-NC-SA 2.5 and never redistributed (D28): data/raw/ is
gitignored and immutable; only data/raw/PROVENANCE.md is committed (Spec §2.5).

## Status

Fase 0 — repository scaffolding: §6.2 interface stubs only; no logic implemented.
