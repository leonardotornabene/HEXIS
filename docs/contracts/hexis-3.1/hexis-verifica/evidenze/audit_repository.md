# HEXIS — audit del repository e migrazione proposta

**Verifica del 15 settembre 2026.** Repository `/Users/leonardoTornabene/Projects/hexis`. Audit senza modifiche ai file tracciati, installazioni, acquisizioni o fit reali. Nessun import da `candidates/`. Lo script non tracciato è stato soltanto letto. Il pacchetto operativo è stato estratto sotto `/private/tmp/hexis_repo_audit_package/HEXIS_v3_allegati`.

## 1. Evidenza effettiva

| Controllo eseguito | Risultato |
|---|---|
| Cronologia locale e riferimento del pacchetto | HEAD osservato `852644b`, ramo `g1/pre-audit`; riferimento integrale del piano `852644b6917790877c7b2ca5df2e76b17829d87c` |
| Stato prima e dopo i controlli | `?? scripts/`; nessuna differenza tracciata. Il repository non è globalmente pulito |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -p no:cacheprovider -q` | **327 passed, 17 skipped in 10.34s**, exit 0 |
| Runtime effettivo | Python **3.12.13**, NumPy **2.5.1**, pandas 3.0.3, pyarrow 25.0.0, conllu 6.0.0, scipy 1.18.0, matplotlib 3.11.0, PyYAML 6.0.3, pytest 9.1.1 |
| Lock | 23 pacchetti; le otto versioni precedenti coincidono con `uv.lock`; SHA-256 `33db43b00bcb21ab12aedf6dcc4257764770bff0115dc0d1dfab6e5ea89876bf` |
| Allegati operativi | Tutti i **33 hash** in `SHA256SUMS.json` coincidono; piano Desktop e copia inclusa sono byte-identici |
| Risultati tracciati | Due manifest di pre-audit, **7 artefatti complessivi**; tutti e sette gli hash verificati coincidono |
| CI | Nessun file di workflow `.github/` tracciato; i test verificati sono locali |

L'output completo della suite è stato osservato nel tool, non salvato preventivamente in un file log. La riga sopra è la sua trascrizione, non un nuovo log di esecuzione. Non è stata rieseguita la suite per fabbricare un allegato. Il `conftest.py` esistente elimina cache compilate dei test; nessun file tracciato risulta cambiato.

I 17 skip sono scaffold senza asserzioni operative: 8 in `tests/test_context_tree.py`, 3 in `tests/test_scores.py`, 3 in `tests/test_tree_slices.py`, 3 in `tests/test_null_calibration.py`. La firma label-free viene controllata, ma il test comportamentale d'invarianza dei punteggi è ancora uno skip (`tests/test_scores.py:18`, `:57`). Verde non significa CTW o pipeline scientifica disponibili.

## 2. Autorità e stato dei gate

Il repository continua a essere v2.1: `AGENTS.md:8`, `docs/02_DECISION_LOG.md:3`, `config/default.yaml:16`. `docs/g1_ratification_record.md:3–14` ratifica esclusivamente le voci tecniche 17–20 e 23–26, senza decidere corpus, registro, alfabeto o T*. G1 rimane aperto (`docs/HANDOFF.md:151–156`), G2 non è stato superato e O7 non è risolto.

I manifest storici dichiarano correttamente `mode: preaudit`, `status: PROVISIONAL`, codice `fb53084b6d6a12a76639aeab098b81dd7368063c`, `dirty: false`; non sono attestazioni di v3 o di un freeze scientifico. `docs/HANDOFF.md:181–213` distingue l'attestazione a `d024cd5` dai run prodotti a `fb53084`.

Il JSON allegato resta `FINAL_PLAN_NOT_APPLIED`. Il lock documentale dice `READY_FOR_V0_DEPOSIT_NOT_A_GATE_CERTIFICATE`, con deposito V0 nullo. Una revisione ridotta deve quindi produrre un nuovo contratto prima dell'implementazione; non può presentarsi come manutenzione già autorizzata dei valori v2.1. Ritirare O7 dalla nuova analisi significa renderlo inapplicabile, non risolverlo retroattivamente. L'eccezione ai pilot precedenti è una dichiarazione nel pacchetto: non ho verificato indipendentemente il consenso originale.

## 3. Differenze tecniche che il riuso deve rispettare

1. **Configurazione.** `config.py:106–156` verifica chiavi ignote e mancanti; `:159–221` valida alcuni tipi usati da G1. Quindi chiamarla soltanto un controllo di presenza è impreciso. Resta insufficiente per il modello: il controllo eseguito ha accettato `d_max=True`, `d_max=-1`, `beta=NaN`, `k_min=-1`, `select='bogus'`. `config_hash` (`:224–227`) produce anche un hash di JSON contenente NaN. La nuova validazione deve rifiutare valori non finiti e tipi/intervalli errati prima di identificare il run.
2. **Semi.** `config.py:230–232` usa XOR/CRC32; il contratto allegato usa `hexis-v3-rng-1` e identità/scopi distinti. Non sono intercambiabili.
3. **Mapping.** `alphabet.py:80–99` elimina un UPOS sconosciuto; verificato con `NOTATAG`. È il contratto v2 dichiarato, non un nuovo bug del lettore: `conllu_reader.py:100` già rifiuta tag non UD. La nuova API pubblica deve rifiutarli anche al confine del mapper.
4. **Alfabeto.** `alphabet.py:171–196` assegna ID per frequenza decrescente, mentre v3 prescrive ordinamento lessicografico. `freeze_alphabet` (`:199–215`) è realmente non implementato. Una rappresentazione modificata richiede nuovi inventari/hash/conteggi, non il riuso dei numeri 106/112/12 come costanti ancora vere.
5. **Identità e coordinate.** `registry.py:12–42` ha i cinque regimi v2, non `PROSE_ALL`, `role` o `dependence_block`; valida `part_order` ma non lo trasferisce a un ordinamento operativo (`:274–293`). `run_audit.py:179–256` conserva prefisso/sent_id e un `token_ord` ricreato con `enumerate`, non tutti gli ID grezzi e gli ordinali richiesti da v3. Occorre preservare `raw_token_id`, parti, ordine sorgente e slot prima di trasformare i dati.
6. **Confini.** `sequences.py:104–198` aggiunge `#` all'alfabeto e concatena le frasi; non implementa il SEP solo contestuale/BOS del nuovo CTW. Se si elimina `bound`, ritirare questo ramo dal percorso v3; mantenere i controlli d'identità, ordine e duplicati delle sequenze.
7. **Persistenza.** `manifest.py:116–130` scrive direttamente, anche con `force`; non è una scrittura atomica con ripresa. `run_audit.py:1115–1162` ha prenotazione, controlli di collisione e rollback sui propri output, ma scrive direttamente i file (`:1122–1125`). Hash, snapshot di input e protezione dalle sovrascritture sono riutilizzabili; atomicità/resume/schema/cardinalità v3 sono lavoro nuovo.
8. **Identificazione.** `run_audit.py:1070–1087` mette anche la data nel run_id. Il contratto v3 esclude data/macchina/percorso dall'identità scientifica e aggiunge lock, dati, registro e alfabeti. `manifest.py:71–113` non ha ancora quel contratto né stati per partizione.
9. **README.** `README.md:178–184` chiama ancora l'audit G1 una firma senza corpo: è falso rispetto a `run_audit.py`. Il README va rifatto solo dopo aver deciso il nuovo perimetro, distinguendo strumenti funzionanti, risultati di sviluppo e risultati finali.

