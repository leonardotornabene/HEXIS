# MASTER TECHNICAL SPECIFICATION — PROJECT HEXIS

**Hexameter Information Signature: morphosyntactic organization under metrical constraint, measured by a single Rissanen-style MDL context-tree instrument** Version 2.0 — 2026-07-06 — Language: English (AI-facing). Supersedes v1.0 (2026-07-05, archived in `archive_v1/`). Companion documents: `02_DECISION_LOG.md` (binding decisions D01–D39), `03_ROADMAP_OPERATIVA_IT.md`, `04_AI_HANDOFF_PROMPT.md`.

**What changed in v2.0 (summary).** The design is consolidated around a **single statistical instrument**: a variable-memory MDL context-tree model (Rissanen-style, per Schürmann & Grassberger 1996 §V). The v1.0 battery of independent estimators (per-chunk entropy with Miller–Madow, standalone conditional entropy, mutual information with shuffle baselines, MI-decay profiles, chunk-level JSD machinery) is retired as confirmatory apparatus: low-order quantities are *smoothed truncations of the context-tree model itself* and appear only as diagnostics or optional appendix material. The confirmatory family shrinks to two document-level statistics (P1 transfer asymmetry, P2 context-gain differential), increasing power under Holm–Bonferroni. Governing decisions: D32–D39. **No confirmatory analysis had been run on real data at the time of this change** — the consolidation is a pre-data design decision, which must be stated in the preprint (no forking-paths concern).

## 0. HOW TO USE THIS DOCUMENT (instructions to AI assistants)

1. This specification and the Decision Log are **binding**. Do not deviate silently. If a deviation seems necessary, propose an explicit amendment to the Decision Log (question → proposal → rationale → consequences) and wait for the project owner's approval.

2. Epistemic labels: **[VERIFIED 2026-07-05]** / **[VERIFIED 2026-07-06]** = checked against the cited primary source on that date; **[FROM PROPOSAL]** = asserted in the original research proposal, re-verify where flagged; **[ASSUMPTION]** = explicitly labeled working assumption; **[GATED:G1]** = finalized at gate G1 (corpus audit) by a pre-registered rule.

3. Notation: `log` = log base 2 everywhere; entropies and code lengths in **bits**. Alphabet `A`, symbols `a ∈ A`, sequence `x_1 … x_N`, document `d`, regime `R`, model `M`. Confirmatory statistics `P1, P2`; secondary `S1`; optional `R1`; Latin replication `L1`.

4. **Claim discipline.** Nothing here claims physical emergence, phase transitions, or symmetry breaking. Licensed framing: *poetry and prose as different regimes of symbolic organization; the poetic regime is subject to a strong formal constraint; the project tests whether that qualitative distinction leaves a measurable signature in the predictive organization of morphosyntactic sequences.* Complex-systems references are conceptual, not operational.

5. **Model-misspecification discipline (new in v2).** The context tree is a *universal-coding measuring instrument*, not a model of the true generative process of language. Its sequential code lengths are operational quantities (upper bounds, in expectation, on entropy rates); all comparisons are between code lengths under one fixed, uniformly applied model class. The project makes **no claim that natural language is a finite-memory / variable-length Markov source**; Chomsky (1956) is the conceptual anchor for this limitation and must never be cited as operational justification for the method (that role belongs to Schürmann & Grassberger 1996 and the VLMC statistics literature). See §10 and D39.

6. Correctness > speed. Reproducibility > sophistication. Every computed number traces to data version + config hash + code commit + seed (§6.5).

## 1. SCIENTIFIC SCOPE (v2 architecture)

### 1.1 Research question (operational form)

Given texts represented as sequences of morphosyntactic symbols (UPOS+DEPREL from Universal Dependencies), fit one family of variable-memory MDL context-tree models and ask whether the hexameter and prose regimes differ measurably in the **predictive organization** of their sequences, read at three depths of the same instrument: - **root (order 0):** symbol distribution — descriptive reading; optional JSD appendix (R1); -**context gain (order ≥ 1):** how many bits/symbol the past buys over the root — confirmatory statistic **P2**; - **full model (transfer):** how well regime-specific predictive structure transfers across regimes — confirmatory statistic **P1**; plus selected-depth profile — secondary **S1**.

### 1.2 Confirmatory statistics, sidedness, and family (pre-registered; D33)

| ID | Statistic (exact definition in §4.4) | Test (exact scheme in §5.2) | Sidedness | Role |
| --- | --- | --- | --- | --- |
| P1 | Mean over evaluation documents of `ΔCE(d) = CE(d\|other regime) − CE(d\|own regime)`, LODO + T*-matched | Exact sign-flip over documents (`2^11 = 2048`, Greek) | One-sided (`> 0`); two-sided also reported | Confirmatory |
| P2 | Difference in document-mean held-out context gain `G(d)` between regimes, `G` computed under label-free pooled LODO models, positions with available context ≥ 4 | Exact document-label permutation (`C(11,5) = 462`, Greek) | Two-sided | Confirmatory |
| S1 | Difference in document-mean selected context depth `D̄(d)`, same label-free protocol and position restriction | Same permutation | Two-sided | Secondary (no α) |
| R1 | JSD between the two regimes' root distributions | Document permutation | One-sided | Optional appendix (no α) |
| L1 | Qualitative replication of P1/P2 signs and CIs on Latin | Exact schemes at Latin sizes (§5.7) | Qualitative | Subordinate |

Family for Holm–Bonferroni at α = 0.05: `{P1, P2}` (thresholds 0.025 / 0.05). Everything else carries no α and is labeled exploratory/secondary. Rationale for the two-statistic family: P1 and P2 target the two distinct claims (transferability of structure; amount of sequential information), are the most robust readings (bits; document-level; position-controlled), and a small family maximizes power — the binding constraint of this corpus. Depth (S1) is demoted because it is the reading most sensitive to parameterization (`d_max`, `k_min`).

### 1.3 Mapping to the proposal's hypotheses (continuity; D33)

H1 (distributional) → root-level descriptive reading + optional R1. H2 (sequential) → **P2** (re-operationalized: context gain *is* the sequential-organization question, order-adaptive instead of order-1). H3 (predictive) → **P1** + S1. H4 (cross-linguistic) → **L1**. The proposal's questions are preserved; their operationalization is consolidated into one instrument. The preprint states this evolution explicitly (§10).

### 1.4 Contrast structure (unchanged from v1)

**Primary (Greek):** HEX vs PROSE_CLASS.

**Auxiliary/exploratory (Greek):** OTHER_VERSE (tragedy) as *specificity check* — if tragedy patterns with HEX, the signature is verse-general; if with prose or intermediate, more meter-specific. PROSE_POST as chronological-robustness set.

