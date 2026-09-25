# HORMATHOS figures

The figures of the study, one panel per image, full width, each with a short explanation beside it. Every panel draws values of the published table named in its footer and nothing else. The [statement of results](../../docs/RESULTS.md) gives every number with its table and its limits; the terms used here are defined there too, in [The question and the measurement](../../docs/RESULTS.md#the-question-and-the-measurement).

## What is being measured

The texts come from an annotated corpus of ancient Greek. Each word carries two labels: its part of speech (noun, verb, …) and its syntactic relation in the sentence (subject, object, …). Joining the two gives one **symbol** per word, for example `NOUN:nsubj`, a noun that is the subject. A sentence thus becomes a sequence of symbols.

A model is trained to predict each symbol from the ones before it in the same sentence. The texts are grouped into seven **blocks**, two in hexameter verse (Homeric and Hesiodic tradition) and five in prose (Herodotus, Thucydides, Athenaeus, Diodorus, Plutarch). Each block is scored by a model trained only on the other six, so no text is predicted by a model that has seen it.

- A **target** is a symbol the model is scored on: every kept symbol from the fifth of its sentence on, so that each has at least four predecessors.
- **Bits per target** measure prediction cost: one bit is the information in a fair yes/no choice. Fewer bits mean better prediction.
- The **gain** is how many bits per target the trained model saves compared with a predictor that knows only how frequent each symbol is.
- The **shuffle** randomly reorders the symbols within each sentence. It keeps which symbols a sentence contains and destroys only their order.
- The **order advantage Q** is the gain in the original order minus the gain after shuffling. It measures how much the order of the symbols helps prediction.

The whole procedure is run several times, each time with different random samples of training text and different shuffles: each run is a **seed**. Where seeds are shown, the large dot is their mean, the small dots are the single seeds and the line runs from the lowest to the highest seed. The spread between seeds reflects the computation only: it is not a confidence interval and says nothing about uncertainty regarding the ancient texts, and no figure carries a significance test. Blue marks hexameter and orange prose, unless the legend says otherwise.

Besides the **main setting**, five variants each change one choice of the analysis to see how much the results depend on it: a weaker prior (the model starts from a smaller assumed count for every symbol), half the training data, contexts up to 12 symbols instead of 8, words with other syntactic relations kept under one shared label instead of removed, and part of speech alone without the relation.

These panels are a presentation. The canonical figures are the five produced by the study's pipeline, kept unchanged with their hashes in [`hexis31/v3-seed0-v3006/`](../README.md#the-final-campaign-hexis31v3-seed0-v3006). [`make_figures.py`](make_figures.py) first renders those five again from the published tables and stops unless every byte matches; then it draws the panels below.

## 1. Corpus and annotation

![Source tokens, kept tokens and targets per document, log scale](corpus__quantities.svg)

**What it shows:** for each document, how many tokens (words and punctuation) the source contains, how many the encoding keeps, and how many of those are targets. **How to read it:** the scale is logarithmic, so each grid line is ten times the previous one. **What to take from it:** the documents differ greatly in size; the *Iliad* alone is larger than any prose document. The six tragedies below the dashed line are counted only to build the inventory of symbols and are never used for training or scoring.

![Share of source tokens kept per document](corpus__retention.svg)

**What it shows:** the share of each document's tokens that the encoding keeps. **How to read it:** the encoding removes punctuation and a few other word classes, and words whose syntactic relation is not one of the 23 kept; the rest stays. **What to take from it:** every scored document keeps between 85% and 90% of its tokens, so no document is shaped by much heavier removals than the others.

![Share of source tokens tagged particle and adverb, per document](corpus__part_adv.svg)

**What it shows:** how often the source annotation tags a word as particle or as adverb. **How to read it:** each document has two bars, one per tag. **What to take from it:** the source tags words as particles in the *Iliad*, in Hesiod and in the tragedies, but never in the *Hymn to Demeter* or in the prose documents: a distinction the annotation applies in some documents and not in others, which need not reflect the language. For this reason the encoding merges particles and adverbs into one class everywhere. This reduces the problem; it does not make the annotation uniform.

## 2. Order advantage per block and per document

The main result: Q for each block and each document in the main setting.

![Order advantage Q per block, main setting: both hexameter blocks below every prose block](profiles__q_block.svg)

**What it shows:** the order advantage Q of each block. **How to read it:** further right means that the original order helps prediction more; the dashed line separates hexameter from prose. **What to take from it:** Q is positive everywhere, and both hexameter blocks (about 0.25–0.26 bits per target) lie below every prose block (0.39–0.54). This is a description of these texts under this procedure, not a proof that metre is the cause: see the limits in the [statement of results](../../docs/RESULTS.md#what-the-results-support-and-what-they-do-not).

![Order advantage Q per document, main setting](profiles__q_document.svg)

**What it shows:** the same Q for each of the eleven scored documents; n is the number of targets per seed. **How to read it:** documents of one block share that block's model. **What to take from it:** the Homeric block is almost entirely the *Iliad* (45,515 of its 46,634 targets), so the block value is essentially the *Iliad*'s. The documents are not eleven independent repetitions.

The two gains of which Q is the difference:

![Gain in the original order per block, main setting](profiles__g_original_block.svg)

**What it shows:** how many bits per target the trained model saves over symbol frequencies alone, with the original order. **What to take from it:** the values match Q almost exactly, because the gain after shuffling, below, is practically zero.

![Gain in the original order per document, main setting](profiles__g_original_document.svg)

**What it shows:** the same gain for each document.

![Gain after shuffling per block, main setting, in units of 10^-16 bits](profiles__g_shuffled_block.svg)

**What it shows:** the gain when the symbols of each sentence are shuffled. **How to read it:** the axis is in units of 10⁻¹⁶ bits, a millionth of a billionth. **What to take from it:** once the order is destroyed the trained model does no better than symbol frequencies; values this small are at the level of the computer's rounding error.

![Gain after shuffling per document, main setting, in units of 10^-16 bits](profiles__g_shuffled_document.svg)

**What it shows:** the same for each document.

## 3. Sensitivity to the analysis choices and the two ways of averaging

The hexameter and prose summaries are averages over their blocks, computed in two ways: with every block weighing the same, or with every target weighing the same, which gives larger blocks more weight.

![Hexameter minus prose in all six settings, both ways of averaging](sensitivities__contrast.svg)

**What it shows:** the mean Q of hexameter minus the mean Q of prose, in every setting and with both ways of averaging. **How to read it:** a value left of zero means hexameter below prose. **What to take from it:** the difference is negative in all six settings and with both averages, between −0.165 and −0.238 bits per target; the spread of the seeds never reaches zero.

![Change of the hexameter-minus-prose difference from the main setting, seed by seed](sensitivities__paired_difference.svg)

**What it shows:** how much each variant changes that difference compared with the main setting, computed on the same seeds. **How to read it:** zero means no change; values right of zero bring the difference closer to zero. **What to take from it:** halving the training data narrows the gap; part of speech alone widens it; contexts of 12 instead of 8 symbols change it by less than a billionth of a bit.

![Q of each block by setting, targets with 4–7 preceding tokens](sensitivities__past_band_4_7.svg)

**What it shows:** the mean Q of each block in each setting, only for targets preceded by 4 to 7 kept tokens of the same sentence. **How to read it:** each line joins one block across the settings; the order of the settings along the axis has no meaning. **What to take from it:** the hexameter blocks stay below the prose blocks in every setting.

![Q of each block by setting, targets with 8 or more preceding tokens](sensitivities__past_band_ge8.svg)

**What it shows:** the same for targets preceded by 8 or more tokens. **What to take from it:** the picture is the same. The two groups of targets come from different positions and sentence lengths, so the comparison between them is not an experiment on context length.

## 4. How different the annotation frequencies are

These panels do not use the models. They compare how often each symbol occurs in each block, whatever its position.

![Jensen–Shannon divergence between every pair of blocks, part of speech + relation](r1__matrix_ud23.svg)

**What it shows:** for each pair of blocks, how different their symbol frequencies are, measured by the Jensen–Shannon divergence: 0 if identical, at most 1 bit. **How to read it:** darker cells are more different pairs. **What to take from it:** the two hexameter blocks are close to each other, the prose blocks are close to each other, and every hexameter–prose pair is further apart. The frequencies alone already differ between the two groups; this neither explains nor confirms the order advantage Q, which concerns order, not frequency.

![Jensen–Shannon divergence between hexameter and prose, in the three annotation schemes](r1__centroids.svg)

**What it shows:** the divergence between the average frequencies of the hexameter blocks and of the prose blocks, in each of the three annotation schemes. **What to take from it:** the difference is smaller when only the part of speech is used.

![Contribution of each symbol to the hexameter–prose divergence, part of speech + relation](r1__contributions_ud23.svg)

**What it shows:** how much each symbol contributes to the hexameter–prose divergence; the contributions add up to the total. **How to read it:** each symbol is a part of speech and a relation, for example `DET:det`, a determiner in its usual role; the grey bar sums all symbols not shown one by one. **What to take from it:** a few symbols account for most of the difference.

![Contribution of each symbol to the hexameter–prose divergence, other relations kept](r1__contributions_ud23_oth.svg)

**What it shows:** the same, when words with other relations are kept under one shared label.

![Contribution of each symbol to the hexameter–prose divergence, part of speech only](r1__contributions_upos_only.svg)

**What it shows:** the same with part of speech alone, 11 symbols, all shown.

## 5. What the models learned: technical diagnostics

These panels describe the models themselves. They are not needed to read the main result; they show how much context the models actually use. The model predicts from a **context tree**: each node is a context, a sequence of preceding symbols seen in training, and deeper nodes are longer contexts.

![Contexts stored per model by depth, split by how often each was seen](supports__depth.svg)

**What it shows:** how many contexts a model stores at each depth, split by how many times each was seen in training. **How to read it:** left bar of each pair, original order; right bar, hatched, shuffled order. **What to take from it:** most deep contexts were seen only once, so they give the model little to learn from.

![Mean weight per target given to each context length](supports__mass_by_length.svg)

**What it shows:** for each context length, the average share of the prediction that the model takes from contexts of that length. **What to take from it:** with the original order the model relies mostly on the one preceding symbol, a little on two; after shuffling it relies only on the plain frequencies (length 0).

![Mean weight given to contexts never seen in training](supports__unseen_mass.svg)

**What it shows:** the average share of the prediction assigned to contexts never seen in training. **What to take from it:** it is very small in the original order and zero after shuffling.

![Average context length used per target](supports__resolved_length.svg)

**What it shows:** the average length of the contexts the prediction draws on. **How to read it:** a target whose prediction draws on no context seen in training has no length and is counted apart, never as zero. **What to take from it:** about one preceding symbol in the original order, zero after shuffling. This describes where the model places its weight, not how far grammatical structure reaches.

## Regenerate

From the repository root, after `uv sync --frozen`:

```bash
uv run python results/figures/make_figures.py
```

The output is deterministic: a second run writes the same bytes.

## Licence

The figures derive from the corpus and are under CC BY-NC-SA 2.5, as their source, UD Ancient Greek Perseus r2.18 (commit `37837c7a3c592c9563f8c51cc63344b87247f8a5`) and AGDT/Perseus. `make_figures.py` is under MIT; this page under CC BY 4.0, except the corpus-derived values it quotes. The licence decisions are recorded in the [decision log](../../docs/02_DECISION_LOG.md).
