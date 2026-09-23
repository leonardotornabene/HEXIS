# HEXIS 3.1 — Allegati del piano definitivo

Data: 15 settembre 2026. Stato: FINAL_PLAN_NOT_APPLIED.

Il piano completo è il file fratello `HEXIS_piano_definitivo_v3.1_2026-09-15.md`. Questi JSON aggiornano registro, corpus atteso, alfabeti, sei celle e contratto di report. Non sono un override della CLI v2.1 né risultati della campagna. Non contengono raw o fit reali nuovi.

Conservare la cartella insieme al piano, al pacchetto `hexis-verifica` e allo ZIP storico identificato nei contratti. La semantica è nel piano; i valori devono coincidere. Depositare in V0 piano/contratti/design_lock; il deposito è ancora nullo. I file della repository sono invariati.

`SHA256SUMS.json` elenca i file della consegna e il piano tramite `../`; `design_lock.json` lega soltanto piano e contratti, senza hash ricorsivi. `verifica_documentale.json` descrive i controlli realmente svolti; non è un certificato dei gate software futuri.

I riferimenti eseguibili restano nello ZIP storico (hash e percorsi nel contratto). Estrarre soltanto le fixture per i test: alcuni main storici fanno fit reali o usano regole obsolete. Nessun test v3.1 è attestato prima del porting.
