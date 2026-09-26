# src/ — the code of the study

`src/hormathos/` is the Python package that produced every published number. It reads the pinned corpus, turns each sentence into a sequence of annotation symbols, trains the prediction models, scores them in the original and in the shuffled order, and writes the tables and figures in [`results/`](../results/README.md). It performs no statistical tests; the plan it implements is in [`docs/contracts/`](../docs/contracts/README.md).

The package sits in `src/` by the usual Python convention, so tests import the installed package and not stray files. This page lives one level up, outside the package, because `src/hormathos/` is frozen with the published runs (see the end of this page).

## How a run flows

| Step | Command (`python -m hormathos.pipeline.…`) | What it does | Output |
|---|---|---|---|
| 1 | `run_audit` | reads the three pinned files of the corpus, checks every annotation and counts the documents | audit tables, in the folder of the encoded corpus |
| 2 | `run_encode` | encodes each sentence as symbols, with its coordinates in the source | the encoded corpus, [`results/hexis31/v1/`](../results/hexis31/README.md) |
| 3 | `run_tree_validation` | runs the prediction model on synthetic cases with known answers and the full test suite, and records both | `tree_validation.json`, `v31_process.json`, `v31.junit.xml` |
| 4 | `run_descriptive` | trains and scores the models of each analysis setting and repetition, and can resume a stopped campaign | one record per train–score pair |
| 5 | `run_report` | checks the campaign is complete and consistent, aggregates it, draws the five figures and compares a separate regeneration of the first repetition | the published tables and figures |

The exact commands of the final campaign are in the logs under [`results/hexis31/`](../results/hexis31/README.md), each in its folder's `commands.txt`.

## Map of the package

| Path | Content |
|---|---|
| `conllu_reader.py` | reads CoNLL-U, the plain-text format of the corpus, and reports errors with their line |
| `alphabet.py` | checks the part-of-speech tags and merges adverbs and particles into one symbol |
| `corpus.py` | census and encoding of the documents into symbol sequences |
| `config.py`, `contracts.py` | load the settings in [`config/`](../config/README.md) and the deposited contracts, and refuse any value that differs from the plan |
| `manifest.py` | file hashes and pinned package versions |
| `model/context_tree.py` | the prediction model: context-tree weighting, which mixes predictions from contexts of every length up to a maximum depth and is frozen after training |
| `model/diagnostics.py` | how much weight the model gives each context length, and the sums used in scoring |
| `protocols/sampling.py` | draws the training sample and the shuffle; every random draw is fixed by the seed |
| `protocols/scores.py` | the losses in bits, the gain G, the order advantage Q and the two ways of averaging |
| `protocols/r1.py` | the descriptive comparison of symbol frequencies between blocks (Jensen–Shannon divergence) |
| `pipeline/` | the five steps above; `corpus_run.py` and `scientific_run.py` give each run its identity and publish it atomically: a run's files appear together or not at all |
| `viz/plots.py` | the five figures, drawn from the verified tables alone |

[`docs/RESULTS.md`](../docs/RESULTS.md#the-question-and-the-measurement) defines every term used here. To read the code, start with `model/context_tree.py`, then `protocols/scores.py`, then `pipeline/run_descriptive.py`. Most modules open with a docstring naming the section of the plan they implement.

## Why the code must not change

Every run records a hash of each `.py` file in `src/hormathos/`, together with the tests, the configuration and the locked dependencies. A published run can be resumed or reported only by the same code. Any change to these files would require a new run in a new folder, and no further run is authorized. The code that produced the published evidence is also fixed by the Git tag `hormathos-v5-evidence`.
