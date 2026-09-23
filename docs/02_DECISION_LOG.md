# Decision Log attivo — HEXIS 3.1

## V3-001 — Adozione della v3.1 e prima tranche V0–V1

**Data del deposito: 2026-09-16. Stato: ADOTTATA per le nuove esecuzioni.** Fonte di autorizzazione: richiesta dell'utente nella sessione corrente di implementare il piano definitivo V0–V1. Non si attribuiscono a questa richiesta autorizzazioni pregresse o attività V2–V5.

Il [piano v3.1](contracts/hexis-3.1/HEXIS_piano_definitivo_v3.1_2026-09-15.md) e i contratti depositati costituiscono l'unica autorità attiva. Il [record esterno](V3-001-deposit.json) identifica tutti i byte; gli stati originari `FINAL_PLAN_NOT_APPLIED` e `V0_deposit: null` nei materiali restano intatti e descrivono la consegna precedente. L'atto presente ne adotta il contenuto senza modificare ciò che i digest identificano. Il commit di deposito sarà riferito dal manifest successivo, senza autoriferimento.

Per la v3.1 sono **non applicabili**: inferenza P1/P2, latino, O7 come blocco operativo, costanti permutazionali, G0–G7 e relativo ordine, sensitività precedenti, sign-stability, selettore Rissanen/penalità, sequenze con SEP/#, chunk e modelli di riferimento. Sono sostituiti dai §§3–14 della v3.1: greco, sette blocchi, CTW congelato, due bracci, sei celle, target j≥4, RNG SHA-256, checklist V0–V5. Non si dichiara O7 risolto né G2 superato nel progetto v2.1.

Restano: bit/log base 2, test prima del codice, controlli rigorosi e determinismo, raw immutabili, nessun import da candidates, core senza etichette/annotazione separata, nessuna nuova dipendenza o fonte bibliografica implicita. Le nuove soglie A/B sono diagnostiche. I 17 skip storici non costituiscono accettazione attiva: gli obblighi futuri sono esplicitamente PENDING nell'[inventario](TEST_INVENTORY.md).

Storia epistemica: sono stati osservati pilot reali; questo è un protocollo prospettico dopo sviluppo, non una preregistrazione antecedente ai dati. La copertura verificata e i limiti sono nel §2 del piano e nel verdetto depositato. Il resoconto `contracts/hexis-3.1/HEXIS_v3_allegati/authorization_and_experiments.json` è fonte delle autorizzazioni pregresse **con la verificabilità lì dichiarata**: non è un consenso originale indipendentemente verificato; non si ricostruiscono date/orari mancanti. I 25 esiti sintetici archiviati sono evidenze storiche, non accettazione del futuro CTW canonico. Nessun nuovo fit reale è autorizzato da questa tranche.

D01–D54 sono conservate integralmente qui sotto. [D55](g1_D55_proposal.md) resta PROPOSED, applicata a nulla nella v2.1; le [ratifiche tecniche G1](g1_ratification_record.md) conservano esattamente gli stati originari. Il proposal PDF e README di backup sono storici; la riscrittura del proposal e la pubblicazione rimangono separate.

---

## V3-001 — Nota di esecuzione V2, 2026-09-17

La richiesta corrente dell'utente autorizza la ripresa e il completamento del piano
V2 sul ramo `codex/hexis31-v0-v1`, con revisione integrale successiva e arresto prima
di V3. Questa fonte è distinta dalla richiesta V0–V1 del deposito: non le si
attribuiscono retroattivamente nuove autorizzazioni. Nessun fit reale, pubblicazione
o cambiamento dei byte normativi è incluso nella ripresa.

Il §11.1 è applicato conservando i nomi pubblici `pooled_score_core` e
`annotate_scores` con API per gli slot accoppiati e per l'annotazione del registro.
Le firme a cinque/tre argomenti del protocollo v2.1 sono sostituite, insieme ai
relativi attesi di firma; resta verificato il vincolo valido di indipendenza dalle
etichette, ora anche comportamentalmente. Questo adeguamento tecnico attua
V3-001 e non ratifica G0/D52 retroattivamente. Evidenze e limite V3–V5
nell'[handoff](HANDOFF.md) e nell'[inventario](TEST_INVENTORY.md).

