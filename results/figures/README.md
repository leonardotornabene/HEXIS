# HORMATHOS figures

The five figures of the final campaign, redrawn for reading: one panel per image, full width, one below the other (V3-009 in the [decision log](../../docs/02_DECISION_LOG.md)). Each panel draws values of the published tables named in its footer and nothing else; the [statement of results](../../docs/RESULTS.md) gives every number with its table and its limits.

These are a presentation. The canonical figures are the five frozen SVGs in [`hexis31/v3-seed0-v3006/`](../README.md#the-final-campaign-hexis31v3-seed0-v3006), recorded with their hashes in the run manifest and unchanged. [`make_figures.py`](make_figures.py) first renders those five again from the published tables with the frozen code and stops unless every byte matches, then draws the panels below.

How to read them: scores are in bits per eligible target. Where seeds are shown, the large dot is the mean across seeds, the small dots are the single seeds and the line is their min–max. Seeds are computational repetitions, not samples of the ancient texts: the line is not a confidence interval, and no figure carries a significance test. Blue marks hexameter (HEX), orange prose (PROSE_ALL), unless the legend says otherwise.

## 1. Corpus and annotation

![Raw tokens, retained tokens and eligible targets per document, log scale](corpus__quantities.svg)

![Share of raw tokens retained per document](corpus__retention.svg)

![Share of raw tokens tagged PART and ADV in the source, per document](corpus__part_adv.svg)

## 2. Block and document profiles

The main result: Q, the order advantage, for each held-out block and each document in the main setting C0.

![Q per block in C0: both hexameter blocks below every prose block](profiles__q_block.svg)

![Q per document in C0](profiles__q_document.svg)

Q is the gain in attested order minus the gain under the within-sentence shuffle. The two gains:

![G original per block in C0](profiles__g_original_block.svg)

![G original per document in C0](profiles__g_original_document.svg)

![G shuffled per block in C0, in units of 10^-16 bits](profiles__g_shuffled_block.svg)

![G shuffled per document in C0, in units of 10^-16 bits](profiles__g_shuffled_document.svg)

## 3. Sensitivities and the two weightings

![D_Q, hexameter minus prose, in all six settings under both weightings](sensitivities__contrast.svg)

![Each setting minus C0 on the same seeds](sensitivities__paired_difference.svg)

![Block Q by setting, targets with 4–7 retained predecessors](sensitivities__past_band_4_7.svg)

![Block Q by setting, targets with 8 or more retained predecessors](sensitivities__past_band_ge8.svg)

## 4. R1: descriptive divergences between annotation counts

![Jensen–Shannon divergence between every pair of blocks, ud23](r1__matrix_ud23.svg)

![Jensen–Shannon divergence between the hexameter and prose centroids, three representations](r1__centroids.svg)

![Symbol contributions to the centroid divergence, ud23](r1__contributions_ud23.svg)

![Symbol contributions to the centroid divergence, ud23_oth](r1__contributions_ud23_oth.svg)

![Symbol contributions to the centroid divergence, upos_only](r1__contributions_upos_only.svg)

## 5. Model supports and mixture masses

![Observed nodes per model by structural depth and support class](supports__depth.svg)

![Mean observed mass per target by lexical context length](supports__mass_by_length.svg)

![Mean mass routed to unseen branches](supports__unseen_mass.svg)

![Mean resolved context length over valid targets](supports__resolved_length.svg)

## Regenerate

From the repository root, after `uv sync --frozen`:

```bash
uv run python results/figures/make_figures.py
```

The output is deterministic: a second run writes the same bytes.

## Licence

The figures derive from the corpus and are under CC BY-NC-SA 2.5, as their source, UD Ancient Greek Perseus r2.18 (commit `37837c7a3c592c9563f8c51cc63344b87247f8a5`) and AGDT/Perseus. `make_figures.py` is under MIT; this page under CC BY 4.0, except the corpus-derived values it quotes. See V3-002, V3-007 and V3-009 in the [decision log](../../docs/02_DECISION_LOG.md).
