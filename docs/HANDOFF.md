# Handoff HEXIS 3.1 — stato attuale

**V0–V2 completati; V3–V5 non attestati; nessun fit reale; nessun push.** Ramo di lavoro `codex/hexis31-realign`, creato da `5f1ec06afa192c8d0f006d7f39cdb97df72c2983`. La cronologia dettagliata delle tranche precedenti non è ripetuta qui: sta nella storia Git e, nella sua ultima forma pre-riallineamento, in [archive/docs/HANDOFF.md](../archive/docs/HANDOFF.md).

## Identità

| Oggetto | Identità |
|---|---|
| Deposito V0 | `e98fb8edde91e821c415e26f33b7bdeb549b50ba`; 63 digest in [V3-001-deposit.json](V3-001-deposit.json) |
| Corpus V1 | `7afdd3a4f87341110b0f15a77179febe9075ee9b`; run consegnato `results/hexis31/v1`, manifest SHA-256 `154433c772f41e444f86b8787e0ee0003c546d9fb398b6ee0f634ce193f3421f` |
| Chiusura V2 | `0a6f644`; revisione pre-V3 `0dc69b5`, attestato **351 v31 / 672 passed + 17 skip** |
| Base del riallineamento | `5f1ec06`, tag `archive/pre-realign`; storia v2.1 al tag `archive/v2.1` = `852644b6917790877c7b2ca5df2e76b17829d87c` |
| Ambiente | Python 3.12.13, `uv.lock` `33db43b00bcb21ab12aedf6dcc4257764770bff0115dc0d1dfab6e5ea89876bf`, 23 pacchetti |

## Decisioni del proprietario del 22 settembre 2026 (D1–D4)

- **D1** — nessun push pubblico finché un atto di pubblicazione non decide sui derivati. Superata da V3-002, che diventa efficace al primo push e richiede prima la decisione sulla licenza.
- **D2** — il validatore del report rigenera ledger, conteggi di rimescolamento e provenienza C0 (attuata in `0dc69b5`).
- **D3** — la deviazione della CLI dal §14.1 è registrata nella nota V3-001 del [Decision Log](02_DECISION_LOG.md).
- **D4** — le cinque figure sono corrette nei difetti e nella leggibilità (attuata in `0dc69b5`).

La nota sul `.DS_Store` entrato e uscito dal deposito è ora in V3-002, che la registra come parte dell'atto.

## Perimetro del congelamento

`_code_identity()` copre tutto `src/hexis`; l'evidenza V2 (`validation_run.context`) lega anche `tests/*.py`, `conftest.py`, `pyproject.toml`, il file di configurazione, `uv.lock` e il manifest del corpus usato. Dopo la pubblicazione di una validazione, modificare uno di questi impedisce la ripresa e impone una directory nuova con V2 e V3 rifatti. I documenti e `archive/` restano fuori dal perimetro e modificabili. Il riallineamento ha riaperto questo congelamento **prima** che qualunque evidenza V2 o V3 fosse pubblicata: sotto `results/hexis31/` esistono solo i run V1.

## Sequenza operativa prevista per V3–V5, non eseguita

Albero tracciato pulito (`scripts/` e `docs/proposal/` non tracciati sono ammessi), corpus `results/hexis31/v1`, destinazioni nuove sotto `results/hexis31/`:

```bash
uv sync --frozen
uv run python -m hexis.pipeline.run_tree_validation --config config/default.yaml --corpus-dir results/hexis31/v1 --output-dir results/hexis31/<run>
uv run python -m hexis.pipeline.run_descriptive --config config/default.yaml --corpus-dir results/hexis31/v1 --output-dir results/hexis31/<run> --seed 0
# §12.2: stessa coppia di comandi in una directory distinta, stesso codice
uv run python -m hexis.pipeline.run_tree_validation --config config/default.yaml --corpus-dir results/hexis31/v1 --output-dir results/hexis31/<regen>
uv run python -m hexis.pipeline.run_descriptive --config config/default.yaml --corpus-dir results/hexis31/v1 --output-dir results/hexis31/<regen> --seed 0
# V4, dopo la revisione di V3
uv run python -m hexis.pipeline.run_descriptive --config config/default.yaml --corpus-dir results/hexis31/v1 --output-dir results/hexis31/<run> --resume
# V5
uv run python -m hexis.pipeline.run_report --config config/default.yaml --corpus-dir results/hexis31/v1 --output-dir results/hexis31/<run> --regenerated-dir results/hexis31/<regen>
```

## Obblighi aperti

1. **Code review integrale**, sull'albero finale e sul diff `5f1ec06..HEAD`, con la [mappa dei test](TEST_INVENTORY.md) come ingresso.
2. **Licenza dei derivati (E2)**: decisione del proprietario, da registrare in V3-002 prima del push.
3. **Research proposal 3.1 (§17.1)**: non ancora depositato. In `docs/proposal/` esistono file locali non tracciati; tracciarli è una decisione separata, perché entrerebbero nel perimetro della pubblicazione.
4. **V3–V5**: prova tecnica, campagna, report e figure, nell'ordine del §14.

Arresto per revisione prima di V3.
