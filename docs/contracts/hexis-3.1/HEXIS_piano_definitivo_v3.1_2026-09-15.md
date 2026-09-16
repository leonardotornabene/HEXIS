# HEXIS 3.1 — Piano definitivo di riallineamento

**Ordine entro frase delle annotazioni morfosintattiche in un corpus finito di greco antico**  
**Specifica scientifica, contratto operativo e piano di migrazione — 15 settembre 2026**

**Stato della consegna:** recepimento documentale delle decisioni C01–C30 del verdetto consolidato del 15 settembre; piano pronto per la migrazione normativa, l'implementazione e la redazione del nuovo research proposal. **Non applicato alla repository; nessun gate software futuro attestato; nessun risultato finale disponibile.**

Questa versione sostituisce il piano 3.0.1 come documento di destinazione. La richiesta corrente autorizza il riallineamento del piano: non viene usata per modificare il codice, eseguire nuovi fit reali o riscrivere retroattivamente le decisioni della repository. Il deposito futuro di **V3-001** applicherà in modo esplicito il nuovo disegno. Fino a quel deposito le regole v2.1 continuano a governare le esecuzioni della repository.

## 0. Autorità, materiali e uso del documento

Il piano è una riscrittura integrale coerente con il [verdetto consolidato](/Users/leonardoTornabene/Desktop/hexis-verifica/HEXIS_verdetto_consolidato_2026-09-15.md), comprensiva delle correzioni tecniche e delle rinunce metodologiche motivate nella verifica. Le prescrizioni contenute nei materiali precedenti sono state esaminate come oggetto della revisione, non eseguite come istruzioni operative. Le revisioni A/B restano storia critica; non costituiscono fonti normative concorrenti.

La consegna comprende questo documento e la cartella [HEXIS_allegati_v3.1_2026-09-15](/Users/leonardoTornabene/Desktop/HEXIS_allegati_v3.1_2026-09-15/):

| File | Funzione |
|---|---|
| `hexis_v3.1_design.json` | Contratto strutturato: identità, registro completo, blocchi, trasformazioni, sei celle, semi e popolazioni |
| `corpus_atteso_v3.1.json` | Conteggi documentali e di blocco, attese della rappresentazione accorpata |
| `alphabets_v3.1.json` | Tre liste lessicografiche, ID e tipi presenti soltanto nei sei documenti non valutati |
| `report_contract_v3.1.json` | Granularità degli output, chiavi attese, ricostruzione e controlli di completezza |
| `design_lock.json` | Digest esterni del piano e dei contratti; deposito V0 ancora nullo |
| `verifica_documentale.json`, `SHA256SUMS.json`, `LEGGIMI.md` | Provenienza, controlli effettuati e istruzioni di conservazione |

Il testo governa la semantica; i JSON ne rendono espliciti i valori e gli elenchi. Una divergenza è un errore da correggere prima del deposito, non un'alternativa lasciata all'implementatore. Gli allegati 3.0.1 non sono più il contratto di destinazione. Il loro archivio rimane necessario **soltanto come evidenza storica e fonte identificata delle fixture**, con le limitazioni del §12; nessun suo script va eseguito indiscriminatamente.

Riferimenti materiali:

| Oggetto | Identità |
|---|---|
| Repository esaminata | `g1/pre-audit`, commit `852644b6917790877c7b2ca5df2e76b17829d87c` |
| Piano 3.0.1 originale | SHA-256 `83fed73f273c0552281a7180b101f944c84577b100c43e5a738d95cb85ebab38` |
| ZIP operativo 3.0.1 | `HEXIS_allegati_operativi_v3_2026-09-11.zip`, SHA-256 `6f2e5935b0d0bd70e98028414d085f74e1bd617fc5e293c0b61c8b99a266db8f` |
| Verdetto consolidato | SHA-256 `9cf75b7618864fa208092f5ed163976a385ef5fb0bad806e846ff84661fa7a12` |
| Lock della repository | SHA-256 `33db43b00bcb21ab12aedf6dcc4257764770bff0115dc0d1dfab6e5ea89876bf` |

L'Appendice A traccia tutti i trenta recepimenti. Il disegno non lascia da scegliere durante i fit corpus, modello, numero di celle, pesi, semi, popolazione valutata o risultati obbligatori. Restano da realizzare e verificare i contratti software qui specificati.

## 1. Oggetto scientifico e gerarchia dei risultati

### 1.1 Domanda definitiva

> Nel corpus greco UD Perseus fissato, quale vantaggio predittivo aggiuntivo offre l'ordine entro frase delle annotazioni rispetto al loro rimescolamento entro frase, sotto un CTW congelato addestrato sugli altri blocchi? Come variano i profili dei documenti e dei blocchi con rappresentazione, budget e scelte essenziali del predittore?

HEXIS è uno **studio descrittivo, riproducibile, di un corpus finito**. Il predittore CTW combina probabilisticamente alberi di contesto a memoria finita; non seleziona un unico ordine. Le misure confrontano perdite predittive fuori dal training, espresse in bit per simbolo codificato eleggibile. L'analisi riguarda le sequenze delle annotazioni, non il lessico o l'albero sintattico completo.

Il contributo consiste nel rendere controllabile questo confronto, mostrare i profili dei testi disponibili e quantificare quanto i punteggi dipendano dalle scelte dichiarate. Non richiede che emergano memoria lunga, separazione fra gruppi o risultati positivi. I precedenti su contesti variabili e ritmo, stilometria sintattica greca e classificazione prosa/verso delimitano la novità (§18).

### 1.2 Unica gerarchia

1. **Risultato principale:** i sette profili Q di blocco, con G originale/rimescolato e tutte e quattro le CE; gli undici documenti primari sono visibili separatamente.
2. **Sintesi subordinata:** differenza HEX/prosa delle medie a peso uguale fra blocchi, D_Q, con D_G originale e rimescolato.
3. **Seconda pesatura obbligatoria:** stesse quantità per gruppo e contrasti pesati per target eleggibili della variante corrente.
4. **Diagnostiche:** fasce di storia, supporto dei contesti, pesi della miscela, ritenzione, esposizione del training e frammenti.
5. **Lettura distribuzionale R1:** JSD dei conteggi completi originali dei sette blocchi, nelle tre rappresentazioni.

I semi sono repliche computazionali. SD campionaria, minimo e massimo fra semi descrivono campionamento e rimescolamento; non costituiscono incertezza di popolazione. Gli undici documenti non sono undici repliche indipendenti. Non si calcolano p-value, intervalli bootstrap, Holm, Bayes factor fra regimi o ranghi permutazionali.

### 1.3 Portata delle conclusioni

Sono ammesse descrizioni del vantaggio misurato sotto questo predittore, questa codifica e questi training. Non sono identificati effetto causale del metro, effetto separato di epoca/autore/genere, entropia vera del greco, informazione mutua della lingua, complessità della grammatica o difficoltà cognitiva.

DEPREL deriva dall'analisi del testo completo e può dipendere da parole successive e dalla testa sintattica. La predizione delle etichette non simula un lettore che anticipa parole. La sequenza conserva categorie e relazioni, perdendo la gerarchia dell'albero. La cross-entropia empirica è un costo di codifica sotto un predittore fissato: non diventa automaticamente un tasso entropico o un'informazione mutua.

## 2. Evidenze pregresse e stato epistemico

Il protocollo è **prospettico dopo sviluppo metodologico e osservazione di pilot reali**, non una preregistrazione antecedente a ogni osservazione. Il nuovo accorpamento cambia task e prior totale; la campagna finale non è una replica identica dei pilot. Cambiare convenzione di semi non cancella l'esposizione ai risultati precedenti.

| Evidenza | Copertura e limite |
|---|---|
| Suite della repository nella verifica del 15 settembre | 327 passed, 17 skipped; gli skip sono scaffold, non accettazione del CTW futuro |
| Enumerazione CTW storica | 120 casi, 9.189 asserzioni; errore massimo 1,07×10⁻¹⁴; evidenza archiviata, non riesecuzione nella presente redazione |
| Identità prequenziale/integrata storica | Errore massimo 1,42×10⁻¹⁴ sul training |
| Caso razionale indipendente della verifica | Cinque alberi in un caso binario D2; errore probabilità 1,11×10⁻¹⁶ |
| Piccoli sintetici della verifica | 25 casi rieseguiti; soglie effettive rispettate, incluso ciclo CE<0,02 |
| Pilot storico C0 | 140 modelli originali, sette blocchi × venti semi, alfabeto m=106 |
| Sensibilità storiche | 63 modelli originali, sette per ciascuna delle nove configurazioni storiche; seme 0 |
| Controllo storico di ordine | Sette coppie C0 al solo seme 0; non venti semi accoppiati |
| Contratto 3.0.1 successivo | Sette coppie C0 con nuovo RNG più una coppia `bound`: 16 modelli e 84 valutazioni tragiche; prove storiche, non risultati 3.1 |
| Revisione del 12 settembre | Riesecuzioni d'ambiente, diagnostiche, frammenti e fixture di report; non una campagna finale |

Dai venti semi originali si ricostruisce **D_G originale medio = −0,1780246797**, SD fra semi 0,0110277710, intervallo osservato [−0,1982444032; −0,1573585892] bit/simbolo. Il controllo accoppiato storico consente **D_Q ≈ −0,1772407629 soltanto al seme 0**; qui coincide numericamente con D_G. Mancano i bracci rimescolati necessari a chiamare D_Q il contrasto medio sui venti semi o i contrasti delle sensibilità originali.

Il pilot ha documentato supporto scarso dei contesti profondi: circa l'84–85% dei nodi osservati a profondità 3 ha meno di cinque osservazioni; D12/C0 coincide alla precisione archiviata. Non prova memoria grammaticale corta. Lo stress lag 2 con m=106 ha CE circa 5,09–5,13 contro oracle circa 1,13109; con massa Dirichlet totale 1 circa 3,84–3,90. La capacità di rappresentare una dipendenza non ne garantisce l'apprendimento nel campione.

Le sensibilità storiche di Diodoro sono reali: variazione di G circa −0,04781 bit in `bound` e −0,04761 col prior estremo. Non identificano un singolo nodo responsabile né dimostrano un bug. Restano nel resoconto di sviluppo; le configurazioni ritirate non vengono reinserite nella campagna.

L'allegato storico `authorization_and_experiments.json` è un resoconto delle autorizzazioni pregresse. La presente redazione non verifica indipendentemente il consenso originario, non lo nega e non inventa orari. V3-001 ne registrerà fonte, portata e verificabilità, distinguendolo da un eventuale atto originale recuperato. Nessun vecchio G2 viene dichiarato superato retroattivamente.

## 3. Corpus, identità e unità

### 3.1 Fonte congelata

Si usano soltanto i tre CoNLL-U greci UD Ancient Greek Perseus `r2.18`, commit `37837c7a3c592c9563f8c51cc63344b87247f8a5`. Gli split train/dev/test sono ricomposti; non hanno funzione sperimentale.

| File | SHA-256 |
|---|---|
| `grc_perseus-ud-dev.conllu` | `7899f809fc250404839694330b9db25f79a5b1f20cfa12e6dc3a368a4ec7cd22` |
| `grc_perseus-ud-test.conllu` | `e18d47c395c0ec8da678fb5e315ce6d90133e88c25ed2a55bc72a2a66e6254d5` |
| `grc_perseus-ud-train.conllu` | `d7471c9b91bcd975848fa5d9b65c31f1fc48a597ed3667796968a82c6d098a7e` |

Qualunque discrepanza interrompe l'audit. I raw rimangono immutabili e ignorati da Git. Una nuova versione del corpus richiede nuovo contratto e nuovi risultati. La provenienza necessaria a riprodurre l'acquisizione deve essere tracciata fuori da `data/raw/`.

### 3.2 Unità e registro

- Token sorgente: riga CoNLL-U con ID intero; multiword ed empty node non aggiungono osservazioni.
- Frase sorgente: `sent_id` univoco; nessuna ridefinizione con punteggiatura o versi.
- Documento canonico: opera/estratto definito nel registro. Ateneo XII e XIII sono due parti di un documento.
- Blocco di dipendenza: escluso integralmente dal training; unità di peso uniforme della sintesi subordinata.
- Seme: replica computazionale, mai unità scientifica indipendente.

Il censimento comprende **202.989 token sorgente, 13.919 frasi, 18 prefissi, 17 documenti**. Il registro strutturato conserva tutti i prefissi, URN, `part_order`, attribuzioni, epoche, regimi originari, ruoli e flag. Non si deducono identità dal titolo. L'Appendice B espone la corrispondenza completa.

