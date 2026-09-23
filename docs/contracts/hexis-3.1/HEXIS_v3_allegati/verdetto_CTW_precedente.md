# HEXIS — verifica del CTW e verdetto di fattibilità

**Data:** 11 settembre 2026.  
**Oggetto:** verifica autorizzata del passaggio dal selettore `monotone-stop` a un Context-Tree Weighting per alfabeto non binario.  
**Stato:** verifica conclusa; nessuna modifica applicata alla repository; nuovo piano di aggiornamento ancora da scrivere.

## Verdetto

**Il passaggio al CTW è tecnicamente fattibile e dispone ora di un prototipo funzionante, verificato sia matematicamente sia sulle dimensioni reali di HEXIS. Possiamo procedere alla scrittura del nuovo piano.**

L'esito favorevole riguarda uno studio descrittivo della prestazione predittiva su un corpus finito. Non autorizza tre conclusioni più forti: che la sparsità sia eliminata, che il modello recuperi tutta l'informazione linguistica, o che il guadagno rispetto alla radice identifichi automaticamente dipendenze interne al testo. Le verifiche mostrano precisamente perché queste conclusioni sarebbero sbagliate.

Il nuovo piano dovrà recepire le convenzioni operative verificate e un controllo che distrugga l'ordine dei simboli preservandone la composizione entro frase. Quest'ultimo utilizza lo stesso CTW: non richiede un secondo strumento scientifico. La sua necessità emerge da un controesempio controllato, non da una cautela generica.

Non è stata verificata una pipeline di produzione già integrata in HEXIS: il core canonico della repository contiene ancora funzioni non implementate. È stata verificata la fattibilità del suo sostituto e del protocollo necessario a utilizzarlo.

## 1. Provenienza, autorizzazione e integrità

La connessione GitHub conferma il branch `g1/pre-audit` al commit `852644b6917790877c7b2ca5df2e76b17829d87c`; `master` resta al commit `3f5a6eafac83e5c190a866c8bea1937d8284ce75`. L'audit usa il primo, coerentemente con la revisione precedente.

Sono stati riletti `AGENTS.md`, configurazione, interfacce del modello, campionamento, score, proposta ridimensionata e fonte metodologica. I 120 file tracciati sono stati confrontati tramite SHA-256 prima e dopo le verifiche: **nessuna variazione; stato Git pulito**. Non sono stati importati i moduli del candidato in quarantena; non sono stati modificati dati originali o allegati.

Le prove reali sono esperimenti separati di fattibilità, autorizzati dalla richiesta di verificare il cambiamento. Non costituiscono un passaggio dei vecchi gate G2/G3, né una ratifica implicita delle nuove specifiche. Non sono stati calcolati contrasti fra regimi, p-value o intervalli di confidenza scientifici.

