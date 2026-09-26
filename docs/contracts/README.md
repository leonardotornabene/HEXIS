# docs/contracts/ — the plan fixed before the campaign

This folder holds the research plan of HORMATHOS and its machine-readable contracts, deposited on 15 September 2026, before the final campaign was run. Everything the study measures was defined here first. The code reads its values from these files, and the settings in [`config/`](../../config/README.md) are checked against them. The deposit carries the project's working title of the time, HEXIS 3.1, in its folder and file names. These names are fixed with its bytes.

## Two folders

| Folder | What it is | Authority |
|---|---|---|
| [`hexis-3.1/`](hexis-3.1/) | the deposit, in Italian, byte for byte as delivered | **normative**: it governs |
| [`hexis-3.1-en/`](hexis-3.1-en/README.md) | English translations of its texts and of two Italian decision-log entries | non-normative: the original governs |

The plan's text governs meaning; its JSON files fix values. [`../V3-001-deposit.json`](../V3-001-deposit.json) records the SHA-256 of every deposited file. A test recomputes them all. The pipeline refuses to run if the folder of contracts it reads holds any file more or any file less than its checksums list. For this reason nothing new is ever placed inside `hexis-3.1/`, not even an introduction, and this page describes it from outside.

## Inside the deposit, `hexis-3.1/`

| Path | Content |
|---|---|
| `HEXIS_piano_definitivo_v3.1_2026-09-15.md` | the plan: question, corpus, model, measures, figures, checks. Start here ([English](hexis-3.1-en/HEXIS_piano_definitivo_v3.1_2026-09-15.md)) |
| `HEXIS_allegati_v3.1_2026-09-15/` | the contracts the code reads: the design (documents, blocks, the six analysis settings), the expected corpus counts, the symbol alphabets, the report contract, a lock binding them to the plan, their checksums. `LEGGIMI.md` ("read me") describes them |
| `HEXIS_v3_allegati/` | the attachments of the previous plan version 3.0.1 (11–12 September): its full text, its review, its reference scripts and their validation outputs. `verifiche_CTW_precedenti.zip` holds the earlier checks of the prediction model, which the 3.1 contracts name as executable references. Its `README.md` lists every file |
| `HEXIS_allegati_operativi_v3_2026-09-11.zip` | the same 3.0.1 delivery as one archive, as it was transmitted |
| `hexis-verifica/` | the consolidated verdict of 15 September that turned 3.0.1 into 3.1, with the audits and scripts behind it (`evidenze/`, "evidence") |
| `fixtures/ctw_validation/` | four scripts of those earlier checks, taken from `verifiche_CTW_precedenti.zip`. The tests and the synthetic check of the model use `verify_synthetic.py` to generate cases with known answers |

## Where to go next

- To read the plan, use the [English companion](hexis-3.1-en/HEXIS_piano_definitivo_v3.1_2026-09-15.md).
- For how the plan was adopted and applied, see the [decision log](../02_DECISION_LOG.md), entry V3-001, and its [English companion](hexis-3.1-en/decision-log/V3-001.md).
- For what the plan's measures turned out to be, see the [statement of results](../RESULTS.md).
