# PROGETTO HEXIS — INDICE DEL PACCHETTO OPERATIVO

**Hexameter Information Signature** — Organizzazione morfosintattica sotto vincolo metrico, misurata con un unico strumento: il context tree MDL alla Rissanen. **Versione 2.1 — 21 luglio 2026.** Sostituisce la v2.0 (6 luglio 2026); la v1.0 (5 luglio 2026) resta conservata in `archive_v1/`.

## Che cosa è cambiato nella v2.0 (in una frase)

Il progetto è stato consolidato attorno a **un solo strumento statistico**: la batteria di misure separate della v1.0 (entropia per chunk, JSD confermativa, entropia condizionata, informazione mutua con baseline di shuffle) è ritirata come apparato confermativo, perché quelle grandezze sono *troncature lisciate del context tree stesso*; restano come diagnostiche interne. Le ipotesi diventano **tre letture di un unico modello**: radice (distribuzionale), guadagno di contesto (sequenziale, statistica P2), transfer inter-regime (predittiva, statistica P1). La JSD sopravvive come appendice facoltativa (v2.1: elevata a lettura descrittiva prevista, D41). Decisioni di governo: **D32–D39** nel Decision Log. Il cambiamento è avvenuto **prima di qualunque calcolo sui dati reali**, e lo dichiareremo nel preprint.

## Che cosa è cambiato nella v2.1 (21 luglio 2026)

Sincronizzazione del pacchetto operativo con la **proposta finale** e chiusura dei nodi procedurali; tutte decisioni pre-dati (**D40–D51** nel Decision Log): crosswalk vincolante fra le ipotesi della proposta finale e le statistiche (H1 = P2, H2 = P1 + S1, H3 = L1; premessa distribuzionale = radice + R1; D40, verificato sul testo finale); la JSD (R1) diventa lettura distribuzionale descrittiva prevista, senza α né test, con caveat di dipendenza dalla taglia (D41); il piano di sensibilità è partizionato in robustezza parametrica e analisi di rappresentazione (D42); ogni soglia esatta dichiara la propria lateralità e il piano-autore diventa descrittivo senza α (D43); la validità del sign-flip di P1 è una **questione aperta e bloccante** (O7), da risolvere con uno studio di calibrazione su dati sintetici — per questo **il Gate G2 è riposizionato dopo G3** (D44(vii); ordine v2.1: G0 → G1 → G3 → G2 → G4 → G5 → G6 → G7; invariante intatto: prima di G2 solo sintetici, primi fit reali a G4); G0 non richiede più la profilazione (O6 → G3) e l'acquisizione dei treebank può procedere in parallelo a G0 (D45); politica dei manifest chiarita — un manifest centrale per run più un sidecar minimo per artefatto (D46); `hexis_ctree` v0.1.0 in quarantena come candidato non canonico, con l'emendamento D18-A1 depositato come proposta (D47); la Master Spec è riemessa con il restauro documentato dei blocchi normativi danneggiati in fase di generazione PDF (D48; tabella completa prima/dopo in `RESTAURO_01_MASTER_SPEC.md`); nuova lettura descrittiva `G_own` per disambiguare la sede della firma (D49); regola GATE-A × C0: la configurazione primaria non si duplica (D50); ambito di T* ristretto al contrasto primario, con il costo di potenza della taglia uniforme dichiarato (D51). Tre nodi restano deliberatamente differiti (DN-1/2/3, determinanti a G2). Registro bibliografico: crosswalk con la numerazione finale e voce 26 (Greco et al. 2023) aggiunta e verificata su fonte primaria.

## I cinque documenti

