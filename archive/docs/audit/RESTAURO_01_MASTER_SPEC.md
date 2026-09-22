# RESTAURO DEI BLOCCHI NORMATIVI — 01_MASTER_SPEC (D48)

**Data:** 2026-07-21. **Baseline:** conversioni `.md` del 2026-07-21 (canoniche; da committare tal quali con danno dichiarato — commit 1). **Restauro:** questo intervento (commit 2), interamente deterministico: ogni sito è determinato da un'occorrenza parallela intatta nello stesso documento o dal contesto immediato; nessuna ricostruzione discrezionale. I corsivi orfani sono irrecuperabili e non normativi (dichiarato in D48).

**Contabilità del danno (esecuzione vs censimento).** Il censimento preliminare su PDF contava 33 siti (A15/B6/C7/D5). L'esecuzione, che vede il testo byte per byte, ha contato con precisione maggiore: **6 blocchi riunificati** (da **32 frammenti** recintati: node-fields ×2, training ×4, §6.1 ×8, §6.2 ×9, §6.3 ×6, §9 ×3), **15 ricongiunzioni di riga** (14 interne ai blocchi + 1 in §2.5), **8 ripristini di glifo** (𝔻 ∖ {d} ×2 in §4.2/§5.2, da occorrenza parallela p. 9 e dal Decision Log D36; `s*` ×2 in §4.1/§4.3, da P_{s*} intatto; monotone-stop ×1, ricongiunto al sito `s*` di §4.1; D̄(d) ×4, tre in §4.4 e uno in App. B, da occorrenza parallela nella tabella §1.2) e **7 riparazioni di enfasi** (§1.1; §4.1 correspondence; §4.1 selezione; §4.3 Fallbacks; §4.4 P2 e S1; §4.5 never-inferential; §10 Results — contando P2/S1 come due). Il delta rispetto al censimento (+3 riparazioni elementari) deriva da conteggi più fini rivelati dal testo: §6.1 aveva 8 frammenti e non 7; D̄(d) ricorre 4 volte e non 3; P2/S1 sono due siti gemelli.

**Nota sulle voci RA.** Sei interventi sono al tempo stesso restauro ed emendamento ratificato (tag RA): il blocco restaurato incorpora anche l'aggiunta v2.1 (es. §6.1 aggiunge `run_null_calibration.py` e `candidates/` per D44/D47; §9 adotta l'ordine v2.1 per D44(vii); §4.2/§4.4/§5.1/§5.2 sono riscritture integrali che uniscono restauro e decisioni D41–D51). La colonna «decisione» lo dichiara; il confronto prima/dopo mostra entrambe le componenti.

---
## Sito 1 — B1 §4.1 node fields  [tag R — D48]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
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
```

**Dopo (testo restaurato):**

```text
```text
counts: dict[symbol -> int]   # n_s(a): times context s was followed by a (so far)
total:  int                   # N_s
L_self: float                 # accumulated sequential code length of symbols emitted under s
L_par:  float                 # code length the PARENT's predictor assigned to those same symbols
children: dict[symbol -> Node]
```
```

---

## Sito 2 — B2 §4.1 training pass  [tag R — D48]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
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
```

**Dopo (testo restaurato):**

```text
```text
path = [root]; node = root
for depth in 1 .. min(available_past, d_max):
    σ = symbol at distance depth in the past
    node = node.children.setdefault(σ, new Node)     # grow on first visit
    path.append(node)
p_prev = None
for depth, node in enumerate(path):                  # predict-then-update, PRE-update counts
    p = P_node(x); node.L_self += −log2(p)
    if depth > 0: node.L_par += −log2(p_prev)
    p_prev = p
for node in path: node.counts[x] += 1; node.total += 1
```
```

---

