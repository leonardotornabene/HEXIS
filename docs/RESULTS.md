# HORMATHOS — results and limitations (deposited design 3.1)

This is the statement of results and limitations that closed phase V5 of the deposited
design on 25 September 2026 (§14 V5, §16). Until V3-007 it was the first section of the
[handoff](HANDOFF.md), which remains the technical record of how every number was
produced and checked. It moved here with its wording unchanged, except six sentences
that said where its evidence was and that it is now published. The tables and figures
it cites are described in [results/README.md](../results/README.md).

## V5 results and limitations — 25 September 2026

**Statement of results and limitations (§14 V5, §16). V5 COMPLETED on 25 September 2026.**
The account was prepared in two reviewed stages. The owner delegated the review of the
numerical dossier to Codex, then authorized correction of its one finding: the
definition of `direct_context_targets` in X1 now follows §5.2, while the source numbers
and implementation were already correct. The owner then asked for the second review of
the complete scientific account; its corrections are recorded in the checkpoint at the
end of this section. No new fit, analytical cell or aggregation is introduced. The
closure record at the end of this section lists the final acceptance checks.
The historical sections of the [handoff](HANDOFF.md) retain their original wording and status in their dated context.

### Evidence identity and scope

The campaign is [v3-seed0-v3006](../results/hexis31/v3-seed0-v3006/manifest.json),
run ID `6aa1b719e274116c5660790cf9b2ad73c7e1853cec672688e1dc27d6b7d60e05`.
Its manifest SHA-256 is `3243fc329351e45e1d1c2c2f68a5be57fec2ea197ef5a81a170a5c11f4ca6dab`.
The prescribed, separately executed seed-0 regeneration is
[v3-seed0-v3006-regeneration](../results/hexis31/v3-seed0-v3006-regeneration/manifest.json),
manifest SHA-256 `72b6cdee3220cbea97ba0bfb969bd2f3b871f244e62a8f3da3182d6d84c3790a`.
Both have the same scientific run identity. The lock SHA-256 is
`33db43b00bcb21ab12aedf6dcc4257764770bff0115dc0d1dfab6e5ea89876bf`.

Read-only checks for this dossier, from `05ece9cf29c8976f9c059155ea2eb43a7c863335`,
matched the deposited contract, current code/configuration/test/lock context and corpus
manifest against V2 evidence; `verify_evidence` accepted its 431 recorded passing cases.
`validate_run` accepted all 931 artifact hashes, and `check_keys` accepted the exact
490 pair / 980 model identities. Direct byte comparisons of the 70 artifacts named in
the report's regeneration record passed. The 431-case suite was not rerun for this
preliminary dossier; the final complete acceptance run is reserved for closure after
the second review.

The preparation plan recalled a byte reconstruction of 13 tables and five figures;
the accessible [V5 check log](../results/hexis31/v5-logs/02-report-checks.log) records
their hashes but not that reconstruction. This evidence gap was closed by calling the
existing frozen report functions on the published partitions and corpus, writing only
to a temporary directory: all 13 tables and five figures reproduced byte for byte.
No fit ran and no campaign artifact was overwritten. The script and its log are published
since V3-007: [reconstruct.py](../results/hexis31/v5-logs/closure/reconstruct.py) and
[reconstruct.log](../results/hexis31/v5-logs/closure/reconstruct.log).

The [V4 verification record](../results/hexis31/v4-logs/commands.txt) covers the entire
campaign's keys, ledgers, denominators, shuffle/root checks and C0 loss-sum reconstruction.
It does not regenerate CTW fits for seeds 1–19. The separately executed regeneration
covers only the prescribed seed 0: 42 pairs / 84 models, 70 compared artifacts.
**The V4 terminal log and Python exit status remain lost**; the completion evidence is
the manifest and subsequent checks, as recorded in the dated campaign section of the
[handoff](HANDOFF.md).

Since V3-007 the result links in this dossier point to files published in the repository;
the per-pair records, sample ledgers and C0 position vectors are in the archives of the
GitHub Release described in [results/README.md](../results/README.md). The raw data are
not redistributed. The proposal remains a separate activity.

### Reading the numerical tables

Scores are in **bits per eligible target**; R1 divergences and contributions are in
**bits**. O means original order; R means the prescribed within-sentence shuffle.
`G_O = CE_0 O − CE_CTW O`, `G_R = CE_0 R − CE_CTW R`, and `Q = G_O − G_R`.
All contrasts are **HEX − PROSE_ALL**; all sensitivity differences are **cell − C0**
on the same seed. Four CE terms remain necessary because the scored symbol population
can differ between arms despite identical eligible slots.

Every printed score uses six decimals, except nonzero magnitudes below 10⁻⁶, shown in
scientific notation with three significant digits. Rounding is presentation only:
coincident printed numbers are not mathematical identities. `null` is not zero.
The report's `mean`, sample `sd` (denominator S−1), `min`, `max` and `S` describe
computational variation over seeds, not uncertainty about ancient texts.
Tables labelled means select the `mean` field; no statistics are recomputed here.

The hierarchy remains seven block profiles and eleven documents, followed by two
subordinate group summaries. This is a finite corpus with two HEX and five PROSE_ALL
blocks, different training for each held-out block, chronological and annotation
confounding, offline annotations, a control conditioned on sentence composition,
and already observed pilots. The Iliad supplies about 97.5% of the retained C0 tokens
of HOMERIC_TRADITION (§3.3); the block conventions do not establish independent authors.
The six `inventory_only` documents contribute only to census/alphabet, never these scores.

### Population and denominator register

This campaign describes prediction of the annotations in the pinned UD Ancient Greek
Perseus corpus under the deposited frozen CTW procedure. Training leaves out an entire
block; the held-out documents are scored on every eligible within-sentence slot. The
analysis concerns the retained annotation sequence, not lexical prediction or the full
dependency tree. Deletions close gaps, so context length is measured in retained symbols,
not raw-word distance. Sentence boundaries reset history; initial tokens contribute to
training and test history but do not receive primary test loss.

The [corpus and annotation figure](../results/hexis31/v3-seed0-v3006/figure__corpus_annotation.svg)
shows raw/retained quantities, eligible counts, retention and the source PART/ADV
discontinuity by document. Its inventory-only eligible counts are potential audit
positions, not evaluated positions. Global ADV/PART merging mitigates the documented
discontinuity; it does not establish homogeneous annotation. C0 and UPOS each have
109,108 eligible targets per seed, while OTH has 109,716 (N1–N2). These are finite,
representation-specific populations, not samples of independent linguistic observations.

C0, a_total1, q_half and D12 use ud23 (m=100); upos uses upos_only (m=11) with the
**exact C0 retention and target mask**. OTH uses ud23_oth (m=105) and its own population.
`4_7` and `ge8` mean 4–7 and ≥8 retained predecessors in the same sentence. `all` is
their total, not a third disjoint population. C0 uses seeds 0–19; each perturbation 0–9.
Counts below are per seed and are not multiplied by S.

**Table N1 — block denominators.** Source: [block_pairs.csv](../results/hexis31/v3-seed0-v3006/block_pairs.csv); filters `seed=0`, `cell=C0|oth`; keys `(cell, held_block_key, seed, past_band)`, with `held_block` as label. Columns select `n`; units: eligible targets. The C0 columns also apply to upos and the three other ud23 cells, checked against every source row.

| Block | C0 all | C0 4–7 | C0 ≥8 | OTH all | OTH 4–7 | OTH ≥8 |
|---|---|---|---|---|---|---|
| HOMERIC_TRADITION | 46634 | 20241 | 26393 | 47062 | 20381 | 26681 |
| HESIODIC_TRADITION | 6375 | 2405 | 3970 | 6398 | 2410 | 3988 |
| HERODOTUS | 12946 | 3977 | 8969 | 12994 | 3983 | 9011 |
| THUCYDIDES | 7227 | 1989 | 5238 | 7234 | 1990 | 5244 |
| ATHENAEUS | 16691 | 5641 | 11050 | 16786 | 5659 | 11127 |
| DIODORUS | 12334 | 2898 | 9436 | 12334 | 2898 | 9436 |
| PLUTARCH | 6901 | 1840 | 5061 | 6908 | 1842 | 5066 |

**Table N2 — document identities and denominators.** Source: [document_scores.csv](../results/hexis31/v3-seed0-v3006/document_scores.csv); filters `seed=0`, `cell=C0|oth`; keys `(cell, held_block_key, seed, doc_id, past_band)`; `n` is the denominator. Work names and complete retained-token counts are selected from [V1 documents.csv](../results/hexis31/v1/documents.csv), `role=primary`, `variant=ud23`, keyed by `(variant, doc_id)`. C0 all-target denominators for the total document profiles are its `eligible` column; total profiles themselves come from `seed_summaries.csv`.

| Document key (`doc_id`) | Work | Block | C0 retained | C0 all | C0 4–7 | C0 ≥8 | OTH 4–7 | OTH ≥8 |
|---|---|---|---|---|---|---|---|---|
| tlg0012.tlg001.perseus-grc1.tb.xml | Iliad | HOMERIC_TRADITION | 69327 | 45515 | 19783 | 25732 | 19918 | 26009 |
| tlg0013.tlg002.perseus-grc1.tb.xml | Homeric Hymn to Demeter | HOMERIC_TRADITION | 1761 | 1119 | 458 | 661 | 463 | 672 |
| tlg0020.tlg001.perseus-grc1.tb.xml | Theogony | HESIODIC_TRADITION | 4023 | 2945 | 942 | 2003 | 944 | 2011 |
| tlg0020.tlg002.perseus-grc1.tb.xml | Works and Days | HESIODIC_TRADITION | 3189 | 2077 | 887 | 1190 | 889 | 1195 |
| tlg0020.tlg003.perseus-grc1.tb.xml | Shield of Heracles | HESIODIC_TRADITION | 2070 | 1353 | 576 | 777 | 577 | 782 |
| tlg0016.tlg001.perseus-grc1.1.tb.xml | Histories, book 1 (Herodotus) | HERODOTUS | 17301 | 12946 | 3977 | 8969 | 3983 | 9011 |
| tlg0003.tlg001.perseus-grc1.1.tb.xml | Histories, book 1 (Thucydides) | THUCYDIDES | 9346 | 7227 | 1989 | 5238 | 1990 | 5244 |
| tlg0008.tlg001.perseus-grc1.tb.xml | Deipnosophistae, books 12-13 | ATHENAEUS | 23133 | 16691 | 5641 | 11050 | 5659 | 11127 |
| tlg0060.tlg001.perseus-grc3.11.tb.xml | Bibliotheca historica, book 11 | DIODORUS | 15266 | 12334 | 2898 | 9436 | 2898 | 9436 |
| tlg0007.tlg004.perseus-grc1.tb.xml | Lycurgus | PLUTARCH | 4481 | 3493 | 925 | 2568 | 926 | 2571 |
| tlg0007.tlg015.perseus-grc1.tb.xml | Alcibiades | PLUTARCH | 4403 | 3408 | 915 | 2493 | 916 | 2495 |

### Primary profiles and computational dispersion

In C0, the mean Q values of HOMERIC_TRADITION and HESIODIC_TRADITION are respectively
0.262112 and 0.252991 bits/target. The five prose-block means are 0.393150 for HERODOTUS,
0.429579 for THUCYDIDES, 0.452080 for ATHENAEUS, 0.526170 for DIODORUS and 0.542858 for
PLUTARCH (P1). Thus all seven block means are positive, and both HEX block means are
below each prose block mean in this procedure. Positive Q means a larger gain over
the corresponding root predictor in original order than under the fixed shuffle;
it does not identify the cause of the between-block differences.

