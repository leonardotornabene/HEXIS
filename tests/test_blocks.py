"""Block segmentation tests (Spec §7, gate G0; §3.6; D34 — descriptive F7 only).

Chosen contract (not fixed in §6.2; see docs/HANDOFF.md): ``doc`` is one
document's sentences, each a sequence of symbols; ``make_blocks`` returns a list
of blocks, each a list of whole sentences. Greedy fill to >= n_block tokens; the
trailing partial block is kept iff its token count >= min_frac * n_block. Blocks
never span documents because the pipeline calls make_blocks per document.
"""

import math

import pytest

from hexis.blocks import make_blocks


def _sent(k):
    return list(range(k))


def _tokens(block):
    return sum(len(s) for s in block)


@pytest.mark.g0
def test_sentence_aligned_fill():
    doc = [_sent(400)] * 5  # 2000 tokens in five 400-token sentences
    blocks = make_blocks(doc, n_block=1000, min_frac=0.5)
    assert [_tokens(b) for b in blocks] == [1200, 800]  # greedy overshoot then kept tail
    # each completed (non-final) block reaches n_block, and minimally so:
    assert _tokens(blocks[0]) >= 1000
    assert _tokens(blocks[0][:-1]) < 1000  # dropping its last sentence falls short
    # partition preserves sentence order and content (no tail discarded here):
    assert [s for b in blocks for s in b] == doc


@pytest.mark.g0
def test_tail_kept_iff_at_least_min_frac():
    kept = make_blocks([_sent(1000), _sent(700)], n_block=1000, min_frac=0.5)
    assert [_tokens(b) for b in kept] == [1000, 700]  # tail 700 >= 500 → kept

    dropped = make_blocks([_sent(1000), _sent(300)], n_block=1000, min_frac=0.5)
    assert [_tokens(b) for b in dropped] == [1000]  # tail 300 < 500 → discarded


@pytest.mark.g0
def test_never_spans_documents():
    doc_a = [_sent(300), _sent(300)]  # 600 tokens: one partial block
    doc_b = [_sent(800)]
    per_document = make_blocks(doc_a, n_block=1000) + make_blocks(doc_b, n_block=1000)
    spanning = make_blocks(doc_a + doc_b, n_block=1000)
    # per-document blocking keeps A and B apart; naive concatenation would merge them
    assert [_tokens(b) for b in per_document] == [600, 800]
    assert [_tokens(b) for b in spanning] == [1400]
    assert per_document != spanning
    # every block is a contiguous slice of exactly the sentences passed in
    assert [s for b in make_blocks(doc_a, n_block=1000) for s in b] == doc_a


@pytest.mark.g0
def test_oversized_sentence_is_its_own_block():
    blocks = make_blocks([_sent(1500), _sent(600)], n_block=1000, min_frac=0.5)
    assert [_tokens(b) for b in blocks] == [1500, 600]  # sentences are never split


@pytest.mark.g0
def test_empty_and_all_dropped_documents_produce_no_blocks():
    assert make_blocks([], n_block=1000, min_frac=0.5) == []
    assert make_blocks([[], []], n_block=1000, min_frac=0.5) == []


@pytest.mark.g0
def test_invalid_block_parameters_fail_loud():
    errors = []
    invalid = (
        (0, 0.5),
        (-1, 0.5),
        (1000, -0.1),
        (1000, 1.1),
        (1000, math.nan),
    )
    for n_block, min_frac in invalid:
        with pytest.raises(ValueError) as exc:
            make_blocks([_sent(1)], n_block=n_block, min_frac=min_frac)
        errors.append(exc.value)
    assert all(error.args for error in errors)