**Primary (Latin):** HEX vs PROSE_ALL (union; corpus size forbids a period split).

Claims are about *this corpus*; dialect, epoch, genre, annotation policy and annotation quality are named confounds (§5.8). "Prosa coeva" is operationalized as *classical prose* — the earliest substantial Greek prose in existence; strict coevality with archaic epic does not exist and this is stated openly.

## 2. CORPUS FACTS AND PROVENANCE (carried over from v1; all [VERIFIED 2026-07-05] unless noted)

### 2.1 Sources and versions

Universal Dependencies release: **v2.18** (both treebank pages link "Download all treebanks: UD 2.18"). Pin this release (D03); if a newer release exists at download time, pin the newest and record it; never mix releases.

Treebanks: `UD_Ancient_Greek-Perseus` (`grc_perseus`), `UD_Latin-Perseus` (`la_perseus`).

Pages: https://universaldependencies.org/treebanks/grc_perseus/index.html, https://universaldependencies.org/treebanks/la_perseus/index.html Repos: https://github.com/UniversalDependencies/UD_Ancient_Greek-Perseus, https://github.com/UniversalDependencies/UD_Latin-Perseus Both are automatic conversions of the Ancient Greek and Latin Dependency Treebank (AGLDT) 2.1 (Perseus); morphology/lemmatization semi-automatic (Morpheus), **syntactic annotation manual**, UD conversion by G. G. A. Celano.

License: **CC BY-NC-SA 2.5** both. Consequences (D28): research use fine; **no data redistribution** in the repository; `data/raw/` gitignored; publish code + derived statistics only.

### 2.2 Verified statistics

|  | `grc_perseus` | `la_perseus` |
| --- | --- | --- |
| Sentences | 13,919 | 2,273 |
| Tokens | 202,989 | 28,868 tokens; 29,223 syntactic words |
| Multiword tokens | None reported | 355 (clitic univerbation: `que`, `ue`, …) → parser **MUST** expand MWTs; sequences use syntactic words (§3.2) |
| UPOS used | 15/17: ADJ ADP ADV AUX CCONJ DET INTJ NOUN NUM PART PRON PUNCT SCONJ VERB X (no PROPN, no SYM) | 16/17: adds PROPN; no SYM |
| DEPRELs | 28 types, 1 subtype (`nsubj:outer`); not used: `expl`, `dislocated`, `clf`, `fixed`, `flat`, `compound`, `list`, `goeswith`, `reparandum`, `dep` | 20 subtypes (`acl:relcl`, `advcl:abs/cmp/pred`, `advmod:emph/lmod/neg/tmod`, `aux:pass`, `ccomp:reported`, `conj:expl`, `csubj:pass`, `det:numgov`, `flat:name/redup`, `nsubj:outer/pass`, `nummod:gov`, `obl:arg/cmp`) + base `flat`, `discourse`, `orphan`, `vocative`, `punct`; not used: `expl`, `dislocated`, `clf`, `fixed`, `compound`, `list`, `goeswith`, `reparandum`, `dep`; `iobj` present but marginal (README: replaced by `obl` / `obl:arg`) |

### 2.3 Document registry and regime taxonomy (labels: HEX | PROSE_CLASS | PROSE_POST | OTHER_VERSE | EXCLUDED)

Assignments from the verified works tables; `sent_id` -prefix mapping finalized at Gate G1 (§3.3).

**Greek:** HEX = Homer *Iliad*; Hesiod *Theogony*, *Works and Days*, *Shield of Heracles*; *Hymn to Demeter* (listed under both "Anonymous" and "Pseudo-Homer" — audit resolves whether duplicate; merge if so). OTHER_VERSE = Aeschylus ×7 (*Agamemnon, Eumenides, Libation Bearers, Prometheus Bound, Persians, Seven Against Thebes, Suppliant Women*), Sophocles ×5 (*Ajax, Antigone, Electra, Oedipus Tyrannus, Trachiniae*) — tragedy is metrically mixed (iambic trimeter + lyric): it operationalizes "non-hexameter verse", not one meter. PROSE_CLASS = Herodotus; Thucydides; Lysias ×4 (*Against Pancleon; Alcibiades 1; Alcibiades 2; On the Murder of Eratosthenes*). PROSE_POST = Polybius; Diodorus Siculus; Plutarch ×2 (*Alcibiades, Lycurgus*); Athenaeus; Apollodorus; Aesop (flag `dating_uncertain`).

**Latin:** HEX = Vergil *Aeneid*; Ovid *Metamorphoses*. PROSE_CLASS = Cicero *In Catilinam*; Sallust *Bellum Catilinae*; Augustus *Res Gestae* (flag `epigraphic`). PROSE_POST = Tacitus *Historiae*; Suetonius *Life of Augustus*; Petronius *Satyricon* (flag `verse_insets`; audit checks whether verse portions are in the sample; sentence-level exclusion if identifiable). OTHER_VERSE = Propertius *Elegies* (elegiac couplets); Phaedrus *Fabulae* (iambic senarii). EXCLUDED = Jerome *Vulgata* (late-antique translation; UD genre "bible").

**Analysis sets:** GRC-HEX (5 docs, Hymn merged), GRC-PROSE:= PROSE_CLASS (6 docs), GRC-TRAG, GRC-PROSE-POST; LA-HEX (2), LA-PROSE:= PROSE_CLASS ∪ PROSE_POST (6), LA-OTHERV. Registry schema per document: `language, doc_id, source_urn, author, work, regime, meter, period,` `n_sentences, n_tokens_raw, n_tokens_retained, flags`.

### 2.4 UD splits are ignored (D03)

Concatenate train/dev/test, re-derive documents from `sent_id` / `newdoc`; all analysis splits are document-level. Prevents leakage in the LODO protocols (§4.2).

### 2.5 Acquisition and provenance protocol

```text
git clone https://github.com/UniversalDependencies/UD_Ancient_Greek-Perseus.git
git clone https://github.com/UniversalDependencies/UD_Latin-Perseus.git
```

```text
cd <repo> && git checkout r2.18     # confirm tag; else the tagged release matching the
pinned version
git rev-parse HEAD                   # record commit SHA in data/raw/PROVENANCE.md
shasum -a 256 *.conllu               # record file hashes
```

`data/raw/PROVENANCE.md` records URLs, tag, commit SHAs, SHA-256 per file, download date, downloader. Raw data immutable, gitignored; only PROVENANCE.md committed.

### 2.6 Errata to the proposal (correct in the preprint)

E1: grc_perseus contains far more than the proposal lists — 12 tragedies and six post-classical prose authors [VERIFIED]; exploited as the three-regime design.

