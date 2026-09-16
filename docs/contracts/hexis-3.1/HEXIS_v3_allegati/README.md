# HEXIS 3.0.1 — Allegati al piano integrale

Revisione autorizzata del **12 settembre 2026**; prima consegna 11 settembre. La data nei nomi esterni del piano e dell’archivio conserva la prima consegna. Il piano e questo pacchetto costituiscono una specifica di destinazione: la repository non è stata modificata e la pipeline v3 non è ancora integrata.

Trasmettere **l’intero archivio operativo**, non il solo archivio CTW storico. Il piano incluso è identico a quello consegnato separatamente. `SHA256SUMS.json` elenca ricorsivamente tutti gli altri file, escluso se stesso. La versione iniziale degli allegati è conservata senza modifiche in `history/allegati_v3_0_originali.zip` e non governa la revisione corrente.

## Contenuto e autorità

| File | Ruolo |
|---|---|
| `HEXIS_piano_integrale_v3_2026-09-11.md` | Specifica semantica integrale, revisione 3.0.1 |
| `CHANGELOG_REVIEW_2026-09-12.md` | Esito e trattamento di B1–B3, S1–S8 e rilievi minori |
| `hexis_v3_design.json` | Contratto strutturato: 9 celle, 7 blocchi, 18 prefissi/17 documenti, pesi e governance |
| `corpus_atteso.json` | Conteggi verificati per documento, blocco e codifica |
| `design_lock.json` | Digest esterni del piano e del contratto; pronti per il deposito V0, non attestazione del suo superamento |
| `authorization_and_experiments.json` | Eccezione autorizzata al vecchio freeze e campagne documentate; atto Git ancora da depositare |
| `identita_fonti_verificate.json` | Identità e hash delle sorgenti documentali controllate |
| `protocol_contract.py` | Semi, campionamento, rimescolamento e confini |
| `ctw_reference.py` | Nucleo CTW di riferimento separato, invariato |
| `resolved_diagnostics.py` | Massa risolta e profondità della nuova diagnostica |
| `score_contract.py` | JSD, aggregazione primaria e riaggregazione secondaria per target eleggibili |
| `report_contract.py` | Precondizioni di completezza, binding e integrità per il futuro report |
| `validate_contract.py` | Configurazione, fixture, pilot opzionale di 16 fit reali/84 valutazioni probe |
| `validate_diagnostics.py`, `validate_scores.py`, `validate_report.py` | Test supplementari di diagnostiche, formule e rifiuto di campagne incoerenti |
| `validate_revision.py` | Censimento frammenti, ablazione e controesempi S1/S3 |
| `compare_numpy.py` | Confronto riproducibile di 7 fold e 42 contributi per versione NumPy |
| `contract_validation.json` | Riesecuzione del contratto sotto NumPy 2.5.1, 16 fit reali/84 valutazioni probe |
| `diagnostics_validation.json`, `scores_validation.json`, `report_validation.json` | Esiti effettivi dei test supplementari; i manifest del report sono fixture sintetiche |
| `revision_validation.json` | Censimento, 14 fit reali di ablazione e 9 fit sintetici di controesempio |
| `numpy_2_3_5_validation.json`, `numpy_2_5_1_validation.json` | Digest ottenuti separatamente dalle due versioni |
| `numpy_comparison.json` | Confronto dei digest e portata della verifica |
| `package_validation.json` | Coerenza finale, integrità e mancata modifica del repository |
| `verifiche_CTW_precedenti.zip` | Prove CTW storiche, incluse fixture, ledger e generatori |
| `verdetto_CTW_precedente.md`, `verifica_comparata_precedente.md` | Giudizi storici anteriori alla specifica v3 |
| `history/HEXIS_piano_integrale_v3_0.md` | Piano iniziale conservato, superato dalla revisione corrente |
| `history/allegati_v3_0_originali.zip` | Copia byte per byte del pacchetto iniziale, con evidenze e configurazione originali |
| `SHA256SUMS.json` | Inventario di integrità del pacchetto corrente |

