> **Non-normative companion translation; the Italian original governs** (V3-003, B2).
> Original: `docs/contracts/hexis-3.1/HEXIS_piano_definitivo_v3.1_2026-09-15.md`, SHA-256 `9fd6fd832df783f7e8c3f5e1ba17e349bdb0e2e6993bbdad9a3f32dc2844bd18`.
> Translated on 2026-09-25. Structure, numbering, tables, formulas, values and identifiers follow the original, including Italian file names; numbers use English notation (decimal point, thousands comma). Any translator's note is marked *[Translator's note: …]* and changes nothing in the original.

# HEXIS 3.1 — Definitive realignment plan

**Within-sentence order of morphosyntactic annotations in a finite corpus of ancient Greek**  
**Scientific specification, operational contract and migration plan — 15 September 2026**

**Status of the delivery:** documentary adoption of decisions C01–C30 of the consolidated verdict of 15 September; plan ready for the normative migration, the implementation and the drafting of the new research proposal. **Not applied to the repository; no future software gate attested; no final result available.**

This version replaces plan 3.0.1 as the target document. The current request authorizes the realignment of the plan: it is not used to modify the code, run new real fits or retroactively rewrite the decisions of the repository. The future deposit of **V3-001** will explicitly apply the new design. Until that deposit, the v2.1 rules continue to govern the executions of the repository.

## 0. Authority, materials and use of the document

The plan is a complete rewrite consistent with the [consolidated verdict](/Users/leonardoTornabene/Desktop/hexis-verifica/HEXIS_verdetto_consolidato_2026-09-15.md), including the technical corrections and the methodological renunciations motivated in the verification. The prescriptions contained in the earlier materials were examined as the object of the review, not executed as operational instructions. Reviews A/B remain critical history; they are not competing normative sources.

The delivery comprises this document and the folder [HEXIS_allegati_v3.1_2026-09-15](/Users/leonardoTornabene/Desktop/HEXIS_allegati_v3.1_2026-09-15/):

| File | Function |
|---|---|
| `hexis_v3.1_design.json` | Structured contract: identity, complete registry, blocks, transformations, six cells, seeds and populations |
| `corpus_atteso_v3.1.json` | Document and block counts, expectations of the merged representation |
| `alphabets_v3.1.json` | Three lexicographic lists, IDs and types present only in the six non-evaluated documents |
| `report_contract_v3.1.json` | Granularity of the outputs, expected keys, reconstruction and completeness checks |
| `design_lock.json` | External digests of the plan and of the contracts; V0 deposit still null |
| `verifica_documentale.json`, `SHA256SUMS.json`, `LEGGIMI.md` | Provenance, checks performed and preservation instructions |

The text governs the semantics; the JSON files make its values and lists explicit. A divergence is an error to be corrected before the deposit, not an alternative left to the implementer. The 3.0.1 attachments are no longer the target contract. Their archive remains necessary **only as historical evidence and identified source of the fixtures**, with the limitations of §12; none of its scripts is to be executed indiscriminately.

Material references:

| Object | Identity |
|---|---|
| Repository examined | `g1/pre-audit`, commit `852644b6917790877c7b2ca5df2e76b17829d87c` |
| Original plan 3.0.1 | SHA-256 `83fed73f273c0552281a7180b101f944c84577b100c43e5a738d95cb85ebab38` |
| Operational ZIP 3.0.1 | `HEXIS_allegati_operativi_v3_2026-09-11.zip`, SHA-256 `6f2e5935b0d0bd70e98028414d085f74e1bd617fc5e293c0b61c8b99a266db8f` |
| Consolidated verdict | SHA-256 `9cf75b7618864fa208092f5ed163976a385ef5fb0bad806e846ff84661fa7a12` |
| Repository lock | SHA-256 `33db43b00bcb21ab12aedf6dcc4257764770bff0115dc0d1dfab6e5ea89876bf` |

Appendix A traces all thirty adoptions. The design leaves nothing to be chosen during the fits: corpus, model, number of cells, weights, seeds, evaluated population or mandatory results. What remains is to build and verify the software contracts specified here.

## 1. Scientific object and hierarchy of results

### 1.1 Definitive question

> In the pinned UD Perseus Greek corpus, what additional predictive advantage does the within-sentence order of the annotations offer over their within-sentence shuffling, under a frozen CTW trained on the other blocks? How do the profiles of the documents and blocks vary with representation, budget and essential choices of the predictor?

HEXIS is a **descriptive, reproducible study of a finite corpus**. The CTW predictor probabilistically combines finite-memory context trees; it does not select a single order. The measures compare out-of-training predictive losses, expressed in bits per eligible encoded symbol. The analysis concerns the sequences of annotations, not the lexicon or the complete syntactic tree.

The contribution consists in making this comparison controllable, showing the profiles of the available texts and quantifying how much the scores depend on the declared choices. It does not require that long memory, separation between groups or positive results emerge. The precedents on variable contexts and rhythm, Greek syntactic stylometry and prose/verse classification delimit the novelty (§18).

### 1.2 Single hierarchy

1. **Main result:** the seven block Q profiles, with original/shuffled G and all four CE; the eleven primary documents are visible separately.
2. **Subordinate summary:** HEX/prose difference of the equal-weight block means, D_Q, with original and shuffled D_G.
3. **Mandatory second weighting:** the same quantities per group and contrasts weighted by eligible targets of the current variant.
4. **Diagnostics:** history bands, context support, mixture weights, retention, training exposure and fragments.
5. **Distributional reading R1:** JSD of the complete original counts of the seven blocks, in the three representations.

Seeds are computational replicates. Sample SD, minimum and maximum across seeds describe sampling and shuffling; they do not constitute population uncertainty. The eleven documents are not eleven independent replicates. No p-values, bootstrap intervals, Holm corrections, Bayes factors between regimes or permutation ranks are computed.

### 1.3 Scope of the conclusions

Descriptions of the advantage measured under this predictor, this encoding and these trainings are admitted. Not identified are: a causal effect of metre, a separate effect of epoch/author/genre, the true entropy of Greek, the mutual information of the language, the complexity of the grammar or cognitive difficulty.

DEPREL derives from the analysis of the complete text and can depend on later words and on the syntactic head. Predicting the labels does not simulate a reader anticipating words. The sequence keeps categories and relations, losing the hierarchy of the tree. Empirical cross-entropy is a coding cost under a fixed predictor: it does not automatically become an entropy rate or a mutual information.

## 2. Prior evidence and epistemic status

The protocol is **prospective after methodological development and observation of real pilots**, not a preregistration preceding every observation. The new merging changes the task and the total prior; the final campaign is not an identical replication of the pilots. Changing the seed convention does not erase the exposure to earlier results.

| Evidence | Coverage and limit |
|---|---|
| Repository suite in the verification of 15 September | 327 passed, 17 skipped; the skips are scaffolds, not acceptance of the future CTW |
| Historical CTW enumeration | 120 cases, 9,189 assertions; maximum error 1.07×10⁻¹⁴; archived evidence, not re-executed in the present drafting |
| Historical prequential/integrated identity | Maximum error 1.42×10⁻¹⁴ on the training |
| Independent rational case of the verification | Five trees in a binary D2 case; probability error 1.11×10⁻¹⁶ |
| Small synthetics of the verification | 25 cases re-executed; effective thresholds respected, including cycle CE<0.02 |
| Historical C0 pilot | 140 original models, seven blocks × twenty seeds, alphabet m=106 |
| Historical sensitivities | 63 original models, seven for each of the nine historical configurations; seed 0 |
| Historical order control | Seven C0 pairs at seed 0 only; not twenty paired seeds |
| Subsequent contract 3.0.1 | Seven C0 pairs with new RNG plus one `bound` pair: 16 models and 84 tragic evaluations; historical proofs, not 3.1 results |
| Review of 12 September | Environment re-executions, diagnostics, fragments and report fixtures; not a final campaign |

From the twenty original seeds one reconstructs **mean original D_G = −0.1780246797**, SD across seeds 0.0110277710, observed range [−0.1982444032, −0.1573585892] bits/symbol. The historical paired control allows **D_Q ≈ −0.1772407629 at seed 0 only**; here it coincides numerically with D_G. The shuffled arms needed to call D_Q the mean contrast over the twenty seeds, or the contrasts of the original sensitivities, are missing.

The pilot documented sparse support of deep contexts: about 84–85% of the nodes observed at depth 3 have fewer than five observations; D12/C0 coincide at the archived precision. This does not prove short grammatical memory. The lag-2 stress test with m=106 has CE about 5.09–5.13 against an oracle of about 1.13109; with total Dirichlet mass 1, about 3.84–3.90. The ability to represent a dependency does not guarantee that it is learned in the sample.

The historical sensitivities of Diodorus are real: change of G about −0.04781 bits in `bound` and −0.04761 with the extreme prior. They do not identify a single responsible node nor demonstrate a bug. They remain in the development account; the retired configurations are not reinserted in the campaign.

The historical attachment `authorization_and_experiments.json` is an account of the earlier authorizations. The present drafting does not independently verify the original consent, does not deny it and does not invent times. V3-001 will record its source, scope and verifiability, distinguishing it from any recovered original act. No old G2 is retroactively declared passed.

## 3. Corpus, identity and units

### 3.1 Pinned source

Only the three Greek CoNLL-U files of UD Ancient Greek Perseus `r2.18`, commit `37837c7a3c592c9563f8c51cc63344b87247f8a5`, are used. The train/dev/test splits are recombined; they have no experimental function.

| File | SHA-256 |
|---|---|
| `grc_perseus-ud-dev.conllu` | `7899f809fc250404839694330b9db25f79a5b1f20cfa12e6dc3a368a4ec7cd22` |
| `grc_perseus-ud-test.conllu` | `e18d47c395c0ec8da678fb5e315ce6d90133e88c25ed2a55bc72a2a66e6254d5` |
| `grc_perseus-ud-train.conllu` | `d7471c9b91bcd975848fa5d9b65c31f1fc48a597ed3667796968a82c6d098a7e` |

Any discrepancy interrupts the audit. The raw files remain immutable and ignored by Git. A new version of the corpus requires a new contract and new results. The provenance needed to reproduce the acquisition must be tracked outside `data/raw/`.

### 3.2 Units and registry

- Source token: CoNLL-U line with integer ID; multiword tokens and empty nodes add no observations.
- Source sentence: unique `sent_id`; no redefinition by punctuation or verses.
- Canonical document: work/excerpt defined in the registry. Athenaeus XII and XIII are two parts of one document.
- Dependency block: excluded entirely from training; uniform-weight unit of the subordinate summary.
- Seed: computational replicate, never an independent scientific unit.

The census comprises **202,989 source tokens, 13,919 sentences, 18 prefixes, 17 documents**. The structured registry keeps all prefixes, URNs, `part_order`, attributions, epochs, original regimes, roles and flags. No identity is inferred from the title. Appendix B shows the complete correspondence.