E2: la_perseus additionally contains Jerome, Propertius, Phaedrus, Petronius, Suetonius, Augustus [VERIFIED]; **Caesar is absent**.

E3: la_perseus has 355 multiword tokens requiring expansion [VERIFIED]; unaddressed in the proposal.

E4: Latin `flat` / `flat:name` / `flat:redup` unaddressed by the proposal's mapping; rule added (D09).

E5: "3 Greek / 6 Latin treebanks" (proposal §2.2/§5.2) — re-verify against the UD v2.18 index at G1 (open item O1).

E6: proposal §6.3 footnote misattributes the Rissanen suffix tree to reference 2 (Mansilla & Bush); correct reference is Schürmann & Grassberger. "Rinassen" in H3 is a typo for "Rissanen".

E7 (confirmations): 202,989 tokens ✓; "15 UPOS, 28 DEPREL" ✓; Latin ≈ 29k ✓; Thucydides present ✓.

**E8 (new, v2):** the proposal's implicit novelty claim must be repositioned. Prose/verse discrimination from POS-based features in Latin is a solved, easy classification task (Chen et al. 2024, ML4AL [VERIFIED 2026-07-06]); context-tree model selection has already been used for linguistic rhythm (Galves et al. 2012, Ann. Appl. Stat. [VERIFIED 2026-07-06]). The defensible contribution is: **morphosyntactic (UPOS+DEPREL) representation + metrical-constraint framing + adaptive-memory predictive instrument + cross-regime transfer + Greek/Latin comparison** — with both papers cited and differentiated in related work (D39; registry in `03_ROADMAP` appendix).

## 3. DATA PIPELINE SPECIFICATION

### 3.1 Environment

Python 3.12 via `uv`. Pinned deps (frozen in `uv.lock` at G0): `numpy`, `pandas`, `pyarrow`, `conllu`, `scipy`, `matplotlib`, `pyyaml`, `pytest`. No GPU. Compute budget quantified in §5.6: full confirmatory + sensitivity plan ≈ a few laptop-hours.

### 3.2 CoNLL-U parsing rules (unchanged from v1)

Use the `conllu` library (or equivalent validated streaming parser). Per sentence: read `sent_id` (mandatory —fail loudly if absent) and `newdoc id` if present; **skip MWT range lines (** `i-j` **), keep syntactic-word rows** (expands Latin clitics); **skip empty nodes (** `i.1` **)**; required columns `ID, FORM, UPOS, HEAD, DEPREL`; validate UPOS in the UD tag set and DEPREL non-empty; on violation raise with file, sent_id, token id. Surface order = CoNLL-U ID order. Sentence = CoNLL-U sentence (editorial segmentation; verse boundaries are NOT encoded — out of scope v1 of the pipeline, D11; sentence-length differences between regimes are handled by the position restriction in §4.4, D35).

### 3.3 Document identity (unchanged)

Derive `doc_id` from `sent_id` prefixes (Perseus URN-style) and/or `newdoc id`. G1 procedure: enumerate all prefixes with sentence/token counts → human-verified `config/registry_overrides.yaml` assigning `(author, work, regime, meter, period, flags)`, cross-checked against §2.3. Audit fails on any unassigned sentence. Hymn-to-Demeter duplication resolved here (O2).

### 3.4 Alphabet mapping (total function; order of operations normative; unchanged from v1)

Given raw `(UPOS_raw, DEPREL_raw)`: 1. `deprel_base = DEPREL_raw.lower().split(":")[0]` — one rule implements every subtype mapping in the proposal and all 20 Latin subtypes verified (acl:relcl→acl, advcl:abs→advcl, advmod:neg→advmod, aux:pass→aux, nsubj:pass/outer→nsubj, obl:arg/cmp→obl, ccomp:reported→ccomp, conj:expl→conj, det:numgov→det, nummod:gov→nummod, advmod:emph/lmod/tmod→advmod, advcl:cmp/pred→advcl, flat:name/redup→flat). 2. `PROPN → NOUN` (Latin only; Greek has no PROPN [VERIFIED]). 3. Retain iff UPOS ∈ {ADJ, ADP, ADV, AUX, CCONJ, DET, NOUN, NUM, PART, PRON, SCONJ, VERB} (12); delete tokens with UPOS ∈ {PUNCT, X, INTJ, SYM} (drop_reason `upos_excluded`; D05). 4. Retain iff `deprel_base` ∈ {root, nsubj, csubj, obj, iobj, ccomp, xcomp, obl, advcl, advmod, acl, amod, appos, det, nummod, nmod, case, mark, aux, cop, cc, conj, parataxis} (23). Any other base deprel on a retained-UPOS token (`discourse`, `vocative`, `orphan`, `flat`, `dep`, anything unexpected) → **excluded-deprel policy** (D06): PRIMARY = delete (drop_reason `deprel_excluded:<label>`); SENSITIVITY = map to catch-all `oth` (`UPOS:oth`). 5. `symbol = f"{UPOS}:{deprel_base}"`. Max |A| = 12 × 23 = 276 (+12 `UPOS:oth` in the sensitivity arm). Frozen alphabet = symbols observed at G1; integer ids by descending pooled frequency; persisted to `data/processed/alphabet.json`.

**UPOS-only alphabet (mandatory robustness arm, D31):** `symbol = UPOS` (12 symbols). All confirmatory statistics replicated on it: DEPREL annotation quality is expected lower for poetry (non-canonical order; proposal §8.4), and treebank annotation policies differ (e.g. Perseus-vs-EvaLatin DET usage documented by Chen et al. 2024). Convergence across alphabets is itself a reported result.

**Audit gates at G1 (pre-registered; D06/D09):** full raw UPOS×DEPREL contingency per document and regime; drop-rate tables by rule and label. **GATE-A:** any excluded category > 2% of raw tokens in any regime → both policies (drop / `oth`) become co-primary sensitivity and the imbalance is discussed (vocatives plausibly genre-skewed: epic invocations). **GATE-B:** any document with < 70% retention flagged for inspection.

### 3.5 Sequence semantics and boundary policy (unchanged)

Object of study for document d: ordered list of sentences, each a tuple of retained symbols in surface order; deletions close gaps. **P-RESET (primary, D10):** all contexts truncate at sentence start; no cross-sentence statistics. **P-BOUND (sensitivity):** concatenation with explicit boundary symbol `#` added to the alphabet; no reset.

### 3.6 Block segmentation (descriptive only; replaces v1 chunking — D34)

The v1 chunk layer is **removed from all inference** (chunk-level statistics no longer exist in the design). A minimal utility `make_blocks(doc, n_block=1000, min_frac=0.5)` (sentence-aligned greedy fill, blocks never span documents) is retained **only** for one descriptive figure: within-document held-out CE profiles along the two largest documents (F7). No block-level tests, no block permutation, no chunk-size sensitivity axis.

