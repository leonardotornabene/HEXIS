# Handoff HEXIS 3.1 — V3-001 — tranche V0–V2 conclusa

**V0–V2 completati; V3–V5 non attestati; nessun nuovo fit reale.** Stato V0–V1 verificato il 16 settembre 2026, stato V2 il 17 settembre 2026. Ramo locale: `codex/hexis31-v0-v1`.

## Revisioni e autorità

- Base verificata: `852644b6917790877c7b2ca5df2e76b17829d87c`.
- V0, deposito e migrazione normativa: `e98fb8edde91e821c415e26f33b7bdeb549b50ba`.
- V1, corpus e persistenza: `7afdd3a4f87341110b0f15a77179febe9075ee9b`.
- V0+V1, attestazione documentale: `b607cef434ffa8698cb2e4ca0387d2b759a18862`.
- V2, core e protocollo, quattro milestone chiusi in sequenza: `105c0aae26f4eb9b54267e02ee45f5449e565ac6`, `3119517da223940cc51eabaef096508c33c6ec03`, `e9c8c96e4573fb9585f4250ce38f47d5cc3a2998`, `de8ea5d576c415aa6bc082186b8ce649271a664b`.
- L'aggiornamento finale di questo handoff è documentale; il manifest identifica il commit produttore sopra, senza autoriferimenti.

Autorità: [specifica attiva](01_MASTER_SPEC.md), [V3-001](02_DECISION_LOG.md) e piano/JSON byte-identificati in `contracts/hexis-3.1/`. Il [record esterno del deposito](V3-001-deposit.json) conserva i digest; nessun byte normativo o atteso è stato aggiornato per far passare i controlli. Verificati 8 digest della consegna, 14 verdetto/evidenze, 33 file del pacchetto storico, 103 dell'archivio interno e le quattro fixture CTW. Le fixture non sono state eseguite come programmi storici.

Le dieci copie v2.1 sono confrontate con gli originali tramite [inventario SHA-256](history/v2.1/SHA256SUMS.json). D01–D54, D55 proposto, ratifiche tecniche G1, proposal e materiali precedenti conservano il loro stato storico. Le fonti/limitazioni delle autorizzazioni pregresse restano in V3-001 e nel §2 del piano; nessun G2 retroattivo.

## Comandi e risultati effettivamente eseguiti (V0–V1)

```bash
uv lock --check
uv run pytest -q
uv run pytest -q -m v31
.venv/bin/python -m hexis.pipeline.run_audit --config config/default.yaml --data-root data/raw/UD_Ancient_Greek-Perseus --output-dir results/hexis31/v1
.venv/bin/python -m hexis.pipeline.run_encode --config config/default.yaml --data-root data/raw/UD_Ancient_Greek-Perseus --output-dir results/hexis31/v1
.venv/bin/python -m hexis.pipeline.run_encode --config config/default.yaml --data-root data/raw/UD_Ancient_Greek-Perseus --output-dir results/hexis31/v1-reproduction
```

Tutti exit 0. L'interprete `.venv` è l'ambiente Python 3.12 gestito e sincronizzato da uv. `uv lock --check`: 23 pacchetti risolti, lock invariato. Suite completa: **411 passed, 17 skipped**, tutti scaffold storici; accettazione attiva: **88 passed, 340 deselected, zero skip**. Test nuovi scritti ed eseguiti rossi prima delle rispettive implementazioni. Una revisione indipendente di configurazione, corpus, persistenza e storia non ha rilevato problemi bloccanti.

Le verifiche includono errori localizzati di parsing, input mancanti/extra/alterati e cambiati durante il run, record riordinati e coordinate numeriche, Ateneo XII/XIII, frasi vuote sintetiche, unknown UPOS pubblico, mapping globale e sottotipi, maschere C0/UPOS, inventari esclusivi, denominatori A/B, assert eseguiti e raccolta nominale, round-trip, corruzioni a cardinalità invariata, collisioni e scritture interrotte. Atomicità mediante temporanei nella destinazione e pubblicazione esclusiva con hard link; manifest sostituito atomicamente per ultimo. Questa scelta tecnica impedisce overwrite anche in una collisione fra controllo e pubblicazione.

## Esecuzioni reali e identità (V1)

Identità comune: `a04db5ca9bdfec4e9444fc01745c7210862eaebe5654bb8046b545bfbe154d42`.

- [Manifest principale](../results/hexis31/v1/manifest.json), SHA-256 `154433c772f41e444f86b8787e0ee0003c546d9fb398b6ee0f634ce193f3421f`.
- [Manifest di riproduzione](../results/hexis31/v1-reproduction/manifest.json), SHA-256 `de08d13de608b33b4618b26b95359226179ad1c62c681e1104a151cca7611ef8`.
- Lock: `33db43b00bcb21ab12aedf6dcc4257764770bff0115dc0d1dfab6e5ea89876bf`.

