# HEXIS 3.1

Studio descrittivo dell'ordine entro frase delle annotazioni morfosintattiche nel corpus finito greco UD Perseus r2.18. La decisione [V3-001](docs/02_DECISION_LOG.md) adotta il [contratto completo](docs/01_MASTER_SPEC.md).

Disponibili: lettore CoNLL-U, caricamento rigoroso della configurazione e verifiche dei contratti depositati. Audit/codifica V1 in implementazione e verifica; i comandi operativi saranno attestati al termine dei test. CTW, campionamento/shuffle, score, R1 e report della campagna appartengono a **V2–V5**, non attestati. Nessun risultato finale e nessun nuovo fit reale in questa tranche.

Python 3.12 via uv, dipendenze e lock conservati. `uv run pytest -m v31` seleziona l'accettazione attiva; `uv run pytest` comprende anche la suite storica e i suoi scaffold esplicitamente pendenti. Gli skip storici non attestano il nuovo software. [Inventario test](docs/TEST_INVENTORY.md), [roadmap](docs/03_ROADMAP_OPERATIVA_IT.md), [handoff](docs/HANDOFF.md).

Il corpus include 17 documenti censiti: 11 primari in sette blocchi, sei solo inventario. Alfabeto accorpato ADV/PART, varianti 100/105/11. Target con almeno quattro predecessori nella frase; regimi sorgente separati dal gruppo del report.

La v2.1, il proposal PDF e i README di backup sono storici. La riscrittura del proposal e la pubblicazione dei dati sono separate. Le utility statistiche conservate non entrano nella pipeline descrittiva. Lo script locale di acquisizione non è uno strumento canonico.

Codice MIT; i raw e i derivati del corpus mantengono CC BY-NC-SA 2.5. Raw immutabili/ignorati e risultati locali voluminosi esclusi dalla pubblicazione. Non redistribuire i treebank tramite questo repository. [Bibliografia attiva](docs/BIBLIOGRAPHY.md).
