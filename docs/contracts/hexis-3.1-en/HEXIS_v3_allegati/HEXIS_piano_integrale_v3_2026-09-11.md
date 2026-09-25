> **Non-normative companion translation; the Italian original governs** (V3-003, B2).
> Original: `docs/contracts/hexis-3.1/HEXIS_v3_allegati/HEXIS_piano_integrale_v3_2026-09-11.md` (plan 3.0.1, superseded by plan 3.1), SHA-256 `83fed73f273c0552281a7180b101f944c84577b100c43e5a738d95cb85ebab38`.
> Translated on 2026-09-25. Structure, numbering, tables, formulas, values and identifiers follow the original, including file names, links and code; numbers in the prose use English notation. Any translator's note is marked *[Translator's note: …]* and changes nothing in the original.

# HEXIS 3.0.1 — Complete update plan

**Sequential organization of morphosyntactic annotations in a finite corpus of ancient Greek**  
**Scientific specification, operational protocol and migration plan — initial version 11 September 2026; authorized revision 12 September 2026**

**Status:** plan concluded and delivered; integration into the repository not performed. The feasibility of the CTW core and of the protocol was verified with separate experiments. The definitive results of the study and the passing of the gates of the future implementation are not yet available.

The document defines the decisions to be applied together, without leaving methodological alternatives to be chosen during the execution. The attachments contain structured configuration, document registry, expected counts, executable contracts and results of the additional checks. The Git reference is `g1/pre-audit`, commit `852644b6917790877c7b2ca5df2e76b17829d87c`; the specification does not presuppose that the stubs present are already implemented.

**Necessary package.** This plan must be used together with `HEXIS_allegati_operativi_v3_2026-09-11.zip`, in the version 3.0.1 identified by the README and by the register of the changes. The date in the name indicates the first delivery; the current revision is of 12 September. The earlier `HEXIS_CTW_verifiche_riproducibili_2026-09-11.zip` contains only the earlier CTW proofs and does not replace the normative attachments. The current operational archive also includes an identical copy of this plan, the register of the changes and the hashes: transmitting the whole package to the reviewer is sufficient. The initial version of the attachments is kept in `history/` and is not normative for the revision.

**Perimeter of the revision.** Adopted are: motivation of the fragments, recording of the authorized exception to the earlier freeze, reaggregation by targets, automatic blocks on the emission of the contrasts, omitted references, preservation of the statistical utilities and maintenance of the existing lock. Corpus, CTW, Q, JSD, nine cells and 1,400 fits remain those defined in the initial version. No determined direction of the training asymmetry is assumed.

## 1. Overall decision and reason for the downsizing

HEXIS becomes a **descriptive, reproducible study of a finite corpus**, which compares the predictability of the sequences of UPOS+DEPREL annotations under a variable-memory predictor. The core is a CTW for non-binary outcomes, with probabilistic averaging over the trees and Dirichlet regularization. The main readings are the gain with respect to the root predictor and its variation when the order of the symbols within the sentence is destroyed. The JSD separately describes the differences in the composition of the alphabet.

Of the two original proposals, `piano_ultimato_HEXIS.md` constitutes the better basis for the perimeter: it abandons an inference on the population not supported by the composition of the data. No equal merging is made. From that proposal the finite corpus, the dependency blocks, the balancing of the training and the feasibility are kept; the technical parts superseded by the CTW checks are replaced. The JSD is kept, in accordance with the explicit decision of the person responsible for the project and with the subsequent feasibility verdict.

The old `monotone-stop` selector is retired. The specific motivation is that a delayed dependency can require an order-2 context while offering no improvement at the first level: a local stop can prevent its exploration. The CTW probabilistically compares the alternatives of the whole subtree. The family of variable contexts is not replaced with a fixed-order model and it is not claimed that the CTW eliminates the Markovian character: with a finite maximum depth it remains a finite-memory family.

### 1.1 Final research question

> In the pinned UD Perseus Greek corpus, what predictive advantage does the observed order of the UPOS+DEPREL annotations offer, with respect to the same protocol applied to sequences shuffled within the sentence? How do these scores differ between the blocks of hexameter tradition and the available prose blocks, and how much do they depend on encoding, regularization, budget and boundaries?