The original CTW loss is below its original root loss in each C0 block. Shuffled gains
are numerically near zero, so G_O and Q coincide at the displayed precision in P1;
their separate unrounded records remain necessary. The four CE columns also show why
the two root losses cannot be cancelled: for HOMERIC_TRADITION, for example, the mean
original root CE is 4.817659 and the shuffled root CE is 4.724583 bits/target. Shuffling
moves symbols across the eligibility boundary while keeping the scored slots fixed.
Numerically small G_R is observed behavior of this trained control, not an identity
of CTW or evidence that every component of G_O is caused by linguistic order.

The document detail qualifies the block summaries. The Iliad has mean Q 0.260925 and
the Hymn to Demeter 0.310402; the Homeric block is dominated by the Iliad's 45,515 of
46,634 eligible targets (N1–N2). Within the Hesiodic block, the means are 0.259376 for
Theogony, 0.228274 for Works and Days and 0.277033 for Shield of Heracles. Within
PLUTARCH, Lycurgus has 0.552685 and Alcibiades 0.532785. The four single-document
blocks retain the document means already reported for HERODOTUS, THUCYDIDES, ATHENAEUS
and DIODORUS. These eleven details are not eleven independent replications: documents
share exclusion blocks and are evaluated under the block's training.

P4 gives computational dispersion for every document and block. For example, the
Homeric block has sample SD 0.002318 and min–max 0.255151–0.265862; the Hesiodic block
has SD 0.005909 and min–max 0.241140–0.262615, all in bits/target over 20 seeds.
The [profile figure](../results/hexis31/v3-seed0-v3006/figure__block_document_profiles.svg)
shows individual seeds, means and computational min–max bars. Neither these bars nor
the SDs quantify uncertainty about authors, works or ancient Greek beyond this corpus.
Chronology, tradition, genre and form are confounded, and the block-specific training
differs; the observed ordering of profiles cannot resolve those explanations.

**Tables P1–P3 — C0 means for every block and document, total and both bands.** Source: [seed_summaries.csv](../results/hexis31/v3-seed0-v3006/seed_summaries.csv); filters `cell=C0`, `level=block|document`, `aggregation=not_applicable`, `past_band` as named by each table; keys `(cell, level, unit, aggregation, past_band, metric)`. Each column selects `mean` for the metric in the legend, S=20. Units: bits/target, using N1/N2 for the corresponding unit and band. Document titles below map to the exact keys in N2. All seven metrics, all three bands, all six cells and their full `mean/sd/min/max/S/reason` records are available at that source; this is the extended profile table, including every perturbation document profile.

**P1: all eligible targets.**

| Level / unit | CE_CTW O | CE_0 O | CE_CTW R | CE_0 R | G_O | G_R | Q |
|---|---|---|---|---|---|---|---|
| block / HOMERIC_TRADITION | 4.555547 | 4.817659 | 4.724583 | 4.724583 | 0.262112 | 4.44e-17 | 0.262112 |
| block / HESIODIC_TRADITION | 4.670339 | 4.923330 | 4.877657 | 4.877657 | 0.252991 | 0.000000 | 0.252991 |
| block / HERODOTUS | 4.393918 | 4.787068 | 4.642541 | 4.642541 | 0.393150 | 4.44e-17 | 0.393150 |
| block / THUCYDIDES | 4.323848 | 4.753427 | 4.613959 | 4.613959 | 0.429579 | 0.000000 | 0.429579 |
| block / ATHENAEUS | 4.233885 | 4.685965 | 4.561370 | 4.561370 | 0.452080 | 8.88e-17 | 0.452080 |
| block / DIODORUS | 3.992307 | 4.518477 | 4.405177 | 4.405177 | 0.526170 | 1.33e-16 | 0.526170 |
| block / PLUTARCH | 4.234179 | 4.777036 | 4.637199 | 4.637199 | 0.542858 | 0.000000 | 0.542858 |
| document / Iliad | 4.556667 | 4.817592 | 4.722331 | 4.722331 | 0.260925 | 4.44e-17 | 0.260925 |
| document / Homeric Hymn to Demeter | 4.509990 | 4.820392 | 4.816211 | 4.816211 | 0.310402 | 0.000000 | 0.310402 |
| document / Theogony | 4.705676 | 4.965053 | 4.942266 | 4.942266 | 0.259376 | 0.000000 | 0.259376 |
| document / Works and Days | 4.653625 | 4.881899 | 4.795500 | 4.795500 | 0.228274 | 1.33e-16 | 0.228274 |
| document / Shield of Heracles | 4.619082 | 4.896116 | 4.863144 | 4.863144 | 0.277033 | 4.44e-17 | 0.277033 |
| document / Histories, book 1 (Herodotus) | 4.393918 | 4.787068 | 4.642541 | 4.642541 | 0.393150 | 4.44e-17 | 0.393150 |
| document / Histories, book 1 (Thucydides) | 4.323848 | 4.753427 | 4.613959 | 4.613959 | 0.429579 | 0.000000 | 0.429579 |
| document / Deipnosophistae, books 12-13 | 4.233885 | 4.685965 | 4.561370 | 4.561370 | 0.452080 | 8.88e-17 | 0.452080 |
| document / Bibliotheca historica, book 11 | 3.992307 | 4.518477 | 4.405177 | 4.405177 | 0.526170 | 1.33e-16 | 0.526170 |
| document / Lycurgus | 4.315890 | 4.868575 | 4.705074 | 4.705074 | 0.552685 | 8.88e-17 | 0.552685 |
| document / Alcibiades | 4.150430 | 4.683215 | 4.567630 | 4.567630 | 0.532785 | 0.000000 | 0.532785 |

**P2: 4–7 predecessors.**

| Level / unit | CE_CTW O | CE_0 O | CE_CTW R | CE_0 R | G_O | G_R | Q |
|---|---|---|---|---|---|---|---|
| block / HOMERIC_TRADITION | 4.477913 | 4.733888 | 4.708097 | 4.708097 | 0.255975 | 1.33e-16 | 0.255975 |
| block / HESIODIC_TRADITION | 4.556054 | 4.847359 | 4.844516 | 4.844516 | 0.291305 | 4.44e-17 | 0.291305 |
| block / HERODOTUS | 4.315565 | 4.691483 | 4.621264 | 4.621264 | 0.375918 | 4.44e-17 | 0.375918 |
| block / THUCYDIDES | 4.216529 | 4.648209 | 4.585934 | 4.585934 | 0.431680 | 4.44e-17 | 0.431680 |
| block / ATHENAEUS | 4.171896 | 4.605758 | 4.532228 | 4.532228 | 0.433863 | 1.78e-16 | 0.433863 |
| block / DIODORUS | 3.880698 | 4.372812 | 4.372352 | 4.372352 | 0.492114 | 8.88e-17 | 0.492114 |
| block / PLUTARCH | 4.158536 | 4.658718 | 4.588694 | 4.588694 | 0.500182 | 1.33e-16 | 0.500182 |
| document / Iliad | 4.476794 | 4.732908 | 4.706760 | 4.706760 | 0.256114 | 8.88e-17 | 0.256114 |
| document / Homeric Hymn to Demeter | 4.526268 | 4.776215 | 4.765851 | 4.765851 | 0.249948 | 0.000000 | 0.249948 |
| document / Theogony | 4.532573 | 4.864426 | 4.876013 | 4.876013 | 0.331853 | 4.44e-17 | 0.331853 |
| document / Works and Days | 4.637553 | 4.876956 | 4.804010 | 4.804010 | 0.239402 | 8.88e-17 | 0.239402 |
| document / Shield of Heracles | 4.468950 | 4.773869 | 4.855383 | 4.855383 | 0.304919 | 8.88e-17 | 0.304919 |
| document / Histories, book 1 (Herodotus) | 4.315565 | 4.691483 | 4.621264 | 4.621264 | 0.375918 | 4.44e-17 | 0.375918 |
| document / Histories, book 1 (Thucydides) | 4.216529 | 4.648209 | 4.585934 | 4.585934 | 0.431680 | 4.44e-17 | 0.431680 |
| document / Deipnosophistae, books 12-13 | 4.171896 | 4.605758 | 4.532228 | 4.532228 | 0.433863 | 1.78e-16 | 0.433863 |
| document / Bibliotheca historica, book 11 | 3.880698 | 4.372812 | 4.372352 | 4.372352 | 0.492114 | 8.88e-17 | 0.492114 |
| document / Lycurgus | 4.185436 | 4.708838 | 4.647579 | 4.647579 | 0.523402 | 4.44e-17 | 0.523402 |
| document / Alcibiades | 4.131342 | 4.608050 | 4.529165 | 4.529165 | 0.476708 | 8.88e-17 | 0.476708 |

**P3: ≥8 predecessors.**

| Level / unit | CE_CTW O | CE_0 O | CE_CTW R | CE_0 R | G_O | G_R | Q |
|---|---|---|---|---|---|---|---|
| block / HOMERIC_TRADITION | 4.615085 | 4.881905 | 4.737227 | 4.737227 | 0.266819 | 0.000000 | 0.266819 |
| block / HESIODIC_TRADITION | 4.739573 | 4.969353 | 4.897733 | 4.897733 | 0.229780 | 0.000000 | 0.229780 |
| block / HERODOTUS | 4.428661 | 4.829452 | 4.651975 | 4.651975 | 0.400791 | 8.88e-17 | 0.400791 |
| block / THUCYDIDES | 4.364599 | 4.793381 | 4.624601 | 4.624601 | 0.428782 | 4.44e-17 | 0.428782 |
| block / ATHENAEUS | 4.265530 | 4.726910 | 4.576247 | 4.576247 | 0.461379 | 1.33e-16 | 0.461379 |
| block / DIODORUS | 4.026584 | 4.563214 | 4.415258 | 4.415258 | 0.536629 | 8.88e-17 | 0.536629 |
| block / PLUTARCH | 4.261680 | 4.820053 | 4.654833 | 4.654833 | 0.558373 | 4.44e-17 | 0.558373 |
| document / Iliad | 4.618075 | 4.882699 | 4.734302 | 4.734302 | 0.264624 | 4.44e-17 | 0.264624 |
| document / Homeric Hymn to Demeter | 4.498711 | 4.851001 | 4.851105 | 4.851105 | 0.352290 | 4.44e-17 | 0.352290 |
| document / Theogony | 4.787086 | 5.012377 | 4.973425 | 4.973425 | 0.225291 | 0.000000 | 0.225291 |
| document / Works and Days | 4.665604 | 4.885584 | 4.789156 | 4.789156 | 0.219980 | 4.44e-17 | 0.219980 |
| document / Shield of Heracles | 4.730378 | 4.986739 | 4.868897 | 4.868897 | 0.256361 | 0.000000 | 0.256361 |
| document / Histories, book 1 (Herodotus) | 4.428661 | 4.829452 | 4.651975 | 4.651975 | 0.400791 | 8.88e-17 | 0.400791 |
| document / Histories, book 1 (Thucydides) | 4.364599 | 4.793381 | 4.624601 | 4.624601 | 0.428782 | 4.44e-17 | 0.428782 |
| document / Deipnosophistae, books 12-13 | 4.265530 | 4.726910 | 4.576247 | 4.576247 | 0.461379 | 1.33e-16 | 0.461379 |
| document / Bibliotheca historica, book 11 | 4.026584 | 4.563214 | 4.415258 | 4.415258 | 0.536629 | 8.88e-17 | 0.536629 |
| document / Lycurgus | 4.362880 | 4.926112 | 4.725784 | 4.725784 | 0.563232 | 4.44e-17 | 0.563232 |
| document / Alcibiades | 4.157436 | 4.710803 | 4.581748 | 4.581748 | 0.553367 | 0.000000 | 0.553367 |

