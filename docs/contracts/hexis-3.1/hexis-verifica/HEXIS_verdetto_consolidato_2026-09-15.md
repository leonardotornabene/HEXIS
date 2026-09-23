# HEXIS — Verdetto consolidato e compendio delle modifiche

**Data:** 15 settembre 2026.  
**Oggetto:** confronto del piano 3.0.1 con le due revisioni metodologiche, i dati fissati, gli allegati eseguibili e la repository.  
**Stato:** proposta consolidata di modifica, **non applicata e non ratificata**. Questo rapporto non sostituisce automaticamente le istruzioni v2.1 ancora presenti nella repository.

## 1. Verdetto

**Il ridimensionamento è valido. Il piano 3.0.1 richiede però una revisione sostanziale prima di diventare la base definitiva del nuovo proposal e della migrazione.** Non occorre cambiare nuovamente modello, ampliare il corpus o recuperare l'inferenza abbandonata.

La soluzione raccomandata è una sola:

1. Studio descrittivo del corpus greco fissato, limitato all'ordine **entro frase** delle annotazioni.
2. Accorpamento globale `PART`/`ADV`, dichiarato come perdita deliberata di dettaglio, senza attribuirgli una normalizzazione completa.
3. Risultato principale costituito dai **sette profili di blocco**, con gli undici documenti visibili; differenza HEX/prosa come sintesi subordinata e condizionata ai training disponibili.
4. CTW congelato, Q a quattro termini, rimescolamento accoppiato e JSD conservati.
5. Sei celle: `C0`, `a_total1`, `q_half`, `D12`, `oth`, `upos`. Eliminazione di D6, `rho09`, `bound` e delle valutazioni tragiche finali.
6. Persistenza dettagliata per posizione soltanto in C0; aggregati verificabili per le sensibilità. Un manifest e un controllo di completezza ristretto sostituiscono l'apparato di certificazione separata.
7. Correzione delle attestazioni sui pilot: **il contrasto a venti semi già ricostruibile è D_G originale, non un D_Q verificato a venti semi**.

Questa scelta porta da **1.400 a 980 modelli scientifici**, elimina **1.680 valutazioni probe** e riduce le righe posizionali persistite da **12.704.540 a 2.182.160**. La riduzione è rispettivamente del **30%** e dell'**82,82% delle sole righe posizionali**; non è una misura del risparmio totale di disco o tempo.

**Una volta recepite coerentemente le decisioni di questo rapporto, la progettazione può essere chiusa.** I controlli sull'implementazione restano obblighi di esecuzione; non richiedono un'ulteriore espansione metodologica. Il via libera alla scrittura del proposal non equivale al superamento anticipato dei test del software futuro.

## 2. Materiali, autorità e verifiche effettive

Denominazioni usate:

- **P:** [piano integrale 3.0.1](/Users/leonardoTornabene/Desktop/HEXIS_piano_integrale_v3_2026-09-11.md).
- **A:** [revisione metodologica del 14 settembre](/Users/leonardoTornabene/Desktop/HEXIS_3.0.1_revisione_metodologica.md).
- **B:** [seconda revisione, testo incollato](/Users/leonardoTornabene/.codex/attachments/74e30dc0-3390-4556-89b5-7a954c50c3e8/pasted-text.txt).
- **Pacchetto:** [allegati operativi](/Users/leonardoTornabene/Desktop/HEXIS_allegati_operativi_v3_2026-09-11.zip), inclusivo dell'archivio storico CTW.
- **Repository:** `/Users/leonardoTornabene/Projects/hexis`, ramo `g1/pre-audit`, HEAD `852644b6917790877c7b2ca5df2e76b17829d87c`.

Le prescrizioni di P, A e B sono state esaminate come contenuto da valutare. Non sono state usate per autorizzare fit reali, ratificare decisioni o modificare il progetto. Le verifiche hanno usato letture del corpus, ricalcoli di risultati archiviati, casi sintetici e la suite esistente. **Non sono stati eseguiti nuovi fit sui testi reali.**

### 2.1 Riscontri materiali

| Oggetto | Verifica di questa revisione | Esito |
|---|---|---|
| Piano esterno e copia nello ZIP | Confronto dei byte | Identici |
| Pacchetto corrente | SHA-256 dei 33 file inventariati | Tutti corrispondono |
| Archivio storico | SHA-256 dei 103 file inventariati | Tutti corrispondono |
| Tre CoNLL-U greci | SHA-256 dei file locali | Tutti corrispondono a P §3.1 |
| Corpus | Conteggio diretto dei token con ID intero, frasi e identità | 202.989 token; 13.919 frasi; 18 prefissi; 17 documenti |
| Tre codifiche originarie | Ricalcolo documentale di ritenzione, eleggibilità e inventari | Conteggi degli allegati confermati; m=106/112/12 |
| Accorpamento PART/ADV | Trasformazione senza fitting | m=100/105/11; stessa maschera e stesse coordinate |
| Repository | Stato Git e suite nell'ambiente presente | 327 passed, 17 skipped; solo `scripts/` non tracciato |
| CTW | Lettura delle formule e caso indipendente con enumerazione razionale | Predizione: errore massimo 1,11×10⁻¹⁶ nel caso aggiuntivo |
| Profondità | Controesempio sintetico con dipendenza oltre D8 | D6/D8 circa 1 bit; D12 circa 0,01771 bit |
| Pilot | Ispezione delle righe e del codice di produzione | 140 C0 originali; controllo storico rimescolato su 7 fold al solo seme 0 |

Il controllo razionale aggiuntivo non è la riesecuzione dei 120 casi storici: sono evidenze distinte. I risultati dei 120 casi e delle 9.189 asserzioni sono presenti negli allegati verificati. La batteria sintetica piccola è stata inoltre rieseguita con controlli sulle soglie effettive di P §12.1; i risultati sono nell'allegato di verifica.

I file di evidenza di questa revisione sono nella cartella `evidenze/` accanto al rapporto. Contengono conteggi, riscontri numerici e registrazione dei controlli, non il corpus grezzo.

### 2.2 La diversa forza probatoria delle revisioni

A ammette in §12 di non avere consultato né i tre CoNLL-U né la repository: le sue verifiche documentali del corpus erano controlli di coerenza degli allegati, integrati da totali pubblici. Non equivalgono a una ricostruzione dei dati sorgente. B ha individuato un problema che quei controlli non potevano rilevare, e il nuovo conteggio diretto lo conferma.

Entrambe le revisioni riconoscono correttamente la coerenza del nucleo CTW e la necessità della riduzione inferenziale. **B fornisce la base migliore per il perimetro finale. A contiene rilievi utili, ma anche extrapolazioni e alcuni errori che non vanno recepiti.**

## 3. Confronto ragionato: che cosa accogliere e che cosa correggere

