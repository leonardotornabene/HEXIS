> **Non-normative companion translation; the Italian original governs** (V3-003, B2).
> Original: member `HEXIS_v3_allegati/README.md` of `docs/contracts/hexis-3.1/HEXIS_v3_allegati/history/allegati_v3_0_originali.zip`, SHA-256 of the member `b483f4023a4be07963d0ef5e1c8b39ec3ae217c218dd1c4a3a76e41795542bd7`. The ZIP is unchanged; this companion mirrors its path with the archive name as a folder.
> Translated on 2026-09-25. Structure, tables, values and identifiers follow the original; code blocks are reproduced unchanged. Numbers use English notation. Any translator's note is marked *[Translator's note: …]* and changes nothing in the original.

# HEXIS 3.0 — Attachments to the complete plan of 11 September 2026

These files accompany `HEXIS_piano_integrale_v3_2026-09-11.md`. The plan is complete as a specification; the repository has not been modified. The executable references are separate checks, not an already integrated canonical pipeline.

## Contents and authority

| File | Role |
|---|---|
| `hexis_v3_design.json` | Structured specification: parameters of the 9 cells, 7 blocks, registry of 18 prefixes/17 documents, inputs and cardinalities |
| `corpus_atteso.json` | Verified counts per document, block and encoding; reference of the data gate |
| `identita_fonti_verificate.json` | Metadata and hashes of the four bibliographic sources additionally checked |
| `protocol_contract.py` | Executable contract of seeds, sampling, shuffling and boundaries |
| `ctw_reference.py` | Copy of the already verified CTW core; separate mathematical reference |
| `resolved_diagnostics.py` | Operational definition of the resolved mass and of its depth |
| `score_contract.py` | Minimal references for JSD and descriptive weights |
| `validate_contract.py` | Consistency of the configuration, fixtures and optional pilot on real data |
| `validate_diagnostics.py` | 765 histories and counterexample on the improper cancellation of the root CE |
| `validate_scores.py` | JSD, support with zeros, contributions, weights and four terms of Q |
| `contract_validation.json` | Actual result of the new contract, including 16 real fits and 84 probe evaluations |
| `diagnostics_validation.json`, `scores_validation.json` | Actual results of the other additional checks |
| `verifiche_CTW_precedenti.zip` | Archive already delivered: synthetic sources, enumeration, pre-pilot protocol, ledgers and results |
| `verdetto_CTW_precedente.md`, `verifica_comparata_precedente.md` | Trace of the judgement that precedes the v3 specification |
| `package_validation.json` | Outcome of the final check of cardinalities, operational formulas, sources and integrity of the repository |
| `SHA256SUMS.json` | Hashes of the other components, excluding this inventory itself |

`hexis_v3_design.json` is a target contract and cannot be passed to the old CLI as if it were a compatible configuration. The conversion to the application schema happens in the V0–V2 migration. The reference code does not implement all the type validations, the CLI, the manifests and the final outputs prescribed by the plan.

The historical field `weighted_depth` returned by `ctw_reference.py` remains in the reference results for traceability; it is not the v3 scientific diagnostic. The latter is defined in `resolved_diagnostics.py`. No module of the project must import these files as a shortcut to passing the gates.

## Reproducing the additional checks

Actual environment: Python 3.12.14, NumPy 2.3.5. The additional contract uses only the standard library and NumPy. Do not import modules from a `candidates/` folder.

Extract the package into a new folder, keeping this copy as evidence. In the execution copy:

```bash
python -B validate_contract.py --output rerun_contract
python -B validate_diagnostics.py
python -B validate_scores.py
```

The last two commands write their JSON files in the folder of the script. To avoid overwriting the original evidence, run them only in the working copy.

To repeat the 16 real fits, acquire the three CoNLL-U files from the UD commit and the hashes present in the JSON. The earlier CTW archive includes `prepare_data.py` and the instructions for this acquisition. Pass the directory of the files, for example:

```bash
python -B validate_contract.py --raw-dir raw/UD_Ancient_Greek-Perseus --output rerun_real
```

Cloning HEXIS is not needed for this check. The data are not included in the package. The 14 C0 fits form seven original/shuffled pairs at the first seed of the new convention; one additional pair verifies `bound`. They are not the final 1,400-fit scientific run. The validator does not compute the contrast between groups.

## Interpretation of the outcomes

PASS means that the cases actually executed satisfy the checks. It does not mean universal absence of bugs, already demonstrated correctness of the future implementation or demonstration of a metrical effect. The plan establishes the tests that the integrated code will have to pass. The data, the code of the repository and the original attachments have not been modified.
