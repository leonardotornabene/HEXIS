# data/ — where the corpus comes from

HORMATHOS studies three files of the Ancient Greek Perseus treebank of Universal Dependencies, release r2.18. The treebank records, for every word, its part of speech and its syntactic relation. This folder records exactly which files those are, so that anyone can fetch the same bytes and the code can refuse any other.

| Path | What it is |
|---|---|
| [`provenance_v31.json`](provenance_v31.json) | the pin that the code reads: repository, release, commit `37837c7…` and the SHA-256 of the three CoNLL-U files. A run stops if any file on disk differs |
| `raw/` | where the corpus is cloned. Git tracks only [`raw/PROVENANCE.md`](raw/PROVENANCE.md), the record of the first acquisition on 26 July 2026 |

## Getting the corpus

The corpus is not stored in this repository: its files stay in `raw/` on your machine, ignored by Git (decision-log entry V3-002). Fetch them from the pinned commit:

```bash
git clone https://github.com/UniversalDependencies/UD_Ancient_Greek-Perseus data/raw/UD_Ancient_Greek-Perseus
git -C data/raw/UD_Ancient_Greek-Perseus checkout 37837c7a3c592c9563f8c51cc63344b87247f8a5
```

The files in `raw/` are never modified, and the code refuses to write any output inside it.

## Reading `raw/PROVENANCE.md`

`PROVENANCE.md` is a record, kept as it was written at acquisition. It also lists a Latin treebank, from an earlier design that compared Greek and Latin. That comparison was retired, and the Latin files enter nothing in the active study. Its references (Spec §2.5, D28, D45) point to documents of that earlier design, now in [`archive/`](../archive/). `provenance_v31.json` records the hash of `PROVENANCE.md`, so the record cannot change unnoticed.

## Licence

The corpus is distributed under CC BY-NC-SA 2.5 by its authors (UD Ancient Greek Perseus and the Ancient Greek Dependency Treebank). Everything derived from it in [`results/`](../results/README.md) keeps that licence; see [Licences](../README.md#licences).
