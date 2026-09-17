# Inventario test HEXIS 3.1 — V3-001

Accettazione attiva: marker `v31`; raccolta effettiva obbligatoria, assert eseguiti,
nessuno skip/xfail/xpass. Il confronto col contratto non sostituisce i test del CTW.

| ID | Stato V0–V2 | Copertura / obbligo residuo |
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
| T18 | V2 | Controesempi di dipendenza interna e di pool eterogeneo al livello del campione e in G/Q: G_R non nullo con due modelli fittati |
| T19 | V2 | Q a quattro termini; controesempio archiviato d'inversione del segno riprodotto sul CTW canonico |
| T20 | V2 | Aggregazioni/due pesi |
| T21 | V2 | Sensibilità accoppiate |
| T22 | V2 | Masse/supporti/L_resolved |
| T23 | V2 | R1 |
| T24 | PARZIALE V1 | Censimento dei sei inventory_only; assenza training/scoring finale PENDING V5 |
| T25 | PENDING V4 | Uguaglianza 490/980 chiavi modello/coppia |
| T26 | V2 | Atomicità/interruzione, resume, corruzione, duplicati e chiavi extra: corpus (V1) e stage scientifico (V2) |
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
| test_context_tree.py, test_tree_slices.py, test_scores.py, test_null_calibration.py | Scaffold storico, escluso dall'accettazione v31. Selettore/slices/inferenza RITIRATI; CTW, quattro score e core label-free SOSTITUITI nell'attivo da T09–T23 |

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

## Evidenze V2 — punteggi e diagnostiche (T18 residuo, T19–T22)

- `test_v31_scores.py`: fixture interamente sintetiche (alfabeti m=2..5, frasi giocattolo, tre blocchi).
  **Nessun fit sul corpus greco**: il freeze dei fit reali fino a V3 vale anche per i test.
- T19: il controesempio archiviato di `diagnostics_validation.json` (Q≈0,7134571524694422, scorciatoia
  `CE_CTW_R−CE_CTW_O`≈−0,6650544707842875, differenza di radice ≈1,3785116232537296) è **riprodotto dal
  CTW canonico** entro 1e-9 bit passando per `score_streams`/`aggregate`/`ce_gain_q`: il segno della
  scorciatoia è opposto a quello di Q. Sul percorso completo §7 le quattro CE per slot coincidono con
  `CTW.evaluate` alle stesse tolleranze, e gli slot dei due bracci sono verificati uno-a-uno.
- T18 (residuo): pool eterogeneo a due dialetti fittato sui due bracci — G_R = 0,817 bit, Q = −0,216
  mentre G_O = 0,601: assumere G_R=0 sbaglierebbe anche il segno. Quota di slot cambiati 18/44 letta
  da `changed_count`/`total_count` dello shuffle, non ricalcolata.
- T20: perdite→documenti→blocchi→gruppi su lunghezze diseguali; la CE di blocco è somma/target
  (13/3), non media delle medie documentali (5,5); il totale è la somma delle due fasce disgiunte.
  Le due pesature restituiscono le quattro CE, G_O, G_R e Q, e `D_Q = D_G_O − D_G_R` è verificato
  in `contrasts` per entrambe; un blocco senza score interrompe il contrasto.
- T21: dieci semi per cella, aggregazione **per seme prima** delle cinque statistiche (SD con S−1,
  null a S=1); il join accoppiato rifiuta duplicati e insiemi di slot diversi — il caso OTH, dove la
  popolazione di target cambia, non viene allineato per lunghezza uguale.
- T22: R come somma diretta (mai `1-unseen_mass`), masse+unseen=1 entro 1e-12, L_resolved null con
  motivo `no_resolved_mass` a training vuoto e 0,0 su foglia forzata D=0; media come somma dei validi
  diviso il conteggio valido; fascia vuota con n=0, somme additive 0 e CE/G/Q null `empty_bucket`.