The contribution is a documented and controlled comparison of this corpus, not the invention of the CTW, a theory of grammar or the first application of quantitative methods to the prose/verse distinction. Earlier works exist on stylometric classification of ancient Greek, including with syntactic features. [Gianitsos et al., 2019](https://aclanthology.org/W19-2507/).

The positive contribution consists in quantifying the advantage of the order of the annotations with respect to the within-sentence composition, documenting how much context the sample really allows to use and showing the dependence of the results on representation and protocol. This contribution remains informative if the predictive advantage concentrates on short contexts: it requires neither the recovery of a long memory nor a sharp separation between groups.

The closest precedent on the relation between variable contexts and rhythm is Galves et al. (2012): selection of VLMCs on rhythmic encodings of Portuguese texts. HEXIS instead adopts a CTW predictive evaluation of Greek morphosyntactic annotations, under the order control and the finite scope defined here. Gorman and Gorman (2016) are a relevant precedent on the syntactic stylometry of Greek, with features derived from the paths of the dependency trees. These differences delimit the contribution, without claiming an absolute priority. [Galves et al.](https://arxiv.org/pdf/0902.3619), [Gorman and Gorman](https://digitalcommons.unl.edu/historyfacpub/208/).

### 1.2 Admitted results and excluded interpretations

Descriptions of the following type are admitted: «with this encoding and this protocol, the block presents a gain of X bits per symbol; the order control changes it by Y». An arithmetic difference between the means of the two sets of blocks is admitted.

Not identified are: causality of the metre; separate effect of chronology, author or genre; “true” entropy of Greek; mutual information of the language; overall grammatical complexity; cognitive difficulty of reading; absence of dependencies beyond the depth usable by the sample. A small or null result does not demonstrate the absence of linguistic structure.

The symbols are annotations made on the complete text: DEPREL can depend on information later than the word and on its syntactic head. Their prediction is not equivalent to the prediction of the words by a reader. Moreover, the sequence eliminates the hierarchy of the dependencies: it keeps categories and relations, not the complete syntactic tree.

### 1.3 Why the informational measures remain legitimate

Entropy and mutual information are functionals of distributions; sparsity concerns their estimation and the adequacy of the representation and of the model. The criticism of a grammar reduced to local transitions does not make every descriptive probabilistic measure unusable. In HEXIS this confusion is avoided by declaring what is actually measured: an out-of-training predictive loss, under an explicitly delimited predictor. The literature on estimators from finite sequences motivates caution towards automatic equivalences between code length and entropy rate. [Schürmann and Grassberger, 1996; deposit 2002](https://arxiv.org/abs/cond-mat/0203436).

The empirical cross-entropy can be interpreted as an average coding cost under the frozen predictor. The theoretical identity between cross-entropy, entropy and divergence holds under appropriate distributions and expectations; it does not automatically turn an empirical difference between two estimated models into a mutual information.

## 2. Status of the proofs and distinction from preregistration

The earlier checks are reported in `HEXIS_verifica_comparata_2026-09-11.md`, `HEXIS_verdetto_CTW_2026-09-11.md` and in the respective reproducible archives. For this specification checks were added on the contracts of sampling, seeds, shuffling, boundaries and composition of the package.

| Evidence already available | Outcome and scope |
|---|---|
| Repository suite in the first audit | 327 pass, 17 skip; the latter are scaffolds, not verified models |
| Independent CTW enumeration | 120 cases, 9,189 assertions; maximum error 1.07 × 10⁻¹⁴ |
| Prequential/integrated identity on the training | Maximum error 1.42 × 10⁻¹⁴ |
| BOS boundaries and separator | Partition of the counts and normalization verified |
| Earlier synthetic pipeline | 140 fits, seven blocks × 20 seeds |
| Earlier real pilot | 140 C0 fits and 63 sensitivity fits, all completed |
| Earlier order control | Heterogeneous synthetic cases and delayed dependency; seven real folds at the first seed |
| New contract of the plan | Detailed outcomes in `contract_validation.json`; distinct from the definitive scientific results |

In the small synthetic case the CTW recovers a delayed dependency that the monotone selector did not recover. However, with 106 symbols and a delayed dependency spread over the whole alphabet, the pilot presents CE about 5.09–5.13 against a reference of 1.131 bits: the order is representable, but the sample is not enough to estimate it well. With total pseudocount 1 the CE falls to about 3.84–3.90, still far from the reference. This limit remains part of the methodological result.

In the 140 real C0 fits the gain varies between 0.26001 and 0.55301 bits/symbol; these are extremes across blocks and seeds, not a contrast of regime. Going from depth 8 to 12 does not change the CE of the first seed at the recorded precision. About 84–85% of the observed nodes of depth 3 have fewer than five observations. These are evidence of limited statistical support, not a demonstration that Greek has memory 1.

The limited support of the deep contexts is already a result of the pilot, not only a hypothetical risk. It remains distinct from the result of the final analysis. The historical ranges of about 1.00–1.22 in C0 and 1.93–2.13 in UPOS come from the `weighted_depth` diagnostic of the prototype: they must not be renamed “v3 resolved depth”. The new diagnostic of §9 is not retroactively attributed to those numbers.

**Real pilots were observed before this plan.** The document is a prospective protocol for the final analysis after methodological development, not a preregistration preceding every observation. The pilots remain archived, including the unfavourable ones; they are not reused as if they were results of the new sequence of seeds.

## 3. Data, identities and units of the project

### 3.1 Pinned source

Only the three Greek files of UD Ancient Greek Perseus of release `r2.18`, at commit `37837c7a3c592c9563f8c51cc63344b87247f8a5`, are used. The documents are recomposed through `sent_id`; the UD train/dev/test splits have no experimental function.

| File | SHA-256 |
|---|---|
| `grc_perseus-ud-dev.conllu` | `7899f809fc250404839694330b9db25f79a5b1f20cfa12e6dc3a368a4ec7cd22` |
| `grc_perseus-ud-test.conllu` | `e18d47c395c0ec8da678fb5e315ce6d90133e88c25ed2a55bc72a2a66e6254d5` |
| `grc_perseus-ud-train.conllu` | `d7471c9b91bcd975848fa5d9b65c31f1fc48a597ed3667796968a82c6d098a7e` |

Source: [verified UD snapshot](https://github.com/UniversalDependencies/UD_Ancient_Greek-Perseus/tree/37837c7a3c592c9563f8c51cc63344b87247f8a5). The audit must fail if even a single hash changes; updating the corpus requires a new version of the protocol and new results.

### 3.2 Hierarchy of the units

- **Source token:** CoNLL-U line with integer ID; multiword ranges and decimal empty nodes are not additional observations.
- **Source sentence:** uniquely identified by `sent_id`; not redefined by punctuation or verses.
- **Canonical document:** a work or an excerpt defined in the registry; Athenaeus XII and XIII constitute one document with two parts.
- **Dependency block:** unit excluded entirely from the training and unit of weight in the comparison between groups.
- **Seed:** computational replicate of sampling and shuffling, never a scientific replicate.

The blocks limit the evident contamination between associated texts; they do not demonstrate independence among the seven blocks. “Homeric tradition” and “Hesiodic tradition” are conservative conventions of the design, not philological attributions to a single author.

### 3.3 Pinned primary corpus

| Block | Documents/excerpts | Group | C0 tokens | C0 evaluated positions |
|---|---|---|---:|---:|
| HOMERIC_TRADITION | Iliad; Hymn to Demeter | HEX | 71,088 | 46,634 |
| HESIODIC_TRADITION | Theogony; Works and Days; Shield of Heracles | HEX | 9,282 | 6,375 |
| HERODOTUS | Histories, book I | PROSE_ALL | 17,301 | 12,946 |
| THUCYDIDES | Histories, book I | PROSE_ALL | 9,346 | 7,227 |
| ATHENAEUS | Deipnosophistae, books XII–XIII | PROSE_ALL | 23,133 | 16,691 |
| DIODORUS | Bibliotheca historica, book XI | PROSE_ALL | 15,266 | 12,334 |
| PLUTARCH | Lycurgus; Alcibiades | PROSE_ALL | 8,884 | 6,901 |
| **Total** | **11 documents, 7 blocks** | **2 HEX / 5 prose** | **154,300** | **109,108** |

The complete identities, the URNs and the prefixes are in `hexis_v3_design.json`, a normative part of this plan. The corpus contains 18 Greek prefixes, traced back to 17 documents, 11 primary and 6 probes. The original tokens are 202,989, the sentences 13,919. No Greek text present in the three files is excluded from the census.

The verified upstream XML files confirm the bibliographic headers of Theogony, Works and Days, Shield and Diodorus; for the latter the first passage reference is `11.1.1`. The hashes and the point links are in `identita_fonti_verificate.json`. The catalogue of the treebank also confirms the perimeter of the works. [AGDT 2.1, inventory and description of the annotation](https://github.com/PerseusDL/treebank_data/blob/bf4334f0af5e13d16b04c1cccd6237e683ac6f5f/v2.1/Greek/README.MD).

The Shield keeps a label of Hesiodic tradition without asserting authorial authenticity. The Hymn to Demeter keeps the author “Anonymous” and is prudentially associated with the Homeric block. It is not necessary to solve an attribution problem to exclude these texts together from the training. The Iliad makes up about 97.5% of the tokens of the Homeric block: the block results reflect this dominance, which must appear in the report.

### 3.4 Tragic probe

| Document | C0 tokens | Evaluated positions |
|---|---:|---:|
| Sophocles, Trachiniae | 4,224 | 2,610 |
| Sophocles, Antigone | 3,573 | 2,076 |
| Sophocles, Ajax | 4,364 | 2,503 |
| Sophocles, Oedipus Tyrannus | 4,571 | 2,610 |
| Sophocles, Electra | 4,259 | 2,331 |
| Aeschylus, Suppliant Women | 1,284 | 639 |
| **Total** | **22,275** | **12,769** |

They are texts in mixed metres, not a homogeneous category of trimeters. They remain outside every training and every primary contrast; they are evaluated under all the already trained C0 models, in both arms. No “tragedy effect” is estimated on six independent replicates: five works are by Sophocles.

### 3.5 Confounding that delimits the conclusions

In the primary corpus the HEX label coincides with the archaic component; comparable archaic prose is missing. Epoch, tradition, genre and form are not separable. The prose labels refer to the works, without metrical certification of every token or removal of any verse quotations. The annotation comes from different processes and annotators: UD uniformization does not prove identical quality across works. No per-annotator control is invented in the absence of sufficient metadata.

Long sentences receive more weight because they offer more positions. Excluding the first four symbols does not equalize the distribution of the lengths. The result remains conditional on this distribution; the two history bands planned in §9 make it visible without creating a further inferential analysis.

## 4. Encoding and population of the targets

### 4.1 Deterministic transformation

Mandatory order: keep lines with integer ID; map `PROPN → NOUN`; select UPOS; derive the base DEPREL with `lower().split(':', 1)[0]`; apply the policy of the variant; assign the ID of the symbol.

UPOS kept: `ADJ, ADP, ADV, AUX, CCONJ, DET, NOUN, NUM, PART, PRON, SCONJ, VERB`. UPOS removed: `PUNCT, X, INTJ, SYM`. Any other UPOS not explicitly handled is an input error, not a silent removal.

DEPREL kept: `root, nsubj, csubj, obj, iobj, ccomp, xcomp, obl, advcl, advmod, acl, amod, appos, det, nummod, nmod, case, mark, aux, cop, cc, conj, parataxis`.

`ud23` is the historical name of the project subset: it is **not** the whole inventory of the UD relations. The general inventory comprises 37 base relations and possible subtypes. [UD documentation](https://universaldependencies.org/u/dep/index.html).

| Variant | Rule | Verified alphabet |
|---|---|---:|
| `ud23` / C0 | UPOS:DEPREL; remove relations outside the 23 | 106 |
| `ud23_oth` | Same UPOS; outside relations aggregated into `oth` | 112 |
| `upos_only` | **Same retention mask as C0**, then remove DEPREL from the symbol | 12 |

Removals close the gaps: the context counts retained symbols, not distances in original words. The original coordinates remain in the output. No additional words are removed to “clean” inconvenient results and no FEATS, lemma or lexicon are introduced.

### 4.2 Frozen alphabet

For each of the three variants, the inventory is the union of the symbols observed in the 17 documents, probes included. The strings are sorted lexicographically, with consecutive integer IDs from 0. BOS and SEP have reserved negative IDs and do not enter the alphabet of the outcomes.

This choice is **transductive and closed**: the support of the complete corpus is known, held-out included, but no frequencies, transitions or weights are transferred from the test to the training. The protocol is therefore not presented as an evaluation on completely unknown future texts. A new symbol after the freeze causes an error; there is no implicit `UNK`.

### 4.3 Retention checks

The census is kept per document and original regime (`HEX`, `PROSE_CLASS`, `PROSE_POST`, `OTHER_VERSE`), before the descriptive union `PROSE_ALL`.

Check A computes, for each excluded relation, the number of tokens with admissible UPOS and that relation, divided by **all raw tokens of the regime**. A share >2% produces a flag; different relations are not summed to compare them with the threshold. Check B flags documents with retention <70%. These are conventional diagnostic thresholds, not guarantees of linguistic validity.

With the frozen inputs the earlier audit produced no blockers on these thresholds; the largest flaggable category was `vocative` in the tragedy, about 1.28%. The future execution must recompute the values. A different result with identical inputs and encoding is an error to be solved. The `oth` cell remains mandatory independently of check A: no conditional branch changes the budget.

### 4.4 Evaluable targets

A position is evaluable if it has **at least four ordinary retained predecessors in its own sentence**: zero-based index `j ≥ 4`. The population is fixed before seeing the scores and is identical for root and CTW, original and shuffled, and for the sensitivities that keep the C0 mask.

All training tokens, including the initial ones, contribute to the counts. On the test the first four receive no primary score but feed the history. There is no subsampling of the test nor a test budget `m`; all eligible positions are evaluated.

The `oth` variant can modify the target population. The comparison with C0 is therefore flagged as a change of representation and population. No fake numerical correspondence between different rows is forced.

## 5. Sampling, exclusion and seeds

### 5.1 Leave-one-block-out training

For each of the seven held-out blocks and each seed, exclude all its documents. From the remaining six blocks extract exactly `q = 8.884` tokens each, for `6q = 53.304` tokens of C0 training. The value is the minimum of the C0 availability of the seven blocks; it remains 8,884 in `oth` too, to isolate the encoding from the budget. `q_half` uses 4,442 and 26,652 tokens in total.

*[Translator's note: in the code spans, kept as in the original, `q = 8.884` and `6q = 53.304` mean 8,884 and 53,304.]*

The training is balanced by block, not by group. Excluding HEX, the training contains 1/6 of HEX tokens; excluding prose it contains 2/6. The share of the **test group** is respectively 1/6 and 4/6. This asymmetry is a declared property of the estimand. The direction of the bias is not presumed a priori. Eliminating this asymmetry would require another protocol and is not presented as obtained by the simple balancing of the blocks.

Q does not automatically correct the asymmetry of the composition of the training. It is not demonstrated, however, that it necessarily penalizes HEX or makes the comparison conservative: the share of one's own group does not guarantee similarity of the sequences. A D=8 CTW counterexample verified in the revision shows Q decreasing when the weight of the group less similar to the target increases; an opposite scenario shows Q increasing. The results and the generator are in the attachments of the revision. They are not an estimate of the bias in Greek.

The table of the seven folds must include the HEX/prose training shares and the share of the test group. Any plot of Q against the share of one's own group is only a representation of this structure: the share here takes two values determined by the group, so it does not separately identify an effect of exposure.

### 5.2 Sampling algorithm

1. Sort all the sentences of the block by `(canonical_doc_id, part_order, source_ordinal, sent_id)`, including any sentences without retained symbols.
2. Permute the sentence indices uniformly with the `sample` subseed. Empty sentences do not contribute to the budget, but remain in the universe of the permutation to stabilize the pairing between encodings.
3. Consume whole sentences until the next one exceeds the remainder. For that last one choose uniformly a contiguous segment of the exact residual length, with a sentence-specific `fragment` subseed.
4. Stop. The result has exactly q tokens, no repeated sentence and at most one fragment per contributing block, hence at most six fragments per fit.
5. Record for each included sentence `sent_id, start, end, fragment`, with zero-based bounds in the encoded sequence and interval `[start, end)`.

It is not a uniform sample of single tokens: it favours the integrity of the sentences. In C0 each sentence/fragment constitutes an independent stream, initialized without earlier history. The excluded portion of a fragmented sentence provides no context to the model.

The numerical sensitivities reuse exactly the C0 ledger of the same seed and fold. `q_half` reuses the permutation of the sentences, but the random cut of the last sentence can change: token-by-token nesting is **not** guaranteed. `upos_only` keeps the C0 ledger. `oth` reuses the order of the same sentences but can stop elsewhere because of the different lengths. The boundary cell uses the same C0 sample.

**Explicit decision on finding C5.** The final fragment, already present in the proposal `piano_ultimato`, is kept, after re-examining the objection of the proposal `piano_finale`. The operational priority is an exactly equal contribution of tokens from each block. The accepted cost is that an internal cut creates a start of the sampled stream that does not coincide with the start of the source sentence. BOS means the end of the history available in the stream, not proof of a natural linguistic boundary. It is not claimed that the cost is identically null; the loss of the token-by-token nesting of `q_half` is part of the same decision.

The additional C0 census over the 20 seeds found 671 fragments in 840 contributions, 563 of them with a start internal to the sentence. At D=8, 3,477 training targets out of 7,462,560 are directly affected, about 0.0466%. This share does not mathematically bound the variation of the predictions: the posterior weights can propagate the effect. Eliminating all fragments, without replacing them, on the seven folds of the first seed, the maximum absolute deviation of Q was 0.000685 bits/symbol. It is a local feasibility check, not a complete final sensitivity nor a universal guarantee.

The ledger and the final diagnostics must record, per contributing block and pair, `fragment_count`, `internal_start_count`, `fragment_tokens` and `direct_context_targets = Σ min(D, fragment_length)` over the fragments with `start > 0`. The cut coordinates are shared by the two arms: they are not counted as two independent decisions. At most six fragments per pair imply at most 4,200 distinct segments in the 700-pair plan; 8,400 is only the bound of their occurrences in the two arms. The whole-sentence comparison remains a separate development check and does not add a tenth cell.

### 5.3 Identity of the seeds and invariance to the labels

Master seed: `20260706`. C0: indices 0–19; each sensitivity: 0–9. The new convention is `hexis-v3-rng-1`, distinct from the earlier pilot based on CRC32.

`block_key = SHA256(JSON_canonico(lista ordinata dei canonical_doc_id del blocco))`. The display name of the block, the author, the group and the epoch do not enter the seed.

*[Translator's note: in the code span, kept as in the original, `JSON_canonico(lista ordinata dei canonical_doc_id del blocco)` means "canonical JSON (sorted list of the canonical_doc_id of the block)".]*

For each draw the object is built with only the keys:

```json
{"version":"hexis-v3-rng-1","master":20260706,"seed":0,"held":"<block_key>","block":"<block_key>","purpose":"sample","sid":"","start":0,"end":0}
```

The values in angle brackets illustrate the type; in execution they are the real hashes. Serialization: UTF-8 JSON, `ensure_ascii=False`, `sort_keys=True`, `separators=(',', ':')`, without newline. The integer seed is formed by the first 16 bytes of the SHA-256, big-endian. RNG: `numpy.random.Generator(numpy.random.PCG64(seme))`.

Admitted purposes: `sample`, `fragment`, `shuffle_train`, `shuffle_eval`, `shuffle_probe`. For `fragment` use `sid` and bounds 0/0; for shuffle use `sid` and the bounds of the segment, or 0/length for the whole sentence. In the probe `block` is the hash of the list containing only the probe document. The numerical parameters, the name of the cell, the variant and the labels do not enter the derivation. This allows the planned pairing. The data are fixed and identified in the manifest, but the hash of the complete configuration is not a random ingredient.

The executable contract and a reference vector are in the attachments. Renaming blocks and changing the order of the input records must not change samples, scores or models. An actual change of the members of a block changes its identifier and is a new version of the design.

## 6. Mathematical contract of the CTW

### 6.1 Parameters and counts

Let A be the frozen alphabet, `m = |A|`, `D = 8`, `a = 0,5` pseudocount **per symbol**, `rho = 0,5` prior probability of stopping. The names `a` and `rho` are distinct; the old ambiguous `beta` is eliminated.

*[Translator's note: `a = 0,5` and `rho = 0,5` are kept in code notation as in the original: 0.5.]*

Each node s represents a suffix, traversed from the most recent to the least recent symbol. `n_s(x)` counts the ordinary outcomes x observed under that context; `N_s = Σ_x n_s(x)`. The local distribution is:

\[
p_s(x)=\frac{n_s(x)+a}{N_s+ma}.
\]

No `k_min`, `gamma`, heuristic pruning, `argmax` selection or additional penalties are applied. All observed contexts up to D are built; the empty subtrees are represented implicitly.

The methodological source is the CTW/BCT for finite alphabets, with integrated evidence and averaging over models. The HEXIS conventions for separate streams and boundary symbols are an explicit adaptation, verified separately; they are not attributed textually to the paper. [Kontoyiannis et al., version 3, 2022](https://arxiv.org/abs/2007.14900v3).

### 6.2 BOS and consistent partition

At the start of each stream the history is empty. For each ordinary target, the root is visited, then the available history in reverse order, up to D. If the history ends before D, a **BOS** edge is added, leading to a terminal leaf. BOS has ID −1, appears only in contexts and is not predicted.

A non-terminal node must satisfy, for every outcome x:

\[
n_s(x)=\sum_{c\in\mathrm{children}(s)}n_{sc}(x).
\]

BOS collects precisely the initial observations that would otherwise have no child. The root trained on all tokens is never compared with children trained only on the internal positions. The nodes at depth D and those reached through BOS are forced leaves.

### 6.3 Integrated evidence and recursion

The Dirichlet evidence of the node is:

\[
E_s=\frac{\Gamma(ma)}{\Gamma(N_s+ma)}
\prod_{x\in A}\frac{\Gamma(n_s(x)+a)}{\Gamma(a)}.
\]

For a forced leaf, `W_s = E_s`. Otherwise:

\[
W_s=\rho E_s+(1-\rho)\prod_{c}W_{sc}.
\]

A subtree without observations has `E = W = 1`; the unit factors are omitted from the product without eliminating probability mass. The posterior probability of stopping is:

\[
w_s=\frac{\rho E_s}{W_s},
\]

with `w_s = 1` in the forced leaves. By induction on the depth, the recursion is equivalent to the sum of the evidences of all admitted trees, weighted by the stop/split prior. The partition of the counts makes the comparison consistent. The computed evidence does not require a random order of the streams.

The family of contexts includes the possible SEP and BOS according to the convention of §7; the prior of stopping is always rho, without an automatic correction depending on the number of edges. The asymptotic theorems for stationary sources are not transferred without proof to the composite corpus.

### 6.4 Frozen prediction

With counts and weights fixed on the training, for the history h:

\[
q_s(x\mid h)=w_s p_s(x)+(1-w_s)q_{sc}(x\mid h),
\]

where c is the next edge of the history. On a forced leaf p_s is used; entering a never-observed subtree the prediction is uniform, `1/m`. At the root one obtains `q_CTW`.

During the whole evaluation, **neither the counts nor the weights w change**. The history proceeds along the test sequence and can contain earlier test symbols. The following symbols are not read to predict the target; the annotated representation nonetheless remains offline, as clarified in §1.2.

This predictor is a frozen average of the predictions of the models weighted on the training. It is not the joint probability of the test obtained by updating the posterior over the trees online. The product of its conditional probabilities is nonetheless a well-defined predictive code. The comparison root uses the same global counts of the training and the same a:

\[
q_0(x)=\frac{n_\varnothing(x)+a}{N_\varnothing+ma}.
\]

### 6.5 Arithmetic and numerical checks

The evidences are computed in natural logarithms with `lgamma`, stable summation and `logaddexp` or equivalent; only the final losses are converted to bits. Use float64, never float32. Root and CTW must give finite and positive probabilities, summing to 1 within tolerance.

Keep `log_rho` and `log_one_minus_rho` separate. The form `rho = 1 - 2**(-(m-1))` can round to 1 for m=106: it must not be used to represent the prior suggested as a default in part of the literature. This numerical test remains in the test suite even if that configuration is not a final cell.

A normalization deviation within `1e-12` is tolerated in the small tests; beyond the threshold it is an error. Clipping a weight just above 1 is admitted only if the deviation is ≤`1e-12`, with an explicit check; no generalized clipping is used to hide problems. In the enumeration tests the absolute tolerance on the probabilities is `1e-12`, on the log-evidences `1e-10`. On large outputs the tolerance for reconstructing the CE is `1e-9` bits/symbol, on reproductions across platforms `1e-8`. Counts and coordinates must coincide exactly.

## 7. Boundaries and order control

### 7.1 Primary configuration of the boundaries

C0 resets the history at every sentence or fragment. Sentences are not concatenated only because they are contiguous in the sampling permutation. Documents, parts or gaps are not crossed. The training statistically aggregates separate streams.

### 7.2 `bound` sensitivity

The sample is sorted by source identity and order. Two sentences can be linked only when:

- they belong to the same canonical document **and to the same source prefix**;
- they have the same part and consecutive source ordinals;
- they have consecutive ranks in the complete list of the sentences, built before retention and sampling;
- both are whole and non-empty.

The rule identifies adjacency in the observed treebank; it does not demonstrate continuity of the whole ancient work. No link crosses the change between Athenaeus XII and XIII. A sentence not selected, empty or fragmented interrupts the chain. Two sentences separated by a jump in the identifiers remain separate even if they become neighbours in the subset.

Between admitted sentences SEP, ID −2, is inserted **only in the context**. SEP consumes one position of the structural depth D, is not a target and does not increase m. The history can cross it; the counter of predecessors in the current sentence nonetheless restarts from zero. Therefore the eligible coordinates remain those of C0. No EOS or other symbols are inserted.

### 7.3 Mandatory, paired shuffling

For each fold/seed pair and for each cell:

1. Build the training sample only once.
2. Prepare an original arm and a shuffled arm.
3. In the second, permute the symbols uniformly **within each sampled sentence or fragment**, after the sampling. Each element carries its source coordinate with it; the coordinate of the slot remains distinct.
4. Train a CTW from scratch on the shuffled training.
5. Shuffle independently each sentence of the held-out block, with RNG purpose `shuffle_eval`, and evaluate it under the shuffled model.
6. For `bound`, first shuffle within each sentence and then apply exactly the same links and SEP of the original arm. SEP is not moved.

**One permutation per seed** is used: 20 paired realizations in C0 and 10 in each sensitivity. No replicates are added on the basis of a result close to zero. Sampling and permutation contribute jointly to the variability across seeds; the design does not separately estimate their variance components.

The shuffling keeps exactly the length, the multiset of the symbols per sentence/fragment and the root counts of the training. It does not keep n-grams, syntactic dependencies or grammaticality. Sentences whose symbols are all identical may not change: record the share of slots whose symbol changes, without repeating the permutation until it “changes enough”.

Permutation without replacement introduces its own dependencies from finite composition. The control is neither an i.i.d. source nor a universal estimate of the bias of the CTW. It serves to compare the observed order with **this defined transformation**, keeping composition and segmentation. A positive Q score does not automatically isolate syntax, metre or a causal effect.

### 7.4 Why a difference of gains is needed

The earlier synthetic control produced positive gains of about 0.52–0.89 bits in texts internally i.i.d. but heterogeneous across blocks: the context can help to recognize the composition of the text. After the comparison with the shuffling the residual was about −0.0014–0.0018; in the source with delayed dependency about 0.53 remained. This is the empirical reason for making the paired comparison central.

Even if the training roots of the two arms are identical, **the root CE of the test can differ**: excluding the first four slots, the shuffling changes which symbols enter the score. Q is not simplified into `CE_CTW_shuffled − CE_CTW_original`. All four terms are computed and kept.

In the seven real folds of the first seed already examined, shuffled G is zero at the recorded numerical precision, so Q coincides numerically with original G. This preliminary outcome is declared before the final run; it is not assumed to hold for all seeds and cells. The 700 shuffled fits are a predefined control that can refute the interpretation of G alone, not an operation to be omitted because the first pilot is favourable.

There is no theorem imposing a shuffled G exactly null in finite samples: the CTW mixture does not necessarily select the root. In the additional i.i.d. control the stopping weight at the root is about 0.80775 and the gain about 0.000195 bits/symbol. Moreover, within-sentence shuffling does not in general produce an i.i.d. sequence. The numerical coincidence with the root predictor must be described as an observed result, not as a mathematical necessity.

## 8. Measures, weights and mandatory results

### 8.1 Losses and gains

Let I_b be the set of eligible slots of block b in the current variant; `n_b = |I_b|`. For seed s and arm z, original O or shuffled R:

\[
CE_{b,s}^{z}=\frac{1}{n_b}\sum_{i\in I_b}-\log_2 q_{CTW,s}^{z}(x_i^{z}\mid h_i^{z}),
\]

\[
CE_{0,b,s}^{z}=\frac{1}{n_b}\sum_{i\in I_b}-\log_2q_{0,s}^{z}(x_i^{z}),
\qquad G_{b,s}^{z}=CE_{0,b,s}^{z}-CE_{b,s}^{z}.
\]

The central measure is:

\[
Q_{b,s}=G_{b,s}^{O}-G_{b,s}^{R}.
\]

Unit: bits per eligible encoded symbol. G can be negative; Q can be negative. Neither is truncated to zero. Q expresses the additional advantage of the context under the observed order with respect to the specified control.

### 8.2 Aggregation

Within each document and block the losses are summed and divided by the number of targets. This weighs the documents by their targets, without giving the Hymn the same weight as the Iliad. The separate results of the 11 documents are nonetheless kept, so that the block mean does not hide their heterogeneity.

For each seed:

\[
D_{Q,s}=\frac{1}{2}\sum_{b\in HEX}Q_{b,s}
-\frac{1}{5}\sum_{b\in PROSE\_ALL}Q_{b,s}.
\]

The primary result is `D_Q = mean_s D_Q,s` in C0. Also mandatorily reported are the seven `mean_s Q_b,s`, the corresponding original/shuffled G and the contrasts `D_G_original` and `D_G_shuffled`. None of the latter replaces Q because it gives a larger separation.

The groups have uniform weight **across blocks**, not across tokens. The mean over seeds is arithmetic. The SD over seeds uses denominator S−1; minimum and maximum are also reported. No p-values, bootstrap CIs, Holm, population confidence intervals, Bayes factors between regimes or percentages of “significance” are computed. Tokens, documents of the same block or seeds are not reused as independent n.

The contrast is specific to the leave-one-block-out procedure with a different training per block. It is not the comparison of the seven blocks under a single commonly trained model. It can be reconstructed exactly from the seven scores and this reconstruction is a mandatory test.

### 8.2-bis Mandatory reaggregation by eligible targets

The primary contrast remains the one with uniform weight across blocks. For all nine cells, on the same Q already available, the following is also computed:

\[
D_{Q,s}^{token}=\frac{\sum_{b\in HEX}n_b Q_{b,s}}{\sum_{b\in HEX}n_b}
-\frac{\sum_{b\in PROSE\_ALL}n_b Q_{b,s}}{\sum_{b\in PROSE\_ALL}n_b}.
\]

The weights are the numbers of **eligible** targets of the current variant, not the raw tokens, the total retained tokens or the training q. The two components original/shuffled G are reported likewise, verifying `D_Q_token = D_G_original_token − D_G_shuffled_token`. Mean, SD, minimum and maximum are computed on the same seeds of the cell. The comparisons between sensitivities and C0 remain paired on the first ten seeds.

In C0 the weight of the Hesiodic block on the HEX side goes from 50% to 12.0263%, because it contributes 6,375 of the 53,009 HEX eligible targets. The reaggregation changes the question: description of the average block against description of the average target in the group. Neither is an inferential correction of the other; the one with the larger separation is not chosen. This reading trains no models, introduces no tenth cell and changes neither the budget nor the per-position outputs. The summaries are emitted only after the checks of §14.2.

### 8.3 JSD of the root distributions: R1

For each variant, on the **complete original tokens** of each primary block, including the initial ones, build:

\[
r_b(x)=\frac{n_b^{all}(x)+0.5}{N_b^{all}+0.5m}.
\]

These are descriptive distributions of the whole block, distinct from the leave-one-block-out training roots used for G. Also publish the unsmoothed counts and frequencies: smoothing must not hide the census.

For p and q, with `u = (p+q)/2`:

\[
JSD(p,q)=\tfrac12\sum_xp(x)\log_2\frac{p(x)}{u(x)}
+\tfrac12\sum_xq(x)\log_2\frac{q(x)}{u(x)}.
\]

The 21 pairs among seven blocks and the symmetric 7×7 matrix are computed; the diagonal is zero. The centroids `r_HEX = mean dei 2 r_b` and `r_PROSE = mean dei 5 r_b` are also formed, then their JSD. This does not coincide with the mean of the pair JSDs, which is not used as a substitute.

*[Translator's note: in the code spans, kept as in the original, `mean dei 2 r_b` and `mean dei 5 r_b` mean "mean of the 2 r_b" and "mean of the 5 r_b".]*

The contributions of each symbol to the JSD of the centroids are published, with a verified sum. The distributions have common support; the JSD is in [0,1] bits and does not require strictly positive probabilities. In the code `0 log 0 = 0` is handled correctly even if smoothing makes the current inputs positive. The divergence is not called a metric distance; no clustering with implicit metric assumptions is introduced. Source: Jianhua Lin, *Divergence Measures Based on the Shannon Entropy*, 1991, supplied PDF `jensen-shannon.pdf`.

R1 is run for C0, `oth` and `upos_only`, without CTW fits and without seeds. A marginal difference does not demonstrate a difference in order, and vice versa. R1 is mandatory but not an additional inferential family.

### 8.4 Probe without new training

For each tragic document evaluate the two arms under all 7×20 original/shuffled C0 models, using `shuffle_probe` for the transformation of the test. Compute CE, CE0, G and Q per document/fold/seed. Report the seven means over seeds and a document summary that assigns weight 1/7 to the folds and 1/20 to the seeds.

The folds share training and the seeds share texts: the dispersion is descriptive, not an inferential interval. Do not aggregate the six tragedies into an eighth block and do not compare directly the summary of the probe with a primary block as if they had identical exposure to the training. The probe is not an independent check of generalization outside the corpus, since its inventory is included in the alphabet.

## 9. Diagnostics of the model and of the positions

Each fit produces: number of nodes per structural depth; distribution of the support of the nodes in classes `0, 1, 2–4, 5–9, ≥10`; number of outcomes observed at the root; share of test targets never observed at the root; predictive mass routed towards the first unobserved subtree; times and memory. The nodes with zero support are implicit: class zero is not obtained by enumerating an exponential tree; the implicit branches encountered in evaluation are reported separately.

For a history, the mass that stops at an observed node is the product of the continuation probabilities along the path, multiplied by w_s. The residual mass at the first unobserved branch is `unseen_mass`. The observed stopping masses plus `unseen_mass` must sum to 1.

Define `lexical_context_length(s)` as the number of ordinary edges in the context of the node: BOS and SEP do not count. The histogram of the observed masses by that length is accumulated and, if the observed mass is positive, the mean conditional on the observed part is reported:

\[
L_{resolved}=\frac{\sum_{s\ osservati}\lambda_s\,lexical\_context\_length(s)}{1-unseen\_mass}.
\]

*[Translator's note: in the formula, kept as in the original, `osservati` means "observed".]*

In the code the denominator is computed as a direct sum of the resolved masses, avoiding the loss of precision of `1 − unseen_mass` when the residual mass is almost one. With empty training unobserved mass 1 and no resolved mass are assigned. If the denominator is zero, the value is `null` with reason `no_resolved_mass`, not zero. This is a diagnostic of the component resolved by the data. It is **not** the expectation of the depth of all posterior trees: in the empty subtrees the prior allows further depth, while giving the same uniform prediction. The `weighted_depth` of the old prototype, which collapses that part at the first absent node, remains a historical field and is retired from the v3 scientific outputs.

Also publish, for each block and arm, number of targets and gains in the bands `4 ≤ available_past < 8` and `available_past ≥ 8`; use the same definition in the `bound` cell. An empty band has count zero and a null score with an explicit reason. Do not create others after observing the results. No “interesting” contexts are selected to support a main conclusion; any subsequent linguistic examples are separate and declared exploration.

## 10. Final matrix of the analyses and budget

| Cell | Only variation with respect to C0 | Seeds | Original fits | Shuffled fits |
|---|---|---:|---:|---:|
| C0 | m=106; D=8; a=0.5 per symbol; rho=0.5; q=8,884; reset | 20 | 140 | 140 |
| a_total1 | a=1/m, total Dirichlet mass 1 | 10 | 70 | 70 |
| q_half | q=4,442 | 10 | 70 | 70 |
| D6 | D=6 | 10 | 70 | 70 |
| D12 | D=12 | 10 | 70 | 70 |
| rho09 | rho=0.9 | 10 | 70 | 70 |
| oth | alphabet `ud23_oth`, m=112; q unchanged | 10 | 70 | 70 |
| upos | alphabet `upos_only`, m=12; C0 mask | 10 | 70 | 70 |
| bound | links and SEP of §7.2 | 10 | 70 | 70 |
| **Total** | **9 cells, 700 pairs** | | **700** | **700** |

They are therefore **1,400 fits**, plus evaluations without new training. The 280 C0 fits also generate 1,680 document-probe evaluations: 6 documents × 7 folds × 20 seeds × 2 arms. R1 adds no fits. There are no factorial combinations between sensitivities.

The sensitivity to the almost always stopping prior of the literature remains in the earlier numerical validation; it does not enter the final analysis, where `rho09` gives an explicit and readable perturbation. `argmax`, monotone selection and `k_min/gamma` rules do not constitute sensitivities of the new model.

For each sensitivity compare its ten seeds with **the same first ten C0 seeds**, through paired differences per block/seed. The twenty-seed C0 summary remains the central result, but it must not be subtracted from a ten-seed sensitivity while calling the difference “paired”.

Variations of a, rho, q and D measure the dependence of the result on choices of the predictor and of the sampling. `oth`, `upos` and `bound` change representation or availability of context: describe them as such. The CE of different alphabets do not have an identical informational reference scale; a smaller value in UPOS does not automatically mean greater linguistic organization. The gains too concern different tasks.

Sign stability is not imposed as a condition for completing the project. An inversion must be reported as dependence of the description on the analytical choices, not corrected with another cell. The final model is not chosen on the basis of the maximum contrast between groups.

## 11. Software contracts and outputs

### 11.1 Separation of responsibilities

The following APIs are implementation requirements, not commands already available in the verified commit.

| Component | Input | Output and obligations |
|---|---|---|
| Reader/census | CoNLL-U files with expected hashes | Source records with identity and order; error on duplicates or missing metadata |
| Encoder | Records + variant | Sequences, coordinate map, frozen inventory and audit of the removals |
| Sampler | Records of the blocks, block keys, held-out, q, seed | Ledger and streams; no regime label |
| CTW `fit` | Stream of integers, m, D, a, log-prior | Frozen model, diagnostics and fingerprint |
| CTW `predict_proba` | Frozen model, history | Normalized vector over A, no mutation |
| Score | Model, sequences, coordinates, eligible mask | Per-position losses and aggregates without labels |
| Pairing | Original/shuffled output on the same set of slots | Q and correspondence checks |
| Annotation | Scores + registry + block map | Groups and metadata for the tables; the only stage that uses the regime to aggregate |
| R1 | Complete counts per block and variant | Roots, centroids, JSD and contributions |
| Report | Validated tables and manifests | Figures and text making corpus, weights and limits explicit |

Configuration: strict schema with admitted keys, types and ranges. Reject unknown keys, retired historical parameters, NaN/Inf, booleans used as integers, negative D, non-positive q, non-positive a, rho outside (0,1), repeated seeds, duplicate cells, inconsistent alphabets and incomplete groups/blocks. The key-presence-only check currently present in the project is insufficient.

The integers of the counts must avoid overflow; the symbols are non-negative integers <m. Negative IDs are reserved: BOS must not be supplied as an element of the stream, SEP is admitted only in `bound`. The public function must reject floats silently converted into integers. D=0 and empty training remain test cases, but the real protocol imposes the D and q of the declared cells.

### 11.2 Source tables and coordinates

Output `documents.csv`: one row per canonical document, with `doc_id, source_prefixes, work, author_label, period_label, regime, role, dependence_block, raw_tokens, raw_sentences, kept_tokens, eligible_tokens, retention, flags`, distinct per variant where necessary.

Output `coordinates.parquet`: one row per retained ordinary token, with `variant, slot_uid, doc_id, sent_id, source_prefix, part_order, source_ordinal, source_rank, raw_token_id, encoded_index, symbol_id, available_past, eligible`. `slot_uid` is a stable integer assigned in the canonical order of each variant; the complete key includes the variant. Textual identities kept in dictionaries, without repeating long strings in the score vectors.

Output `alphabet.json`: variant, sorted list of the symbols, m, mapping, perimeter of the 17 documents and hash. The file of the audit counts also includes all removed rows with reason and coordinates, or an equivalent source table from which to reconstruct them exactly.

### 11.3 Ledger and identification of the executions

For each fold/seed and distinct sample: `sample_ledger.json`, with keys of the six blocks, q, selected sentences, bounds, fragments, source coordinates of the segment and derived seeds. The numerical cells can reference the same ledger through its hash; do not duplicate it pretending independent samples.

The scientific execution is identified by `run_id = SHA256(JSON canonico del run_contract)`. The `run_contract` comprises the version of the specification, the commit of the code, the hash of the data, the hash of the registry and of the alphabets, the hash of the configuration, the lock of the dependencies and the RNG version. It does not comprise timestamps, absolute paths, machine labels or measured times. The external manifest also records these environmental data, without using them as seeds.

*[Translator's note: in the code span, kept as in the original, `JSON canonico del run_contract` means "canonical JSON of the run_contract".]*

Per fit: key `(run_id, cell, held_block_key, seed, arm)`. For a pair: the same key without `arm`. A probe adds `probe_doc_id` to the key of the evaluation, without creating a model.

### 11.4 Per-position scores

Save all positions of the seven blocks in all cells, and of the six probes in C0, in Parquet partitions per pair/cell. A row pairs the same **slot**, not necessarily the same original token:

`slot_uid, original_symbol_id, shuffled_symbol_id, shuffled_origin_slot_uid, loss_ctw_original, loss_root_original, loss_ctw_shuffled, loss_root_shuffled, unseen_mass_original, unseen_mass_shuffled, resolved_mean_original, resolved_mean_shuffled`.

The four losses and the numerical diagnostics are float64; `resolved_mean` is nullable according to §9. The coordinates of the slot and of the provenance of the shuffled symbol must allow exact reconstruction. The first is the place where one evaluates; the second is the moved token. For probes the same structure and the dictionary of their coordinates are used.

The partition metadata contain `run_id, cell, fold, seed, variant, target_role, target_doc_id se probe, model_hash_original, model_hash_shuffled, ledger_hash`. No group column enters the core. The pairing is verified with a one-to-one join on the slots, not through simple equality of the lengths.

*[Translator's note: in the code span, `target_doc_id se probe` means "target_doc_id if probe".]*

For the nodes the whole tree of each fit is not saved: the fingerprint is kept and the tree is regenerated from sample and parameters. Keeping one pair of models in memory is sufficient; once evaluation and writing are finished, free it. The shared dictionaries of the coordinates remain small.

### 11.5 Mandatory aggregates and figures

`model_diagnostics.csv`: one row per fit with times, peak RSS and the statistics of §9; mass and support histograms in associated JSON. `document_scores.csv`: one row per document/seed/cell/arm, number of targets, sums of the losses, CE, CE0 and G. `block_pairs.csv`: one row per block/seed/cell, the four CE, G in the two arms and Q. `contrasts.csv`: one row per cell/seed with group means and D_Q, original/shuffled D_G.

`seed_summaries.csv`: mean, sample SD, minimum, maximum and effective S of every planned quantity. `sensitivity_pairs.csv`: differences with respect to C0 on the same first ten seeds, with type of change (`numerical`, `budget`, `representation`, `boundary`). `probe_scores.csv`: values per document/fold/seed and declared summaries. `root_distributions.csv`, `jsd_pairs.csv`, `jsd_centroids.csv`, `jsd_contributions.csv`: R1 results, per variant. `past_buckets.csv`: the two predetermined bands.

Mandatory figures, generated exclusively from these tables:

1. Corpus: quantities and retention per document, with a visible separation between primary documents and probes.
2. Seven blocks: original and shuffled G side by side; Q panel; points per seed and mean. If bars are shown, indicate explicitly “min–max across seeds”, never “CI”.
3. C0 D_Q and eight sensitivities, with C0 values of the first ten seeds in the panel of the paired comparisons.
4. R1: C0 7×7 heatmap, values of the centroids in the three variants and contributions of the symbols; complete table in the attachment, without filters that remove unfavourable contributions.
5. Support of the contexts and unobserved mass; highlight the distinction between maximum admitted depth and depth supported by the data.
6. Probe: six separate documents, seven fold means per document and summary; no inferential error bars.

No figures are produced for chunks of 1,000 tokens, networks of reference models, lexicons of contexts or learning curves. Philological examples are not a necessary deliverable for closing the downsized project.

`aggregation_weights.csv` contains, per variant and block, group, eligible n, primary weight and per-target weight. `contrasts.csv` and `seed_summaries.csv` include `aggregation = equal_block | eligible_token_weighted`, with distinct keys and the two schemes always side by side. The summaries concerning the groups are produced only by `run_report` after the completeness check; the fit pipelines produce individual scores and the corresponding sums, not intermediate contrasts.

In the contrast panel of figure 3 add the reaggregation by targets, identifying its different estimand. Do not add a mandatory figure or fit. The training shares and the fragment metrics enter the existing diagnostic tables.

### 11.6 Manifest, resumption and errors

Each partition is written to a temporary file in the destination directory, verified and renamed atomically. The manifest records size, hash, number of rows, schema and status `complete`. A temporary file does not count as a result.

`--resume` reuses a partition only if contract, hash and cardinality coincide; otherwise it fails. Results of different commits or configurations are not mixed. There is no silent overwriting: a new version produces a new run_id; an already complete directory remains immutable. The error messages identify file, document, sentence, cell and stage concerned without reporting whole texts.

A zero denominator in a secondary band produces null with a reason. A primary block without targets, an impossible budget, a non-finite model, a missing pair or an unforeseen parameter stop the cell and prevent the final report. Blocks or seeds causing errors are not excluded automatically. An incomplete execution keeps diagnostic evidence but does not reach the status `COMPLETE`.

## 12. Acceptance tests

The tests must verify properties or cases with an independently known answer. Comparing the function with its own rewritten formula is not enough. The earlier exact proofs provide an independent reference; the porting must keep their cases and tolerances, not only copy the implementation.

| ID | Property and criterion | Current evidence / integration action |
|---|---|---|
| T01 | Hashes of the three files, uniqueness of the sent_ids, 18 prefixes → 17 documents | Already verified; gate of the canonical reader |
| T02 | 202,989 tokens and 13,919 sentences; per-document counts of the expected JSON | Already verified; exact equality required |
| T03 | All UPOS/DEPREL rules, subtypes, multiword/empty lines, malformed inputs | Reuse valid existing cases, add missing cases |
| T04 | m=106/112/12; UPOS mask and coordinates identical to C0 | Verified in the new contract too |
| T05 | No member of the held-out block in the training; probes never in the training | Verified; assert on the complete identities |
| T06 | Exact q; no replacement of sentences; ≤1 fragment/block; empty sentences and impossible budget | Executable contract included |
| T07 | Invariance to the order of the records and to renaming of the labels; ledgers reused in the planned cells | Contract and new integration tests |
| T08 | Reference RNG vector; separation of purposes; repeatability | 3,360 derived keys checked without collisions; fix the vector in the suite |
| T09 | Partition of the counts in every node for every outcome, terminal BOS, SEP context only | Verified in the prototype; bring to the core |
| T10 | Enumeration of all small trees against W and prediction | 120 cases passed; error within §6.5 |
| T11 | Sum of probabilities=1; unknown symbols/branches; empty training; D=0 | Already verified; no NaN/Inf |
| T12 | Prequential/integrated identity of the training; invariance to the order of the streams | Already verified; do not confuse with updating the test |
| T13 | Counts, log-evidences and weights identical before/after any evaluation | Fingerprint unchanged, also after probes |
| T14 | Extreme priors in log, rho at m=106 not implicitly rounded to 1 | Numerical case already reproduced |
| T15 | Synthetic i.i.d. 4, cycle 3, Markov 1, lag 2, variable memory | Targets and thresholds of the synthetic protocol below |
| T16 | m=106 stress | Execution/support test; gap from the oracle reported, not hidden |
| T17 | Shuffling keeps multiset and root; keeps mask and separators | New real pairs and fixtures passed |
| T18 | Counterexample of heterogeneity without internal dependency | G can be positive; Q check in the predetermined cases |
| T19 | Q uses four terms and not the shortcut between two CE | Exact counterexample included in the attachments |
| T20 | Aggregation from losses → documents → blocks → groups; uniform primary weight and secondary per-target weight | Independent fixtures with different lengths, eligible denominators and four-term identity |
| T21 | Sensitivities compared with C0 on the same 10 seeds; OTH with a distinct population | Exact joins and mismatch detection |
| T22 | Mass diagnostics and resolved depth | 765 histories checked, including SEP, D=0 and empty training |
| T23 | Symmetric JSD, diagonal 0, range [0,1], handling of zeros and sum of the contributions | Tests with equal/disjoint distributions and hand-made fixtures |
| T24 | Six probes × 7 folds × 20 seeds × 2 arms, without new fits | 84 evaluations in the new one-seed pilot; final cardinality to be verified |
| T25 | Final number of fits 1,400, no duplicate or omitted seed | Configuration validated; final completeness check |
| T26 | Atomic writing, hashes, correct resumption, rejection of corrupted artifacts | To be implemented and verified with simulated interruption |
| T27 | Tables and figures reconstructible from the per-position outputs | To be verified in the canonical pipeline |
| T28 | No import of `candidates/` or of the inferential utilities in the v3 scientific path; no skipped test-gate | The tests of the preserved statistical utilities remain admitted; inventory of the gates rebuilt |
| T29 | Same dataset/sample: exact repeatability of identities; CE within tolerance across platforms | Reproducibility gate, without a promise of bit-identity of the floats |
| T30 | Consistency of the perimeter and block of the contrasts before certificates and completeness | Rejection of different hashes, absent certificates, missing cells/fits/probes/R1, duplicates and corrupted artifacts; checks of §14.2 |

T08 comprises two distinct campaigns: the earlier synthetic pipeline checked 1,680 derived keys with its own convention; `validate_contract.py` checks 3,360 of them with `hexis-v3-rng-1`, over 20 seeds × 7 held-out × 6 contributors × 4 purposes. They are not the same set automatically doubled by the arms. The results, the version of the derivation and the keys considered remain identified separately. The collision check on these sets does not prove universal absence of collisions.

### 12.1 Frozen synthetic battery

Reuse the generation algorithms and the seeds of the earlier `verify_synthetic.py`, already identified by the hashes of the CTW package. Training 53,304, independent test 100,000, first four targets excluded, five seeds for the small sources. Do not regenerate until passing.

| Source | Rule | Quantitative criterion |
|---|---|---|
| Uniform i.i.d., m=4 | Independent equiprobable draws | \|CE−2\| ≤0.02 |
| Deterministic cycle, m=3 | Periodic succession of three symbols | CE <0.02 |
| Binary Markov 1 | P(same symbol)=0.8 | \|CE−h₂(0.2)\| ≤0.03 |
| Binary lag 2 | P(copy of the symbol at distance 2)=0.9 | \|CE−h₂(0.1)\| ≤0.03 |
| Variable memory | Earlier generator, contexts of length 1/2 | Deviation from the oracle of the realization ≤0.03 |

The implementation of generator, oracle probabilities and seeds is imported as a verifiable fixture from the earlier archive, outside the `candidates/` quarantine; it must not be reconstructed from memory. To make it available without depending on a conversation, the package attached to the plan contains the corresponding reference files. The scripts are evidence and fixtures, not modules to be imported into the scientific pipeline.

m=106 stress: three seeds for uniform i.i.d., lag 2 with copy 0.9 and uniform innovation 0.1, and a frequent binary core plus rare symbols. In the second case the probability of coincidence is `0,9 + 0,1/106`, not simply 0.9: the reference is about 1.13109 bits. Do not require the CTW to reach the oracle with the available sample; require counts, normalization, execution and recording of the gap. Presenting a known deficit as a “passed accuracy test” would be incorrect.

*[Translator's note: the code span `0,9 + 0,1/106` is kept as in the original: 0.9 + 0.1/106.]*

The heterogeneity check and the one on shuffling keep the generators and seeds of the earlier experiments. The thresholds of small residual Q in the known cases verify those synthetic cases; they do not calibrate a significance test on the Greek corpus.

### 12.2 Status of the new executable contract

`validate_contract.py` verified the structure of the plan, sampling and coordinates, and ran 14 paired C0 fits — seven folds, first seed of the new convention — plus one `bound` pair, for **16 fits**. It evaluated the six probes under the two arms of the seven folds, for **84 evaluations**. The result is PASS. No scientific contrasts between groups were produced by this pilot.

`validate_diagnostics.py` verified **765 histories**. The counterexample on the improper cancellation of the roots gives Q≈0.71346, while the shortcut between the CE alone gives about −0.66505: even the sign can be wrong. It is a substantial operational correction adopted in the formulas and in the outputs.

The revision of 12 September re-runs the 16-fit contract under NumPy 2.5.1 and attaches the comparisons between versions, the ablation of the fragments, the synthetic counterexamples, the reaggregation by targets and the tests of rejection of incomplete/corrupted manifests. The results are in `revision_validation.json`, `numpy_*_validation.json`, `scores_validation.json` and `report_validation.json`; the manifests of the report trial are synthetic fixtures, not the results of the 1,400 fits.

These scripts verify the contract and the separate reference; they do not certify the future implementation of the files of the repository. A complete specification can define all the gates, but only the integrated code will be able to pass them.

## 13. Migration of the repository

### 13.1 Single update act

Create the implementation branch from the verified revision, preserving the Git history. Record a decision **V3-001** in a new namespace, so as not to collide with D55 and its technical acts. V3-001 entirely replaces the v2.1 operational design and the A/B proposals for the v3 executions. D01–D54 and the G1/D55 acts remain historical documentation; none of their methodological clauses survives implicitly in conflict with this plan.

Explicitly kept are: immutability of the raw data; provenance; exclusion of `candidates/`; independence of the core from the labels; reproducibility; rejection of silent overwrites; tests with actual assertions. Replaced according to this specification are the selector, the family of analyses, the unit of exclusion, inference, gates and outputs.

The migration package comprises in the same documentary commit: MASTER_SPEC, Decision Log, roadmap, index, handoff, AGENTS/CLAUDE, configuration and registry. The earlier technical ratification of the audit must not be cited as if it had already ratified all the document attributions of the old proposed registry. The new registry reports the verified identities and the grouping conventions decided here.

The attached file `hexis_v3_design.json` carries `FINAL_PLAN_NOT_APPLIED`: it is the delivered structured specification, not an override to be surreptitiously accepted by the old CLI. During the authorized implementation its contents are converted into the v3 schema and the canonical registry is deposited with the status required by the new pipeline, together with the decision V3-001. The ratification check of the previous version is not disabled in order to run v3.

**Mandatory clause of V3-001 — authorized exception to the v2.1 freeze.** Record that the session of 11 September 2026 contains the authorization of the person responsible to verify the change of model on the real data too, before the old G2, keeping the repository intact. That authorization prevails over the earlier operational rule for the isolated pilots; it does not constitute a retroactive passing of G2. Distinguish: date of the authorization/activity reconstructed from the session record; date of the deposit of the act in Git; identifiers of the proofs. The document must not invent the time of the consent if not recorded.

The act includes the campaigns of 203 real C0/sensitivity fits, the order control, the subsequent checks of the contract and the review checks of 12 September, with references to the results and to any re-executions. “203 fits” is not declared the total of every invocation ever made. The re-executions do not become scientific replicates. The attachment `authorization_and_experiments.json` distinguishes documented campaigns, repetitions visible in the session record and the unapplied status of the act. The consent to the revision of 12 September authorizes the modification of the plan and of the attachments, not the implementation in the repository.

**Freeze of the contract in V0.** Deposit the bytes of `hexis_v3_design.json`, their SHA-256 and the hash of the plan as the immutable analytical contract of the version. The external record `design_lock.json` contains the digests without inserting them recursively into the file whose hash is computed. The future application configuration must export an equivalent canonical contract; its analytical projection is compared field by field with the deposited contract, besides the check of the bytes of the reference. A modification of parameters, members of the blocks, seeds, transformations, weights or mandatory results requires a new version and a motivated act. The simple rewriting of a hash does not count as a ratification.

### 13.2 Destination of the existing components

| Path or component | Concrete intervention |
|---|---|
| `src/hexis/conllu_reader.py` | Keep the verified parsing; ensure the required identity, order and coordinates |
| `src/hexis/registry.py` | Apply the Greek registry of 18 prefixes / 17 documents, map of 7 blocks, roles and flags; no heuristics on titles |
| `src/hexis/alphabet.py` | Reuse mapping and audit; complete freeze and inventories with the rules of §4 |
| `src/hexis/sequences.py` | Implement/reset-verify streams, fragments and context-only SEP |
| `src/hexis/config.py` | Replace the presence check with strict validation of the v3 schema |
| `src/hexis/model/context_tree.py` | Implement non-binary CTW, frozen model, log-prior and the API of §11; replace the stubs of the selector |
| `src/hexis/model/diagnostics.py` | Implement resolved/unobserved masses and support; retire the selected depth |
| `src/hexis/protocols/sampling.py` | Implement the attached contract, ledger, subseeds and transformations |
| `src/hexis/protocols/scores.py` | Implement four losses, G, Q, aggregations and probes |
| `src/hexis/manifest.py` | Extend contracts/hashes, atomicity and resumption without mixing versions |
| `src/hexis/pipeline/run_audit.py` | Reuse the audit; separate integrity gates from old methodological states |
| `src/hexis/pipeline/run_encode.py` | Implement coordinates and frozen alphabets |
| `src/hexis/pipeline/run_tree_validation.py` | Connect synthetic and exact tests of the CTW |
| `src/hexis/pipeline/run_confirmatory.py` | Retire from the active path; the new `run_descriptive.py` runs pairs and individual sums; the contrasts belong to `run_report` |
| `src/hexis/pipeline/run_sensitivity.py` | Orchestrate the eight predetermined cells and the paired comparisons |
| New `src/hexis/pipeline/run_report.py` | R1, output validation, figures and descriptive report |
| `run_null_calibration.py`, `run_reference.py`, `run_latin.py` | Retire from the CLI and from the active orchestration |
| `model/lexicon.py`, `blocks.py` for chunks | Retire from the v3 scientific path; do not confuse chunks with dependence_block |
| `stats/permutation.py`, `bootstrap.py`, `holm.py` | Keep the working utilities and the valid tests; mark their historical use, without import in the v3 scientific path nor active inferential entry points |
| `viz/plots.py` | Implement only the six required figures and their provenance |
| `tests/`, `conftest.py`, `pyproject.toml` | v3 inventory without skipped gates; update superseded tests with a motivation, keep valid generic checks |
| `docs/`, `README.md`, `AGENTS.md`, `CLAUDE.md` | Single realignment to the actual scope, models, commands and gates |
| `candidates/` | Remains quarantined, never imported, never collected by pytest |
| Historical results and documents | Kept as v2/pilot, not renamed v3 results |

Retiring a protocol means removing its active entry points and updating the tests that declared it mandatory, leaving a trace of the replacement. It does not mean leaving `pass`, TODO or `NotImplementedError` in a path advertised as usable. No attempt is made to obtain “green” by disabling still relevant checks.

The verified statistical utilities have respectively 94, 74 and 44 lines and do not contain `NotImplementedError`. The migration does not treat them as stubs to be deleted. The historical attestation 327 pass / 17 skip, and the g0/g1 inventories, do not certify the v3 set: rebuild the inventory with a motivated correspondence between tests kept, replaced and retired, without weakening the properties still required.

Before operating on a local copy, take the census of the untracked files and preserve them. The reviewer reports `scripts/reacquire_raw_data.sh`, not available in the verified copy and not recoverable through GitHub: content and date are not attested by this plan. Do not delete it, overwrite it or assume it as a canonical source; verify it in the local copy before any reuse. Its absence from the Git snapshot does not prevent the documentary revision authorized here.

### 13.3 Closure of the old methodological branches

| Earlier theme | Final decision |
|---|---|
| P1, own-regime models and transfer | Retired; no estimate hidden in the probes |
| P2 as a confirmatory test | Replaced by the G/Q and D_Q description, without inference |
| S1, difference of selected depth | Replaced by the diagnostics of §9; no single depth chosen |
| R1 | Kept mandatory, descriptive JSD of the roots |
| Latin/L1 | Outside the study; historical data kept, no new collection |
| Sign-flip, exchangeability, O7, attainable minimum p | Not applicable to v3 because that test is not run; not declared “resolved” for the old design |
| Label permutations, including ranks over the 21 allocations | Retired; no surreptitious reading as evidence of significance |
| Bootstrap, Holm, α | Retired from the family of results |
| Learning curve and test budget | Retired; q_half the only size variation, complete test |
| Quarantine of the candidate | Kept |
| Sentences/fragments, BOS/SEP | Complete contract §§5–7; no `#` in the denominator of the outcomes |
| Alphabet and automatic alternatives | Three predetermined variants; no change of method conditional on the result |
| New manual annotations, neural models, external parsers | Not required for this study |

## 14. Implementation sequence and gates

The v3 gates are new and do not automatically inherit the passing of the v2.1 gates. Linear order: **V0 → V1 → V2 → V3 → V4 → V5**.

| Gate | Work | Verifiable exit criterion |
|---|---|---|
| V0 — Migration of the contract | Deposit V3-001, authorized exception, documents, registry, test inventory and design_lock | Analytical contract frozen by hash; no retired parameter/entry point still mandatory |
| V1 — Corpus and encoding | Audit of hashes, identities, three representations and coordinates | Counts of the expected JSON identical; 7 blocks / 11 primary / 6 probes; all data mapped |
| V2 — Core and protocol | CTW, sampler, shuffling, scores, JSD and persistence | Relevant T01–T23 and T26 passed; exact and synthetic tests complete |
| V3 — Freeze of the execution | Integrated trial with one seed for all 9 cells, resource check, lock and manifest | 126 technical fits completed, 84 C0 probe evaluations; no subsequent methodological change without a new version |
| V4 — Final execution | 1,400 fits, probes, R1, tables and diagnostics | Cardinalities, hashes, slots and aggregations complete; T24–T27 passed |
| V5 — Reproducible delivery | Figures, report, check of a resumption and reproduction of selected cases | T28–T30; document with limits and negative results; no missing artifact |

The V3 trial is not a phase for choosing hyperparameters on the contrasts. It serves to verify the integration of all cells. Finite scores, identities and resources are checked; the official commands emit no contrasts between groups before the completion of V4 and the check of §14.2. The analytical contract is already frozen in V0; V3 freezes implementation and environment. The earlier pilots remain declared.

If V3 is run with the same code, data, configuration and definitive contract and the outputs respect the final schema, its 126 fit partitions can be reused through `--resume`: the unique scientific fits remain 1,400. If a bug that changes a result or a coordinate is corrected, commit/run_id change and those results are not reused. Pilots of different versions are not added together to reach the budget.

### 14.1 Target commands

The final CLI must support at least the following path, to be documented only when implemented:

```bash
uv sync --frozen
uv run pytest -q
uv run python -m hexis.pipeline.run_audit --config config/default.yaml
uv run python -m hexis.pipeline.run_encode --config config/default.yaml
uv run python -m hexis.pipeline.run_tree_validation --config config/default.yaml
uv run python -m hexis.pipeline.run_descriptive --config config/default.yaml --cell C0
uv run python -m hexis.pipeline.run_sensitivity --config config/default.yaml
uv run python -m hexis.pipeline.run_report --config config/default.yaml
```

`run_descriptive` runs both arms and the probes, producing scores per document/block without aggregations between groups. `run_sensitivity` runs all eight cells in the order of the JSON, each with both arms. The report refuses to present a final conclusion if the contract requires missing artifacts. `--resume` is an explicit option of the stages that produce results, with the rules of §11.6.

The current sequence of gates in the repository is not bypassed to run these commands. First V0 is applied, then the new interfaces are implemented and verified. This document is not an instruction to call today entry points not yet present.

### 14.2 Mandatory checks before the contrasts

`run_report` is the only entry point that emits D_Q, the two D_G components, the reaggregations by targets and the contrast plots. Before emitting them it must:

1. Verify the digest of the deposited contract and the correspondence of the application configuration, without modifying the lock automatically.
2. Verify the V0–V3 certificates, bound to the contract, the implementation commit and the lock of the dependencies. V3 is attested externally to the content that identifies the run, so as not to create a circular dependency between certificate and run_id. A correction of the code invalidates the certificate concerning that code.
3. Generate from the contract the expected set of keys `(cell, held_block_key, seed, arm)` and compare it for equality with the 1,400 complete unique keys. Reject missing, additional, duplicate or incomplete keys; checking the total number is not enough.
4. Verify likewise the 1,680 C0 probe evaluations and the R1 outputs of all three variants; verify hashes, schemas, cardinalities of the slots and prescribed denominators.
5. Require for each artifact the outcome of the verification of its bytes against its hash in the manifest; a nominal presence is not equivalent to integrity. The absence or corruption of a single cell prevents both final aggregations.

The individual outputs needed to diagnose a failure remain available, but the command does not write a partial contrast table as a final result. The lists of seeds, the history bands and the number of permutations are those of the contract, without informal overrides. The reference `report_contract.py` and the associated tests demonstrate the rejection of incomplete or inconsistent cases; the reader of the files and the actual verification of their hashes must be integrated into the canonical manifest and subjected to T26/T30.

These checks make the official path verifiable; they cannot prevent a person from computing a contrast independently from the available data. The project keeps a prospective protocol after pilots, without pretending a preregistration preceding the observations.

## 15. Resources, environment and concrete feasibility

### 15.1 Observed measurements

In the separate benchmark with Python 3.12.14, NumPy 2.3.5 and PyYAML 6.0.3: C0 fit of 53,304 tokens about 0.63–0.70 s; held-out evaluation 0.024–0.224 s; evaluation of the whole probe 0.046–0.055 s. C0 peak RSS about 174 MiB; maximum in the real pilots about 240 MiB at D12. No GPU is needed.

The environment of the first audit of the canonical suite used the repository lock and NumPy 2.5.1; the environment of the prototype and of the initial additional contracts used NumPy 2.3.5. They are two distinct environments and must not be confused in a single reproducibility attestation.

**The repository lock is kept**, including NumPy 2.5.1, with Python 3.12 and the dependencies already planned; neither a downgrade to 2.3.5 nor a new pin of PyYAML is imposed to align with the prototype. In the check of 12 September, seven folds per version and 42 sampled contributions per version gave identical hashes between NumPy 2.3.5 and 2.5.1 for ledgers, permutations, models and scores. The scripts and the digests are attached. The comparison took place on the same host and Python runtime: it does not certify all platforms or the whole application stack.

PCG64 has compatibility guarantees for its own stream, but not every transformation of `Generator` has a universal guarantee across versions; therefore vectors and empirical tests are kept. [NumPy compatibility](https://numpy.org/doc/stable/reference/random/compatibility.html). `uv sync --frozen` must use the lock identified in the contract; the gates run the whole suite and the integrated trials under that environment. If a test fails, stop and diagnose before changing dependencies: no automatic resolution or version substitution. A necessary change of the lock is motivated and versioned and invalidates the earlier certificates. No CTW library is added.

### 15.2 Execution and disk budget

For 1,400 fits, a prudent estimate on the same order of hardware is **20–60 minutes** for computation and support operations. It is a projection from the prototype, not a measured time of the complete pipeline. Parquet writes, rendering and the conditions of the machine can affect it. Sequential execution as default; parallelism not necessary.

The `oth` primary positions are 109,716, against 109,108 in C0. With the eight sensitivities, C0 and the probes, the outputs contain **12,704,540 paired rows**. Eight float64 and 12 bytes of identifiers per row require about 921 MiB, before metadata, null validity and indices. Compression can reduce the space but is not a guarantee. Reserve **10 GB of free space** for inputs, partitions, temporaries and results; a machine with **8 GB of RAM** is a prudent endowment for sequential execution. A measured minimum requirement of 8 GB is not declared: the isolated model uses much less.

The losses must be written per partition, without concatenating all results in a single DataFrame in memory. Not all trees are stored. The peak must be measured in the integration; an unforeseen growth requires correcting the use of memory, not reducing cells, blocks or seeds a posteriori.

The earlier estimate of about 100 MiB concerned six float64 vectors for the 2,182,160 original C0 positions alone. The estimate of about 921 MiB instead concerns 12,704,540 paired rows, all cells and probes, with eight float64 and four identifiers (12 bytes in all). They are different schemas and populations; neither figure is the measure of the total memory of the process.

### 15.3 Residual human and technical work

Planning estimate, not an empirical measure: about **8–13 days of concentrated work** for a competent implementer using the available proofs: 1–2 days for migration/data; 2–3 for core and protocol; 2–3 for outputs/tests; 1–2 for integration and reproducibility; 2–3 for report and scientific review. The calendar depends on familiarity with the code. The dominant cost is controlled integration, not training.

The perimeter requires no new annotations, enlargement of the corpus, GPU access or neural training. These are the concrete reasons why the downsizing is feasible. Acceptance remains based on the gates, not on the obligation to respect a time forecast.

## 16. Rules for the scientific conclusion

Technical completion is independent of the sign and size of D_Q. The project concludes successfully if the protocol is executed correctly and the report faithfully describes the results, even when the difference between groups is small, inconsistent across blocks or sensitive to the encoding.

| Observed situation | Permitted conclusion |
|---|---|
| Original G positive, shuffled G similar | The gain of the CTW does not clearly distinguish the observed order from the chosen control |
| Q positive in the blocks, small difference between groups | Order offers an advantage under the predictor, without a marked descriptive separation between the available groups |
| D_Q consistent in sign across the sensitivities | Description stable with respect to the perturbations performed, without causal or population inference |
| D_Q changes sign or size in the sensitivities | The comparative conclusion depends on the analytical choices; show all cells |
| D6, D8 and D12 almost equal | Greater depth does not improve performance in the sample/protocol; not absence of deep linguistic dependencies |
| `upos_only` and C0 differ | Results dependent on the level of representation; no automatic identification of the causal contribution of DEPREL |
| Heterogeneous tragic probes | The original comparison does not define a uniform property of “verse”; no additional category is trained |
| High JSD with similar Q | Marginal differences of the symbols, without a corresponding difference in the measured order advantage |

The report must expose, next to the main result: composition of the corpus; 2 HEX blocks against 5 prose blocks; chronological confounding; leave-one-block-out training balanced by block but not by regime; offline annotations; shuffling conditional on the per-sentence composition; seed variability as computational variability; earlier observation of the pilots.

Do not use “absence of effect” without specifying the measured effect and the resolution limit; do not turn a seed SD into uncertainty about the ancient texts. Do not use the term “confirmatory” for the v3 design. A datum is not considered invalid because it makes the narrative less sharp.

## 17. Materials to be delivered at the end of the implementation

1. v3 repository with the freeze commit, complete tests and locked dependencies.
2. Corpus registry with identities, blocks, flags and sources; three alphabets and audit of the removals.
3. Configuration of the nine cells, ledgers, manifests and verified per-position/aggregate outputs.
4. Six figures, complete tables and scientific report with the central result D_Q and its components.
5. Reproduction instructions in a new folder, hash verification and resumption of an interrupted partition.
6. Archive of the pilots and of the decision path, to distinguish methodological development and final analysis.

The raw data remain immutable and are not added to the repository. The provenance and the licence indication of the treebank are kept. The acquisition scripts use the pinned commit and hashes. Any external publication is an act subsequent to the verification of the results; this plan neither publishes nor modifies the project.

## 18. Sources and actual use

- **HEXIS repository**, revision `852644b…`: state of the code, specifications and proposed registry examined. [Snapshot](https://github.com/leonardotornabene/HEXIS/tree/852644b6917790877c7b2ca5df2e76b17829d87c).
- **UD Ancient Greek Perseus r2.18**, revision `37837c7…`: corpus actually counted and used in the pilots. [Snapshot](https://github.com/UniversalDependencies/UD_Ancient_Greek-Perseus/tree/37837c7a3c592c9563f8c51cc63344b87247f8a5).
- **AGDT 2.1**, revision `bf4334f…`: inventory and bibliographic metadata of the sources; it does not replace the UD data in the fits. [Description](https://github.com/PerseusDL/treebank_data/blob/bf4334f0af5e13d16b04c1cccd6237e683ac6f5f/v2.1/Greek/README.MD). Links to the four verified XML files in the JSON attachment.
- **Kontoyiannis, Mertzanis, Panotopoulou, Papageorgiou and Skoularidou**, *Bayesian Context Trees: Modelling and exact inference for discrete time series*, version 3, 2022: CTW/BCT foundation and prior on the models. [Text](https://arxiv.org/abs/2007.14900v3). The HEXIS handling of boundaries and frozen score is specified and validated here, not attributed in full to the source.
- **Galves, Galves, García, Garcia and Leonardi**, *Context tree selection and linguistic rhythm retrieval from written texts*, Annals of Applied Statistics 6(1), 2012, 186–209, DOI 10.1214/11-AOAS511: direct precedent on variable contexts and rhythm; model selection on rhythmic encodings of Portuguese. [Verified text](https://arxiv.org/pdf/0902.3619).
- **Vanessa B. Gorman and Robert J. Gorman**, *Approaching Questions of Text Reuse in Ancient Greek Using Computational Syntactic Stylometry*, Open Linguistics 2, 2016, 500–510, DOI 10.1515/opli-2016-0026: syntactic stylometry of Greek with features of paths in the trees, distinct from the label sequences of HEXIS. [Authors' deposit](https://digitalcommons.unl.edu/historyfacpub/208/).

- **Schürmann and Grassberger**, *Entropy estimation of symbol sequences*, Chaos 6, 1996, 414–427; arXiv 2002: estimation from finite sequences and motivation of the convergence/support checks. [Text](https://arxiv.org/abs/cond-mat/0203436).
- **Lin**, *Divergence Measures Based on the Shannon Entropy*, IEEE Transactions on Information Theory 37(1), 1991, 145–151: JSD; supplied PDF `jensen-shannon.pdf`.
- **de Marneffe, Manning, Nivre and Zeman**, *Universal Dependencies*, Computational Linguistics 47(2), 2021, 255–308, DOI 10.1162/coli_a_00402: nature of the annotation level; supplied PDF `coli_a_00402.pdf`.
- **Herrera, Silai, Guillaume and Kahane**, *Extraction of Contrastive Rules from Syntactic Treebanks: A Case Study in Romance Languages*, QUASY 2025, 26–38: limits of the comparability of treebanks; supplied PDF `2025.quasy-1.5v1.pdf`. Their test protocol is not imported into the HEXIS design.
- **Gianitsos, Bolt, Chaudhuri and Dexter**, *Stylometric Classification of Ancient Greek Literary Texts by Genre*, 2019: precedent that prevents generic claims of novelty on the quantitative prose/verse distinction. [Article](https://aclanthology.org/W19-2507/).

The research documents and the other supplied PDFs constitute the theoretical and historical context of the project. They are not used as empirical proof of the software feasibility or as certification of the new formulas. No operational conclusion depends on the authority of an author or on an unverified claim contained in the proposals.

## 19. Final attestation of the plan

The plan resolves the decisions on corpus, representation, units, sampling, predictor, order control, measures, weights, sensitivities, probes, JSD, outputs, migration and acceptance. The executable reference shows that the core can operate at the real dimensions of the project and that the new contracts have verified examples.

**The feasibility judgement is favourable for this perimeter.** The document is ready to guide the implementation. It is not equivalent to a certification of code not yet integrated, to a promise of positive results or to the absolute absence of scientific limits. The limits that affect the interpretation are incorporated into the question and the protocol, instead of being left as objections to be faced after the computation.

The normative attachments are `hexis_v3_design.json`, `corpus_atteso.json` and the contracts described in the README of the package. The text governs the semantics; the JSON governs the list and the values of the cells and of the registry. Any divergence between the two is an error of the package to be corrected before the implementation, not a faculty of choosing the preferred value.