---

## V3-001 — Nota di esecuzione pre-V3, 2026-09-22

La revisione integrale chiesta dall'utente prima di V3 ha ricevuto quattro decisioni esplicite
(D1–D4, [handoff](HANDOFF.md)). Qui si registra la sola deviazione dal testo del contratto.

**CLI (§14.1).** Le righe del §14.1 sono comandi di principio. Gli entry point implementati
richiedono in più destinazioni esplicite: `--data-root`/`--output-dir` per audit e codifica;
`--corpus-dir`/`--output-dir` per `run_descriptive`, `run_report` e per la pubblicazione delle
evidenze con `run_tree_validation`; `--regenerated-dir` per il report scientifico (§12.2). Accettano
inoltre `--seed 0`, `--resume` e `--fixture`. Motivo: il §11.7 vieta sovrascritture implicite e
richiede pubblicazione atomica in una destinazione nuova o in una ripresa verificata, quindi nessuna
destinazione è dedotta. Nessun parametro scientifico passa dalla CLI: celle, semi e pesi restano
quelli della proiezione depositata. Nessuna clausola, atteso o byte contrattuale è modificato.

---

## V3-002 — Riallineamento della repository e atto di pubblicazione, 2026-09-22

**Stato: ADOTTATA; esecuzione in corso sul ramo `codex/hexis31-realign`.** Fonte di autorizzazione: richiesta dell'utente del 22 settembre 2026 di allineare integralmente la repository al piano v3.1 prima della code review e di V3, con le decisioni E1–E8 e N1–N4 riportate sotto. L'atto non modifica alcun byte del deposito né i tre blocchi V3-001 sopra, che restano gli atti del 16, 17 e 22 settembre. Base: `5f1ec06afa192c8d0f006d7f39cdb97df72c2983`. Storia v2.1 già pubblica: `852644b6917790877c7b2ca5df2e76b17829d87c`. I tag annotati `archive/pre-realign` e `archive/v2.1` puntano a questi due commit; le ancore normative sono gli SHA, non i nomi dei tag.

**Archivio (§13.1 p.4–5, §17.3).** Tutto ciò che non appartiene al percorso 3.1 esce dall'albero attivo ed entra in `archive/`, con questa regola: il file che a `5f1ec06` stava in `P` sta ora in `archive/P`, con gli stessi byte. `archive/` non viene importato, non viene raccolto da pytest, non entra nell'identità del codice (`src/hexis`) né nel contesto delle evidenze V2 (`tests/*.py`). È un registro, non un albero eseguibile: ogni voce si esegue a `5f1ec06`, dove il suo codice è vivo. Due test attivi lo vincolano: nessun suo file è raccolto, nemmeno da `pytest .`, e ogni suo file ha il blob che aveva alla base. Stato delle voci:

| Voce | Posizione | Stato |
|---|---|---|
| D01–D54, specifica, roadmap, handoff e istruzioni v2.1 | `archive/docs/history/v2.1/` | FROZEN per la v2.1; nessuna autorità per nuove esecuzioni; byte verificati dal loro `SHA256SUMS.json` |
| D55 | `archive/docs/g1_D55_proposal.md` | PROPOSED, applicata a nulla |
| Ratifiche tecniche G1 e proposta di registro | `archive/docs/g1_*` | Stati originari; non ratificano il corpus né l'analisi 3.1 |
| `candidates/` | `archive/candidates/` | In quarantena (D47); nessun import |
| Utility statistiche e loro test (§13.2) | `archive/src/hexis/stats/`, `archive/tests/` | Storiche, funzionanti a `5f1ec06`; nessun import nella pipeline |
| Registro, sequenze, blocchi, lessico v2.1, `legacy_audit`, cinque stadi ritirati | `archive/src/hexis/…` | Ritirati; sostituiti da `corpus.py`, `sampling.py`, `corpus_run.py`, `run_descriptive.py` |
| Test v2.1, G0, G1 e scaffold, compresi i 17 skip | `archive/tests/` | Storici; destinazione di ogni test nella mappa di [TEST_INVENTORY](TEST_INVENTORY.md) |
| Proposal PDF v2, README di backup, PDF v2.0, audit, piani di implementazione | `archive/` | Superati; il proposal 3.1 (§17.1) resta da scrivere |
| Tabelle e log pre-audit G1 | `archive/results/` | Non canonici; già pubblici dal push di `852644b` |
| Configurazione v2.1 | `archive/config/history/v2.1/` | Storica |
| Handoff, inventario e registro di riconciliazione a `5f1ec06` | `archive/docs/` | Resoconto dettagliato V0–V2 citato dalle note V3-001 |
| README a `5f1ec06` | `archive/README.md` | Storico; lo stato delle voci è in questa tabella |

