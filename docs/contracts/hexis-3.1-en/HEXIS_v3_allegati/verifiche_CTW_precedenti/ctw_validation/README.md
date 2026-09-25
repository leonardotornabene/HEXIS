> **Non-normative companion translation; the Italian original governs** (V3-003, B2).
> Original: member `ctw_validation/README.md` of `docs/contracts/hexis-3.1/HEXIS_v3_allegati/verifiche_CTW_precedenti.zip` (the same ZIP recurs, identical, inside the other ZIPs of the deposit), SHA-256 of the member `43030800574715b1501a80382c31cada6bd391fd5892218dd46bef3ac8dc5359`. The ZIP is unchanged; this companion mirrors its path with the archive name as a folder.
> Translated on 2026-09-25. Structure and identifiers follow the original; code blocks are reproduced unchanged. Where the original omits the space between a word and a number (e.g. «alfabeto106», «versione3»), the translation restores it. Any translator's note is marked *[Translator's note: …]* and changes nothing in the original.

# CTW checks for HEXIS — 11 September 2026

Verification prototype, separate from the repository. It is not a production patch,
it does not modify the ratified scientific plan and it produces no significance tests.
The external report summarizes the verdict; MATHEMATICAL_CONTRACT.md specifies
formulas, boundaries, frozen prediction and limits of the guarantees.

## Reproduction

Extract the archive into a new directory. `ctw_validation/` and
`corpus_check.json` must be in the same parent directory.
Python verified: 3.12.14. Dependencies: requirements.txt. No GPU.

The purely mathematical and synthetic trials require neither GitHub nor the treebanks:

```bash
python -m venv .venv
.venv/bin/pip install -r ctw_validation/requirements.txt
.venv/bin/python ctw_validation/verify_exact.py
.venv/bin/python ctw_validation/verify_synthetic.py
.venv/bin/python ctw_validation/verify_heterogeneity.py
```

To also reproduce the real pilot an authorized copy of HEXIS is needed in the
sibling directory `HEXIS`, at commit
`852644b6917790877c7b2ca5df2e76b17829d87c`. Clone into a new directory,
without changing an existing working copy. The script reads only config,
proposed registry and PROVENANCE from the copy. It imports no modules of the repository
and does not import the quarantined candidate.

`prepare_data.py` downloads the three UD files at the pinned commit and verifies their hashes.
It does not overwrite pre-existing files and fails if a hash does not coincide.
The original data are distributed by the authors of the treebank under the licence
indicated in the provenance (CC BY-NC-SA 2.5); they are not included in the archive.

```bash
.venv/bin/python ctw_validation/prepare_data.py
.venv/bin/python ctw_validation/verify_pipeline.py
.venv/bin/python ctw_validation/pilot.py --cell C0 --seeds 20
.venv/bin/python ctw_validation/pilot.py --cell a_total1
.venv/bin/python ctw_validation/pilot.py --cell rho09
.venv/bin/python ctw_validation/pilot.py --cell rho_literature
.venv/bin/python ctw_validation/pilot.py --cell q_half
.venv/bin/python ctw_validation/pilot.py --cell D6
.venv/bin/python ctw_validation/pilot.py --cell D12
.venv/bin/python ctw_validation/pilot.py --cell oth
.venv/bin/python ctw_validation/pilot.py --cell upos
.venv/bin/python ctw_validation/pilot.py --cell bound
.venv/bin/python ctw_validation/verify_shuffle.py
.venv/bin/python ctw_validation/benchmark.py
```

The scripts write only results and logs in their own verification directory;
new executions replace the result files of the prototype. Extract a
second copy if you wish to keep the original results for comparison.
Durations and peak memory depend on the computer. The scores must
coincide within the declared numerical error, with data, dependencies and seeds fixed.

## Evidence files

- exact_results.json: complete enumeration, normalization, freezing,
  invariance to the labels of the symbols and to the order of the streams, prequential identity.
- pipeline_results.json: 140 fits on seven synthetic blocks and 20 seeds,
  held-out exclusion, exact budget, adjacency, seeds and separators.
- synthetic_results.json: 61 evaluations, five replicates per small analytical source
  and three per source with alphabet 106. The experiments with different a/rho
  reuse the counts, they do not require new samples.
- pilot_C0.json: 140 real fits, with metadata, times, diagnostics and scores
  of the single blocks; no contrast between groups.
- pilot_*.json: nine sensitivities, seven folds and one seed each.
- ledger_*.json: provenance of the samples for the first seed of each cell.
- heterogeneity_results.json: spurious gain with respect to an interpretation
  as internal dependency, on i.i.d. texts with different marginals.
- shuffle_results.json: control with shuffling within stream/sentence;
  three synthetic seeds and one real pilot on the seven folds. It is not a calibrated
  null distribution nor an inference procedure.
- benchmark_results.json: isolated profiling, unobserved symbols and memory.
- pilot_positions_example.npz: six numerical vectors for one fold, without text.
- completion.json: integrity of the 120 tracked files and summary of the audit.

## Primary methodological source

Kontoyiannis et al., *Bayesian context trees: modelling and exact inference
for discrete time series*, version 3, 2022:
https://arxiv.org/abs/2007.14900v3

Relevant readings: §§2.2–2.3, algorithm 3.1, §3.6, appendix D.
The BOS/SEP handling is an explicit conditional adaptation, proved in the
contract and verified by enumeration; it is not attributed textually
to the article. The PDF of the source is not redistributed in this archive.

## Findings that the new plan must adopt

1. CTW resolves the local veto of the previous selector, not the scarcity of data.
2. With 106 symbols the deep information recovered can remain limited.
3. A gain over a common model is not equivalent to mutual information internal to the
   text: the control on order is needed if a sequential reading is wanted.
4. rho, pseudocount a and depth are distinct choices; the new parameters
   must not be confused with beta/gamma of the old method.
5. The plan will have to ratify boundaries and outputs before the canonical implementation.