### 3.7 Intermediate data formats (Parquet)

`tokens.parquet`: `language, doc_id, sent_id, token_ord, upos_raw, deprel_raw, upos,` `deprel_base, symbol_id (int16, −1 if dropped), kept (bool), drop_reason (str|null)`.

`sequences.parquet`: `language, doc_id, sent_ord, symbols (list<int16>)` — retained symbols only.

`alphabet.json`: `{symbol: id}` + variant tag (`ud23`, `ud23_oth`, `upos_only`), creation date, config hash.

`scores/*.parquet`: per-document score tables produced by §4.4 protocols (schema in §6.2). Every derived file carries a `manifest.json` sidecar (§6.5).

## 4. THE INSTRUMENT AND ITS READINGS (all logarithms base 2; all quantities in bits)

### 4.1 Model class and estimator (the core; carried from v1 §4.6, unchanged algorithmically)

**Status and correspondence.** Fully specified variant of Rissanen's Context algorithm, consistent with the adaptive-context description in Schürmann & Grassberger (1996) §V.A–B (arXiv:cond-mat/0203436; Chaos 6(3):414–427) and with the VLMC literature (Rissanen 1983; Bühlmann & Wyner 1999). **Task T5.1** (roadmap Phase 2): read SG96 §V line-by-line; record any divergence between published estimator/penalty and these defaults as D18-A1; provide a config preset reproducing the published choices. Scientific claims rest on *a well-**defined MDL context model applied uniformly to all regimes*, not on numerical replication of the 1996 paper (D18). CTW (Willems–Shtarkov–Tjalkens 1995) is an optional robustness comparator (no selection step ⇒ checks that conclusions are not artifacts of the selection rule).

**Parameters (config** `context_tree:` **):** `d_max = 8`, `beta = 0.5` (add-β, Krichevsky–Trofimov-style), `k_min = 2`, `gamma = 0.0` bits, `select = monotone`. Sensitivity (§5.6): β ∈ {1/|A|, 0.25, 1.0}, d_max ∈ {6, 12}, select = argmax.

**Data structure.** Trie over *reversed* contexts; root = empty context; child of node s under symbol σ = context (σ·s), one symbol deeper into the past. Node fields:

```text
counts: dict[symbol -> int]   # n_s(a): times context s was followed by a (so far)
total:  int                   # N_s
L_self: float                 # accumulated sequential code length of symbols emitted under
```

```text
s
L_par:  float                 # code length the PARENT's predictor assigned to those same
symbols
children: dict[symbol -> Node]
```

Predictive probability (pre-update counts): `P_s(a) = (n_s(a) + β) / (N_s + β·|A|)` — never zero; |A| = frozen alphabet size for the (language, variant); at β = 0.5 and |A| ≈ 150 the pseudo-mass is β|A| ≈ 75, i.e. deep, rarely-visited nodes stay heavily smoothed until they earn their keep — that is the implicit MDL model cost at work.

**Training pass (single, prequential).** For each sentence, for each position t with symbol x and within-sentence past (truncated at sentence start under P-RESET):

```text
path = [root]; node = root
for depth in 1 .. min(available_past, d_max):
```

```text
    σ = symbol at distance depth in the past
    node = node.children.setdefault(σ, new Node)     # grow on first visit
    path.append(node)
p_prev = None
```

```text
for depth, node in enumerate(path):                   # predict-then-update, PRE-update
counts
    p = P_node(x); node.L_self += −log2(p)
    if depth > 0: node.L_par += −log2(p_prev)
```

```text
    p_prev = p
for node in path: node.counts[x] += 1; node.total += 1
```

**MDL efficiency:** `Δ(s) = L_par(s) − L_self(s)` = bits saved, on exactly the positions where s applied, by using s instead of its parent. Both code lengths are prequential, so parameter cost is implicit (early-visit redundancy of add-β coding); hence `Δ(s) > γ` **is** the MDL rule; no separate penalty is added (γ = 0 default; γ > 0 = stricter margin).

**Selection at a position** with matching path s₀ ⊂ … ⊂ s_k: s *= deepest s_j with, for every i = 1…j,* `total(s_i)` `≥ k_min` *and* `Δ(s_i) > γ` *(monotone-stop**). Variant `argmax` (deepest prefix maximizing Σ Δ) implemented for sensitivity.

**Complexity:** O(N·d_max) time, ≤ O(N·d_max) nodes. Pure-Python first; a fit at N ≈ 40–60k tokens, d_max = 8 costs ≈ 1–3 s [ASSUMPTION, profiled at G0]; vectorize only if profiling demands.

### 4.2 Fitting protocols (three, all document-level; D36)

Let the primary-contrast document set be 𝔻 = HEX ∪ PROSE (Greek: 5 + 6 = 11 docs). All training subsamples draw **whole sentences uniformly without replacement until ≥ T* retained tokens**; S = 20 seeds per condition (seed derivation §6.5); seed-mean reported with sd. - **(a) Reference models** (descriptive only): one per regime, fit on ALL its documents, full data, no LODO. Used for §4.5 readings and R1. Never used for confirmatory statistics. - **(b) Regime LODO models** (for P1): for evaluation document d and training regime R_tr ∈ {HEX, PROSE}: pool = docs of R_tr minus d (if R_d = R_tr); subsample to T*; fit; evaluate d. - (c) Pooled LODO models (for P2/S1; label-free by construction): for evaluation document d: pool =* 𝔻 *\ {d} —* no regime information used anywhere*; subsample to T*; fit; evaluate d. **T* (GATED:G1):** T* = min over ALL training conditions in (b) and (c) of available retained tokens (the binding condition is expected to be "HEX minus Iliad"). One T* per language, used uniformly across (b) and (c) so that gain and CE are size-comparable. Contingency (pre-registered): if T* < 15k retained tokens, record D-amendment and add learning-curve emphasis (below). **Learning curves (descriptive):** CE(d|R_tr) vs training size T ∈ {5k, 10k, 20k, T*} for representative documents — makes the size-dependence of every conclusion visible (F8).

### 4.3 Evaluation semantics (frozen tree; no updates)

Walk the matching path; select s *by the frozen rule;* `codelen(t) = −log2 P_{s*}(x_t)` *. Fallbacks:** context prefix absent from the tree → deepest existing ancestor satisfying the rule (root always exists); symbols unseen in training → β-smoothing (never zero). Per-position record: `(depth_selected, depth_matched,` `available_past, codelen_root, codelen_selected)`. Coverage statistics reported per evaluation: unseen-context rate, distribution of depth_matched vs depth_selected.

### 4.4 Score functions (exact definitions; the confirmatory layer)

