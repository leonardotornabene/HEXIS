"""Score functions and LODO orchestration (Spec §4.2, §4.4; D35, D36).

pooled_scores must never consult regime labels (D36); the byte-identical
label-invariance test (Spec §7) guards this and must never be weakened.
"""

import pandas as pd


def delta_ce_scores(registry, sequences, alphabet, cfg, rng) -> pd.DataFrame:
    """ΔCE scores under protocol (b), regime LODO (Spec §4.2, §4.4).

    Rows: doc_id, regime, ce_own(mean,sd), ce_other(mean,sd), dce, n_positions.
    ΔCE needs no position restriction: within-document difference, position
    effects cancel (D35).
    """
    raise NotImplementedError


def pooled_scores(registry, sequences, alphabet, cfg, rng) -> pd.DataFrame:
    """Gain/depth scores under protocol (c), pooled LODO — LABEL-FREE (D36).

    Rows: doc_id, regime, gain_mean(mean,sd), depth_mean(mean,sd),
    frac_restricted, coverage. Primary gain/depth restricted to positions with
    available_past ≥ 4 (D35). Regime labels must never be consulted (D36).
    """
    raise NotImplementedError


def learning_curves(registry, sequences, alphabet, cfg, rng) -> pd.DataFrame:
    """CE vs training-size grid, descriptive only (Spec §4.2; figure F8).

    Spec §6.2 elides the parameters ("..."); mirrored from the sibling score
    functions pending implementation-time confirmation.
    """
    raise NotImplementedError
