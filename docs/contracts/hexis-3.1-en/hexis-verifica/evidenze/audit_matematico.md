> **Non-normative companion translation; the Italian original governs** (V3-003, B2).
> Original: `docs/contracts/hexis-3.1/hexis-verifica/evidenze/audit_matematico.md`, SHA-256 `c14e1a1326501ba45c7464be0d7a668d5c015c68728a85b51a2cd4d48627f9ab`.
> Translated on 2026-09-25. Structure, values and identifiers follow the original, including paths; numbers use English notation. Any translator's note is marked *[Translator's note: …]* and changes nothing in the original.

# HEXIS — independent mathematical verification of reviews A and B

Date: 15 September 2026. Perimeter: reading of the documents, examination of the isolated CTW reference, recomputation of the historical JSON files and small synthetic counterexamples. No new real fit, import from `candidates/` or modification of the repository. The proposals were not treated as authorizations for the migration.

## Verdict

Keep CTW, frozen prediction and four-term Q. Prefer B's downsizing: six cells C0, `a_total1`, `q_half`, D12, `oth`, UPOS; no final probe, `bound`, new balanced protocol, `deprel_only`, rank or mandatory normalized ratio. The main result must be the profile of the seven blocks; D_Q is a descriptive summary of the procedure. The global PART/ADV merging proposed by B is consistent with this solution, with target alphabets 100/105/11: the counts are the object of the parallel corpus audit, not of this mathematical verification.

A contains useful observations, but numerous conclusions go beyond the proofs. I did not find in the mathematical sections of B an error comparable to those listed below. The simplification of the outputs requires an explicit modification of the reconstructibility contracts.

## 1. What the archive really demonstrates

Independent reading of `verifiche_CTW_precedenti.zip/ctw_validation/`:

| Evidence | Actual coverage |
|---|---:|
| `pilot_C0.json` | 140 original fits = 7 blocks × 20 seeds |
| Each of the other nine `pilot_*.json` | 7 original fits, seed 0 |
| `shuffle_results.json`, real section | 7 C0 pairs, sampling seed 0 |

`verify_shuffle.py` explicitly calls `fold_data(blocks, held, 0, 8884)`: there is no shuffle campaign here over the twenty seeds or the other cells. The seven additional pairs in `contract_validation.json` use the new RNG convention and do not fill this gap.

From the 140 originals one reconstructs:

- mean original D_G = **−0.17802467965627133 bits/symbol**;
- sample SD across seeds = **0.011027771033396177**;
- range = **[−0.1982444032327907, −0.1573585891563815]**.

For seed 0 alone, with both arms archived, D_G = D_Q = **−0.17724076290276225**, since the seven recorded shuffled G are zero. It is not legitimate to call the mean value over the twenty seeds D_Q: G_R is missing on 19 seeds. A similar problem affects table A of the sensitivities: it contains D_G contrasts, not Q contrasts verified for those cells.

The recommendation to declare the pilots clearly is right. On the other hand A's sentences «the final result is already known» and «1,400 executions will discover nothing» are excessive. Conventions, contracts and now also the representation change; above all, a forecast of the results is not their verification.

## 2. CTW core and Q: confirmed

I compared the formulas of §§6–8 of the plan with `ctw_reference.py`. The BOS count ensures that every observation of a non-terminal node belongs to exactly one child; the integrated evidences allow the recursive stop/split mixture. The frozen predictor is a convex combination of the posterior local distributions under the weights learned on the training. It does not coincide with the prediction of the test obtained by progressively updating parameters and posteriors, but it remains a normalized conditional code.

An independent enumeration with rational probabilities, on a binary D2 case with separate streams, compared all five admitted trees: maximum error on the probabilities **1.1102230246251565e−16**, on the evidence logs **2.6645352591003757e−15**. This is a small autonomous check, not a complete certification of the future API.

The formula remains:

`Q = (CE0_O − CE_CTW_O) − (CE0_R − CE_CTW_R)`.

The identity of the root counts of the training does not imply identity of the root losses on the test targets: the shuffle moves symbols into and out of the mask of the first four positions. No terms or arms are eliminated on the basis of the pilot.

## 3. Zero in float64: not a collapse theorem

A §6.1 confuses three properties:

1. overwhelming predominance of one component in the evidence;
2. weight rounded to 0 or 1 in float64;
3. mathematical probability exactly zero.

With finite counts, `a>0` and stop/split priors both positive, at a non-forced node both evidences are positive. The stopping posterior is therefore mathematically strictly between 0 and 1. It can be indistinguishable from an extreme in the numerical representation.

The sentence «underflow threshold of log1p(exp(x)) ~37 nats» is wrong. Check already performed:

- `exp(−37) = 8.533047625744066e−17`;
- `log1p(exp(−37))` keeps this value, not zero;
- `exp(−745) = 5e−324`, while `exp(−746) = 0`.

About 37 nats is the scale at which a small component can be lost in the rounding of a weight close to one; it is not the underflow threshold of the exponential. Moreover the reference computes `hi + log1p(exp(lo-hi))`: when `hi` is large in absolute value, the small correction can be lost earlier. In the check `hi=−192272.7` and `lo=hi−25`, the result is already exactly `hi` in float64. There is no universal threshold of 37 for the whole implementation.

