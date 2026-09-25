> **Non-normative companion translation; the Italian original governs** (V3-003, B2).
> Original: `docs/contracts/hexis-3.1/HEXIS_v3_allegati/README.md`, SHA-256 `a774f686236cbcaffc0aed77aa6e5279096295ba3b01193b6cec799bdab26343`.
> Translated on 2026-09-25. Structure, tables, values and identifiers follow the original, including file names; code blocks are reproduced unchanged. Numbers use English notation. Any translator's note is marked *[Translator's note: …]* and changes nothing in the original.

# HEXIS 3.0.1 — Attachments to the complete plan

Revision authorized on **12 September 2026**; first delivery 11 September. The date in the external names of the plan and of the archive keeps the first delivery. The plan and this package constitute a target specification: the repository has not been modified and the v3 pipeline is not yet integrated.

Transmit **the whole operational archive**, not only the historical CTW archive. The included plan is identical to the one delivered separately. `SHA256SUMS.json` recursively lists all the other files, excluding itself. The initial version of the attachments is kept without changes in `history/allegati_v3_0_originali.zip` and does not govern the current revision.

## Contents and authority

| File | Role |
|---|---|
| `HEXIS_piano_integrale_v3_2026-09-11.md` | Complete semantic specification, revision 3.0.1 |
| `CHANGELOG_REVIEW_2026-09-12.md` | Outcome and treatment of B1–B3, S1–S8 and minor findings |
| `hexis_v3_design.json` | Structured contract: 9 cells, 7 blocks, 18 prefixes/17 documents, weights and governance |
| `corpus_atteso.json` | Verified counts per document, block and encoding |
| `design_lock.json` | External digests of the plan and of the contract; ready for the V0 deposit, not an attestation that it was passed |
| `authorization_and_experiments.json` | Authorized exception to the old freeze and documented campaigns; Git act still to be deposited |
| `identita_fonti_verificate.json` | Identities and hashes of the documentary sources checked |
| `protocol_contract.py` | Seeds, sampling, shuffling and boundaries |
| `ctw_reference.py` | Separate reference CTW core, unchanged |
| `resolved_diagnostics.py` | Resolved mass and depth of the new diagnostic |
| `score_contract.py` | JSD, primary aggregation and secondary reaggregation by eligible targets |
| `report_contract.py` | Completeness, binding and integrity preconditions for the future report |
| `validate_contract.py` | Configuration, fixtures, optional pilot of 16 real fits/84 probe evaluations |
| `validate_diagnostics.py`, `validate_scores.py`, `validate_report.py` | Additional tests of diagnostics, formulas and rejection of inconsistent campaigns |
| `validate_revision.py` | Census of fragments, ablation and counterexamples S1/S3 |
| `compare_numpy.py` | Reproducible comparison of 7 folds and 42 contributions per NumPy version |
| `contract_validation.json` | Re-execution of the contract under NumPy 2.5.1, 16 real fits/84 probe evaluations |
| `diagnostics_validation.json`, `scores_validation.json`, `report_validation.json` | Actual outcomes of the additional tests; the report manifests are synthetic fixtures |
| `revision_validation.json` | Census, 14 real ablation fits and 9 synthetic counterexample fits |
| `numpy_2_3_5_validation.json`, `numpy_2_5_1_validation.json` | Digests obtained separately from the two versions |
| `numpy_comparison.json` | Comparison of the digests and scope of the check |
| `package_validation.json` | Final consistency, integrity and non-modification of the repository |
| `verifiche_CTW_precedenti.zip` | Historical CTW proofs, including fixtures, ledgers and generators |
| `verdetto_CTW_precedente.md`, `verifica_comparata_precedente.md` | Historical judgements earlier than the v3 specification |
| `history/HEXIS_piano_integrale_v3_0.md` | Initial plan kept, superseded by the current revision |
| `history/allegati_v3_0_originali.zip` | Byte-for-byte copy of the initial package, with the original evidence and configuration |
| `SHA256SUMS.json` | Integrity inventory of the current package |

Correspondence of the historical titles cited in the plan: `HEXIS_verdetto_CTW_2026-09-11.md` is kept here as `verdetto_CTW_precedente.md`; `HEXIS_verifica_comparata_2026-09-11.md` as `verifica_comparata_precedente.md`. The shortened names do not indicate new judgements.

The text governs the semantics and the JSON the values/lists. The executable contracts illustrate the specified operations, but do not implement all the public validations, the application manifests, the certificates, the CLI or the definitive outputs. No module of the future pipeline must import these prototypes as a shortcut to the gates. `report_contract.py` verifies bytes and keys; the pipeline must add checking of the contents, of the slots and of the canonical certificates, and then pass T26/T30.

The historical field `weighted_depth` remains in the prototype and in the evidence for traceability; the v3 scientific diagnostic is that of `resolved_diagnostics.py`.

## Reproducing

Extract into a new folder. Before running, verify the hashes with the standard library:

```bash
python -B - <<'PY'
from pathlib import Path
import hashlib,json
for name,expected in json.loads(Path('SHA256SUMS.json').read_text()).items():
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==expected,name
print('Integrità verificata')
PY
```

*[Translator's note: the script prints «Integrità verificata», "Integrity verified"; the code is reproduced unchanged.]*

Keep this copy of the evidence intact. Run the tests in **a second working copy**, because some commands update their own JSON files:

```bash
python -B validate_contract.py --output rerun_contract
python -B validate_diagnostics.py
python -B validate_scores.py
python -B validate_report.py
```

The contract uses the standard library and NumPy. Python verified: 3.12.14. For the real data acquire the three CoNLL-U files from the commit and the hashes in the contract; `prepare_data.py` and instructions are in the historical CTW archive. The data are not included. Cloning HEXIS is not necessary.

```bash
python -B validate_contract.py --raw-dir raw/UD_Ancient_Greek-Perseus --output rerun_real
python -B validate_revision.py --raw-dir raw/UD_Ancient_Greek-Perseus --output rerun_revision.json
python -B compare_numpy.py --raw-dir raw/UD_Ancient_Greek-Perseus --output rerun_numpy.json
```

`validate_revision.py` compares the ablation with the included `contract_validation.json`: that baseline must contain the seven C0 folds. Its formulas remain the same under both compared versions.

To repeat the comparison between versions explicitly without modifying a project:

```bash
uv run --no-project --with numpy==2.3.5 python -B compare_numpy.py --raw-dir raw/UD_Ancient_Greek-Perseus --output rerun_numpy_2_3_5.json
uv run --no-project --with numpy==2.5.1 python -B compare_numpy.py --raw-dir raw/UD_Ancient_Greek-Perseus --output rerun_numpy_2_5_1.json
```

Compare the fields `ledger_and_shuffle_sha256` and `model_and_scores_sha256`. The environment of the future integration keeps instead the `uv.lock` of the repository, without downgrades or new pins dictated by the prototype. The complete verification of the stack happens in the gates.

## Meaning of the outcomes

PASS concerns the cases executed and the separate contract. It does not certify the future implementation, the 1,400 final fits or a positive scientific result. The ablation has local scope; the synthetic counterexamples refute universal claims, they do not estimate the linguistic bias of the corpus. No real contrast between groups was produced in these new checks. The original research attachments and the files of the repository remain unchanged.
