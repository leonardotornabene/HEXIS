# Inventario test HEXIS 3.1 — V3-001

Accettazione attiva: marker `v31`; raccolta effettiva obbligatoria, assert eseguiti,
nessuno skip/xfail/xpass. Il confronto col contratto non sostituisce test del futuro CTW.

| ID | Stato V0–V1 | Copertura / obbligo residuo |
|---|---|---|
| T01 | V1 | Input/hash, sent_id, 18 prefissi/17 documenti |
| T02 | V1 | Conteggi documento/blocco e intero corpus |
| T03 | V1 | Parsing, coordinate, identità, errori localizzati |
| T04 | V1 | Mapping globale, inventari, C0/UPOS, inventory_only |
| T05 | PENDING V2 | Esclusione held-out e inventory_only dal training |
| T06 | PENDING V2 | Campione q, vuoti, frammenti |
| T07 | PARZIALE V1 | Ordine sorgente; invarianza comportamentale core PENDING V2 |
| T08 | PENDING V2 | RNG/campione/shuffle |
| T09 | PARZIALE V1 | Stream/reset; partizione CTW/BOS PENDING V2 |
| T10 | PENDING V2 | Enumerazione CTW indipendente |
| T11 | PENDING V2 | Normalizzazione/parametri/input del core |
| T12 | PENDING V2 | Identità prequenziale/integrata |
| T13 | PENDING V2 | Modello congelato |
| T14 | PENDING V2 | Log-prior e saturazione |
| T15 | PENDING V2 | 25 sintetici eseguiti sul CTW canonico |
| T16 | PENDING V2 | Stress storico m106 |
| T17 | PENDING V2 | Multinsiemi, slot e provenienza shuffle |
| T18 | PENDING V2 | Eterogeneità e dipendenza |
| T19 | PENDING V2 | Q a quattro termini |
| T20 | PENDING V2 | Aggregazioni/due pesi |
| T21 | PENDING V2 | Sensibilità accoppiate |
| T22 | PENDING V2 | Masse/supporti/L_resolved |
| T23 | PENDING V2 | R1 |
| T24 | PARZIALE V1 | Censimento dei sei inventory_only; assenza training/scoring finale PENDING V5 |
| T25 | PENDING V4 | Uguaglianza 490/980 chiavi modello/coppia |
| T26 | PARZIALE V1 | Atomicità/corruzione corpus; resume modellistico PENDING V2 |
| T27 | PENDING V5 | Ricostruzione score/diagnostiche e figure |
| T28 | V0–V1 | Pipeline senza candidates/inferenza; accettazione senza skip |
| T29 | PARZIALE V1 | Identità/round-trip corpus; CE/riproduzione modelli PENDING V5 |
| T30 | PENDING V5 | Report scientifico completo |

| Suite precedente | Disposizione e motivazione |
|---|---|
| test_conllu_reader.py, test_registry.py, test_g1_registry.py | MANTENUTI: parsing/validazioni generiche; registro attivo verificato da test_v31_corpus/config |
| test_alphabet.py, test_g1_alphabet.py | MANTENUTI storici con configurazione v2.1 esplicita; totalità su tag ignoti/ID per frequenza SOSTITUITI nell'attivo da T03/T04 |
| test_sequences.py, test_g1_sequences.py | MANTENUTI generici/storici; concatenazione SEP RITIRATA nell'attivo; stream e coordinate T03/T09 |
| test_run_audit.py | MANTENUTO sull'audit storico esplicito; gate bilingue, provenance e sidecar v2.1 RITIRATI nell'attivo; difese riusate e testate in T01/T26/T29 |
| test_determinism.py | MANTENUTO hashing/scrittura e RNG storico; RNG scientifico SHA-256 PENDING T08 |
| test_permutation.py, test_bootstrap_holm.py, test_blocks.py | MANTENUTI utility storiche funzionanti, senza import nella pipeline descrittiva |
| test_g0_enforcement.py, test_g1_enforcement.py, test_gate_inventory_anchor.py | MANTENUTI controlli storici; medesimo enforcement esteso a v31 |
| test_docs_consistency.py | MANTENUTO allineamento storia G1 e copie istruzioni |
| test_context_tree.py, test_tree_slices.py, test_scores.py, test_null_calibration.py | Scaffold storico, escluso dall'accettazione v31. Selettore/slices/inferenza RITIRATI; CTW, quattro score e core label-free da SOSTITUIRE con T09–T23 |

Le quattro fixture CTW depositate sono identificate, non eseguite in V0–V1.
I 17 skip storici restano visibili nella suite completa, mai conteggiati come accettazione.

## Evidenze V0–V1 concluse

- `test_v31_config.py`: deposito, proiezione campo/tipo, YAML duplicati, parametri ritirati, isolamento storico.
- `test_v31_corpus.py`: T01–T04, coordinate/ordine numerico/parti, maschere/reset/target, A/B diagnostiche e corruzioni semantiche.
- `test_v31_persistence.py`: integrità dei tre input, snapshot, identità, round-trip, collisioni/concorrenza, interruzione, corruzione e schema del manifest.
- `test_v31_docs.py`: autorità attiva, digest del deposito e delle dieci copie storiche, assenza di import inferenziali/candidates nella pipeline.
- `test_v31_enforcement.py` e `test_gate_inventory_anchor.py`: inventario nominale confrontato con la raccolta effettiva, assert eseguiti, rifiuto di skip/xfail/test vuoti e ancore assenti.

Accettazione sul codice V1 `7afdd3a`: **88 passed, zero skip**. Suite completa: **411 passed, 17 skipped storici**.
Le parti PENDING della tabella restano tali; V0–V1 non promuove T05–T30 integralmente a completati.