- Il confine pubblico attivo è `pooled_score_core` (slot accoppiati, quattro perdite,
  nessuna etichetta) più `annotate_scores` (join col registro senza alterare gli score).
  `score_streams` resta un alias della stessa implementazione. I test di firma in
  `test_scores.py` sono adeguati al vocabolario 3.1 e inclusi nell'accettazione attiva;
  gli scaffold inferenziali dello stesso file restano storici.
- Suite completa dopo T18–T22: **498 passed, 17 skipped storici**.

## Evidenze V2 — R1 (T23)

- `test_v31_r1.py`: fixture proprie (sette blocchi giocattolo, m=5), indipendenti dal resto di V2 —
  R1 non usa CTW, campione né semi (§8.3).
- Simmetria, diagonale zero, range [0,1] bit con il limite superiore **raggiunto esattamente** su
  distribuzioni disgiunte (`0 log 0 = 0` senza NaN), zero esatto su distribuzioni coincidenti e somma
  dei contributi per simbolo uguale alla JSD entro 1e-15.
- `block_counts` conta **tutti** i token trattenuti della variante, anche i primi quattro slot non
  eleggibili; `r_b=(n+0,5)/(N+0,5m)` confrontato elemento per elemento, con massa positiva anche per
  un simbolo mai osservato nel blocco.
- Matrice 7×7 e 21 coppie coerenti fra loro; centroidi come media uniforme dei blocchi del gruppo e
  **una sola JSD dei centroidi**, numericamente distinta dalla media delle JSD di coppia
  (0,19507 contro 0,19689 sulla fixture).
- Suite completa dopo T23: **501 passed, 17 skipped storici**.

## Evidenze V2 — persistenza scientifica, manifest e ripresa (T26)

- `test_v31_descriptive.py`: campagna giocattolo (tre documenti, alfabeto m=5, due blocchi, due celle,
  un seme) pubblicata in un corpus V1 temporaneo e guidata dalle vere CLI. **Nessun fit sul corpus
  greco**: il freeze dei fit reali fino a V3 vale anche qui, e il file resta eseguibile senza `data/raw`.
- Il contratto giocattolo **non è** la proiezione analitica depositata: per esso entrambe le CLI
  esigono `--fixture` e lo rifiutano sulla configurazione depositata, e il report registra
  `checks.scientific = False`. La campagna sintetica non è leggibile come risultato.
- Manifest `hexis-scientific-manifest-1` distinto da `hexis-corpus-manifest-1`: `corpus_run` resta
  chiuso e ne sono importate senza modifiche solo le utility agnostiche al formato
  (`write_artifact`, `artifact_record`, `_read_json`, `check_destination`, `_code_identity`).
- Atomicità: scrittura in temporaneo dentro la destinazione, round-trip di ogni artefatto, hard-link
  dei soli file nuovi, `os.replace` del manifest **per ultimo**, rollback su eccezione. Un'eccezione a
  metà scrittura lascia i byte del manifest precedente intatti; un hard-link orfano sopravvissuto a un
  kill rende il run invalido e blocca la ripresa finché non è rimosso.
- Ripresa: una partizione si riusa solo con identità, byte/hash, schema, cardinalità e chiavi
  coincidenti. Rifiutate una configurazione cambiata (`run_contract.configuration`), un corpus cambiato
  (`run_contract.alphabets`) e un'identità del codice cambiata (`run_contract.code`); una ripresa senza
  lavoro residuo è un no-op, non una seconda pubblicazione; lo stage `report` chiude il run.
- Corruzione e chiavi: cinque guasti sugli artefatti (byte riscritti, parquet troncato, file assente,
  cardinalità falsificata nel manifest, `run_id` falsificato) e otto sul manifest (chiave JSON
  duplicata, valore non finito, campo ignoto, campo mancante, chiave modello duplicata, chiave modello
  extra, artefatto extra sul disco, stage ignoto) sono tutti rilevati, e nessuno di essi è riusabile
  con `--resume`.
