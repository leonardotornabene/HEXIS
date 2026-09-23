# G1 corpus audit

- Status: **INCOMPLETE / PENDING_REGISTRY**
- Entry point: `hexis.pipeline.run_audit --pre-audit`
- Run id: `audit_preaudit_53f76d297774_cbeffa78b04e_fb53084b6d6a_2026-09-04`
- Config SHA-256: `53f76d297774bba46042d97e6170b093fcef4833a4633633a7712192d14b2440`
- Overrides file: `docs/g1_registry_proposal.yaml`
- Overrides SHA-256: `0b4fa57750ce9691e28505a715d06ca2084895fd8ec4aff35dff676186fc8543`
- UD release (verified against provenance, D03): r2.18
- Raw provenance: **VERIFIED** (`data/raw/PROVENANCE.md`)

> This run is **deliberately incomplete**. It was invoked with
> `--pre-audit`, which is the only way to reach this state: the
> canonical default aborts on any unassigned sentence (§3.3).
> No gate verdict and no T* appear below, and nothing is frozen.

## Declared readings

Five points of §3.4 admit more than one reading. They are stated here rather
than settled silently in code:

1. **GATE-A denominator.** All raw syntactic words of the regime — not the
   excluded subtotal, and not a per-document figure. GATE-A is a per-regime
   threshold (§3.4).
2. **GATE-A scope.** Evaluated **per excluded-deprel label**, and over the
   census of retained-UPOS tokens whose `deprel_base` falls outside the 23,
   independently of whether the active policy drops them or maps them to
   `oth`. D06's escalation names a category and offers an alternative policy
   only for excluded deprels; the D05 UPOS deletions have no alternative and
   are outside the gate. Counting drops instead would make the gate unable to
   fire in exactly the `(ud23_oth, ·)` cells D50 makes mandatory to interpret.
3. **Which regimes carry the GATE-A verdict.** The census below covers all
   five D04 labels; the **verdict** is read over the analysed regimes only,
   excluding `EXCLUDED`.
   D06 says "in any regime" and D04 does list `EXCLUDED` among the five, so
   the literal reading includes it; the substantive one does not, because an
   `EXCLUDED` document enters no estimand. Firing GATE-A is not a precaution
   but a binding change: D50 gives the `(ud23_oth, ·)` cells mandatory-
   interpretation status and puts a declared caveat on **every primary
   conclusion**. Deriving that from material the study does not analyse would
   make the report less accurate, not more cautious. **GATE-B is deliberately
   not narrowed the same way** — §3.4 asks it to *flag a document for
   inspection*, and a flag that names its own document misleads no one, so a
   gate that only asks someone to look may look everywhere.
4. **Exploratory regimes keep their firing power.** The narrowing of reading 3
   stops at D04's disposal label: `OTHER_VERSE` and `PROSE_POST` are analysed
   (§1.4 — specificity check, chronological-robustness set), so an imbalance
   there is evidence about the same annotation the primary contrast reads, and
   D06's category is a property of the annotation rather than of one regime's
   role. This is the reading that can actually bind. Under a primary
   contrast that excludes those regimes, a trigger there would still put D50's
   caveat on every primary conclusion; that is accepted deliberately and is a
   ratification question, not a code default.
5. **Language scope.** Shares are computed per `(language, regime)` — |A|, T*
   and the inferential families are per language (§4.1, §4.2, §5.7), and
   pooling would dilute a Latin excess against the far larger Greek tally. The
   **verdict is one per run**: a trigger in either language fires the gate for
   the whole design, because D06 escalates the excluded-deprel *policy*, which
   both languages and every §5.6 cell share.

## Document inventory

One row per **canonical document**: the §2.3 registry schema, with the
declared merges applied and `n_tokens_retained` filled (`build_registry`
leaves that column null and requires it complete before the G1 freeze;
filling it is not freezing it, and nothing here is persisted).

`n_tokens_retained` is the count under this run's configuration, and is the
column from which T* is derived by hand while `t_star` awaits signature
ratification.

