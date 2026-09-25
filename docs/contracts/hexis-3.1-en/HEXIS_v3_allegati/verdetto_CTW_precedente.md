> **Non-normative companion translation; the Italian original governs** (V3-003, B2).
> Original: `docs/contracts/hexis-3.1/HEXIS_v3_allegati/verdetto_CTW_precedente.md`, SHA-256 `6ceac64acffe31ef0e8705fcf44adb18dd18ca38193ffabbcf14ef1799f8a133`.
> Translated on 2026-09-25. Structure, tables, values and identifiers follow the original, including links; numbers use English notation. Any translator's note is marked *[Translator's note: …]* and changes nothing in the original.

# HEXIS — verification of the CTW and feasibility verdict

**Date:** 11 September 2026.  
**Subject:** authorized verification of the move from the `monotone-stop` selector to a Context-Tree Weighting for a non-binary alphabet.  
**Status:** verification concluded; no change applied to the repository; new update plan still to be written.

## Verdict

**The move to the CTW is technically feasible and now has a working prototype, verified both mathematically and at the real dimensions of HEXIS. We can proceed to writing the new plan.**

The favourable outcome concerns a descriptive study of predictive performance on a finite corpus. It does not authorize three stronger conclusions: that sparsity is eliminated, that the model recovers all the linguistic information, or that the gain over the root automatically identifies dependencies internal to the text. The checks show precisely why these conclusions would be wrong.

The new plan will have to adopt the verified operational conventions and a control that destroys the order of the symbols while preserving their composition within the sentence. The latter uses the same CTW: it does not require a second scientific instrument. Its necessity emerges from a controlled counterexample, not from a generic caution.

A production pipeline already integrated in HEXIS was not verified: the canonical core of the repository still contains unimplemented functions. The feasibility of its replacement and of the protocol needed to use it was verified.

## 1. Provenance, authorization and integrity

The GitHub connection confirms the branch `g1/pre-audit` at commit `852644b6917790877c7b2ca5df2e76b17829d87c`; `master` remains at commit `3f5a6eafac83e5c190a866c8bea1937d8284ce75`. The audit uses the former, consistently with the previous review.

`AGENTS.md`, configuration, model interfaces, sampling, scores, downsized proposal and methodological source were reread. The 120 tracked files were compared through SHA-256 before and after the checks: **no variation; clean Git status**. The modules of the quarantined candidate were not imported; original data or attachments were not modified.

The real trials are separate feasibility experiments, authorized by the request to verify the change. They do not constitute passing the old gates G2/G3, nor an implicit ratification of the new specifications. No contrasts between regimes, p-values or scientific confidence intervals were computed.

