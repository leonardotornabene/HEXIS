# HEXIS — Verifica comparata delle due proposte e punto di arresto

**Data:** 11 settembre 2026  
**Documenti valutati:** `piano_finale_HEXIS.md` e `piano_ultimato_HEXIS.md`  
**Repository:** `leonardotornabene/HEXIS`, ramo `g1/pre-audit`  
**Commit verificato:** `852644b6917790877c7b2ca5df2e76b17829d87c`  
**Stato del rapporto:** valutazione documentale ed empirica con un impedimento metodologico verificato. Non è una proposta ratificata, una nuova specifica operativa o una certificazione dell’intero progetto.

## 1. Verdetto raggiunto e limite della consegna

**`piano_ultimato_HEXIS.md` è la base preferibile per il ridimensionamento. Nessuna delle due proposte è pronta per essere ratificata integralmente nella forma attuale.**

La superiorità del secondo piano riguarda scelte sostanziali: statuto descrittivo coerente con il corpus disponibile, uso di tutte le posizioni held-out, rinuncia a una giustificazione inferenziale non stabilita, migliore delimitazione delle affermazioni e riconoscimento della distanza fra algoritmo proposto e fonte bibliografica.

Esiste però un problema condiviso, anteriore alla discussione sull’inferenza: la selezione `monotone-stop` può impedire al modello di utilizzare dipendenze d’ordine 2 che i test di accettazione gli impongono di recuperare. Il problema è stato riprodotto su dati sintetici alla taglia di training prevista dal nuovo disegno, e ricontrollato con una seconda ricostruzione numerica indipendente.

**Mi arresto prima di presentare una “versione definitiva” perché rimane da chiarire il vincolo scientifico sullo strumento:** il context tree a ordine variabile è un elemento da conservare necessariamente, oppure è un mezzo sostituibile per ottenere una misura descrittiva affidabile in tempi brevi? La risposta cambia quali soluzioni devono essere confrontate e validate. Non è una questione di formattazione, ratifica amministrativa o scelta di un nome.

La raccomandazione è conservare l’impostazione descrittiva del secondo piano e il requisito scientificamente utile di riconoscere il processo noto d’ordine 2; rimettere in discussione il selettore o, se ammesso dall’obiettivo del lavoro, lo strumento. Non raccomando di rendere verde il gate scegliendo un seme favorevole o sopprimendo il benchmark che ha rivelato il problema.

## 2. Che cosa è stato effettivamente verificato

### 2.1 Accesso, versioni e integrità

L’accesso al repository attraverso GitHub è riuscito. Il ramo predefinito è `master`, a `3f5a6eafac83e5c190a866c8bea1937d8284ce75`; `g1/pre-audit` è avanti di 47 commit e non è indietro rispetto a `master`. Entrambi i piani fanno riferimento a `g1/pre-audit` e al commit effettivamente presente. È quindi questa la baseline pertinente, non il solo README del ramo predefinito.

Il lavoro è stato svolto su una copia separata. Non sono state apportate modifiche alla repository remota, ai file versionati della copia o agli allegati. I controlli conclusivi `git status --porcelain=v1`, `git diff --exit-code` e `git diff --cached --exit-code` hanno restituito uno stato pulito. Gli script aggiuntivi di verifica e i loro risultati si trovano fuori dalla copia della repository.

Sono stati letti integralmente entrambi i piani. Sono stati inoltre esaminati i documenti normativi pertinenti, le decisioni D18/D32/D36/D39/D43/D44/D47/D49/D52/D53, i registri e le proposte G1, il codice e i test relativi a lettura, codifica, sequenze, scoring, selezione e permutazioni. Sono stati consultati i materiali scientifici allegati rilevanti; la pagina della fonte Schürmann–Grassberger contenente la regola di selezione è stata controllata anche visivamente.