`PROSE_ALL` raggruppa nel report `PROSE_CLASS` e `PROSE_POST`; non sostituisce il regime sorgente. “Homeric tradition” e “Hesiodic tradition” sono convenzioni conservative di esclusione, non prove di comune autore o indipendenza statistica dei blocchi. L'Inno a Demetra resta attribuito ad Anonymous; lo Scudo conserva l'attribuzione tradizionale con flag esplicito.

### 3.3 Undici documenti primari in sette blocchi

| Blocco | Opere/estratti | Gruppo | Token C0 | Target C0 | Token OTH | Target OTH |
|---|---|---|---:|---:|---:|---:|
| HOMERIC_TRADITION | Iliade; Inno a Demetra | HEX | 71.088 | 46.634 | 71.547 | 47.062 |
| HESIODIC_TRADITION | Teogonia; Opere e giorni; Scudo | HEX | 9.282 | 6.375 | 9.308 | 6.398 |
| HERODOTUS | Storie I | PROSE_ALL | 17.301 | 12.946 | 17.349 | 12.994 |
| THUCYDIDES | Storie I | PROSE_ALL | 9.346 | 7.227 | 9.353 | 7.234 |
| ATHENAEUS | Deipnosofisti XII–XIII | PROSE_ALL | 23.133 | 16.691 | 23.231 | 16.786 |
| DIODORUS | Biblioteca storica XI | PROSE_ALL | 15.266 | 12.334 | 15.266 | 12.334 |
| PLUTARCH | Licurgo; Alcibiade | PROSE_ALL | 8.884 | 6.901 | 8.893 | 6.908 |
| **Totale** | **11 documenti / 7 blocchi** | **2 HEX / 5 prosa** | **154.300** | **109.108** | **154.947** | **109.716** |

UPOS ha gli stessi token e target C0. Il nuovo accorpamento non cambia alcuna maschera. L'Iliade costituisce circa il 97,5% dei token del blocco omerico: questa dominanza deve comparire nella descrizione del profilo.

### 3.4 Sei documenti soltanto censiti

Trachinie, Antigone, Aiace, Edipo re ed Elettra di Sofocle, e Supplici di Eschilo hanno ruolo **`inventory_only`**: censimento, ritenzione e inventario dei tipi, senza training, scoring, probe o figura tragica. Sono testi a metro misto, non un controllo omogeneo di trimetri. I loro 22.275 token C0 e 12.769 posizioni potenzialmente eleggibili restano conteggi di audit, non posizioni da valutare.

Per conservare la scelta di supporto del piano verificato, l'alfabeto usa tutti i 17 documenti. Dopo l'accorpamento i sei non valutati aggiungono **9 tipi esclusivi C0, 10 OTH, zero UPOS**. Il supporto resta quindi chiuso e transduttivo: si conoscono i tipi del corpus completo, senza trasferire frequenze o transizioni al training. Limitarsi ai soli primari produrrebbe 91/95/11 tipi e costituirebbe un'altra modifica, qui esclusa.

### 3.5 Limiti del confronto

Nel primario HEX coincide con la componente arcaica; manca prosa arcaica comparabile. Cronologia, tradizione, genere e forma non sono separabili. Le etichette di prosa riguardano opere, senza certificazione metrica token per token. I campi `subdoc` degli XML di Ateneo esaminati sono riferimenti di passo, non marcatori automatici di citazione: non si inventa un censimento metrico delle citazioni.

L'annotazione non è necessariamente omogenea fra opere. L'accorpamento del §4 mitiga una discontinuità concreta senza uniformare tutte le categorie o DEPREL. Mancano metadati sufficienti per un controllo per annotatore. Le frasi lunghe contribuiscono più target; l'esclusione dei primi quattro simboli non ne pareggia le distribuzioni.

## 4. Rappresentazione, audit e target

### 4.1 Ordine deterministico della codifica

1. Conservare righe con ID intero e tutte le coordinate sorgente; validare tag e struttura. Un UPOS sorgente ignoto è errore anche nella funzione pubblica di mapping.
2. Applicare `PROPN → NOUN`, quindi la maschera degli UPOS ammessi.
3. Ricavare la relazione base con `lower().split(':', 1)[0]` e applicare la politica della variante.
4. Accorpare **globalmente** `PART → ADV_PART` e `ADV → ADV_PART`; nessuna condizione su lemma, testo o gruppo.
5. Costruire il simbolo e assegnare l'ID dell'inventario lessicografico congelato.

UPOS ammessi prima dell'accorpamento: `ADJ, ADP, ADV, AUX, CCONJ, DET, NOUN, NUM, PART, PRON, SCONJ, VERB`. Eliminati: `PUNCT, X, INTJ, SYM`. `ADV_PART` è una categoria di progetto, non un nuovo tag UD accettabile come input sorgente.

Le 23 relazioni conservate sono: `root, nsubj, csubj, obj, iobj, ccomp, xcomp, obl, advcl, advmod, acl, amod, appos, det, nummod, nmod, case, mark, aux, cop, cc, conj, parataxis`. `ud23` denomina questo sottoinsieme storico, non l'intero inventario UD.

| Variante / cella | Politica | m | Massa totale con a=0,5 |
|---|---|---:|---:|
| `ud23` / C0 | Simbolo `UPOS_accorpato:DEPREL_base`; eliminare relazioni esterne alle 23 | **100** | **50** |
| `ud23_oth` / oth | Stessi UPOS; relazioni esterne aggregate in `oth` | **105** | **52,5** |
| `upos_only` / upos | **Maschera C0**, poi proiezione su UPOS accorpato | **11** | **5,5** |

Gli ID sono consecutivi da 0 sulle stringhe ordinate lessicograficamente. BOS ha ID interno −1, solo nei contesti; non appartiene agli esiti. Non sono previsti SEP, EOS o `UNK`. Un simbolo nuovo dopo il freeze causa errore. `representation_version = hexis-3.1-adv-part-1` distingue gli inventari nuovi da quelli 106/112/12 dei pilot.

Le eliminazioni chiudono i vuoti: il contesto conta simboli trattenuti, non distanza in parole grezze. Si conservano UPOS e DEPREL sorgente nell'audit. Nessuna riannotazione manuale, euristica lessicale, FEATS, lemma o lessico entra nel predittore.

### 4.2 Ragione dell'accorpamento e limiti

La verifica diretta conta **11.270 PART nei due blocchi HEX, zero nei cinque blocchi prosastici**: 9.884 omerici e 1.386 esiodei. Per γάρ, nel blocco omerico vi sono 526 PART/13 ADV, in quello esiodeo 54/0, e soltanto ADV nella prosa. L'Inno a Demetra ha zero PART e contiene tutti i tredici γάρ ADV omerici: la discontinuità non coincide perfettamente col gruppo a livello documentale.

Si riduce deliberatamente il dettaglio di una distinzione applicata in modo discontinuo. Non si afferma che ogni annotazione PART sia errata né che il corpus accorpato sia omogeneo. CCONJ, DEPREL e casi come δέ/τε conservano eterogeneità residua. L'accorpamento cambia anche m e la massa del prior: un confronto col pilot non identifica un effetto puro della sola distinzione PART/ADV.

### 4.3 Censimento informativo e controlli

Per documento, blocco e regime originario registrare: UPOS/DEPREL sorgente, eliminazioni con causa e coordinate, ritenzione grezzo→codificato, eleggibili/codificati, numero di frasi senza target e distribuzione delle lunghezze codificate. Censire tutti i 17 documenti; rendere leggibili i controlli anche nei blocchi primari.

- **A:** per ciascuna relazione esclusa, token con UPOS ammesso e quella relazione divisi per tutti i token grezzi del regime; quota >2% segnala. Non sommare relazioni per confrontarle alla soglia. Mostrare anche gli stessi conteggi per documento/blocco.
- **B:** ritenzione documentale <70% segnala.
- Hash, identità e conteggi attesi sono controlli esatti: una discrepanza fa fallire. Le soglie A/B sono diagnostiche, non certificati di comparabilità.

Nel corpus sono presenti **27 DEPREL base e 28 etichette** contando `nsubj:outer`. PROPN e SYM hanno zero occorrenze; le frasi vuote dopo codifica sono zero. Restano casi di test, non trasformazioni effettivamente osservate. I 374 `discourse` sono tutti INTJ, già esclusi dagli UPOS: OTH non li recupera. I `vocative` con UPOS ammesso esclusi sono 459 omerici e 26 esiodei, circa 0,560% e 0,242% dei rispettivi token grezzi. Non qualificarli senza prova come relazioni tipiche della poesia. Il censimento verificato non supera le soglie convenzionali; i valori vanno comunque ricalcolati dall'implementazione.

### 4.4 Target fissati prima degli score

È eleggibile lo slot con **almeno quattro predecessori ordinari trattenuti nella propria frase**, indice zero-based `j ≥ 4`. Tutti i token di training, anche iniziali, contribuiscono ai conteggi. Nel test i primi quattro alimentano la storia senza ricevere perdita primaria. Si valutano tutte le posizioni eleggibili, senza budget o sottocampionamento di test.

In C0 sono eleggibili **53.009/80.370 = 65,96%** dei token HEX e **56.099/73.930 = 75,88%** dei token prosastici trattenuti. Il risultato riguarda posizioni interne e pesa maggiormente frasi lunghe. Le due fasce diagnostiche sono **4–7** e **≥8** predecessori, in ogni cella e braccio. Non sono co-primarie; in D12 la seconda non garantisce dodici predecessori.

Radice e CTW, originale e rimescolato, usano gli stessi slot nella variante. Le celle numeriche e UPOS mantengono la maschera C0. OTH cambia anche la popolazione di target; non si forza un accoppiamento fra righe di codifiche diverse.

## 5. Training, campionamento e casualità

### 5.1 Esclusione per blocco e budget

Per ogni blocco held-out e seme, escludere **tutti** i suoi documenti. Ciascuno degli altri sei contribuisce esattamente **q=8.884 token**, per **53.304** totali. q è il minimo C0 fra i sette blocchi e rimane fisso anche in OTH. `q_half` usa **4.442**, totale **26.652**.

| Gruppo del test | HEX nel training | Prosa nel training | Gruppo del test nel training |
|---|---:|---:|---:|
| HEX | 1/6 | 5/6 | 1/6 |
| Prosa | 2/6 | 4/6 | 4/6 |

Il training è bilanciato per blocco, non per gruppo. La tabella dei sette fold riporta queste quote, anche vicino ai contrasti. Q non corregge automaticamente l'asimmetria; non se ne presume il verso o il carattere conservativo. La quota del proprio gruppo assume due valori determinati dall'etichetta e non identifica da sola l'effetto dell'esposizione. Non si aggiungono `balanced`, modelli comuni o fit per regime.

Quando Plutarco contribuisce in C0 usa tutti i suoi 8.884 token: multinsieme e conteggi del braccio originale sono fissi; l'ordine del ledger può variare e **lo shuffle varia ancora** fra semi.

### 5.2 Algoritmo esatto del campione

1. Ordinare tutte le frasi di un blocco per `(canonical_doc_id, part_order, source_ordinal, sent_id)`, incluse eventuali frasi codificate vuote.
2. Permutare uniformemente gli indici con il sottoseme `sample`. I vuoti restano nell'universo della permutazione ma non consumano budget.
3. Consumare frasi intere finché la successiva supera il residuo positivo. Di quest'ultima scegliere uniformemente un segmento contiguo di lunghezza pari al residuo, con sottoseme `fragment` specifico della frase.
4. Arrestarsi appena raggiunto q: nessuna frase ripetuta, al massimo un frammento per contributore, dunque sei per coppia.
5. Registrare `sent_id, start, end, fragment`, con intervallo `[start,end)` nella frase codificata, coordinate sorgente e sottosemi.

È un campionamento che privilegia frasi intere, non un campione uniforme di singoli token. Ogni frase/frammento è uno **stream autonomo con reset**. La parte esclusa della frase non fornisce storia. BOS significa inizio della storia disponibile nello stream campionato, non necessariamente confine linguistico naturale.

C0, `a_total1`, D12 e UPOS riusano esattamente il ledger C0 per fold/seme. `q_half` riusa la permutazione ma il taglio casuale finale può cambiare: nessun annidamento token per token promesso. OTH riusa l'ordine delle frasi ma può fermarsi altrove. I due bracci condividono sempre le coordinate di taglio del proprio campione.

Il frammento finale è mantenuto per garantire uguale contributo di token. La prova storica a venti semi rilevava 671 frammenti su 840 contributi, 563 con inizio interno; l'ablazione al solo primo seme produceva massimo scarto assoluto Q 0,000685 bit/simbolo. Sono prove locali col vecchio alfabeto, non un limite universale o un'analisi finale da ripetere obbligatoriamente.

