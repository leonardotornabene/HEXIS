# G1 registry proposal — PROPOSED / UNVERIFIED

**This is not the registry.** `config/registry_overrides.yaml` declares
human-verified assignments (§3.3, D04) and **remains empty** until the owner
ratifies the rows below.

The **YAML is the assignment** — the complete record, and the only thing the
stage reads. This document carries the **evidence** for it, and shows a subset of
the fields: identity, regime, counts and how each identification was made. The
registry fields not in the tables below — `meter`, `period`, `flags`,
`canonical_doc_id`, `part_order` — live in the YAML, and every row where one of
them carries a decision is listed under "Fields that carry a decision" and in
"Open questions". Read the YAML for the full record; read this for why:

```
uv run python -m hexis.pipeline.run_audit --pre-audit \
    --overrides docs/g1_registry_proposal.yaml
```

That YAML is executable **only** under `--pre-audit`. The canonical default mode
fails loudly on any unassigned sentence and is the mode that will run once the
registry is ratified.

`build_registry` requires every field and a valid regime label, so the YAML is
complete rather than partially blank. Completeness is a mechanical requirement of
the loader, **not** a claim of verification: every row below is `PROPOSED /
UNVERIFIED` until you sign it off, and §"Open questions" lists what is genuinely
undecided.

**The "pre-audit only" restriction is enforced, not merely stated.** The YAML
carries a reserved top-level key `_status: PROPOSED`, and the stage refuses to
produce a canonical report from any overrides file whose `_status` is not
`RATIFIED`. Ratifying the rows therefore has a mechanical step: copy them into
`config/registry_overrides.yaml` and set `_status: RATIFIED` there. Keys starting
with `_` are reserved metadata and are never read as document assignments.

**Licence (D28).** Documents are identified by TLG/PHI id, CTS URN, `sent_id`
prefix, counts and catalogue link — and by nothing else. **No word, name or line
of the treebanks appears here**; where a check against the source text was made it
stays uncommitted, and the table records only that it was made and what it
concluded. The URN is the identifier of record; the link is a convenience.

**Not every row was checked the same way, and the 30 reconcile exactly:**

| how identified | count | rows |
| --- | --- | --- |
| local check against the source text | **23** | Iliad; Herodotus; Thucydides; Plutarch ×2; Sophocles ×5; Aeschylus; all 12 Latin |
| catalogue evidence alone (TLG/PHI number + §2.3) | **7** | Hesiod ×3; Diodorus bk 11; Hymn to Demeter; Athenaeus bk 12, bk 13 |
| | **30** | |

The seven catalogue-only rows are the ones most worth a second pair of eyes. Two
of them matter beyond their own identity: the **Hymn** carries O2/O8, and the
**Athenaeus** pair carries the merge that turns 30 prefixes into 29 documents.

Counts are from the label-free pre-audit run, cited by the stable half of its
identity — `preaudit_53f76d297774_75e8a4ae9993` — because the trailing date
component of a `run_id` is the regeneration date and moves whenever the artifacts
are rebuilt, while the fingerprint does not. It enumerates raw prefixes (18 grc +
12 la, totals reconciling with §2.2); the merge in question 1 below is what turns
30 of them into 29 documents.

**URN level.** The tables and the YAML both give the **edition-level** URN — the
`…perseus-grc1` / `…perseus-lat1` suffix — because that is the object the
treebank was converted from. The catalogue links resolve at author level, which
is the level Perseus exposes for browsing.

---

## Greek — `grc_perseus`, 18 raw prefixes → 17 canonical documents if Athenaeus merges

