# CHANGELOG — RIALLINEAMENTO DOCUMENTALE v2.1 (2026-07-21)

Esecuzione delle decisioni **D40–D51** (ratificate da Massimo il 2026-07-21; adozione dei file = ratifica finale) sui cinque documenti operativi. Ogni edit è stato applicato con ancoraggio esatto e fallimento rumoroso; la traccia macchina-leggibile completa (old/new verbatim per ogni edit) è in `AUDIT_EDITS_v2_1.json`. Il restauro della Master Spec è documentato per esteso in `RESTAURO_01_MASTER_SPEC.md` (D48).

**Legenda tag:** R = restauro (D48); A = emendamento ratificato; RA = entrambi nello stesso sito.

## Protocollo di adozione nel repository (`~/Projects/hexis/docs/`)

1. **Commit 1 (baseline dichiarata):** committare le conversioni `.md` del 2026-07-21 tal quali (i cinque file caricati in sessione), con messaggio che dichiara il danno da generazione PDF (D48). Questo preserva il punto di partenza verificabile.
2. **Commit 2 (v2.1):** sostituire i cinque file con le versioni di questa consegna e committare insieme `RESTAURO_01_MASTER_SPEC.md`, `CHANGELOG_RIALLINEAMENTO_v2_1.md` e `AUDIT_EDITS_v2_1.json` (suggerito: in `docs/` o `docs/audit/`). Il `git diff` fra i due commit è la verifica indipendente e integrale di ogni modifica qui dichiarata.
3. La v2.0 in PDF può essere archiviata (es. `archive_v2_0_pdf/`) come registrazione storica; non è più la fonte canonica.

## Sintesi per documento

**00_LEGGIMI_INDICE.md — 12 edit.** Versione 2.1; nuova sezione «Che cosa è cambiato nella v2.1»; tabella dei documenti aggiornata (51 decisioni, O7 bloccante, DN-1–3); ordine di lettura D32–D51; novità di verifica v2.1 (Greco et al. 2023); stato del progetto con ordine di esecuzione v2.1 e gate riordinati G0→G1→G3→G2→G4→…

| # | Tag | Decisione | Sito |
| --- | --- | --- | --- |
| 1 | A | v2.1 | header versione |
| 2 | A | D41 | nota storica JSD |
| 3 | A | v2.1 | sezione v2.1 |
| 4 | A | v2.1 | riga Spec |
| 5 | A | v2.1 | riga Spec gate |
| 6 | A | v2.1 | riga Decision Log |
| 7 | A | v2.1 | riga Roadmap |
| 8 | A | v2.1 | riga Handoff |
| 9 | A | v2.1 | ordine lettura |
| 10 | A | v2.1 | verifiche fondanti |
| 11 | A | v2.1 | stato v2.1 |
| 12 | A | D44(vii)+D45+D42 | blocco gate v2.1 |

**01_MASTER_SPEC.md — 6 sostituzioni di blocco + 40 edit puntuali.** Riemissione v2.1: restauro D48 (vedi RESTAURO) + tabella degli emendamenti in testa + emendamenti D40–D51 come da tabella nel documento stesso. Verifiche superate: YAML §6.3 analizzato dal parser (23 `deprel_keep`, ultima `parataxis`, d_max 8, famiglia [P1, P2]); batteria finale 11/11 (zero riferimenti fantasma §6.5, zero «optional appendix» non annotati, zero «min p = 0.05», zero «profiled at G0», glifi ripristinati, ordine v2.1 dichiarato due volte, header e footer v2.1).

Blocchi (pass A): | # | Tag | Decisione | Sito |
| --- | --- | --- | --- |
| 1 | R | D48 | B1 §4.1 node fields |
| 2 | R | D48 | B2 §4.1 training pass |
| 3 | RA | D48+D44+D47 | B3 §6.1 repository tree |
| 4 | RA | D48+D44 | B4 §6.2 interfaces |
| 5 | R | D48 | B5 §6.3 YAML |
| 6 | RA | D48+D44+D45 | B6 §9 DAG |