**Supersessioni puntuali di V3-001 (i suoi byte non cambiano).** «D01–D54 sono conservate integralmente qui sotto» va letto come conservate integralmente in `archive/docs/history/v2.1/02_DECISION_LOG.md`, che è byte per byte l'appendice tolta da questo log. I link a `g1_D55_proposal.md`, `g1_ratification_record.md`, e le note V3-001 sulle evidenze in HANDOFF e nell'inventario, si risolvono con la regola `archive/P`. «I 17 skip storici…» ora ha un esito: gli skip sono archiviati con i loro file, e nessun test attivo è skip. «Nessun import da candidates» resta in vigore. «Qui si registra la sola deviazione dal testo del contratto», nella nota pre-V3, va letto insieme alle deviazioni 4 e 5 sotto.

**Deviazioni dichiarate.**
1. **§13.2, percorsi.** La mappa indica `registry.py`, `sequences.py` e `stats/` come sedi del lavoro. Le funzioni 3.1 corrispondenti vivono da V1–V2 in `corpus.py` e `sampling.py`. Le utility statistiche sono conservate come storiche in archivio invece che in `src/hexis/stats/`, e i loro test non si eseguono nell'albero attivo.
2. **Codice v2.1 nei moduli vivi.** Vengono rimossi:
   - in `alphabet.py`: gli ID per frequenza, l'inventario, il freeze e l'audit A/B v2.1, la colonna `available_past` di `map_tokens` (quella 3.1 è in `coordinates`);
   - in `config.py`: il loader, il merge e le forme G1 v2.1, `config_hash`, e `derive_seed` basato su CRC32 (il contratto usa SHA-256);
   - in `scores.py`: i tre stub e l'alias `score_streams`, perché il nome del contratto è `pooled_score_core` (§11.1);
   - in `manifest.py`: il writer del manifest e dei sidecar v2.1.

   Gli stadi ritirati non esistono più: è un vincolo più forte del rifiuto di eseguirli (§13.2, «ritirare CLI»). `check_output_locations`, `staged_inputs` e `verify_inputs_unchanged`, con le loro dipendenze `_conllu_paths` e `CANONICAL_DATA_ROOT`, passano da `legacy_audit` a `corpus_run`. Il confronto con `ast.dump` dà identici `check_output_locations`, `staged_inputs` e `_conllu_paths`, con due differenze dichiarate. Il messaggio di rifiuto di `verify_inputs_unchanged` cita il §11.7 al posto di «§6.4, D46», riferimento ritirato; logica, condizioni e tipo d'eccezione sono invariati. `CANONICAL_DATA_ROOT` è la radice `data/raw` della repository e non più un percorso relativo alla directory corrente (code review del 23 settembre), e il controllo equivalente che `check_destination` ripeteva è tolto.