Riferimento di versione: [commit HEXIS esaminato](https://github.com/leonardotornabene/HEXIS/commit/852644b6917790877c7b2ca5df2e76b17829d87c).

### 2.2 Suite esistente

L’ambiente è stato ricostruito da `uv.lock`, senza modificare il lockfile. La suite è stata eseguita con cache di pytest disabilitata e bytecode indirizzato fuori dalla repository:

```text
327 passed, 17 skipped in 14.04s
```

Python utilizzato: 3.12.14. Dipendenze rilevanti del lock: NumPy 2.5.1, pytest 9.1.1, conllu 6.0.0, pandas 3.0.3, pyarrow 25.0.0.

Questo conferma il conteggio dichiarato dai piani, ma non certifica la validità dello strumento. `ContextTree.__init__`, `fit`, `evaluate` e le altre operazioni centrali sollevano ancora `NotImplementedError`. I test dei quattro processi analitici sono esplicitamente saltati come scaffold. Anche sampler, scoring applicativo, codifica finale e validazione del tree sono incompleti.

**Non è stato eseguito alcun fit di un context model sui testi reali.** Le verifiche sui dati reali sono conteggi e controlli della rappresentazione; gli esperimenti sul modello usano soltanto sequenze sintetiche. Non sono stati importati i modelli in quarantena da `candidates/`.

Fonti: [strumento canonico](https://github.com/leonardotornabene/HEXIS/blob/852644b6917790877c7b2ca5df2e76b17829d87c/src/hexis/model/context_tree.py), [test analitici](https://github.com/leonardotornabene/HEXIS/blob/852644b6917790877c7b2ca5df2e76b17829d87c/tests/test_context_tree.py).

### 2.3 Stato delle decisioni

Il registro G1 conferma le ratifiche tecniche 17–20 e 23–26; le decisioni scientifiche restano aperte. I due documenti allegati sono proposte. La presenza di un valore nei loro testi, o la sua marcatura come verificato, non lo rende una scelta ratificata né una misura indipendentemente controllata.

La richiesta attuale autorizza la valutazione e la formulazione di una nuova proposta; non è stata trattata come autorizzazione ad applicare modifiche al progetto.

Fonte: [registro delle ratifiche G1](https://github.com/leonardotornabene/HEXIS/blob/852644b6917790877c7b2ca5df2e76b17829d87c/docs/g1_ratification_record.md).

## 3. Corpus: ricalcolo indipendente

I tre file greci sono stati acquisiti al commit upstream `37837c7a3c592c9563f8c51cc63344b87247f8a5`. I rispettivi SHA-256 coincidono esattamente con quelli registrati da HEXIS in `data/raw/PROVENANCE.md`. Il conteggio è stato ricalcolato leggendo le righe CoNLL-U e applicando la mappatura dichiarata nel config, senza addestrare alcun modello.

I risultati sotto riportati sono verificati **condizionatamente al registro proposto**: il ricalcolo non sostituisce una ratifica filologica delle identità, delle attribuzioni o dei raggruppamenti.

| Blocco proposto | Token C0 | Posizioni con almeno 4 simboli precedenti |
|---|---:|---:|
| HOMERIC_TRADITION | 71.088 | 46.634 |
| HESIODIC_TRADITION | 9.282 | 6.375 |
| HERODOTUS | 17.301 | 12.946 |
| THUCYDIDES | 9.346 | 7.227 |
| ATHENAEUS | 23.133 | 16.691 |
| DIODORUS | 15.266 | 12.334 |
| PLUTARCH | 8.884 | 6.901 |
| **Totale primario** | **154.300** | **109.108** |

Altri riscontri:

- 202.989 righe sintattiche nel corpus greco; 13.919 frasi.
- Alfabeti osservati sui 17 documenti greci: `ud23 = 106`, `ud23_oth = 112`, `upos_only = 12`.
- Tragedia: 22.275 token C0 e 12.769 posizioni eleggibili, in sei documenti.
- Quota minima comune alle tre rappresentazioni: `q = 8.884`.
- L’Inno a Demetra contiene 1.119 posizioni eleggibili; l’Iliade 45.515.
- L’Iliade pesa il 97,6005% delle posizioni eleggibili del blocco omerico, oppure il 97,5228% dei suoi token. Sono pesi diversi, benché numericamente vicini.

La formula corretta è `sum(max(L-4, 0))`. Il calcolo `token - 4*frasi` è soltanto un limite inferiore. Il valore 6.375 del secondo piano è confermato; il primo piano non conosceva ancora questo valore e in alcune argomentazioni tratta limiti inferiori come se fossero taglie effettive.

Il dato di 232.212 righe complessive riportato dal secondo piano comprende anche il latino: non è il numero di righe greche. In questa verifica non è stato ricalcolato il corpus latino, destinato all’esclusione in entrambi i piani.

Fonte degli hash: [provenienza degli input](https://github.com/leonardotornabene/HEXIS/blob/852644b6917790877c7b2ca5df2e76b17829d87c/data/raw/PROVENANCE.md).

## 4. Valutazione separata di `piano_finale_HEXIS.md`

### 4.1 Aspetti utili

Il piano riconosce correttamente la dipendenza fra testi della stessa tradizione, espone l’asimmetria della composizione del training, segnala il rischio di adiacenze artificiali in P-BOUND e dichiara che il software centrale deve ancora essere scritto. Il passaggio a contributi di training per blocco limita il dominio quantitativo dell’Iliade sul training pooled.

Questi elementi sono utili, ma non sostengono la certificazione inferenziale che il testo tende ad attribuirsi.

### 4.2 La scambiabilità non è stata stabilita

Un test di permutazione può essere esatto sotto ipotesi precise sulla distribuzione congiunta dei dati o sull’assegnazione delle etichette. La label-blindness del software impedisce una forma di circolarità; non dimostra quelle ipotesi.

L’assenza di campionamento probabilistico, da sola, non vieta ogni forma di inferenza basata su modelli. Qui, tuttavia, non viene fornito un modello stocastico sostantivo che giustifichi la scambiabilità dei sette blocchi storici. Il perfetto allineamento fra i due blocchi esametrici e il periodo arcaico, le dipendenze testuali e i molteplici confondenti rendono ingiustificata una certificazione di esattezza applicata a questo corpus.

È legittimo descrivere un risultato come esatto **se** una determinata ipotesi vale. Non è legittimo far diventare tale condizione una proprietà verificata del disegno. Il primo piano alterna correttamente la formula condizionale a espressioni troppo forti come “valido per costruzione”.

La letteratura sui test di permutazione distingue inoltre l’uguaglianza delle distribuzioni dall’uguaglianza di un solo parametro. Non offre una scorciatoia per sette blocchi non scambiabili. [Chung e Romano, 2013](https://arxiv.org/abs/1304.5939).

### 4.3 Uguali quote non implicano uguali varianze

La frase secondo cui `q` e `m` uguali renderebbero uguali le varianze marginali “per costruzione” è falsa. La varianza dipende anche dalle distribuzioni, dalle dipendenze seriali, dalle lunghezze delle frasi, dall’eterogeneità interna e dal modello addestrato.

Anche nel caso elementare di campionamento uniforme senza reinserimento da una popolazione finita di score fissati, la varianza della media dipende da `S_b²(1/m - 1/N_b)`, non soltanto da `m`. Uguali `m` con diversi `N_b` o `S_b²` non producono uguale varianza.

I test deterministici di invarianza sono verifiche software importanti, ma non sono “più forti” di ogni calibrazione nel senso di poter certificare ipotesi sulla generazione dei dati. Verificano proprietà diverse.

### 4.4 L’“impossibilità formale” del latino è smentita dal codice

Il piano sostiene che, con gruppi 2/7 e 36 allocazioni, il minimo bilaterale sia `2/36 = 0,0556`. Per la regola bilaterale effettivamente implementata non è vero: con gruppi di dimensione diversa non è garantita un’allocazione speculare con statistica opposta.

Controesempio eseguito usando direttamente `exact_label_permutation` della repository:

```text
score:   [100, 99, 0, 0, 0, 0, 0, 0, 0]
etichette: 2 nel primo gruppo, 7 nel secondo
allocazioni: 36
p bilaterale: 0,027777777777777776 = 1/36
```

È una falsificazione sufficiente dell’asserita impossibilità generale. La regola D43 già distingue questi casi. L’esclusione del latino può restare giustificata dalla scarsità e inadeguatezza del materiale rispetto allo studio ridotto; non da questo argomento matematico.

Fonte del calcolo: [permutation.py](https://github.com/leonardotornabene/HEXIS/blob/852644b6917790877c7b2ca5df2e76b17829d87c/src/hexis/stats/permutation.py).

### 4.5 L’argomento quantitativo sull’Inno non è una verifica del disegno reale

Il primo piano presenta un moltiplicatore universale della varianza basato sul rapporto fra due taglie di valutazione. Non considera la correzione per popolazione finita e impiega anche valori che erano soltanto limiti inferiori.

Usando le taglie effettive, il passaggio da 6.375 a 1.119 posizioni, nel solo blocco omerico di 46.634 posizioni, moltiplicherebbe la componente di varianza da campionamento uniforme di score fissati per circa 6,44. Per il blocco esiodeo, valutato integralmente a 6.375 posizioni, quella componente parte invece da zero. Non esiste dunque il medesimo moltiplicatore per tutti i blocchi. L’aggiunta della variabilità dei fit rende la situazione ulteriore, non risolta dal rapporto fra taglie.

Le tabelle di potenza riportate dal piano restano simulazioni condizionali a un generatore e a parametri. Non sono misure della potenza del protocollo reale su questi testi. Non sono state riprodotte in questa verifica, e non le uso come fondamento del verdetto.

### 4.6 Il rapporto con la composizione del training è sovraenunciato

Con quote esatte, la frazione di training del proprio gruppo è 1/6 nei fold HEX e 4/6 nei fold prosa. Questo risultato aritmetico è corretto. Non ne segue un teorema sulla direzione del gain: la direzione indicata da D44 era condizionata alla relazione fra gain e rappresentazione del proprio regime nel training.

Il primo piano elimina tale condizione quando parla di “direzione nota”. Una cross-entropy differenziale rispetto alla root può reagire alla miscela in modi diversi. Un test bilaterale, inoltre, non corregge la composizione del training né i confondenti.

### 4.7 Fattibilità e giudizio

Con il sampler a frasi intere e arresto prima del superamento, il training effettivo è **al massimo** `6q`; non è esattamente 53.304 token in ogni fold. Il rapporto con la vecchia finestra 40–60k non dimostra sufficienza statistica: quella finestra era un’ipotesi di profilazione, non una soglia empiricamente validata di apprendimento.

**Giudizio sul primo piano:** contiene materiale operativo recuperabile, ma non costituisce una base affidabile da ratificare integralmente. Alcune “correzioni definitive” sono esse stesse errori. Non raccomando di conservare l’inferenza come percorso principale in attesa che una revisione esterna renda credibile l’ipotesi sostantiva mancante.

## 5. Valutazione separata di `piano_ultimato_HEXIS.md`

### 5.1 Miglioramenti sostanziali

Il secondo piano compie una scelta scientificamente difendibile per il materiale disponibile: descrive differenze finite e condizionate al protocollo, senza trasformarle in generalizzazioni sull’esametro greco.

L’eliminazione di `m` è un miglioramento pratico concreto: tutte le 109.108 posizioni eleggibili del primario possono contribuire alle rispettive medie, senza un ulteriore sottocampionamento casuale. I blocchi possono mantenere peso uniforme nel contrasto anche se contengono numeri diversi di posizioni. L’uguaglianza dei pesi fra blocchi non richiede l’uguaglianza del numero dei loro target.

Sono corretti anche: gain signed; separazione fra variabilità computazionale e repliche scientifiche; visibilità dei sette score; dichiarazione dell’alfabeto costruito anche sul probe tragico; distinzione fra modello Rissanen-inspired e replica dell’algoritmo originale; mantenimento della valutazione held-out senza aggiornamenti.

Il rango delle 21 allocazioni è matematicamente calcolabile e descrittivamente lecito se resta tale. Non aggiunge repliche, identificazione causale o validità inferenziale. Non è indispensabile al valore scientifico del lavoro e non deve guidarne la narrativa.

### 5.2 Il difetto decisivo resta nel selettore primario

La denominazione più accurata dello strumento non ne modifica il comportamento. Il piano conserva `select: monotone` come primaria e conserva il requisito di recuperare la sorgente d’ordine 2. Il conflitto dimostrato nella sezione 7 rimane quindi pienamente attivo.

La descrizione del progetto come “metodologico” rende particolarmente importante questo punto: uno strumento può essere un funzionale ben definito e tuttavia non possedere la capacità che viene usata per giustificarne l’impiego. La riproducibilità non basta a colmare tale distanza.

### 5.3 Contratti operativi da precisare prima dell’implementazione

Oltre al selettore, il testo conserva dettagli con effetti reali:

1. **Accoppiamento dei seed.** L’`analysis_id` contiene la cella, ma `q_half` deve riutilizzare la stessa permutazione di C0. Occorre definire un namespace di campionamento condiviso per le celle accoppiate, distinto dall’identità completa del run. Le due prescrizioni attuali non determinano un’unica implementazione.
2. **Ammissibilità in `argmax`.** Va chiarito se un nodo sia ammissibile per il proprio supporto o soltanto se tutti gli antenati superano la regola monotona. Nella seconda interpretazione il difetto non viene risolto. La somma dei Delta, calcolati su insiemi diversi di occorrenze, non va presentata senza dimostrazione come confronto diretto di due codici completi sugli stessi target.
3. **Significato di `#`.** “Può essere appreso” e “non è mai target” devono distinguere esplicitamente eventi di aggiornamento durante il fit da posizioni incluse nello scoring. Un simbolo contato come esito nel training e poi escluso dalla media lessicale produce un modello diverso da un simbolo utilizzato soltanto come contesto.
4. **Adiacenza sorgente.** L’adiacenza di ranghi consecutivi dopo ordinamento non dimostra da sola l’adiacenza nel testo integrale. P-BOUND richiede una regola che non unisca lacune documentate del materiale di partenza. Identità del testo, ordine degli estratti e continuità sono verifiche distinte.
5. **MCSE del contrasto.** Va calcolato sui contrasti per seed, `D_s`, preservando le dipendenze fra i sette score, se si vuole un MCSE di `D_BB`. Non basta combinare gli errori dei singoli blocchi come se fossero indipendenti. La descrizione della precisione computazionale deve restare separata da intervalli di popolazione.
6. **Sensibilità a 10 seed contro primaria a 20.** Va resa visibile anche la differenza accoppiata sui medesimi primi 10 seed. Altrimenti un cambio di segno può incorporare differenze di campionamento e non soltanto il parametro modificato.
7. **Unseen rates e schemi.** Numeratori, denominatori e maschere di queste diagnostiche devono essere fissati. La coordinata completa del risultato deve ricostruire sempre anche il documento, non soltanto la coppia frase/token.
8. **Profilazione pertinente.** Il costo va misurato anche con alfabeto e sparsità compatibili con 106 simboli e frasi, non dedotto dai soli processi binari. Il numero di fit non è una stima della durata dello sviluppo o della riproduzione completa.

Sono precisazioni risolvibili nella specifica successiva. Non autorizzano a dichiarare l’attuale testo già privo di decisioni implementative aperte.

### 5.4 Quota esatta e segmenti finali

La quota esatta del secondo piano rende esatte le contribuzioni lessicali dei blocchi. Il segmento finale introduce un reset artificiale, dichiarato. Questo è un compromesso metodologico da definire e quantificare; non rende automaticamente invalido il protocollo, come potrebbe suggerire la critica del primo piano.

Né il mantenimento dei segmenti né l’arresto con undershoot risolvono il problema del selettore. Non bisogna concentrare la revisione su questi dettagli lasciando intatto l’impedimento principale.

### 5.5 Giudizio

**Giudizio sul secondo piano:** migliore base di lavoro, coerente nell’impostazione epistemica generale, con conteggi principali confermati. Non ratificabile integralmente finché il conflitto modello/benchmark resta irrisolto e i contratti sopra indicati non sono resi univoci.

## 6. Confronto diretto

| Criterio | Piano finale | Piano ultimato | Valutazione |
|---|---|---|---|
| Statuto delle conclusioni | Test condizionale con scambiabilità non stabilita | Descrizione finita del corpus | Preferibile il secondo |
| Uso dei target held-out | Sottocampione di dimensione minima comune | Tutti i target eleggibili | Preferibile il secondo |
| Scelta dei blocchi | Giustificazioni anche legate a una potenza non misurata | Raggruppamenti prudenziali dichiarati | Preferibile il secondo; resta verifica filologica |
| Minimo bilaterale latino | Argomento `2/36` errato | Inferenza latina eliminata | Il secondo evita il falso fondamento |
| Quantificazione del modello | Tende a sostenere una capacità di lettura della memoria | Limita le interpretazioni e il richiamo a Rissanen | Preferibile il secondo |
| Riconoscimento del processo d’ordine 2 | Richiesto, ma può essere bloccato da monotone | Stesso conflitto | Difetto condiviso decisivo |
| P-BOUND e riproducibilità | Alcuni dettagli corretti, altri incompleti | Contratti più sviluppati, ancora ambigui in punti specifici | Vantaggio del secondo, senza certificazione finale |
| Prontezza per ratifica integrale | No | No | Nessuno dei due è già pronto |

Il confronto non richiede un compromesso fra le due proposte. La direzione descrittiva del secondo piano è preferibile; non occorre reintrodurre il capitolo inferenziale del primo per bilanciare il giudizio.

## 7. Esperimento decisivo: dipendenza d’ordine 2

### 7.1 Perché questo è il benchmark pertinente

Entrambi i piani ereditano dalla Master Spec il processo

```text
X_t = X_(t-2) XOR Z_t, con Z_t ~ Bernoulli(0.1)
```

con inizializzazione stazionaria. Conoscere il simbolo immediatamente precedente non riduce l’incertezza; conoscere quello a distanza 2 sì. L’entropia condizionata pertinente è `H_b(0.1) ≈ 0,4690` bit/simbolo, mentre un predittore d’ordine 0 o 1 rimane attorno a 1 bit.

Il benchmark verifica una proprietà sostanziale: raggiungere una dipendenza utile oltre un livello intermedio non informativo. Il suo fallimento non riguarda i confondenti del corpus greco, la dimensione dei gruppi o l’inferenza statistica.

### 7.2 Protocollo della verifica

È stata costruita una riproduzione autonoma e minimale dello pseudocodice normativo:

- crescita eager dei contesti fino a profondità 8;
- add-beta con beta 0,5;
- counts e probabilità pre-update;
- `L_self` e `L_parent` sulle occorrenze previste;
- soglie `k_min = 2`, `gamma = 0`;
- selezione monotona letterale;
- valutazione congelata su una sequenza indipendente;
- 100.000 simboli di valutazione, con 99.996 target dopo la restrizione `past >= 4`.

La lettura a profondità fissa 2 è soltanto un controllo diagnostico che dimostra la presenza di informazione recuperabile nello stesso albero. Non è stata promossa a strumento del progetto.

### 7.3 Risultati riproducibili

| Training | Seme training | CE monotone | CE a profondità 2 | Quota di target risolti alla root da monotone |
|---:|---:|---:|---:|---:|
| 53.304 | 0 | 0,737041 | 0,468445 | 50,505% |
| 53.304 | 1 | **1,000353** | **0,467852** | **100%** |
| 53.304 | 2 | 0,467730 | 0,467730 | 0% |
| 53.304 | 3 | 0,470830 | 0,470830 | 0% |
| 53.304 | 4 | 0,734940 | 0,468218 | 50,438% |
| 200.000 | 0 | **1,000042** | **0,468436** | **100%** |

Questi numeri non dicono che monotone fallisca in ogni realizzazione. Dimostrano che il recupero può dipendere da fluttuazioni accidentali al livello intermedio. Mostrano anche un caso in cui aumentare il training a 200.000 simboli non risolve il problema.

Controlli semplici nello stesso apparato: i.i.d. a quattro simboli, CE held-out 2,000001; ciclo ABC, CE 0,000081; Markov d’ordine 1, CE 0,720464 contro riferimento 0,721928. Sono controlli della riproduzione autonoma, non l’esecuzione dei test G3 canonici ancora incompleti.

### 7.4 Meccanismo del fallimento

Nel caso `N = 53.304`, seme 1:

```text
Delta al contesto di profondità 1, simbolo 0: -4,435064 bit
Delta al contesto di profondità 1, simbolo 1: -0,311236 bit

Delta ai quattro contesti di profondità 2:
  6.322,783235; 7.554,256417; 6.976,058466; 7.289,262934 bit
```

I nodi a profondità 2 guadagnano migliaia di bit sul parent. La regola vieta però di raggiungerli perché i due nodi di profondità 1 non superano la soglia. Il risultato held-out coincide interamente con la root.

Non è necessario un errore di programmazione per ottenere questo esito: è una conseguenza della regola. Non si corregge aumentando semplicemente `d_max`, perché il percorso viene arrestato prima.

### 7.5 Verifica indipendente del calcolo

Per tutti i nodi è stato controllato il totale `L_self` contro la formula chiusa Dirichlet-multinomiale, indipendente dall’accumulazione prequenziale. Gli scarti osservati sono inferiori a `1e-8` bit nei controlli eseguiti.

Per il caso bloccante è stata inoltre ricostruita la probabilità pre-update mediante array cumulativi, senza usare la routine del tree. I sei Delta a profondità 1 e 2 coincidono con quelli della riproduzione sequenziale entro `1e-7` bit; gli scarti effettivi sono molto più piccoli.

Questi controlli riducono il rischio che il risultato derivi da un errore dell’esperimento di verifica. Non costituiscono una prova generale di correttezza di ogni possibile implementazione futura.

### 7.6 Confronto con la fonte metodologica

Schürmann e Grassberger, §V.B, formulano la scelta attraverso un contesto che migliora sul parent e il successivo comportamento del contesto più lungo. Il testo non richiede che ogni antenato, a partire dalla root, migliori a sua volta. La differenza di segno rispetto alla convenzione HEXIS va naturalmente tenuta presente.

Nel caso con livello 1 non migliorativo e livello 2 migliorativo, le due regole non sono equivalenti. Il commento del candidato in quarantena che parla di equivalenza operativa non risolve questa divergenza. Il secondo piano migliora la denominazione dello strumento, ma conserva il comportamento problematico.

Fonte: [Schürmann e Grassberger, Entropy estimation of symbol sequences, 1996; versione arXiv del 2002](https://arxiv.org/abs/cond-mat/0203436), §V.B, pagina 9 del PDF allegato.

## 8. Che cosa si può conservare e che cosa non è ancora deciso

La direzione consigliata per la revisione successiva è già sufficientemente fondata:

- studio descrittivo sul corpus greco delimitato;
- conclusioni condizionate a rappresentazione, segmentazione e protocollo;
- valutazione di tutte le posizioni eleggibili;
- blocchi visibili individualmente, con distinzione fra pesi entro blocco e fra blocchi;
- nessuna replica scientifica attribuita ai seed;
- fit reali successivi alla definizione e validazione dello strumento;
- ritiro dei rami fuori scope senza lasciare entry point applicativi incompleti attivi;
- nessuna promessa di identificare l’effetto causale del metro o la memoria della lingua.

Resta da decidere se il contributo desiderato sia necessariamente quello di un **misuratore adattivo a contesto variabile**, oppure quello di una **misurazione predittiva descrittiva** per cui la scelta dello strumento resta aperta. Queste due priorità possono richiedere percorsi diversi e tempi di sviluppo diversi.

La sostituzione di monotone con una stringa `argmax` non è una soluzione già verificata: occorre definire esattamente l’insieme dei nodi candidati, la quantità ottimizzata, le penalità implicite o esplicite e il fallback; poi verificare che il recupero dell’ordine 2 non avvenga al prezzo di sovraadattamento sui controlli i.i.d. o di un costo incompatibile con lo scopo.

Non è stata implementata né certificata in questa consegna una regola sostitutiva. Presentarla come definitiva prima di queste verifiche contraddirebbe il criterio richiesto per il lavoro.

## 9. Limiti espliciti della verifica

Sono stati verificati il commit, la suite esistente, i conteggi greci, gli hash degli input, il controesempio della permutazione, il conflitto fra selettore e benchmark e i punti documentali discussi sopra.

Non sono stati certificati:

- tutti i dettagli filologici dei 17 documenti e ogni continuità necessaria a P-BOUND;
- una misura scientifica sui testi greci, perché nessun modello vi è stato addestrato;
- la durata dell’implementazione del nuovo protocollo;
- una pipeline completa del disegno ridotto, oggi assente;
- le tabelle di potenza del primo piano;
- l’assenza di ogni altro difetto nella repository;
- la validità generale di uno strumento sostitutivo ancora da selezionare e validare.

Il confronto bibliografico conferma che la separazione prosa/verso mediante caratteristiche sintattiche ha precedenti importanti. Il lavoro di Gianitsos et al. riporta oltre il 97% di accuratezza e F1 nel proprio studio; ciò impedisce una rivendicazione ingenua di primato, non certifica automaticamente l’identificazione di una proprietà universale del greco. [Gianitsos et al., 2019](https://aclanthology.org/W19-2507/).

Anche la letteratura sui context tree per il ritmo linguistico usa procedure di selezione proprie, con ipotesi e risultati specifici: non trasferisce automaticamente tali garanzie al selettore HEXIS. [Galves et al., Context tree selection and linguistic rhythm retrieval from written texts](https://arxiv.org/abs/0902.3619).

## 10. Materiali riproducibili e tracciabilità

L’archivio di verifica consegnato separatamente contiene:

- `check_corpus.py`: ricalcolo dai file CoNLL-U, senza fit reali;
- `check_method.py`: riproduzione autonoma della regola letterale e controlli sintetici;
- `check_independent.py`: seconda ricostruzione numerica e controesempio usando la funzione di permutazione della repository;
- `corpus_check.json`, `method_check.json`, `independent_check.json`;
- istruzioni, riferimenti di versione e hash dei file dell’archivio.

Non contiene i dati grezzi del corpus, né una nuova versione del progetto. I tempi degli script sono tempi dei controlli sintetici in questo ambiente; non sono benchmark della futura pipeline HEXIS.

SHA-256 degli allegati analizzati:

```text
piano_finale_HEXIS.md
c9b4ecee16040d4f9bf57c29e3bd1ed29a98c9a2f484e678499769143f0d1835

piano_ultimato_HEXIS.md
1c0bf17490a48b63921f42db8755d15de8abb1426ef9adefc52bdae9fcdf6d47
```

**Esito operativo:** conservare il secondo piano come base della revisione; non applicare nessuno dei due integralmente. La proposta definitiva resta sospesa sul chiarimento dello statuto dello strumento, con evidenza sufficiente per escludere la ratifica invariata di `monotone-stop` insieme al requisito attuale di recupero affidabile dell’ordine 2.