**Table P4 — Q dispersion for the same C0 profiles.** Same source and keys as P1–P3, `metric=q`. Each entry is **mean / sample SD / min / max**, S=20, in bits/target; denominator follows the column band in N1/N2. Dispersion of each of the other six metrics is retained in the extended source with identical keys and fields; no SD or extreme is averaged across lower-level units.

| Level / unit | All: mean / SD / min / max | 4–7: mean / SD / min / max | ≥8: mean / SD / min / max |
|---|---|---|---|
| block / HOMERIC_TRADITION | 0.262112 / 0.002318 / 0.255151 / 0.265862 | 0.255975 / 0.002767 / 0.247406 / 0.260333 | 0.266819 / 0.002306 / 0.261091 / 0.270102 |
| block / HESIODIC_TRADITION | 0.252991 / 0.005909 / 0.241140 / 0.262615 | 0.291305 / 0.003463 / 0.285084 / 0.300607 | 0.229780 / 0.009704 / 0.211525 / 0.244282 |
| block / HERODOTUS | 0.393150 / 0.002549 / 0.388604 / 0.396779 | 0.375918 / 0.003878 / 0.368083 / 0.382311 | 0.400791 / 0.002461 / 0.395584 / 0.404595 |
| block / THUCYDIDES | 0.429579 / 0.002932 / 0.424545 / 0.434837 | 0.431680 / 0.005159 / 0.418265 / 0.438820 | 0.428782 / 0.002895 / 0.423241 / 0.435230 |
| block / ATHENAEUS | 0.452080 / 0.001850 / 0.448172 / 0.455421 | 0.433863 / 0.002786 / 0.429777 / 0.438473 | 0.461379 / 0.002067 / 0.456726 / 0.465852 |
| block / DIODORUS | 0.526170 / 0.001907 / 0.522185 / 0.528965 | 0.492114 / 0.003483 / 0.485031 / 0.499240 | 0.536629 / 0.002277 / 0.531753 / 0.540485 |
| block / PLUTARCH | 0.542858 / 0.003466 / 0.536831 / 0.549146 | 0.500182 / 0.005478 / 0.491138 / 0.511872 | 0.558373 / 0.003683 / 0.550327 / 0.565281 |
| document / Iliad | 0.260925 / 0.002291 / 0.254166 / 0.264647 | 0.256114 / 0.002716 / 0.247667 / 0.260152 | 0.264624 / 0.002320 / 0.258808 / 0.268103 |
| document / Homeric Hymn to Demeter | 0.310402 / 0.007308 / 0.291010 / 0.319645 | 0.249948 / 0.010015 / 0.224712 / 0.268158 | 0.352290 / 0.007889 / 0.336169 / 0.365914 |
| document / Theogony | 0.259376 / 0.012746 / 0.229129 / 0.279556 | 0.331853 / 0.008230 / 0.320893 / 0.346012 | 0.225291 / 0.017569 / 0.185973 / 0.249684 |
| document / Works and Days | 0.228274 / 0.003938 / 0.220799 / 0.233793 | 0.239402 / 0.006746 / 0.225641 / 0.251901 | 0.219980 / 0.005922 / 0.210206 / 0.231469 |
| document / Shield of Heracles | 0.277033 / 0.007231 / 0.264111 / 0.290499 | 0.304919 / 0.010675 / 0.289196 / 0.323606 | 0.256361 / 0.009372 / 0.241328 / 0.273345 |
| document / Histories, book 1 (Herodotus) | 0.393150 / 0.002549 / 0.388604 / 0.396779 | 0.375918 / 0.003878 / 0.368083 / 0.382311 | 0.400791 / 0.002461 / 0.395584 / 0.404595 |
| document / Histories, book 1 (Thucydides) | 0.429579 / 0.002932 / 0.424545 / 0.434837 | 0.431680 / 0.005159 / 0.418265 / 0.438820 | 0.428782 / 0.002895 / 0.423241 / 0.435230 |
| document / Deipnosophistae, books 12-13 | 0.452080 / 0.001850 / 0.448172 / 0.455421 | 0.433863 / 0.002786 / 0.429777 / 0.438473 | 0.461379 / 0.002067 / 0.456726 / 0.465852 |
| document / Bibliotheca historica, book 11 | 0.526170 / 0.001907 / 0.522185 / 0.528965 | 0.492114 / 0.003483 / 0.485031 / 0.499240 | 0.536629 / 0.002277 / 0.531753 / 0.540485 |
| document / Lycurgus | 0.552685 / 0.003921 / 0.546292 / 0.560823 | 0.523402 / 0.007351 / 0.514594 / 0.542218 | 0.563232 / 0.004283 / 0.553102 / 0.569629 |
| document / Alcibiades | 0.532785 / 0.004046 / 0.524340 / 0.539983 | 0.476708 / 0.008946 / 0.456651 / 0.489381 | 0.553367 / 0.004069 / 0.545574 / 0.562361 |

### Both subordinate summaries in all six cells

With equal block weights in C0, the mean Q is 0.257551 for HEX and 0.468767 for PROSE_ALL;
their difference is −0.211216 bits/target. With eligible-target weights, the respective
means are 0.261015 and 0.463038, giving −0.202023 (S1). The two contrasts have sample
SDs 0.003639 and 0.002754 and computational min–max ranges −0.217762 to −0.204675 and
−0.209126 to −0.197321 (S2). These are two descriptions of the same finite procedure:
the average block and the average eligible target within each group.

The target weighting gives the Hesiodic block share 0.120263 of HEX instead of 0.500000
(S3), increasing the dominance of the Homeric material. Neither weighting corrects
the other or balances chronology, annotation or training. In the C0 folds, HEX supplies
0.166667 of training tokens when a HEX block is held out and 0.333333 when a prose block
is held out (S3); the group contrast therefore compares different fitted training
mixtures, not texts evaluated under one common model.

The mean HEX − PROSE_ALL Q contrast is negative under both weights in every declared
cell, with every observed per-cell computational range also below zero (S1–S2).
For a_total1 the two means are −0.222067 and −0.209439; for q_half, −0.177569 and
−0.165288; for D12, −0.209560 and −0.200845; for OTH, −0.203113 and −0.193254; for
UPOS, −0.237546 and −0.230473, in equal-block/eligible-target order. The seven block
Q means remain positive in all six cells (extended profiles). Reporting these signs
does not make seed agreement an acceptance criterion or an inferential test. Because
C0 has 20 seeds and the other cells ten, differences between these displayed cell
means are not the paired sensitivity estimates; those are D1–D3 below.

**Table S0 — group populations and replication counts.** Source: [contrasts.csv](../results/hexis31/v3-seed0-v3006/contrasts.csv), `seed=0`, `aggregation=equal_block`, `group=HEX|PROSE_ALL`; keys `(cell, seed, aggregation, group)`, values `n` (eligible targets per seed). These populations are the same under both weightings and across seeds; the weights themselves differ (S3). S is selected from `seed_summaries.csv` for the corresponding cell/group. HEX has two blocks, PROSE_ALL five; the contrast has no separate target denominator.

| Cell | HEX targets | PROSE_ALL targets | S |
|---|---|---|---|
| C0 | 53009 | 56099 | 20 |
| a_total1 | 53009 | 56099 | 10 |
| q_half | 53009 | 56099 | 10 |
| D12 | 53009 | 56099 | 10 |
| oth | 53460 | 56256 | 10 |
| upos | 53009 | 56099 | 10 |

**Table S1 — HEX, PROSE_ALL and HEX − PROSE_ALL, both weightings adjacent.** Source: [seed_summaries.csv](../results/hexis31/v3-seed0-v3006/seed_summaries.csv); filters `level=group`, `past_band=all`; keys `(cell, level, unit, aggregation, past_band, metric)`, where `unit=contrast` is HEX − PROSE_ALL. Entries select `mean`; all seven columns are bits/target. S=20 for C0 and 10 elsewhere. [contrasts.csv](../results/hexis31/v3-seed0-v3006/contrasts.csv) retains every seed under `(cell, seed, aggregation, group)` and its `n`; group `n` is the total eligible population under either weighting, while contrast `n` is not a loss denominator. Equal-block means use 2 HEX / 5 PROSE_ALL blocks; target-weighted means use their respective eligible totals. No pooled denominator is assigned to the difference of groups.