3. **Freeze pre-V3.** Il congelamento dichiarato il 22 settembre copriva `src/hexis`, i test, `conftest.py`, `pyproject.toml`, la configurazione e il lock. Viene riaperto qui, prima di qualunque pubblicazione V2 o V3: sotto `results/hexis31/` esistono solo i run V1. L'attestazione di `0dc69b5` (351 v31; 672 passed più 17 skip) resta prova di quel commit. L'accettazione V2 si riattesta sul commit del riallineamento. Il corpus `results/hexis31/v1` resta il corpus di V3: la sua identità è per contenuto, `validate_run` non vincola il codice, e il riallineamento deve riprodurne byte per byte i nove artefatti. Configurazione, lock, deposito e raw restano invariati.
4. **§11.2, ledger.** Il piano nomina un `sample_ledger.json` che contiene anche q. Il ledger è pubblicato come un file per campione distinto, `sample_ledger__<sha256>.json`, citato per hash da ogni coppia che lo usa; q sta nel record della coppia e si ricava esattamente dalle righe, come somma di `end − start` per contributore. Un file unico andrebbe riscritto a ogni coppia pubblicata, mentre il §11.7 vuole immutabili gli artefatti pubblicati.
5. **§9.1, picco RSS.** Il `peak_rss` di ogni modello è il massimo raggiunto dal processo fino a quel modello (`resource.getrusage(RUSAGE_SELF).ru_maxrss`), non il picco del modello isolato: in una campagna sequenziale è un limite superiore. Ogni record lo dichiara in `rss_method`.

Le deviazioni 4 e 5 sono attuate da V2 e finora erano descritte soltanto nell'handoff, nell'inventario e nel registro di riconciliazione ora in `archive/docs/`, che non sono un'autorità.

**Deposito.** Il commit V0 `e98fb8e` aveva depositato 64 file, tra cui `hexis-verifica/.DS_Store` (6.148 byte, sha256 `18cc90e9ff3e6473b1790a06f5bbf5afb3be60f5359284118c94b4f8383df96b`, contenente soltanto i nomi dei file della cartella). Non compariva nel `SHA256SUMS.json` del pacchetto. Il commit V1 `7afdd3a` lo ha rimosso insieme alla sua riga nel record, senza documentarlo. Lo si registra qui. I 63 digest restanti sono invariati.

**Decisioni del proprietario del 22 settembre 2026 (D1–D4, già in HANDOFF).**
- D1: nessun push pubblico senza un atto di pubblicazione. È superata dall'atto sotto, che diventa efficace solo al push.
- D2: il validatore rigenera ledger, conteggi di shuffle e provenienza C0.
- D3: la deviazione della CLI è registrata nella nota V3-001.
- D4: le figure sono state corrette.

D2–D4 restano attuate da `0dc69b5`.

**Atto di pubblicazione (§17.3).**
- *Perimetro.* Tutti gli oggetti raggiungibili dal ramo e dai tag pubblicati che non sono già su `origin`: la storia successiva a `852644b`, non soltanto l'albero finale. Quanto sta fino a `852644b` compreso è pubblico dal push di `g1/pre-audit`.
- *Codice e configurazione* (`src/`, `tests/`, `conftest.py`, `pyproject.toml`, `uv.lock`, `config/`, e il codice e la configurazione conservati sotto `archive/`): licenza MIT, [LICENSE](../LICENSE), che in testa rinvia a questo atto per tutto ciò che non è codice.
- *Documenti e deposito contrattuale*: i documenti del progetto, compresi quelli sotto `archive/` e i PDF; i metadati `data/provenance_v31.json` e `data/raw/PROVENANCE.md`; il deposito contrattuale come un'unica opera — testi, JSON, script e archivi ZIP — pubblicato byte per byte come depositato: **CC BY 4.0**, con attribuzione a Leonardo Tornabene. Sono opera dell'autore e devono restare citabili in revisione. La licenza del codice non si estende né ai documenti né ai dati.
- *Derivati del corpus UD Ancient Greek Perseus r2.18* (CC BY-NC-SA 2.5):
  - (a) **simboli per posizione:** `ctw_validation/pilot_positions_example.npz`, sha256 `738f0ccbe395a562cd47435f984474d6c2206dcac7757a38eb4b0c5575e89fec`, con 46.634 posizioni del pilot storico (`loss`, `root_loss`, `weighted_depth`, `matched_depth`, `unseen_weight`, `past`);
  - (b) **coordinate:** i 70 `ctw_validation/ledger_<cella>_B<k>.json`, con `sent_id` e intervalli dei campioni dei pilot, e le citazioni puntuali di `sent_id` in `hexis-verifica/evidenze/corpus_audit.json` e `audit_corpus.md`;
  - (c) **aggregati:** risultati dei pilot, conteggi, inventari e alfabeti dei contratti, conteggi fissati nei test, tabelle pre-audit G1 in `archive/results/`.

  I file (a) e (b) stanno in `HEXIS_v3_allegati/verifiche_CTW_precedenti.zip`, sha256 `85fce2a6462fd741b2cc5616aa85863ef4c25235a84b463da1e6c6e6e35f6198` (in `V3-001-deposit.json`). Lo stesso ZIP compare altre tre volte, identico, dentro gli ZIP del deposito. Il digest di ciascun file è in `ctw_validation/FILE_HASHES.json`, cioè fra i 103 digest interni verificati da V3-001 e ricontrollati il 22 settembre. Licenza dei derivati del corpus, categorie (a), (b) e (c): **CC BY-NC-SA 2.5**, la stessa della fonte, con attribuzione a UD Ancient Greek Perseus r2.18 al commit `37837c7a3c592c9563f8c51cc63344b87247f8a5` e ad AGDT/Perseus. Non è una scelta fra licenze possibili: ShareAlike impone a un adattamento la licenza della fonte e NonCommercial vieta l'uso che una licenza permissiva concederebbe, quindi dichiarare MIT su questi file sarebbe una promessa che l'autore non è in condizione di mantenere.
