"""Configuration for the MDL context-tree model.

Defaults implement the FROZEN HEXIS primary configuration C0
(Master Spec section 4.1 / section 6.3; Decision Log D18/D37):

    beta = 0.5, k_min = 2, delta_threshold (= gamma) = 0.0, max_depth = 8,
    growth = "eager" (the spec's training pass grows a node on first visit:
    ``node.children.setdefault(sigma, new Node)``), monotone-stop selection.

The alternative preset :meth:`ContextTreeConfig.sg96_published` reproduces
the choices published by Schuermann & Grassberger (1996) as closely as the
paper specifies them; it exists for Task T5.1 (line-by-line correspondence
audit, Decision Log D18) and as sensitivity material. Divergences between
the two presets are itemized in ASSUMPTIONS.md (D18-A1 candidate material).

Provenance of individual parameters
-----------------------------------
- ``beta``: conditional estimator p_hat = (n_a + beta)/(n + beta*d)
  [S&G Eq. (21)]. C0 fixes beta = 0.5 (Krichevsky-Trofimov-style; D18).
  S&G Eq. (30) instead reports beta = 1/d (p_hat = (k + 1/d)/(n + 1)) as
  *numerically* superior on written English -- an empirical finding in the
  source, not a theorem. beta is a declared sensitivity axis (D37:
  beta in {1/|A|, 0.25, 1.0}).
- ``k_min``: minimum training count total(s_i) required at every node
  accepted by the monotone-stop selection (Spec section 4.1; D18: k_min = 2).
  S&G define no such floor; ``k_min = 1`` disables it (any existing node
  has total >= 1), which is the S&G-faithful setting.
- ``delta_threshold``: the spec's gamma, in bits. Selection accepts a node
  s_i iff Delta_spec(s_i) = L_par - L_self > gamma; in this codebase the
  stored ``delta`` is the S&G-oriented L_self - L_par, so the equivalent
  condition is delta < -delta_threshold. gamma = 0 per D18; S&G Sec. V.B
  likewise use a non-negative threshold "chosen differently in different
  applications".
- ``max_depth``: d_max = 8 per D18 (Latin default 6 per D24, set by the
  caller). S&G Sec. VI.B sanction depth-truncated trees as a variant.
  Sensitivity axis (D37: d_max in {6, 12}).
- ``growth``: "eager" reproduces the spec pseudocode (grow on first visit,
  at most one new node per position, depth-capped). "rissanen" implements
  the frugal rule described at the end of S&G Sec. IV (create the single
  new node only when the count of the current symbol at the deepest
  matched node reaches 2). Growth policy affects which nodes *exist*;
  selection (delta_threshold, k_min) decides which are *trusted*.

The ``select = argmax`` variant of D37 (deepest prefix maximizing the
cumulative saving) is NOT implemented yet; it is one sensitivity cell and
is tracked in ASSUMPTIONS.md as pending work.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional

_ALLOWED_GROWTH = ("eager", "rissanen")


@dataclass(frozen=True)
class ContextTreeConfig:
    """Hyperparameters of the context-tree model.

    Attributes
    ----------
    beta:
        Additive smoothing of the conditional estimator
        p_hat(a | context) = (n_a + beta) / (n + beta * d)  [S&G Eq. (21)].
        ``0.5`` (default) is C0 / Krichevsky-Trofimov; ``None`` resolves to
        1/d at model construction [S&G Eq. (30)]; ``1.0`` is Laplace.
    max_depth:
        Hard cap on context length (spec d_max). Contexts never cross
        sentence boundaries regardless of this value.
    delta_threshold:
        The spec's gamma >= 0, in bits. A node is accepted by the selection
        rule only if its accumulated code-length saving vs its parent
        exceeds gamma (stored-delta form: delta < -delta_threshold).
    k_min:
        Minimum training count required at every accepted node
        (spec k_min; 1 disables the floor -- S&G-faithful).
    growth:
        ``"eager"`` (default; spec section 4.1 pseudocode) or ``"rissanen"``
        (S&G Sec. IV frugal rule).
    """

    beta: Optional[float] = 0.5
    max_depth: int = 8
    delta_threshold: float = 0.0
    k_min: int = 2
    growth: str = "eager"

    def __post_init__(self) -> None:
        if self.beta is not None and not (self.beta > 0.0):
            raise ValueError(f"beta must be > 0 or None (got {self.beta!r})")
        if self.max_depth < 1:
            raise ValueError(f"max_depth must be >= 1 (got {self.max_depth!r})")
        if self.delta_threshold < 0.0:
            raise ValueError(
                f"delta_threshold must be >= 0 (got {self.delta_threshold!r})"
            )
        if self.k_min < 1:
            raise ValueError(f"k_min must be >= 1 (got {self.k_min!r})")
        if self.growth not in _ALLOWED_GROWTH:
            raise ValueError(
                f"growth must be one of {_ALLOWED_GROWTH} (got {self.growth!r})"
            )

    # ------------------------------------------------------------------ #
    # Named presets
    # ------------------------------------------------------------------ #
    @classmethod
    def hexis_c0(cls, max_depth: int = 8) -> "ContextTreeConfig":
        """The FROZEN HEXIS primary configuration C0 (D18/D37).

        Identical to the bare defaults; provided as an explicit, greppable
        name for provenance logs. ``max_depth`` is exposed because the Latin
        arm uses d_max = 6 (D24) with the other C0 values unchanged.
        """
        return cls(beta=0.5, max_depth=max_depth, delta_threshold=0.0,
                   k_min=2, growth="eager")

    @classmethod
    def sg96_published(cls, max_depth: int = 8) -> "ContextTreeConfig":
        """Schuermann & Grassberger (1996) published choices (Task T5.1).

        beta = 1/d (Eq. (30)); Rissanen frugal growth (Sec. IV); no count
        floor (k_min = 1); threshold 0. NOTE: S&G do not cap the tree depth
        in Sec. V; the cap is kept here for tractability and is itself a
        divergence to record under T5.1 (S&G Sec. VI.B legitimizes
        truncated trees as upper bounds).
        """
        return cls(beta=None, max_depth=max_depth, delta_threshold=0.0,
                   k_min=1, growth="rissanen")

    def to_dict(self) -> dict:
        """Serializable record of the configuration (for provenance logs)."""
        return asdict(self)