| language | doc_id | source_urn | author | work | regime | meter | period | n_sentences | n_tokens_raw | n_tokens_retained | flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| la | phi0448.phi001.perseus-lat1.tb.xml | urn:cts:latinLit:phi0448.phi001.perseus-lat1 | Caesar | De bello Gallico | PROSE_CLASS | prose | classical | 24 | 352 | 304 | ['absent_from_readme', 'contradicts_e2', 'smallest_document'] |
| la | phi0474.phi013.perseus-lat1.tb.xml | urn:cts:latinLit:phi0474.phi013.perseus-lat1 | Cicero | In Catilinam | PROSE_CLASS | prose | classical | 137 | 1915 | 1571 | [] |
| la | phi0620.phi001.perseus-lat1.tb.xml | urn:cts:latinLit:phi0620.phi001.perseus-lat1 | Propertius | Elegiae | OTHER_VERSE | elegiac couplets | classical | 224 | 2801 | 2318 | [] |
| la | phi0631.phi001.perseus-lat1.tb.xml | urn:cts:latinLit:phi0631.phi001.perseus-lat1 | Sallust | Bellum Catilinae | PROSE_CLASS | prose | classical | 336 | 4999 | 4130 | [] |
| la | phi0690.phi003.perseus-lat1.tb.xml | urn:cts:latinLit:phi0690.phi003.perseus-lat1 | Vergil | Aeneid | HEX | hexameter | classical | 68 | 779 | 638 | ['smallest_hex_document'] |
| la | phi0959.phi006.perseus-lat1.tb.xml | urn:cts:latinLit:phi0959.phi006.perseus-lat1 | Ovid | Metamorphoses | HEX | hexameter | classical | 183 | 2655 | 2205 | [] |
| la | phi0972.phi001.perseus-lat1.xml | urn:cts:latinLit:phi0972.phi001.perseus-lat1 | Petronius | Satyricon | PROSE_POST | prose | imperial | 547 | 5955 | 4812 | ['verse_insets', 'o4_open', 'prefix_lacks_tb_infix'] |
| la | phi0975.phi001.perseus-lat1.tb.xml | urn:cts:latinLit:phi0975.phi001.perseus-lat1 | Phaedrus | Fabulae | OTHER_VERSE | iambic senarii | imperial | 389 | 4118 | 3383 | [] |
| la | phi1221.phi007.perseus-lat1.tb.xml | urn:cts:latinLit:phi1221.phi007.perseus-lat1 | Augustus | Res Gestae Divi Augusti | PROSE_CLASS | prose | classical | 38 | 713 | 620 | ['epigraphic'] |
| la | phi1348.abo012.perseus-lat1.tb.xml | urn:cts:latinLit:phi1348.abo012.perseus-lat1 | Suetonius | Divus Augustus | PROSE_POST | prose | imperial | 109 | 2066 | 1748 | [] |
| la | phi1351.phi005.perseus-lat1.tb.xml | urn:cts:latinLit:phi1351.phi005.perseus-lat1 | Tacitus | Historiae | PROSE_POST | prose | imperial | 64 | 867 | 730 | ['upstream_urn_conflict'] |
| grc | tlg0003.tlg001.perseus-grc1.1.tb.xml | urn:cts:greekLit:tlg0003.tlg001.perseus-grc1 | Thucydides | Histories, book 1 | PROSE_CLASS | prose | classical | 532 | 10396 | 9346 | ['partial_work_single_book'] |
| grc | tlg0007.tlg004.perseus-grc1.tb.xml | urn:cts:greekLit:tlg0007.tlg004.perseus-grc1 | Plutarch | Lycurgus | PROSE_POST | prose | imperial | 248 | 5044 | 4481 | [] |
| grc | tlg0007.tlg015.perseus-grc1.tb.xml | urn:cts:greekLit:tlg0007.tlg015.perseus-grc1 | Plutarch | Alcibiades | PROSE_POST | prose | imperial | 251 | 4943 | 4403 | [] |
| grc | tlg0008.tlg001.perseus-grc1.tb.xml | urn:cts:greekLit:tlg0008.tlg001.perseus-grc1 | Athenaeus | Deipnosophistae, books 12-13 | PROSE_POST | prose | imperial | 1630 | 26245 | 23133 | ['partial_work_two_books', 'merged_prefixes'] |
| grc | tlg0011.tlg001.perseus-grc2.tb.xml | urn:cts:greekLit:tlg0011.tlg001.perseus-grc2 | Sophocles | Trachiniae | OTHER_VERSE | iambic trimeter + lyric (mixed) | classical | 431 | 5229 | 4224 | [] |
| grc | tlg0011.tlg002.perseus-grc2.tb.xml | urn:cts:greekLit:tlg0011.tlg002.perseus-grc2 | Sophocles | Antigone | OTHER_VERSE | iambic trimeter + lyric (mixed) | classical | 391 | 4299 | 3573 | [] |
| grc | tlg0011.tlg003.perseus-grc1.tb.xml | urn:cts:greekLit:tlg0011.tlg003.perseus-grc1 | Sophocles | Ajax | OTHER_VERSE | iambic trimeter + lyric (mixed) | classical | 490 | 5319 | 4364 | [] |
| grc | tlg0011.tlg004.perseus-grc1.tb.xml | urn:cts:greekLit:tlg0011.tlg004.perseus-grc1 | Sophocles | Oedipus Tyrannus | OTHER_VERSE | iambic trimeter + lyric (mixed) | classical | 520 | 5600 | 4571 | [] |
| grc | tlg0011.tlg005.perseus-grc2.tb.xml | urn:cts:greekLit:tlg0011.tlg005.perseus-grc2 | Sophocles | Electra | OTHER_VERSE | iambic trimeter + lyric (mixed) | classical | 528 | 5239 | 4259 | [] |
| grc | tlg0012.tlg001.perseus-grc1.tb.xml | urn:cts:greekLit:tlg0012.tlg001.perseus-grc1 | Homer | Iliad | HEX | hexameter | archaic | 6003 | 79890 | 69327 | [] |
| grc | tlg0013.tlg002.perseus-grc1.tb.xml | urn:cts:greekLit:tlg0013.tlg002.perseus-grc1 | Anonymous | Homeric Hymn to Demeter | HEX | hexameter | archaic | 166 | 2061 | 1761 | ['o2_single_prefix', 'o8_author_block_open'] |
| grc | tlg0016.tlg001.perseus-grc1.1.tb.xml | urn:cts:greekLit:tlg0016.tlg001.perseus-grc1 | Herodotus | Histories, book 1 | PROSE_CLASS | prose | classical | 1092 | 19575 | 17301 | ['partial_work_single_book'] |
| grc | tlg0020.tlg001.perseus-grc1.tb.xml | urn:cts:greekLit:tlg0020.tlg001.perseus-grc1 | Hesiod | Theogony | HEX | hexameter | archaic | 273 | 4610 | 4023 | [] |
| grc | tlg0020.tlg002.perseus-grc1.tb.xml | urn:cts:greekLit:tlg0020.tlg002.perseus-grc1 | Hesiod | Works and Days | HEX | hexameter | archaic | 283 | 3725 | 3189 | [] |
| grc | tlg0020.tlg003.perseus-grc1.tb.xml | urn:cts:greekLit:tlg0020.tlg003.perseus-grc1 | Hesiod | Shield of Heracles | HEX | hexameter | archaic | 182 | 2403 | 2070 | [] |
| la | tlg0031.tlg027.perseus-lat1.tb.xml | urn:cts:greekLit:tlg0031.tlg027.perseus-lat1 | Jerome | Vulgata (Apocalypsis) | EXCLUDED | prose | late-antique | 154 | 2003 | 1827 | ['bible', 'late_antique_translation'] |
| grc | tlg0060.tlg001.perseus-grc3.11.tb.xml | urn:cts:greekLit:tlg0060.tlg001.perseus-grc3 | Diodorus Siculus | Bibliotheca historica, book 11 | PROSE_POST | prose | hellenistic | 733 | 16882 | 15266 | ['partial_work_single_book'] |
| grc | tlg0085.tlg001.perseus-grc2.tb.xml | urn:cts:greekLit:tlg0085.tlg001.perseus-grc2 | Aeschylus | Suppliant Women | OTHER_VERSE | iambic trimeter + lyric (mixed) | classical | 166 | 1529 | 1284 | ['e1_only_one_aeschylus_play_present'] |