| File | Lingua | Contenuto | Quando usarlo |
| --- | --- | --- | --- |
| `00_LEGGIMI_INDICE.md` | IT | Questo indice | Ora |
| `01_MASTER_SPEC.md` | EN | **Il documento centrale (v2.1, con tabella degli emendamenti in testa):** fatti di corpus verificati, pipeline, alfabeto, l'algoritmo integrale del context tree con pseudocodice normativo, i protocolli di fitting (riferimento / LODO di regime / LODO pooled label-free), le statistiche P1/P2/S1/R1/L1, l'inferenza esatta a livello di documento, architettura software, suite di test con verità analitiche, tabelle/figure, gate G0–G7 (ordine di esecuzione v2.1) | Da allegare in ogni sessione AI |
| `02_DECISION_LOG.md` | EN | 53 decisioni: D01–D31 con stato aggiornato, D32–D39 (v2) per esteso, **D40–D51 (v2.1, sincronizzazione con la proposta finale)** per esteso, **D52–D53 (ratifica post-v2.1)** per esteso; open items O1–O8 (**O7 bloccante per G2/G5**); nodi differiti DN-1–DN-3 | Ogni volta che qualcosa deve cambiare: si emenda qui, mai in silenzio |
| `03_ROADMAP_OPERATIVA_IT.md` | IT | Roadmap v2.1: 13 settimane nominali dentro la tua finestra di 12–15, con il context tree **anticipato alla Fase 2** e la Fase 1 divisa in **1a** (pipeline non-tree → G0) e **1b** (audit → G1; acquisizione in parallelo a G0, D45); criteri di accettazione allineati all'ordine v2.1 dei gate; checklist di comprensione, prompt-tipo; in appendice il **REGISTRO BIBLIOGRAFICO COMPLETO** (le fonti della proposta con crosswalk alla numerazione finale, Chomsky, Galves 2012, Chen 2024, i fondamenti VLMC, le risorse dati, e Greco et al. 2023 aggiunta in v2.1 — con stato di verifica e ruolo nel preprint) | La tua guida quotidiana; il registro serve alla Fase 7 |
| `04_AI_HANDOFF_PROMPT.md` | EN | Bootstrap prompt v2.1 (regole del disegno a strumento unico + disciplina O7/D44), template `CLAUDE.md`, template di sessione, checklist di revisione | All'avvio di ogni sessione AI |

## Ordine di lettura consigliato

1. Questo indice.

2. `03_ROADMAP_OPERATIVA_IT.md` per intero, inclusa la sezione "Le decisioni che definiscono il progetto" e l'appendice bibliografica.

3. `01_MASTER_SPEC.md`: §1 (le tre letture e le statistiche P1/P2), §2 (fatti di corpus), §4 (lo strumento), §9 (gate). Il resto fase per fase.

4. `02_DECISION_LOG.md`: leggi per esteso D32–D53; scorri le altre.

## Le scoperte di verifica che restano fondanti (invariate dalla v1.0)

1. Il treebank greco contiene **12 tragedie** (Eschilo ×7, Sofocle ×5) e molta prosa post-classica → disegno a più regimi, con la tragedia come test di specificità.

2. Il treebank latino contiene anche Girolamo (Vulgata, esclusa), Properzio, Fedro, Petronio, Svetonio, Augusto; **Cesare è assente**.

3. Release corrente **UD v2.18**; licenza **CC BY-NC-SA 2.5** (nessuna ridistribuzione dei dati nel repository). Novità di verifica della v2.0 (6 luglio 2026): citazioni **Galves et al. 2012** e **Chen et al. 2024** verificate su fonte primaria e inserite nel registro con obbligo di differenziazione nel related work. Novità di verifica della v2.1 (21 luglio 2026): **Greco et al. 2023** verificata su fonte primaria nei materiali di progetto e aggiunta al registro (voce 26); corrispondenza completa fra registro e bibliografia della proposta finale verificata sul testo.

## Regola d'oro del progetto (invariata)

Nessuna modifica silenziosa. Ogni cambiamento a metodologia, alfabeto, parametri o protocolli passa da un emendamento esplicito al `02_DECISION_LOG.md`. Le AI sono vincolate a questa regola dal file `04_AI_HANDOFF_PROMPT.md`.

## Stato del progetto

- [x] Proposta di ricerca (documento di partenza)

- [x] Verifica fatti di corpus su fonti primarie (5 lug 2026)

- [x] Pacchetto operativo v1.0 (5 lug 2026, archiviato)

- [x] Ristrutturazione a strumento unico + pacchetto v2.0 (6 lug 2026)

- [x] **Sincronizzazione con la proposta finale + riallineamento v2.1 (21 lug 2026, questo)**

**Ordine di esecuzione v2.1 (D44(vii)): G0 → G1 → G3 → G2 → G4 → G5 → G6 → G7.**

- [ ] Gate G0: ambiente + test non-tree verdi (asserzioni reali) + infrastruttura deterministica (profilazione → G3; D45)

- [ ] Gate G1: audit → registro, alfabeto e T* CONGELATI (con O2/O8 risolti)

- [ ] Gate G3: context tree validato sui quattro processi analitici + profilazione O6 + studio di calibrazione del null O7

- [ ] Gate G2: piano confermativo congelato (OSF opzionale; richiede O7 risolto)

- [ ] Gate G4: modelli di riferimento + letture descrittive

- [ ] Gate G5: inferenza confermativa (P1, P2; S1) — richiede O7 risolto

- [ ] Gate G6: latino + sottocampioni appaiati

- [ ] Gate G7: piano di sensibilità (13 celle, partizione D42) → scrittura

- [ ] Preprint su arXiv (cs.CL)