## Sito 3 — B3 §6.1 repository tree  [tag RA — D48+D44+D47]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
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
```

**Dopo (testo restaurato + emendato):**

```text
```text
hexis/
├── pyproject.toml  uv.lock  README.md  CLAUDE.md
├── config/
│   ├── default.yaml                 # §6.3 — single source of parameters
│   └── registry_overrides.yaml      # human-verified doc_id → (author, work, regime, …) (G1)
├── data/
│   ├── raw/        # immutable UD clones; gitignored; PROVENANCE.md committed
│   ├── interim/    # tokens.parquet
│   └── processed/  # sequences.parquet, alphabet.json, scores/*.parquet
├── src/hexis/
│   ├── config.py  conllu_reader.py  registry.py  alphabet.py  sequences.py  blocks.py
│   ├── model/
│   │   ├── context_tree.py   # ContextTree, TreeParams, EvalResult  (§4.1–4.3)
│   │   ├── diagnostics.py    # slice identities (§4.6)
│   │   └── lexicon.py        # context-importance extraction (§4.5)
│   ├── protocols/
│   │   ├── sampling.py       # whole-sentence subsampling to T*, seed derivation
│   │   └── scores.py         # ΔCE, gain, depth scores; LODO orchestration; learning curves (§4.2/4.4)
│   ├── stats/
│   │   ├── permutation.py    # exact label permutation, exact sign-flip
│   │   ├── bootstrap.py      # hierarchical document bootstrap
│   │   └── holm.py
│   ├── viz/plots.py          # F1–F10 (§8)
│   ├── manifest.py
│   └── pipeline/             # CLI entry points, one per stage
│       ├── run_audit.py  run_encode.py  run_tree_validation.py
│       ├── run_reference.py  run_confirmatory.py  run_latin.py  run_sensitivity.py
│       └── run_null_calibration.py   # O7/D44 synthetic null-calibration study (G3)
├── candidates/               # quarantined non-canonical implementations (D47); never imported by src/hexis
├── tests/                    # §7
├── results/tables|figures|logs      # artifacts named {stage}_{config-hash}_{date}
└── notebooks/                # exploration only; nothing canonical
```
```

---

## Sito 4 — B4 §6.2 interfaces  [tag RA — D48+D44]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
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
```

**Dopo (testo restaurato + emendato):**

```text
```text
# model/context_tree.py
@dataclass
class TreeParams: d_max: int = 8; beta: float = 0.5; k_min: int = 2; gamma: float = 0.0; select: str = "monotone"

class ContextTree:
    def __init__(self, n_symbols: int, params: TreeParams): ...
    def fit(self, sent_seqs: Iterable[Sequence[int]]) -> None      # single prequential pass; sets self.h_online
    def evaluate(self, sent_seqs) -> EvalResult                    # frozen; per-position records (§4.3)
    def root_distribution(self) -> np.ndarray                      # smoothed (add-β)
    def node_table(self, depth: int) -> pd.DataFrame               # diagnostics/lexicon support
    def top_contexts(self, k: int = 20) -> pd.DataFrame            # by Δ(s) (lexicon, §4.5)

@dataclass
class EvalResult:
    ce: float; n: int
    depth_selected: np.ndarray; depth_matched: np.ndarray; available_past: np.ndarray
    codelen_root: np.ndarray; codelen_selected: np.ndarray
    unseen_context_rate: float

# protocols/scores.py
def delta_ce_scores(registry, sequences, alphabet, cfg, rng) -> pd.DataFrame
    # rows: doc_id, regime, ce_own(mean,sd), ce_other(mean,sd), dce, n_positions   [protocol (b)]
def pooled_scores(registry, sequences, alphabet, cfg, rng) -> pd.DataFrame
    # rows: doc_id, regime, gain_mean(mean,sd), depth_mean(mean,sd), frac_restricted,
    #       own_regime_pool_fraction (D44), coverage   [protocol (c); LABEL-FREE]
def learning_curves(...) -> pd.DataFrame                           # CE vs T grid (descriptive)

