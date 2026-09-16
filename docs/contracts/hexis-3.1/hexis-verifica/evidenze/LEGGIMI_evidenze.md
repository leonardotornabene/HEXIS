# Evidenze della revisione consolidata

Questi file accompagnano il rapporto del 15 settembre 2026. Non applicano modifiche metodologiche alla repository e non contengono i dati grezzi.

## Contenuto

- `input_verificati.json`: identità dei materiali esaminati; 33 hash del pacchetto corrente e 103 dell'archivio storico verificati senza discrepanze.
- `corpus_audit.json`, `audit_corpus.md`: conteggi ricostruiti dai CoNLL-U, accorpamento e controlli dei due XML Ateneo.
- `audit_repository.md`: controlli dello stato effettivo e trascrizione dell'esito pytest. Non è un log completo della suite.
- `audit_matematico.md`, `controlli_matematici.txt`: lettura dei pilot e piccoli controlli sintetici indipendenti.
- `sintetici_25.json`: riesecuzione dei 25 casi piccoli del piano; tutte le soglie prescritte soddisfatte, inclusa CE strettamente minore di 0,02 per il ciclo.
- `verifica_corpus.py`, `verifica_matematica.py`, `verifica_sintetici.py`: controlli ripetibili senza nuovi fit reali. I due script matematici impiegano il riferimento degli allegati, non il modello canonico ancora da implementare.

I rapporti degli audit separati conservano i percorsi temporanei della sessione come provenienza storica. Le copie e gli script qui presenti sono le evidenze da conservare. In caso di differenza interpretativa, il documento principale contiene il verdetto consolidato.

## Ripetizione dei controlli

Usare Python 3.12 e il NumPy del lock della repository (2.5.1 nel controllo). Il censimento usa soltanto la libreria standard.

1. Per il corpus, fornire allo script la repository con i tre raw già presenti e lo ZIP operativo originario:

   ```text
   python verifica_corpus.py --repo /percorso/hexis --zip /percorso/HEXIS_allegati_operativi_v3_2026-09-11.zip
   ```

   Il risultato JSON va allo standard output. Non ricalcola i metadati degli XML upstream: quei controlli sono documentati separatamente nel rapporto corpus.

2. Per la matematica, estrarre in una cartella di lavoro lo ZIP originale. Estrarre separatamente il suo `verifiche_CTW_precedenti.zip`. Fornire la cartella esterna `HEXIS_v3_allegati` e quella interna `ctw_validation`:

   ```text
   python verifica_matematica.py /percorso/HEXIS_v3_allegati /percorso/storico/ctw_validation
   ```

   Lo script legge i pilot già esistenti ed esegue soltanto piccoli fit sintetici. L'output è numerico; lo script conserva l'asserzione sul caso razionale. I risultati osservati della sessione sono in `controlli_matematici.txt`.

3. Per i 25 sintetici piccoli, fornire la cartella storica e un percorso di output **nuovo**:

   ```text
   python verifica_sintetici.py /percorso/storico/ctw_validation /percorso/nuovo_risultato.json
   ```

   Lo script fallisce su soglia violata, mutazione del modello durante la valutazione o file di output già esistente. Non legge i CoNLL-U.

## Portata

I 120 casi di enumerazione e le prove più grandi precedenti restano evidenze del pacchetto originario, verificato per integrità. Il piccolo caso razionale e i 25 sintetici qui documentati sono controlli della presente revisione. Non vengono confusi con test di accettazione superati dalla futura implementazione della repository.

Il censimento nuovo conferma i valori sorgente. Non misura l'effetto dell'accorpamento sui punteggi reali: quella valutazione appartiene alla campagna futura dopo la migrazione del contratto.