Riferimenti alla copia verificata: [repository HEXIS](https://github.com/leonardotornabene/HEXIS/tree/852644b6917790877c7b2ca5df2e76b17829d87c), [specifica vigente](https://github.com/leonardotornabene/HEXIS/blob/852644b6917790877c7b2ca5df2e76b17829d87c/docs/01_MASTER_SPEC.md).

## 2. Dati verificati

I tre file CoNLL-U greci sono stati nuovamente letti, ricodificati con una procedura separata e confrontati con gli hash di `PROVENANCE.md` e dell'audit precedente. Il commit UD è `37837c7a3c592c9563f8c51cc63344b87247f8a5`.

| Elemento | Quantità verificata |
|---|---:|
| Token greci originali | 202.989 |
| Frasi greche originali | 13.919 |
| Token dei sette blocchi primari, codifica C0 | 154.300 |
| Posizioni primarie con almeno quattro predecessori trattenuti | 109.108 |
| Alfabeto UPOS+DEPREL, C0 | 106 simboli |
| Alfabeto con categoria `oth` | 112 simboli |
| Alfabeto solo UPOS | 12 simboli |
| Budget per blocco di addestramento | 8.884 token |
| Addestramento per fold: sei blocchi | 53.304 token |
| Probe tragico, token C0 | 22.275 |
| Probe tragico, posizioni eleggibili | 12.769 |

L'inventario dell'alfabeto comprende anche il probe tragico, come nella proposta esaminata. È un inventario chiuso e transduttivo di simboli; non sono trasferiti conteggi del testo held-out nell'addestramento.

Il campionatore è stato implementato fuori dalla repository: permutazione delle frasi, frasi intere fino al budget, al massimo un frammento finale contiguo, esattamente 8.884 token per contributo. Tutti i documenti del blocco held-out sono esclusi. Le sensibilità numeriche usano gli stessi campioni; il budget dimezzato riusa la medesima permutazione iniziale. Una nuova codifica può cambiare il punto di arresto del campione, e questo viene registrato.

## 3. Formulazione verificata

La base è il CTW per alfabeti finiti non binari: media probabilistica sugli alberi e distribuzioni Dirichlet ai nodi. La fonte consultata esplicita l'algoritmo, l'inferenza sui modelli e l'estensione a parametri Dirichlet arbitrari. [Kontoyiannis et al., versione 3, 2022](https://arxiv.org/abs/2007.14900v3).

La configurazione del pilot, stabilita prima dei risultati reali, è:

| Scelta | Valore |
|---|---|
| Pseudoconteggio per simbolo, `a` | 0,5 |
| Probabilità a priori di arresto, `rho` | 0,5 |
| Profondità massima | 8 |
| Selezione locale monotona | Assente |
| Soglia `k_min` o `gamma` | Assente |
| Probabilità su ramo mai osservato | Distribuzione uniforme sullo stesso alfabeto |
| Addestramento | Tutti i token ordinari del campione |
| Valutazione primaria | Stesse coordinate per radice e CTW; almeno 4 predecessori nella frase |
| Aggiornamento durante la valutazione | Nessuno, né dei conteggi né dei pesi degli alberi |

`a` e `rho` hanno ruoli diversi. Non si deve riutilizzare ambiguamente il vecchio nome `beta` per entrambi.

### Confini e conteggi

È stata risolta una questione che un semplice riuso del CTW non avrebbe risolto: se si contano tutti i token alla radice ma si ignorano quelli senza un contesto sufficientemente lungo nei figli, il confronto fra arresto e suddivisione può usare insiemi diversi di osservazioni.

Il prototipo usa **BOS soltanto nel contesto**, come foglia terminale che rappresenta la fine della storia disponibile. Non viene predetto e non amplia l'alfabeto degli esiti. Ogni osservazione di un nodo va esattamente in un figlio; i conteggi restano quindi una partizione coerente. Le frasi e i frammenti isolati azzerano la storia.

Questa convenzione è un adattamento condizionale esplicito. L'identità della miscela è dimostrata per induzione nel contratto matematico allegato e verificata tramite enumerazione; non viene attribuita testualmente alla fonte né usata per trasferire automaticamente teoremi asintotici al corpus eterogeneo.

Per la sola sensibilità ai confini è stato verificato un separatore di contesto, anch'esso mai predetto, fra frasi effettivamente adiacenti dello stesso documento. Il controllo richiede adiacenza negli identificativi sorgente e nelle posizioni complete, non soltanto nel sottoinsieme campionato. Una lacuna, un cambio di parte/documento, una frase vuota o un frammento interrompono il collegamento. **Questa convenzione sostituisce quella ambigua del vecchio piano in cui `#` entrava nel denominatore ma non era mai un target.**

### Predizione congelata e numerica

La storia del testo di test avanza, ma il modello non apprende da esso. La verifica confronta la predizione congelata con la media esplicita delle predizioni di tutti gli alberi piccoli, pesati soltanto con i dati di training. Non si confonde questa quantità con la predizione CTW online che aggiorna il posterior a ogni token.

È stato anche verificato un problema numerico concreto: con 106 simboli, costruire in binary64 `rho = 1 - 2**(-105)` produce esattamente 1. Una traduzione ingenua del suggerimento della fonte eliminerebbe quindi la probabilità di suddivisione. Il prototipo conserva separatamente i logaritmi delle due probabilità; la sensibilità corrispondente è stata eseguita con successo.

## 4. Verifiche esatte e integrazione sintetica

| Verifica | Esito |
|---|---|
| Enumerazione completa di piccoli alberi, alfabeti 2/3 e profondità 0–3 | 120 casi superati |
| Controlli puntuali, comprese probabilità e invarianti | 9.189 asserzioni superate |
| Errore massimo rispetto all'enumerazione | 1,07 × 10⁻¹⁴ |
| Identità fra codice prequenziale e probabilità integrata | Errore 1,42 × 10⁻¹⁴ |
| Enumerazione con separatore e BOS | Errore predittivo 2,22 × 10⁻¹⁶ |
| Normalizzazione, simboli/contesti mai osservati, addestramento vuoto | Superati |
| Invarianza alla rinomina dei simboli e all'ordine degli stream | Superata |
| Conteggi e pesi invariati dopo la valutazione | Superata |
| Pipeline sintetica: sette blocchi × 20 semi | 140 fit completati |
| Esclusione held-out, budget esatto, frammenti e adiacenza | Superati |
| Identificativi dei sottosemi controllati | 1.680, senza collisioni |

La logica centrale non riceve etichette di regime. La costruzione del corpus usa il registro per fissare inclusioni e blocchi; il modello e il campionatore ricevono soltanto le sequenze e la mappa dei blocchi. L'ordine degli stream non richiede più una fonte autonoma di variabilità: l'evidenza integrata è invariante a tale ordine.

## 5. Sorgenti sintetiche: cosa funziona e cosa resta limitato

Ogni sorgente piccola è stata verificata con cinque semi, 53.304 token di training e 100.000 token indipendenti di test; la valutazione esclude le prime quattro posizioni. Nessun seme è stato selezionato perché favorevole.

| Sorgente | Riferimento | Cross-entropia CTW: minimo–massimo |
|---|---:|---:|
| Indipendente uniforme, 4 simboli | 2,00000 | 1,99999–2,00007 |
| Ciclo deterministico, 3 simboli | 0 | 0,0000813 |
| Dipendenza immediata, permanenza 0,8 | 0,72193 | 0,72006–0,72641 |
| Dipendenza ritardata di 2 posizioni, accuratezza 0,9 | 0,46900 | 0,46467–0,47361 |
| Memoria variabile di ordine 1/2 | Oracle della realizzazione | 0,64854–0,65516; entro la tolleranza rispetto all'oracle |

Tutte le soglie dichiarate prima degli esperimenti sono superate. **Il CTW recupera la dipendenza ritardata senza il veto intermedio del selettore precedente.**

Le prove con 106 simboli, tre semi per sorgente, mostrano anche il limite:

| Sorgente con 106 simboli | Esito |
|---|---|
| Indipendente uniforme | CE 6,72932–6,72962; riferimento 6,72792 |
| Dipendenza ritardata distribuita sull'intero alfabeto | CE 5,08720–5,12908; riferimento 1,13109 |
| Stessa dipendenza, pseudoconteggio totale 1 | CE 3,84248–3,89842: miglioramento, ma ampio divario residuo |
| Nucleo binario frequente con 10% di simboli rari | Guadagno positivo: circa 0,19–0,20 bit/simbolo con C0 |

Il secondo caso è deliberatamente difficile: il modello deve stimare molte distribuzioni contestuali da pochi esempi ciascuna. Il fatto che la famiglia possa rappresentare la sorgente non significa che 53.304 token bastino per stimarla. Questo è **un limite empirico importante, non un test di correttezza fallito da occultare**. Il CTW attenua il problema della selezione e regolarizza la stima; non rende disponibile informazione che il campione non sostiene.

## 6. Pilot reale e sensibilità

Sono stati completati **140 fit C0**: sette fold × 20 semi. Inoltre sono state eseguite nove sensibilità su tutti i sette fold, un seme ciascuna: **63 fit**, per 203 fit principali e di sensibilità complessivi. Il probe tragico è stato valutato sotto ciascuno dei 140 modelli C0 senza addestrare modelli aggiuntivi.

Le sensibilità coprono pseudoconteggio totale 1, `rho=0,9`, probabilità di split suggerita dalla fonte, metà training, profondità 6/12, alfabeto `oth`, solo-UPOS e separatore di contesto.

Tutte terminano con punteggi finiti e coordinate eleggibili coerenti. Nei 140 fit C0 il guadagno varia da 0,26001 a 0,55301 bit/simbolo; la profondità media pesata varia da 1,00015 a 1,21930. Questi intervalli descrivono i punteggi dei blocchi e dei campioni, **non un effetto fra regimi o un intervallo di confidenza**.

La deviazione standard fra semi, per blocco, varia da circa 0,00297 a 0,02065 bit/simbolo. È variabilità computazionale del campionamento, non incertezza sulla popolazione dei testi.

La lettura più importante è la concentrazione sui contesti brevi. Nel primo seme, passare da profondità 8 a 12 non modifica le CE alla precisione osservata; il massimo scarto passando a 6 è circa 2,42 × 10⁻⁷ bit/simbolo. A profondità 3, circa 84–85% dei nodi osservati ha meno di cinque occorrenze. Con il solo alfabeto UPOS, più piccolo, la profondità pesata sale a circa 1,93–2,13.

Questi risultati **non dimostrano che il linguaggio abbia memoria 1**, né che l'alfabeto UPOS sia scientificamente migliore. Mostrano quanto supporto il campione offre al particolare modello e alla rappresentazione scelta. La cella con metà training si concentra quasi interamente al primo livello: una conferma del ruolo della taglia.

Nel profiling del primo seme, il training osserva 83–87 dei 106 simboli dell'inventario; il tasso di target held-out mai osservati alla radice è fra 0 e 0,04194%. Lo smoothing garantisce probabilità positive anche in questi casi.

Non è stata eseguita l'intera analisi scientifica a dieci semi per tutte le sensibilità. Le prove presenti verificano esecuzione, risorse e comportamento; non certificano la stabilità di un contrasto fra gruppi che non è stato calcolato.

## 7. Scoperta interpretativa e controllo sull'ordine

È stato costruito un controllo aggiuntivo necessario alla validità della lettura: sette testi internamente i.i.d., ma con frequenze binarie differenti. Con training comune, il CTW ottiene un guadagno da 0,523 a 0,894 bit/simbolo, pur non essendoci dipendenza interna in alcun testo. Il contesto aiuta a riconoscere quale distribuzione sta producendo le osservazioni.

Quando il training contiene soltanto testi con la stessa distribuzione del test, il guadagno è praticamente nullo: da −0,0000068 a 0,000000035. **Pertanto il guadagno pooled non può essere chiamato, senza ulteriori controlli, misura pura della dipendenza interna o dell'informazione mutua del testo.**

È stata verificata una risposta concreta: addestrare e valutare lo stesso CTW dopo un rimescolamento indipendente dell'ordine entro ogni stream/frase, preservando simboli e lunghezze. Il training rimescolato mantiene esattamente gli stessi conteggi di radice del training originale. L'esclusione held-out e il budget restano identici.

Esiti del controllo:

- Nei testi i.i.d. eterogenei, la differenza fra guadagno originale e rimescolato resta fra −0,00140 e 0,00176 bit/simbolo.
- Nella sorgente con dipendenza ritardata, tale differenza è fra 0,52660 e 0,53177 bit/simbolo: la dipendenza viene distinta dal solo cambiamento delle frequenze.
- Nel pilot reale del primo seme, su tutti e sette i fold, il guadagno del modello addestrato e valutato sui testi rimescolati è 0 alla precisione registrata, contro 0,27277–0,53914 sui testi originali.

L'ultimo risultato è favorevole ma resta un pilot con un rimescolamento per fold. Non è un test di significatività, non dimostra un effetto del metro e non sostituisce i controlli di annotazione e composizione. Il nuovo piano dovrà fissare la replica di questo controllo e la sua lettura descrittiva prima dell'analisi finale. La fattibilità computazionale e la capacità del controllo di separare i due fenomeni nei casi noti sono già verificate.

## 8. Costi e lavoro di implementazione

Profiling separato con Python 3.12.14, NumPy 2.3.5 e PyYAML 6.0.3; CPU ordinaria, nessuna GPU:

| Operazione | Misura |
|---|---:|
| Fit C0, 53.304 token | 0,63–0,70 secondi |
| Valutazione del blocco escluso | 0,024–0,224 secondi |
| Valutazione dell'intero probe tragico | 0,046–0,055 secondi |
| Picco RSS del processo nel benchmark C0 | 174,4 MiB |
| Massimo RSS nei pilot reali di sensibilità | circa 240 MiB, profondità 12 |
| Massimo RSS della batteria sintetica | circa 254 MiB |

I tempi misurati riguardano questa macchina. Una proiezione per un budget dell'ordine di 700 fit è nell'ordine di 10–30 minuti per il prototipo e le sue operazioni di supporto, con esecuzione sequenziale; è una stima, non la durata misurata di una pipeline completa da 700 fit. Figure, esportazioni finali e condizioni del computer dell'utente non sono incluse in una promessa temporale.

I sei vettori numerici di output per tutte le 2.182.160 posizioni C0 dei 20 semi richiederebbero circa 100 MiB non compressi, prima di coordinate e metadati. Un esempio da 46.634 posizioni occupa 162.270 byte compresso. Occorre conservare le coordinate in forma compatta e scartare ogni albero dopo la valutazione: non serve tenere in memoria 140 alberi o salvarne ogni nodo.

Il lavoro residuo è identificabile: integrare il core e la configurazione, implementare campionatore e score canonici, collegare provenienza/output, portare i test, aggiornare documenti e gate. La repository contiene ancora stub nel modello, negli score e in diversi comandi della pipeline. Il prototipo non deve essere presentato come una loro implementazione già completata. Non servono nuove annotazioni, un modello neurale o una nuova raccolta di corpus per il perimetro verificato.

## 9. Condizioni da recepire nel nuovo piano

1. Adottare un unico CTW per esiti non binari, con distinzione esplicita fra pseudoconteggi e prior sugli alberi.
2. Congelare conteggi e pesi durante l'evaluation; mantenere la stessa popolazione di target per radice e CTW.
3. Ratificare la gestione BOS e l'eventuale separatore di contesto; eliminare l'ambiguità del vecchio `#`.
4. Ritirare `monotone-stop`, `argmax`, `k_min`, `gamma` e le interpretazioni basate su un'unica profondità selezionata.
5. Conservare il controllo di ordine rimescolato come diagnostica dello stesso strumento; non interpretare da solo il guadagno pooled come dipendenza interna.
6. Limitare le conclusioni al corpus, alla codifica e al predittore; non leggere la scarsità di contesti profondi come una proprietà grammaticale dimostrata.
7. Mantenere la JSD delle distribuzioni di radice come lettura descrittiva separatamente identificata, senza reintrodurre una batteria di stimatori concorrenti.
8. Registrare che sono già stati osservati pilot reali. Il nuovo documento non dovrà fingere una preregistrazione precedente a queste osservazioni.

**Non sono rimasti bloccanti tecnici nelle prove definite. Sono rimasti limiti scientifici reali, ora identificati e affrontabili attraverso uno scope corretto e controlli già prototipati. È su questa base, e non su una promessa di assenza assoluta di limiti, che il giudizio di fattibilità è favorevole.**

## Allegati riproducibili

L'archivio comprende codice del prototipo, verifiche indipendenti, contratto matematico, protocollo fissato prima dei risultati, risultati JSON, ledger dei campioni e istruzioni di riproduzione. Non contiene il testo originale del treebank né una copia della repository. Gli hash dei dati e del codice consentono di identificare esattamente gli input e la versione verificata.
