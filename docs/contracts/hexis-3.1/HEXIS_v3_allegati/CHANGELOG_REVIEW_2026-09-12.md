# HEXIS 3.0.1 — Registro della revisione autorizzata

Data: 12 settembre 2026. Versione precedente: 3.0, 11 settembre. La data nei nomi dei due file di consegna conserva quella della creazione iniziale. La revisione riguarda piano e allegati; nessun intervento nella repository.

Le decisioni incorporano le obiezioni fondate e correggono le affermazioni del revisore che non risultano generali. Non cambiano corpus, CTW, misura Q, JSD, nove celle, semi o budget di 1.400 fit. Nessun contrasto finale è stato selezionato o presentato.

| Obiezione | Giudizio e decisione applicata | Riscontro operativo |
|---|---|---|
| B1 — Allegati assenti per il revisore | Problema di consegna: l’archivio CTW storico non è il pacchetto operativo. La consegna corrente è autosufficiente per testo, configurazione e contratti; include una copia identica del piano. | README, inventario SHA-256; vecchio pacchetto conservato byte per byte in `history/` |
| B2 — Frammenti e inizi artificiali | Obiezione fondata. Confermato deliberatamente il budget esatto con al più un frammento finale per contributore; BOS significa inizio dello stream campionato. C5 delle proposte precedenti è esplicitamente superata, con costo dichiarato. | §5.2; censimento 840 contributi, 671 frammenti, 563 inizi interni; ablazione su sette fold C0 al primo seme, 14 fit; `validate_revision.py` |
| B3 — Freeze v2.1 e fit precedenti a G2 | Obbligo documentale fondato. V3-001 deve registrare l’eccezione autorizzata, senza simulare un G2 superato o retrodatare il deposito Git. | §13.1; `authorization_and_experiments.json`; atto ancora da depositare nell’implementazione |
| S1 — Bias necessariamente contro HEX | Asimmetria reale, direzione universale non dimostrata. Un controesempio CTW mostra che aumentare la quota etichettata come proprio gruppo può diminuire Q oppure aumentarlo. Q non garantisce la rimozione del confondimento. | §5.1; controesempio riproducibile; quote del training obbligatorie. La quota è collineare con il gruppo e non identifica una correzione causale. |
| S2 — Sensibilità ai pesi | Accolta. Affiancare in tutte le celle una riaggregazione pesata per target eleggibili della variante; primaria resta la media dei blocchi. | §8.2-bis e §11.5; configurazione, `token_weighted_contrast`, fixture con pesi diseguali e scomposizione di Q; zero fit aggiuntivi |
| S3 — G del rimescolato nullo | Nullo osservato nel pilot, non identità matematica per ogni campione finito i.i.d. Mantenuti i 700 fit del controllo e le due componenti di Q. | §7.4; caso i.i.d. finito con G non nullo e peso di arresto inferiore a 1 |
| S4 — Impegni solo verbali | Accolta. Contratto analitico congelato in V0; implementazione/ambiente in V3; soltanto `run_report` emette contrasti dopo campagna completa e verificata. | §14.2; `design_lock.json`, `report_contract.py`, test di omissione, duplicazione, sostituzione e corruzione. Il riferimento non sostituisce schemi/manifest/gate della futura pipeline. |
| S5 — Contributo e contesti brevi | Contributo positivo esplicitato. Contesti profondi poco supportati sono già evidenza del pilot, senza trasformarli nel risultato finale. Corretta l’etichetta: gli intervalli storici provengono da `weighted_depth`, non dalla nuova profondità risolta. | §1.1, §2, §9, §16 |
| S6 — Precedenti bibliografici | Reinseriti Galves et al. 2012 e Gorman & Gorman 2016, con differenze di oggetto e metodo. | §1.1 e §18; collegamenti alle fonti primarie |
| S7 — Utility statistiche | Conservare moduli funzionanti e relativi test, escludendo il loro uso nella pipeline scientifica v3. Vecchie attestazioni non diventano nuovi gate. | §13.2; nessuna cancellazione del codice effettuata |
| S8 — Downgrade NumPy | Eliminato. Conservare `uv.lock`, NumPy 2.5.1 e dipendenze esistenti; confronto empirico dei vettori sotto entrambe le versioni. | §15.1; 7 fold/42 contributi per versione, digest uguali; contratto completo supplementare rieseguito sotto 2.5.1 |

## Precisazioni minori recepite

- Stime disco distinte per colonne e materializzazione; 12.704.540 righe accoppiate non diventano il numero di fit.
- 3.360 chiavi di derivazione verificate dal nuovo contratto non sono le 1.680 valutazioni probe né le chiavi del pilot storico.
- `config/default.yaml` va sostituito integralmente nella migrazione, non adattato facendo convivere silenziosamente v2.1 e v3.
- `scripts/reacquire_raw_data.sh`, segnalato come non tracciato dal revisore, non è disponibile nella copia qui verificata: deve essere preservato e controllato nella working copy del responsabile. Non se ne certifica il contenuto.
- Corretto il refuso `D=01–D54` in `D01–D54` e riallineata la tabella dei comandi: i fit scrivono somme e score individuali; i contrasti sono emessi dal report.

## Portata delle verifiche

Il censimento e l’ablazione non provano che i frammenti siano irrilevanti su ogni seme/cella. L’ablazione elimina il frammento dalla stessa lista già scelta, senza rimpiazzo; è una verifica di sviluppo, non una nuova cella da selezionare sul risultato. Il massimo scarto assoluto di Q nel pilot verificato è circa 0,00068506544 bit/simbolo.

Il confronto NumPy verifica il contratto su questa macchina, con lo stesso Python. Non garantisce l’identità universale di ogni trasformazione di `Generator` o la compatibilità dell’intero stack. I gate della futura integrazione restano necessari.

I test sul report usano fixture sintetiche complete/incomplete. Non attestano che siano stati eseguiti i 1.400 fit finali né producono certificati V0–V3 reali. La verifica dei byte degli artefatti è effettiva; la verifica della loro semantica scientifica e degli slot è prescritta alla pipeline integrata.

La revisione chiude le decisioni del piano. Restano attività di implementazione esplicite, con criteri di accettazione; non alternative metodologiche da decidere dopo i risultati.