| Questione | Riscontro contro P, dati o codice | Decisione consolidata |
|---|---|---|
| Studio finito e descrittivo | Compatibile con corpus, dipendenze fra opere e assenza di campionamento di popolazione | Accogliere entrambe |
| CTW e Q a quattro termini | Formule coerenti; la scorciatoia può invertire il segno | Conservare |
| Discontinuità PART/ADV, B | 11.270 PART nei due blocchi HEX, zero nei cinque prosastici | Correggere la rappresentazione prima del nuovo freeze |
| «Risultato finale già noto», A §§1–3 | I 20 semi contengono G originale; mancano gli shuffle accoppiati per estendere l'identità Q=G a tutta la campagna | Correggere; dichiarare il pilot G e la copertura effettiva del controllo |
| «D_Q non identificato», A §4 | La statistica descrittiva è definita; non è identificato un effetto separato di metro, epoca o esposizione | Restringere l'oggetto interpretativo, senza dichiarare il numero privo di significato |
| `balanced` identifica il contrasto, A §4.1 | Il 50/50 pareggia una quota ma cambia il budget; non pareggia autori, annotazione o somiglianza fra training e test | Non aggiungere la cella |
| Storia disponibile «esclusa» come problema, A §4.2 | Il ricalcolo riguarda G; due fasce non pareggiano le distribuzioni di frase. Con D12, ≥8 non satura neppure la profondità ammessa | Conservare le due fasce come diagnostica, senza co-primario |
| Profilo prima del contrasto, A e B | Coerente con il disegno effettivo | Accogliere, con sette blocchi e undici dettagli documentali |
| Riaggregazione senza opere, A §4.3 | Non rimuove quell'opera dai training degli altri fold | Non chiamarla leave-one-document-out né controllo di contaminazione; non renderla nuovo deliverable |
| Citazioni di Ateneo da `subdoc`, A §4.3 | Gli XML hanno riferimenti di passo, non marcatori di citazione | Non introdurre un censimento automatico non supportato dai dati |
| `deprel_only` attribuisce il fenomeno, A §5 | Task differenti non danno una decomposizione additiva del guadagno | Non aggiungere la cella |
| Stesso contrasto in UPOS e C0 implica nessun contributo DEPREL, A §5 | Stessa differenza fra medie può accompagnarsi a livelli e comportamenti molto diversi | Vietare questa deduzione; descrivere soltanto la concordanza osservata |
| Q=G «strutturale» e tutto G è ordine, A §6.1 | Identità numerica in alcuni fit, non proprietà generale né identificazione linguistica | Conservare quattro termini e bracci effettivi in ogni cella |
| D6=D8=D12 «per costruzione», A §6.3 | Il pilot D6 presenta anche scarti non nulli; esiste un controesempio sintetico netto | Togliere D6 per restringere il controllo; conservare D12 |
| Prior rho «inerte», A §6.4 | Variazioni reali e sintetiche verificabili | Fissare rho=0,5; eliminare la sensibilità dichiarando la rinuncia |
| `bound` inutile perché misura 10⁻⁷, A §6.5 | Nel pilot Diodoro cambia di circa −0,04781 bit | Eliminarla per limitare la domanda all'intrafrase, come propone B |
| Generalizzazioni sulle soglie, A §6.2 | A §12.5 ne riconosce correttamente la dipendenza dalla sorgente; alcune conclusioni del §6.2 eccedono comunque quella portata | Conservare il limite illustrato dai sintetici, senza costanti universali |
| G/CE0 rende confrontabili gli alfabeti, A §7 | È un rapporto rispetto a baseline diverse, non una scala universale | Non aggiungere la metrica |
| JSD pesata per token obbligatoria, A §7 | R1 e Q hanno popolazioni e domande distinte, già definite da P | Conservare R1 originale e conteggi non smussati |
| Rango 1/21 da reintrodurre, A §§3,7 | Calcolabile ma non necessario; non fornisce validità inferenziale | Mantenere il ritiro delle permutazioni di etichette |
| Probe tragico da eliminare, B | Aggiunge output e domanda scientifica senza essere un controllo metrico pulito | Accogliere |
| Sei celle, B | Conservano regolarizzazione locale, budget, profondità superiore e due scelte di rappresentazione | Accogliere |
| Persistenza ridotta, A | Fattibile, ma quattro somme da sole non ricostruiscono tutte le diagnostiche | Accogliere con il contratto minimo del §7 |
| Colonne shuffled omesse perché «costanti», A | La perdita di radice varia con il simbolo; l'uguaglianza col CTW non è garantita | Non imporre costanti; conservare le quattro perdite dove previste |
| Certificati separati da semplificare, A e B | Integrità e completezza sono verificabili con manifest e un validatore ristretto | Accogliere, conservando evidenze e vincoli sui byte |

### 3.1 L'errore quantitativo più rilevante della revisione A

Da `pilot_C0.json` si ricostruisce:

\[
\overline{D_{G^O}}=-0{,}1780246797\quad\text{bit/simbolo},
\]

con SD fra semi **0,0110277710** e intervallo osservato **[−0,1982444032; −0,1573585892]**. Queste quantità sono riproducibili. Il file storico `shuffle_results.json` e il suo produttore `verify_shuffle.py` coprono però soltanto **sette fold al seme 0**. Per quel seme il contrasto Q è circa **−0,1772407629** e coincide numericamente con quello G.

Non si può sostituire il controllo mancante negli altri 19 semi con la supposizione che dia lo stesso esito. Lo stesso problema riguarda le sensibilità storiche, che hanno sette righe originali ciascuna. La tabella di A etichettata D_Q per tutte le configurazioni è in realtà ricavata da G originale.

La formulazione corretta è quindi: **il pilot ha già mostrato una separazione di G originale; il controllo accoppiato disponibile è compatibile con Q=G nei casi verificati. Il risultato della nuova campagna, soprattutto dopo la modifica dell'alfabeto, non è ancora stato osservato.** Cambiare semi non cancella l'esposizione ai pilot; dichiararla non autorizza a inventare i risultati mancanti.

### 3.2 Perché le aggiunte di A non chiuderebbero i confondimenti

Il budget `balanced` di 18.564 token è ottenibile in linea di principio: il blocco esiodeo residuo limita il lato HEX a 9.282. Ma rispetto ai 53.304 token C0 cambia contemporaneamente esposizione e quantità di training. Inoltre va ancora definita la ripartizione fra blocchi: 9.282 non si divide esattamente per cinque o per quattro. Servirebbero una regola ulteriore e nuovi contratti. Un sintetico in cui 18.564 token bastano non certifica la sufficienza nel greco.

La quota 50/50 non separa annotazione, epoca, somiglianza tra opere e diversità dei contributori. La persistenza del segno non escluderebbe un effetto dell'esposizione. Si tratta di una diversa domanda possibile, non della correzione obbligata di questo studio descrittivo.

Analogamente, togliere Ateneo soltanto dalla media conserva Ateneo nei training dei punteggi degli altri blocchi. Togliere l'Iliade lascia il suo materiale nei training degli altri fold. Queste operazioni misurano l'influenza dei pesi sui punteggi già stimati, non una pipeline rifatta senza quelle opere. I profili documentali e i due schemi di peso già previsti rendono visibile la dominanza senza aggiungere undici contrasti.

## 4. Decisioni scientifiche da recepire

Gli identificativi C01–C30 costituiscono la lista operativa delle modifiche. Sono raccomandazioni concrete per la prossima revisione del contratto.

### C01 — Riscrivere domanda, titolo e promessa del progetto

Domanda di destinazione:

> Nel corpus greco UD Perseus fissato, quale vantaggio predittivo aggiuntivo offre l'ordine entro frase delle annotazioni rispetto al loro rimescolamento entro frase, sotto un CTW congelato addestrato sugli altri blocchi? Come variano i profili dei documenti e dei blocchi con rappresentazione, budget e scelte essenziali del predittore?

HEX/prosa rimane una lettura descrittiva di quei profili. Togliere dal titolo e dagli obiettivi le promesse di effetto del vincolo metrico, firma universale, memoria della grammatica, transfer fra regimi e generalizzazione al greco. Le etichette delle opere non certificano il metro di ogni passo. [P §§1,3.5,16]

