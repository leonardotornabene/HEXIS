# G1 — registro delle ratifiche

**Stato: nulla è ratificato.** Questo file è il posto unico dove si registrano le
decisioni man mano che vengono prese, una alla volta. Non è un documento di
evidenza e non ne duplica il contenuto: ogni riga porta un'etichetta e un numero,
e l'autorità su numeri e argomenti resta il checklist di
`docs/g1_D55_proposal.md` (con `docs/g1_registry_proposal.md` per le 30 righe).

**Regola.** Una decisione registrata qui **non è applicata a nulla**.
`01_MASTER_SPEC.md`, `02_DECISION_LOG.md` e `config/` restano intatti finché il
pacchetto non viene depositato come **atto unico** (voce 18: rotta (a) separata o
(b) omnibus). Fino ad allora questo file è l'unico posto in cui una ratifica
esiste, ed è ciò da cui si scriveranno le voci `Dnn-A1`.

**Sostituisce** `HEXIS_foglio_ratifica_G1.pdf` (18 agosto 2026, `g1/pre-audit` @
`61d6496`), archiviato fuori albero — sha256
`73b2afcbbb9774e228a68bf8f1de453be532757fcb02ba9aa30012cc431f39d4`.
**La sua numerazione non è trasferibile qui: coincidono solo le voci 1–11.** Il
foglio numera 12, 13, 14 e 15 ciò che qui è **17, 18, 19 e 21**; lascia senza
numero, nella sua sezione C, ciò che qui è **12–16**; e non contiene affatto le
voci **20, 22, 23, 24, 25, 26, 27** né l'**ambito documentale dell'alfabeto**. Un verdetto preso
sul foglio va quindi trascritto **per argomento, mai per numero**. Una copia
firmabile si rigenera alla fine, con i verdetti dentro, se serve.

**Lingua:** italiano come il foglio, perché è la superficie con cui decidi; le
voci `Dnn-A1` che ne discendono saranno in inglese come il resto del Decision Log.

---

## Ordine consigliato

1. **Voce 21 per prima** — decide se le voci 1–7 si prendono oggi o dopo il
   supervisore linguistico. È l'unica che riordina tutte le altre, e costa nulla.
2. **Blocco tecnico, indipendente da A/B:** 8, 9, 10, 11, 17, 18, 19, 20, 23, 24,
   25. Sblocca tutto il lavoro implementativo (contratto `freeze_alphabet`,
   `t_star`, semantic inventory check, governance) senza toccare una costante
   scientifica. La 24 va presa **con** la 18: quella decide la forma del deposito,
   questa il suo perimetro.
3. **Voce 1** — con il supervisore se la 21 dice «prima», da sola se dice «dopo».
4. **Voci 2–7** — il registro e ciò che ci sta attaccato.
5. **Sezione B** — dopo il freeze, ai gate che la richiedono.

---

## A — bloccano il freeze di G1