Per contributore/coppia registrare `fragment_count`, `internal_start_count`, `fragment_tokens`, `direct_context_targets = Σ min(D, fragment_length)` per frammenti con start>0. Il massimo è **sei segmenti frammentati per coppia, 2.940 occorrenze di segmenti nell'intera campagna**, contate una volta per coppia e condivise dai due bracci; le occorrenze nei bracci sono al più 5.880. Il riuso del ledger fra celle può ridurre ulteriormente il numero di segmenti materialmente distinti.

### 5.3 RNG, identità e invarianza

Master seed **20260706**; C0 semi **0–19**, ogni sensibilità **0–9**. Convenzione **`hexis-v3-rng-1`**, distinta da XOR/CRC32 storico.

`block_key = SHA256(JSON canonico della lista ordinata dei canonical_doc_id membri)`. Autore, epoca, gruppo e nome visualizzato del blocco non entrano nel derivatore. Per ogni estrazione:

```json
{"version":"hexis-v3-rng-1","master":20260706,"seed":0,"held":"<held_block_key>","block":"<contributing_or_evaluated_block_key>","purpose":"sample","sid":"","start":0,"end":0}
```

JSON UTF-8 con `ensure_ascii=False`, `sort_keys=True`, `separators=(',', ':')`, senza newline. L'intero seed è formato dai primi 16 byte SHA-256, big-endian; usare `numpy.random.Generator(numpy.random.PCG64(seed))` (equivalente a `default_rng(seed)` col PCG64 verificato).

Scopi attivi: **`sample`, `fragment`, `shuffle_train`, `shuffle_eval`**. `sample` usa sid vuoto e 0/0; `fragment` usa sent_id e 0/0; lo shuffle usa sent_id e start/end del segmento, oppure 0/lunghezza per frase test intera. In `shuffle_eval`, `held` e `block` sono la chiave del blocco test. Lo scopo storico `shuffle_probe` è ritirato dal contratto attivo.

Parametri numerici, cella, variante, etichette e hash della configurazione non entrano nel seed: così si preserva l'accoppiamento richiesto. Nel training ogni frase usa un RNG di shuffle derivato indipendentemente: il riordino degli stream non consuma un generatore condiviso. Rinomine e riordino dei record non devono cambiare campioni, conteggi o score. Cambiare i membri di un blocco cambia la chiave e richiede una versione nuova.

## 6. Contratto matematico del CTW

### 6.1 Conteggi e distribuzioni locali

A è l'alfabeto congelato, m la sua cardinalità; C0 ha D=8, **a=0,5 per simbolo**, **ρ=0,5 probabilità a priori di arresto**. Non riutilizzare il nome ambiguo `beta`. Un nodo s rappresenta un suffisso percorso dal simbolo più recente al meno recente. Per esito ordinario x:

\[
N_s=\sum_{x\in A}n_s(x),\qquad p_s(x)=\frac{n_s(x)+a}{N_s+ma}.
\]

Tutti i contesti osservati fino a D contribuiscono. Non vi sono `k_min`, `gamma`, pruning euristico, `argmax`, selezione monotona o penalità supplementari. Lo strumento è una media sui modelli, non un selettore con arresto locale.

### 6.2 BOS e partizione dei conteggi

Per ogni target di training visitare radice e storia disponibile in ordine inverso, fino a D. Se la storia termina prima di D aggiungere un arco BOS che porta a foglia terminale. BOS compare solo nei contesti e non è predetto. A profondità D e sotto BOS le foglie sono forzate. In ogni nodo non terminale, per ogni x:

\[
n_s(x)=\sum_{c\in children(s)}n_{sc}(x).
\]

BOS raccoglie precisamente le osservazioni iniziali: radice e figli non sono addestrati su popolazioni incoerenti. Ogni frase/frammento resetta la storia. Nessun collegamento fra frasi, parti o documenti; nessun SEP nella nuova API scientifica.

### 6.3 Evidenza integrata e miscela

\[
E_s=\frac{\Gamma(ma)}{\Gamma(N_s+ma)}\prod_{x\in A}\frac{\Gamma(n_s(x)+a)}{\Gamma(a)}.
\]

Nelle foglie forzate W_s=E_s; altrove:

\[
W_s=\rho E_s+(1-\rho)\prod_c W_{sc},\quad
w_s^{stop}=\frac{\rho E_s}{W_s},\quad
w_s^{split}=\frac{(1-\rho)\prod_cW_{sc}}{W_s}.
\]

Un sottoalbero vuoto ha E=W=1; ometterne i fattori unitari non elimina massa. La ricorsione equivale alla somma delle evidenze degli alberi ammessi, pesate dal prior di arresto/suddivisione. L'evidenza non richiede ordine casuale degli stream. Le convenzioni di stream e BOS sono un adattamento HEXIS esplicito; i teoremi su sorgenti stazionarie non vengono trasferiti senza prova al corpus composito. Il fondamento metodologico è CTW/BCT; si veda la fonte e la delimitazione d'uso in §18.

### 6.4 Predizione congelata e radice

Fissati conteggi e pesi sul solo training, seguendo il successivo arco c della storia h:

\[
q_s(x\mid h)=w_s^{stop}p_s(x)+w_s^{split}q_{sc}(x\mid h).
\]

Su foglia forzata q_s=p_s; entrando in un sottoalbero mai osservato q=1/m. Alla radice si ottiene q_CTW. Il confronto di radice usa gli stessi conteggi globali e a:

\[
q_0(x)=\frac{n_\varnothing(x)+a}{N_\varnothing+ma}.
\]

Durante l'intera valutazione non cambiano **conteggi, evidenze o pesi**. La storia avanza con i simboli precedenti del test, senza leggere i successivi per la predizione. Il prodotto delle probabilità condizionali è un codice predittivo normalizzato; non è l'evidenza congiunta del test con posterior aggiornato online. L'identità prequenziale/integrata si verifica sul training con conteggi **pre-update**, senza autorizzare aggiornamenti sul test.

### 6.5 Numerica e diagnostica di saturazione

Evidenze in logaritmi naturali (`lgamma`, somme stabili, `logaddexp` o equivalente); perdite finali in **log base 2**. Usare float64, conteggi senza overflow, probabilità finite positive e normalizzate. Conservare `log_rho` e `log_one_minus_rho` separati.

Nei nodi non forzati definire u=logρ+logE e v=log(1−ρ)+ΣlogW_figli. Con δ=u−v:

\[
\log w^{stop}=-\operatorname{logaddexp}(0,-\delta),\qquad
\log w^{split}=-\operatorname{logaddexp}(0,\delta).
\]

Ricavare entrambi i pesi da queste quantità; non ottenere il peso piccolo soltanto come `1-stop`. Nei nodi forzati stop=1 e split=0 sono prescritti matematicamente. Negli altri, evidenze finite e prior interno danno due pesi positivi in aritmetica esatta; un 0/1 float64 può essere saturazione numerica, non selezione discreta.

Registrare **`root_stop`** e **`delta_root=u_root−v_root` in nats**: positivo favorisce arresto, negativo suddivisione. Per D=0, delta_root è null con motivo `forced_leaf`, root_stop=1. Circa 37 nat riguarda la perdita di una componente piccola sommata a 1, non l'underflow di `log1p(exp(-37))`; l'esponenziale float64 va a zero verso −745/−746. La sottrazione di grandi log-evidenze può introdurre altra perdita di precisione.

Non costruire il prior estremo come `1-2**(-(m-1))` in float; tenerne i due log-contributi. Il caso m=106 rimane un test numerico storico. Nessun clipping indiscriminato: se si corregge uno scarto di arrotondamento, verificarlo e limitarlo a ≤10⁻¹² senza nascondere errori.

Tolleranze: probabilità/normalizzazione nei piccoli test 10⁻¹² assoluto; log-evidenze d'enumerazione 10⁻¹⁰; ricostruzione CE su output grandi 10⁻⁹ bit/simbolo; riproduzione fra piattaforme 10⁻⁸. Identità, conteggi, coordinate e chiavi coincidono esattamente. Nessun test richiede G_R=0 o D8=D12.

## 7. Controllo d'ordine accoppiato

Per ogni coppia `(cella, fold, seme)`:

1. Costruire il campione di training una sola volta.
2. Preparare braccio originale O e braccio rimescolato R.
3. In R permutare uniformemente **il simbolo composito intero** entro ciascuna frase/frammento campionato, dopo il campionamento. Non separare UPOS e DEPREL.
4. Adattare un modello R con evidenze e pesi propri, sul training rimescolato.
5. Rimescolare indipendentemente ciascuna frase del blocco test con `shuffle_eval` e valutarla sotto R; valutare l'originale sotto O.
6. Accoppiare per identità dello **slot** eleggibile; la provenienza del token spostato è un campo diverso. Verificare la corrispondenza uno-a-uno prima di aggregare.

Si usa una permutazione per seme: venti C0, dieci in ogni sensibilità. Non ripetere fino a ottenere un cambiamento o un segno gradito. Registrare quota di slot con simbolo diverso, con denominatore esplicito; le frasi costanti possono restare identiche. Campionamento e shuffle contribuiscono congiuntamente alla variabilità computazionale, senza decomposizione delle varianze.

Lo shuffle conserva lunghezza e multinsieme di ogni frase/frammento e **conteggi di radice del training**. Non conserva n-grammi, grammaticalità o dipendenze sintattiche. La permutazione senza rimpiazzo induce dipendenze da composizione finita: il controllo non è i.i.d. né stima universale del bias.

La radice O e la radice R sono uguali come distribuzioni di training, ma **le loro CE sul test eleggibile possono differire**: lo shuffle sposta simboli oltre il limite dei primi quattro slot. Occorrono sempre i quattro termini di Q. Il controesempio archiviato dà Q≈0,71346 e scorciatoia `CE_CTW_R−CE_CTW_O`≈−0,66505: può cambiare persino il segno.

G_R nullo alla precisione registrata in alcuni pilot è un risultato osservato, non un'identità generale. Un controllo sintetico i.i.d. del pacchetto aveva root_stop≈0,80775 e G≈0,000195. Le **490 identità rimescolate finali** restano obbligatorie anche se sembrano ridondanti dopo un pilot.

## 8. Punteggi, aggregazioni e R1

### 8.1 Definizioni

Sia I_b l'insieme degli slot eleggibili del blocco b nella variante e n_b=|I_b|. Per seme s e braccio z∈{O,R}:

\[
CE_{CTW,b,s}^{z}=\frac{1}{n_b}\sum_{i\in I_b}-\log_2q_{CTW,s}^{z}(x_i^z\mid h_i^z),
\qquad CE_{0,b,s}^{z}=\frac{1}{n_b}\sum_{i\in I_b}-\log_2q_{0,s}^{z}(x_i^z),
\]

\[
G_{b,s}^{z}=CE_{0,b,s}^{z}-CE_{CTW,b,s}^{z},\qquad
Q_{b,s}=G_{b,s}^{O}-G_{b,s}^{R}.
\]

La cella è sottintesa negli indici. Le stesse definizioni valgono per documento e fascia di storia, con il proprio denominatore. G e Q possono essere negativi: non troncarli. Q quantifica il vantaggio aggiuntivo del contesto con ordine originale rispetto alla trasformazione fissata, non un effetto linguistico depurato da annotazione e training.

### 8.2 Profili e due sintesi subordinate

Dentro documento e blocco **sommare le perdite e dividere per i target**, senza media non pesata di medie documentali. I sette profili di blocco e gli undici documenti sono il primo risultato del report. Per ogni seme, la sintesi a peso uguale fra blocchi è:

\[
D_{Q,s}^{equal}=\frac12\sum_{b\in HEX}Q_{b,s}-\frac15\sum_{b\in PROSE\_ALL}Q_{b,s}.
\]

La sintesi obbligatoria per target eleggibili è:

\[
D_{Q,s}^{target}=\frac{\sum_{b\in HEX}n_bQ_{b,s}}{\sum_{b\in HEX}n_b}
-\frac{\sum_{b\in PROSE\_ALL}n_bQ_{b,s}}{\sum_{b\in PROSE\_ALL}n_b}.
\]

Per entrambe calcolare anche le medie di gruppo delle quattro CE, G_O e G_R e verificare `D_Q = D_G_O − D_G_R`. I pesi sono target eleggibili della variante, mai raw, token trattenuti complessivi o q. Le due pesature si riportano in tutte le sei celle, affiancate. In C0 il blocco esiodeo passa dal 50% del lato HEX a 6.375/53.009≈12,0263%.