For evaluation document d with N_d evaluated positions: - **CE(d | R_tr)** = seed-mean of (1/N_d) Σ_t codelen_selected(t) under protocol (b). **ΔCE(d) = CE(d | other) − CE(d | own)**; > 0 ⇒ own-regime advantage. **P1 = mean_d ΔCE(d)** over all 11 evaluation documents. No position restriction: ΔCE is a within-document difference, so position/sentence-length effects cancel between the two models. - **Context gain** at position t under a pooled LODO model (protocol c): `g(t) = codelen_root(t) − codelen_selected(t)` ≥ 0-ish (can be negative at k_min/γ boundaries; keep signed), where codelen_root uses the SAME fitted model's root predictor. **Position restriction (D35):** the primary gain statistic uses only positions with `available_past ≥ 4` (i.e., at least the 5th retained token of its sentence). Rationale: under P-RESET, early positions mechanically lack context; if regimes differ in sentence length (editorial segmentation!), unrestricted means would confound gain with sentence length. The unrestricted variant is a sensitivity cell; the fraction of qualifying positions per regime is reported (audit + T3). **G(d)** = seed-mean of mean_t∈restricted g(t). **P2 = mean_{d**∈**HEX} G(d) − mean_{d**∈**PROSE} G(d)**. - **Depth score:** D̄ (d) = seed-mean of mean_t∈restricted depth_selected(t), same protocol/restriction. **S1 = mean_{d**∈**HEX} D̄ (d) − mean_{d**∈**PROSE} D̄ (d)**. - **R1 (optional appendix):** JSD(P_root^HEX, P_root^PROSE) between reference-model root distributions; JSD(P,Q) = ½Σ P log(P/M) + ½Σ Q log(Q/M), M = (P+Q)/2, ∈ [0,1] bits. Labeled: computed on **smoothed** (add-β) distributions.

### 4.5 Model-level readings (descriptive outputs from reference models)

`h_online` per reference model: in-sample sequential entropy-rate estimate accumulated during the training pass, h_online = (1/N) Σ_t −log2 P_{s*(t)}(x_t) with online Δ-based selection and pre-update probabilities — a genuine sequential code length, hence an upper bound on the source entropy rate in expectation. Reported once per regime for SG96 comparability; never inferential** (D19/D32).

Selected-depth histograms and **gain-vs-available-context curves** (mean g(t) as a function of available_past = 1…d_max) per regime, on held-out material via the LODO protocols — these are the v2 replacements for the v1 MI-decay profile, and answer the same question ("how far back does structure reach?") with the adaptive instrument (F5–F6).

**Context lexicon (new; D38):** rank tree nodes by total importance Δ(s) (bits saved vs parent over all occurrences); report top-k = 20 contexts per regime with N_s, depth, Δ(s), and the context string in UPOS:deprel symbols. This is the linguistics-facing interpretability output ("which morphosyntactic contexts carry the memory"). In-sample and descriptive; so labeled (T6, F9).

Root distributions and rank–frequency curves per regime (F1).

### 4.6 Diagnostics (test suite, NOT paper results; D32)

Machine-checkable slice identities of the fitted tree: (i) root distribution equals the add-β-smoothed unigram distribution of the training sample, max abs deviation < 1e−12; (ii) each depth-1 node's distribution equals the smoothed conditional bigram distribution for its context symbol; (iii) `evaluate()` on the training material with updates disabled reproduces per-position code lengths consistent with stored L_self totals at the root. These certify that the low-order "measures" live inside the instrument; they appear in `tests/`, at most as one appendix table in the preprint. **The v1 standalone estimators (per-chunk H_ML/H_MM, redundancy, standalone conditional entropy, MI with shuffle baselines, MI-decay, higher-order tables, chunk-level JSD machinery, PERMANOVA) are retired and MUST NOT be reintroduced as results** (D32); if a reviewer requests them, they are derivable as smoothed slices and computed then, with the smoothing caveat stated.

### 4.7 Analytic validation targets (mandatory; gate G3)

Four processes with known ground truth (tolerances are test assertions): (a) i.i.d. uniform, m = 4, N = 2×10⁵: h_online → 2.000 bits (tol 0.02); mean selected depth < 0.2. (b) deterministic period-3 cycle ABCABC…: held-out CE < 0.02 bits; depths concentrated at 1. (c) order-1 binary Markov chain, P(stay) = 0.8: entropy rate = H_b(0.2) = 0.7219 bits; held-out CE within 0.03. (d) order-2 process X_t = X_{t−2} XOR Z_t, Z_t ~ Bernoulli(0.1): true rate H_b(0.1) = 0.4690 bits while any order-1 model yields ≈ 1.0 bit (X_t ⊥ X_{t−1}); the tree must reach depth 2 and achieve held-out CE within 0.03 of 0.4690 — proves MDL selection buys depth when depth pays. H_b(p):= −p log p − (1−p) log(1−p). Plus (new in v2): slice tests §4.6; label-free property test (G(d) output invariant under permutation of regime labels in the input registry — code-level guarantee of D36); fallback and unseen-symbol tests; cross-entropy on two known Markov chains where CE(B‖A) is analytic.

## 5. STATISTICAL INFERENCE FRAMEWORK (v2)

### 5.1 Units, exchangeability, tiers (D21 carried; Tier-3 removed by D33/D34)

Tokens nest in sentences, sentences in documents, documents in authors; document-mates share author, dialect, topic, annotation habits. **Randomization unit = document.** - **Tier 1 (primary): exact document-level schemes.** Greek primary contrast: 11 documents → P2/S1/R1 label permutation exact over C(11,5) = 462 assignments (min attainable p = 1/462 ≈ 0.0022); P1 sign-flip exact over 2^11 = 2048 (min one-sided p ≈ 0.00049). Both minima < 0.025, so Holm-family significance is attainable — stated explicitly. - **Tier 2 (ultra-conservative): exact author-level permutation.** {Homer, Hesiod, Hymn-anon} vs {Herodotus, Thucydides, Lysias}: C(6,3) = 20 → min p = 0.05 exactly. Reported openly: author-level significance below 0.05 is structurally unattainable with this corpus; hence effect sizes, CIs and the cross-validated transfer design carry much of the evidential weight. Robustness rerun with Lysias' four orations merged into one author-level pseudo-document. - The v1 Tier-3 chunk-level benchmark is **removed** (chunks no longer exist in inference; D34). p-value convention: `p = (1 + #{perm stat` `≥ observed}) / (1 + #perms)` for Monte Carlo; exact enumeration where listed (no add-one needed but reported both ways for transparency).

### 5.2 Validity arguments (new; D36 — read carefully, this is the v2 core)

