# PROGETTO HEXIS — ROADMAP OPERATIVA

Dal giorno zero al preprint, architettura v2.0 a strumento unico (context tree alla Rissanen). Versione 2.1 — 21 luglio 2026. Sostituisce la v2.0 (6 luglio 2026); la v1.0 resta archiviata in `archive_v1/`. Destinatario: te. Lingua: italiano. Documento tecnico vincolante: `01_MASTER_SPEC.md` v2.1 (citato come §N); decisioni: `02_DECISION_LOG.md` v2.1 (D01–D54; O7 bloccante per G2/G5). Ordine di esecuzione v2.1 dei gate (D44(vii)): **G0 → G1 → G3 → G2 → G4 → G5 → G6 → G7**.

## Premessa 1: il modello di lavoro "ibrido guidato" (invariato)

Tu resti l'autorità metodologica; l'AI è l'ingegnere. **Capisci tu** (senza doverlo saper programmare): entropia ed entropy rate; il principio MDL e la quantità Δ(s); perché la quantità primaria è la cross-entropy held-out; perché la permutazione si fa a livello di documento; perché i punteggi di P2 devono essere costruiti "alla cieca" rispetto alle etichette; cosa i risultati non dimostrano. **Delega all'AI**: codice, test, grafici, debugging. **Verifichi sempre**: ogni numero deve dichiarare dati, parametri, commit e seed (manifest).

## Premessa 2: il tempo

Hai dichiarato 12–15 settimane, chiedendo però di ottimizzare per qualità e non per calendario. Il piano nominale è di **13 settimane** a ~10 h/settimana (≈ 117–133 h totali); le settimane 14–15 sono margine per imprevisti. Il rischio maggiore del progetto (la correttezza del context tree) è stato **anticipato alla Fase 2**: se qualcosa deve rompersi, si rompe presto, quando costa poco. Se il tempo si allunga, si allunga la Fase 7 (scrittura), mai la validazione.

## Rituale di ogni sessione (10 minuti che risparmiano ore)

1. Rileggi il criterio di accettazione della fase corrente.

2. Sessione AI nuova: incolla il bootstrap (`04_AI_HANDOFF_PROMPT.md`) + allega Spec e Decision Log.

3. Dichiara: fase, task, "definition of done".

4. Fine sessione: test scritti e verdi? Manifest generato? Se no, non è finito.

## FASE 0 — Ambiente su macOS (settimana 1, 6–10 h)

**Obiettivo:** Mac pronto: Python moderno, versionamento, Claude Code. Nessuna analisi. **Passi:** (1) Terminale; (2) `xcode-select --install`; (3) Homebrew dal sito ufficiale https://brew.sh (su Apple Silicon: aggiungi `eval` `"$(/opt/homebrew/bin/brew shellenv)"` al profilo); (4) `brew install git` e `brew install --cask` `visual-studio-code`; (5) uv dal sito ufficiale https://docs.astral.sh/uv, poi `uv python install 3.12`; (6) **Claude Code** dalla guida ufficiale **https://code.claude.com/docs/en/setup** (installer nativo raccomandato su Mac, niente Node richiesto; verifica con `claude doctor`; richiede piano Pro/Max o API key) [verificato 2026-07-05]; (7) account GitHub + repo privato `hexis`; (8) `git config --global user.name/email`. **Deliverable:** `git --version`, `uv --version`, `claude doctor`, `code --version` rispondono senza errori. **Prompt-tipo (EN):**

Read `01_MASTER_SPEC.md` §3.1 and §6.1. Initialize the `hexis` skeleton exactly per §6.1: pyproject (Python 3.12, deps §6.3), `src/hexis` stubs with the §6.2 signatures (type hints, docstrings, `raise` `NotImplementedError`), `tests/`, `.gitignore` (ignore `data/raw/`), `config/default.yaml` verbatim from §6.3. No logic yet. Run `uv run pytest` to confirm collection.

**Chiusura fase:** nessuna profilazione richiesta a G0 (O6 è spostato a G3; D45; un microbenchmark sintetico indicativo è ammesso solo via il candidato in quarantena D47, etichettato come indicativo). **Gate G0** si chiude in Fase 1a con i test non-tree reali e l'infrastruttura deterministica verificata.

## FASE 1a — Pipeline non-tree → chiusura Gate G0 (settimana 2, ~8–10 h)

