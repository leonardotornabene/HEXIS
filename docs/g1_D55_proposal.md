# D55 — proposal, NOT applied

**Status: PROPOSED.** Drafted to slot into `02_DECISION_LOG.md` §II after
ratification. Two things are being proposed here, and they stand differently:

- **Every scientific and governance item — §(i)–(xiii), §(xv)–(xvi) — is applied
  to nothing.** `01_MASTER_SPEC.md`, `02_DECISION_LOG.md`, `CLAUDE.md`,
  `AGENTS.md`, `README.md` and `config/` are untouched, and no alphabet, registry
  or T\* is frozen.
- **The thirteen software conventions in §(xiv) are implemented**, because the evidence
  in this document could not be produced without them: two audit runs that differ
  only in mode would otherwise overwrite each other, and an unratified registry
  would otherwise be able to produce a canonical report. They are in force in the
  pre-audit pipeline and are submitted here for ratification like everything else.
  Ratifying them changes no result; rejecting them means changing the stage before
  the canonical audit runs.

Prepared at the G1 pre-audit, 2026-08-15/16; revised 2026-08-17 after a full audit
of the branch, which added §(xvi), took the GATE-A declared readings from three to
five (§xiii), and attached to option A the two counterweights that were only
reachable from later sections (§iii). Revised again **2026-08-20**, after a review
of the ratification sheet against this document, the spec and the code: added the
third counterweight to option A and **route A\*** (§iii), the **document scope** of
the alphabet inventory and the version-control clause (§xv), a fourth expectation
to the semantic inventory check (§xvi), the **`D29-A1`** row this ledger was
missing (§Governance), the split of §(viii) between the registry-schema constraint
and the ordering rule, and checklist items **21–23**. No figure below comes from a
model (D30 intact — counts only, no fit).

**Provenance, stated precisely.** Two classes of evidence, not one:

1. **From the pre-audit reports**, with each set of numbers tied to the run that
   produced it. Both runs share
   `config_sha256 = 53f76d297774bba46042d97e6170b093fcef4833a4633633a7712192d14b2440`
   (C0 as committed in `config/default.yaml`), and both manifests live at
   `results/logs/<run_id>/manifest.json` carrying the SHA-256 of every input and
   artifact.

   A run is cited by the **stable half** of its identity, `{config_hash}_{inputs
   fingerprint}` — the trailing date component is the regeneration date and moves
   whenever the artifacts are rebuilt, while the fingerprint does not, because it
   is a digest of the inputs themselves.

   | run (stable identity) | overrides | what is read from it |
   | --- | --- | --- |
   | `preaudit_53f76d297774_75e8a4ae9993` | `config/registry_overrides.yaml` (empty) | the 18 + 12 raw-prefix enumeration; per-prefix sentence, raw and retained counts; per-prefix retention (min 80.8%); \|A_grc\| = 106 and \|A_la\| = 102 |
   | `preaudit_53f76d297774_f389dca36708` | `docs/g1_registry_proposal.yaml` | the 29-document canonical inventory (Athenaeus merged); per-regime drop rates and restricted-position fractions; the per-regime excluded-DEPREL shares (max 1.28% grc / 1.11% la) |

   The full id appends the day the artifacts were last rebuilt. That component is
   deliberately **not** quoted here: pinning it makes this document stale on the
   next regeneration, and the commit sequence below requires at least one more.
   Read it off the filenames in `results/tables/`.

   **What is and is not reproducible, precisely.** Regenerating on the same day
   reproduces the report, the CSVs and the sidecars **byte for byte** — verified.
   The **manifest never does**, because it records `created_utc`, a wall-clock
   timestamp; and across a day boundary the `run_id` changes, which changes the
   filenames, the "Run id" line inside the report, and therefore the sidecars too.
   Stable in every case are the counts and tables themselves and the
   `{config_hash}_{fingerprint}` half of the identity — which is why runs are
   cited by that half.

   The T\* arithmetic of §(ix) and the learning-curve grids of §(x) are derived by
   hand from the `n_tokens_retained` column of the **second** run, whose documents
   are canonical. Both runs record `mode: preaudit` and **`git.dirty: false`**:
   the flag is sampled **before** the run's own writes (§xiv, convention 11), and
   each run was generated on a clean tree and committed before the next was
   generated (`1680d3a`, `84a9319`). An earlier draft of this paragraph said
   `true`, describing the sequence as planned rather than as executed.
2. **From evidence outside those reports**, and so cited on its own terms: the
   MWT count and UD commit SHAs (`data/raw/PROVENANCE.md`); the README-vs-data
   divergence (the treebank READMEs at the pinned commits); the `sent_ord`
   ordinal evidence; and the document identifications — **23 of the 30** from
   local checks against the source text (not committed — D28), the remaining
   **7** from catalogue evidence alone, itemised in the registry proposal.

**Licence note (D28).** This document identifies documents by TLG/PHI id, CTS
URN, `sent_id` prefix and counts. No text of the treebanks is reproduced.

**Identifications are not uniform**, and the split is recorded per row in
`docs/g1_registry_proposal.md`: **23 of the 30** were checked locally against the
source text (those checks are not committed), and **7 rest on catalogue evidence
alone** — Hesiod ×3, Diodorus bk 11, the Hymn, and Athenaeus bks 12 and 13. Two of
the seven carry decisions: the Hymn carries O2/O8, and the Athenaeus pair carries
the merge.

---

## D55 — The corpus does not match §2.3, and the inference plan's constants follow the corpus

**Q.** §2.3's works tables, §4.2's 𝔻 = 11, and the enumeration constants of
D21/D24/D33/D43 (462 / 2048 / 20 / 64 / 56 / 256, restated in `CLAUDE.md`) all
presuppose a document inventory. The G1 enumeration is the first time that
inventory has been read off the pinned data. It does not match.

### (i) The finding, stated narrowly

Enumerating `sent_id` prefixes over the pinned commits
(`37837c7a…` grc, `a296f012…` la, both r2.18) yields **18 raw prefixes in
`grc_perseus` and 12 in `la_perseus`**. The totals confirm the enumeration is
complete, not a filtering artifact: 13,919 sentences / 202,989 syntactic words
(grc) and 2,273 / 29,223 + 355 MWT (la), each matching §2.2 exactly.

The treebank READMEs list ~31 Greek works and 11 Latin ones. The verifiable fact,
and the only one asserted here: **at the pinned commit the README works table and
the `.conllu` contents disagree.** No claim is made about the cause.

Not present in `grc_perseus` at r2.18, though listed in §2.3: Lysias ×4,
Polybius, Apollodorus, Aesop, and 6 of the 7 Aeschylus plays (only
`tlg0085.tlg001`, *Suppliant Women*, is present).

Confirmed unchanged: §2.2's tag inventories and the E7 confirmations — grc 15/17
UPOS (no PROPN, no SYM) with 28 DEPREL types; la 16/17 UPOS (adds PROPN) with 48
types = 28 base + 20 subtypes; 355 Latin MWTs; Thucydides present.

### (ii) Errata corrected: E1 and E2

