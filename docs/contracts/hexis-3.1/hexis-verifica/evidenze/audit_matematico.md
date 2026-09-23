# HEXIS — verifica matematica indipendente delle revisioni A e B

Data: 15 settembre 2026. Perimetro: lettura dei documenti, esame del riferimento CTW isolato, ricalcolo dei JSON storici e piccoli controesempi sintetici. Nessun nuovo fit reale, import da `candidates/` o modifica della repository. Le proposte non sono state trattate come autorizzazioni alla migrazione.

## Verdetto

Conservare CTW, predizione congelata e Q a quattro termini. Preferire il ridimensionamento di B: sei celle C0, `a_total1`, `q_half`, D12, `oth`, UPOS; nessun probe finale, `bound`, nuovo protocollo balanced, `deprel_only`, rango o rapporto normalizzato obbligatorio. Il risultato principale deve essere il profilo dei sette blocchi; D_Q è una sintesi descrittiva della procedura. L'accorpamento globale PART/ADV proposto da B è coerente con questa soluzione, con alfabeti di destinazione 100/105/11: i conteggi sono oggetto dell'audit corpus parallelo, non di questa verifica matematica.

A contiene osservazioni utili, ma numerose conclusioni vanno oltre le prove. Non ho trovato nelle sezioni matematiche di B un errore paragonabile a quelli elencati sotto. La semplificazione degli output richiede una modifica esplicita dei contratti di ricostruibilità.

## 1. Che cosa l'archivio dimostra realmente

Lettura indipendente di `verifiche_CTW_precedenti.zip/ctw_validation/`:

| Evidenza | Copertura effettiva |
|---|---:|
| `pilot_C0.json` | 140 fit originali = 7 blocchi × 20 semi |
| Ciascuno degli altri nove `pilot_*.json` | 7 fit originali, seme 0 |
| `shuffle_results.json`, sezione real | 7 coppie C0, seme di campionamento 0 |

`verify_shuffle.py` chiama esplicitamente `fold_data(blocks, held, 0, 8884)`: non esiste qui una campagna shuffle dei venti semi o delle altre celle. Le sette coppie supplementari in `contract_validation.json` impiegano la nuova convenzione RNG e non colmano questa lacuna.

Dai 140 originali si ricostruisce:

- D_G originale medio = **−0,17802467965627133 bit/simbolo**;
- SD campionaria tra semi = **0,011027771033396177**;
- intervallo = **[−0,1982444032327907; −0,1573585891563815]**.

Per il solo seme 0 con entrambi i bracci archiviati, D_G = D_Q = **−0,17724076290276225**, poiché i sette G rimescolati registrati sono zero. Non è lecito chiamare il valore medio sui venti semi D_Q: manca G_R su 19 semi. Analogo problema per la tabella A delle sensibilità: contiene contrasti D_G, non contrasti Q verificati per quelle celle.

La raccomandazione di dichiarare chiaramente i pilot è giusta. Sono invece eccessive le frasi A «il risultato finale è già noto» e «1.400 esecuzioni non scopriranno nulla». Cambiano convenzioni, contratti e ora anche rappresentazione; soprattutto, una previsione dei risultati non ne è la verifica.

## 2. Nucleo CTW e Q: confermati

Ho confrontato le formule §§6–8 del piano con `ctw_reference.py`. Il conteggio BOS assicura che ogni osservazione di un nodo non terminale appartenga a esattamente un figlio; le evidenze integrate consentono la miscela ricorsiva arresto/suddivisione. Il predittore congelato è una combinazione convessa delle distribuzioni locali posteriori sotto i pesi appresi sul training. Non coincide con la predizione del test aggiornando progressivamente parametri e posteriori, ma rimane un codice condizionale normalizzato.

Un'enumerazione indipendente con probabilità razionali, su un caso binario D2 con stream separati, ha confrontato tutti i cinque alberi ammessi: errore massimo sulle probabilità **1,1102230246251565e−16**, sui log di evidenza **2,6645352591003757e−15**. Questo è un controllo piccolo e autonomo, non una certificazione completa della futura API.

La formula resta:

`Q = (CE0_O − CE_CTW_O) − (CE0_R − CE_CTW_R)`.

L'identità dei conteggi di radice del training non implica identità delle perdite di radice sui target del test: lo shuffle sposta simboli dentro e fuori dalla maschera delle prime quattro posizioni. Non si eliminano termini né bracci in base al pilot.

## 3. Zero in float64: non è un teorema di collasso

