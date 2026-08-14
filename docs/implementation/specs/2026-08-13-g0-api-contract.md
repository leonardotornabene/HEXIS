# G0 API contract — alphabet, registry, sequences

Ratified by the owner 2026-08-13, following the precedent of the 2026-07-27
ratification recorded in `docs/HANDOFF.md`. These are **implementation-level
readings**, not Decision-Log changes: they fix signatures and return shapes left
free by the Spec. No parameter, statistic, hypothesis, inferential family or gate
order changes. All pre-data. The registry merge mechanism and the meaning of
`n_tokens_raw` were clarified and ratified by the owner on 2026-08-14 after the
PR #1 pre-merge review.

Authority for each: D54(v) explicitly defers the return shape of
`alphabet.map_token` to separate ratification; `registry.build_registry` and the
whole of `sequences` are marked "signature finalized at implementation" in the
Phase-0 scaffold and carry no §6.2 contract.

## 1. `alphabet`

```python
@dataclass(frozen=True)
class MappedToken:
    upos: str                  # after PROPN -> NOUN (D08)
    deprel_base: str           # literal result of step 1, before any policy substitution
    kept: bool
    symbol: str | None         # None iff kept is False
    drop_reason: str | None    # 'upos_excluded' | 'deprel_excluded:<label>' | None

def strip_subtype(deprel: str) -> str
def map_token(upos_raw: str, deprel_raw: str, cfg: Mapping) -> MappedToken
```

**Relation to `tokens.parquet` (§3.7).** `MappedToken` is the transient result of
the mapping, *not* a parquet row. The row adds `language, doc_id, sent_id,
token_ord, upos_raw, deprel_raw` from the caller, and stores `symbol_id`
(int16, −1 if dropped) rather than `symbol` — ids exist only after
`freeze_alphabet` at G1.

**Totality (D09).** Total over any raw `(UPOS, DEPREL)` pair of strings: always
returns a `MappedToken`, never `None`, never raises on an unexpected label. An
*inconsistent configuration* is a different matter and must fail loud.

**Invariants (tested).**

- `kept is True` ⟺ `symbol is not None` and `drop_reason is None`
- `kept is False` ⟺ `symbol is None` and `drop_reason is not None`
- under the `oth` policy: `deprel_base == "vocative"`, `symbol == "NOUN:oth"` —
  the substitution appears only in `symbol`, so the G1 audit and GATE-A can still
  see which category was absorbed.

**Configuration coupling.** `alphabet.variant` and `alphabet.excluded_deprel_policy`
encode the same choice twice. The canonical combinations are exactly the three
alphabet-policy cells of D37:

| variant | excluded_deprel_policy | symbol |
| --- | --- | --- |
| `ud23` | `drop` | `f"{UPOS}:{deprel_base}"` |
| `ud23_oth` | `oth` | `f"{UPOS}:{deprel_base}"`, excluded → `f"{UPOS}:oth"` |
| `upos_only` | `drop` | `UPOS` |

Any other pairing raises. Silent acceptance would let a run claim a cell it did
not compute.

**`upos_only` (D31).** Steps 1–4 stay active under the `drop` policy; only step 5
changes. §3.4 introduces the UPOS-only arm as a change of *symbol form*, not of
the retention rules, and D42(ii) reads the alphabet cells as localizing the
dependency information — which requires the position sets to stay identical to
C0. Disabling step 4 would change the observed token set and would need an
amendment to D31/D42.

## 2. `registry`

```python
def enumerate_prefixes(sentences, *, language) -> pd.DataFrame
    # columns: language, doc_id, n_sentences, n_tokens_raw
def build_registry(prefix_counts, overrides) -> pd.DataFrame
    # columns: §2.3 registry schema
```

**doc_id derivation (D03, §3.3).** Verified 2026-08-13 by a format-only probe of
one file per language (no enumeration, no counts, no assignment — the G1 audit
remains strictly after G0): `sent_id` is `<newdoc id>@<ordinal>` in both
treebanks. `doc_id` is therefore the substring before the **last** `@`
(`rsplit("@", 1)`). When `newdoc id` is present it must agree with the derived
prefix; disagreement raises.