- Determinismo: la stessa campagna in due destinazioni produce artefatti **byte per byte identici** e
  manifest uguali in tutto tranne `metadata` — timestamp, macchina, percorsi e risorse sono metadati
  esterni, fuori da `run_id` e dai semi (§11.3).
- Validatore del report (§14.2): i sei passi sono eseguiti in ordine e registrati in `checks.steps`;
  una campagna incompleta, uno scoring `inventory_only`, un'evidenza registrata sotto altro codice/lock
  e una seconda emissione sono rifiutati prima di scrivere qualunque tabella. Le fixture
  registrano V0/V1; il report reale richiede anche V2/V3. Il loro deposito nel manifest
  resta parte della futura integrazione V3, non è attestato dalla campagna giocattolo.
- Ritiri §13.2 verificati come comportamento: `run_confirmatory`, `run_null_calibration`,
  `run_reference`, `run_latin` e `run_sensitivity` dichiarano il ritiro nella docstring ed escono con
  errore esplicito; `model/lexicon.py` e `blocks.py` non sono importati dal percorso descrittivo.
- Le cinque figure del §11.6 restano fuori da V2: `viz/plots.py` non è toccato e il report non scrive
  alcuna figura (T27/T30 restano PENDING V5).
- Suite completa dopo T26: **543 passed, 17 skipped storici**.

Accettazione sul codice V2 `de8ea5d`: **220 passed, 340 deselected, zero skip**. Suite completa:
**543 passed, 17 skipped storici**; `uv lock --check` invariato su 23 pacchetti. I conteggi
intermedi delle sezioni precedenti sono istantanee prese al termine di ciascun milestone, prima
dei rispettivi commit di correzione della review; questi due conteggi descrivono la prima chiusura
V2, prima della ripresa documentata sotto. Le parti PENDING V4/V5 della tabella restano tali.

## Ripresa V2 — collegamenti e persistenza, 2026-09-17

- T19/T20/T28: API pubbliche operative `pooled_score_core` e `annotate_scores`; score e
  diagnostiche byte-identici cambiando le etichette, fingerprint congelato e join che
  rifiuta chiavi duplicate/mancanti/null e sovrascrittura dei punteggi.
- T26: pubblicazione atomica dopo ciascuna coppia. Interruzione prima del secondo fit,
  ripresa delle coppie residue e confronto con una nuova esecuzione indipendente;
  stessi artefatti byte per byte. Selezione del solo seme 0, rifiuto del report
  incompleto e completamento successivo senza cambiare `run_id` o rifittare le coppie presenti.
- T06/T26/T29: `sample_ledger__<sha256>.json` per campione distinto, referenziato dalle
  coppie e riusato senza overwrite; hash, cardinalità e riferimenti verificati anche
  durante resume. Rigenerazione sintetica del fingerprint originale dal ledger riletto.
- T21/T26: confronto degli insiemi di slot con le coordinate prima di scartare i
  vettori delle sensibilità; errori rilevati anche a cardinalità invariata.
- T15/T16/T26: `run_tree_validation --config` valida la proiezione depositata;
  output atomico, rifiuto della collisione con un altro scrittore e protezione dei
  raw anche attraverso symlink e con `--force`.
- La raccolta nominale in `test_v31_enforcement.py` include tutte queste nuove verifiche.
  Nessun test scientifico atteso, soglia, seme, dato raw o byte contrattuale modificato.
  Sono sostituiti soltanto gli attesi delle firme del protocollo v2.1, come registrato
  nella nota di esecuzione V3-001; il confine senza etichette resta obbligatorio.

Accettazione sui byte della ripresa committati in `d38b5a7`:
**240 passed, 338 deselected, zero skip**.
Suite completa: **561 passed, 17 skipped storici**. Lock invariato, 23 pacchetti.
I 20 casi attivi aggiunti comprendono 18 nuovi casi e i due test di firma
preesistenti; la revisione integrale e V3–V5 restano fuori da questa attestazione.