**Obiettivo:** implementare e testare tutto ciò che non è l'albero: `conllu_reader`, `registry`, `alphabet`, `sequences`, `blocks` + test (§7) con asserzioni reali (zero skip nel set G0), più l'infrastruttura deterministica (derivazione dei seed, risoluzione della config, scrittura del manifest per run con sidecar minimo — §6.4/D46, protezione da sovrascrittura). **Cosa impari:** il formato CoNLL-U; i multiword token latini (que/ue) e perché si espandono; l'alfabeto UPOS+DEPREL come funzione totale (§3.4). **Criterio di accettazione (G0, riformulato da D45):** ambiente bloccato; tutti i test non-tree verdi con asserzioni reali; infrastruttura deterministica verificata. Nessuna profilazione qui: O6 → G3 (D45). **Clausola di acquisizione parallela (D45):** il clone dei treebank e la compilazione di `PROVENANCE.md` (v2.18, §2.5, con SHA-256 e commit) sono acquisizione, non audit, non toccano modelli e possono procedere in parallelo a G0; l'audit di G1 resta rigorosamente dopo G0. **Prompt-tipo (EN):**

Implement `conllu_reader.py` per §3.2 and `alphabet.py` per §3.4 (TOTAL function; order of operations normative), tests first (§7, incl. a synthetic CoNLL-U fixture with one MWT range and one empty node). Real assertions only — no skipped tests in the G0 set. Also implement the deterministic infrastructure: seed derivation, config resolution, run-manifest writing with minimal sidecars (§6.4/D46), overwrite protection.

## FASE 1b — Audit del corpus → Gate G1 (settimana 3, ~10 h)

