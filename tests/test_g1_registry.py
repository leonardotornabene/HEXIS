"""G1 guards on registry field *values* (Spec §2.3, D04).

Marked `g1`, never `g0`: `tests/test_registry.py` carries a module-level `g0`
marker, so anything added there would silently join the attested 144-test G0
selection. Canonical command: `uv run pytest -m g1 --strict-markers`.

`build_registry` checked that the five required fields were *present*, which is
not the same as their carrying content: `author: ""` passed, and `flags: draft`
was coerced by `list()` into five single-character flags nobody wrote. Those
values reach the frozen registry with nothing left to flag them.

`pytest.raises` executes no Python `assert`, and the repo-root conftest fails any
gated test that runs none — hence the `as caught` idiom throughout.

Never delete or weaken a test to make it pass.
"""

import pandas as pd
import pytest

from hexis import registry

pytestmark = pytest.mark.g1

PREFIX_COUNTS = pd.DataFrame(
    [{"language": "grc", "doc_id": "alpha.tb.xml", "n_sentences": 2, "n_tokens_raw": 7}],
    columns=list(registry.PREFIX_COLUMNS),
)

BASE = {
    "author": "Alpha",
    "work": "Alpha Work",
    "regime": "HEX",
    "meter": "hexameter",
    "period": "archaic",
}


def _overrides(**changes):
    return {"alpha.tb.xml": {**BASE, **changes}}


@pytest.mark.parametrize("field", registry.REQUIRED_OVERRIDE_FIELDS)
def test_a_blank_required_field_is_refused(field):
    """Presence is not content: a whitespace-only `author` satisfies the
    missing-fields check and reaches the registry as an empty cell."""
    with pytest.raises(ValueError) as caught:
        registry.build_registry(PREFIX_COUNTS, _overrides(**{field: "   "}))

    assert field in str(caught.value)


def test_a_bare_string_flags_value_is_refused():
    """`list("draft")` is `["d", "r", "a", "f", "t"]` — five flags nobody wrote,
    and each of them would then have to agree across a merge."""
    with pytest.raises(ValueError) as caught:
        registry.build_registry(PREFIX_COUNTS, _overrides(flags="draft"))

    assert "flags" in str(caught.value)


def test_a_non_string_flag_element_is_refused():
    with pytest.raises(ValueError) as caught:
        registry.build_registry(PREFIX_COUNTS, _overrides(flags=["ok", 3]))

    assert "flags" in str(caught.value)


@pytest.mark.parametrize("value", [-1, 1.5, "2", True])
def test_a_part_order_that_cannot_order_parts_is_refused(value):
    """`part_order` is declared-but-unread today, so nothing else would catch a
    value that cannot order anything. `True` is included because
    `isinstance(True, int)` is True in Python."""
    with pytest.raises(ValueError) as caught:
        registry.build_registry(PREFIX_COUNTS, _overrides(part_order=value))

    assert "part_order" in str(caught.value)


def test_a_well_formed_assignment_still_builds():
    """The guards must not reject the shapes the G1 proposal actually uses."""
    frame = registry.build_registry(
        PREFIX_COUNTS, _overrides(flags=["ok"], part_order=0)
    )

    assert list(frame["author"]) == ["Alpha"]
    assert list(frame["flags"]) == [["ok"]]
