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
| 2B — M4 | COMPLETATO | 302 v31 pass; 86 test mirati pass |
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

## 2B — persistenza e controlli semantici

Sette regressioni iniziali rosse riproducono lock ereditato, documento senza target, risorse assenti e famiglie/bracci non controllati. Aggiunte regressioni rosse per semi bool/float, somme corrotte in resume, misure risorse mancanti/duplicate/negative o con unità ambigue e JSON con chiavi duplicate. Il lettore verifica ora schemi esatti, chiavi e conteggi, denominatori del corpus/budget e masse; ricostruisce da C0 anche somme e conteggi validi/null di L_resolved e somme unseen. La tolleranza CE è 1e-9 bit/target (§6.5); diagnostiche e conservazione delle masse usano 1e-12 per posizione per l'accumulo numerico. Chiavi e conteggi restano esatti.

Le righe documento/fascia vuote sono prodotte e ricostruite usando tutti i documenti held-out, con somme zero e null motivati nel report. Il precedente test negativo ora corrompe esplicitamente il risultato: conserva il rifiuto dell'omissione senza richiedere che il produttore continui a omettere le righe.

Tempi di fit e valutazione in secondi da `time.perf_counter`; RSS in byte da `resource.getrusage(RUSAGE_SELF).ru_maxrss`, massimo storico del processo osservato per modello, non misura isolata dell'allocazione del singolo modello. Tutte le misure sono in `metadata`, escluse da identità, partizioni e tabelle deterministiche. Nessuna previsione della campagna.

R1 conserva ora sia frequenze empiriche sia smussate accanto ai conteggi (§8.3), senza cambiare la JSD. Revisioni dei cambiamenti separate dalla scrittura hanno segnalato e fatto coprire anche la completezza dei metadati delle risorse. Nessun fit reale.

Chiusura 2B: `uv run pytest -q tests/test_v31_report_semantics.py tests/test_v31_completion.py tests/test_v31_descriptive.py --tb=short` → `86 passed in 17.65s`; `uv run pytest -m v31 -q` → `302 passed, 338 deselected in 82.57s (0:01:22)`, exit 0 e zero skip/xfail.