`PROSE_ALL` groups `PROSE_CLASS` and `PROSE_POST` in the report; it does not replace the source regime. “Homeric tradition” and “Hesiodic tradition” are conservative exclusion conventions, not proofs of common authorship or statistical independence of the blocks. The Hymn to Demeter remains attributed to Anonymous; the Shield keeps the traditional attribution with an explicit flag.

### 3.3 Eleven primary documents in seven blocks

| Block | Works/excerpts | Group | C0 tokens | C0 targets | OTH tokens | OTH targets |
|---|---|---|---:|---:|---:|---:|
| HOMERIC_TRADITION | Iliad; Hymn to Demeter | HEX | 71,088 | 46,634 | 71,547 | 47,062 |
| HESIODIC_TRADITION | Theogony; Works and Days; Shield | HEX | 9,282 | 6,375 | 9,308 | 6,398 |
| HERODOTUS | Histories I | PROSE_ALL | 17,301 | 12,946 | 17,349 | 12,994 |
| THUCYDIDES | Histories I | PROSE_ALL | 9,346 | 7,227 | 9,353 | 7,234 |
| ATHENAEUS | Deipnosophistae XII–XIII | PROSE_ALL | 23,133 | 16,691 | 23,231 | 16,786 |
| DIODORUS | Bibliotheca historica XI | PROSE_ALL | 15,266 | 12,334 | 15,266 | 12,334 |
| PLUTARCH | Lycurgus; Alcibiades | PROSE_ALL | 8,884 | 6,901 | 8,893 | 6,908 |
| **Total** | **11 documents / 7 blocks** | **2 HEX / 5 prose** | **154,300** | **109,108** | **154,947** | **109,716** |

UPOS has the same tokens and targets as C0. The new merging changes no mask. The Iliad makes up about 97.5% of the tokens of the Homeric block: this dominance must appear in the description of the profile.

### 3.4 Six documents only inventoried

Sophocles' Trachiniae, Antigone, Ajax, Oedipus Tyrannus and Electra, and Aeschylus' Suppliant Women have role **`inventory_only`**: census, retention and inventory of types, without training, scoring, probe or tragic figure. They are texts in mixed metres, not a homogeneous control of trimeters. Their 22,275 C0 tokens and 12,769 potentially eligible positions remain audit counts, not positions to evaluate.

To keep the support choice of the verified plan, the alphabet uses all 17 documents. After the merging, the six non-evaluated documents add **9 exclusive C0 types, 10 OTH, zero UPOS**. The support therefore remains closed and transductive: the types of the complete corpus are known, without transferring frequencies or transitions to the training. Restricting to the primary documents alone would produce 91/95/11 types and would be another modification, excluded here.

### 3.5 Limits of the comparison

In the primary set HEX coincides with the archaic component; comparable archaic prose is missing. Chronology, tradition, genre and form are not separable. The prose labels concern works, without token-by-token metrical certification. The `subdoc` fields of the Athenaeus XML files examined are passage references, not automatic quotation markers: no metrical census of the quotations is invented.

The annotation is not necessarily homogeneous across works. The merging of §4 mitigates a concrete discontinuity without making all categories or DEPREL uniform. Sufficient metadata for a per-annotator control are missing. Long sentences contribute more targets; excluding the first four symbols does not equalize their distributions.

## 4. Representation, audit and targets

### 4.1 Deterministic order of the encoding

1. Keep lines with integer ID and all source coordinates; validate tags and structure. An unknown source UPOS is an error also in the public mapping function.
2. Apply `PROPN → NOUN`, then the mask of admitted UPOS.
3. Derive the base relation with `lower().split(':', 1)[0]` and apply the policy of the variant.
4. Merge **globally** `PART → ADV_PART` and `ADV → ADV_PART`; no condition on lemma, text or group.
5. Build the symbol and assign the ID of the frozen lexicographic inventory.

UPOS admitted before the merging: `ADJ, ADP, ADV, AUX, CCONJ, DET, NOUN, NUM, PART, PRON, SCONJ, VERB`. Removed: `PUNCT, X, INTJ, SYM`. `ADV_PART` is a project category, not a new UD tag acceptable as source input.

The 23 relations kept are: `root, nsubj, csubj, obj, iobj, ccomp, xcomp, obl, advcl, advmod, acl, amod, appos, det, nummod, nmod, case, mark, aux, cop, cc, conj, parataxis`. `ud23` names this historical subset, not the whole UD inventory.

| Variant / cell | Policy | m | Total mass with a=0.5 |
|---|---|---:|---:|
| `ud23` / C0 | Symbol `merged_UPOS:base_DEPREL`; remove relations outside the 23 | **100** | **50** |
| `ud23_oth` / oth | Same UPOS; outside relations aggregated into `oth` | **105** | **52.5** |
| `upos_only` / upos | **C0 mask**, then projection onto the merged UPOS | **11** | **5.5** |

IDs are consecutive from 0 over the lexicographically sorted strings. BOS has internal ID −1, only in contexts; it does not belong to the outcomes. No SEP, EOS or `UNK` is provided. A new symbol after the freeze causes an error. `representation_version = hexis-3.1-adv-part-1` distinguishes the new inventories from the 106/112/12 of the pilots.

Removals close the gaps: context counts retained symbols, not distance in raw words. Source UPOS and DEPREL are kept in the audit. No manual re-annotation, lexical heuristic, FEATS, lemma or lexicon enters the predictor.

### 4.2 Reason for the merging and limits

The direct check counts **11,270 PART in the two HEX blocks, zero in the five prose blocks**: 9,884 Homeric and 1,386 Hesiodic. For γάρ, the Homeric block has 526 PART/13 ADV, the Hesiodic 54/0, and prose only ADV. The Hymn to Demeter has zero PART and contains all thirteen Homeric ADV γάρ: the discontinuity does not coincide perfectly with the group at document level.

The detail of a discontinuously applied distinction is deliberately reduced. It is not claimed that every PART annotation is wrong nor that the merged corpus is homogeneous. CCONJ, DEPREL and cases such as δέ/τε keep residual heterogeneity. The merging also changes m and the mass of the prior: a comparison with the pilot does not identify a pure effect of the PART/ADV distinction alone.

### 4.3 Informative census and checks

For each document, block and original regime record: source UPOS/DEPREL, removals with cause and coordinates, raw→encoded retention, eligible/encoded, number of sentences without targets and distribution of encoded lengths. Take the census of all 17 documents; make the checks readable in the primary blocks too.

- **A:** for each excluded relation, tokens with admitted UPOS and that relation divided by all raw tokens of the regime; a share >2% flags. Do not sum relations to compare them with the threshold. Also show the same counts per document/block.
- **B:** document retention <70% flags.
- Hashes, identities and expected counts are exact checks: a discrepancy fails. Thresholds A/B are diagnostics, not certificates of comparability.

The corpus contains **27 base DEPREL and 28 labels** counting `nsubj:outer`. PROPN and SYM have zero occurrences; sentences empty after encoding are zero. They remain test cases, not transformations actually observed. The 374 `discourse` are all INTJ, already excluded by the UPOS: OTH does not recover them. The excluded `vocative` with admitted UPOS are 459 Homeric and 26 Hesiodic, about 0.560% and 0.242% of the respective raw tokens. Do not qualify them without proof as relations typical of poetry. The verified census does not exceed the conventional thresholds; the values must nonetheless be recomputed by the implementation.

### 4.4 Targets fixed before the scores

A slot is eligible if it has **at least four ordinary retained predecessors in its own sentence**, zero-based index `j ≥ 4`. All training tokens, including initial ones, contribute to the counts. In the test the first four feed the history without receiving primary loss. All eligible positions are evaluated, without test budget or subsampling.

In C0 **53,009/80,370 = 65.96%** of the HEX tokens and **56,099/73,930 = 75.88%** of the retained prose tokens are eligible. The result concerns internal positions and weighs long sentences more. The two diagnostic bands are **4–7** and **≥8** predecessors, in every cell and arm. They are not co-primary; in D12 the second does not guarantee twelve predecessors.

Root and CTW, original and shuffled, use the same slots in the variant. The numerical cells and UPOS keep the C0 mask. OTH also changes the target population; no pairing is forced between rows of different encodings.

## 5. Training, sampling and randomness

### 5.1 Exclusion by block and budget

For each held-out block and seed, exclude **all** its documents. Each of the other six contributes exactly **q=8,884 tokens**, for **53,304** in total. q is the C0 minimum among the seven blocks and stays fixed in OTH too. `q_half` uses **4,442**, total **26,652**.

| Test group | HEX in training | Prose in training | Test group in training |
|---|---:|---:|---:|
| HEX | 1/6 | 5/6 | 1/6 |
| Prose | 2/6 | 4/6 | 4/6 |

The training is balanced by block, not by group. The table of the seven folds reports these shares, also next to the contrasts. Q does not automatically correct the asymmetry; neither its direction nor a conservative character is presumed. The share of one's own group takes two values determined by the label and does not by itself identify the effect of exposure. No `balanced`, common models or per-regime fits are added.

When Plutarch contributes in C0 it uses all its 8,884 tokens: multiset and counts of the original arm are fixed; the order of the ledger can vary and **the shuffle still varies** across seeds.

### 5.2 Exact sampling algorithm

1. Sort all sentences of a block by `(canonical_doc_id, part_order, source_ordinal, sent_id)`, including any sentences encoded as empty.
2. Permute the indices uniformly with the `sample` subseed. Empty sentences remain in the universe of the permutation but consume no budget.
3. Consume whole sentences until the next one exceeds the positive remainder. From that last one choose uniformly a contiguous segment of length equal to the remainder, with a sentence-specific `fragment` subseed.
4. Stop as soon as q is reached: no repeated sentence, at most one fragment per contributor, hence six per pair.
5. Record `sent_id, start, end, fragment`, with interval `[start,end)` in the encoded sentence, source coordinates and subseeds.

It is a sampling that favours whole sentences, not a uniform sample of single tokens. Each sentence/fragment is an **autonomous stream with reset**. The excluded part of the sentence provides no history. BOS means start of the history available in the sampled stream, not necessarily a natural linguistic boundary.

C0, `a_total1`, D12 and UPOS reuse exactly the C0 ledger per fold/seed. `q_half` reuses the permutation but the final random cut can change: no token-by-token nesting is promised. OTH reuses the order of the sentences but can stop elsewhere. The two arms always share the cut coordinates of their own sample.

The final fragment is kept to guarantee an equal token contribution. The historical twenty-seed test found 671 fragments in 840 contributions, 563 with an internal start; the ablation at the first seed only produced a maximum absolute Q deviation of 0.000685 bits/symbol. These are local proofs with the old alphabet, not a universal bound or a final analysis to be repeated compulsorily.