# stats/permutation.py
def exact_label_permutation(scores: np.ndarray, labels: np.ndarray, sided: str) -> PermResult   # enumerates C(n,k)
def exact_sign_flip(values: np.ndarray, sided: str) -> PermResult                               # enumerates 2^n
# PermResult(p_exact, observed, null_distribution, n_enumerated)
```
```

---

## Sito 5 — B5 §6.3 YAML  [tag R — D48]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
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
```

**Dopo (testo restaurato):**

```text
```text
seeds: {global: 20260706}            # per-analysis seed = global XOR crc32(analysis_id)
corpus:
  ud_release: "r2.18"
  languages: [grc, la]
  primary_contrast: {grc: [HEX, PROSE_CLASS], la: [HEX, PROSE_ALL]}
alphabet:
  variant: ud23                      # ud23 | ud23_oth | upos_only
  upos_keep: [ADJ, ADP, ADV, AUX, CCONJ, DET, NOUN, NUM, PART, PRON, SCONJ, VERB]
  upos_drop: [PUNCT, X, INTJ, SYM]
  upos_map:  {PROPN: NOUN}
  deprel_keep: [root, nsubj, csubj, obj, iobj, ccomp, xcomp, obl, advcl, advmod, acl,
                amod, appos, det, nummod, nmod, case, mark, aux, cop, cc, conj, parataxis]
  excluded_deprel_policy: drop       # drop | oth
  gate_a_threshold: 0.02
sequence: {boundary: reset}          # reset | bound
context_tree: {d_max: 8, beta: 0.5, k_min: 2, gamma: 0.0, select: monotone}
scores:
  t_star: null                       # fixed at G1 per language; recorded here
  n_seeds: 20
  min_available_past: 4              # D35 position restriction for gain/depth
  learning_curve_T: [5000, 10000, 20000]
stats: {alpha: 0.05, family: [P1, P2], boot_B: 2000}
latin: {d_max: 6, matched_subsamples_B: 100}
blocks: {n_block: 1000, min_frac: 0.5}   # descriptive F7 only (D34)
```
```

---

## Sito 6 — B6 §9 DAG  [tag RA — D48+D44+D45]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
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
```

**Dopo (testo restaurato + emendato):**

```text
```text
G0  environment + non-tree tests green (real assertions; zero skipped in the G0 set)
    + deterministic infrastructure verified (seed, config, manifest, overwrite protection)
    — fit-cost profiling moved to G3 (O6/D45)
G1  corpus audit → registry + alphabet + T* FROZEN     (real data: counts only)
G3  context tree validated: four analytic processes + slice + label-free + score tests
    + O6 fit-cost profiling + O7 null-calibration study (D44/D45)
G2  analysis-plan freeze (§4.4/§5; optional OSF)       (REQUIRES O7 resolved — D44;
    before ANY model fit on real data)
G4  reference models fitted; diagnostics pass; descriptive readings produced (T6, F1, F5–F7, h_online)
G5  confirmatory inference complete (P1, P2, S1; T3, T5, F2–F4)   (REQUIRES O7 resolved — D44)
G6  Latin replication + matched Greek subsampling (L1)
G7  sensitivity plan complete (T4, F10) → writing
```
```

---

## Sito 7 — §1.1 R1 + emphasis  [tag RA — D48+D41]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
read at three depths of the same instrument: - **root (order 0):** symbol distribution — descriptive reading; optional JSD appendix (R1); -**context gain (order ≥ 1):**
```

**Dopo (testo restaurato + emendato):**

```text
read at three depths of the same instrument: - **root (order 0):** symbol distribution — descriptive distributional reading incl. R1 (D41); - **context gain (order ≥ 1):**
```

---

## Sito 8 — §2.5 wrapped comment  [tag R — D48]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
git checkout r2.18     # confirm tag; else the tagged release matching the
pinned version
```

**Dopo (testo restaurato):**

```text
git checkout r2.18     # confirm tag; else the tagged release matching the pinned version
```

---

