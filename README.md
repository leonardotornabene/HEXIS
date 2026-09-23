# HEXIS 3.1

A descriptive study of within-sentence order in the morphosyntactic annotations of the finite Greek corpus UD Perseus r2.18. The authority is the [deposited plan](docs/contracts/hexis-3.1/HEXIS_piano_definitivo_v3.1_2026-09-15.md) with its byte-identified JSON contracts, adopted by [V3-001](docs/02_DECISION_LOG.md); [V3-002](docs/02_DECISION_LOG.md) realigned the repository and governs its publication.

## Status

**V0–V2 completed; V3–V5 not attested; no real fit has ever been run.** Implemented and verified on synthetic and analytical fixtures: the corpus reader and encoding, the frozen CTW, sampling with the contract RNG and the shuffle, the four losses with G and Q, diagnostics, R1, atomic persistence with resume, the report tables and the five figures. The real corpus has been read and encoded once (V1), and its nine artifacts are reproducible byte for byte. The campaign, the final contrasts and the results belong to V3–V5 and do not exist. Work stops for review before V3.

The active tree holds the 3.1 path only. The history — v2.1, the G0/G1 gates, `candidates/`, the statistical utilities, the previous proposal, the pre-audit results — is preserved byte for byte under `archive/`, at the path it had at `5f1ec06`, with the status of each item declared in [V3-002](docs/02_DECISION_LOG.md); the archive is not an authority and is never executed.

## Usage

```bash
uv sync --frozen
uv run pytest
uv run python -m hexis.pipeline.run_tree_validation --config config/default.yaml
uv run python -m hexis.pipeline.run_audit  --config config/default.yaml --data-root data/raw/UD_Ancient_Greek-Perseus --output-dir results/hexis31/<new>
uv run python -m hexis.pipeline.run_encode --config config/default.yaml --data-root data/raw/UD_Ancient_Greek-Perseus --output-dir results/hexis31/<new>
```

The corpus is not included: `data/raw` is immutable, ignored by Git and never redistributed here. A run's destination must be new; a second launch of the same stage is refused, and no write is implicit. `run_descriptive` and `run_report` are implemented and verified on fixtures: on the deposited configuration they run from V3 onwards, with frozen code.

Active acceptance: `uv run pytest` and `uv run pytest -m v31` collect the same tests, all marked, with no skip and one executed assert each. Verbatim counts are in the [handoff](docs/HANDOFF.md); the map and the obligations are in the [inventory](docs/TEST_INVENTORY.md).

## Scientific scope

Seventeen documents are censused: eleven primary documents in seven blocks, and six inventory-only documents that are never trained on or scored. The alphabet merges ADV and PART globally, in three variants of size 100, 105 and 11. Targets have at least four predecessors in the same sentence, and there is no history across sentences. The measures are out-of-training predictive losses in bits per symbol: no inference, no p-values, no intervals. Seeds are computational replicates, not population uncertainty, and the eleven documents are not eleven independent replicates.

## Licences and data

Licences are set by the publication act in [V3-002](docs/02_DECISION_LOG.md), and nowhere else; [LICENSE](LICENSE) covers the code and refers to the act for documents and data. The raw data are not redistributed by this repository. [Active bibliography](docs/BIBLIOGRAPHY.md).

Python 3.12 via uv, with the lock preserved. The 3.1 research proposal (§17.1) has not been deposited yet. The project documents under `docs/`, including the deposited plan and the Decision Log, are written in Italian.
