# PROJECT HEXIS — DECISION LOG

Version 2.0 — 2026-07-06. Binding companion to `01_MASTER_SPEC.md` v2.0. Supersedes v1.0 (2026-07-05, archived in `archive_v1/`). Format: **Q** question · **D** decision · **R** rationale · **Status** (FROZEN | GATED:G1 | SUPERSEDED by Dnn | AMENDED by Dnn) · ★ = declared deviation from / extension of the research proposal. Amendment protocol: changing a FROZEN entry requires a new `D{n}-A1` entry recording old value, new value, reason, date, and impact on already-computed results (re-run or retired). **No silent changes.**

Reading guide: §I carries v1 decisions with updated status (self-contained one-paragraph form); §II contains the v2 architecture decisions D32–D39 in full; §III open items.

## §I — CARRIED DECISIONS (v1 → v2 status)

**D01 — Artifact languages.** AI-facing spec/log in English; owner-facing index/roadmap in Italian; preprint in English. Status: FROZEN.

**D02 — Naming.** Project HEXIS; repo `hexis`; package `src/hexis`; snake_case functions, PascalCase classes; stable vocabulary per Spec App. B. v2 adds: statistics P1/P2/S1/R1/L1, primary configuration C0, protocols (a)/(b)/(c). Status: FROZEN (vocabulary extended).

**D03 — Data version and splits.** Pin UD v2.18 (tag + commit SHA + SHA-256 recorded); **ignore UD train/dev/test entirely**; re-derive documents from `sent_id`. R: UD splits serve parser benchmarks and can cut documents → leakage in document-level protocols. Status: FROZEN.

**D04** ★ **— Regime taxonomy.** Five labels HEX / PROSE_CLASS / PROSE_POST / OTHER_VERSE / EXCLUDED; Greek primary contrast HEX vs PROSE_CLASS; tragedy = specificity check (exploratory); Latin PROSE_ALL = union. R: verified corpus composition (12 tragedies; post-classical prose; Vulgate etc.). Status: FROZEN (assignments GATED:G1).

**D05 — UPOS deletions.** Delete tokens with UPOS ∈ {PUNCT, X, INTJ, SYM}; drop_reason recorded; adjacency closes gaps. Status: FROZEN.

**D06 — Excluded-DEPREL policy + GATE-A.** Retained-UPOS token with excluded deprel: PRIMARY = drop; SENSITIVITY = map to `oth`. GATE-A: any excluded label > 2% of raw tokens in any regime at audit → both policies co-primary + discussed (vocatives plausibly genre-skewed). Status: FROZEN policy, GATED:G1 escalation.

**D07 — Subtype handling.** Universal rule `deprel.lower().split(":")[0]`; covers all 20 verified Latin subtypes and the proposal's mapping list. Status: FROZEN.

**D08 — PROPN → NOUN** (Latin only; Greek has no PROPN [verified]). Status: FROZEN.

**D09 —** `flat` **and unexpected labels.** After stripping, any label not in the retained 23 falls under D06 (total function); audited under GATE-A. Status: FROZEN, GATED:G1.

**D10 — Sentence boundaries.** PRIMARY P-RESET (contexts truncate at sentence start; no cross-sentence statistics); SENSITIVITY P-BOUND (concatenation with `#` boundary symbol in the alphabet). Status: FROZEN.

**D11 — Verse boundaries.** Not encoded in these treebanks; out of scope v1 of the pipeline; named limitation + future work (re-alignment with editions). Status: FROZEN.

**D12 — Chunking.** v1 defined sentence-aligned chunks (1000/500) as the unit for distributional measures. Status: **AMENDED by D34** — the chunk layer is demoted to a descriptive block utility only (no inference, no chunk-size sensitivity axis).

**D13 — Entropy estimation (per-chunk ML + Miller–Madow; redundancy).** Status: **SUPERSEDED by D32** — no standalone entropy results exist in v2; low-order quantities are smoothed slices/diagnostics of the instrument.

