# Roadmap HEXIS 3.1 — V3-001

Il [contratto depositato](contracts/hexis-3.1/HEXIS_piano_definitivo_v3.1_2026-09-15.md) §14 definisce la checklist ordinata.

| Fase | Contenuto | Stato della tranche |
|---|---|---|
| V0 | Deposito, autorità, configurazione, registro e test | COMPLETATO — e98fb8e |
| V1 | Corpus, mapping, audit, coordinate e persistenza | COMPLETATO — 7afdd3a |
| V2 | CTW, RNG/campione/shuffle, quattro perdite, diagnostiche, R1, resume | COMPLETATO — chiusura verificata il 22/09/2026, codice 0a6f644; evidenze nell'handoff |
| V3 | Seme 0, sei celle, sette fold: 42 coppie/84 modelli; freeze | PENDING — prima vanno implementate le cinque figure §11.6 |
| V4 | 490 coppie/980 modelli; tutte le celle/semi/bracci | PENDING |
| V5 | Report, cinque figure, due pesi, rigenerazione e completezza | PENDING |

Chiusura V2 (codice `0a6f644`): **328 test v31 senza skip; 649 passed e 17 skip storici nella
suite completa**, lock invariato. Evidenze V2/V3 nel manifest, controllo tecnico 42/84, tabelle
del report e confronto di rigenerazione verificati soltanto su fixture. L'identità del codice
comprende tutto `src/hexis`: le cinque figure §11.6 vanno implementate prima del freeze di V3.
**Arresto per revisione prima di V3**; V3 resta non eseguito. Storico della ripresa (`d38b5a7`):
240 test v31; 561 passed e 17 skip.

Nessun nuovo fit reale prima di V3 dopo V0–V2. Completamento corpus distinto da scientifico. Pubblicazione e proposal sono attività separate. [Bibliografia attiva](BIBLIOGRAPHY.md); [roadmap e registro storici](history/v2.1/03_ROADMAP_OPERATIVA_IT.md).
