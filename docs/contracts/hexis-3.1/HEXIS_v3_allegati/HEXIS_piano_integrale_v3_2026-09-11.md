# HEXIS 3.0.1 — Piano integrale di aggiornamento

**Organizzazione sequenziale delle annotazioni morfosintattiche in un corpus finito di greco antico**  
**Specifica scientifica, protocollo operativo e piano di migrazione — versione iniziale 11 settembre 2026; revisione autorizzata 12 settembre 2026**

**Stato:** piano concluso e consegnato; integrazione nella repository non eseguita. La fattibilità del nucleo CTW e del protocollo è stata verificata con esperimenti separati. I risultati definitivi dello studio e il superamento dei gate della futura implementazione non sono ancora disponibili.

Il documento definisce le decisioni da applicare insieme, senza lasciare alternative metodologiche da scegliere durante l’esecuzione. Gli allegati contengono configurazione strutturata, registro documentale, conteggi attesi, contratti eseguibili e risultati delle verifiche supplementari. Il riferimento Git è `g1/pre-audit`, commit `852644b6917790877c7b2ca5df2e76b17829d87c`; la specifica non presuppone che gli stub presenti siano già implementati.

**Pacchetto necessario.** Questo piano va utilizzato insieme a `HEXIS_allegati_operativi_v3_2026-09-11.zip`, nella versione 3.0.1 identificata dal README e dal registro delle modifiche. La data nel nome indica la prima consegna; la revisione corrente è del 12 settembre. Il precedente `HEXIS_CTW_verifiche_riproducibili_2026-09-11.zip` contiene soltanto le prove CTW precedenti e non sostituisce gli allegati normativi. Nell’archivio operativo corrente sono inclusi anche una copia identica di questo piano, il registro delle modifiche e gli hash: è sufficiente trasmettere l’intero pacchetto al revisore. La versione iniziale degli allegati è conservata in `history/` e non è normativa per la revisione.

**Perimetro della revisione.** Si recepiscono motivazione dei frammenti, registrazione dell’eccezione autorizzata al freeze precedente, riaggregazione per target, blocchi automatici dell’emissione dei contrasti, riferimenti omessi, conservazione delle utility statistiche e mantenimento del lock esistente. Corpus, CTW, Q, JSD, nove celle e 1.400 fit rimangono quelli definiti nella versione iniziale. Non si assume una direzione determinata dell’asimmetria del training.

## 1. Decisione complessiva e ragione del ridimensionamento

HEXIS diventa uno **studio descrittivo, riproducibile, su un corpus finito**, che confronta la prevedibilità delle sequenze di annotazioni UPOS+DEPREL sotto un predittore a memoria variabile. Il nucleo è un CTW per esiti non binari, con media probabilistica sugli alberi e regolarizzazione Dirichlet. Le letture principali sono il guadagno rispetto al predittore di radice e la sua variazione quando si distrugge l’ordine dei simboli entro frase. La JSD descrive separatamente le differenze di composizione dell’alfabeto.

Fra le due proposte originarie, `piano_ultimato_HEXIS.md` costituisce la base migliore per il perimetro: abbandona un’inferenza sulla popolazione non sostenuta dalla composizione dei dati. Non si effettua una fusione paritaria. Si conservano di quella proposta corpus finito, blocchi di dipendenza, bilanciamento del training e fattibilità; si sostituiscono le parti tecniche superate dalle verifiche CTW. La JSD viene mantenuta, conformemente alla decisione esplicita del responsabile del progetto e al successivo verdetto di fattibilità.

Il vecchio selettore `monotone-stop` è ritirato. La motivazione specifica è che una dipendenza ritardata può richiedere un contesto di ordine 2 pur non offrendo un miglioramento al primo livello: un arresto locale può impedirne l’esplorazione. Il CTW confronta probabilisticamente le alternative dell’intero sottoalbero. Non si sostituisce la famiglia dei contesti variabili con un modello di ordine fisso e non si sostiene che il CTW elimini il carattere markoviano: con profondità massima finita rimane una famiglia a memoria finita.

### 1.1 Domanda di ricerca finale

> Nel corpus greco UD Perseus fissato, quale vantaggio predittivo offre l’ordine osservato delle annotazioni UPOS+DEPREL, rispetto al medesimo protocollo applicato a sequenze rimescolate entro frase? Come differiscono questi punteggi tra i blocchi di tradizione esametrica e i blocchi prosastici disponibili, e quanto dipendono da codifica, regolarizzazione, budget e confini?