## 4. Mappa completa del percorso applicativo

| File o gruppo | Azione futura minima |
|---|---|
| `src/hexis/conllu_reader.py` | Riutilizzare parsing e validazioni; preservare le coordinate richieste nel successivo strato |
| `src/hexis/registry.py` | Riutilizzare identità/merge/errori; aggiornare schema, ruoli e blocchi; consumare realmente `part_order` |
| `src/hexis/alphabet.py` | Riutilizzare mapping/audit con le correzioni dichiarate; implementare freeze e nuovo ordine degli ID |
| `src/hexis/sequences.py` | Riutilizzare controlli d'ordine/duplicazione e reset; aggiungere coordinate; ritirare il vecchio `#` |
| `src/hexis/config.py` | Conservare lettore YAML con rifiuto duplicati e hash; schema unico v3 rigoroso, nuovo derivatore dei semi |
| `src/hexis/manifest.py` | Estendere solo per contratto identificato, scrittura atomica, verifica contenuti/chiavi e ripresa |
| `src/hexis/pipeline/run_audit.py` | Riutilizzare lettura, snapshot/hash, censimento e controlli; rimuovere la vecchia macchina scientifica di ratifica, T* e doppia lingua |
| `src/hexis/model/context_tree.py` | Sostituire dataclass/API v2 e tutti gli stub con CTW; non esiste una vecchia implementazione canonica da rifattorizzare |
| `src/hexis/model/diagnostics.py` | Implementare diagnostiche prescritte; oggi è solo docstring |
| `src/hexis/protocols/sampling.py` | Implementare; oggi è solo docstring |
| `src/hexis/protocols/scores.py` | Sostituire gli stub P1/P2/curve con perdite, G, Q e aggregazione dichiarata, mantenendo il core label-free |
| `src/hexis/viz/plots.py` | Implementare solo figure ancora richieste; oggi è solo docstring |
| `run_encode.py`, `run_tree_validation.py`, `run_sensitivity.py` | Implementare; oggi tutti stub |
| Nuovi `run_descriptive.py`, `run_report.py` | Orchestrazione delle coppie e unico reporter; non occorre un framework o un servizio |
| `run_confirmatory.py`, `run_null_calibration.py`, `run_reference.py`, `run_latin.py` | Ritirare dall'albero applicativo/CLI; sono stub. Traccia storica in Git, senza mantenerli come comandi apparentemente utilizzabili |
| `src/hexis/model/lexicon.py`, `src/hexis/blocks.py` | Ritirare dal percorso scientifico; il primo è solo docstring, il secondo è codice funzionante per chunk, non blocchi di dipendenza |
| `src/hexis/stats/{permutation,bootstrap,holm}.py` | Conservare utility funzionanti e test validi come storico; nessun import nel percorso scientifico v3. Sono 94/74/44 righe, non stub |
| `src/hexis/**/__init__.py` | Conservare i file vuoti di package; niente astrazioni nuove |
| `config/default.yaml`, `config/registry_overrides.yaml` | Sostituire insieme al contratto: oggi il registro canonico contiene solo commenti |
| `tests/test_conllu_reader.py`, alphabet/registry/sequences e corrispondenti `test_g1_*` | Mantenere proprietà compatibili; sostituire esplicitamente aspettative v2 incompatibili |
| `tests/test_run_audit.py`, `tests/test_determinism.py` | Riutilizzare integrità/input/collisioni; adattare formato, identità, schema e resume |
| `tests/test_context_tree.py`, `test_tree_slices.py`, `test_scores.py` | Portare prove indipendenti e asserzioni eseguibili; ritirare solo proprietà del selettore/P1 realmente sostituite |
| `tests/test_null_calibration.py`, `tests/test_blocks.py` | Ritirare dal gate scientifico v3; nessun bisogno di implementare un'analisi abbandonata |
| `tests/test_permutation.py`, `test_bootstrap_holm.py` | Conservare con le utility, senza certificarvi v3 |
| `conftest.py`, `tests/test_g0_enforcement.py`, `test_g1_enforcement.py`, `test_gate_inventory_anchor.py`, `test_docs_consistency.py` | Ricostruire un inventario v3 compatto. Conservare no-skip e asserzioni reali; ritirare contatori, firme, tassonomie e ratifiche obsolete, con mappa esplicita della sostituzione |
| `tests/conftest.py`, `pyproject.toml`, `uv.lock` | Riutilizzare fixture/dependency stack; aggiornare descrizione e marker. Nessuna nuova dipendenza CTW o cambio di NumPy necessario |
| MASTER_SPEC, Decision Log, roadmap, indice, HANDOFF, README, AGENTS, CLAUDE | Un atto di migrazione coerente e una fonte autorevole nuova; evitare copie divergenti del disegno |
| `docs/g1_*`, `docs/implementation/`, `docs/audit/`, vecchi PDF, `README_backup.md`, `README_v1_backup.md`, proposta PDF | Conservare come storia con stato esplicito; toglierli dal percorso operativo e dai vincoli del nuovo gate |
| `candidates/` | Quarantena invariata, mai importare né raccogliere in pytest |
| `results/`, `data/raw/PROVENANCE.md`, raw ignorati | Conservare storia e provenienza; nessuna rinomina dei pre-audit/pilot in risultati finali |
| `.gitignore`, `LICENSE`, sezione licenze | Separare output di lavoro voluminosi dai risultati pubblicabili e dichiarare quali vengono distribuiti; non lasciare che la nuova directory di score finisca tutta automaticamente in Git |
| `scripts/reacquire_raw_data.sh` non tracciato | Preservare; verificare/correggere in un incarico successivo prima dell'eventuale adozione |