## Retention and drop rates, per document

| language | doc_id | n_raw | n_kept | n_upos_excluded | n_deprel_excluded | retention | upos_excluded_rate | deprel_excluded_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| grc | tlg0003.tlg001.perseus-grc1.1.tb.xml | 10396 | 9346 | 1043 | 7 | 0.8990 | 0.1003 | 0.0007 |
| grc | tlg0007.tlg004.perseus-grc1.tb.xml | 5044 | 4481 | 558 | 5 | 0.8884 | 0.1106 | 0.0010 |
| grc | tlg0007.tlg015.perseus-grc1.tb.xml | 4943 | 4403 | 536 | 4 | 0.8908 | 0.1084 | 0.0008 |
| grc | tlg0008.tlg001.perseus-grc1.tb.xml | 26245 | 23133 | 3014 | 98 | 0.8814 | 0.1148 | 0.0037 |
| grc | tlg0011.tlg001.perseus-grc2.tb.xml | 5229 | 4224 | 927 | 78 | 0.8078 | 0.1773 | 0.0149 |
| grc | tlg0011.tlg002.perseus-grc2.tb.xml | 4299 | 3573 | 681 | 45 | 0.8311 | 0.1584 | 0.0105 |
| grc | tlg0011.tlg003.perseus-grc1.tb.xml | 5319 | 4364 | 891 | 64 | 0.8205 | 0.1675 | 0.0120 |
| grc | tlg0011.tlg004.perseus-grc1.tb.xml | 5600 | 4571 | 952 | 77 | 0.8163 | 0.1700 | 0.0138 |
| grc | tlg0011.tlg005.perseus-grc2.tb.xml | 5239 | 4259 | 905 | 75 | 0.8129 | 0.1727 | 0.0143 |
| grc | tlg0012.tlg001.perseus-grc1.tb.xml | 79890 | 69327 | 10120 | 443 | 0.8678 | 0.1267 | 0.0055 |
| grc | tlg0013.tlg002.perseus-grc1.tb.xml | 2061 | 1761 | 284 | 16 | 0.8544 | 0.1378 | 0.0078 |
| grc | tlg0016.tlg001.perseus-grc1.1.tb.xml | 19575 | 17301 | 2226 | 48 | 0.8838 | 0.1137 | 0.0025 |
| grc | tlg0020.tlg001.perseus-grc1.tb.xml | 4610 | 4023 | 576 | 11 | 0.8727 | 0.1249 | 0.0024 |
| grc | tlg0020.tlg002.perseus-grc1.tb.xml | 3725 | 3189 | 528 | 8 | 0.8561 | 0.1417 | 0.0021 |
| grc | tlg0020.tlg003.perseus-grc1.tb.xml | 2403 | 2070 | 326 | 7 | 0.8614 | 0.1357 | 0.0029 |
| grc | tlg0060.tlg001.perseus-grc3.11.tb.xml | 16882 | 15266 | 1616 | 0 | 0.9043 | 0.0957 | 0.0000 |
| grc | tlg0085.tlg001.perseus-grc2.tb.xml | 1529 | 1284 | 236 | 9 | 0.8398 | 0.1543 | 0.0059 |
| la | phi0448.phi001.perseus-lat1.tb.xml | 352 | 304 | 42 | 6 | 0.8636 | 0.1193 | 0.0170 |
| la | phi0474.phi013.perseus-lat1.tb.xml | 1915 | 1571 | 306 | 38 | 0.8204 | 0.1598 | 0.0198 |
| la | phi0620.phi001.perseus-lat1.tb.xml | 2801 | 2318 | 441 | 42 | 0.8276 | 0.1574 | 0.0150 |
| la | phi0631.phi001.perseus-lat1.tb.xml | 4999 | 4130 | 795 | 74 | 0.8262 | 0.1590 | 0.0148 |
| la | phi0690.phi003.perseus-lat1.tb.xml | 779 | 638 | 134 | 7 | 0.8190 | 0.1720 | 0.0090 |
| la | phi0959.phi006.perseus-lat1.tb.xml | 2655 | 2205 | 426 | 24 | 0.8305 | 0.1605 | 0.0090 |
| la | phi0972.phi001.perseus-lat1.xml | 5955 | 4812 | 1054 | 89 | 0.8081 | 0.1770 | 0.0149 |
| la | phi0975.phi001.perseus-lat1.tb.xml | 4118 | 3383 | 697 | 38 | 0.8215 | 0.1693 | 0.0092 |
| la | phi1221.phi007.perseus-lat1.tb.xml | 713 | 620 | 86 | 7 | 0.8696 | 0.1206 | 0.0098 |
| la | phi1348.abo012.perseus-lat1.tb.xml | 2066 | 1748 | 275 | 43 | 0.8461 | 0.1331 | 0.0208 |
| la | phi1351.phi005.perseus-lat1.tb.xml | 867 | 730 | 122 | 15 | 0.8420 | 0.1407 | 0.0173 |
| la | tlg0031.tlg027.perseus-lat1.tb.xml | 2003 | 1827 | 164 | 12 | 0.9121 | 0.0819 | 0.0060 |