## Sito 9 — §4.1 emphasis  [tag R — D48]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
Scientific claims rest on *a well-**defined MDL context model applied uniformly to all regimes*, not on numerical replication
```

**Dopo (testo restaurato):**

```text
Scientific claims rest on **a well-defined MDL context model applied uniformly to all regimes**, not on numerical replication
```

---

## Sito 10 — §4.1 selection s*  [tag R — D48]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
**Selection at a position** with matching path s₀ ⊂ … ⊂ s_k: s *= deepest s_j with, for every i = 1…j,* `total(s_i)` `≥ k_min` *and* `Δ(s_i) > γ` *(monotone-stop**). Variant `argmax`
```

**Dopo (testo restaurato):**

```text
**Selection at a position** with matching path s₀ ⊂ … ⊂ s_k: `s*` = deepest s_j with, for every i = 1…j, `total(s_i) ≥ k_min` and `Δ(s_i) > γ` (monotone-stop). Variant `argmax`
```

---

## Sito 11 — §4.2 full paragraph  [tag RA — D48+D46+D51]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
Let the primary-contrast document set be 𝔻 = HEX ∪ PROSE (Greek: 5 + 6 = 11 docs). All training subsamples draw **whole sentences uniformly without replacement until ≥ T* retained tokens**; S = 20 seeds per condition (seed derivation §6.5); seed-mean reported with sd. - **(a) Reference models** (descriptive only): one per regime, fit on ALL its documents, full data, no LODO. Used for §4.5 readings and R1. Never used for confirmatory statistics. - **(b) Regime LODO models** (for P1): for evaluation document d and training regime R_tr ∈ {HEX, PROSE}: pool = docs of R_tr minus d (if R_d = R_tr); subsample to T*; fit; evaluate d. - (c) Pooled LODO models (for P2/S1; label-free by construction): for evaluation document d: pool =* 𝔻 *\ {d} —* no regime information used anywhere*; subsample to T*; fit; evaluate d. **T* (GATED:G1):** T* = min over ALL training conditions in (b) and (c) of available retained tokens (the binding condition is expected to be "HEX minus Iliad"). One T* per language, used uniformly across (b) and (c) so that gain and CE are size-comparable. Contingency (pre-registered): if T* < 15k retained tokens, record D-amendment and add learning-curve emphasis (below). **Learning curves (descriptive):** CE(d|R_tr) vs training size T ∈ {5k, 10k, 20k, T*} for representative documents — makes the size-dependence of every conclusion visible (F8).
```

**Dopo (testo restaurato + emendato):**

```text
Let the primary-contrast document set be 𝔻 = HEX ∪ PROSE (Greek: 5 + 6 = 11 docs). All training subsamples draw **whole sentences uniformly without replacement until ≥ T* retained tokens**; S = 20 seeds per condition (seed derivation §6.4); seed-mean reported with sd. - **(a) Reference models** (descriptive only): one per regime, fit on ALL its documents, full data, no LODO. Used for §4.5 readings and R1. Never used for confirmatory statistics. - **(b) Regime LODO models** (for P1): for evaluation document d and training regime R_tr ∈ {HEX, PROSE}: pool = docs of R_tr minus d (if R_d = R_tr); subsample to T*; fit; evaluate d. - **(c) Pooled LODO models** (for P2/S1; label-free by construction): for evaluation document d: pool = 𝔻 ∖ {d} — **no regime information used anywhere**; subsample to T*; fit; evaluate d. **T* (GATED:G1; scope per D51):** T* = min over the training conditions of protocols (b) and (c) **on the primary contrast only** of available retained tokens (binding condition expected: "HEX minus Iliad" from (b); for (c) it is 𝔻 minus its largest document). Exploratory arms (tragedy, PROSE_POST) run at their own binding sizes, documented separately and labeled non-comparable with primary readings (D51). One T* per language, used uniformly across (b) and (c): this purchases cross-reading comparability (root/gain/transfer at one common training size — the locus narrative) at a **declared cost of P2 power**, since the protocol-(c) pool could support a larger training size; the cost is made visible descriptively by the learning curves, whose protocol-(c) curves extend beyond T* where the pool permits (D51). Contingency (pre-registered): if T* < 15k retained tokens, record D-amendment and add learning-curve emphasis (below). **Learning curves (descriptive):** CE(d|R_tr) vs training size T ∈ {5k, 10k, 20k, T*} for representative documents — makes the size-dependence of every conclusion visible (F8).
```

---

## Sito 12 — §4.3 emphasis + s*  [tag R — D48]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
Walk the matching path; select s *by the frozen rule;* `codelen(t) = −log2 P_{s*}(x_t)` *. Fallbacks:**
```