- *Precedenza per porzioni.* Un derivato del corpus conserva CC BY-NC-SA 2.5 anche dentro un file di un'altra categoria: inventari e alfabeti nei JSON del contratto, conteggi fissati nei test, file (a) e (b) dentro gli ZIP del deposito. Quelle porzioni seguono la licenza del corpus; il resto del file segue la propria. Nessun byte è sotto due licenze.
- *Clausola residua.* Ogni file del perimetro non nominato sopra, nell'albero o nella storia, segue la categoria della sua natura: codice o configurazione MIT, documento o metadato CC BY 4.0, derivato del corpus CC BY-NC-SA 2.5.
- *Non pubblicati:* i raw (`data/raw` resta ignorato; `PROVENANCE.md` contiene soltanto hash e metadati d'acquisizione) e i run locali `results/hexis31/`.
- *Portata nel tempo:* l'atto copre soltanto ciò che esiste oggi. I vettori per posizione di C0 della campagna V4–V5, quando esisteranno, non sono compresi e richiedono un atto proprio.
- *Efficacia:* al primo push; dopo la pubblicazione non si ritira. La verifica con la sede editoriale prevista qui non ha destinatario: al 23 settembre 2026 la sede non è determinabile e la destinazione probabile è un archivio di preprint. Si pubblica quindi senza sede. I derivati del corpus restano in questo repository, o in un suo deposito con DOI, sotto la loro licenza; un testo futuro li cita per link e non li include fra i propri file. La licenza di quel testo è una decisione futura (*Portata nel tempo*).

**Decisioni.**
- E1: il deposito resta intatto.
- E2: licenze decise il 22 settembre 2026 — MIT per il codice, CC BY 4.0 per i documenti dell'autore, CC BY-NC-SA 2.5 per i derivati del corpus. Precedenza per porzioni, clausola residua e nota d'ambito in LICENSE decise il 23 settembre 2026, dopo la code review.
- E3: pubblicazione di tutto, per nome.
- E4: il PDF v2 va in archivio senza sostituto.
- E5: il ramo remoto `g1/pre-audit` si cancella dopo il merge, verificata l'ascendenza.
- E6: l'appendice D01–D54 esce dal log.
- E7: handoff e inventario sono riscritti come stato attuale.
- E8: ogni test raccolto è v31.
- E9: pubblicazione senza sede editoriale determinata (23 settembre 2026); i derivati del corpus si citano per link.
- N1: il workspace di verifica sta fuori dalla repository.
- N2: differenziale di copertura con la sola libreria standard.
- N3: una riga-guardia sugli elementi ritirati nelle istruzioni.
- N4: regola `archive/P`.
- Resta tracciato `data/raw/PROVENANCE.md`.
- Il merge in master avverrà con merge commit, senza squash o rebase.