Le due sintesi descrivono rispettivamente il blocco medio e il target medio nei gruppi. Nessuna corregge inferenzialmente l'altra; non scegliere la pesatura con maggiore separazione. I training differiscono fra fold: il contrasto descrive questa procedura leave-one-block-out, non sette testi sotto un modello comune.

Prima aggregare per seme, poi riportare media aritmetica, SD con denominatore S−1, minimo e massimo fra semi e S effettivo. Non mediare SD o estremi documentali per produrre quelli di blocco/gruppo. Nessun “±” privo di etichetta. Le sintesi finali fra gruppi sono prodotte dal solo report completo (§14).

### 8.3 R1: JSD senza inferenza

Per ciascuna delle tre rappresentazioni aggiornate usare tutti i **token originali trattenuti completi** dei sette blocchi, inclusi quelli iniziali. Conservare conteggi e frequenze non smussate; definire:

\[
r_b(x)=\frac{n_b^{all}(x)+0,5}{N_b^{all}+0,5m}.
\]

Sono distribuzioni del blocco completo, non radici dei training leave-one-block-out. Per u=(p+q)/2:

\[
JSD(p,q)=\frac12\sum_xp(x)\log_2\frac{p(x)}{u(x)}
+\frac12\sum_xq(x)\log_2\frac{q(x)}{u(x)}.
\]

Produrre **21 coppie e matrice 7×7** per variante, diagonale zero, simmetria e range [0,1] bit. Definire centroidi r_HEX come media uniforme dei due r_b e r_PROSE come media uniforme dei cinque r_b, poi la loro JSD. Non sostituirla con media delle JSD di coppia. Conservare tutti i contributi per simbolo e verificarne la somma.

