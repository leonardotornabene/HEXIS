# PROGETTO HEXIS — INDICE DEL PACCHETTO OPERATIVO

**Hexameter Information Signature** — Organizzazione morfosintattica sotto vincolo metrico, misurata con un unico strumento: il context tree MDL alla Rissanen. **Versione 2.0 — 6 luglio 2026.** Sostituisce integralmente la v1.0 (5 luglio 2026), conservata in `archive_v1/`.

## Che cosa è cambiato nella v2.0 (in una frase)

Il progetto è stato consolidato attorno a **un solo strumento statistico**: la batteria di misure separate della v1.0 (entropia per chunk, JSD confermativa, entropia condizionata, informazione mutua con baseline di shuffle) è ritirata come apparato confermativo, perché quelle grandezze sono *troncature lisciate del context tree stesso*; restano come diagnostiche interne. Le ipotesi diventano **tre letture di un unico modello**: radice (distribuzionale), guadagno di contesto (sequenziale, statistica P2), transfer inter-regime (predittiva, statistica P1). La JSD sopravvive come appendice facoltativa. Decisioni di governo: **D32–D39** nel Decision Log. Il cambiamento è avvenuto **prima di qualunque calcolo sui dati reali**, e lo dichiareremo nel preprint.

## I cinque documenti

| File | Lingua | Contenuto | Quando usarlo |
| --- | --- | --- | --- |
| `00_LEGGIMI_INDICE.md` | IT | Questo indice | Ora |
| `01_MASTER_SPEC.md` | EN | **Il documento centrale (v2.0):** fatti di corpus verificati, pipeline, alfabeto, l'algoritmo integrale del context tree con pseudocodice normativo, i protocolli di fitting (riferimento / LODO di regime / LODO pooled label-free), le statistiche P1/P2/S1/R1/L1, l'inferenza esatta a livello di documento, architettura software, suite di test con verità analitiche, tabelle/figure, gate G0–G7 | Da allegare in ogni sessione AI |
| `02_DECISION_LOG.md` | EN | 39 decisioni: D01–D31 riportate con stato aggiornato (alcune superate da D32), le nuove D32–D39 per esteso, open items O1–O6 | Ogni volta che qualcosa deve cambiare: si emenda qui, mai in silenzio |
| `03_ROADMAP_OPERATIVA_IT.md` | IT | Roadmap v2.0: 13 settimane nominali dentro la tua finestra di 12–15, con il context tree **anticipato alla Fase 2** (il rischio maggiore si affronta subito); criteri di accettazione, checklist di comprensione, prompt-tipo; in appendice il **REGISTRO BIBLIOGRAFICO COMPLETO** (tutte le fonti: le 11 della proposta, Chomsky, Galves 2012, Chen 2024, i fondamenti VLMC, le risorse dati — con stato di verifica e ruolo nel preprint) | La tua guida quotidiana; il registro serve alla Fase 7 |
| `04_AI_HANDOFF_PROMPT.md` | EN | Bootstrap prompt v2.0 (con le regole del disegno a strumento unico), template `CLAUDE.md`, template di sessione, checklist di revisione | All'avvio di ogni sessione AI |

## Ordine di lettura consigliato

1. Questo indice.

2. `03_ROADMAP_OPERATIVA_IT.md` per intero, inclusa la sezione "Le decisioni che definiscono il progetto" e l'appendice bibliografica.

3. `01_MASTER_SPEC.md`: §1 (le tre letture e le statistiche P1/P2), §2 (fatti di corpus), §4 (lo strumento), §9 (gate). Il resto fase per fase.

4. `02_DECISION_LOG.md`: leggi per esteso D32–D39; scorri le altre.

## Le scoperte di verifica che restano fondanti (invariate dalla v1.0)

1. Il treebank greco contiene **12 tragedie** (Eschilo ×7, Sofocle ×5) e molta prosa post-classica → disegno a più regimi, con la tragedia come test di specificità.

2. Il treebank latino contiene anche Girolamo (Vulgata, esclusa), Properzio, Fedro, Petronio, Svetonio, Augusto; **Cesare è assente**.

3. Release corrente **UD v2.18**; licenza **CC BY-NC-SA 2.5** (nessuna ridistribuzione dei dati nel repository). Novità di verifica della v2.0 (6 luglio 2026): citazioni **Galves et al. 2012** e **Chen et al. 2024** verificate su fonte primaria e inserite nel registro con obbligo di differenziazione nel related work.

## Regola d'oro del progetto (invariata)

Nessuna modifica silenziosa. Ogni cambiamento a metodologia, alfabeto, parametri o protocolli passa da un emendamento esplicito al `02_DECISION_LOG.md`. Le AI sono vincolate a questa regola dal file `04_AI_HANDOFF_PROMPT.md`.

## Stato del progetto

- [x] Proposta di ricerca (documento di partenza)

- [x] Verifica fatti di corpus su fonti primarie (5 lug 2026)

- [x] Pacchetto operativo v1.0 (5 lug 2026, archiviato)

- [x] **Ristrutturazione a strumento unico + pacchetto v2.0 (6 lug 2026, questo)**

- [ ] Gate G0: ambiente + test non-tree verdi + profiling costo fit

- [ ] Gate G1: audit → registro, alfabeto e T* CONGELATI

- [ ] Gate G2: piano confermativo congelato (OSF opzionale)

- [ ] Gate G3: context tree validato sui quattro processi analitici

- [ ] Gate G4: modelli di riferimento + letture descrittive

- [ ] Gate G5: inferenza confermativa (P1, P2; S1)

- [ ] Gate G6: latino + sottocampioni appaiati

- [ ] Gate G7: piano di sensibilità (13 celle) → scrittura

- [ ] Preprint su arXiv (cs.CL)