**Obiettivo:** con i treebank acquisiti (`PROVENANCE.md` compilato), produrre l'audit che **congela alfabeto, registro e T\***. **Cosa impari:** le GATE-A/GATE-B; cosa è T* e perché serve (§4.2; ambito del contrasto primario, D51). **Cosa fa l'AI:** `run_audit` → `audit_report.md`. **Decisioni umane:** compili `config/registry_overrides.yaml` mappando ogni prefisso `sent_id` a (autore, opera, regime) contro le tabelle verificate di §2.3; risolvi il duplicato *Inno a Demetra* (O2 — nota D43(vi): la decisione ha conseguenze inferenziali dichiarate sul piano-autore, tracciate come O8); verifichi la partizione autoriale 3/3 (O8); controlli GATE-A (es. vocativi > 2%? — in caso di attivazione vale D50: C0 resta l'unica primaria e le celle `oth` diventano a interpretazione obbligatoria) e GATE-B; verifichi gli inserti in versi di Petronio (O4); prendi nota di T* calcolato (atteso vincolante: "HEX meno Iliade"; ambito: solo contrasto primario, D51). **Criterio di accettazione (G1):** nessuna frase non assegnata; gates risolti; O2/O8 risolti; `alphabet.json`, registro e T* congelati; tutti i test non-tree verdi (G0 incluso). **Touchpoint supervisore linguistico.** **Nota v2.1 (D44(vii)): il Gate G2 non segue più immediatamente G1** — è riposizionato dopo G3, perché il congelamento del piano richiede la risoluzione di O7 (validità del sign-flip), che a sua volta richiede l'albero implementato. L'invariante di D30 resta intatto: prima di G2 solo dati sintetici; i primi fit su dati reali restano a G4, dopo il congelamento. **Prompt-tipo (EN):**

Implement `run_audit.py` producing `audit_report.md` with the contingency tables, GATE-A/B evaluations, per-regime restricted-position fractions (D35), and the T* computation per §4.2 (primary-contrast scope, D51). Do not freeze anything — I review before G1.

## FASE 2 — IL CUORE: context tree, teoria + implementazione + validazione → Gate G3 (settimane 4–7, ~30–35 h)

È la fase cardine, anticipata rispetto alla v1: il progetto ora è questo strumento. **Cosa impari (indispensabile, da possedere davvero):** - entropy rate; perché la conditional entropy a ordine fisso non basta; - MDL: un contesto più lungo si usa solo se ripaga; Δ(s) = L_par − L_self; perché la codifica prequenziale include già il costo del modello (niente penalità separata); - la regola di selezione monotone-stop; il ruolo di β, k_min, γ, d_max; - perché la quantità primaria è la CE held-out e non h_online (D19/D32); - **Task T5.1:** lettura integrale di Schürmann & Grassberger 1996 §V.A–B (arXiv:cond-mat/0203436), annotando nel Decision Log (eventuale D18-A1) ogni differenza tra le formule pubblicate e i default della Spec. **Cosa fa l'AI:** implementa `model/context_tree.py` esattamente per §4.1–4.3 (pseudocodice normativo), `model/diagnostics.py` (identità delle "fette": radice = unigramma lisciato; nodi di profondità 1 = bigrammi lisciati), e i test: i **quattro processi analitici** (§4.7: uniforme → 2.000 bit; ciclo periodo-3 → CE < 0.02; Markov P(stay)=0.8 → 0.7219; XOR ordine-2 ε=0.1 → 0.4690 contro

≈1.0 dell'ordine-1), slice tests, fallback, simboli mai visti. **In più nella v2.1 (D44/D45):** (a) **profilazione O6** del costo di fit (conferma del budget D37) — qui, non a G0; (b) **studio di calibrazione del null (O7, bloccante per G2/G5):** su soli dati sintetici, generazione da un unico processo (H0 vera), partizione in 11 pseudo-documenti con il profilo di taglie del corpus (disponibile dopo G1), esecuzione della catena completa (LODO, T*-matching, media sui seed, sign-flip) e misura dell'errore di tipo I empirico ai livelli nominali, con la permutazione di P2 come controllo positivo; software: `pipeline/run_null_calibration.py` + `tests/test_null_calibration.py`; consegna: report di calibrazione. **Criterio di accettazione (G3):** tutti i test elencati in §7 per G3 verdi (incluso `test_null_calibration`); T5.1 completato e loggato; profilazione O6 registrata; report di calibrazione O7 consegnato. **Touchpoint supervisore matematico** (in agenda anche D18-A1, la proposta di emendamento sulla politica di crescita depositata via D47). Nessun dato reale è ancora stato toccato da un modello. **Al termine di G3: Gate G2** — congelamento del piano confermativo (§4.4/§5; hash del piano registrato; deposito OSF opzionale; **richiede O7 risolto**). Da qui in poi, prima di toccare dati reali con un modello, il piano è chiuso; ogni modifica passa dal Decision Log. **Prompt-tipo (EN):**

Implement `model/context_tree.py` per §4.1–§4.3 exactly: reversed-context trie, prequential add-β predictor, predict-then-update with PRE-update counts, Δ(s) = L_par − L_self, monotone-stop selection with k_min/γ, d_max, frozen-tree `evaluate()` with ancestor fallback and per-position records. Write `tests/test_context_tree.py` and `tests/test_tree_slices.py` FIRST with the §4.7 targets and tolerances. Do not touch real data until all pass. Explain in comments why the sequential code length already includes the model cost.

## FASE 3 — Modelli di riferimento e letture descrittive → Gate G4 (settimana 8, ~10 h)

**Obiettivo:** primi fit sui dati reali (post-freeze): un modello di riferimento per regime (protocollo a, §4.2); diagnostiche §4.6 verdi sui fit reali; letture descrittive: distribuzioni-radice e rank–frequency (F1), curve guadagno-vs-contesto e profondità (F5–F6, via protocolli held-out), profili CE nei blocchi per Iliade ed Erodoto (F7), h_online (una riga per regime, comparabilità SG96), e il **lessico dei contesti** (D38: top-20 per regime per Δ(s), T6/F9) — l'output interpretabile per il lettore linguista. **Criterio (G4):** diagnostiche verdi; figure/tabelle con manifest; niente statistiche confermative ancora. **Nota (dichiarata):** la precedenza delle letture descrittive (G4) sull'inferenza (G5) è presentazionale, non epistemica: il piano confermativo è già congelato a G2, quindi vedere le descrittive non apre gradi di libertà analitici.

## FASE 4 — Inferenza confermativa → Gate G5 (settimane 9–10, ~15 h)

**Obiettivo:** P1 e P2 (più S1 secondaria). **Cosa impari:** perché i punteggi di P2 sono **label-free** (protocollo c: modelli pooled LODO che non consultano mai le etichette → la permutazione esatta sui punteggi fissi è valida sotto H0; D36 — corregge un difetto sottile della v1); perché P1 usa il sign-flip (simmetria di ΔCE sotto H0 con T*-matching); la **restrizione di posizione** available_past ≥ 4 (D35: la segmentazione in frasi è editoriale; senza restrizione il guadagno confonderebbe organizzazione e lunghezza delle frasi); Holm su famiglia {P1, P2} (soglie 0.025/0.05; minimi raggiungibili 1/2048 e 1/462, con lateralità dichiarata accanto a ogni soglia — D43: per la permutazione a gruppi disuguali le soglie uni- e bilaterale coincidono). **Cosa fa l'AI:** `protocols/sampling.py`, `protocols/scores.py` (delta_ce_scores; pooled_scores **con test di invarianza alle etichette obbligatorio**), `stats/permutation.py` (enumerazioni esatte), bootstrap gerarchico, `run_confirmatory` → T3, T5, F2–F4 (+ curve di apprendimento F8). **Criterio (G5):** test §7 verdi (incluso label-free byte-identico); risultati con p esatti Tier-1, più il piano-autore **descrittivo senza α** (D43: soglie strutturali dichiarate — permutazione bilaterale 2/20 = 0,10; sign-flip unilaterale 1/64 ≈ 0,016; punteggio di blocco = media non pesata dei suoi documenti; rerun Lisia-fusa anch'esso senza α), effetti in bit, CI bootstrap (etichettate "tra documenti", §5.3); colonne descrittive `G_own` e frazioni di pool own-regime (D44/D49); dot plot per documento come display primario. **Prerequisito (D44): O7 risolto** — nessuna inferenza confermativa su P1 prima della validazione del sign-flip.

