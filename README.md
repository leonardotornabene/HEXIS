# HORMATHOS

*Hormathos* (ὁρμαθός) means a chain of things hanging one from another. In Plato's *Ion* (533e), it is the chain of iron rings suspended from a magnet. The name reflects the question behind this project: how much does a symbol's place in a sentence help us predict it from the symbols that came before? At the end of each sentence, the chain of predictions starts again.

HORMATHOS studies the order of grammatical and syntactic annotations in a defined corpus of ancient Greek texts. It asks whether patterns learned from other texts make the attested order more predictable than a comparison in which the same annotations are shuffled *within each sentence*. The study measures a difference in predictive performance; it does not claim to identify a single linguistic cause.

## Status

The study is complete as specified by its deposited design (phases V0–V5, 25 September 2026). The corpus was acquired and encoded; the prediction method and analysis workflow were checked against analytical and synthetic cases; the full campaign of 980 models across six analysis settings was run, reported and verified, and its first seed was reproduced byte for byte. The [statement of results and limitations](docs/RESULTS.md) gives every number with its source table; the [handoff](docs/HANDOFF.md) is the technical record of how they were produced. The finished results are published in [results/](results/README.md) (V3-007).

## Main result

Each block is evaluated by a model trained on the other blocks. Q is the model's gain over a frequency-only baseline in the attested order minus its gain when the same annotations are shuffled within each sentence. Its unit is bits per eligible target.

**Main setting (C0):** mean Q over 20 computational seeds. Eligible target counts are per seed.

| Block | Eligible targets per seed | Mean Q (bits/target) |
|---|---:|---:|
| Homeric tradition | 46,634 | 0.262 |
| Hesiodic tradition | 6,375 | 0.253 |
| Herodotus | 12,946 | 0.393 |
| Thucydides | 7,227 | 0.430 |
| Athenaeus | 16,691 | 0.452 |
| Diodorus | 12,334 | 0.526 |
| Plutarch | 6,901 | 0.543 |

![Q per block in C0: both hexameter blocks below every prose block](results/figures/profiles__q_block.svg)

Every figure of the study, one panel at a time, is in the [figure gallery](results/figures/README.md).

The two hexameter blocks have lower Q than each of the five prose blocks. In C0, the hexameter-minus-prose contrast is −0.211 bits/target with equal block weights and −0.202 with eligible-target weights; it remains negative in all six settings under both weightings.

This is a descriptive contrast in a finite corpus, not an attribution to metre. There are only two hexameter and five prose blocks; the *Iliad* supplies 45,515 of the Homeric block's 46,634 eligible targets. Chronology, genre, annotation practice and the different training mixtures cannot be separated. Seed variation is computational, not uncertainty about the ancient texts; the study reports no significance tests. [RESULTS.md](docs/RESULTS.md) gives complete values, dispersion, sensitivity analyses and limitations.

## Where to start

| If you want… | Read |
|---|---|
| the results, with every number traced to its table, and their limits | [docs/RESULTS.md](docs/RESULTS.md) |
| the data: tables, figures, manifests, logs and the full archives | [results/README.md](results/README.md) |
| the research design, fixed before the campaign was run | [deposited plan 3.1, English companion](docs/contracts/hexis-3.1-en/HEXIS_piano_definitivo_v3.1_2026-09-15.md) (the [Italian original](docs/contracts/hexis-3.1/HEXIS_piano_definitivo_v3.1_2026-09-15.md) governs) |
| why the project looks the way it does: every decision since the design | [decision log](docs/02_DECISION_LOG.md) |
| how the results were produced, checked and re-checked | [handoff](docs/HANDOFF.md) and [test inventory](docs/TEST_INVENTORY.md) |
| a map of all documents | [docs/00_INDEX.md](docs/00_INDEX.md) |

## How the project developed

The work began with a question about Homeric composition and the possibilities of information theory. It then considered a comparison between hexameter and prose, first also in Latin. Limited comparable annotated data, uneven coverage of authors and works, and too few independent units made broad claims about composition or genre difficult to support. The present design therefore asks a narrower question: how large and how consistent is the predictive advantage of attested order across the texts available, and how sensitive is it to reasonable choices in the analysis? Hexameter and prose remain a descriptive comparison within that study.