### C02 — Stabilire una gerarchia unica dei risultati

- **Principale:** sette Q di blocco, insieme a G originale/rimescolato e alle quattro CE; gli undici documenti devono essere leggibili separatamente.
- **Sintesi subordinata:** D_Q a peso uguale fra blocchi, con D_G originale/rimescolato.
- **Seconda pesatura obbligatoria:** medesime quantità pesate per target eleggibili.
- **Diagnostiche:** due fasce di storia, supporti, masse, dati di training e ritenzione.
- **Lettura distribuzionale:** R1/JSD con la popolazione definita in P.

Non attribuire agli undici documenti il rango di undici repliche indipendenti. Conservare l'esclusione per blocco e la media per target dentro il blocco. La SD, il minimo e il massimo sui semi descrivono variabilità computazionale; non usare il simbolo ± senza specificarne il significato.

### C03 — Conservare le identità del corpus e togliere il probe dall'analisi finale

Conservare i tre file, il commit UD, gli hash, i 18 prefissi, i 17 documenti del censimento e gli undici primari in sette blocchi. Conservare nel registro i regimi originali `HEX`, `PROSE_CLASS`, `PROSE_POST`, `OTHER_VERSE`; `PROSE_ALL` è un raggruppamento di report delle due prose.

Le sei tragedie diventano **documenti censiti senza scoring finale**: nessun training, nessuna valutazione probe, nessuna figura tragica e nessuna conclusione di specificità rispetto alla tragedia. Conservare lo storico delle prove già eseguite, senza rinominarlo risultato finale.

Per evitare un'ulteriore variazione analitica, mantenere l'inventario alfabetico definito sull'intero censimento di 17 documenti. Va scritto esplicitamente: i sei documenti non valutati contribuiscono soltanto all'inventario dei tipi. Dopo l'accorpamento rimangono **9 tipi C0 e 10 tipi OTH esclusivi di quei documenti**, contro 10 e 12 prima; in UPOS nessuno. Il disegno rimane chiuso e transduttivo. **Non ridurre contestualmente il supporto ai soli primari:** darebbe altri alfabeti, 91/95/11.

### C04 — Accorpare globalmente PART e ADV

Applicare a tutte le rappresentazioni la mappa `PART → ADV_PART` e `ADV → ADV_PART`, dopo la verifica dei tag sorgente e senza condizionarla a lemma, opera o gruppo. `ADV_PART` è una categoria di progetto, non un nuovo tag UD. Conservare nel censimento gli UPOS originali.

| Variante | Prima | Dopo | Token/target |
|---|---:|---:|---|
| `ud23`, C0 | 106 | **100** | Invariati |
| `ud23_oth` | 112 | **105** | Invariati rispetto alla precedente `oth` |
| `upos_only` | 12 | **11** | Stessa maschera di C0 |

Il conteggio diretto conferma 9.884 PART nel blocco omerico e 1.386 in quello esiodeo. Per γάρ: 526 PART/13 ADV nel blocco omerico, 54/0 in quello esiodeo, e soltanto ADV nei cinque blocchi prosastici. **L'Inno a Demetra ha zero PART e contiene tutti i 13 γάρ ADV del blocco omerico:** l'associazione non è perfetta a livello documentale. Il rilievo riguarda l'annotazione disponibile, non la dimostrazione che ogni singola analisi sia errata. La documentazione AGDT del commit fissato riconosce il problema della distinzione avverbio/particella. [AGDT, nota di annotazione](https://github.com/PerseusDL/treebank_data/blob/bf4334f0af5e13d16b04c1cccd6237e683ac6f5f/v2.1/Greek/README.MD#L67)

L'accorpamento riduce una distinzione applicata in modo discontinuo. Non uniforma CCONJ, DEPREL o tutte le particelle: δέ e τε rimangono esempi di eterogeneità residua. Non correggere i token con euristiche basate sul lemma e non avviare una riannotazione manuale. Mantenere nel report il limite di comparabilità anche dopo l'accorpamento.

### C05 — Propagare davvero il nuovo alfabeto

Rigenerare liste lessicografiche, ID, hash, configurazione e aspettative dei test. I nomi storici `ud23`, `ud23_oth`, `upos_only` possono restare, ma la versione della rappresentazione deve indicare l'accorpamento: stesso nome di variante non significa stessi byte né stesso modello.

Con a=0,5 per simbolo le masse Dirichlet diventano **50, 52,5 e 5,5**, rispettivamente; in `a_total1` C0 usa **a=1/100**, non 1/106. Anche lo smoothing R1 deve usare il nuovo m. Non riutilizzare i vecchi modelli o i loro score. I ledger sorgente possono restare uguali quando maschere e permutazioni coincidono; vanno riconvalidati contro le nuove coordinate e il nuovo contratto.

Questa scelta modifica il task e il prior totale: non presentare l'eventuale differenza dal pilot come misura pura dell'effetto PART/ADV. Non aggiungere una cella finale con l'alfabeto precedente: conservarne i risultati come sviluppo storico.

### C06 — Rendere l'audit annotativo e della ritenzione informativo

Riportare per documento e blocco: conteggi UPOS/DEPREL sorgente, token eliminati con causa, ritenzione grezzo→codificato, eleggibili/codificati, frasi senza target e lunghezze codificate. Rendere visibili i controlli A e B anche nei blocchi primari, non soltanto nella tragedia.

Correzioni verificate:

- Nel corpus sono presenti **27 DEPREL base e 28 etichette contando `nsubj:outer`**, non 29+1 come scrive A.
- `PROPN` e `SYM` hanno zero occorrenze; anche le frasi vuote dopo codifica sono zero. Conservare la gestione dei casi limite nei test; non descrivere il mapping PROPN come trasformazione effettivamente avvenuta.
- `discourse` compare su 374 token, tutti `INTJ`: è già escluso dalla maschera UPOS. `oth` non recupera questi token. Il problema delle relazioni eliminate non va descritto come se `oth` conservasse tutto ciò che C0 scarta.
- I `vocative` con UPOS ammesso eliminati sono 459 nel blocco omerico e 26 in quello esiodeo: circa **0,560% e 0,242% dei rispettivi token grezzi**. Riportare i valori effettivi, senza definirli a priori le relazioni «più caratteristiche» della poesia.

Le soglie convenzionali >2% e ritenzione <70% possono restare semplici segnalazioni. Non costituiscono un certificato di omogeneità annotativa. Hash e conteggi attesi, invece, sono controlli di identità che devono fallire sulle discrepanze.

### C07 — Conservare il training per blocco e descriverne esattamente l'esposizione

Mantenere q=8.884 per ciascuno dei sei contributori, 53.304 token totali; `q_half` usa 4.442 e 26.652. Nessun blocco held-out, o suo documento, entra nel training.

| Test | HEX nel training | Prosa nel training | Gruppo del test nel training |
|---|---:|---:|---:|
| HEX | 1/6 | 5/6 | 1/6 |
| Prosa | 2/6 | 4/6 | 4/6 |

Inserire questa tabella nel metodo e vicino al contrasto, senza affermare una direzione necessaria dello scarto. Nessuna cella `balanced`, nessun modello comune aggiuntivo, nessun fit per regime.

Plutarco contribuisce tutti i suoi 8.884 token in C0 quando non è held-out: il multinsieme di training originale e i suoi conteggi sono fissi, ma il ledger può avere ordine diverso e il **rimescolamento continua a variare**. Correggere la formula troppo generale di A sul contributo «deterministico su tutti i semi».

### C08 — Conservare il campionamento, senza riaprire i frammenti