## FASE 5 — Latino + sottocampioni greci appaiati → Gate G6 (settimana 11, ~8–10 h)

**Obiettivo:** L1. P1-latino (sign-flip esatto 2^8 = 256) e P2-latino (permutazione esatta C(8,2) = 28, soglie coincidenti per entrambe le lateralità — D43 → qualitativa per costruzione, niente α); d_max = 6; sensibilità senza Petronio e senza Res Gestae; **B = 100 sottocampioni greci** appaiati alle taglie latine, con localizzazione percentile dei valori latini (risponde a: le differenze greco–latino eccedono l'effetto della sola taglia?).

## FASE 6 — Piano di sensibilità → Gate G7 (settimana 12, ~8–10 h)

**Obiettivo:** stabilità delle conclusioni sulle **13 celle** di D37: blocco fattoriale {alfabeto-policy × confine} = 6 celle con inferenza completa (S = 10; C0 a S = 20) + blocco OAT {β ∈ {1/|A|, 0.25, 1.0}, d_max ∈ {6, 12}, argmax, guadagno non ristretto} = 7 celle a stima puntuale. Budget ≈ 3–5 ore macchina (confermato dal profiling di G3, O6/D45). **Disciplina di claim (D42):** le 13 celle sono partizionate — (i) blocco di **robustezza parametrica** (C0 + le 7 celle OAT): stabilità di segno **richiesta** per qualunque conclusione sostanziale; (ii) blocco di **analisi di rappresentazione** (le 5 celle fattoriali non-C0: alfabeto × confine): cambiano l'oggetto osservato, quindi gli esiti si **riportano e interpretano**, mai come condizioni automatiche di validità (un effetto presente su ud23 e assente su solo-UPOS localizza la firma nell'informazione di dipendenza: è un risultato, non un fallimento di robustezza); ogni conclusione primaria si riferisce esplicitamente alla rappresentazione primaria; l'instabilità nel blocco (i) è essa stessa un risultato (T4/F10). **Se GATE-A si è attivata a G1 (D50):** C0 resta l'unica primaria; le celle `(ud23, oth)` sono a interpretazione obbligatoria nei Risultati. Il braccio **solo-UPOS** è dentro il blocco fattoriale ed è irrinunciabile (D31).

## FASE 7 — Preprint (settimane 13–15, ~20–25 h)

