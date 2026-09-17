# Inventario test HEXIS 3.1 — V3-001

Accettazione attiva: marker `v31`; raccolta effettiva obbligatoria, assert eseguiti,
nessuno skip/xfail/xpass. Il confronto col contratto non sostituisce test del futuro CTW.

| ID | Stato V0–V1 | Copertura / obbligo residuo |
|---|---|---|
| T01 | V1 | Input/hash, sent_id, 18 prefissi/17 documenti |
| T02 | V1 | Conteggi documento/blocco e intero corpus |
| T03 | V1 | Parsing, coordinate, identità, errori localizzati |
| T04 | V1 | Mapping globale, inventari, C0/UPOS, inventory_only |
| T05 | V2 | Esclusione di held-out e `inventory_only` dal training, in tutte le sei celle per sette fold |
| T06 | V2 | q esatto, nessun rimpiazzo, ≤1 frammento per contributore, vuoti e budget impossibili |
| T07 | V2 | Ordine sorgente; campionatore invariante all'ordine dei record e cieco alle etichette; riuso di ledger e permutazione come dichiarato |
| T08 | V2 | Vettore §12.2 e sette `block_key` depositati, scopi separati, ripetibilità, accoppiamento O/R; nessuno scopo di sonda attivo |
| T09 | V2 | Stream/reset e partizione esatta del campione; BOS terminale e partizione dei conteggi in T10–T11 |
| T10 | V2 | Enumerazione indipendente degli alberi ammessi contro evidenza, peso di radice e predizione |
| T11 | V2 | Normalizzazione, supporto raro/ignoto, training vuoto, D=0, m100/105/11, input rigorosi |
| T12 | V2 | Identità prequenziale/integrata pre-update; invarianza all'ordine degli stream |
| T13 | V2 | Conteggi/evidenze/pesi/fingerprint invariati dalla valutazione |
| T14 | V2 | Prior estremo in log, due pesi da δ, saturazione distinta dalle foglie forzate |
| T15 | V2 | 25 sintetici alle soglie §12.1 sul CTW canonico; violazione → exit non zero |
| T16 | V2 | Stress storico m106: esecuzione, normalizzazione, supporti, deficit registrato |
| T17 | V2 | Lunghezza, multinsieme, maschera e conteggi di radice conservati; slot distinto dalla provenienza |
| T18 | PARZIALE V2 | Controesempi prefissati di dipendenza interna e di pool eterogeneo al livello del campione; il divario in G/Q sugli stessi controesempi richiede i modelli (PENDING con T19) |
| T19 | PENDING V2 | Q a quattro termini |
| T20 | PENDING V2 | Aggregazioni/due pesi |
| T21 | PENDING V2 | Sensibilità accoppiate |
| T22 | PENDING V2 | Masse/supporti/L_resolved |
| T23 | PENDING V2 | R1 |
| T24 | PARZIALE V1 | Censimento dei sei inventory_only; assenza training/scoring finale PENDING V5 |
| T25 | PENDING V4 | Uguaglianza 490/980 chiavi modello/coppia |
| T26 | PARZIALE V1 | Atomicità/corruzione corpus; resume modellistico PENDING V2 |
| T27 | PENDING V5 | Ricostruzione score/diagnostiche e figure |
| T28 | V0–V1 | Pipeline senza candidates/inferenza; accettazione senza skip |
| T29 | PARZIALE V1 | Identità/round-trip corpus; CE/riproduzione modelli PENDING V5 |
| T30 | PENDING V5 | Report scientifico completo |

| Suite precedente | Disposizione e motivazione |
|---|---|
| test_conllu_reader.py, test_registry.py, test_g1_registry.py | MANTENUTI: parsing/validazioni generiche; registro attivo verificato da test_v31_corpus/config |
| test_alphabet.py, test_g1_alphabet.py | MANTENUTI storici con configurazione v2.1 esplicita; totalità su tag ignoti/ID per frequenza SOSTITUITI nell'attivo da T03/T04 |
| test_sequences.py, test_g1_sequences.py | MANTENUTI generici/storici; concatenazione SEP RITIRATA nell'attivo; stream e coordinate T03/T09 |
| test_run_audit.py | MANTENUTO sull'audit storico esplicito; gate bilingue, provenance e sidecar v2.1 RITIRATI nell'attivo; difese riusate e testate in T01/T26/T29 |
| test_determinism.py | MANTENUTO hashing/scrittura e RNG storico (XOR/CRC32); RNG scientifico SHA-256 SOSTITUITO nell'attivo da T08 |
| test_permutation.py, test_bootstrap_holm.py, test_blocks.py | MANTENUTI utility storiche funzionanti, senza import nella pipeline descrittiva |
| test_g0_enforcement.py, test_g1_enforcement.py, test_gate_inventory_anchor.py | MANTENUTI controlli storici; medesimo enforcement esteso a v31 |
| test_docs_consistency.py | MANTENUTO allineamento storia G1 e copie istruzioni |
| test_context_tree.py, test_tree_slices.py, test_scores.py, test_null_calibration.py | Scaffold storico, escluso dall'accettazione v31. Selettore/slices/inferenza RITIRATI; CTW, quattro score e core label-free da SOSTITUIRE con T09–T23 |