**Dopo (testo restaurato):**

```text
Walk the matching path; select `s*` by the frozen rule; `codelen(t) = −log2 P_{s*}(x_t)`. **Fallbacks:**
```

---

## Sito 13 — §4.4 full paragraph + G_own  [tag RA — D48+D41+D49]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
For evaluation document d with N_d evaluated positions: - **CE(d | R_tr)** = seed-mean of (1/N_d) Σ_t codelen_selected(t) under protocol (b). **ΔCE(d) = CE(d | other) − CE(d | own)**; > 0 ⇒ own-regime advantage. **P1 = mean_d ΔCE(d)** over all 11 evaluation documents. No position restriction: ΔCE is a within-document difference, so position/sentence-length effects cancel between the two models. - **Context gain** at position t under a pooled LODO model (protocol c): `g(t) = codelen_root(t) − codelen_selected(t)` ≥ 0-ish (can be negative at k_min/γ boundaries; keep signed), where codelen_root uses the SAME fitted model's root predictor. **Position restriction (D35):** the primary gain statistic uses only positions with `available_past ≥ 4` (i.e., at least the 5th retained token of its sentence). Rationale: under P-RESET, early positions mechanically lack context; if regimes differ in sentence length (editorial segmentation!), unrestricted means would confound gain with sentence length. The unrestricted variant is a sensitivity cell; the fraction of qualifying positions per regime is reported (audit + T3). **G(d)** = seed-mean of mean_t∈restricted g(t). **P2 = mean_{d**∈**HEX} G(d) − mean_{d**∈**PROSE} G(d)**. - **Depth score:** D̄ (d) = seed-mean of mean_t∈restricted depth_selected(t), same protocol/restriction. **S1 = mean_{d**∈**HEX} D̄ (d) − mean_{d**∈**PROSE} D̄ (d)**. - **R1 (optional appendix):** JSD(P_root^HEX, P_root^PROSE) between reference-model root distributions; JSD(P,Q) = ½Σ P log(P/M) + ½Σ Q log(Q/M), M = (P+Q)/2, ∈ [0,1] bits. Labeled: computed on **smoothed** (add-β) distributions.
```

**Dopo (testo restaurato + emendato):**

```text
For evaluation document d with N_d evaluated positions: - **CE(d | R_tr)** = seed-mean of (1/N_d) Σ_t codelen_selected(t) under protocol (b). **ΔCE(d) = CE(d | other) − CE(d | own)**; > 0 ⇒ own-regime advantage. **P1 = mean_d ΔCE(d)** over all 11 evaluation documents. No position restriction: ΔCE is a within-document difference, so position/sentence-length effects cancel between the two models. - **Context gain** at position t under a pooled LODO model (protocol c): `g(t) = codelen_root(t) − codelen_selected(t)` ≥ 0-ish (can be negative at k_min/γ boundaries; keep signed), where codelen_root uses the SAME fitted model's root predictor. **Position restriction (D35):** the primary gain statistic uses only positions with `available_past ≥ 4` (i.e., at least the 5th retained token of its sentence). Rationale: under P-RESET, early positions mechanically lack context; if regimes differ in sentence length (editorial segmentation!), unrestricted means would confound gain with sentence length. The unrestricted variant is a sensitivity cell; the fraction of qualifying positions per regime is reported (audit + T3). **G(d)** = seed-mean of mean_t∈restricted g(t). **P2 = mean_{d∈HEX} G(d) − mean_{d∈PROSE} G(d)**. Estimand note (D49): G(d) is the gain **of the pooled model**; a group difference in G admits two readings — flatter conditional structure in a regime, or greater distance of that regime from the pooled mixture (the latter overlapping with what P1 measures) — which P2 alone does not separate; see the descriptive `G_own` below and the claim wording in §5.8. - **Depth score:** D̄(d) = seed-mean of mean_t∈restricted depth_selected(t), same protocol/restriction. **S1 = mean_{d∈HEX} D̄(d) − mean_{d∈PROSE} D̄(d)**. - **R1 (descriptive distributional reading; D41):** JSD(P_root^HEX, P_root^PROSE) between reference-model root distributions; JSD(P,Q) = ½Σ P log(P/M) + ½Σ Q log(Q/M), M = (P+Q)/2, ∈ [0,1] bits. **No test, no α.** Labeled: computed on **smoothed** (add-β), **size-unmatched** reference models (not T*-matched), hence weakly size-dependent; displayed with this label wherever it appears. A T*-matched variant is deferred (DN-1).