| Cell | Group or contrast | Weight | CE_CTW O | CE_0 O | CE_CTW R | CE_0 R | G_O | G_R | Q |
|---|---|---|---|---|---|---|---|---|---|
| C0 | HEX | Equal block | 4.612943 | 4.870495 | 4.801120 | 4.801120 | 0.257551 | 2.22e-17 | 0.257551 |
| C0 | HEX | Eligible target | 4.569352 | 4.830368 | 4.742992 | 4.742992 | 0.261015 | 3.91e-17 | 0.261015 |
| C0 | PROSE_ALL | Equal block | 4.235627 | 4.704395 | 4.572049 | 4.572049 | 0.468767 | 5.33e-17 | 0.468767 |
| C0 | PROSE_ALL | Eligible target | 4.229328 | 4.692366 | 4.561864 | 4.561864 | 0.463038 | 6.60e-17 | 0.463038 |
| C0 | contrast | Equal block | 0.377316 | 0.166100 | 0.229071 | 0.229071 | -0.211216 | -3.11e-17 | -0.211216 |
| C0 | contrast | Eligible target | 0.340024 | 0.138001 | 0.181128 | 0.181128 | -0.202023 | -2.69e-17 | -0.202023 |
| a_total1 | HEX | Equal block | 4.632902 | 4.869793 | 4.801216 | 4.801216 | 0.236892 | 1.78e-16 | 0.236892 |
| a_total1 | HEX | Eligible target | 4.585415 | 4.830287 | 4.743709 | 4.743709 | 0.244873 | 1.10e-16 | 0.244873 |
| a_total1 | PROSE_ALL | Equal block | 4.246784 | 4.705743 | 4.572853 | 4.572853 | 0.458959 | 1.60e-16 | 0.458959 |
| a_total1 | PROSE_ALL | Eligible target | 4.239279 | 4.693591 | 4.562698 | 4.562698 | 0.454311 | 1.56e-16 | 0.454311 |
| a_total1 | contrast | Equal block | 0.386118 | 0.164050 | 0.228363 | 0.228363 | -0.222067 | 1.78e-17 | -0.222067 |
| a_total1 | contrast | Eligible target | 0.346135 | 0.136697 | 0.181011 | 0.181011 | -0.209439 | -4.56e-17 | -0.209439 |
| q_half | HEX | Equal block | 4.662253 | 4.871714 | 4.803216 | 4.803216 | 0.209460 | 1.33e-16 | 0.209460 |
| q_half | HEX | Eligible target | 4.616769 | 4.832092 | 4.745695 | 4.745695 | 0.215323 | 1.67e-16 | 0.215323 |
| q_half | PROSE_ALL | Equal block | 4.318190 | 4.705219 | 4.572633 | 4.572633 | 0.387029 | 8.88e-17 | 0.387029 |
| q_half | PROSE_ALL | Eligible target | 4.312488 | 4.693099 | 4.562482 | 4.562482 | 0.380611 | 7.33e-17 | 0.380611 |
| q_half | contrast | Equal block | 0.344063 | 0.166494 | 0.230583 | 0.230583 | -0.177569 | 4.44e-17 | -0.177569 |
| q_half | contrast | Eligible target | 0.304281 | 0.138993 | 0.183212 | 0.183212 | -0.165288 | 9.36e-17 | -0.165288 |
| D12 | HEX | Equal block | 4.610482 | 4.869292 | 4.800729 | 4.800729 | 0.258810 | 0.000000 | 0.258810 |
| D12 | HEX | Eligible target | 4.568243 | 4.830146 | 4.743386 | 4.743386 | 0.261903 | 0.000000 | 0.261903 |
| D12 | PROSE_ALL | Equal block | 4.236087 | 4.704457 | 4.571742 | 4.571742 | 0.468370 | 3.55e-17 | 0.468370 |
| D12 | PROSE_ALL | Eligible target | 4.229653 | 4.692401 | 4.561638 | 4.561638 | 0.462748 | 4.60e-17 | 0.462748 |
| D12 | contrast | Equal block | 0.374395 | 0.164836 | 0.228987 | 0.228987 | -0.209560 | -3.55e-17 | -0.209560 |
| D12 | contrast | Eligible target | 0.338590 | 0.137745 | 0.181749 | 0.181749 | -0.200845 | -4.60e-17 | -0.200845 |
| oth | HEX | Equal block | 4.627883 | 4.883097 | 4.824585 | 4.824585 | 0.255214 | 0.000000 | 0.255214 |
| oth | HEX | Eligible target | 4.587044 | 4.845707 | 4.773379 | 4.773379 | 0.258664 | 0.000000 | 0.258664 |
| oth | PROSE_ALL | Equal block | 4.255230 | 4.713557 | 4.582755 | 4.582755 | 0.458327 | -7.11e-17 | 0.458327 |
| oth | PROSE_ALL | Eligible target | 4.251272 | 4.703189 | 4.574596 | 4.574596 | 0.451917 | -4.47e-17 | 0.451917 |
| oth | contrast | Equal block | 0.372653 | 0.169540 | 0.241830 | 0.241830 | -0.203113 | 7.11e-17 | -0.203113 |
| oth | contrast | Eligible target | 0.335771 | 0.142518 | 0.198782 | 0.198782 | -0.193254 | 4.47e-17 | -0.193254 |
| upos | HEX | Equal block | 2.768024 | 2.815518 | 2.856816 | 2.856816 | 0.047494 | 4.44e-17 | 0.047494 |
| upos | HEX | Eligible target | 2.769984 | 2.824711 | 2.871325 | 2.871325 | 0.054726 | 1.07e-17 | 0.054726 |
| upos | PROSE_ALL | Equal block | 2.722536 | 3.007576 | 3.004457 | 3.004457 | 0.285040 | 4.07e-07 | 0.285040 |
| upos | PROSE_ALL | Eligible target | 2.715452 | 3.000651 | 3.000932 | 3.000932 | 0.285200 | 2.51e-07 | 0.285199 |
| upos | contrast | Equal block | 0.045488 | -0.192058 | -0.147641 | -0.147641 | -0.237547 | -4.07e-07 | -0.237546 |
| upos | contrast | Eligible target | 0.054533 | -0.175940 | -0.129606 | -0.129607 | -0.230473 | -2.51e-07 | -0.230473 |

**Table S2 — computational Q dispersion, both weightings side by side.** Same source, filters and units as S1, `metric=q`. Each entry is **mean / sample SD / min / max**. Full seven-metric dispersion is in the same source rows, selected by `metric`; S is printed explicitly.

| Cell | Group or contrast | S | Equal block: mean / SD / min / max | Eligible target: mean / SD / min / max |
|---|---|---|---|---|
| C0 | HEX | 20 | 0.257551 / 0.003216 / 0.252135 / 0.263457 | 0.261015 / 0.002186 / 0.254986 / 0.265283 |
| C0 | PROSE_ALL | 20 | 0.468767 / 0.001510 / 0.465391 / 0.470672 | 0.463038 / 0.001339 / 0.459990 / 0.464924 |
| C0 | contrast | 20 | -0.211216 / 0.003639 / -0.217762 / -0.204675 | -0.202023 / 0.002754 / -0.209126 / -0.197321 |
| a_total1 | HEX | 10 | 0.236892 / 0.006868 / 0.225652 / 0.244100 | 0.244873 / 0.003058 / 0.239942 / 0.248582 |
| a_total1 | PROSE_ALL | 10 | 0.458959 / 0.003390 / 0.453831 / 0.463692 | 0.454311 / 0.003512 / 0.449801 / 0.460061 |
| a_total1 | contrast | 10 | -0.222067 / 0.007928 / -0.236100 / -0.212708 | -0.209439 / 0.004073 / -0.217533 / -0.203403 |
| q_half | HEX | 10 | 0.209460 / 0.006919 / 0.196467 / 0.219545 | 0.215323 / 0.006622 / 0.208108 / 0.226970 |
| q_half | PROSE_ALL | 10 | 0.387029 / 0.003381 / 0.382596 / 0.391389 | 0.380611 / 0.003539 / 0.376177 / 0.385585 |
| q_half | contrast | 10 | -0.177569 / 0.007330 / -0.189084 / -0.167704 | -0.165288 / 0.008210 / -0.176259 / -0.154141 |
| D12 | HEX | 10 | 0.258810 / 0.003422 / 0.252135 / 0.263457 | 0.261903 / 0.001642 / 0.260046 / 0.265283 |
| D12 | PROSE_ALL | 10 | 0.468370 / 0.001837 / 0.465391 / 0.470672 | 0.462748 / 0.001699 / 0.459990 / 0.464924 |
| D12 | contrast | 10 | -0.209560 / 0.003481 / -0.215566 / -0.204675 | -0.200845 / 0.002344 / -0.204879 / -0.197321 |
| oth | HEX | 10 | 0.255214 / 0.003708 / 0.248681 / 0.260299 | 0.258664 / 0.002209 / 0.255261 / 0.262305 |
| oth | PROSE_ALL | 10 | 0.458327 / 0.005513 / 0.450781 / 0.465553 | 0.451917 / 0.005811 / 0.444222 / 0.459488 |
| oth | contrast | 10 | -0.203113 / 0.005876 / -0.212309 / -0.194089 | -0.193254 / 0.006615 / -0.204227 / -0.185222 |
| upos | HEX | 10 | 0.047494 / 0.002084 / 0.043789 / 0.050215 | 0.054726 / 0.001875 / 0.050874 / 0.057148 |
| upos | PROSE_ALL | 10 | 0.285040 / 0.002038 / 0.282827 / 0.288896 | 0.285199 / 0.002135 / 0.283051 / 0.289145 |
| upos | contrast | 10 | -0.237546 / 0.003081 / -0.242562 / -0.234172 | -0.230473 / 0.002836 / -0.234060 / -0.226157 |

**Table S3 — populations and weights.** Source: [aggregation_weights.csv](../results/hexis31/v3-seed0-v3006/aggregation_weights.csv); filters `seed=0`, cells C0/oth/q_half, both aggregations; key `(cell, seed, aggregation, held_block_key)`. `n` is eligible targets per held-out block; `share` is its within-group summary weight. `training_tokens/available_tokens` is the block's sampling quota when it contributes, not the held-out population. `training_share` uses available retained tokens as denominator. `fold_training_tokens` and `fold_share_HEX/PROSE_ALL` refer to the training of the fold holding out the named block. Shares are fractions, not percentages. The complete 980-row source includes all seeds/cells. a_total1/D12/upos share these C0 count/weight/quota fields; OTH changes populations and q_half changes the quota.

| Cell / block | n | Equal share | Target share | Contributor quota / available | Sample fraction | Fold training | Fold HEX share | Fold PROSE share |
|---|---|---|---|---|---|---|---|---|
| C0 / HOMERIC_TRADITION | 46634 | 0.500000 | 0.879737 | 8884 / 71088 | 0.124972 | 53304 | 0.166667 | 0.833333 |
| C0 / HESIODIC_TRADITION | 6375 | 0.500000 | 0.120263 | 8884 / 9282 | 0.957121 | 53304 | 0.166667 | 0.833333 |
| C0 / HERODOTUS | 12946 | 0.200000 | 0.230771 | 8884 / 17301 | 0.513496 | 53304 | 0.333333 | 0.666667 |
| C0 / THUCYDIDES | 7227 | 0.200000 | 0.128826 | 8884 / 9346 | 0.950567 | 53304 | 0.333333 | 0.666667 |
| C0 / ATHENAEUS | 16691 | 0.200000 | 0.297528 | 8884 / 23133 | 0.384040 | 53304 | 0.333333 | 0.666667 |
| C0 / DIODORUS | 12334 | 0.200000 | 0.219861 | 8884 / 15266 | 0.581947 | 53304 | 0.333333 | 0.666667 |
| C0 / PLUTARCH | 6901 | 0.200000 | 0.123015 | 8884 / 8884 | 1.000000 | 53304 | 0.333333 | 0.666667 |
| oth / HOMERIC_TRADITION | 47062 | 0.500000 | 0.880322 | 8884 / 71547 | 0.124170 | 53304 | 0.166667 | 0.833333 |
| oth / HESIODIC_TRADITION | 6398 | 0.500000 | 0.119678 | 8884 / 9308 | 0.954448 | 53304 | 0.166667 | 0.833333 |
| oth / HERODOTUS | 12994 | 0.200000 | 0.230980 | 8884 / 17349 | 0.512076 | 53304 | 0.333333 | 0.666667 |
| oth / THUCYDIDES | 7234 | 0.200000 | 0.128591 | 8884 / 9353 | 0.949856 | 53304 | 0.333333 | 0.666667 |
| oth / ATHENAEUS | 16786 | 0.200000 | 0.298386 | 8884 / 23231 | 0.382420 | 53304 | 0.333333 | 0.666667 |
| oth / DIODORUS | 12334 | 0.200000 | 0.219248 | 8884 / 15266 | 0.581947 | 53304 | 0.333333 | 0.666667 |
| oth / PLUTARCH | 6908 | 0.200000 | 0.122796 | 8884 / 8893 | 0.998988 | 53304 | 0.333333 | 0.666667 |
| q_half / HOMERIC_TRADITION | 46634 | 0.500000 | 0.879737 | 4442 / 71088 | 0.062486 | 26652 | 0.166667 | 0.833333 |
| q_half / HESIODIC_TRADITION | 6375 | 0.500000 | 0.120263 | 4442 / 9282 | 0.478561 | 26652 | 0.166667 | 0.833333 |
| q_half / HERODOTUS | 12946 | 0.200000 | 0.230771 | 4442 / 17301 | 0.256748 | 26652 | 0.333333 | 0.666667 |
| q_half / THUCYDIDES | 7227 | 0.200000 | 0.128826 | 4442 / 9346 | 0.475284 | 26652 | 0.333333 | 0.666667 |
| q_half / ATHENAEUS | 16691 | 0.200000 | 0.297528 | 4442 / 23133 | 0.192020 | 26652 | 0.333333 | 0.666667 |
| q_half / DIODORUS | 12334 | 0.200000 | 0.219861 | 4442 / 15266 | 0.290973 | 26652 | 0.333333 | 0.666667 |
| q_half / PLUTARCH | 6901 | 0.200000 | 0.123015 | 4442 / 8884 | 0.500000 | 26652 | 0.333333 | 0.666667 |

### Paired sensitivity register

