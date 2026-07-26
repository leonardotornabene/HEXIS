"""Block segmentation — descriptive only (Spec §3.6; D34: no inference, figure F7 only)."""


def make_blocks(doc, n_block: int = 1000, min_frac: float = 0.5):
    """Sentence-aligned greedy fill; blocks never span documents (Spec §3.6).

    ``doc`` is one document's sentences, each a sequence of symbols. Whole
    sentences accumulate into the current block until it reaches ``n_block``
    tokens; the trailing partial block is kept iff it holds >= ``min_frac *
    n_block`` tokens, else discarded. Sentences are never split, so a completed
    block may overshoot ``n_block`` by up to its last sentence. Called per
    document by the pipeline, so blocks never span documents.

    Serves only the descriptive within-document CE profile figure F7 (D34):
    no block-level tests, no block permutation, no chunk-size sensitivity axis.
    """
    blocks = []
    current = []
    count = 0
    for sent in doc:
        current.append(sent)
        count += len(sent)
        if count >= n_block:
            blocks.append(current)
            current = []
            count = 0
    if current and count >= min_frac * n_block:
        blocks.append(current)
    return blocks
