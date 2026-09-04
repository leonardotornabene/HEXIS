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
ROOT = DOCS.parent

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


def _checklist_sections() -> dict[int, str]:
    """Item number -> "A" | "B" | "C", from the checklist's own subheadings."""
    text = PROPOSAL.read_text(encoding="utf-8")
    section = text.partition(CHECKLIST_HEADING)[2].split("\n## ")[0]
    return _walk(section, r"^### ([ABC])\.", r"^(\d+)\. ")


def _record_sections() -> dict[int, str]:
    text = RECORD.read_text(encoding="utf-8")
    tables = text.partition("\n## Verdetti")[0]
    return _walk(tables, r"^## ([ABC]) ", r"^\|\s*(\d+)\s*\|")


def _record_statuses() -> dict[int, str]:
    text = RECORD.read_text(encoding="utf-8").partition("\n## Verdetti")[0]
    statuses = {}
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and cells[0].isdigit():
            statuses[int(cells[0])] = cells[3]
    return statuses


def _walk(text: str, heading: str, item: str) -> dict[int, str]:
    current, found = None, {}
    for line in text.splitlines():
        section = re.match(heading, line)
        if section:
            current = section.group(1)
        number = re.match(item, line)
        if number:
            found[int(number.group(1))] = current
    return found


def test_the_two_documents_agree_on_which_section_each_item_is_in():
    """Numbering agreement is not agreement. Item 27 (the Tacitus URN conflict)
    sat in the checklist's section C — "not scientific gates at all" — while the
    record had it in A, blocking the freeze, and the three tests above passed
    throughout: they compare sets of integers, and 27 is in both files either
    way. What the two documents disagreed about was whether a decision blocks
    G1, which is the one thing the pair exists to state.
    """
    checklist, record = _checklist_sections(), _record_sections()

    disagreed = {
        number: (checklist.get(number), record.get(number))
        for number in sorted(set(checklist) | set(record))
        if checklist.get(number) != record.get(number)
    }

    assert not disagreed, f"item -> (checklist section, record section): {disagreed}"


def test_every_item_is_inside_a_lettered_section():
    """A `None` section means an item drifted above the first subheading, where
    the comparison above would call the two documents equal by matching None."""
    for name, sections in (
        ("checklist", _checklist_sections()),
        ("record", _record_sections()),
    ):
        orphaned = sorted(n for n, s in sections.items() if s is None)

        assert not orphaned, f"{name} numbers {orphaned} outside any A/B/C section"


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

    expected = set(range(1, 28))
    assert checklist == expected, (
        f"missing: {sorted(expected - checklist)}; unexpected: {sorted(checklist - expected)}"
    )


def test_only_the_owner_ratified_technical_items_are_closed():
    statuses = _record_statuses()
    technical = set(range(17, 21)) | set(range(23, 27))

    assert {number for number, status in statuses.items() if status == "RATIFICATA"} == technical
    assert {number for number, status in statuses.items() if status == "APERTA"} == (
        set(range(1, 28)) - technical
    )


def test_the_three_standing_instruction_copies_are_identical():
    template_doc = (DOCS / "04_AI_HANDOFF_PROMPT.md").read_text(encoding="utf-8")
    fenced = template_doc.partition("````markdown\n")[2].partition("\n````")[0] + "\n"
    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert fenced == claude
    assert agents.splitlines(keepends=True)[1:] == claude.splitlines(keepends=True)[1:]