Per contributor/pair record `fragment_count`, `internal_start_count`, `fragment_tokens`, `direct_context_targets = Σ min(D, fragment_length)` for fragments with start>0. The maximum is **six fragmented segments per pair, 2,940 segment occurrences in the whole campaign**, counted once per pair and shared by the two arms; the occurrences in the arms are at most 5,880. The reuse of the ledger across cells can further reduce the number of materially distinct segments.

### 5.3 RNG, identity and invariance

Master seed **20260706**; C0 seeds **0–19**, each sensitivity **0–9**. Convention **`hexis-v3-rng-1`**, distinct from the historical XOR/CRC32.

`block_key = SHA256(canonical JSON of the sorted list of member canonical_doc_id)`. Author, epoch, group and display name of the block do not enter the derivation. For each draw:

```json
{"version":"hexis-v3-rng-1","master":20260706,"seed":0,"held":"<held_block_key>","block":"<contributing_or_evaluated_block_key>","purpose":"sample","sid":"","start":0,"end":0}
```

UTF-8 JSON with `ensure_ascii=False`, `sort_keys=True`, `separators=(',', ':')`, without newline. The integer seed is formed by the first 16 bytes of the SHA-256, big-endian; use `numpy.random.Generator(numpy.random.PCG64(seed))` (equivalent to `default_rng(seed)` with the verified PCG64).

Active purposes: **`sample`, `fragment`, `shuffle_train`, `shuffle_eval`**. `sample` uses an empty sid and 0/0; `fragment` uses sent_id and 0/0; the shuffle uses sent_id and start/end of the segment, or 0/length for a whole test sentence. In `shuffle_eval`, `held` and `block` are the key of the test block. The historical purpose `shuffle_probe` is retired from the active contract.

Numerical parameters, cell, variant, labels and the hash of the configuration do not enter the seed: this preserves the required pairing. In training each sentence uses an independently derived shuffle RNG: reordering the streams does not consume a shared generator. Renaming and reordering the records must not change samples, counts or scores. Changing the members of a block changes the key and requires a new version.

## 6. Mathematical contract of the CTW

### 6.1 Counts and local distributions

A is the frozen alphabet, m its cardinality; C0 has D=8, **a=0.5 per symbol**, **ρ=0.5 prior probability of stopping**. Do not reuse the ambiguous name `beta`. A node s represents a suffix traversed from the most recent to the least recent symbol. For an ordinary outcome x:

\[
N_s=\sum_{x\in A}n_s(x),\qquad p_s(x)=\frac{n_s(x)+a}{N_s+ma}.
\]

All observed contexts up to D contribute. There are no `k_min`, `gamma`, heuristic pruning, `argmax`, monotone selection or additional penalties. The instrument is an average over models, not a selector with local stopping.

### 6.2 BOS and partition of the counts

For each training target visit the root and the available history in reverse order, up to D. If the history ends before D, add a BOS edge leading to a terminal leaf. BOS appears only in contexts and is not predicted. At depth D and below BOS the leaves are forced. In every non-terminal node, for every x:

\[
n_s(x)=\sum_{c\in children(s)}n_{sc}(x).
\]

BOS collects precisely the initial observations: root and children are not trained on inconsistent populations. Each sentence/fragment resets the history. No link between sentences, parts or documents; no SEP in the new scientific API.

### 6.3 Integrated evidence and mixture

\[
E_s=\frac{\Gamma(ma)}{\Gamma(N_s+ma)}\prod_{x\in A}\frac{\Gamma(n_s(x)+a)}{\Gamma(a)}.
\]

In forced leaves W_s=E_s; elsewhere:

\[
W_s=\rho E_s+(1-\rho)\prod_c W_{sc},\quad
w_s^{stop}=\frac{\rho E_s}{W_s},\quad
w_s^{split}=\frac{(1-\rho)\prod_cW_{sc}}{W_s}.
\]

An empty subtree has E=W=1; omitting its unit factors removes no mass. The recursion is equivalent to the sum of the evidences of the admitted trees, weighted by the stop/split prior. The evidence does not require a random order of the streams. The stream and BOS conventions are an explicit HEXIS adaptation; theorems on stationary sources are not transferred without proof to the composite corpus. The methodological foundation is CTW/BCT; see the source and the delimitation of use in §18.

### 6.4 Frozen prediction and root

With counts and weights fixed on the training alone, following the next edge c of the history h:

\[
q_s(x\mid h)=w_s^{stop}p_s(x)+w_s^{split}q_{sc}(x\mid h).
\]

On a forced leaf q_s=p_s; entering a never-observed subtree q=1/m. At the root one obtains q_CTW. The root comparison uses the same global counts and a:

\[
q_0(x)=\frac{n_\varnothing(x)+a}{N_\varnothing+ma}.
\]

During the whole evaluation **counts, evidences or weights** do not change. The history advances with the preceding test symbols, without reading the following ones for the prediction. The product of the conditional probabilities is a normalized predictive code; it is not the joint evidence of the test with a posterior updated online. The prequential/integrated identity is verified on the training with **pre-update** counts, without authorizing updates on the test.

### 6.5 Numerics and saturation diagnostics

Evidences in natural logarithms (`lgamma`, stable sums, `logaddexp` or equivalent); final losses in **log base 2**. Use float64, counts without overflow, finite positive and normalized probabilities. Keep `log_rho` and `log_one_minus_rho` separate.

In non-forced nodes define u=logρ+logE and v=log(1−ρ)+ΣlogW_children. With δ=u−v:

\[
\log w^{stop}=-\operatorname{logaddexp}(0,-\delta),\qquad
\log w^{split}=-\operatorname{logaddexp}(0,\delta).
\]

Derive both weights from these quantities; do not obtain the small weight only as `1-stop`. In forced nodes stop=1 and split=0 are mathematically prescribed. In the others, finite evidences and an interior prior give two positive weights in exact arithmetic; a float64 0/1 can be numerical saturation, not a discrete selection.

Record **`root_stop`** and **`delta_root=u_root−v_root` in nats**: positive favours stopping, negative splitting. For D=0, delta_root is null with reason `forced_leaf`, root_stop=1. About 37 nats concerns the loss of a small component added to 1, not the underflow of `log1p(exp(-37))`; the float64 exponential goes to zero towards −745/−746. The subtraction of large log-evidences can introduce further loss of precision.

Do not build the extreme prior as `1-2**(-(m-1))` in float; keep its two log-contributions. The case m=106 remains a historical numerical test. No indiscriminate clipping: if a rounding deviation is corrected, verify it and limit it to ≤10⁻¹² without hiding errors.

Tolerances: probability/normalization in the small tests 10⁻¹² absolute; enumeration log-evidences 10⁻¹⁰; CE reconstruction on large outputs 10⁻⁹ bits/symbol; reproduction across platforms 10⁻⁸. Identities, counts, coordinates and keys coincide exactly. No test requires G_R=0 or D8=D12.

## 7. Paired order control

For each pair `(cell, fold, seed)`:

1. Build the training sample only once.
2. Prepare the original arm O and the shuffled arm R.
3. In R permute uniformly **the whole composite symbol** within each sampled sentence/fragment, after sampling. Do not separate UPOS and DEPREL.
4. Fit an R model with its own evidences and weights, on the shuffled training.
5. Shuffle independently each sentence of the test block with `shuffle_eval` and evaluate it under R; evaluate the original under O.
6. Pair by identity of the eligible **slot**; the provenance of the moved token is a different field. Verify the one-to-one correspondence before aggregating.

One permutation per seed is used: twenty in C0, ten in each sensitivity. Do not repeat until obtaining a change or a welcome sign. Record the share of slots with a different symbol, with an explicit denominator; constant sentences can remain identical. Sampling and shuffling contribute jointly to the computational variability, without a decomposition of the variances.

The shuffle preserves length and multiset of every sentence/fragment and **the root counts of the training**. It does not preserve n-grams, grammaticality or syntactic dependencies. Permutation without replacement induces dependencies from finite composition: the control is neither i.i.d. nor a universal estimate of the bias.

Root O and root R are equal as training distributions, but **their CE on the eligible test can differ**: the shuffle moves symbols across the boundary of the first four slots. The four terms of Q are always needed. The archived counterexample gives Q≈0.71346 and shortcut `CE_CTW_R−CE_CTW_O`≈−0.66505: it can even change the sign.

G_R null at the recorded precision in some pilots is an observed result, not a general identity. A synthetic i.i.d. control of the package had root_stop≈0.80775 and G≈0.000195. The **490 final shuffled identities** remain mandatory even if they look redundant after a pilot.

## 8. Scores, aggregations and R1

### 8.1 Definitions

Let I_b be the set of eligible slots of block b in the variant and n_b=|I_b|. For seed s and arm z∈{O,R}:

\[
CE_{CTW,b,s}^{z}=\frac{1}{n_b}\sum_{i\in I_b}-\log_2q_{CTW,s}^{z}(x_i^z\mid h_i^z),
\qquad CE_{0,b,s}^{z}=\frac{1}{n_b}\sum_{i\in I_b}-\log_2q_{0,s}^{z}(x_i^z),
\]

\[
G_{b,s}^{z}=CE_{0,b,s}^{z}-CE_{CTW,b,s}^{z},\qquad
Q_{b,s}=G_{b,s}^{O}-G_{b,s}^{R}.
\]

The cell is implicit in the indices. The same definitions hold for document and history band, with their own denominator. G and Q can be negative: do not truncate them. Q quantifies the additional advantage of the context with original order with respect to the fixed transformation, not a linguistic effect purged of annotation and training.

### 8.2 Profiles and two subordinate summaries

Within document and block **sum the losses and divide by the targets**, without an unweighted mean of document means. The seven block profiles and the eleven documents are the first result of the report. For each seed, the equal-weight summary across blocks is:

\[
D_{Q,s}^{equal}=\frac12\sum_{b\in HEX}Q_{b,s}-\frac15\sum_{b\in PROSE\_ALL}Q_{b,s}.
\]

The mandatory summary by eligible targets is:

\[
D_{Q,s}^{target}=\frac{\sum_{b\in HEX}n_bQ_{b,s}}{\sum_{b\in HEX}n_b}
-\frac{\sum_{b\in PROSE\_ALL}n_bQ_{b,s}}{\sum_{b\in PROSE\_ALL}n_b}.
\]

For both also compute the group means of the four CE, G_O and G_R and verify `D_Q = D_G_O − D_G_R`. The weights are eligible targets of the variant, never raw tokens, total retained tokens or q. The two weightings are reported in all six cells, side by side. In C0 the Hesiodic block goes from 50% of the HEX side to 6,375/53,009≈12.0263%.

The two summaries describe respectively the average block and the average target in the groups. Neither corrects the other inferentially; do not choose the weighting with greater separation. The trainings differ across folds: the contrast describes this leave-one-block-out procedure, not seven texts under a common model.

