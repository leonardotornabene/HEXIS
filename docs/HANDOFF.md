# Handoff HEXIS 3.1 — stato attuale

**V0–V2 completati; V3–V5 non attestati; nessun fit reale; nessun push.** Ramo di lavoro `codex/hexis31-realign`, creato da `5f1ec06afa192c8d0f006d7f39cdb97df72c2983`. La cronologia dettagliata delle tranche precedenti non è ripetuta qui: sta nella storia Git e, nella sua ultima forma pre-riallineamento, in [archive/docs/HANDOFF.md](../archive/docs/HANDOFF.md).

## Riallineamento del 22 settembre 2026 — verifica

Commit del riallineamento su `codex/hexis31-realign`: atto `1294f55`, migrazione dei test `90dffc0`, codice e gate `f6ffe51`, documenti e archivio `08ba6cd`, residui `1f441ff`. Questa sezione è documentale e non cita il proprio commit.

**Suite e gate.** Righe finali verbatim:

```text
uv run --frozen pytest -q -p no:cacheprovider
398 passed in 190.31s (0:03:10)

uv run --frozen pytest --collect-only -q          398 tests collected
uv run --frozen pytest -m v31 --collect-only -q   398 tests collected
uv lock --check                                   Resolved 23 packages
```

Le due selezioni coincidono, nessuno skip e nessun deselected. Base di confronto a `5f1ec06`: 672 passed più 17 skip nella suite completa, 351 nell'accettazione.

**Nessun file perso.** Ogni percorso esistente a `5f1ec06` è oggi o nell'albero attivo o in `archive/`: 101 file archiviati, tutti con lo stesso blob dell'originale; 30 file attivi modificati; nessun file attivo nuovo fuori dall'archivio.

**Invarianti.** I 69 file tracciati del deposito, del record, del lock, della configurazione, della provenienza e di `data/raw/PROVENANCE.md` hanno blob identici a `5f1ec06`. I 98 file locali di `data/raw`, `scripts/` e `results/hexis31` hanno gli stessi sha256 del baseline.

**Equivalenza del percorso 3.1.** La batteria sintetica congelata è identica byte per byte alla sua esecuzione a `5f1ec06`. Il corpus V1 rigenerato riproduce i nove artefatti byte per byte; nel manifest differiscono soltanto `run_id`, l'identità del codice e i quattro campi esterni dichiarati in anticipo (`created_utc`, `output_dir`, `implementation_commit`, e `tracked_dirty` quando l'albero non è pulito).

**Copertura.** Differenziale per riga fra suite completa e `-m v31`, misurato a codice invariato con `sys.monitoring` della libreria standard: 231 righe erano raggiunte solo dai test non v31, tutte e sole nel codice v2.1 poi rimosso. Nessuna riga del percorso 3.1 ha perso copertura.

**Mutazioni.** Le 40 mutazioni della revisione pre-V3 si ancorano ancora tutte al codice attuale: **35 uccise, 5 sopravvissute — M3, M6, M14, A1, P1 — le stesse di `0dc69b5`**, dominate da controlli più forti.

**Residui.** Fuori dal deposito, dall'archivio e dagli atti restano soltanto menzioni della storia come storia e guardie che ne vietano il ritorno. Due link relativi dentro V3-001 restano rotti per scelta, perché i byte di un atto non si riscrivono: V3-002 li risolve con la regola `archive/<percorso>`. Il commento di `config/registry_overrides.yaml` cita ancora `history/v2.1`: la configurazione è un invariante di questo riallineamento e non è stata toccata.

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
2. **Licenze**: decise ed espresse nell'atto (MIT / CC BY 4.0 / CC BY-NC-SA 2.5). Resta da verificare con la sede editoriale, prima del push, che la clausola NonCommercial sia compatibile con i suoi materiali supplementari.
3. **Research proposal 3.1 (§17.1)**: non ancora depositato. In `docs/proposal/` esistono file locali non tracciati; tracciarli è una decisione separata, perché entrerebbero nel perimetro della pubblicazione.
4. **V3–V5**: prova tecnica, campagna, report e figure, nell'ordine del §14.

Arresto per revisione prima di V3.