References to the verified copy: [HEXIS repository](https://github.com/leonardotornabene/HEXIS/tree/852644b6917790877c7b2ca5df2e76b17829d87c), [specification in force](https://github.com/leonardotornabene/HEXIS/blob/852644b6917790877c7b2ca5df2e76b17829d87c/docs/01_MASTER_SPEC.md).

## 2. Verified data

The three Greek CoNLL-U files were read again, re-encoded with a separate procedure and compared with the hashes of `PROVENANCE.md` and of the previous audit. The UD commit is `37837c7a3c592c9563f8c51cc63344b87247f8a5`.

| Element | Verified quantity |
|---|---:|
| Original Greek tokens | 202,989 |
| Original Greek sentences | 13,919 |
| Tokens of the seven primary blocks, C0 encoding | 154,300 |
| Primary positions with at least four retained predecessors | 109,108 |
| UPOS+DEPREL alphabet, C0 | 106 symbols |
| Alphabet with the `oth` category | 112 symbols |
| UPOS-only alphabet | 12 symbols |
| Budget per training block | 8,884 tokens |
| Training per fold: six blocks | 53,304 tokens |
| Tragic probe, C0 tokens | 22,275 |
| Tragic probe, eligible positions | 12,769 |

The inventory of the alphabet also includes the tragic probe, as in the proposal examined. It is a closed and transductive inventory of symbols; no counts of the held-out text are transferred into the training.

The sampler was implemented outside the repository: permutation of the sentences, whole sentences up to the budget, at most one final contiguous fragment, exactly 8,884 tokens per contribution. All documents of the held-out block are excluded. The numerical sensitivities use the same samples; the halved budget reuses the same initial permutation. A new encoding can change the stopping point of the sample, and this is recorded.

## 3. Verified formulation

The basis is the CTW for finite non-binary alphabets: probabilistic average over the trees and Dirichlet distributions at the nodes. The source consulted makes explicit the algorithm, the inference on the models and the extension to arbitrary Dirichlet parameters. [Kontoyiannis et al., version 3, 2022](https://arxiv.org/abs/2007.14900v3).

The configuration of the pilot, fixed before the real results, is:

| Choice | Value |
|---|---|
| Pseudocount per symbol, `a` | 0.5 |
| Prior probability of stopping, `rho` | 0.5 |
| Maximum depth | 8 |
| Monotone local selection | Absent |
| Threshold `k_min` or `gamma` | Absent |
| Probability on a never-observed branch | Uniform distribution over the same alphabet |
| Training | All ordinary tokens of the sample |
| Primary evaluation | Same coordinates for root and CTW; at least 4 predecessors in the sentence |
| Update during the evaluation | None, neither of the counts nor of the weights of the trees |

`a` and `rho` have different roles. The old name `beta` must not be reused ambiguously for both.

### Boundaries and counts

A question was resolved that a simple reuse of the CTW would not have resolved: if all tokens are counted at the root but those without a sufficiently long context are ignored in the children, the comparison between stopping and splitting can use different sets of observations.

The prototype uses **BOS only in the context**, as a terminal leaf representing the end of the available history. It is not predicted and does not enlarge the alphabet of the outcomes. Each observation of a node goes into exactly one child; the counts therefore remain a consistent partition. Isolated sentences and fragments reset the history.

This convention is an explicit conditional adaptation. The identity of the mixture is proved by induction in the attached mathematical contract and verified through enumeration; it is not attributed textually to the source nor used to transfer automatically asymptotic theorems to the heterogeneous corpus.

For the boundary sensitivity alone a context separator was verified, it too never predicted, between actually adjacent sentences of the same document. The check requires adjacency in the source identifiers and in the complete positions, not only in the sampled subset. A gap, a change of part/document, an empty sentence or a fragment interrupts the link. **This convention replaces the ambiguous one of the old plan in which `#` entered the denominator but was never a target.**

### Frozen prediction and numerics

The history of the test text advances, but the model does not learn from it. The check compares the frozen prediction with the explicit average of the predictions of all small trees, weighted only with the training data. This quantity is not confused with the online CTW prediction that updates the posterior at every token.

A concrete numerical problem was also verified: with 106 symbols, building in binary64 `rho = 1 - 2**(-105)` produces exactly 1. A naive translation of the suggestion of the source would therefore eliminate the probability of splitting. The prototype keeps the logarithms of the two probabilities separately; the corresponding sensitivity was run successfully.

## 4. Exact checks and synthetic integration

| Check | Outcome |
|---|---|
| Complete enumeration of small trees, alphabets 2/3 and depth 0–3 | 120 cases passed |
| Point checks, including probabilities and invariants | 9,189 assertions passed |
| Maximum error with respect to the enumeration | 1.07 × 10⁻¹⁴ |
| Identity between prequential code and integrated probability | Error 1.42 × 10⁻¹⁴ |
| Enumeration with separator and BOS | Predictive error 2.22 × 10⁻¹⁶ |
| Normalization, never-observed symbols/contexts, empty training | Passed |
| Invariance to renaming of the symbols and to the order of the streams | Passed |
| Counts and weights unchanged after the evaluation | Passed |
| Synthetic pipeline: seven blocks × 20 seeds | 140 fits completed |
| Held-out exclusion, exact budget, fragments and adjacency | Passed |
| Identifiers of the subseeds checked | 1,680, without collisions |

The central logic receives no regime labels. The construction of the corpus uses the registry to fix inclusions and blocks; the model and the sampler receive only the sequences and the map of the blocks. The order of the streams no longer requires an autonomous source of variability: the integrated evidence is invariant to that order.

## 5. Synthetic sources: what works and what remains limited

Each small source was verified with five seeds, 53,304 training tokens and 100,000 independent test tokens; the evaluation excludes the first four positions. No seed was selected because favourable.

| Source | Reference | CTW cross-entropy: minimum–maximum |
|---|---:|---:|
| Independent uniform, 4 symbols | 2.00000 | 1.99999–2.00007 |
| Deterministic cycle, 3 symbols | 0 | 0.0000813 |
| Immediate dependency, persistence 0.8 | 0.72193 | 0.72006–0.72641 |
| Dependency delayed by 2 positions, accuracy 0.9 | 0.46900 | 0.46467–0.47361 |
| Variable memory of order 1/2 | Oracle of the realization | 0.64854–0.65516; within the tolerance with respect to the oracle |

All thresholds declared before the experiments are passed. **The CTW recovers the delayed dependency without the intermediate veto of the previous selector.**

The trials with 106 symbols, three seeds per source, also show the limit:

| Source with 106 symbols | Outcome |
|---|---|
| Independent uniform | CE 6.72932–6.72962; reference 6.72792 |
| Delayed dependency spread over the whole alphabet | CE 5.08720–5.12908; reference 1.13109 |
| Same dependency, total pseudocount 1 | CE 3.84248–3.89842: improvement, but wide residual gap |
| Frequent binary core with 10% rare symbols | Positive gain: about 0.19–0.20 bits/symbol with C0 |

The second case is deliberately difficult: the model must estimate many contextual distributions from few examples each. The fact that the family can represent the source does not mean that 53,304 tokens suffice to estimate it. This is **an important empirical limit, not a failed correctness test to be hidden**. The CTW mitigates the selection problem and regularizes the estimate; it does not make available information that the sample does not support.

## 6. Real pilot and sensitivities

**140 C0 fits** were completed: seven folds × 20 seeds. In addition nine sensitivities were run on all seven folds, one seed each: **63 fits**, for 203 main and sensitivity fits in all. The tragic probe was evaluated under each of the 140 C0 models without training additional models.

The sensitivities cover total pseudocount 1, `rho=0.9`, split probability suggested by the source, half training, depth 6/12, `oth` alphabet, UPOS-only and context separator.

All end with finite scores and consistent eligible coordinates. In the 140 C0 fits the gain varies from 0.26001 to 0.55301 bits/symbol; the weighted mean depth varies from 1.00015 to 1.21930. These ranges describe the scores of the blocks and of the samples, **not an effect between regimes or a confidence interval**.

The standard deviation across seeds, per block, varies from about 0.00297 to 0.02065 bits/symbol. It is computational variability of the sampling, not uncertainty about the population of texts.

The most important reading is the concentration on short contexts. In the first seed, going from depth 8 to 12 does not change the CE at the observed precision; the maximum deviation going to 6 is about 2.42 × 10⁻⁷ bits/symbol. At depth 3, about 84–85% of the observed nodes have fewer than five occurrences. With the UPOS-only alphabet, smaller, the weighted depth rises to about 1.93–2.13.

These results **do not demonstrate that the language has memory 1**, nor that the UPOS alphabet is scientifically better. They show how much support the sample offers to the particular model and to the chosen representation. The half-training cell concentrates almost entirely at the first level: a confirmation of the role of size.

In the profiling of the first seed, the training observes 83–87 of the 106 symbols of the inventory; the rate of held-out targets never observed at the root is between 0 and 0.04194%. Smoothing guarantees positive probabilities in these cases too.

The complete ten-seed scientific analysis was not run for all sensitivities. The present trials verify execution, resources and behaviour; they do not certify the stability of a contrast between groups that was not computed.

## 7. Interpretive discovery and control on order

An additional control needed for the validity of the reading was built: seven internally i.i.d. texts, but with different binary frequencies. With a common training, the CTW obtains a gain from 0.523 to 0.894 bits/symbol, although there is no internal dependency in any text. The context helps to recognize which distribution is producing the observations.

When the training contains only texts with the same distribution as the test, the gain is practically null: from −0.0000068 to 0.000000035. **Therefore the pooled gain cannot be called, without further controls, a pure measure of the internal dependency or of the mutual information of the text.**

A concrete answer was verified: training and evaluating the same CTW after an independent shuffling of the order within each stream/sentence, preserving symbols and lengths. The shuffled training keeps exactly the same root counts as the original training. Held-out exclusion and budget remain identical.

Outcomes of the control:

- In the heterogeneous i.i.d. texts, the difference between original and shuffled gain stays between −0.00140 and 0.00176 bits/symbol.
- In the source with delayed dependency, that difference is between 0.52660 and 0.53177 bits/symbol: the dependency is distinguished from the mere change of frequencies.
- In the real pilot of the first seed, on all seven folds, the gain of the model trained and evaluated on the shuffled texts is 0 at the recorded precision, against 0.27277–0.53914 on the original texts.

The last result is favourable but remains a pilot with one shuffle per fold. It is not a significance test, does not demonstrate an effect of the metre and does not replace the controls of annotation and composition. The new plan will have to fix the replication of this control and its descriptive reading before the final analysis. The computational feasibility and the ability of the control to separate the two phenomena in the known cases are already verified.

## 8. Costs and implementation work

Separate profiling with Python 3.12.14, NumPy 2.3.5 and PyYAML 6.0.3; ordinary CPU, no GPU:

| Operation | Measure |
|---|---:|
| C0 fit, 53,304 tokens | 0.63–0.70 seconds |
| Evaluation of the excluded block | 0.024–0.224 seconds |
| Evaluation of the whole tragic probe | 0.046–0.055 seconds |
| Peak RSS of the process in the C0 benchmark | 174.4 MiB |
| Maximum RSS in the real sensitivity pilots | about 240 MiB, depth 12 |
| Maximum RSS of the synthetic battery | about 254 MiB |

The measured times concern this machine. A projection for a budget of the order of 700 fits is of the order of 10–30 minutes for the prototype and its support operations, with sequential execution; it is an estimate, not the measured duration of a complete 700-fit pipeline. Figures, final exports and conditions of the user's computer are not included in a time promise.

The six numerical output vectors for all 2,182,160 C0 positions of the 20 seeds would require about 100 MiB uncompressed, before coordinates and metadata. An example with 46,634 positions takes 162,270 bytes compressed. Coordinates must be kept in compact form and every tree discarded after the evaluation: there is no need to keep 140 trees in memory or to save every node of them.

The residual work is identifiable: integrate the core and the configuration, implement canonical sampler and scores, connect provenance/outputs, bring the tests, update documents and gates. The repository still contains stubs in the model, in the scores and in several commands of the pipeline. The prototype must not be presented as an already completed implementation of them. No new annotations, neural model or new corpus collection are needed for the verified perimeter.

## 9. Conditions to be adopted in the new plan

1. Adopt a single CTW for non-binary outcomes, with an explicit distinction between pseudocounts and priors on the trees.
2. Freeze counts and weights during the evaluation; keep the same target population for root and CTW.
3. Ratify the BOS handling and the possible context separator; eliminate the ambiguity of the old `#`.
4. Retire `monotone-stop`, `argmax`, `k_min`, `gamma` and the interpretations based on a single selected depth.
5. Keep the shuffled-order control as a diagnostic of the same instrument; do not interpret the pooled gain alone as internal dependency.
6. Limit the conclusions to the corpus, the encoding and the predictor; do not read the scarcity of deep contexts as a demonstrated grammatical property.
7. Keep the JSD of the root distributions as a separately identified descriptive reading, without reintroducing a battery of competing estimators.
8. Record that real pilots have already been observed. The new document must not pretend a preregistration preceding these observations.

**No technical blockers remain in the defined trials. Real scientific limits remain, now identified and addressable through a correct scope and controls already prototyped. It is on this basis, and not on a promise of absolute absence of limits, that the feasibility judgement is favourable.**

## Reproducible attachments

The archive comprises code of the prototype, independent checks, mathematical contract, protocol fixed before the results, JSON results, sample ledgers and reproduction instructions. It does not contain the original text of the treebank nor a copy of the repository. The hashes of the data and of the code allow identifying exactly the inputs and the verified version.