**D14** ★ **— JSD inference (pooled confirmatory + PERMANOVA secondary; pairwise descriptive).** Status: **SUPERSEDED by D32/D33** — JSD survives only as optional appendix R1 on reference-model root distributions (no α); pairwise-chunk machinery and PERMANOVA retired.

**D15** ★ **— Sequential measures pooled at regime level.** Status: **SUPERSEDED by D32** — no standalone conditional-entropy/MI estimation; the sequential-organization question is re-operationalized as P2 (context gain).

**D16 — MI shuffle baseline.** Status: **SUPERSEDED by D32** — retired; the held-out gain-vs-available-context curves replace the MI-decay profile with an adaptive-order instrument.

**D17 — Higher-order measures exploratory.** Status: **SUPERSEDED by D32** — the adaptive tree replaces fixed higher-order tables entirely.

**D18 — Context-tree variant + T5.1.** Prequential add-β trie (β = 0.5), monotone-stop MDL selection on Δ(s) = L_par − L_self > γ, k_min = 2, γ = 0, d_max = 8; algorithm fully specified in Spec §4.1; estimator/selection parameterized. **Task T5.1:** read Schürmann & Grassberger 1996 §V.A–B line-by-line; record divergences from these defaults as D18-A1; provide a config preset reproducing the published choices. CTW = optional robustness comparator. Status: FROZEN (T5.1 rescheduled to roadmap Phase 2 — the tree is now front-loaded).

**D19** ★ **— Held-out primacy.** Held-out cross-entropy (document-level) is the inferential quantity; in-sample h_online reported once per reference model for SG96 comparability, never inferential. Status: FROZEN; **generalized by D32** (held-out primacy now governs the whole design).

**D20** ★ **— Transfer protocol.** Document-level leave-one-out; training pools subsampled to fixed T* tokens (whole sentences, S = 20 seeds); ΔCE(d) = CE(cross) − CE(own); Lysias-merged robustness rerun. Status: FROZEN; **extended by D36** (pooled label-free LODO protocol added) and by the learning-curve display (Spec §4.2).

**D21** ★ **— Randomization unit = document.** Tier 1 exact document-level schemes (Greek: label permutation C(11,5) = 462; sign-flip 2^11 = 2048); Tier 2 exact author-level (C(6,3) = 20; **min p = 0.05 — declared structural floor**). The v1 Tier-3 chunk benchmark is removed (D33/D34). R: document-mates share author/dialect/topic/annotation → chunk permutation violates exchangeability. This remains the project's most important statistical correction. Status: FROZEN.

**D22 — Effects and uncertainty.** Effects = the statistics themselves in bits; hierarchical document bootstrap 95% CIs (B = 2000) on fixed per-document score tables; per-document dot plots as the primary honest display. Chunk-level Cliff's δ retired with the chunk layer. Status: FROZEN (AMENDED by D32/D34 as noted).

**D23 — Sidedness and multiplicity (v1 family {H1, H2a, H2b, H3a, H3b}).** Status: **SUPERSEDED by D33.** The v1 principle carried unchanged: direction of constraint effects is never assumed (constraint ≠ lower entropy/gain by assumption) — hence P2/S1 two-sided.

**D24 — Latin protocol.** LA-PROSE = PROSE_CLASS ∪ PROSE_POST; Jerome EXCLUDED; Propertius/Phaedrus → OTHER_VERSE; sensitivity excluding Petronius (verse insets) and Res Gestae (epigraphic); matched Greek subsampling B = 100 (whole-sentence stratified draws at Latin sizes). v2 sizes: P1- Latin sign-flip 2^8 = 256; P2-Latin permutation C(8,2) = 28 → min p ≈ 0.036 > 0.025 ⇒ **Latin cannot enter the Holm family; L1 is qualitative by design**. Latin d_max default 6. Status: FROZEN (assignments GATED:G1).