**What stays at G1.** Full enumeration over the corpus, the human-verified
assignments in `config/registry_overrides.yaml`, and O2/O8. In particular the
probe shows Greek prefixes of the form `…perseus-grc1.1.tb.xml`, whose `.1.`
may be an internal subdivision rather than the work; if so, distinct prefixes
must be merged. Which real prefixes resolve to one document is decided only at
G1; the mechanism is fixed here.

**Override merge mechanism (owner-ratified 2026-08-14).** The overrides mapping
remains keyed by the raw prefix emitted by `enumerate_prefixes`. Each assignment
may carry `canonical_doc_id`, a nonempty string defaulting to that raw prefix.
`build_registry` groups assignments by this target and sums `n_sentences` and
`n_tokens_raw`. Every prefix in a merged group must agree on `language`,
`source_urn`, `author`, `work`, `regime`, `meter`, `period`, and `flags`; a
conflict raises with the field, both raw prefixes, and canonical target. Because
`source_urn` defaults to the raw prefix, a real multi-prefix merge **must** set
the same explicit `source_urn` on every contributing assignment — without it the
defaults differ and the merge raises. This preserves the raw-prefix-to-document
trace in the overrides while keeping one row per observed document in the §2.3
registry.

**Canonical target validation (owner-ratified 2026-08-14, including the
post-merge hardening below).** A wrong merge target is silent: every sentence stays
assigned, so §3.3's "the audit fails on any unassigned sentence" never fires,
while the resulting document count fixes the exact enumeration sizes of D43 and
therefore the attainable p floors. Two rules reject unshared mistyped targets
while preserving shared synthetic canonical IDs:

1. a target may differ from its raw prefix **only if at least two raw prefixes
   share it**. An unshared target means no merge is happening, so it can only be
   an error. This rejects unshared invented targets, and rejects near-miss typos
   and Unicode homoglyphs when they *split* a group into singleton targets;
2. a merge target must be a **stable root**: if A → B then B → B. No chain or
   cycle may make the intended document ambiguous.

All topology violations are reported in one error, each naming the raw prefix
and its target. Invalid target values still fail immediately. The target is
deliberately **not** required to be an existing raw
prefix: merging subdivisions `X.1`/`X.2` into `X` must stay legal where a bare
`X` never occurs, and promoting one subdivision to stand for the whole document
would be arbitrary.

These rules bound the mechanism, not the inventory. They cannot detect a typo
that lands on another *valid* group, nor a semantically wrong but
correctly-shaped assignment. That is the job of the §3.3 cross-check against
§2.3, which remains a G1 deliverable and is specified in §5 below.

**`n_tokens_raw` (owner-ratified 2026-08-14).** Count the integer-ID syntactic
word rows yielded by the D54 reader, before alphabet mapping or retention. MWT
range rows and empty nodes are excluded; their integer-ID word components —
including split Latin clitics — are counted separately. PUNCT and every other
representation category are still included. This is the raw population used by
the G1 audit and the GATE-A/GATE-B denominators.

`n_tokens_retained` (§2.3) is nullable `Int64` during G0 — it depends on the
frozen alphabet — and must be complete before the G1 freeze.

## 3. `sequences`

```python
def build_sequences(tokens_with_sent_ord) -> pd.DataFrame
    # columns: language, doc_id, sent_ord, symbols (list<int16>)   [§3.7]
def extend_alphabet_bound(alphabet: Mapping[str, int]) -> dict[str, int]
def to_model_input(sequences, *, doc_id, boundary, boundary_id=None) -> list[list[int]]
```

- `sequences.parquet` is always sentence-based and never contains `#`. P-BOUND is
  produced at run time (D52(x)).
