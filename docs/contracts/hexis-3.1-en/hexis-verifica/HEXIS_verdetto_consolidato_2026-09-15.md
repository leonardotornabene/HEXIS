> **Non-normative companion translation; the Italian original governs** (V3-003, B2).
> Original: `docs/contracts/hexis-3.1/hexis-verifica/HEXIS_verdetto_consolidato_2026-09-15.md`, SHA-256 `9cf75b7618864fa208092f5ed163976a385ef5fb0bad806e846ff84661fa7a12`.
> Translated on 2026-09-25. Structure, numbering, tables, formulas, values and identifiers follow the original, including paths and file names; numbers use English notation. Any translator's note is marked *[Translator's note: …]* and changes nothing in the original.

# HEXIS — Consolidated verdict and compendium of the changes

**Date:** 15 September 2026.  
**Subject:** comparison of plan 3.0.1 with the two methodological reviews, the pinned data, the executable attachments and the repository.  
**Status:** consolidated proposal of change, **not applied and not ratified**. This report does not automatically replace the v2.1 instructions still present in the repository.

## 1. Verdict

**The downsizing is valid. Plan 3.0.1, however, requires a substantial revision before becoming the definitive basis of the new proposal and of the migration.** There is no need to change the model again, enlarge the corpus or recover the abandoned inference.

The recommended solution is a single one:

1. Descriptive study of the pinned Greek corpus, limited to the **within-sentence** order of the annotations.
2. Global `PART`/`ADV` merging, declared as a deliberate loss of detail, without attributing to it a complete normalization.
3. Main result made of the **seven block profiles**, with the eleven documents visible; HEX/prose difference as a subordinate summary conditional on the available trainings.
4. Frozen CTW, four-term Q, paired shuffling and JSD kept.
5. Six cells: `C0`, `a_total1`, `q_half`, `D12`, `oth`, `upos`. Elimination of D6, `rho09`, `bound` and of the final tragic evaluations.
6. Detailed per-position persistence only in C0; verifiable aggregates for the sensitivities. One manifest and a restricted completeness check replace the separate certification apparatus.
7. Correction of the attestations on the pilots: **the twenty-seed contrast already reconstructible is the original D_G, not a D_Q verified over twenty seeds**.

This choice goes from **1,400 to 980 scientific models**, eliminates **1,680 probe evaluations** and reduces the persisted positional rows from **12,704,540 to 2,182,160**. The reduction is respectively **30%** and **82.82% of the positional rows alone**; it is not a measure of the total saving of disk or time.

**Once the decisions of this report are consistently adopted, the design can be closed.** The checks on the implementation remain execution obligations; they do not require a further methodological expansion. The go-ahead for writing the proposal is not equivalent to passing the tests of the future software in advance.

## 2. Materials, authority and actual checks

Names used:

- **P:** [complete plan 3.0.1](/Users/leonardoTornabene/Desktop/HEXIS_piano_integrale_v3_2026-09-11.md).
- **A:** [methodological review of 14 September](/Users/leonardoTornabene/Desktop/HEXIS_3.0.1_revisione_metodologica.md).
- **B:** [second review, pasted text](/Users/leonardoTornabene/.codex/attachments/74e30dc0-3390-4556-89b5-7a954c50c3e8/pasted-text.txt).
- **Package:** [operational attachments](/Users/leonardoTornabene/Desktop/HEXIS_allegati_operativi_v3_2026-09-11.zip), including the historical CTW archive.
- **Repository:** `/Users/leonardoTornabene/Projects/hexis`, branch `g1/pre-audit`, HEAD `852644b6917790877c7b2ca5df2e76b17829d87c`.

The prescriptions of P, A and B were examined as content to be evaluated. They were not used to authorize real fits, ratify decisions or modify the project. The checks used readings of the corpus, recomputations of archived results, synthetic cases and the existing suite. **No new fits were run on the real texts.**

### 2.1 Material findings

| Object | Check of this review | Outcome |
|---|---|---|
| External plan and copy in the ZIP | Comparison of the bytes | Identical |
| Current package | SHA-256 of the 33 inventoried files | All match |
| Historical archive | SHA-256 of the 103 inventoried files | All match |
| Three Greek CoNLL-U files | SHA-256 of the local files | All match P §3.1 |
| Corpus | Direct count of the tokens with integer ID, sentences and identities | 202,989 tokens; 13,919 sentences; 18 prefixes; 17 documents |
| Three original encodings | Document recomputation of retention, eligibility and inventories | Counts of the attachments confirmed; m=106/112/12 |
| PART/ADV merging | Transformation without fitting | m=100/105/11; same mask and same coordinates |
| Repository | Git status and suite in the present environment | 327 passed, 17 skipped; only `scripts/` untracked |
| CTW | Reading of the formulas and independent case with rational enumeration | Prediction: maximum error 1.11×10⁻¹⁶ in the additional case |
| Depth | Synthetic counterexample with a dependency beyond D8 | D6/D8 about 1 bit; D12 about 0.01771 bits |
| Pilot | Inspection of the rows and of the production code | 140 original C0; historical shuffled control on 7 folds at seed 0 only |

The additional rational check is not the re-execution of the 120 historical cases: they are distinct evidence. The results of the 120 cases and of the 9,189 assertions are present in the verified attachments. The small synthetic battery was also re-executed with checks on the actual thresholds of P §12.1; the results are in the verification attachment.

The evidence files of this review are in the `evidenze/` folder next to the report. They contain counts, numerical findings and records of the checks, not the raw corpus.

### 2.2 The different probative strength of the reviews

A admits in §12 that it consulted neither the three CoNLL-U files nor the repository: its documentary checks of the corpus were consistency checks of the attachments, supplemented by public totals. They are not equivalent to a reconstruction of the source data. B identified a problem that those checks could not detect, and the new direct count confirms it.

Both reviews correctly recognize the consistency of the CTW core and the need for the inferential reduction. **B provides the better basis for the final perimeter. A contains useful findings, but also extrapolations and some errors that must not be adopted.**

## 3. Reasoned comparison: what to accept and what to correct