**D25 — Confound register and claim wording.** Named confounds: dialect, epoch, genre, annotation policy, annotation quality; v2 adds **editorial sentence segmentation** (→ D35) and **LODO pool composition** (→ D36 note). Claim template: "in this corpus, the hexameter regime differs from classical prose in ⟨locus⟩ by ⟨effect⟩ bits [CI]"; no causal attribution to meter; no finite-memory claim about language (Spec §0.5). Status: FROZEN (extended).

**D26 — Determinism.** All randomness via `np.random.default_rng(derived_seed)`; per-analysis seed = global XOR crc32(analysis_id); manifests (git commit, config hash, data hashes, versions, timestamps, seed) for every artifact. **D26-A1 (2026-07-06):** global seed set to 20260706 to mark the v2 design epoch (v1 value 20260705; no results existed, so no impact). Status: FROZEN.

**D27 — Environment.** Python 3.12 via uv; deps numpy/pandas/pyarrow/conllu/scipy/matplotlib/pyyaml/pytest; locked at G0. Status: FROZEN.

**D28 — Licensing.** CC BY-NC-SA 2.5 data [verified] never redistributed; `data/raw` gitignored; PROVENANCE.md committed; repo publishes code + derived statistics + figures. Status: FROZEN.

**D29 — Dissemination and supervision.** arXiv cs.CL (optional cross-list physics.data-an). Touchpoints re-anchored to v2 gates: after **G1** (linguistic supervisor: registry + alphabet), after **G3** (mathematical supervisor: tree implementation + T5.1 correspondence), pre-submission (both). Status: FROZEN.

**D30 — Analysis freeze.** Gate **G2** freezes Spec §4.4/§5 after G1 and **before any model is fitted to real data —including the descriptive reference models** (their readings could steer analyst choices). OSF deposit recommended, optional. Pre-G2 exploration: synthetic data only. Amendments discovered during synthetic validation (G3) pass through this log. Status: FROZEN (repositioned).

**D31 — UPOS-only robustness arm.** Every confirmatory statistic replicated on the 12-symbol UPOS alphabet. R: poetry DEPRELs noisier (proposal §8.4); treebank annotation policies differ (Perseus vs EvaLatin DET conventions, documented by Chen et al. 2024). Convergence across alphabets is a reported result. Status: FROZEN, **mandatory** (its weight increases under the mono-instrument design).

## §II — v2 ARCHITECTURE DECISIONS (new)

**D32** ★★ **— Single-instrument architecture (master decision of v2). Q:** The proposal and Spec v1.0 deployed a battery of independent estimators (per-chunk Shannon entropy with Miller–Madow, redundancy, chunk-level JSD machinery + PERMANOVA, pooled conditional entropy, MI with shuffle baselines, MI-decay profiles, exploratory higher orders) alongside the context tree. The owner requested consolidation to a single targeted experiment centered on the Rissanen-style method, without losing the project's questions. **D:** One model class —the MDL context tree of Spec §4.1 — is the sole instrument. All scientific quantities are readings of fitted models: root distribution (order 0), held-out context gain (order ≥ 1), held-out transfer (full model). Low-order classical quantities are **smoothed truncations of the model** (root = add-β unigram; depth-1 nodes = smoothed bigram tables): they exist as machine-checked diagnostics (Spec §4.6) and, at most, one appendix table — never as standalone results. JSD is demoted to optional appendix R1 (a one-line function of the two root distributions; the only symmetric quantity not derivable from a single model, kept as a near-zero-cost independent cross-check). Retired and **not to be reintroduced as results**: per-chunk entropy/redundancy, standalone conditional entropy, MI (+ decay, shuffle baselines), higher-order tables, chunk JSD machinery, PERMANOVA, Lempel–Ziv cross-check.