Le quattro fixture CTW depositate sono identificate, non eseguite in V0–V1.
I 17 skip storici restano visibili nella suite completa, mai conteggiati come accettazione.

## Evidenze V0–V1 concluse

- `test_v31_config.py`: deposito, proiezione campo/tipo, YAML duplicati, parametri ritirati, isolamento storico.
- `test_v31_corpus.py`: T01–T04, coordinate/ordine numerico/parti, maschere/reset/target, A/B diagnostiche e corruzioni semantiche.
- `test_v31_persistence.py`: integrità dei tre input, snapshot, identità, round-trip, collisioni/concorrenza, interruzione, corruzione e schema del manifest.
- `test_v31_docs.py`: autorità attiva, digest del deposito e delle dieci copie storiche, assenza di import inferenziali/candidates nella pipeline.
- `test_v31_enforcement.py` e `test_gate_inventory_anchor.py`: inventario nominale confrontato con la raccolta effettiva, assert eseguiti, rifiuto di skip/xfail/test vuoti e ancore assenti.

Accettazione sul codice V1 `7afdd3a`: **88 passed, zero skip**. Suite completa: **411 passed, 17 skipped storici**.
Le parti PENDING della tabella restano tali; V0–V1 non promuove T05–T30 integralmente a completati.

## Evidenze V2 — nucleo CTW (T10–T16)

- `test_v31_context_tree.py`: oracolo di enumerazione indipendente, partizione BOS, normalizzazione e
  input del core, identità prequenziale, modello congelato, numerica dei due pesi, batteria §12.1.
- Batteria eseguita da `hexis.pipeline.run_tree_validation`: 25 piccoli sintetici tutti entro le soglie
  della tabella §12.1 (**`iid` m=4 alla soglia 0,02 del piano, non allo 0,03 dello script storico**) e
  nove casi di stress m106 con deficit registrato, senza criterio di superamento dell'oracle.
- Suite completa dopo T10–T16: **456 passed, 17 skipped storici**. A quel punto T05–T09 e T17–T30 restavano PENDING.

## Evidenze V2 — campionamento, RNG e shuffle (T05–T09, T17, T18)

- `test_v31_sampling.py`: derivatore §5.3 reimplementato in modo indipendente nel test (solo `hashlib`/`json`)
  e confrontato col vettore §12.2 — chiavi `held`/`fixture`, seme derivato, `permutation(6)`, ledger
  `@1[0,5) @5[0,7) @4[0,2) @2[3,6)` e sottoseme `fragment` di `@2`; i **sette `block_key` depositati**
  ricalcolati dai rispettivi membri.
- Esclusione verificata sul corpus reale per **sei celle × sette fold**: mai un documento del blocco
  held-out, mai un `inventory_only` (neppure se elencato fra i membri), sempre sei contributori da q
  esatto. Plutarco contribuente in C0 usa tutti i suoi 8.884 token in 499 frasi senza alcun frammento.
- Riuso dichiarato (`hexis_v3.1_design.json.sampling`): `a_total1`/`D12`/`upos` riproducono il ledger C0
  **byte per byte**; `q_half` e `oth` ne riusano solo l'ordine delle frasi e ricalcolano arresto e taglio.
- Il campionatore legge `role` e le coordinate sorgente: regime, gruppo e `dependence_block` possono
  essere rimossi o falsificati senza cambiare il ledger, e l'ordine dei record è indifferente.
- T18 è chiuso al livello del campione (multinsieme identico, dipendenze locali diverse; pool eterogeneo
  che resta non i.i.d. dopo il rimescolamento). Il confronto in G/Q sugli stessi controesempi resta a T19.
- Ordine canonico e supporto del taglio ripinnati contro una trascrizione indipendente di §5.2 nel test
  (l'identità della frase non è la chiave: `@10` precede `@2` in ordine lessicografico) e contro la
  copertura completa degli offset ammessi; il ledger regge il round-trip parquet dell'artefatto V1.
- Suite completa dopo T05–T09/T17–T18: **486 passed, 17 skipped storici**.
