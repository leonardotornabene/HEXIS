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
`source_urn` defaults to the raw prefix, a real multi-prefix merge normally sets
the same explicit `source_urn` on every contributing assignment. This preserves
the raw-prefix-to-document trace in the overrides while keeping one row per
observed document in the §2.3 registry.

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
- **Greek prefix granularity** (`…grc1.1.…`): work vs internal subdivision —
  G1 audit, coupled to O2/O8.