### Excluded-UPOS census (D05), by label

| language | doc_id | upos | n | share_of_raw |
| --- | --- | --- | --- | --- |
| grc | tlg0003.tlg001.perseus-grc1.1.tb.xml | INTJ | 8 | 0.0008 |
| grc | tlg0003.tlg001.perseus-grc1.1.tb.xml | PUNCT | 1035 | 0.0996 |
| grc | tlg0007.tlg004.perseus-grc1.tb.xml | INTJ | 5 | 0.0010 |
| grc | tlg0007.tlg004.perseus-grc1.tb.xml | PUNCT | 553 | 0.1096 |
| grc | tlg0007.tlg015.perseus-grc1.tb.xml | INTJ | 2 | 0.0004 |
| grc | tlg0007.tlg015.perseus-grc1.tb.xml | PUNCT | 534 | 0.1080 |
| grc | tlg0008.tlg001.perseus-grc1.tb.xml | INTJ | 46 | 0.0018 |
| grc | tlg0008.tlg001.perseus-grc1.tb.xml | PUNCT | 2964 | 0.1129 |
| grc | tlg0008.tlg001.perseus-grc1.tb.xml | X | 4 | 0.0002 |
| grc | tlg0011.tlg001.perseus-grc2.tb.xml | INTJ | 53 | 0.0101 |
| grc | tlg0011.tlg001.perseus-grc2.tb.xml | PUNCT | 874 | 0.1671 |
| grc | tlg0011.tlg002.perseus-grc2.tb.xml | INTJ | 32 | 0.0074 |
| grc | tlg0011.tlg002.perseus-grc2.tb.xml | PUNCT | 648 | 0.1507 |
| grc | tlg0011.tlg002.perseus-grc2.tb.xml | X | 1 | 0.0002 |
| grc | tlg0011.tlg003.perseus-grc1.tb.xml | INTJ | 31 | 0.0058 |
| grc | tlg0011.tlg003.perseus-grc1.tb.xml | PUNCT | 859 | 0.1615 |
| grc | tlg0011.tlg003.perseus-grc1.tb.xml | X | 1 | 0.0002 |
| grc | tlg0011.tlg004.perseus-grc1.tb.xml | INTJ | 41 | 0.0073 |
| grc | tlg0011.tlg004.perseus-grc1.tb.xml | PUNCT | 908 | 0.1621 |
| grc | tlg0011.tlg004.perseus-grc1.tb.xml | X | 3 | 0.0005 |
| grc | tlg0011.tlg005.perseus-grc2.tb.xml | INTJ | 51 | 0.0097 |
| grc | tlg0011.tlg005.perseus-grc2.tb.xml | PUNCT | 854 | 0.1630 |
| grc | tlg0012.tlg001.perseus-grc1.tb.xml | INTJ | 113 | 0.0014 |
| grc | tlg0012.tlg001.perseus-grc1.tb.xml | PUNCT | 9991 | 0.1251 |
| grc | tlg0012.tlg001.perseus-grc1.tb.xml | X | 16 | 0.0002 |
| grc | tlg0013.tlg002.perseus-grc1.tb.xml | PUNCT | 284 | 0.1378 |
| grc | tlg0016.tlg001.perseus-grc1.1.tb.xml | INTJ | 31 | 0.0016 |
| grc | tlg0016.tlg001.perseus-grc1.1.tb.xml | PUNCT | 2190 | 0.1119 |
| grc | tlg0016.tlg001.perseus-grc1.1.tb.xml | X | 5 | 0.0003 |
| grc | tlg0020.tlg001.perseus-grc1.tb.xml | INTJ | 2 | 0.0004 |
| grc | tlg0020.tlg001.perseus-grc1.tb.xml | PUNCT | 574 | 0.1245 |
| grc | tlg0020.tlg002.perseus-grc1.tb.xml | INTJ | 1 | 0.0003 |
| grc | tlg0020.tlg002.perseus-grc1.tb.xml | PUNCT | 527 | 0.1415 |
| grc | tlg0020.tlg003.perseus-grc1.tb.xml | INTJ | 3 | 0.0012 |
| grc | tlg0020.tlg003.perseus-grc1.tb.xml | PUNCT | 323 | 0.1344 |
| grc | tlg0060.tlg001.perseus-grc3.11.tb.xml | PUNCT | 1615 | 0.0957 |
| grc | tlg0060.tlg001.perseus-grc3.11.tb.xml | X | 1 | 0.0001 |
| grc | tlg0085.tlg001.perseus-grc2.tb.xml | INTJ | 5 | 0.0033 |
| grc | tlg0085.tlg001.perseus-grc2.tb.xml | PUNCT | 230 | 0.1504 |
| grc | tlg0085.tlg001.perseus-grc2.tb.xml | X | 1 | 0.0007 |
| la | phi0448.phi001.perseus-lat1.tb.xml | PUNCT | 42 | 0.1193 |
| la | phi0474.phi013.perseus-lat1.tb.xml | INTJ | 3 | 0.0016 |
| la | phi0474.phi013.perseus-lat1.tb.xml | PUNCT | 303 | 0.1582 |
| la | phi0620.phi001.perseus-lat1.tb.xml | INTJ | 8 | 0.0029 |
| la | phi0620.phi001.perseus-lat1.tb.xml | PUNCT | 433 | 0.1546 |
| la | phi0631.phi001.perseus-lat1.tb.xml | PUNCT | 795 | 0.1590 |
| la | phi0690.phi003.perseus-lat1.tb.xml | PUNCT | 134 | 0.1720 |
| la | phi0959.phi006.perseus-lat1.tb.xml | INTJ | 3 | 0.0011 |
| la | phi0959.phi006.perseus-lat1.tb.xml | PUNCT | 422 | 0.1589 |
| la | phi0959.phi006.perseus-lat1.tb.xml | X | 1 | 0.0004 |
| la | phi0972.phi001.perseus-lat1.xml | INTJ | 11 | 0.0018 |
| la | phi0972.phi001.perseus-lat1.xml | PUNCT | 1043 | 0.1751 |
| la | phi0975.phi001.perseus-lat1.tb.xml | INTJ | 6 | 0.0015 |
| la | phi0975.phi001.perseus-lat1.tb.xml | PUNCT | 691 | 0.1678 |
| la | phi1221.phi007.perseus-lat1.tb.xml | PUNCT | 86 | 0.1206 |
| la | phi1348.abo012.perseus-lat1.tb.xml | PUNCT | 275 | 0.1331 |
| la | phi1351.phi005.perseus-lat1.tb.xml | PUNCT | 122 | 0.1407 |
| la | tlg0031.tlg027.perseus-lat1.tb.xml | INTJ | 3 | 0.0015 |
| la | tlg0031.tlg027.perseus-lat1.tb.xml | PUNCT | 161 | 0.0804 |