**Obiettivo:** preprint arXiv cs.CL che regga un linguista computazionale, un teorico dell'informazione e un ingegnere. **Struttura → contenuti (Spec §10):** Introduzione (inquadramento a regimi; domanda = organizzazione predittiva sotto vincolo); Related work nei tre filoni con **differenziazioni obbligatorie** da Galves et al. 2012 e Chen et al. 2024 (D39; erratum E8 sulla novità); Corpus (T1, confondenti §5.8); Metodi (§3–§5, algoritmo §4.1, nota di corrispondenza SG96, **paragrafo di evoluzione del disegno**: consolidamento pre-dati, D32–D36); Risultati (letture descrittive, poi confermativo, poi specificità-tragedia, latino, robustezza; confermativo/esplorativo rigorosamente separati; risultati negativi/instabili riportati); Discussione (cosa autorizza la *sede* della firma: radice / guadagno / transfer; Anderson solo concettuale); Limiti (piano-autore descrittivo senza α, soglia strutturale bilaterale 0,10 — D43; confondenti; **misspecificazione ancorata a Chomsky 1956**: lo strumento è un dispositivo di codifica universale, nessuna pretesa che la lingua sia una sorgente a memoria finita); Sviluppi futuri (proposta §10; confini di verso D11; comparatore CTW). **Fonti:** tutte e sole quelle del Registro bibliografico (appendice qui sotto), dopo la passata di completamento O5. **Touchpoint entrambi i supervisori** prima della sottomissione (D29).

## Checklist di comprensione personale (da spuntare prima del preprint)

Sai spiegare a voce, senza appunti: - [ ] entropia, entropy rate, cross-entropy: cosa misurano e in che unità; - [ ] MDL e Δ(s); perché la codifica prequenziale include il costo del modello; - [ ] come l'albero seleziona la profondità (monotone-stop) e cosa fanno β, k_min, γ, d_max; - [ ] perché la quantità primaria è la CE held-out e non la stima in-sample; - [ ] perché il matching T* è necessario; - [ ] perché la permutazione si fa a documento (exchangeability), perché ogni soglia dichiara la propria lateralità (D43) e perché il piano-autore è descrittivo senza α (soglia strutturale bilaterale di P2 = 0,10); - [ ] perché i punteggi di P2 sono costruiti senza consultare le etichette (validità del test esatto); - [ ] perché il guadagno si calcola solo su posizioni con contesto disponibile ≥ 4; - [ ] la radice e i nodi di profondità 1 come "fette lisciate" delle misure classiche (diagnostica, non risultato); - [ ] perché il sign-flip di P1 richiede la simmetria congiunta dei segni e non solo quella marginale, perché resta una questione aperta (D44/O7) e come lo studio di calibrazione su sintetici la verifica; - [ ] perché il guadagno pooled (P2) non distingue da solo "meno struttura condizionale" da "maggiore distanza dalla miscela" e a cosa serve la lettura descrittiva G_own (D49); - [ ] cosa i risultati NON dimostrano: nessuna causalità metrica; nessuna pretesa di memoria finita del linguaggio (Chomsky 1956 come limite concettuale).

## Le decisioni che definiscono il progetto (sintesi in italiano)

1. **D32 — Strumento unico.** Un solo modello (context tree MDL); le misure di ordine basso sono sue troncature lisciate: diagnostiche, non risultati; la JSD è una lettura distribuzionale descrittiva prevista, senza α né test (D41; era "appendice facoltativa" fino alla v2.0). Deciso da te, pre-dati: nessuna analisi confermativa aveva toccato i dati reali (lo dichiareremo nel preprint).

2. **D21 + D36 — Permutazione a documento e punteggi label-free.** La correzione statistica più importante (documenti, non chunk) più la correzione v2: i punteggi permutati devono essere costruiti alla cieca rispetto alle etichette — la v1 aveva qui un difetto sottile, ora corretto e dichiarato.

3. **D19/D20 — Held-out + T*.** Si inferisce solo su dati mai visti dal modello, a parità di dimensione di training.

4. **D33 — Famiglia {P1, P2}.** Due sole statistiche confermative: transfer e guadagno di contesto. Meno correzione di molteplicità, più potenza; la profondità (S1) è secondaria perché più sensibile ai parametri.

5. **D35 — Restrizione di posizione.** Il guadagno si misura solo dove il contesto è disponibile: la segmentazione in frasi è editoriale e non deve confondere la misura.