A §6.1 confonde tre proprietà:

1. predominio schiacciante di una componente nell'evidenza;
2. peso arrotondato a 0 o 1 in float64;
3. probabilità matematica esattamente nulla.

Con conteggi finiti, `a>0` e prior di arresto/suddivisione entrambi positivi, a un nodo non forzato entrambe le evidenze sono positive. Il posterior di arresto è quindi matematicamente strettamente tra 0 e 1. Può essere indistinguibile da un estremo nella rappresentazione numerica.

La frase «soglia di sottotraboccamento di log1p(exp(x)) ~37 nat» è errata. Controllo già eseguito:

- `exp(−37) = 8,533047625744066e−17`;
- `log1p(exp(−37))` conserva questo valore, non zero;
- `exp(−745) = 5e−324`, mentre `exp(−746) = 0`.

Circa 37 nat è la scala a cui una piccola componente può perdersi nell'arrotondamento di un peso vicino a uno; non è la soglia di underflow dell'esponenziale. Inoltre il riferimento calcola `hi + log1p(exp(lo-hi))`: quando `hi` è grande in valore assoluto, la piccola correzione può perdersi prima. Nel controllo `hi=−192272,7` e `lo=hi−25`, il risultato è già esattamente `hi` in float64. Non esiste una soglia universale 37 per l'intera implementazione.

I margini di 6.680 o 20.454 nat riportati da A, se correttamente misurati nei suoi sintetici, implicano un'approssimazione numerica estremamente netta in quei casi. Non sono misure dei margini reali di tutte le celle; non li ho ricalcolati. L'archivio registra `root_stop=0.0` nei 140 originali, ma non contiene i log-evidence dei relativi alberi per ricostruire ogni margine senza rifit.

Diagnostica minima utile: accanto a `root_stop`, salvare

`delta_root = (log_rho + logE_root) − (log_split + sum(logW_children))`.

È il log-rapporto posterior di arresto/suddivisione alla radice, computabile durante il fit. Se necessario, riportare i log dei due pesi mediante formule stabili. Non introdurre una soglia di selezione del modello o una nuova cella. Un grande margine alla radice non dimostra che rho sia irrilevante nei nodi discendenti.

Anche qualora G_R fosse numericamente zero in tutta una futura campagna, la conclusione è «nessun vantaggio contestuale misurato nel controllo con questo predittore». Non dimostra che la composizione non contribuisca né attribuisce causalmente tutto G all'ordine linguistico.

## 4. Profondità e prior non sono inerti per costruzione

A §6.3 dice D6=D8=D12 «esattamente». I JSON completi smentiscono l'identità D6/D8, pur confermando differenze molto piccole. Al seme 0, D6−C0:

| Blocco | Differenza di G |
|---|---:|
| Erodoto | −1,0838937192e−8 |
| Tucidide | −1,6743811893e−10 |
| Ateneo | +2,4132042420e−7 |
| Diodoro | +2,5731305975e−11 |
| Plutarco | −5,5552333844e−8 |

D12/C0 è identico nei sette valori G archiviati. Nessuna di queste osservazioni costituisce un'identità del metodo. Controesempio sintetico già eseguito: sequenza binaria di de Bruijn di ordine 9, training lungo 20.480, test 4.096, valutazione da posizione 12. CE D6 e D8 = **0,999999999805135**; CE D12 = **0,017709289896079353**. Una vera dipendenza oltre D8 è quindi apprendibile in un caso appropriato.

Anche rho cambia le predizioni: su un piccolo training binario sintetico, la probabilità dello stesso esito dopo la stessa storia passa da **0,5882695298** con rho=0,1 a **0,6287599095** con rho=0,9. Nei dati archiviati `rho_literature` cambia G di Diodoro di **−0,0476143229**; `bound` lo cambia di **−0,0478091219**. A riconosce questi numeri ma li rende incompatibili con i propri titoli «inerte».

Il CTW è una miscela continua per prior interni e conteggi fissati. Una risposta ripida o una saturazione numerica può apparire come commutazione; dai soli aggregati non si identifica un nodo responsabile. L'ipotesi A sul «commutatore discreto» di Diodoro rimane da verificare, non è una diagnosi acquisita.

## 5. Prior della letteratura e conteggi dei fit

