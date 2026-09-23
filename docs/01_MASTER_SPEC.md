# HEXIS 3.1 — specifica attiva

**V3-001, adottata il 16 settembre 2026; V3-002, riallineamento della repository, 22 settembre 2026.** L'autorità scientifica e operativa completa è il [piano depositato](contracts/hexis-3.1/HEXIS_piano_definitivo_v3.1_2026-09-15.md) e i quattro JSON identificati dal suo `design_lock.json`. Il testo governa la semantica, i JSON fissano valori ed elenchi. Non esistono parametri alternativi applicativi: ogni campo della proiezione YAML è confrontato con il deposito.

Studio descrittivo dell'ordine entro frase delle annotazioni nel corpus finito greco UD Perseus r2.18. Inventario di 17 documenti, 11 primari in sette blocchi e sei `inventory_only`. Rappresentazioni accorpate ADV/PART; CTW congelato implementato e verificato in V2; profili Q/G/quattro CE, due pesature e R1 secondo il contratto.

**V0–V2 completati; V3–V5 non attestati; nessun fit reale.** Le proprietà verificate su fixture sintetiche e analitiche conservano il loro credito; l'attestazione V2 di `0dc69b5` resta prova di quel commit ed è riattestata sul commit del riallineamento ([handoff](HANDOFF.md)). Arresto per revisione prima di V3. I fit iniziano soltanto in V3 dopo V0–V2. Il completamento del corpus è distinto dal completamento scientifico.

L'albero attivo contiene soltanto il percorso 3.1. Tutto il resto — v2.1, G0/G1, `candidates/`, utility statistiche, proposal precedente, risultati pre-audit — è conservato byte per byte in `archive/`, al percorso che aveva a `5f1ec06`, come storia con stato dichiarato in [V3-002](02_DECISION_LOG.md) e senza autorità sulle nuove esecuzioni. Nessuna apertura storica è dichiarata risolta.

Una divergenza scientifica arresta il passaggio interessato: richiede una correzione esplicita del contratto, mai l'aggiornamento degli attesi per ottenere un test verde.
