# G1 — registro delle ratifiche

**Stato: ratificate le sole voci tecniche 17–20 e 23–26; tutte le decisioni
scientifiche restano aperte.** Questo file è il posto unico dove si registrano le
decisioni man mano che vengono prese. Non è un documento di
evidenza e non ne duplica il contenuto: ogni riga porta un'etichetta e un numero,
e l'autorità su numeri e argomenti resta il checklist di
`docs/g1_D55_proposal.md` (con `docs/g1_registry_proposal.md` per le 30 righe).

**Regola.** Le ratifiche tecniche del 4 settembre sono applicate al ramo
`g1/pre-audit`; non modificano costanti, registro, alfabeto o T\*. Le decisioni
scientifiche registrate qui non si applicano finché i rispettivi emendamenti non
sono depositati. `01_MASTER_SPEC.md`, `02_DECISION_LOG.md` e i valori scientifici
in `config/` restano quindi intatti; la voce 18 impone emendamenti separati.

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

Il blocco tecnico 17–20 e 23–26 è concluso. Per ciò che resta:

1. **Voce 21 per prima** — decide se le voci 1–7 si prendono oggi o dopo il
   supervisore linguistico. È l'unica che riordina tutte le altre, e costa nulla.
2. **Voci 8–11** — contratti del freeze e letture GATE-A, ancora scientifici o
   accoppiati al contenuto ratificato.
3. **Voce 1** — con il supervisore se la 21 dice «prima», da sola se dice «dopo».
4. **Voce 27, poi 2–7** — prima si dispone il conflitto URN di Tacito, poi si può
   ratificare l'intero registro che lo contiene.
5. **Sezione B** — dopo il freeze, ai gate che la richiedono.

---

## A — bloccano il freeze di G1

| # | decisione | dipende da | stato | verdetto | data |
| --- | --- | --- | --- | --- | --- |
| 1 | Contrasto primario greco: opzione **A**, **B** o **route A\*** (A + interruttore condizionale su O7, entrambi i T\* congelati) | 21 · reciproca con 16 sotto A\* | APERTA | — | — |
| 2 | Il registro: tutte e 30 le righe (regime, `meter`, `period`, `flags`, `source_urn`) | 21 · 27 | APERTA | — | — |
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
| 27 | Tacito `phi1351.phi005`: il testo è *Historiae*, ma Perseus assegna phi005 agli *Annales*. **(a)** tenere l'URN upstream e il flag · **(b)** correggere `source_urn` a phi004 · **(c)** trattenere la riga per il supervisore linguistico (**consigliata**) | 21 | APERTA | — | — |

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
| 17 | Convenzioni software §xiv, `--force` solo pre-audit e disciplina di ri-attestazione stretta | — | RATIFICATA | Canonico pulito e senza `--force`; ogni commit sostanziale richiede i gate, salvo un unico commit amministrativo solo-HANDOFF | 2026-09-04 |
| 18 | Rotta per depositare gli emendamenti | — | RATIFICATA | Voci separate, ciascuna con il proprio impatto | 2026-09-04 |
| 19 | `results/` e artefatti congelati | — | RATIFICATA | `results/` resta tracciato; eccezione `.gitignore` esplicita per i futuri artefatti congelati | 2026-09-04 |
| 20 | Gate `g1`: inventario di copertura obbligatoria | — | RATIFICATA | Le undici aree correnti sono normative; i due file-inventario sono ancorati dal `conftest.py` di repository | 2026-09-04 |
| 23 | Legare gli input dell'audit a `PROVENANCE.md` | — | RATIFICATA | Canonico blocca assenza o mismatch; pre-audit li espone nel report e manifest | 2026-09-04 |
| 24 | Ambito documentale dell'atto di ratifica | 18 | RATIFICATA | L'atto che muta lo stato scientifico aggiorna nello stesso commit ogni puntatore e copia derivata ancora applicabile | 2026-09-04 |
| 25 | Identità delle tre copie delle istruzioni permanenti | — | RATIFICATA | Test byte-per-byte; in `AGENTS.md` differisce soltanto la prima riga | 2026-09-04 |
| 26 | Autorità del registro canonico | 2 · 18 | RATIFICATA | Solo `config/registry_overrides.yaml`, su commit Git pulito; `_status` resta necessario ma non sufficiente | 2026-09-04 |

---

## Verdetti

Il 4 settembre 2026 il proprietario ha approvato la sanatura tecnica integrale,
senza autorizzare alcuna scelta scientifica:

- **17:** ratificate le convenzioni tecniche come riscritte in §xiv. Il canonico
  richiede commit pulito e rifiuta `--force`; il pre-audit può forzare ma dichiara
  il rischio di stato parziale. Ogni commit sostanziale richiede un nuovo run;
  solo un commit finale che modifica esclusivamente `docs/HANDOFF.md` può riportare
  i conteggi misurati sul proprio genitore.
- **18:** scelta la rotta a emendamenti separati.
- **19:** `results/` resta versionato; l'eccezione per i futuri artefatti congelati
  sarà esplicita e contestuale al freeze.
- **20:** l'inventario G1 corrente è normativo e i file-inventario G0/G1 non possono
  essere rimossi o smarcati lasciando verde il gate.
- **23:** il Markdown esistente di `PROVENANCE.md` è l'ancora; nessun nuovo formato.
- **24:** il futuro atto scientifico deve aggiornare nello stesso commit tutti i
  puntatori e documenti derivati che esso rende falsi; nessun conteggio manuale di
  occorrenze costituisce prova di completezza.
- **25:** le tre copie delle istruzioni sono vincolate da test.
- **26:** l'autorità canonica deriva dal path di repository e dal commit pulito
  registrato nel manifest. Non si attribuisce al path una prova crittografica di
  intenzione umana che non possiede.