First aggregate per seed, then report the arithmetic mean, SD with denominator S−1, minimum and maximum across seeds and the effective S. Do not average document SDs or extremes to produce those of block/group. No unlabelled “±”. The final summaries between groups are produced only by the complete report (§14).

### 8.3 R1: JSD without inference

For each of the three updated representations use all the **complete retained original tokens** of the seven blocks, including initial ones. Keep unsmoothed counts and frequencies; define:

\[
r_b(x)=\frac{n_b^{all}(x)+0.5}{N_b^{all}+0.5m}.
\]

They are distributions of the complete block, not roots of the leave-one-block-out trainings. For u=(p+q)/2:

\[
JSD(p,q)=\frac12\sum_xp(x)\log_2\frac{p(x)}{u(x)}
+\frac12\sum_xq(x)\log_2\frac{q(x)}{u(x)}.
\]

Produce **21 pairs and a 7×7 matrix** per variant, zero diagonal, symmetry and range [0,1] bits. Define centroids r_HEX as the uniform mean of the two r_b and r_PROSE as the uniform mean of the five r_b, then their JSD. Do not replace it with the mean of the pair JSDs. Keep all per-symbol contributions and verify their sum.

Handle `0 log 0 = 0`; the JSD does not require strictly positive inputs even though here they are smoothed. Do not call the divergence a metric distance. Do not add clustering, tests, target-weighted centroids, JSD of targets only or of the non-evaluated documents. R1 neither corrects nor validates Q: it describes a different, explicitly chosen population. It requires neither CTW nor seeds. [Lin, 1991](https://www.cise.ufl.edu/~anand/sp06/jensen-shannon.pdf).

## 9. Diagnostics and semantics

### 9.1 Model support

Per model: observed nodes per structural depth, supports in classes **1, 2–4, 5–9, ≥10**, number of observed and unobserved outcomes at the root, root_stop and delta_root, fit/evaluation times and peak RSS. Support class **0** concerns implicit subtrees: record evaluation encounters, without enumerating an exponential tree or adding them to the materialized nodes.

Per arm and evaluated population: number and share of targets whose symbol was not observed at the root, mass routed to the first unobserved subtree, distribution of the weights by context length and counts of the history bands. The denominators accompany the shares.

### 9.2 Mixture weights and L_resolved

For a history, λ_s is the product of the continuation weights before s times the stopping weight in s. λ_s is collected only in nodes with at least one training observation; the remaining mass at the first never-observed branch is `unseen_mass`. The observed masses and unseen_mass sum to 1 within tolerance. A node with a single observation is observed, without a guarantee of precision.

`lexical_context_length(s)` counts the ordinary edges in the context; BOS does not count. Keep the observed masses per length ℓ=0,…,D. If R is their direct sum:

\[
L_{resolved}=\frac{\sum_{s\ osservati}\lambda_s\,lexical\_context\_length(s)}{R}.
\]

*[Translator's note: in the formula, kept as in the original, `osservati` means "observed".]*

Compute R as a direct sum, not as `1-unseen_mass`. With empty training, even if D=0, the prediction is uniform, unseen_mass=1, R=0 and L_resolved is **null** with reason `no_resolved_mass`. In non-empty forced-leaf nodes all the mass reached stops.

L_resolved describes the **observed lengths to which the mixture assigns weight**, conditional on the observed mass; it does not measure reliability, grammatical depth or maximum recoverable order. λ_s is not the responsibility of the component for the symbol actually seen, which would also depend on p_s(x). Do not add that new diagnostic. The old `weighted_depth` remains a historical field; do not rename its values as L_resolved 3.1.

### 9.3 Explicit aggregation

For each document, seed, cell, arm and band keep the **sum of the valid L_resolved and their number**, the number of nulls, the sums of unseen_mass and of the masses by length, and the counts of the targets unseen at the root. The block L_resolved mean is the sum of the valid per-position values divided by the valid number; if n>0 and the valid number is zero, the mean is null with reason `no_resolved_mass`. **Do not** replace it with the ratio of aggregated mass moments: it is a different quantity. `mean_unseen=sum_unseen/n` and `mean_mass[ℓ]=sum_mass[ℓ]/n` use all targets, not only those with a valid L_resolved.

The bands 4–7 and ≥8 have n and all the components of Q. If a band is empty, n=0, additive sums=0 and CE/G/Q/means=null with reason `empty_bucket`; no false zero score. The counts of the histograms and the supports needed by the figures must be collected during the evaluation. Do not select contexts or new bands a posteriori to support the result.

## 10. Six cells and definitive budget

| Cell | Variant | m | D | a per symbol | ρ | q per contributor | Seeds | O+R models |
|---|---|---:|---:|---:|---:|---:|---|---:|
| **C0** | ud23 | **100** | 8 | 0.5 | 0.5 | 8,884 | 0–19 | **280** |
| a_total1 | ud23 | 100 | 8 | **0.01** | 0.5 | 8,884 | 0–9 | 140 |
| q_half | ud23 | 100 | 8 | 0.5 | 0.5 | **4,442** | 0–9 | 140 |
| D12 | ud23 | 100 | **12** | 0.5 | 0.5 | 8,884 | 0–9 | 140 |
| oth | ud23_oth | **105** | 8 | 0.5 | 0.5 | 8,884 | 0–9 | 140 |
| upos | upos_only | **11** | 8 | 0.5 | 0.5 | 8,884 | 0–9 | 140 |
| **Total** | **6 cells / 490 pairs** | | | | | | | **980** |

All cells use reset and two arms. No factorial combination. `a_total1` means total Dirichlet mass 1; the contract stores **a per symbol=0.01**, without the earlier ambiguous field a=1 associated with a mode.

The sensitivities compare ten seeds with **the same first ten C0 seeds**, through paired differences per block/seed and for both subordinate summaries. Do not subtract the twenty-seed C0 mean and call the comparison paired. Differences between variants are task differences; OTH also changes targets. Lower CE in UPOS, similar G or concordant contrasts give neither a universal scale nor a decomposition of the DEPREL contribution.

D6, `rho09`, `bound` and all tragic evaluations are retired. The renunciations are explicit: no final sensitivity to the stop/split prior, no evaluation of boundary crossing, no specificity with respect to other metres. `a_total1` perturbs **another** prior. D12 checks only the increase of the maximum depth. These cuts limit the questions; they are not motivated by the similarity of the results in the pilot.

No sign-stability is a completion condition. Inversions and instabilities are reported, without changing cells, weights or seeds. Reusing counts for prior/D is an optional optimization, after verified equivalence: it requires new evidences/weights and correct leaves. Truncating a D12 while keeping its weights does not produce a D8. The scientific identities remain 980; no general cache system is needed.

## 11. Software contracts and persistence

### 11.1 Responsibilities and API

| Component | Contract |
|---|---|
| Reader/census | Three exact inputs, identity/order/coordinates, localized errors on duplicates or missing metadata |
| Encoder | Masks, merging, frozen inventories and causes of removal |
| Sampler | Blocks identified by their members, q, held-out and seed → ledger/stream; no group label |
| CTW fit | Stream of integers, m,D,a and log-prior → frozen model and fingerprint |
| CTW predict_proba | History → normalized vector over A; no mutation |
| Score/pairing | Same slots → four losses and diagnostics; label-free core |
| Annotation | Registry and scores → names/groups; the only stage that introduces the regime into the aggregations |
| R1 | Complete original counts → distributions, JSD and contributions |
| Report | Verified artifacts → the same aggregations for tables and five figures |

Keep the label-free name/contract of `pooled_score_core` where relevant and the introduction of labels through `annotate_scores`. The invariance must become an executable behavioural test, beyond the signature check.

Strict schema: reject unknown/missing keys, YAML duplicates, retired parameters, NaN/Inf, bools as integers, silently converted floats, non-integer m or m<2, symbols outside [0,m), negative D, q≤0, a≤0, non-interior prior, duplicate seeds/cells and inconsistent block members. D=0 and empty training are valid cases of the core, not real cells. BOS is internal; no negative ID in a public stream. Reuse the safe YAML and the already working checks of `config.py`, completing its schema.

### 11.2 Audit, coordinates and ledger

`documents.csv`: document records per variant with doc_id, prefixes/parts, work, attribution, epoch, regime, role, block, raw/sentences, kept/eligible, retention and flags. Removed source data with cause/coordinates in a dedicated table or a reconstructible equivalent. No raw data is redistributed in the kit of the plan.

`coordinates.parquet`: per retained token, `variant, slot_uid, doc_id, sent_id, source_prefix, part_order, source_ordinal, source_rank, raw_token_id, encoded_index, symbol_id, available_past, eligible`. The eligibility of the inventory_only documents is potential, for the census; the role forbids their scoring. `slot_uid` is a stable integer in the canonical order of the variant; the complete key includes the variant. Textual identities in shared dictionaries, without duplicating long strings in the vectors.

Source ordering: prefix identified by the `sent_id`, final numeric ordinal and rank among all sentences of that prefix; validate uniqueness and syntax. Do not use the train/dev/test order to recompose the text. Per document, sort by part and ordinal. The canonical order of the coordinates follows `(doc_id, part_order, source_ordinal, sent_id, encoded_index)`.

`sample_ledger.json`: per distinct sample, contributing blocks, q, coordinates/fragments/subseeds and hash. The cells that reuse it cite its hash. Keep the transformations, or the data needed to regenerate them exactly from the RNG contract and the ledger.

### 11.3 Identification of the run

`run_id = SHA256(canonical JSON of the run_contract)`. The contract comprises the version of the plan/representation, the hash of the deposited analytical contract, scientific code, data, registry, alphabets, configuration, lock and RNG version. Timestamps, machine, paths and times are external metadata, excluded from run_id and seeds.

For the final campaign require **clean tracked code and no scientific producer depending on untracked files**. Do not delete ignored raw files or unrelated local scripts to obtain that requirement. The deposit commit and the implementation commit are different fields: do not insert into the file just committed the hash of its own commit, creating a circular dependency. The deposit act is referenced by the subsequent external manifest.

Model key: `(run_id, cell, held_block_key, seed, arm)`. Pair key: the same without arm. No probe evaluation identity. A fingerprint of the model attests the computed content, without replacing independent tests.

### 11.4 Positions in C0 only

C0 persistence: **2,182,160 paired rows** (109,108 slots × 20 seeds), divided into the 140 pairs. Minimum fields:

```text
slot_uid, original_symbol_id, shuffled_symbol_id, shuffled_origin_slot_uid,
loss_ctw_original, loss_root_original, loss_ctw_shuffled, loss_root_shuffled,
unseen_mass_original, unseen_mass_shuffled,
resolved_mean_original, resolved_mean_shuffled
```

The four losses and the diagnostics are float64; L_resolved nullable with reason. Metadata: run_id, cell, fold, seed, variant, hashes of the two models and of the ledger. The coordinate dictionary makes slots and provenance recoverable. The four losses are always kept: no constant columns imposed by the historical collapse.

Do not persist the complete trees of every fit: fingerprint, sample and parameters allow regeneration. Sequential default, one pair in memory and writing per partition; then free the models.

### 11.5 Aggregated sensitivities, diagnostics and reconstruction

For each document/seed/cell/band keep **n and four unrounded sums of the losses**, one paired row with keys and hashes. The two bands are disjoint rows; the total is obtained by summing, without treating it as a third population. For each arm also keep the summaries of §9.3, the histograms by length and the counts of the shuffle. The supports belong to the model; they are not multiplied by the documents in the fit summary.

Before discarding the vectors of the sensitivities verify uniqueness and **equality of the set of slots** of the arms, of the coordinates and of the expected denominators. Their equal length is not enough. Blocks and groups are reconstructed from sums/denominators; mean and SD over seeds only after that reconstruction.

For C0 fully reconstruct losses, CE/G/Q and sums/means of L_resolved and unseen_mass from the persisted vectors. The mass histograms, the supports of the model and the counts of the symbols unseen at the root are verified from the collected summaries and from the prescribed regeneration: they are not all derivable from the positional columns listed. For the sensitivities verify schema, key sets, additivity, denominators and diagnostics from the aggregates; verify the positional computation through deterministic regeneration of **predetermined** cases (§12). The sums alone do not allow reconstructing every vector or uncollected histograms: a later check of a single loss requires redoing the case from the ledger. The hashes guarantee identity of the bytes, not mathematical correctness.

Tables of the report, derived from a single aggregation implementation:

- `document_scores.csv`, `block_pairs.csv`: all CE, G, Q, denominators and bands, with document and block detail.
- `aggregation_weights.csv`, `contrasts.csv`: group means and contrasts with `aggregation=equal_block|eligible_token_weighted`; training shares next to the results.
- `seed_summaries.csv`, `sensitivity_pairs.csv`: mean/SD/min/max/S and differences on the same first ten C0 seeds.
- `model_diagnostics.csv` and associated histograms: supports, masses, nulls, unseen targets, root_stop/delta_root, resources; ledger with the diagnostics of the fragments.
- `root_distributions.csv`, `jsd_pairs.csv`, `jsd_centroids.csv`, `jsd_contributions.csv`: complete R1.

Do not create a second band table with independent aggregation logic: the bands are a dimension of the scores and of the existing panels.

### 11.6 Five figures

1. **Corpus/annotation:** quantities, retention and discontinuity per document; primary and inventory-only roles visible.
2. **Profiles:** seven blocks G_O/G_R/Q and eleven document details; points per seed and mean, any bars explicitly computational min–max.
3. **Sensitivities and weights:** C0 and five perturbations, paired comparisons on the first ten seeds, two subordinate weightings side by side; bands in the existing panels.
4. **R1:** C0 7×7 matrix, JSD of the centroids in the three representations and contributions; complete data without selection of favourable contributions.
5. **Supports and masses:** supports of the nodes, masses by length, unseen_mass and L_resolved with the semantics of §9.

All derive from the verified tables. No tragic figure, per chunk, lexicon of contexts, network of reference models or learning curve. No inferential CI.

### 11.7 Manifest, writing and resumption

A single manifest per run contains the identity of contract/data/registry/alphabets/code/lock, RNG version, keys of the executions, results of the checks and references to their evidence, exact list of the artifacts with hash, size, schema and cardinality. No separate certificates, signatures or nested attestations are needed.

Write to a temporary file in the destination directory, verify, rename atomically; the same protection for updating the manifest. A temporary file does not count as complete output. No silent overwriting: collisions fail; any `--force` must be explicit and not mix versions. A complete run keeps its results immutable.

`--resume` reuses a partition only if identity, bytes/hash, schema, cardinality and keys coincide. Do not reuse output of different code/contracts. An empty band gives null with reasons; a primary block without targets, an impossible budget, a non-finite model, a missing pair or unforeseen parameters stop the cell and block the report. No problematic seed or block is excluded automatically. The individual outputs remain available for diagnosis, without the final state COMPLETE.

## 12. Acceptance: tests before implementations

Bring the relevant tests before the new code; do not weaken a still valid property. The historical scripts are isolated references/fixtures and not production dependencies; no import from `candidates/`. A green v2.1 suite does not certify v3.1. The active checks cannot be skips or placeholders.

| ID | Mandatory property of the 3.1 target |
|---|---|
| T01 | Three exact names/hashes, unique sent_ids; 18 prefixes → 17 documents |
| T02 | 202,989 tokens / 13,919 sentences and all expected document/block counts |
| T03 | Parsing and coordinates; UPOS/DEPREL/subtypes, multiword/empty, precise errors on malformed input |
| T04 | Global merging; m=100/105/11; lexicographic IDs; UPOS same mask/coordinates as C0; 9/10/0 exclusive inventory_only types |
| T05 | Exclusion of every held-out member and of every inventory_only from the training |
| T06 | Exact q, no replacement, ≤1 fragment/contributor, empty sentences and impossible budgets |
| T07 | Invariance to the order of records/labels; declared ledger reuse; no dependency on groups in the core |
| T08 | Known RNG vector, separation of purposes, repeatability and pairing; no active shuffle_probe |
| T09 | Exact partition by outcome, terminal BOS, reset; no SEP/# as outcome or link |
| T10 | Independent enumeration of small trees against evidence and prediction, at the tolerances of §6.5 |
| T11 | Normalization, rare/unknown support, empty training, D=0; m100/105/11 parametrized; strict inputs |
| T12 | Prequential/integrated identity of the training with pre-update; invariance to the order of the streams |
| T13 | Counts/evidences/weights/fingerprint unchanged before and after every evaluation |
| T14 | Extreme priors in log, two stable weights, saturation distinct from forced leaves |
| T15 | All 25 small synthetics at the thresholds of §12.1; violations cause a non-zero exit |
| T16 | Historical m106 stress: execution, normalization, supports and declared gap from the oracle |
| T17 | Shuffle preserves multiset/root, slots and mask; provenance distinct from the slot |
| T18 | Predetermined counterexamples of heterogeneity and internal dependency; no universal assumption G_R=0 |
| T19 | Four-term Q and counterexample of sign inversion of the shortcut |
| T20 | Losses→documents→blocks→groups; two weightings and four components with fixtures of unequal lengths |
| T21 | Sensitivities on the first ten C0 seeds; OTH changes population; exact joins and mismatches detected |
| T22 | Masses/supports/L_resolved, valid_count/null_count, empty bands, correct per-position mean |
| T23 | R1: symmetry, diagonal, range, zeros, centroids and sum of contributions with independent fixtures |
| T24 | Six inventory_only in the census and included only in the inventory: zero training and zero final scoring |
| T25 | Equality of the expected sets of 490 pairs / 980 models, complete cells/seeds/arms |
| T26 | Atomic/interrupted writing, resume, corruption, duplicates and extra keys rejected |
| T27 | C0: CE/G/Q and L/unseen from the vectors; other diagnostics from the summaries and the regeneration; sensitivities from aggregates plus regeneration; five derived figures |
| T28 | No import of candidates or inferential utilities in the pipeline; no skip in the active tests |
| T29 | Reproducibility of exact identities and CE within tolerances; state of the code and lock verified |
| T30 | No incomplete final contrast/report: check of bytes, contract, key sets, R1 and denominators, without autonomous certificates |

The generic cases concerning preserved statistical utilities remain valid. Retiring a requirement of the selector or of the probes means replacing its test with a reason, not adding a skip or deleting generic checks. In particular T24 verifies the absence of scoring of the six documents.

### 12.1 Frozen synthetic battery

Reuse exactly the algorithms, seeds and oracles of `ctw_validation/verify_synthetic.py` inside `verifiche_CTW_precedenti.zip` of the package identified in §0. Do not reconstruct the generator from memory. Training **53,304**, independent test **100,000**, exclusion of the first four slots; five seeds for the five small sources.

| Source | Rule | Criterion for each case |
|---|---|---|
| Uniform m=4 | i.i.d. equiprobable | \|CE−2\|≤0.02 |
| Cycle m=3 | Deterministic periodic | **CE<0.02** |
| Binary Markov 1 | P(same)=0.8 | \|CE−h₂(0.2)\|≤0.03; reference 0.721928… |
| Binary lag 2 | P(copy at distance 2)=0.9 | \|CE−h₂(0.1)\|≤0.03; reference 0.468996… |
| Variable memory | Contexts 1/2, archive generator | Deviation from the oracle of the realization ≤0.03 |

Training seeds 0–4, test 10000+seed; each sequence is a single stream; CTW D8/a0.5/ρ0.5. In the historical variable-memory generator, P(x_i=1)=0.2 if x_(i−1)=0, otherwise 0.1 if x_(i−2)=0, otherwise 0.9. Keep the order of the RNG calls and the initialization of the identified file. **Its realized oracle uses i=2,…,N−1 and denominator N−2; the scoring uses i=4,…,N−1 and N−4.** This verified fixture is explicitly kept, without describing the denominators as identical or silently redefining the oracle.

Thresholds and seeds are not changed after the results. A JSON `analytic_pass=false` followed by exit 0 does not pass the gate. Keep the known lag-2 comparison recovered with respect to the reference of about 1 bit of the historical local selector, without reintroducing it in the Greek results.

**Historical m=106** stress, three seeds for uniform, lag 2 with copy 0.9/uniform innovation 0.1 and a binary core with rare symbols. In lag 2 the coincidence is 0.9+0.1/106, oracle about 1.13109 bits. Counts, normalization, execution and recording of the deficit are required, not reaching the oracle. No further calibration campaign for the new alphabets: m100/105/11 are covered by the parametrized checks of input/normalization/support.

The heterogeneity and shuffle synthetics keep the archived fixtures; the thresholds in those cases do not calibrate a test on Greek. The counterexample of depth beyond D8 only shows that D12 can differ, not a universal detectability threshold.

### 12.2 RNG fixture and predetermined reproduction

Known artificial vector: held members `['held']`, contributor `['fixture']`; block_key respectively `e7b28f6b342cb9fe4fe171f6f02275c1de5349f73462a8709b4e0679a332ab99` and `b074a6afd500bbf0891340a1cdda223c1516d7bb52518b820848e1d29d12788a`. With master 20260706, seed 0, purpose sample, empty sid and bounds 0/0, derived seed **218577625307806857638750380866922209360** and `permutation(6)=[0,4,3,2,1,5]`.

Sentence fixture `fixture@1`…`fixture@6`, lengths `[5,8,0,2,7,6]`, q=17: expected ledger `@1[0,5), @5[0,7), @4[0,2), @2[3,6)`; only the last one is a fragment. The fragment subseed of @2 is **46436027119566646866315332695474949224**. The historical script of the contract contains other real activities: extract the fixture from it, do not launch it just to verify the seed.

For T27/T29 fix **before the campaign** the regeneration of seed 0 of all seven folds in all six cells (42 pairs / 84 models), in a distinct directory, comparing them with the partitions of the campaign. It is a reproduction check of the already planned integrated trial, not new scientific identities or new seeds. For the sensitivities also compare the regenerated aggregates and diagnostics; check the slots in memory. Also test a resumption with simulated interruption/corruption on persistence fixtures. No case chosen for its score.

## 13. Normative and technical migration

### 13.1 V3-001: single act to be deposited

In the implementation assignment create a `codex/…` branch from the verified revision or from an evolution of it reviewed first; preserve history and local files. The namespace **V3-001** does not collide with D55. The act shall contain these points, without residual methodological alternatives:

1. Adopt **HEXIS 3.1** and the contract delivered here for the new executions; explicitly replace the v2.1 operational design and plan 3.0.1.
2. Adopt together the finite/within-sentence Greek scope, registry, merging, frozen CTW, Q, hierarchy of profiles, two weightings, R1, six cells, outputs and the V0–V5 checklist.
3. Declare **not applicable to 3.1**, without treating them as resolved in v2.1: confirmatory P1/P2, Latin/L1, O7/sign-flip, permutation constants, the 13 v2.1 cells, sign-stability and gates G0–G7. Do not silently replace the disputed constants of D55.
4. Keep D01–D54, proposed D55, G1 technical ratifications, old plans and reviews as history with a clear status. The G1 technical ratifications do not retroactively ratify the corpus or this analysis.
5. Keep immutability/provenance of the raw files, label-free core, quarantine of `candidates/`, determinism, safe writes and effective tests.
6. Record the pilots already observed and the authorizations **with source and degree of verifiability** (§2). The session account does not become an independent verification of consent nor a retroactive passing of G2. Distinguish the dates of the activities, of the documented consent and of the Git deposit; do not invent times.

Update in the same normative step: `docs/01_MASTER_SPEC.md`, `docs/02_DECISION_LOG.md`, `docs/03_ROADMAP_OPERATIVA_IT.md` and the bibliographic registry, `docs/00_LEGGIMI_INDICE.md`, `docs/HANDOFF.md`, `docs/04_AI_HANDOFF_PROMPT.md`, `AGENTS.md`, `CLAUDE.md`, configuration, registry, test inventory and package metadata. README and proposal must immediately take on the new perimeter and the actual status; the operational availability of the commands is attested after implementation and tests.

Deposit the bytes of the contracts and of the plan with the external digests of `design_lock.json`. The status of the delivery remains `FINAL_PLAN_NOT_APPLIED`; do not have it surreptitiously accepted by the v2.1 CLI. The record of the V0 deposit is external to the content that identifies the contract. The application configuration shall export an equivalent analytical projection, compared field by field, besides verifying the deposited bytes. Changing corpus, parameters, blocks, transformations, targets, seeds, weights or mandatory results requires a version and a motivated decision; recomputing a hash is not enough.

### 13.2 Concrete map of the work

| Path / area | Intervention |
|---|---|
| `src/hexis/conllu_reader.py` | Reuse parsing and validations; preserve the necessary raw IDs, identities, order and coordinates |
| `src/hexis/registry.py` | Complete registry/parts/roles/blocks; consume `part_order`; separate regime from report group |
| `src/hexis/alphabet.py` | Global merging, errors on unknowns, lexicographic IDs and freeze; document audit |
| `src/hexis/sequences.py` | Sentence/fragment streams with reset and coordinates; retire concatenation and predicted `#`, no SEP |
| `src/hexis/config.py` | Keep safe YAML and the rejection of duplicates/keys; new strict schema and SHA-256 derivation |
| `src/hexis/model/context_tree.py` | Canonical CTW in place of the stub; numerics and frozen API; isolated reference only in the tests |
| `src/hexis/model/diagnostics.py` | Supports and mixture weights, L_resolved/null; no selected depth |
| `src/hexis/protocols/sampling.py` | Exact sample, fragments, RNG, ledger and shuffle |
| `src/hexis/protocols/scores.py` | Four losses, paired slots, sums and G/Q; core independent of the groups |
| `src/hexis/manifest.py` | Reuse provenance/hashes; complete run_contract, atomicity, resume and completeness checks |
| `src/hexis/pipeline/run_audit.py` | Keep the working defences; separate identity from the old gates/bilingual methodology |
| `run_encode.py`, `run_tree_validation.py` | Implement the stages before advertising them |
| New `run_descriptive.py`, `run_report.py` | One parametrized executor of the six cells and one reporter with a single aggregation |
| `run_sensitivity.py` | Retire the entry point from the target; cell selection in the same executor |
| `run_confirmatory.py`, `run_null_calibration.py`, `run_reference.py`, `run_latin.py` | Retire CLIs and obligations; no hidden call |
| `model/lexicon.py`, `blocks.py` | Retire lexicon/chunk from the scientific path; chunk ≠ dependency block |
| `stats/permutation.py`, `bootstrap.py`, `holm.py` | Keep working utilities and valid tests as history; no import in the descriptive pipeline |
| `viz/plots.py` | Five figures derived from the validated tables |
| `tests/`, `conftest.py`, pytest markers | New inventory with a kept/replaced/retired map; no skip in the active acceptance |
| `pyproject.toml`, `uv.lock` | Consistent metadata, same stack; no CTW library or unmotivated downgrade |
| `.gitignore`, `LICENSE`, licence documentation | Separate code, documents, raw files, large local outputs and materials intended for publication |
| local `scripts/reacquire_raw_data.sh` | Preserve the original; any corrected and verified canonical version before advertising it |

The verification finds working parsing/audit and statistical utilities, many scientific modules as stubs. `config.py` already rejects unknown/missing keys and some G1 structures: do not rewrite it as if it did not exist. The historical mapping can discard an unknown tag and the alphabet was sorted by frequency: these behaviours must be explicitly replaced. The existing writing does not yet provide all the required atomicity/resumption. The 327 historical passes do not attest a new CTW or an available pipeline; the behavioural test of label-free scores was a skip. No tracked CI workflow exists: do not invent CI attestations or introduce adding one as a requirement of this plan.

### 13.3 Acquisition and local files

The script `scripts/reacquire_raw_data.sh` **exists and is readable, but is not tracked**. It reads provenance from raw, acquires Greek and Latin and iterates over the files present without comparing the set of the three expected ones. The SKIP branch for a missing hash is not verified error handling: `set -euo pipefail` can interrupt earlier. Do not use it today to repair an already verified corpus.

Any version adopted must use provenance tracked outside raw, acquire only the pinned Greek, compare **the set of the three expected CoNLL-U names** and all hashes, fail on missing/extra/missing hash/ambiguous record. The comparison concerns the CoNLL-U files of the Greek source; it does not forbid README or metadata of the clone. Do not automatically alter pre-existing clones. Preserve untracked files and local data without deletions to obtain an apparently clean Git state.

## 14. Execution sequence and completeness

V0–V5 are an **ordered checklist**, not a system of separate certificates. The manifest collects outcomes and references to the checks in the context of the actual code/contract/lock.

| Step | Work | Verifiable output |
|---|---|---|
| **V0 — Contract** | Deposit V3-001, texts, registry, attachments/lock and test inventory | Consistent target contract; old incompatible clauses explicitly historical |
| **V1 — Corpus** | Reading, hashes, identity, merging and coordinates | 17 documents, 11 primary, 6 inventory-only, m100/105/11 and identical counts |
| **V2 — Core/protocol** | CTW, sampling/RNG/shuffle, scores, diagnostics, R1 and persistence | Exact/synthetic tests and relevant checks T01–T23/T26 passed, without skips |
| **V3 — Integration** | One seed (0) for all six cells; resource measurements; freeze of code/environment | **42 pairs / 84 technical models**, finite/consistent, zero probes, final schema verified |
| **V4 — Campaign** | Six cells, all seeds/arms, R1 and outputs | **490 pairs / 980 model identities**, three R1, complete key sets and artifacts |
| **V5 — Delivery** | Report, five figures, resumption and predetermined regeneration | T24–T30 complete; results/limits stated without selection of the sign |

The analytical contract is frozen in V0; V3 freezes implementation and environment. New real fits start only in the integrated trial, after V0–V2 in the new authorized path. V3 verifies integration/resources; it does not select parameters through the contrasts. If the 84 technical models use exactly the final code, contract and schema, they can be reused through resume in the 980. A correction that changes code/run_id requires regeneration under the new identity; results of different versions are not added together.

### 14.1 Target CLI, to be advertised only when implemented

```bash
uv sync --frozen
uv run pytest -q
uv run python -m hexis.pipeline.run_audit --config config/default.yaml
uv run python -m hexis.pipeline.run_encode --config config/default.yaml
uv run python -m hexis.pipeline.run_tree_validation --config config/default.yaml
uv run python -m hexis.pipeline.run_descriptive --config config/default.yaml --cell all
uv run python -m hexis.pipeline.run_report --config config/default.yaml
```

`run_descriptive` accepts `all` or one of the six verified cells; it runs the two arms and produces individual scores/sums. The V3 trial selects only seed 0 as the contract prescribes and remains an incomplete technical trial, not a final campaign with redefined cardinality. `--resume` follows §11.7. R1, summaries and figures use the single report. No separate orchestrator for sensitivities, no additional framework. These are future requirements, not invitations to call absent entry points today or to skip the v2.1 gates.

### 14.2 Report validator

Before emitting contrasts between groups or a final report:

1. Verify bytes/hashes of the deposited contract, plan/lock and analytical projection of the configuration; do not automatically update the expected hashes.
2. Verify the required V0–V3 evidence referred to the code and lock of the run, in the same manifest. A handwritten PASS is not equivalent to the proofs.
3. Generate from the contract the keys `(cell,held_block_key,seed,arm)` and compare by **equality of sets** with the 980 complete identities; detect duplicates before turning the lists into sets. Repeat for the 490 pairs and the expected document/band keys.
4. Verify the exact list of artifacts, bytes/hashes, sizes, schemas, slots, roles and denominators. C0: all expected rows. Sensitivities: both bands per document even if empty, four sums and diagnostic summaries.
5. Compute/verify the three R1, the 21 pairs per variant, centroids and contributions. Reject any inventory_only scoring.
6. Reconstruct losses→documents→blocks→groups and the identities of Q in the two weights; verify the regeneration outcomes prescribed for the definitive V5 delivery.

Absence/corruption of a single cell prevents both final summaries. Individual diagnostic outputs are available; a partial contrast is not written as a definitive result. The complete scientific report is emitted after the V4 checks and, for the final delivery status, V5. The figures derive from the same aggregates, without another implementation of the formulas.

### 14.3 Cardinalities not to be confused

| Quantity | Value and meaning |
|---|---|
| Cells / pairs / models | **6 / 490 / 980** |
| C0 / sensitivity pairs | **140 / 350** |
| Seed-0 technical trial | **42 pairs / 84 models**; reusable only under the definitive identity |
| Probe evaluations | **0** |
| Documents × seeds × cell × arm before the bands | **1,540** logical rows = 11×(20+5×10)×2 |
| Paired aggregates per document and two bands | **440 C0 + 1,100 sensitivities = 1,540** rows; same number, **different schema** from the previous row |
| Persisted C0 positional paired rows | **2,182,160** = 109,108×20 |
| Theoretical positional rows of all six cells | **7,643,640** = 109,108×60 + 109,716×10; not all persisted |
| R1 | **3×21 pairs**, three 7×7 matrices and three centroids/contributions |

The numbers are summary checks; they do not replace the expected keys. The logical rows per arm can be seen as derived from the paired rows, without duplicating storage. An empty band remains a row with n=0 and null with reasons.

## 15. Environment and resources

Python 3.12 via uv; keep the repository lock. The verification of 15 September recorded Python 3.12.13 and NumPy 2.5.1 consistent with the lock; the initial prototypes used Python 3.12.14/NumPy 2.3.5. They are distinct environments. The comparisons of 12 September on seven folds and 42 contributions gave identical hashes between the two NumPy versions on the same host: they do not certify all platforms or the whole pipeline.

The plan adds no dependencies, imposes no downgrade and requires no GPU. `uv sync --frozen` uses the identified lock. A necessary change of dependencies requires a motivation/version and repetition of the relevant checks, not an automatic resolution to make the run pass.

The historical measurements of the prototype — C0 fit about 0.63–0.70 s, held-out evaluation 0.024–0.224 s, C0 RSS about 174 MiB and maximum about 240 MiB for D12 — attest only those trials. Time, RSS and disk of the 3.1 pipeline **are to be measured in V3**; no more precise forecast of days or minutes becomes a requirement.

From 1,400 to 980 scientific models: a **30%** reduction. From 12,704,540 positional rows of the old schema to 2,182,160: an **82.82% reduction of the positional rows alone**. This is not equivalent to a total reduction of time/disk. At 76 bytes/row the C0 numerical payload alone is about **158.2 MiB** before overhead; it is not a Parquet benchmark or a RAM requirement. The old 921 MiB referred to the old schema and do not remain the target requirement.

Write per partition, do not concatenate the whole campaign in memory; keep one pair of models at a time. Insufficient resources require correcting the management or providing adequate capacity, not reducing blocks, seeds or cells a posteriori. The residual cost is mainly integration/tests/report, not new collection or annotation.

## 16. Rules of the conclusions

| Outcome / situation | Admitted interpretation |
|---|---|
| G_O positive, G_R similar | The gain does not clearly distinguish observed order and the chosen control |
| Q positive, small contrast | Relative advantage under this predictor, without strong descriptive separation between the available groups |
| Signs/magnitudes varying by cell or weight | Dependence on the declared choices and on the distribution of the targets; no selection of the preferred result |
| G_R numerically null | Measured behaviour of the control; no collapse theorem or causal attribution of all of G to order |
| D8/D12 similar | No improvement in the evaluated configurations; not absence of dependencies beyond eight symbols |
| C0/UPOS with similar contrasts | Concordance of the summary in two representations; not proof that DEPREL does not contribute |
| Technically correct merging | Mitigation of the documented discontinuity; not demonstrated annotation homogeneity |
| High JSD, similar Q | Marginal differences without a corresponding difference in the measured order advantage |
| Six texts only in the inventory | No final conclusion on specificity with respect to tragedy or other metres |

Next to the profiles and the summaries expose: finite corpus, 2/5 blocks, dominance of the works, chronological/annotation confounding, different training per fold, offline annotations, control conditioned on within-sentence composition, weights and computational nature of the dispersion, and pilots already observed.

Do not add G/CE0, DEPREL-only, label permutations, balanced models or reaggregations without single works to attempt an unsupported attribution. Removing a work only from the mean does not eliminate it from the trainings of the other folds and is not leave-one-document-out. The possible effect of the merging on G/Q is unknown before the campaign: it is a future result, not a suspended methodological decision.

Completion depends on the correctness of the execution, not on the sign, the separation or the confirmation of the pilot. No “absent effect” without defining the quantity and the limits of the measure. No seed SD is turned into uncertainty about the ancient texts.

## 17. README, research proposal and scientific delivery

### 17.1 Before the code: consistent scientific proposal

This plan and its contracts close the decisions to be transferred into the new proposal. The proposal can be written **before the campaign**, declaring implementation in progress and final results absent. It must contain:

1. Title and within-sentence question of §1; circumscribed contribution and relevant precedents.
2. Pinned corpus, 17 inventoried/11 primary/7 blocks, two HEX/five prose and ADV_PART merging.
3. Frozen CTW, training per block, four-term Q, main profiles, two subordinate summaries and R1.
4. Six cells, targets j≥4, computational seeds, no population inference.
5. Earlier pilots described as D_G and Q controls actually covered; limits and completion criteria independent of the outcome.

Do not promise an effect of the metrical constraint, a universal signature, a memory of the grammar, transfer between regimes, Latin results or generalization to Greek. The active bibliography derives from the registry of §18, updated in the same normative act.

### 17.2 README: status first, operations after the tests

The normative realignment of the README must immediately report the 3.1 scope, the real status of the implementation, verified materials, limits and authoritative references. Do not call the existing audit a stub nor describe the still absent CTW as available.

After V2/V3 add only commands actually implemented and verified: installation from the lock, controlled acquisition, audit/encoding, tests, single executor, resume and report. After V5 document reproduction, delivered artifacts and results. No circular dependency between a “final” README and the certification of the software.

### 17.3 Deliverables of the implementation

Repository consistent with 3.1 with commits/lock and tests; registry/alphabets/audit; 980 identities, ledgers and manifest; C0 vectors and sufficient aggregates of the sensitivities; complete R1; five figures and report; resumption/regeneration check; historical archive and reproduction instructions in a new folder.

Raw data, coordinates and per-position symbols remain **local reproduction artifacts** until a subsequent publication act declares their destination, provenance and applicable conditions. Do not automatically attribute the licence of the code to the data or to the derived sequences. The project distinguishes code, documents and source data; raw CC BY-NC-SA 2.5 and existing indications remain tracked, without deciding here the legal qualification of the derivatives. The present delivery publishes no data, does not redistribute raw files and does not modify licences of the repository.

## 18. Active target bibliographic registry

These are the sources directly used, to be adopted into the registry of the project in V0 while keeping the historical one. The citation obligations concerning Latin, transfer and retired estimators do not remain constraints of 3.1 if they have no function in the text. No source external to the registry is implicitly introduced in the proposal.

| ID | Reference and function |
|---|---|
| B01 | **UD Ancient Greek Perseus r2.18**, commit `37837c7a3c592c9563f8c51cc63344b87247f8a5`: actual data, also identified by the three hashes. [Snapshot](https://github.com/UniversalDependencies/UD_Ancient_Greek-Perseus/tree/37837c7a3c592c9563f8c51cc63344b87247f8a5) |
| B02 | **AGDT 2.1**, commit `bf4334f0af5e13d16b04c1cccd6237e683ac6f5f`: inventory/metadata and note on the adverb/particle distinction. It does not replace the UD corpus and does not certify homogeneity. [Description](https://github.com/PerseusDL/treebank_data/blob/bf4334f0af5e13d16b04c1cccd6237e683ac6f5f/v2.1/Greek/README.MD) |
| B03 | **Kontoyiannis, Mertzanis, Panotopoulou, Papageorgiou, Skoularidou (2022)**, *Bayesian Context Trees: Modelling and Exact Inference for Discrete Time Series*, JRSS B **84(4), 1287–1323**, DOI **10.1111/rssb.12511**. Foundation of the CTW/BCT mixture; BOS and freezing of the whole test are HEXIS conventions made explicit here, not attributed in full to the paper. [Publisher](https://academic.oup.com/jrsssb/article/84/4/1287/7073257) |
| B04 | **Galves, Galves, García, Garcia, Leonardi (2012)**, *Context tree selection and linguistic rhythm retrieval from written texts*, Annals of Applied Statistics **6(1), 186–209**, DOI **10.1214/11-AOAS511**. Precedent on context selection and rhythmic encodings of Portuguese, distinct from the CTW evaluation of Greek annotations. [Primary text](https://arxiv.org/abs/0902.3619) |
| B05 | **Vanessa B. Gorman, Robert J. Gorman (2016)**, *Approaching Questions of Text Reuse in Ancient Greek Using Computational Syntactic Stylometry*, Open Linguistics **2, 500–510**, DOI **10.1515/opli-2016-0026**. Syntactic stylometry on tree paths; pages confirmed by the deposit. [Authors' deposit](https://digitalcommons.unl.edu/historyfacpub/208/) |
| B06 | **Schürmann, Grassberger (1996)**, *Entropy estimation of symbol sequences*, Chaos **6, 414–427**; arXiv deposit 2002. Caution on estimation from finite sequences and convergence; it does not identify the empirical gains with mutual information. [Primary text](https://arxiv.org/abs/cond-mat/0203436) |
| B07 | **Jianhua Lin (1991)**, *Divergence Measures Based on the Shannon Entropy*, IEEE Transactions on Information Theory **37(1), 145–151**. Definition and properties of the JSD. [Article](https://www.cise.ufl.edu/~anand/sp06/jensen-shannon.pdf) |
| B08 | **de Marneffe, Manning, Nivre, Zeman (2021)**, *Universal Dependencies*, Computational Linguistics **47(2), 255–308**, DOI **10.1162/coli_a_00402**. Nature of the annotation scheme; it does not certify the quality of each work. [ACL](https://aclanthology.org/2021.cl-2.11/) |
| B09 | **Herrera, Silai, Corro, Guillaume, Kahane (2025)**, *Extraction of Contrastive Rules from Syntactic Treebanks: A Case Study in Romance Languages*, QUASY/SyntaxFest **26–38**, **version 2**. Limits of comparability; no import of their inferential protocol. v1 had four authors: the addition of Caio Corro is a version change, not a retroactive correction of v1. [PDF v2](https://aclanthology.org/2025.quasy-1.5v2.pdf), [metadata/versions](https://aclanthology.org/2025.quasy-1.5/) |
| B10 | **Gianitsos, Bolt, Chaudhuri, Dexter (2019)**, *Stylometric Classification of Ancient Greek Literary Texts by Genre*, Proceedings of the **3rd Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature, 52–60**, DOI **10.18653/v1/W19-2507**. Precedent on Greek prose/verse classification; no absolute priority claimed by HEXIS. [ACL](https://aclanthology.org/W19-2507/) |

The verification reports and the historical JSON files are evidence of the project, distinct from the scientific bibliography. The metadata of B03/B05/B09/B10 were rechecked on the primary sources during this drafting; the other citations keep the verification documented by the consolidated report.

## 19. Final status of the design and closure criteria

The target design is defined: corpus and roles, merging, targets, training, seeds, CTW, Q, weights, R1, diagnostics, six cells, persistence and checks require no new choices guided by the results. The documentary verification and the recount confirm the consistency of the adopted values. **They do not constitute a certification of the future implementation or a guarantee of positive scientific conclusions.**

The residual uncertainties are delimited: size of the new G/Q, complete annotation comparability, share of metrical quotations, point explanations of the historical sensitivities, verifiability of the original authorization and integrated performance. They do not require enlarging corpus, model or analysis: they are declared and, where relevant, measured in the prescribed campaign.

Definitive sequence: **adoption and deposit of the contract → proposal and normative realignment of the README → implementation and verification → operational update of the README → complete campaign, reproduction and report**. The new document is the plan of this work; it does not anticipate its outcomes.

## Appendix A — Complete traceability C01–C30

| Decision of the verification | Adoption in this version |
|---|---|
| C01 | §1: title/within-sentence question, circumscribed promise |
| C02 | §§1.2,8: seven main profiles, eleven details, two subordinate summaries |
| C03 | §§3,11–12: tragedies inventory_only only and inventory over 17 documents |
| C04 | §4.1–4.2: global PART/ADV and annotation limit |
| C05 | §§4,10 and JSON: m100/105/11, updated priors, new inventories/IDs/hashes |
| C06 | §4.3: source audit, exclusions and concrete corrections |
| C07 | §5.1: q/exposure and the Plutarch clarification |
| C08 | §5.2: sample/fragments/ledger kept and explicit limits |
| C09 | §§4.4,9: j≥4 and two secondary bands |
| C10 | §§7–8: shuffle of the two arms, slots and four-term Q |
| C11 | §10: six cells, pairing with the first ten C0 seeds and renunciations |
| C12 | §8.3: original R1 in the three updated representations |
| C13 | §6: frozen CTW, BOS/reset, no active SEP |
| C14 | §9: mixture weights, L_resolved and corrected aggregation/null |
| C15 | §6.5: two weights from log-contributions, delta_root and saturation |
| C16 | §12: 25 cases at the thresholds, historical m106 stress and actual m in the checks |
| C17 | §10: optional verified reuse, always 980 identities |
| C18 | §2: historical Diodorus, no mandatory additional investigation |
| C19 | §§2,13: separation of pilot/campaign/consent and no retroactive G2 |
| C20 | §16: limits of the conclusions, no undue attribution |
| C21 | §18: short registry and corrected metadata/versions |
| C22 | §11.4–11.5: positional C0, sufficient aggregated sensitivities |
| C23 | §§11,14: single executor/report and five figures |
| C24 | §§11.7,14: lock/manifest/validator, without separate certificates |
| C25 | §§10,14.3,15: cardinalities and resources recomputed; new attachments |
| C26 | §§11.3,11.7: identified code, atomicity, resume and no implicit overwrite |
| C27 | §13: map adherent to the code and local acquisition script |
| C28 | §12: T01–T30 updated, no skips and generic properties kept |
| C29 | §13: V3-001 act, version 3.1 and single normative realignment |
| C30 | §§14,17,19: ready design distinct from pipeline and verified results |

## Appendix B — Registry and document counts

The following table is generated from the verified registry and from the attached expectations. The block abbreviations are the full ones of §3.3; for `inventory_only` the block is null. The URNs and the philological flags are kept in full in the JSON of the contract.

| Source prefix | Canonical document | Part | Regime | Role | Block |
|---|---|---:|---|---|---|
| `tlg0012.tlg001.perseus-grc1.tb.xml` | `tlg0012.tlg001.perseus-grc1.tb.xml` | 0 | HEX | primary | HOMERIC_TRADITION |
| `tlg0020.tlg001.perseus-grc1.tb.xml` | `tlg0020.tlg001.perseus-grc1.tb.xml` | 0 | HEX | primary | HESIODIC_TRADITION |
| `tlg0020.tlg002.perseus-grc1.tb.xml` | `tlg0020.tlg002.perseus-grc1.tb.xml` | 0 | HEX | primary | HESIODIC_TRADITION |
| `tlg0020.tlg003.perseus-grc1.tb.xml` | `tlg0020.tlg003.perseus-grc1.tb.xml` | 0 | HEX | primary | HESIODIC_TRADITION |
| `tlg0013.tlg002.perseus-grc1.tb.xml` | `tlg0013.tlg002.perseus-grc1.tb.xml` | 0 | HEX | primary | HOMERIC_TRADITION |
| `tlg0016.tlg001.perseus-grc1.1.tb.xml` | `tlg0016.tlg001.perseus-grc1.1.tb.xml` | 0 | PROSE_CLASS | primary | HERODOTUS |
| `tlg0003.tlg001.perseus-grc1.1.tb.xml` | `tlg0003.tlg001.perseus-grc1.1.tb.xml` | 0 | PROSE_CLASS | primary | THUCYDIDES |
| `tlg0008.tlg001.perseus-grc1.12.tb.xml` | `tlg0008.tlg001.perseus-grc1.tb.xml` | 12 | PROSE_POST | primary | ATHENAEUS |
| `tlg0008.tlg001.perseus-grc1.13.tb.xml` | `tlg0008.tlg001.perseus-grc1.tb.xml` | 13 | PROSE_POST | primary | ATHENAEUS |
| `tlg0060.tlg001.perseus-grc3.11.tb.xml` | `tlg0060.tlg001.perseus-grc3.11.tb.xml` | 0 | PROSE_POST | primary | DIODORUS |
| `tlg0007.tlg004.perseus-grc1.tb.xml` | `tlg0007.tlg004.perseus-grc1.tb.xml` | 0 | PROSE_POST | primary | PLUTARCH |
| `tlg0007.tlg015.perseus-grc1.tb.xml` | `tlg0007.tlg015.perseus-grc1.tb.xml` | 0 | PROSE_POST | primary | PLUTARCH |
| `tlg0011.tlg001.perseus-grc2.tb.xml` | `tlg0011.tlg001.perseus-grc2.tb.xml` | 0 | OTHER_VERSE | inventory_only | — |
| `tlg0011.tlg002.perseus-grc2.tb.xml` | `tlg0011.tlg002.perseus-grc2.tb.xml` | 0 | OTHER_VERSE | inventory_only | — |
| `tlg0011.tlg003.perseus-grc1.tb.xml` | `tlg0011.tlg003.perseus-grc1.tb.xml` | 0 | OTHER_VERSE | inventory_only | — |
| `tlg0011.tlg004.perseus-grc1.tb.xml` | `tlg0011.tlg004.perseus-grc1.tb.xml` | 0 | OTHER_VERSE | inventory_only | — |
| `tlg0011.tlg005.perseus-grc2.tb.xml` | `tlg0011.tlg005.perseus-grc2.tb.xml` | 0 | OTHER_VERSE | inventory_only | — |
| `tlg0085.tlg001.perseus-grc2.tb.xml` | `tlg0085.tlg001.perseus-grc2.tb.xml` | 0 | OTHER_VERSE | inventory_only | — |

| Document | Raw | Sentences | C0/UPOS retained | C0/UPOS eligible | OTH retained | OTH eligible |
|---|---:|---:|---:|---:|---:|---:|
| `tlg0003.tlg001.perseus-grc1.1.tb.xml` | 10396 | 532 | 9346 | 7227 | 9353 | 7234 |
| `tlg0007.tlg004.perseus-grc1.tb.xml` | 5044 | 248 | 4481 | 3493 | 4486 | 3497 |
| `tlg0007.tlg015.perseus-grc1.tb.xml` | 4943 | 251 | 4403 | 3408 | 4407 | 3411 |
| `tlg0008.tlg001.perseus-grc1.tb.xml` | 26245 | 1630 | 23133 | 16691 | 23231 | 16786 |
| `tlg0011.tlg001.perseus-grc2.tb.xml` | 5229 | 431 | 4224 | 2610 | 4302 | 2674 |
| `tlg0011.tlg002.perseus-grc2.tb.xml` | 4299 | 391 | 3573 | 2076 | 3618 | 2115 |
| `tlg0011.tlg003.perseus-grc1.tb.xml` | 5319 | 490 | 4364 | 2503 | 4428 | 2558 |
| `tlg0011.tlg004.perseus-grc1.tb.xml` | 5600 | 520 | 4571 | 2610 | 4648 | 2680 |
| `tlg0011.tlg005.perseus-grc2.tb.xml` | 5239 | 528 | 4259 | 2331 | 4334 | 2389 |
| `tlg0012.tlg001.perseus-grc1.tb.xml` | 79890 | 6003 | 69327 | 45515 | 69770 | 45927 |
| `tlg0013.tlg002.perseus-grc1.tb.xml` | 2061 | 166 | 1761 | 1119 | 1777 | 1135 |
| `tlg0016.tlg001.perseus-grc1.1.tb.xml` | 19575 | 1092 | 17301 | 12946 | 17349 | 12994 |
| `tlg0020.tlg001.perseus-grc1.tb.xml` | 4610 | 273 | 4023 | 2945 | 4034 | 2955 |
| `tlg0020.tlg002.perseus-grc1.tb.xml` | 3725 | 283 | 3189 | 2077 | 3197 | 2084 |
| `tlg0020.tlg003.perseus-grc1.tb.xml` | 2403 | 182 | 2070 | 1353 | 2077 | 1359 |
| `tlg0060.tlg001.perseus-grc3.11.tb.xml` | 16882 | 733 | 15266 | 12334 | 15266 | 12334 |
| `tlg0085.tlg001.perseus-grc2.tb.xml` | 1529 | 166 | 1284 | 639 | 1293 | 646 |

## Appendix C — Status of the verification of the present delivery

The drafting rechecked the hashes of the verification package and of the earlier attachments, redid the census without fitting and verified the merged alphabets. The documentary checks compare the thirty adoptions, text/JSON, keys and cardinalities, digests, local references and absence of old active parameters. The independent checks controlled formulas/diagnostics, the RNG vector and the actual coverage of the pilots. The historical suite and the 25 synthetics remain attestations of the delivered verification; they are not presented as tests just executed on the future canonical code.

No new real fit, modification of the repository or publication of data is part of this delivery. The results of the checks **actually executed** and the hashes of the target files are in the 3.1 kit. The final deposit check verifies that the bytes on the Desktop coincide with those re-examined.