The paired estimates compare each perturbation with C0 on seeds 0–9 and preserve both
weights. Under a_total1, the mean change in the Q contrast is −0.012507 for equal
blocks and −0.008594 for eligible-target weights (D2). The block changes are not
uniform: DIODORUS increases by 0.033702, while the other six block means decrease
(D1). PLUTARCH's paired range spans −0.026928 to 0.001497. These are observed responses
to the declared Dirichlet prior change; no particular node or annotation is identified
as their cause. This cell does not vary the stop/split prior.

Halving the training quota reduces mean Q in all seven blocks. The contrast changes
by +0.031991 and +0.035557 under the two weights, bringing the negative contrast closer
to zero (D1–D2). This is a comparison of the two specified training budgets, not a
learning curve or a claim that the change is linear. OTH also reduces all seven block
Q means, and changes the contrast by +0.006447 and +0.007591. It changes the retained
symbols, alphabet, sampling endpoint and eligible population; its difference is a task
comparison, not an isolated effect of adding a dependency label.

Increasing the maximum depth from D8 to D12 gives mean paired contrast changes of
−1.47e-10 and −1.07e-10 bits/target. The tiny values are retained in D1–D3: the two HEX
block differences are recorded as zero, while several prose folds have small nonzero
differences. The evaluated depth increase changes the measured gains only at these
small scales. It does not demonstrate the absence of dependencies beyond eight symbols
or that longer structure is learnable from this training. The visible difference
between the C0 and D12 means in S1 also reflects their different seed coverage.

UPOS changes the mean paired contrast by −0.027986 and −0.029628. Its exact C0 mask
allows the same eligible positions, but its smaller alphabet changes the prediction
task and the total Dirichlet mass. Lower CE or a concordant contrast sign cannot be
read as a decomposition of DEPREL information, nor does subtracting UPOS from C0 measure
the independent contribution of DEPREL. The full seven-component paired differences
in D3 keep the root losses and shuffled gains visible beside Q.

The prespecified history bands give a further descriptive distinction (P2–P4).
For the Homeric block, mean Q is 0.255975 at 4–7 predecessors and 0.266819 at ≥8;
the Hesiodic means instead decrease from 0.291305 to 0.229780. HERODOTUS, ATHENAEUS,
DIODORUS and PLUTARCH have higher means in the latter band, while THUCYDIDES changes
from 0.431680 to 0.428782. At document level, the Hymn changes from 0.249948 to 0.352290,
whereas Theogony changes from 0.331853 to 0.225291. These bands contain different
positions and sentence-length mixtures; they are not interventions on history length.
In D12, membership in ≥8 does not guarantee twelve predecessors. No new band or
post-hoc context selection is used.

The [sensitivity and weighting figure](../results/hexis31/v3-seed0-v3006/figure__sensitivities_two_weights.svg)
places cell contrasts, paired changes and block means by history band side by side.
The left panel's bars are computational min–max ranges; the paired panel contains the
ten seed differences, and the band panel contains block means, not additional replicates.

**Tables D1–D2 — paired Q differences.** Sources: [sensitivity_pairs.csv](../results/hexis31/v3-seed0-v3006/sensitivity_pairs.csv) and [seed_summaries.csv](../results/hexis31/v3-seed0-v3006/seed_summaries.csv). D1 selects `level=block_difference`, D2 `level=group_difference`, both `past_band=all`, `metric=q`, all five non-C0 cells. Keys are `(cell, level, unit, aggregation, past_band, metric)` in the summaries; each underlying paired row additionally has `seed`, `reference=C0`, `value`, `reference_value`, `difference`. Every entry is **mean / sample SD / min / max** of `cell − C0` on seeds **0–9**, S=10. Units: bits/target; each operand uses its own N1/N2/S1 population. In particular OTH changes the target population; the paired seed does not equate the two tasks. These rows never subtract C0's 20-seed mean. All seven metrics and both block history bands are available under the same keys in the linked sources (there is no document-difference level or group-band contrast).

| Cell | Block | ΔQ: mean / SD / min / max (S=10) |
|---|---|---|
| a_total1 | HOMERIC_TRADITION | -0.015483 / 0.003223 / -0.020447 / -0.010235 |
| a_total1 | HESIODIC_TRADITION | -0.028353 / 0.011589 / -0.051210 / -0.017593 |
| a_total1 | HERODOTUS | -0.031210 / 0.003654 / -0.039306 / -0.026207 |
| a_total1 | THUCYDIDES | -0.023760 / 0.005404 / -0.032646 / -0.014981 |
| a_total1 | ATHENAEUS | -0.013819 / 0.005657 / -0.023024 / -0.003844 |
| a_total1 | DIODORUS | 0.033702 / 0.003796 / 0.026602 / 0.038211 |
| a_total1 | PLUTARCH | -0.011967 / 0.008285 / -0.026928 / 0.001497 |
| q_half | HOMERIC_TRADITION | -0.045703 / 0.008675 / -0.061376 / -0.032304 |
| q_half | HESIODIC_TRADITION | -0.052996 / 0.013293 / -0.068737 / -0.026446 |
| q_half | HERODOTUS | -0.078796 / 0.004198 / -0.084926 / -0.071903 |
| q_half | THUCYDIDES | -0.062612 / 0.003738 / -0.067233 / -0.055237 |
| q_half | ATHENAEUS | -0.080627 / 0.004565 / -0.086353 / -0.073051 |
| q_half | DIODORUS | -0.094805 / 0.006059 / -0.102723 / -0.081424 |
| q_half | PLUTARCH | -0.089863 / 0.004640 / -0.098617 / -0.084316 |
| D12 | HOMERIC_TRADITION | 0.000000 / 0.000000 / 0.000000 / 0.000000 |
| D12 | HESIODIC_TRADITION | 0.000000 / 0.000000 / 0.000000 / 0.000000 |
| D12 | HERODOTUS | 8.50e-14 / 2.57e-13 / 0.000000 / 8.14e-13 |
| D12 | THUCYDIDES | 1.28e-11 / 3.66e-11 / 0.000000 / 1.17e-10 |
| D12 | ATHENAEUS | 9.12e-11 / 2.40e-10 / 0.000000 / 7.64e-10 |
| D12 | DIODORUS | 0.000000 / 0.000000 / 0.000000 / 0.000000 |
| D12 | PLUTARCH | 6.32e-10 / 1.17e-09 / 0.000000 / 3.51e-09 |
| oth | HOMERIC_TRADITION | -0.003134 / 0.000830 / -0.004758 / -0.002028 |
| oth | HESIODIC_TRADITION | -0.004058 / 0.000675 / -0.004998 / -0.002973 |
| oth | HERODOTUS | -0.006349 / 0.000528 / -0.007278 / -0.005303 |
| oth | THUCYDIDES | -0.004856 / 0.000465 / -0.005687 / -0.004099 |
| oth | ATHENAEUS | -0.006853 / 0.000681 / -0.008416 / -0.006226 |
| oth | DIODORUS | -0.027731 / 0.025441 / -0.053360 / -0.002403 |
| oth | PLUTARCH | -0.004425 / 0.000376 / -0.005075 / -0.003782 |
| upos | HOMERIC_TRADITION | -0.205866 / 0.003258 / -0.213970 / -0.201874 |
| upos | HESIODIC_TRADITION | -0.216767 / 0.007606 / -0.226872 / -0.200224 |
| upos | HERODOTUS | -0.149124 / 0.002344 / -0.152887 / -0.146287 |
| upos | THUCYDIDES | -0.185833 / 0.004414 / -0.191301 / -0.176748 |
| upos | ATHENAEUS | -0.189830 / 0.003823 / -0.194636 / -0.183502 |
| upos | DIODORUS | -0.149833 / 0.001946 / -0.152254 / -0.146433 |
| upos | PLUTARCH | -0.242031 / 0.004724 / -0.246947 / -0.233242 |

| Cell | Group or contrast | Equal block ΔQ: mean / SD / min / max | Eligible target ΔQ: mean / SD / min / max |
|---|---|---|---|
| a_total1 | HEX | -0.021918 / 0.005423 / -0.033372 / -0.016050 | -0.017031 / 0.002668 / -0.020104 / -0.013263 |
| a_total1 | PROSE_ALL | -0.009411 / 0.002530 / -0.013273 / -0.005842 | -0.008437 / 0.002686 / -0.011853 / -0.003988 |
| a_total1 | contrast | -0.012507 / 0.007104 / -0.027529 / -0.006208 | -0.008594 / 0.003351 / -0.015835 / -0.005406 |
| q_half | HEX | -0.049350 / 0.005608 / -0.056928 / -0.041442 | -0.046580 / 0.006888 / -0.057175 / -0.034987 |
| q_half | PROSE_ALL | -0.081341 / 0.002453 / -0.085438 / -0.076759 | -0.082137 / 0.002889 / -0.086532 / -0.076649 |
| q_half | contrast | 0.031991 / 0.005564 / 0.025453 / 0.041245 | 0.035557 / 0.008034 / 0.022729 / 0.045450 |
| D12 | HEX | 0.000000 / 0.000000 / 0.000000 / 0.000000 | 0.000000 / 0.000000 / 0.000000 / 0.000000 |
| D12 | PROSE_ALL | 1.47e-10 / 2.37e-10 / 2.56e-14 / 7.27e-10 | 1.07e-10 / 1.59e-10 / 1.65e-14 / 4.69e-10 |
| D12 | contrast | -1.47e-10 / 2.37e-10 / -7.27e-10 / -2.56e-14 | -1.07e-10 / 1.59e-10 / -4.69e-10 / -1.65e-14 |
| oth | HEX | -0.003596 / 0.000673 / -0.004878 / -0.002735 | -0.003240 / 0.000782 / -0.004784 / -0.002273 |
| oth | PROSE_ALL | -0.010043 / 0.005172 / -0.015410 / -0.004858 | -0.010831 / 0.005653 / -0.016763 / -0.005244 |
| oth | contrast | 0.006447 / 0.005391 / 0.000241 / 0.012083 | 0.007591 / 0.005901 / 0.000652 / 0.013579 |
| upos | HEX | -0.211316 / 0.004349 / -0.217380 / -0.202808 | -0.207177 / 0.003132 / -0.214409 / -0.203024 |
| upos | PROSE_ALL | -0.183330 / 0.002345 / -0.186673 / -0.178806 | -0.177549 / 0.002139 / -0.180619 / -0.173158 |
| upos | contrast | -0.027986 / 0.003605 / -0.036513 / -0.024003 | -0.029628 / 0.002890 / -0.034848 / -0.026339 |

**Table D3 — all seven components of the paired contrast differences.** Same sources and units, `level=group_difference`, `unit=contrast`, `past_band=all`; entries select `mean`, S=10. This retains the direction of each loss and gain change beside ΔQ. The complete dispersion and HEX/PROSE_ALL component means are in the linked summaries, without selection by sign.

