# HORMATHOS

*Hormathos* (ὁρμαθός) means a chain of things hanging one from another. In Plato's *Ion* (533e), it is the chain of iron rings suspended from a magnet. The name reflects the question behind this project: how much does a symbol's place in a sentence help us predict it from the symbols that came before? At the end of each sentence, the chain of predictions starts again.

HORMATHOS studies the order of grammatical and syntactic annotations in a defined corpus of ancient Greek texts. It asks whether patterns learned from other texts make the attested order more predictable than a comparison in which the same annotations are shuffled *within each sentence*. The study measures a difference in predictive performance; it does not claim to identify a single linguistic cause.

## How the project developed

The work began with a question about Homeric composition and the possibilities of information theory. It then considered a comparison between hexameter and prose. Limited comparable annotated data, uneven coverage of authors and works, and too few independent units made broad claims about composition or genre difficult to support. The present design therefore asks a narrower question: how large and how consistent is the predictive advantage of attested order across the texts available, and how sensitive is it to reasonable choices in the analysis? Hexameter and prose remain a descriptive comparison within that study.

The project is now called **HORMATHOS**. **HEXIS 3.1** remains the name of the [deposited research design](docs/contracts/hexis-3.1/HEXIS_piano_definitivo_v3.1_2026-09-15.md) that governs it. Earlier approaches are preserved in the [archive](archive/); the active repository follows the deposited design. The [decision log](docs/02_DECISION_LOG.md) records that transition: V3-001 adopts the design, V3-002 realigns the repository and governs its publication, and V3-003 gives the project its name.

## Status

The corpus has been acquired and encoded, and the prediction method and analysis workflow have been checked against analytical and synthetic cases. A first technical run on the real corpus, using one computational seed, has also been completed and reproduced byte for byte. It shows that the workflow can execute and be verified; it is not the completed study. The planned runs across all seeds, the final comparisons and the research report are still pending review and completion. The [handoff](docs/HANDOFF.md) gives the precise technical record.

## Scope and materials

The study inventories 17 documents from UD Ancient Greek Perseus r2.18. Eleven documents in seven blocks enter the predictive analysis; six others help define the annotation inventory but are never used to train or score the models. Predictions use earlier retained annotations in the same sentence, and performance is reported as predictive loss in bits per symbol. Results will be descriptive: computational repetitions are not independent samples of ancient texts, and the study does not report population-level significance tests.

The raw corpus is not included or redistributed here. The pipeline runs from a checkout of this repository; setup, validation and run instructions are in the [handoff](docs/HANDOFF.md) and [roadmap](docs/03_ROADMAP.md). The [bibliography](docs/BIBLIOGRAPHY.md) lists the project's active sources. [LICENSE](LICENSE) and the [publication decision](docs/02_DECISION_LOG.md) specify the terms for code, documents and data.
