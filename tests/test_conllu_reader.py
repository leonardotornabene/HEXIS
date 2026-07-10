"""CoNLL-U reader tests (Spec §7, gate G0; §3.2).

Fase 0 placeholders: cases enumerated per Spec §7, no assertions yet.
Never delete or weaken a test to make it pass.
"""

import pytest

SKIP = pytest.mark.skip(reason="Fase 0 scaffold — implement at gate G0 per Spec §7")


@SKIP
def test_malformed_row_raises_with_location():
    """Malformed row → parse error carrying file, sent_id, token id (§3.2)."""


@SKIP
def test_sent_id_required():
    """sent_id mandatory — fail loudly if absent (§3.2)."""


@SKIP
def test_id_order_preserved():
    """Surface order = CoNLL-U ID order (§3.2)."""
