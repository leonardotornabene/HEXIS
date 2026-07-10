"""Slice identities of the fitted tree — test-suite diagnostics, never paper results
(Spec §4.6; D32): root = add-β unigram; depth-1 nodes = smoothed bigram tables;
evaluate-on-train consistency with stored L_self totals.

Interface not specified in Spec §6.2; signatures will be proposed for approval
before implementation — no invented contracts.
"""