- **E1** ("grc_perseus contains far more than the proposal lists — 12 tragedies
  and six post-classical prose authors [VERIFIED]") is **contradicted**. The
  release holds **6 tragedies** (Sophocles ×5, Aeschylus ×1) and **3**
  post-classical prose authors (Athenaeus, Diodorus, Plutarch). The
  three-regime design survives; its dimensions do not.
- **E2** ("Caesar is absent") is **contradicted**. `phi0448.phi001` is Caesar,
  *De bello Gallico* (24 sentences / 352 raw / 304 retained tokens), absent from
  the Latin README works table.
- **E5** (proposal's "3 Greek / 6 Latin treebanks") is **not** touched here. It
  concerns the count of UD treebanks, not the contents of the two pinned ones,
  and remains open as **O1**.

### (iii) Greek primary contrast — an explicit choice, not a default

Applying §2.3's labels to the actual inventory (`docs/g1_registry_proposal.yaml`)
gives, in Greek: HEX **5** (unchanged), PROSE_CLASS **2** (Herodotus bk 1,
Thucydides bk 1), OTHER_VERSE 6, PROSE_POST 5 raw prefixes → 4 documents if
Athenaeus 12+13 merge.

**Option A (recommended) — keep PROSE_CLASS as the primary prose set.**
𝔻 = 5 + 2 = 7. Conservative: it preserves the estimand "hexameter vs *classical*
prose" and keeps PROSE_POST intact as the chronological control arm.

**Read this recommendation with its three counterweights, all established below
and none visible from this paragraph alone.** (i) §(iv-bis): if O7 sends P1 to
a relabelling test, option A removes confirmatory attainability at document level
entirely, while option B survives it — the strongest single argument in B's
favour found anywhere in this amendment. (ii) §5.3 and the touched-documents
table: with a prose side of **2** documents, the between-document bootstrap is
not merely "crude" but near-degenerate — resampling 2 with replacement has 3
distinct outcomes — and the per-document dot plots (F3–F4) carry 7 points, of
which 2 carry the entire prose group. (iii) §(v): **even with the sign-flip
standing**, P2 cannot be the *first* rejection of the Holm family under option A,
its floor 0.0476 exceeding α/2 = 0.025 — so P2 rejects only if P1 rejects first
**and** P2 lands exactly on its floor, i.e. the 5 HEX and 2 PROSE values separate
perfectly, one arrangement out of 21. Under option A the confirmatory layer
therefore rests on P1 alone, which is the one statistic whose validity O7 leaves
open. The recommendation stands on the estimand
and on keeping the chronological control arm; it does not stand on power.

**Option B — GRC-PROSE := PROSE_CLASS ∪ PROSE_POST**, mirroring Latin's
PROSE_ALL (§5.7). 𝔻 = 5 + 6 = 11, restoring C(11,5) = 462 and 2¹¹ = 2048 exactly.
This must not be adopted merely because it restores the constants. Its full
consequences:

1. the estimand changes from "classical prose" to **diachronic prose** spanning
   Herodotus to Athenaeus — roughly seven centuries;
2. the **chronological control arm is consumed**: PROSE_POST can no longer serve
   as the independent period contrast, since it is inside the primary;
3. period becomes a confound *within* the primary contrast, requiring a new entry
   in the §5.8 confound register;
4. author blocks recompose, and **how** depends on O8, which is still open.
   PROSE_ALL contributes 5 blocks (Herodotus, Thucydides, Athenaeus, Diodorus,
   Plutarch); both O8 readings give unequal group sizes, so the one- and two-sided
   label-permutation floors coincide (D43):

   | O8 reading | HEX / PROSE blocks | P2 | P2 floor | P1 | P1 floor |
   | --- | --- | --- | --- | --- | --- |
   | Hymn-anon | 3 / 5 | C(8,3) = 56 | 1/56 ≈ 0.0179, both sides | 2⁸ = 256 | 1/256 ≈ 0.0039 one-sided; 2/256 ≈ 0.0078 two-sided |
   | Hymn → Homer | 2 / 5 | C(7,2) = 21 | 1/21 ≈ 0.0476, both sides | 2⁷ = 128 | 1/128 ≈ 0.0078 one-sided; 2/128 ≈ 0.0156 two-sided |

   Option B does not restore the author-level constants — and, read through Holm
   rather than through P2's floor alone, it does something more consequential.
   **With the sign-flip standing, under both O8 readings the author-level family
   becomes capable of joint significance**: P1 clears the first threshold (0.0039
   or 0.0078, both < 0.025) and P2 then clears the second (0.0179 or 0.0476, both
   < 0.05). D43(iii) withdrew α at Tier 2 precisely because the author level could
   not attain joint significance; under option B that premise fails, so **option B
   reopens D43(iii)**. Under option A neither reading attains anything at author
   level (§(vii)), so option A leaves D43(iii) standing on its original reasoning.

   **O8 becomes determinant only if P1 moves to a relabelling test** (§(iv-bis)):
   Tier 2 then has floor 1/56 ≈ 0.0179 under Hymn-anon, which still starts the
   family, but 1/C(7,2) = 1/21 ≈ 0.0476 under Hymn → Homer, which does not. So
   "option B reopens D43(iii) regardless of O8" holds under the sign-flip and
   **not** under that remedy — a qualification an earlier draft of this amendment
   omitted;
5. the O7 calibration study must be rebuilt on 11 pseudo-documents with a 5/6
   profile;
6. the merge of Athenaeus 12+13 becomes **load-bearing**: without it PROSE_ALL is
   7 documents and 𝔻 = 12, not 11.

If option B is chosen it is a **pre-model redesign**, declared as such in the
preprint, taken with the linguistic supervisor — not a technical correction.

**Route A\* — option A with a pre-registered conditional switch (added
2026-08-20).** The A/B choice is being taken **before** the one study that would
inform it. O7 is a G3 study, and the roadmap's G3 description says its size
profile is available *after* G1 — so the amendment that fixes 𝔻 must be filed
before the calibration that says whether 𝔻 = 7 can carry a confirmatory family at
all. That loop is real, and it has a third exit which is neither A nor B but a
rule about them:

> **Primary contrast = option A.** If O7 invalidates the exact sign-flip for P1
> **and** the replacement scheme it validates has, at 𝔻 = 7, a minimum attainable
> one-sided p greater than α/2 = 0.025, the primary contrast becomes option B.
> Both T\* values are frozen at G1 from the ratified registry by the same rule
> (`t_star`, §xi, run twice): **T\*_grc = 9,346 under A and 11,043 under B**.

What it costs: `t_star` runs twice and both results are frozen; `D25-A1` (the
claim template) is filed **conditionally** rather than not at all; `D37-A1` (the
fit budget) states both figures; and the preprint declares the rule together with
its trigger. What it buys: the branch in which option A leaves nothing attainable
at document level (§iv-bis) stops being a discovery at G3 and becomes a
contingency named before any model is fitted.

**Why this is not estimand-shopping.** The trigger is a property of the
*randomization scheme*, measured on **synthetic** data, and it is written down
before the calibration runs. No real-data quantity enters it, D30 is untouched,
and every real-data number that could inform the choice — the document counts,
the token counts, both T\* values, the GATE-A shares — is already on the table
today. The alternative is not a purer design: it is the same switch taken at G3
without having been declared.

### (iv) Recomputed enumeration constants under option A

Every floor states its sidedness, as D43 requires.

| quantity | §5.1 / D43 as written | option A | floor |
| --- | --- | --- | --- |
| P2 label permutation (document) | C(11,5) = 462 | **C(7,5) = 21** | 1/21 ≈ 0.0476, one- and two-sided coincide (5/2 unequal) |
| P1 sign-flip (document) | 2¹¹ = 2048 | **2⁷ = 128** | 1/128 ≈ 0.0078 one-sided; 2/128 ≈ 0.0156 two-sided |
| P2 author-level (Hymn-anon) | C(6,3) = 20 | **C(5,3) = 10** | 1/10 = 0.10, one- and two-sided coincide (3/2 unequal) |
| P1 author-level (Hymn-anon) | 2⁶ = 64 | **2⁵ = 32** | 1/32 ≈ 0.031 one-sided; 2/32 ≈ 0.063 two-sided |
| Lysias-merged rerun (D20/D43(iv)) | C(8,3) = 56, 2⁸ = 256 | **no referent** | — |

The author-level rows assume the Hymn-anon reading of O8; the alternative is
tabled in §(vii) and is materially worse.

**One clause is struck, not two decisions.** D20 is the **transfer protocol**
itself — document-level LODO, T\*-matched subsampling, S = 20 seeds, ΔCE — of
which the Lysias-merged rerun is a single trailing clause. What has no referent is
**that clause and D43(iv)**: Lysias is not in the release. Everything else in D20
stands untouched, and an earlier draft of this amendment which said "D20 … is to
be struck" would have deleted the main protocol along with it.

Deleting a declared robustness analysis is a real loss and is recorded as such,
not quietly dropped: Tier 1's only within-author robustness check disappears with
it, leaving Tier 2 (itself without α) as the sole answer to intra-author
dependence.

### (iv-bis) Every attainability statement below is conditional on O7

O7 — whether the exact sign-flip is a valid null for P1 — is **open and blocking
for G2/G5** (D44). Every P1 floor in this amendment assumes the sign-flip stands:
2ⁿ over documents, 2^blocks over author blocks.

If it does not, D44 does not prescribe a single replacement. **One** remedy is to
test P1 by refitting under relabelling, whose orbit is then the label-permutation
orbit over the same set — that is the branch tabled below, and it is tabled
because its arithmetic is computable, not because it is the only outcome. D44
equally permits **some other validated scheme**, whose orbit is unknown until O7
names it; nothing here forecloses that, and the table below must not be read as
"the two possible futures".

Under the refit remedy specifically:

| arm | P1 floor if sign-flip stands | P1 floor if P1 becomes a relabelling test | family under Holm |
| --- | --- | --- | --- |
| Option A, documents | 1/128 ≈ 0.0078 | **1/C(7,5) = 1/21 ≈ 0.0476** | nothing attainable: 0.0476 > 0.025, so the family cannot start |
| Option B, documents | 1/2048 ≈ 0.00049 | 1/C(11,5) = 1/462 ≈ 0.0022 | both steps attainable either way |
| Latin | 1/512 ≈ 0.0020 | **1/C(9,2) = 1/36 ≈ 0.0278** | nothing attainable: 0.0278 > 0.025 |
| Option B, Tier 2, Hymn-anon | 1/256 ≈ 0.0039 | 1/C(8,3) = 1/56 ≈ 0.0179 | attainable either way |
| Option B, Tier 2, Hymn → Homer | 1/128 ≈ 0.0078 | **1/C(7,2) = 1/21 ≈ 0.0476** | nothing attainable, so O8 becomes determinant |

The consequence for the option A / option B decision is sharp and should be on the
record before it is taken: **under option A, the refit remedy removes confirmatory
attainability at document level entirely**, because P1 and P2 would then share the
same 21-element orbit and neither could clear the first Holm threshold. Option B
survives it at document level. This is a dependency between two
decisions that are otherwise unrelated, and it is the strongest argument in
option B's favour found anywhere in this amendment.

Nothing here pre-empts O7: it is a G3 study on synthetic data, and this section
records what each of its two outcomes would imply. Every statement in §(v)–(vii)
is to be read under "if the sign-flip stands".

### (v) Holm attainability — correcting the wording, not only the numbers

P2's floor 0.0476 exceeds Holm's **first** threshold α/2 = 0.025 but lies below
the **second**, α = 0.05. So the correct statement is:

> P2 cannot be the first rejection of the Holm family. It can still be rejected at
> the second step, provided P1 is rejected first at 0.025.

The formulation "P2 can no longer attain Holm significance" is **wrong** and must
not enter the record. Amends the attainability wording of D33 and D43(ii)–(iii).
Note the asymmetry this creates: the family's power now depends on P1 being the
smaller p-value, which is a declared structural feature of the plan under option A,
not an artifact of any dataset.

### (vi) Latin — Caesar, and the constants that follow

`phi0448.phi001` = Caesar, *De bello Gallico*
(`urn:cts:latinLit:phi0448.phi001.perseus-lat1`; Perseus/Scaife catalogue),
identified locally by author id and text. **Proposed: PROSE_CLASS**, flagged
`absent_from_readme`, `contradicts_e2`, `smallest_document`.

Excluding it would require an explicit motivation on the record. Size alone is
not one: at 304 retained tokens it is small, but Vergil's *Aeneid* — a **primary
HEX document** — has 638, and Augustus's *Res Gestae* 620. A size-based exclusion
rule that removes Caesar would have to be applied consistently, and applied
consistently it would gut the Latin arm.

With Caesar included, LA-PROSE := PROSE_CLASS ∪ PROSE_POST = 4 + 3 = **7**, so
𝔻_la = 2 + 7 = 9:

| quantity | §5.7 as written | with Caesar | floor |
| --- | --- | --- | --- |
| P2-Latin label permutation | C(8,2) = 28 | **C(9,2) = 36** | 1/36 ≈ 0.0278, one- and two-sided coincide (2/7 unequal) |
| P1-Latin sign-flip | 2⁸ = 256 | **2⁹ = 512** | 1/512 ≈ 0.0020 one-sided; 2/512 ≈ 0.0039 two-sided |

**§5.7's stated reason does not survive, though its decision may.** §5.7 excludes
Latin because "min p ≈ 0.036 > 0.025 → Latin cannot enter the Holm family". That
is the same faulty step corrected in §(v): exceeding the *first* Holm threshold
does not put a test out of reach, only out of reach *first*. Within a two-member
Latin family, Holm could reject both — P1 at 0.0020 < 0.025, then P2 at
0.0278 < 0.05 — and this was already true at 0.036 before Caesar was found.

So Latin's qualitative status (L1) has to rest on its own reasons, which are
real and unaffected: T\*_la = 638 retained tokens, two orders of magnitude below
the size §4.1 profiles against; `d_max = 6` against C0's 8, a declared
configuration difference; and L1's stated role as replication rather than
confirmation. **Restated:** Latin is qualitative **by design decision**, not by
structural impossibility.

**Family membership: the arithmetic, computed, so the choice is informed.** A
Latin family of 2 uses thresholds α/2 = 0.025 and α = 0.05; a joint family of 4
uses α/4 = 0.0125, α/3 ≈ 0.0167, α/2 = 0.025, α = 0.05. Applying Holm step-down to
the floors of §(iv), §(vi) and §(iv-bis):

| scenario | Greek family of 2 | Latin family of 2 | joint family of 4 |
| --- | --- | --- | --- |
| A + sign-flip | both attainable | both attainable | **only the two P1s** — P2-Latin's 0.0278 exceeds the third threshold 0.025 |
| B + sign-flip | both | both | **all four** |
| A + refit remedy | none | none | none |
| B + refit remedy | both | none | **only the two Greek** |

Two consequences worth stating plainly, neither of them a matter of taste:

1. **Joining Latin to the Greek family never gains a rejection and can cost two.**
   Under A + sign-flip, separate families make all four tests attainable while the
   joint family reaches only the two P1s. Holm's thresholds tighten with family
   size, and Latin's floors are the loosest in the set, so Latin's admission
   spends α that Greek was using.
2. **What separation costs is control, not power.** Two families of 2 control α
   within each language and nothing across them; the joint family controls α over
   all four. The choice is between a stronger claim about fewer things and a weaker
   claim about more — and it should be made on that basis, not on the attainability
   counts above.

This amendment records the arithmetic; the decision is the owner's.

Amends D24, D43 and §5.7 — the arithmetic **and**, in §5.7, the rationale.

### (vii) O2 resolved at document level; O8 remains open

**O2 — resolved, partially.** `grc_perseus` contains exactly one Hymn-to-Demeter
prefix, `tlg0013.tlg002` (166 sentences / 2,061 raw / 1,761 retained). The
README's listing of the work under both "Anonymous" and "Pseudo-Homer" is a
catalogue duplication, **not** a data duplication. No merge is required and
GRC-HEX remains 5 documents.

**O8 — still open, and still consequential.** O2's document-level resolution does
*not* settle which **author block** the Hymn belongs to. Both readings remain
live, and D43's sidedness rule is stated for each (the two-sided floor doubles the
one-sided one only when the randomization orbit contains the sign-mirror — always
for sign-flips, and for label permutations only with **equal** group sizes):

| O8 reading | HEX / PROSE blocks | P2 permutation | P2 floor | P1 sign-flip | P1 floor |
| --- | --- | --- | --- | --- | --- |
| Hymn-anon (own block) | 3 / 2 — unequal | C(5,3) = 10 | 1/10 = 0.10, one- and two-sided coincide | 2⁵ = 32 | 1/32 ≈ 0.031 one-sided; 2/32 ≈ 0.063 two-sided |
| Hymn → Homer | 2 / 2 — **equal** | C(4,2) = 6 | 1/6 ≈ 0.167 one-sided; **2/6 ≈ 0.333 two-sided** | 2⁴ = 16 | 1/16 = 0.0625 one-sided; 2/16 = 0.125 two-sided |

P2 is two-sided, so the operative floor in the Hymn→Homer reading is 0.333.

Read through Holm rather than through either floor alone: under **option A** the
smallest attainable p in the author-level family is P1's — 0.031 (Hymn-anon) or
0.0625 (Hymn→Homer) — and both exceed the first threshold 0.025, so **nothing is
rejected at either step under either reading**. D43(iii)'s premise therefore
holds unchanged under option A. (It does *not* hold under option B; see §(iii).)

The two readings are still not equivalent — the gap between a P2 floor of 0.10
and one of 0.333 is large — so the reading must be recorded rather than assumed.

D43(vi)'s branch therefore **cannot be declared inert**. The decision is the
linguistic supervisor's and belongs to the ratification, not to this document.

### (viii) `sent_ord` — the rule, and the evidence for it

Sentence order within a document cannot be taken from file order.

- Within `tlg0012.tlg001…` (Iliad), file order and numeric-`@N` order disagree at
  exactly two positions: `@2280661 → @2274455` and `@2282520 → @2274879`. The
  numeric ordinal is text order — verified locally, `@2274452`/`@2274453` are
  *Il.* 1.605–610 and `@2274455` is *Il.* 2.1 — while file order places Book 2
  some 2,800 sentences late.
- Four documents span two UD split files (Athenaeus 12, Athenaeus 13, Aeneid,
  Phaedrus). For the Aeneid, file order is wrong in the other direction:
  `train` holds ordinals 2–34 and `test` holds 41–175.
- No `sent_id` is duplicated anywhere in either treebank.

**Proposed rule**, in two cases, because `part_order` does not exist for most
documents:

- **single-prefix document** — `sent_ord` = rank of the numeric `@N` ordinal
  within the document. `part_order` is absent and plays no part.
- **merged document** — `sent_ord` = rank under the key `(part_order, ordinal)`.

**Proposed constraint:** when `canonical_doc_id` merges two or more raw prefixes,
`part_order` is mandatory — an integer, present for every member of the group and
unique within it. Without it the ordinals of the parts interleave and a merged
document produces duplicate or scrambled ranks. This is the only reason
`part_order` appears in the registry proposal, and it is why the Athenaeus merge
decision and the `sent_ord` rule have to be ratified together.

**Which half rides with the merge (refined 2026-08-20).** "Together" is one word
for two objects. The **constraint** is a registry-schema rule — it is what makes a
merged document well-formed — so it belongs with the merge decision (checklist 4)
and with the freeze. The **ordering rule** is read only by `run_encode` and the
P-BOUND arm, so it stays where the checklist puts it (13). Ratifying the merge
without the constraint leaves `part_order` accepted and unvalidated
(`KNOWN_OVERRIDE_FIELDS`), which is correct only for as long as nothing reads it —
and by then the file it lives in is `RATIFIED`.

Bearing: under P-RESET (primary, D10) contexts truncate at sentence start, so
sentence order does not affect the primary readings. It affects the P-BOUND
sensitivity cell and the F7 block figure. It is settled now because it is cheap to
settle now, not because a primary result depends on it.

### (ix) T\* — derivation, and the contingency it triggers

`t_star` is **not implemented** (see §(xi)). The values below are arithmetic over
the `n_tokens_retained` column of the pre-audit report, shown in full so that a
reader who never runs the code can recompute them.

Greek retained tokens under C0, by **canonical document** (the provisional run
applies the proposed Athenaeus merge, so its inventory has 29 rows, not 30):
Iliad 69,327 · Athenaeus 23,133 (= bk 12 10,129 + bk 13 13,004) · Herodotus
17,301 · Diodorus 15,266 · Thucydides 9,346 · Plutarch *Lyc.* 4,481 · Plutarch
*Alc.* 4,403 · Theogony 4,023 · *W&D* 3,189 · *Shield* 2,070 · Hymn 1,761.
Latin: Petronius 4,812 · Sallust 4,130 · Phaedrus 3,383 · Propertius 2,318 ·
Ovid 2,205 · Jerome 1,827 · Suetonius 1,748 · Cicero 1,571 · Tacitus 730 ·
Vergil 638 · Augustus 620 · Caesar 304.

The Athenaeus merge is load-bearing for option B only: it is in PROSE_POST, which
option A's primary contrast excludes.

**Option A, Greek.** HEX = 80,370; PROSE_CLASS = 26,647; 𝔻 = 107,017.

| protocol | training condition | available |
| --- | --- | --- |
| (b) | HEX ∖ Iliad | 80,370 − 69,327 = 11,043 |
| (b) | PROSE ∖ Herodotus | 26,647 − 17,301 = **9,346** |
| (b) | PROSE ∖ Thucydides | 26,647 − 9,346 = 17,301 |
| (b) | cross-regime pools (full HEX / full PROSE) | 80,370 / 26,647 |
| (c) | 𝔻 ∖ Iliad | 107,017 − 69,327 = 37,690 |

**T\*_grc = 9,346**, binding condition **protocol (b), training regime
PROSE_CLASS, evaluation document Herodotus** — the pool is then Thucydides alone.

This **contradicts D51(iii)**, which pre-registers "HEX minus Iliad" as the
expected binding condition. The expectation was formed when PROSE_CLASS had 6
documents; with 2, the prose side binds. D51(iii)'s expectation is to be updated
to record the actual condition.

**Option B, Greek** (Athenaeus merged). PROSE_ALL = 73,930; 𝔻 = 154,300.
Binding: (b) HEX ∖ Iliad = **11,043**; (c) 𝔻 ∖ Iliad = 84,973. **T\*_grc =
11,043** — and here D51(iii)'s expectation does hold.

**Latin** (Caesar included). HEX = 2,843; PROSE_ALL = 13,915; 𝔻 = 16,758.
Binding: (b) HEX ∖ Ovid = **638**; (c) 𝔻 ∖ Petronius = 11,946. **T\*_la = 638**,
binding condition protocol (b), training regime HEX, evaluation document Ovid —
the pool is the *Aeneid* alone.

**All three trigger §4.2's pre-registered contingency (T\* < 15k).** This
amendment is that record. Latin at 638 is not a marginal shortfall: it is
two orders of magnitude below the 40–60k fit size §4.1 profiles against, and it
should be read as a statement about what the Latin arm can support at all.

### (x) Learning-curve grid when the fixed sizes are unreachable

§4.2 fixes the descriptive grid at T ∈ {5k, 10k, 20k, T\*}. Under the T\* values
above, 20k is unreachable in every case, 10k is unreachable under option A, and
**all three fixed sizes are unreachable in Latin**. §4.2 does not say what to do.

**The grid has two parts, and an earlier draft of this amendment wrongly collapsed
them into one.** D51(ii) and §4.2 require the protocol-(c) curves to **extend
beyond T\*** where the pooled pool permits — that extension is what makes the
declared cost of the uniform T\* visible, so truncating every curve at T\* would
delete the evidence D51 exists to produce.

**Proposed rule, part 1 — the common grid** (protocols (b) and (c), the
comparable region). Keep the fixed points strictly below T\*, then append T\*. If
that leaves fewer than three points, replace the fixed grid entirely with the
proportional grid {0.25, 0.5, 0.75, 1.0} × T\*, labelling the axis proportional
wherever it is plotted. **Rounding: half-up to whole tokens** — stated because it
bites here (0.25 × 9,346 = 2,336.5 and 0.75 × 9,346 = 7,009.5 are exact halves,
and Python's built-in `round` is banker's rounding, which would give 2,336 and
7,010 from the same rule).

**Proposed rule, part 2 — the protocol-(c) extension** (D51(ii)). Beyond T\*,
protocol (c) alone continues at the fixed points that exceed T\* and do not exceed
the binding protocol-(c) pool. These points carry no protocol-(b) counterpart by
construction and are plotted as a visually distinct continuation.

| arm | T\* | (c) pool bound | common grid | (c) extension |
| --- | --- | --- | --- | --- |
| Greek, option A | 9,346 | 37,690 | proportional {2337, 4673, 7010, 9346} | {10000, 20000} |
| Greek, option B | 11,043 | 84,973 | fixed {5000, 10000, 11043} | {20000} |
| Latin | 638 | 11,946 | proportional {160, 319, 479, 638} | {5000, 10000} |

Latin is the case that shows why the extension matters: the common region ends at
638 tokens while protocol (c) reaches 11,946 — a factor of nearly twenty. Curves
built on a fixed grid and curves built on a proportional one are never overlaid,
and the F8 caption names the grid in force and where the (c) extension begins.

### (xi) `t_star` signature, submitted for approval

`protocols/sampling.py` states its interface is unspecified in §6.2 and that
signatures are to be proposed for approval before implementation. Proposed:

```python
def t_star(
    registry: pd.DataFrame,
    *,
    language: str,
    contrast: tuple[Collection[str], Collection[str]],
) -> TStarResult
```

- operates on **one language at a time**;
- `contrast` is a **pair of regime-label sets**, one per side, not a flat sequence.
  A flat `Sequence[str]` cannot express the contrast at all once a side is a union:
  `["HEX", "PROSE_CLASS", "PROSE_POST"]` does not say which side PROSE_POST is on.
  Greek option A is `(("HEX",), ("PROSE_CLASS",))`; Greek option B and Latin are
  `(("HEX",), ("PROSE_CLASS", "PROSE_POST"))`. `PROSE_ALL` is a name for that union
  and is **never** matched as a registry label;
- scope is D51(i): the primary contrast only; exploratory arms are reported at
  their own binding sizes;
- returns the minimum, the binding condition, the full per-condition table, and
  the `< 15k` contingency flag;
- requires `registry.n_tokens_retained` to be complete and raises if it is not.

**Precondition chain, to run before it at the canonical audit:**
C0 token mapping → aggregate retained tokens per canonical `doc_id` → fill
`registry.n_tokens_retained` (left null by `build_registry` by design) → validate
no NA remains → `t_star`.

**Two `config/default.yaml` keys cannot hold the result in their present shape**
(proposed, **not applied** — `config/` is untouched by this amendment):

| key | now | proposed |
| --- | --- | --- |
| `scores.t_star` | `null` — one scalar | `{grc: null, la: null}` — T\* is per language (§4.2), and the two differ by more than an order of magnitude (9,346 vs 638) |
| `corpus.primary_contrast` | `{grc: [HEX, PROSE_CLASS], la: [HEX, PROSE_ALL]}` — a flat pair in which `PROSE_ALL` is a label that does not exist | `{grc: [[HEX], [PROSE_CLASS]], la: [[HEX], [PROSE_CLASS, PROSE_POST]]}` — one label set per side, so the union is spelled out where it is declared rather than resolved by convention downstream |
| `scores.learning_curve_T` | `[5000, 10000, 20000]` | unchanged as the fixed grid, but §(x)'s two-part rule decides which of its points survive per arm and which become the protocol-(c) extension |

### (xii) D44 / O7 — the null calibration must be rebuilt

O7 is blocking for G2/G5 (D44). Its design — "partition into 11 pseudo-documents
with the size profile of the corpus" — is now wrong under option A:

- **7** pseudo-documents, not 11, with a **5/2** size profile;
- the LODO composition changes accordingly, and the protocol-(b) prose pool
  becomes a single document, which is the regime the calibration must exercise;
- **P2 cannot be calibrated at the 0.025 level at all.** Its smallest attainable
  p is 1/21 ≈ 0.0476, so the empirical rejection rate at nominal 0.025 is
  structurally zero — an uninformative number, not a passing result, and it must
  not be reported as if the test were conservative.

**Proposed:** P2 remains the positive control **at the 0.05 level**, and D55
declares 0.05 as the only nominal level at which P2 is calibrated under option A.
P1 (floor ≈ 0.0078) is calibrated at both 0.025 and 0.05 as planned.

`tests/test_null_calibration.py` and `pipeline/run_null_calibration.py` are
scaffolds today and are updated **after** ratification, at G3 — not now.

### (xiii) GATE-A / GATE-B — declared readings, provisional figures

Five readings of §3.4 are declared rather than settled silently in code, and are
restated in each audit report. Readings 4 and 5 were added by the audit of
2026-08-17, which found that the reading spelled out (3) governs the case that
cannot currently bind, while the two that can were left implicit:

1. **GATE-A denominator** = all raw syntactic words of the regime; not the
   excluded subtotal, not a per-document figure.
2. **GATE-A category scope** = per excluded-deprel label, computed over the census
   of retained-UPOS tokens whose `deprel_base` falls outside the 23,
   **independently of whether the active policy drops them or maps them to
   `oth`**. Counting drops would make the gate structurally unable to fire in
   exactly the `(ud23_oth, ·)` cells D50 makes mandatory to interpret. The D05
   UPOS deletions have no alternative policy and are outside the gate.
3. **GATE-A regime scope** = the **analysed** regimes. The census covers all five
   D04 labels and every row is published; the **verdict** excludes `EXCLUDED`.

   This third reading was found late, by running the canonical branch on real
   data for the first time — the pre-audit had never exercised a verdict. D06 says
   "in any regime" and D04 does list `EXCLUDED` among the five, so the literal
   reading includes it; the substantive one does not, because an `EXCLUDED`
   document enters no estimand (not P1, P2, S1, R1 or L1, no regime aggregate, no
   T\*). The asymmetry is deliberate and rests on what firing *costs*: GATE-A is
   not a precaution but a binding change — D50 gives the `(ud23_oth, ·)` cells
   mandatory-interpretation status and puts a declared caveat on **every primary
   conclusion**. Deriving that from material the study does not analyse would make
   the report less accurate rather than more cautious.

   **GATE-B is deliberately not narrowed the same way.** §3.4 asks it to *flag a
   document for inspection*; a flag that names its own document misleads nobody,
   and implausible retention on an excluded text is evidence about the mapping,
   which is worth a look wherever it occurs. The governing principle, stated once:
   **a gate whose firing changes the study is read over the material the study
   analyses; a gate that only asks someone to look may look everywhere.**

   Today the reading changes no verdict: the single `EXCLUDED` document (Jerome,
   Vulgate) reaches a maximum share of **0.30%** against the 2% threshold and
   retains **91.2%** against the 70% one. It is declared because G1 freezes the
   verdict, not because it currently binds.

4. **Exploratory regimes keep their firing power — by decision, not by omission.**
   The narrowing of reading 3 stops at D04's disposal label. `OTHER_VERSE` and
   `PROSE_POST` are *analysed* (§1.4: specificity check, chronological-robustness
   set), so an imbalance there is evidence about the same annotation the primary
   contrast reads, and D06's category is a property of the annotation rather than
   of one regime's role in the design.

   **This is the reading that can actually bind, and the figures say so.** The
   largest excluded-deprel share anywhere in the corpus is `OTHER_VERSE`
   `vocative` at **1.28%** — 64% of the threshold — against **0.52%** in HEX and
   **0.18%** in PROSE_CLASS. D06 motivated the gate with epic invocations; the
   data put tragedy 2.5× above hexameter and both primary regimes comfortably
   below. So under **option A**, whose primary contrast is HEX vs PROSE_CLASS, a
   GATE-A trigger would most plausibly come from a regime that contributes to no
   primary estimand and would still put D50's caveat on every primary conclusion.

   That consequence is **accepted deliberately**: the alternative — deriving the
   verdict scope from the ratified primary contrast — would make the scope depend
   on the A/B decision (under option B, `PROSE_POST` joins the primary and the set
   changes), and would silence exactly the evidence that a category is unstable
   across regimes. Ratifying reading 4 is therefore a choice between two coherent
   positions, not the confirmation of a default.

5. **Language scope: shares per language, verdict per run.** Shares are computed
   per `(language, regime)`, because |A|, T\*, and the inferential families are per
   language (§4.1, §4.2, §5.7) and pooling would dilute a Latin excess against the
   Greek tally an order of magnitude larger. The **verdict is one per run**: a
   trigger in either language fires GATE-A for the whole design, since D06
   escalates the excluded-deprel *policy*, which both languages and every §5.6
   cell share. The consequence to have on record before the freeze: a Latin-only
   excess would attach D50's caveat to the Greek primary conclusions, and vice
   versa. Today the margins are wide on both sides (grc 1.28%, la 1.11%).

Provisional figures under the proposed registry — **no verdict is declared**,
because a verdict requires a ratified registry:

- highest per-regime excluded-deprel share: **grc 1.28%** (OTHER_VERSE,
  `vocative`), **la 1.11%** (PROSE_POST, `discourse`) — both below the 2%
  threshold;
- lowest per-prefix retention **80.8%** (Sophocles, *Trachiniae*), well above the
  70% GATE-B threshold.

The retention figure is a screen over **raw prefixes**, not canonical documents.
It is informative in one direction only: a token-weighted mean of values all above
the threshold is itself above it, so no merge can pull a document under 70%.

If GATE-A does fire at the canonical audit, D50 governs: C0 stays the unique
primary and no cells are added.

### (xiv) Software conventions adopted to produce this evidence

**Thirteen** conventions, all in force in the pre-audit pipeline and all submitted for
ratification. Each exists because the evidence above could not be produced safely
without it — none of them changes a number. Listed exhaustively, because earlier
drafts of this section undercounted twice.

Convention 13 was added on 2026-08-17 on the owner's authorization, after the audit
of that day found that the G1 tests carried no gate of their own. It is the only
convention that is not required to *produce* the evidence: it is required to keep
the evidence from decaying unnoticed. Its first run was itself the argument —
nineteen G1 tests passed while executing no Python assert at all, relying on
`pytest.raises(match=…)`, which is exactly what D52(iii) refuses to count. They now
capture the exception and assert on its content, so each one states what the error
must *say*, not merely that one was raised. Mutation-verified: skipping a G1 test
and stripping the only assert from another each turn `-m g1` red.

| # | convention | what breaks without it |
| --- | --- | --- |
| 1 | mode in `run_id` and artifact names | pre-audit and canonical runs over identical inputs share a name |
| 2 | input fingerprint in `run_id` and artifact names | two runs differing only in overrides collide |
| 3 | manifest `mode`/`status`, `entry_point` = the invocation | the mode is only recoverable by parsing a filename |
| 4 | `status` column in every companion CSV | a table detached from name and sidecar looks canonical |
| 5 | `_status: RATIFIED` required for a canonical audit | an unratified registry can produce gate verdicts |
| 6 | `corpus.languages` treated as the corpus, not an allowlist | a missing treebank yields a complete-looking half-audit |
| 7 | **inputs staged**: bytes read once, digest taken of what was read, parse consuming a private copy of those same bytes | edit → parse → restore publishes a report the manifest does not describe, and no before/after digest comparison can see it |
| 8 | **re-verification before publishing** — digests re-checked and the data root re-globbed for files that *appeared* | a run whose sources moved underneath it describes a state that no longer exists |
| 9 | **atomic `run_id` reservation** (exclusive `mkdir` of the log directory) | `_preflight` is check-then-act, so concurrent runs both pass it and both write |
| 10 | **rollback over the predetermined destinations on failure**, released reservation, with `_preflight` and the reservation *outside* the guarded block | a write failing partway leaves a truncated artifact that no "what succeeded" record would catch — and a rollback that also covers the preflight deletes the very artifacts the refusal protects |
| 11 | **git state sampled before the first write** (`manifest.git_state()` public, `build_manifest(git=…)`) | the stage writes into the worktree, so a sample taken at manifest-assembly time reports a dirtiness the run itself created |
| 12 | **unknown override fields rejected** (`registry.KNOWN_OVERRIDE_FIELDS`), `part_order` listed as declared-but-unread | the required five are caught by their absence, but a mistyped *optional* key (`flag:` for `flags:`) was dropped without a trace and appeared in no artifact |
| 13 | **`g1` marker + the same enforcement as G0** (`conftest.GATE_MARKERS`, `uv run pytest -m g1 --strict-markers`) | the G1 tests ran only inside the full suite, where a skipped one moves `239 passed / 17 skipped` to `238 / 18` and stays green — the failure mode D52(iii) forbids for G0 and left open for G1 |

**Convention 12 changes a G0-attested contract, so it is gated like one.** It
lives in `registry.build_registry`, whose mandatory-coverage area is
"registry construction and validation" in the D52(ii) inventory. Testing it only
in the unmarked G1 file would have left `pytest -m g0` green while the rule went
unexercised — the same "asserted but not enforced" gap this section exists to
close. Two `g0`-marked tests were therefore added to `tests/test_registry.py` and
**named in the inventory**, so deleting either turns the gate red rather than
merely lowering a count (mutation-verified).

**Consequence for the attestation, which is the owner's to complete.** Both lines
of `docs/HANDOFF.md`'s attestation block are stale: the G0 selection moves
**142 → 144**, and the full suite moves **142 passed / 17 skipped → 239 / 17**,
since this branch adds the G1 tests (236 before the 2026-08-17 audit added three
more, all outside the G0 selection — hence a moved suite total and an unmoved
gate count). That block is deliberately **not** updated
here: it records counts measured *on a clean tree together with their commit*, and
this tree is not clean. Re-attesting is a step of the commit sequence below, and
it has its own commit there — it cannot precede the commit it must name.

**Exception, declared:** conventions 9 and 10 do not apply under `--force`. Force
skips the preflight, so a destination may hold a previous run's artifact and the
proof that deletion is safe is absent — losing someone else's output is worse than
leaving a partial one. Under `--force` a failed run leaves its partial state in
place. **The exception stops there:** convention 8 in particular still holds under
`--force` — a run whose inputs moved underneath it publishes nothing, whatever
the operator asked to overwrite. (An earlier draft of this paragraph named
conventions 8 and 9; that was an off-by-one left by splitting the old convention 7
into staging and re-verification, and it described the code incorrectly.)

**Two properties of the naming that the reader should not assume:**

- **Truncation.** `run_id` and filenames carry the **first 12 hex characters** of
  the config hash and of the input fingerprint, not the full digests. The full
  values are in the manifest (`config_sha256`, and a SHA-256 per input). Twelve
  characters is ample against accident and is not a cryptographic commitment.
- **Path sensitivity.** The fingerprint digests `path\tsha256` lines, so it is a
  function of *where* the inputs are as well as *what* they contain: the same
  corpus audited from a different data root yields a different `run_id`. That is
  intended — provenance is about a particular reading of particular files — but it
  means the fingerprint is not a content-address and two identical corpora in two
  locations do not share an identity.

**And one property that is weaker than earlier drafts claimed.** Same-day
regeneration reproduces the **report, the CSVs and the sidecars** byte for byte —
but **never the manifest**, which carries `created_utc`, a wall-clock timestamp.
Across a day boundary less still is stable: `run_id` carries the date, so the
filenames change, the "Run id" line inside the report changes, and the sidecars
follow. What survives both is everything downstream of the identity — the counts,
the tables, the CSV bodies and the `{config_hash}_{fingerprint}` half of the name,
which is why §"Provenance" cites runs by that half.

§6.1 names artifacts `{stage}_{config-hash}_{date}`. That rule collides in two
distinct ways here, and the second is the dangerous one:

- two runs sharing a config and a date but differing in their **overrides file**;
- a **pre-audit and a canonical audit** over identical data, config and overrides.
  These differ in meaning, not in inputs: one withholds every verdict, the other
  decides them. Under §6.1 they would share a name, so `--force` would silently
  replace one with the other and the manifest could not say which it held.

**Proposed name:** `audit_report_{mode}_{config_hash}_{inputs_fp}_{date}.md`,
with `mode ∈ {preaudit, canonical}` and `inputs_fp` a SHA-256 over the sorted
`path\tsha256` lines of **every `.conllu` file and the overrides file**. The
resolved config is deliberately *not* in `inputs_fp`: it is not a file on disk
but a merge result, and it already enters the name as `config_hash` and the
manifest as `config_sha256`.

**Proposed additions to the D46 record**, so no consumer has to parse the mode
back out of a filename: the manifest gains `mode` (`preaudit` | `canonical`) and
`status` (`PROVISIONAL` | `CANONICAL`); `entry_point` becomes the actual
invocation (`hexis.pipeline.run_audit --pre-audit`), which propagates the mode
into every artifact's sidecar; and every companion CSV carries a `status` column,
so a table detached from both its filename and its sidecar still cannot be
mistaken for a canonical one.

**Proposed reserved key in the overrides schema:** keys beginning with `_` are
metadata, never document assignments. `_status` declares a file's ratification
state, and a canonical audit requires `_status: RATIFIED` **explicitly** — an
absent, empty or unrecognised value is refused. Ratification is opt-in: the
inverse rule (refuse only files that declare themselves PROPOSED) would make the
guarantee depend on a proposal's author remembering to mark it, and §3.3 requires
assignments to be human-verified, which is a claim someone has to make rather than
one to infer from silence. Ratifying the registry therefore has a mechanical step:
copy the rows into `config/registry_overrides.yaml` and set `_status: RATIFIED`
there.

**Proposed corpus-completeness check:** `corpus.languages` is the corpus, not an
allowlist. A run whose data root lacks a configured language is refused in both
modes, because a missing treebank yields an audit that is correct about what it
saw and wrong about what it claims to be — and `--pre-audit` exists for registry
gaps, not corpus gaps.

A deliberate single-language audit needs **two** changes, not one: narrowing
`corpus.languages` *and* pointing `--data-root` at that language's treebank. The
two checks are deliberately opposite in direction and neither is redundant —
`corpus.languages` minus the data root catches a *missing* treebank, and the data
root minus `corpus.languages` catches an *unexpected* one (a file whose language
is not configured is an error, not something to skip silently, since skipping is
how half-audits are produced). The stage's error message says so.

**Not proposed here:** binding the
audit to the exact five files and SHA-256s of `data/raw/PROVENANCE.md`. That is
the stronger check, it needs a machine-readable provenance format, and inventing
one silently is exactly what this amendment exists to prevent — recorded as an
open item below.

**Proposed provenance fix:** `manifest.git_state()` becomes public and
`build_manifest` accepts `git=`, so a stage can sample git **before** its first
write. Artifacts must exist before they can be hashed, so the manifest is
necessarily assembled after the stage has written into the worktree; sampling git
at that point attributes the run's own untracked outputs to the tree it started
from. The pre-audit runs now record the state that preceded them.

All of the above are implemented and in force in the two pre-audit runs; submitted
here for ratification.

---

### (xv) `alphabet.json` — §3.7 and §4.1 contradict each other, and G1 cannot close until they do not

`freeze_alphabet` is unimplemented, and not only because the registry is
unratified. §3.7 specifies the artifact as `{symbol: id}` plus **one** variant tag,
creation date and config hash — with **no language field**. §4.1 defines |A| as
the alphabet size for the **(language, variant)** pair. The two cannot both
describe one file, and no decision anywhere resolves them. Until one is chosen the
function cannot be written, so **this blocks the G1 freeze independently of every
scientific question in this amendment**.

**Four things must be decided together**, and deciding only the first leaves the
function unwritable.

**(1) Shape.** Two options, each stated as exactly one thing:

| | **(A) a single nested artifact** | **(B) one artifact per (language, variant)** *(recommended)* |
| --- | --- | --- |
| files | **exactly one**, `alphabet.json`, nested language → variant → symbols | **one per pair**, `alphabet_{language}_{variant}.json`, each exactly §3.7's current shape |
| §3.7 | shape changes: two nesting levels are added | shape unchanged; the **filename** carries the pair |
| \|A\| lookup | index by language, then by variant | the file *is* the pair |
| risk | a reader who forgets the nesting pools two alphabets — precisely the error `observed_alphabet` now refuses at runtime | more files in the manifest |

**Recommendation: (B).** §4.1 says the alphabet *is* per (language, variant); an
artifact per pair makes that structural rather than conventional, leaves §3.7's
declared shape literally intact, and makes the pooling mistake unrepresentable
rather than merely rejected.

**(2) Document scope of the inventory — which documents constitute |A|.** §3.4
says only "frozen alphabet = symbols observed at G1". Observed over **which
documents**? Nothing in the spec, the Decision Log or this amendment says, and the
audit stage answers it by default: `run_audit` passes every token of the language,
`EXCLUDED` included. That default is one act away from being frozen.

It is not cosmetic. |A| enters every predictive probability through
`P_s(a) = (n_s(a) + β)/(N_s + β·|A|)`, and §4.1 names β·|A| "the implicit MDL model
cost at work" — the term that decides how deep the tree is allowed to go. Measured
on the second pre-audit run (C0, `ud23` / `drop`):

| document scope | \|A_grc\| | β·\|A_grc\| | \|A_la\| | β·\|A_la\| |
| --- | --- | --- | --- | --- |
| every document of the language — **today's default** | 106 | 53.0 | 102 | 51.0 |
| every document except `EXCLUDED` — *recommended* | 106 | 53.0 | **101** | 50.5 |
| the primary contrast only | **86** (A) / 96 (B) | 43.0 / 48.0 | 98 | 49.0 |

Two facts the table makes concrete. In Latin exactly one symbol — `CCONJ:nmod` —
exists in the corpus **only** because of Jerome, a document assigned `EXCLUDED`,
which enters no estimand, no regime aggregate and no T\*: as things stand it
receives pseudo-mass in every Latin model the study fits. In Greek the
primary-contrast reading would cut β·|A| by 19% and, worse, would make |A| a
**function of the A/B decision** — the choice of contrast would silently retune the
instrument.

**Recommendation: every document of the language except `EXCLUDED`.** It is the
line §(xiii) already draws for GATE-A reading 3, and for the same reason: *a census
over everything, an effect only over the material the study analyses.* It also
survives two tests the narrower reading fails — |A| stays independent of the A/B
choice, and the exploratory arms (tragedy, and `PROSE_POST` under option A) keep
their symbols inside the frozen alphabet, where §4.3's fallback covers "unseen in
training" but nothing covers "outside the alphabet".

Cost of adopting it: one filter in the freeze stage, and one symbol fewer in Latin.
Cost of leaving it undecided: the number is frozen by default, which is the failure
mode this amendment exists to prevent.

**(3) Scope of the freeze — which alphabets, not just which shape.** §3.4 speaks
of "the frozen alphabet" in the singular, but §5.6 runs three alphabet variants
(`ud23`, `ud23_oth`, `upos_only`) across two languages. Either:

- **C0 only** (2 artifacts): the sensitivity variants derive their alphabets when
  their cells run, at G6. Smaller freeze, but the sensitivity alphabets are then
  *not* pre-registered, and a variant's ids could differ from what G1 would have
  produced had it looked.
- **all six** (3 variants × 2 languages) — **recommended**: every alphabet the
  plan will ever use is fixed before any model sees real data, which is what the
  freeze is for. The cost is computing five extra inventories from a token table
  the audit has already built.

**(4) Atomicity — and no re-freezing.** Whichever shape is chosen, **all the
artifacts of the freeze are published in one act or none are**, under a single
run_id, with the same preflight-and-rollback discipline the audit already uses.
Option (B)'s multiple files must **not** be read as licensing a language or a
variant to be re-frozen later on its own: after G1 nothing is re-frozen at all,
and a correction is a Decision-Log amendment with its own re-run, not a quiet
rewrite of one file.

**And version-controlled in the same act (added 2026-08-20).** `data/processed/`
is gitignored, under a note that defers the re-include exception for the derived
statistics D28 does publish — naming `alphabet.json` among them — to **G4/G5**. But
`alphabet.json` is frozen at **G1**: as things stand the freeze writes its
artifacts into an ignored directory and "frozen" has no versioned referent. The
`.gitignore` exception is part of the freeze, not of a later gate. Whether
`results/` is tracked is a different question (checklist 19) and this clause holds
under either answer.

**(5) `freeze_alphabet` contract**, to be ratified with the above:

```python
def freeze_alphabet(
    tokens, cfg, *, language: str, out_dir: Path, force: bool = False
) -> Path
```

- computes `observed_alphabet(tokens, cfg, language=language)` and writes it with
  the §3.7 payload: `{symbol: id}`, the variant tag, creation date, config hash;
- **refuses to overwrite** without `force`, like every other artifact (§6.4);
- **refuses a token table carrying more than the named language**, exactly as
  `observed_alphabet` does — the guarantee must not weaken at the moment of
  freezing;
- **records its own document scope** in the §3.7 payload — the canonical
  `doc_id`s the inventory was computed over, or their count plus a digest — so the
  artifact states the rule it was built under, and the semantic inventory check of
  §(xvi) can verify it against the ratified registry instead of trusting the
  caller;
- writes a sidecar per artifact and is recorded in the run manifest;
- is called once per (language, variant) in scope, from a single stage that
  publishes them atomically.

### (xvi) The semantic inventory check — a tracked pre-freeze requirement whose expectations this amendment invalidates

`docs/implementation/specs/2026-08-13-g0-api-contract.md` §5 records, under
"tracked, not decided here", a **semantic inventory check required before the G1
freeze**. It is the mechanized form of the cross-check §3.3 already demands
("cross-checked against §2.3"), and it exists because the merge-target rules
"bound the mechanism, not the inventory": they cannot tell a correctly-shaped
wrong assignment from a right one. As specified there, the audit must fail loud
unless

1. the set of `(language, author, work, regime)` in the built registry equals the
   set declared in Spec §2.3 — identity first, since a count check alone is
   satisfiable by a wrong assignment that preserves *n*;
2. the per-regime document counts match the declared analysis sets — Greek HEX 5 /
   PROSE_CLASS 6, Latin HEX 2 / PROSE 6;
3. the enumeration sizes recomputed from the built registry match the applicable
   D43 rows — 462 / 2048, 28 / 256, 56 / 256, and 20 / 64 (or 10 / 32).

It was left unimplemented for one stated reason: expectation (1) needed the **O2**
ruling, and "writing the expectation before that ruling would hard-code a guess
into the check meant to catch guesses."

**What this amendment does to it.** O2 is now resolved at document level (§vii),
so that blocker is gone — but expectations (2) and (3) are *precisely* the values
amended here. Greek PROSE_CLASS is 2, not 6; Latin PROSE is 7, not 6; Lysias has
no referent; and every enumeration constant is recomputed in §(iv), §(vi) and
§(vii). Written as it stands, the check is now unsatisfiable by any correct
registry. Its substance has nonetheless been performed — by hand, in §(i)–(iii)
and in `docs/g1_registry_proposal.md`, which is exactly the §2.3 cross-check,
document by document, with the discrepancies enumerated rather than absorbed.

**Proposed, and it is an implementation obligation rather than a Decision-Log
amendment** (the contract it lives in is an implementation-level ratification; no
parameter, statistic or gate order changes, so it adds no row to the ledger
below):

- the check's **reference set moves from §2.3 to the ratified registry** — after
  ratification the registry *is* the corpus description, and §2.3 becomes the
  document that is amended to match it, not the one checked against;
- expectation (2) becomes the ratified per-regime counts under the chosen option
  (A: Greek HEX 5 / PROSE_CLASS 2, Latin HEX 2 / PROSE 7; B: Greek HEX 5 /
  PROSE_ALL 6);
- expectation (3) becomes the enumerations recomputed here, so the check remains
  what it was meant to be — the derived last line that catches a registry edit
  silently changing an attainable p floor;
- a **fourth expectation** is added: the frozen alphabet's declared document
  scope equals the analysed documents of the ratified registry (§xv(2)). The check
  exists to catch a registry edit that silently moves a derived quantity, and |A|
  is one of them;
- it runs **in the canonical audit, before anything is frozen**, and fails loud;
- it is written **with its tests**, like every other rule in this stage.

Recorded because the alternative is the failure mode this amendment exists to
prevent: a ratified requirement dropped in silence because the values it names
went stale.

## Governance — this document is not yet in the form the Decision Log requires

`02_DECISION_LOG.md` states the protocol in its header, and it is binding:

> Amendment protocol: changing a FROZEN entry requires a new `D{n}-A1` entry
> recording old value, new value, reason, date, and impact on already-computed
> results (re-run or retired). **No silent changes.**

A single omnibus entry is **not** that form. The decisions touched:

- **unconditionally (11):** D04, D06, D20, D21, D24, **D29**, D33, D43, D44, D46,
  D51 — D29 added 2026-08-20, see its ledger row and checklist 21;
- **only under option A (1):** D37 (the fit budget);
- **only under option B (1):** D25 (the claim template).

So **twelve** amendments under either option, **thirteen** entries in total across
both. `author_block` is a **second clause of `D43-A1`**, not a further decision —
it does not raise the count. Two genuinely **new** decisions sit alongside them:
`D55` (the corpus finding and the §xiv conventions) and `D56` (the `alphabet.json`
schema, §xv).

The ledger below therefore has **seventeen rows for fifteen items**: the thirteen
amendments, plus `D55` and `D56`. The two extra rows are `D43-A1`'s second clause,
already excluded from the count above, and **`DN-2`**, which is a *deferred node*
of §IV and not a frozen decision — it is tabled because option A voids its premise
and option B widens it, so ratifying either leaves it in a different state than it
is in now, but amending it is not among the twelve.

The conforming shape is one `Dnn-A1` per touched decision plus those two new
entries. Presented as a ledger below so ratification is mechanical; **which route
to take is the owner's call**, and there are two:

- **(a) File the ledger as separate entries** — `D04-A1` … `D51-A1`, plus `D55`
  and `D56`. **The option A/B decision is not new matter**: it changes the
  contrast D04 froze, so it belongs to `D04-A1`, and `D55` is left with the corpus
  finding and the software conventions only. Conforms to the protocol as written.
- **(b) Keep one omnibus `D55`** and record an explicit derogation from the
  amendment protocol inside it, since the amendments share one cause and splitting
  them risks their being ratified apart.

I recommend (a): the protocol says "no silent changes", and an omnibus makes each
individual change harder to see. But the entries are interdependent — ratifying
`D21-A1` without `D51-A1` would leave the plan incoherent — so (a) must be
ratified as a single act even if filed as separate entries.

### Amendment ledger — draft `Dnn-A1` entries

Impact is identical for every row and is stated once: **no already-computed result
is affected.** No model has been fitted to real data (D30 holds; first fits are at
G4), so nothing is re-run and nothing is retired. Date for all: the date of
ratification.

| entry | old value | new value | reason |
| --- | --- | --- | --- |
| **`D04-A1`** | regime taxonomy with "Greek primary contrast HEX vs PROSE_CLASS", rationale "**R: verified corpus composition (12 tragedies; post-classical prose; …)**" | the ratified option A or B; rationale replaced by the enumerated composition | **the central amendment.** D04 freezes the Greek contrast, and the rationale it is frozen on is precisely the composition E1 got wrong — 6 tragedies, not 12. The A/B decision *is* an amendment to D04 |
| `D20-A1` | transfer protocol including "Lysias-merged robustness rerun" | same protocol, **Lysias clause removed** | Lysias is absent from r2.18; the clause has no referent (§iv) |
| `D21-A1` | randomization schemes at 11 documents | schemes at the ratified 𝔻 (7 under option A, 11 under option B) | the corpus inventory (§i, §iii) |
| `D24-A1` | Latin P1 2⁸ = 256, P2 C(8,2) = 28, "cannot enter the Holm family" | 2⁹ = 512, C(9,2) = 36, and qualitative **by design decision** | Caesar is present (§ii, §vi); the exclusion rationale was a Holm misreading (§v) |
| **`D25-A1`** (option B only) | claim template "…differs from **classical prose**…" | "…differs from **prose**…", with period declared a confound *inside* the primary contrast | under option B the prose side spans Herodotus to Athenaeus, so the frozen claim template would state something the design no longer measures (§iii). **Not needed under option A** |
| **`D06-A1`** | "GATE-A: any excluded label > 2% of raw tokens in any regime at audit" — denominator, category scope, regime scope, the standing of exploratory regimes and the language scope all left to reading | the **five** readings of §(xiii) made explicit: denominator = all raw syntactic words **of the regime**; category scope = **per excluded-deprel label**, over the census of retained-UPOS tokens outside the 23 **independently of the drop/`oth` policy**; regime scope = the **analysed** regimes, `EXCLUDED` censused but unable to fire the verdict (GATE-B, being a flag and not an escalation, stays unnarrowed); exploratory regimes (`OTHER_VERSE`, `PROSE_POST`) **keep** their firing power even where the primary contrast excludes them; shares are computed per `(language, regime)` and the **verdict is one per run**, so a trigger in either language escalates the whole design | the audit cannot evaluate GATE-A without fixing all five, and three are changes of substance: counting drops would make the gate structurally unable to fire in the `(ud23_oth, ·)` cells D50 makes mandatory to interpret; letting `EXCLUDED` fire would let a document that enters no estimand impose D50's caveat on every primary conclusion; and readings 4–5 decide whether that caveat can be imposed by a regime outside the primary contrast (the likeliest trigger today: `OTHER_VERSE` at 1.28%) or by the other language |
| **`D29-A1`** *(added 2026-08-20)* | supervision touchpoints "re-anchored to v2 gates: **after G1** (linguistic supervisor: registry + alphabet)" | the linguistic touchpoint precedes the **freeze**; the mathematical (after G3) and pre-submission touchpoints are unchanged | its object *is* what G1 freezes. A registry and an alphabet reviewed after they are frozen cannot be changed by the review: every correction would then cost an amendment with a re-run, and the seven catalogue-only rows would receive their second pair of eyes only after the act that makes them binding. D29 is FROZEN, so the reordering is an amendment and not a reading — and it was missing from this ledger until 2026-08-20 |
| `D33-A1` | multiplicity wording resting on "floor > 0.025 ⇒ unattainable" | Holm restated: exceeding α/2 puts a test out of reach *first*, not out of reach | §(v) |
| `D37-A1` *(option A only)* | "Total 13 cells. **Budget: ≈ 330 fits/cell** ≈ 10–20 laptop-minutes ⇒ ≈ 3–5 h total" — 330 = 11 docs × 3 fits × 10 seeds | 13 cells **unchanged**; budget recomputed to **≈ 210 fits/cell** (7 × 3 × 10) and the total scaled accordingly | D37 does not enumerate documents, so the cell count is untouched; what it freezes and what the corpus changes is the **fit budget**. Under option B, 11 × 3 × 10 = 330 stands and **no amendment is needed** |
| `D43-A1` | tiers, floors and sidedness at 11 documents / 6 author blocks | recomputed floors with sidedness per §(iv), §(vii); D43(iv) Lysias clause removed | the corpus inventory |
| `D44-A1` | O7 calibration on 11 pseudo-documents | 7 (option A) or 11 (option B) with the ratified size profile; P2 calibrated only at levels it can attain | §(xii) |
| `D46-A1` | manifest fields as frozen | adds `mode`, `status`, pre-captured `git`, snapshot `inputs`; `entry_point` is the invocation | §(xiv) |
| `D51-A1` | T\* scope with expected binding condition "HEX minus Iliad" | T\* per §(ix); binding condition recorded as observed; learning-curve grid per §(x) | the binding condition moved to the prose side under option A |
| **`D55`** (new) | — | the corpus finding, and §(xiv)'s conventions | not an amendment: a new question the corpus posed. The A/B decision itself belongs to `D04-A1`, since that is the entry that freezes the contrast |
| `D43-A1` *(second clause, if `author_block` is adopted)* | author blocks named in prose by D43(v); the registry schema has only `author` | schema gains **`author_block`**, defaulting to `author` | `author` is bibliographic attribution; the author block is **D43(v)'s randomization unit**. One field for both would decide O8 by transcription (registry proposal, question 5). Belongs to D43, **not** D03: D03 governs the release pin, the splits and document derivation, and says nothing about author blocks. Schema impact on §2.3 / §3.3 |
| **`D56`** (new) | §3.7: `alphabet.json` = `{symbol: id}` + one variant tag, **no language field**, and no statement anywhere of which **documents** the observed inventory covers | one of the two shapes in §(xv), plus the **document scope** of the inventory (§xv(2)), the freeze scope, atomicity including the `.gitignore` exception, and the `freeze_alphabet` contract | §3.7 and §4.1 contradict each other today, and `freeze_alphabet` cannot be written until that is resolved — so **G1 cannot close without this**. A **new decision**, not an amendment to D46: D46 governs run manifests and sidecars, not artifact schemas |
| `DN-2` (deferred node) | "whether Tier 2 spends α on P1 alone (one-sided floor 0.0156 < 0.025)" | **premise void under option A** (floor 0.031 > 0.025); under option B the question widens from "P1 alone" to the whole Tier-2 family, which is attainable | §(iii), §(vii) |

## Documents this amendment touches, if ratified

None of these has been edited. The list is exhaustive as far as a search for the
superseded constants reaches (`462`, `2048`, `C(11,5)`, `C(8,2)`, `2^11`), plus
the files below it that carry no constant but encode the same assumptions:

| file | what is stale |
| --- | --- |
| `docs/01_MASTER_SPEC.md` | §2.3 works tables **and the registry schema** (`author_block`, if adopted); §2.6 errata E1, E2; §3.3 (document identity, `part_order`, `sent_ord`); §3.4 (GATE-A readings); §4.2 (𝔻 = 11, T\*, learning-curve grid and its protocol-(c) extension); §5.1 (462 / 2048 / 20 / 64 / 56 / 256); §5.2 (per-regime pool fractions quoted at 11 documents); §5.3 (see below); §5.4 (Holm wording); §5.6 (13 cells over 11 documents); §5.7 (Latin 28 / 256 and its rationale); §5.8 (confound register, if option B); §6.1 (artifact naming); §6.4 (manifest fields); §8 (F3–F4 "11 points", T1–T3 shapes) |
| `docs/02_DECISION_LOG.md` | **D04** (the contrast and the composition it is frozen on), D20, D21, D24, **D25** (option B only), D33, D37, D43 (floors, and `author_block` if adopted), D44, D46, D51; the new `alphabet.json` decision (§xv); open items O1, O2, O4, O8; deferred node DN-2 |
| `docs/03_ROADMAP_OPERATIVA_IT.md` | the G1 and G3 phase descriptions (11 pseudo-documents at O7); the placement of the linguistic touchpoint inside the G1 phase, if `D29-A1` is ratified |
| `docs/04_AI_HANDOFF_PROMPT.md` | the enumeration constants quoted to a fresh agent |
| `CLAUDE.md` | the "exact schemes" line (Greek 462 / 2048; Latin 28 / 256; author 20 / 64; Lysias-merged 56 / 256) — **and the pointer note added under it on 2026-08-17**, which says this amendment is PROPOSED and applied to nothing. Ratifying makes that note false, so it is replaced by the ratified constants in the same act; it exists only because these two files are loaded as standing instructions in every session, so a superseded constant left unflagged is re-derived indefinitely (owner-authorized, no value changed) |
| `AGENTS.md` | the same line and the same note, mirrored — the two files are byte-identical below their first line, and any edit to one is an edit to both |
| `README.md` | the design summary's document counts and constants |
| `docs/implementation/specs/2026-08-13-g0-api-contract.md` | constants quoted in the ratified API contract — and, more than constants, **§5's semantic inventory check**: its reference set (§2.3) and its expectations (Greek HEX 5 / PROSE_CLASS 6, Latin HEX 2 / PROSE 6; 462 / 2048, 28 / 256, 56 / 256, 20 / 64) are exactly what this amendment replaces, so the check is unsatisfiable as written and must be re-pointed at the ratified registry before the freeze (§xvi) |
| `src/hexis/stats/permutation.py:4` | module docstring: "Greek 2^11 = 2048 … Latin 2^8 = 256" |
| `docs/01_MASTER_SPEC.md` §5.3 | "5–6 documents per group make these CIs crude" and "per-document dot displays (11 points, F3–F4)" — under option A one group holds **2** documents, where a between-document bootstrap is not crude but near-degenerate (resampling 2 with replacement has 3 distinct outcomes), and the dot plots carry 7 points |
| `config/default.yaml` | `corpus.primary_contrast` (flat pair, `PROSE_ALL` not a label), `scores.t_star` (scalar, must be per language), `scores.learning_curve_T` (needs §(x)'s two-part reading) |
| `config/registry_overrides.yaml` | empty; receives the ratified rows **and** `_status: RATIFIED` |
| `.gitignore` | `data/processed/` is ignored under a note deferring the re-include exception for `alphabet.json` to G4/G5 — but the artifact is created at G1, so the exception belongs to the freeze (§xv(4)) |
| `src/hexis/pipeline/run_null_calibration.py`, `tests/test_null_calibration.py` | scaffolds sized for 11 pseudo-documents; O7 must be rebuilt per §(xii) — at G3, after ratification |
| `02_DECISION_LOG.md` §IV, `DN-2` | premise void under option A; widened under option B (ledger above) |

`candidates/hexis-ctree/` also carries the old constants and is deliberately left
alone: it is quarantined and never imported (D47). `docs/audit/` is a historical
record of the v2.1 realignment and is not corrected retrospectively.

## Decision checklist — everything G1 needs from you, in one place

Gathered here because it is otherwise scattered across two documents and seventeen
sections. Nothing below can be settled by the agent. **They do not all block the
same thing**, and an earlier draft of this checklist wrongly said they did.

### A. Blocks the G1 freeze — the freeze cannot proceed without these

1. **Option A, option B, or route A\*** for the Greek primary contrast — §(iii),
   with all three counterweights in view: the refit-remedy dependency of
   §(iv-bis), the Holm structure of §(v) (under A, P2 can never be the family's
   *first* rejection, so the confirmatory layer rests on P1 alone), and the
   2-document bootstrap of §5.3. Route A\* is option A plus a pre-registered
   conditional switch keyed on the O7 outcome, with both T\* values frozen
   (§iii, added 2026-08-20). This *is* `D04-A1`.
2. **The registry: all 30 rows.** Ratification covers every `PROPOSED /
   UNVERIFIED` row, not only the seven catalogue-only ones — regime, `meter`,
   `period`, `flags` and `source_urn` for each of the 30. The seven are simply the
   rows whose *identity* rests on the thinnest evidence.
3. **Caesar's regime** — PROSE_CLASS as proposed, or excluded with a stated reason
   that is not size (§vi).
4. **Athenaeus 12+13** — merge or not; decides 29 vs 30 documents and, under
   option B, whether 𝔻 = 11 or 12 (registry proposal Q1). **With it, the
   `part_order` constraint** (mandatory, integer, present and unique within every
   merged group), which is what makes a merged document well-formed and is the
   half of §(viii) that belongs to the registry schema; the ordering rule itself
   stays at 13 (added 2026-08-20).
5. **Book-level documents** — Herodotus `.1`, Thucydides `.1`, Diodorus `.11` each
   standing as one document (registry proposal Q3).
6. **`period` vocabulary and values** — §2.3 fixes neither (registry proposal,
   "Fields that carry a decision").
7. **O8 and `author_block`** — the author-level floors are part of what G1 freezes
   and are not derivable from the bibliographic `author` field (§vii).
8. **GATE-A readings — five, not three.** Denominator; per-label scope; **which
   regimes carry the verdict** (`EXCLUDED` censused but non-firing); whether
   **exploratory regimes keep their firing power** where the primary contrast
   excludes them — the likeliest trigger today is `OTHER_VERSE` at 1.28%, so this
   is the reading that can actually bind; and the **language scope** (shares per
   language, one verdict per run, so a Latin excess escalates the Greek design).
   The gate cannot be evaluated without all five (§xiii, `D06-A1`).
9. **`alphabet.json`: shape, document scope, freeze scope, atomicity, and the
   `freeze_alphabet` contract** (§xv, `D56`). Blocks the freeze on its own,
   independently of every scientific question here. **Document scope added
   2026-08-20**: nothing says which documents the observed inventory covers, and
   the default about to be frozen puts a symbol contributed only by an `EXCLUDED`
   document (`CCONJ:nmod`, Jerome) into the alphabet of every Latin model, while
   the narrower reading would make |A| a function of the A/B decision (§xv(2)).
   Atomicity now includes the `.gitignore` exception without which the frozen
   artifacts are written to an ignored directory.
10. **T\*** — the `t_star` signature (§xi) and the two config keys that must hold
    its result per language (§xi).
11. **The semantic inventory check** (§xvi) — confirm that its reference set moves
    from §2.3 to the **ratified registry**, and that expectations (2) and (3)
    become the ratified per-regime counts and the enumerations recomputed here.
    The check itself is then implemented, with its tests, and must pass before
    anything is frozen; what cannot be settled without you is what it should be
    checking against, since the values the contract names are the ones this
    amendment replaces. Includes the fourth expectation added 2026-08-20: that the
    frozen alphabet's declared document scope matches the ratified registry.

21. **The linguistic supervisor's touchpoint — before or after the freeze**
    (`D29-A1`, new 2026-08-20). D29 anchors it "after G1"; its object is the
    registry and the alphabet, which is exactly what G1 freezes. This item decides
    the **order of the rest**: items 1–7 are the touchpoint's subject matter, so
    ratifying them today pre-empts the review this item would institute. Strictly
    speaking it blocks the freeze only if the answer is "before" — which is why it
    is the one to answer first.

### B. Blocks later gates, not G1

12. **Latin family membership** — own family of 2 or joined into 4 (§vi). Bears on
    G5's inference, not on what G1 freezes.
13. **The `sent_ord` ordering rule** — §(viii). The audit and the freeze read no
    sentence order; `run_encode` and the P-BOUND arm do, and must not run until
    the rule exists **with its tests**. The `part_order` *constraint* that used to
    sit here moved to **item 4** on 2026-08-20: it is a registry-schema rule, it
    rides with the merge decision, and leaving it here would ratify a merge whose
    well-formedness nothing validates.
14. **Learning-curve grid** — §(x). A G6 display; needed before F8 is drawn.
15. **O4** — Petronius verse insets. Sentence-level exclusion would change the
    encoded corpus, so it is needed before `run_encode`, not before the freeze.
16. **O7's own resolution** — a G3 study; §(iv-bis) records what each outcome
    implies, and D44 already blocks G2/G5 on it.

22. **Whether the Latin arm survives its own T\*** (new 2026-08-20). §(ix)
    records T\*_la = **638** retained tokens — two orders of magnitude below the
    size §4.1 profiles against — and that all three arms trip §4.2's pre-registered
    `T* < 15k` contingency (Greek 9,346 under A, 11,043 under B). The contingency
    itself is automatic and is filed as `D51-A1`; what no document decides is
    whether L1 at 638 tokens remains a design arm or becomes an appendix. Bears on
    G6, not on the freeze: T\* is frozen either way.

### C. Repository and process governance — not scientific gates at all

17. **The thirteen software conventions** of §(xiv), including the `--force` exception
    and convention 13 (the `g1` gate, authorized 2026-08-17 and pending ratification
    with the rest).
18. **Route (a) or (b)** for filing the amendments (§Governance).
19. **Whether `results/` is tracked or gitignored**, and the commit order
    (§Committing this package). A Git question — with one half that is not
    optional under either answer (added 2026-08-20): `data/processed/` is
    gitignored, and its re-include exception for the frozen artifacts is noted for
    G4/G5 while the artifacts it names are created at **G1**. That exception lands
    with the freeze (§xv(4)).
20. **The `g1` gate — decided and implemented (convention 13), ratification
    pending with the rest.** The marker plus the enforcement it inherits from G0
    is in force; what is *not* done, deliberately, is a D52(ii)-style inventory of
    mandatory G1 areas by test name. That step presupposes a normative definition
    of the G1 set, and no decision provides one — D52 governs G0 only. If you want
    it, it is a Decision-Log matter, not a convention. **Sequencing, added
    2026-08-20:** if you want it, it has to exist *before* the canonical audit run,
    not after — after the freeze the gate has guarded nothing. That is the exact
    failure that reopened G0, where `-m g0` exited 0 with three mandatory areas at
    zero coverage.

23. **Binding the audit's inputs to `PROVENANCE.md`** (new 2026-08-20; promoted
    from the open items). Conventions 7–8 guarantee that a run describes the bytes
    it read; nothing asserts that those bytes are the five `.conllu` files pinned
    at r2.18. The record is not missing — the manifest carries every input digest
    and `PROVENANCE.md` carries the declared ones — only the comparison is manual.
    The freeze is not blocked by this; the question is whether the canonical run
    should refuse to proceed when the two disagree. Recommended: yes, and before
    the canonical run, since that is the run whose inputs get frozen.

## Open items this amendment does not close

- **O1 / E5** — the count of UD treebanks per language at v2.18.
- **O4** — Petronius verse insets: `phi0972.phi001` is flagged `verse_insets`;
  sentence-level identification has not been attempted.
- **O8** — the Hymn's author block (§vii), and the `author_block` field the
  registry needs to express the answer. Under option A it changes the floors but
  not attainability (nothing is attainable at author level either way). Under
  option B it changes the floors and, **if P1 moves to a relabelling test**, it
  also decides whether D43(iii) reopens at all: Hymn-anon still starts the family
  at 1/56, Hymn → Homer does not at 1/21.
- **The option A / option B decision itself** (§iii), which is the owner's and the
  linguistic supervisor's.
- **Latin family membership** (§vi) — own family of 2, or joined to the Greek
  family of 4.
- **Binding the audit to `PROVENANCE.md`** (§xiv) — needs a machine-readable
  provenance format before the exact five files and SHA-256s can be enforced.
  Promoted to a decision on 2026-08-20: **checklist 23**.
- **`sent_ord` and `part_order`** (§viii) — the rule is proposed, not implemented,
  and neither is the `part_order` constraint that goes with it (mandatory,
  integer, unique within a merged group). Nothing in the audit or the freeze reads
  sentence order, so it does not block them; `run_encode` and the P-BOUND arm do,
  and must not run until it exists with its tests. Split on 2026-08-20: the
  **constraint** is checklist 4 (it rides with the merge), the **rule** is
  checklist 13.
- **The semantic inventory check** (§xvi) — tracked in the ratified G0 API
  contract §5, still unimplemented, and now unsatisfiable as written because its
  expectations are the values this amendment replaces. Its substance was performed
  by hand in §(i)–(iii); the mechanized form is re-pointed at the ratified registry
  and must pass before the freeze. Not a Decision-Log amendment, so it carries no
  ledger row — which is precisely why it needed naming here.
- **A normative definition of the G1 test set** — the `g1` gate exists
  (convention 13), but no decision says which behaviours it must cover, so it
  enforces discipline over whatever is marked rather than over a mandated set.
  The D52(ii) analogue for G1 is a Decision-Log matter if it is wanted at all.

## Committing this package — the order matters

Both manifests here record `git.dirty: false` — the outcome of the order below,
not its premise. Before that order was executed the flag read `true`, honestly
rather than self-inflictedly (it is sampled before the run's own writes — §xiv,
convention 11), because the generator, its tests and these documents were
uncommitted. A naive "commit, then regenerate" does **not** clear it: `results/`
is tracked, so the regenerated artifacts make the tree dirty again the moment
they are written.

Two orders that do work:

1. **Three commits: code, attestation, artifacts.** The attestation cannot come
   first, because `docs/HANDOFF.md` requires it to be measured "on a clean tree"
   and recorded "together with its commit" — and before the code is committed the
   tree is not clean and that commit does not yet exist. The repository's own
   precedent is the right order: `180e05c` (code) then `56ad331`
   (*docs: re-attest G0 after inventory hardening*), which names it.

   Remove `results/` entirely → **commit generator, tests and documents** (call it
   `X`; the tree is now clean) → on `X` run `-m g0`, **`-m g1`** (convention 13),
   the full suite and
   `uv lock --check` → **commit the re-attestation naming `X`**, replacing the
   block in `docs/HANDOFF.md` (the G0 selection is **144**, not the 142 recorded
   there, and the full suite is **239 passed, 17 skipped**, not 142/17) →
   regenerate on the still-clean tree (the manifest samples `dirty: false`
   **before** writing) → commit `results/`. The manifests then name the
   attestation commit, which is the first commit at which the code and its
   recorded evidence agree.

   **One commit per run — found by executing this sequence on 2026-08-17, and it
   is not a detail.** With `results/` tracked, only the *first* regenerated run
   sees a clean tree: the second samples git after the first has written into the
   worktree and records `git.dirty: true`. That flag would then report a
   dirtiness caused by a **sibling artifact of the same package**, which is the
   same distortion convention 11 exists to remove — one step removed. So each run
   is generated and committed before the next is generated, and the two manifests
   name different commits by construction (here `1680d3a` and `84a9319`). The
   alternative that removes the problem structurally is gitignoring `results/`,
   which is the open question below — **ignored**, not merely untracked:
   `manifest.git_state()` reads `git status --porcelain`, which lists untracked
   files as `??` and would therefore still report dirty. Ignored files do not
   appear there, so every run of a batch would sample `dirty: false` from the
   same commit.
2. **Regenerate in a clean worktree.** Same first two commits; then check the
   attestation commit out in a fresh worktree with no `results/`, regenerate
   there, copy the artifacts back and commit them.

Either way the artifacts must be **removed, not merely overwritten**, before the
first commit: leaving the current ones in place carries a manifest that names a
commit predating the code that made it. Whether `results/` should be tracked at
all, or gitignored like `data/interim` and `data/processed`, is itself a question
for ratification — D28 permits publishing derived statistics, so tracking them is
allowed, not required.