| Cell | Weight | ΔCE_CTW O | ΔCE_0 O | ΔCE_CTW R | ΔCE_0 R | ΔG_O | ΔG_R | ΔQ |
|---|---|---|---|---|---|---|---|---|
| a_total1 | Equal block | 0.011722 | -0.000785 | -0.000624 | -0.000624 | -0.012507 | 5.33e-17 | -0.012507 |
| a_total1 | Eligible target | 0.007545 | -0.001049 | -0.000737 | -0.000737 | -0.008594 | 3.14e-19 | -0.008594 |
| q_half | Equal block | -0.030332 | 0.001659 | 0.001596 | 0.001596 | 0.031991 | 7.99e-17 | 0.031991 |
| q_half | Eligible target | -0.034309 | 0.001248 | 0.001464 | 0.001464 | 0.035557 | 1.40e-16 | 0.035557 |
| D12 | Equal block | 1.47e-10 | 0.000000 | 0.000000 | 0.000000 | -1.47e-10 | 0.000000 | -1.47e-10 |
| D12 | Eligible target | 1.07e-10 | 0.000000 | 0.000000 | 0.000000 | -1.07e-10 | 0.000000 | -1.07e-10 |
| oth | Equal block | -0.001742 | 0.004705 | 0.012844 | 0.012844 | 0.006447 | 1.07e-16 | 0.006447 |
| oth | Eligible target | -0.002819 | 0.004773 | 0.017034 | 0.017034 | 0.007591 | 9.06e-17 | 0.007591 |
| upos | Equal block | -0.328907 | -0.356894 | -0.376628 | -0.376628 | -0.027987 | -4.07e-07 | -0.027986 |
| upos | Eligible target | -0.284057 | -0.313686 | -0.311355 | -0.311355 | -0.029628 | -2.51e-07 | -0.029628 |

### R1: all three marginal comparisons

The JSD between the uniformly averaged HEX and PROSE_ALL block distributions is
0.119662 bits for ud23, 0.119827 for ud23_oth and 0.074570 for upos_only (R1b).
These values describe differences in complete retained marginal distributions,
including initial tokens. They use neither the primary-score denominators nor the
leave-one-block-out training roots.

R1a retains every block pair in each representation. In ud23, the two HEX blocks have
JSD 0.019219; prose–prose values run from 0.008898 (ATHENAEUS/HERODOTUS) to 0.031830
(DIODORUS/HERODOTUS), and cross-group values from 0.105706 (HOMERIC_TRADITION/HERODOTUS)
to 0.159383 (HESIODIC_TRADITION/DIODORUS). This is a description of the listed marginals,
not a classification test, clustering result or proof of homogeneous groups. The
[R1 figure](../results/hexis31/v3-seed0-v3006/figure__R1.svg) shows the ud23 matrix,
the three centroid divergences and all centroid contributions; R1c links every symbol
contribution for every pair as well. JSD is called a divergence, not a metric distance.
Marginal differences neither explain away nor validate Q, which describes a different
population and a conditional prediction comparison. No inferential uncertainty is
assigned to these three deterministic R1 calculations.

R1 uses complete original retained tokens, **including sentence-initial tokens**,
from the seven primary blocks, not only eligible targets, sampled training roots or
inventory-only texts. It has no seed dimension. [root_distributions.csv](../results/hexis31/v3-seed0-v3006/root_distributions.csv) holds 1,512 rows keyed by `(variant, block, symbol_id)`, with unsmoothed `count`,
`empirical_frequency=count/N_all` and `smoothed_frequency=(count+0.5)/(N_all+0.5m)`.
Complete block token counts come from the deposited §3.3 table (C0/UPOS 154,300,
OTH 154,947 across primary blocks); per-document counts are in V1 `documents.csv`.

**Table R1a — all 21 unordered pairs, three representations.** Source: [jsd_pairs.csv](../results/hexis31/v3-seed0-v3006/jsd_pairs.csv); no row excluded; keys `(variant, block_a, block_b)`, value `jsd` in bits. Each column reconstructs its full 7×7 matrix by reflection, with diagonal zero; no averaging or new JSD computation is involved. Variant alphabets m=100/105/11 and denominators are the smoothed full-block distributions above.

| Block a | Block b | ud23 | ud23_oth | upos_only |
|---|---|---|---|---|
| ATHENAEUS | DIODORUS | 0.020419 | 0.022237 | 0.011264 |
| ATHENAEUS | HERODOTUS | 0.008898 | 0.009087 | 0.004768 |
| ATHENAEUS | HESIODIC_TRADITION | 0.122103 | 0.121955 | 0.071131 |
| ATHENAEUS | HOMERIC_TRADITION | 0.109465 | 0.109125 | 0.068845 |
| ATHENAEUS | PLUTARCH | 0.012499 | 0.013178 | 0.004465 |
| ATHENAEUS | THUCYDIDES | 0.011728 | 0.012546 | 0.004326 |
| DIODORUS | HERODOTUS | 0.031830 | 0.033030 | 0.022657 |
| DIODORUS | HESIODIC_TRADITION | 0.159383 | 0.160368 | 0.105904 |
| DIODORUS | HOMERIC_TRADITION | 0.148153 | 0.150556 | 0.109659 |
| DIODORUS | PLUTARCH | 0.019680 | 0.020078 | 0.011243 |
| DIODORUS | THUCYDIDES | 0.026261 | 0.026569 | 0.017228 |
| HERODOTUS | HESIODIC_TRADITION | 0.129018 | 0.129026 | 0.073721 |
| HERODOTUS | HOMERIC_TRADITION | 0.105706 | 0.105875 | 0.065179 |
| HERODOTUS | PLUTARCH | 0.012127 | 0.012491 | 0.004722 |
| HERODOTUS | THUCYDIDES | 0.010295 | 0.010672 | 0.003507 |
| HESIODIC_TRADITION | HOMERIC_TRADITION | 0.019219 | 0.019727 | 0.006041 |
| HESIODIC_TRADITION | PLUTARCH | 0.143105 | 0.143201 | 0.079803 |
| HESIODIC_TRADITION | THUCYDIDES | 0.133590 | 0.133860 | 0.073182 |
| HOMERIC_TRADITION | PLUTARCH | 0.126905 | 0.127931 | 0.075758 |
| HOMERIC_TRADITION | THUCYDIDES | 0.113307 | 0.114601 | 0.065728 |
| PLUTARCH | THUCYDIDES | 0.009704 | 0.009738 | 0.003873 |

**Table R1b — centroid divergences.** Source: [jsd_centroids.csv](../results/hexis31/v3-seed0-v3006/jsd_centroids.csv); all rows, key `(variant, group_a, group_b)`, value `jsd` in bits. Each HEX centroid is the uniform mean of its two smoothed block distributions; PROSE_ALL uses five. These are neither target-weighted centroids nor averages of pair divergences.

| Variant | HEX blocks | PROSE_ALL blocks | Centroid JSD (bits) |
|---|---|---|---|
| ud23 | 2 | 5 | 0.119662 |
| ud23_oth | 2 | 5 | 0.119827 |
| upos_only | 2 | 5 | 0.074570 |

**R1c — complete contributions, available locally.** [jsd_contributions.csv](../results/hexis31/v3-seed0-v3006/jsd_contributions.csv) retains all **4,752** symbol contributions: keys `(variant, scope, a, b, symbol_id)`,
`scope=block_pair|group_centroid`, value `contribution` in bits. All symbols, including
zero contributions, are retained for all 21 pairs and each centroid comparison in
each representation: (21+1)×(100+105+11). `symbol` maps the frozen lexicographic ID.
There is no top-contributor selection. The numerical check compares every contribution
sum with the corresponding published JSD. Full centroid vectors are reconstructible
from the linked smoothed block frequencies with uniform weights within each group
(1/2 per HEX block, 1/5 per PROSE_ALL block).

### Diagnostics and resources: exact access paths

The [support and mixture figure](../results/hexis31/v3-seed0-v3006/figure__supports_mixture_masses.svg)
summarizes C0: node counts are averaged per model and arm, while evaluation masses are
pooled over documents, bands and seeds using all eligible targets; L_resolved uses
only positions with valid resolved mass. These denominators differ from the two
group-summary weightings. X1 retains the full diagnostics of all cells and seeds;
X2–X3 give the explicitly fixed C0 seed-0 slice, not a selected campaign extreme.

In that slice, the original models record root_stop 0.000000 and negative root
stop-minus-split log-evidence differences, while the shuffled models record root_stop
1.000000 and positive differences (X2). The original mixtures assign mass beyond the
root; the shuffled L_resolved means and unseen masses shown in X3 are zero. This is
numerical behavior at the recorded precision, not a general collapse theorem. The
full report includes nonzero shuffled gains, most visibly the UPOS/PLUTARCH seed-0
all-target G_R of 0.000020 bits/target (`block_pairs.csv`, cell=upos, seed=0,
held_block=PLUTARCH, past_band=all). The small shuffled gains are retained in Q.

Null L_resolved values and symbols unseen at the root are distinct diagnostics. In
the original C0 seed-0 Iliad rows, valid/null counts are 19,781/2 in band 4–7 and
25,731/1 in band ≥8; root-unseen target counts are one in each band (X3).
These records must not be converted into zero-length contexts or conflated with
the implicit unseen-branch encounters, which can occur even when their routed mass
is numerically zero. A materialized node with low support remains observed; its
presence supplies no guarantee of precision or grammatical interpretation.

The complete training-quota and fragment records accompany these diagnostics (S3,
X1). An internal fragment start resets the available history; omitted tokens do not
provide context. `direct_context_targets` counts the first min(D, fragment_length)
positions affected by such an internal reset, not eligible held-out scoring targets.
For example, the C0 seed-0 THUCYDIDES fold contains a Hesiodic contributor fragment
with start=1, end=3 and direct_context_targets=2, although a two-token stream has no
eligible test target. This clarifies the definition; it is not a new fragment ablation
or a bound on the effect of fragmentation on Q. Resource records below measure this
execution and do not add a model-complexity penalty to the losses.

**Table X1 — diagnostic source register, all cells/seeds included.** Each linked source is part of the same hash-verified manifest. The table specifies complete selections and denominators; nested histogram fields are JSON cells in the CSV, not missing supplementary files. No new cross-seed diagnostic aggregation is introduced.

| Source / rows | Selection and keys | Fields, units and denominator |
|---|---|---|
| [model_diagnostics.csv](../results/hexis31/v3-seed0-v3006/model_diagnostics.csv) / 980 | All; (cell, held_block_key, seed, arm) | `nodes`, `node_count_by_structural_depth`, `support_histogram_1_2to4_5to9_10plus_by_depth`: node counts per model/depth, support bins 1, 2–4, 5–9, ≥10; do not multiply by document count. `root_observed_symbol_count`, `root_unseen_symbol_count`: alphabet types. `root_stop`: probability; `delta_root_nats_stop_minus_split`: nats, with `delta_root_reason`. `fit_seconds`, `evaluation_seconds`: seconds; `peak_rss`: bytes, process high-water mark, not additive RAM. |
| [arm_diagnostics.csv](../results/hexis31/v3-seed0-v3006/arm_diagnostics.csv) / 3,080 | All; (cell, held_block_key, seed, doc_id, arm, past_band) | `n`: targets. `resolved_mean=sum_resolved_valid/resolved_valid_count`; zero valid mass is null with reason, never a length zero. `resolved_null_count_by_reason_no_resolved_mass`: null count. `unseen_mass_mean=sum_unseen_mass/n`; `sum_observed_mass_by_length_ℓ/n`: mass at ℓ ordinary edges, BOS excluded. `root_unseen_target_count/n`: fraction of targets unseen at root. `implicit_unseen_branch_encounter_count`: encounters with support 0, not materialized nodes. |
| [fragment_diagnostics.csv](../results/hexis31/v3-seed0-v3006/fragment_diagnostics.csv) / 2,940 | All; (cell, held_block_key, seed, contributor_key) | `fragment_count`, `internal_start_count`: fragment counts; `fragment_tokens`: retained tokens in cut fragments; `direct_context_targets = Σ min(D, fragment_length)` over fragments with `start>0` (§5.2): positions whose available context is directly affected by the internal reset, including initial positions, not the count of eligible scoring targets. Six contributors per pair; shared by both arms, not two independent samples. The named sample ledger records coordinates and subseeds. |
| [aggregation_weights.csv](../results/hexis31/v3-seed0-v3006/aggregation_weights.csv) / 980 | All; (cell, seed, aggregation, held_block_key) | `n`, `weight`, `share`: held-out populations and within-group weights. `training_tokens/available_tokens`: contributor quota/retained supply. `fold_training_tokens`: tokens after excluding the held-out block; `fold_share_*` uses that denominator. |
| [document_scores.csv](../results/hexis31/v3-seed0-v3006/document_scores.csv) / 1,540; [block_pairs.csv](../results/hexis31/v3-seed0-v3006/block_pairs.csv) / 1,470 | All; (cell, held_block_key, seed[, doc_id], past_band) | `n`, four `sum_loss_*` (bits), CE/G/Q (bits/target), `reason`; `changed_symbol_eligible_slot_count/eligible_slot_count` measures changed symbols only on eligible slots. Both bands are retained even if empty. |