## 5. Script di acquisizione: lettura statica, nessuna esecuzione

Lo script di 76 righe non è incluso nello snapshot Git. Non può essere qualificato come artefatto attestato al commit di riferimento.

- `:73–74` acquisisce sempre greco **e latino**: il secondo download non serve al nuovo scope.
- `:42–47` salta il checkout se la directory esiste; non verifica il commit HEAD in quel caso. Gli hash validano il contenuto controllato, non attestano HEAD.
- `:52–66` itera sui file presenti: non confronta l'insieme dei file attesi con quelli trovati. Se manca uno dei tre file greci e gli altri coincidono, quel file mancante non viene verificato.
- `:31`, `:40` estraggono valori da testo Markdown con espressioni regolari e non validano esplicitamente unicità/formato del record estratto.
- `:54–58` contiene una gestione dei file senza hash apparentemente basata su `SKIP`, ma con `set -euo pipefail` la ricerca `grep` fallita può terminare già l'assegnazione `expected=...`. Non descriverlo come un rifiuto progettato e testato con errore preciso.

Riuso eventuale: solo greco, insieme dei tre nomi attesi esatto, hash precisi, errore su mancante/extra/record ambiguo; nessuna modifica automatica a un clone preesistente. Preferibile riusare le primitive di verifica di provenienza già presenti, senza creare un secondo sistema di verità. Nessuna di queste modifiche è stata eseguita.