6. **D04 — Cinque regimi.** La tragedia come test di specificità (firma dell'esametro o del verso?); prosa classica vs post-classica separate nel greco.

7. **D31 — Braccio solo-UPOS.** I DEPREL sono più rumorosi in poesia: tutto si replica sull'alfabeto dei soli UPOS; con uno strumento unico questo controllo pesa ancora di più.

8. **D06/GATE-A, D18/T5.1.** Soglia d'allerta sugli scarti di annotazione; audit riga-per-riga della corrispondenza con Schürmann & Grassberger.

9. **D42 — Robustezza parametrica vs analisi di rappresentazione.** Le 13 celle di sensibilità non sono tutte uguali: le perturbazioni dei parametri devono confermare il segno; i cambi di rappresentazione (alfabeto, confini) cambiano l'oggetto osservato e si interpretano, non si usano come veto automatico.

10. **D44/O7 — Validità del sign-flip di P1: questione aperta, bloccante.** La costruzione garantisce la simmetria marginale di ΔCE sotto H0, non l'invarianza congiunta richiesta dal sign-flip esatto (i pool di addestramento si sovrappongono → componente di modo comune). Si risolve con uno studio di calibrazione su dati sintetici prima del congelamento del piano; per questo G2 è riposizionato dopo G3 (D44(vii)). Conseguenza pratica: nessuna inferenza confermativa su P1 prima di O7.

11. **D43 + D49–D51 — Sincronizzazione v2.1.** Lateralità dichiarata accanto a ogni soglia e piano-autore descrittivo senza α (D43); lettura descrittiva G_own per la sede della firma (D49); GATE-A non duplica la configurazione primaria (D50); T* calcolato sul solo contrasto primario, con il costo di potenza della taglia uniforme dichiarato (D51).

## Nota strumenti

L'intera analisi gira su un portatile: fit singolo ≈ 1–3 s (da profilare a G3; O6/D45), piano di sensibilità completo ≈ 3–5 ore. Claude Code (app o estensione VS Code) lavora direttamente sul repository mostrando i diff prima di accettarli.

# APPENDICE — REGISTRO BIBLIOGRAFICO COMPLETO (D39)

Tutte le fonti del progetto, in un solo luogo. Legenda stato: **[V]** = verificata in sessione su fonte primaria (con data); **[P]** = fornita dalla proposta con link primario, dettagli da completare; **[S]** = riferimento canonico, dettagli standard da ricontrollare; **[T]** = da verificare. Regola: prima della sottomissione, passata di completamento **O5** su ogni voce non-[V]. Nulla si cita nel preprint se non è in questo registro.

**Nota v2.1 (2026-07-21; D40).** La numerazione della Sezione A è quella della proposta PRE-finale. La proposta finale ha rinumerato la bibliografia in [1]–[22]; corrispondenza verificata sul testo finale il 2026-07-21: registro 1→[1], 2→[6], 3→[18]/[19], 4→[2], 5→[4], 6→[5], 7→[22], 8→[7], 9→[20], 10→[15], 11→[3], 12→[16], 13→[11], 14→[14], 15→[8], 16→[9], 18→[12], 20→[10], 22→[17], 25→[13]. Le voci 17, 19 e 21 del registro non sono citate nella proposta finale (il registro resta il superinsieme delle fonti del preprint). La voce [21] della proposta (Greco et al. 2023) era assente dal registro ed è stata aggiunta come voce 26. La regola resta invariata: nulla si cita nel preprint se non è in questo registro; la passata O5 riverifica anche questa corrispondenza.

## A. Fonti della proposta (numerazione originale della proposta PRE-finale)

1. **Shannon, C. E. (1948).** "A Mathematical Theory of Communication". *Bell System Technical Journal* 27(3): 379–423; 27(4): 623–656. [S] URL della proposta: people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf — Ruolo: quadro fondativo (Introduzione; sorgenti simboliche).

2. **Mansilla, R. & Bush, E. (2003).** "Increase of Complexity from Classical Greek to Latin Poetry". *Complex Systems* 14(3): 201–213. [P — dettagli dalla bibliografia della proposta finale, 2026-07-21; verifica su fonte primaria in O5] URL: content.wolfram.com/sites/13/2023/02/14-3-1.pdf — Ruolo: precedente metrico-prosodico sull'esametro; related work filone (i); differenziazione: alfabeto prosodico vs morfosintattico.

3. **Universal Dependencies** (sito; release **v2.18** e pagine treebank) [V 2026-07-05]. URL: universaldependencies.org — Ruolo: fonte dati e framework.

4. **de Marneffe, M.-C., Manning, C. D., Nivre, J., Zeman, D. (2021).** "Universal Dependencies". *Computational Linguistics* 47(2): 255–308. [S] URL: direct.mit.edu/coli/article/47/2/255/98516 — Ruolo: framework di annotazione (Corpus/Metodi).

5. **Schürmann, T. & Grassberger, P. (1996).** "Entropy estimation of symbol sequences". *Chaos* 6(3): 414–427; arXiv:cond-mat/0203436. [V, sessione di progettazione] — Ruolo: **autorità operativa** del metodo (§4.1; Task T5.1).

6. **Montemurro, M. A. & Zanette, D. H. (2011).** "Universal Entropy of Word Ordering Across Linguistic Families". *PLoS ONE* 6(5): e19875. [S] — Ruolo: related work (i), entropia dell'ordine delle parole (uso di Lempel–Ziv).

7. **Lin, J. (1991).** "Divergence measures based on the Shannon entropy". *IEEE Transactions on Information* *Theory* 37(1): 145–151. [S] — Ruolo: definizione JSD (appendice R1).

8. **Šeļa, A. & Gronas, M. (2022).** "Measuring Rhythm Regularity in Verse: Entropy of Inter-Stress Intervals". In *CHR 2022: Computational Humanities Research Conference*, CEUR Workshop Proceedings Vol-3290, Anversa, pp. 231–242. [P — dalla proposta finale, 2026-07-21; O5] URL: ceur-ws.org/Vol-3290/short_paper5417.pdf — Ruolo: related work (i), regolarità ritmica del verso.

9. **Cover, T. M. & Thomas, J. A. (2006).** *Elements of Information Theory*, 2ª ed., Wiley-Interscience. [S — la proposta finale cita l'edizione 2006; conferma editoriale in O5] — Ruolo: definizioni standard e notazione.

10. **Herrera, S., Silai, I.-M., Guillaume, B., Kahane, S. (2025).** "Extraction of Contrastive Rules from Syntactic Treebanks: A Case Study in Romance Languages". In *Proceedings of the Third Workshop on Quantitative Syntax (QUASY, SyntaxFest 2025)*, ACL, pp. 26–38; ACL Anthology 2025.quasy-1.5. [P — dalla proposta finale, 2026-07-21; O5] — Ruolo: giustificazione delle esclusioni (PUNCT ecc., §3.4).

11. **Anderson, P. W. (1972).** "More Is Different". *Science* 177(4047): 393–396. [S] — Ruolo: ancoraggio concettuale/epistemologico (Introduzione/Discussione); **mai operativo**.

12. **Chomsky, N. (1956).** "Three Models for the Description of Language". *IRE Transactions on Information* *Theory* IT-2(3): 113–124. DOI: 10.1109/TIT.1956.1056813. [V, sessione precedente] — Ruolo: ancoraggio concettuale della **limitazione di misspecificazione** (i modelli markoviani a memoria finita non sono modelli della grammatica; lo strumento è un dispositivo di misura): sezione Limiti (+ eventuale cenno in Introduzione). **Mai** come giustificazione operativa del metodo (quella è la [5] con la letteratura VLMC). Collocazione definitiva: decisione aperta di scrittura, Fase 7.

## B. Fonti aggiunte in fase di progettazione (obbligatorie nel related work; D39)

13. **Galves, A., Galves, C., García, J. E., Garcia, N. L., Leonardi, F. (2012).** "Context tree selection and linguistic rhythm retrieval from written texts". *Annals of Applied Statistics* 6(1): 186–209. DOI: 10.1214/11-AOAS511; arXiv:0902.3619. [V 2026-07-06] — Ruolo: **precedente più vicino** (selezione di modelli VLMC per il ritmo linguistico, portoghese europeo vs brasiliano). Differenziazione obbligatoria: alfabeto ritmico-accentuale vs morfosintattico; identità dialettale vs vincolo formale; nessun transfer predittivo inter-regime.

14. **Chen, S. L., Burns, P. J., Bolt, T. J., Chaudhuri, P., Dexter, J. P. (2024).** "Leveraging Part-of-Speech Tagging for Enhanced Stylometry of Latin Literature". *Proceedings of the 1st Workshop on Machine Learning for Ancient Languages (ML4AL 2024)*, pp. 251–259, ACL. [V 2026-07-06] URL: aclanthology.org/2024.ml4al-1.24/ — Ruolo: dimostra che la **classificazione** prosa/verso da tratti POS in latino è risolta e facile → riposizionamento della novità (erratum E8); il loro limite dichiarato (n-grammi POS a ordine fisso corto) è esattamente ciò che lo strumento adattivo supera; documenta inoltre differenze di convenzioni di annotazione tra treebank (rilevante per D31).

## C. Fondamenti metodologici richiesti dall'architettura v2 (Metodi / related work filone ii)

15. **Rissanen, J. (1983).** "A universal data compression system". *IEEE Transactions on Information Theory* 29(5): 656–664. [V da snippet, 2026-07-06] — origine dell'algoritmo Context e dei modelli a contesti.

16. **Bühlmann, P. & Wyner, A. J. (1999).** "Variable length Markov chains". *Annals of Statistics* 27: 480–513. [V da snippet, 2026-07-06] — quadro statistico VLMC.

17. **Ron, D., Singer, Y., Tishby, N. (1996).** "The Power of Amnesia: Learning Probabilistic Automata with Variable Memory Length". *Machine Learning* 25 (fascicolo/pagine da verificare) [S/T]. — Probabilistic Suffix Trees nel machine learning.

18. **Willems, F. M. J., Shtarkov, Y. M., Tjalkens, T. J. (1995).** "The Context-Tree Weighting Method: Basic Properties". *IEEE Transactions on Information Theory* 41(3): 653–664. [S] — comparatore CTW (robustezza opzionale, D32).

19. **Krichevsky, R. E. & Trofimov, V. K. (1981).** "The Performance of Universal Encoding". *IEEE Transactions* *on Information Theory* 27(2): 199–207 (dettagli da ricontrollare) [S/T]. — stimatore KT (β = 1/2).

20. **Csiszár, I. & Talata, Z. (2006).** "Context tree estimation for not necessarily finite memory processes, via BIC and MDL". *IEEE Transactions on Information Theory* 52: 1007–1016. [V da snippet, 2026-07-06] —consistenza della stima MDL/BIC degli alberi di contesto.

21. **Galves, A. & Löcherbach, E. (2008).** "Stochastic chains with memory of variable length". In *Festschrift for* *Jorma Rissanen*, TICSP Series vol. 38, pp. 117–133; arXiv:0804.2050. [V da snippet, 2026-07-06] — rassegna VLMC.

22. **Holm, S. (1979).** "A simple sequentially rejective multiple test procedure". *Scandinavian Journal of Statistics* 6(2): 65–70 (dettagli da ricontrollare) [S/T]. — correzione di molteplicità (famiglia {P1, P2}).

## D. Risorse dati (da accreditare nel preprint)

23. **UD_Ancient_Greek-Perseus** (`grc_perseus`), UD v2.18 — 13.919 frasi; 202.989 token; conversione UD di G. G. A. Celano da AGLDT 2.1; licenza CC BY-NC-SA 2.5. [V 2026-07-05] Pagina: universaldependencies.org/treebanks/grc_perseus/.

24. **UD_Latin-Perseus** (`la_perseus`), UD v2.18 — 2.273 frasi; 28.868 token / 29.223 parole sintattiche; 355 MWT; stessa provenienza e licenza. [V 2026-07-05] Pagina: universaldependencies.org/treebanks/la_perseus/.

25. **AGLDT 2.1** (Ancient Greek and Latin Dependency Treebank, Perseus) — la risorsa sorgente va accreditata; riferimento canonico: **Bamman, D. & Crane, G. (2011).** "The Ancient Greek and Latin Dependency Treebanks". In C. Sporleder, A. van den Bosch, K. Zervanou (a cura di), *Language Technology for Cultural Heritage*, Springer, Berlino–Heidelberg, pp. 79–98. [P — dettagli dalla bibliografia della proposta finale, 2026-07-21; verifica su fonte primaria in O5]

## E. Aggiunte v2.1 (2026-07-21)

26. **Greco, M., Cometa, A., Artoni, F., Frank, R., Moro, A. (2023).** "False perspectives on human language: Why statistics needs linguistics". *Frontiers in Language Sciences* 2: 1178932. DOI: 10.3389/flang.2023.1178932. [V 2026-07-21 — verificata su fonte primaria presente nei materiali di progetto] — Ruolo: principio di dipendenza-dalla-rappresentazione delle misure statistiche (citata nella proposta finale §2.4: il surprisal acquista contenuto linguistico solo rispetto al modello che definisce eventi e probabilità); pertinente in Metodi (la coppia UPOS+DEPREL come proiezione lineare con perdita) e Limiti. Aggiunta in v2.1 perché citata dalla proposta finale ma assente dal registro.

*Fine del registro. Ogni nuova fonte introdotta nel corso del progetto va aggiunta qui con stato e ruolo, prima di essere citata altrove.*