**R:** (i) the truncation identity makes separate estimation redundant; (ii) the proposal's real question — the *locus* of the signature: distributional vs sequential vs predictive (§9.2) — is answered *within* the instrument by root / gain / transfer; (iii) a two-statistic confirmatory family maximizes power under Holm, the binding constraint of this corpus; (iv) one predictive model of the source is the coherent operationalization of the regimes framing; (v) pilot scoping and the owner's time budget. **Caveats recorded:** slices are add-β-smoothed, prequential quantities —always labeled as such, never presented as ML or Miller–Madow estimates. **Risk accepted:** a mono-instrument design concentrates all risk on the correctness and parameterization of the tree; mitigations are structural: analytic ground-truth suite (gate G3), slice diagnostics, T5.1 correspondence audit, mandatory UPOS-only arm (D31), sensitivity plan (D37), R1 as independent check. **Provenance:** owner-initiated, 2026-07-06, **pre-data** — no confirmatory analysis had touched real data; stated in the preprint (no forking-paths concern). **Supersedes:** D13, D14, D15, D16, D17, D23 (→ D33). **Amends:** D12 (→ D34), D22. Status: FROZEN.

**D33** ★ **— Hypothesis and statistic restructure. D:** Confirmatory family = **{P1, P2}**, Holm–Bonferroni α = 0.05 (thresholds 0.025 / 0.05; Holm valid under arbitrary dependence). P1 = mean ΔCE (one-sided > 0; two-sided also reported); P2 = regime difference in document-mean restricted context gain (two-sided — direction never assumed). S1 (depth differential) = pre-registered secondary, no α — demoted because depth is the reading most sensitive to parameterization (d_max, k_min), while gain is in bits and position-controlled. R1 (JSD) optional appendix, no α. L1 (Latin) qualitative, no α. **Mapping to the proposal:** H1 → root reading + R1; H2 → P2; H3 → P1 + S1; H4 → L1. Tier-3 chunk benchmark removed. **Attainability check (declared):** min exact p — sign-flip 1/2048 ≈ 0.00049; label permutation 1/462 ≈ 0.0022 — both < 0.025, so family significance is attainable at Tier 1; the Tier-2 author-level floor of 0.05 remains and is declared (D21). Status: FROZEN.

**D34 — Chunk layer demoted. D:** No chunk/block statistic enters inference anywhere. `make_blocks` (sentence-aligned, n = 1000, min_frac = 0.5, never spans documents) is retained **only** for the descriptive within-document CE profile figure (F7, two largest documents). The chunk-size sensitivity axis is removed. **What is lost and its replacement:** v1's per-chunk displays of document effects → per-document dot plots (11 points; F3–F4) + F7 profiles, which display heterogeneity more honestly at the actual unit of inference. Status: FROZEN.

**D35 — Position restriction for gain and depth scores. Q:** Under P-RESET, early-in-sentence positions mechanically lack context; sentence segmentation is *editorial* and may differ systematically between regimes → unrestricted mean gain would confound sequential organization with sentence length. **D:** Primary G(d) and D̄ (d) use only positions with `available_past ≥ 4` (at least the 5th retained token of the sentence); the unrestricted variant is a sensitivity cell (D37); qualifying-position fractions per regime are reported (audit + T3). ΔCE needs no restriction: it is a within-document difference between two models evaluated at identical positions, so position effects cancel. Status: FROZEN.

**D36** ★ **— Label-free score construction and exact test validity. Q:** Permutation tests on model-derived scores are invalid if the scores themselves depend on the permuted labels. v1's H3b (regime-specific held-out depth profiles, document-label permutation) had exactly this subtle flaw. **D:** (i) **P2/S1:** scores computed under protocol (c) — pooled LODO models fit on 𝔻∖{d} with **no regime information consulted anywhere** (score = f(d, 𝔻∖{d})). Under H0 (one process; labels arbitrary) the fixed score vector is exchangeable ⇒ exact label permutation is valid. A **code-level label-invariance test is mandatory** (pooled_scores output byte-identical under permuted registry labels; Spec §7). (ii) **P1:** exact sign-flip on {ΔCE(d)}: with T*-matching, under H0 the "own" and "other" pools are equally sized samples from one process ⇒ CE(d|own) and CE(d|other) identically distributed ⇒ ΔCE symmetric about 0. Seed-averaging before flipping is legitimate (internal replicates). (iii) **LODO composition note:** removing d slightly tilts the pooled pool against d's own regime; irrelevant under H0, *conservative dilution* under H1 — stated, not corrected. (iv) **No refit-per-permutation:** unnecessary given the construction; would cost ≈ 10² laptop-hours for no added validity. Status: FROZEN. (Corrects v1; recorded openly.)