| # | decisione | dipende da | stato | verdetto | data |
| --- | --- | --- | --- | --- | --- |
| 1 | Contrasto primario greco: opzione **A**, **B** o **route A\*** (A + interruttore condizionale su O7, entrambi i T\* congelati) | 21 · reciproca con 16 sotto A\* | APERTA | — | — |
| 2 | Il registro: tutte e 30 le righe (regime, `meter`, `period`, `flags`, `source_urn`) | 21 | APERTA | — | — |
| 3 | Cesare, *De bello Gallico* — regime (proposto PROSE_CLASS) | 21 | APERTA | — | — |
| 4 | Ateneo 12+13 — merge, **e con esso il vincolo `part_order`** | 21 | APERTA | — | — |
| 5 | Libri singoli (Erodoto 1, Tucidide 1, Diodoro 11) come documenti interi | 21 | APERTA | — | — |
| 6 | Vocabolario e valori del campo `period` | 21 | APERTA | — | — |
| 7 | O8 e il campo `author_block` | 21 | APERTA | — | — |
| 8 | GATE-A — le cinque letture dichiarate | — | APERTA | — | — |
| 9 | `alphabet.json`: forma · **ambito documentale** · ampiezza del freeze · atomicità (+ eccezione `.gitignore`) · contratto | — | APERTA | — | — |
| 10 | `t_star`: firma proposta e le due chiavi di `config/default.yaml` | — | APERTA | — | — |
| 11 | Semantic inventory check — contro cosa si confronta (+ quarta attesa: ambito dell'alfabeto) | — | APERTA | — | — |
| 21 | Touchpoint del supervisore linguistico **prima** del freeze (`D29-A1`) | — | APERTA | — | — |
| 27 | Tacito `phi1351.phi005`: URN ed etichetta dell'opera non possono essere entrambi giusti — Perseus dice *Annales*, il README del treebank dice *Historiae*. **(a)** tenere l'URN trascritto e registrare il conflitto · **(b)** correggere a phi004 · **(c)** trattenere la riga per il supervisore linguistico (**consigliata**) | 2 · 21 | APERTA | — | — |

## B — bloccano gate successivi, non il freeze

| # | decisione | dipende da | stato | verdetto | data |
| --- | --- | --- | --- | --- | --- |
| 12 | Famiglia latina: propria da 2 o unita in una da 4 | 1 | APERTA | — | — |
| 13 | Regola `sent_ord` (l'ordinamento; il vincolo è alla voce 4) | 4 | APERTA | — | — |
| 14 | Griglia delle learning curve | 1 | APERTA | — | — |
| 15 | O4 — inserti in versi in Petronio | — | APERTA | — | — |
| 16 | O7 — la sua risoluzione (studio G3 su dati sintetici) | 1 (profilo di taglie) | APERTA | — | — |
| 22 | Il braccio latino a T\* = 638: resta un braccio del disegno o diventa appendice | — | APERTA | — | — |

## C — governance di repository e processo

| # | decisione | dipende da | stato | verdetto | data |
| --- | --- | --- | --- | --- | --- |
| 17 | Le tredici convenzioni software (§xiv), eccezione `--force` inclusa **+ la disciplina di ri-attestazione: nessun re-run per i commit solo-documentali** (deciso dal proprietario il 3 set 2026, in vigore, da ratificare qui) | — | APERTA | — | — |
| 18 | Rotta (a) voci separate o (b) omnibus, per depositare gli emendamenti | — | APERTA | — | — |
| 19 | `results/` tracciato o ignorato **+** eccezione `.gitignore` per gli artefatti congelati | — | APERTA | — | — |
| 20 | Gate `g1`: inventario di copertura obbligatoria — **costruito il 3 set 2026** (`tests/test_g1_enforcement.py`, undici aree, verificate contro la collection viva di pytest); resta da ratificare se quelle undici aree sono la definizione normativa dell'insieme G1 | — | APERTA | — | — |
| 23 | Legare gli input dell'audit a `PROVENANCE.md` | — | APERTA | — | — |
| 24 | Ambito documentale dell'atto di ratifica: le **dodici** dichiarazioni su **sette** file che la ratifica rende false nello stesso istante (undici fino al 3 set 2026: la dodicesima è nata dallo stesso ramo che mantiene questa voce) | 18 | APERTA | — | — |
| 25 | Se qualcosa debba imporre l'identità delle tre copie delle istruzioni permanenti (`CLAUDE.md`, `AGENTS.md`, template di `04` §B) | — | APERTA | — | — |
| 26 | `_status: RATIFIED` è un'autodichiarazione del file, non prova della ratifica: **α** ancorare al path di default (non implementabile) · **β** imporre il basename (teatro) · **γ** registrare il digest ratificato fuori dal file (**consigliata**) · **δ** lasciarla com'è | 2 · 18 | APERTA | — | — |

---

## Verdetti

*(vuoto: nessuna decisione presa. Ogni verdetto va qui per esteso — voce, scelta,
motivazione a verbale se il foglio ne chiede una, data — e la riga corrispondente
sopra passa da APERTA a RATIFICATA.)*