**P2/S1 (exact permutation on label-free scores).** G(d) and D̄ (d) are computed under protocol (c), a score function of (d, 𝔻{d}) that never consults regime labels. Under H0 ("all documents generated by one process; labels arbitrary"), the score vector is exchangeable across label assignments, so permuting labels over the FIXED score vector is an exact randomization test. This **fixes a flaw in v1's H3b**, where regime-specific held- out profiles were permuted at document level although the scores themselves depended on the labels — subtly invalid; corrected here by construction.

**LODO composition note.** Removing d from the pooled training pool shifts pool composition slightly against d's own regime. Under H0 this is irrelevant (one process). Under H1 it *dilutes* G-differences conservatively (each doc is scored against a background under-representing its regime). Stated as a conservative bias, not corrected.

**P1 (exact sign-flip).** Under H0, "own" and "other" training pools are equally sized (T*-matched) samples of documents from the same process, so CE(d|own) and CE(d|other) are identically distributed and ΔCE(d) is symmetric about 0; sign-flip over documents is the exact test. Seed-averaging before flipping is legitimate (seeds are internal replicates).

**Why no refit-per-permutation:** a fully refit permutation (462 × all fits) is unnecessary given the label-free construction, and would cost ≈ 10² laptop-hours for no additional validity.

### 5.3 Effect sizes and uncertainty (D22 carried)

Effects are the statistics themselves, in **bits**, with hierarchical bootstrap 95% CIs: resample documents with replacement within each label group (B = 2000, seeded), recompute the document-mean statistics from the fixed per-document score tables. Honest caveat: 5–6 documents per group make these CIs crude; reported with that statement. Per-document dot displays (11 points, F3–F4) are the primary honest visualization.

### 5.4 Multiplicity (D33)

Holm–Bonferroni over family {P1, P2} at α = 0.05 (ordered p compared to 0.025 then 0.05). S1, R1, tragedy contrasts, PROSE_POST, Latin, learning curves, lexicon: no α, labeled secondary/exploratory in every table and figure. Note: Holm is valid under arbitrary dependence between P1 and P2.

### 5.5 Analysis freeze (D30 carried, repositioned)

Gate **G2** freezes this section and §4.4 **after** G1 (audit; which may adjust only what its pre-registered gates allow: excluded-deprel escalation, registry, T*) and **before** any model is fitted to real data — including the descriptive reference models, whose readings could otherwise steer analyst choices. Optional OSF deposit recommended. Pre-G2 exploration: synthetic data only.

### 5.6 Sensitivity plan (explicit cell list; D37)

Primary configuration **C0** = (alphabet ud23, excluded-deprel drop, boundary P-RESET, β 0.5, d_max 8, select monotone, gain restriction available_past ≥ 4). - **Factorial block** (full recompute of P1 and P2 point estimates + exact inference, S = 10 seeds): alphabet-policy ∈ {(ud23, drop), (ud23, oth), upos_only} × boundary ∈ {P-RESET, P-BOUND} = **6 cells** (C0 among them at S = 20). - **One-at-a-time block** around C0 (point estimates only, S = 10): β ∈ {1/|A|, 0.25, 1.0} (3 cells), d_max ∈ {6, 12} (2), select = argmax (1), gain restriction ≥ 0 i.e. unrestricted (1) = **7 cells**. - Compute estimate: per cell ≈ 11 docs × (2 regime fits + 1 pooled fit) × 10 seeds = 330 fits ≈ 10–20 laptop-minutes → total ≈ 3–5 hours [ASSUMPTION, verified at G0 profiling]. Stability table T4: per cell, sign, magnitude, and (factorial block) exact p of P1 and P2. A conclusion is claimed only if sign-stable across all 13 cells; instability is reported as a finding.

### 5.7 Latin protocol and matched Greek subsampling (D24 carried, restated at v2 sizes)

LA-HEX (2 docs) vs LA-PROSE (6 docs), 8 evaluation documents. P1-Latin: exact sign-flip 2^8 = 256 (min one-sided p ≈ 0.0039). P2-Latin: exact label permutation C(8,2) = 28 (min p ≈ 0.036 > 0.025 → **Latin cannot enter the Holm family and is qualitative by design**, L1: sign + CI replication, no α spent). d_max = 6 default for Latin (T*_la small). **Matched Greek baseline:** B = 100 stratified whole-sentence subsamples of Greek matching Latin per-regime retained-token counts; compute P1/P2 point estimates on each; locate the Latin observed values within the Greek subsample distribution (percentile) — answers "are Greek–Latin differences beyond what corpus size alone produces?" (proposal §8.1).

### 5.8 Confound register and claim wording (D25 carried, extended)

Named confounds: dialect (Homeric vs Ionic/Attic), epoch, genre, annotation policy (Latin iobj ≈ absent; DET conventions differ across treebanks), annotation quality (poetry DEPRELs noisier → the UPOS-only arm), **editorial sentence segmentation** (→ position restriction D35, P-BOUND arm), training-set composition under LODO (→ §5.2 note). Licensed claim template: "in this corpus, the hexameter regime differs from classical prose in ⟨locus: transfer / context gain⟩ by ⟨effect⟩ bits [CI]"; causal attribution to meter is never asserted; no claim that language is a finite-memory source (§0.5).

## 6. SOFTWARE ARCHITECTURE (v2)

### 6.1 Repository tree

```text
hexis/
├── pyproject.toml  uv.lock  README.md  CLAUDE.md
```

```text
├── config/
│   ├── default.yaml                 # §6.3 — single source of parameters
│   └── registry_overrides.yaml      # human-verified doc_id → (author, work, regime, …)
(G1)
```

```text
├── data/
│   ├── raw/        # immutable UD clones; gitignored; PROVENANCE.md committed
│   ├── interim/    # tokens.parquet
│   └── processed/  # sequences.parquet, alphabet.json, scores/*.parquet
├── src/hexis/
```

```text
│   ├── config.py  conllu_reader.py  registry.py  alphabet.py  sequences.py  blocks.py
│   ├── model/
│   │   ├── context_tree.py   # ContextTree, TreeParams, EvalResult  (§4.1–4.3)
│   │   ├── diagnostics.py    # slice identities (§4.6)
```

```text
│   │   └── lexicon.py        # context-importance extraction (§4.5)
│   ├── protocols/
│   │   ├── sampling.py       # whole-sentence subsampling to T*, seed derivation
│   │   └── scores.py         # ΔCE, gain, depth scores; LODO orchestration; learning
```

```text
curves (§4.2/4.4)
│   ├── stats/
│   │   ├── permutation.py    # exact label permutation, exact sign-flip
│   │   ├── bootstrap.py      # hierarchical document bootstrap
```

