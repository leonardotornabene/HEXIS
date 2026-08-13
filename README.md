# HEXIS — Hexameter Information Signature

Do hexameter poetry and prose differ not only in sound and convention, but in
the way grammatical structure unfolds through a text?

This project treats that question as an empirical one. Ancient Greek and Latin
texts are reduced to sequences of grammatical labels — each word replaced by its
part of speech and by the type of its relation to the word it depends on, with
the words themselves discarded. What remains is a stream of abstract symbols.
The question becomes whether the past of such a stream predicts its future
differently in verse than in prose, and whether that difference is large enough
not to be chance.

The instrument is a context tree in the sense of Rissanen: a single model that
learns, from the data, how far back one must look to predict the next symbol,
keeping only the context lengths that pay for themselves. It is read in three
ways: as a distribution over symbols, as the improvement in prediction that
context buys, and as the cost of predicting one kind of writing with a model
trained on the other. Everything is measured in bits.

The hypothesis is not that poetry is more ordered, or simpler, or more
predictable. Metrical constraint might plausibly produce any of these, or none.
What will be reported is fixed in advance, whatever the outcome; and with eleven
documents the power to detect small effects is limited, a limit declared in the
design rather than discovered afterwards.

**Full research proposal: [`HEXIS_research_proposal.pdf`](HEXIS_research_proposal.pdf)
— written in Italian. An English summary is in preparation.**

## At a glance

**The symbols.** Every word that is kept becomes one abstract symbol, pairing its
part of speech with the type of its syntactic relation. Twelve parts of speech
and twenty-three relation types give an alphabet of at most 276 symbols.
Everything is then computed a second time on a coarser alphabet that uses parts
of speech alone, so that a result which depends on the syntactic annotation can
be told apart from one that does not.

**The corpus.** Two treebanks from the Universal Dependencies project, release
2.18: Ancient Greek and Latin, both converted from the Ancient Greek and Latin
Dependency Treebank, whose syntactic annotation is manual rather than automatic.
The Greek treebank holds 13,919 sentences and 202,989 tokens, the Latin 2,273
sentences and 28,868 tokens. Those are the totals of the treebanks; the analysed
sample is smaller.

**The comparison.** Eleven Greek documents: five in hexameter against six of
classical prose. Twelve tragedies are added as a control asking whether any
signature that appears belongs to hexameter or to verse in general. Prose of a
later period is added as a control for the passage of time. Latin plays a
deliberately subordinate part, two verse documents against six of prose, and the
asymmetry is stated rather than smoothed over.

**The two tests.** Both compare whole documents rather than sentences or words.
The *transfer* test asks whether a text costs more to predict when the model has
learned from the other kind of writing than from its own, and by how many bits.
The *context gain* test asks whether the two kinds differ in how much prediction
improves when the past is consulted at all rather than ignored; it is computed
under models that are never shown which document belongs to which group. Because
two hypotheses are tested rather than one, the threshold for significance is
corrected accordingly.

**The inference.** Both tests are settled by enumerating every possible
reassignment — 2,048 sign reversals for the transfer test, 462 relabelings for
the context gain test — and asking how extreme the observed value is among them.
Nothing is approximated and nothing is assumed about the shape of any
distribution. With eleven documents that is the only defensible choice, and
those same eleven documents are what limits how small an effect could be seen.

## Current status

The design is written down in full and cannot change quietly: every
methodological choice is a numbered, dated entry in a decision log that now runs
to fifty-four entries, and a choice is revised by adding an entry, never by
editing one. The plan is not yet sealed, however. Sealing it is a deliberate
step, and it is held up by the open question described below.

What exists today is that written design, and an interface. Every part of the
software is declared — its inputs, its outputs, and the section of the
specification it answers to — and not one of those declarations has a working
body behind it yet. The tests describe the intended behaviour ahead of the code,
and all of them are currently skipped; each is switched on as the component it
describes is written. **No model has been fitted to anything, real or synthetic,
and no results exist.**

This ordering is deliberate rather than incidental. The rule that governs it is
that nothing is fitted to real data until the plan is sealed: until then the work
runs on artificial data whose answer is known in advance, and the first fits on
the corpus come afterwards. The corpus is looked at once before that point, in
order to settle which texts count as which, which symbols actually occur, and
how much training material each document may use. Those decisions are taken
without computing any of the quantities the study reports, and are recorded
together with whatever consequences they carry. What is not claimed is that every
choice was made in ignorance of the corpus. Some could not have been.

The record of that ordering is the research proposal, which predates the
software, together with the decision log, which is only ever appended to. The
commit history of this repository agrees with both — but this is a repository I
maintain myself, and a history one maintains oneself is not an independent
timestamp. It is offered as a record, not as proof.

### The open question

Nine questions are tracked as open. Eight are ordinary: checks postponed until
the corpus is examined, or references to be completed before submission. One is
not.

