# config/ — the settings of the plan

The two files here hold, in YAML, the choices of the deposited plan that the code needs at run time. They add no choice of their own. On loading, the code checks every value against the contracts in [`docs/contracts/`](../docs/contracts/README.md) and stops at the first difference, so these files cannot silently depart from the plan.

| File | What it holds |
|---|---|
| [`default.yaml`](default.yaml) | the whole plan as the code uses it: which part-of-speech tags are kept, dropped or merged, the rules of random draws, the six analysis settings (`cells`), the blocks and documents, the sampling, shuffle and model, the two ways of averaging and the expected corpus counts. Every run passes it with `--config` |
| [`registry_overrides.yaml`](registry_overrides.yaml) | the registry of documents alone, which every run reads and hashes as a separate input: for each of the 18 source files, its document, author, work, hexameter or prose, block and role. Eleven documents in seven blocks are scored, one of them from two source files; six are only counted |

Both files record `spec_version: HEXIS-3.1` because the plan was deposited under that working title. The name `registry_overrides.yaml` is kept because the code and the run records use it.

## Where to go next

- For why each value is what it is, see the [plan](../docs/contracts/hexis-3.1-en/HEXIS_piano_definitivo_v3.1_2026-09-15.md).
- For what the settings mean in plain words, see [the statement of results](../docs/RESULTS.md#the-question-and-the-measurement).

## Why these files must not change

Each run records the hash of its configuration and of the registry. The runs published in [`results/`](../results/README.md) can be checked, resumed or reported only with these exact bytes.