The margins of 6,680 or 20,454 nats reported by A, if correctly measured in its synthetics, imply an extremely sharp numerical approximation in those cases. They are not measurements of the real margins of all cells; I did not recompute them. The archive records `root_stop=0.0` in the 140 originals, but does not contain the log-evidences of the corresponding trees to reconstruct each margin without refitting.

Useful minimum diagnostic: next to `root_stop`, save

`delta_root = (log_rho + logE_root) − (log_split + sum(logW_children))`.

It is the posterior stop/split log-ratio at the root, computable during the fit. If necessary, report the logs of the two weights through stable formulas. Do not introduce a model-selection threshold or a new cell. A large margin at the root does not show that rho is irrelevant in the descendant nodes.

Even if G_R were numerically zero in a whole future campaign, the conclusion is «no contextual advantage measured in the control with this predictor». It does not show that composition does not contribute nor causally attribute all of G to linguistic order.

## 4. Depth and prior are not inert by construction

A §6.3 says D6=D8=D12 «exactly». The complete JSON files refute the D6/D8 identity, while confirming very small differences. At seed 0, D6−C0:

| Block | Difference of G |
|---|---:|
| Herodotus | −1.0838937192e−8 |
| Thucydides | −1.6743811893e−10 |
| Athenaeus | +2.4132042420e−7 |
| Diodorus | +2.5731305975e−11 |
| Plutarch | −5.5552333844e−8 |

D12/C0 is identical in the seven archived G values. None of these observations constitutes an identity of the method. Synthetic counterexample already run: binary de Bruijn sequence of order 9, training of length 20,480, test 4,096, evaluation from position 12. CE D6 and D8 = **0.999999999805135**; CE D12 = **0.017709289896079353**. A true dependency beyond D8 is therefore learnable in an appropriate case.

rho too changes the predictions: on a small synthetic binary training, the probability of the same outcome after the same history goes from **0.5882695298** with rho=0.1 to **0.6287599095** with rho=0.9. In the archived data `rho_literature` changes the G of Diodorus by **−0.0476143229**; `bound` changes it by **−0.0478091219**. A acknowledges these numbers but makes them incompatible with its own «inert» headings.

The CTW is a continuous mixture for interior priors and fixed counts. A steep response or a numerical saturation can look like switching; from the aggregates alone no responsible node is identified. A's hypothesis of a «discrete switch» in Diodorus remains to be verified; it is not an established diagnosis.

## 5. Prior from the literature and fit counts

The primary source confirms that the default proposed by the authors is beta about `1−2^(−(m−1))`, with beta the probability of stopping. Its log-split at m106 is **−72.78045395879425**; `1−2^(−105)` rounds to one in float64. Here A and the plan are right. It is a prior choice of the source, not an obligation for every HEXIS adaptation. Keeping the numerical test is sufficient in the reduced perimeter; omitting the rho cell explicitly renounces its final sensitivity.

