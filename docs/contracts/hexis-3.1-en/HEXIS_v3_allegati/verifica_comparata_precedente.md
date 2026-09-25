> **Non-normative companion translation; the Italian original governs** (V3-003, B2).
> Original: `docs/contracts/hexis-3.1/HEXIS_v3_allegati/verifica_comparata_precedente.md`, SHA-256 `f31003ca50988da6a0ba61a1a43705b7810ac9089bf56e6d07828d1347c0720c`.
> Translated on 2026-09-25. Structure, tables, values and identifiers follow the original, including links; the five code blocks are reproduced unchanged, Italian labels and decimal commas included. Numbers in the prose use English notation. Any translator's note is marked *[Translator's note: …]* and changes nothing in the original.

# HEXIS — Comparative verification of the two proposals and stopping point

**Date:** 11 September 2026  
**Documents evaluated:** `piano_finale_HEXIS.md` and `piano_ultimato_HEXIS.md`  
**Repository:** `leonardotornabene/HEXIS`, branch `g1/pre-audit`  
**Verified commit:** `852644b6917790877c7b2ca5df2e76b17829d87c`  
**Status of the report:** documentary and empirical evaluation with a verified methodological impediment. It is not a ratified proposal, a new operational specification or a certification of the whole project.

*[Translator's note: `piano_finale_HEXIS.md` is the "final plan" and `piano_ultimato_HEXIS.md` the "completed plan"; the text calls them the first and the second plan.]*

## 1. Verdict reached and limit of the delivery

**`piano_ultimato_HEXIS.md` is the preferable basis for the downsizing. Neither of the two proposals is ready to be ratified in full in its current form.**

The superiority of the second plan concerns substantial choices: a descriptive status consistent with the available corpus, use of all held-out positions, renunciation of an unestablished inferential justification, better delimitation of the claims and recognition of the distance between the proposed algorithm and the bibliographic source.

There is, however, a shared problem, prior to the discussion on inference: the `monotone-stop` selection can prevent the model from using order-2 dependencies that the acceptance tests require it to recover. The problem was reproduced on synthetic data at the training size planned by the new design, and rechecked with a second independent numerical reconstruction.

**I stop before presenting a “definitive version” because the scientific constraint on the instrument remains to be clarified:** is the variable-order context tree an element that must necessarily be kept, or is it a replaceable means to obtain a reliable descriptive measure in a short time? The answer changes which solutions must be compared and validated. It is not a question of formatting, administrative ratification or choice of a name.

The recommendation is to keep the descriptive approach of the second plan and the scientifically useful requirement of recognizing the known order-2 process; to put the selector back into question or, if the objective of the work admits it, the instrument. I do not recommend turning the gate green by choosing a favourable seed or suppressing the benchmark that revealed the problem.

## 2. What was actually verified

### 2.1 Access, versions and integrity

Access to the repository through GitHub succeeded. The default branch is `master`, at `3f5a6eafac83e5c190a866c8bea1937d8284ce75`; `g1/pre-audit` is 47 commits ahead and not behind `master`. Both plans refer to `g1/pre-audit` and to the commit actually present. This is therefore the relevant baseline, not only the README of the default branch.

The work was done on a separate copy. No changes were made to the remote repository, to the versioned files of the copy or to the attachments. The concluding checks `git status --porcelain=v1`, `git diff --exit-code` and `git diff --cached --exit-code` returned a clean state. The additional verification scripts and their results are outside the copy of the repository.

Both plans were read in full. The relevant normative documents, the decisions D18/D32/D36/D39/D43/D44/D47/D49/D52/D53, the G1 registers and proposals, and the code and tests concerning reading, encoding, sequences, scoring, selection and permutations were also examined. The relevant attached scientific materials were consulted; the page of the Schürmann–Grassberger source containing the selection rule was also checked visually.

Version reference: [HEXIS commit examined](https://github.com/leonardotornabene/HEXIS/commit/852644b6917790877c7b2ca5df2e76b17829d87c).

### 2.2 Existing suite

The environment was rebuilt from `uv.lock`, without modifying the lockfile. The suite was run with the pytest cache disabled and bytecode directed outside the repository:

```text
327 passed, 17 skipped in 14.04s
```

Python used: 3.12.14. Relevant dependencies of the lock: NumPy 2.5.1, pytest 9.1.1, conllu 6.0.0, pandas 3.0.3, pyarrow 25.0.0.

This confirms the count declared by the plans, but does not certify the validity of the instrument. `ContextTree.__init__`, `fit`, `evaluate` and the other central operations still raise `NotImplementedError`. The tests of the four analytical processes are explicitly skipped as scaffolds. Sampler, application scoring, final encoding and validation of the tree are incomplete as well.

**No fit of a context model was run on the real texts.** The checks on the real data are counts and checks of the representation; the experiments on the model use only synthetic sequences. The quarantined models from `candidates/` were not imported.

Sources: [canonical instrument](https://github.com/leonardotornabene/HEXIS/blob/852644b6917790877c7b2ca5df2e76b17829d87c/src/hexis/model/context_tree.py), [analytical tests](https://github.com/leonardotornabene/HEXIS/blob/852644b6917790877c7b2ca5df2e76b17829d87c/tests/test_context_tree.py).

### 2.3 Status of the decisions

The G1 register confirms the technical ratifications 17–20 and 23–26; the scientific decisions remain open. The two attached documents are proposals. The presence of a value in their texts, or its marking as verified, does not make it a ratified choice nor an independently checked measure.

The current request authorizes the evaluation and the formulation of a new proposal; it was not treated as an authorization to apply changes to the project.

Source: [register of the G1 ratifications](https://github.com/leonardotornabene/HEXIS/blob/852644b6917790877c7b2ca5df2e76b17829d87c/docs/g1_ratification_record.md).

## 3. Corpus: independent recomputation

The three Greek files were acquired at the upstream commit `37837c7a3c592c9563f8c51cc63344b87247f8a5`. Their SHA-256 coincide exactly with those recorded by HEXIS in `data/raw/PROVENANCE.md`. The count was recomputed by reading the CoNLL-U lines and applying the mapping declared in the config, without training any model.

The results reported below are verified **conditionally on the proposed registry**: the recomputation does not replace a philological ratification of the identities, attributions or groupings.

| Proposed block | C0 tokens | Positions with at least 4 preceding symbols |
|---|---:|---:|
| HOMERIC_TRADITION | 71,088 | 46,634 |
| HESIODIC_TRADITION | 9,282 | 6,375 |
| HERODOTUS | 17,301 | 12,946 |
| THUCYDIDES | 9,346 | 7,227 |
| ATHENAEUS | 23,133 | 16,691 |
| DIODORUS | 15,266 | 12,334 |
| PLUTARCH | 8,884 | 6,901 |
| **Primary total** | **154,300** | **109,108** |

Other findings:

- 202,989 syntactic lines in the Greek corpus; 13,919 sentences.
- Alphabets observed on the 17 Greek documents: `ud23 = 106`, `ud23_oth = 112`, `upos_only = 12`.
- Tragedy: 22,275 C0 tokens and 12,769 eligible positions, in six documents.
- Minimum quota common to the three representations: `q = 8.884`.
- The Hymn to Demeter contains 1,119 eligible positions; the Iliad 45,515.
- The Iliad weighs 97.6005% of the eligible positions of the Homeric block, or 97.5228% of its tokens. They are different weights, although numerically close.

*[Translator's note: `q = 8.884` is 8,884 tokens; it is kept in code notation as in the original.]*

The correct formula is `sum(max(L-4, 0))`. The computation `token - 4*frasi` is only a lower bound. The value 6,375 of the second plan is confirmed; the first plan did not yet know this value and in some arguments treats lower bounds as if they were actual sizes.

The figure of 232,212 total lines reported by the second plan also includes Latin: it is not the number of Greek lines. In this verification the Latin corpus, destined for exclusion in both plans, was not recomputed.

Source of the hashes: [provenance of the inputs](https://github.com/leonardotornabene/HEXIS/blob/852644b6917790877c7b2ca5df2e76b17829d87c/data/raw/PROVENANCE.md).

## 4. Separate evaluation of `piano_finale_HEXIS.md`

### 4.1 Useful aspects

The plan correctly recognizes the dependence between texts of the same tradition, exposes the asymmetry of the training composition, flags the risk of artificial adjacencies in P-BOUND and declares that the central software is still to be written. The move to per-block training contributions limits the quantitative dominance of the Iliad over the pooled training.

These elements are useful, but they do not support the inferential certification that the text tends to attribute to itself.

### 4.2 Exchangeability has not been established

A permutation test can be exact under precise hypotheses on the joint distribution of the data or on the assignment of the labels. The label-blindness of the software prevents one form of circularity; it does not demonstrate those hypotheses.

The absence of probabilistic sampling, by itself, does not forbid every form of model-based inference. Here, however, no substantive stochastic model is provided that justifies the exchangeability of the seven historical blocks. The perfect alignment between the two hexameter blocks and the archaic period, the textual dependencies and the multiple confounders make a certification of exactness applied to this corpus unjustified.

It is legitimate to describe a result as exact **if** a given hypothesis holds. It is not legitimate to turn that condition into a verified property of the design. The first plan correctly alternates the conditional formula with expressions that are too strong, such as “valid by construction”.

The literature on permutation tests moreover distinguishes equality of distributions from equality of a single parameter. It offers no shortcut for seven non-exchangeable blocks. [Chung and Romano, 2013](https://arxiv.org/abs/1304.5939).

### 4.3 Equal quotas do not imply equal variances

The sentence according to which equal `q` and `m` would make the marginal variances equal “by construction” is false. The variance also depends on the distributions, the serial dependencies, the lengths of the sentences, the internal heterogeneity and the trained model.

Even in the elementary case of uniform sampling without replacement from a finite population of fixed scores, the variance of the mean depends on `S_b²(1/m - 1/N_b)`, not only on `m`. Equal `m` with different `N_b` or `S_b²` do not produce equal variance.

The deterministic invariance tests are important software checks, but they are not “stronger” than every calibration in the sense of being able to certify hypotheses on the generation of the data. They verify different properties.

### 4.4 The “formal impossibility” of Latin is refuted by the code

The plan claims that, with groups 2/7 and 36 allocations, the two-sided minimum is `2/36 = 0,0556`. For the two-sided rule actually implemented this is not true: with groups of different size, a mirror allocation with an opposite statistic is not guaranteed.

Counterexample run directly using `exact_label_permutation` of the repository:

```text
score:   [100, 99, 0, 0, 0, 0, 0, 0, 0]
etichette: 2 nel primo gruppo, 7 nel secondo
allocazioni: 36
p bilaterale: 0,027777777777777776 = 1/36
```

*[Translator's note: in the output, `etichette` means "labels", `nel primo gruppo`/`nel secondo` "in the first group"/"in the second", `allocazioni` "allocations" and `p bilaterale` "two-sided p". In the prose above, `2/36 = 0,0556` is kept in code notation as in the original: 0.0556.]*

It is a sufficient falsification of the claimed general impossibility. Rule D43 already distinguishes these cases. The exclusion of Latin can remain justified by the scarcity and inadequacy of the material with respect to the reduced study; not by this mathematical argument.

Source of the computation: [permutation.py](https://github.com/leonardotornabene/HEXIS/blob/852644b6917790877c7b2ca5df2e76b17829d87c/src/hexis/stats/permutation.py).

### 4.5 The quantitative argument on the Hymn is not a verification of the real design

The first plan presents a universal variance multiplier based on the ratio between two evaluation sizes. It does not consider the finite-population correction and also uses values that were only lower bounds.

Using the actual sizes, going from 6,375 to 1,119 positions, in the Homeric block alone of 46,634 positions, would multiply the variance component from uniform sampling of fixed scores by about 6.44. For the Hesiodic block, evaluated in full at 6,375 positions, that component instead starts from zero. There is therefore not the same multiplier for all blocks. Adding the variability of the fits makes the situation further complicated, not resolved by the ratio of sizes.

The power tables reported by the plan remain simulations conditional on a generator and parameters. They are not measures of the power of the real protocol on these texts. They were not reproduced in this verification, and I do not use them as a foundation of the verdict.

### 4.6 The relation with the composition of the training is overstated

With exact quotas, the fraction of training of one's own group is 1/6 in the HEX folds and 4/6 in the prose folds. This arithmetic result is correct. A theorem on the direction of the gain does not follow from it: the direction indicated by D44 was conditional on the relation between gain and representation of one's own regime in the training.

The first plan eliminates that condition when it speaks of a “known direction”. A differential cross-entropy with respect to the root can react to the mixture in different ways. A two-sided test, moreover, corrects neither the composition of the training nor the confounders.

### 4.7 Feasibility and judgement

With the whole-sentence sampler stopping before exceeding, the actual training is **at most** `6q`; it is not exactly 53,304 tokens in every fold. The relation with the old 40–60k window does not demonstrate statistical sufficiency: that window was a profiling hypothesis, not an empirically validated learning threshold.

**Judgement on the first plan:** it contains recoverable operational material, but it does not constitute a reliable basis to be ratified in full. Some “definitive corrections” are themselves errors. I do not recommend keeping inference as the main path while waiting for an external review to make the missing substantive hypothesis credible.

## 5. Separate evaluation of `piano_ultimato_HEXIS.md`

### 5.1 Substantial improvements

The second plan makes a scientifically defensible choice for the available material: it describes finite differences conditional on the protocol, without turning them into generalizations about the Greek hexameter.

The elimination of `m` is a concrete practical improvement: all 109,108 eligible positions of the primary set can contribute to their respective means, without a further random subsampling. The blocks can keep uniform weight in the contrast even if they contain different numbers of positions. Equality of the weights across blocks does not require equality of the number of their targets.

Also correct are: signed gain; separation between computational variability and scientific replicates; visibility of the seven scores; declaration of the alphabet built also on the tragic probe; distinction between a Rissanen-inspired model and a replica of the original algorithm; maintenance of the held-out evaluation without updates.

The rank of the 21 allocations is mathematically computable and descriptively legitimate if it remains so. It adds no replicates, causal identification or inferential validity. It is not indispensable to the scientific value of the work and must not drive its narrative.

### 5.2 The decisive defect remains in the primary selector

A more accurate name of the instrument does not modify its behaviour. The plan keeps `select: monotone` as the primary and keeps the requirement of recovering the order-2 source. The conflict demonstrated in section 7 therefore remains fully active.

The description of the project as “methodological” makes this point particularly important: an instrument can be a well-defined functional and yet not possess the capability used to justify its employment. Reproducibility is not enough to fill that gap.

### 5.3 Operational contracts to be clarified before the implementation

Besides the selector, the text keeps details with real effects:

1. **Pairing of the seeds.** The `analysis_id` contains the cell, but `q_half` must reuse the same permutation as C0. A shared sampling namespace for the paired cells must be defined, distinct from the complete identity of the run. The two current prescriptions do not determine a single implementation.
2. **Admissibility in `argmax`.** It must be clarified whether a node is admissible by its own support or only if all ancestors pass the monotone rule. In the second interpretation the defect is not resolved. The sum of the Deltas, computed on different sets of occurrences, must not be presented without proof as a direct comparison of two complete codes on the same targets.
3. **Meaning of `#`.** “Can be learned” and “is never a target” must explicitly distinguish update events during the fit from positions included in the scoring. A symbol counted as an outcome in the training and then excluded from the lexical mean produces a different model from a symbol used only as context.
4. **Source adjacency.** Adjacency of consecutive ranks after sorting does not by itself demonstrate adjacency in the complete text. P-BOUND requires a rule that does not join documented gaps of the source material. Identity of the text, order of the excerpts and continuity are distinct checks.
5. **MCSE of the contrast.** It must be computed on the per-seed contrasts, `D_s`, preserving the dependencies among the seven scores, if an MCSE of `D_BB` is wanted. Combining the errors of the single blocks as if they were independent is not enough. The description of the computational precision must remain separate from population intervals.
6. **10-seed sensitivities against the 20-seed primary.** The paired difference on the same first 10 seeds must also be made visible. Otherwise a sign change can incorporate sampling differences and not only the modified parameter.
7. **Unseen rates and schemas.** Numerators, denominators and masks of these diagnostics must be fixed. The complete coordinate of the result must always reconstruct the document too, not only the sentence/token pair.
8. **Relevant profiling.** The cost must also be measured with an alphabet and a sparsity compatible with 106 symbols and sentences, not deduced from binary processes alone. The number of fits is not an estimate of the duration of the development or of the complete reproduction.

These are clarifications resolvable in the next specification. They do not authorize declaring the current text already free of open implementation decisions.

### 5.4 Exact quota and final segments

The exact quota of the second plan makes the lexical contributions of the blocks exact. The final segment introduces an artificial, declared reset. This is a methodological compromise to be defined and quantified; it does not automatically make the protocol invalid, as the criticism of the first plan might suggest.

Neither keeping the segments nor stopping with undershoot solves the problem of the selector. The review must not concentrate on these details while leaving the main impediment intact.

### 5.5 Judgement

**Judgement on the second plan:** better working basis, consistent in its general epistemic approach, with the main counts confirmed. Not ratifiable in full while the model/benchmark conflict remains unresolved and the contracts indicated above are not made univocal.

## 6. Direct comparison

| Criterion | Final plan | Completed plan | Evaluation |
|---|---|---|---|
| Status of the conclusions | Conditional test with unestablished exchangeability | Finite description of the corpus | The second preferable |
| Use of the held-out targets | Subsample of the minimum common size | All eligible targets | The second preferable |
| Choice of the blocks | Justifications also tied to an unmeasured power | Declared prudential groupings | The second preferable; philological check remains |
| Two-sided Latin minimum | Wrong `2/36` argument | Latin inference eliminated | The second avoids the false foundation |
| Quantification of the model | Tends to claim an ability to read memory | Limits the interpretations and the reference to Rissanen | The second preferable |
| Recognition of the order-2 process | Required, but can be blocked by monotone | Same conflict | Decisive shared defect |
| P-BOUND and reproducibility | Some details correct, others incomplete | More developed contracts, still ambiguous in specific points | Advantage of the second, without final certification |
| Readiness for full ratification | No | No | Neither is ready yet |

The comparison does not require a compromise between the two proposals. The descriptive direction of the second plan is preferable; there is no need to reintroduce the inferential chapter of the first to balance the judgement.

## 7. Decisive experiment: order-2 dependency

### 7.1 Why this is the relevant benchmark

Both plans inherit from the Master Spec the process

```text
X_t = X_(t-2) XOR Z_t, con Z_t ~ Bernoulli(0.1)
```

with stationary initialization. Knowing the immediately preceding symbol does not reduce the uncertainty; knowing the one at distance 2 does. The relevant conditional entropy is `H_b(0.1) ≈ 0,4690` bits/symbol, while an order-0 or order-1 predictor remains around 1 bit.

*[Translator's note: in the code block, `con` means "with"; `H_b(0.1) ≈ 0,4690` is kept as in the original: 0.4690.]*

The benchmark verifies a substantial property: reaching a useful dependency beyond a non-informative intermediate level. Its failure does not concern the confounders of the Greek corpus, the size of the groups or statistical inference.

### 7.2 Protocol of the check

An autonomous and minimal reproduction of the normative pseudocode was built:

- eager growth of the contexts up to depth 8;
- add-beta with beta 0.5;
- pre-update counts and probabilities;
- `L_self` and `L_parent` on the predicted occurrences;
- thresholds `k_min = 2`, `gamma = 0`;
- literal monotone selection;
- frozen evaluation on an independent sequence;
- 100,000 evaluation symbols, with 99,996 targets after the restriction `past >= 4`.

The reading at fixed depth 2 is only a diagnostic check demonstrating the presence of recoverable information in the same tree. It was not promoted to an instrument of the project.

### 7.3 Reproducible results

| Training | Training seed | Monotone CE | CE at depth 2 | Share of targets resolved at the root by monotone |
|---:|---:|---:|---:|---:|
| 53,304 | 0 | 0.737041 | 0.468445 | 50.505% |
| 53,304 | 1 | **1.000353** | **0.467852** | **100%** |
| 53,304 | 2 | 0.467730 | 0.467730 | 0% |
| 53,304 | 3 | 0.470830 | 0.470830 | 0% |
| 53,304 | 4 | 0.734940 | 0.468218 | 50.438% |
| 200,000 | 0 | **1.000042** | **0.468436** | **100%** |

These numbers do not say that monotone fails in every realization. They show that recovery can depend on accidental fluctuations at the intermediate level. They also show a case in which increasing the training to 200,000 symbols does not solve the problem.

Simple checks in the same apparatus: i.i.d. with four symbols, held-out CE 2.000001; ABC cycle, CE 0.000081; order-1 Markov, CE 0.720464 against reference 0.721928. These are checks of the autonomous reproduction, not the execution of the canonical G3 tests still incomplete.

### 7.4 Mechanism of the failure

In the case `N = 53.304`, seed 1:

```text
Delta al contesto di profondità 1, simbolo 0: -4,435064 bit
Delta al contesto di profondità 1, simbolo 1: -0,311236 bit

Delta ai quattro contesti di profondità 2:
  6.322,783235; 7.554,256417; 6.976,058466; 7.289,262934 bit
```

*[Translator's note: in the code block, «Delta al contesto di profondità 1, simbolo 0» means "Delta at the context of depth 1, symbol 0" and «Delta ai quattro contesti di profondità 2» "Delta at the four contexts of depth 2"; the values keep the original Italian notation (thousands point, decimal comma). `N = 53.304` is 53,304.]*

The nodes at depth 2 gain thousands of bits over the parent. The rule, however, forbids reaching them because the two nodes of depth 1 do not pass the threshold. The held-out result coincides entirely with the root.

A programming error is not needed to obtain this outcome: it is a consequence of the rule. It is not corrected by simply increasing `d_max`, because the path is stopped earlier.

### 7.5 Independent check of the computation

For all nodes the total `L_self` was checked against the closed Dirichlet-multinomial formula, independent of the prequential accumulation. The observed deviations are below `1e-8` bits in the checks performed.

For the blocking case the pre-update probability was moreover reconstructed through cumulative arrays, without using the routine of the tree. The six Deltas at depth 1 and 2 coincide with those of the sequential reproduction within `1e-7` bits; the actual deviations are much smaller.

These checks reduce the risk that the result derives from an error of the verification experiment. They do not constitute a general proof of correctness of every possible future implementation.

### 7.6 Comparison with the methodological source

Schürmann and Grassberger, §V.B, formulate the choice through a context that improves on the parent and the subsequent behaviour of the longer context. The text does not require that every ancestor, starting from the root, improves in turn. The difference of sign with respect to the HEXIS convention must of course be kept in mind.

In the case with a non-improving level 1 and an improving level 2, the two rules are not equivalent. The comment of the quarantined candidate that speaks of operational equivalence does not resolve this divergence. The second plan improves the name of the instrument, but keeps the problematic behaviour.

Source: [Schürmann and Grassberger, Entropy estimation of symbol sequences, 1996; arXiv version of 2002](https://arxiv.org/abs/cond-mat/0203436), §V.B, page 9 of the attached PDF.

## 8. What can be kept and what is not yet decided

The direction recommended for the next revision is already sufficiently founded:

- descriptive study on the delimited Greek corpus;
- conclusions conditional on representation, segmentation and protocol;
- evaluation of all eligible positions;
- blocks individually visible, with a distinction between weights within a block and across blocks;
- no scientific replication attributed to the seeds;
- real fits after the definition and validation of the instrument;
- retirement of the out-of-scope branches without leaving incomplete application entry points active;
- no promise to identify the causal effect of the metre or the memory of the language.

It remains to be decided whether the desired contribution is necessarily that of an **adaptive variable-context meter**, or that of a **descriptive predictive measurement** for which the choice of the instrument remains open. These two priorities can require different paths and different development times.

Replacing monotone with an `argmax` string is not an already verified solution: the exact set of candidate nodes, the optimized quantity, the implicit or explicit penalties and the fallback must be defined; then it must be verified that the recovery of order 2 does not happen at the price of overfitting on the i.i.d. checks or of a cost incompatible with the purpose.

No replacement rule was implemented or certified in this delivery. Presenting it as definitive before these checks would contradict the criterion required for the work.

## 9. Explicit limits of the verification

Verified were the commit, the existing suite, the Greek counts, the hashes of the inputs, the permutation counterexample, the conflict between selector and benchmark and the documentary points discussed above.

Not certified were:

- all the philological details of the 17 documents and every continuity needed by P-BOUND;
- a scientific measure on the Greek texts, because no model was trained on them;
- the duration of the implementation of the new protocol;
- a complete pipeline of the reduced design, absent today;
- the power tables of the first plan;
- the absence of every other defect in the repository;
- the general validity of a replacement instrument still to be selected and validated.

The bibliographic comparison confirms that the separation of prose/verse through syntactic features has important precedents. The work of Gianitsos et al. reports over 97% accuracy and F1 in its own study; this prevents a naive claim of primacy, it does not automatically certify the identification of a universal property of Greek. [Gianitsos et al., 2019](https://aclanthology.org/W19-2507/).

The literature on context trees for linguistic rhythm also uses its own selection procedures, with specific hypotheses and results: it does not automatically transfer those guarantees to the HEXIS selector. [Galves et al., Context tree selection and linguistic rhythm retrieval from written texts](https://arxiv.org/abs/0902.3619).

## 10. Reproducible materials and traceability

The verification archive delivered separately contains:

- `check_corpus.py`: recomputation from the CoNLL-U files, without real fits;
- `check_method.py`: autonomous reproduction of the literal rule and synthetic checks;
- `check_independent.py`: second numerical reconstruction and counterexample using the permutation function of the repository;
- `corpus_check.json`, `method_check.json`, `independent_check.json`;
- instructions, version references and hashes of the files of the archive.

It does not contain the raw data of the corpus, nor a new version of the project. The times of the scripts are times of the synthetic checks in this environment; they are not benchmarks of the future HEXIS pipeline.

SHA-256 of the attachments analysed:

```text
piano_finale_HEXIS.md
c9b4ecee16040d4f9bf57c29e3bd1ed29a98c9a2f484e678499769143f0d1835

piano_ultimato_HEXIS.md
1c0bf17490a48b63921f42db8755d15de8abb1426ef9adefc52bdae9fcdf6d47
```

**Operational outcome:** keep the second plan as the basis of the revision; apply neither of the two in full. The definitive proposal remains suspended on the clarification of the status of the instrument, with sufficient evidence to exclude the unchanged ratification of `monotone-stop` together with the current requirement of reliable recovery of order 2.