Edit puntuali (pass B): | # | Tag | Decisione | Sito |
| --- | --- | --- | --- |
| 1 | A | v2.1 | header version |
| 2 | A | v2.1 | v2.1 summary + amendment table |
| 3 | A | v2.1 | §0.2 label dates |
| 4 | A | D46 | §0.6 ghost ref |
| 5 | RA | D48+D41 | §1.1 R1 + emphasis |
| 6 | A | D41 | §1.2 R1 row |
| 7 | A | D49+D43+D44 | §1.2 rationale |
| 8 | A | D40 | §1.3 crosswalk |
| 9 | R | D48 | §2.5 wrapped comment |
| 10 | A | D46 | §3.7 sidecar |
| 11 | R | D48 | §4.1 emphasis |
| 12 | R | D48 | §4.1 selection s* |
| 13 | A | D45 | §4.1 profiling gate |
| 14 | RA | D48+D46+D51 | §4.2 full paragraph |
| 15 | R | D48 | §4.3 emphasis + s* |
| 16 | RA | D48+D41+D49 | §4.4 full paragraph + G_own |
| 17 | R | D48 | §4.5 emphasis |
| 18 | A | D49 | §4.5 F5 curves |
| 19 | A | realignment ⑥ | §4.5 lexicon caveat |
| 20 | RA | D43 | §5.1 full rewrite |
| 21 | RA | D48+D44 | §5.2 full rewrite |
| 22 | A | realignment ⑤ | §5.3 CI semantics |
| 23 | A | D44(vii) | §5.5 freeze reposition |
| 24 | A | D42+D50+D45 | §5.6 partition + GATE-A |
| 25 | A | D43 | §5.7 sidedness + d_max |
| 26 | A | D44(iv) | §5.8 confound pointer |
| 27 | A | D49 | §5.8 claim template |
| 28 | A | D46 | §6.4 manifest policy |
| 29 | A | D44 | §7 permutation + calibration rows |
| 30 | A | D43+D44+D49+⑤ | §8 T3 |
| 31 | A | ⑥ | §8 T6 |
| 32 | A | D49 | §8 F5 |
| 33 | A | D41 | §8 R1 figure |
| 34 | A | D44(vii)+D45 | §9 order note + criteria |
| 35 | R | D48 | §10 emphasis |
| 36 | A | D43 | §10 Tier-2 limitation |
| 37 | RA | D48+D49+D44 | App B glossary |
| 38 | A | D40 | App C crosswalk |
| 39 | A | v2.1 | footer |
| 40 | A | D41 | v2.0 summary historical note |

**02_DECISION_LOG.md — 15 edit.** Versione 2.1; disciplina append-only: le voci D01–D39 restano intatte nel testo, con il solo campo di stato esteso dove emendate (D06→D50; D18→D18-A1 via D47; D20/D21/D24→D43; D26→D46; D30→D44(vii); D32→D41; D33→D40+D43; D36→D44, congelata come registrazione storica con clausola (i) valida; D37→D42+D50); §II-bis con **D40–D51 per esteso**; §III con O6 spostato a G3, **O7 bloccante** e O8; §IV con i nodi differiti DN-1/2/3 e i loro gate determinanti.

| # | Tag | Decisione | Sito |
| --- | --- | --- | --- |
| 1 | A | v2.1 | — |
| 2 | A | v2.1 | — |
| 3 | A | D50 | — |
| 4 | A | D47 | — |
| 5 | A | D43 | — |
| 6 | A | D43 | — |
| 7 | A | D43 | — |
| 8 | A | D46 | — |
| 9 | A | D44 | — |
| 10 | A | D41 | — |
| 11 | A | D40 | — |
| 12 | A | D44 | — |
| 13 | A | D42 | — |
| 14 | A | D44 | — |
| 15 | A | D45 | — |

**03_ROADMAP_OPERATIVA_IT.md — 21 edit.** Versione 2.1; Fase 0 senza profilazione (D45); **Fase 1 divisa in 1a/1b** con clausola di acquisizione parallela e nota di riposizionamento di G2 (D44(vii)); Fase 2 con O6+O7 e «al termine: Gate G2»; Fase 3 con la nota sulla separazione presentazionale G4/G5; Fase 4 con lateralità dichiarata, piano-autore descrittivo senza α e prerequisito O7; Fase 5 nota lateralità; Fase 6 con la partizione D42 e la regola D50; Fase 7 limiti aggiornati; checklist con tre item nuovi/aggiornati (D43, D44, D49); «decisioni che definiscono» con item 1 aggiornato (D41) e nuovi item 9–11; nota strumenti (O6→G3); registro bibliografico con **nota di crosswalk alla numerazione finale**, completamenti alle voci 2, 8, 9, 10, 25 marcati [P — dalla proposta finale; verifica O5] e **voce 26 (Greco et al. 2023) [V 2026-07-21 su fonte primaria nei materiali]**.

