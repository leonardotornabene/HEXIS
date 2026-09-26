# results/hexis31/ — the runs as the pipeline wrote them

Each folder here was written by the pipeline or by a check, and is published byte for byte. Nothing inside was edited afterwards; for this reason the folders have no introduction of their own, and this page describes them. The name `hexis31` comes from HEXIS 3.1, the working title of the plan when the data were produced. The manifests record these paths, so they are kept.

| Folder | What it is | Start with |
|---|---|---|
| [`v1/`](v1/) | the encoded corpus, input of every run: documents, audit tables, sentences as symbol sequences and their coordinates in the source | `documents.csv` |
| [`v3-seed0-v3006/`](v3-seed0-v3006/) | **the final campaign**: 980 models in six analysis settings, their aggregated tables, the five figures and the evidence that the code passed its checks | `seed_summaries.csv` |
| [`v3-seed0-v3006-regeneration/`](v3-seed0-v3006-regeneration/) | the first repetition run a second time, separately: 70 of 70 compared files identical | `manifest.json` |
| [`v3-seed0-v3006-logs/`](v3-seed0-v3006-logs/) | how the campaign was started: checks, first repetition of every setting, regeneration, independent checks | `commands.txt` |
| [`v4-logs/`](v4-logs/) | the verification of the complete campaign | `commands.txt` |
| [`v5-logs/`](v5-logs/) | the report and the final checks; `closure/README.txt` describes its subfolder | `commands.txt` |
| [`v3-005-review/`](v3-005-review/) | the review before the campaign: 18 deliberately broken versions of the code, all caught by the checks | `mutate.log` |

Each run folder opens with its `manifest.json`, which lists every file with its SHA-256. The logs are verbatim: they use the project's internal names, and local paths such as `/Users/…` or `/tmp/…` are those of the author's machine. `v3`, `v4` and `v5` name the phases of the project in which a folder was written. `v3006` names the decision-log entry V3-006, after which the campaign was run.

[`../README.md`](../README.md) describes every published table file by file, and the statement of results reads them. The per-model records, too large for Git, are in the archives of the GitHub Release `hormathos-v5-evidence`; [`../README.md`](../README.md#complete-archives) says how to download and verify them. Once extracted here, their files stay ignored by Git.
