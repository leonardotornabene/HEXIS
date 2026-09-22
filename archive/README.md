# Archivio HEXIS — storia, non autorità

Questa cartella conserva ciò che non appartiene al percorso 3.1. Ogni file sta al percorso che aveva al commit `5f1ec06afa192c8d0f006d7f39cdb97df72c2983`, con gli stessi byte: il file che stava in `P` sta qui in `archive/P`.

L'archivio è un registro, non un albero eseguibile. Non viene importato, non viene raccolto da pytest, non entra nell'identità del codice né nel contesto delle evidenze. Le sue suite e i suoi moduli si eseguono a quel commit, dove il loro codice è vivo; qui alcuni import non si risolvono, ed è voluto.

Lo stato di ogni voce — v2.1, D01–D54, D55 proposto, ratifiche tecniche G1, `candidates/` in quarantena, utility statistiche, proposal precedente, risultati pre-audit — è dichiarato in V3-002, nel [Decision Log](../docs/02_DECISION_LOG.md). Nessuna voce è autorità per nuove esecuzioni e nessuna apertura storica è dichiarata risolta.

Per leggere la storia senza toccare l'albero di lavoro: `git show archive/pre-realign:<percorso>` oppure `git worktree add`. Un `git checkout` di un commit anteriore nella copia principale cancellerebbe i file locali ignorati.