The means of L_resolved are means of valid position values, not ratios of aggregated
mass moments. L_resolved is an assigned context length conditional on observed mass,
not reliability, grammatical depth or a maximum recoverable order. Masses by length and
unseen mass use all targets, and sum to one within tolerance after division by `n`.
Columns for lengths 9–12 are populated for D12; blank cells in the other depth-8 models
mean those lengths are outside the model, not `no_resolved_mass`. Empty scored buckets
retain n=0, additive sums=0 and null means/scores with reason `empty_bucket`.
`root_stop` saturation and tiny G_R values must remain recorded numerical behavior,
not a theorem that the shuffled CTW equals its root.

**Table X2 — model records at a fixed reference slice.** Source: [model_diagnostics.csv](../results/hexis31/v3-seed0-v3006/model_diagnostics.csv); filter `cell=C0, seed=0`, all seven held-out blocks and both arms. Key `(cell, held_block_key, seed, arm)`; counts per model, delta in nats, times in seconds, RSS in bytes. This is a reference slice, not a campaign mean or a selected extreme; X1 links all remaining models and their complete support histograms.

| Block / arm | Nodes | Root seen / unseen types | root_stop | delta_root (nats) | Fit s | Eval s | Peak RSS bytes |
|---|---|---|---|---|---|---|---|
| HOMERIC_TRADITION / original | 171304 | 82 / 18 | 0.000000 | -11315.194089 | 0.629680 | 1.726143 | 1277710336 |
| HOMERIC_TRADITION / shuffled | 193401 | 82 / 18 | 1.000000 | 4542.699079 | 0.880536 | 1.973282 | 1277710336 |
| HESIODIC_TRADITION / original | 170130 | 80 / 20 | 0.000000 | -11302.257111 | 0.636460 | 0.234558 | 1156141056 |
| HESIODIC_TRADITION / shuffled | 192158 | 80 / 20 | 1.000000 | 4729.027752 | 0.866225 | 0.235393 | 1156141056 |
| HERODOTUS / original | 166983 | 81 / 19 | 0.000000 | -10867.122089 | 0.624931 | 0.490825 | 1130033152 |
| HERODOTUS / shuffled | 188815 | 81 / 19 | 1.000000 | 4432.017910 | 0.843873 | 0.492131 | 1130033152 |
| THUCYDIDES / original | 167316 | 83 / 17 | 0.000000 | -10474.248757 | 0.555008 | 0.287599 | 1277710336 |
| THUCYDIDES / shuffled | 188599 | 83 / 17 | 1.000000 | 4413.447331 | 0.999279 | 0.287368 | 1277710336 |
| ATHENAEUS / original | 169942 | 81 / 19 | 0.000000 | -10447.308388 | 0.611543 | 0.635328 | 906403840 |
| ATHENAEUS / shuffled | 191016 | 81 / 19 | 1.000000 | 4394.965343 | 1.003647 | 0.637413 | 906403840 |
| DIODORUS / original | 168631 | 81 / 19 | 0.000000 | -9816.390961 | 0.611663 | 0.485879 | 1058783232 |
| DIODORUS / shuffled | 187585 | 81 / 19 | 1.000000 | 4346.570574 | 0.840481 | 0.485617 | 1058783232 |
| PLUTARCH / original | 166849 | 79 / 21 | 0.000000 | -9818.770438 | 0.563156 | 0.262022 | 1277710336 |
| PLUTARCH / shuffled | 187190 | 79 / 21 | 1.000000 | 4288.383063 | 1.005005 | 0.261826 | 1277710336 |

**Table X3 — evaluation records at the same fixed reference seed.** Source: [arm_diagnostics.csv](../results/hexis31/v3-seed0-v3006/arm_diagnostics.csv); filters `cell=C0, seed=0`, all documents, arms and bands; key `(cell, held_block_key, seed, doc_id, arm, past_band)`. Counts: `n`, valid `resolved_valid_count`, null `resolved_null_count_by_reason_no_resolved_mass`, `root_unseen_target_count`, `implicit_unseen_branch_encounter_count`. L selects `resolved_mean` (ordinary context length); unseen mass selects `unseen_mass_mean` (fraction over n). Full sums and every mass-by-length component are in X1, including all other cells/seeds.

| Document / arm / band | n | Valid / null L | Mean L | Mean unseen mass | Root-unseen targets | Implicit encounters |
|---|---|---|---|---|---|---|
| Iliad / original / 4_7 | 19783 | 19781 / 2 | 1.003277 | 0.000532 | 1 | 17096 |
| Iliad / original / ge8 | 25732 | 25731 / 1 | 1.003527 | 0.000790 | 1 | 25704 |
| Iliad / shuffled / 4_7 | 19783 | 19783 / 0 | 0.000000 | 0.000000 | 1 | 19517 |
| Iliad / shuffled / ge8 | 25732 | 25732 / 0 | 0.000000 | 0.000000 | 2 | 25732 |
| Homeric Hymn to Demeter / original / 4_7 | 458 | 458 / 0 | 1.000000 | 0.000570 | 0 | 445 |
| Homeric Hymn to Demeter / original / ge8 | 661 | 661 / 0 | 1.001523 | 0.000010 | 0 | 661 |
| Homeric Hymn to Demeter / shuffled / 4_7 | 458 | 458 / 0 | 0.000000 | 0.000000 | 1 | 452 |
| Homeric Hymn to Demeter / shuffled / ge8 | 661 | 661 / 0 | 0.000000 | 0.000000 | 1 | 661 |
| Theogony / original / 4_7 | 942 | 942 / 0 | 1.003186 | 0.000773 | 0 | 849 |
| Theogony / original / ge8 | 2003 | 2003 / 0 | 1.002509 | 0.000697 | 0 | 1944 |
| Theogony / shuffled / 4_7 | 942 | 942 / 0 | 0.000000 | 0.000000 | 0 | 929 |
| Theogony / shuffled / ge8 | 2003 | 2003 / 0 | 0.000000 | 0.000000 | 0 | 2003 |
| Works and Days / original / 4_7 | 887 | 887 / 0 | 1.006362 | 0.001466 | 0 | 780 |
| Works and Days / original / ge8 | 1190 | 1190 / 0 | 1.005046 | 0.002284 | 0 | 1190 |
| Works and Days / shuffled / 4_7 | 887 | 887 / 0 | 0.000000 | 0.000000 | 0 | 872 |
| Works and Days / shuffled / ge8 | 1190 | 1190 / 0 | 0.000000 | 0.000000 | 0 | 1190 |
| Shield of Heracles / original / 4_7 | 576 | 575 / 1 | 1.000000 | 0.001780 | 1 | 515 |
| Shield of Heracles / original / ge8 | 777 | 777 / 0 | 1.007767 | 0.000990 | 0 | 777 |
| Shield of Heracles / shuffled / 4_7 | 576 | 576 / 0 | 0.000000 | 0.000000 | 0 | 566 |
| Shield of Heracles / shuffled / ge8 | 777 | 777 / 0 | 0.000000 | 0.000000 | 1 | 777 |
| Histories, book 1 (Herodotus) / original / 4_7 | 3977 | 3977 / 0 | 1.139563 | 0.001784 | 0 | 3245 |
| Histories, book 1 (Herodotus) / original / ge8 | 8969 | 8969 / 0 | 1.134549 | 0.002371 | 0 | 8958 |
| Histories, book 1 (Herodotus) / shuffled / 4_7 | 3977 | 3977 / 0 | 0.000000 | 0.000000 | 0 | 3921 |
| Histories, book 1 (Herodotus) / shuffled / ge8 | 8969 | 8969 / 0 | 0.000000 | 0.000000 | 0 | 8969 |
| Histories, book 1 (Thucydides) / original / 4_7 | 1989 | 1989 / 0 | 1.154571 | 0.000673 | 0 | 1575 |
| Histories, book 1 (Thucydides) / original / ge8 | 5238 | 5236 / 2 | 1.136663 | 0.001867 | 3 | 5226 |
| Histories, book 1 (Thucydides) / shuffled / 4_7 | 1989 | 1989 / 0 | 0.000000 | 0.000000 | 1 | 1958 |
| Histories, book 1 (Thucydides) / shuffled / ge8 | 5238 | 5238 / 0 | 0.000000 | 0.000000 | 1 | 5238 |
| Deipnosophistae, books 12-13 / original / 4_7 | 5641 | 5640 / 1 | 1.146586 | 0.000955 | 0 | 4657 |
| Deipnosophistae, books 12-13 / original / ge8 | 11050 | 11044 / 6 | 1.154329 | 0.001839 | 7 | 11014 |
| Deipnosophistae, books 12-13 / shuffled / 4_7 | 5641 | 5641 / 0 | 0.000000 | 0.000000 | 2 | 5558 |
| Deipnosophistae, books 12-13 / shuffled / ge8 | 11050 | 11050 / 0 | 0.000000 | 0.000000 | 6 | 11050 |
| Bibliotheca historica, book 11 / original / 4_7 | 2898 | 2898 / 0 | 1.204018 | 0.000572 | 0 | 2087 |
| Bibliotheca historica, book 11 / original / ge8 | 9436 | 9434 / 2 | 1.205013 | 0.000725 | 2 | 9402 |
| Bibliotheca historica, book 11 / shuffled / 4_7 | 2898 | 2898 / 0 | 0.000000 | 0.000000 | 0 | 2858 |
| Bibliotheca historica, book 11 / shuffled / ge8 | 9436 | 9436 / 0 | 0.000000 | 0.000000 | 2 | 9436 |
| Lycurgus / original / 4_7 | 925 | 924 / 1 | 1.167335 | 0.002849 | 0 | 727 |
| Lycurgus / original / ge8 | 2568 | 2566 / 2 | 1.158710 | 0.003216 | 2 | 2566 |
| Lycurgus / shuffled / 4_7 | 925 | 925 / 0 | 0.000000 | 0.000000 | 0 | 911 |
| Lycurgus / shuffled / ge8 | 2568 | 2568 / 0 | 0.000000 | 0.000000 | 1 | 2568 |
| Alcibiades / original / 4_7 | 915 | 915 / 0 | 1.151767 | 0.001422 | 0 | 687 |
| Alcibiades / original / ge8 | 2493 | 2491 / 2 | 1.159464 | 0.001473 | 2 | 2488 |
| Alcibiades / shuffled / 4_7 | 915 | 915 / 0 | 0.000000 | 0.000000 | 0 | 900 |
| Alcibiades / shuffled / ge8 | 2493 | 2493 / 0 | 0.000000 | 0.000000 | 2 | 2493 |