## 6. Riduzione di output e governance consigliata

**C0 dettagliato, sensibilità aggregate è una riduzione sensata**, purché il nuovo contratto dichiari la minore granularità dell'audit. Senza probe, C0 contiene 2.182.160 righe accoppiate con i conteggi originali; circa 158 MiB sono il solo payload teorico a 76 byte/riga, non disco/RAM misurati. I numeri vanno ricalcolati se cambia la rappresentazione o la ritenzione.

Per ogni sensibilità conservare almeno identità complete della coppia, hash di modello/ledger, numero target e quattro somme delle perdite per documento e fascia di storia, più aggregati sufficienti a ricostruire esattamente le diagnostiche ancora richieste. Per la profondità condizionale non basta una media generica: conservare i suoi numeratori e denominatori. Conteggi grezzi R1, distribuzioni e contributi restano necessari. Ledger, coordinate e semi consentono la rigenerazione di un fit.

Le figure e le tabelle si ricostruiscono da questi output; **non** si può sostenere di ricontrollare ogni somma delle sensibilità da perdite per posizione che non vengono più conservate. La verifica numerica di dettaglio delle sensibilità richiede rigenerazione mirata di casi prefissati. Non omettere automaticamente le perdite o i fit rimescolati sulla base del collasso osservato nel pilot: non è un'identità universale del protocollo.

