> **Non-normative companion translation; the Italian original governs** (V3-003, B2).
> Original: `docs/contracts/hexis-3.1/HEXIS_v3_allegati/CHANGELOG_REVIEW_2026-09-12.md`, SHA-256 `0f3ebf4a9c7eb9700b3209bdcfe64a9302d815933e1d8357042338d051561fab`.
> Translated on 2026-09-25. Structure, tables, values and identifiers follow the original; numbers use English notation. Any translator's note is marked *[Translator's note: …]* and changes nothing in the original.

# HEXIS 3.0.1 — Register of the authorized revision

Date: 12 September 2026. Previous version: 3.0, 11 September. The date in the names of the two delivery files keeps that of the initial creation. The revision concerns plan and attachments; no intervention in the repository.

The decisions incorporate the well-founded objections and correct the reviewer's claims that do not turn out to be general. They do not change corpus, CTW, measure Q, JSD, nine cells, seeds or the budget of 1,400 fits. No final contrast was selected or presented.

| Objection | Judgement and decision applied | Operational check |
|---|---|---|
| B1 — Attachments missing for the reviewer | Delivery problem: the historical CTW archive is not the operational package. The current delivery is self-sufficient for text, configuration and contracts; it includes an identical copy of the plan. | README, SHA-256 inventory; old package kept byte for byte in `history/` |
| B2 — Fragments and artificial starts | Well-founded objection. The exact budget with at most one final fragment per contributor is deliberately confirmed; BOS means start of the sampled stream. C5 of the earlier proposals is explicitly superseded, with a declared cost. | §5.2; census of 840 contributions, 671 fragments, 563 internal starts; ablation on seven C0 folds at the first seed, 14 fits; `validate_revision.py` |
| B3 — v2.1 freeze and fits before G2 | Well-founded documentary obligation. V3-001 must record the authorized exception, without simulating a passed G2 or backdating the Git deposit. | §13.1; `authorization_and_experiments.json`; act still to be deposited in the implementation |
| S1 — Bias necessarily against HEX | Real asymmetry, universal direction not demonstrated. A CTW counterexample shows that increasing the share labelled as one's own group can decrease Q or increase it. Q does not guarantee the removal of the confounding. | §5.1; reproducible counterexample; training shares mandatory. The share is collinear with the group and does not identify a causal correction. |
| S2 — Sensitivity to the weights | Accepted. Place side by side in all cells a reaggregation weighted by eligible targets of the variant; the mean of the blocks remains primary. | §8.2-bis and §11.5; configuration, `token_weighted_contrast`, fixtures with unequal weights and decomposition of Q; zero additional fits |
| S3 — G of the shuffled arm null | Null observed in the pilot, not a mathematical identity for every finite i.i.d. sample. The 700 fits of the control and the two components of Q are kept. | §7.4; finite i.i.d. case with non-null G and stopping weight below 1 |
| S4 — Only verbal commitments | Accepted. Analytical contract frozen in V0; implementation/environment in V3; only `run_report` emits contrasts after a complete and verified campaign. | §14.2; `design_lock.json`, `report_contract.py`, tests of omission, duplication, substitution and corruption. The reference does not replace the schemas/manifests/gates of the future pipeline. |
| S5 — Contribution and short contexts | Positive contribution made explicit. Poorly supported deep contexts are already evidence of the pilot, without turning them into the final result. The label is corrected: the historical ranges come from `weighted_depth`, not from the new resolved depth. | §1.1, §2, §9, §16 |
| S6 — Bibliographic precedents | Galves et al. 2012 and Gorman & Gorman 2016 reinserted, with differences of object and method. | §1.1 and §18; links to the primary sources |
| S7 — Statistical utilities | Keep working modules and their tests, excluding their use in the v3 scientific pipeline. Old attestations do not become new gates. | §13.2; no deletion of code performed |
| S8 — NumPy downgrade | Eliminated. Keep `uv.lock`, NumPy 2.5.1 and existing dependencies; empirical comparison of the vectors under both versions. | §15.1; 7 folds/42 contributions per version, equal digests; complete supplementary contract re-run under 2.5.1 |

## Minor clarifications adopted

- Disk estimates distinct for columns and materialization; 12,704,540 paired rows do not become the number of fits.
- 3,360 derivation keys verified by the new contract are not the 1,680 probe evaluations nor the keys of the historical pilot.
- `config/default.yaml` must be replaced entirely in the migration, not adapted by silently letting v2.1 and v3 coexist.
- `scripts/reacquire_raw_data.sh`, reported as untracked by the reviewer, is not available in the copy verified here: it must be preserved and checked in the working copy of the person responsible. Its content is not certified.
- The typo `D=01–D54` is corrected to `D01–D54` and the table of commands realigned: the fits write sums and individual scores; the contrasts are emitted by the report.

## Scope of the checks

The census and the ablation do not prove that the fragments are irrelevant on every seed/cell. The ablation removes the fragment from the same list already chosen, without replacement; it is a development check, not a new cell to be selected on the result. The maximum absolute deviation of Q in the verified pilot is about 0.00068506544 bits/symbol.

The NumPy comparison verifies the contract on this machine, with the same Python. It does not guarantee the universal identity of every transformation of `Generator` or the compatibility of the whole stack. The gates of the future integration remain necessary.

The tests on the report use complete/incomplete synthetic fixtures. They do not attest that the 1,400 final fits were run nor do they produce real V0–V3 certificates. The verification of the bytes of the artifacts is effective; the verification of their scientific semantics and of the slots is prescribed to the integrated pipeline.

The revision closes the decisions of the plan. What remains are explicit implementation activities, with acceptance criteria; not methodological alternatives to be decided after the results.