La fonte primaria conferma che il default proposto dagli autori è beta circa `1−2^(−(m−1))`, con beta probabilità di arresto. Il suo log-split a m106 è **−72,78045395879425**; `1−2^(−105)` arrotonda a uno in float64. Qui A e il piano hanno ragione. È una scelta di prior della fonte, non un obbligo per ogni adattamento HEXIS. Conservare il test numerico è sufficiente nel perimetro ridotto; omettere la cella rho rinuncia esplicitamente alla sua sensibilità finale.

La versione pubblicata è: Kontoyiannis, Mertzanis, Panotopoulou, Papageorgiou e Skoularidou, *Bayesian Context Trees: Modelling and Exact Inference for Discrete Time Series*, **JRSS Series B 84(4), settembre 2022, 1287–1323**, DOI **10.1111/rssb.12511**. [Pagina dell'editore](https://academic.oup.com/jrsssb/article/84/4/1287/7073257). Il ragionamento sul prior è nel §2.2 della [versione primaria arXiv v3](https://arxiv.org/html/2007.14900v3#S2.SS2). Integrare i metadati editoriali è opportuno; chiamare il preprint degli stessi autori «fonte secondaria» è scorretto.

A ha ragione che si possono riutilizzare i conteggi. A e rho richiedono nuove evidenze/pesi; D inferiore richiede forzare le foglie al nuovo limite e ricalcolare ricorsivamente i pesi degli antenati. Troncare soltanto la valutazione di un modello D12 mantenendone i pesi non equivale a rifare D8. Nel sintetico, il troncamento corretto con ripesatura ha riprodotto D8 con errore zero.

La riduzione dell'accumulo dei conteggi non elimina modelli scientifici:

- vecchio piano: **1.400** combinazioni `(cella, blocco, seme, braccio)`; riuso semplice possibile con **840** accumuli di conteggi;
- sei celle: **980** combinazioni = `2×7×(20+5×10)`; riuso C0/D12/a consente **700** accumuli nella strategia semplice.

700 non è una pretesa di minimo teorico di ogni possibile ottimizzazione. Le 980 combinazioni rimangono da ripesare, valutare e verificare secondo il loro contratto. Il campionamento delle celle numeriche era già esattamente accoppiato nel piano; il riuso non crea tale proprietà, riduce lavoro duplicato.

## 6. Lunghezza disponibile, esposizione e identificazione

La fascia `past>=8` satura precisamente il numero massimo di simboli leggibili dal D8 con reset intrafrastico. Non rende uguali i contesti, il supporto osservato, la lunghezza delle frasi, la posizione interna né la composizione del training. Non equivale a matching esatto. Per D12, la medesima fascia non satura neppure la profondità disponibile.

Il contrasto originale ricalcolato nella fascia è **D_G=−0,18470778832902407**, non D_Q a venti semi. È un'evidenza contro la spiegazione ristretta «il contrasto deriva interamente da avere meno di otto predecessori nei target», non un'esclusione generale del confondimento della lunghezza. Conservare le due fasce come diagnostica già prevista; non promuovere il risultato favorevole del pilot a co-primario.

D_Q è un funzionale descrittivo ben definito di dati, protocollo e semi. È invece non identificato come effetto intrinseco o causale di regime. Una cella 50/50 pareggia una quota del training, ma cambia anche il budget (53.304→18.564) e mantiene differenti blocchi disponibili, cronologia e annotazione. Un sintetico in cui 18.564 token bastano non prova che bastino per il corpus o per ogni tipo di dipendenza. La persistenza del segno non «esclude il meccanismo esposizione» in generale.

Una riaggregazione senza un documento è possibile sugli score esistenti, ma non è una campagna riaddestrata senza quel documento: il testo escluso può ancora aver contribuito ai training degli altri fold. Non aggiungerla come nuova analisi obbligatoria.

## 7. Massa risolta, responsabilità predittiva e confronti tra alfabeti

`lambda_s` è peso di miscela instradato verso il contesto, prima di osservare il target. La responsabilità di quel componente per l'esito effettivo x sarebbe invece `lambda_s*p_s(x)/q(x|h)`. Le due quantità non coincidono. Nel piccolo esempio verificato, il peso del contesto lungo 2 è **0,36363636**, la sua probabilità locale dell'esito è 0,75 e quella complessiva 0,59090909: responsabilità **0,46153846**. Non rinominare la prima come contributo informativo dell'esito.

B correttamente nota che una sola osservazione è supporto, non precisione: con m106 e a0,5 il simbolo osservato ha probabilità 1,5/54 e gli altri raccolgono il 97,2222%. L_resolved resta una diagnostica dei pesi attribuiti a contesti osservati, non profondità grammaticale o certificazione della memoria recuperata. Tenere supporto, massa non osservata, istogrammi e null motivati; nessuna nuova statistica di responsabilità è necessaria.

La quasi uguaglianza del contrasto C0/UPOS non dimostra che DEPREL non contribuisca: contributi simili ai due gruppi possono cancellarsi nella differenza; cambiano anche task, alphabet e prior totale. `deprel_only` non separerebbe causalmente i contributi dei due livelli.

`G/CE0` è una frazione della perdita di quello specifico task, non una normalizzazione che renda rappresentazioni diverse equivalenti. Controesempio concettuale: aggiungere all'esito un bit indipendente imprevedibile lascia G invariato e aumenta CE0 di un bit, riducendo il rapporto senza cambiare la dipendenza d'ordine di partenza. Non è l'«unica misura confrontabile» promessa da A. Non aggiungerla obbligatoriamente.

Il rango 1/21 riflette che i due blocchi HEX hanno i due G più bassi nel pilot. Senza scambiabilità non acquista valore inferenziale; il fatto che sia calcolabile non obbliga a inserirlo nel report. I sette punti mostrano già la separazione.

## 8. Tagli motivati e output minimi verificabili

Tagliare D6 perché una sola perturbazione superiore D12 basta al perimetro; tagliare bound perché si sceglie una domanda intrafrastica; tagliare probe perché aprono una domanda distinta; tagliare rho dichiarando la sensibilità cui si rinuncia. Conservare `a_total1`, `q_half`, D12 per verificare tre scelte diverse: regolarizzazione locale, disponibilità di dati, limite di profondità. Queste motivazioni valgono anche se il pilot avesse dato un altro segno e quindi evitano la selezione guidata dall'esito.

Le soglie di apprendimento sintetiche dipendono dalla famiglia di sorgenti, distribuzione marginale, lunghezza, segmentazione, prior e metrica. Cambiare m a parità di probabilità di copia non mantiene necessariamente fissa la quantità d'informazione predicibile. I numeri A non sono soglie del greco né una graduatoria generale del «potere» delle rappresentazioni. Conservare i sintetici prefissati e lo stress dichiarato; l'accorpamento degli alfabeti richiede aggiornare esplicitamente i parametri dei test di destinazione, non riutilizzare attestazioni m106 come se validassero automaticamente m100.

È ragionevole persistere tutte le posizioni soltanto in C0 e aggregati nelle sensibilità, a condizione di conservare:

- chiavi complete, ledger, hash modello, coordinate/identità del corpus e parametri necessari alla rigenerazione;
- per documento, seme, braccio e fascia: n e somme delle due perdite; derivazione verificabile di blocchi, quattro CE, Q, contrasti e pesi;
- diagnostiche per fit, conteggi per fascia, supporti e istogrammi prefissati di massa/routing, denominatori dei valori null;
- riassunti ai livelli e con i pesi esattamente prescritti; la media per target di L_resolved non si ricostruisce dal solo rapporto delle masse aggregate.

Quattro somme non bastano a riprodurre istogrammi, coordinate o qualunque futura statistica posizionale. T27 deve distinguere ricostruzione dalle righe C0, ricostruzione dagli aggregati delle sensibilità e verifica di rigenerazione controllata dal ledger. Non promettere ricostruibilità posizionale da aggregati che hanno perso l'informazione. Verificare l'accoppiamento degli slot prima dell'aggregazione. Non imporre asserzioni future G_R=0 o L_resolved_R=0 solo perché osservate nel pilot; usare normale compressione e aggregazione.

## Evidenza riproducibile di questo audit

- Script isolato: `/private/tmp/hexis_math_audit_20260915/audit_math.py`.
- Output già prodotto: `/private/tmp/hexis_math_audit_20260915/math_checks.txt`.
- Copia estratta degli allegati: `/private/tmp/hexis_math_audit_20260915/HEXIS_v3_allegati/`.
- Storico: `/private/tmp/hexis_math_audit_20260915/history/ctw_validation/`.
- Runtime del controllo: Python 3.12.13 e NumPy 2.5.1 della repository, nessuna dipendenza aggiunta.

Sono state eseguite soltanto le prove documentate nello script. Le esperienze sintetiche più grandi dichiarate da A non sono state ripetute e non vengono presentate come verifiche indipendenti di questo audit. Il report conclude una revisione, non applica il nuovo disegno ai documenti vincolanti del progetto.