Entrambi registrano il commit V1, il commit V0 distinto e `tracked_dirty=false` al momento dell'esecuzione. `completed_stages=[audit, encode]`, `corpus_complete=true`, `scientific_complete=false`. I manifest differiscono nei metadati esterni (directory/timestamp), esclusi dall'identità. **Tutti i nove artefatti, incluse chiavi, contenuti, schemi e cardinalità, sono identici byte per byte nelle due directory.** `validate_run` ha riletto e verificato entrambe le esecuzioni; confronto aggiuntivo dei byte di ciascun file superato.

| Artefatto | Cardinalità (righe o membri JSON) |
|---|---:|
| `alphabets.json` | 3 |
| `audit_A.csv` | 29 |
| `audit_contingency.csv` | 2075 |
| `audit_summary.csv` | 84 |
| `coordinates.parquet` | 530720 |
| `documents.csv` | 51 |
| `exclusions.parquet` | 78247 |
| `sequences.parquet` | 41757 |
| `source_audit.json` | 9 |

Riconteggio esatto: **202.989 token sorgente, 13.919 frasi, 18 prefissi, 17 documenti**, 11 primari in sette blocchi e sei `inventory_only`. Tre alfabeti **100/105/11**, con **9/10/0** tipi esclusivi dei documenti solo inventariati. **51 documenti/variante, 41.757 frasi/variante, 530.720 coordinate trattenute**. Controlli A e B: zero segnalazioni; restano diagnostici. Tutti gli attesi documentali, di blocco e di popolazione coincidono, non soltanto i totali.

La provenienza attiva è in [data/provenance_v31.json](../data/provenance_v31.json), fuori da raw. Tre input greci e commit sorgente `37837c7a3c592c9563f8c51cc63344b87247f8a5` verificati. Raw greci/latini, provenienza storica, risultati precedenti e script locale preservati. I derivati reali sono locali/ignorati da Git; nessuna pubblicazione dei dati. `v1-development` conserva una prova tecnica precedente sotto una diversa identità, non è il run consegnato.

## Comandi e risultati effettivamente eseguiti (V2)

```bash
uv lock --check
uv run pytest -q
uv run pytest -m v31 -q
```

Rieseguiti sul codice `de8ea5d`, tutti exit 0. `uv lock --check`: 23 pacchetti risolti, lock invariato. Suite completa: **543 passed, 17 skipped**, i medesimi scaffold storici di V0–V1. Accettazione attiva: **220 passed, 340 deselected, zero skip**. Il criterio §14 per V2 — «Test esatti/sintetici e controlli pertinenti T01–T23/T26 superati, senza skip» — è soddisfatto: l'[inventario](TEST_INVENTORY.md) porta T05–T23 e T26 a V2, e T01–T04 restano coperti da V1.

I quattro milestone sono stati scritti test-first e revisionati singolarmente: nucleo CTW, numerica dei due pesi e batteria §12.1 congelata (T10–T16); campionamento, identità RNG contro il vettore §12.2 e controllo d'ordine accoppiato (T05–T09, T17, T18); quattro perdite, aggregazioni nelle due pesature, diagnostiche e R1 (T19–T23); persistenza scientifica, manifest `hexis-scientific-manifest-1`, CLI, ripresa e i ritiri §13.2 (T26). Le evidenze per ID sono nell'inventario, non duplicate qui.

## Ripresa dopo interruzione — 2026-09-17

La ripresa parte da `feb23af`: i milestone e la prima attestazione V2 erano già
committati, con il solo `scripts/reacquire_raw_data.sh` non tracciato. La verifica
iniziale ha riprodotto **220 passed, 340 deselected**, senza skip. Il lavoro
esistente è stato conservato; sono stati completati i collegamenti rimasti nel
percorso V2, con test rossi osservati prima delle modifiche:

- API pubbliche `pooled_score_core` e `annotate_scores` operative, senza nuova
  formula di scoring; le etichette si aggiungono agli score fissati.
- Selezione `--seed 0` senza alterare configurazione o identità, pubblicazione
  dopo ciascuna coppia e ripresa effettiva dopo un'interruzione fra coppie.
- Ledger completi `sample_ledger__<sha256>.json`, condivisi dalle coppie che
  riusano il campione, con riferimenti/hash/cardinalità verificati in lettura.
- Verifica degli insiemi di slot anche nelle sensibilità prima di scartare i
  vettori; configurazione della batteria sintetica validata e output atomico,
  protetto da collisioni e destinazioni raw anche via symlink.
- I record V0/V1 da soli non consentono più l'emissione di un report reale;
  le evidenze V2/V3 saranno collegate nell'integrazione, non simulate qui.

Comandi eseguiti e righe finali verbatim, tutti exit 0:

```text
uv run pytest -q
561 passed, 17 skipped in 87.22s (0:01:27)

uv run pytest -m v31 -q
240 passed, 338 deselected in 79.63s (0:01:19)

uv lock --check
Resolved 23 packages in 4ms
```

