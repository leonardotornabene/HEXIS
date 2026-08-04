# HEXIS — Hexameter Information Signature

Do hexameter poetry and prose differ not only in sound and convention, but in
the way grammatical structure unfolds through a text?

This project treats that question as an empirical one. Ancient Greek and Latin
texts are reduced to sequences of grammatical labels — each word replaced by
its part of speech and its syntactic role, with the words themselves discarded.
What remains is a stream of abstract symbols. The question becomes whether the
past of such a stream predicts its future differently in verse than in prose,
and whether that difference is large enough not to be chance.

The instrument is a context tree in the sense of Rissanen: a model that learns,
from the data, how far back one must look to predict the next symbol, keeping
only the context lengths that pay for themselves. The quantity of interest is
measured in bits — how much the past reduces uncertainty about what comes next.

The hypothesis is not that poetry is more ordered, or simpler, or more
predictable. Metrical constraint might plausibly produce any of these, or none.
The study is designed so that a null result is as informative as a positive one.

**Full research proposal: [`HEXIS_research_proposal.pdf`](HEXIS_research_proposal.pdf)
— written in Italian. An English summary can be provided on request.**

## Current status

The design is complete and frozen. The software that will run it is still being
written. **No analysis has been performed on real data, and no results exist.**

This ordering is deliberate rather than incidental. Every decision about what to
measure and how to test it was fixed in writing before any data were examined,
so that the analysis cannot be adjusted after seeing which version of it gives a
more interesting answer. The commit history of this repository is the record of
that ordering, and the decision log is its written trace.

One methodological question remains unresolved and is documented as open: whether
the randomization procedure planned for the first of the two statistics is valid
under its null hypothesis, or whether it would produce too many false positives.
Work on that statistic is suspended until the question is settled. It is
recorded as decision D44 in the decision log.

## What is in this repository

**Documents** (`docs/`)

- `01_MASTER_SPEC.md` — the specification: what is measured, on which texts,
  with which parameters, and how significance is assessed. Binding.
- `02_DECISION_LOG.md` — every methodological decision taken, numbered and
  dated, with its rationale, the alternatives considered, and its consequences.
  Append-only: entries are amended by later entries, never edited or deleted.
- `03_ROADMAP_OPERATIVA_IT.md` — the working plan, in Italian.
- `04_AI_HANDOFF_PROMPT.md` — the briefing used to bring an AI assistant up to
  the current state of the project.
- `00_LEGGIMI_INDICE.md` — index of the four documents above.

**Code** (`src/hexis/`) — the implementation: reading the treebanks, building
the symbol sequences, fitting the context tree, computing the statistics, running
the randomization tests. Written test-first; incomplete by design.

**Tests** (`tests/`) — the test suite. Most tests are currently skipped: they
describe behaviour that has been specified but not yet implemented, and are
activated as each component is written.

**Configuration** (`config/`) — the frozen parameters of the analysis, kept
separate from the code so that no parameter can be changed silently.

**Data** (`data/raw/`) — the corpora themselves are not stored here. The source
treebanks are UD_Ancient_Greek-Perseus and UD_Latin-Perseus, release r2.18,
licensed CC BY-NC-SA 2.5 and not redistributed. `PROVENANCE.md` records their
exact version and checksums so that anyone can obtain identical copies.

**Prior implementation** (`candidates/`) — an earlier, independent context-tree
implementation, kept isolated for reference and comparison. It is not used by
the pipeline and is excluded from the test suite.

**Assistant instructions** (`CLAUDE.md`, `AGENTS.md`) — standing instructions
given to AI coding assistants working on this repository.

## Running the code

Python 3.12, managed with `uv`.

uv sync # install the environment
uv run pytest # run the test suite


The analysis pipeline is not yet runnable.

## Author

Leonardo Tornabene, Turin. Independent work, carried out outside any
institution, while completing secondary school.

AI assistants were used for implementation and for methodological review. The
research question, the design, the methodological decisions and the contents of
the decision log are my own.
