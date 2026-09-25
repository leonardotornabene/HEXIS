V5 closure aids, 25 September 2026 (local record, Git-ignored, not deposited).
Copied from /tmp/hormathos-v5-review and /tmp/hormathos-v5-baseline.json with
timestamps preserved (cp -p). Read-only checks; none of them fits a model or
writes into the campaign directories.

reconstruct.py / reconstruct.log  frozen report functions rerun on the published
                                  partitions into /tmp: 13 tables and 5 figures
                                  byte-identical (outputs not kept: identical to
                                  results/hexis31/v3-seed0-v3006).
dossier.py                        editorial selection of the numerical tables.
section.md                        snapshot of the phase-2 numerical dossier.
check_dossier.py, docs-tests.log  first-review checks (1,987 fields, 19 tables).
baseline-hashes.json              preparation baseline of the tracked tree.
final/                            closure: 01-pytest.log (431 passed), all.txt and
                                  v31.txt (identical collections), hashes.py,
                                  check_dossier_final.py.
visual/                           render.py, render2.py and the 2,400 px PNG
                                  previews used for the figure review.
Scripts expect the repository root as the working directory and the /tmp paths
they name; they are kept as evidence of what was run.