The design was written, reviewed and deposited on 15 September 2026, under the working title HEXIS 3.1, before the campaign was run; results of earlier pilots were already known to the author, a limitation the results statement records. The code implements the deposited design, and every deviation from it is declared in the decision log. The project was later named **HORMATHOS**, the name it carries throughout; HEXIS survives only in the deposit, in the identifiers and paths that it and the published evidence fix, and in historical records. Earlier approaches, including the abandoned inferential design, are kept unchanged in [archive/](archive/). The [decision log](docs/02_DECISION_LOG.md) records every transition: V3-001 adopts the design, V3-002 realigns the repository and sets the licences, V3-003 gives the project its name, V3-004 to V3-006 close the reviews before the campaign, V3-007 publishes the results, V3-008 extends the name HORMATHOS to every reader-facing text and to the release, and V3-009 adds the figures for reading.

## How this project was made

HORMATHOS is an independent project by Leonardo Tornabene, a student, carried out alone and outside any institution. The research question, the design and its successive revisions, every decision in the log, the reviews and the acceptance of each phase are the author's. The code, tests and most documents were written with AI coding assistants — Claude Code (Anthropic) and Codex (OpenAI) — working from the author's specifications and checked by the author at every step; many commits carry a `Co-Authored-By` line naming the assistant. [CLAUDE.md](CLAUDE.md) and [AGENTS.md](AGENTS.md) are the standing instructions given to those assistants, identical to [docs/04_AI_HANDOFF_PROMPT.md](docs/04_AI_HANDOFF_PROMPT.md).

## Repository layout

| Path | What it is |
|---|---|
| [`docs/`](docs/00_INDEX.md) | results statement, specification, decision log, roadmap, handoff, test inventory, bibliography |
| [`docs/contracts/hexis-3.1/`](docs/contracts/hexis-3.1/) | the deposited design and its JSON contracts, byte-identified (Italian); English companions in [`hexis-3.1-en/`](docs/contracts/hexis-3.1-en/) |
| [`results/`](results/README.md) | published results of the final campaign, the delivered corpus encoding and the logs of every check |
| [`src/hormathos/`](src/hormathos/) | the package: CoNLL-U reading and encoding (`corpus`, `alphabet`), the context-tree-weighting predictor (`model/`), sampling, scores and R1 (`protocols/`), run stages (`pipeline/`), figures (`viz/`) |
| [`tests/`](tests/) | 431 acceptance tests, all run with no skip; map in [TEST_INVENTORY](docs/TEST_INVENTORY.md) |
| [`config/`](config/) | the YAML projection of the deposited configuration and the registry |
| [`data/`](data/) | provenance of the pinned corpus; the raw files are not redistributed |
| [`archive/`](archive/) | earlier designs and code, byte for byte as they were at `5f1ec06`; a record, not part of the active project (its own README describes that past state) |
| `CLAUDE.md`, `AGENTS.md` | instructions for the AI coding assistants (see above) |
| `pyproject.toml`, `uv.lock`, `conftest.py` | Python 3.12 environment, locked dependencies, test enforcement |

## Reproduce

```bash
uv sync --frozen
git clone https://github.com/UniversalDependencies/UD_Ancient_Greek-Perseus data/raw/UD_Ancient_Greek-Perseus
git -C data/raw/UD_Ancient_Greek-Perseus checkout 37837c7a3c592c9563f8c51cc63344b87247f8a5
uv run pytest            # 431 passed, no skip
```

The SHA-256 of each input file is in [data/raw/PROVENANCE.md](data/raw/PROVENANCE.md). To verify the complete campaign, download the archives of the [GitHub Release](https://github.com/leonardotornabene/HORMATHOS/releases/tag/hormathos-v5-evidence) and follow [results/README.md](results/README.md). The commands that produced every run are in the [handoff](docs/HANDOFF.md); rerunning the campaign or the report is done from the tag `hormathos-v5-evidence` (the same commit as `hexis31-v5-evidence`), the code and perimeter of the published evidence.

## Licences

| Material | Licence |
|---|---|
| Code and configuration, including check scripts | MIT, [LICENSE](LICENSE) |
| Documents, the deposited design and logs | CC BY 4.0, attribution to Leonardo Tornabene |
| Everything derived from the corpus: encoded corpus, tables, figures, ledgers, position vectors | CC BY-NC-SA 2.5, as the source: UD Ancient Greek Perseus r2.18 and AGDT/Perseus |

The decisions are recorded in the publication acts [V3-002 and V3-007](docs/02_DECISION_LOG.md); where a file mixes categories, each portion keeps its own licence. The [bibliography](docs/BIBLIOGRAPHY.md) lists the project's sources.
