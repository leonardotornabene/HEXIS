# Roadmap HEXIS 3.1 — V3-001, V3-002

Il [contratto depositato](contracts/hexis-3.1/HEXIS_piano_definitivo_v3.1_2026-09-15.md) §14 definisce la checklist ordinata.

| Fase | Contenuto | Stato della tranche |
|---|---|---|
| V0 | Deposito, autorità, configurazione, registro e test | COMPLETATO — `e98fb8e` |
| V1 | Corpus, mapping, audit, coordinate e persistenza | COMPLETATO — `7afdd3a`; il corpus consegnato è `results/hexis31/v1` |
| V2 | CTW, RNG/campione/shuffle, quattro perdite, diagnostiche, R1, resume | COMPLETATO — chiusura `0a6f644`, revisione pre-V3 `0dc69b5`; riattestato dopo il riallineamento |
| — | Riallineamento della repository e atto di pubblicazione (V3-002) | COMPLETATO — code review integrale e verifica di conformità; pubblicato il 2026-09-23, merge in `master` `73df64d` |
| V3 | Seme 0, sei celle, sette fold: 42 coppie/84 modelli; freeze | PENDING — arresto per revisione prima dell'apertura |
| V4 | 490 coppie/980 modelli; tutte le celle, i semi e i bracci | PENDING |
| V5 | Report, cinque figure, due pesi, rigenerazione e completezza | PENDING — codice pronto; esecuzione e verifica |

Il riallineamento non ha cambiato né il contratto né i dati: deposito, configurazione, `uv.lock`, provenienza e raw sono invariati, e il corpus V1 è stato rigenerato identico byte per byte nei suoi nove artefatti. Ha invece riaperto il congelamento pre-V3 dichiarato il 22 settembre, prima che qualunque evidenza V2 o V3 fosse pubblicata.

Accettazione attiva: `uv run pytest` e `uv run pytest -m v31` raccolgono gli stessi test, senza skip. Conteggi e comandi verbatim nell'[handoff](HANDOFF.md); obblighi residui e mappa dei test nell'[inventario](TEST_INVENTORY.md).

Nessun nuovo fit reale prima di V3. Completamento del corpus distinto dal completamento scientifico. Il research proposal 3.1 (§17.1) e la pubblicazione restano attività separate, la seconda regolata dall'atto in V3-002. [Bibliografia attiva](BIBLIOGRAPHY.md); registro storico in [archivio](../archive/docs/history/v2.1/03_ROADMAP_OPERATIVA_IT.md).
