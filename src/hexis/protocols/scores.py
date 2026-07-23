"""Score functions and LODO orchestration (Spec §4.2, §4.4; D35, D36, D52).

pooled_score_core is the label-free protocol-(c) boundary. Registry-derived
fields enter only through annotate_scores; pooled_scores remains the public
composition. The G3 byte-identity tests must never be weakened.
"""

import pandas as pd


def delta_ce_scores(registry, sequences, alphabet, cfg, rng) -> pd.DataFrame:
    """ΔCE scores under protocol (b), regime LODO (Spec §4.2, §4.4).

    Rows: doc_id, regime, ce_own(mean,sd), ce_other(mean,sd), dce, n_positions.
    ΔCE needs no position restriction: within-document difference, position
    effects cancel (D35).
    """
    raise NotImplementedError


def pooled_score_core(
    sequences, alphabet, cfg, rng, doc_ids
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Protocol-(c) label-free core returning scores and sampling ledger (D52).

    Model-derived score columns, in order: doc_id, gain_mean, gain_sd,
    depth_mean, depth_sd, frac_restricted, coverage. Ledger columns, in order:
    evaluation_doc_id, seed, training_doc_id, sampled_token_count.
    """
    raise NotImplementedError


def annotate_scores(scores, ledger, registry) -> pd.DataFrame:
    """Attach registry fields and own-regime pool fraction to fixed scores (D52).

    This label-aware stage is outside the byte-identity guarantee.
    """
    raise NotImplementedError


def pooled_scores(registry, sequences, alphabet, cfg, rng) -> pd.DataFrame:
    """Public protocol-(c) scoring contract: label-free core plus annotation.

    The eventual implementation is the thin composition required by D52(v).
    Scoring behavior remains unimplemented in this scaffold.
    """
    raise NotImplementedError


def learning_curves(registry, sequences, alphabet, cfg, rng) -> pd.DataFrame:
    """CE vs training-size grid, descriptive only (Spec §4.2; figure F8).

    Spec §6.2 elides the parameters ("..."); mirrored from the sibling score
    functions pending implementation-time confirmation.
    """
    raise NotImplementedError
