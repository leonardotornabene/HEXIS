# HEXIS 3.1 — registro di riconciliazione V2

Piano utente: riallineamento → 2A M1–M3 → 2B persistenza → 2C evidenze → revisione separata → chiusura; nessun fit reale V3, push o merge. Base `8b4d50432724442465d4d3003a2d37717395126a`, ramo `codex/hexis31-v0-v1`, checkout richiesto già attivo, solo `?? scripts/` iniziale. Autorità: V3-001 e piano/JSON depositati; attesi immutabili.

Digest SHA-256 iniziali:

```json
{
  "docs/V3-001-deposit.json": "e0d8951f60e6eebaa31e957db7c8733fe30b3b09ce9f3db8cbece397c3d2694c",
  "uv.lock": "33db43b00bcb21ab12aedf6dcc4257764770bff0115dc0d1dfab6e5ea89876bf",
  "scripts/reacquire_raw_data.sh": "4524ac4162250520cf73283aa4b66bd4a22a6164ab8b4cd512741425f116b2bb"
}
```

| Sottostadio | Stato | Evidenza |
|---|---|---|
| 1 — riallineamento | COMPLETATO — a535484 | 12 test documentali superati; attestazioni storiche conservate |
| 2A — M1–M3 | COMPLETATO | 262 v31 pass; 25 sintetici + 9 stress; revisione separata delle correzioni superata |
| 2B — M4 | PENDING | Lacune esplicitate nell'inventario |
| 2C — M5 | PENDING | Nessun fit reale autorizzato |
| 3 — revisione integrale | PENDING | Separata dall'implementazione |
| 4 — chiusura | PENDING | V2 dichiarabile solo dopo tutti i controlli |

La modifica dei test documentali sostituisce l'attesa di una dichiarazione generale non giustificata con la rettifica richiesta dall'utente; non indebolisce proprietà scientifiche.

## 2A — verifiche e divergenze dimostrate

Base riprodotta: `uv run pytest -m v31 -q` → `240 passed, 338 deselected in 87.27s (0:01:27)`; documentazione dopo rettifica → `12 passed in 0.12s`.

Il confronto M1–M3 ha rilevato istogrammi di supporto mancanti (§9.1), incontri con rami non osservati persi quando la massa va in underflow, slot duplicati/provenienza non biunivoca e simboli invalidi non rifiutati dal percorso score. Dodici regressioni prima rosse, poi verdi. Generatori, RNG, formule CTW/Q/R1 e attesi congelati restano invariati.

La batteria restituiva successo con righe mancanti/duplicate, stress non finito o fuori normalizzazione, conteggi/supporti/deficit corrotti e PASS non coerente con le perdite: dieci fallimenti osservati prima della correzione. La revisione separata ha inoltre richiesto il confronto dell'oracle registrato con la fixture congelata. I nove stress mantengono un criterio di validità numerica, senza richiesta di raggiungere l'oracle.

Verifica mirata protocollo: `uv run pytest -q tests/test_v31_scores.py tests/test_v31_r1.py tests/test_v31_sampling.py` → `58 passed in 16.50s`. Un primo controllo del nuovo validatore ha rifiutato anche log-evidenze NumPy valide; la serializzazione esplicita float64→float nativo nel record corregge il tipo senza modificare il valore.

Chiusura 2A: `uv run pytest -m v31 -q` → `262 passed, 338 deselected in 77.00s (0:01:16)`, exit 0, nessuno skip/xfail. Include i 25 sintetici e i nove stress. Review separata delle correzioni conclusa senza rilievi aperti dopo regressione oracle-drift rossa/verde.