```text
│   │   └── holm.py
│   ├── viz/plots.py          # F1–F10 (§8)
│   ├── manifest.py
│   └── pipeline/             # CLI entry points, one per stage
│       ├── run_audit.py  run_encode.py  run_tree_validation.py
```

```text
│       ├── run_reference.py  run_confirmatory.py  run_latin.py  run_sensitivity.py
├── tests/                    # §7
├── results/tables|figures|logs      # artifacts named {stage}_{config-hash}_{date}
└── notebooks/                # exploration only; nothing canonical
```

### 6.2 Key interfaces (binding contracts)

```text
# model/context_tree.py
@dataclass
class TreeParams: d_max: int = 8; beta: float = 0.5; k_min: int = 2; gamma: float = 0.0;
```

```text
select: str = "monotone"
class ContextTree:
    def __init__(self, n_symbols: int, params: TreeParams): ...
    def fit(self, sent_seqs: Iterable[Sequence[int]]) -> None      # single prequential
pass; sets self.h_online
```

```text
    def evaluate(self, sent_seqs) -> EvalResult                    # frozen; per-position
records (§4.3)
    def root_distribution(self) -> np.ndarray                      # smoothed (add-β)
    def node_table(self, depth: int) -> pd.DataFrame               # diagnostics/lexicon
```

```text
support
    def top_contexts(self, k: int = 20) -> pd.DataFrame            # by Δ(s) (lexicon,
§4.5)
@dataclass
```

```text
class EvalResult:
    ce: float; n: int
    depth_selected: np.ndarray; depth_matched: np.ndarray; available_past: np.ndarray
    codelen_root: np.ndarray; codelen_selected: np.ndarray
    unseen_context_rate: float
```

```text
# protocols/scores.py
def delta_ce_scores(registry, sequences, alphabet, cfg, rng) -> pd.DataFrame
    # rows: doc_id, regime, ce_own(mean,sd), ce_other(mean,sd), dce, n_positions
```

```text
[protocol (b)]
def pooled_scores(registry, sequences, alphabet, cfg, rng) -> pd.DataFrame
    # rows: doc_id, regime, gain_mean(mean,sd), depth_mean(mean,sd), frac_restricted,
coverage  [protocol (c); LABEL-FREE]
```

```text
def learning_curves(...) -> pd.DataFrame                            # CE vs T grid
(descriptive)
```

`# stats/permutation.py`

```text
def exact_label_permutation(scores: np.ndarray, labels: np.ndarray, sided: str) ->
PermResult   # enumerates C(n,k)
def exact_sign_flip(values: np.ndarray, sided: str) -> PermResult
# enumerates 2^n
# PermResult(p_exact, observed, null_distribution, n_enumerated)
```

Carried unchanged from v1: `conllu_reader.iter_sentences` (MWT expansion, empty-node skip, fail-loud validation), `alphabet.strip_subtype / map_token / run_audit / freeze_alphabet` (total function; §3.4), `registry.build_registry`.

### 6.3 Configuration (config/default.yaml — complete v2 default)

```text
seeds: {global: 20260706}            # per-analysis seed = global XOR crc32(analysis_id)
corpus:
  ud_release: "r2.18"
```

```text
  languages: [grc, la]
  primary_contrast: {grc: [HEX, PROSE_CLASS], la: [HEX, PROSE_ALL]}
alphabet:
  variant: ud23                      # ud23 | ud23_oth | upos_only
  upos_keep: [ADJ, ADP, ADV, AUX, CCONJ, DET, NOUN, NUM, PART, PRON, SCONJ, VERB]
```

```text
  upos_drop: [PUNCT, X, INTJ, SYM]
  upos_map:  {PROPN: NOUN}
  deprel_keep: [root, nsubj, csubj, obj, iobj, ccomp, xcomp, obl, advcl, advmod, acl,
                amod, appos, det, nummod, nmod, case, mark, aux, cop, cc, conj, parataxis]
```

```text
  excluded_deprel_policy: drop       # drop | oth
  gate_a_threshold: 0.02
sequence: {boundary: reset}          # reset | bound
context_tree: {d_max: 8, beta: 0.5, k_min: 2, gamma: 0.0, select: monotone}
```

```text
scores:
  t_star: null                       # fixed at G1 per language; recorded here
  n_seeds: 20
  min_available_past: 4              # D35 position restriction for gain/depth
  learning_curve_T: [5000, 10000, 20000]
```

```text
stats: {alpha: 0.05, family: [P1, P2], boot_B: 2000}
latin: {d_max: 6, matched_subsamples_B: 100}
blocks: {n_block: 1000, min_frac: 0.5}   # descriptive F7 only (D34)
```

### 6.4 Determinism and provenance (D26/D27 carried)

All randomness via `np.random.default_rng(derived_seed)`. Every stage writes `results/logs/{run_id}/manifest.json` (git commit, dirty flag, resolved-config sha256, input hashes, package versions, timestamps, seed). `logging` only (no prints in library code). No silent overwrites (`--force` required). Raw data immutable.

## 7. TEST SUITE (pytest; all green at the stated gates)

| Test file | Cases (ground truth) | Gate |
| --- | --- | --- |
| `test_alphabet.py` | Subtype stripping incl. multi-colon; PROPN→NOUN; drop rules; `oth` arm; totality on any UD label; synthetic CoNLL-U with MWT range + empty node | G0 |
| `test_conllu_reader.py` | Malformed row → `ParseError` with location; `sent_id` required; ID order preserved | G0 |
| `test_blocks.py` | Sentence-aligned fill; tail ≥/< `min_frac`; never spans documents | G0 |
| `test_context_tree.py` | The four analytic processes of §4.7 with stated tolerances; `d_max` honored; `k_min`/γ behavior; fallback to deepest ancestor; unseen symbol never `p = 0` | G3 |
| `test_tree_slices.py` | Root = add-β unigram (max dev < `1e−12`); depth-1 nodes = smoothed bigram tables; evaluate-on-train consistency (§4.6) | G3 |
| `test_scores.py` | `ΔCE` on two analytic Markov chains matches analytic `CE(B‖A)`; gain restriction respects `available_past`; label-free test: `pooled_scores` output byte-identical under permuted registry labels | G3 |
| `test_permutation.py` | Exact enumeration counts = `C(n,k)` and `2^n`; null synthetic → `p ~ Uniform` (KS over repetitions); planted effect → small p; one/two-sided consistency | G0 |
| `test_bootstrap_holm.py` | Holm ordering on fixed p-vector (family of 2: 0.025/0.05); bootstrap reproducibility under fixed seed | G0 |

Edge cases throughout: empty sequences, single-symbol alphabet, sentences shorter than restriction, all-dropped sentences.

## 8. OUTPUTS