The published version is: Kontoyiannis, Mertzanis, Panotopoulou, Papageorgiou and Skoularidou, *Bayesian Context Trees: Modelling and Exact Inference for Discrete Time Series*, **JRSS Series B 84(4), September 2022, 1287–1323**, DOI **10.1111/rssb.12511**. [Publisher's page](https://academic.oup.com/jrsssb/article/84/4/1287/7073257). The reasoning on the prior is in §2.2 of the [primary arXiv version v3](https://arxiv.org/html/2007.14900v3#S2.SS2). Adding the editorial metadata is appropriate; calling the same authors' preprint a «secondary source» is incorrect.

A is right that the counts can be reused. A and rho require new evidences/weights; a lower D requires forcing the leaves at the new limit and recursively recomputing the weights of the ancestors. Truncating only the evaluation of a D12 model while keeping its weights is not equivalent to redoing D8. In the synthetic case, correct truncation with reweighting reproduced D8 with zero error.

*[Translator's note: in «A and rho require new evidences/weights», A refers to the parameter a (the per-symbol Dirichlet mass), not to review A.]*

The reduction in count accumulation eliminates no scientific models:

- old plan: **1,400** combinations `(cell, block, seed, arm)`; simple reuse possible with **840** count accumulations;
- six cells: **980** combinations = `2×7×(20+5×10)`; reuse of C0/D12/a allows **700** accumulations in the simple strategy.

700 is not a claim of the theoretical minimum of every possible optimization. The 980 combinations remain to be reweighted, evaluated and verified according to their contract. The sampling of the numerical cells was already exactly paired in the plan; reuse does not create that property, it reduces duplicated work.

## 6. Available length, exposure and identification

The band `past>=8` saturates precisely the maximum number of symbols readable by D8 with within-sentence reset. It does not make equal the contexts, the observed support, the length of the sentences, the internal position nor the composition of the training. It is not equivalent to exact matching. For D12, the same band does not even saturate the available depth.

The original contrast recomputed in the band is **D_G=−0.18470778832902407**, not a twenty-seed D_Q. It is evidence against the narrow explanation «the contrast derives entirely from having fewer than eight predecessors in the targets», not a general exclusion of length confounding. Keep the two bands as the already planned diagnostic; do not promote the favourable result of the pilot to co-primary.

D_Q is a well-defined descriptive functional of data, protocol and seeds. It is, however, not identified as an intrinsic or causal effect of regime. A 50/50 cell equalizes a share of the training, but also changes the budget (53,304→18,564) and keeps different available blocks, chronology and annotation. A synthetic case in which 18,564 tokens suffice does not prove that they suffice for the corpus or for every type of dependency. The persistence of the sign does not «exclude the exposure mechanism» in general.

A reaggregation without one document is possible on the existing scores, but it is not a campaign retrained without that document: the excluded text may still have contributed to the trainings of the other folds. Do not add it as a new mandatory analysis.

## 7. Resolved mass, predictive responsibility and comparisons between alphabets

`lambda_s` is the mixture weight routed towards the context, before observing the target. The responsibility of that component for the actual outcome x would instead be `lambda_s*p_s(x)/q(x|h)`. The two quantities do not coincide. In the small verified example, the weight of the context of length 2 is **0.36363636**, its local probability of the outcome is 0.75 and the overall one 0.59090909: responsibility **0.46153846**. Do not rename the first as the informative contribution of the outcome.

B correctly notes that a single observation is support, not precision: with m106 and a0.5 the observed symbol has probability 1.5/54 and the others collect 97.2222%. L_resolved remains a diagnostic of the weights attributed to observed contexts, not grammatical depth or a certification of the recovered memory. Keep support, unobserved mass, histograms and null values with reasons; no new responsibility statistic is needed.

The near equality of the C0/UPOS contrast does not show that DEPREL does not contribute: similar contributions to the two groups can cancel in the difference; task, alphabet and total prior also change. `deprel_only` would not causally separate the contributions of the two levels.

`G/CE0` is a fraction of the loss of that specific task, not a normalization that makes different representations equivalent. Conceptual counterexample: adding to the outcome an independent unpredictable bit leaves G unchanged and increases CE0 by one bit, reducing the ratio without changing the original order dependency. It is not the «only comparable measure» promised by A. Do not add it as mandatory.

The rank 1/21 reflects that the two HEX blocks have the two lowest G in the pilot. Without exchangeability it acquires no inferential value; the fact that it is computable does not oblige inserting it into the report. The seven points already show the separation.

## 8. Motivated cuts and minimal verifiable outputs

Cut D6 because a single upper perturbation D12 is enough for the perimeter; cut bound because a within-sentence question is chosen; cut probes because they open a distinct question; cut rho declaring the sensitivity renounced. Keep `a_total1`, `q_half`, D12 to verify three different choices: local regularization, data availability, depth limit. These motivations hold even if the pilot had given another sign and therefore avoid outcome-driven selection.

The synthetic learning thresholds depend on the family of sources, marginal distribution, length, segmentation, prior and metric. Changing m at equal copy probability does not necessarily keep the amount of predictable information fixed. A's numbers are not thresholds for Greek nor a general ranking of the «power» of the representations. Keep the predetermined synthetics and the declared stress; the merging of the alphabets requires explicitly updating the parameters of the target tests, not reusing m106 attestations as if they automatically validated m100.

It is reasonable to persist all positions only in C0 and aggregates in the sensitivities, provided that the following are kept:

- complete keys, ledgers, model hashes, coordinates/identity of the corpus and parameters needed for regeneration;
- per document, seed, arm and band: n and sums of the two losses; verifiable derivation of blocks, four CE, Q, contrasts and weights;
- per-fit diagnostics, per-band counts, supports and predetermined mass/routing histograms, denominators of the null values;
- summaries at the levels and with the weights exactly prescribed; the per-target mean of L_resolved is not reconstructed from the ratio of the aggregated masses alone.

Four sums are not enough to reproduce histograms, coordinates or any future positional statistic. T27 must distinguish reconstruction from the C0 rows, reconstruction from the aggregates of the sensitivities and regeneration check controlled by the ledger. Do not promise positional reconstructibility from aggregates that have lost the information. Verify the pairing of the slots before aggregation. Do not impose future assertions G_R=0 or L_resolved_R=0 only because they were observed in the pilot; use normal compression and aggregation.

## Reproducible evidence of this audit

- Isolated script: `/private/tmp/hexis_math_audit_20260915/audit_math.py`.
- Output already produced: `/private/tmp/hexis_math_audit_20260915/math_checks.txt`.
- Extracted copy of the attachments: `/private/tmp/hexis_math_audit_20260915/HEXIS_v3_allegati/`.
- History: `/private/tmp/hexis_math_audit_20260915/history/ctw_validation/`.
- Runtime of the check: Python 3.12.13 and NumPy 2.5.1 of the repository, no dependency added.

Only the proofs documented in the script were performed. The larger synthetic experiments declared by A were not repeated and are not presented as independent verifications of this audit. The report concludes a review; it does not apply the new design to the binding documents of the project.
