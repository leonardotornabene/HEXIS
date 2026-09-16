# Handoff HEXIS 3.1 — V3-001 — tranche V0–V1 conclusa

**V0–V1 completati; V2–V5 non attestati; nessun nuovo fit reale.** Stato verificato il 16 settembre 2026. Ramo locale: `codex/hexis31-v0-v1`.

## Revisioni e autorità

- Base verificata: `852644b6917790877c7b2ca5df2e76b17829d87c`.
- V0, deposito e migrazione normativa: `e98fb8edde91e821c415e26f33b7bdeb549b50ba`.
- V1, corpus e persistenza: `7afdd3a4f87341110b0f15a77179febe9075ee9b`.
- L'aggiornamento finale di questo handoff è documentale; il manifest identifica il commit produttore sopra, senza autoriferimenti.

Autorità: [specifica attiva](01_MASTER_SPEC.md), [V3-001](02_DECISION_LOG.md) e piano/JSON byte-identificati in `contracts/hexis-3.1/`. Il [record esterno del deposito](V3-001-deposit.json) conserva i digest; nessun byte normativo o atteso è stato aggiornato per far passare i controlli. Verificati 8 digest della consegna, 14 verdetto/evidenze, 33 file del pacchetto storico, 103 dell'archivio interno e le quattro fixture CTW. Le fixture non sono state eseguite come programmi storici.

Le dieci copie v2.1 sono confrontate con gli originali tramite [inventario SHA-256](history/v2.1/SHA256SUMS.json). D01–D54, D55 proposto, ratifiche tecniche G1, proposal e materiali precedenti conservano il loro stato storico. Le fonti/limitazioni delle autorizzazioni pregresse restano in V3-001 e nel §2 del piano; nessun G2 retroattivo.

## Comandi e risultati effettivamente eseguiti

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

## Esecuzioni reali e identità

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

## Obblighi residui

L'[inventario T01–T30](TEST_INVENTORY.md) distingue copertura completa V1 e parti ancora PENDING. V2 deve implementare CTW, sampling/RNG/shuffle, core comportamentalmente indipendente dalle etichette, quattro perdite, diagnostiche, R1 e resume, con fixture esatte e 25 sintetici alle soglie congelate. V3 resta la prova reale tecnica dopo V0–V2: 42 coppie/84 modelli. V4 resta la campagna 490 coppie/980 identità. V5 resta ricostruzione, rigenerazione prefissata, due pesature e cinque figure. Nessuno di questi risultati è anticipato dai conteggi V1.

Riscrittura del proposal e pubblicazione sono attività separate. Il vecchio [handoff v2.1](history/v2.1/HANDOFF.md) è conservato integralmente.
