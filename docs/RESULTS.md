# HORMATHOS — results and limitations

This document states what the study found and what it does not show. Every number is taken from a published table of the final campaign, named beside it; nothing is recomputed here, and every result is descriptive. The terms are defined in the next section; [Reading the source tables](#reading-the-source-tables) explains how each label in the tables corresponds to the codes used in the published files.

The study follows a research plan, version 3.1, written, reviewed and deposited on 15 September 2026 before the final campaign was run ([English companion](contracts/hexis-3.1-en/HEXIS_piano_definitivo_v3.1_2026-09-15.md); the [Italian original](contracts/hexis-3.1/HEXIS_piano_definitivo_v3.1_2026-09-15.md) governs). The statement that closed the study on 25 September 2026, with the record of its two reviews, is preserved word for word in the [handoff at the tag `hormathos-v5-evidence`](https://github.com/leonardotornabene/HORMATHOS/blob/hormathos-v5-evidence/docs/HANDOFF.md#v5-results-and-limitations--25-september-2026). This document gives the same results with the same tables and numbers, in wording that does not require knowledge of the project's internal records. The tables and figures it cites are described in [results/README.md](../results/README.md); the figures, with an explanation beside each, are in the [figure gallery](../results/figures/README.md).

## The question and the measurement

**Corpus.** The texts come from the pinned release r2.18 of the Universal Dependencies (UD) Ancient Greek Perseus treebank, in which every word carries a part-of-speech tag and a syntactic dependency relation assigned by annotators. Seventeen documents are used. Eleven are scored; six tragedies are *census-only*: they are counted when the inventory of symbols is built and never enter training or scoring.

**Symbols.** Each kept word becomes one symbol joining its part of speech and its relation, for example `NOUN:nsubj`, a noun that is the subject. Proper nouns are counted as nouns. Particles and adverbs are merged into one class, `ADV_PART`, because the source applies the two tags inconsistently across documents (see [Corpus and populations](#corpus-and-populations)). Punctuation and a few other word classes are removed, as are words whose relation is not one of the 23 kept; removals close the gaps, so context is counted in kept symbols, not in words of the source. Three **annotation schemes** are used:

- *part of speech + relation*, 100 symbols: the main scheme;
- *other relations kept*: the same, except that words with any other relation are kept under one shared label instead of removed, 105 symbols, and therefore a different set of scored positions;
- *part of speech only*, 11 symbols, on exactly the same positions as the main scheme.

**Sentences and targets.** Each sentence is an independent sequence: the history starts again at every sentence, and nothing is predicted across a sentence boundary. A **target** is a position with at least four kept predecessors in its own sentence. The first four positions of each sentence feed the history and the training counts but are not scored. Targets are further split by how many kept tokens precede them in the sentence: 4–7 or 8 or more.

**Blocks.** The eleven scored documents form seven **blocks**, the units of every comparison. Two are in hexameter verse: the *Homeric tradition* (the *Iliad* and the *Homeric Hymn to Demeter*) and the *Hesiodic tradition* (*Theogony*, *Works and Days*, *Shield of Heracles*). Five are in prose, one per author: Herodotus, Thucydides, Athenaeus, Diodorus, Plutarch. The two traditions are conservative grouping conventions, not claims of common authorship.

**Training on the other blocks.** Each block is scored by a model trained without any of its documents. Each of the other six blocks contributes the same number of kept tokens, 8,884, for 53,304 in all, drawn at random, mostly as whole sentences. Where a sentence is cut, the fragment starts a history of its own: the tokens left out never serve as context.

**Predictor.** The model is **context-tree weighting** (CTW), a Bayesian mixture over all models that predict a symbol from a variable number of preceding symbols, up to a maximum **depth** of eight. It keeps a tree of the contexts seen in training and weights them by how well they predicted in training; in each context the symbol probabilities start from a prior count of 0.5 for every symbol. The procedure is fixed in advance and does not adapt to the results.

**Cross-entropy, gain and order advantage.** The **cross-entropy** (CE) of a predictor is the average number of bits it needs per target: −log₂ of the probability it gave to the symbol that actually occurred. One bit is the information in a fair yes/no choice; fewer bits mean better prediction. Two predictors are scored on the same targets: the trained model, and a **frequency predictor** that knows only how often each symbol occurs in the training sample. The **gain** G is the difference, CE of the frequency predictor minus CE of the model: how many bits per target the context saves.

The **shuffle** is the control. In every training and scored sentence the symbols are randomly reordered, keeping which symbols the sentence contains and destroying only their order; a separate model is trained and scored on the shuffled text. The study therefore has two **conditions**, original order and shuffled, and four cross-entropies. The **order advantage** is

Q = G(original) − G(shuffled),

in bits per target. Q is positive when the original order helps prediction more than the shuffled order does. All four cross-entropies are kept, because shuffling can move a different symbol into a scored position: the positions are the same in both conditions, their symbols need not be.

**Seeds.** The whole procedure is repeated with different random draws of the training sample and of the shuffle; each repetition is a **seed**. The main setting uses seeds 0–19, each variant seeds 0–9: 490 train–score pairs and 980 models in all. The mean, the sample standard deviation (SD, denominator S − 1, where S is the number of seeds), the minimum and the maximum over seeds describe computational variation only. They are not uncertainty about the ancient texts; no significance test, p-value or confidence interval is computed.

**Settings.** Besides the main setting, five variants each change one choice:

| Setting | What changes |
|---|---|
| Main | part of speech + relation, depth 8, prior 0.5 per symbol, 8,884 training tokens per contributing block, seeds 0–19 |
| Weaker prior | prior 0.01 per symbol instead of 0.5 |
| Half training data | 4,442 training tokens per contributing block instead of 8,884 |
| Depth 12 | contexts of up to twelve symbols instead of eight |
| Other relations kept | the *other relations kept* scheme, with its own positions |
| Part of speech only | the *part of speech only* scheme, on the positions of the main setting |

**Hexameter and prose.** The two groups are summarized by averaging their blocks in two ways: with every block weighing the same (each hexameter block 1/2, each prose block 1/5), or with every target weighing the same, which gives larger blocks more weight. The **hexameter − prose difference** subtracts the prose average from the hexameter average; a negative value means hexameter below prose. A **paired change** compares a variant with the main setting seed by seed on the seeds 0–9 that both share.

**Display.** Every score is printed with six decimals, except nonzero magnitudes below 10⁻⁶, printed in scientific notation with three significant digits. Rounding is presentation only: numbers that coincide when printed are not mathematically identical. `null` marks a quantity that is undefined, never a zero.

## Corpus and populations

The campaign describes how well the annotations of this corpus can be predicted by this procedure. It concerns the sequence of kept annotation symbols: not the prediction of words, and not the full dependency tree.

The [corpus figure](../results/figures/README.md#1-corpus-and-annotation) shows, per document, the source and kept tokens, the targets, the share kept and the source tagging of particles and adverbs. For the census-only documents, the targets it shows are positions that would qualify, not positions evaluated. Before the merging, the source tags words as particles only in the verse documents and never in the prose; merging particles and adverbs everywhere reduces this discontinuity, but it does not make the annotation homogeneous.

The main setting and part of speech only each have 109,108 targets per seed; the other-relations setting has 109,716 (Tables 1–2). These are finite populations fixed by each scheme, not samples of independent linguistic observations. Counts below are per seed and are never multiplied by the number of seeds. "All targets" is the total of the two groups by preceding tokens, not a third, separate population.

**Table 1 — targets per block.** Source: [block_pairs.csv](../results/hexis31/v3-seed0-v3006/block_pairs.csv), seed 0, column `n`. The main-setting columns also hold for the weaker prior, half training data, depth 12 and part of speech only, as every source row confirms.

| Block | Main: all | Main: 4–7 | Main: ≥8 | Other relations kept: all | Other relations kept: 4–7 | Other relations kept: ≥8 |
|---|---|---|---|---|---|---|
| Homeric tradition | 46634 | 20241 | 26393 | 47062 | 20381 | 26681 |
| Hesiodic tradition | 6375 | 2405 | 3970 | 6398 | 2410 | 3988 |
| Herodotus | 12946 | 3977 | 8969 | 12994 | 3983 | 9011 |
| Thucydides | 7227 | 1989 | 5238 | 7234 | 1990 | 5244 |
| Athenaeus | 16691 | 5641 | 11050 | 16786 | 5659 | 11127 |
| Diodorus | 12334 | 2898 | 9436 | 12334 | 2898 | 9436 |
| Plutarch | 6901 | 1840 | 5061 | 6908 | 1842 | 5066 |

**Table 2 — documents and their targets.** Source: [document_scores.csv](../results/hexis31/v3-seed0-v3006/document_scores.csv), seed 0, column `n`. Work names and kept tokens come from the delivered corpus, [documents.csv](../results/hexis31/v1/documents.csv) (scored documents, main scheme); the total targets per document are its `eligible` column.

| Document key (`doc_id`) | Work | Block | Kept tokens | Main: all | Main: 4–7 | Main: ≥8 | Other relations kept: 4–7 | Other relations kept: ≥8 |
|---|---|---|---|---|---|---|---|---|
| tlg0012.tlg001.perseus-grc1.tb.xml | Iliad | Homeric tradition | 69327 | 45515 | 19783 | 25732 | 19918 | 26009 |
| tlg0013.tlg002.perseus-grc1.tb.xml | Homeric Hymn to Demeter | Homeric tradition | 1761 | 1119 | 458 | 661 | 463 | 672 |
| tlg0020.tlg001.perseus-grc1.tb.xml | Theogony | Hesiodic tradition | 4023 | 2945 | 942 | 2003 | 944 | 2011 |
| tlg0020.tlg002.perseus-grc1.tb.xml | Works and Days | Hesiodic tradition | 3189 | 2077 | 887 | 1190 | 889 | 1195 |
| tlg0020.tlg003.perseus-grc1.tb.xml | Shield of Heracles | Hesiodic tradition | 2070 | 1353 | 576 | 777 | 577 | 782 |
| tlg0016.tlg001.perseus-grc1.1.tb.xml | Histories, book 1 (Herodotus) | Herodotus | 17301 | 12946 | 3977 | 8969 | 3983 | 9011 |
| tlg0003.tlg001.perseus-grc1.1.tb.xml | Histories, book 1 (Thucydides) | Thucydides | 9346 | 7227 | 1989 | 5238 | 1990 | 5244 |
| tlg0008.tlg001.perseus-grc1.tb.xml | Deipnosophistae, books 12-13 | Athenaeus | 23133 | 16691 | 5641 | 11050 | 5659 | 11127 |
| tlg0060.tlg001.perseus-grc3.11.tb.xml | Bibliotheca historica, book 11 | Diodorus | 15266 | 12334 | 2898 | 9436 | 2898 | 9436 |
| tlg0007.tlg004.perseus-grc1.tb.xml | Lycurgus | Plutarch | 4481 | 3493 | 925 | 2568 | 926 | 2571 |
| tlg0007.tlg015.perseus-grc1.tb.xml | Alcibiades | Plutarch | 4403 | 3408 | 915 | 2493 | 916 | 2495 |

## Order advantage by block and document

In the main setting the mean Q is 0.262112 bits per target for the Homeric tradition and 0.252991 for the Hesiodic tradition. The five prose blocks have 0.393150 (Herodotus), 0.429579 (Thucydides), 0.452080 (Athenaeus), 0.526170 (Diodorus) and 0.542858 (Plutarch) (Table 3). All seven means are positive, and both hexameter means are below every prose mean under this procedure. A positive Q means that the model gains more over the frequency predictor in the original order than after the shuffle; it does not identify why the blocks differ.

In every block the model's cross-entropy in the original order is below that of the frequency predictor. The gains after shuffling are practically zero, so the gain in the original order and Q coincide at the printed precision in Table 3; both are kept, unrounded, in the source. The four cross-entropies also show why the two frequency predictors cannot be cancelled against each other: for the Homeric tradition the mean frequency cross-entropy is 4.817659 bits per target in the original order and 4.724583 after shuffling, because the shuffle moves symbols in and out of the scored positions. A gain after shuffling this small is the observed behaviour of this control, not a mathematical identity of the predictor, and it does not show that all of the gain in the original order comes from linguistic order.

The documents qualify the block values. The *Iliad* has mean Q 0.260925 and the *Hymn to Demeter* 0.310402; the Homeric block is dominated by the *Iliad*, with 45,515 of its 46,634 targets (Tables 1–2). In the Hesiodic block the means are 0.259376 for the *Theogony*, 0.228274 for *Works and Days* and 0.277033 for the *Shield of Heracles*. For Plutarch, the *Lycurgus* has 0.552685 and the *Alcibiades* 0.532785. The four single-document blocks repeat the values of their documents. These eleven values are not eleven independent replications: documents of one block share its exclusion and its model.

Table 6 gives the spread over seeds for every block and document. The Homeric block, for example, has SD 0.002318 and range 0.255151–0.265862; the Hesiodic block has SD 0.005909 and range 0.241140–0.262615, in bits per target over 20 seeds. The [profile panels](../results/figures/README.md#2-order-advantage-per-block-and-per-document) show single seeds, means and ranges. Neither the ranges nor the SDs measure uncertainty about authors, works or ancient Greek beyond this corpus. Chronology, tradition, genre and verse form vary together, and each block is scored by a differently trained model; the order of the profiles cannot tell these explanations apart.

**Tables 3–5 — mean cross-entropies, gains and Q in the main setting, for every block and document.** Source: [seed_summaries.csv](../results/hexis31/v3-seed0-v3006/seed_summaries.csv), main setting, blocks and documents, column `mean` over 20 seeds, in bits per target; each unit's targets are in Tables 1–2. The same source holds, for all six settings and both groups of targets, the mean, SD, minimum and maximum of every quantity.

**Table 3: all targets.**

| Block or document | Model CE, original | Frequency CE, original | Model CE, shuffled | Frequency CE, shuffled | Gain, original | Gain, shuffled | Q |
|---|---|---|---|---|---|---|---|
| Homeric tradition (block) | 4.555547 | 4.817659 | 4.724583 | 4.724583 | 0.262112 | 4.44e-17 | 0.262112 |
| Hesiodic tradition (block) | 4.670339 | 4.923330 | 4.877657 | 4.877657 | 0.252991 | 0.000000 | 0.252991 |
| Herodotus (block) | 4.393918 | 4.787068 | 4.642541 | 4.642541 | 0.393150 | 4.44e-17 | 0.393150 |
| Thucydides (block) | 4.323848 | 4.753427 | 4.613959 | 4.613959 | 0.429579 | 0.000000 | 0.429579 |
| Athenaeus (block) | 4.233885 | 4.685965 | 4.561370 | 4.561370 | 0.452080 | 8.88e-17 | 0.452080 |
| Diodorus (block) | 3.992307 | 4.518477 | 4.405177 | 4.405177 | 0.526170 | 1.33e-16 | 0.526170 |
| Plutarch (block) | 4.234179 | 4.777036 | 4.637199 | 4.637199 | 0.542858 | 0.000000 | 0.542858 |
| Iliad | 4.556667 | 4.817592 | 4.722331 | 4.722331 | 0.260925 | 4.44e-17 | 0.260925 |
| Homeric Hymn to Demeter | 4.509990 | 4.820392 | 4.816211 | 4.816211 | 0.310402 | 0.000000 | 0.310402 |
| Theogony | 4.705676 | 4.965053 | 4.942266 | 4.942266 | 0.259376 | 0.000000 | 0.259376 |
| Works and Days | 4.653625 | 4.881899 | 4.795500 | 4.795500 | 0.228274 | 1.33e-16 | 0.228274 |
| Shield of Heracles | 4.619082 | 4.896116 | 4.863144 | 4.863144 | 0.277033 | 4.44e-17 | 0.277033 |
| Histories, book 1 (Herodotus) | 4.393918 | 4.787068 | 4.642541 | 4.642541 | 0.393150 | 4.44e-17 | 0.393150 |
| Histories, book 1 (Thucydides) | 4.323848 | 4.753427 | 4.613959 | 4.613959 | 0.429579 | 0.000000 | 0.429579 |
| Deipnosophistae, books 12-13 | 4.233885 | 4.685965 | 4.561370 | 4.561370 | 0.452080 | 8.88e-17 | 0.452080 |
| Bibliotheca historica, book 11 | 3.992307 | 4.518477 | 4.405177 | 4.405177 | 0.526170 | 1.33e-16 | 0.526170 |
| Lycurgus | 4.315890 | 4.868575 | 4.705074 | 4.705074 | 0.552685 | 8.88e-17 | 0.552685 |
| Alcibiades | 4.150430 | 4.683215 | 4.567630 | 4.567630 | 0.532785 | 0.000000 | 0.532785 |

**Table 4: targets after 4–7 preceding tokens.**

| Block or document | Model CE, original | Frequency CE, original | Model CE, shuffled | Frequency CE, shuffled | Gain, original | Gain, shuffled | Q |
|---|---|---|---|---|---|---|---|
| Homeric tradition (block) | 4.477913 | 4.733888 | 4.708097 | 4.708097 | 0.255975 | 1.33e-16 | 0.255975 |
| Hesiodic tradition (block) | 4.556054 | 4.847359 | 4.844516 | 4.844516 | 0.291305 | 4.44e-17 | 0.291305 |
| Herodotus (block) | 4.315565 | 4.691483 | 4.621264 | 4.621264 | 0.375918 | 4.44e-17 | 0.375918 |
| Thucydides (block) | 4.216529 | 4.648209 | 4.585934 | 4.585934 | 0.431680 | 4.44e-17 | 0.431680 |
| Athenaeus (block) | 4.171896 | 4.605758 | 4.532228 | 4.532228 | 0.433863 | 1.78e-16 | 0.433863 |
| Diodorus (block) | 3.880698 | 4.372812 | 4.372352 | 4.372352 | 0.492114 | 8.88e-17 | 0.492114 |
| Plutarch (block) | 4.158536 | 4.658718 | 4.588694 | 4.588694 | 0.500182 | 1.33e-16 | 0.500182 |
| Iliad | 4.476794 | 4.732908 | 4.706760 | 4.706760 | 0.256114 | 8.88e-17 | 0.256114 |
| Homeric Hymn to Demeter | 4.526268 | 4.776215 | 4.765851 | 4.765851 | 0.249948 | 0.000000 | 0.249948 |
| Theogony | 4.532573 | 4.864426 | 4.876013 | 4.876013 | 0.331853 | 4.44e-17 | 0.331853 |
| Works and Days | 4.637553 | 4.876956 | 4.804010 | 4.804010 | 0.239402 | 8.88e-17 | 0.239402 |
| Shield of Heracles | 4.468950 | 4.773869 | 4.855383 | 4.855383 | 0.304919 | 8.88e-17 | 0.304919 |
| Histories, book 1 (Herodotus) | 4.315565 | 4.691483 | 4.621264 | 4.621264 | 0.375918 | 4.44e-17 | 0.375918 |
| Histories, book 1 (Thucydides) | 4.216529 | 4.648209 | 4.585934 | 4.585934 | 0.431680 | 4.44e-17 | 0.431680 |
| Deipnosophistae, books 12-13 | 4.171896 | 4.605758 | 4.532228 | 4.532228 | 0.433863 | 1.78e-16 | 0.433863 |
| Bibliotheca historica, book 11 | 3.880698 | 4.372812 | 4.372352 | 4.372352 | 0.492114 | 8.88e-17 | 0.492114 |
| Lycurgus | 4.185436 | 4.708838 | 4.647579 | 4.647579 | 0.523402 | 4.44e-17 | 0.523402 |
| Alcibiades | 4.131342 | 4.608050 | 4.529165 | 4.529165 | 0.476708 | 8.88e-17 | 0.476708 |

**Table 5: targets after 8 or more preceding tokens.**

| Block or document | Model CE, original | Frequency CE, original | Model CE, shuffled | Frequency CE, shuffled | Gain, original | Gain, shuffled | Q |
|---|---|---|---|---|---|---|---|
| Homeric tradition (block) | 4.615085 | 4.881905 | 4.737227 | 4.737227 | 0.266819 | 0.000000 | 0.266819 |
| Hesiodic tradition (block) | 4.739573 | 4.969353 | 4.897733 | 4.897733 | 0.229780 | 0.000000 | 0.229780 |
| Herodotus (block) | 4.428661 | 4.829452 | 4.651975 | 4.651975 | 0.400791 | 8.88e-17 | 0.400791 |
| Thucydides (block) | 4.364599 | 4.793381 | 4.624601 | 4.624601 | 0.428782 | 4.44e-17 | 0.428782 |
| Athenaeus (block) | 4.265530 | 4.726910 | 4.576247 | 4.576247 | 0.461379 | 1.33e-16 | 0.461379 |
| Diodorus (block) | 4.026584 | 4.563214 | 4.415258 | 4.415258 | 0.536629 | 8.88e-17 | 0.536629 |
| Plutarch (block) | 4.261680 | 4.820053 | 4.654833 | 4.654833 | 0.558373 | 4.44e-17 | 0.558373 |
| Iliad | 4.618075 | 4.882699 | 4.734302 | 4.734302 | 0.264624 | 4.44e-17 | 0.264624 |
| Homeric Hymn to Demeter | 4.498711 | 4.851001 | 4.851105 | 4.851105 | 0.352290 | 4.44e-17 | 0.352290 |
| Theogony | 4.787086 | 5.012377 | 4.973425 | 4.973425 | 0.225291 | 0.000000 | 0.225291 |
| Works and Days | 4.665604 | 4.885584 | 4.789156 | 4.789156 | 0.219980 | 4.44e-17 | 0.219980 |
| Shield of Heracles | 4.730378 | 4.986739 | 4.868897 | 4.868897 | 0.256361 | 0.000000 | 0.256361 |
| Histories, book 1 (Herodotus) | 4.428661 | 4.829452 | 4.651975 | 4.651975 | 0.400791 | 8.88e-17 | 0.400791 |
| Histories, book 1 (Thucydides) | 4.364599 | 4.793381 | 4.624601 | 4.624601 | 0.428782 | 4.44e-17 | 0.428782 |
| Deipnosophistae, books 12-13 | 4.265530 | 4.726910 | 4.576247 | 4.576247 | 0.461379 | 1.33e-16 | 0.461379 |
| Bibliotheca historica, book 11 | 4.026584 | 4.563214 | 4.415258 | 4.415258 | 0.536629 | 8.88e-17 | 0.536629 |
| Lycurgus | 4.362880 | 4.926112 | 4.725784 | 4.725784 | 0.563232 | 4.44e-17 | 0.563232 |
| Alcibiades | 4.157436 | 4.710803 | 4.581748 | 4.581748 | 0.553367 | 0.000000 | 0.553367 |

**Table 6 — spread of Q over seeds, main setting.** Same source as Tables 3–5, quantity Q. Each entry is **mean / SD / minimum / maximum** over 20 seeds, in bits per target. The spread of the other quantities is in the same source; no SD or extreme is averaged across units.

| Block or document | All targets: mean / SD / min / max | 4–7: mean / SD / min / max | ≥8: mean / SD / min / max |
|---|---|---|---|
| Homeric tradition (block) | 0.262112 / 0.002318 / 0.255151 / 0.265862 | 0.255975 / 0.002767 / 0.247406 / 0.260333 | 0.266819 / 0.002306 / 0.261091 / 0.270102 |
| Hesiodic tradition (block) | 0.252991 / 0.005909 / 0.241140 / 0.262615 | 0.291305 / 0.003463 / 0.285084 / 0.300607 | 0.229780 / 0.009704 / 0.211525 / 0.244282 |
| Herodotus (block) | 0.393150 / 0.002549 / 0.388604 / 0.396779 | 0.375918 / 0.003878 / 0.368083 / 0.382311 | 0.400791 / 0.002461 / 0.395584 / 0.404595 |
| Thucydides (block) | 0.429579 / 0.002932 / 0.424545 / 0.434837 | 0.431680 / 0.005159 / 0.418265 / 0.438820 | 0.428782 / 0.002895 / 0.423241 / 0.435230 |
| Athenaeus (block) | 0.452080 / 0.001850 / 0.448172 / 0.455421 | 0.433863 / 0.002786 / 0.429777 / 0.438473 | 0.461379 / 0.002067 / 0.456726 / 0.465852 |
| Diodorus (block) | 0.526170 / 0.001907 / 0.522185 / 0.528965 | 0.492114 / 0.003483 / 0.485031 / 0.499240 | 0.536629 / 0.002277 / 0.531753 / 0.540485 |
| Plutarch (block) | 0.542858 / 0.003466 / 0.536831 / 0.549146 | 0.500182 / 0.005478 / 0.491138 / 0.511872 | 0.558373 / 0.003683 / 0.550327 / 0.565281 |
| Iliad | 0.260925 / 0.002291 / 0.254166 / 0.264647 | 0.256114 / 0.002716 / 0.247667 / 0.260152 | 0.264624 / 0.002320 / 0.258808 / 0.268103 |
| Homeric Hymn to Demeter | 0.310402 / 0.007308 / 0.291010 / 0.319645 | 0.249948 / 0.010015 / 0.224712 / 0.268158 | 0.352290 / 0.007889 / 0.336169 / 0.365914 |
| Theogony | 0.259376 / 0.012746 / 0.229129 / 0.279556 | 0.331853 / 0.008230 / 0.320893 / 0.346012 | 0.225291 / 0.017569 / 0.185973 / 0.249684 |
| Works and Days | 0.228274 / 0.003938 / 0.220799 / 0.233793 | 0.239402 / 0.006746 / 0.225641 / 0.251901 | 0.219980 / 0.005922 / 0.210206 / 0.231469 |
| Shield of Heracles | 0.277033 / 0.007231 / 0.264111 / 0.290499 | 0.304919 / 0.010675 / 0.289196 / 0.323606 | 0.256361 / 0.009372 / 0.241328 / 0.273345 |
| Histories, book 1 (Herodotus) | 0.393150 / 0.002549 / 0.388604 / 0.396779 | 0.375918 / 0.003878 / 0.368083 / 0.382311 | 0.400791 / 0.002461 / 0.395584 / 0.404595 |
| Histories, book 1 (Thucydides) | 0.429579 / 0.002932 / 0.424545 / 0.434837 | 0.431680 / 0.005159 / 0.418265 / 0.438820 | 0.428782 / 0.002895 / 0.423241 / 0.435230 |
| Deipnosophistae, books 12-13 | 0.452080 / 0.001850 / 0.448172 / 0.455421 | 0.433863 / 0.002786 / 0.429777 / 0.438473 | 0.461379 / 0.002067 / 0.456726 / 0.465852 |
| Bibliotheca historica, book 11 | 0.526170 / 0.001907 / 0.522185 / 0.528965 | 0.492114 / 0.003483 / 0.485031 / 0.499240 | 0.536629 / 0.002277 / 0.531753 / 0.540485 |
| Lycurgus | 0.552685 / 0.003921 / 0.546292 / 0.560823 | 0.523402 / 0.007351 / 0.514594 / 0.542218 | 0.563232 / 0.004283 / 0.553102 / 0.569629 |
| Alcibiades | 0.532785 / 0.004046 / 0.524340 / 0.539983 | 0.476708 / 0.008946 / 0.456651 / 0.489381 | 0.553367 / 0.004069 / 0.545574 / 0.562361 |

## Hexameter and prose

With every block weighing the same, the mean Q in the main setting is 0.257551 for hexameter and 0.468767 for prose; their difference is −0.211216 bits per target. With every target weighing the same, the averages are 0.261015 and 0.463038, and the difference is −0.202023 (Table 8). The two differences have SDs 0.003639 and 0.002754 and ranges −0.217762 to −0.204675 and −0.209126 to −0.197321 over seeds (Table 9). They are two descriptions of the same procedure: the average block and the average target of each group.

Weighting by targets gives the Hesiodic block a share of 0.120263 of the hexameter average instead of 0.500000 (Table 10), increasing the weight of the Homeric material. Neither weighting corrects the other, and neither balances chronology, annotation or training. In the main setting, hexameter makes up 0.166667 of the training tokens when a hexameter block is held out and 0.333333 when a prose block is held out (Table 10): the group difference compares blocks scored by models trained on different mixtures, not texts scored by one common model.

The mean hexameter − prose difference in Q is negative in every setting and with both weightings, and every range over seeds is also below zero (Tables 8–9). For the weaker prior the two means are −0.222067 and −0.209439; for half training data −0.177569 and −0.165288; for depth 12 −0.209560 and −0.200845; for other relations kept −0.203113 and −0.193254; for part of speech only −0.237546 and −0.230473 (blocks equal, then targets equal). The seven block means of Q stay positive in all six settings (source of Tables 3–5). Reporting these signs does not make agreement between seeds a criterion of success or a statistical test. Because the main setting has 20 seeds and the variants ten, differences between the setting means printed here are not the paired changes; those are in Tables 11–13.

**Table 7 — targets per group and number of seeds.** Source: [contrasts.csv](../results/hexis31/v3-seed0-v3006/contrasts.csv), seed 0, column `n` (targets per seed); the number of seeds from `seed_summaries.csv`. The populations are the same under both weightings and in every seed; only the weights differ (Table 10). Hexameter has two blocks, prose five; the difference has no target count of its own.

| Setting | Hexameter targets | Prose targets | Seeds |
|---|---|---|---|
| Main | 53009 | 56099 | 20 |
| Weaker prior | 53009 | 56099 | 10 |
| Half training data | 53009 | 56099 | 10 |
| Depth 12 | 53009 | 56099 | 10 |
| Other relations kept | 53460 | 56256 | 10 |
| Part of speech only | 53009 | 56099 | 10 |

**Table 8 — hexameter, prose and their difference, both weightings.** Source: [seed_summaries.csv](../results/hexis31/v3-seed0-v3006/seed_summaries.csv), groups, all targets, column `mean`, in bits per target, over 20 seeds in the main setting and 10 elsewhere. [contrasts.csv](../results/hexis31/v3-seed0-v3006/contrasts.csv) holds every seed. Blocks-equal averages use two hexameter and five prose blocks; targets-equal averages use their total targets. No pooled target count is assigned to the difference.

| Setting | Group or difference | Averaging | Model CE, original | Frequency CE, original | Model CE, shuffled | Frequency CE, shuffled | Gain, original | Gain, shuffled | Q |
|---|---|---|---|---|---|---|---|---|---|
| Main | Hexameter | Blocks equal | 4.612943 | 4.870495 | 4.801120 | 4.801120 | 0.257551 | 2.22e-17 | 0.257551 |
| Main | Hexameter | Targets equal | 4.569352 | 4.830368 | 4.742992 | 4.742992 | 0.261015 | 3.91e-17 | 0.261015 |
| Main | Prose | Blocks equal | 4.235627 | 4.704395 | 4.572049 | 4.572049 | 0.468767 | 5.33e-17 | 0.468767 |
| Main | Prose | Targets equal | 4.229328 | 4.692366 | 4.561864 | 4.561864 | 0.463038 | 6.60e-17 | 0.463038 |
| Main | Hexameter − prose | Blocks equal | 0.377316 | 0.166100 | 0.229071 | 0.229071 | -0.211216 | -3.11e-17 | -0.211216 |
| Main | Hexameter − prose | Targets equal | 0.340024 | 0.138001 | 0.181128 | 0.181128 | -0.202023 | -2.69e-17 | -0.202023 |
| Weaker prior | Hexameter | Blocks equal | 4.632902 | 4.869793 | 4.801216 | 4.801216 | 0.236892 | 1.78e-16 | 0.236892 |
| Weaker prior | Hexameter | Targets equal | 4.585415 | 4.830287 | 4.743709 | 4.743709 | 0.244873 | 1.10e-16 | 0.244873 |
| Weaker prior | Prose | Blocks equal | 4.246784 | 4.705743 | 4.572853 | 4.572853 | 0.458959 | 1.60e-16 | 0.458959 |
| Weaker prior | Prose | Targets equal | 4.239279 | 4.693591 | 4.562698 | 4.562698 | 0.454311 | 1.56e-16 | 0.454311 |
| Weaker prior | Hexameter − prose | Blocks equal | 0.386118 | 0.164050 | 0.228363 | 0.228363 | -0.222067 | 1.78e-17 | -0.222067 |
| Weaker prior | Hexameter − prose | Targets equal | 0.346135 | 0.136697 | 0.181011 | 0.181011 | -0.209439 | -4.56e-17 | -0.209439 |
| Half training data | Hexameter | Blocks equal | 4.662253 | 4.871714 | 4.803216 | 4.803216 | 0.209460 | 1.33e-16 | 0.209460 |
| Half training data | Hexameter | Targets equal | 4.616769 | 4.832092 | 4.745695 | 4.745695 | 0.215323 | 1.67e-16 | 0.215323 |
| Half training data | Prose | Blocks equal | 4.318190 | 4.705219 | 4.572633 | 4.572633 | 0.387029 | 8.88e-17 | 0.387029 |
| Half training data | Prose | Targets equal | 4.312488 | 4.693099 | 4.562482 | 4.562482 | 0.380611 | 7.33e-17 | 0.380611 |
| Half training data | Hexameter − prose | Blocks equal | 0.344063 | 0.166494 | 0.230583 | 0.230583 | -0.177569 | 4.44e-17 | -0.177569 |
| Half training data | Hexameter − prose | Targets equal | 0.304281 | 0.138993 | 0.183212 | 0.183212 | -0.165288 | 9.36e-17 | -0.165288 |
| Depth 12 | Hexameter | Blocks equal | 4.610482 | 4.869292 | 4.800729 | 4.800729 | 0.258810 | 0.000000 | 0.258810 |
| Depth 12 | Hexameter | Targets equal | 4.568243 | 4.830146 | 4.743386 | 4.743386 | 0.261903 | 0.000000 | 0.261903 |
| Depth 12 | Prose | Blocks equal | 4.236087 | 4.704457 | 4.571742 | 4.571742 | 0.468370 | 3.55e-17 | 0.468370 |
| Depth 12 | Prose | Targets equal | 4.229653 | 4.692401 | 4.561638 | 4.561638 | 0.462748 | 4.60e-17 | 0.462748 |
| Depth 12 | Hexameter − prose | Blocks equal | 0.374395 | 0.164836 | 0.228987 | 0.228987 | -0.209560 | -3.55e-17 | -0.209560 |
| Depth 12 | Hexameter − prose | Targets equal | 0.338590 | 0.137745 | 0.181749 | 0.181749 | -0.200845 | -4.60e-17 | -0.200845 |
| Other relations kept | Hexameter | Blocks equal | 4.627883 | 4.883097 | 4.824585 | 4.824585 | 0.255214 | 0.000000 | 0.255214 |
| Other relations kept | Hexameter | Targets equal | 4.587044 | 4.845707 | 4.773379 | 4.773379 | 0.258664 | 0.000000 | 0.258664 |
| Other relations kept | Prose | Blocks equal | 4.255230 | 4.713557 | 4.582755 | 4.582755 | 0.458327 | -7.11e-17 | 0.458327 |
| Other relations kept | Prose | Targets equal | 4.251272 | 4.703189 | 4.574596 | 4.574596 | 0.451917 | -4.47e-17 | 0.451917 |
| Other relations kept | Hexameter − prose | Blocks equal | 0.372653 | 0.169540 | 0.241830 | 0.241830 | -0.203113 | 7.11e-17 | -0.203113 |
| Other relations kept | Hexameter − prose | Targets equal | 0.335771 | 0.142518 | 0.198782 | 0.198782 | -0.193254 | 4.47e-17 | -0.193254 |
| Part of speech only | Hexameter | Blocks equal | 2.768024 | 2.815518 | 2.856816 | 2.856816 | 0.047494 | 4.44e-17 | 0.047494 |
| Part of speech only | Hexameter | Targets equal | 2.769984 | 2.824711 | 2.871325 | 2.871325 | 0.054726 | 1.07e-17 | 0.054726 |
| Part of speech only | Prose | Blocks equal | 2.722536 | 3.007576 | 3.004457 | 3.004457 | 0.285040 | 4.07e-07 | 0.285040 |
| Part of speech only | Prose | Targets equal | 2.715452 | 3.000651 | 3.000932 | 3.000932 | 0.285200 | 2.51e-07 | 0.285199 |
| Part of speech only | Hexameter − prose | Blocks equal | 0.045488 | -0.192058 | -0.147641 | -0.147641 | -0.237547 | -4.07e-07 | -0.237546 |
| Part of speech only | Hexameter − prose | Targets equal | 0.054533 | -0.175940 | -0.129606 | -0.129607 | -0.230473 | -2.51e-07 | -0.230473 |

**Table 9 — spread of Q over seeds for the groups and their difference.** Same source and units as Table 8, quantity Q; each entry is **mean / SD / minimum / maximum**. The spread of every other quantity is in the same source.

| Setting | Group or difference | Seeds | Blocks equal: mean / SD / min / max | Targets equal: mean / SD / min / max |
|---|---|---|---|---|
| Main | Hexameter | 20 | 0.257551 / 0.003216 / 0.252135 / 0.263457 | 0.261015 / 0.002186 / 0.254986 / 0.265283 |
| Main | Prose | 20 | 0.468767 / 0.001510 / 0.465391 / 0.470672 | 0.463038 / 0.001339 / 0.459990 / 0.464924 |
| Main | Hexameter − prose | 20 | -0.211216 / 0.003639 / -0.217762 / -0.204675 | -0.202023 / 0.002754 / -0.209126 / -0.197321 |
| Weaker prior | Hexameter | 10 | 0.236892 / 0.006868 / 0.225652 / 0.244100 | 0.244873 / 0.003058 / 0.239942 / 0.248582 |
| Weaker prior | Prose | 10 | 0.458959 / 0.003390 / 0.453831 / 0.463692 | 0.454311 / 0.003512 / 0.449801 / 0.460061 |
| Weaker prior | Hexameter − prose | 10 | -0.222067 / 0.007928 / -0.236100 / -0.212708 | -0.209439 / 0.004073 / -0.217533 / -0.203403 |
| Half training data | Hexameter | 10 | 0.209460 / 0.006919 / 0.196467 / 0.219545 | 0.215323 / 0.006622 / 0.208108 / 0.226970 |
| Half training data | Prose | 10 | 0.387029 / 0.003381 / 0.382596 / 0.391389 | 0.380611 / 0.003539 / 0.376177 / 0.385585 |
| Half training data | Hexameter − prose | 10 | -0.177569 / 0.007330 / -0.189084 / -0.167704 | -0.165288 / 0.008210 / -0.176259 / -0.154141 |
| Depth 12 | Hexameter | 10 | 0.258810 / 0.003422 / 0.252135 / 0.263457 | 0.261903 / 0.001642 / 0.260046 / 0.265283 |
| Depth 12 | Prose | 10 | 0.468370 / 0.001837 / 0.465391 / 0.470672 | 0.462748 / 0.001699 / 0.459990 / 0.464924 |
| Depth 12 | Hexameter − prose | 10 | -0.209560 / 0.003481 / -0.215566 / -0.204675 | -0.200845 / 0.002344 / -0.204879 / -0.197321 |
| Other relations kept | Hexameter | 10 | 0.255214 / 0.003708 / 0.248681 / 0.260299 | 0.258664 / 0.002209 / 0.255261 / 0.262305 |
| Other relations kept | Prose | 10 | 0.458327 / 0.005513 / 0.450781 / 0.465553 | 0.451917 / 0.005811 / 0.444222 / 0.459488 |
| Other relations kept | Hexameter − prose | 10 | -0.203113 / 0.005876 / -0.212309 / -0.194089 | -0.193254 / 0.006615 / -0.204227 / -0.185222 |
| Part of speech only | Hexameter | 10 | 0.047494 / 0.002084 / 0.043789 / 0.050215 | 0.054726 / 0.001875 / 0.050874 / 0.057148 |
| Part of speech only | Prose | 10 | 0.285040 / 0.002038 / 0.282827 / 0.288896 | 0.285199 / 0.002135 / 0.283051 / 0.289145 |
| Part of speech only | Hexameter − prose | 10 | -0.237546 / 0.003081 / -0.242562 / -0.234172 | -0.230473 / 0.002836 / -0.234060 / -0.226157 |

**Table 10 — targets and weights.** Source: [aggregation_weights.csv](../results/hexis31/v3-seed0-v3006/aggregation_weights.csv), seed 0, main setting, other relations kept and half training data. *Targets* are those of the held-out block; its *shares* are its weights within its group. *Training tokens taken / available* is the block's quota when it contributes to training and the kept tokens it has; *share taken* is their ratio. The last three columns describe the training of the model that scores the named block. Shares are fractions, not percentages. The weaker prior, depth 12 and part of speech only share the main-setting values; other relations kept changes the populations, half training data the quota. The complete source covers every seed and setting.

| Setting / block | Targets | Share, blocks equal | Share, targets equal | Training tokens taken / available | Share taken | Training tokens of the model | Hexameter share of training | Prose share of training |
|---|---|---|---|---|---|---|---|---|
| Main / Homeric tradition | 46634 | 0.500000 | 0.879737 | 8884 / 71088 | 0.124972 | 53304 | 0.166667 | 0.833333 |
| Main / Hesiodic tradition | 6375 | 0.500000 | 0.120263 | 8884 / 9282 | 0.957121 | 53304 | 0.166667 | 0.833333 |
| Main / Herodotus | 12946 | 0.200000 | 0.230771 | 8884 / 17301 | 0.513496 | 53304 | 0.333333 | 0.666667 |
| Main / Thucydides | 7227 | 0.200000 | 0.128826 | 8884 / 9346 | 0.950567 | 53304 | 0.333333 | 0.666667 |
| Main / Athenaeus | 16691 | 0.200000 | 0.297528 | 8884 / 23133 | 0.384040 | 53304 | 0.333333 | 0.666667 |
| Main / Diodorus | 12334 | 0.200000 | 0.219861 | 8884 / 15266 | 0.581947 | 53304 | 0.333333 | 0.666667 |
| Main / Plutarch | 6901 | 0.200000 | 0.123015 | 8884 / 8884 | 1.000000 | 53304 | 0.333333 | 0.666667 |
| Other relations kept / Homeric tradition | 47062 | 0.500000 | 0.880322 | 8884 / 71547 | 0.124170 | 53304 | 0.166667 | 0.833333 |
| Other relations kept / Hesiodic tradition | 6398 | 0.500000 | 0.119678 | 8884 / 9308 | 0.954448 | 53304 | 0.166667 | 0.833333 |
| Other relations kept / Herodotus | 12994 | 0.200000 | 0.230980 | 8884 / 17349 | 0.512076 | 53304 | 0.333333 | 0.666667 |
| Other relations kept / Thucydides | 7234 | 0.200000 | 0.128591 | 8884 / 9353 | 0.949856 | 53304 | 0.333333 | 0.666667 |
| Other relations kept / Athenaeus | 16786 | 0.200000 | 0.298386 | 8884 / 23231 | 0.382420 | 53304 | 0.333333 | 0.666667 |
| Other relations kept / Diodorus | 12334 | 0.200000 | 0.219248 | 8884 / 15266 | 0.581947 | 53304 | 0.333333 | 0.666667 |
| Other relations kept / Plutarch | 6908 | 0.200000 | 0.122796 | 8884 / 8893 | 0.998988 | 53304 | 0.333333 | 0.666667 |
| Half training data / Homeric tradition | 46634 | 0.500000 | 0.879737 | 4442 / 71088 | 0.062486 | 26652 | 0.166667 | 0.833333 |
| Half training data / Hesiodic tradition | 6375 | 0.500000 | 0.120263 | 4442 / 9282 | 0.478561 | 26652 | 0.166667 | 0.833333 |
| Half training data / Herodotus | 12946 | 0.200000 | 0.230771 | 4442 / 17301 | 0.256748 | 26652 | 0.333333 | 0.666667 |
| Half training data / Thucydides | 7227 | 0.200000 | 0.128826 | 4442 / 9346 | 0.475284 | 26652 | 0.333333 | 0.666667 |
| Half training data / Athenaeus | 16691 | 0.200000 | 0.297528 | 4442 / 23133 | 0.192020 | 26652 | 0.333333 | 0.666667 |
| Half training data / Diodorus | 12334 | 0.200000 | 0.219861 | 4442 / 15266 | 0.290973 | 26652 | 0.333333 | 0.666667 |
| Half training data / Plutarch | 6901 | 0.200000 | 0.123015 | 4442 / 8884 | 0.500000 | 26652 | 0.333333 | 0.666667 |

## Sensitivity to the analysis choices

The paired changes compare each variant with the main setting on seeds 0–9, under both weightings. With the weaker prior the mean change of the hexameter − prose difference is −0.012507 with blocks equal and −0.008594 with targets equal (Table 12). The blocks do not move alike: Diodorus increases by 0.033702, while the other six decrease (Table 11), and Plutarch's paired range spans −0.026928 to 0.001497. These are observed responses to the change of this prior; no single context or annotation is identified as their cause. The prior on how often the model stops at a shorter context is not varied.

Halving the training data reduces the mean Q of all seven blocks. The difference changes by +0.031991 and +0.035557 under the two weightings, moving closer to zero (Tables 11–12). This compares two fixed training sizes; it is not a learning curve and does not show that the change is linear. Keeping the other relations also reduces all seven block means, and changes the difference by +0.006447 and +0.007591. It changes the kept symbols, the inventory of symbols, the end of the training sample and the scored positions: its difference is a comparison of two tasks, not the isolated effect of adding one label.

Raising the maximum depth from eight to twelve changes the mean difference by −1.47e-10 and −1.07e-10 bits per target. These tiny values are kept in Tables 11–13: the two hexameter blocks show exactly zero change, several prose blocks small nonzero changes. The deeper model changes the measured gains only at these scales. This does not show that there are no dependencies beyond eight symbols, nor that longer structure could be learned from this training. The visible difference between the main and depth-12 means in Table 8 also reflects their different numbers of seeds.

Part of speech only changes the mean difference by −0.027986 and −0.029628. It scores the same positions as the main setting, but its smaller set of symbols changes the prediction task and the total prior. A lower cross-entropy or a difference of the same sign cannot be read as a measure of how much the relations contribute, and subtracting one setting from the other does not isolate that contribution. Table 13 keeps every component of the paired change beside Q.

The two groups of targets by preceding tokens, fixed in the plan, give a further description (Tables 4–6). For the Homeric block the mean Q is 0.255975 after 4–7 tokens and 0.266819 after 8 or more; the Hesiodic mean instead falls from 0.291305 to 0.229780. Herodotus, Athenaeus, Diodorus and Plutarch are higher in the second group, while Thucydides moves from 0.431680 to 0.428782. Among documents, the *Hymn* moves from 0.249948 to 0.352290 and the *Theogony* from 0.331853 to 0.225291. The two groups contain different positions and mixtures of sentence lengths: they are not experiments on context length. With depth 12, a target preceded by 8 or more tokens need not have twelve. No other grouping of targets and no selection of contexts after the fact is used.

The [sensitivity panels](../results/figures/README.md#3-sensitivity-to-the-analysis-choices-and-the-two-ways-of-averaging) show the differences in every setting, the paired changes and the block means for each group of targets.

**Tables 11–12 — paired changes of Q.** Sources: [sensitivity_pairs.csv](../results/hexis31/v3-seed0-v3006/sensitivity_pairs.csv) (each seed) and [seed_summaries.csv](../results/hexis31/v3-seed0-v3006/seed_summaries.csv) (their summaries); all targets, the five variants. Every entry is **mean / SD / minimum / maximum** of *variant − main setting* over seeds 0–9, in bits per target. Each side uses its own targets; with other relations kept these differ, and pairing the seeds does not make the two tasks equal. The 20-seed mean of the main setting is never subtracted. Every quantity and both groups of targets for blocks are in the linked sources; there are no document-level changes and no group differences by group of targets.

**Table 11: blocks.**

| Setting | Block | ΔQ: mean / SD / min / max (10 seeds) |
|---|---|---|
| Weaker prior | Homeric tradition | -0.015483 / 0.003223 / -0.020447 / -0.010235 |
| Weaker prior | Hesiodic tradition | -0.028353 / 0.011589 / -0.051210 / -0.017593 |
| Weaker prior | Herodotus | -0.031210 / 0.003654 / -0.039306 / -0.026207 |
| Weaker prior | Thucydides | -0.023760 / 0.005404 / -0.032646 / -0.014981 |
| Weaker prior | Athenaeus | -0.013819 / 0.005657 / -0.023024 / -0.003844 |
| Weaker prior | Diodorus | 0.033702 / 0.003796 / 0.026602 / 0.038211 |
| Weaker prior | Plutarch | -0.011967 / 0.008285 / -0.026928 / 0.001497 |
| Half training data | Homeric tradition | -0.045703 / 0.008675 / -0.061376 / -0.032304 |
| Half training data | Hesiodic tradition | -0.052996 / 0.013293 / -0.068737 / -0.026446 |
| Half training data | Herodotus | -0.078796 / 0.004198 / -0.084926 / -0.071903 |
| Half training data | Thucydides | -0.062612 / 0.003738 / -0.067233 / -0.055237 |
| Half training data | Athenaeus | -0.080627 / 0.004565 / -0.086353 / -0.073051 |
| Half training data | Diodorus | -0.094805 / 0.006059 / -0.102723 / -0.081424 |
| Half training data | Plutarch | -0.089863 / 0.004640 / -0.098617 / -0.084316 |
| Depth 12 | Homeric tradition | 0.000000 / 0.000000 / 0.000000 / 0.000000 |
| Depth 12 | Hesiodic tradition | 0.000000 / 0.000000 / 0.000000 / 0.000000 |
| Depth 12 | Herodotus | 8.50e-14 / 2.57e-13 / 0.000000 / 8.14e-13 |
| Depth 12 | Thucydides | 1.28e-11 / 3.66e-11 / 0.000000 / 1.17e-10 |
| Depth 12 | Athenaeus | 9.12e-11 / 2.40e-10 / 0.000000 / 7.64e-10 |
| Depth 12 | Diodorus | 0.000000 / 0.000000 / 0.000000 / 0.000000 |
| Depth 12 | Plutarch | 6.32e-10 / 1.17e-09 / 0.000000 / 3.51e-09 |
| Other relations kept | Homeric tradition | -0.003134 / 0.000830 / -0.004758 / -0.002028 |
| Other relations kept | Hesiodic tradition | -0.004058 / 0.000675 / -0.004998 / -0.002973 |
| Other relations kept | Herodotus | -0.006349 / 0.000528 / -0.007278 / -0.005303 |
| Other relations kept | Thucydides | -0.004856 / 0.000465 / -0.005687 / -0.004099 |
| Other relations kept | Athenaeus | -0.006853 / 0.000681 / -0.008416 / -0.006226 |
| Other relations kept | Diodorus | -0.027731 / 0.025441 / -0.053360 / -0.002403 |
| Other relations kept | Plutarch | -0.004425 / 0.000376 / -0.005075 / -0.003782 |
| Part of speech only | Homeric tradition | -0.205866 / 0.003258 / -0.213970 / -0.201874 |
| Part of speech only | Hesiodic tradition | -0.216767 / 0.007606 / -0.226872 / -0.200224 |
| Part of speech only | Herodotus | -0.149124 / 0.002344 / -0.152887 / -0.146287 |
| Part of speech only | Thucydides | -0.185833 / 0.004414 / -0.191301 / -0.176748 |
| Part of speech only | Athenaeus | -0.189830 / 0.003823 / -0.194636 / -0.183502 |
| Part of speech only | Diodorus | -0.149833 / 0.001946 / -0.152254 / -0.146433 |
| Part of speech only | Plutarch | -0.242031 / 0.004724 / -0.246947 / -0.233242 |

**Table 12: groups and their difference.**

| Setting | Group or difference | Blocks equal, ΔQ: mean / SD / min / max | Targets equal, ΔQ: mean / SD / min / max |
|---|---|---|---|
| Weaker prior | Hexameter | -0.021918 / 0.005423 / -0.033372 / -0.016050 | -0.017031 / 0.002668 / -0.020104 / -0.013263 |
| Weaker prior | Prose | -0.009411 / 0.002530 / -0.013273 / -0.005842 | -0.008437 / 0.002686 / -0.011853 / -0.003988 |
| Weaker prior | Hexameter − prose | -0.012507 / 0.007104 / -0.027529 / -0.006208 | -0.008594 / 0.003351 / -0.015835 / -0.005406 |
| Half training data | Hexameter | -0.049350 / 0.005608 / -0.056928 / -0.041442 | -0.046580 / 0.006888 / -0.057175 / -0.034987 |
| Half training data | Prose | -0.081341 / 0.002453 / -0.085438 / -0.076759 | -0.082137 / 0.002889 / -0.086532 / -0.076649 |
| Half training data | Hexameter − prose | 0.031991 / 0.005564 / 0.025453 / 0.041245 | 0.035557 / 0.008034 / 0.022729 / 0.045450 |
| Depth 12 | Hexameter | 0.000000 / 0.000000 / 0.000000 / 0.000000 | 0.000000 / 0.000000 / 0.000000 / 0.000000 |
| Depth 12 | Prose | 1.47e-10 / 2.37e-10 / 2.56e-14 / 7.27e-10 | 1.07e-10 / 1.59e-10 / 1.65e-14 / 4.69e-10 |
| Depth 12 | Hexameter − prose | -1.47e-10 / 2.37e-10 / -7.27e-10 / -2.56e-14 | -1.07e-10 / 1.59e-10 / -4.69e-10 / -1.65e-14 |
| Other relations kept | Hexameter | -0.003596 / 0.000673 / -0.004878 / -0.002735 | -0.003240 / 0.000782 / -0.004784 / -0.002273 |
| Other relations kept | Prose | -0.010043 / 0.005172 / -0.015410 / -0.004858 | -0.010831 / 0.005653 / -0.016763 / -0.005244 |
| Other relations kept | Hexameter − prose | 0.006447 / 0.005391 / 0.000241 / 0.012083 | 0.007591 / 0.005901 / 0.000652 / 0.013579 |
| Part of speech only | Hexameter | -0.211316 / 0.004349 / -0.217380 / -0.202808 | -0.207177 / 0.003132 / -0.214409 / -0.203024 |
| Part of speech only | Prose | -0.183330 / 0.002345 / -0.186673 / -0.178806 | -0.177549 / 0.002139 / -0.180619 / -0.173158 |
| Part of speech only | Hexameter − prose | -0.027986 / 0.003605 / -0.036513 / -0.024003 | -0.029628 / 0.002890 / -0.034848 / -0.026339 |

**Table 13 — all components of the paired change of the hexameter − prose difference.** Same sources and units; column `mean` over 10 seeds. It shows the direction of each change of cross-entropy and gain beside the change of Q; the spread and the separate hexameter and prose components are in the same source.

| Setting | Averaging | Δ Model CE, original | Δ Frequency CE, original | Δ Model CE, shuffled | Δ Frequency CE, shuffled | Δ Gain, original | Δ Gain, shuffled | ΔQ |
|---|---|---|---|---|---|---|---|---|
| Weaker prior | Blocks equal | 0.011722 | -0.000785 | -0.000624 | -0.000624 | -0.012507 | 5.33e-17 | -0.012507 |
| Weaker prior | Targets equal | 0.007545 | -0.001049 | -0.000737 | -0.000737 | -0.008594 | 3.14e-19 | -0.008594 |
| Half training data | Blocks equal | -0.030332 | 0.001659 | 0.001596 | 0.001596 | 0.031991 | 7.99e-17 | 0.031991 |
| Half training data | Targets equal | -0.034309 | 0.001248 | 0.001464 | 0.001464 | 0.035557 | 1.40e-16 | 0.035557 |
| Depth 12 | Blocks equal | 1.47e-10 | 0.000000 | 0.000000 | 0.000000 | -1.47e-10 | 0.000000 | -1.47e-10 |
| Depth 12 | Targets equal | 1.07e-10 | 0.000000 | 0.000000 | 0.000000 | -1.07e-10 | 0.000000 | -1.07e-10 |
| Other relations kept | Blocks equal | -0.001742 | 0.004705 | 0.012844 | 0.012844 | 0.006447 | 1.07e-16 | 0.006447 |
| Other relations kept | Targets equal | -0.002819 | 0.004773 | 0.017034 | 0.017034 | 0.007591 | 9.06e-17 | 0.007591 |
| Part of speech only | Blocks equal | -0.328907 | -0.356894 | -0.376628 | -0.376628 | -0.027987 | -4.07e-07 | -0.027986 |
| Part of speech only | Targets equal | -0.284057 | -0.313686 | -0.311355 | -0.311355 | -0.029628 | -2.51e-07 | -0.029628 |

## Annotation frequencies compared

This comparison does not use the models. It measures how different the frequencies of the symbols are between blocks, with the **Jensen–Shannon divergence** (JSD): a symmetric measure, in bits, that is 0 for identical distributions and at most 1. It is called a divergence, not a distance.

The JSD between the average hexameter and the average prose distribution, every block weighing the same, is 0.119662 bits with part of speech + relation, 0.119827 with other relations kept and 0.074570 with part of speech only (Table 15). These values describe differences between the complete symbol distributions, including the first tokens of each sentence; they use neither the scored targets nor the training samples.

Table 14 gives every pair of blocks. With part of speech + relation the two hexameter blocks have JSD 0.019219; pairs of prose blocks range from 0.008898 (Athenaeus–Herodotus) to 0.031830 (Diodorus–Herodotus), and hexameter–prose pairs from 0.105706 (Homeric tradition–Herodotus) to 0.159383 (Hesiodic tradition–Diodorus). This describes these distributions; it is not a classification test, a clustering or a proof that the groups are homogeneous. The [frequency panels](../results/figures/README.md#4-how-different-the-annotation-frequencies-are) show the matrix of pairs, the three group divergences and the contribution of each symbol. Differences of frequency neither explain away nor confirm Q, which concerns a different population and the effect of order on prediction. These three calculations are deterministic and have no seeds.

They use all kept tokens of the seven blocks, **including the first tokens of each sentence**, and neither the census-only texts nor the training samples. [root_distributions.csv](../results/hexis31/v3-seed0-v3006/root_distributions.csv) holds 1,512 rows, one per scheme, block and symbol, with the plain `count`, the frequency `count/N_all` and the smoothed frequency `(count+0.5)/(N_all+0.5m)`, where N_all is the block's kept tokens and m the number of symbols. The seven blocks have 154,300 kept tokens in the main scheme and in part of speech only, and 154,947 with other relations kept; the counts per document are in the delivered corpus, `documents.csv`.

**Table 14 — every pair of blocks, three annotation schemes.** Source: [jsd_pairs.csv](../results/hexis31/v3-seed0-v3006/jsd_pairs.csv), every row, column `jsd`, in bits. Each column fills a 7 × 7 symmetric matrix with zeros on the diagonal; nothing is averaged.

| Block a | Block b | Part of speech + relation | Other relations kept | Part of speech only |
|---|---|---|---|---|
| Athenaeus | Diodorus | 0.020419 | 0.022237 | 0.011264 |
| Athenaeus | Herodotus | 0.008898 | 0.009087 | 0.004768 |
| Athenaeus | Hesiodic tradition | 0.122103 | 0.121955 | 0.071131 |
| Athenaeus | Homeric tradition | 0.109465 | 0.109125 | 0.068845 |
| Athenaeus | Plutarch | 0.012499 | 0.013178 | 0.004465 |
| Athenaeus | Thucydides | 0.011728 | 0.012546 | 0.004326 |
| Diodorus | Herodotus | 0.031830 | 0.033030 | 0.022657 |
| Diodorus | Hesiodic tradition | 0.159383 | 0.160368 | 0.105904 |
| Diodorus | Homeric tradition | 0.148153 | 0.150556 | 0.109659 |
| Diodorus | Plutarch | 0.019680 | 0.020078 | 0.011243 |
| Diodorus | Thucydides | 0.026261 | 0.026569 | 0.017228 |
| Herodotus | Hesiodic tradition | 0.129018 | 0.129026 | 0.073721 |
| Herodotus | Homeric tradition | 0.105706 | 0.105875 | 0.065179 |
| Herodotus | Plutarch | 0.012127 | 0.012491 | 0.004722 |
| Herodotus | Thucydides | 0.010295 | 0.010672 | 0.003507 |
| Hesiodic tradition | Homeric tradition | 0.019219 | 0.019727 | 0.006041 |
| Hesiodic tradition | Plutarch | 0.143105 | 0.143201 | 0.079803 |
| Hesiodic tradition | Thucydides | 0.133590 | 0.133860 | 0.073182 |
| Homeric tradition | Plutarch | 0.126905 | 0.127931 | 0.075758 |
| Homeric tradition | Thucydides | 0.113307 | 0.114601 | 0.065728 |
| Plutarch | Thucydides | 0.009704 | 0.009738 | 0.003873 |

**Table 15 — divergence between the hexameter and prose averages.** Source: [jsd_centroids.csv](../results/hexis31/v3-seed0-v3006/jsd_centroids.csv), every row, column `jsd`, in bits. The hexameter average is the plain mean of its two smoothed block distributions, the prose average of its five. These are neither target-weighted averages nor averages of the pair divergences.

| Annotation scheme | Hexameter blocks | Prose blocks | Divergence between group averages (bits) |
|---|---|---|---|
| Part of speech + relation | 2 | 5 | 0.119662 |
| Other relations kept | 2 | 5 | 0.119827 |
| Part of speech only | 2 | 5 | 0.074570 |

**Complete contributions.** [jsd_contributions.csv](../results/hexis31/v3-seed0-v3006/jsd_contributions.csv) holds all **4,752** contributions of single symbols, in bits: for each scheme, each of the 21 pairs and the hexameter–prose comparison, every symbol, including zero contributions, (21+1)×(100+105+11). No leading symbols are selected. The checks compare every sum of contributions with its published JSD. The group averages can be rebuilt from the smoothed block frequencies with weight 1/2 per hexameter block and 1/5 per prose block.

## Model diagnostics

These records describe the models rather than the result; they show how much context the models store and actually use. The CTW model keeps a **context tree**: each node is a context, a sequence of preceding symbols seen in training, and its **depth** is the length of that sequence, the sentence start counting as one step. When it predicts, the model divides its probability among contexts of different lengths; the share given to each is its **weight**, and the share left for contexts never seen in training is the **unseen weight**. The **mean context length** of a prediction is the weighted average length of the seen contexts it draws on, the sentence start not counted; a prediction that draws on no seen context has no such length and is recorded as `null` with its reason, never as zero.

The [diagnostic panels](../results/figures/README.md#5-what-the-models-learned-technical-diagnostics) summarize the main setting: stored contexts are averaged per model and condition, while weights are pooled over documents, groups of targets and seeds, using all targets; the mean context length uses only targets that have one. These averages differ from the two group weightings. Table 16 lists the complete records of every setting and seed; Tables 17–18 give a fixed reference slice, the main setting at seed 0, not a selected extreme of the campaign.

In that slice the original-order models never stop at the root, the context of length zero (stop weight 0.000000): they always pass on to longer contexts, and their evidence difference at the root, stop minus split, is negative. The shuffled models always stop at the root (1.000000), with positive differences (Table 17). Put simply, in the original order the model uses the preceding symbols, after shuffling it falls back on the plain frequencies: the shuffled mean context lengths and unseen weights in Table 18 are zero. This is numerical behaviour at the recorded precision, not a general law. The full report contains nonzero gains after shuffling, most visibly 0.000020 bits per target for Plutarch with part of speech only at seed 0, all targets (`block_pairs.csv`). These small gains remain inside Q.

A missing context length and a symbol never seen in training are different records. In the original-order *Iliad* at seed 0, 19,781 targets have a context length and 2 do not after 4–7 tokens, 25,731 and 1 after 8 or more; one target in each group is a symbol never seen in training (Table 18). These records must not be turned into zero-length contexts, nor confused with the encounters with unseen branches, which can occur even when the weight sent there is numerically zero. A context seen only once is still a seen context; being stored guarantees neither precision nor a grammatical meaning.

The complete records of the training quotas and fragments accompany these diagnostics (Tables 10 and 16). A fragment that starts inside a sentence restarts the available history; the tokens left out give no context. `direct_context_targets` counts the first min(D, fragment length) positions affected by such a restart, where D is the maximum depth; it does not count scored targets. For example, at seed 0 the model that scores Thucydides in the main setting contains a Hesiodic fragment with start 1, end 3 and `direct_context_targets` 2, although a stream of two tokens has no scored target. This clarifies the definition; it is not a separate analysis of fragmentation or a bound on its effect on Q. The resource records measure this execution and add no complexity penalty to the losses.

**Table 16 — where the complete diagnostics are.** Every file is part of the same hash-verified manifest. The table gives, for each, its rows, keys and fields; nested histograms are JSON cells in the CSV. No new average across seeds is introduced.

| Source / rows | Rows identified by | Fields, units and denominators |
|---|---|---|
| [model_diagnostics.csv](../results/hexis31/v3-seed0-v3006/model_diagnostics.csv) / 980 | setting, held-out block, seed, condition | `nodes`, `node_count_by_structural_depth`, `support_histogram_1_2to4_5to9_10plus_by_depth`: stored contexts per model and depth, by times seen (1, 2–4, 5–9, ≥10); not to be multiplied by the number of documents. `root_observed_symbol_count`, `root_unseen_symbol_count`: symbols seen and unseen in training. `root_stop`: probability of stopping at the root; `delta_root_nats_stop_minus_split`: root evidence difference in nats, with `delta_root_reason`. `fit_seconds`, `evaluation_seconds`: seconds; `peak_rss`: bytes, the highest memory of the process, not additive. |
| [arm_diagnostics.csv](../results/hexis31/v3-seed0-v3006/arm_diagnostics.csv) / 3,080 | setting, held-out block, seed, document, condition, group of targets | `n`: targets. `resolved_mean=sum_resolved_valid/resolved_valid_count`: mean context length; a prediction with no seen context is `null` with its reason, never a length of zero. `resolved_null_count_by_reason_no_resolved_mass`: targets without a context length. `unseen_mass_mean=sum_unseen_mass/n`: unseen weight; `sum_observed_mass_by_length_ℓ/n`: weight on contexts of ℓ preceding symbols, the sentence start not counted. `root_unseen_target_count/n`: share of targets whose symbol was never seen in training. `implicit_unseen_branch_encounter_count`: encounters with never-seen branches, which are not stored contexts. |
| [fragment_diagnostics.csv](../results/hexis31/v3-seed0-v3006/fragment_diagnostics.csv) / 2,940 | setting, held-out block, seed, contributing block | `fragment_count`, `internal_start_count`: number of fragments, and of fragments starting inside a sentence; `fragment_tokens`: kept tokens in cut fragments; `direct_context_targets = Σ min(D, fragment_length)` over fragments with `start>0`: positions whose available context is directly shortened by the restart, first positions included, not scored targets. Six contributing blocks per pair, shared by both conditions, not two independent samples. The sample ledger of each pair records coordinates and sub-seeds. |
| [aggregation_weights.csv](../results/hexis31/v3-seed0-v3006/aggregation_weights.csv) / 980 | setting, seed, averaging, held-out block | `n`, `weight`, `share`: targets of the held-out block and its weights within its group. `training_tokens/available_tokens`: quota taken from a contributing block and its kept tokens. `fold_training_tokens`: training tokens of the model that scores the block; `fold_share_*` uses them as denominator. |
| [document_scores.csv](../results/hexis31/v3-seed0-v3006/document_scores.csv) / 1,540; [block_pairs.csv](../results/hexis31/v3-seed0-v3006/block_pairs.csv) / 1,470 | setting, held-out block, seed, document (first file only), group of targets | `n`, the four loss sums `sum_loss_*` (bits), cross-entropies, gains and Q (bits per target), `reason`; `changed_symbol_eligible_slot_count/eligible_slot_count` measures how many scored positions the shuffle filled with a different symbol. Both groups of targets are kept even when empty. |

The mean context lengths are means of the values of single positions, not ratios of pooled weights. They describe where the model places its weight given the seen contexts; they do not measure reliability, grammatical depth or the longest recoverable dependency. The weights by length and the unseen weight use all targets and sum to one within tolerance after division by `n`. Lengths 9–12 exist only at depth 12; blank cells in the depth-8 models mean that those lengths are outside the model, not that the length is missing. An empty group of targets keeps n = 0, sums equal to zero and `null` means and scores, with reason `empty_bucket`. The stopping at the root and the tiny shuffled gains remain recorded numerical behaviour, not a theorem that the shuffled model equals the frequency predictor.

**Table 17 — model records, main setting, seed 0.** Source: [model_diagnostics.csv](../results/hexis31/v3-seed0-v3006/model_diagnostics.csv), all seven held-out blocks and both conditions. Counts per model; the evidence difference in nats (natural-log units), times in seconds, memory in bytes. A reference slice, not a campaign mean or a selected extreme; Table 16 links every other model and its complete histograms.

| Block / condition | Contexts stored | Symbols seen / unseen in training | Stop weight at the root | Root evidence, stop − split (nats) | Fitting (s) | Scoring (s) | Peak memory (bytes) |
|---|---|---|---|---|---|---|---|
| Homeric tradition / original | 171304 | 82 / 18 | 0.000000 | -11315.194089 | 0.629680 | 1.726143 | 1277710336 |
| Homeric tradition / shuffled | 193401 | 82 / 18 | 1.000000 | 4542.699079 | 0.880536 | 1.973282 | 1277710336 |
| Hesiodic tradition / original | 170130 | 80 / 20 | 0.000000 | -11302.257111 | 0.636460 | 0.234558 | 1156141056 |
| Hesiodic tradition / shuffled | 192158 | 80 / 20 | 1.000000 | 4729.027752 | 0.866225 | 0.235393 | 1156141056 |
| Herodotus / original | 166983 | 81 / 19 | 0.000000 | -10867.122089 | 0.624931 | 0.490825 | 1130033152 |
| Herodotus / shuffled | 188815 | 81 / 19 | 1.000000 | 4432.017910 | 0.843873 | 0.492131 | 1130033152 |
| Thucydides / original | 167316 | 83 / 17 | 0.000000 | -10474.248757 | 0.555008 | 0.287599 | 1277710336 |
| Thucydides / shuffled | 188599 | 83 / 17 | 1.000000 | 4413.447331 | 0.999279 | 0.287368 | 1277710336 |
| Athenaeus / original | 169942 | 81 / 19 | 0.000000 | -10447.308388 | 0.611543 | 0.635328 | 906403840 |
| Athenaeus / shuffled | 191016 | 81 / 19 | 1.000000 | 4394.965343 | 1.003647 | 0.637413 | 906403840 |
| Diodorus / original | 168631 | 81 / 19 | 0.000000 | -9816.390961 | 0.611663 | 0.485879 | 1058783232 |
| Diodorus / shuffled | 187585 | 81 / 19 | 1.000000 | 4346.570574 | 0.840481 | 0.485617 | 1058783232 |
| Plutarch / original | 166849 | 79 / 21 | 0.000000 | -9818.770438 | 0.563156 | 0.262022 | 1277710336 |
| Plutarch / shuffled | 187190 | 79 / 21 | 1.000000 | 4288.383063 | 1.005005 | 0.261826 | 1277710336 |

**Table 18 — scoring records, main setting, seed 0.** Source: [arm_diagnostics.csv](../results/hexis31/v3-seed0-v3006/arm_diagnostics.csv), every document, condition and group of targets. Counts: targets `n`; targets with and without a context length; targets whose symbol was never seen in training; encounters with unseen branches. The mean context length is `resolved_mean`, in preceding symbols; the unseen weight is `unseen_mass_mean`, a fraction of `n`. Complete sums and every weight by length are in Table 16's sources, for all settings and seeds.

| Document / condition / preceding tokens | Targets | With / without a context length | Mean context length | Mean weight on unseen contexts | Targets never seen in training | Encounters with unseen branches |
|---|---|---|---|---|---|---|
| Iliad / original / 4–7 | 19783 | 19781 / 2 | 1.003277 | 0.000532 | 1 | 17096 |
| Iliad / original / ≥8 | 25732 | 25731 / 1 | 1.003527 | 0.000790 | 1 | 25704 |
| Iliad / shuffled / 4–7 | 19783 | 19783 / 0 | 0.000000 | 0.000000 | 1 | 19517 |
| Iliad / shuffled / ≥8 | 25732 | 25732 / 0 | 0.000000 | 0.000000 | 2 | 25732 |
| Homeric Hymn to Demeter / original / 4–7 | 458 | 458 / 0 | 1.000000 | 0.000570 | 0 | 445 |
| Homeric Hymn to Demeter / original / ≥8 | 661 | 661 / 0 | 1.001523 | 0.000010 | 0 | 661 |
| Homeric Hymn to Demeter / shuffled / 4–7 | 458 | 458 / 0 | 0.000000 | 0.000000 | 1 | 452 |
| Homeric Hymn to Demeter / shuffled / ≥8 | 661 | 661 / 0 | 0.000000 | 0.000000 | 1 | 661 |
| Theogony / original / 4–7 | 942 | 942 / 0 | 1.003186 | 0.000773 | 0 | 849 |
| Theogony / original / ≥8 | 2003 | 2003 / 0 | 1.002509 | 0.000697 | 0 | 1944 |
| Theogony / shuffled / 4–7 | 942 | 942 / 0 | 0.000000 | 0.000000 | 0 | 929 |
| Theogony / shuffled / ≥8 | 2003 | 2003 / 0 | 0.000000 | 0.000000 | 0 | 2003 |
| Works and Days / original / 4–7 | 887 | 887 / 0 | 1.006362 | 0.001466 | 0 | 780 |
| Works and Days / original / ≥8 | 1190 | 1190 / 0 | 1.005046 | 0.002284 | 0 | 1190 |
| Works and Days / shuffled / 4–7 | 887 | 887 / 0 | 0.000000 | 0.000000 | 0 | 872 |
| Works and Days / shuffled / ≥8 | 1190 | 1190 / 0 | 0.000000 | 0.000000 | 0 | 1190 |
| Shield of Heracles / original / 4–7 | 576 | 575 / 1 | 1.000000 | 0.001780 | 1 | 515 |
| Shield of Heracles / original / ≥8 | 777 | 777 / 0 | 1.007767 | 0.000990 | 0 | 777 |
| Shield of Heracles / shuffled / 4–7 | 576 | 576 / 0 | 0.000000 | 0.000000 | 0 | 566 |
| Shield of Heracles / shuffled / ≥8 | 777 | 777 / 0 | 0.000000 | 0.000000 | 1 | 777 |
| Histories, book 1 (Herodotus) / original / 4–7 | 3977 | 3977 / 0 | 1.139563 | 0.001784 | 0 | 3245 |
| Histories, book 1 (Herodotus) / original / ≥8 | 8969 | 8969 / 0 | 1.134549 | 0.002371 | 0 | 8958 |
| Histories, book 1 (Herodotus) / shuffled / 4–7 | 3977 | 3977 / 0 | 0.000000 | 0.000000 | 0 | 3921 |
| Histories, book 1 (Herodotus) / shuffled / ≥8 | 8969 | 8969 / 0 | 0.000000 | 0.000000 | 0 | 8969 |
| Histories, book 1 (Thucydides) / original / 4–7 | 1989 | 1989 / 0 | 1.154571 | 0.000673 | 0 | 1575 |
| Histories, book 1 (Thucydides) / original / ≥8 | 5238 | 5236 / 2 | 1.136663 | 0.001867 | 3 | 5226 |
| Histories, book 1 (Thucydides) / shuffled / 4–7 | 1989 | 1989 / 0 | 0.000000 | 0.000000 | 1 | 1958 |
| Histories, book 1 (Thucydides) / shuffled / ≥8 | 5238 | 5238 / 0 | 0.000000 | 0.000000 | 1 | 5238 |
| Deipnosophistae, books 12-13 / original / 4–7 | 5641 | 5640 / 1 | 1.146586 | 0.000955 | 0 | 4657 |
| Deipnosophistae, books 12-13 / original / ≥8 | 11050 | 11044 / 6 | 1.154329 | 0.001839 | 7 | 11014 |
| Deipnosophistae, books 12-13 / shuffled / 4–7 | 5641 | 5641 / 0 | 0.000000 | 0.000000 | 2 | 5558 |
| Deipnosophistae, books 12-13 / shuffled / ≥8 | 11050 | 11050 / 0 | 0.000000 | 0.000000 | 6 | 11050 |
| Bibliotheca historica, book 11 / original / 4–7 | 2898 | 2898 / 0 | 1.204018 | 0.000572 | 0 | 2087 |
| Bibliotheca historica, book 11 / original / ≥8 | 9436 | 9434 / 2 | 1.205013 | 0.000725 | 2 | 9402 |
| Bibliotheca historica, book 11 / shuffled / 4–7 | 2898 | 2898 / 0 | 0.000000 | 0.000000 | 0 | 2858 |
| Bibliotheca historica, book 11 / shuffled / ≥8 | 9436 | 9436 / 0 | 0.000000 | 0.000000 | 2 | 9436 |
| Lycurgus / original / 4–7 | 925 | 924 / 1 | 1.167335 | 0.002849 | 0 | 727 |
| Lycurgus / original / ≥8 | 2568 | 2566 / 2 | 1.158710 | 0.003216 | 2 | 2566 |
| Lycurgus / shuffled / 4–7 | 925 | 925 / 0 | 0.000000 | 0.000000 | 0 | 911 |
| Lycurgus / shuffled / ≥8 | 2568 | 2568 / 0 | 0.000000 | 0.000000 | 1 | 2568 |
| Alcibiades / original / 4–7 | 915 | 915 / 0 | 1.151767 | 0.001422 | 0 | 687 |
| Alcibiades / original / ≥8 | 2493 | 2491 / 2 | 1.159464 | 0.001473 | 2 | 2488 |
| Alcibiades / shuffled / 4–7 | 915 | 915 / 0 | 0.000000 | 0.000000 | 0 | 900 |
| Alcibiades / shuffled / ≥8 | 2493 | 2493 / 0 | 0.000000 | 0.000000 | 2 | 2493 |

The campaign's resource totals are 713.32 s of fitting and 535.60 s of scoring summed over the 980 models, with a peak memory of 1,654,919,168 bytes; the wall time of the campaign run recorded in its manifest is 7,450.8 s. These are measurements of this execution, not forecasts or guarantees. Values per model are in Table 16's sources; the report stage records its own resources in its manifest. No resource figure is used as a score or a complexity penalty.

## Figures

The study's pipeline produced five figures, kept unchanged with their hashes in the run manifest. The [figure gallery](../results/figures/README.md) redraws the same published values one panel at a time, each with an explanation beside it; it is a presentation, not evidence, and does not replace the five figures.

| Figure | Tables it draws on | Panels for reading |
|---|---|---|
| [corpus and annotation](../results/hexis31/v3-seed0-v3006/figure__corpus_annotation.svg) | `documents.csv` and `audit_contingency.csv` of the delivered corpus: quantities, share kept and source tagging, census-only documents included | [gallery, section 1](../results/figures/README.md#1-corpus-and-annotation) |
| [block and document profiles](../results/hexis31/v3-seed0-v3006/figure__block_document_profiles.svg) | Tables 3–6; the complete seed summaries hold every component and group of targets | [gallery, section 2](../results/figures/README.md#2-order-advantage-per-block-and-per-document) |
| [sensitivities and the two weightings](../results/hexis31/v3-seed0-v3006/figure__sensitivities_two_weights.svg) | Tables 7–13: both weightings and the paired changes on seeds 0–9 | [gallery, section 3](../results/figures/README.md#3-sensitivity-to-the-analysis-choices-and-the-two-ways-of-averaging) |
| [annotation frequencies](../results/hexis31/v3-seed0-v3006/figure__R1.svg) | Tables 14–15 and the complete contributions | [gallery, section 4](../results/figures/README.md#4-how-different-the-annotation-frequencies-are) |
| [supports and weights](../results/hexis31/v3-seed0-v3006/figure__supports_mixture_masses.svg) | Tables 16–18: stored contexts, weights and context lengths, each with its own denominator | [gallery, section 5](../results/figures/README.md#5-what-the-models-learned-technical-diagnostics) |

The five figures were reproduced byte for byte from the published tables, and all five were rendered at 2,400 pixels wide and read against the tables ([scripts and previews](../results/hexis31/v5-logs/closure/visual/)); none was edited. Every panel is legible and agrees with its tables: the shuffled-gain panels use axes of 10⁻¹⁶ and 10⁻¹⁵, consistent with Table 3; the targets with and without a context length pooled over the main setting, 2,181,798/362 in the original order and 2,182,160/0 shuffled, match `arm_diagnostics.csv` and sum to 20 × 109,108. Two limits of presentation are recorded, not corrected: in the supports figure the stacked original-order bar at depth 5 exceeds the upper axis limit and is clipped; in the band panel of the sensitivity figure the block means are unlabelled points, so single blocks are read from Tables 4–5. Neither affects a published number, and neither occurs in the gallery panels.

## What the results support, and what they do not

**What can be concluded.** Under this fixed predictor, this encoding and this training on the other blocks, the results support only the following descriptions.

1. *Order advantage.* In the main setting every block and document has a positive mean Q, and in all six settings every block's lowest seed is positive (Tables 3 and 6 and their source). Q is an advantage in prediction of the original order over the fixed within-sentence shuffle, under this predictor. It is not an entropy rate, a mutual information of Greek, a grammatical memory or a measure of cognitive difficulty.
2. *The shuffled control.* The gain after shuffling is practically zero in the main setting; the largest value among the 490 pairs is 0.000020 bits per target (part of speech only, Plutarch, seed 0, all targets). This is the measured behaviour of the chosen control: no theorem, and no attribution of the whole gain in the original order to linguistic order. In the main setting Q and the gain in the original order coincide at the printed precision because of this observation, not by definition; with part of speech only they already differ in the sixth decimal (Table 8).
3. *Hexameter and prose.* The hexameter − prose difference in Q is negative under both weightings in all six settings, with means from −0.237546 (part of speech only, blocks equal) to −0.165288 (half training data, targets equal) and every range over seeds below zero (Tables 8–9). It describes two hexameter and five prose blocks, each scored by a differently trained model. It is not an effect of metre, period, author, genre or verse form, and not a separation of populations; no size is attributed to it.
4. *Sensitivities.* The sign and size of the paired changes depend on the setting and, with the weaker prior, on the block (Diodorus moves opposite to the other six): the results depend on the declared choices and on the distribution of targets, and are reported without choosing a preferred one. Depth 12 against depth 8: no improvement in the configurations evaluated, which is not an absence of dependencies beyond eight symbols. Main against part of speech only: differences of the same sign show that the summary agrees in two schemes; they neither prove that the relations contribute nothing nor measure their contribution by subtraction. Other relations kept is a different task with its own targets.
5. *Merging particles and adverbs.* It reduces the documented discontinuity of the source tagging; it does not demonstrate homogeneous annotation. Its effect on the gains and on Q is not identified: the campaign has no unmerged version, and comparison with the pilot changes more than the merging.
6. *Annotation frequencies.* With part of speech + relation, the hexameter–prose JSD is 0.119662 bits; hexameter–prose pairs of blocks range from 0.105706 to 0.159383 and pairs within a group are at most 0.031830 (Tables 14–15). These are differences between complete distributions of symbols. They neither explain nor confirm Q.
7. *Census-only texts.* The six tragedies enter only the census and the inventory of symbols; nothing is concluded about how hexameter compares with tragedy or with other metres.

**Limits that qualify every result above.**

- *Finite corpus.* One pinned release of one treebank and eleven scored documents; nothing here extends to Greek in general, to the authors' complete works or to other annotations.
- *Two and five blocks.* Each group summary rests on two hexameter and five prose units.
- *One work dominates.* The *Iliad* supplies 45,515 of the Homeric block's 46,634 targets, and weighting by targets gives that block 0.879737 of the hexameter average (Tables 2 and 10).
- *Chronology and annotation are confounded with the groups.* Hexameter coincides with the archaic texts, and no comparable archaic prose exists. Before merging, the source had 11,270 particles in hexameter and none in prose; conjunctions and relations keep residual differences of practice, and no information on annotators allows a control.
- *A different training for each block.* Each held-out block is scored by a model trained on a different mixture; hexameter makes up 0.166667 or 0.333333 of the training (Table 10).
- *Annotations assigned afterwards.* The relations are assigned by annotators who read the whole sentence, so they can depend on later words and on the head of the relation; predicting them does not simulate a reader, and the sequence loses the tree structure.
- *Weightings.* The two averages describe the average block and the average target; neither corrects the other, and neither balances chronology, annotation or training.
- *A control that keeps each sentence's composition.* The shuffle reorders the symbols of each sampled or scored sentence, so Q concerns order given which symbols a sentence contains. Shuffling without replacement makes the control neither a sequence of independent draws nor a general estimate of bias. Long sentences contribute more targets; skipping the first four positions does not equalize them.
- *Spread over seeds is computational.* The SD, minimum and maximum over seeds describe the random sampling and shuffling. No p-values, intervals, multiple-comparison corrections, Bayes factors or permutation ranks are computed, and no SD over seeds becomes uncertainty about the ancient texts.
- *Pilots already seen.* The plan was written after methodological development and real pilots; it is prospective, not a preregistration. The earlier pilot of the main setting (106 symbols, original order only) recorded a mean hexameter − prose difference in gain of −0.178025 bits per symbol over 20 seeds; the task, the prior and the seed convention have changed since, so this campaign does not replicate it.

**What the design leaves out**, fixed before the campaign and not motivated by its results: no final sensitivity to the prior on stopping at a shorter context (the weaker prior changes a different prior); no evaluation across sentence boundaries; no comparison of hexameter with other metres. Variants of earlier plans were retired: a depth of six, a stopping prior of 0.9, an evaluation across sentence boundaries and every evaluation on tragedy; there are no combinations of variants. No ratio of gain to frequency cross-entropy, no relations-only scheme, no permutation of labels, no balanced model and no re-averaging without single works is added; dropping a work from an average would not remove it from the training of the other blocks and is not a leave-one-document-out analysis.

## How the numbers were produced and checked

The final campaign is the run [v3-seed0-v3006](../results/hexis31/v3-seed0-v3006/manifest.json), run ID `6aa1b719e274116c5660790cf9b2ad73c7e1853cec672688e1dc27d6b7d60e05`, manifest SHA-256 `3243fc329351e45e1d1c2c2f68a5be57fec2ea197ef5a81a170a5c11f4ca6dab`. The plan prescribes a separate regeneration of seed 0, [v3-seed0-v3006-regeneration](../results/hexis31/v3-seed0-v3006-regeneration/manifest.json), manifest SHA-256 `72b6cdee3220cbea97ba0bfb969bd2f3b871f244e62a8f3da3182d6d84c3790a`: it has the same scientific run identity, and its 70 compared artifacts are identical to the campaign's. The dependency lock has SHA-256 `33db43b00bcb21ab12aedf6dcc4257764770bff0115dc0d1dfab6e5ea89876bf`.

- The code, configuration, tests, lock and corpus were matched against the deposited plan and against the evidence of the acceptance run bound to this code; its 431 recorded passing tests were accepted.
- `validate_run` accepted the hashes of all 931 artifacts listed in the manifest, and the exact 490 train–score pairs and 980 models were checked.
- The 13 tables and five figures were rebuilt from the published data with the frozen report code, writing only to a temporary directory: all reproduced byte for byte ([reconstruct.py](../results/hexis31/v5-logs/closure/reconstruct.py), [reconstruct.log](../results/hexis31/v5-logs/closure/reconstruct.log)). No model was fitted and no campaign file was overwritten.
- The [verification of the campaign](../results/hexis31/v4-logs/commands.txt) covers the keys, sample ledgers, denominators, shuffles and frequency predictors of the whole campaign, and rebuilds the loss sums of the main setting from the saved values of each position. It does not refit the CTW models of seeds 1–19; the prescribed regeneration covers seed 0 only (42 pairs, 84 models, 70 compared artifacts).
- A separate editorial check matched the 1,987 numbers of the tables to the source rows and the stated rounding, checked the shape of every table and every link, and verified every sum of frequency contributions.
- The final acceptance run gave **431 passed**, with no skip or expected failure, and the ordinary and marked test collections list the same 431 tests.

**What remains open.** The terminal log and exit status of the campaign run were lost; its completion is shown by the manifest and the checks that followed, as the [record of that loss](../results/hexis31/v4-logs/01-v4-resume-log-lost.txt) states. The CTW losses of seeds 1–19 have not been independently regenerated. The rebuilding of tables and figures and the rendering of the figures were local checks; their scripts and logs are published in [`results/hexis31/v5-logs/closure/`](../results/hexis31/v5-logs/closure/). The per-pair records, sample ledgers and position vectors of the main setting are in the archives of the GitHub Release described in [results/README.md](../results/README.md); the raw data are not redistributed.

As the plan requires, completion depends on correct execution, not on the sign of the results, on separation between groups or on confirming the pilot; no "absent effect" is claimed.

## Reading the source tables

The published CSV files use short codes. Every label in this document corresponds to one of them:

| Label here | Code in the CSV files |
|---|---|
| Main setting, weaker prior, half training data, depth 12, other relations kept, part of speech only | `cell` = `C0`, `a_total1`, `q_half`, `D12`, `oth`, `upos` |
| Part of speech + relation, other relations kept, part of speech only (schemes) | `variant` = `ud23`, `ud23_oth`, `upos_only` |
| Homeric tradition, Hesiodic tradition, Herodotus, Thucydides, Athenaeus, Diodorus, Plutarch | `held_block` / `block` = `HOMERIC_TRADITION`, `HESIODIC_TRADITION`, `HERODOTUS`, `THUCYDIDES`, `ATHENAEUS`, `DIODORUS`, `PLUTARCH` |
| Hexameter, prose, hexameter − prose difference | `group` or `unit` = `HEX`, `PROSE_ALL`, `contrast` |
| Blocks equal, targets equal | `aggregation` = `equal_block`, `eligible_token_weighted` |
| Original order, shuffled | `arm` = `original`, `shuffled` |
| All targets; after 4–7; after 8 or more preceding tokens | `past_band` = `all`, `4_7`, `ge8` |
| Block, document, group, paired change of a block or group | `level` = `block`, `document`, `group`, `block_difference`, `group_difference` |
| Model CE, frequency CE, gain, Q (original / shuffled) | `metric` = `ce_ctw_original`, `ce_root_original`, `ce_ctw_shuffled`, `ce_root_shuffled`, `g_original`, `g_shuffled`, `q` |
| Census-only document | `role` = `inventory_only` (scored documents: `primary`) |
| Targets | `n`, or `eligible` in `documents.csv` |

Each summary row of `seed_summaries.csv` is identified by `(cell, level, unit, aggregation, past_band, metric)` and holds `mean`, `sd`, `min`, `max`, `S` and, for a `null`, its `reason`. The paired rows of `sensitivity_pairs.csv` add `seed`, `reference` (always the main setting), `value`, `reference_value` and `difference`.
