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
from conllu import TokenList

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
    # Without this the `regime` case is vacuous: a whitespace-only regime is
    # already refused by the pre-existing label check, whose message names the
    # field too, so the parametrisation passed with the blank guard deleted.
    assert "blank" in str(caught.value)


@pytest.mark.parametrize("value", ["", "   ", 42, None])
def test_a_blank_source_urn_is_refused(value):
    """`source_urn` is published in the registry and carries the work's identity —
    it is the field the unresolved Tacitus conflict lives in (checklist item 27).
    Its value was never checked at all: only its *presence* on a merge was."""
    with pytest.raises(ValueError) as caught:
        registry.build_registry(PREFIX_COUNTS, _overrides(source_urn=value))

    assert "source_urn" in str(caught.value)


def test_a_sent_id_repeated_in_the_stream_is_refused():
    """`read_tokens` refuses a repeated `sent_id`; `enumerate_prefixes` performs
    the same per-document aggregation from the same sentence stream and let it
    inflate `n_sentences` and `n_tokens_raw` — the guard belonged in both."""
    sentences = [
        TokenList([{"id": 1, "form": "x"}], {"sent_id": "alpha.tb.xml@1"}),
        TokenList([{"id": 1, "form": "x"}], {"sent_id": "alpha.tb.xml@1"}),
    ]

    with pytest.raises(ValueError) as caught:
        registry.enumerate_prefixes(sentences, language="grc")

    assert "occurs twice" in str(caught.value)


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
    `isinstance(True, int)` is True in Python; `-1` because the owner ruled on
    2026-09-04 that the shape stays non-negative until something reads it."""
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
