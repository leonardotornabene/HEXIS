# HORMATHOS documents — a reading guide (design HEXIS 3.1)

Start from the [README](../README.md). Then, by what you need:

| Document | What it is | Read it if… |
|---|---|---|
| [RESULTS.md](RESULTS.md) | Statement of results and limitations, every number traced to its table | you want the findings and what they do not show |
| [../results/README.md](../results/README.md) | Guide to the published tables, figures, logs and archives | you want the data |
| [Deposited plan 3.1, English](contracts/hexis-3.1-en/HEXIS_piano_definitivo_v3.1_2026-09-15.md) | The research design, fixed before the campaign; the [Italian original](contracts/hexis-3.1/HEXIS_piano_definitivo_v3.1_2026-09-15.md) and its JSON contracts govern, identified by [V3-001-deposit.json](V3-001-deposit.json) | you want to judge the method |
| [02_DECISION_LOG.md](02_DECISION_LOG.md) | Every decision since the design: V3-001 adopts it, V3-002 realigns the repository and sets the licences, V3-003 names the project, V3-004–V3-006 close the reviews, V3-007 publishes the results. V3-001 and V3-002 are in Italian, with [English companions](contracts/hexis-3.1-en/decision-log/) | you want to know why something is as it is |
| [01_MASTER_SPEC.md](01_MASTER_SPEC.md) | One-page statement of authority and perimeter | you are checking what governs what |
| [03_ROADMAP.md](03_ROADMAP.md) | Phases V0–V5 with their commits and status | you want the timeline |
| [HANDOFF.md](HANDOFF.md) | Technical record: runs, commands, checks, reviews, identities, dated newest first | you want to verify or reproduce a step |
| [TEST_INVENTORY.md](TEST_INVENTORY.md) | Map from each obligation of the design to the test that enforces it | you want to know what the tests guarantee |
| [BIBLIOGRAPHY.md](BIBLIOGRAPHY.md) | Active sources | you want the references |
| [04_AI_HANDOFF_PROMPT.md](04_AI_HANDOFF_PROMPT.md) | Standing instructions for the AI coding assistants, copied to `CLAUDE.md` and `AGENTS.md` | you want to see how the assistants were constrained |

The [contracts/](contracts/) folder holds the deposit byte for byte (`hexis-3.1/`, Italian, normative) and its non-normative English companions (`hexis-3.1-en/`, V3-003), each opening with the SHA-256 of its original. The [archive](../archive/) keeps v2.1, G0/G1, `candidates/`, the statistical utilities, the previous proposal and the pre-audit results with the bytes they had at `5f1ec06`: a record, not an executable tree and not a competing authority; the status of each item is in V3-002. The new research proposal (§17.1) has not been deposited yet.