Corrispondenza dei titoli storici citati nel piano: `HEXIS_verdetto_CTW_2026-09-11.md` è conservato qui come `verdetto_CTW_precedente.md`; `HEXIS_verifica_comparata_2026-09-11.md` come `verifica_comparata_precedente.md`. I nomi abbreviati non indicano nuovi giudizi.

Il testo governa la semantica e il JSON i valori/elenchi. I contratti eseguibili illustrano le operazioni specificate, ma non implementano tutte le validazioni pubbliche, i manifest applicativi, i certificati, la CLI o gli output definitivi. Nessun modulo della futura pipeline deve importare questi prototipi come scorciatoia ai gate. `report_contract.py` verifica byte e chiavi; la pipeline deve aggiungere controllo dei contenuti, degli slot e dei certificati canonici, quindi superare T26/T30.

Il campo storico `weighted_depth` rimane nel prototipo e nelle evidenze per tracciabilità; la diagnostica scientifica v3 è quella di `resolved_diagnostics.py`.

## Riprodurre

Estrarre in una cartella nuova. Prima di eseguire, verificare gli hash con la libreria standard:

```bash
python -B - <<'PY'
from pathlib import Path
import hashlib,json
for name,expected in json.loads(Path('SHA256SUMS.json').read_text()).items():
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==expected,name
print('Integrità verificata')
PY
```

Conservare intatta questa copia dell’evidenza. Eseguire i test in **una seconda copia di lavoro**, perché alcuni comandi aggiornano i propri JSON:

```bash
python -B validate_contract.py --output rerun_contract
python -B validate_diagnostics.py
python -B validate_scores.py
python -B validate_report.py
```

Il contratto usa libreria standard e NumPy. Python verificato: 3.12.14. Per i dati reali acquisire i tre CoNLL-U dal commit e dagli hash nel contratto; `prepare_data.py` e istruzioni sono nell’archivio CTW storico. I dati non sono inclusi. Non è necessario clonare HEXIS.

```bash
python -B validate_contract.py --raw-dir raw/UD_Ancient_Greek-Perseus --output rerun_real
python -B validate_revision.py --raw-dir raw/UD_Ancient_Greek-Perseus --output rerun_revision.json
python -B compare_numpy.py --raw-dir raw/UD_Ancient_Greek-Perseus --output rerun_numpy.json
```

`validate_revision.py` confronta l’ablazione con il `contract_validation.json` incluso: tale baseline deve contenere i sette fold C0. Le sue formule restano uguali sotto entrambe le versioni confrontate.

Per ripetere esplicitamente il confronto fra versioni senza modificare un progetto:

```bash
uv run --no-project --with numpy==2.3.5 python -B compare_numpy.py --raw-dir raw/UD_Ancient_Greek-Perseus --output rerun_numpy_2_3_5.json
uv run --no-project --with numpy==2.5.1 python -B compare_numpy.py --raw-dir raw/UD_Ancient_Greek-Perseus --output rerun_numpy_2_5_1.json
```

Confrontare i campi `ledger_and_shuffle_sha256` e `model_and_scores_sha256`. L’ambiente della futura integrazione conserva invece il `uv.lock` del repository, senza downgrade o nuovi pin dettati dal prototipo. La verifica completa dello stack avviene nei gate.

## Significato degli esiti

PASS riguarda i casi eseguiti e il contratto separato. Non certifica la futura implementazione, i 1.400 fit finali o un risultato scientifico positivo. L’ablazione ha portata locale; i controesempi sintetici confutano affermazioni universali, non stimano il bias linguistico del corpus. Nessun contrasto reale fra gruppi è stato prodotto in queste nuove verifiche. Gli allegati originali della ricerca e i file del repository rimangono invariati.
