# HORMATHOS

*Hormathos* (ὁρμαθός) means a chain of things hanging one from another. In Plato's *Ion* (533e), it is the chain of iron rings suspended from a magnet. The name reflects the question behind this project: how much does a symbol's place in a sentence help us predict it from the symbols that came before? At the end of each sentence, the chain of predictions starts again.

HORMATHOS studies the order of grammatical and syntactic annotations in a defined corpus of ancient Greek texts. It asks whether patterns learned from other texts make the attested order more predictable than a comparison in which the same annotations are shuffled *within each sentence*. The study measures a difference in predictive performance; it does not claim to identify a single linguistic cause.

## How the project developed

The work began with a question about Homeric composition and the possibilities of information theory. It then considered a comparison between hexameter and prose. Limited comparable annotated data, uneven coverage of authors and works, and too few independent units made broad claims about composition or genre difficult to support. The present design therefore asks a narrower question: how large and how consistent is the predictive advantage of attested order across the texts available, and how sensitive is it to reasonable choices in the analysis? Hexameter and prose remain a descriptive comparison within that study.

The project is now called **HORMATHOS**. **HEXIS 3.1** remains the name of the [deposited research design](docs/contracts/hexis-3.1/HEXIS_piano_definitivo_v3.1_2026-09-15.md) that governs it. Earlier approaches are preserved in the [archive](archive/); the active repository follows the deposited design. The [decision log](docs/02_DECISION_LOG.md) records that transition: V3-001 adopts the design, V3-002 realigns the repository and governs its publication, and V3-003 gives the project its name.

## Status

The study is complete as specified by the deposited design (phases V0–V5, 25 September 2026). The corpus was acquired and encoded; the prediction method and analysis workflow were checked against analytical and synthetic cases; the full campaign of 980 models across six analysis settings was run, reported and verified, and its first seed was reproduced byte for byte. The [handoff](docs/HANDOFF.md) gives the complete statement of results and limitations, with every number traced to its source table, and the precise technical record.

In brief, under the frozen predictor and the block-by-block training of this design:

- In each of the seven text blocks, a model trained on the other texts gains more over a frequency-only baseline on the attested order of the annotations than on the same annotations shuffled within each sentence. In the main setting the mean advantage ranges from about 0.25 bits per predicted symbol (Hesiodic tradition) to about 0.54 (Plutarch); the Homeric tradition has about 0.26.
- In the main setting the two hexameter blocks show a smaller advantage than each of the five prose blocks. The hexameter-minus-prose difference is about −0.21 bits per symbol when blocks are weighted equally and about −0.20 when every predicted symbol counts equally. It is negative in all six analysis settings and under both weightings.
- Changing the prior, halving the training data, adding other dependency labels, using part of speech alone or deepening the model changes these values by amounts reported in full. Deepening from eight to twelve symbols changes them only at the 10⁻¹⁰ scale, which does not show that longer dependencies are absent.

These are descriptions of a finite corpus, not general claims about Greek, metre or authors. There are two hexameter blocks and five prose blocks, and the *Iliad* dominates its block. Chronology, genre and annotation practice cannot be separated. Each block is scored by a model trained on a different mixture of the other texts. The variation across computational seeds is not uncertainty about the ancient texts. The handoff lists every limitation, the questions the design deliberately leaves out and the procedural reservations. Publication of the corpus-derived data remains a separate decision.

## Scope and materials

The study inventories 17 documents from UD Ancient Greek Perseus r2.18. Eleven documents in seven blocks enter the predictive analysis; six others help define the annotation inventory but are never used to train or score the models. Predictions use earlier retained annotations in the same sentence, and performance is reported as predictive loss in bits per symbol. Results are descriptive: computational repetitions are not independent samples of ancient texts, and the study does not report population-level significance tests.

The raw corpus is not included or redistributed here. The pipeline runs from a checkout of this repository; setup, validation and run instructions are in the [handoff](docs/HANDOFF.md) and [roadmap](docs/03_ROADMAP.md). The [bibliography](docs/BIBLIOGRAPHY.md) lists the project's active sources. [LICENSE](LICENSE) and the [publication decision](docs/02_DECISION_LOG.md) specify the terms for code, documents and data.