I 20 test attivi in più comprendono 18 nuovi casi e i due controlli di firma
già esistenti, ora inclusi anche in v31; i 17 skip restano tutti storici.
I confronti indipendenti delle fixture verificano identità e artefatti byte per
byte sia tra due destinazioni sia tra esecuzione ripresa ed esecuzione nuova;
il fingerprint originale è inoltre rigenerato dal ledger riletto da disco.
La batteria completa mantiene i 25 sintetici e i nove stress m106 alle soglie
depositate. Nessun atteso numerico è stato rigenerato.

Piano, quattro JSON e `design_lock.json`: **sei confronti byte per byte col
Desktop superati**. `uv.lock` resta
`33db43b00bcb21ab12aedf6dcc4257764770bff0115dc0d1dfab6e5ea89876bf`.
Sotto `results/hexis31` restano i soli manifest `v1`, `v1-reproduction` e
`v1-development`. Nessun nuovo fit reale, nessuna pubblicazione, script locale
e materiali storici preservati. Arresto per la revisione successiva prima di V3.

## V2 non produce esecuzioni reali

V2 non ha una sezione di esecuzioni reali e identità, e non per omissione: per disegno non esegue campagne e non pubblica artefatti scientifici. `results/hexis31/` contiene ancora soltanto le directory V1 già attestate; nessun manifest scientifico reale esiste. Il piano §14 fissa il confine: «I nuovi fit reali iniziano soltanto nella prova integrata, dopo V0–V2 nel nuovo percorso autorizzato». Il criterio di completamento di V2 è quindi la copertura di test, non un run.

CTW, quattro punteggi, diagnostiche, R1 e persistenza scientifica sono verificati su fixture interamente sintetiche o analitiche: alfabeti giocattolo m=2…5, frasi giocattolo, tre e sette blocchi, tre documenti, due celle e uno o due semi. Per queste configurazioni giocattolo le due CLI esigono `--fixture` e il report registra `checks.scientific = False`. La proiezione analitica depositata è già accettata senza `--fixture`; l'opzione `--fixture` la rifiuta. La precedente frase secondo cui le CLI funzionavano soltanto su fixture era inesatta: questa ripresa corregge la documentazione, senza eseguire fit reali.

Un solo contatto col corpus reale resta in V2, ed è di campionamento, non di modello: `tests/test_v31_sampling.py` ricostruisce il corpus V1 dai tre input greci per verificare, su sei celle × sette fold, che nessun documento held-out e nessun `inventory_only` entri nel training e che il ledger sia quello dichiarato. Nessun modello vi è fittato, esattamente come nei test corpus di V1.

## Obblighi residui

L'[inventario T01–T30](TEST_INVENTORY.md) distingue la copertura V0–V2 dalle parti ancora PENDING. V2 è concluso: CTW, sampling/RNG/shuffle, core comportamentalmente indipendente dalle etichette, quattro perdite, diagnostiche, R1 e resume esistono e sono coperti, con le fixture esatte e i 25 sintetici alle soglie congelate. Restano PENDING la parte modellistica di T24 e T29, T25 in V4, T27 e T30 in V5.

V3 resta la prossima tranche e non è aperta da questo handoff: un seme (0) per tutte le sei celle, misure risorse, freeze di codice e ambiente, per **42 coppie / 84 modelli tecnici**, finiti/coerenti, zero probe e schema finale verificato. `run_descriptive --seed 0` seleziona tale sottoinsieme senza modificare la configurazione analitica o il `run_id`; la successiva esecuzione senza `--seed`, con `--resume`, completa i semi previsti.

All'apertura di V3 resta da collegare al manifest la prova dell'accettazione V2 e quella dell'integrazione V3 sotto codice/lock effettivi. L'esecutore oggi registra dai byte verificati soltanto V0/V1: il report reale ora rifiuta questi due record come evidenza sufficiente, mentre il report delle fixture resta disponibile e non scientifico. La suite V2 non attesta questa integrazione futura. V4 resta la campagna **490 coppie / 980 identità di modello**; V5 resta report, cinque figure, due pesature, ripresa e rigenerazione prefissata.

Le istruzioni `AGENTS.md`/`CLAUDE.md`/`04_AI_HANDOFF_PROMPT.md`, la specifica attiva e il marker pytest sono riallineati allo stato V0–V2. Restano distinti codice implementato, accettazione sintetica e risultati scientifici: nessuna istruzione apre V3 automaticamente. La revisione integrale è rinviata come richiesto dall'utente; questa ripresa completa collegamenti e verifiche del piano V2, non attesta una nuova revisione integrale.

Riscrittura del proposal e pubblicazione sono attività separate. Il vecchio [handoff v2.1](history/v2.1/HANDOFF.md) è conservato integralmente.
