# docs/contracts/hexis-3.1-en/ — English companions

The deposited plan and two founding decisions are written in Italian, and the Italian text governs. This folder gives English readers a faithful translation of each. The translations are companions only: where they differ from the original, the original is right.

## How the folder is laid out

Each translation sits at the same relative path as its original in [`../hexis-3.1/`](../README.md), so the two can be read side by side. The Italian file names are kept, for example `LEGGIMI.md` ("read me") and `evidenze/` ("evidence"). Only texts are translated: the JSON contracts, scripts and archives are not, since their values and identifiers are the same in every language.

Every translation opens with a short header that gives:

- the path of its original;
- the SHA-256 of the original, so anyone can confirm which bytes were translated;
- the translation date and any conventions, such as English number notation.

Translator's notes are marked *[Translator's note: …]* and change nothing in the original.

## What is here

| Path | Translation of |
|---|---|
| [`HEXIS_piano_definitivo_v3.1_2026-09-15.md`](HEXIS_piano_definitivo_v3.1_2026-09-15.md) | the plan. Start here |
| `HEXIS_allegati_v3.1_2026-09-15/`, `HEXIS_v3_allegati/`, `hexis-verifica/` | the readable texts of the deposit's attachments, previous version and verdict. A text that exists only inside a ZIP archive sits in a folder named after the archive |
| [`decision-log/`](decision-log/) | the decision-log entries V3-001 (adoption of the plan) and V3-002 (realignment of the repository and publication), whose Italian originals are in [`../../02_DECISION_LOG.md`](../../02_DECISION_LOG.md) |
| `check_companions.py`, `pairs_all.json` | the check of the translations: for each original–translation pair listed in `pairs_all.json`, it compares the header hash, the structure (headings, tables, lists) and every number |

To run the check from the repository root:

```bash
uv run python docs/contracts/hexis-3.1-en/check_companions.py . docs/contracts/hexis-3.1-en/pairs_all.json
```