Campaign resource totals remain the measured records in the dated V4/V5 section:
713.32 s summed fit time and 535.60 s summed evaluation time over 980 models, peak RSS
1,654,919,168 bytes; the V4 resume wall time in the manifest is 7,450.8 s. These are
historical measurements, not forecasts or performance guarantees. Per-model values are
in X1; the report manifest has separate report-stage resources. No resource sum is used
as a score or complexity penalty.

### Existing figures and review boundary

| Figure | Numerical companion / scope |
|---|---|
| [figure__corpus_annotation.svg](../results/hexis31/v3-seed0-v3006/figure__corpus_annotation.svg) | V1 documents.csv and audit_contingency.csv: quantities, retention and annotation census, including inventory_only. |
| [figure__block_document_profiles.svg](../results/hexis31/v3-seed0-v3006/figure__block_document_profiles.svg) | P1–P4; the linked extended seed summaries contain all profile components and bands. |
| [figure__sensitivities_two_weights.svg](../results/hexis31/v3-seed0-v3006/figure__sensitivities_two_weights.svg) | S1–S3, D1–D3; both weights and paired first-ten-seed differences. |
| [figure__R1.svg](../results/hexis31/v3-seed0-v3006/figure__R1.svg) | R1a–R1c: three complete pair tables and centroid/contribution records. |
| [figure__supports_mixture_masses.svg](../results/hexis31/v3-seed0-v3006/figure__supports_mixture_masses.svg) | X1–X3: model supports, assigned masses and resolved lengths with their own denominators. |

Byte identity of the five figures was checked during preparation. For this draft all
five were rasterized from the published SVGs (headless browser, 2,400 px wide; scripts
and previews in [v5-logs/closure/visual](../results/hexis31/v5-logs/closure/visual/)) and read against the text; no frozen figure was edited.
Every panel is legible and agrees with its companion tables: the shuffled-gain panels
of the profile figure use 10⁻¹⁶ and 10⁻¹⁵ axes, consistent with P1; the supports figure's
pooled C0 valid/null counts, 2,181,798/362 original and 2,182,160/0 shuffled, match
`arm_diagnostics.csv` and sum to 20 × 109,108. Two presentation limits of the frozen
figures are recorded, not corrected: in the support panel the stacked original bar at
structural depth 5 exceeds the upper axis limit and is clipped; in the band panel of
the sensitivity figure the block means are unlabelled points, so individual blocks are
read from P2–P3. Neither affects a published number.

### Limitations and permitted conclusions

**Permitted descriptive conclusions.** Under this frozen CTW, this encoding and these
block-excluding trainings (§1.3), the account supports only the following descriptions.

1. *Order advantage.* In C0 every block and document has positive mean Q, and in all
   six cells every block's computational minimum over seeds is positive (P1, P4 and the
   extended profiles). Q is a relative predictive advantage of the original order over
   the fixed within-sentence shuffle under this predictor. It is not an entropy rate,
   a mutual information of Greek, a grammatical memory or a cognitive difficulty.
2. *Shuffled control.* G_R is numerically null in the C0 profiles; the largest pair-level
   value among the 490 pairs is 0.000020 bits/target (upos, PLUTARCH, seed 0, all targets).
   This is measured behaviour of the chosen control (§16): no collapse theorem, and no
   attribution of all of G_O to linguistic order. In C0, Q and G_O coincide at the
   displayed precision because of this observation, not by definition; in upos they
   already differ in the sixth decimal (S1).
3. *Group summaries.* The HEX − PROSE_ALL Q contrast is negative under both weights in
   all six cells, with means from −0.237546 (upos, equal block) to −0.165288 (q_half,
   eligible target) and every per-cell computational range below zero (S1–S2). It
   describes two HEX and five prose blocks under different fold trainings. It is not an
   effect of metre, epoch, author, genre or form (§1.3, §3.5), and not a separation of
   populations; no size qualifier is attached to it.
4. *Sensitivities.* Signs and magnitudes of the paired changes depend on the cell and,
   under a_total1, on the block (DIODORUS moves opposite to the other six): dependence on
   the declared choices and on the distribution of targets (§16), reported without
   selecting a preferred result. D8/D12: no improvement in the evaluated configurations,
   not an absence of dependencies beyond eight symbols. C0/UPOS: contrasts of the same
   sign are a concordance of the summary in two representations, not proof that DEPREL
   does not contribute and not a measure of its contribution by subtraction. OTH is a
   different task with its own population.
5. *ADV_PART merging.* A mitigation of the documented PART/ADV discontinuity, not
   demonstrated annotation homogeneity. Its effect on G/Q is not identified: the campaign
   has no unmerged arm, and comparison with the pilot changes more than the merging (§4.2).
6. *R1.* In ud23 the centroid JSD is 0.119662 bits; cross-group pairs range 0.105706–0.159383
   and within-group pairs are at most 0.031830 (R1a–R1b). These are differences between
   complete marginal distributions. They neither explain nor validate Q.
7. *Inventory-only texts.* The six texts enter census and alphabet only; no conclusion
   is drawn on specificity relative to tragedy or other metres.

**Limitations that qualify every result above** (§16, §3.5):

- *Finite corpus.* One pinned UD Perseus release and eleven primary documents; nothing
  here generalizes to Greek, to the authors' complete works or to other annotations.
- *Two and five blocks.* Each group summary rests on two HEX and five PROSE_ALL units.
- *Work dominance.* The Iliad supplies 45,515 of the 46,634 HOMERIC_TRADITION eligible
  targets, and the target weighting gives that block 0.879737 of HEX (N2, S3).
- *Chronological and annotation confounding.* HEX coincides with the archaic component
  and no comparable archaic prose exists (§3.5). Before merging, the source had 11,270
  PART in HEX and none in prose (§4.2); CCONJ and DEPREL keep residual heterogeneity,
  and no annotator metadata allow a control.
- *Different training per fold.* Each held-out block is scored by a model trained on a
  different mixture; the HEX share of fold training is 0.166667 or 0.333333 (S3).
- *Offline annotations.* DEPREL is assigned from the complete sentence and may depend on
  later words and on the head; predicting labels does not simulate a reader, and the
  sequence loses the tree hierarchy (§1.3).
- *Weights.* The equal-block and eligible-target summaries describe the average block
  and the average target; neither corrects the other, and neither balances chronology,
  annotation or training (§8.2).
- *Control conditioned on sentence composition.* The shuffle permutes the whole composite
  symbols of each sampled or evaluated sentence, so Q concerns order given that
  composition. Permutation without replacement makes the control neither i.i.d. nor a
  universal estimate of bias (§7). Long sentences contribute more targets; excluding the
  first four symbols does not equalize them (§3.5).
- *Computational dispersion.* SD, minimum and maximum over seeds describe sampling and
  shuffling. No p-values, intervals, Holm corrections, Bayes factors or permutation ranks
  are computed, and no seed SD becomes uncertainty about ancient texts (§1.2, §16).
- *Pilots already observed.* The protocol is prospective after methodological development
  and real pilots, not a preregistration (§2). The historical C0 pilot (m=106, original
  arms only) recorded mean D_G −0.178025 bits/symbol over 20 seeds; the changed task,
  prior mass and seed convention make this campaign no replica of it.

**Design omissions** (§10, §16), fixed before the campaign and not motivated by its
results: no final sensitivity to the stop/split prior (a_total1 perturbs a different
prior); no cross-boundary evaluation; no specificity comparison with other metres;
D6, `rho09`, `bound` and every tragic evaluation retired; no factorial combinations.
No G/CE_0 ratio, DEPREL-only representation, label permutation, balanced model or
reaggregation without single works is added; dropping a work from a mean would not
remove it from the other folds' training and is not leave-one-document-out.

**Procedural reservations.** The V4 terminal log and exit status are lost. The CTW
losses of seeds 1–19 are not independently regenerated: §12.2 prescribes seed 0, and
the V4 check recomputes samples, shuffles, root losses and the C0 position-to-sum
reconstruction, not the CTW losses. The byte reconstruction of the 13 tables
and five figures and the figure rasterization ran as local checks; their scripts and logs
are published in `results/hexis31/v5-logs/closure/` since V3-007, which also publishes the
result artifacts and the C0 position vectors (§17.3). The raw data are not redistributed.

**Completion criterion.** As §16 requires, completion depends on correct execution, not
on sign, separation or confirmation of the pilot; no "absent effect" is asserted.

**First-review checkpoint.** The numerical checks found no discrepancy in the source
identities, displayed selections, denominator coverage, contrast direction or paired
seed sets. A separate read-only editorial check matched 1,987 displayed numeric fields
to source rows and the specified rounding, checked the 19 table shapes and every local
link, and verified all R1 contribution sums. The existing documentation checks passed:
`UV_NO_CACHE=1 uv run --python 3.12 --no-sync pytest -q -p no:cacheprovider tests/test_v31_docs.py`
(11 passed). `git diff --check` passed. A hash comparison with the preparation baseline
found only `docs/HANDOFF.md` changed; removing this new section recovers the previous
handoff byte for byte. The frozen perimeter, manifest and all 931 artifacts are unchanged.
The missing reconstruction record was addressed as documented above;
the lost V4 terminal log remains an explicit procedural limitation. The owner's
numerical review of that dossier was delegated to Codex, as recorded at the head of
this section.

**Second-review checkpoint.** The complete draft adds the interpretive text and the
limitations above, all selected from the already verified tables, V1 `documents.csv`
and the deposit. The dossier check was rerun on the complete draft (same 1,987 fields,
19 tables and links; only `docs/HANDOFF.md` changed; frozen perimeter, manifest and 931
artifacts unchanged). The two presentation limits of the figures are recorded above.
The owner then asked for the second review before proceeding. Checked against §§3.3, 5.2,
7–10 and 16, the source row counts and the THUCYDIDES seed-0 sample ledger, it corrected
four draft statements: Q = G_O at display precision is now limited to C0, since upos
differs in the sixth decimal; the largest G_R follows the six-decimal rule; the V4 check
is no longer said to recompute "every other quantity"; a repeated R1 sentence was removed.
It added the weighting limitation and the non-i.i.d. nature of the shuffle (§7, §8.2).

**Closure, 25 September 2026: V5 COMPLETED.** After the second review, the owner
authorized closure. This section became the statement of results and limitations; the
README received its summary (§17.2); the specification, roadmap, index, test inventory
and the three copies of the standing instructions record V0–V5 completed. The test
inventory keeps as PENDING only activities outside V0–V5: the publication act for
corpus derivatives (§17.3), the proposal (§17.1) and the English companions (V3-003).
Final acceptance, run once from `05ece9cf29c8976f9c059155ea2eb43a7c863335` with these
documentary changes only:
`UV_NO_CACHE=1 uv run --python 3.12 --no-sync pytest -q -p no:cacheprovider -rsx`
gave **431 passed** in 204.00 s, with no skip or xfail (Python 3.12.13). Ordinary and
`-m v31` collections both list the same 431 test IDs. `uv lock --check` resolved 23
packages with the lock unchanged. The documentary tests are part of that suite: deposit
and lock bytes, V3-001 acts, instruction copies, archive bytes and the tracked sdist.
A read-only hash comparison against the preparation baseline found changes only in the
nine documents named above. The 49 frozen files (`src/`, `tests/`, `config/`,
`conftest.py`, `pyproject.toml`, `uv.lock`) and the 102 archived files are unchanged.
Both manifests are unchanged (`3243fc32…` and `72b6cdee…`), all 931 artifact hashes
match, and run ID `6aa1b719…` is unchanged. Local drafts `docs/proposal/` and `scripts/`
remain untracked. There was no fit, push or data publication.
