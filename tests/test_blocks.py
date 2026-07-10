"""Block segmentation tests (Spec §7, gate G0; §3.6; D34 — descriptive F7 only).

Fase 0 placeholders: cases enumerated per Spec §7, no assertions yet.
Never delete or weaken a test to make it pass.
"""

import pytest

SKIP = pytest.mark.skip(reason="Fase 0 scaffold — implement at gate G0 per Spec §7")


@SKIP
def test_sentence_aligned_fill():
    """Sentence-aligned greedy fill to n_block (§3.6)."""


@SKIP
def test_tail_min_frac():
    """Tail block kept iff ≥ min_frac, else discarded (§3.6)."""


@SKIP
def test_never_spans_documents():
    """Blocks never span documents (§3.6)."""