Mantenere permutazione delle frasi, budget esatto e al massimo un frammento per blocco contribuente. Un frammento è uno stream autonomo: non eredita la storia della porzione esclusa. Conservare coordinate, ragione del taglio, sottoseme e metriche già richieste da P §5.2.

Le celle numeriche e UPOS riusano il ledger C0; `q_half` condivide l'ordine delle frasi ma non promette annidamento dei token; `oth` può fermarsi altrove. Non aggiungere un nuovo confronto a frasi intere: l'ablazione pregressa resta una prova locale di sviluppo, non una garanzia generale.

### C09 — Fissare la popolazione dei target e lasciare le fasce secondarie

Conservare `available_past ≥ 4` entro la frase codificata. In C0 sono valutati **53.009/80.370 = 65,96%** dei token HEX trattenuti e **56.099/73.930 = 75,88%** di quelli prosastici. Scrivere che il risultato riguarda posizioni interne e pesa maggiormente le frasi lunghe.

Le fasce restano **4–7** e **≥8**, con conteggi e tutte le componenti di Q, per ogni cella e braccio. Non creare co-primari, matching di lunghezza o nuove standardizzazioni. In D12 la fascia ≥8 non significa disponibilità di tutti i dodici predecessori. Il ricalcolo di A sulla fascia ≥8 mostra una persistenza di D_G nel pilot, non elimina tutti gli effetti della segmentazione.

### C10 — Conservare Q e restringerne l'interpretazione

\[
Q=(CE_0^O-CE_{CTW}^O)-(CE_0^R-CE_{CTW}^R).
\]

Conservare rimescolamento di training **e** test entro ciascuna frase/frammento, nuovo adattamento del braccio rimescolato e accoppiamento per slot. Permutare il simbolo composito intero; non UPOS e DEPREL separatamente. La provenienza del token spostato è diversa dalla coordinata dello slot valutato.

Le radici del training dei due bracci hanno gli stessi conteggi. Le CE0 sul test eleggibile possono differire perché lo shuffle muove simboli attraverso il limite dei primi quattro slot. Il controesempio del pacchetto dà Q≈0,71346 e scorciatoia≈−0,66505.

Uno shuffle per seme resta sufficiente al perimetro scelto: 20 C0, 10 per sensibilità. Non ripetere fino a ottenere un cambiamento o un segno gradito. Non porre `G_R=0` come test di accettazione. Q positivo descrive il vantaggio relativo rispetto a quella trasformazione, non identifica da solo sintassi, metro o un ordine linguistico depurato dalle convenzioni annotative.

### C11 — Ridurre e congelare le sei celle

| Cella | m | D | a per simbolo | rho | q per contributore | Semi | Modelli O+R |
|---|---:|---:|---:|---:|---:|---:|---:|
| C0 | 100 | 8 | 0,5 | 0,5 | 8.884 | 20 | 280 |
| a_total1 | 100 | 8 | 0,01 | 0,5 | 8.884 | 10 | 140 |
| q_half | 100 | 8 | 0,5 | 0,5 | 4.442 | 10 | 140 |
| D12 | 100 | 12 | 0,5 | 0,5 | 8.884 | 10 | 140 |
| oth | 105 | 8 | 0,5 | 0,5 | 8.884 | 10 | 140 |
| upos | 11 | 8 | 0,5 | 0,5 | 8.884 | 10 | 140 |
| **Totale** | | | | | | | **980** |

Conservare master seed 20260706, indici C0 0–19, sensibilità 0–9 e convenzione SHA-256/PCG64 `hexis-v3-rng-1`. Accoppiare le sensibilità ai **primi dieci** C0, non alla media C0 su venti.

Le rinunce vanno esplicitate: eliminando `rho09` non si valuta più la sensibilità al prior arresto/suddivisione; `a_total1` riguarda un altro prior. Eliminando `bound` non si valuta più la dipendenza dai confini. D12 resta un controllo unilaterale sull'aumento della profondità, non un'esplorazione completa di D.

Non scegliere i tagli perché producono risultati simili nel pilot. Si tagliano domande accessorie e si conservano le quattro cause essenziali di dipendenza del punteggio: regolarizzazione locale, budget, profondità ammessa e rappresentazione.

### C12 — Conservare R1 senza nuove famiglie di JSD

Per ciascuna delle tre rappresentazioni aggiornate, conservare conteggi completi originali dei sette blocchi, frequenze non smussate, distribuzioni con pseudoconteggio 0,5, 21 coppie, matrice 7×7, centroidi a peso uniforme fra blocchi e contributi dei simboli. JSD in bit, diagonale zero, simmetria, range [0,1] e trattamento corretto di `0 log 0`.