Il contributo è un confronto documentato e controllato di questo corpus, non l’invenzione del CTW, una teoria della grammatica o la prima applicazione di metodi quantitativi alla distinzione prosa/verso. Esistono lavori anteriori su classificazione stilometrica del greco antico, anche con caratteristiche sintattiche. [Gianitsos et al., 2019](https://aclanthology.org/W19-2507/).

Il contributo positivo consiste nel quantificare il vantaggio dell’ordine delle annotazioni rispetto alla composizione entro frase, documentare quanto contesto il campione consenta effettivamente di utilizzare e mostrare la dipendenza dei risultati da rappresentazione e protocollo. Questo contributo rimane informativo se il vantaggio predittivo si concentra sui contesti brevi: non richiede il recupero di una memoria lunga né una separazione netta fra gruppi.

Il precedente più vicino sul rapporto fra contesti variabili e ritmo è Galves et al. (2012): selezione di VLMC su codifiche ritmiche di testi portoghesi. HEXIS adotta invece una valutazione predittiva CTW di annotazioni morfosintattiche greche, sotto il controllo di ordine e lo scope finito qui definiti. Gorman e Gorman (2016) costituiscono un precedente pertinente sulla stilometria sintattica del greco, con caratteristiche ricavate dai percorsi degli alberi di dipendenza. Queste differenze delimitano il contributo, senza rivendicare una priorità assoluta. [Galves et al.](https://arxiv.org/pdf/0902.3619), [Gorman e Gorman](https://digitalcommons.unl.edu/historyfacpub/208/).

### 1.2 Risultati ammessi e interpretazioni escluse

Sono ammesse descrizioni del tipo: «con questa codifica e questo protocollo, il blocco presenta un guadagno di X bit per simbolo; il controllo di ordine lo modifica di Y». È ammessa una differenza aritmetica fra le medie dei due insiemi di blocchi.

Non sono identificate: causalità del metro; effetto separato di cronologia, autore o genere; entropia “vera” del greco; informazione mutua della lingua; complessità grammaticale complessiva; difficoltà cognitiva di lettura; assenza di dipendenze oltre la profondità utilizzabile dal campione. Un risultato piccolo o nullo non dimostra l’assenza di struttura linguistica.

I simboli sono annotazioni realizzate sul testo completo: DEPREL può dipendere da informazioni successive alla parola e dalla sua testa sintattica. La loro predizione non equivale alla previsione delle parole da parte di un lettore. Inoltre, la sequenza elimina la gerarchia delle dipendenze: conserva categorie e relazioni, non l’albero sintattico completo.

### 1.3 Perché le misure informative restano legittime

Entropia e informazione mutua sono funzionali di distribuzioni; la sparsità riguarda la loro stima e l’adeguatezza della rappresentazione e del modello. La critica a una grammatica ridotta a transizioni locali non rende inutilizzabile ogni misura probabilistica descrittiva. In HEXIS si evita questa confusione dichiarando che cosa viene effettivamente misurato: una perdita predittiva fuori dal training, sotto un predittore esplicitamente delimitato. La letteratura sugli stimatori da sequenze finite motiva la cautela verso equivalenze automatiche fra lunghezza di codice e tasso entropico. [Schürmann e Grassberger, 1996; deposito 2002](https://arxiv.org/abs/cond-mat/0203436).

La cross-entropia empirica può essere interpretata come costo medio di codifica sotto il predittore congelato. L’identità teorica tra cross-entropia, entropia e divergenza vale sotto distribuzioni e aspettative appropriate; non trasforma automaticamente una differenza empirica fra due modelli stimati in un’informazione mutua.

## 2. Stato delle prove e distinzione dalla preregistrazione

Le verifiche precedenti sono riportate in `HEXIS_verifica_comparata_2026-09-11.md`, `HEXIS_verdetto_CTW_2026-09-11.md` e nei rispettivi archivi riproducibili. Per questa specifica sono state aggiunte verifiche sui contratti di campionamento, semi, rimescolamento, confini e composizione del pacchetto.

| Evidenza già disponibile | Esito e portata |
|---|---|
| Suite della repository nel primo audit | 327 pass, 17 skip; questi ultimi sono scaffold, non modelli verificati |
| Enumerazione CTW indipendente | 120 casi, 9.189 asserzioni; errore massimo 1,07 × 10⁻¹⁴ |
| Identità prequenziale/integrata sul training | Errore massimo 1,42 × 10⁻¹⁴ |
| Confini BOS e separatore | Partizione dei conteggi e normalizzazione verificate |
| Pipeline sintetica precedente | 140 fit, sette blocchi × 20 semi |
| Pilot reale precedente | 140 fit C0 e 63 fit di sensibilità, tutti completati |
| Controllo precedente di ordine | Casi sintetici eterogenei e dipendenza ritardata; sette fold reali al primo seme |
| Nuovo contratto del piano | Esiti dettagliati in `contract_validation.json`; distinto dai risultati scientifici definitivi |

Il CTW recupera nel sintetico piccolo una dipendenza ritardata che il selettore monotono non recuperava. Tuttavia, con 106 simboli e una dipendenza ritardata distribuita su tutto l’alfabeto, il pilot presenta CE circa 5,09–5,13 contro un riferimento 1,131 bit: l’ordine è rappresentabile, ma il campione non basta a stimarlo bene. Con pseudoconteggio totale 1 la CE scende a circa 3,84–3,90, ancora lontana dal riferimento. Questo limite resta parte del risultato metodologico.

Nei 140 fit C0 reali il guadagno varia fra 0,26001 e 0,55301 bit/simbolo; sono estremi fra blocchi e semi, non un contrasto di regime. Il passaggio da profondità 8 a 12 non cambia le CE del primo seme alla precisione registrata. Circa l’84–85% dei nodi osservati di profondità 3 ha meno di cinque osservazioni. Sono evidenze di supporto statistico limitato, non una dimostrazione che il greco abbia memoria 1.

Il supporto limitato dei contesti profondi è già un risultato del pilot, non soltanto un rischio ipotetico. Rimane distinto dal risultato dell’analisi finale. Gli intervalli storici circa 1,00–1,22 in C0 e 1,93–2,13 in UPOS provengono dalla diagnostica `weighted_depth` del prototipo: non vanno rinominati “profondità risolta v3”. La nuova diagnostica del §9 non è retroattivamente attribuita a quei numeri.

**Sono stati osservati pilot reali prima di questo piano.** Il documento è un protocollo prospettico per l’analisi finale dopo sviluppo metodologico, non una preregistrazione antecedente a ogni osservazione. I pilot restano archiviati, inclusi quelli sfavorevoli; non si riutilizzano come se fossero risultati della nuova sequenza di semi.

## 3. Dati, identità e unità del progetto

### 3.1 Sorgente congelata

Si utilizzano soltanto i tre file greci UD Ancient Greek Perseus della release `r2.18`, al commit `37837c7a3c592c9563f8c51cc63344b87247f8a5`. Si ricompongono i documenti attraverso `sent_id`; gli split UD train/dev/test non hanno funzione sperimentale.

| File | SHA-256 |
|---|---|
| `grc_perseus-ud-dev.conllu` | `7899f809fc250404839694330b9db25f79a5b1f20cfa12e6dc3a368a4ec7cd22` |
| `grc_perseus-ud-test.conllu` | `e18d47c395c0ec8da678fb5e315ce6d90133e88c25ed2a55bc72a2a66e6254d5` |
| `grc_perseus-ud-train.conllu` | `d7471c9b91bcd975848fa5d9b65c31f1fc48a597ed3667796968a82c6d098a7e` |

Fonte: [snapshot UD verificato](https://github.com/UniversalDependencies/UD_Ancient_Greek-Perseus/tree/37837c7a3c592c9563f8c51cc63344b87247f8a5). L’audit deve fallire se cambia anche un solo hash; aggiornare il corpus richiede una nuova versione del protocollo e nuovi risultati.

### 3.2 Gerarchia delle unità

- **Token sorgente:** riga CoNLL-U con ID intero; intervalli multiword ed empty node decimali non sono osservazioni aggiuntive.
- **Frase sorgente:** identificata univocamente da `sent_id`; non ridefinita con punteggiatura o versi.
- **Documento canonico:** un’opera o un estratto definito nel registro; Ateneo XII e XIII costituiscono un documento con due parti.
- **Blocco di dipendenza:** unità esclusa integralmente dal training e unità di peso nel confronto fra gruppi.
- **Seme:** replica computazionale del campionamento e del rimescolamento, mai una replica scientifica.

I blocchi limitano la contaminazione evidente fra testi associati; non dimostrano indipendenza fra i sette blocchi. “Homeric tradition” e “Hesiodic tradition” sono convenzioni conservative del disegno, non attribuzioni filologiche a un unico autore.

### 3.3 Corpus primario fissato

| Blocco | Documenti/estratti | Gruppo | Token C0 | Posizioni valutate C0 |
|---|---|---|---:|---:|
| HOMERIC_TRADITION | Iliade; Inno a Demetra | HEX | 71.088 | 46.634 |
| HESIODIC_TRADITION | Teogonia; Opere e giorni; Scudo di Eracle | HEX | 9.282 | 6.375 |
| HERODOTUS | Storie, libro I | PROSE_ALL | 17.301 | 12.946 |
| THUCYDIDES | Storie, libro I | PROSE_ALL | 9.346 | 7.227 |
| ATHENAEUS | Deipnosofisti, libri XII–XIII | PROSE_ALL | 23.133 | 16.691 |
| DIODORUS | Biblioteca storica, libro XI | PROSE_ALL | 15.266 | 12.334 |
| PLUTARCH | Licurgo; Alcibiade | PROSE_ALL | 8.884 | 6.901 |
| **Totale** | **11 documenti, 7 blocchi** | **2 HEX / 5 prosa** | **154.300** | **109.108** |

Le identità complete, gli URN e i prefissi sono in `hexis_v3_design.json`, parte normativa di questo piano. Il corpus contiene 18 prefissi greci, ricondotti a 17 documenti, 11 primari e 6 probe. I token originali sono 202.989, le frasi 13.919. Nessun testo greco presente nei tre file viene escluso dal censimento.

I file XML upstream verificati confermano intestazioni bibliografiche di Teogonia, Opere e giorni, Scudo e Diodoro; per quest’ultimo il primo riferimento di passo è `11.1.1`. Gli hash e i collegamenti puntuali sono in `identita_fonti_verificate.json`. Il catalogo del treebank conferma anche il perimetro delle opere. [AGDT 2.1, inventario e descrizione dell’annotazione](https://github.com/PerseusDL/treebank_data/blob/bf4334f0af5e13d16b04c1cccd6237e683ac6f5f/v2.1/Greek/README.MD).

Lo Scudo mantiene un’etichetta di tradizione esiodea senza affermare autenticità autoriale. L’Inno a Demetra mantiene autore “Anonymous” e viene associato prudenzialmente al blocco omerico. Non occorre risolvere un problema di attribuzione per escludere insieme questi testi dal training. L’Iliade costituisce circa il 97,5% dei token del blocco omerico: i risultati di blocco riflettono questa dominanza, che deve comparire nel report.

### 3.4 Probe tragico

| Documento | Token C0 | Posizioni valutate |
|---|---:|---:|
| Sofocle, Trachinie | 4.224 | 2.610 |
| Sofocle, Antigone | 3.573 | 2.076 |
| Sofocle, Aiace | 4.364 | 2.503 |
| Sofocle, Edipo re | 4.571 | 2.610 |
| Sofocle, Elettra | 4.259 | 2.331 |
| Eschilo, Supplici | 1.284 | 639 |
| **Totale** | **22.275** | **12.769** |

Sono testi a metro misto, non una categoria omogenea di trimetri. Restano fuori da ogni training e da ogni contrasto primario; si valutano sotto tutti i modelli C0 già addestrati, in entrambi i bracci. Non si stima un “effetto tragedia” su sei repliche indipendenti: cinque opere sono di Sofocle.

### 3.5 Confondimenti che delimitano le conclusioni

Nel corpus primario l’etichetta HEX coincide con la componente arcaica; manca prosa arcaica comparabile. Epoca, tradizione, genere e forma non sono separabili. Le etichette di prosa si riferiscono alle opere, senza certificazione metrica di ogni token o rimozione di eventuali citazioni in versi. L’annotazione proviene da processi e annotatori diversi: l’uniformazione UD non prova identica qualità fra opere. Non si inventa un controllo per annotatore in assenza di metadati sufficienti.

Le frasi lunghe ricevono più peso perché offrono più posizioni. Escludere i primi quattro simboli non pareggia la distribuzione delle lunghezze. Il risultato rimane condizionato a questa distribuzione; le due fasce di storia previste nel §9 la rendono visibile senza creare un’ulteriore analisi inferenziale.

## 4. Codifica e popolazione dei target

### 4.1 Trasformazione deterministica

Ordine obbligatorio: conservare righe con ID intero; mappare `PROPN → NOUN`; selezionare UPOS; ricavare DEPREL base con `lower().split(':', 1)[0]`; applicare la politica della variante; assegnare l’ID del simbolo.

UPOS conservati: `ADJ, ADP, ADV, AUX, CCONJ, DET, NOUN, NUM, PART, PRON, SCONJ, VERB`. UPOS eliminati: `PUNCT, X, INTJ, SYM`. Qualunque altro UPOS non gestito esplicitamente è un errore di input, non un’eliminazione silenziosa.

DEPREL conservati: `root, nsubj, csubj, obj, iobj, ccomp, xcomp, obl, advcl, advmod, acl, amod, appos, det, nummod, nmod, case, mark, aux, cop, cc, conj, parataxis`.

`ud23` è il nome storico del sottoinsieme di progetto: **non** è l’intero inventario delle relazioni UD. L’inventario generale comprende 37 relazioni di base e possibili sottotipi. [Documentazione UD](https://universaldependencies.org/u/dep/index.html).

| Variante | Regola | Alfabeto verificato |
|---|---|---:|
| `ud23` / C0 | UPOS:DEPREL; eliminare relazioni fuori dalle 23 | 106 |
| `ud23_oth` | Stessi UPOS; relazioni esterne aggregate in `oth` | 112 |
| `upos_only` | **Stessa maschera di ritenzione di C0**, poi eliminare DEPREL dal simbolo | 12 |

Le eliminazioni chiudono i vuoti: il contesto conta simboli trattenuti, non distanze in parole originali. Le coordinate originali restano nell’output. Non si eliminano parole aggiuntive per “pulire” risultati scomodi e non si introducono FEATS, lemma o lessico.

### 4.2 Alfabeto congelato

Per ciascuna delle tre varianti, l’inventario è l’unione dei simboli osservati nei 17 documenti, inclusi i probe. Le stringhe sono ordinate lessicograficamente, con ID interi consecutivi da 0. BOS e SEP hanno ID riservati negativi e non entrano nell’alfabeto degli esiti.

Questa scelta è **transduttiva e chiusa**: si conosce il supporto del corpus completo, compreso l’held-out, ma non si trasferiscono frequenze, transizioni o pesi dal test al training. Non si presenta quindi il protocollo come valutazione su testi futuri completamente ignoti. Un nuovo simbolo dopo il freeze causa errore; non esiste un `UNK` implicito.

### 4.3 Controlli di ritenzione

Si conserva il censimento per documento e regime originale (`HEX`, `PROSE_CLASS`, `PROSE_POST`, `OTHER_VERSE`), prima dell’unione descrittiva `PROSE_ALL`.

Il controllo A calcola, per ciascuna relazione esclusa, il numero di token con UPOS ammissibile e quella relazione, diviso per **tutti i token grezzi del regime**. Una quota >2% produce una segnalazione; non si sommano relazioni diverse per confrontarle alla soglia. Il controllo B segnala documenti con ritenzione <70%. Sono soglie diagnostiche convenzionali, non garanzie di validità linguistica.

Con gli input congelati l’audit precedente non ha prodotto bloccanti su queste soglie; la maggiore categoria segnalabile era `vocative` nella tragedia, circa 1,28%. La futura esecuzione deve ricalcolare i valori. Un risultato differente a input e codifica identici è un errore da risolvere. La cella `oth` rimane obbligatoria indipendentemente dal controllo A: nessun ramo condizionale cambia il budget.

### 4.4 Target valutabili

Una posizione è valutabile se ha **almeno quattro predecessori ordinari trattenuti nella propria frase**: indice zero-based `j ≥ 4`. La popolazione è fissata prima di vedere i punteggi ed è identica per radice e CTW, originale e rimescolato, e per le sensibilità che mantengono la maschera C0.

Tutti i token di training, inclusi quelli iniziali, contribuiscono ai conteggi. Sul test i primi quattro non ricevono un punteggio primario ma alimentano la storia. Non vi è sottocampionamento del test né budget di test `m`; si valutano tutte le posizioni eleggibili.

La variante `oth` può modificare la popolazione di target. Il confronto con C0 viene quindi segnalato come cambiamento di rappresentazione e popolazione. Non si forza una finta corrispondenza numerica fra righe diverse.

## 5. Campionamento, esclusione e semi

### 5.1 Training leave-one-block-out

Per ciascuno dei sette blocchi held-out e ciascun seme, escludere tutti i suoi documenti. Dai restanti sei blocchi estrarre esattamente `q = 8.884` token ciascuno, per `6q = 53.304` token di training C0. Il valore è il minimo della disponibilità C0 dei sette blocchi; resta 8.884 anche in `oth`, per isolare la codifica dal budget. `q_half` usa 4.442 e 26.652 token totali.

Il training è bilanciato per blocco, non per gruppo. Escludendo HEX, il training contiene 1/6 di token HEX; escludendo prosa ne contiene 2/6. La quota del **gruppo del test** è rispettivamente 1/6 e 4/6. Questa asimmetria è una proprietà dichiarata dell’estimando. Non se ne presume a priori la direzione del bias. Eliminare tale asimmetria richiederebbe un altro protocollo e non viene presentato come ottenuto dal semplice bilanciamento dei blocchi.

Q non corregge automaticamente l’asimmetria della composizione del training. Non è però dimostrato che essa penalizzi necessariamente HEX o renda il confronto conservativo: la quota del proprio gruppo non garantisce somiglianza delle sequenze. Un controesempio CTW D=8 verificato nella revisione mostra Q in diminuzione quando aumenta il peso del gruppo meno simile al target; uno scenario opposto mostra Q in aumento. I risultati e il generatore sono negli allegati della revisione. Non sono una stima del bias nel greco.

La tabella dei sette fold deve includere le quote del training HEX/prosa e del gruppo del test. Un eventuale grafico Q contro quota del proprio gruppo è soltanto una rappresentazione di questa struttura: la quota assume qui due valori determinati dal gruppo, quindi non identifica separatamente un effetto dell’esposizione.

### 5.2 Algoritmo del campione

1. Ordinare tutte le frasi del blocco per `(canonical_doc_id, part_order, source_ordinal, sent_id)`, incluse eventuali frasi senza simboli trattenuti.
2. Permutare uniformemente gli indici delle frasi con il sottoseme `sample`. Le frasi vuote non contribuiscono al budget, ma rimangono nell’universo della permutazione per stabilizzare l’accoppiamento fra codifiche.
3. Consumare frasi intere finché la successiva supera il residuo. Per quest’ultima scegliere uniformemente un segmento contiguo della lunghezza esatta residua, con sottoseme `fragment` specifico della frase.
4. Arrestarsi. Il risultato ha esattamente q token, nessuna frase ripetuta e al massimo un frammento per blocco contribuente, quindi al massimo sei frammenti per fit.
5. Registrare per ogni frase inclusa `sent_id, start, end, fragment`, con estremi zero-based nella sequenza codificata e intervallo `[start, end)`.

Non è un campione uniforme di singoli token: privilegia l’integrità delle frasi. In C0 ogni frase/frammento costituisce uno stream indipendente, inizializzato senza storia precedente. La porzione esclusa di una frase frammentata non fornisce contesto al modello.

Le sensibilità numeriche riusano esattamente il ledger C0 del medesimo seme e fold. `q_half` riusa la permutazione delle frasi, ma il taglio casuale dell’ultima frase può cambiare: **non** si garantisce annidamento token per token. `upos_only` conserva il ledger C0. `oth` riusa l’ordine delle stesse frasi ma può fermarsi altrove per le diverse lunghezze. La cella dei confini usa lo stesso campione C0.

**Decisione esplicita sul rilievo C5.** Si mantiene il frammento finale, già presente nella proposta `piano_ultimato`, dopo aver riesaminato l’obiezione della proposta `piano_finale`. La priorità operativa è il contributo esattamente uguale di token da ciascun blocco. Il costo accettato è che un taglio interno crea un inizio di stream campionato che non coincide con l’inizio della frase sorgente. BOS significa fine della storia disponibile nello stream, non prova di un confine linguistico naturale. Non si sostiene che il costo sia identicamente nullo; la perdita dell’annidamento token per token di `q_half` è parte della stessa decisione.

Il censimento supplementare C0 sui 20 semi ha rilevato 671 frammenti in 840 contributi, 563 dei quali con inizio interno alla frase. A D=8 sono direttamente interessati 3.477 target di training su 7.462.560, circa 0,0466%. Questa quota non limita matematicamente la variazione delle predizioni: i pesi posteriori possono propagare l’effetto. Eliminando tutti i frammenti, senza sostituirli, sui sette fold del primo seme, il massimo scarto assoluto di Q è stato 0,000685 bit/simbolo. È un controllo locale di fattibilità, non una sensibilità finale completa né una garanzia universale.

Il ledger e la diagnostica finale devono registrare, per blocco contribuente e coppia, `fragment_count`, `internal_start_count`, `fragment_tokens` e `direct_context_targets = Σ min(D, fragment_length)` sui frammenti con `start > 0`. Le coordinate di taglio sono condivise dai due bracci: non si contano come due decisioni indipendenti. Al più sei frammenti per coppia implicano al più 4.200 segmenti distinti nel piano da 700 coppie; 8.400 è soltanto il limite delle loro occorrenze nei due bracci. Il confronto a frasi intere resta una verifica separata di sviluppo e non aggiunge una decima cella.

### 5.3 Identità dei semi e invarianza alle etichette

Master seed: `20260706`. C0: indici 0–19; ogni sensibilità: 0–9. La nuova convenzione è `hexis-v3-rng-1`, distinta dal pilot precedente basato su CRC32.

`block_key = SHA256(JSON_canonico(lista ordinata dei canonical_doc_id del blocco))`. Il nome visualizzato del blocco, l’autore, il gruppo e l’epoca non entrano nel seme.

Per ogni estrazione si costruisce l’oggetto con le sole chiavi:

```json
{"version":"hexis-v3-rng-1","master":20260706,"seed":0,"held":"<block_key>","block":"<block_key>","purpose":"sample","sid":"","start":0,"end":0}
```

I valori fra parentesi angolari illustrano il tipo; in esecuzione sono gli hash reali. Serializzazione: JSON UTF-8, `ensure_ascii=False`, `sort_keys=True`, `separators=(',', ':')`, senza newline. Il seme intero è formato dai primi 16 byte SHA-256, big-endian. RNG: `numpy.random.Generator(numpy.random.PCG64(seme))`.

Scopi ammessi: `sample`, `fragment`, `shuffle_train`, `shuffle_eval`, `shuffle_probe`. Per `fragment` usare `sid` e estremi 0/0; per shuffle usare `sid` e gli estremi del segmento, o 0/lunghezza per la frase intera. Nel probe `block` è l’hash della lista contenente il solo documento probe. I parametri numerici, il nome della cella, la variante e le etichette non entrano nel derivatore. Questo consente l’accoppiamento previsto. I dati sono fissati e identificati nel manifest, ma l’hash della configurazione completa non è un ingrediente casuale.

Il contratto eseguibile e un vettore di riferimento sono negli allegati. Rinomine di blocchi e cambi d’ordine dei record in input non devono cambiare campioni, score o modelli. Un cambiamento effettivo dei membri di un blocco cambia il suo identificativo ed è una nuova versione del disegno.

## 6. Contratto matematico del CTW

### 6.1 Parametri e conteggi

Sia A l’alfabeto congelato, `m = |A|`, `D = 8`, `a = 0,5` pseudoconteggio **per simbolo**, `rho = 0,5` probabilità a priori di arresto. I nomi `a` e `rho` sono distinti; il vecchio `beta` ambiguo viene eliminato.

Ogni nodo s rappresenta un suffisso, percorso dal simbolo più recente al meno recente. `n_s(x)` conta gli esiti ordinari x osservati sotto quel contesto; `N_s = Σ_x n_s(x)`. La distribuzione locale è:

\[
p_s(x)=\frac{n_s(x)+a}{N_s+ma}.
\]

Non si applicano `k_min`, `gamma`, pruning euristico, selezione `argmax` o penalità supplementari. Si costruiscono tutti i contesti osservati fino a D; i sottoalberi vuoti sono rappresentati implicitamente.

La fonte metodologica è il CTW/BCT per alfabeti finiti, con evidenza integrata e media sui modelli. Le convenzioni HEXIS per stream separati e simboli di confine sono un adattamento esplicito, verificato separatamente; non sono attribuite testualmente al paper. [Kontoyiannis et al., versione 3, 2022](https://arxiv.org/abs/2007.14900v3).

### 6.2 BOS e partizione coerente

All’inizio di ciascuno stream la storia è vuota. Per ogni target ordinario, si visita la radice, poi la storia disponibile in ordine inverso, fino a D. Se la storia termina prima di D, si aggiunge un arco **BOS**, che conduce a una foglia terminale. BOS ha ID −1, compare solo nei contesti e non viene predetto.

Un nodo non terminale deve soddisfare, per ogni esito x:

\[
n_s(x)=\sum_{c\in\mathrm{children}(s)}n_{sc}(x).
\]

BOS raccoglie precisamente le osservazioni iniziali che altrimenti non avrebbero un figlio. Non si confronta mai la radice addestrata su tutti i token con figli addestrati soltanto sulle posizioni interne. I nodi a profondità D e quelli raggiunti attraverso BOS sono foglie forzate.

### 6.3 Evidenza integrata e ricorsione

L’evidenza Dirichlet del nodo è:

\[
E_s=\frac{\Gamma(ma)}{\Gamma(N_s+ma)}
\prod_{x\in A}\frac{\Gamma(n_s(x)+a)}{\Gamma(a)}.
\]

Per una foglia forzata, `W_s = E_s`. Altrimenti:

\[
W_s=\rho E_s+(1-\rho)\prod_{c}W_{sc}.
\]

Un sottoalbero privo di osservazioni ha `E = W = 1`; i fattori unitari si omettono dal prodotto senza eliminare massa di probabilità. La probabilità a posteriori di arresto è:

\[
w_s=\frac{\rho E_s}{W_s},
\]

con `w_s = 1` nelle foglie forzate. Per induzione sulla profondità, la ricorsione equivale alla somma delle evidenze di tutti gli alberi ammessi, pesate dal prior di arresto/suddivisione. La partizione dei conteggi rende coerente il confronto. L’evidenza calcolata non richiede un ordine casuale degli stream.

La famiglia di contesti comprende l’eventuale SEP e BOS secondo la convenzione del §7; il prior di arresto è sempre rho, senza una correzione automatica dipendente dal numero di archi. I teoremi asintotici per sorgenti stazionarie non vengono trasferiti senza prova al corpus composito.

### 6.4 Predizione congelata

Fissati conteggi e pesi sul training, per la storia h:

\[
q_s(x\mid h)=w_s p_s(x)+(1-w_s)q_{sc}(x\mid h),
\]

dove c è il successivo arco della storia. Su foglia forzata si usa p_s; entrando in un sottoalbero mai osservato la predizione è uniforme, `1/m`. Alla radice si ottiene `q_CTW`.

Durante tutta la valutazione, **né i conteggi né i pesi w cambiano**. La storia procede lungo la sequenza di test e può contenere simboli test precedenti. I simboli successivi non vengono letti per predire il target; la rappresentazione annotata resta comunque offline, come chiarito nel §1.2.

Questo predittore è una media congelata delle predizioni dei modelli pesati sul training. Non è la probabilità congiunta del test ottenuta aggiornando online il posterior sugli alberi. Il prodotto delle sue probabilità condizionali è comunque un codice predittivo ben definito. La radice di confronto usa gli stessi conteggi globali del training e lo stesso a:

\[
q_0(x)=\frac{n_\varnothing(x)+a}{N_\varnothing+ma}.
\]

### 6.5 Aritmetica e controlli numerici

Le evidenze si calcolano in logaritmi naturali con `lgamma`, somma stabile e `logaddexp` o equivalente; si convertono in bit soltanto le perdite finali. Usare float64, mai float32. La radice e il CTW devono dare probabilità finite e positive, somma 1 entro tolleranza.

Conservare separatamente `log_rho` e `log_one_minus_rho`. La forma `rho = 1 - 2**(-(m-1))` può arrotondare a 1 per m=106: non deve essere usata per rappresentare il prior suggerito come default in una parte della letteratura. Questa prova numerica rimane nel test suite anche se quella configurazione non è una cella finale.

Una deviazione di normalizzazione entro `1e-12` è tollerata nei piccoli test; oltre soglia è errore. Il clipping di un peso appena oltre 1 è ammesso soltanto se lo scarto è ≤`1e-12`, con controllo esplicito; non si usa clipping generalizzato per nascondere problemi. Nei test di enumerazione la tolleranza assoluta sulle probabilità è `1e-12`, sui log-evidence `1e-10`. Su output grandi la tolleranza di ricostruzione delle CE è `1e-9` bit/simbolo, su riproduzioni fra piattaforme `1e-8`. I conteggi e le coordinate devono coincidere esattamente.

## 7. Confini e controllo di ordine

### 7.1 Configurazione primaria dei confini

C0 azzera la storia ad ogni frase o frammento. Non si concatenano frasi soltanto perché contigue nella permutazione di campionamento. Non si attraversano documenti, parti o lacune. Il training aggrega statisticamente stream separati.

### 7.2 Sensibilità `bound`

Si ordina il campione per identità e ordine sorgente. Due frasi si possono collegare soltanto quando:

- appartengono allo stesso documento canonico **e allo stesso prefisso sorgente**;
- hanno stessa parte e ordinali sorgente consecutivi;
- hanno ranghi consecutivi nell’elenco completo delle frasi, costruito prima di ritenzione e campionamento;
- entrambe sono intere e non vuote.

La regola identifica adiacenza nel treebank osservato, non dimostra continuità dell’intera opera antica. Nessun collegamento attraversa il cambio fra Ateneo XII e XIII. Una frase non selezionata, vuota o frammentata interrompe la catena. Due frasi separate da un salto negli identificativi rimangono separate anche se diventano vicine nel sottoinsieme.

Fra frasi ammesse si inserisce SEP, ID −2, **solo nel contesto**. SEP consuma una posizione della profondità strutturale D, non è target e non aumenta m. La storia può attraversarlo; il contatore di predecessori nella frase corrente riparte comunque da zero. Pertanto le coordinate eleggibili rimangono quelle di C0. Non si inseriscono EOS o altri simboli.

### 7.3 Rimescolamento obbligatorio, accoppiato

Per ogni coppia fold/seme e per ogni cella:

1. Costruire una sola volta il campione di training.
2. Preparare un braccio originale e un braccio rimescolato.
3. Nel secondo permutare uniformemente i simboli **entro ciascuna frase campionata o frammento**, dopo il campionamento. Ogni elemento porta con sé la coordinata sorgente; la coordinata dello slot resta distinta.
4. Addestrare da zero un CTW sul training rimescolato.
5. Rimescolare indipendentemente ciascuna frase del blocco held-out, con scopo RNG `shuffle_eval`, e valutarla sotto il modello rimescolato.
6. Per `bound`, rimescolare prima entro ogni frase e poi applicare esattamente i medesimi collegamenti e SEP del braccio originale. SEP non viene spostato.

Si impiega **una permutazione per seme**: 20 realizzazioni accoppiate in C0 e 10 in ogni sensibilità. Non si aggiungono repliche sulla base di un risultato vicino a zero. Campionamento e permutazione contribuiscono congiuntamente alla variabilità fra semi; il disegno non stima separatamente le loro componenti di varianza.

Il rimescolamento conserva esattamente lunghezza, multinsieme dei simboli per frase/frammento e conteggi di radice del training. Non conserva n-grammi, dipendenze sintattiche o grammaticalità. Frasi con simboli tutti identici possono non cambiare: registrare la quota di slot il cui simbolo cambia, senza ripetere la permutazione finché “cambia abbastanza”.

La permutazione senza rimpiazzo introduce le proprie dipendenze da composizione finita. Il controllo non è una sorgente i.i.d. né una stima universale del bias del CTW. Serve a confrontare l’ordine osservato con **questa trasformazione definita**, mantenendo composizione e segmentazione. Un punteggio Q positivo non isola automaticamente sintassi, metro o un effetto causale.

### 7.4 Perché occorre una differenza di guadagni

Il controllo sintetico precedente ha prodotto guadagni positivi di circa 0,52–0,89 bit in testi internamente i.i.d. ma eterogenei fra blocchi: il contesto può aiutare a riconoscere la composizione del testo. Dopo confronto con il rimescolamento il residuo era circa −0,0014–0,0018; nella sorgente con dipendenza ritardata rimaneva circa 0,53. È la ragione empirica per rendere centrale il confronto accoppiato.

Anche se le radici di training dei due bracci sono identiche, **le CE di radice del test possono differire**: escludendo i primi quattro slot, il rimescolamento cambia quali simboli entrano nel punteggio. Non si semplifica Q in `CE_CTW_shuffled − CE_CTW_original`. Si calcolano e conservano tutti e quattro i termini.

Nei sette fold reali del primo seme già esaminati, G rimescolato è zero alla precisione numerica registrata, dunque Q coincide numericamente con G originale. Questo esito preliminare viene dichiarato prima del run finale; non si assume che valga per tutti i semi e le celle. I 700 fit rimescolati sono un controllo predefinito che può smentire l’interpretazione del solo G, non un’operazione da omettere perché il primo pilot è favorevole.

Non esiste un teorema che imponga G rimescolato esattamente nullo in campioni finiti: la miscela CTW non seleziona obbligatoriamente la radice. Nel controllo i.i.d. supplementare il peso di arresto alla radice è circa 0,80775 e il guadagno circa 0,000195 bit/simbolo. Inoltre il rimescolamento entro frase non produce in generale una sequenza i.i.d. La coincidenza numerica col predittore di radice va descritta come risultato osservato, non come necessità matematica.

## 8. Misure, pesi e risultati obbligatori

### 8.1 Perdite e guadagni

Sia I_b l’insieme degli slot eleggibili del blocco b nella variante corrente; `n_b = |I_b|`. Per seme s e braccio z, originale O o rimescolato R:

\[
CE_{b,s}^{z}=\frac{1}{n_b}\sum_{i\in I_b}-\log_2 q_{CTW,s}^{z}(x_i^{z}\mid h_i^{z}),
\]

\[
CE_{0,b,s}^{z}=\frac{1}{n_b}\sum_{i\in I_b}-\log_2q_{0,s}^{z}(x_i^{z}),
\qquad G_{b,s}^{z}=CE_{0,b,s}^{z}-CE_{b,s}^{z}.
\]

La misura centrale è:

\[
Q_{b,s}=G_{b,s}^{O}-G_{b,s}^{R}.
\]

Unità: bit per simbolo codificato eleggibile. G può essere negativo; Q può essere negativo. Non si tronca a zero nessuno dei due. Q esprime il vantaggio aggiuntivo del contesto sotto l’ordine osservato rispetto al controllo specificato.

### 8.2 Aggregazione

Dentro ogni documento e blocco si sommano le perdite e si divide per il numero di target. Ciò pesa i documenti secondo i target, senza attribuire all’Inno lo stesso peso dell’Iliade. Si conservano comunque i risultati separati degli 11 documenti, perché la media di blocco non ne nasconda l’eterogeneità.

Per ogni seme:

\[
D_{Q,s}=\frac{1}{2}\sum_{b\in HEX}Q_{b,s}
-\frac{1}{5}\sum_{b\in PROSE\_ALL}Q_{b,s}.
\]

Il risultato primario è `D_Q = mean_s D_Q,s` in C0. Si riportano obbligatoriamente anche i sette `mean_s Q_b,s`, i corrispondenti G originali/rimescolati e i contrasti `D_G_original` e `D_G_shuffled`. Nessuno di questi ultimi sostituisce Q perché dà una separazione maggiore.

I gruppi hanno peso uniforme **fra blocchi**, non fra token. La media sui semi è aritmetica. La SD sui semi usa denominatore S−1; si riportano inoltre minimo e massimo. Non si calcolano p-value, bootstrap CI, Holm, intervalli di confidenza della popolazione, Bayes factor fra regimi o percentuali di “significatività”. Non si riutilizzano i token, i documenti del medesimo blocco o i semi come n indipendenti.

Il contrasto è specifico della procedura leave-one-block-out con training diverso per blocco. Non è il confronto dei sette blocchi sotto un unico modello addestrato comune. Si può ricostruire esattamente dai sette punteggi e questa ricostruzione è un test obbligatorio.

### 8.2-bis Riaggregazione obbligatoria per target eleggibili

Il contrasto primario rimane quello con peso uniforme fra blocchi. Per tutte le nove celle si calcola anche, sugli stessi Q già disponibili:

\[
D_{Q,s}^{token}=\frac{\sum_{b\in HEX}n_b Q_{b,s}}{\sum_{b\in HEX}n_b}
-\frac{\sum_{b\in PROSE\_ALL}n_b Q_{b,s}}{\sum_{b\in PROSE\_ALL}n_b}.
\]

I pesi sono i numeri di target **eleggibili** della variante corrente, non i token grezzi, i token trattenuti complessivi o i q di training. Si riportano analogamente le due componenti G originale/rimescolato, verificando `D_Q_token = D_G_original_token − D_G_shuffled_token`. Media, SD, minimo e massimo si calcolano sugli stessi semi della cella. I confronti fra sensibilità e C0 restano accoppiati sui primi dieci semi.

In C0 il peso del blocco esiodeo nel lato HEX passa dal 50% al 12,0263%, perché contribuisce 6.375 dei 53.009 target eleggibili HEX. La riaggregazione cambia la domanda: descrizione del blocco medio contro descrizione del target medio nel gruppo. Nessuna delle due è una correzione inferenziale dell’altra; non si sceglie quella con maggiore separazione. Questa lettura non addestra modelli, non introduce una decima cella e non cambia il budget né gli output per posizione. Le sintesi sono emesse soltanto dopo i controlli del §14.2.

### 8.3 JSD delle distribuzioni di radice: R1

Per ciascuna variante, sui **token originali completi** di ciascun blocco primario, inclusi quelli iniziali, costruire:

\[
r_b(x)=\frac{n_b^{all}(x)+0,5}{N_b^{all}+0,5m}.
\]

Queste sono distribuzioni descrittive dell’intero blocco, distinte dalle radici di training leave-one-block-out utilizzate per G. Pubblicare anche i conteggi e le frequenze non smussate: lo smoothing non deve nascondere il censimento.

Per p e q, con `u = (p+q)/2`:

\[
JSD(p,q)=\tfrac12\sum_xp(x)\log_2\frac{p(x)}{u(x)}
+\tfrac12\sum_xq(x)\log_2\frac{q(x)}{u(x)}.
\]

Si calcolano le 21 coppie fra sette blocchi e la matrice simmetrica 7×7; la diagonale è zero. Si formano inoltre i centroidi `r_HEX = mean dei 2 r_b` e `r_PROSE = mean dei 5 r_b`, quindi la loro JSD. Questa non coincide con la media delle JSD di coppia, che non viene usata come sostituto.

Si pubblicano i contributi di ogni simbolo alla JSD dei centroidi, con somma verificata. Le distribuzioni hanno supporto comune; la JSD è in [0,1] bit e non richiede probabilità strettamente positive. Nel codice si gestisce correttamente `0 log 0 = 0` anche se lo smoothing rende positivi gli input correnti. La divergenza non viene chiamata distanza metrica; non si introduce clustering con assunzioni metriche implicite. Fonte: Jianhua Lin, *Divergence Measures Based on the Shannon Entropy*, 1991, PDF fornito `jensen-shannon.pdf`.

R1 viene eseguita per C0, `oth` e `upos_only`, senza fit CTW e senza semi. Una differenza marginale non dimostra differenza nell’ordine, e viceversa. R1 è obbligatoria ma non una famiglia inferenziale aggiuntiva.

### 8.4 Probe senza nuovo training

Per ogni documento tragico valutare i due bracci sotto tutti i 7×20 modelli C0 originali/rimescolati, usando `shuffle_probe` per la trasformazione del test. Calcolare CE, CE0, G e Q per documento/fold/seme. Riportare le sette medie sui semi e una sintesi documentale che assegna peso 1/7 ai fold e 1/20 ai semi.

I fold condividono training e i semi condividono testi: la dispersione è descrittiva, non un intervallo inferenziale. Non aggregare le sei tragedie in un ottavo blocco e non confrontare direttamente la sintesi del probe con un primario come se avessero identica esposizione al training. Il probe non è una verifica indipendente di generalizzazione fuori corpus, dato che il suo inventario è incluso nell’alfabeto.

## 9. Diagnostica del modello e delle posizioni

Ogni fit produce: numero di nodi per profondità strutturale; distribuzione del supporto dei nodi in classi `0, 1, 2–4, 5–9, ≥10`; numero di esiti osservati alla radice; quota di target test mai osservati alla radice; massa predittiva instradata verso il primo sottoalbero non osservato; tempi e memoria. I nodi con supporto zero sono impliciti: la classe zero non si ottiene enumerando un albero esponenziale; si riportano separatamente i rami impliciti incontrati in valutazione.

Per una storia, la massa che si arresta in un nodo osservato è il prodotto delle probabilità di prosecuzione lungo il cammino, moltiplicato per w_s. La massa residua al primo ramo non osservato è `unseen_mass`. Le masse di arresto osservate più `unseen_mass` devono sommare a 1.

Definire `lexical_context_length(s)` come il numero di archi ordinari nel contesto del nodo: BOS e SEP non contano. Si accumula l’istogramma delle masse osservate per tale lunghezza e si riporta, se la massa osservata è positiva, la media condizionata alla parte osservata:

\[
L_{resolved}=\frac{\sum_{s\ osservati}\lambda_s\,lexical\_context\_length(s)}{1-unseen\_mass}.
\]

Nel codice il denominatore viene calcolato come somma diretta delle masse risolte, evitando la perdita di precisione di `1 − unseen_mass` quando la massa residua è quasi uno. Con training vuoto si assegna massa non osservata 1 e nessuna massa risolta. Se il denominatore è zero, il valore è `null` con motivo `no_resolved_mass`, non zero. Questa è una diagnostica della componente risolta dai dati. **Non** è l’aspettativa della profondità di tutti gli alberi posteriori: nei sottoalberi vuoti il prior consente ulteriore profondità, pur dando la medesima predizione uniforme. Il `weighted_depth` del vecchio prototipo, che collassa tale parte al primo nodo assente, resta un campo storico e viene ritirato dagli output scientifici v3.

Pubblicare inoltre, per ciascun blocco e braccio, numero di target e guadagni nelle fasce `4 ≤ available_past < 8` e `available_past ≥ 8`; usare la stessa definizione nella cella `bound`. Una fascia vuota ha conteggio zero e score null con motivo esplicito. Non crearne altre dopo aver osservato i risultati. Non si selezionano contesti “interessanti” per sostenere una conclusione principale; eventuali esempi linguistici successivi sono esplorazione separata e dichiarata.

## 10. Matrice finale delle analisi e budget

| Cella | Unica variazione rispetto a C0 | Semi | Fit originali | Fit rimescolati |
|---|---|---:|---:|---:|
| C0 | m=106; D=8; a=0,5 per simbolo; rho=0,5; q=8.884; reset | 20 | 140 | 140 |
| a_total1 | a=1/m, massa Dirichlet totale 1 | 10 | 70 | 70 |
| q_half | q=4.442 | 10 | 70 | 70 |
| D6 | D=6 | 10 | 70 | 70 |
| D12 | D=12 | 10 | 70 | 70 |
| rho09 | rho=0,9 | 10 | 70 | 70 |
| oth | alfabeto `ud23_oth`, m=112; q invariato | 10 | 70 | 70 |
| upos | alfabeto `upos_only`, m=12; maschera C0 | 10 | 70 | 70 |
| bound | collegamenti e SEP del §7.2 | 10 | 70 | 70 |
| **Totale** | **9 celle, 700 coppie** | | **700** | **700** |

Sono quindi **1.400 fit**, più valutazioni senza nuovo training. I 280 fit C0 generano anche 1.680 valutazioni documento-probe: 6 documenti × 7 fold × 20 semi × 2 bracci. R1 non aggiunge fit. Non vi sono combinazioni fattoriali fra sensibilità.

La sensibilità al prior quasi sempre fermante della letteratura rimane nella validazione numerica precedente; non entra nell’analisi finale, dove `rho09` dà una perturbazione esplicita e leggibile. `argmax`, selezione monotona e regole `k_min/gamma` non costituiscono sensibilità del nuovo modello.

Per ogni sensibilità confrontare i suoi dieci semi con **gli stessi primi dieci semi C0**, mediante differenze accoppiate per blocco/seme. La sintesi C0 a venti semi resta il risultato centrale, ma non va sottratta a una sensibilità a dieci semi chiamando la differenza “accoppiata”.

Variazioni di a, rho, q e D misurano dipendenza del risultato da scelte del predittore e del campionamento. `oth`, `upos` e `bound` cambiano rappresentazione o disponibilità di contesto: descriverle come tali. Le CE di alfabeti diversi non hanno un’identica scala informativa di riferimento; un valore minore in UPOS non significa automaticamente organizzazione linguistica maggiore. Anche i guadagni riguardano task differenti.

Non si impone stabilità di segno come condizione per completare il progetto. Un’inversione deve essere riportata come dipendenza della descrizione dalle scelte analitiche, non corretta con un’altra cella. Non si sceglie il modello finale in base al massimo contrasto fra gruppi.

## 11. Contratti software e output

### 11.1 Separazione delle responsabilità

Le API seguenti sono requisiti di implementazione, non comandi già disponibili nel commit verificato.

| Componente | Input | Output e obblighi |
|---|---|---|
| Lettore/censimento | File CoNLL-U con hash attesi | Record sorgente con identità e ordine; errore su duplicati o metadati mancanti |
| Codificatore | Record + variante | Sequenze, mappa coordinate, inventario congelato e audit delle eliminazioni |
| Campionatore | Record dei blocchi, chiavi dei blocchi, held-out, q, seme | Ledger e stream; nessuna etichetta di regime |
| CTW `fit` | Stream di interi, m, D, a, log-prior | Modello congelato, diagnostica e fingerprint |
| CTW `predict_proba` | Modello congelato, storia | Vettore normalizzato su A, nessuna mutazione |
| Score | Modello, sequenze, coordinate, maschera eleggibile | Perdite per posizione e aggregati senza etichette |
| Accoppiamento | Output originale/rimescolato sullo stesso insieme di slot | Q e controlli di corrispondenza |
| Annotazione | Score + registro + mappa blocchi | Gruppi e metadati per tabelle; unica fase che usa regime per aggregare |
| R1 | Conteggi completi per blocco e variante | Radici, centroidi, JSD e contributi |
| Report | Tabelle e manifest validati | Figure e testo che esplicitano corpus, pesi e limiti |

Configurazione: schema rigoroso con chiavi ammesse, tipi e intervalli. Rifiutare chiavi sconosciute, parametri storici ritirati, NaN/Inf, booleani usati come interi, D negativo, q non positivo, a non positivo, rho fuori (0,1), semi ripetuti, celle duplicate, alfabeti inconsistenti e gruppi/blocchi incompleti. La verifica di sola presenza delle chiavi oggi presente nel progetto è insufficiente.

Gli interi dei conteggi devono evitare overflow; i simboli sono interi non negativi <m. Gli ID negativi sono riservati: BOS non deve essere fornito come elemento dello stream, SEP è ammesso soltanto in `bound`. La funzione pubblica deve rifiutare float convertiti silenziosamente in interi. D=0 e training vuoto rimangono casi di test, ma il protocollo reale impone D e q delle celle dichiarate.

### 11.2 Tabelle sorgente e coordinate

Output `documents.csv`: una riga per documento canonico, con `doc_id, source_prefixes, work, author_label, period_label, regime, role, dependence_block, raw_tokens, raw_sentences, kept_tokens, eligible_tokens, retention, flags`, distinto per variante dove necessario.

Output `coordinates.parquet`: una riga per token ordinario trattenuto, con `variant, slot_uid, doc_id, sent_id, source_prefix, part_order, source_ordinal, source_rank, raw_token_id, encoded_index, symbol_id, available_past, eligible`. `slot_uid` è un intero stabile assegnato nell’ordine canonico di ciascuna variante; la chiave completa comprende la variante. Identità testuali conservate in dizionari, senza ripetere stringhe lunghe nei vettori dei punteggi.

Output `alphabet.json`: variante, lista ordinata dei simboli, m, mapping, perimetro dei 17 documenti e hash. Il file dei conteggi di audit include anche tutte le righe eliminate con ragione e coordinate, o una tabella sorgente equivalente da cui ricostruirle esattamente.

### 11.3 Ledger e identificazione delle esecuzioni

Per ogni fold/seme e campione distinto: `sample_ledger.json`, con chiavi dei sei blocchi, q, frasi selezionate, estremi, frammenti, coordinate sorgente del segmento e seed derivati. Le celle numeriche possono riferire lo stesso ledger tramite hash; non duplicarlo fingendo campioni indipendenti.

L’esecuzione scientifica è identificata da `run_id = SHA256(JSON canonico del run_contract)`. Il `run_contract` comprende versione della specifica, commit del codice, hash dei dati, hash del registro e degli alfabeti, hash della configurazione, lock delle dipendenze e versione RNG. Non comprende timestamp, percorsi assoluti, etichette di macchina o tempi misurati. Il manifest esterno registra anche questi dati ambientali, senza usarli come seed.

Per fit: chiave `(run_id, cell, held_block_key, seed, arm)`. Per una coppia: stessa chiave senza `arm`. Un probe aggiunge `probe_doc_id` alla chiave della valutazione, senza creare un modello.

### 11.4 Punteggi per posizione

Salvare tutte le posizioni dei sette blocchi in tutte le celle, e dei sei probe in C0, in partizioni Parquet per coppia/cella. Una riga accoppia lo stesso **slot**, non necessariamente lo stesso token originale:

`slot_uid, original_symbol_id, shuffled_symbol_id, shuffled_origin_slot_uid, loss_ctw_original, loss_root_original, loss_ctw_shuffled, loss_root_shuffled, unseen_mass_original, unseen_mass_shuffled, resolved_mean_original, resolved_mean_shuffled`.

Le quattro perdite e le diagnostiche numeriche sono float64; `resolved_mean` è nullable secondo §9. Le coordinate dello slot e della provenienza del simbolo rimescolato devono consentire la ricostruzione esatta. La prima è il luogo in cui si valuta; la seconda è il token spostato. Per probe si usa la medesima struttura e il dizionario delle sue coordinate.

I metadati di partizione contengono `run_id, cell, fold, seed, variant, target_role, target_doc_id se probe, model_hash_original, model_hash_shuffled, ledger_hash`. Nessuna colonna di gruppo entra nel core. L’accoppiamento è verificato con una join uno a uno sugli slot, non mediante la semplice uguaglianza delle lunghezze.

Per i nodi non si salva l’intero albero di ogni fit: si conserva il fingerprint e si rigenera da campione e parametri. È sufficiente mantenere in memoria una coppia di modelli; terminata valutazione e scrittura, liberarla. I dizionari condivisi delle coordinate restano piccoli.

### 11.5 Aggregati e figure obbligatorie

`model_diagnostics.csv`: una riga per fit con tempi, picco RSS e statistiche del §9; istogrammi di massa e supporto in JSON associato. `document_scores.csv`: una riga per documento/seme/cella/braccio, numero di target, somme delle perdite, CE, CE0 e G. `block_pairs.csv`: una riga per blocco/seme/cella, i quattro CE, G nei due bracci e Q. `contrasts.csv`: una riga per cella/seme con medie dei gruppi e D_Q, D_G originali/rimescolati.

`seed_summaries.csv`: media, SD campionaria, minimo, massimo e S effettivo di ogni quantità prevista. `sensitivity_pairs.csv`: differenze rispetto a C0 sugli stessi primi dieci semi, con tipo di cambiamento (`numerical`, `budget`, `representation`, `boundary`). `probe_scores.csv`: valori per documento/fold/seme e sintesi dichiarate. `root_distributions.csv`, `jsd_pairs.csv`, `jsd_centroids.csv`, `jsd_contributions.csv`: risultati R1, per variante. `past_buckets.csv`: le due fasce prefissate.

Figure obbligatorie, generate esclusivamente da queste tabelle:

1. Corpus: quantità e ritenzione per documento, con separazione visibile fra primari e probe.
2. Sette blocchi: G originale e rimescolato affiancati; pannello Q; punti per seme e media. Se si mostrano barre, indicare esplicitamente “min–max fra semi”, mai “CI”.
3. D_Q C0 e otto sensibilità, con valori C0 dei primi dieci semi nel pannello dei confronti accoppiati.
4. R1: heatmap 7×7 C0, valori dei centroidi nelle tre varianti e contributi dei simboli; tabella completa nell’allegato, senza filtri che eliminino contributi sfavorevoli.
5. Supporto dei contesti e massa non osservata; evidenziare la distinzione fra profondità massima ammessa e profondità sostenuta dai dati.
6. Probe: sei documenti separati, sette medie di fold per documento e sintesi; nessuna barra di errore inferenziale.

Non si producono figure per chunk da 1.000 token, reti di modelli di riferimento, lessici di contesti o learning curve. Gli esempi filologici non sono un deliverable necessario alla chiusura del progetto ridimensionato.

`aggregation_weights.csv` contiene, per variante e blocco, gruppo, n eleggibili, peso primario e peso per target. `contrasts.csv` e `seed_summaries.csv` includono `aggregation = equal_block | eligible_token_weighted`, con chiavi distinte e i due schemi sempre affiancati. I riepiloghi relativi ai gruppi sono prodotti soltanto da `run_report` dopo il controllo di completezza; le pipeline di fit producono score individuali e le relative somme, non contrasti intermedi.

Nel pannello dei contrasti della figura 3 aggiungere la riaggregazione per target, identificandone il diverso estimando. Non aggiungere una figura o un fit obbligatorio. Le quote del training e le metriche dei frammenti entrano nelle tabelle diagnostiche esistenti.

### 11.6 Manifest, ripresa e errori

Ogni partizione viene scritta su file temporaneo nella directory di destinazione, verificata e rinominata atomicamente. Il manifest registra dimensione, hash, numero di righe, schema e stato `complete`. Un file temporaneo non conta come risultato.

`--resume` riutilizza una partizione soltanto se contratto, hash e cardinalità coincidono; altrimenti fallisce. Non si mescolano risultati di commit o configurazioni diversi. Non esiste sovrascrittura silenziosa: una nuova versione produce un nuovo run_id; una directory già completa rimane immutabile. I messaggi di errore identificano file, documento, frase, cella e fase interessati senza riportare interi testi.

Un denominatore zero in una fascia secondaria produce null motivato. Un blocco primario senza target, un budget impossibile, un modello non finito, una mancata coppia o un parametro non previsto arrestano la cella e impediscono il report finale. Non vengono esclusi automaticamente blocchi o semi che causano errori. Un’esecuzione incompleta conserva evidenza diagnostica ma non porta lo stato `COMPLETE`.

## 12. Test di accettazione

I test devono verificare proprietà o casi con risposta indipendentemente nota. Non è sufficiente confrontare la funzione con la sua stessa formula riscritta. Le prove esatte precedenti forniscono un riferimento indipendente; il porting deve conservarne casi e tolleranze, non soltanto copiare l’implementazione.

| ID | Proprietà e criterio | Evidenza attuale / azione di integrazione |
|---|---|---|
| T01 | Hash dei tre file, unicità dei sent_id, 18 prefissi → 17 documenti | Già verificato; gate del lettore canonico |
| T02 | 202.989 token e 13.919 frasi; conteggi per documento del JSON atteso | Già verificato; uguaglianza esatta richiesta |
| T03 | Tutte le regole UPOS/DEPREL, sottotipi, righe multiword/empty, input malformati | Riutilizzare casi validi presenti, aggiungere casi mancanti |
| T04 | m=106/112/12; maschera e coordinate UPOS identiche a C0 | Verificato anche nel nuovo contratto |
| T05 | Nessun membro del blocco held-out nel training; probe mai nel training | Verificato; assert sulle identità complete |
| T06 | q esatto; senza rimpiazzo di frasi; ≤1 frammento/blocco; vuoti e budget impossibile | Contratto eseguibile incluso |
| T07 | Invarianza all’ordine dei record e alla rinomina delle etichette; ledger riusati nelle celle previste | Contratto e nuovi test di integrazione |
| T08 | Vettore RNG di riferimento; separazione degli scopi; ripetibilità | 3.360 chiavi derivate controllate senza collisioni; fissare vettore in suite |
| T09 | Partizione dei conteggi in ogni nodo per ogni esito, BOS terminale, SEP solo contesto | Verificato nel prototipo; portare al core |
| T10 | Enumerazione di tutti gli alberi piccoli contro W e predizione | 120 casi superati; errore entro §6.5 |
| T11 | Somma delle probabilità=1; simboli/rami ignoti; training vuoto; D=0 | Già verificato; nessun NaN/Inf |
| T12 | Identità prequenziale/integrata del training; invarianza all’ordine degli stream | Già verificato; non confondere con aggiornamento del test |
| T13 | Conteggi, log-evidenze e pesi identici prima/dopo qualunque evaluation | Fingerprint invariato, anche dopo probe |
| T14 | Priori estremi in log, rho a m=106 non arrotondato implicitamente a 1 | Caso numerico già riprodotto |
| T15 | Sintetico i.i.d. 4, ciclo 3, Markov 1, lag 2, memoria variabile | Target e soglie del protocollo sintetico sotto |
| T16 | Stress m=106 | Test di esecuzione/supporto; divario dall’oracle riportato, non occultato |
| T17 | Rimescolamento conserva multinsieme e radice; mantiene maschera e separatori | Nuove coppie reali e fixture superate |
| T18 | Controesempio di eterogeneità senza dipendenza interna | G può essere positivo; controllo Q nei casi prefissati |
| T19 | Q usa quattro termini e non la scorciatoia fra due CE | Controesempio esatto incluso negli allegati |
| T20 | Aggregazione da perdite → documenti → blocchi → gruppi; peso uniforme primario e per target secondario | Fixture indipendenti con lunghezze diverse, denominatori eleggibili e identità a quattro termini |
| T21 | Sensibilità confrontate con C0 agli stessi 10 semi; OTH con popolazione distinta | Join esatte e rilevazione mismatch |
| T22 | Diagnostiche di massa e profondità risolta | 765 storie controllate, incluse SEP, D=0 e training vuoto |
| T23 | JSD simmetrica, diagonale0, range[0,1], gestionezeri e somma contributi | Test con distribuzioni uguali/disgiunte e fixture a mano |
| T24 | Sei probe × 7 fold × 20 semi × 2 bracci, senza nuovi fit | 84 valutazioni nel nuovo pilot a un seme; cardinalità finale da verificare |
| T25 | Numero finale di fit 1.400, nessun duplicato o seme omesso | Configurazione validata; controllo completezza finale |
| T26 | Scrittura atomica, hash, ripresa corretta, rifiuto di artefatti corrotti | Da implementare e verificare con interruzione simulata |
| T27 | Tabelle e figure ricostruibili dagli output per posizione | Da verificare nella pipeline canonica |
| T28 | Nessun import di `candidates/` o delle utility inferenziali nel percorso scientifico v3; nessun test-gate saltato | I test delle utility statistiche conservate restano ammessi; inventario dei gate ricostruito |
| T29 | Stesso dataset/campione: ripetibilità esatta identità; CE entro tolleranza fra piattaforme | Gate di riproducibilità, senza promessa di bit-identità dei float |
| T30 | Coerenza del perimetro e blocco dei contrasti prima dei certificati e della completezza | Rifiuto di hash diversi, certificati assenti, celle/fit/probe/R1 mancanti, duplicati e artefatti corrotti; controlli §14.2 |

T08 comprende due campagne distinte: la pipeline sintetica precedente controllava 1.680 chiavi derivate con la propria convenzione; `validate_contract.py` ne controlla 3.360 con `hexis-v3-rng-1`, su 20 semi × 7 held-out × 6 contributori × 4 scopi. Non sono lo stesso insieme raddoppiato automaticamente dai bracci. I risultati, la versione del derivatore e le chiavi considerate restano identificati separatamente. Il controllo di collisione su questi insiemi non prova assenza universale di collisioni.

### 12.1 Batteria sintetica congelata

Riutilizzare gli algoritmi di generazione e i semi del precedente `verify_synthetic.py`, già identificati dagli hash del pacchetto CTW. Training 53.304, test indipendente 100.000, primi quattro target esclusi, cinque semi per le sorgenti piccole. Non rigenerare fino al passaggio.

| Sorgente | Regola | Criterio quantitativo |
|---|---|---|
| i.i.d. uniforme, m=4 | Estrazioni indipendenti equiprobabili | \|CE−2\| ≤0,02 |
| Ciclo deterministico, m=3 | Successione periodica di tre simboli | CE <0,02 |
| Binaria Markov 1 | P(stesso simbolo)=0,8 | \|CE−h₂(0,2)\| ≤0,03 |
| Binaria lag 2 | P(copia del simbolo a distanza 2)=0,9 | \|CE−h₂(0,1)\| ≤0,03 |
| Memoria variabile | Generatore precedente, contesti di lunghezza 1/2 | Scarto dall’oracle della realizzazione ≤0,03 |

L’implementazione di generatore, probabilità oracle e semi viene importata come fixture verificabile dall’archivio precedente, fuori dalla quarantena `candidates/`; non va ricostruita a memoria. Per renderla disponibile senza dipendere da una conversazione, il pacchetto allegato al piano contiene i relativi file di riferimento. Gli script sono evidenza e fixture, non moduli da importare nella pipeline scientifica.

Stress m=106: tre semi per i.i.d. uniforme, lag 2 con copia 0,9 e innovazione uniforme 0,1, e nucleo binario frequente più simboli rari. Nel secondo caso la probabilità di coincidenza è `0,9 + 0,1/106`, non semplicemente 0,9: il riferimento è circa 1,13109 bit. Non imporre che il CTW raggiunga l’oracle con il campione disponibile; imporre conteggi, normalizzazione, esecuzione e registrazione del divario. Presentare un deficit noto come “test passato di accuratezza” sarebbe scorretto.

La verifica di eterogeneità e quella sul rimescolamento conservano generatori e semi degli esperimenti precedenti. Le soglie di piccolo residuo Q nei casi noti verificano quei casi sintetici; non calibrano un test di significatività sul corpus greco.

### 12.2 Stato del nuovo contratto eseguibile

`validate_contract.py` ha verificato la struttura del piano, campionamento e coordinate, ed eseguito 14 fit C0 accoppiati — sette fold, primo seme della nuova convenzione — più una coppia `bound`, per **16 fit**. Ha valutato i sei probe sotto i due bracci dei sette fold, per **84 valutazioni**. Il risultato è PASS. Non sono stati prodotti contrasti scientifici fra gruppi da questo pilot.

`validate_diagnostics.py` ha verificato **765 storie**. Il controesempio sulla cancellazione impropria delle radici dà Q≈0,71346, mentre la scorciatoia fra le sole CE dà circa −0,66505: perfino il segno può essere sbagliato. È una correzione operativa sostanziale recepita nelle formule e negli output.

La revisione del 12 settembre riesegue il contratto da 16 fit sotto NumPy 2.5.1 e allega i confronti fra versioni, l’ablazione dei frammenti, i controesempi sintetici, la riaggregazione per target e i test di rifiuto dei manifest incompleti/corrotti. I risultati sono in `revision_validation.json`, `numpy_*_validation.json`, `scores_validation.json` e `report_validation.json`; i manifest della prova di report sono fixture sintetiche, non i risultati dei 1.400 fit.

Questi script verificano il contratto e il riferimento separato; non certificano l’implementazione futura dei file della repository. Una specifica completa può definire tutti i gate, ma soltanto il codice integrato potrà superarli.

## 13. Migrazione della repository

### 13.1 Atto unico di aggiornamento

Creare il ramo di implementazione dalla revisione verificata, preservando la storia Git. Registrare una decisione **V3-001** in un nuovo namespace, così da non collidere con D55 e con i suoi atti tecnici. V3-001 sostituisce integralmente il disegno operativo v2.1 e le proposte A/B per le esecuzioni v3. D01–D54 e gli atti G1/D55 rimangono documentazione storica; nessuna loro clausola metodologica sopravvive implicitamente in conflitto con questo piano.

Si mantengono esplicitamente: immutabilità dei dati grezzi; provenienza; esclusione di `candidates/`; indipendenza del core dalle etichette; riproducibilità; rifiuto di sovrascritture silenziose; test con asserzioni effettive. Si sostituiscono selettore, famiglia delle analisi, unità di esclusione, inferenza, gate e output secondo questa specifica.

Il pacchetto di migrazione comprende nello stesso commit documentale: MASTER_SPEC, Decision Log, roadmap, indice, handoff, AGENTS/CLAUDE, configurazione e registro. La ratifica tecnica precedente dell’audit non deve essere citata come se avesse già ratificato tutte le attribuzioni documentali del vecchio registro proposto. Il nuovo registro riporta le identità verificate e le convenzioni di raggruppamento qui decise.

Il file allegato `hexis_v3_design.json` porta `FINAL_PLAN_NOT_APPLIED`: è la specifica strutturata consegnata, non un override da far accettare surrettiziamente alla vecchia CLI. Durante l’implementazione autorizzata si convertono i suoi contenuti nello schema v3 e si deposita il registro canonico con lo stato richiesto dalla nuova pipeline, insieme alla decisione V3-001. Non si disabilita il controllo di ratifica della versione precedente per poter eseguire v3.

**Clausola obbligatoria di V3-001 — eccezione autorizzata al freeze v2.1.** Registrare che la sessione dell’11 settembre 2026 contiene l’autorizzazione del responsabile a verificare il cambiamento di modello anche sui dati reali, prima del vecchio G2, mantenendo intatta la repository. Tale autorizzazione prevale sulla regola operativa precedente per i pilot isolati; non costituisce un passaggio retroattivo di G2. Distinguere: data dell’autorizzazione/attività ricostruita dal registro di sessione; data del deposito dell’atto in Git; identificativi delle prove. Il documento non deve inventare l’ora del consenso se non registrata.

L’atto include le campagne da 203 fit reali C0/sensibilità, il controllo di ordine, le verifiche successive del contratto e le verifiche di revisione del 12 settembre, con riferimenti ai risultati e alle eventuali riesecuzioni. “203 fit” non è dichiarato totale di ogni invocazione mai effettuata. Le riesecuzioni non diventano repliche scientifiche. L’allegato `authorization_and_experiments.json` distingue campagne documentate, ripetizioni visibili nel registro di sessione e stato non applicato dell’atto. Il consenso alla revisione del 12 settembre autorizza la modifica del piano e degli allegati, non l’implementazione nella repository.

**Freeze del contratto in V0.** Depositare i byte di `hexis_v3_design.json`, il loro SHA-256 e l’hash del piano come contratto analitico immutabile della versione. Il record esterno `design_lock.json` contiene i digest senza inserirli ricorsivamente dentro il file di cui si calcola l’hash. La futura configurazione applicativa deve esportare un contratto canonico equivalente; la sua proiezione analitica è confrontata campo per campo al contratto depositato, oltre al controllo dei byte del riferimento. Una modifica di parametri, membri dei blocchi, semi, trasformazioni, pesi o risultati obbligatori richiede una nuova versione e un atto motivato. La semplice riscrittura di un hash non vale come ratifica.

### 13.2 Destinazione dei componenti esistenti

| Percorso o componente | Intervento concreto |
|---|---|
| `src/hexis/conllu_reader.py` | Conservare il parsing verificato; assicurare identità, ordine e coordinate richieste |
| `src/hexis/registry.py` | Applicare registro greco a 18 prefissi / 17 documenti, mappa di 7 blocchi, ruoli e flag; nessuna euristica su titoli |
| `src/hexis/alphabet.py` | Riutilizzare mapping e audit; completare freeze e inventari con regole §4 |
| `src/hexis/sequences.py` | Implementare/reset verificare stream, frammenti e SEP di solo contesto |
| `src/hexis/config.py` | Sostituire controllo di presenza con validazione rigorosa dello schema v3 |
| `src/hexis/model/context_tree.py` | Implementare CTW non binario, modello congelato, log-prior e API §11; sostituire gli stub del selettore |
| `src/hexis/model/diagnostics.py` | Implementare masse risolte/non osservate e supporto; ritirare profondità selezionata |
| `src/hexis/protocols/sampling.py` | Implementare il contratto allegato, ledger, sottosemi e trasformazioni |
| `src/hexis/protocols/scores.py` | Implementare quattro perdite, G, Q, aggregazioni e probe |
| `src/hexis/manifest.py` | Estendere contratti/hash, atomicità e ripresa senza mescolare versioni |
| `src/hexis/pipeline/run_audit.py` | Riutilizzare audit; separare gate di integrità da vecchi stati metodologici |
| `src/hexis/pipeline/run_encode.py` | Implementare coordinate e alfabeti congelati |
| `src/hexis/pipeline/run_tree_validation.py` | Collegare test sintetici ed esatti del CTW |
| `src/hexis/pipeline/run_confirmatory.py` | Ritirare dal percorso attivo; nuovo `run_descriptive.py` esegue coppie e somme individuali; i contrasti spettano a `run_report` |
| `src/hexis/pipeline/run_sensitivity.py` | Orchestrare le otto celle prefissate e i confronti accoppiati |
| Nuovo `src/hexis/pipeline/run_report.py` | R1, validazione output, figure e report descrittivo |
| `run_null_calibration.py`, `run_reference.py`, `run_latin.py` | Ritirare dalla CLI e dall’orchestrazione attiva |
| `model/lexicon.py`, `blocks.py` per chunk | Ritirare dal percorso scientifico v3; non confondere chunk con dependence_block |
| `stats/permutation.py`, `bootstrap.py`, `holm.py` | Conservare le utility funzionanti e i test validi; marcarne l’uso storico, senza import nel percorso scientifico v3 né entry point inferenziali attivi |
| `viz/plots.py` | Implementare soltanto le sei figure richieste e relativa provenienza |
| `tests/`, `conftest.py`, `pyproject.toml` | Inventario v3 senza skip dei gate; aggiornare test superseded con motivazione, mantenere controlli generici validi |
| `docs/`, `README.md`, `AGENTS.md`, `CLAUDE.md` | Riallineamento unico a scope, modelli, comandi e gate effettivi |
| `candidates/` | Resta in quarantena, mai importato, mai raccolto da pytest |
| Risultati e documenti storici | Conservati come v2/pilot, non rinominati risultati v3 |

Ritirare un protocollo significa rimuoverne gli entry point attivi e aggiornare i test che lo dichiaravano obbligatorio, lasciando traccia della sostituzione. Non significa lasciare `pass`, TODO o `NotImplementedError` in un percorso pubblicizzato come utilizzabile. Non si cerca di ottenere “verde” disattivando controlli ancora pertinenti.

Le utility statistiche verificate hanno rispettivamente 94, 74 e 44 righe e non contengono `NotImplementedError`. La migrazione non le tratta come stub da cancellare. L’attestazione storica 327 pass / 17 skip, e gli inventari g0/g1, non certificano l’insieme v3: ricostruire l’inventario con corrispondenza motivata fra test mantenuti, sostituiti e ritirati, senza indebolire le proprietà ancora richieste.

Prima di operare su una copia locale, censire i file non tracciati e preservarli. Il revisore segnala `scripts/reacquire_raw_data.sh`, non disponibile nella copia verificata e non recuperabile attraverso GitHub: contenuto e data non sono attestati da questo piano. Non cancellarlo, sovrascriverlo o assumerlo fonte canonica; verificarlo nella copia locale prima di un eventuale riuso. La sua assenza dallo snapshot Git non impedisce la revisione documentale qui autorizzata.

### 13.3 Chiusura dei vecchi rami metodologici

| Tema precedente | Decisione finale |
|---|---|
| P1, modelli del proprio regime e trasferimento | Ritirati; nessuna stima nascosta nei probe |
| P2 come test confermativo | Sostituito da descrizione G/Q e D_Q, senza inferenza |
| S1, differenza di profondità selezionata | Sostituito dalla diagnostica §9; nessuna singola profondità scelta |
| R1 | Mantenuta obbligatoria, JSD descrittiva delle radici |
| Latino/L1 | Fuori dallo studio; dati storici conservati, non nuova raccolta |
| Sign-flip, scambiabilità, O7, minimi p raggiungibili | Non applicabili alla v3 perché non viene eseguito quel test; non dichiarati “risolti” per il vecchio disegno |
| Permutazioni delle etichette, inclusi ranghi sulle 21 allocazioni | Ritirate; nessuna lettura surrettizia come evidenza di significatività |
| Bootstrap, Holm, α | Ritirati dalla famiglia dei risultati |
| Learning curve e budget di test | Ritirati; q_half unica variazione di taglia, test completo |
| Quarantena del candidato | Conservata |
| Frasi/frammenti, BOS/SEP | Contratto completo §§5–7; nessun `#` nel denominatore degli esiti |
| Alfabeto e alternative automatiche | Tre varianti prefissate; nessun cambio di metodo condizionato al risultato |
| Annotazioni manuali nuove, modelli neurali, parser esterni | Non richiesti per questo studio |

## 14. Sequenza di implementazione e gate

I gate v3 sono nuovi e non ereditano automaticamente il passaggio dei gate v2.1. Ordine lineare: **V0 → V1 → V2 → V3 → V4 → V5**.

| Gate | Lavoro | Criterio di uscita verificabile |
|---|---|---|
| V0 — Migrazione del contratto | Depositare V3-001, eccezione autorizzata, documenti, registro, inventario test e design_lock | Contratto analitico congelato per hash; nessun parametro/entry point ritirato ancora obbligatorio |
| V1 — Corpus e codifica | Audit degli hash, identità, tre rappresentazioni e coordinate | Conteggi del JSON atteso identici; 7 blocchi / 11 primari / 6 probe; tutti i dati mappati |
| V2 — Core e protocollo | CTW, campionatore, rimescolamento, score, JSD e persistenza | T01–T23 e T26 pertinenti superati; test esatti e sintetici completi |
| V3 — Freeze dell’esecuzione | Prova integrata a un seme per tutte le 9 celle, controllo risorse, lock e manifest | 126 fit tecnici completati, 84 valutazioni probe C0; nessuna modifica metodologica successiva senza versione nuova |
| V4 — Esecuzione finale | 1.400 fit, probe, R1, tabelle e diagnostiche | Cardinalità, hash, slot e aggregazioni completi; T24–T27 superati |
| V5 — Consegna riproducibile | Figure, report, verifica di una ripresa e riproduzione di casi selezionati | T28–T30; documento con limiti e risultati negativi; nessun artefatto mancante |

La prova V3 non è una fase per scegliere iperparametri sui contrasti. Serve a verificare l’integrazione di tutte le celle. Si controllano punteggi finiti, identità e risorse; i comandi ufficiali non emettono contrasti fra gruppi prima del completamento di V4 e del controllo §14.2. Il contratto analitico è già congelato in V0; V3 congela implementazione e ambiente. I pilot precedenti restano dichiarati.

Se V3 viene eseguito con lo stesso codice, dati, configurazione e contratto definitivo e gli output rispettano lo schema finale, le sue 126 partizioni-fit possono essere riutilizzate tramite `--resume`: i fit unici scientifici restano 1.400. Se si corregge un bug che cambia un risultato o una coordinata, cambiano commit/run_id e quei risultati non vengono riutilizzati. Non si sommano pilot di versioni differenti per raggiungere il budget.

### 14.1 Comandi di destinazione

La CLI finale deve supportare almeno il seguente percorso, da documentare solo quando implementato:

```bash
uv sync --frozen
uv run pytest -q
uv run python -m hexis.pipeline.run_audit --config config/default.yaml
uv run python -m hexis.pipeline.run_encode --config config/default.yaml
uv run python -m hexis.pipeline.run_tree_validation --config config/default.yaml
uv run python -m hexis.pipeline.run_descriptive --config config/default.yaml --cell C0
uv run python -m hexis.pipeline.run_sensitivity --config config/default.yaml
uv run python -m hexis.pipeline.run_report --config config/default.yaml
```

`run_descriptive` esegue entrambi i bracci e i probe, producendo score per documento/blocco senza aggregazioni fra gruppi. `run_sensitivity` esegue tutte le otto celle nell’ordine del JSON, ciascuna con entrambi i bracci. Il report si rifiuta di presentare una conclusione finale se il contratto richiede artefatti mancanti. `--resume` è un’opzione esplicita degli stage che producono risultati, con le regole §11.6.

La sequenza attuale di gate nella repository non viene aggirata per eseguire questi comandi. Prima si applica V0, poi si implementano e si verificano le nuove interfacce. Questo documento non rappresenta un’istruzione a chiamare oggi entry point non ancora presenti.

### 14.2 Controlli obbligatori prima dei contrasti

`run_report` è l’unico entry point che emette D_Q, le due componenti D_G, le riaggregazioni per target e i grafici di contrasto. Prima di emetterli deve:

1. Verificare il digest del contratto depositato e la corrispondenza della configurazione applicativa, senza modificare il lock automaticamente.
2. Verificare i certificati V0–V3, legati a contratto, commit dell’implementazione e lock delle dipendenze. V3 viene attestato esternamente al contenuto che identifica il run, così da non creare una dipendenza circolare tra certificato e run_id. Una correzione del codice invalida il certificato relativo a quel codice.
3. Generare dal contratto l’insieme atteso delle chiavi `(cell, held_block_key, seed, arm)` e confrontarlo per uguaglianza con le 1.400 chiavi uniche complete. Rifiutare chiavi mancanti, aggiuntive, duplicate o non complete; non basta controllare il numero totale.
4. Verificare analogamente le 1.680 valutazioni probe C0 e gli output R1 di tutte e tre le varianti; verificare hash, schemi, cardinalità degli slot e denominatori prescritti.
5. Richiedere per ciascun artefatto l’esito della verifica dei byte contro il suo hash nel manifest; una presenza nominale non equivale a integrità. L’assenza o corruzione di una sola cella impedisce entrambe le aggregazioni finali.

Gli output individuali necessari per diagnosticare un fallimento rimangono disponibili, ma il comando non scrive una tabella di contrasto parziale come risultato finale. Gli elenchi di semi, le fasce di storia e il numero di permutazioni sono quelli del contratto, senza override informali. Il riferimento `report_contract.py` e i test associati dimostrano il rifiuto dei casi incompleti o incoerenti; il lettore dei file e la verifica effettiva dei loro hash devono essere integrati nel manifest canonico e sottoposti a T26/T30.

Questi controlli rendono verificabile il percorso ufficiale; non possono impedire a una persona di calcolare autonomamente un contrasto dai dati disponibili. Il progetto mantiene un protocollo prospettico dopo pilot, senza fingere una preregistrazione antecedente alle osservazioni.

## 15. Risorse, ambiente e fattibilità concreta

### 15.1 Misure osservate

Nel benchmark separato con Python 3.12.14, NumPy 2.3.5 e PyYAML 6.0.3: fit C0 da 53.304 token circa 0,63–0,70 s; valutazione held-out 0,024–0,224 s; valutazione dell’intero probe 0,046–0,055 s. Picco RSS C0 circa 174 MiB; massimo nei pilot reali circa 240 MiB a D12. Non occorre una GPU.

L’ambiente del primo audit della suite canonica usava il lock del repository e NumPy 2.5.1; l’ambiente del prototipo e dei contratti supplementari iniziali usava NumPy 2.3.5. Sono due ambienti distinti e non devono essere confusi in un’unica attestazione di riproducibilità.

**Si conserva il lock della repository**, incluso NumPy 2.5.1, con Python 3.12 e le dipendenze già previste; non si impone un downgrade a 2.3.5 né un nuovo pin di PyYAML per uniformarsi al prototipo. Nella verifica del 12 settembre, sette fold per versione e 42 contributi campionati per versione hanno dato hash identici fra NumPy 2.3.5 e 2.5.1 per ledger, permutazioni, modelli e punteggi. Gli script e i digest sono allegati. Il confronto è avvenuto sullo stesso host e runtime Python: non certifica tutte le piattaforme o l’intero stack applicativo.

PCG64 ha garanzie di compatibilità del proprio flusso, ma non ogni trasformazione di `Generator` ha una garanzia universale tra versioni; perciò si conservano vettori e test empirici. [Compatibilità NumPy](https://numpy.org/doc/stable/reference/random/compatibility.html). `uv sync --frozen` deve utilizzare il lock identificato nel contratto; i gate eseguono sotto tale ambiente l’intera suite e le prove integrate. Se un test fallisce, si interrompe e si diagnostica prima di cambiare dipendenze: nessuna risoluzione automatica o sostituzione di versione. Un cambiamento necessario del lock è motivato e versionato e invalida i certificati precedenti. Non si aggiunge una libreria CTW.

### 15.2 Budget di esecuzione e disco

Per 1.400 fit, una stima prudente sullo stesso ordine di hardware è **20–60 minuti** per calcolo e operazioni di supporto. È una proiezione dal prototipo, non un tempo misurato della pipeline completa. Scritture Parquet, rendering e condizioni della macchina possono incidere. Esecuzione sequenziale come default; parallelismo non necessario.

Le posizioni primarie `oth` sono 109.716, contro 109.108 C0. Con le otto sensibilità, C0 e i probe, gli output contengono **12.704.540 righe accoppiate**. Otto float64 e 12 byte di identificativi per riga richiedono circa 921 MiB, prima di metadata, validità dei null e indici. La compressione può ridurre lo spazio ma non è una garanzia. Riservare **10 GB di spazio libero** per input, partizioni, temporanei e risultati; una macchina con **8 GB di RAM** è una dotazione prudente per l’esecuzione sequenziale. Non si dichiara un requisito minimo misurato di 8 GB: il modello isolato usa molto meno.

Le perdite devono essere scritte per partizione, senza concatenare tutti i risultati in un unico DataFrame in memoria. Non si memorizzano tutti gli alberi. Il picco deve essere misurato nell’integrazione; una crescita non prevista richiede correggere l’uso della memoria, non ridurre celle, blocchi o semi a posteriori.

La stima precedente di circa 100 MiB riguardava sei vettori float64 per le sole 2.182.160 posizioni C0 originali. La stima di circa 921 MiB riguarda invece 12.704.540 righe accoppiate, tutte le celle e i probe, con otto float64 e quattro identificativi (12 byte complessivi). Sono schemi e popolazioni differenti; nessuna delle due cifre è la misura della memoria totale del processo.

### 15.3 Lavoro umano e tecnico residuo

Stima di pianificazione, non misura empirica: circa **8–13 giornate di lavoro concentrato** per un implementatore competente che utilizzi le prove disponibili: 1–2 giorni per migrazione/dati; 2–3 per core e protocollo; 2–3 per output/test; 1–2 per integrazione e riproducibilità; 2–3 per report e revisione scientifica. Il calendario dipende dalla familiarità con il codice. Il costo dominante è l’integrazione controllata, non il training.

Il perimetro non richiede nuove annotazioni, ampliamento del corpus, accesso a GPU o addestramento neurale. Queste sono le ragioni concrete per cui il ridimensionamento è fattibile. L’accettazione resta basata sui gate, non sull’obbligo di rispettare una previsione temporale.

## 16. Regole per la conclusione scientifica

Il completamento tecnico è indipendente dal segno e dalla grandezza di D_Q. Il progetto si conclude con successo se il protocollo viene eseguito correttamente e il report descrive fedelmente i risultati, anche quando la differenza tra gruppi è piccola, incoerente tra blocchi o sensibile alla codifica.

| Situazione osservata | Conclusione consentita |
|---|---|
| G originale positivo, G rimescolato simile | Il guadagno del CTW non distingue chiaramente l’ordine osservato dal controllo scelto |
| Q positivo nei blocchi, differenza fra gruppi piccola | L’ordine offre un vantaggio sotto il predittore, senza una separazione descrittiva marcata fra i gruppi disponibili |
| D_Q consistente nel segno attraverso le sensibilità | Descrizione stabile rispetto alle perturbazioni eseguite, senza inferenza causale o di popolazione |
| D_Q cambia segno o ampiezza nelle sensibilità | La conclusione comparativa dipende dalle scelte analitiche; mostrare tutte le celle |
| D6, D8 e D12 quasi uguali | Profondità maggiore non migliora la prestazione nel campione/protocollo; non assenza di dipendenze linguistiche profonde |
| `upos_only` e C0 differiscono | Risultati dipendenti dal livello di rappresentazione; non identificazione automatica del contributo causale di DEPREL |
| Probe tragici eterogenei | Il confronto originale non definisce una proprietà uniforme di “verso”; nessuna categoria aggiuntiva viene addestrata |
| JSD elevata con Q simile | Differenze marginali dei simboli, senza corrispondente differenza nel vantaggio d’ordine misurato |

Il report deve esporre, vicino al risultato principale: composizione del corpus; 2 blocchi HEX contro 5 di prosa; confondimento cronologico; training leave-one-block-out bilanciato per blocco ma non per regime; annotazioni offline; rimescolamento condizionato alla composizione per frase; variabilità dei semi come variabilità computazionale; osservazione precedente dei pilot.

Non usare “assenza di effetto” senza specificare l’effetto misurato e il limite di risoluzione; non trasformare una SD dei semi in incertezza sui testi antichi. Non usare il termine “confermativo” per il disegno v3. Non si considera invalido un dato perché rende meno netta la narrazione.

## 17. Materiali da consegnare al termine dell’implementazione

1. Repository v3 con commit del freeze, test completi e dipendenze bloccate.
2. Registro del corpus con identità, blocchi, flag e fonti; tre alfabeti e audit delle eliminazioni.
3. Configurazione delle nove celle, ledger, manifest e output per posizione/aggregati verificati.
4. Sei figure, tabelle integrali e report scientifico con il risultato centrale D_Q e le sue componenti.
5. Istruzioni di riproduzione in una cartella nuova, verifica hash e ripresa di una partizione interrotta.
6. Archivio dei pilot e del percorso di decisione, per distinguere sviluppo metodologico e analisi finale.

I dati grezzi restano immutabili e non vengono aggiunti al repository. Si conserva la provenienza e l’indicazione di licenza del treebank. Gli script di acquisizione usano il commit e gli hash fissati. L’eventuale pubblicazione esterna è un atto successivo alla verifica dei risultati; questo piano non pubblica né modifica il progetto.

## 18. Fonti e uso effettivo

- **Repository HEXIS**, revisione `852644b…`: stato del codice, specifiche e registro proposto esaminati. [Snapshot](https://github.com/leonardotornabene/HEXIS/tree/852644b6917790877c7b2ca5df2e76b17829d87c).
- **UD Ancient Greek Perseus r2.18**, revisione `37837c7…`: corpus effettivamente contato e utilizzato nei pilot. [Snapshot](https://github.com/UniversalDependencies/UD_Ancient_Greek-Perseus/tree/37837c7a3c592c9563f8c51cc63344b87247f8a5).
- **AGDT2.1**, revisione `bf4334f…`: inventario e metadati bibliografici delle sorgenti; non sostituisce i dati UD nei fit. [Descrizione](https://github.com/PerseusDL/treebank_data/blob/bf4334f0af5e13d16b04c1cccd6237e683ac6f5f/v2.1/Greek/README.MD). Collegamenti ai quattro XML verificati nell’allegato JSON.
- **Kontoyiannis, Mertzanis, Panotopoulou, Papageorgiou e Skoularidou**, *Bayesian Context Trees: Modelling and exact inference for discrete time series*, versione 3, 2022: fondamento CTW/BCT e prior sui modelli. [Testo](https://arxiv.org/abs/2007.14900v3). La gestione di confini e score congelato di HEXIS è specificata e validata qui, non attribuita integralmente alla fonte.
- **Galves, Galves, García, Garcia e Leonardi**, *Context tree selection and linguistic rhythm retrieval from written texts*, Annals of Applied Statistics 6(1), 2012, 186–209, DOI 10.1214/11-AOAS511: precedente diretto su contesti variabili e ritmo; selezione di modelli su codifiche ritmiche del portoghese. [Testo verificato](https://arxiv.org/pdf/0902.3619).
- **Vanessa B. Gorman e Robert J. Gorman**, *Approaching Questions of Text Reuse in Ancient Greek Using Computational Syntactic Stylometry*, Open Linguistics 2, 2016, 500–510, DOI 10.1515/opli-2016-0026: stilometria sintattica del greco con caratteristiche di percorsi negli alberi, distinta dalle sequenze di etichette di HEXIS. [Deposito degli autori](https://digitalcommons.unl.edu/historyfacpub/208/).

- **Schürmann e Grassberger**, *Entropy estimation of symbol sequences*, Chaos 6, 1996, 414–427; arXiv 2002: stima da sequenze finite e motivazione dei controlli di convergenza/supporto. [Testo](https://arxiv.org/abs/cond-mat/0203436).
- **Lin**, *Divergence Measures Based on the Shannon Entropy*, IEEE Transactions on Information Theory 37(1), 1991, 145–151: JSD; PDF fornito `jensen-shannon.pdf`.
- **de Marneffe, Manning, Nivre e Zeman**, *Universal Dependencies*, Computational Linguistics 47(2), 2021, 255–308, DOI 10.1162/coli_a_00402: natura del livello di annotazione; PDF fornito `coli_a_00402.pdf`.
- **Herrera, Silai, Guillaume e Kahane**, *Extraction of Contrastive Rules from Syntactic Treebanks: A Case Study in Romance Languages*, QUASY 2025, 26–38: limiti della comparabilità dei treebank; PDF fornito `2025.quasy-1.5v1.pdf`. Non viene importato il loro protocollo di test nel disegno HEXIS.
- **Gianitsos, Bolt, Chaudhuri e Dexter**, *Stylometric Classification of Ancient Greek Literary Texts by Genre*, 2019: precedente che impedisce rivendicazioni generiche di novità sulla distinzione quantitativa prosa/verso. [Articolo](https://aclanthology.org/W19-2507/).

I documenti di ricerca e gli altri PDF forniti costituiscono il contesto teorico e storico del progetto. Non vengono usati come prova empirica della fattibilità software o come certificazione delle nuove formule. Nessuna conclusione operativa dipende dall’autorità di un autore o da un’affermazione non verificata contenuta nelle proposte.

## 19. Attestazione finale del piano

Il piano risolve le decisioni di corpus, rappresentazione, unità, campionamento, predittore, controllo d’ordine, misure, pesi, sensibilità, probe, JSD, output, migrazione e accettazione. Il riferimento eseguibile dimostra che il nucleo può operare sulle dimensioni reali del progetto e che i nuovi contratti hanno esempi verificati.

**Il giudizio di fattibilità è favorevole per questo perimetro.** Il documento è pronto per guidare l’implementazione. Non equivale a una certificazione di codice non ancora integrato, a una promessa di risultati positivi o all’assenza assoluta di limiti scientifici. I limiti che incidono sull’interpretazione sono incorporati nella domanda e nel protocollo, anziché lasciati come obiezioni da affrontare dopo il calcolo.

Gli allegati normativi sono `hexis_v3_design.json`, `corpus_atteso.json` e i contratti descritti nel README del pacchetto. Il testo governa la semantica; il JSON governa l’elenco e i valori delle celle e del registro. Qualunque divergenza fra i due è un errore del pacchetto da correggere prima dell’implementazione, non una facoltà di scegliere il valore preferito.
