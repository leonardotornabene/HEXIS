"""The G1 ratification checklist and the ratification record must agree.

Unmarked, and deliberately so: this is documentation bookkeeping, not a gate. It
asserts nothing about the science and nothing about G1's software contract, so
adding it to `g1` would only couple the gate to prose — and would oblige the
D55 §xiv convention-13 inventory to name it. It runs in `uv run pytest`, which is
where drift shows up.

It exists because the item numbering was being reconciled by hand across two
files, and hand-reconciliation is exactly what put the superseded
`HEXIS_foglio_ratifica_G1.pdf` out of step with the record beyond item 11 — the
record says so at its head, and warns that a verdict taken on the sheet must be
transcribed by argument and never by number.

The two documents use different shapes on purpose and neither is reformatted to
suit a test: the checklist is a numbered markdown list, the record a table keyed
by number. The checklist parse is scoped to its own section because numbered
lists appear elsewhere in the proposal.
"""

import re
from pathlib import Path

DOCS = Path(__file__).parent.parent / "docs"
PROPOSAL = DOCS / "g1_D55_proposal.md"
RECORD = DOCS / "g1_ratification_record.md"

CHECKLIST_HEADING = "## Decision checklist"


def _checklist_items() -> list[int]:
    """Item numbers from the proposal's checklist section, in document order."""
    text = PROPOSAL.read_text(encoding="utf-8")
    _, _, after = text.partition(CHECKLIST_HEADING)
    assert after, f"{PROPOSAL.name} no longer has a {CHECKLIST_HEADING!r} section"
    section = after.split("\n## ")[0]
    return [int(m.group(1)) for m in re.finditer(r"^(\d+)\. ", section, re.M)]


def _record_items() -> list[int]:
    """Item numbers from the record's decision tables, in document order.

    Scoped above `## Verdetti`: that section is where each verdict is written out
    in full, item number included, so an unscoped parse would eventually read a
    verdict as a second declaration of the item it settles.
    """
    text = RECORD.read_text(encoding="utf-8")
    tables = text.partition("\n## Verdetti")[0]
    return [int(m.group(1)) for m in re.finditer(r"^\|\s*(\d+)\s*\|", tables, re.M)]


def test_the_checklist_and_the_record_number_the_same_items():
    checklist, record = set(_checklist_items()), set(_record_items())

    assert checklist == record, (
        f"only in the D55 checklist: {sorted(checklist - record)}; "
        f"only in the ratification record: {sorted(record - checklist)}"
    )


def test_neither_document_numbers_an_item_twice():
    """A set comparison hides a duplicate, and two rows numbered 17 are exactly
    the drift this file exists to catch."""
    for name, items in (("checklist", _checklist_items()), ("record", _record_items())):
        repeated = sorted({n for n in items if items.count(n) > 1})

        assert not repeated, f"{name} numbers {repeated} more than once"


def test_the_item_numbers_are_a_gapless_run_from_one():
    """A gap means an item was dropped from both files at once, which no
    cross-comparison would see."""
    checklist = set(_checklist_items())

    assert checklist == set(range(1, max(checklist) + 1)), (
        f"missing: {sorted(set(range(1, max(checklist) + 1)) - checklist)}"
    )