Non cambiare automaticamente i pesi di R1 perché Q ha anche una sintesi per target: R1 descrive tutti i token trattenuti, Q una popolazione eleggibile. La differenza è dichiarata, non incoerente. Non aggiungere JSD dei soli target, JSD dei probe, nuovi centroidi, test o clustering. R1 non corregge né convalida Q. [P §8.3; Lin, 1991](https://www.cise.ufl.edu/~anand/sp06/jensen-shannon.pdf)

## 5. CTW, diagnostica e precisione: che cosa mantenere e correggere

### C13 — Conservare il contratto matematico, sostituendo il vecchio selettore

Portare il CTW a esiti non binari: evidenza Dirichlet, miscela arresto/suddivisione, foglie forzate a D, BOS terminale soltanto nei contesti, sottoalberi vuoti con evidenza unitaria e predizione uniforme. Conservare la partizione esatta dei conteggi e la predizione congelata durante tutta la valutazione.

Non importare il prototipo come dipendenza di produzione e non importare `candidates/`. Il riferimento e le fixture indipendenti servono alla verifica del porting. Eliminare dal percorso attivo `monotone-stop`, `argmax`, `k_min`, `gamma`, la profondità selezionata e la penalità aggiuntiva. Il fondamento CTW/BCT non impone il ritorno all'inferenza fra regimi. [Kontoyiannis et al., 2022](https://academic.oup.com/jrsssb/article/84/4/1287/7073257)

Tolto `bound`, **SEP non è richiesto nella nuova API scientifica**. Conservare BOS e reset; il supporto SEP del riferimento resta nella storia delle verifiche. Non mantenere un flag di collegamento nascosto né il vecchio `#` come esito predetto.

### C14 — Correggere la semantica della profondità

`L_resolved` descrive la lunghezza dei contesti osservati a cui la miscela assegna massa, condizionata alla massa osservata. Un nodo con una sola osservazione è comunque osservato. La quantità non misura precisione, affidabilità, profondità grammaticale o limite massimo di memoria recuperabile.

Inoltre le masse λ lungo il cammino sono **pesi della miscela**, non la quota attribuibile a ciascun contesto della probabilità del simbolo effettivamente visto. Quest'ultima dipenderebbe anche da `p_s(x)`. Non aggiungere una nuova diagnostica di responsabilità: correggere il linguaggio.

Conservare istogrammi dei supporti e delle masse, `unseen_mass`, numero di simboli di radice non osservati in training e relative quote sul test. Definire l'aggregazione delle diagnostiche: media dei valori per posizione con numero esplicito di valori validi; non confonderla con il rapporto tra masse sommate. `resolved_mean=null` deve avere motivo `no_resolved_mass`; fasce vuote devono avere score null con motivo e conteggio zero.

### C15 — Evitare conclusioni errate dagli zeri numerici

Nei **nodi non forzati**, con evidenze finite e prior interno a (0,1), entrambe le componenti della miscela sono positive in aritmetica esatta. Il peso 1,0 memorizzato può essere una saturazione numerica sostenuta da evidenza molto forte; non trasforma il CTW in un selettore discreto. Nelle foglie forzate a D o sotto BOS, invece, il peso di arresto 1 è matematicamente prescritto.

A chiama ~37 nat una soglia di underflow di `log1p(exp(x))`: è sbagliato. `log1p(exp(-37))` resta circa 8,53×10⁻¹⁷; l'underflow dell'esponenziale float64 avviene verso −745/−746. Intorno a **37 nat di differenza fra log-componenti** può invece perdersi la componente piccola sommata a 1; sottrarre grandi log-evidenze introduce ulteriori perdite di precisione.

Usare operazioni stabili sui log e controlli espliciti, come richiesto da P. Ricavare **entrambi** i pesi posteriori dalla differenza fra i due log-contributi, evitando di ottenere il peso piccolo soltanto come `1-stop`; non affidarsi a un `min(1, ...)` indiscriminato. Conservare `root_stop` e, per interpretarne la saturazione, la differenza fra log-contributo di arresto e di suddivisione alla radice. Specificarne segno e unità in nats; le perdite restano in bit.

Non costruire il prior estremo della letteratura come `1-2**(-(m-1))` in float. Il caso deve restare un test numerico, anche se non è una cella finale. Nessun test deve imporre che lo shuffle collassi o che un D maggiore dia lo stesso risultato.

### C16 — Conservare i sintetici senza trasformarli in una soglia del greco

Mantenere i 25 casi piccoli con generatori e semi fissati: uniforme a quattro simboli, ciclo, Markov 1, dipendenza lag 2, memoria variabile. Conservare soglie 0,02 per uniforme/ciclo e 0,03 per gli altri confronti prescritti. Il gate deve fallire su una violazione: un campo JSON `analytic_pass=false` con exit riuscita non basta.

Conservare lo stress storico m=106 come riferimento verificabile e dichiararlo **stress storico**, non alfabeto C0 nuovo. Coprire inoltre gli m effettivi 100/105/11 nei controlli parametrizzati di normalizzazione, input e supporto; non inventare un'ulteriore campagna di calibrazione o nuove soglie empiriche.

Il deficit dello stress lag 2 a 106 simboli dimostra che rappresentare una dipendenza non basta ad apprenderla nel campione. I valori di rilevabilità costruiti da A su una sorgente specifica non diventano costanti del greco. Il rapporto 106/5 rispetto all'alfabeto di Galves è circa 21,2, non letteralmente cento: descrivere la differenza di dimensione senza l'espressione «due ordini di grandezza».

### C17 — Non trasformare il riuso dei conteggi in una riduzione dei modelli

Variare a o rho può riusare i conteggi, ma richiede nuove evidenze, nuovi pesi e nuova valutazione. Un modello a profondità inferiore può derivare dai conteggi D12 **solo** imponendo le foglie corrette e ricalcolando le evidenze e i pesi. Tagliare il percorso di predizione mantenendo i pesi D12 non è equivalente.

Questa è un'ottimizzazione facoltativa di implementazione, da usare soltanto se semplice e verificata; non fa parte delle economie necessarie. La campagna ha sempre **980 identità di modello**, anche quando parte dei conteggi viene riusata. Evitare un sistema di cache generale o un livello di astrazione aggiuntivo solo per risparmiare fit già brevi.

### C18 — Trattare l'instabilità di Diodoro proporzionatamente

Il calo storico di circa 0,048 bit sotto `bound` o prior estremo è reale; non dimostra da solo un bug né l'attivazione di un singolo «commutatore». Una miscela continua può essere molto sensibile a piccole variazioni dell'evidenza.

Conservare l'osservazione nel resoconto dei pilot. La pipeline finale deve mostrare Diodoro come ogni altro blocco nelle celle rimaste e fornire le diagnostiche comuni. Non subordinare la chiusura a una ricerca filologica o a un lessico di nodi «responsabili» di configurazioni ritirate. Se i controlli di identità o numerici falliscono, correggere il bug; una variazione finita e coerente dei punteggi non è di per sé un fallimento tecnico.

## 6. Stato epistemico, interpretazioni e bibliografia

### C19 — Rendere preciso il resoconto dello sviluppo

Nella nuova specifica, nel proposal e nel report finale distinguere:

1. Pilot originali C0 e sensibilità, con vecchio alfabeto e convenzione di semi.
2. Controlli rimescolati effettivamente disponibili, con semi e celle coperti.
3. Prove successive del contratto e ripetizioni di ambiente.
4. Nuova campagna con rappresentazione accorpata e contratto integrato.

Non descrivere il nuovo protocollo come preregistrazione precedente a qualsiasi osservazione. Non chiamare i fit finali una mera replica identica se cambia l'alfabeto. Non cambiare la regola analitica o il numero di semi per conservare la separazione storica.

L'allegato sulle autorizzazioni pregresse è un resoconto di sessione, non una verifica indipendente del consenso originario. Nella migrazione riportarne fonte e grado di verificabilità; non inventare orari e non dichiarare un passaggio retroattivo di G2. Il presente audit non aggiunge un'autorizzazione a nuovi fit reali.

### C20 — Completare le regole delle conclusioni

Conservare risultati negativi o instabili come esiti legittimi. Aggiungere esplicitamente:

- Accorpamento annotativo riuscito tecnicamente ≠ omogeneità linguistica dimostrata.
- C0 e UPOS con contrasti simili: **concordanza della sintesi in due rappresentazioni**, non prova che DEPREL non contribuisca.
- Profili o segni diversi fra pesature: dipendenza dalla distribuzione dei target, non scelta del peso «giusto».
- G_R numericamente nullo: comportamento osservato del predittore sotto quel controllo, non teorema sull'ordine.
- D8/D12 simili: assenza di miglioramento nelle configurazioni valutate, non assenza di dipendenze oltre otto simboli.
- Assenza dei probe: nessuna conclusione finale sulla specificità rispetto ad altri metri.

Non aggiungere G/CE0, `deprel_only`, ranghi permutazionali o nuove riaggregazioni per tentare un'attribuzione che il disegno non sostiene.

### C21 — Correggere e accorciare il registro bibliografico attivo

Usare poche fonti direttamente pertinenti, conservando lo storico del registro. Correzioni da applicare:

- **Kontoyiannis et al.**: citazione pubblicata in *JRSS B* **84(4), 2022, 1287–1323**, DOI **10.1111/rssb.12511**. La preprint è una fonte primaria anch'essa; il problema era l'incompletezza bibliografica, non l'uso di una fonte secondaria. [Editore](https://academic.oup.com/jrsssb/article/84/4/1287/7073257)
- **Gianitsos et al.**: *Proceedings of the 3rd Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature*, **52–60**, 2019; DOI **10.18653/v1/W19-2507**. [ACL](https://aclanthology.org/W19-2507/)
- **Gorman e Gorman**: le pagine **500–510** sono confermate direttamente dal deposito degli autori; non restano una questione aperta. [Deposito](https://digitalcommons.unl.edu/historyfacpub/208/)
- **Herrera et al.**: il PDF v1 citato dal piano ha quattro autori; la versione aggiornata v2 aggiunge **Caio Corro**. Non è corretto accusare il piano di avere omesso un autore del v1. Per il nuovo testo usare la versione corrente, dopo averne registrato il cambio di versione, oppure mantenere un collegamento esplicito al v1 esaminato. Raccomandazione di destinazione: citare **Herrera, Silai, Corro, Guillaume, Kahane**, QUASY 2025, **26–38**, collegando il v2. [v1](https://aclanthology.org/2025.quasy-1.5v1.pdf), [v2](https://aclanthology.org/2025.quasy-1.5v2.pdf)
- Le informazioni bibliografiche di **Galves**, **Schürmann–Grassberger**, **Lin** e **de Marneffe et al.** risultano coerenti con le fonti primarie consultate. [Galves](https://arxiv.org/abs/0902.3619), [Schürmann–Grassberger](https://arxiv.org/abs/cond-mat/0203436), [de Marneffe](https://aclanthology.org/2021.cl-2.11/)

Registrare nella nuova versione le fonti del CTW e della stilometria greca introdotte dal piano ma non ancora allineate al vecchio registro. Eliminare obblighi di citazione legati a risultati latini, transfer o stimatori ritirati quando non svolgono più una funzione nel testo. Non attribuire a un precedente né il contratto BOS di HEXIS né una certificazione della qualità del corpus.

## 7. Riduzione di output, governance e implementazione

### C22 — Ridurre la persistenza, mantenendo ciò che permette di controllare Q

**C0:** conservare tutte le 2.182.160 righe accoppiate per slot, con le quattro perdite float64, coordinate, simbolo originale e rimescolato, provenienza dello shuffle e diagnostiche per posizione già definite. Non omettere le perdite rimescolate assumendo che coincidano con la radice.

**Sensibilità:** conservare un aggregato per documento/seme/cella/fascia di storia, con n e **quattro somme delle perdite**; conservare inoltre i sufficienti riepiloghi delle diagnostiche previste, non soltanto CE arrotondate. In particolare, per ciascun braccio: **somma dei `resolved_mean` validi e loro conteggio**, conteggi null, somme delle masse per lunghezza, somma della massa non osservata, supporti del modello, conteggi di target non visti alla radice e diagnostiche dello shuffle. Conservare i ledger e le informazioni necessarie a rigenerare i punteggi.

Le aggregazioni di blocco e di gruppo si ricostruiscono da somme e denominatori. Media, SD, minimo e massimo sui semi si calcolano dopo le aggregazioni per seme. Non fare medie di medie non pesate dentro il blocco.

**Costo epistemico esplicito:** per le sensibilità non conservate per posizione, una verifica successiva di una singola perdita richiede la rigenerazione dal ledger. Non promettere che ogni vettore sia ricostruibile dalle sole somme. Gli hash attestano l'identità dei byte, non la correttezza del calcolo; servono anche fixture indipendenti e una rigenerazione deterministica di casi prefissati.

Il controllo di uguaglianza degli slot fra bracci rimane obbligatorio **prima dell'aggregazione**, anche quando i vettori vengono poi scartati. Gli istogrammi necessari a una figura non si possono ricostruire dalle sole quattro somme: devono essere raccolti durante la valutazione.

### C23 — Semplificare i comandi e le tabelle

Usare un solo esecutore parametrizzato per C0 e per le cinque sensibilità. `run_sensitivity` non necessita di un'orchestrazione distinta: può essere ritirato dal percorso di destinazione, lasciando la selezione delle celle al contratto o a un argomento verificato. Non introdurre un nuovo framework di workflow.

Conservare le responsabilità: audit/codifica, validazione, esecuzione descrittiva e report. Le tabelle documentali e di blocco sono gli input verificabili; contrasti, riepiloghi e figure sono derivati dal medesimo report. Evitare più implementazioni della stessa aggregazione.

Conservare **cinque figure** del piano, aggiornate: corpus/annotazione; profili G/Q con dettaglio documentale; sensibilità e due pesature; R1; supporti e masse del modello. Eliminare la figura tragica. Le fasce di storia entrano nelle tabelle e nei pannelli esistenti, senza creare un nuovo apparato grafico.

### C24 — Conservare la catena di verifica, togliere i certificati separati

Mantenere `design_lock.json` come riferimento depositato, un manifest per run e un validatore del report. Le fasi V0–V5 possono restare come checklist ordinata, ma non richiedono file di certificazione autonomi, firme o un sistema generale di attestazioni.

Il manifest contiene: hash di contratto/dati/registro/alfabeti/codice/lock, versione RNG, identità delle esecuzioni, elenco esatto degli artefatti con hash/dimensioni/schemi/cardinalità e risultati dei controlli con riferimento al contesto verificato. Conservare l'identità deterministica `run_id` calcolata dal contratto canonico; timestamp, macchina e percorsi locali rimangono metadati esterni, senza entrare nel run_id o nei semi. Uno stato `PASS` scritto a mano non sostituisce evidenze di verifica.

`run_report` continua a rifiutare risultati finali incompleti: confronto per **uguaglianza degli insiemi di chiavi**, rilevazione dei duplicati, verifica dei byte, denominatori e ricostruzione delle somme. Restano disponibili gli output individuali per diagnosticare gli errori. Non servono certificati annidati per ottenere queste proprietà.

### C25 — Ricalcolare tutti i numeri operativi e i controlli di completezza

| Quantità | Nuovo valore |
|---|---:|
| Celle | 6 |
| Coppie fold/seme/cella | 490 |
| Identità di modello, due bracci | **980** |
| Coppie C0 | 140 |
| Coppie sensibilità | 350 |
| Righe documento/seme/cella/braccio, prima delle fasce | 1.540 |
| Prova tecnica a un seme per cella, due bracci | **84 modelli**, 42 coppie |
| Valutazioni probe | **0** |
| Righe accoppiate se si persistessero tutte le sei celle | 7.643.640 |
| Righe accoppiate effettivamente richieste, solo C0 | **2.182.160** |
| R1 | 3 rappresentazioni × 21 coppie, più centroidi/contributi |

Non usare 980 o 84 come unico controllo: generare le chiavi attese da contratto, fold, bracci e semi. Gli 84 modelli tecnici possono contribuire ai 980 soltanto se prodotti con identici codice, contratto e schema definitivo. Nessuna somma di output di versioni diverse.

Aggiornare schema e contenuto di tutti gli allegati dipendenti da questi numeri; togliere probe e SEP dalle aspettative. La stima di 921 MiB del piano è aritmeticamente corretta per lo schema vecchio, ma non è più il fabbisogno nuovo. Il corpo numerico delle sole righe C0, ipotizzando ancora 76 byte/riga, è circa 158,2 MiB prima di overhead: non è un benchmark né un requisito RAM. Misurare tempo, memoria e spazio nella prova integrata; non inventare una nuova stima di giornate più precisa dei dati disponibili.

### C26 — Mantenere scritture sicure, ripresa e provenienza del codice

Scrivere temporaneamente, verificare e rinominare atomicamente; niente sovrascritture silenziose. Riutilizzare una partizione soltanto se identità, hash e cardinalità coincidono. Nessuna esclusione automatica di blocchi o semi problematici.

Un commit non identifica eventuali modifiche non committate o file non tracciati importati durante il run. Per la campagna finale richiedere uno stato del codice tracciato pulito e nessun produttore scientifico dipendente da file non tracciati, oppure registrare esplicitamente un'identità dei sorgenti che li comprenda. Per questo progetto la prima strada è la più semplice. Gli script locali estranei e i dati ignorati non devono essere cancellati per ottenere questo requisito.

### C27 — Migrare il codice sulla base di ciò che esiste davvero

Il piano sottostima alcune parti già funzionanti e suggerisce un riuso troppo diretto di altre. Mappa di destinazione:

| Percorso | Azione necessaria |
|---|---|
| `src/hexis/conllu_reader.py` | Riutilizzare parsing e controlli validi; completare identità/ordine/coordinate richiesti dal registro nuovo |
| `src/hexis/registry.py` | Applicare registro verificato, parti, ruoli e sette blocchi; mantenere separati regime originale e gruppo del report |
| `src/hexis/alphabet.py` | Aggiungere accorpamento; errori su tag ignoti; inventario lessicografico congelato; ritenzione documentale verificabile |
| `src/hexis/sequences.py` | Sostituire la vecchia semantica di concatenazione e `#` predetto con stream per frase/frammento, reset e coordinate; nessun SEP attivo |
| `src/hexis/config.py` | Conservare YAML sicuro e rifiuto dei duplicati; sostituire lo schema metodologico e completare tipi/intervalli/valori finiti |
| `src/hexis/model/context_tree.py` | Implementare CTW canonico al posto dello stub; API congelata e numerica controllata |
| `src/hexis/model/diagnostics.py` | Implementare masse/supporti e null motivati; ritirare profondità selezionata |
| `src/hexis/protocols/sampling.py` | Implementare campionamento e RNG dal contratto, riuso ledger, frammenti e shuffle |
| `src/hexis/protocols/scores.py` | Implementare perdite, accoppiamento, somme e Q; core indipendente dai gruppi |
| `src/hexis/manifest.py` | Riutilizzare identità e provenienza valide; aggiungere atomicità/ripresa/completeness richieste |
| `src/hexis/pipeline/run_audit.py` | Conservare difese già verificate; separare identità dei dati dai vecchi gate metodologici |
| `run_encode.py`, `run_tree_validation.py` | Completare stadi pubblicizzati soltanto quando operativi |
| Nuovi `run_descriptive.py`, `run_report.py` | Un esecutore delle sei celle e un report unico, senza contrasto finale parziale |
| `run_confirmatory.py`, `run_null_calibration.py`, `run_reference.py`, `run_latin.py` | Ritirare entry point e obblighi attivi; nessuna chiamata nascosta |
| `run_sensitivity.py` | Ritirare l'entry point dalla destinazione documentata; le sei celle usano il medesimo esecutore |
| `model/lexicon.py`, `blocks.py` | Ritirare lessico e chunk dal percorso scientifico; non confondere chunk con blocchi di dipendenza |
| `stats/permutation.py`, `bootstrap.py`, `holm.py` | Conservare utility e test validi come codice storico, senza import nella pipeline descrittiva |
| `viz/plots.py` | Solo cinque figure derivate dalle tabelle verificate |
| `tests/`, `conftest.py`, configurazione pytest | Riallineare inventario e controlli ai contratti nuovi; vietare skip nei controlli di accettazione attivi. Non risulta un workflow CI tracciato: non inventare attestazioni di CI né renderne l'aggiunta obbligatoria |
| `pyproject.toml`, `uv.lock` | Aggiornare descrizione e metadati necessari; conservare lo stack senza nuove librerie né downgrade immotivati |
| `.gitignore`, `LICENSE` e indicazioni di licenza | Tenere fuori da Git gli output voluminosi di lavoro; distinguere codice, documenti, dati sorgente e artefatti destinati alla pubblicazione |
| `scripts/reacquire_raw_data.sh` | Preservare l'originale locale; verificarne e correggerne l'eventuale versione di destinazione prima di pubblicizzarla |

Tre precisazioni concrete:

1. `config.py` **non** verifica soltanto la presenza: rifiuta già chiavi ignote/mancanti e alcune strutture G1. Mancano validazioni adeguate dei parametri futuri; esempi attualmente accettabili includono valori metodologici fuori contratto e NaN. Riutilizzare i controlli funzionanti, non riscrivere tutto.
2. Il vecchio `observed_alphabet` ordina per frequenza; il piano nuovo richiede ordine lessicografico. Il comportamento vecchio di `map_token` scarta un UPOS sconosciuto, mentre il contratto nuovo deve segnalarlo come errore.
3. Le utility statistiche sono implementate; molti moduli scientifici sono invece stub. I 327 test passati non attestano il CTW nuovo. Ritirare un comando non significa lasciarlo nella documentazione con `NotImplementedError`.

L'attuale script di acquisizione esiste ed è leggibile, ma non è tracciato. Legge la provenienza da `data/raw/PROVENANCE.md`, acquisisce greco e latino e controlla i file presenti senza confrontarli con l'insieme dei tre attesi. Ha un ramo `SKIP` per l'hash mancante, ma `set -euo pipefail` può arrestarlo prima: non è una gestione esplicita e verificata degli errori. Una riproduzione in checkout pulito deve disporre della provenienza **tracciata fuori da raw**, acquisire soltanto il greco richiesto e verificare esattamente i tre nomi attesi. Deve fallire su file atteso assente, extra, hash atteso mancante o record ambiguo. Non eseguire oggi lo script per colmare queste lacune: i dati presenti sono già verificati.

La documentazione deve distinguere i dati conservati localmente dagli artefatti effettivamente distribuiti. Non assegnare automaticamente ai simboli e alle coordinate per posizione la licenza del codice. La pubblicazione esterna rimane una fase successiva, con provenienza e condizioni dei materiali dichiarate; questo rapporto non ridistribuisce i raw né decide la qualificazione giuridica dei dati derivati.

### C28 — Portare i test prima delle nuove implementazioni

Mantenere le proprietà pertinenti, sostituendo i vecchi obblighi metodologici con motivazione esplicita. Minimo necessario:

- Hash, identità e conteggi del corpus; accorpamento, m100/105/11, maschere e coordinate.
- Tipi rigorosi: niente bool come interi, float convertiti silenziosamente, NaN/Inf, simboli fuori alfabeto, duplicati o chiavi ignote.
- Campioni esatti, nessuna contaminazione held-out, frammenti, semi, riuso ledger e invarianza all'ordine dei record/alle etichette.
- Enumerazione indipendente di alberi piccoli, partizione con BOS, normalizzazione, training vuoto, D=0, identità prequenziale e assenza di aggiornamento del test.
- Sintetici alle soglie effettive, prior estremi, supporto raro; nessun requisito di buon risultato sul greco.
- Shuffle e Q a quattro termini, allineamento degli slot e ricostruzione da somme alle due pesature.
- Fasce vuote/null, masse e supporti, JSD e contributi.
- Rifiuto di campagna incompleta o corrotta, chiavi duplicate/aggiuntive, ripresa e scrittura interrotta.
- Ricostruzione completa C0 dai vettori; per le sensibilità, verifica degli aggregati e rigenerazione di coppie prefissate, senza pretendere informazioni non persistite.

Non trasformare T24 sui probe in un test saltato: sostituirlo con il controllo che quei documenti non vengano addestrati né valutati e abbiano soltanto il ruolo censimento/inventario. Aggiornare T25/T30 a 980, T04 agli alfabeti nuovi e tutti i riferimenti ai certificati/SEP. Non indebolire i controlli generici ancora validi per ottenere una suite verde.

### C29 — Riallineare in un atto unico la documentazione normativa

Depositare una decisione nel namespace **V3-001** che sostituisca esplicitamente v2.1 per le esecuzioni nuove e recepisca questa revisione del piano 3.0.1. Attribuire al nuovo contratto una versione diversa; raccomandazione: **3.1**, perché cambiano rappresentazione, risultato principale e output, non soltanto refusi.

Aggiornare insieme:

- `docs/01_MASTER_SPEC.md`, `docs/02_DECISION_LOG.md`, `docs/03_ROADMAP_OPERATIVA_IT.md` e registro bibliografico;
- `docs/00_LEGGIMI_INDICE.md`, `docs/HANDOFF.md` e `docs/04_AI_HANDOFF_PROMPT.md`;
- `AGENTS.md`, `CLAUDE.md`, `README.md`, configurazione, registro, metadati del pacchetto e inventario test;
- contratto strutturato, attese di corpus, alfabeti, design lock e contratti di report presenti negli allegati.

Conservare D01–D54, D55 proposto e le ratifiche tecniche G1 come storia con stato chiaro. Nessuna clausola ritirata deve restare implicitamente vincolante: P1/P2 confermativi, latino, O7, soglie permutazionali, 13 celle, obblighi di sign-stability e vecchi gate vanno dichiarati **non applicabili alla nuova versione**, non «risolti» nel vecchio progetto.

Preservare espressamente immutabilità dei raw, provenienza, core senza etichette, quarantena dei candidati, test reali e divieto di sovrascrittura silenziosa. Le due revisioni rimangono documenti critici storici; non diventano fonti normative concorrenti con la specifica consolidata.

### C30 — Separare la chiusura del progetto dalla certificazione dei risultati

**Prima del nuovo proposal e dell'allineamento sostanziale del README:** recepire tutte le decisioni C01–C30 nel contratto di destinazione, con matrice, numeri, output e ruoli senza alternative residue. È possibile redigere una proposta metodologica prima di eseguire la campagna; deve dire che l'implementazione è in corso.

**Prima di dichiarare disponibile la pipeline:** applicare C22–C28 e superare i relativi controlli. Il README deve pubblicizzare soltanto i comandi realmente implementati; stato e limiti restano visibili.

**Prima del report scientifico definitivo:** completare 980 identità di modello e le tre R1, verificare artefatti e aggregazioni, eseguire la ripresa/riproduzione prevista e produrre le cinque figure. Il completamento non dipende dal segno, dalla separazione dei gruppi o dalla conferma del pilot.

Non creare una dipendenza circolare chiedendo un README «finale» prima del codice e poi usando quel README per certificare il codice. Il riallineamento normativo precede l'implementazione; l'attestazione operativa segue le verifiche.

## 8. Passata completa sul piano: sezioni da cambiare

| Sezione di P | Aggiornamento richiesto |
|---|---|
| Testata e stato | Nuova versione; proposta consolidata applicata solo dopo atto; nessun risultato futuro attestato |
| §1 | Domanda intrafrastica, profili principali, limite alla lettura linguistica |
| §2 | Pilot D_G distinto da D_Q; copertura dei bracci; vecchio alfabeto identificato |
| §3 | Corpus conservato; tragedie solo censimento/inventario; annotazione concreta e pesi visibili |
| §4 | ADV_PART, m100/105/11, hash nuovi, errori sugli ignoti, audit corretto delle esclusioni |
| §5 | Campionamento conservato; training diverso per fold; precisazione Plutarco; nessuna balanced |
| §6 | CTW conservato; parametri nuovi per m; pesi numerici stabili; BOS e reset |
| §7 | Eliminazione bound/SEP; shuffle mantenuto; nessuna identità generale Q=G |
| §8 | Profili principali, due pesature subordinate; R1 conservata; eliminazione scoring probe |
| §9 | Semantica diagnostica corretta, null motivati, masse/supporti persistiti; fasce non co-primarie |
| §10 | Sei celle, 980 modelli; rinunce esplicite; nessun confronto universale fra alfabeti |
| §11 | Un esecutore; C0 posizionale/sensibilità aggregate; cinque figure; manifest ristretto |
| §12 | Test nuovi per accorpamento e ruoli; adattamento T04/T24–T30; soglie reali vincolanti |
| §13 | V3-001 e versione nuova; riuso selettivo del codice; script locale finalmente censito |
| §14 | Checklist lineare, 84 modelli tecnici, 980 finali, niente certificati separati |
| §15 | Lock conservato; stime vecchie identificate come storiche; nuovo benchmark integrato |
| §16 | Regole C20; nessuna falsa attribuzione a DEPREL/ordine/memoria |
| §17 | Sei celle, nessun probe, cinque figure, persistenza ridotta e verifica proporzionata |
| §18 | Citazioni completate/versionate e registro ridotto alle fonti usate |
| §19 | Verdetto sul disegno distinto da gate software ed esiti scientifici |

## 9. Che cosa rimane incerto, senza riaprire il progetto

1. **Effetto quantitativo dell'accorpamento su G/Q:** non misurato in questa revisione; richiede i fit della nuova campagna. Non è una scelta da rimandare ai risultati: la mappa si decide ora per la discontinuità documentata.
2. **Comparabilità annotativa completa:** non dimostrata e non promessa. La riduzione del dettaglio mitiga un problema specifico; il disegno conserva limiti annotativi, storici e di training.
3. **Quota esatta di citazioni metriche in Ateneo:** non ricostruibile automaticamente dai campi XML esaminati. Non introdurre conteggi o attribuzioni inventati; l'opera resta classificata a livello documentale.
4. **Cause puntuali delle sensibilità storiche di Diodoro:** i cambiamenti dei punteggi sono verificati, l'attribuzione a un nodo non lo è. Non è un blocco della domanda ridotta.
5. **Autorizzazione originale delle sessioni pregresse:** distinguere il resoconto allegato dall'atto eventualmente recuperabile. Non presumere una violazione e non certificare un consenso non osservato.
6. **Prestazioni della pipeline integrata:** non misurate perché la pipeline non è ancora implementata. I tempi dei prototipi non sono una garanzia sul run finale.

Non sono state rieseguite le calibrazioni sintetiche ad hoc di A, le percentuali di collegamento `bound` di B o la verifica delle linee guida in tutti i 18 XML. Per questi ultimi sono stati nuovamente ispezionati i due XML di Ateneo; il rapporto non promuove attestazioni delle revisioni a controlli indipendenti non effettuati. Nessuna decisione finale dipende dall'esattezza delle percentuali `bound` o dalle soglie specifiche di A.

Questi punti non giustificano nuovi corpora, nuove annotazioni, un altro modello o una campagna di inferenza. Richiedono una formulazione corretta e, dove pertinente, i normali controlli dell'esecuzione già prevista.

## 10. Verdetto finale per il passaggio successivo

**Favorevole alla chiusura del disegno con le trenta modifiche sopra; non favorevole all'adozione integrale di A, né all'applicazione della 3.0.1 invariata.**

Il progetto risultante è sufficientemente definito per scrivere un nuovo proposal onesto e breve: corpus chiuso, annotazione accorpata, confronto intrafrastico, profili individuali, CTW congelato, Q accoppiato, JSD descrittiva, sei celle e criteri di conclusione indipendenti dal risultato.

Il punto ancora decisivo non è «trovare il controllo che separi definitivamente il metro». È **smettere di promettere quella separazione**, rendendo invece completamente verificabile la quantità che i dati e il protocollo permettono di descrivere. Il nuovo proposal deve assumere questa promessa circoscritta; la repository deve implementarla; il report finale deve rispettarla anche se l'esito differisce dal pilot.

La sequenza consigliata è: **recepimento del contratto consolidato → redazione coerente del proposal e riallineamento normativo → implementazione e verifica → aggiornamento operativo definitivo del README → risultati e report**. Non serve un ulteriore giro di ampliamento metodologico per iniziare questa sequenza.
