# Handoff HEXIS 3.1 — stato attuale

**V0–V2 completati; V3–V5 non attestati; nessun fit reale.** Pubblicazione del 2026-09-23: il push del ramo `codex/hexis31-realign` a `2ebb3464b871c1f831d0608edba052ccb4b92be9` e dei tag `archive/pre-realign` e `archive/v2.1`; seguono l'unione in `master` con merge commit, senza squash né rebase, e la cancellazione del ramo remoto `g1/pre-audit` (V3-002, E5). Ramo di lavoro `codex/hexis31-realign`, creato da `5f1ec06afa192c8d0f006d7f39cdb97df72c2983`. La cronologia dettagliata delle tranche precedenti non è ripetuta qui: sta nella storia Git e, nella sua ultima forma pre-riallineamento, in [archive/docs/HANDOFF.md](../archive/docs/HANDOFF.md).

## Code review del 23 settembre 2026

Due review integrali di `5f1ec06..a4a8871`, ciascun rilievo verificato sul repository prima di agire.

**Accolti e corretti.** L'archivio era raccolto da `pytest .`: il riallineamento aveva tolto `norecursedirs`, e il docstring che prometteva il contrario non aveva un assert. L'attestazione del trasferimento da `legacy_audit` diceva «senza modifiche», mentre il messaggio di `verify_inputs_unchanged` era cambiato. L'atto dava due licenze agli stessi byte e non copriva `config/`, i metadati di `data/`, gli script del deposito né il codice sotto `archive/`. `LICENSE` non dichiarava il proprio ambito, e il README ripeteva l'atto. `archive/README.md` era una nota nuova al posto del README storico. `.gitignore` non ignorava più `data/interim/` e `data/processed/`, e ignorava anche `archive/results/`. `CANONICAL_DATA_ROOT` dipendeva dalla directory corrente. Restavano una docstring falsa in `manifest.py`, un commento orfano e righe vuote residue. Due test nuovi vincolano l'archivio: `test_the_archive_is_never_collected_even_from_the_root` e `test_every_archived_file_has_its_bytes_at_the_base`.

**Respinti.** Limitare al solo repository la regola «ogni test raccolto è v31»: `test_every_collected_test_is_active_acceptance` la verifica proprio in un progetto sintetico, e nessun progetto sintetico ha test senza marker. Modificare i due test che rifiutano un `hexis.stats` importabile: il rifiuto è corretto, e la causa si evita come dice «Eseguire la storia».

**Attestazione.** Correzioni in `61d4a08` (test prima, poi codice e configurazione) e `2eabcb6` (atto e documenti); questa sezione non cita il proprio commit. Misurata su `2eabcb6`, albero tracciato pulito prima e dopo:

```text
uv run --frozen pytest -q -p no:cacheprovider
400 passed in 163.67s (0:02:43)

uv run --frozen pytest --collect-only -q          400 tests collected
uv run --frozen pytest -m v31 --collect-only -q   400 tests collected
uv run --frozen pytest . --collect-only -q        400 tests collected
uv lock --check                                   Resolved 23 packages
```

Le tre raccolte hanno gli stessi node ID e nessuno sotto `archive/`. Prima delle correzioni, i due test nuovi fallivano ciascuno sul proprio rilievo: `archive/tests/test_old.py` raccolto da `pytest .`, e `archive/README.md` con blob `d8c0353` invece di `d0e062e`. L'archivio ha 102 file su 102 identici a `5f1ec06`, nessun percorso perso. Rispetto a `legacy_audit` a `5f1ec06`, l'AST differisce soltanto per `verify_inputs_unchanged` e `CANONICAL_DATA_ROOT`, come dichiara V3-002. Il corpus V1 rigenerato con `run_encode` a `2eabcb6`, in una directory esterna, riproduce i nove artefatti byte per byte; nel manifest differiscono soltanto `run_id`, l'identità del codice e i campi esterni già dichiarati.

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

**Nessun file perso.** Ogni percorso esistente a `5f1ec06` è oggi o nell'albero attivo o in `archive/`: 102 file archiviati, tutti con lo stesso blob dell'originale; 34 file attivi modificati; nessun file attivo nuovo fuori dall'archivio. Fino alla correzione del 23 settembre questa riga contava 101 e 30: la centoduesima voce era una nota nuova al posto del README storico, e i file modificati erano già 33.

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

- **D1** — nessun push pubblico finché un atto di pubblicazione non decide sui derivati. Superata dall'atto di pubblicazione di V3-002, efficace al primo push.
- **D2** — il validatore del report rigenera ledger, conteggi di rimescolamento e provenienza C0 (attuata in `0dc69b5`).
- **D3** — la deviazione della CLI dal §14.1 è registrata nella nota V3-001 del [Decision Log](02_DECISION_LOG.md).
- **D4** — le cinque figure sono corrette nei difetti e nella leggibilità (attuata in `0dc69b5`).

La nota sul `.DS_Store` entrato e uscito dal deposito è ora in V3-002, che la registra come parte dell'atto.

## Perimetro del congelamento

`_code_identity()` copre tutto `src/hexis`; l'evidenza V2 (`validation_run.context`) lega anche `tests/*.py`, `conftest.py`, `pyproject.toml`, il file di configurazione, `uv.lock` e il manifest del corpus usato. Dopo la pubblicazione di una validazione, modificare uno di questi impedisce la ripresa e impone una directory nuova con V2 e V3 rifatti. I documenti restano fuori dal perimetro e modificabili; `archive/` è fuori dal perimetro ma vincolato ai byte di `5f1ec06` da `test_every_archived_file_has_its_bytes_at_the_base`. Il riallineamento ha riaperto questo congelamento **prima** che qualunque evidenza V2 o V3 fosse pubblicata: sotto `results/hexis31/` esistono solo i run V1.

## Eseguire la storia

La storia si esegue soltanto in un worktree separato: `git worktree add ../hexis-pre-realign archive/pre-realign`. Un checkout di `5f1ec06` nella copia principale lascerebbe file ignorati che il ritorno al ramo non toglie. `src/hexis/stats/__pycache__/` renderebbe `hexis.stats` importabile come namespace package, e due test attivi lo rifiutano, giustamente. Gli output v2.1 in `data/interim/` e `data/processed/` sono derivati del corpus, e per questo sono ignorati.

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

1. **Code review integrale**: eseguita il 23 settembre 2026, con due review; esiti e correzioni nella sezione in testa. La verifica di conformità al piano dello stesso giorno non trova scostamenti di sostanza; le due letture di V2 non ancora dichiarate nell'albero attivo sono ora le deviazioni 4 e 5 di V3-002.
2. **Licenze**: decise nell'atto di pubblicazione di V3-002, e soltanto lì. La sede editoriale non è determinabile: l'atto registra la pubblicazione senza sede (E9).
3. **Research proposal 3.1 (§17.1)**: non ancora depositato. In `docs/proposal/` esistono file locali non tracciati; tracciarli è una decisione separata, perché entrerebbero nel perimetro della pubblicazione.
4. **V3–V5**: prova tecnica, campagna, report e figure, nell'ordine del §14.

Arresto per revisione prima di V3.