### Excluded-DEPREL census (D06/D09), by label

| language | doc_id | deprel_base | n | share_of_raw |
| --- | --- | --- | --- | --- |
| grc | tlg0003.tlg001.perseus-grc1.1.tb.xml | vocative | 7 | 0.0007 |
| grc | tlg0007.tlg004.perseus-grc1.tb.xml | vocative | 5 | 0.0010 |
| grc | tlg0007.tlg015.perseus-grc1.tb.xml | vocative | 4 | 0.0008 |
| grc | tlg0008.tlg001.perseus-grc1.tb.xml | orphan | 2 | 0.0001 |
| grc | tlg0008.tlg001.perseus-grc1.tb.xml | vocative | 96 | 0.0037 |
| grc | tlg0011.tlg001.perseus-grc2.tb.xml | vocative | 78 | 0.0149 |
| grc | tlg0011.tlg002.perseus-grc2.tb.xml | vocative | 45 | 0.0105 |
| grc | tlg0011.tlg003.perseus-grc1.tb.xml | vocative | 64 | 0.0120 |
| grc | tlg0011.tlg004.perseus-grc1.tb.xml | vocative | 77 | 0.0138 |
| grc | tlg0011.tlg005.perseus-grc2.tb.xml | vocative | 75 | 0.0143 |
| grc | tlg0012.tlg001.perseus-grc1.tb.xml | vocative | 443 | 0.0055 |
| grc | tlg0013.tlg002.perseus-grc1.tb.xml | vocative | 16 | 0.0078 |
| grc | tlg0016.tlg001.perseus-grc1.1.tb.xml | vocative | 48 | 0.0025 |
| grc | tlg0020.tlg001.perseus-grc1.tb.xml | vocative | 11 | 0.0024 |
| grc | tlg0020.tlg002.perseus-grc1.tb.xml | vocative | 8 | 0.0021 |
| grc | tlg0020.tlg003.perseus-grc1.tb.xml | vocative | 7 | 0.0029 |
| grc | tlg0085.tlg001.perseus-grc2.tb.xml | vocative | 9 | 0.0059 |
| la | phi0448.phi001.perseus-lat1.tb.xml | discourse | 2 | 0.0057 |
| la | phi0448.phi001.perseus-lat1.tb.xml | flat | 4 | 0.0114 |
| la | phi0474.phi013.perseus-lat1.tb.xml | discourse | 26 | 0.0136 |
| la | phi0474.phi013.perseus-lat1.tb.xml | flat | 4 | 0.0021 |
| la | phi0474.phi013.perseus-lat1.tb.xml | vocative | 8 | 0.0042 |
| la | phi0620.phi001.perseus-lat1.tb.xml | discourse | 9 | 0.0032 |
| la | phi0620.phi001.perseus-lat1.tb.xml | flat | 1 | 0.0004 |
| la | phi0620.phi001.perseus-lat1.tb.xml | vocative | 32 | 0.0114 |
| la | phi0631.phi001.perseus-lat1.tb.xml | discourse | 33 | 0.0066 |
| la | phi0631.phi001.perseus-lat1.tb.xml | flat | 34 | 0.0068 |
| la | phi0631.phi001.perseus-lat1.tb.xml | vocative | 7 | 0.0014 |
| la | phi0690.phi003.perseus-lat1.tb.xml | discourse | 3 | 0.0039 |
| la | phi0690.phi003.perseus-lat1.tb.xml | flat | 2 | 0.0026 |
| la | phi0690.phi003.perseus-lat1.tb.xml | vocative | 2 | 0.0026 |
| la | phi0959.phi006.perseus-lat1.tb.xml | discourse | 6 | 0.0023 |
| la | phi0959.phi006.perseus-lat1.tb.xml | orphan | 5 | 0.0019 |
| la | phi0959.phi006.perseus-lat1.tb.xml | vocative | 13 | 0.0049 |
| la | phi0972.phi001.perseus-lat1.xml | discourse | 71 | 0.0119 |
| la | phi0972.phi001.perseus-lat1.xml | flat | 3 | 0.0005 |
| la | phi0972.phi001.perseus-lat1.xml | orphan | 3 | 0.0005 |
| la | phi0972.phi001.perseus-lat1.xml | vocative | 12 | 0.0020 |
| la | phi0975.phi001.perseus-lat1.tb.xml | discourse | 23 | 0.0056 |
| la | phi0975.phi001.perseus-lat1.tb.xml | orphan | 1 | 0.0002 |
| la | phi0975.phi001.perseus-lat1.tb.xml | vocative | 14 | 0.0034 |
| la | phi1221.phi007.perseus-lat1.tb.xml | discourse | 2 | 0.0028 |
| la | phi1221.phi007.perseus-lat1.tb.xml | flat | 5 | 0.0070 |
| la | phi1348.abo012.perseus-lat1.tb.xml | discourse | 23 | 0.0111 |
| la | phi1348.abo012.perseus-lat1.tb.xml | flat | 19 | 0.0092 |
| la | phi1348.abo012.perseus-lat1.tb.xml | vocative | 1 | 0.0005 |
| la | phi1351.phi005.perseus-lat1.tb.xml | discourse | 5 | 0.0058 |
| la | phi1351.phi005.perseus-lat1.tb.xml | flat | 10 | 0.0115 |
| la | tlg0031.tlg027.perseus-lat1.tb.xml | discourse | 4 | 0.0020 |
| la | tlg0031.tlg027.perseus-lat1.tb.xml | flat | 6 | 0.0030 |
| la | tlg0031.tlg027.perseus-lat1.tb.xml | vocative | 2 | 0.0010 |

