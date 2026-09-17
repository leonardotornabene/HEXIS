# HEXIS 3.1

Studio descrittivo dell'ordine entro frase delle annotazioni morfosintattiche nel corpus finito greco UD Perseus r2.18. La decisione [V3-001](docs/02_DECISION_LOG.md) adotta il [contratto completo](docs/01_MASTER_SPEC.md).

V0–V1 completati e verificati: deposito normativo, configurazione rigorosa, audit e codifica reali. I nove artefatti sono stati riprodotti identici byte per byte in due directory distinte. V2 completato e attestato su fixture sintetiche/analitiche: CTW, campionamento/shuffle, punteggi, diagnostiche, R1 e persistenza scientifica. Fit reali, campagna, report e figure appartengono a **V3–V5**, non attestati. Nessun risultato finale e nessun nuovo fit reale in questa tranche.

Comandi operativi, dalla radice della repository (la destinazione iniziale deve essere nuova):

```bash
uv run python -m hexis.pipeline.run_audit --config config/default.yaml --data-root data/raw/UD_Ancient_Greek-Perseus --output-dir results/hexis31/new-run
uv run python -m hexis.pipeline.run_encode --config config/default.yaml --data-root data/raw/UD_Ancient_Greek-Perseus --output-dir results/hexis31/new-run
```

`run_encode` può anche creare direttamente un nuovo run, includendo l'audit. Un secondo avvio dello stesso stadio è rifiutato. Il manifest del corpus distingue `corpus_complete` da `scientific_complete`; lo stadio descrittivo ha un proprio run con un solo manifest, partizioni per coppia e ledger identificati dall'hash. La ripresa è verificata su fixture sintetiche, anche dopo un'interruzione fra coppie.

La batteria sintetica è eseguibile con `uv run python -m hexis.pipeline.run_tree_validation --config config/default.yaml`. Le CLI descrittive accettano la configurazione depositata; `--fixture` serve soltanto alle configurazioni giocattolo. La selezione `--seed 0` è implementata per la futura prova V3, ma **questa tranche si ferma per revisione prima di V3**. Il report reale richiederà nel manifest anche le evidenze di accettazione V2 e integrazione V3.

Python 3.12 via uv, dipendenze e lock conservati. `uv run pytest -m v31` seleziona l'accettazione attiva; `uv run pytest` comprende anche la suite storica e i suoi scaffold esplicitamente pendenti. Risultati verificati: **240 test attivi senza skip; 561 passed e 17 skip storici nella suite completa**. Gli skip storici non attestano il nuovo software. [Inventario test](docs/TEST_INVENTORY.md), [roadmap](docs/03_ROADMAP_OPERATIVA_IT.md), [handoff](docs/HANDOFF.md).

Il corpus include 17 documenti censiti: 11 primari in sette blocchi, sei solo inventario. Alfabeto accorpato ADV/PART, varianti 100/105/11. Target con almeno quattro predecessori nella frase; regimi sorgente separati dal gruppo del report.

La v2.1, il proposal PDF e i README di backup sono storici. La riscrittura del proposal e la pubblicazione dei dati sono separate. Le utility statistiche conservate non entrano nella pipeline descrittiva. Lo script locale di acquisizione non è uno strumento canonico.

Codice MIT; i raw e i derivati del corpus mantengono CC BY-NC-SA 2.5. Raw immutabili/ignorati e risultati locali voluminosi esclusi dalla pubblicazione. Non redistribuire i treebank tramite questo repository. [Bibliografia attiva](docs/BIBLIOGRAPHY.md).