| Question | Finding against P, data or code | Consolidated decision |
|---|---|---|
| Finite and descriptive study | Compatible with the corpus, dependencies between works and absence of population sampling | Accept both |
| CTW and four-term Q | Consistent formulas; the shortcut can invert the sign | Keep |
| PART/ADV discontinuity, B | 11,270 PART in the two HEX blocks, zero in the five prose blocks | Correct the representation before the new freeze |
| «Final result already known», A §§1–3 | The 20 seeds contain original G; the paired shuffles needed to extend the identity Q=G to the whole campaign are missing | Correct; declare the G pilot and the actual coverage of the control |
| «D_Q not identified», A §4 | The descriptive statistic is defined; a separate effect of metre, epoch or exposure is not identified | Restrict the interpretive object, without declaring the number meaningless |
| `balanced` identifies the contrast, A §4.1 | The 50/50 equalizes a share but changes the budget; it does not equalize authors, annotation or similarity between training and test | Do not add the cell |
| Available history «excluded» as a problem, A §4.2 | The recomputation concerns G; two bands do not equalize the sentence distributions. With D12, ≥8 does not even saturate the admitted depth | Keep the two bands as diagnostics, without co-primary status |
| Profile before the contrast, A and B | Consistent with the actual design | Accept, with seven blocks and eleven document details |
| Reaggregation without works, A §4.3 | It does not remove that work from the trainings of the other folds | Do not call it leave-one-document-out nor a contamination check; do not make it a new deliverable |
| Athenaeus quotations from `subdoc`, A §4.3 | The XML files have passage references, not quotation markers | Do not introduce an automatic census not supported by the data |
| `deprel_only` attributes the phenomenon, A §5 | Different tasks do not give an additive decomposition of the gain | Do not add the cell |
| Same contrast in UPOS and C0 implies no DEPREL contribution, A §5 | The same difference between means can go with very different levels and behaviours | Forbid this deduction; describe only the observed concordance |
| Q=G «structural» and all of G is order, A §6.1 | Numerical identity in some fits, not a general property nor a linguistic identification | Keep four terms and actual arms in every cell |
| D6=D8=D12 «by construction», A §6.3 | The D6 pilot also shows non-zero deviations; a sharp synthetic counterexample exists | Remove D6 to narrow the check; keep D12 |
| Prior rho «inert», A §6.4 | Real and synthetic variations verifiable | Fix rho=0.5; eliminate the sensitivity, declaring the renunciation |
| `bound` useless because it measures 10⁻⁷, A §6.5 | In the pilot Diodorus changes by about −0.04781 bits | Eliminate it to limit the question to the within-sentence level, as B proposes |
| Generalizations on the thresholds, A §6.2 | A §12.5 correctly recognizes their dependence on the source; some conclusions of §6.2 nonetheless exceed that scope | Keep the limit illustrated by the synthetics, without universal constants |
| G/CE0 makes the alphabets comparable, A §7 | It is a ratio with respect to different baselines, not a universal scale | Do not add the metric |
| Token-weighted JSD mandatory, A §7 | R1 and Q have distinct populations and questions, already defined by P | Keep the original R1 and unsmoothed counts |
| Rank 1/21 to be reintroduced, A §§3,7 | Computable but not necessary; it provides no inferential validity | Keep the retirement of the label permutations |
| Tragic probe to be eliminated, B | It adds outputs and a scientific question without being a clean metrical control | Accept |
| Six cells, B | They keep local regularization, budget, higher depth and two representation choices | Accept |
| Reduced persistence, A | Feasible, but four sums alone do not reconstruct all the diagnostics | Accept with the minimum contract of §7 |
| Shuffled columns omitted because «constant», A | The root loss varies with the symbol; equality with the CTW is not guaranteed | Do not impose constants; keep the four losses where planned |
| Separate certificates to be simplified, A and B | Integrity and completeness are verifiable with a manifest and a restricted validator | Accept, keeping evidence and constraints on the bytes |

### 3.1 The most relevant quantitative error of review A

From `pilot_C0.json` one reconstructs:

\[
\overline{D_{G^O}}=-0.1780246797\quad\text{bit/simbolo},
\]