| `sent_id` prefix | edition URN (`urn:cts:greekLit:…`) | proposed author / work | regime | sent. | raw | retained | evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `tlg0012.tlg001.perseus-grc1.tb.xml` | `tlg0012.tlg001.perseus-grc1` | Homer, *Iliad* | HEX | 6003 | 79890 | 69327 | [tlg0012](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0012/) + local text check |
| `tlg0020.tlg001.perseus-grc1.tb.xml` | `tlg0020.tlg001.perseus-grc1` | Hesiod, *Theogony* | HEX | 273 | 4610 | 4023 | [tlg0020](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0020/) + §2.3; catalogue numbering only |
| `tlg0020.tlg002.perseus-grc1.tb.xml` | `tlg0020.tlg002.perseus-grc1` | Hesiod, *Works and Days* | HEX | 283 | 3725 | 3189 | [tlg0020](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0020/) + §2.3; catalogue numbering only |
| `tlg0020.tlg003.perseus-grc1.tb.xml` | `tlg0020.tlg003.perseus-grc1` | Hesiod, *Shield of Heracles* | HEX | 182 | 2403 | 2070 | [tlg0020](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0020/) + §2.3; catalogue numbering only |
| `tlg0013.tlg002.perseus-grc1.tb.xml` | `tlg0013.tlg002.perseus-grc1` | Anonymous, *Homeric Hymn to Demeter* | HEX | 166 | 2061 | 1761 | [tlg0013](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0013/) + §2.3; **catalogue only**; sole Hymn prefix (resolves O2) |
| `tlg0016.tlg001.perseus-grc1.1.tb.xml` | `tlg0016.tlg001.perseus-grc1` | Herodotus, *Histories* bk 1 | PROSE_CLASS | 1092 | 19575 | 17301 | [tlg0016](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0016/) + local text check |
| `tlg0003.tlg001.perseus-grc1.1.tb.xml` | `tlg0003.tlg001.perseus-grc1` | Thucydides, *Histories* bk 1 | PROSE_CLASS | 532 | 10396 | 9346 | [tlg0003](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0003/) + local text check |
| `tlg0008.tlg001.perseus-grc1.12.tb.xml` | `tlg0008.tlg001.perseus-grc1` | Athenaeus, *Deipnosophistae* bk 12 | PROSE_POST | 649 | 11283 | 10129 | [tlg0008](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0008/) + §2.3; **catalogue only**; merge candidate, `part_order: 12` |
| `tlg0008.tlg001.perseus-grc1.13.tb.xml` | `tlg0008.tlg001.perseus-grc1` | Athenaeus, *Deipnosophistae* bk 13 | PROSE_POST | 981 | 14962 | 13004 | [tlg0008](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0008/) + §2.3; **catalogue only**; merge candidate, `part_order: 13` |
| `tlg0060.tlg001.perseus-grc3.11.tb.xml` | `tlg0060.tlg001.perseus-grc3` | Diodorus Siculus, *Bibliotheca historica* bk 11 | PROSE_POST | 733 | 16882 | 15266 | [tlg0060](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0060/) + §2.3; catalogue id only |
| `tlg0007.tlg004.perseus-grc1.tb.xml` | `tlg0007.tlg004.perseus-grc1` | Plutarch, *Lycurgus* | PROSE_POST | 248 | 5044 | 4481 | [tlg0007](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0007/) + local text check |
| `tlg0007.tlg015.perseus-grc1.tb.xml` | `tlg0007.tlg015.perseus-grc1` | Plutarch, *Alcibiades* | PROSE_POST | 251 | 4943 | 4403 | [tlg0007](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0007/) + local text check |
| `tlg0011.tlg001.perseus-grc2.tb.xml` | `tlg0011.tlg001.perseus-grc2` | Sophocles, *Trachiniae* | OTHER_VERSE | 431 | 5229 | 4224 | [tlg0011](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0011/) + local check of named characters |
| `tlg0011.tlg002.perseus-grc2.tb.xml` | `tlg0011.tlg002.perseus-grc2` | Sophocles, *Antigone* | OTHER_VERSE | 391 | 4299 | 3573 | [tlg0011](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0011/) + local check of named characters |
| `tlg0011.tlg003.perseus-grc1.tb.xml` | `tlg0011.tlg003.perseus-grc1` | Sophocles, *Ajax* | OTHER_VERSE | 490 | 5319 | 4364 | [tlg0011](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0011/) + local check of named characters |
| `tlg0011.tlg004.perseus-grc1.tb.xml` | `tlg0011.tlg004.perseus-grc1` | Sophocles, *Oedipus Tyrannus* | OTHER_VERSE | 520 | 5600 | 4571 | [tlg0011](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0011/) + local check of named characters |
| `tlg0011.tlg005.perseus-grc2.tb.xml` | `tlg0011.tlg005.perseus-grc2` | Sophocles, *Electra* | OTHER_VERSE | 528 | 5239 | 4259 | [tlg0011](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0011/) + local check of named characters |
| `tlg0085.tlg001.perseus-grc2.tb.xml` | `tlg0085.tlg001.perseus-grc2` | Aeschylus, *Suppliant Women* | OTHER_VERSE | 166 | 1529 | 1284 | [tlg0085](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AgreekLit%3Atlg0085/) + local check of named characters; **only Aeschylus play present** |