## Alphabet inventory (observed, NOT frozen)

Per (language, variant) — §4.1 defines |A| for that pair, so the two
languages are never pooled. No `alphabet.json` is written by this stage.

| language | variant | excluded_deprel_policy | alphabet_size |
| --- | --- | --- | --- |
| grc | ud23 | drop | 106 |
| la | ud23 | drop | 102 |

### Most frequent symbols, per language

| language | id | symbol | n | share_of_retained |
| --- | --- | --- | --- | --- |
| grc | 0 | ADV:advmod | 18138 | 0.1027 |
| grc | 1 | VERB:root | 13225 | 0.0749 |
| grc | 2 | DET:det | 11812 | 0.0669 |
| grc | 3 | ADJ:nmod | 11581 | 0.0656 |
| grc | 4 | NOUN:obj | 11160 | 0.0632 |
| grc | 5 | ADP:case | 10599 | 0.0600 |
| grc | 6 | NOUN:obl | 9371 | 0.0531 |
| grc | 7 | VERB:advcl | 9370 | 0.0531 |
| grc | 8 | PART:advmod | 8761 | 0.0496 |
| grc | 9 | NOUN:nsubj | 8324 | 0.0471 |
| grc | 10 | NOUN:nmod | 6917 | 0.0392 |
| grc | 11 | CCONJ:cc | 5316 | 0.0301 |
| grc | 12 | VERB:conj | 5297 | 0.0300 |
| grc | 13 | PART:cc | 4851 | 0.0275 |
| grc | 14 | PRON:obj | 4138 | 0.0234 |
| grc | 15 | PRON:nsubj | 3671 | 0.0208 |
| grc | 16 | VERB:xcomp | 2843 | 0.0161 |
| grc | 17 | NOUN:conj | 2765 | 0.0157 |
| grc | 18 | SCONJ:mark | 2264 | 0.0128 |
| grc | 19 | PRON:obl | 2184 | 0.0124 |
| la | 0 | VERB:root | 2082 | 0.0857 |
| la | 1 | NOUN:obl | 1967 | 0.0810 |
| la | 2 | NOUN:obj | 1741 | 0.0717 |
| la | 3 | ADV:advmod | 1690 | 0.0696 |
| la | 4 | CCONJ:cc | 1505 | 0.0620 |
| la | 5 | NOUN:nsubj | 1456 | 0.0600 |
| la | 6 | ADJ:amod | 1398 | 0.0576 |
| la | 7 | ADP:case | 1335 | 0.0550 |
| la | 8 | VERB:advcl | 1062 | 0.0437 |
| la | 9 | DET:det | 975 | 0.0401 |
| la | 10 | VERB:conj | 843 | 0.0347 |
| la | 11 | NOUN:nmod | 840 | 0.0346 |
| la | 12 | SCONJ:mark | 752 | 0.0310 |
| la | 13 | NOUN:conj | 562 | 0.0231 |
| la | 14 | PRON:nsubj | 539 | 0.0222 |
| la | 15 | VERB:xcomp | 418 | 0.0172 |
| la | 16 | PRON:obj | 415 | 0.0171 |
| la | 17 | PRON:obl | 363 | 0.0149 |
| la | 18 | VERB:acl | 355 | 0.0146 |
| la | 19 | AUX:cop | 350 | 0.0144 |