The transfer test was to be settled by trying every way of reversing the sign of
each document's result — 2,048 of them — and asking how extreme the observed
value is among those. That procedure is exact only if reversing the signs
independently really does generate the range of outcomes the null hypothesis
allows. Taken on its own, each document's quantity is symmetric about zero,
which is a weaker property than the one required. The eleven documents are
trained on material drawn from two heavily overlapping pools, so a chance
fluctuation that makes one pool more representative than the other pushes every
document at once — one way for the verse documents, the other way for the prose.
Independent sign reversals cannot produce a shared push of that kind, and with
only eleven documents it does not average away. The consequence would be a test
that rejects the null too often.

The context gain test is not affected. Its randomization requires only that the
eleven scores be interchangeable when the null hypothesis is true, and they are
computed without the model ever being shown the labels.

Until the question is settled the transfer test is not run, and the plan cannot
be sealed. It is to be settled by a calibration study on artificial data —
running the whole procedure in a world where the null hypothesis is true by
construction, and counting how often it is wrongly rejected, with the context
gain test's randomization as a positive control — and by a mathematician's
reading. The machinery itself is written and tested; what is in doubt is whether
it answers the question it was built to answer.

## What is in this repository

**Documents** (`docs/`)

- `01_MASTER_SPEC.md` — the specification: what is measured, on which texts,
  with which parameters, and how significance is assessed. Binding.
- `02_DECISION_LOG.md` — every methodological choice taken, numbered and dated,
  with its rationale, the alternatives considered, and its consequences; the
  open questions are gathered in a section of their own. Append-only: entries
  are amended by later entries, never edited or deleted.
- `03_ROADMAP_OPERATIVA_IT.md` — the working plan, in Italian.
- `04_AI_HANDOFF_PROMPT.md` — the briefing used to bring an AI assistant up to
  the current state of the project.
- `00_LEGGIMI_INDICE.md` — index of the four documents above, in Italian.
- `audit/` — the working record of two corrections made to binding text: the
  restoration of passages damaged when the specification was converted to PDF,
  and the alignment of the working documents with the final proposal. Kept
  because corrections to binding text should themselves be inspectable.
- `implementation/` — plans and design notes for the current phase of coding.
  Working documents: they answer to the specification, never the reverse.
- `archive_v2_0_pdf/` — the superseded previous version of the five documents.

**Code** (`src/hexis/`) — the declared interface of the software: reading the
treebanks, building the symbol sequences, fitting the context tree, computing
the statistics, running the randomization tests. Every signature is fixed
against the specification; no function body is implemented yet. Written
test-first, and incomplete by design rather than by neglect.

**Tests** (`tests/`) — the test suite. Every test is currently skipped: each
describes behaviour that has been specified but not yet implemented, and is
switched on as its component is written. When the first stage of work is
declared complete, the suite must run with nothing skipped and nothing asserted
only in name — a condition enforced by the test configuration rather than
checked by eye.

**Configuration** (`config/`) — the parameters of the analysis, kept separate
from the code so that no parameter can be changed silently. Two of them are
deliberately left empty and are filled only after the corpus has been examined:
the symbols that actually occur, and the amount of training material each
document is allowed.

**Data** (`data/raw/`) — the corpora themselves are not stored here. The source
treebanks are `UD_Ancient_Greek-Perseus` and `UD_Latin-Perseus`, release 2.18,
licensed CC BY-NC-SA 2.5 and not redistributed. `PROVENANCE.md` is the record in
which their commit hashes, per-file checksums and acquisition date are entered
at the moment they are downloaded, so that anyone can obtain identical copies.

**Candidate implementation** (`candidates/`) — an earlier attempt at the context
tree, kept in quarantine. It departs from the growth rule laid down in the
specification, and its own tests cover only one of the four cases with known
answers that the accepted implementation must reproduce. It is therefore never
imported by the pipeline and never collected by the test suite. It may be
promoted only if it is brought into conformance and passes those cases.

**Assistant instructions** (`CLAUDE.md`, `AGENTS.md`) — standing instructions
given to AI coding assistants working on this repository.

## Running the code

Python 3.12, managed with [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync         # install the locked environment
uv run pytest   # run the test suite
```

Every test is currently skipped, so the suite passes without asserting anything.
That is the expected state at this stage, not a sign that something works.

The analysis pipeline is not yet runnable.

## Author and contact

Leonardo Tornabene, Turin. Independent work, carried out outside any
institution, while still at secondary school.
leonardo.tornabene@gmail.com

Every methodological decision is mine and was ratified by me before entering the
record; the drafting of documents and code was AI-assisted, under my review. The
standing instructions given to the assistants are in this repository, so that the
terms of that assistance can be inspected rather than taken on trust.

I am looking for methodological supervision, and would welcome a reading from
anyone working on variable-memory models, on exact inference in small samples, or
on Universal Dependencies for the classical languages. The most useful thing
anyone could tell me at present concerns the open question above: whether that
randomization can be repaired, or must be replaced by one that retrains under
relabeling, or by something else entirely.

## License

The code is released under the MIT license; see `LICENSE`. The documents — the
specification, the decision log, the roadmap, the research proposal and this file
— are released under CC BY 4.0.

The corpora are not redistributed here. The statistics derived from them, once
they exist, will be released under CC BY-NC-SA 4.0 with attribution to Universal
Dependencies, inheriting the terms of the treebanks rather than resting on a
judgement about whether measurements computed from a corpus are a derivative
of it.
