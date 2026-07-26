# Raw data provenance (Spec §2.5, D28)

Raw data is immutable and gitignored; this file is the only committed content of
data/raw/. Acquired 2026-07-26 (Fase 1a, unit P6; acquisition only, no audit, no
model — D45). Values recorded at acquisition time, never reconstructed.

| Field | UD_Ancient_Greek-Perseus | UD_Latin-Perseus |
|---|---|---|
| Repository URL | https://github.com/UniversalDependencies/UD_Ancient_Greek-Perseus | https://github.com/UniversalDependencies/UD_Latin-Perseus |
| UD release tag (pinned, D03) | r2.18 | r2.18 |
| Commit SHA (`git rev-parse HEAD`) | 37837c7a3c592c9563f8c51cc63344b87247f8a5 | a296f012949ef766ffdc5898ded59ffe0a7c3c6a |
| Download date (UTC) | 2026-07-26 | 2026-07-26 |
| Downloaded by | Claude Code (autonomous overnight run, branch phase1a/overnight-2026-07-25) | Claude Code (autonomous overnight run, branch phase1a/overnight-2026-07-25) |

## SHA-256 per `.conllu` file (`shasum -a 256 *.conllu`)

**UD_Ancient_Greek-Perseus** (commit `37837c7a3c592c9563f8c51cc63344b87247f8a5`):

| file | sha256 |
|---|---|
| grc_perseus-ud-dev.conllu | `7899f809fc250404839694330b9db25f79a5b1f20cfa12e6dc3a368a4ec7cd22` |
| grc_perseus-ud-test.conllu | `e18d47c395c0ec8da678fb5e315ce6d90133e88c25ed2a55bc72a2a66e6254d5` |
| grc_perseus-ud-train.conllu | `d7471c9b91bcd975848fa5d9b65c31f1fc48a597ed3667796968a82c6d098a7e` |

**UD_Latin-Perseus** (commit `a296f012949ef766ffdc5898ded59ffe0a7c3c6a`):

| file | sha256 |
|---|---|
| la_perseus-ud-test.conllu | `e0e53fdcc8040a2a6d3b6e7b5dfa69fa35d355ce11cae0682b61e6848745d386` |
| la_perseus-ud-train.conllu | `49d2e3813fc34595fe8cf569f263df4396e4b21aba9429fcdb0eea3ae09e64fa` |

Note (D03): train/dev/test are concatenated and documents re-derived from
`sent_id`/`newdoc` downstream; the UD splits are not analysis splits.

License: CC BY-NC-SA 2.5 (both treebanks); no redistribution (D28).