| # | Tag | Decisione | Sito |
| --- | --- | --- | --- |
| 1 | A | v2.1 | header |
| 2 | A | D45 | Fase 0 chiusura |
| 3 | A | D45+D44(vii)+D50+D43+D51 | Fase 1 -> 1a/1b |
| 4 | A | D44+D45+D47 | Fase 2 G3+G2 |
| 5 | A | realignment ⑦ | Fase 3 nota |
| 6 | A | D43 | Fase 4 minimi |
| 7 | A | D43+D44+D49 | Fase 4 criterio |
| 8 | A | D43 | Fase 5 sidedness |
| 9 | A | D42+D50+D45 | Fase 6 partizione |
| 10 | A | D43 | Fase 7 limiti |
| 11 | A | D43 | checklist piano-autore |
| 12 | A | D44+D49 | checklist nuovi item |
| 13 | A | D41 | decisioni item 1 |
| 14 | A | D42+D44+D43+D49+D50+D51 | decisioni item 9-11 |
| 15 | A | D45 | nota strumenti |
| 16 | A | D40 | registro crosswalk |
| 17 | A | D40/O5 | registro #2 |
| 18 | A | D40/O5 | registro #8 |
| 19 | A | D40/O5 | registro #9 |
| 20 | A | D40/O5 | registro #10 |
| 21 | A | D40/O5 | registro #25 + #26 |

**04_AI_HANDOFF_PROMPT.md — 15 edit.** Versione 2.1; bootstrap con D01–D51, O7 bloccante e ordine v2.1; regola 2 (JSD→D41), regola 3 (clausola O7: mai congelare/eseguire inferenza confermativa P1 pre-O7), regola 7 (G2 dopo G3), regola 10 (manifest D46); template CLAUDE.md con enumerazioni complete e lateralità (D43), tre nuovi «Do not» (pre-O7, candidates/, celle di rappresentazione) e freeze aggiornato; checklist di revisione con controlli D43/D44/D49 e limiti aggiornati.

| # | Tag | Decisione | Sito |
| --- | --- | --- | --- |
| 1 | A | v2.1 | header |
| 2 | A | v2.1 | bootstrap design tag |
| 3 | A | v2.1+D44 | bootstrap authoritative docs |
| 4 | A | D41 | rule 2 JSD |
| 5 | A | D44 | rule 3 sign-flip |
| 6 | A | D44(vii) | rule 7 freeze |
| 7 | A | D46 | rule 10 manifest |
| 8 | A | v2.1 | CLAUDE.md title |
| 9 | A | v2.1+D44 | CLAUDE.md authoritative |
| 10 | A | D44(vii) | CLAUDE.md freeze |
| 11 | A | D46 | CLAUDE.md determinism |
| 12 | A | D41 | CLAUDE.md JSD |
| 13 | A | D43+D44+D47+D42 | CLAUDE.md schemes + new do-nots |
| 14 | A | D43+D44+D49 | checklist method |
| 15 | A | D43+v2.1 | checklist text |

## Correzione dichiarata in esecuzione (da ratificare con l'adozione)

Nella sessione di audit precedente Claude aveva raddoppiato le soglie bilaterali anche per permutazioni a **gruppi disuguali**. La regola corretta, ora scritta in D43 e applicata ovunque: la soglia bilaterale vale 2× l'unilaterale **solo se l'orbita di randomizzazione contiene lo specchio del segno** — sempre per i sign-flip; per le permutazioni di etichette solo con gruppi uguali; con gruppi disuguali le soglie coincidono. Claim ritirati: 2/462 (→ 1/462, entrambe le lateralità), 2/28 (→ 1/28 ≈ 0,036; D24 numericamente invariata), Lisia-fusa 2/56 (→ **1/56 ≈ 0,018, sotto Holm-1**; lo status senza α resta), fallback O2 a 5 blocchi 0,20 (→ 1/10 = 0,10). Restano validi: piano-autore P2 bilaterale 2/20 = 0,10 (gruppi uguali) e P1-autore unilaterale 1/64 ≈ 0,0156. La proposta finale (§6.11) dichiara esattamente 1/2048, 1/462, 0,10 e ≈0,016 — coerente con la regola corretta.

## Fuori ambito di questa consegna (promemoria)

- **Erratum proposta-side (§6.11):** «non può raggiungere la significatività di famiglia» → «non può raggiungere la significatività **congiunta** della famiglia» (P1-autore da solo ha piso 0,0156 < 0,025). Da integrare nella passata E1–E20 sul docx della proposta, che resta un deliverable separato.
- **ASSUMPTIONS.md §B3:** il testo integrale della proposta D18-A1 va completato da quel file (fuori dai cinque documenti) al touchpoint di Fase 2.