*[Translator's note: in the formula, kept as in the original apart from the decimal point, `bit/simbolo` means "bits/symbol".]*

with SD across seeds **0.0110277710** and observed range **[−0.1982444032, −0.1573585892]**. These quantities are reproducible. The historical file `shuffle_results.json` and its producer `verify_shuffle.py`, however, cover only **seven folds at seed 0**. For that seed the Q contrast is about **−0.1772407629** and coincides numerically with the G contrast.

The missing control in the other 19 seeds cannot be replaced by the supposition that it gives the same outcome. The same problem concerns the historical sensitivities, which have seven original rows each. A's table labelled D_Q for all configurations is in reality derived from original G.

The correct formulation is therefore: **the pilot already showed a separation of original G; the available paired control is compatible with Q=G in the verified cases. The result of the new campaign, above all after the change of the alphabet, has not yet been observed.** Changing seeds does not erase the exposure to the pilots; declaring it does not authorize inventing the missing results.

### 3.2 Why A's additions would not close the confounding

The `balanced` budget of 18,564 tokens is obtainable in principle: the residual Hesiodic block limits the HEX side to 9,282. But with respect to the 53,304 C0 tokens it changes exposure and quantity of training at the same time. Moreover the split between blocks remains to be defined: 9,282 is not exactly divisible by five or by four. A further rule and new contracts would be needed. A synthetic case in which 18,564 tokens suffice does not certify sufficiency for Greek.

The 50/50 share does not separate annotation, epoch, similarity between works and diversity of the contributors. The persistence of the sign would not exclude an effect of exposure. It is a different possible question, not the obligatory correction of this descriptive study.

Similarly, removing Athenaeus only from the mean keeps Athenaeus in the trainings of the scores of the other blocks. Removing the Iliad leaves its material in the trainings of the other folds. These operations measure the influence of the weights on the scores already estimated, not a pipeline redone without those works. The document profiles and the two weighting schemes already planned make the dominance visible without adding eleven contrasts.

## 4. Scientific decisions to be adopted

The identifiers C01–C30 constitute the operational list of the changes. They are concrete recommendations for the next revision of the contract.

### C01 — Rewrite question, title and promise of the project

Target question:

> In the pinned UD Perseus Greek corpus, what additional predictive advantage does the within-sentence order of the annotations offer over their within-sentence shuffling, under a frozen CTW trained on the other blocks? How do the profiles of the documents and blocks vary with representation, budget and essential choices of the predictor?

HEX/prose remains a descriptive reading of those profiles. Remove from the title and the objectives the promises of an effect of the metrical constraint, a universal signature, a memory of the grammar, transfer between regimes and generalization to Greek. The labels of the works do not certify the metre of every passage. [P §§1,3.5,16]

### C02 — Establish a single hierarchy of results

- **Main:** seven block Q, together with original/shuffled G and the four CE; the eleven documents must be readable separately.
- **Subordinate summary:** equal-block-weight D_Q, with original/shuffled D_G.
- **Mandatory second weighting:** the same quantities weighted by eligible targets.
- **Diagnostics:** two history bands, supports, masses, training data and retention.
- **Distributional reading:** R1/JSD with the population defined in P.

Do not give the eleven documents the status of eleven independent replicates. Keep the exclusion by block and the per-target mean within the block. The SD, the minimum and the maximum over seeds describe computational variability; do not use the ± symbol without specifying its meaning.

### C03 — Keep the identities of the corpus and remove the probe from the final analysis

Keep the three files, the UD commit, the hashes, the 18 prefixes, the 17 documents of the census and the eleven primary documents in seven blocks. Keep in the registry the original regimes `HEX`, `PROSE_CLASS`, `PROSE_POST`, `OTHER_VERSE`; `PROSE_ALL` is a report grouping of the two proses.

The six tragedies become **documents in the census without final scoring**: no training, no probe evaluation, no tragic figure and no conclusion of specificity with respect to tragedy. Keep the history of the proofs already run, without renaming it final result.

To avoid a further analytical variation, keep the alphabetic inventory defined over the whole census of 17 documents. It must be written explicitly: the six non-evaluated documents contribute only to the inventory of the types. After the merging **9 C0 types and 10 OTH types exclusive to those documents** remain, against 10 and 12 before; in UPOS none. The design remains closed and transductive. **Do not at the same time reduce the support to the primary documents alone:** it would give other alphabets, 91/95/11.

### C04 — Merge PART and ADV globally

Apply to all representations the map `PART → ADV_PART` and `ADV → ADV_PART`, after the check of the source tags and without conditioning it on lemma, work or group. `ADV_PART` is a project category, not a new UD tag. Keep the original UPOS in the census.

| Variant | Before | After | Tokens/targets |
|---|---:|---:|---|
| `ud23`, C0 | 106 | **100** | Unchanged |
| `ud23_oth` | 112 | **105** | Unchanged with respect to the earlier `oth` |
| `upos_only` | 12 | **11** | Same mask as C0 |

The direct count confirms 9,884 PART in the Homeric block and 1,386 in the Hesiodic one. For γάρ: 526 PART/13 ADV in the Homeric block, 54/0 in the Hesiodic one, and only ADV in the five prose blocks. **The Hymn to Demeter has zero PART and contains all 13 ADV γάρ of the Homeric block:** the association is not perfect at document level. The finding concerns the available annotation, not a demonstration that every single analysis is wrong. The AGDT documentation of the pinned commit acknowledges the problem of the adverb/particle distinction. [AGDT, annotation note](https://github.com/PerseusDL/treebank_data/blob/bf4334f0af5e13d16b04c1cccd6237e683ac6f5f/v2.1/Greek/README.MD#L67)

The merging reduces a distinction applied discontinuously. It does not make CCONJ, DEPREL or all particles uniform: δέ and τε remain examples of residual heterogeneity. Do not correct the tokens with lemma-based heuristics and do not start a manual re-annotation. Keep the comparability limit in the report also after the merging.

### C05 — Really propagate the new alphabet

Regenerate lexicographic lists, IDs, hashes, configuration and test expectations. The historical names `ud23`, `ud23_oth`, `upos_only` can remain, but the version of the representation must indicate the merging: the same variant name does not mean the same bytes nor the same model.

With a=0.5 per symbol the Dirichlet masses become **50, 52.5 and 5.5**, respectively; in `a_total1` C0 uses **a=1/100**, not 1/106. The R1 smoothing must also use the new m. Do not reuse the old models or their scores. The source ledgers can remain the same when masks and permutations coincide; they must be revalidated against the new coordinates and the new contract.

This choice modifies the task and the total prior: do not present any difference from the pilot as a pure measure of the PART/ADV effect. Do not add a final cell with the earlier alphabet: keep its results as historical development.

### C06 — Make the annotation and retention audit informative

Report per document and block: source UPOS/DEPREL counts, tokens removed with cause, raw→encoded retention, eligible/encoded, sentences without targets and encoded lengths. Make checks A and B visible in the primary blocks too, not only in the tragedy.

Verified corrections:

- The corpus contains **27 base DEPREL and 28 labels counting `nsubj:outer`**, not 29+1 as A writes.
- `PROPN` and `SYM` have zero occurrences; sentences empty after encoding are zero too. Keep the handling of the edge cases in the tests; do not describe the PROPN mapping as a transformation that actually happened.
- `discourse` appears on 374 tokens, all `INTJ`: it is already excluded by the UPOS mask. `oth` does not recover these tokens. The problem of the removed relations must not be described as if `oth` kept everything C0 discards.
- The removed `vocative` with admitted UPOS are 459 in the Homeric block and 26 in the Hesiodic one: about **0.560% and 0.242% of the respective raw tokens**. Report the actual values, without defining them a priori as the relations «most characteristic» of poetry.

The conventional thresholds >2% and retention <70% can remain simple flags. They do not constitute a certificate of annotation homogeneity. Hashes and expected counts, on the other hand, are identity checks that must fail on discrepancies.

### C07 — Keep training by block and describe its exposure exactly

Keep q=8,884 for each of the six contributors, 53,304 tokens in total; `q_half` uses 4,442 and 26,652. No held-out block, or document of it, enters the training.

| Test | HEX in training | Prose in training | Test group in training |
|---|---:|---:|---:|
| HEX | 1/6 | 5/6 | 1/6 |
| Prose | 2/6 | 4/6 | 4/6 |

Insert this table in the method and next to the contrast, without asserting a necessary direction of the deviation. No `balanced` cell, no additional common model, no per-regime fit.

Plutarch contributes all its 8,884 tokens in C0 when it is not held out: the original training multiset and its counts are fixed, but the ledger can have a different order and the **shuffling continues to vary**. Correct A's too general formula about the contribution «deterministic over all seeds».

### C08 — Keep the sampling, without reopening the fragments

Keep the permutation of the sentences, the exact budget and at most one fragment per contributing block. A fragment is an autonomous stream: it does not inherit the history of the excluded portion. Keep coordinates, reason for the cut, subseed and the metrics already required by P §5.2.

The numerical cells and UPOS reuse the C0 ledger; `q_half` shares the order of the sentences but does not promise token nesting; `oth` can stop elsewhere. Do not add a new whole-sentence comparison: the earlier ablation remains a local development proof, not a general guarantee.

### C09 — Fix the target population and leave the bands secondary

Keep `available_past ≥ 4` within the encoded sentence. In C0 **53,009/80,370 = 65.96%** of the retained HEX tokens and **56,099/73,930 = 75.88%** of the prose ones are evaluated. Write that the result concerns internal positions and weighs long sentences more.

The bands remain **4–7** and **≥8**, with counts and all the components of Q, for every cell and arm. Do not create co-primaries, length matching or new standardizations. In D12 the band ≥8 does not mean availability of all twelve predecessors. A's recomputation on the band ≥8 shows a persistence of D_G in the pilot; it does not eliminate all the effects of segmentation.

### C10 — Keep Q and restrict its interpretation

\[
Q=(CE_0^O-CE_{CTW}^O)-(CE_0^R-CE_{CTW}^R).
\]

Keep the shuffling of training **and** test within each sentence/fragment, a new fit of the shuffled arm and pairing by slot. Permute the whole composite symbol; not UPOS and DEPREL separately. The provenance of the moved token is different from the coordinate of the evaluated slot.

The training roots of the two arms have the same counts. The CE0 on the eligible test can differ because the shuffle moves symbols across the boundary of the first four slots. The counterexample of the package gives Q≈0.71346 and shortcut≈−0.66505.

One shuffle per seed remains sufficient for the chosen perimeter: 20 C0, 10 per sensitivity. Do not repeat until obtaining a change or a welcome sign. Do not set `G_R=0` as an acceptance test. Positive Q describes the relative advantage with respect to that transformation; it does not by itself identify syntax, metre or a linguistic order purged of the annotation conventions.

### C11 — Reduce and freeze the six cells

| Cell | m | D | a per symbol | rho | q per contributor | Seeds | O+R models |
|---|---:|---:|---:|---:|---:|---:|---:|
| C0 | 100 | 8 | 0.5 | 0.5 | 8,884 | 20 | 280 |
| a_total1 | 100 | 8 | 0.01 | 0.5 | 8,884 | 10 | 140 |
| q_half | 100 | 8 | 0.5 | 0.5 | 4,442 | 10 | 140 |
| D12 | 100 | 12 | 0.5 | 0.5 | 8,884 | 10 | 140 |
| oth | 105 | 8 | 0.5 | 0.5 | 8,884 | 10 | 140 |
| upos | 11 | 8 | 0.5 | 0.5 | 8,884 | 10 | 140 |
| **Total** | | | | | | | **980** |

Keep master seed 20260706, C0 indices 0–19, sensitivities 0–9 and the SHA-256/PCG64 convention `hexis-v3-rng-1`. Pair the sensitivities with the **first ten** C0 seeds, not with the twenty-seed C0 mean.

The renunciations must be made explicit: eliminating `rho09`, the sensitivity to the stop/split prior is no longer evaluated; `a_total1` concerns another prior. Eliminating `bound`, the dependence on boundaries is no longer evaluated. D12 remains a one-sided check on the increase of depth, not a complete exploration of D.

Do not choose the cuts because they produce similar results in the pilot. Accessory questions are cut and the four essential causes of dependence of the score are kept: local regularization, budget, admitted depth and representation.

### C12 — Keep R1 without new families of JSD

For each of the three updated representations, keep complete original counts of the seven blocks, unsmoothed frequencies, distributions with pseudocount 0.5, 21 pairs, 7×7 matrix, centroids with uniform weight across blocks and the contributions of the symbols. JSD in bits, zero diagonal, symmetry, range [0,1] and correct handling of `0 log 0`.

Do not automatically change the weights of R1 because Q also has a per-target summary: R1 describes all retained tokens, Q an eligible population. The difference is declared, not inconsistent. Do not add JSD of the targets only, JSD of the probes, new centroids, tests or clustering. R1 neither corrects nor validates Q. [P §8.3; Lin, 1991](https://www.cise.ufl.edu/~anand/sp06/jensen-shannon.pdf)

## 5. CTW, diagnostics and precision: what to keep and correct

### C13 — Keep the mathematical contract, replacing the old selector

Bring the CTW to non-binary outcomes: Dirichlet evidence, stop/split mixture, leaves forced at D, terminal BOS only in the contexts, empty subtrees with unit evidence and uniform prediction. Keep the exact partition of the counts and the frozen prediction during the whole evaluation.

Do not import the prototype as a production dependency and do not import `candidates/`. The reference and the independent fixtures serve to verify the port. Remove from the active path `monotone-stop`, `argmax`, `k_min`, `gamma`, the selected depth and the additional penalty. The CTW/BCT foundation does not impose a return to inference between regimes. [Kontoyiannis et al., 2022](https://academic.oup.com/jrsssb/article/84/4/1287/7073257)

With `bound` removed, **SEP is not required in the new scientific API**. Keep BOS and reset; the SEP support of the reference remains in the history of the checks. Do not keep a hidden link flag nor the old `#` as a predicted outcome.

### C14 — Correct the semantics of depth

`L_resolved` describes the length of the observed contexts to which the mixture assigns mass, conditional on the observed mass. A node with a single observation is nonetheless observed. The quantity does not measure precision, reliability, grammatical depth or the maximum limit of recoverable memory.

Moreover the masses λ along the path are **mixture weights**, not the share attributable to each context of the probability of the symbol actually seen. The latter would also depend on `p_s(x)`. Do not add a new responsibility diagnostic: correct the language.

Keep histograms of the supports and of the masses, `unseen_mass`, the number of root symbols not observed in training and the corresponding shares on the test. Define the aggregation of the diagnostics: mean of the per-position values with an explicit number of valid values; do not confuse it with the ratio between summed masses. `resolved_mean=null` must have reason `no_resolved_mass`; empty bands must have null scores with a reason and a zero count.

### C15 — Avoid wrong conclusions from numerical zeros

In the **non-forced nodes**, with finite evidences and an interior prior in (0,1), both components of the mixture are positive in exact arithmetic. The stored weight 1.0 can be a numerical saturation sustained by very strong evidence; it does not turn the CTW into a discrete selector. In the leaves forced at D or below BOS, on the other hand, the stopping weight 1 is mathematically prescribed.

A calls ~37 nats an underflow threshold of `log1p(exp(x))`: this is wrong. `log1p(exp(-37))` remains about 8.53×10⁻¹⁷; the underflow of the float64 exponential happens towards −745/−746. Around **37 nats of difference between log-components**, instead, the small component added to 1 can be lost; subtracting large log-evidences introduces further losses of precision.

Use stable operations on the logs and explicit checks, as P requires. Derive **both** posterior weights from the difference between the two log-contributions, avoiding obtaining the small weight only as `1-stop`; do not rely on an indiscriminate `min(1, ...)`. Keep `root_stop` and, to interpret its saturation, the difference between the stop and split log-contributions at the root. Specify its sign and its unit in nats; the losses remain in bits.

Do not build the extreme prior of the literature as `1-2**(-(m-1))` in float. The case must remain a numerical test, even if it is not a final cell. No test must impose that the shuffle collapses or that a larger D gives the same result.

### C16 — Keep the synthetics without turning them into a threshold for Greek

Keep the 25 small cases with fixed generators and seeds: uniform with four symbols, cycle, Markov 1, lag-2 dependency, variable memory. Keep the thresholds 0.02 for uniform/cycle and 0.03 for the other prescribed comparisons. The gate must fail on a violation: a JSON field `analytic_pass=false` with a successful exit is not enough.

Keep the historical m=106 stress as a verifiable reference and declare it a **historical stress**, not a new C0 alphabet. Also cover the actual m 100/105/11 in the parametrized checks of normalization, input and support; do not invent a further calibration campaign or new empirical thresholds.

The deficit of the lag-2 stress at 106 symbols shows that representing a dependency is not enough to learn it in the sample. The detectability values built by A on a specific source do not become constants of Greek. The ratio 106/5 with respect to Galves's alphabet is about 21.2, not literally a hundred: describe the difference in size without the expression «two orders of magnitude».

### C17 — Do not turn the reuse of counts into a reduction of models

Varying a or rho can reuse the counts, but requires new evidences, new weights and a new evaluation. A model of lower depth can derive from the D12 counts **only** by imposing the correct leaves and recomputing evidences and weights. Cutting the prediction path while keeping the D12 weights is not equivalent.

This is an optional implementation optimization, to be used only if simple and verified; it is not part of the necessary economies. The campaign always has **980 model identities**, even when part of the counts is reused. Avoid a general cache system or an additional abstraction layer only to save already short fits.

### C18 — Treat the instability of Diodorus proportionately

The historical drop of about 0.048 bits under `bound` or the extreme prior is real; by itself it demonstrates neither a bug nor the activation of a single «switch». A continuous mixture can be very sensitive to small variations of the evidence.

Keep the observation in the account of the pilots. The final pipeline must show Diodorus like every other block in the remaining cells and provide the common diagnostics. Do not make closure conditional on a philological search or on a lexicon of nodes «responsible» for retired configurations. If the identity or numerical checks fail, correct the bug; a finite and consistent variation of the scores is not in itself a technical failure.

## 6. Epistemic status, interpretations and bibliography

### C19 — Make the account of the development precise

In the new specification, in the proposal and in the final report distinguish:

1. Original C0 pilots and sensitivities, with the old alphabet and seed convention.
2. Shuffled controls actually available, with the seeds and cells covered.
3. Subsequent proofs of the contract and environment repetitions.
4. New campaign with the merged representation and the integrated contract.

Do not describe the new protocol as a preregistration preceding any observation. Do not call the final fits a mere identical replication if the alphabet changes. Do not change the analytical rule or the number of seeds to keep the historical separation.

The attachment on the earlier authorizations is a session account, not an independent verification of the original consent. In the migration report its source and degree of verifiability; do not invent times and do not declare a retroactive passing of G2. The present audit adds no authorization for new real fits.

### C20 — Complete the rules of the conclusions

Keep negative or unstable results as legitimate outcomes. Add explicitly:

- Technically successful annotation merging ≠ demonstrated linguistic homogeneity.
- C0 and UPOS with similar contrasts: **concordance of the summary in two representations**, not proof that DEPREL does not contribute.
- Different profiles or signs between weightings: dependence on the distribution of the targets, not choice of the «right» weight.
- G_R numerically null: observed behaviour of the predictor under that control, not a theorem on order.
- D8/D12 similar: absence of improvement in the evaluated configurations, not absence of dependencies beyond eight symbols.
- Absence of the probes: no final conclusion on specificity with respect to other metres.

Do not add G/CE0, `deprel_only`, permutation ranks or new reaggregations to attempt an attribution that the design does not support.

### C21 — Correct and shorten the active bibliographic registry

Use a few directly relevant sources, keeping the history of the registry. Corrections to apply:

- **Kontoyiannis et al.**: published citation in *JRSS B* **84(4), 2022, 1287–1323**, DOI **10.1111/rssb.12511**. The preprint is a primary source too; the problem was bibliographic incompleteness, not the use of a secondary source. [Publisher](https://academic.oup.com/jrsssb/article/84/4/1287/7073257)
- **Gianitsos et al.**: *Proceedings of the 3rd Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature*, **52–60**, 2019; DOI **10.18653/v1/W19-2507**. [ACL](https://aclanthology.org/W19-2507/)
- **Gorman and Gorman**: the pages **500–510** are confirmed directly by the authors' deposit; they no longer remain an open question. [Deposit](https://digitalcommons.unl.edu/historyfacpub/208/)
- **Herrera et al.**: the v1 PDF cited by the plan has four authors; the updated v2 version adds **Caio Corro**. It is not correct to accuse the plan of having omitted an author of v1. For the new text use the current version, after recording its version change, or keep an explicit link to the v1 examined. Target recommendation: cite **Herrera, Silai, Corro, Guillaume, Kahane**, QUASY 2025, **26–38**, linking v2. [v1](https://aclanthology.org/2025.quasy-1.5v1.pdf), [v2](https://aclanthology.org/2025.quasy-1.5v2.pdf)
- The bibliographic information of **Galves**, **Schürmann–Grassberger**, **Lin** and **de Marneffe et al.** turns out consistent with the primary sources consulted. [Galves](https://arxiv.org/abs/0902.3619), [Schürmann–Grassberger](https://arxiv.org/abs/cond-mat/0203436), [de Marneffe](https://aclanthology.org/2021.cl-2.11/)

Record in the new version the sources of the CTW and of Greek stylometry introduced by the plan but not yet aligned with the old registry. Eliminate citation obligations tied to Latin results, transfer or retired estimators when they no longer serve a function in the text. Do not attribute to a precedent either the HEXIS BOS contract or a certification of the quality of the corpus.

## 7. Output reduction, governance and implementation

### C22 — Reduce persistence, keeping what allows checking Q

**C0:** keep all 2,182,160 paired rows per slot, with the four float64 losses, coordinates, original and shuffled symbol, provenance of the shuffle and the per-position diagnostics already defined. Do not omit the shuffled losses assuming that they coincide with the root.

**Sensitivities:** keep one aggregate per document/seed/cell/history band, with n and **four sums of the losses**; also keep sufficient summaries of the planned diagnostics, not only rounded CE. In particular, for each arm: **sum of the valid `resolved_mean` and their count**, null counts, sums of the masses by length, sum of the unobserved mass, supports of the model, counts of targets unseen at the root and diagnostics of the shuffle. Keep the ledgers and the information needed to regenerate the scores.

The block and group aggregations are reconstructed from sums and denominators. Mean, SD, minimum and maximum over seeds are computed after the per-seed aggregations. Do not take unweighted means of means within the block.

**Explicit epistemic cost:** for the sensitivities not kept per position, a later check of a single loss requires regeneration from the ledger. Do not promise that every vector can be reconstructed from the sums alone. The hashes attest the identity of the bytes, not the correctness of the computation; independent fixtures and a deterministic regeneration of predetermined cases are also needed.

The check of equality of the slots between arms remains mandatory **before aggregation**, even when the vectors are then discarded. The histograms needed for a figure cannot be reconstructed from the four sums alone: they must be collected during the evaluation.

### C23 — Simplify the commands and the tables

Use a single parametrized executor for C0 and for the five sensitivities. `run_sensitivity` does not need a distinct orchestration: it can be retired from the target path, leaving the selection of the cells to the contract or to a verified argument. Do not introduce a new workflow framework.

Keep the responsibilities: audit/encoding, validation, descriptive execution and report. The document and block tables are the verifiable inputs; contrasts, summaries and figures are derived from the same report. Avoid multiple implementations of the same aggregation.

Keep **five figures** of the plan, updated: corpus/annotation; G/Q profiles with document detail; sensitivities and two weightings; R1; supports and masses of the model. Eliminate the tragic figure. The history bands enter the existing tables and panels, without creating a new graphical apparatus.

### C24 — Keep the verification chain, remove the separate certificates

Keep `design_lock.json` as the deposited reference, one manifest per run and a report validator. The phases V0–V5 can remain as an ordered checklist, but they do not require autonomous certification files, signatures or a general system of attestations.

The manifest contains: hashes of contract/data/registry/alphabets/code/lock, RNG version, identities of the executions, exact list of the artifacts with hash/size/schemas/cardinality and results of the checks with reference to the verified context. Keep the deterministic identity `run_id` computed from the canonical contract; timestamps, machine and local paths remain external metadata, without entering the run_id or the seeds. A handwritten `PASS` status does not replace verification evidence.

`run_report` continues to reject incomplete final results: comparison by **equality of the key sets**, detection of duplicates, verification of bytes, denominators and reconstruction of the sums. The individual outputs remain available to diagnose the errors. No nested certificates are needed to obtain these properties.

### C25 — Recompute all the operational numbers and the completeness checks

| Quantity | New value |
|---|---:|
| Cells | 6 |
| Fold/seed/cell pairs | 490 |
| Model identities, two arms | **980** |
| C0 pairs | 140 |
| Sensitivity pairs | 350 |
| Document/seed/cell/arm rows, before the bands | 1,540 |
| Technical trial with one seed per cell, two arms | **84 models**, 42 pairs |
| Probe evaluations | **0** |
| Paired rows if all six cells were persisted | 7,643,640 |
| Paired rows actually required, C0 only | **2,182,160** |
| R1 | 3 representations × 21 pairs, plus centroids/contributions |

Do not use 980 or 84 as the only check: generate the expected keys from contract, folds, arms and seeds. The 84 technical models can contribute to the 980 only if produced with identical code, contract and definitive schema. No sum of outputs of different versions.

Update schema and content of all attachments dependent on these numbers; remove probes and SEP from the expectations. The estimate of 921 MiB of the plan is arithmetically correct for the old schema, but it is no longer the new requirement. The numerical body of the C0 rows alone, still assuming 76 bytes/row, is about 158.2 MiB before overhead: it is not a benchmark nor a RAM requirement. Measure time, memory and space in the integrated trial; do not invent a new estimate of days more precise than the available data.

### C26 — Keep safe writes, resumption and provenance of the code

Write temporarily, verify and rename atomically; no silent overwrites. Reuse a partition only if identity, hash and cardinality coincide. No automatic exclusion of problematic blocks or seeds.

A commit does not identify any uncommitted modifications or untracked files imported during the run. For the final campaign require a clean tracked code state and no scientific producer depending on untracked files, or explicitly record an identity of the sources that includes them. For this project the first route is the simpler. Unrelated local scripts and ignored data must not be deleted to obtain this requirement.

### C27 — Migrate the code on the basis of what really exists

The plan underestimates some already working parts and suggests too direct a reuse of others. Target map:

| Path | Necessary action |
|---|---|
| `src/hexis/conllu_reader.py` | Reuse valid parsing and checks; complete the identity/order/coordinates required by the new registry |
| `src/hexis/registry.py` | Apply the verified registry, parts, roles and seven blocks; keep original regime and report group separate |
| `src/hexis/alphabet.py` | Add the merging; errors on unknown tags; frozen lexicographic inventory; verifiable document retention |
| `src/hexis/sequences.py` | Replace the old concatenation semantics and predicted `#` with sentence/fragment streams, reset and coordinates; no active SEP |
| `src/hexis/config.py` | Keep safe YAML and duplicate rejection; replace the methodological schema and complete types/ranges/finite values |
| `src/hexis/model/context_tree.py` | Implement the canonical CTW in place of the stub; frozen API and controlled numerics |
| `src/hexis/model/diagnostics.py` | Implement masses/supports and null values with reasons; retire the selected depth |
| `src/hexis/protocols/sampling.py` | Implement sampling and RNG from the contract, ledger reuse, fragments and shuffle |
| `src/hexis/protocols/scores.py` | Implement losses, pairing, sums and Q; core independent of the groups |
| `src/hexis/manifest.py` | Reuse valid identity and provenance; add the required atomicity/resumption/completeness |
| `src/hexis/pipeline/run_audit.py` | Keep the already verified defences; separate the identity of the data from the old methodological gates |
| `run_encode.py`, `run_tree_validation.py` | Complete stages advertised only when operational |
| New `run_descriptive.py`, `run_report.py` | One executor of the six cells and a single report, without a partial final contrast |
| `run_confirmatory.py`, `run_null_calibration.py`, `run_reference.py`, `run_latin.py` | Retire entry points and active obligations; no hidden call |
| `run_sensitivity.py` | Retire the entry point from the documented target; the six cells use the same executor |
| `model/lexicon.py`, `blocks.py` | Retire lexicon and chunks from the scientific path; do not confuse chunks with dependency blocks |
| `stats/permutation.py`, `bootstrap.py`, `holm.py` | Keep utilities and valid tests as historical code, without import in the descriptive pipeline |
| `viz/plots.py` | Only five figures derived from the verified tables |
| `tests/`, `conftest.py`, pytest configuration | Realign inventory and checks with the new contracts; forbid skips in the active acceptance checks. No tracked CI workflow exists: do not invent CI attestations nor make adding one mandatory |
| `pyproject.toml`, `uv.lock` | Update description and necessary metadata; keep the stack without new libraries or unmotivated downgrades |
| `.gitignore`, `LICENSE` and licence indications | Keep large working outputs out of Git; distinguish code, documents, source data and artifacts intended for publication |
| `scripts/reacquire_raw_data.sh` | Preserve the local original; verify and correct any target version before advertising it |

Three concrete clarifications:

1. `config.py` does **not** only check presence: it already rejects unknown/missing keys and some G1 structures. Adequate validations of the future parameters are missing; examples currently accepted include methodological values outside the contract and NaN. Reuse the working checks, do not rewrite everything.
2. The old `observed_alphabet` sorts by frequency; the new plan requires lexicographic order. The old behaviour of `map_token` discards an unknown UPOS, while the new contract must report it as an error.
3. The statistical utilities are implemented; many scientific modules are instead stubs. The 327 passed tests do not attest the new CTW. Retiring a command does not mean leaving it in the documentation with `NotImplementedError`.

The current acquisition script exists and is readable, but it is not tracked. It reads provenance from `data/raw/PROVENANCE.md`, acquires Greek and Latin and checks the files present without comparing them with the set of the three expected. It has a `SKIP` branch for the missing hash, but `set -euo pipefail` can stop it earlier: it is not an explicit and verified handling of the errors. A reproduction in a clean checkout must have the provenance **tracked outside raw**, acquire only the required Greek and verify exactly the three expected names. It must fail on an expected file missing, an extra file, a missing expected hash or an ambiguous record. Do not run the script today to fill these gaps: the data present are already verified.

The documentation must distinguish the data kept locally from the artifacts actually distributed. Do not automatically assign the licence of the code to the per-position symbols and coordinates. External publication remains a later phase, with provenance and conditions of the materials declared; this report does not redistribute the raw files nor decide the legal qualification of the derived data.

### C28 — Bring the tests before the new implementations

Keep the relevant properties, replacing the old methodological obligations with an explicit motivation. Minimum necessary:

- Hashes, identities and counts of the corpus; merging, m100/105/11, masks and coordinates.
- Strict types: no bools as integers, silently converted floats, NaN/Inf, symbols outside the alphabet, duplicates or unknown keys.
- Exact samples, no held-out contamination, fragments, seeds, ledger reuse and invariance to the order of records/labels.
- Independent enumeration of small trees, partition with BOS, normalization, empty training, D=0, prequential identity and absence of test updates.
- Synthetics at the actual thresholds, extreme priors, rare support; no requirement of a good result on Greek.
- Shuffle and four-term Q, alignment of the slots and reconstruction from sums in the two weightings.
- Empty/null bands, masses and supports, JSD and contributions.
- Rejection of an incomplete or corrupted campaign, duplicate/additional keys, resumption and interrupted writing.
- Complete C0 reconstruction from the vectors; for the sensitivities, verification of the aggregates and regeneration of predetermined pairs, without claiming information not persisted.

Do not turn T24 on the probes into a skipped test: replace it with the check that those documents are neither trained nor evaluated and have only the census/inventory role. Update T25/T30 to 980, T04 to the new alphabets and all references to certificates/SEP. Do not weaken generic checks still valid to obtain a green suite.

### C29 — Realign the normative documentation in a single act

Deposit a decision in the namespace **V3-001** that explicitly replaces v2.1 for the new executions and adopts this revision of plan 3.0.1. Give the new contract a different version; recommendation: **3.1**, because representation, main result and outputs change, not only typos.

Update together:

- `docs/01_MASTER_SPEC.md`, `docs/02_DECISION_LOG.md`, `docs/03_ROADMAP_OPERATIVA_IT.md` and the bibliographic registry;
- `docs/00_LEGGIMI_INDICE.md`, `docs/HANDOFF.md` and `docs/04_AI_HANDOFF_PROMPT.md`;
- `AGENTS.md`, `CLAUDE.md`, `README.md`, configuration, registry, package metadata and test inventory;
- structured contract, corpus expectations, alphabets, design lock and report contracts present in the attachments.

Keep D01–D54, the proposed D55 and the G1 technical ratifications as history with a clear status. No retired clause must remain implicitly binding: confirmatory P1/P2, Latin, O7, permutation thresholds, 13 cells, sign-stability obligations and old gates must be declared **not applicable to the new version**, not «resolved» in the old project.

Expressly preserve immutability of the raw files, provenance, label-free core, quarantine of the candidates, real tests and the prohibition of silent overwriting. The two reviews remain historical critical documents; they do not become normative sources competing with the consolidated specification.

### C30 — Separate the closure of the design from the certification of the results

**Before the new proposal and the substantial alignment of the README:** adopt all decisions C01–C30 into the target contract, with matrix, numbers, outputs and roles without residual alternatives. A methodological proposal can be drafted before running the campaign; it must say that the implementation is in progress.

**Before declaring the pipeline available:** apply C22–C28 and pass the corresponding checks. The README must advertise only the commands really implemented; status and limits remain visible.

**Before the definitive scientific report:** complete 980 model identities and the three R1, verify artifacts and aggregations, run the prescribed resumption/reproduction and produce the five figures. Completion does not depend on the sign, the separation of the groups or the confirmation of the pilot.

Do not create a circular dependency by asking for a «final» README before the code and then using that README to certify the code. The normative realignment precedes the implementation; the operational attestation follows the checks.

## 8. Complete pass over the plan: sections to change

| Section of P | Update required |
|---|---|
| Heading and status | New version; consolidated proposal applied only after an act; no future result attested |
| §1 | Within-sentence question, main profiles, limit to the linguistic reading |
| §2 | Pilot D_G distinct from D_Q; coverage of the arms; old alphabet identified |
| §3 | Corpus kept; tragedies census/inventory only; concrete annotation and visible weights |
| §4 | ADV_PART, m100/105/11, new hashes, errors on unknowns, corrected audit of the exclusions |
| §5 | Sampling kept; different training per fold; Plutarch clarification; no balanced |
| §6 | CTW kept; new parameters for m; stable numerical weights; BOS and reset |
| §7 | Elimination of bound/SEP; shuffle kept; no general identity Q=G |
| §8 | Main profiles, two subordinate weightings; R1 kept; elimination of probe scoring |
| §9 | Corrected diagnostic semantics, null values with reasons, persisted masses/supports; bands not co-primary |
| §10 | Six cells, 980 models; explicit renunciations; no universal comparison between alphabets |
| §11 | One executor; positional C0/aggregated sensitivities; five figures; restricted manifest |
| §12 | New tests for merging and roles; adaptation of T04/T24–T30; real binding thresholds |
| §13 | V3-001 and new version; selective reuse of the code; local script finally inventoried |
| §14 | Linear checklist, 84 technical models, 980 final, no separate certificates |
| §15 | Lock kept; old estimates identified as historical; new integrated benchmark |
| §16 | Rules C20; no false attribution to DEPREL/order/memory |
| §17 | Six cells, no probe, five figures, reduced persistence and proportionate verification |
| §18 | Citations completed/versioned and registry reduced to the sources used |
| §19 | Verdict on the design distinct from software gates and scientific outcomes |

## 9. What remains uncertain, without reopening the project

1. **Quantitative effect of the merging on G/Q:** not measured in this review; it requires the fits of the new campaign. It is not a choice to postpone until the results: the map is decided now because of the documented discontinuity.
2. **Complete annotation comparability:** not demonstrated and not promised. The reduction of detail mitigates a specific problem; the design keeps annotation, historical and training limits.
3. **Exact share of metrical quotations in Athenaeus:** not automatically reconstructible from the XML fields examined. Do not introduce invented counts or attributions; the work remains classified at document level.
4. **Point causes of the historical sensitivities of Diodorus:** the changes of the scores are verified, the attribution to a node is not. It does not block the reduced question.
5. **Original authorization of the earlier sessions:** distinguish the attached account from any recoverable act. Do not presume a violation and do not certify an unobserved consent.
6. **Performance of the integrated pipeline:** not measured because the pipeline is not yet implemented. The times of the prototypes are not a guarantee on the final run.

A's ad hoc synthetic calibrations, B's `bound` link percentages and the check of the guidelines in all 18 XML files were not re-run. For the latter, the two Athenaeus XML files were inspected again; the report does not promote attestations of the reviews to independent checks not performed. No final decision depends on the exactness of the `bound` percentages or on A's specific thresholds.

These points do not justify new corpora, new annotations, another model or an inference campaign. They require a correct formulation and, where relevant, the normal checks of the already planned execution.

## 10. Final verdict for the next step

**In favour of closing the design with the thirty changes above; not in favour of adopting A in full, nor of applying 3.0.1 unchanged.**

The resulting project is sufficiently defined to write a new honest and short proposal: closed corpus, merged annotation, within-sentence comparison, individual profiles, frozen CTW, paired Q, descriptive JSD, six cells and conclusion criteria independent of the result.

The still decisive point is not «finding the control that definitively separates the metre». It is **to stop promising that separation**, making instead completely verifiable the quantity that the data and the protocol allow to describe. The new proposal must take on this circumscribed promise; the repository must implement it; the final report must respect it even if the outcome differs from the pilot.

The recommended sequence is: **adoption of the consolidated contract → consistent drafting of the proposal and normative realignment → implementation and verification → definitive operational update of the README → results and report**. No further round of methodological enlargement is needed to start this sequence.
