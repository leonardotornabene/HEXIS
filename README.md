# HEXIS 3.1

Studio descrittivo dell'ordine entro frase delle annotazioni morfosintattiche nel corpus finito greco UD Perseus r2.18. L'autorità è il [piano depositato](docs/contracts/hexis-3.1/HEXIS_piano_definitivo_v3.1_2026-09-15.md) con i suoi JSON identificati byte per byte, adottato da [V3-001](docs/02_DECISION_LOG.md); [V3-002](docs/02_DECISION_LOG.md) ha riallineato la repository e regola la pubblicazione.

## Stato

**V0–V2 completati; V3–V5 non attestati; nessun fit reale è mai stato eseguito.** Sono implementati e verificati su fixture sintetiche e analitiche: lettore e codifica del corpus, CTW congelato, campionamento con RNG del contratto e rimescolamento, quattro perdite con G e Q, diagnostiche, R1, persistenza atomica con ripresa, tabelle del report e cinque figure. Il corpus reale è stato letto e codificato una sola volta (V1), e i suoi nove artefatti sono riproducibili byte per byte. Campagna, contrasti finali e risultati appartengono a V3–V5 e non esistono. La tranche si ferma per revisione prima di V3.

L'albero attivo contiene soltanto il percorso 3.1. La storia — v2.1, gate G0/G1, `candidates/`, utility statistiche, proposal precedente, risultati pre-audit — è conservata byte per byte in [archive/](archive/README.md), che non è un'autorità e non viene eseguito.

## Uso

```bash
uv sync --frozen
uv run pytest
uv run python -m hexis.pipeline.run_tree_validation --config config/default.yaml
uv run python -m hexis.pipeline.run_audit  --config config/default.yaml --data-root data/raw/UD_Ancient_Greek-Perseus --output-dir results/hexis31/<nuovo>
uv run python -m hexis.pipeline.run_encode --config config/default.yaml --data-root data/raw/UD_Ancient_Greek-Perseus --output-dir results/hexis31/<nuovo>
```

Il corpus non è incluso: `data/raw` è immutabile, ignorato da Git e mai ridistribuito qui. La destinazione di un run deve essere nuova; un secondo avvio dello stesso stadio è rifiutato e nessuna scrittura è implicita. `run_descriptive` e `run_report` sono implementati e verificati su fixture: sulla configurazione depositata si eseguono a partire da V3, a codice congelato.

Accettazione attiva: `uv run pytest` e `uv run pytest -m v31` raccolgono gli stessi test, tutti marcati, senza skip e con un assert eseguito ciascuno. Conteggi verbatim nell'[handoff](docs/HANDOFF.md); mappa e obblighi nell'[inventario](docs/TEST_INVENTORY.md).

## Perimetro scientifico

Diciassette documenti censiti: undici primari in sette blocchi, sei soltanto d'inventario, mai addestrati né valutati. Alfabeto con accorpamento globale ADV/PART, tre varianti di dimensione 100, 105 e 11. Target con almeno quattro predecessori nella stessa frase, nessuna storia fra frasi. Le misure sono perdite predittive fuori dal training in bit per simbolo: nessuna inferenza, nessun p-value, nessun intervallo. I semi sono repliche computazionali, non incertezza di popolazione, e gli undici documenti non sono undici repliche indipendenti.

## Licenze e dati

Tre licenze, per tre cose diverse (atto di pubblicazione in V3-002). Il **codice** — `src/`, `tests/`, configurazione e lock — è **MIT**. I **documenti dell'autore**, compresi i testi e i JSON del deposito, sono **CC BY 4.0**. Tutto ciò che **deriva dal corpus** — vettori per posizione, ledger con coordinate, aggregati — è **CC BY-NC-SA 2.5**, come la fonte, con attribuzione a UD Ancient Greek Perseus r2.18 al commit `37837c7a`: ShareAlike vincola l'adattamento alla licenza della fonte, e la licenza del codice non si estende né ai documenti né ai dati. I raw non vengono ridistribuiti da questo repository. [Bibliografia attiva](docs/BIBLIOGRAPHY.md).

Python 3.12 via uv, con il lock conservato. Il research proposal 3.1 (§17.1) non è ancora depositato.