- P-RESET → one sequence per sentence. P-BOUND → a single stream per document
  with exactly `n_sentences - 1` boundary symbols; documents are never
  concatenated (`doc_id` is keyword-only and required, so "never spans
  documents" is structural rather than a convention).
- All-dropped sentences remain rows with `symbols == []`; under P-BOUND this can
  produce adjacent boundary symbols, which is correct and not special-cased.
- `extend_alphabet_bound` returns a new mapping with `#` at id `|A|`; all
  existing ids are stable and the input is not mutated. `alphabet.json` is never
  rewritten (D52(x)).
- The output of `to_model_input` is exactly what `ContextTree.fit(sent_seqs)`
  accepts in §6.2, under both policies.

**`sent_ord` is an input, not a derivation.** It must be carried through the
encode stage. It may **not** be reconstructed by sorting `sent_id` strings: the
ordinal is numeric inside a string, so `…@10` sorts before `…@3` and document
order would be silently scrambled. How `sent_ord` is computed — sentences of one
document are spread across the UD split files, which D03 ignores — is an encode
question resolved at G1. Tracked below.

## 4. Manifest extension (D52(x))

D52(x) requires the run-time alphabet extension to be "recorded in the run
manifest", and §7 places that requirement in the `test_sequences.py` row, i.e.
inside the G0 set. `build_manifest` returned a closed dict with no route to
carry it. Ratified additional keyword-only field:

```python
build_manifest(..., *, inputs=(), alphabet_extension=None)
```

emitting, when supplied:

```json
"alphabet_extension": {
  "base_size": 123,
  "added_symbols": {"#": 123},
  "runtime_size": 124
}
```

`None` (P-RESET runs) omits the key, so existing manifests are unaffected.

## 5. Tracked, not decided here

- **`sent_ord` derivation at G1.** Needs a defined document ordering across the
  UD split files. Naming it here so it cannot become a silent convention in the
  encode stage.
- **`|A⁺|` wherever `|A|` enters the tree — GATED:G3.** D52(x) binds the P-BOUND
  extension to `|A⁺| = |A| + 1` "used wherever `|A|` enters", and `|A|` enters the
  instrument twice: the smoothing denominator `N_s + β·|A|` of every predictive
  probability (§4.2) and the `β ∈ {1/|A|, 0.25, 1.0}` one-at-a-time sensitivity
  cell (§5.6). On a P-BOUND run both must read `|A⁺|`. Nothing at G0 consumes
  `|A|` — §3.5 builds the extension, the manifest records it, and there the chain
  stops — so there is nothing to implement or test here; the clause is named so it
  cannot become a silent convention when the context tree lands at G3. The G0
  extension itself is already tested (`test_sequences.py`, §7).
- **Greek prefix granularity** (`…grc1.1.…`): work vs internal subdivision —
  G1 audit, coupled to O2/O8.
- **Semantic inventory check, required before the G1 freeze.** The target rules
  above bound the merge *mechanism*; they cannot tell a correctly-shaped wrong
  assignment from a right one. Before `registry`, `alphabet.json` or T\* are
  frozen, the audit must fail loud unless:
  1. the set of `(language, author, work, regime)` in the built registry equals
     the set declared in Spec §2.3 — **identity first**, since a count check
     alone is satisfiable by a wrong assignment that preserves n, and a split
     can cancel a merge;
  2. the per-regime document counts match the declared analysis sets (Greek
     HEX 5 / PROSE_CLASS 6; Latin HEX 2 / PROSE 6);
  3. the exact enumeration sizes recomputed from the built registry match the
     applicable D43 rows: primary Greek 462 / 2048, Latin 28 / 256 and
     Lysias-merged 56 / 256; author-level 20 / 64 under the 3/3 O2/O8 partition,
     or 10 / 32 if the Hymn is aggregated to Homer. This is a *derived* check,
     not an independent one — it is the last line, not the first.

  This implements the cross-check against §2.3 that §3.3 already requires, and
  makes it mechanical rather than by eye, following the D52(iii) precedent. It is
  **not implemented here**: expectation (1) requires transcribing §2.3's document
  tables and the **O2** ruling. Keeping the Hymn to Demeter as its own anonymous
  block or aggregating it to Homer leaves Tier 1 at 5 Greek HEX documents but
  changes the semantic identity and author-block cardinalities; excluding it would
  instead reduce Greek HEX to 4 and require an amendment to §2.3 and D43. Writing
  the expectation before that ruling would hard-code a guess into the check meant
  to catch guesses.