The **complete** symbol -> id map, including every tie-break, ships as CSV
beside this report: the top of the list does not let a reader check the
ordering rule, and these are the ids the freeze will later assign.

## Companion CSVs

§3.4 pre-registers the **full** raw contingency per document and regime; at
~10² UPOS×DEPREL pairs per document it is unreadable as a table. These files
carry it, each with a sidecar and hashed in the same manifest:

- `alphabet_inventory_preaudit_53f76d297774_cbeffa78b04e_fb53084b6d6a_2026-09-04.csv`
- `contingency_by_document_preaudit_53f76d297774_cbeffa78b04e_fb53084b6d6a_2026-09-04.csv`
- `contingency_by_regime_preaudit_53f76d297774_cbeffa78b04e_fb53084b6d6a_2026-09-04.csv`

## Regime aggregates (PROVISIONAL — unratified registry)

> **PROVISIONAL.** These aggregates come from a *proposed* registry
> that has not been ratified. They are evidence for that ratification,
> never a result: no gate verdict is derived from them here.

### Drop rates by rule, per regime (T2, §8)

| language | regime | n_raw | n_kept | n_upos_excluded | n_deprel_excluded | retention | upos_excluded_rate | deprel_excluded_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| grc | HEX | 92689 | 80370 | 11834 | 485 | 0.8671 | 0.1277 | 0.0052 |
| grc | OTHER_VERSE | 27215 | 22275 | 4592 | 348 | 0.8185 | 0.1687 | 0.0128 |
| grc | PROSE_CLASS | 29971 | 26647 | 3269 | 55 | 0.8891 | 0.1091 | 0.0018 |
| grc | PROSE_POST | 53114 | 47283 | 5724 | 107 | 0.8902 | 0.1078 | 0.0020 |
| la | EXCLUDED | 2003 | 1827 | 164 | 12 | 0.9121 | 0.0819 | 0.0060 |
| la | HEX | 3434 | 2843 | 560 | 31 | 0.8279 | 0.1631 | 0.0090 |
| la | OTHER_VERSE | 6919 | 5701 | 1138 | 80 | 0.8240 | 0.1645 | 0.0116 |
| la | PROSE_CLASS | 7979 | 6625 | 1229 | 125 | 0.8303 | 0.1540 | 0.0157 |
| la | PROSE_POST | 8888 | 7290 | 1451 | 147 | 0.8202 | 0.1633 | 0.0165 |