Absent from the release though listed in §2.3: **Lysias ×4, Polybius,
Apollodorus, Aesop, and 6 of the 7 Aeschylus plays.**

## Latin — `la_perseus`, 12 raw prefixes → 12 canonical documents

| `sent_id` prefix | edition URN (`urn:cts:latinLit:…`) | proposed author / work | regime | sent. | raw | retained | evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `phi0690.phi003.perseus-lat1.tb.xml` | `phi0690.phi003.perseus-lat1` | Vergil, *Aeneid* | HEX | 68 | 779 | 638 | [phi0690](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AlatinLit%3Aphi0690/) + local check of proper nouns |
| `phi0959.phi006.perseus-lat1.tb.xml` | `phi0959.phi006.perseus-lat1` | Ovid, *Metamorphoses* | HEX | 183 | 2655 | 2205 | [phi0959](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AlatinLit%3Aphi0959/) + local check of proper nouns |
| `phi0474.phi013.perseus-lat1.tb.xml` | `phi0474.phi013.perseus-lat1` | Cicero, *In Catilinam* | PROSE_CLASS | 137 | 1915 | 1571 | [phi0474](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AlatinLit%3Aphi0474/) + local check of proper nouns |
| `phi0631.phi001.perseus-lat1.tb.xml` | `phi0631.phi001.perseus-lat1` | Sallust, *Bellum Catilinae* | PROSE_CLASS | 336 | 4999 | 4130 | [phi0631](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AlatinLit%3Aphi0631/) + local check of proper nouns |
| `phi1221.phi007.perseus-lat1.tb.xml` | `phi1221.phi007.perseus-lat1` | Augustus, *Res Gestae* | PROSE_CLASS | 38 | 713 | 620 | [phi1221](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AlatinLit%3Aphi1221/) + local check of the opening sentence |
| `phi0448.phi001.perseus-lat1.tb.xml` | `phi0448.phi001.perseus-lat1` | **Caesar, *De bello Gallico*** | PROSE_CLASS ⚠ | 24 | 352 | 304 | [phi0448](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AlatinLit%3Aphi0448/) + local check of proper nouns; **not in README**, contradicts E2 |
| `phi1351.phi005.perseus-lat1.tb.xml` | `phi1351.phi005.perseus-lat1` | Tacitus, *Historiae* ⚠ | PROSE_POST | 64 | 867 | 730 | [phi1351](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AlatinLit%3Aphi1351/) + local check of proper nouns; ⚠ **URN/work conflict, UNRESOLVED** — see the verification pass below |
| `phi1348.abo012.perseus-lat1.tb.xml` | `phi1348.abo012.perseus-lat1` | Suetonius, *Divus Augustus* | PROSE_POST | 109 | 2066 | 1748 | [phi1348](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AlatinLit%3Aphi1348/) + local check of proper nouns |
| `phi0972.phi001.perseus-lat1.xml` | `phi0972.phi001.perseus-lat1` | Petronius, *Satyricon* | PROSE_POST | 547 | 5955 | 4812 | [phi0972](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AlatinLit%3Aphi0972/) + local check of proper nouns; ⚠ prefix lacks `.tb` |
| `phi0620.phi001.perseus-lat1.tb.xml` | `phi0620.phi001.perseus-lat1` | Propertius, *Elegiae* | OTHER_VERSE | 224 | 2801 | 2318 | [phi0620](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AlatinLit%3Aphi0620/) + local check of proper nouns |
| `phi0975.phi001.perseus-lat1.tb.xml` | `phi0975.phi001.perseus-lat1` | Phaedrus, *Fabulae* | OTHER_VERSE | 389 | 4118 | 3383 | [phi0975](https://atlas.perseus.tufts.edu/library/urn%3Acts%3AlatinLit%3Aphi0975/) + local check of subject vocabulary |
| `tlg0031.tlg027.perseus-lat1.tb.xml` | `urn:cts:`**`greekLit`**`:tlg0031.tlg027.perseus-lat1` ⚠ | Jerome, *Vulgata* (Apocalypsis) | EXCLUDED | 154 | 2003 | 1827 | [tlg0031](https://catalog.perseus.org/catalog/urn%3Acts%3AgreekLit%3Atlg0031.tlg027.perseus-lat1) + local check of subject vocabulary |

⚠ **Namespace exception.** Every other Latin row is `urn:cts:latinLit:…`; this one
is **`greekLit`**. `tlg0031` is the TLG textgroup of the New Testament, and a CTS
URN takes the namespace of its textgroup, not the language of the edition — so the
Latin translation (`perseus-lat1`) of Revelation still sits under `greekLit`. The
Perseus catalogue record linked above is the authority.

---

## Verification pass over all 30 rows (2026-09-03)

Ordered after an external review found that the Tacitus row's URN and its work
label cannot both be right. One wrong row is a reason to re-check thirty, not
one.

**Method, and why it is not the one the review asked for.** The review proposed
recording each document's incipit and explicit as internal evidence. That is
forbidden by this document's own licence clause above (D28): *no word, name or
line of the treebanks appears here*. What replaces it is evidence that is
mechanical, licence-safe and reproducible by anyone with the pinned release:

1. **Prefix and sentence-count identity.** Every `sent_id` in the five pinned
   `.conllu` files was reduced to its prefix and counted. The result is **exactly
   the 30 prefixes** tabulated above, with **all 30 sentence counts matching** —
   18 `grc` + 12 `la`, no prefix present that no row claims, no row claiming a
   prefix the release lacks. This is what makes the tables above a description of
   r2.18 rather than a description of §2.3.
2. **Work label against the treebank's own README.** Each README declares the
   works its release contains. That declaration is the treebank's claim about
   itself, independent of both the catalogue and of us, so it is the third
   witness a two-way disagreement needs.

**Latin — 11 of 12 rows corroborated.** `UD_Latin-Perseus/README.md` declares
eleven works, and eleven of the twelve proposed labels appear in it verbatim
(allowing the README's own *Phaerus* for Phaedrus and *Life of Augustus* for
*Divus Augustus*). The twelfth is **Caesar**, which the README does not declare
at all — the already-recorded E2 contradiction, now confirmed from the opposite
direction: it is not that we mislabelled a declared work, it is that a prefix is
present that the release does not announce.

**Greek — 18 of 18 rows corroborated, with one new finding.**
`UD_Ancient_Greek-Perseus/README.md` declares thirty works, and every one of the
eighteen proposed labels appears among them. The README also confirms **E1** from
the same direction: it declares **seven** Aeschylus plays where the release
carries **one**, and declares Lysias ×4, Polybius, Apollodorus and Aesop, none of
which is present. A README is a claim about a release, not the release.

**New finding — the Hymn is doubly attributed in the README (bears on O8).** The
Greek README lists *Hymn to Demeter* **twice**, once under `Anonymous` and once
under `Pseudo-Homer`, for the **single** prefix
`tlg0013.tlg002.perseus-grc1.tb.xml`. O2 stays resolved — one prefix, no
duplication in the data — but the source the registry would appeal to is itself
undecided between an anonymous attribution and a Homeric one. That is precisely
the O8 question (open question 5 above): whether the Hymn is its own author block
or Homer's. The registry proposes `author: Anonymous`, which is one of the two
things the README says, and it must not be read as settled by transcription.

**No row is corrected here.** Where the evidence agrees, it is recorded as
agreeing; where it does not, the row stays as written and is flagged below. Thirty
silent corrections would be the same fault as one silent error.

### UNRESOLVED — Tacitus `phi1351.phi005` (checklist item 27)

Three witnesses, and they do not agree:

| witness | says |
| --- | --- |
| this proposal (line 105) and `docs/g1_registry_proposal.yaml:235` | `phi1351.phi005` **=** *Historiae* |
| Perseus catalogue | `phi1351.`**`phi005`** = ***Annales***; `phi1351.`**`phi004`** = ***Historiae*** |
| `UD_Latin-Perseus/README.md:39` | the release contains Tacitus, ***Historiae*** |

The two claims in our row are separable and can be wrong independently:

- **`work: Historiae`** is corroborated by the treebank's own README and is the
  claim least likely to be wrong.
- **`source_urn: phi1351.phi005.perseus-lat1`** is transcribed from the `sent_id`
  prefix the release itself carries, and the catalogue says that number names a
  different work.

So the likeliest reading is that **the treebank inherited a wrong URN** — the
text is *Historiae*, carried under the identifier of the *Annales*. The opposite
reading, that the URN is right and both the README and our label are wrong,
requires two independent errors instead of one.

**It is not corrected here, and the incipit test that would settle it is barred
by D28.** Establishing which of the two is wrong is a claim about the *treebank*,
not about our registry, and either resolution has a cost the owner must choose:
changing `source_urn` makes the registry disagree with the raw `doc_id` it is
derived from, while leaving it makes the registry cite a URN for a work it does
not contain. The raw `doc_id` is preserved either way — it is the join key and
must never be edited to match a correction.

**Recommended disposal, for the linguistic supervisor (`D29-A1`):** verify
against a printed edition, which is outside D39's citation restriction only if
the registry cites it, and record the outcome as a ratified correction with its
own evidence. Until then the row stands, marked UNRESOLVED.

---

## Fields that carry a decision

`meter` follows §2.3 closely: hexameter for HEX, prose for prose, and the two
verse meters §2.3 names for Propertius and Phaedrus.

**`period` does not.** §2.3 lists `period` as a registry field but **fixes no
vocabulary and assigns no values**. The scale used here — archaic / classical /
hellenistic / imperial / late-antique — and every assignment on it are mine, and
are proposals like everything else in this document. They are not transcriptions
from §2.3, and the boundaries are debatable in at least three places (Diodorus as
hellenistic against late-republican; Phaedrus as imperial though Tiberian; the
Augustan Latin authors grouped as classical). If a controlled vocabulary is wanted,
fixing it here before the freeze is cheaper than migrating a frozen registry.

These are the rows where a YAML field is a judgement rather than a transcription:

| document | field | value | why it matters |
| --- | --- | --- | --- |
| Athenaeus bk 12, bk 13 | `canonical_doc_id`, `part_order` | `tlg0008.tlg001.perseus-grc1.tb.xml`; 12, 13 | 30 raw prefixes → 29 documents; decides whether option B's PROSE_ALL is 6 documents or 7 |
| Homeric Hymn | `flags` | `o2_single_prefix`, `o8_author_block_open` | O2 closed at document level, O8 still open |
| Herodotus, Thucydides, Diodorus | `flags` | `partial_work_single_book` | each is one book standing as a whole document |
| Caesar | `flags` | `absent_from_readme`, `contradicts_e2`, `smallest_document` | regime is proposed, not derived from §2.3 |
| Augustus | `flags` | `epigraphic` | §2.3 flag, carried through |
| Petronius | `flags` | `verse_insets`, `o4_open`, `prefix_lacks_tb_infix` | O4 not attempted |
| Vergil | `flags` | `smallest_hex_document` | 638 retained tokens: this is T\*_la |
| Aeschylus | `flags` | `e1_only_one_aeschylus_play_present` | evidence for erratum E1 |
| Jerome | `source_urn` | `urn:cts:greekLit:…` | namespace exception, see ⚠ above |
| Sophocles ×5, tragedies | `meter` | `iambic trimeter + lyric (mixed)` | §2.3: tragedy operationalizes "non-hexameter verse", not one meter |

The file also carries `_status: PROPOSED`, which is metadata rather than an
assignment and is what blocks a canonical run.

---

## Open questions — these need your decision, not my proposal

1. **Athenaeus 12 + 13 → one document?** Two prefixes of one work. The YAML
   proposes the merge (`canonical_doc_id:
   tlg0008.tlg001.perseus-grc1.tb.xml`). It is not cosmetic: **18 raw prefixes →
   17 canonical documents** with it, and under option B of the D55 proposal it
   decides whether PROSE_ALL is 6 documents (𝔻 = 11, restoring 462/2048) or 7
   (𝔻 = 12).

2. **`part_order` for a merged document.** If the merge is ratified, `part_order`
   should become mandatory — integer, present for every member, unique within the
   canonical group — because `sent_ord` would otherwise produce duplicate ranks.
   Proposed: 12 → `12`, 13 → `13`.

   **Not enforced today, and deliberately so.** No code reads `part_order`,
   because `sent_ord` is one of the three implementations this checkpoint defers
   (with `freeze_alphabet` and `t_star`). The canonical audit does not need
   sentence order and is unaffected; `run_encode` and the P-BOUND arm do, and must
   not run until the rule exists **with its tests**. The freeze is independently
   blocked: `alphabet.freeze_alphabet` raises `NotImplementedError` and `t_star`
   does not exist, so nothing can be frozen by accident in the meantime.

   Unread is not the same as unknown: `part_order` is named in
   `registry.KNOWN_OVERRIDE_FIELDS`, so the schema **accepts** it as a declared
   field rather than dropping it as an unrecognised one. That list is what makes
   the rest of this file safe to write — every key outside it is now refused, so a
   `flag:` typed for `flags:` fails loudly instead of vanishing (D55 §xiv,
   convention 12).

   Accepted is not the same as validated, and since 2026-09-03 it is
   half-validated: `build_registry` now refuses a `part_order` that is not a
   non-negative `int`, booleans included, since `isinstance(True, int)` is true in
   Python. That is a **shape** guarantee, not a use — it still orders nothing,
   because nothing reads it. What remains unchecked is exactly what only matters
   once something does read it: that `part_order` is present on **every** member
   of a merged group and **unique** within it. Both stay implementation
   obligations alongside `sent_ord` (D55 checklist B, item 13), rather than being
   left to be noticed when `run_encode` produces scrambled ranks.

3. **Book-level prefixes standing as whole documents.** Herodotus `.1`,
   Thucydides `.1`, Diodorus `.11` are single books of much longer works, flagged
   `partial_work_single_book`. Proposed: each stands as one document. This is
   what makes Greek PROSE_CLASS two documents rather than two authors' complete
   works, and it is worth an explicit "yes".

4. **Caesar's regime.** `phi0448.phi001` is proposed PROSE_CLASS. Excluding it
   needs a stated reason: at 304 retained tokens it is the smallest document, but
   the *Aeneid* — a primary HEX document — has 638 and the *Res Gestae* 620, so a
   size rule that removes Caesar cannot be applied consistently without gutting
   the Latin arm. Including it moves P2-Latin's floor from ≈0.036 to ≈0.0278
   (still above 0.025; §5.7's qualitative status is unchanged).

   **What that does and does not mean** (stated 2026-09-03): including Caesar
   changes the Latin document count and therefore the size of the Latin
   enumeration, and nothing else. It is **not** evidence for or against either
   side of the Greek A/B choice, which turns on whether PROSE_POST joins the
   primary contrast (𝔻 = 7 vs 11) and is a question about the *Greek* arm alone.
   The two decisions are independent and must be ruled on separately; the floor
   figures above are consequences to weigh, not an argument for a verdict.

5. **O8 — the Hymn's author block, and a missing registry field.** O2 is resolved
   at document level (one prefix, no duplication), but whether the Hymn is its own
   block or Homer's is open, and it changes the author-level enumeration from
   C(5,3) = 10 / 2⁵ = 32 to C(4,2) = 6 / 2⁴ = 16.

   **The registry cannot currently express the answer.** §2.3's schema has
   `author`, which is bibliographic attribution — the Hymn's is `Anonymous`. The
   author *block* is a different thing: the randomization unit of D43(v), an
   inference-level grouping that may merge or split bibliographic authors. Using
   `author` for both would silently decide O8 by transcription. **Proposed
   (requires ratification — a registry schema addition):** a separate
   `author_block` field, defaulting to `author` where the two coincide.

   O8 may stay open through the pre-audit, but **G1 cannot close without it**: the
   author-level floors are part of what G1 freezes, and they are not derivable
   from the bibliographic field.

6. **O4 — Petronius verse insets.** `phi0972.phi001` is flagged `verse_insets`.
   Sentence-level identification of the verse portions has **not** been attempted.

7. **Sophocles play↔number mapping.** The five plays match §2.3's list, and each
   was identified by a local check of its named characters rather than assumed
   from TLG numbering. The three Hesiod works and Diodorus, by contrast, rest on
   catalogue numbering alone — the evidence column says which is which. Worth a
   second pair of eyes at the supervisor touchpoint.

8. **`period` values** are proposed on a coarse scale (archaic / classical /
   hellenistic / imperial / late-antique). §2.3 does not fix a vocabulary; if one
   is wanted, it should be fixed here before the freeze.
