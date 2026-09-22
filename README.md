# HEXIS 3.1

Studio descrittivo dell'ordine entro frase delle annotazioni morfosintattiche nel corpus finito greco UD Perseus r2.18. La decisione [V3-001](docs/02_DECISION_LOG.md) adotta il [contratto completo](docs/01_MASTER_SPEC.md).

V0–V1 completati e verificati: deposito normativo, configurazione rigorosa, audit e codifica reali. I nove artefatti sono stati riprodotti identici byte per byte in due directory distinte. V2 chiusa e verificata il 22 settembre 2026, dopo la riconciliazione M1–M5 e la revisione integrale ([handoff](docs/HANDOFF.md)). Evidenze su fixture sintetiche/analitiche: CTW, campionamento/shuffle, punteggi, diagnostiche, R1, persistenza scientifica e tabelle del report. Anche le cinque figure del §11.6 sono implementate e verificate su fixture (`559dc40`): l'identità del codice comprende tutto `src/hexis`, quindi tutto il codice è scritto prima di V3. La revisione integrale pre-V3 del 22 settembre 2026 ha reso il validatore del report capace di rigenerare campioni e rimescolamenti senza fit, corretto le figure alla cardinalità reale e reso esaustivo l'inventario dei test (`0dc69b5`, [handoff](docs/HANDOFF.md)). Fit reali, campagna, report e figure appartengono a **V3–V5**, non attestati. Nessun risultato finale e nessun nuovo fit reale in questa tranche.

Comandi operativi, dalla radice della repository (la destinazione iniziale deve essere nuova):

```bash
uv sync --frozen
uv run python -m hexis.pipeline.run_audit --config config/default.yaml --data-root data/raw/UD_Ancient_Greek-Perseus --output-dir results/hexis31/new-run
uv run python -m hexis.pipeline.run_encode --config config/default.yaml --data-root data/raw/UD_Ancient_Greek-Perseus --output-dir results/hexis31/new-run
```

`run_encode` può anche creare direttamente un nuovo run, includendo l'audit. Un secondo avvio dello stesso stadio è rifiutato. Il manifest del corpus distingue `corpus_complete` da `scientific_complete`; lo stadio descrittivo ha un proprio run con un solo manifest, partizioni per coppia e ledger identificati dall'hash. La ripresa è verificata su fixture sintetiche, anche dopo un'interruzione fra coppie.

La batteria sintetica è eseguibile con `uv run python -m hexis.pipeline.run_tree_validation --config config/default.yaml`. Le CLI descrittive accettano la configurazione depositata; `--fixture` serve soltanto alle configurazioni giocattolo. La selezione `--seed 0` è implementata per la futura prova V3, ma **questa tranche si ferma per revisione prima di V3**. La pubblicazione delle evidenze V0–V2 in un nuovo run scientifico (`run_tree_validation --corpus-dir … --output-dir …`) è implementata e verificata su fixture; sulla configurazione depositata si esegue all'apertura di V3, a codice congelato. Il report reale esige nel manifest le evidenze V2 e V3, ricalcolate a ogni lettura, e la rigenerazione del seme 0 in una directory distinta (`--regenerated-dir`, §12.2).

Python 3.12 via uv, dipendenze e lock conservati. `uv run pytest -m v31` seleziona l'accettazione attiva; `uv run pytest` comprende anche la suite storica e i suoi scaffold esplicitamente pendenti. Stato attestato sul codice `0dc69b5` (chiusura V2, figure e revisione pre-V3): **351 test attivi senza skip; 672 passed e 17 skip storici nella suite completa**. Gli skip storici non attestano il nuovo software. [Inventario test](docs/TEST_INVENTORY.md), [roadmap](docs/03_ROADMAP_OPERATIVA_IT.md), [handoff](docs/HANDOFF.md).

Il corpus include 17 documenti censiti: 11 primari in sette blocchi, sei solo inventario. Alfabeto accorpato ADV/PART, varianti 100/105/11. Target con almeno quattro predecessori nella frase; regimi sorgente separati dal gruppo del report.

La v2.1, il proposal PDF e i README di backup sono storici. La riscrittura del proposal e la pubblicazione dei dati sono separate. Le utility statistiche conservate non entrano nella pipeline descrittiva. Lo script locale di acquisizione non è uno strumento canonico.

Codice MIT; i raw restano CC BY-NC-SA 2.5; la qualificazione giuridica dei derivati non è decisa in questa tranche (§17.3) e nessun dato viene pubblicato. Raw immutabili/ignorati e risultati locali voluminosi esclusi dalla pubblicazione. Non redistribuire i treebank tramite questo repository. [Bibliografia attiva](docs/BIBLIOGRAPHY.md).
