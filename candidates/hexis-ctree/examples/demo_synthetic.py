#!/usr/bin/env python3
"""End-to-end demonstration of the HEXIS statistic pipeline on synthetic data.

Two synthetic regimes over the same 6-symbol alphabet:

- PROSE: first-order Markov chain with moderate structure
         (each symbol prefers a successor with p=0.45, others 0.11 each;
         analytical entropy rate ~2.27 bits/token).
- HEX:   noisy cyclic template 'abacad' (noise 0.03, random phase per
         sentence): a strong "formal constraint" whose resolution requires
         context depth 2 (phase after 'a' is ambiguous at depth 1).

The demo runs the full chain: pooled label-free model -> per-document
P2 (gain) and S1 (depth) with the available_past >= 4 restriction ->
document-level label permutation tests; and the P1 transfer matrix with
LODO diagonals. Everything is seeded and deterministic.

This is a VALIDATION artifact only: no claim about the Perseus corpora.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hexis_ctree import (
    Alphabet,
    ContextTreeConfig,
    fit_context_tree,
    per_document_depth,
    per_document_gain,
    permutation_test_label_free,
    pooled_document_scores,
    token_weighted_mean_difference,
    transfer_matrix,
)
from hexis_ctree.synthetic import (
    default_symbols,
    markov_document,
    markov_entropy_rate_bits,
    periodic_template_document,
    template_phase_known_entropy_rate_bits,
)

D = 6
N_DOCS_PER_REGIME = 12
N_SENTENCES = 50
SENTENCE_LENGTH = 16
NOISE = 0.03
N_PERMUTATIONS = 5000
SEED_PERM = 42

PROSE_P = [
    [0.45 if j == (i + 1) % D else 0.11 for j in range(D)] for i in range(D)
]
TEMPLATE = list("abacad")


def build_corpus():
    docs, labels = {}, {}
    for k in range(N_DOCS_PER_REGIME):
        docs[f"prose_{k:02d}"] = markov_document(
            PROSE_P, N_SENTENCES, SENTENCE_LENGTH, seed=1000 + k
        )
        labels[f"prose_{k:02d}"] = "PROSE"
        docs[f"hex_{k:02d}"] = periodic_template_document(
            TEMPLATE, D, N_SENTENCES, SENTENCE_LENGTH, NOISE, seed=2000 + k
        )
        labels[f"hex_{k:02d}"] = "HEX"
    return docs, labels


def main() -> None:
    docs, labels = build_corpus()
    n_tokens = sum(
        len(sent) for doc in docs.values() for sent in doc
    )
    alphabet = Alphabet(default_symbols(D))
    config = ContextTreeConfig()  # beta=1/d, max_depth=8, delta=0, rissanen

    print("=" * 72)
    print("HEXIS context-tree demo on synthetic prose/verse regimes")
    print("=" * 72)
    print(f"alphabet d = {D}; documents = {len(docs)} "
          f"({N_DOCS_PER_REGIME} per regime); tokens = {n_tokens}")
    print(f"config = {config.to_dict()}")
    print()
    print("Ground truth:")
    print(f"  PROSE entropy rate (analytical)        : "
          f"{markov_entropy_rate_bits(PROSE_P):.4f} bits/token")
    print(f"  HEX phase-known entropy rate (lower bd): "
          f"{template_phase_known_entropy_rate_bits(D, NOISE):.4f} bits/token")
    print()

    # ---------------- P2 / S1: pooled, label-free ---------------------- #
    pooled = fit_context_tree(list(docs.values()), alphabet, config)
    print(f"Pooled label-free model: {pooled.node_count()} nodes; "
          f"online h_hat = {pooled.online_entropy_rate:.4f} bits/token")
    scores = pooled_document_scores(pooled, docs)

    gains = per_document_gain(scores)
    depths = per_document_depth(scores)

    def group_mean(stats, group):
        # Spec section 4.4 form: unweighted mean over documents (the
        # document is the unit of inference, per D21).
        values = [s.value for i, s in stats.items() if labels[i] == group]
        return sum(values) / len(values)

    print()
    print("P2 -- context gain (bits), positions with available_past >= 4,")
    print("      unweighted means over documents (spec section 4.4 form):")
    print(f"  HEX   mean gain: {group_mean(gains, 'HEX'):.4f}")
    print(f"  PROSE mean gain: {group_mean(gains, 'PROSE'):.4f}")
    t2, p2 = permutation_test_label_free(
        gains, labels, "HEX", "PROSE",
        n_permutations=N_PERMUTATIONS, seed=SEED_PERM,
    )
    print(f"  T = mean(HEX) - mean(PROSE) = {t2:+.4f}   "
          f"perm. p (two-sided, {N_PERMUTATIONS} perms) = {p2:.4g}")

    print()
    print("S1 -- MDL-selected context depth, positions with available_past >= 4,")
    print("      unweighted means over documents (spec section 4.4 form):")
    print(f"  HEX   mean depth: {group_mean(depths, 'HEX'):.4f}")
    print(f"  PROSE mean depth: {group_mean(depths, 'PROSE'):.4f}")
    t1, p1 = permutation_test_label_free(
        depths, labels, "HEX", "PROSE",
        n_permutations=N_PERMUTATIONS, seed=SEED_PERM,
    )
    print(f"  T = mean(HEX) - mean(PROSE) = {t1:+.4f}   "
          f"perm. p (two-sided, {N_PERMUTATIONS} perms) = {p1:.4g}")

    # ---------------- P1: transfer matrix with LODO -------------------- #
    groups = {
        "HEX": [docs[i] for i in sorted(docs) if labels[i] == "HEX"],
        "PROSE": [docs[i] for i in sorted(docs) if labels[i] == "PROSE"],
    }
    tm = transfer_matrix(groups, alphabet, config, lodo_diagonal=True)
    print()
    print("P1 -- transfer matrix, frozen CE in bits/token")
    print("      (rows = evaluated data, columns = model; diagonal = LODO):")
    names = ["HEX", "PROSE"]
    header = "            " + "".join(f"{n:>12}" for n in names)
    print(header)
    for a in names:
        row = "".join(f"{tm[(a, b)]:>12.4f}" for b in names)
        print(f"  {a:>8}  {row}")
    print()
    print("Transfer asymmetries (off-diagonal minus own LODO diagonal):")
    print(f"  CE(HEX | PROSE-model)  - CE(HEX | HEX-model)    = "
          f"{tm[('HEX', 'PROSE')] - tm[('HEX', 'HEX')]:+.4f} bits/token")
    print(f"  CE(PROSE | HEX-model)  - CE(PROSE | PROSE-model)= "
          f"{tm[('PROSE', 'HEX')] - tm[('PROSE', 'PROSE')]:+.4f} bits/token")
    print()
    print("NOTE: synthetic validation only; statistic definitions to be wired")
    print("against the HEXIS master specification before confirmatory use.")


if __name__ == "__main__":
    main()