**D37 — Compute and sensitivity plan (explicit cells). D:** Primary configuration **C0** = (ud23, drop, P-RESET, β 0.5, d_max 8, monotone, restriction ≥ 4; S = 20 seeds). **Factorial block** (full recompute of P1/P2 + exact inference, S = 10): alphabet-policy {(ud23, drop), (ud23, oth), upos_only} × boundary {P-RESET, P-BOUND} = 6 cells (C0 among them). **OAT block** around C0 (point estimates, S = 10): β ∈ {1/|A|, 0.25, 1.0}, d_max ∈ {6, 12}, select = argmax, unrestricted gain = 7 cells. Total 13 cells. Budget: ≈ 330 fits/cell ≈ 10–20 laptop-minutes ⇒ ≈ 3–5 h total [ASSUMPTION → confirmed by G0 profiling, O6]. **Claim discipline:** a conclusion is asserted only if sign-stable across all 13 cells; instability is itself a reported finding (T4/F10). Status: FROZEN.

**D38 — Context lexicon (interpretability output). D:** From each reference model, rank nodes by total importance Δ(s) (bits saved vs parent over all occurrences); report top-20 contexts per regime with context string (UPOS:deprel symbols), depth, N_s, Δ(s) (T6, F9). Explicitly **in-sample and descriptive** — the linguistics-facing reading of "which morphosyntactic contexts carry the memory". Status: FROZEN.

**D39 — Bibliography registry, related-work obligations, Chomsky role. D:** (i) The complete source registry lives in `03_ROADMAP_OPERATIVA_IT.md`, Appendix (statuses [V]/[P]/[S]/[T]; nothing may be cited in the preprint that is not in the registry; completion pass = O5). (ii) **Mandatory related-work citations with differentiation:** Galves et al. 2012 (Ann. Appl. Stat. 6(1):186–209 — closest precedent: VLMC model selection for linguistic rhythm, EP/BP; differs in alphabet [accentual vs morphosyntactic], question [dialect identity vs formal constraint], and absence of cross-regime transfer) and Chen et al. 2024 (ML4AL, pp. 251–259 — POS-feature prose/verse classification in Latin is solved and easy ⇒ novelty repositioned, erratum E8; their fixed-order short-n-gram limitation is precisely what the adaptive instrument addresses). (iii) **Chomsky (1956), IRE Trans. IT 2(3):113–124:** conceptual/epistemological anchor **only** for the model-misspecification limitation (finite-memory Markov-class models are not models of grammar; the tree is a universal-coding measuring device) —**never** cited as operational justification for the method; operational authority = Schürmann & Grassberger 1996 + VLMC statistics literature (Rissanen 1983; Bühlmann & Wyner 1999; Csiszár & Talata 2006). Status: FROZEN.

## §III — OPEN ITEMS (tracked, not blocking)

**O1:** count of Greek/Latin treebanks in UD v2.18 (proposal's "3/6" likely stale) — verify at G1 (erratum E5).

**O2:** duplicate Hymn-to-Demeter registry entries — resolve at G1.

**O3:** Task T5.1 — SG96 §V line-by-line correspondence audit → possible D18-A1 (roadmap Phase 2).

**O4:** Petronius verse insets in the sampled passages — G1 audit; sentence-level exclusion if identifiable.

**O5:** bibliographic completion pass on all [P]/[S]/[T] registry entries (Mansilla & Bush volume/pages; Šeļa & Gronas venue; Cover & Thomas edition; Herrera et al. venue; Bamman & Crane details; Ron et al./KT/Holm details) — preprint phase.

**O6:** fit-cost profiling to confirm the D37 compute budget — G0.
