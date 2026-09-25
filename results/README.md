# HORMATHOS results

The finished results of the HORMATHOS study, published under V3-007 in the [decision log](../docs/02_DECISION_LOG.md). The [statement of results and limitations](../docs/RESULTS.md) reads them; this page says what each file is. Every file here is byte for byte the one the pipeline or a check wrote; nothing was edited for publication.

## The final campaign: `hexis31/v3-seed0-v3006/`

Run ID `6aa1b719e274116c5660790cf9b2ad73c7e1853cec672688e1dc27d6b7d60e05`, 490 train/score pairs and 980 models over six analysis settings (cells), seeds 0–19 in the main cell C0 and 0–9 in the others. [manifest.json](hexis31/v3-seed0-v3006/manifest.json) (SHA-256 `3243fc329351e45e1d1c2c2f68a5be57fec2ea197ef5a81a170a5c11f4ca6dab`) lists all 931 artifacts with their hashes; the repository holds the ones below, the rest is in the campaign archive.

Scores are in bits per eligible target. O is the attested order, R the within-sentence shuffle; `G = CE_root − CE_CTW` is the gain of the trained model over the frequency baseline, and `Q = G_O − G_R` is the order advantage. Cells: `C0` main setting; `a_total1` different prior; `q_half` half the training data; `D12` depth 12 instead of 8; `oth` with other dependency labels; `upos` part of speech alone.

| File | Content |
|---|---|
| [seed_summaries.csv](hexis31/v3-seed0-v3006/seed_summaries.csv) | mean, sd, min, max over seeds of every metric, per cell, block, document and group: the main table |
| [contrasts.csv](hexis31/v3-seed0-v3006/contrasts.csv) | hexameter and prose group summaries and their difference, per cell, seed and weighting |
| [sensitivity_pairs.csv](hexis31/v3-seed0-v3006/sensitivity_pairs.csv) | each cell minus C0 on the same seed |
| [block_pairs.csv](hexis31/v3-seed0-v3006/block_pairs.csv), [document_scores.csv](hexis31/v3-seed0-v3006/document_scores.csv) | loss sums per held-out block and per document, both arms, every seed |
| [aggregation_weights.csv](hexis31/v3-seed0-v3006/aggregation_weights.csv) | the two declared weightings and the training shares behind each block |
| [jsd_pairs.csv](hexis31/v3-seed0-v3006/jsd_pairs.csv), [jsd_centroids.csv](hexis31/v3-seed0-v3006/jsd_centroids.csv), [jsd_contributions.csv](hexis31/v3-seed0-v3006/jsd_contributions.csv) | R1: Jensen–Shannon divergences of the annotation counts, descriptive only |
| [root_distributions.csv](hexis31/v3-seed0-v3006/root_distributions.csv) | symbol frequencies per block, the baseline of every gain |
| [model_diagnostics.csv](hexis31/v3-seed0-v3006/model_diagnostics.csv), [arm_diagnostics.csv](hexis31/v3-seed0-v3006/arm_diagnostics.csv), [fragment_diagnostics.csv](hexis31/v3-seed0-v3006/fragment_diagnostics.csv) | model supports, masses, unseen symbols and sample fragments |
| five `figure__*.svg` | the five figures of the design, as the pipeline wrote them: [corpus](hexis31/v3-seed0-v3006/figure__corpus_annotation.svg), [profiles](hexis31/v3-seed0-v3006/figure__block_document_profiles.svg), [sensitivities](hexis31/v3-seed0-v3006/figure__sensitivities_two_weights.svg), [R1](hexis31/v3-seed0-v3006/figure__R1.svg), [supports and masses](hexis31/v3-seed0-v3006/figure__supports_mixture_masses.svg); to read them, use the [figure gallery](figures/README.md) |
| `tree_validation.json`, `v31_process.json`, `v31.junit.xml` | V2 evidence: the synthetic battery and the 431-test acceptance run bound to this code |

[`hexis31/v3-seed0-v3006-regeneration/`](hexis31/v3-seed0-v3006-regeneration/manifest.json) is the separately executed seed-0 regeneration: 70 of 70 compared artifacts identical.

## Figures for reading: `figures/`

The [figure gallery](figures/README.md) redraws the five figures one panel at a time, full width, from the published tables alone (V3-009). The frozen figures above stay the canonical ones; [`make_figures.py`](figures/make_figures.py) reproduces them byte for byte before it draws.

## Other published material

- [`hexis31/v1/`](hexis31/v1/): the delivered corpus encoding, the input of every run: documents, audit tables, encoded sentences and coordinates.
- [`hexis31/v3-seed0-v3006-logs/`](hexis31/v3-seed0-v3006-logs/), [`v4-logs/`](hexis31/v4-logs/), [`v5-logs/`](hexis31/v5-logs/): the logs, commands and independent check scripts of V3, V4 and V5. Each directory's `commands.txt` gives the commands verbatim. The V4 terminal log was lost, as [its record](hexis31/v4-logs/01-v4-resume-log-lost.txt) states.
- [`hexis31/v3-005-review/`](hexis31/v3-005-review/): the mutation check that closed the V3-005 review, 18 of 18 mutants killed.

The logs are verbatim. Local paths in them (`/Users/…`, `/tmp/…`) are those of the author's machine, and sentences such as "Git-ignored, not deposited" describe their status before V3-007.

## Complete archives

The [GitHub Release `hormathos-v5-evidence`](https://github.com/leonardotornabene/HORMATHOS/releases/tag/hormathos-v5-evidence) holds what is too large for the repository:

| Archive | SHA-256 | Content |
|---|---|---|
| `hormathos-campaign-v3006.tar.gz` (45 MB) | `3dadf6cecc303281897995b84c479721ce56e304859456f18dd9abb0164bec10` | `v1`, `v3-seed0-v3006` complete (490 pair records, 280 sample ledgers, 140 C0 position partitions) and its regeneration |
| `hormathos-superseded-runs.tar.gz` (17 MB) | `1a4fbf43b021dd442285927e8a76e687d905020220d2a29e9c4931f368a42cc3` | historical runs superseded by the reviews V3-005 and V3-006, never resumed: `v1-development`, `v1-reproduction`, `v2-pre-v3-audit-2026-09-24`, `v3-seed0`, `v3-seed0-r4-r6`, their regenerations and logs |

To verify, from the repository root after `uv sync --frozen`:

```bash
shasum -a 256 hormathos-campaign-v3006.tar.gz
tar -xzf hormathos-campaign-v3006.tar.gz -C results/hexis31
uv run python -c "from hormathos.pipeline import scientific_run as s; print(len(s.validate_run('results/hexis31/v3-seed0-v3006')['artifacts']))"   # 931
```

`validate_run` checks every artifact against the manifest. Extracted files that the repository does not track stay ignored by Git.

## Licence

Everything here derived from the corpus — the encoded corpus, tables, figures, manifests, pair records, ledgers and position vectors — is under CC BY-NC-SA 2.5, the licence of its source, UD Ancient Greek Perseus r2.18 (commit `37837c7a3c592c9563f8c51cc63344b87247f8a5`) and AGDT/Perseus. Logs and this page are CC BY 4.0, except the corpus-derived values they quote; check scripts are MIT. See V3-002 and V3-007 in the [decision log](../docs/02_DECISION_LOG.md).