**Tables.** T1 corpus registry (per document: regime, tokens raw/retained, retention %). T2 alphabet audit (UPOS×DEPREL coverage, drop rates by rule/regime, GATE outcomes, restricted-position fractions per regime). T3 confirmatory results (P1, P2 observed; exact p Tier-1 and Tier-2; Holm-adjusted; effects in bits; bootstrap CIs; S1 alongside, labeled secondary). T4 sensitivity stability (13 cells × {sign, magnitude, p where computed}). T5 CE matrix (document × training regime, seed mean ± sd, ΔCE). T6 context lexicon (top-20 contexts per regime: context string, depth, N_s, Δ(s) bits; labeled descriptive/in-sample). **Figures** (title, labeled axes with units, n annotated, run_id footer). F1 root distributions / rank–frequency per regime. F2 CE-matrix heatmap with ΔCE margins. F3 per-document ΔCE dot plot with exact sign-flip null band. F4 per-document G(d) by regime (11 points) with exact permutation null. F5 gain-vs-available-context curves per regime (held-out). F6 selected-depth distributions per regime (restricted positions). F7 within-document block-CE profiles for the two largest documents (descriptive). F8 learning curves CE vs T. F9 context-lexicon bars (top contexts by Δ(s)). F10 sensitivity panel (T4 visualized). Optional appendix figure: R1 JSD display.

## 9. EXECUTION DAG AND GATES (v2 renumbering)

```text
G0 environment + non-tree tests green, fit-cost profiled
G1 corpus audit → registry + alphabet + T* FROZEN     (real data: counts only)
G2 analysis-plan freeze (§4.4/§5; optional OSF)       (before ANY model fit on real data)
```

```text
G3 context tree validated: four analytic processes + slice + label-free + score tests
G4 reference models fitted; diagnostics pass; descriptive readings produced (T6, F1, F5–F7,
h_online)
G5 confirmatory inference complete (P1, P2, S1; T3, T5, F2–F4)
```

```text
G6 Latin replication + matched Greek subsampling (L1)
G7 sensitivity plan complete (T4, F10) → writing
```

Gate criteria: G0 tests + profiling recorded; G1 no unassigned sentences, GATE-A/B resolved, alphabet.json + registry + T* frozen; G2 plan hash recorded; G3 all listed tests green; G4–G7 artifacts + manifests archived.

## 10. PREPRINT MAPPING (v2)

Target: arXiv **cs.CL** (optional cross-list physics.data-an). LaTeX. Structure → content: **Introduction** — regimes framing (§0.4), question as predictive organization under constraint. **Related work** — three strands, each cited and differentiated: (i) information-theoretic text analysis (Shannon; Montemurro & Zanette; Mansilla & Bush; Šeļa & Gronas); (ii) VLMC/context-tree statistics and its linguistic use (Rissanen 1983; Bühlmann & Wyner 1999; SG96 as operational authority; **Galves et al. 2012** — closest precedent: VLMC model selection for linguistic rhythm, EP/BP; differentiate: their alphabet is rhythmic/accentual, ours morphosyntactic; their question dialect identity, ours formal constraint; no cross-regime transfer there); (iii) computational stylometry of classical languages (**Chen et al. 2024 ML4AL** — POS-augmented features separate Latin prose/verse with high accuracy; differentiate: classification accuracy is not the question here; our contribution is the *locus and depth* of the signature via an adaptive-memory instrument, exactly the beyond-short-n-gram direction their fixed-order features cannot probe); UD framework (de Marneffe et al. 2021; Herrera et al. for exclusion choices). **Corpus** — T1, §2, confound statement. **Methods** — §3–§5 with the §4.1 algorithm and the SG96-correspondence note; the design-evolution paragraph: *the estimator battery of the proposal was consolidated pre-data into a single instrument (Decision Log D32–D36); low-order measures are smoothed truncations of the model and were retired as standalone confirmatory analyses before any real-data computation. *Results** — descriptive readings (G4 outputs) then confirmatory (T3, F2–F4), specificity (tragedy, exploratory), Latin (L1), robustness (T4). **Discussion** — what the locus (root / gain / transfer) licenses; Anderson as conceptual framing only. **Limitations** — Tier-2 granularity (min p = 0.05), §5.8 confounds, **model-misspecification statement anchored to Chomsky (1956): the instrument is a universal-coding device; no finite-memory claim about language** (§0.5). **Future work** —proposal §10; verse-boundary extension (D11); CTW comparator; cross-language transfer (excluded here: alphabets differ across languages, D-note in §5.8). Complete bibliographic registry (all sources, statuses, preprint roles): `03_ROADMAP_OPERATIVA_IT.md`, Appendix.

## APPENDIX A — Frozen label sets (unchanged from v1)

UPOS retained (12): ADJ ADP ADV AUX CCONJ DET NOUN NUM PART PRON SCONJ VERB. Dropped: PUNCT X INTJ SYM. Mapped: PROPN→NOUN. DEPREL retained (23): root nsubj csubj obj iobj ccomp xcomp obl advcl advmod acl amod appos det nummod nmod case mark aux cop cc conj parataxis. Excluded (→ D06 policy): punct discourse vocative orphan flat dep + anything else (audited). Subtype stripping universal:

`label.lower().split(":")[0]`.

## APPENDIX B — Notation and glossary (v2)

`A` frozen alphabet; `H_b(p)` binary entropy; `Δ(s)` node MDL efficiency (bits); `s*` selected context; `d*(t)` selected depth; `available_past` within-sentence context length; `CE` held-out cross-entropy (bits/symbol);

`ΔCE(d)` own-regime advantage; `g(t)` code-length gain vs root; `G(d)` restricted document-mean gain; `D̄ (d)` restricted document-mean depth; `h_online` in-sample sequential estimate (descriptive); `T*` matched training size; `C0` primary configuration; statistics P1/P2 (confirmatory), S1 (secondary), R1 (optional), L1 (Latin, qualitative); regimes HEX / PROSE_CLASS / PROSE_POST / OTHER_VERSE / EXCLUDED; gates G0–G7; tiers 1–2.

## APPENDIX C — Proposal-to-v2 hypothesis map

H1 → root reading (descriptive) + R1 (optional). H2 → P2 (context gain: adaptive-order sequential organization). H3 → P1 (transfer) + S1 (depth). H4 → L1. Retired as standalone: per-chunk entropy/redundancy, standalone conditional entropy, MI(+decay, shuffle), chunk JSD machinery — all recoverable as smoothed slices/diagnostics of the instrument (§4.6). Statistical corrections carried from v1 unchanged: document-level randomization (D21), held-out primacy (D19→D32), T*-matching (D20), five-regime taxonomy (D04), UPOS-only arm (D31), GATE-A (D06).

*End of specification v2.0. Amendments only via the Decision Log.*