### Restricted-position fractions (D35, `available_past >= 4`)

| language | regime | n_evaluated | n_restricted | fraction | min_available_past |
| --- | --- | --- | --- | --- | --- |
| grc | HEX | 80370 | 53009 | 0.6596 | 4 |
| grc | OTHER_VERSE | 22275 | 12769 | 0.5732 | 4 |
| grc | PROSE_CLASS | 26647 | 20173 | 0.7570 | 4 |
| grc | PROSE_POST | 47283 | 35926 | 0.7598 | 4 |
| la | EXCLUDED | 1827 | 1230 | 0.6732 | 4 |
| la | HEX | 2843 | 1877 | 0.6602 | 4 |
| la | OTHER_VERSE | 5701 | 3325 | 0.5832 | 4 |
| la | PROSE_CLASS | 6625 | 4520 | 0.6823 | 4 |
| la | PROSE_POST | 7290 | 4530 | 0.6214 | 4 |

### Excluded-DEPREL shares per regime — the GATE-A input, without its verdict

These are the shares GATE-A would be read off. They are published as
evidence for the ratification and carry **no verdict**: a different
ratified merge or regime assignment would change them. The table is the
census over all five D04 labels; declared readings 3-5 govern which of
them a verdict may be read from, once there is one.

| language | regime | deprel_base | n | share_of_raw |
| --- | --- | --- | --- | --- |
| grc | HEX | vocative | 485 | 0.0052 |
| grc | OTHER_VERSE | vocative | 348 | 0.0128 |
| grc | PROSE_CLASS | vocative | 55 | 0.0018 |
| grc | PROSE_POST | orphan | 2 | 0.0000 |
| grc | PROSE_POST | vocative | 105 | 0.0020 |
| la | EXCLUDED | discourse | 4 | 0.0020 |
| la | EXCLUDED | flat | 6 | 0.0030 |
| la | EXCLUDED | vocative | 2 | 0.0010 |
| la | HEX | discourse | 9 | 0.0026 |
| la | HEX | flat | 2 | 0.0006 |
| la | HEX | orphan | 5 | 0.0015 |
| la | HEX | vocative | 15 | 0.0044 |
| la | OTHER_VERSE | discourse | 32 | 0.0046 |
| la | OTHER_VERSE | flat | 1 | 0.0001 |
| la | OTHER_VERSE | orphan | 1 | 0.0001 |
| la | OTHER_VERSE | vocative | 46 | 0.0066 |
| la | PROSE_CLASS | discourse | 63 | 0.0079 |
| la | PROSE_CLASS | flat | 47 | 0.0059 |
| la | PROSE_CLASS | vocative | 15 | 0.0019 |
| la | PROSE_POST | discourse | 99 | 0.0111 |
| la | PROSE_POST | flat | 32 | 0.0036 |
| la | PROSE_POST | orphan | 3 | 0.0003 |
| la | PROSE_POST | vocative | 13 | 0.0015 |

## Gates

**GATE-A: NOT EVALUATED** — registry in docs/g1_registry_proposal.yaml is not ratified (_status: 'PROPOSED'): a gate verdict requires a ratified registry (§3.3); the per-regime shares under *Regime aggregates* above are provisional.

**GATE-B: NOT EVALUATED** — registry in docs/g1_registry_proposal.yaml is not ratified (_status: 'PROPOSED'): a gate verdict requires a ratified registry (§3.3); the per-regime shares under *Regime aggregates* above are provisional.

Retention above **is** computed over canonical documents: the merges
declared in the overrides file have been applied before counting. What
is missing is not the merge but the ratification — a different ratified
merge would regroup these rows, so no verdict is declared from them.

## T*

**T*: not computed.** §4.2/D51 fixes T* at G1, but `t_star` is deliberately
unimplemented: its signature is unspecified in §6.2 and
`protocols/sampling.py` forbids inventing one. The signature is submitted for
ratification with D55; until then T* is derived by hand from the
`n_tokens_retained` column above, and that derivation is shown in the D55
proposal rather than produced here.

## What this stage did not do

- No model was fitted to any data (D30 — counts only).
- No `alphabet.json`, no registry and no T* were frozen.
- `config/registry_overrides.yaml` was not written.