**Descriptive own-regime gain (D49; no α).** `G_own(d)` = seed-mean over positions with `available_past ≥ 4` of `codelen_root − codelen_selected` under the **protocol-(b) own-regime LODO model** for d — zero additional fits (protocol-(b) evaluations already record `codelen_root`). It depends on regime labels by construction, so it is **descriptive only, never permuted, outside the Holm family** (compatible with D36/D21). Reported alongside P2 (T3 descriptive columns) and in F5; it licenses or blocks the wording "hexameter shows lower gain also under its own model" versus "only under the pooled model" (§5.8).
```

---

## Sito 14 — §4.5 emphasis  [tag R — D48]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
Reported once per regime for SG96 comparability; never inferential** (D19/D32).
```

**Dopo (testo restaurato):**

```text
Reported once per regime for SG96 comparability; **never inferential** (D19/D32).
```

---

## Sito 15 — §5.1 full rewrite  [tag RA — D43]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
Tokens nest in sentences, sentences in documents, documents in authors; document-mates share author, dialect, topic, annotation habits. **Randomization unit = document.** - **Tier 1 (primary): exact document-level schemes.** Greek primary contrast: 11 documents → P2/S1/R1 label permutation exact over C(11,5) = 462 assignments (min attainable p = 1/462 ≈ 0.0022); P1 sign-flip exact over 2^11 = 2048 (min one-sided p ≈ 0.00049). Both minima < 0.025, so Holm-family significance is attainable — stated explicitly. - **Tier 2 (ultra-conservative): exact author-level permutation.** {Homer, Hesiod, Hymn-anon} vs {Herodotus, Thucydides, Lysias}: C(6,3) = 20 → min p = 0.05 exactly. Reported openly: author-level significance below 0.05 is structurally unattainable with this corpus; hence effect sizes, CIs and the cross-validated transfer design carry much of the evidential weight. Robustness rerun with Lysias' four orations merged into one author-level pseudo-document. - The v1 Tier-3 chunk-level benchmark is **removed** (chunks no longer exist in inference; D34). p-value convention: `p = (1 + #{perm stat` `≥ observed}) / (1 + #perms)` for Monte Carlo; exact enumeration where listed (no add-one needed but reported both ways for transparency).
```

**Dopo (testo restaurato + emendato):**

```text
Tokens nest in sentences, sentences in documents, documents in authors; document-mates share author, dialect, topic, annotation habits. **Randomization unit = document.** **Sidedness rule (D43, binding):** every declared floor states its sidedness; the two-sided floor doubles the one-sided floor only when the randomization orbit contains the sign-mirror of the observed configuration — always for sign-flips, for label permutations only with equal group sizes; with unequal groups the floors coincide. - **Tier 1 (primary): exact document-level schemes.** Greek primary contrast: 11 documents → P2/S1 label permutation exact over C(11,5) = 462 assignments (unequal 5/6 → one- and two-sided floors coincide at 1/462 ≈ 0.0022); P1 sign-flip exact over 2^11 = 2048 (one-sided floor 1/2048 ≈ 0.00049; two-sided 2/2048 ≈ 0.00098). All Tier-1 floors < 0.025, so Holm-family significance is attainable — stated explicitly. - **Tier 2 (author-level): descriptive robustness without α (D43).** {Homer, Hesiod, Hymn-anon} vs {Herodotus, Thucydides, Lysias} (partition verified at G1 → O8, coupled to O2): label permutation C(6,3) = 20 (equal 3/3 → one-sided floor 1/20 = 0.05; **operative two-sided floor 2/20 = 0.10**, P2 being two-sided); sign-flip 2^6 = 64 (one-sided floor 1/64 ≈ 0.0156). Correct statement: the author-level plan cannot attain joint family significance (P2's floor 0.10 > 0.05); P1 alone could formally cross Holm-1 (0.0156 < 0.025); to avoid an incoherent partial-α family, **no α is spent at Tier 2** (revisitable at G2: DN-2). Declared cost, stated openly: Tier 2 was the design's only inferential answer to intra-author dependence; withdrawing α is a real cost. Its role: verify that sign and magnitude persist when intra-author dependence is removed by construction; sign, magnitude, and exact p values (labeled descriptive) are reported. **Author-block score (D43(v)):** unweighted mean of the per-document scores within the block — the document remains the measurement unit; the block is the randomization unit. **Lysias-merged rerun (D20/D43(iv)):** the four orations merged into one pseudo-document → 8 documents (5/3, unequal): label permutation C(8,3) = 56 (floors coincide at 1/56 ≈ 0.018), sign-flip 2^8 = 256. Declared **robustness analysis without α**; its P2 floor lies below Holm-1, so its outcome is reported but never substitutes the primary Tier-1 result. - The v1 Tier-3 chunk-level benchmark is **removed** (chunks no longer exist in inference; D34). p-value convention: `p = (1 + #{perm stat ≥ observed}) / (1 + #perms)` for Monte Carlo; exact enumeration where listed (no add-one needed but reported both ways for transparency).
```

---

## Sito 16 — §5.2 full rewrite  [tag RA — D48+D44]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
**P2/S1 (exact permutation on label-free scores).** G(d) and D̄ (d) are computed under protocol (c), a score function of (d, 𝔻{d}) that never consults regime labels. Under H0 ("all documents generated by one process; labels arbitrary"), the score vector is exchangeable across label assignments, so permuting labels over the FIXED score vector is an exact randomization test. This **fixes a flaw in v1's H3b**, where regime-specific held- out profiles were permuted at document level although the scores themselves depended on the labels — subtly invalid; corrected here by construction.

**LODO composition note.** Removing d from the pooled training pool shifts pool composition slightly against d's own regime. Under H0 this is irrelevant (one process). Under H1 it *dilutes* G-differences conservatively (each doc is scored against a background under-representing its regime). Stated as a conservative bias, not corrected.

**P1 (exact sign-flip).** Under H0, "own" and "other" training pools are equally sized (T*-matched) samples of documents from the same process, so CE(d|own) and CE(d|other) are identically distributed and ΔCE(d) is symmetric about 0; sign-flip over documents is the exact test. Seed-averaging before flipping is legitimate (seeds are internal replicates).

**Why no refit-per-permutation:** a fully refit permutation (462 × all fits) is unnecessary given the label-free construction, and would cost ≈ 10² laptop-hours for no additional validity.
```

**Dopo (testo restaurato + emendato):**

```text
**P2/S1 (exact permutation on label-free scores).** G(d) and D̄(d) are computed under protocol (c), a score function of (d, 𝔻 ∖ {d}) that never consults regime labels. Under H0 ("all documents generated by one process; labels arbitrary"), the score vector is exchangeable across label assignments, so permuting labels over the FIXED score vector is an exact randomization test. This **fixes a flaw in v1's H3b**, where regime-specific held-out profiles were permuted at document level although the scores themselves depended on the labels — subtly invalid; corrected here by construction. Requirement: joint exchangeability of the label-free score vector — guaranteed by the construction (D36(i) stands).

**LODO composition note (relabeled by D44(iv)).** Removing d from the pooled training pool shifts pool composition against d's own regime, and the shift is **asymmetric between regimes**: a HEX document is scored against a 4+6 pool, a PROSE document against a 5+5 pool, and in tokens the disparity is larger because the Iliad dominates the HEX side. Under H0 this is irrelevant (one process; exchangeability holds → test validity unaffected). Under H1, to the extent that gain increases with own-regime representation in the training pool, it is a **directional displacement of the group difference, not a symmetric shrinkage**: it exaggerates G_HEX < G_PROSE and compresses the opposite — P2 is two-sided (D33) precisely because direction is never assumed. The earlier label "conservative dilution" is withdrawn; effect-size interpretation carries this caveat. Mitigation (binding, D44(iv)): `pooled_scores` reports per document the own-regime token fraction of its training subsample (seed-mean), audited and displayed alongside T3.

**P1 (exact sign-flip) — validity status: OPEN (D44/O7; blocking G2/G5).** Under H0, T*-matched "own" and "other" pools are samples from the same process, so ΔCE(d) is **marginally** symmetric about 0 (D36(ii), which stands). Exactness of the sign-flip, however, requires invariance of the **joint** law of {ΔCE(d)} under coordinatewise sign changes — not implied by the construction: for each seed, the eleven documents' training material is drawn from heavily overlapping pools, so a sampling fluctuation that makes one pool more "typical" induces a common-mode component, coherent in sign within regime and opposite across regimes; with n = 11 it does not average out and cannot be generated by independent flips → risk of an **anti-conservative null**. Seed-averaging reduces subsampling variance but not pool-composition variance, increasing the common mode's relative weight. Resolution before G2 (O7): a null-calibration study on synthetic data runs the full chain under a true H0 and measures the empirical type-I error at nominal levels, with P2's permutation as positive control; named remedies if inflation is found: document-level refit randomization at reduced S, or an alternative pre-specified scheme validated on synthetics (D44(v)). The generic sign-flip utility is still implemented and tested at G0 (D44(vi)).

**Refit-per-permutation (corrected by D44(iii)).** The "no refit needed" argument holds for P2 — the scores are label-free, so refitting under relabeling is genuinely unnecessary. For P1 it is **inverted**: ΔCE depends on labels by definition, and refit-under-relabeling is precisely what would purchase exactness. Corrected cost: ≈ 13 fits per relabeling per seed → 462 × 13 × S; at S = 20 ≈ 1.2 × 10⁵ fits (≈ 33–100 laptop-hours at 1–3 s/fit [ASSUMPTION → O6 at G3]); a reduced-S null lowers this by an order at a declared, conservative cost. Whether a refit scheme is adopted is decided by the O7 calibration outcome.
```

---

## Sito 17 — §10 emphasis  [tag R — D48]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
before any real-data computation. *Results**
```

**Dopo (testo restaurato):**

```text
before any real-data computation.* **Results**
```

---

## Sito 18 — App B glossary  [tag RA — D48+D49+D44]

**Prima (testo danneggiato, verbatim dalla baseline):**

```text
`ΔCE(d)` own-regime advantage; `g(t)` code-length gain vs root; `G(d)` restricted document-mean gain; `D̄ (d)` restricted document-mean depth;
```

**Dopo (testo restaurato + emendato):**

```text
`ΔCE(d)` own-regime advantage; `g(t)` code-length gain vs root; `G(d)` restricted document-mean gain (pooled model); `G_own(d)` descriptive own-regime restricted gain (D49); `own_regime_pool_fraction` per-document own-regime token share of the protocol-(c) training subsample (D44); `D̄(d)` restricted document-mean depth;
```

---
