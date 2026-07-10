"""Block segmentation — descriptive only (Spec §3.6; D34: no inference, figure F7 only)."""


def make_blocks(doc, n_block: int = 1000, min_frac: float = 0.5):
    """Sentence-aligned greedy fill; blocks never span documents (Spec §3.6).

    Serves only the descriptive within-document CE profile figure F7 (D34):
    no block-level tests, no block permutation, no chunk-size sensitivity axis.
    """
    raise NotImplementedError