Gestire `0 log 0 = 0`; la JSD non richiede input strettamente positivi anche se qui sono smussati. Non chiamare la divergenza una distanza metrica. Non aggiungere clustering, test, centroidi pesati per target, JSD dei soli target o dei documenti non valutati. R1 non corregge né convalida Q: descrive una popolazione diversa, esplicitamente scelta. Non richiede CTW o semi. [Lin, 1991](https://www.cise.ufl.edu/~anand/sp06/jensen-shannon.pdf).

## 9. Diagnostiche e semantica

### 9.1 Supporto del modello

Per modello: nodi osservati per profondità strutturale, supporti in classi **1, 2–4, 5–9, ≥10**, numero di esiti osservati e non osservati alla radice, root_stop e delta_root, tempi di fit/valutazione e picco RSS. La classe supporto **0** riguarda sottoalberi impliciti: registrare incontri di valutazione, senza enumerare un albero esponenziale o sommarli ai nodi materializzati.

Per braccio e popolazione valutata: numero e quota di target il cui simbolo non era osservato alla radice, massa instradata al primo sottoalbero non osservato, distribuzione dei pesi per lunghezza del contesto e conteggi delle fasce di storia. I denominatori accompagnano le quote.

### 9.2 Pesi della miscela e L_resolved

Per una storia, λ_s è il prodotto dei pesi di prosecuzione prima di s per il peso di arresto in s. Si raccoglie λ_s solo nei nodi con almeno un'osservazione di training; la massa restante al primo ramo mai osservato è `unseen_mass`. Le masse osservate e unseen_mass sommano a 1 entro tolleranza. Un nodo con una sola osservazione è osservato, senza garanzia di precisione.

`lexical_context_length(s)` conta gli archi ordinari nel contesto; BOS non conta. Conservare le masse osservate per lunghezza ℓ=0,…,D. Se R è la loro somma diretta:

\[
L_{resolved}=\frac{\sum_{s\ osservati}\lambda_s\,lexical\_context\_length(s)}{R}.
\]

Calcolare R come somma diretta, non come `1-unseen_mass`. Con training vuoto, anche se D=0, la predizione è uniforme, unseen_mass=1, R=0 e L_resolved è **null** con motivo `no_resolved_mass`. Nei nodi non vuoti a foglia forzata la massa raggiunta si arresta tutta.

L_resolved descrive le lunghezze **osservate cui la miscela assegna peso**, condizionate alla massa osservata; non misura affidabilità, profondità grammaticale o massimo ordine recuperabile. λ_s non è la responsabilità del componente per il simbolo effettivamente visto, che dipenderebbe anche da p_s(x). Non aggiungere quella nuova diagnostica. Il vecchio `weighted_depth` resta un campo storico; non rinominarne i valori come L_resolved 3.1.

### 9.3 Aggregazione esplicita

Per ogni documento, seme, cella, braccio e fascia conservare la **somma dei L_resolved validi e il loro numero**, il numero dei null, le somme di unseen_mass e delle masse per lunghezza, e i conteggi dei target non visti alla radice. La media L_resolved di blocco è somma dei valori validi per posizione divisa per il numero valido; se n>0 e il numero valido è zero, la media è null con motivo `no_resolved_mass`. **Non** sostituirla col rapporto fra momenti di massa aggregati: è una quantità diversa. `mean_unseen=sum_unseen/n` e `mean_mass[ℓ]=sum_mass[ℓ]/n` usano tutti i target, non soltanto quelli con L_resolved valido.

Le fasce 4–7 e ≥8 hanno n e tutte le componenti di Q. Se una fascia è vuota, n=0, somme additive=0 e CE/G/Q/medie=null con motivo `empty_bucket`; nessun falso score zero. I conteggi degli istogrammi e i supporti necessari alle figure vanno raccolti durante la valutazione. Non selezionare a posteriori contesti o nuove fasce per sostenere il risultato.

## 10. Sei celle e budget definitivo

| Cella | Variante | m | D | a per simbolo | ρ | q per contributore | Semi | Modelli O+R |
|---|---|---:|---:|---:|---:|---:|---|---:|
| **C0** | ud23 | **100** | 8 | 0,5 | 0,5 | 8.884 | 0–19 | **280** |
| a_total1 | ud23 | 100 | 8 | **0,01** | 0,5 | 8.884 | 0–9 | 140 |
| q_half | ud23 | 100 | 8 | 0,5 | 0,5 | **4.442** | 0–9 | 140 |
| D12 | ud23 | 100 | **12** | 0,5 | 0,5 | 8.884 | 0–9 | 140 |
| oth | ud23_oth | **105** | 8 | 0,5 | 0,5 | 8.884 | 0–9 | 140 |
| upos | upos_only | **11** | 8 | 0,5 | 0,5 | 8.884 | 0–9 | 140 |
| **Totale** | **6 celle / 490 coppie** | | | | | | | **980** |

Tutte le celle usano reset e due bracci. Nessuna combinazione fattoriale. `a_total1` significa massa Dirichlet totale 1; il contratto memorizza **a per simbolo=0,01**, senza il precedente campo ambiguo a=1 associato a una modalità.

Le sensibilità confrontano dieci semi con **gli stessi primi dieci C0**, mediante differenze accoppiate per blocco/seme e per entrambe le sintesi subordinate. Non sottrarre la media C0 a venti chiamando il confronto accoppiato. Le differenze fra varianti sono differenze di task; OTH cambia anche target. CE inferiori in UPOS, G simili o contrasti concordi non danno una scala universale né una decomposizione del contributo DEPREL.

Sono ritirate D6, `rho09`, `bound` e tutte le valutazioni tragiche. Le rinunce sono esplicite: nessuna sensibilità finale al prior di arresto/suddivisione, nessuna valutazione dell'attraversamento dei confini, nessuna specificità rispetto ad altri metri. `a_total1` perturba un **altro** prior. D12 controlla soltanto l'aumento della profondità massima. Questi tagli limitano le domande; non sono motivati dalla somiglianza dei risultati nel pilot.

Nessuna sign-stability è condizione di completamento. Inversioni e instabilità si riportano, senza cambiare celle, pesi o semi. Riutilizzare conteggi per prior/D è un'ottimizzazione facoltativa, dopo equivalenza verificata: richiede evidenze/pesi nuovi e foglie corrette. Troncare un D12 mantenendone i pesi non produce D8. Le identità scientifiche restano 980; non serve un sistema generale di cache.

## 11. Contratti software e persistenza

### 11.1 Responsabilità e API

| Componente | Contratto |
|---|---|
| Lettore/censimento | Tre input esatti, identità/ordine/coordinate, errori localizzati su duplicati o metadati mancanti |
| Codificatore | Maschere, accorpamento, inventari congelati e cause di eliminazione |
| Campionatore | Blocchi identificati dai membri, q, held-out e seme → ledger/stream; nessuna etichetta di gruppo |
| CTW fit | Stream di interi, m,D,a e log-prior → modello congelato e fingerprint |
| CTW predict_proba | Storia → vettore su A normalizzato; nessuna mutazione |
| Score/accoppiamento | Stessi slot → quattro perdite e diagnostiche; core senza etichette |
| Annotazione | Registro e score → nomi/gruppi; sola fase che introduce regime nelle aggregazioni |
| R1 | Conteggi originali completi → distribuzioni, JSD e contributi |
| Report | Artefatti verificati → medesime aggregazioni per tabelle e cinque figure |

Conservare il nome/contratto label-free di `pooled_score_core` ove pertinente e l'introduzione delle etichette tramite `annotate_scores`. L'invarianza deve diventare un test comportamentale eseguibile, oltre alla verifica di firma.

Schema rigoroso: rifiutare chiavi ignote/mancanti, duplicati YAML, parametri ritirati, NaN/Inf, bool come interi, float convertiti silenziosamente, m non intero o <2, simboli fuori [0,m), D negativo, q≤0, a≤0, prior non interno, semi/celle duplicati e membri di blocco incoerenti. D=0 e training vuoto sono casi validi del core, non celle reali. BOS è interno; nessun ID negativo in uno stream pubblico. Riutilizzare YAML sicuro e controlli già funzionanti di `config.py`, completandone lo schema.

### 11.2 Audit, coordinate e ledger

`documents.csv`: record documentali per variante con doc_id, prefissi/parti, opera, attribuzione, epoca, regime, ruolo, blocco, raw/frasi, kept/eligible, ritenzione e flag. Dati sorgente eliminati con causa/coordinate in tabella dedicata o equivalente ricostruibile. Nessun dato grezzo viene redistribuito nel kit del piano.

`coordinates.parquet`: per token trattenuto, `variant, slot_uid, doc_id, sent_id, source_prefix, part_order, source_ordinal, source_rank, raw_token_id, encoded_index, symbol_id, available_past, eligible`. L'eleggibilità dei documenti inventory_only è potenziale per censimento; il ruolo ne vieta lo scoring. `slot_uid` è intero stabile nell'ordine canonico della variante; la chiave completa include la variante. Identità testuali in dizionari condivisi, senza duplicare stringhe lunghe nei vettori.

Ordinamento sorgente: prefisso identificato dal `sent_id`, ordinale numerico finale e rango fra tutte le frasi di quel prefisso; validare unicità e sintassi. Non usare l'ordine train/dev/test per ricomporre il testo. Per documento, ordinare per parte e ordinale. L'ordine canonico delle coordinate segue `(doc_id, part_order, source_ordinal, sent_id, encoded_index)`.

`sample_ledger.json`: per campione distinto, blocchi contribuenti, q, coordinate/frammenti/sottosemi e hash. Le celle che lo riusano ne citano l'hash. Conservare le trasformazioni o i dati necessari a rigenerarle esattamente dal contratto RNG e dal ledger.

### 11.3 Identificazione del run

`run_id = SHA256(JSON canonico del run_contract)`. Il contratto comprende versione del piano/rappresentazione, hash del contratto analitico depositato, codice scientifico, dati, registro, alfabeti, configurazione, lock e versione RNG. Timestamp, macchina, percorsi e tempi sono metadati esterni, esclusi da run_id e semi.

Per la campagna finale richiedere **codice tracciato pulito e nessun produttore scientifico dipendente da file non tracciati**. Non cancellare raw ignorati o script locali estranei per ottenere tale requisito. Il commit del deposito e il commit dell'implementazione sono diversi campi: non inserire nel file appena committato l'hash del suo stesso commit creando una dipendenza circolare. L'atto di deposito viene riferito dal manifest esterno successivo.

Chiave modello: `(run_id, cell, held_block_key, seed, arm)`. Chiave coppia: la stessa senza arm. Nessuna identità di valutazione probe. Un fingerprint del modello attesta il contenuto calcolato, senza sostituire test indipendenti.

### 11.4 Posizioni soltanto in C0

Persistenza C0: **2.182.160 righe accoppiate** (109.108 slot × 20 semi), suddivise nelle 140 coppie. Campi minimi:

```text
slot_uid, original_symbol_id, shuffled_symbol_id, shuffled_origin_slot_uid,
loss_ctw_original, loss_root_original, loss_ctw_shuffled, loss_root_shuffled,
unseen_mass_original, unseen_mass_shuffled,
resolved_mean_original, resolved_mean_shuffled
```

Le quattro perdite e le diagnostiche sono float64; L_resolved nullable con motivo. Metadati: run_id, cella, fold, seme, variante, hash dei due modelli e del ledger. Il dizionario coordinate rende recuperabili slot e provenienza. Le quattro perdite sono sempre conservate: niente colonne costanti imposte dal collasso storico.

Non persistere gli alberi completi di ogni fit: fingerprint, campione e parametri consentono rigenerazione. Default sequenziale, una coppia in memoria e scrittura per partizione; poi liberare i modelli.

### 11.5 Sensibilità aggregate, diagnostiche e ricostruzione

Per ciascun documento/seme/cella/fascia conservare **n e quattro somme non arrotondate delle perdite**, una riga accoppiata con chiavi e hash. Le due fasce sono righe disgiunte; il totale si ricava sommando, senza trattarlo come terza popolazione. Per ogni braccio conservare anche i riepiloghi del §9.3, gli istogrammi per lunghezza e i conteggi dello shuffle. I supporti appartengono al modello, non si moltiplicano per i documenti nel riepilogo di fit.

Prima di scartare i vettori delle sensibilità verificare unicità e **uguaglianza dell'insieme degli slot** dei bracci, delle coordinate e dei denominatori attesi. La loro lunghezza uguale non basta. Blocchi e gruppi si ricostruiscono da somme/denominatori; media e SD sui semi solo dopo tale ricostruzione.

Per C0 ricostruire integralmente perdite, CE/G/Q e somme/medie di L_resolved e unseen_mass dai vettori persistiti. Gli istogrammi di massa, i supporti del modello e i conteggi dei simboli non visti alla radice si verificano dai riepiloghi raccolti e dalla rigenerazione prevista: non sono tutti ricavabili dalle colonne posizionali elencate. Per le sensibilità verificare schema, insiemi delle chiavi, additività, denominatori e diagnostiche dagli aggregati; verificare il calcolo posizionale tramite rigenerazione deterministica di casi **prefissati** (§12). Le sole somme non permettono di ricostruire ogni vettore o istogrammi non raccolti: una verifica successiva di singola perdita richiede rifare il caso dal ledger. Gli hash garantiscono identità dei byte, non correttezza matematica.

Tabelle del report, derivate da un'unica implementazione di aggregazione:

- `document_scores.csv`, `block_pairs.csv`: tutte le CE, G, Q, denominatori e fasce, con dettaglio documentale e di blocco.
- `aggregation_weights.csv`, `contrasts.csv`: medie dei gruppi e contrasti con `aggregation=equal_block|eligible_token_weighted`; quote di training accanto ai risultati.
- `seed_summaries.csv`, `sensitivity_pairs.csv`: media/SD/min/max/S e differenze sugli stessi primi dieci semi C0.
- `model_diagnostics.csv` e istogrammi associati: supporti, masse, null, unseen targets, root_stop/delta_root, risorse; ledger con diagnostiche dei frammenti.
- `root_distributions.csv`, `jsd_pairs.csv`, `jsd_centroids.csv`, `jsd_contributions.csv`: R1 completa.

Non creare una seconda tabella di fasce con logica di aggregazione indipendente: le fasce sono una dimensione degli score e dei pannelli esistenti.

### 11.6 Cinque figure

1. **Corpus/annotazione:** quantità, ritenzione e discontinuità per documento; ruoli primario e solo inventario visibili.
2. **Profili:** sette blocchi G_O/G_R/Q e undici dettagli documentali; punti per seme e media, eventuali barre esplicitamente min–max computazionali.
3. **Sensibilità e pesi:** C0 e cinque perturbazioni, confronti accoppiati ai primi dieci semi, due pesature subordinate affiancate; fasce nei pannelli esistenti.
4. **R1:** matrice C0 7×7, JSD dei centroidi nelle tre rappresentazioni e contributi; dati completi senza selezione di contributi favorevoli.
5. **Supporti e masse:** supporti dei nodi, masse per lunghezza, unseen_mass e L_resolved con semantica del §9.

Tutte derivano dalle tabelle verificate. Nessuna figura tragica, per chunk, lessico di contesti, rete di modelli di riferimento o learning curve. Nessuna CI inferenziale.

### 11.7 Manifest, scrittura e ripresa

Un solo manifest per run contiene identità del contratto/dati/registro/alfabeti/codice/lock, versione RNG, chiavi delle esecuzioni, risultati dei controlli e riferimenti alle loro evidenze, lista esatta degli artefatti con hash, dimensioni, schema e cardinalità. Non servono certificati separati, firme o attestazioni annidate.

Scrivere su temporaneo nella directory destinazione, verificare, rinominare atomicamente; stessa protezione per l'aggiornamento del manifest. Un temporaneo non conta come output completo. Nessuna sovrascrittura silenziosa: collisioni falliscono; un eventuale `--force` deve essere esplicito e non mescolare versioni. Un run completo conserva immutabilità dei propri risultati.

`--resume` riusa una partizione soltanto se identità, byte/hash, schema, cardinalità e chiavi coincidono. Non riusare output di codice/contratti diversi. Una fascia vuota dà null motivati; blocco primario senza target, budget impossibile, modello non finito, coppia mancante o parametri non previsti arrestano la cella e bloccano il report. Nessun seme o blocco problematico è escluso automaticamente. Gli output individuali restano disponibili per diagnosi, senza stato finale COMPLETE.

## 12. Accettazione: test prima delle implementazioni

Portare i test pertinenti prima del codice nuovo; non indebolire una proprietà ancora valida. Gli script storici sono riferimenti/fixture isolati e non dipendenze di produzione; nessun import da `candidates/`. Una suite verde v2.1 non certifica v3.1. I controlli attivi non possono essere skip o placeholder.

| ID | Proprietà obbligatoria della destinazione 3.1 |
|---|---|
| T01 | Tre nomi/hash esatti, sent_id univoci; 18 prefissi → 17 documenti |
| T02 | 202.989 token / 13.919 frasi e tutti i conteggi documentali/blocco attesi |
| T03 | Parsing e coordinate; UPOS/DEPREL/sottotipi, multiword/empty, errori precisi su malformati |
| T04 | Accorpamento globale; m=100/105/11; ID lessicografici; UPOS stessa maschera/coordinate C0; 9/10/0 tipi esclusivi inventory_only |
| T05 | Esclusione di ogni membro held-out e di ogni inventory_only dal training |
| T06 | q esatto, nessun rimpiazzo, ≤1 frammento/contributore, vuoti e budget impossibili |
| T07 | Invarianza a ordine dei record/etichette; riuso ledger dichiarato; nessuna dipendenza da gruppi nel core |
| T08 | Vettore RNG noto, separazione scopi, ripetibilità e pairing; nessuno shuffle_probe attivo |
| T09 | Partizione esatta per esito, BOS terminale, reset; nessun SEP/# come esito o collegamento |
| T10 | Enumerazione indipendente di alberi piccoli contro evidenza e predizione, alle tolleranze §6.5 |
| T11 | Normalizzazione, supporto raro/ignoto, training vuoto, D=0; m100/105/11 parametrizzati; input rigorosi |
| T12 | Identità prequenziale/integrata del training con pre-update; invarianza all'ordine degli stream |
| T13 | Conteggi/evidenze/pesi/fingerprint invariati prima e dopo ogni valutazione |
| T14 | Prior estremi in log, due pesi stabili, saturazione distinta dalle foglie forzate |
| T15 | Tutti i 25 piccoli sintetici alle soglie §12.1; violazioni causano exit non zero |
| T16 | Stress storico m106: esecuzione, normalizzazione, supporti e divario dall'oracle dichiarato |
| T17 | Shuffle conserva multinsieme/radice, slot e maschera; provenienza distinta dallo slot |
| T18 | Controesempi prefissati di eterogeneità e dipendenza interna; nessun assunto universale G_R=0 |
| T19 | Q a quattro termini e controesempio di inversione del segno della scorciatoia |
| T20 | Perdite→documenti→blocchi→gruppi; due pesature e quattro componenti con fixture di lunghezze diseguali |
| T21 | Sensibilità sui primi dieci C0; OTH cambia popolazione; join esatte e mismatch rilevati |
| T22 | Masse/supporti/L_resolved, valid_count/null_count, fasce vuote, media per posizione corretta |
| T23 | R1: simmetria, diagonale, range, zeri, centroidi e somma contributi con fixture indipendenti |
| T24 | Sei inventory_only censiti e inclusi solo nell'inventario: zero training e zero scoring finale |
| T25 | Uguaglianza degli insiemi attesi di 490 coppie / 980 modelli, celle/semi/bracci completi |
| T26 | Scrittura atomica/interrotta, resume, corruzione, duplicati e chiavi extra rifiutati |
| T27 | C0: CE/G/Q e L/unseen dai vettori; altre diagnostiche dai riepiloghi e dalla rigenerazione; sensibilità da aggregati più rigenerazione; cinque figure derivate |
| T28 | Nessun import candidates o utility inferenziali nella pipeline; nessuno skip nei test attivi |
| T29 | Riproducibilità identità esatte e CE entro tolleranze; stato del codice e lock verificati |
| T30 | Nessun contrasto/report finale incompleto: controllo byte, contratto, insiemi chiavi, R1 e denominatori, senza certificati autonomi |

I casi generici relativi a utility statistiche conservate restano validi. Ritirare un requisito del selettore o dei probe significa sostituirne motivatamente il test, non aggiungere uno skip o cancellare controlli generici. In particolare T24 verifica l'assenza di scoring dei sei documenti.

### 12.1 Batteria sintetica congelata

Riutilizzare esattamente algoritmi, semi e oracle di `ctw_validation/verify_synthetic.py` dentro `verifiche_CTW_precedenti.zip` del pacchetto identificato in §0. Non ricostruire il generatore a memoria. Training **53.304**, test indipendente **100.000**, esclusione dei primi quattro slot; cinque semi per le cinque sorgenti piccole.

| Sorgente | Regola | Criterio per ogni caso |
|---|---|---|
| Uniforme m=4 | i.i.d. equiprobabile | \|CE−2\|≤0,02 |
| Ciclo m=3 | Periodico deterministico | **CE<0,02** |
| Markov 1 binario | P(stesso)=0,8 | \|CE−h₂(0,2)\|≤0,03; riferimento 0,721928… |
| Lag 2 binario | P(copia distanza 2)=0,9 | \|CE−h₂(0,1)\|≤0,03; riferimento 0,468996… |
| Memoria variabile | Contesti 1/2, generatore archivio | Scarto dall'oracle della realizzazione ≤0,03 |

Semi training 0–4, test 10000+seme; ogni sequenza costituisce un singolo stream; CTW D8/a0,5/ρ0,5. Nel generatore storico di memoria variabile, P(x_i=1)=0,2 se x_(i−1)=0, altrimenti 0,1 se x_(i−2)=0, altrimenti 0,9. Conservare ordine delle chiamate RNG e inizializzazione del file identificato. **Il suo oracle realizzato usa i=2,…,N−1 e denominatore N−2; lo scoring usa i=4,…,N−1 e N−4.** Si conserva esplicitamente questa fixture verificata, senza descrivere i denominatori come identici o ridefinire silenziosamente l'oracle.

Soglie e seed non si cambiano dopo i risultati. Un JSON `analytic_pass=false` seguito da exit 0 non supera il gate. Conservare il confronto noto lag 2 recuperato rispetto al riferimento di circa 1 bit del selettore locale storico, senza reintrodurlo nei risultati greci.

Stress **storico m=106**, tre semi per uniforme, lag 2 con copia 0,9/innovazione uniforme 0,1 e nucleo binario con simboli rari. Nel lag 2 la coincidenza è 0,9+0,1/106, oracle circa 1,13109 bit. Si richiedono conteggi, normalizzazione, esecuzione e registrazione del deficit, non raggiungimento dell'oracle. Nessuna ulteriore campagna di calibrazione degli alfabeti nuovi: m100/105/11 sono coperti dai controlli parametrizzati di input/normalizzazione/supporto.

I sintetici di eterogeneità e shuffle mantengono le fixture archiviate; le soglie in quei casi non calibrano un test sul greco. Il controesempio di profondità oltre D8 dimostra soltanto che D12 può differire, non una soglia di rilevabilità universale.

### 12.2 Fixture RNG e riproduzione prefissata

Vettore artificiale noto: membri held `['held']`, contributore `['fixture']`; block_key rispettivamente `e7b28f6b342cb9fe4fe171f6f02275c1de5349f73462a8709b4e0679a332ab99` e `b074a6afd500bbf0891340a1cdda223c1516d7bb52518b820848e1d29d12788a`. Con master 20260706, seme 0, scopo sample, sid vuoto e estremi 0/0, seed derivato **218577625307806857638750380866922209360** e `permutation(6)=[0,4,3,2,1,5]`.

Fixture di frasi `fixture@1`…`fixture@6`, lunghezze `[5,8,0,2,7,6]`, q=17: ledger atteso `@1[0,5), @5[0,7), @4[0,2), @2[3,6)`; soltanto l'ultima è frammento. Il sottoseme fragment di @2 è **46436027119566646866315332695474949224**. Lo script storico del contratto contiene altre attività reali: estrarne la fixture, non lanciarlo per verificare soltanto il seed.

Per T27/T29 fissare **prima della campagna** la rigenerazione del seme 0 di tutti i sette fold in tutte le sei celle (42 coppie / 84 modelli), in una directory distinta, confrontandoli con le partizioni della campagna. È una verifica di riproduzione della prova integrata già prevista, non nuove identità scientifiche o nuovi semi. Per le sensibilità confrontare anche gli aggregati e le diagnostiche rigenerati; controllare gli slot in memoria. Provare inoltre una ripresa con interruzione/corruzione simulata su fixture di persistenza. Nessun caso scelto per il suo punteggio.

## 13. Migrazione normativa e tecnica

### 13.1 V3-001: atto unico da depositare

Nell'incarico di implementazione creare un ramo `codex/…` dalla revisione verificata o da una sua evoluzione prima riesaminata; preservare storia e file locali. Il namespace **V3-001** non collide con D55. L'atto dovrà contenere questi punti, senza alternative metodologiche residue:

1. Adottare **HEXIS 3.1** e il contratto qui consegnato per le nuove esecuzioni; sostituire esplicitamente il disegno operativo v2.1 e il piano 3.0.1.
2. Recepire insieme scope greco finito/intrafrase, registro, accorpamento, CTW congelato, Q, gerarchia dei profili, due pesature, R1, sei celle, output e checklist V0–V5.
3. Dichiarare **non applicabili alla 3.1**, senza darli per risolti nella v2.1: P1/P2 confermativi, latino/L1, O7/sign-flip, costanti permutazionali, 13 celle v2.1, sign-stability e gate G0–G7. Non sostituire silenziosamente le costanti controverse di D55.
4. Conservare D01–D54, D55 proposto, ratifiche tecniche G1, vecchi piani e revisioni come storia con stato chiaro. Le ratifiche tecniche G1 non ratificano retroattivamente il corpus o questa analisi.
5. Conservare immutabilità/provenienza dei raw, core senza etichette, quarantena `candidates/`, determinismo, scritture sicure e test effettivi.
6. Registrare i pilot già osservati e le autorizzazioni **con fonte e grado di verificabilità** (§2). Il resoconto di sessione non diventa verifica indipendente di consenso né passaggio retroattivo di G2. Distinguere date delle attività, del consenso documentato e del deposito Git; non inventare orari.

Aggiornare nello stesso passaggio normativo: `docs/01_MASTER_SPEC.md`, `docs/02_DECISION_LOG.md`, `docs/03_ROADMAP_OPERATIVA_IT.md` e registro bibliografico, `docs/00_LEGGIMI_INDICE.md`, `docs/HANDOFF.md`, `docs/04_AI_HANDOFF_PROMPT.md`, `AGENTS.md`, `CLAUDE.md`, configurazione, registro, inventario test e metadati del pacchetto. README e proposal devono assumere immediatamente il nuovo perimetro e lo stato effettivo; la disponibilità operativa dei comandi si attesta dopo implementazione e test.

Depositare i byte dei contratti e del piano con i digest esterni di `design_lock.json`. Lo stato della consegna rimane `FINAL_PLAN_NOT_APPLIED`; non farlo accettare surrettiziamente dalla CLI v2.1. Il record del deposito V0 è esterno al contenuto che identifica il contratto. La configurazione applicativa dovrà esportare una proiezione analitica equivalente, confrontata campo per campo, oltre a verificare i byte depositati. Cambiare corpus, parametri, blocchi, trasformazioni, target, semi, pesi o risultati obbligatori richiede versione e decisione motivata; ricalcolare un hash non basta.

### 13.2 Mappa concreta del lavoro

| Percorso / area | Intervento |
|---|---|
| `src/hexis/conllu_reader.py` | Riutilizzare parsing e validazioni; preservare ID grezzi, identità, ordine e coordinate necessari |
| `src/hexis/registry.py` | Registro completo/parti/ruoli/blocchi; consumare `part_order`; separare regime da gruppo del report |
| `src/hexis/alphabet.py` | Accorpamento globale, errori su ignoti, ID lessicografici e freeze; audit documentale |
| `src/hexis/sequences.py` | Stream frase/frammento con reset e coordinate; ritirare concatenazione e `#` predetto, nessun SEP |
| `src/hexis/config.py` | Conservare YAML sicuro e rifiuto duplicati/chiavi; nuovo schema rigoroso e derivatore SHA-256 |
| `src/hexis/model/context_tree.py` | CTW canonico al posto dello stub; numerica e API congelata; riferimento isolato solo nei test |
| `src/hexis/model/diagnostics.py` | Supporti e pesi della miscela, L_resolved/null; nessuna profondità selezionata |
| `src/hexis/protocols/sampling.py` | Campione esatto, frammenti, RNG, ledger e shuffle |
| `src/hexis/protocols/scores.py` | Quattro perdite, slot accoppiati, somme e G/Q; core indipendente dai gruppi |
| `src/hexis/manifest.py` | Riutilizzare provenienza/hash; completare run_contract, atomicità, resume e controlli di completezza |
| `src/hexis/pipeline/run_audit.py` | Conservare difese funzionanti; separare identità dai vecchi gate/metodologia bilingue |
| `run_encode.py`, `run_tree_validation.py` | Implementare gli stadi prima di pubblicizzarli |
| Nuovi `run_descriptive.py`, `run_report.py` | Un esecutore parametrizzato delle sei celle e un reporter con unica aggregazione |
| `run_sensitivity.py` | Ritirare l'entry point dalla destinazione; selezione delle celle nello stesso esecutore |
| `run_confirmatory.py`, `run_null_calibration.py`, `run_reference.py`, `run_latin.py` | Ritirare CLI e obblighi; nessuna chiamata nascosta |
| `model/lexicon.py`, `blocks.py` | Ritirare lessico/chunk dal percorso scientifico; chunk ≠ blocco di dipendenza |
| `stats/permutation.py`, `bootstrap.py`, `holm.py` | Conservare utility funzionanti e test validi come storico; nessun import nella pipeline descrittiva |
| `viz/plots.py` | Cinque figure derivate dalle tabelle validate |
| `tests/`, `conftest.py`, marker pytest | Inventario nuovo con mappa mantenuto/sostituito/ritirato; nessuno skip nell'accettazione attiva |
| `pyproject.toml`, `uv.lock` | Metadati coerenti, stesso stack; nessuna libreria CTW o downgrade immotivato |
| `.gitignore`, `LICENSE`, documentazione licenze | Separare codice, documenti, raw, output locali voluminosi e materiali destinati alla pubblicazione |
| `scripts/reacquire_raw_data.sh` locale | Preservare l'originale; eventuale versione canonica corretta e verificata prima di pubblicizzarla |

La verifica trova parsing/audit e utility statistiche funzionanti, molti moduli scientifici stub. `config.py` rifiuta già chiavi ignote/mancanti e alcune strutture G1: non riscriverlo come se non esistesse. Il mapping storico può scartare un tag sconosciuto e l'alfabeto ordinava per frequenza: questi comportamenti vanno sostituiti esplicitamente. La scrittura esistente non fornisce ancora tutta l'atomicità/ripresa richiesta. I 327 pass storici non attestano CTW nuovo o pipeline disponibile; il test comportamentale dei punteggi senza etichette era uno skip. Non risulta un workflow CI tracciato: non inventare attestazioni CI né introdurne l'aggiunta come requisito di questo piano.

### 13.3 Acquisizione e file locali

Lo script `scripts/reacquire_raw_data.sh` **esiste ed è leggibile, ma non è tracciato**. Legge provenienza da raw, acquisisce greco e latino e itera sui file presenti senza confrontare l'insieme dei tre attesi. Il ramo SKIP per hash mancante non è gestione verificata degli errori: `set -euo pipefail` può interrompere prima. Non usarlo oggi per riparare un corpus già verificato.

La versione eventualmente adottata deve usare provenienza tracciata fuori da raw, acquisire soltanto il greco fissato, confrontare **l'insieme dei tre nomi CoNLL-U attesi** e tutti gli hash, fallire su assente/extra/hash mancante/record ambiguo. Il confronto riguarda i CoNLL-U della sorgente greca, non vieta README o metadati del clone. Non alterare automaticamente cloni preesistenti. Preservare file non tracciati e dati locali senza cancellazioni per ottenere uno stato Git apparentemente pulito.

## 14. Sequenza di esecuzione e completezza

V0–V5 sono una **checklist ordinata**, non un sistema di certificati separati. Il manifest raccoglie esiti e riferimenti alle verifiche nel contesto di codice/contratto/lock effettivo.

| Passo | Lavoro | Uscita verificabile |
|---|---|---|
| **V0 — Contratto** | Deposito V3-001, testi, registro, allegati/lock e inventario test | Contratto di destinazione coerente; vecchie clausole incompatibili esplicitamente storiche |
| **V1 — Corpus** | Lettura, hash, identità, accorpamento e coordinate | 17 documenti, 11 primari, 6 solo inventario, m100/105/11 e conteggi identici |
| **V2 — Core/protocollo** | CTW, sampling/RNG/shuffle, score, diagnostiche, R1 e persistenza | Test esatti/sintetici e controlli pertinenti T01–T23/T26 superati, senza skip |
| **V3 — Integrazione** | Un seme (0) per tutte le sei celle; misure risorse; freeze codice/ambiente | **42 coppie / 84 modelli tecnici**, finiti/coerenti, zero probe, schema finale verificato |
| **V4 — Campagna** | Sei celle, tutti i semi/bracci, R1 e output | **490 coppie / 980 identità di modello**, tre R1, insiemi chiavi e artefatti completi |
| **V5 — Consegna** | Report, cinque figure, ripresa e rigenerazione prefissata | T24–T30 completi; risultati/limiti dichiarati senza selezione del segno |

Il contratto analitico si congela in V0; V3 congela implementazione e ambiente. I nuovi fit reali iniziano soltanto nella prova integrata, dopo V0–V2 nel nuovo percorso autorizzato. V3 verifica integrazione/risorse, non seleziona parametri tramite i contrasti. Se gli 84 modelli tecnici usano esattamente codice, contratto e schema finali, si possono riusare tramite resume nei 980. Una correzione che cambia codice/run_id richiede rigenerazione sotto la nuova identità; non si sommano risultati di versioni diverse.

### 14.1 CLI di destinazione, da pubblicizzare solo quando implementata

```bash
uv sync --frozen
uv run pytest -q
uv run python -m hexis.pipeline.run_audit --config config/default.yaml
uv run python -m hexis.pipeline.run_encode --config config/default.yaml
uv run python -m hexis.pipeline.run_tree_validation --config config/default.yaml
uv run python -m hexis.pipeline.run_descriptive --config config/default.yaml --cell all
uv run python -m hexis.pipeline.run_report --config config/default.yaml
```

`run_descriptive` accetta `all` o una delle sei celle verificate; esegue i due bracci e produce score/somme individuali. La prova V3 seleziona il solo seme 0 previsto dal contratto e resta prova tecnica incompleta, non una campagna finale con cardinalità ridefinita. `--resume` segue §11.7. R1, sintesi e figure usano il report unico. Nessun orchestratore distinto per sensibilità, nessun framework aggiuntivo. Questi sono requisiti futuri, non inviti a chiamare oggi entry point assenti o a saltare i gate v2.1.

### 14.2 Validatore del report

Prima di emettere contrasti fra gruppi o report finale:

1. Verificare byte/hash del contratto depositato, piano/lock e proiezione analitica della configurazione; non aggiornare automaticamente gli hash attesi.
2. Verificare le evidenze richieste di V0–V3 riferite al codice e al lock del run, nello stesso manifest. Un PASS scritto a mano non equivale alle prove.
3. Generare dal contratto le chiavi `(cell,held_block_key,seed,arm)` e confrontare per **uguaglianza degli insiemi** con le 980 identità complete; rilevare duplicati prima di trasformare le liste in insiemi. Ripetere per le 490 coppie e le chiavi documento/fascia previste.
4. Verificare lista esatta di artefatti, byte/hash, dimensioni, schemi, slot, ruoli e denominatori. C0: tutte le righe previste. Sensibilità: entrambe le fasce per documento anche se vuote, quattro somme e riepiloghi diagnostici.
5. Calcolare/verificare le tre R1, le 21 coppie per variante, centroidi e contributi. Rifiutare qualunque scoring inventory_only.
6. Ricostruire perdite→documenti→blocchi→gruppi e le identità di Q nei due pesi; verificare gli esiti di rigenerazione previsti per la consegna definitiva V5.

Assenza/corruzione di una sola cella impedisce entrambe le sintesi finali. Sono disponibili output individuali di diagnosi; non si scrive un contrasto parziale come risultato definitivo. Il report scientifico completo è emesso dopo le verifiche V4 e, per lo stato di consegna finale, V5. Le figure derivano dagli stessi aggregati, senza altra implementazione delle formule.

### 14.3 Cardinalità da non confondere

| Quantità | Valore e significato |
|---|---|
| Celle / coppie / modelli | **6 / 490 / 980** |
| Coppie C0 / sensibilità | **140 / 350** |
| Prova tecnica seme 0 | **42 coppie / 84 modelli**; riusabili solo sotto identità definitiva |
| Valutazioni probe | **0** |
| Documenti × semi × cella × braccio prima delle fasce | **1.540** righe logiche = 11×(20+5×10)×2 |
| Aggregati accoppiati per documento e due fasce | **440 C0 + 1.100 sensibilità = 1.540** righe; stesso numero, **schema diverso** dalla riga precedente |
| Righe accoppiate posizionali C0 persistite | **2.182.160** = 109.108×20 |
| Righe posizionali teoriche di tutte le sei celle | **7.643.640** = 109.108×60 + 109.716×10; non tutte persistite |
| R1 | **3×21 coppie**, tre matrici 7×7 e tre centroidi/contributi |

I numeri sono controlli riepilogativi; non sostituiscono le chiavi attese. Le righe logiche per braccio possono essere viste derivate delle righe accoppiate, senza duplicare storage. Una fascia vuota rimane una riga con n=0 e null motivati.

## 15. Ambiente e risorse

Python 3.12 via uv; conservare il lock della repository. La verifica del 15 settembre registrava Python 3.12.13 e NumPy 2.5.1 coerente col lock; i prototipi iniziali usavano Python 3.12.14/NumPy 2.3.5. Sono ambienti distinti. I confronti del 12 settembre su sette fold e 42 contributi hanno dato hash identici fra le due versioni NumPy sullo stesso host: non certificano tutte le piattaforme o l'intera pipeline.

Il piano non aggiunge dipendenze, non impone downgrade e non richiede GPU. `uv sync --frozen` usa il lock identificato. Un cambiamento necessario di dipendenze richiede motivazione/versione e ripetizione dei controlli pertinenti, non una risoluzione automatica per far passare il run.

Le misure storiche del prototipo — fit C0 circa 0,63–0,70 s, valutazione held-out 0,024–0,224 s, RSS C0 circa 174 MiB e massimo circa 240 MiB D12 — attestano soltanto quelle prove. Tempo, RSS e disco della pipeline 3.1 **vanno misurati in V3**; nessuna previsione più precisa di giornate o minuti diventa requisito.

Da 1.400 a 980 modelli scientifici: riduzione del **30%**. Da 12.704.540 righe posizionali del vecchio schema a 2.182.160: riduzione **82,82% delle sole righe posizionali**. Non equivale a riduzione totale di tempo/disco. A 76 byte/riga il solo payload numerico C0 è circa **158,2 MiB** prima di overhead; non è benchmark Parquet o requisito RAM. Le vecchie 921 MiB si riferivano al vecchio schema e non restano il fabbisogno di destinazione.

Scrivere per partizione, non concatenare l'intera campagna in memoria; conservare una coppia di modelli alla volta. Risorse insufficienti richiedono correggere la gestione o predisporre capacità adeguata, non ridurre a posteriori blocchi, semi o celle. Il costo residuo è soprattutto integrazione/test/report, non nuova raccolta o annotazione.

## 16. Regole delle conclusioni

| Esito / situazione | Interpretazione consentita |
|---|---|
| G_O positivo, G_R simile | Il guadagno non distingue chiaramente ordine osservato e controllo scelto |
| Q positivo, contrasto piccolo | Vantaggio relativo sotto questo predittore, senza forte separazione descrittiva fra i gruppi disponibili |
| Segni/ampiezze variabili per cella o peso | Dipendenza dalle scelte dichiarate e dalla distribuzione dei target; nessuna selezione del risultato preferito |
| G_R numericamente nullo | Comportamento misurato del controllo; nessun teorema di collasso o attribuzione causale di tutto G all'ordine |
| D8/D12 simili | Nessun miglioramento nelle configurazioni valutate; non assenza di dipendenze oltre otto simboli |
| C0/UPOS con contrasti simili | Concordanza della sintesi in due rappresentazioni; non prova che DEPREL non contribuisca |
| Accorpamento tecnicamente corretto | Mitigazione della discontinuità documentata; non omogeneità annotativa dimostrata |
| JSD alta, Q simile | Differenze marginali senza corrispondente differenza nel vantaggio d'ordine misurato |
| Sei testi soltanto nell'inventario | Nessuna conclusione finale sulla specificità rispetto alla tragedia o ad altri metri |

Vicino ai profili e alle sintesi esporre corpus finito, 2/5 blocchi, dominanza delle opere, confondimento cronologico/annotativo, training diverso per fold, annotazioni offline, controllo condizionato alla composizione entro frase, pesi e natura computazionale della dispersione, e pilot già osservati.

Non aggiungere G/CE0, DEPREL-only, permutazioni di etichette, modelli bilanciati o riaggregazioni senza singole opere per tentare un'attribuzione non sostenuta. Togliere un'opera soltanto dalla media non la elimina dai training degli altri fold e non è leave-one-document-out. L'eventuale effetto dell'accorpamento su G/Q è ignoto prima della campagna: è un risultato futuro, non una decisione metodologica sospesa.

Il completamento dipende dalla correttezza dell'esecuzione, non dal segno, dalla separazione o dalla conferma del pilot. Nessun “effetto assente” senza definire quantità e limiti della misura. Nessuna SD dei semi viene trasformata in incertezza sui testi antichi.

## 17. README, research proposal e consegna scientifica

### 17.1 Prima del codice: proposta scientifica coerente

Questo piano e i suoi contratti chiudono le decisioni da trasferire nel nuovo proposal. Il proposal può essere scritto **prima della campagna**, dichiarando implementazione in corso e risultati finali assenti. Deve contenere:

1. Titolo e domanda intrafrastica del §1; contributo circoscritto e precedenti pertinenti.
2. Corpus fissato, 17 censiti/11 primari/7 blocchi, due HEX/cinque prosa e accorpamento ADV_PART.
3. CTW congelato, training per blocco, Q a quattro termini, profili principali, due sintesi subordinate e R1.
4. Sei celle, target j≥4, semi computazionali, nessuna inferenza di popolazione.
5. Pilot pregressi descritti come D_G e controlli Q effettivamente coperti; limiti e criteri di completamento indipendenti dall'esito.

Non promettere effetto del vincolo metrico, firma universale, memoria della grammatica, transfer fra regimi, risultati latini o generalizzazione al greco. La bibliografia attiva deriva dal registro §18, aggiornato nello stesso atto normativo.

### 17.2 README: stato prima, operatività dopo i test

Il riallineamento normativo del README deve riportare subito scope 3.1, stato reale dell'implementazione, materiali verificati, limiti e riferimenti autorevoli. Non chiamare l'audit esistente uno stub né descrivere il CTW ancora assente come disponibile.

Dopo V2/V3 aggiungere soltanto comandi effettivamente implementati e verificati: installazione dal lock, acquisizione controllata, audit/codifica, test, esecutore unico, resume e report. Dopo V5 documentare riproduzione, artefatti consegnati e risultati. Nessuna dipendenza circolare fra README “finale” e certificazione del software.

### 17.3 Deliverable dell'implementazione

Repository coerente 3.1 con commit/lock e test; registro/alfabeti/audit; 980 identità, ledger e manifest; vettori C0 e aggregati sufficienti delle sensibilità; R1 completa; cinque figure e report; verifica di ripresa/rigenerazione; archivio storico e istruzioni di riproduzione in cartella nuova.

Raw, coordinate e simboli per posizione rimangono **artefatti locali di riproduzione** finché un successivo atto di pubblicazione ne dichiari destinazione, provenienza e condizioni applicabili. Non attribuire automaticamente la licenza del codice ai dati o alle sequenze derivate. Il progetto distingue codice, documenti e dati sorgente; raw CC BY-NC-SA 2.5 e indicazioni esistenti restano tracciati, senza decidere qui la qualificazione giuridica dei derivati. La presente consegna non pubblica dati, non ridistribuisce raw e non modifica licenze della repository.

## 18. Registro bibliografico attivo di destinazione

Queste sono le fonti direttamente utilizzate, da recepire nel registro del progetto in V0 conservando quello storico. Gli obblighi di citazione relativi a latino, transfer e stimatori ritirati non rimangono vincoli della 3.1 se non hanno funzione nel testo. Nessuna fonte esterna al registro viene introdotta implicitamente nel proposal.

| ID | Riferimento e funzione |
|---|---|
| B01 | **UD Ancient Greek Perseus r2.18**, commit `37837c7a3c592c9563f8c51cc63344b87247f8a5`: dati effettivi, identificati anche dai tre hash. [Snapshot](https://github.com/UniversalDependencies/UD_Ancient_Greek-Perseus/tree/37837c7a3c592c9563f8c51cc63344b87247f8a5) |
| B02 | **AGDT 2.1**, commit `bf4334f0af5e13d16b04c1cccd6237e683ac6f5f`: inventario/metadati e nota sulla distinzione avverbio/particella. Non sostituisce il corpus UD e non certifica omogeneità. [Descrizione](https://github.com/PerseusDL/treebank_data/blob/bf4334f0af5e13d16b04c1cccd6237e683ac6f5f/v2.1/Greek/README.MD) |
| B03 | **Kontoyiannis, Mertzanis, Panotopoulou, Papageorgiou, Skoularidou (2022)**, *Bayesian Context Trees: Modelling and Exact Inference for Discrete Time Series*, JRSS B **84(4), 1287–1323**, DOI **10.1111/rssb.12511**. Fondamento della miscela CTW/BCT; BOS e congelamento dell'intero test sono convenzioni HEXIS esplicitate qui, non attribuite integralmente al paper. [Editore](https://academic.oup.com/jrsssb/article/84/4/1287/7073257) |
| B04 | **Galves, Galves, García, Garcia, Leonardi (2012)**, *Context tree selection and linguistic rhythm retrieval from written texts*, Annals of Applied Statistics **6(1), 186–209**, DOI **10.1214/11-AOAS511**. Precedente su selezione di contesti e codifiche ritmiche del portoghese, distinto dalla valutazione CTW di annotazioni greche. [Testo primario](https://arxiv.org/abs/0902.3619) |
| B05 | **Vanessa B. Gorman, Robert J. Gorman (2016)**, *Approaching Questions of Text Reuse in Ancient Greek Using Computational Syntactic Stylometry*, Open Linguistics **2, 500–510**, DOI **10.1515/opli-2016-0026**. Stilometria sintattica su percorsi degli alberi; pagine confermate dal deposito. [Deposito degli autori](https://digitalcommons.unl.edu/historyfacpub/208/) |
| B06 | **Schürmann, Grassberger (1996)**, *Entropy estimation of symbol sequences*, Chaos **6, 414–427**; deposito arXiv 2002. Cautela su stima da sequenze finite e convergenza; non identifica i guadagni empirici con informazione mutua. [Testo primario](https://arxiv.org/abs/cond-mat/0203436) |
| B07 | **Jianhua Lin (1991)**, *Divergence Measures Based on the Shannon Entropy*, IEEE Transactions on Information Theory **37(1), 145–151**. Definizione e proprietà JSD. [Articolo](https://www.cise.ufl.edu/~anand/sp06/jensen-shannon.pdf) |
| B08 | **de Marneffe, Manning, Nivre, Zeman (2021)**, *Universal Dependencies*, Computational Linguistics **47(2), 255–308**, DOI **10.1162/coli_a_00402**. Natura dello schema di annotazione; non certifica la qualità di ogni opera. [ACL](https://aclanthology.org/2021.cl-2.11/) |
| B09 | **Herrera, Silai, Corro, Guillaume, Kahane (2025)**, *Extraction of Contrastive Rules from Syntactic Treebanks: A Case Study in Romance Languages*, QUASY/SyntaxFest **26–38**, **versione 2**. Limiti di comparabilità; nessuna importazione del loro protocollo inferenziale. Il v1 aveva quattro autori: l'aggiunta di Caio Corro è un cambio di versione, non una correzione retroattiva del v1. [PDF v2](https://aclanthology.org/2025.quasy-1.5v2.pdf), [metadati/versioni](https://aclanthology.org/2025.quasy-1.5/) |
| B10 | **Gianitsos, Bolt, Chaudhuri, Dexter (2019)**, *Stylometric Classification of Ancient Greek Literary Texts by Genre*, Proceedings of the **3rd Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature, 52–60**, DOI **10.18653/v1/W19-2507**. Precedente sulla classificazione greca prosa/verso; nessuna priorità assoluta rivendicata da HEXIS. [ACL](https://aclanthology.org/W19-2507/) |

I rapporti di verifica e i JSON storici sono evidenze del progetto, distinti dalla bibliografia scientifica. I metadati B03/B05/B09/B10 sono stati ricontrollati sulle fonti primarie durante questa redazione; le altre citazioni conservano la verifica documentata dal rapporto consolidato.

## 19. Stato finale del disegno e criteri di chiusura

Il disegno di destinazione è definito: corpus e ruoli, accorpamento, target, training, semi, CTW, Q, pesi, R1, diagnostiche, sei celle, persistenza e controlli non richiedono nuove scelte guidate dai risultati. La verifica documentale e il riconteggio confermano la coerenza dei valori recepiti. **Non costituiscono una certificazione della futura implementazione o una garanzia di conclusioni scientifiche positive.**

Le incertezze residue sono delimitate: entità dei nuovi G/Q, comparabilità annotativa completa, quota di citazioni metriche, spiegazioni puntuali delle sensibilità storiche, verificabilità dell'autorizzazione originaria e prestazioni integrate. Non richiedono ampliare corpus, modello o analisi: si dichiarano e, dove pertinente, si misurano nella campagna prescritta.

Sequenza definitiva: **recepimento e deposito del contratto → proposal e riallineamento normativo del README → implementazione e verifica → aggiornamento operativo del README → campagna completa, riproduzione e report**. Il nuovo documento è il piano di questo lavoro; non ne anticipa gli esiti.

## Appendice A — Tracciabilità completa C01–C30

| Decisione della verifica | Recepimento in questa versione |
|---|---|
| C01 | §1: titolo/domanda intrafrastica, promessa circoscritta |
| C02 | §§1.2,8: sette profili principali, undici dettagli, due sintesi subordinate |
| C03 | §§3,11–12: tragedie solo inventory_only e inventario su 17 documenti |
| C04 | §4.1–4.2: PART/ADV globale e limite annotativo |
| C05 | §§4,10 e JSON: m100/105/11, prior aggiornati, nuovi inventari/ID/hash |
| C06 | §4.3: audit sorgente, esclusioni e correzioni concrete |
| C07 | §5.1: q/esposizione e precisazione Plutarco |
| C08 | §5.2: campione/frammenti/ledger conservati e limiti espliciti |
| C09 | §§4.4,9: j≥4 e due fasce secondarie |
| C10 | §§7–8: shuffle dei due bracci, slot e Q a quattro termini |
| C11 | §10: sei celle, accoppiamento ai primi dieci C0 e rinunce |
| C12 | §8.3: R1 originaria nelle tre rappresentazioni aggiornate |
| C13 | §6: CTW congelato, BOS/reset, nessun SEP attivo |
| C14 | §9: pesi di miscela, L_resolved e aggregazione/null corretti |
| C15 | §6.5: due pesi da log-contributi, delta_root e saturazione |
| C16 | §12: 25 casi alle soglie, stress storico m106 e m effettivi nei controlli |
| C17 | §10: riuso facoltativo verificato, sempre 980 identità |
| C18 | §2: Diodoro storico, nessuna indagine aggiuntiva obbligatoria |
| C19 | §§2,13: separazione pilot/campagna/consenso e no G2 retroattivo |
| C20 | §16: limiti delle conclusioni, nessuna attribuzione indebita |
| C21 | §18: registro breve e metadati/versioni corretti |
| C22 | §11.4–11.5: C0 posizionale, sensibilità aggregate sufficienti |
| C23 | §§11,14: esecutore/report unici e cinque figure |
| C24 | §§11.7,14: lock/manifest/validatore, senza certificati separati |
| C25 | §§10,14.3,15: cardinalità e risorse ricalcolate; allegati nuovi |
| C26 | §§11.3,11.7: codice identificato, atomicità, resume e niente overwrite implicito |
| C27 | §13: mappa aderente al codice e script acquisizione locale |
| C28 | §12: T01–T30 aggiornati, no skip e proprietà generiche conservate |
| C29 | §13: atto V3-001, versione 3.1 e riallineamento normativo unico |
| C30 | §§14,17,19: disegno pronto distinto da pipeline e risultati verificati |

## Appendice B — Registro e conteggi documentali

La tabella seguente è generata dal registro verificato e dagli attesi allegati. Le sigle di blocco sono quelle integrali del §3.3; per `inventory_only` il blocco è nullo. Gli URN e i flag filologici sono conservati integralmente nel JSON del contratto.

| Prefisso sorgente | Documento canonico | Parte | Regime | Ruolo | Blocco |
|---|---|---:|---|---|---|
| `tlg0012.tlg001.perseus-grc1.tb.xml` | `tlg0012.tlg001.perseus-grc1.tb.xml` | 0 | HEX | primary | HOMERIC_TRADITION |
| `tlg0020.tlg001.perseus-grc1.tb.xml` | `tlg0020.tlg001.perseus-grc1.tb.xml` | 0 | HEX | primary | HESIODIC_TRADITION |
| `tlg0020.tlg002.perseus-grc1.tb.xml` | `tlg0020.tlg002.perseus-grc1.tb.xml` | 0 | HEX | primary | HESIODIC_TRADITION |
| `tlg0020.tlg003.perseus-grc1.tb.xml` | `tlg0020.tlg003.perseus-grc1.tb.xml` | 0 | HEX | primary | HESIODIC_TRADITION |
| `tlg0013.tlg002.perseus-grc1.tb.xml` | `tlg0013.tlg002.perseus-grc1.tb.xml` | 0 | HEX | primary | HOMERIC_TRADITION |
| `tlg0016.tlg001.perseus-grc1.1.tb.xml` | `tlg0016.tlg001.perseus-grc1.1.tb.xml` | 0 | PROSE_CLASS | primary | HERODOTUS |
| `tlg0003.tlg001.perseus-grc1.1.tb.xml` | `tlg0003.tlg001.perseus-grc1.1.tb.xml` | 0 | PROSE_CLASS | primary | THUCYDIDES |
| `tlg0008.tlg001.perseus-grc1.12.tb.xml` | `tlg0008.tlg001.perseus-grc1.tb.xml` | 12 | PROSE_POST | primary | ATHENAEUS |
| `tlg0008.tlg001.perseus-grc1.13.tb.xml` | `tlg0008.tlg001.perseus-grc1.tb.xml` | 13 | PROSE_POST | primary | ATHENAEUS |
| `tlg0060.tlg001.perseus-grc3.11.tb.xml` | `tlg0060.tlg001.perseus-grc3.11.tb.xml` | 0 | PROSE_POST | primary | DIODORUS |
| `tlg0007.tlg004.perseus-grc1.tb.xml` | `tlg0007.tlg004.perseus-grc1.tb.xml` | 0 | PROSE_POST | primary | PLUTARCH |
| `tlg0007.tlg015.perseus-grc1.tb.xml` | `tlg0007.tlg015.perseus-grc1.tb.xml` | 0 | PROSE_POST | primary | PLUTARCH |
| `tlg0011.tlg001.perseus-grc2.tb.xml` | `tlg0011.tlg001.perseus-grc2.tb.xml` | 0 | OTHER_VERSE | inventory_only | — |
| `tlg0011.tlg002.perseus-grc2.tb.xml` | `tlg0011.tlg002.perseus-grc2.tb.xml` | 0 | OTHER_VERSE | inventory_only | — |
| `tlg0011.tlg003.perseus-grc1.tb.xml` | `tlg0011.tlg003.perseus-grc1.tb.xml` | 0 | OTHER_VERSE | inventory_only | — |
| `tlg0011.tlg004.perseus-grc1.tb.xml` | `tlg0011.tlg004.perseus-grc1.tb.xml` | 0 | OTHER_VERSE | inventory_only | — |
| `tlg0011.tlg005.perseus-grc2.tb.xml` | `tlg0011.tlg005.perseus-grc2.tb.xml` | 0 | OTHER_VERSE | inventory_only | — |
| `tlg0085.tlg001.perseus-grc2.tb.xml` | `tlg0085.tlg001.perseus-grc2.tb.xml` | 0 | OTHER_VERSE | inventory_only | — |

| Documento | Raw | Frasi | C0/UPOS trattenuti | C0/UPOS eleggibili | OTH trattenuti | OTH eleggibili |
|---|---:|---:|---:|---:|---:|---:|
| `tlg0003.tlg001.perseus-grc1.1.tb.xml` | 10396 | 532 | 9346 | 7227 | 9353 | 7234 |
| `tlg0007.tlg004.perseus-grc1.tb.xml` | 5044 | 248 | 4481 | 3493 | 4486 | 3497 |
| `tlg0007.tlg015.perseus-grc1.tb.xml` | 4943 | 251 | 4403 | 3408 | 4407 | 3411 |
| `tlg0008.tlg001.perseus-grc1.tb.xml` | 26245 | 1630 | 23133 | 16691 | 23231 | 16786 |
| `tlg0011.tlg001.perseus-grc2.tb.xml` | 5229 | 431 | 4224 | 2610 | 4302 | 2674 |
| `tlg0011.tlg002.perseus-grc2.tb.xml` | 4299 | 391 | 3573 | 2076 | 3618 | 2115 |
| `tlg0011.tlg003.perseus-grc1.tb.xml` | 5319 | 490 | 4364 | 2503 | 4428 | 2558 |
| `tlg0011.tlg004.perseus-grc1.tb.xml` | 5600 | 520 | 4571 | 2610 | 4648 | 2680 |
| `tlg0011.tlg005.perseus-grc2.tb.xml` | 5239 | 528 | 4259 | 2331 | 4334 | 2389 |
| `tlg0012.tlg001.perseus-grc1.tb.xml` | 79890 | 6003 | 69327 | 45515 | 69770 | 45927 |
| `tlg0013.tlg002.perseus-grc1.tb.xml` | 2061 | 166 | 1761 | 1119 | 1777 | 1135 |
| `tlg0016.tlg001.perseus-grc1.1.tb.xml` | 19575 | 1092 | 17301 | 12946 | 17349 | 12994 |
| `tlg0020.tlg001.perseus-grc1.tb.xml` | 4610 | 273 | 4023 | 2945 | 4034 | 2955 |
| `tlg0020.tlg002.perseus-grc1.tb.xml` | 3725 | 283 | 3189 | 2077 | 3197 | 2084 |
| `tlg0020.tlg003.perseus-grc1.tb.xml` | 2403 | 182 | 2070 | 1353 | 2077 | 1359 |
| `tlg0060.tlg001.perseus-grc3.11.tb.xml` | 16882 | 733 | 15266 | 12334 | 15266 | 12334 |
| `tlg0085.tlg001.perseus-grc2.tb.xml` | 1529 | 166 | 1284 | 639 | 1293 | 646 |

## Appendice C — Stato della verifica della presente consegna

La redazione ha ricontrollato gli hash del pacchetto di verifica e degli allegati precedenti, rifatto il censimento senza fitting e verificato gli alfabeti accorpati. I controlli documentali confrontano i trenta recepimenti, testo/JSON, chiavi e cardinalità, digest, riferimenti locali e assenza di vecchi parametri attivi. Le verifiche indipendenti hanno controllato formule/diagnostiche, il vettore RNG e la copertura effettiva dei pilot. La suite storica e i 25 sintetici restano attestazioni della verifica consegnata, non vengono presentati come test appena eseguiti sul futuro codice canonico.

Nessun fit reale nuovo, modifica della repository o pubblicazione di dati è parte di questa consegna. I risultati dei controlli **effettivamente eseguiti** e gli hash dei file di destinazione sono nel kit 3.1. Il controllo finale di deposito verifica che i byte sul Desktop coincidano con quelli riesaminati.
