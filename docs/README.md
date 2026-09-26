# docs/ — the written record of the study

This folder holds the texts that explain HORMATHOS: what it found, the rules it followed and how every step was done and checked. It holds no data. The published tables, figures and logs are in [`results/`](../results/README.md), and the texts here read them. The rules fixed before the campaign are in [`contracts/`](contracts/README.md).

## What is here

| Kind | Documents | Why they are here |
|---|---|---|
| The findings | [RESULTS.md](RESULTS.md) | the statement of results and limitations. It defines every term and traces every number to a published table |
| The rules | [contracts/](contracts/README.md), [01_MASTER_SPEC.md](01_MASTER_SPEC.md), [02_DECISION_LOG.md](02_DECISION_LOG.md), [V3-001-deposit.json](V3-001-deposit.json) | the research plan deposited before the campaign; the page saying which text governs; every decision taken since the plan, as numbered entries V3-001, V3-002, …; the hashes that identify the deposited files |
| The record | [HANDOFF.md](HANDOFF.md), [03_ROADMAP.md](03_ROADMAP.md), [TEST_INVENTORY.md](TEST_INVENTORY.md) | how each run and check was done, with commands and identities, newest first; the timeline of the phases, with their commits; which test enforces each requirement of the plan |
| The sources | [BIBLIOGRAPHY.md](BIBLIOGRAPHY.md) | the only sources the project may cite |
| The AI instructions | [04_AI_HANDOFF_PROMPT.md](04_AI_HANDOFF_PROMPT.md) | the standing instructions given to the AI coding assistants, copied verbatim to `CLAUDE.md` and `AGENTS.md` at the root |

[00_INDEX.md](00_INDEX.md) gives each document one line and says when to read it. The file names are stable because other documents and the tests link to them. The numbers 00–04 only set the reading order.

## Where to start

- For the findings, read [RESULTS.md](RESULTS.md).
- To judge the method, read the [plan, English companion](contracts/hexis-3.1-en/HEXIS_piano_definitivo_v3.1_2026-09-15.md).
- To see why something is as it is, find its entry in the [decision log](02_DECISION_LOG.md).
- To check a number or a run, use the [handoff](HANDOFF.md).

## Language and fixed texts

Every document is in English, except three texts written in Italian that govern: the deposited plan, and the decision-log entries V3-001 and V3-002. They are never rewritten. Their English companions are in [`contracts/hexis-3.1-en/`](contracts/hexis-3.1-en/README.md). Decisions are never edited once taken: a later entry supersedes an earlier one and says so.

## Not here: `archive/`

The [`archive/`](../archive/) folder holds earlier designs and code, byte for byte as they were at commit `5f1ec06`, before the repository was realigned to the plan. Nothing can be added to it, so it has no introduction of its own. Opening it shows `archive/README.md`, which is the project's old front page from that time, not a guide to the folder. The decision-log entry V3-002 lists what the archive holds and why it is kept.