Un manifest breve può contenere contratto/commit/lock/input, stato dei passi, prove eseguite, lista di file con hash/schema/cardinalità e insieme delle chiavi scientifiche. Usare lo stesso reporter per verificarli e rifiutare il risultato ufficiale incompleto. Conservare scrittura atomica, rilevamento duplicati, hash, denominatori, join degli slot, resume coerente e test d'interruzione/corruzione. Non serve un framework di certificati firmati: il piano non richiede in realtà firme crittografiche, e i certificati allegati sono semplici record.

`report_contract.py:1–3` dichiara esplicitamente che il riferimento **non** valida ancora schema dei punteggi, slot, invarianti numeriche e attestazioni della pipeline. Le circa 40 righe della funzione sono una base utile per il confronto insiemistico, non una verifica completa già integrata. Sostituire quattro oggetti-certificato con righe di evidenza nello stesso manifest non autorizza a eliminare tali controlli.

Non ottimizzerei ora il numero delle costruzioni CTW riusando alberi profondi e riponderando i prior: può essere corretto dopo prove di equivalenza, ma il risparmio di calcolo non affronta il costo dominante dell'integrazione e aggiunge stato mutabile. Prima ridurre domande/celle e output; distinguere sempre modelli scientifici valutati da ricostruzioni computazionali.

Licenze: il repository distingue codice MIT, documenti CC BY 4.0 e statistiche future CC BY-NC-SA 4.0 (`README.md:251–261`), mentre i raw sono CC BY-NC-SA 2.5 (`data/raw/PROVENANCE.md:35`). Il piano parla dei raw ma non assegna chiaramente destinazione pubblica/locale alle nuove coordinate e ai simboli per posizione. Occorre dichiararlo nella migrazione, senza dare automaticamente a tutti i file la licenza del codice. Questo rilievo riguarda coerenza del contratto e degli output, non una valutazione giuridica della derivazione.

## 7. Artefatti esistenti allegabili, senza nuove esecuzioni

- Questo rapporto: `/private/tmp/hexis_repo_audit.md`.
- Pacchetto originale: `/Users/leonardoTornabene/Desktop/HEXIS_allegati_operativi_v3_2026-09-11.zip`.
- Copia verificata: `/private/tmp/hexis_repo_audit_package/HEXIS_v3_allegati/`, in particolare `SHA256SUMS.json`, `design_lock.json`, `package_validation.json`, `contract_validation.json`, `diagnostics_validation.json`, `scores_validation.json`, `report_validation.json`, `numpy_comparison.json`, `authorization_and_experiments.json`. Sono **evidenze precedenti al presente audit**, non risultati appena riprodotti.
- Manifest storici verificati: `results/logs/audit_preaudit_53f76d297774_1096e1d24582_fb53084b6d6a_2026-09-04/manifest.json` e `results/logs/audit_preaudit_53f76d297774_cbeffa78b04e_fb53084b6d6a_2026-09-04/manifest.json`; i file corrispondenti sono in `results/tables/`.
- Test storico documentato: `docs/HANDOFF.md:181–213`; runtime e comando appena verificati sono riportati nel §1 di questo rapporto.

**Conclusione:** la base di infrastruttura è concreta e passa i propri test. Il modello e la pipeline v3 devono ancora essere integrati. Il lavoro minimo utile è un contratto ridotto e coerente, riuso selettivo delle protezioni esistenti, CTW/protocollo verificati, output dettagliati C0 e aggregati sufficienti altrove, un solo reporter con controllo completo. Nulla è stato applicato al repository.
