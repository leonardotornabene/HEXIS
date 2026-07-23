"""Rissanen-style MDL context tree, following Schuermann & Grassberger (1996).

Reference
---------
T. Schuermann and P. Grassberger, "Entropy estimation of symbol sequences",
Chaos 6(3):414-427 (1996); arXiv:cond-mat/0203436. Cited below as "S&G".
All equation numbers verified against the arXiv full text.

Correspondence with S&G
-----------------------
1. Conditional probability estimator (S&G Eq. (21)):

       p_hat(a | s^j) = (n_j^(a) + beta) / (n_j + beta * d)

   where s^j is the context of length j, n_j its occurrence count, n_j^(a)
   the count of symbol a after it, d the alphabet size, beta > 0. With
   beta = 1/d this is S&G Eq. (30), p_hat = (k + 1/d)/(n + 1), reported by
   S&G as numerically superior to Laplace's rule on written English.

2. Context selection (S&G Sec. V.B, Eqs. (22)-(24)): each node j > 0 stores

       Delta_j = l(z_j | s^j) - l(z_j | s^(j-1))

   the accumulated (prequential) difference in code length, over the symbols
   z_j that followed context s^j, between coding them at the node itself and
   coding them at its parent. Delta_j < 0 means the longer context has coded
   *those same symbols* more efficiently. Delta is updated incrementally
   during fit, with probabilities evaluated on the counts available *before*
   each update (sequential/prequential MDL), exactly as S&G prescribe
   ("updated recursively while the tree is constructed").

   Selection rule: S&G select the shortest context with Delta_j < -delta
   whose child does not improve (Delta_{j+1} > 0), root otherwise. We
   implement the operationally equivalent *monotone descent*: starting at
   the root, step to the matching child as long as it exists, its
   Delta < -delta_threshold, AND its training count total >= k_min; stop
   otherwise. In the unambiguous cases the two formulations coincide; the
   monotone rule additionally resolves the gap case Delta_{j+1} in
   (-delta, 0], where S&G's literal wording is undefined, by conservatively
   stopping at the parent. This reading is recorded as a proposed Decision
   Log entry (see ASSUMPTIONS.md).

   Correspondence with the HEXIS Master Spec (section 4.1): the spec stores
   Delta_spec(s) = L_par - L_self ("bits saved") and accepts s iff
   Delta_spec(s) > gamma and total(s) >= k_min ("monotone-stop"). The
   ``delta`` stored here is the S&G-oriented L_self - L_par, so
   Delta_spec = -delta and the acceptance condition delta < -delta_threshold
   (with delta_threshold = gamma) is EXACTLY the spec's condition. The
   count floor k_min is applied identically online (pre-update totals) and
   at frozen evaluation (final training totals); k_min = 1 disables it
   (S&G-faithful preset).

3. Tree growth (S&G Sec. IV, "Rissanen's suffix tree"): scanning symbol s_t,
   climb the existing tree along the past s_{t-1}, s_{t-2}, ...; increment
   the count of s_t at every node visited; if the count of s_t at the
   deepest matched node reaches >= 2 (after the increment), create a single
   new child node one symbol deeper, initializing its counts to zero except
   count(s_t) = 1. The ``"eager"`` policy (ablation) creates the child on
   first occurrence instead. Depth is additionally capped at
   ``config.max_depth`` (depth-truncated trees are a variant sanctioned by
   S&G Sec. VI.B).

4. Online entropy-rate estimate (S&G Secs. V.B, V.D): the running average of
   the code length -log2 p_hat(s_t | selected context), with counts as of
   time t (before the update). Convergence caveat (S&G Eq. (28)): at finite
   N the estimate exceeds h and decays only slowly,
   h_hat_N ~ h + c * log(N) / N^gamma; S&G verify this ansatz empirically.
   HEXIS therefore uses the instrument only for *relative comparisons at
   matched N*, never as an absolute entropy-rate estimate.

HEXIS-specific extensions (not in S&G, documented in ASSUMPTIONS.md)
--------------------------------------------------------------------
- Sentence-level hard reset: the context never crosses a sentence boundary;
  no BOS symbol is added to the alphabet; averages run over real tokens only.
- Frozen evaluation mode: S&G define only the online (adaptive) estimator.
  The HEXIS statistics P1 (transfer), P2 (context gain) and S1 (depth)
  require scoring data under a model whose counts and structure are fixed.
  ``score_document`` / ``cross_entropy`` therefore evaluate with frozen
  counts and frozen training-time Delta values: the MDL structure selected
  on the training data determines which contexts are trusted; evaluation is
  pure out-of-sample coding, with no adaptation and no label information.

All code lengths and entropies are in bits (log base 2).
"""

from __future__ import annotations

import math
import pickle
from typing import Dict, Iterable, List, Optional, Sequence

from .alphabet import Alphabet, Document, Sentence
from .config import ContextTreeConfig
from .scores import DocumentScores, SentenceScores

_LOG2 = math.log(2.0)

__version__ = "0.1.0"


class _Node:
    """A context node.

    The node at depth k reached from the root through symbols
    (a_1, ..., a_k) represents the context "previous symbol = a_1,
    symbol before that = a_2, ...": children are keyed by the symbol one
    step further into the past.
    """

    __slots__ = ("counts", "total", "children", "delta", "depth")

    def __init__(self, depth: int):
        self.counts: Dict[int, int] = {}
        self.total: int = 0
        self.children: Dict[int, "_Node"] = {}
        self.delta: float = 0.0
        self.depth: int = depth


class ContextTreeModel:
    """MDL context-tree model over a fixed alphabet.

    Typical HEXIS usage::

        model = ContextTreeModel(alphabet, config)
        model.fit(training_documents)          # online pass, S&G estimator
        h_online = model.online_entropy_rate   # adaptive h_hat (S&G)
        model.freeze()                         # forbid further training
        scores = model.score_document(doc)     # frozen per-position scores
        ce = model.cross_entropy(eval_docs)    # frozen mean code length

    ``fit`` may be called repeatedly before ``freeze`` (incremental
    training); ``online_entropy_rate`` then refers to the pooled pass.
    """

    def __init__(self, alphabet: Alphabet, config: Optional[ContextTreeConfig] = None):
        self.alphabet = alphabet
        self.config = config if config is not None else ContextTreeConfig()
        self.d = len(alphabet)
        # S&G Eq. (30): beta = 1/d unless overridden.
        self.beta = self.config.beta if self.config.beta is not None else 1.0 / self.d
        self._beta_d = self.beta * self.d

        self.root = _Node(depth=0)
        # S&G Sec. V.B initialize the root's Delta to -1 as a sentinel; under
        # the monotone descent rule it is never read, kept for fidelity only.
        self.root.delta = -1.0

        self._frozen = False
        self.n_tokens_trained = 0
        self.n_sentences_trained = 0
        self.n_documents_trained = 0
        self._online_codelen_sum_bits = 0.0

    # ------------------------------------------------------------------ #
    # Elementary quantities
    # ------------------------------------------------------------------ #
    def _log2_prob(self, node: _Node, symbol_id: int) -> float:
        """log2 p_hat(symbol | node context), S&G Eq. (21)."""
        p = (node.counts.get(symbol_id, 0) + self.beta) / (node.total + self._beta_d)
        return math.log(p) / _LOG2

    def _matched_path(self, past: List[int], limit: int) -> List[_Node]:
        """Existing nodes along the past, from the root, up to ``limit`` deep."""
        path = [self.root]
        node = self.root
        depth = 0
        while depth < limit:
            child = node.children.get(past[-1 - depth])
            if child is None:
                break
            path.append(child)
            node = child
            depth += 1
        return path

    def _select_index(self, path: List[_Node]) -> int:
        """Monotone-stop MDL descent (Spec section 4.1; S&G Sec. V.B).

        Step from the root to the next node on the matched path as long as
        that node's Delta < -delta_threshold (spec form:
        Delta_spec = L_par - L_self > gamma) AND its training count
        total >= k_min; return the index (== depth) of the last accepted
        node. Online, totals are pre-update counts; frozen, they are the
        final training counts.
        """
        threshold = -self.config.delta_threshold
        k_min = self.config.k_min
        k = 0
        while k + 1 < len(path):
            nxt = path[k + 1]
            if nxt.delta < threshold and nxt.total >= k_min:
                k += 1
            else:
                break
        return k

    # ------------------------------------------------------------------ #
    # Training (online / adaptive pass, S&G)
    # ------------------------------------------------------------------ #
    def fit(self, documents: Iterable[Document]) -> "ContextTreeModel":
        """Single sequential pass over ``documents`` (S&G online estimator).

        Per position t with symbol s and same-sentence past p (hard reset at
        every sentence boundary):

        1. match the existing path along p (depth <= min(len(p), max_depth));
        2. accumulate the online code length -log2 p_hat(s | selected node),
           with the selection rule applied to the *current* Delta values and
           the probability evaluated on the *current* counts (prequential);
        3. update Delta at every non-root node on the path (S&G Eq. (24),
           incremental form), again with pre-update counts;
        4. increment count(s) at every node on the path;
        5. grow the tree per the configured policy.
        """
        if self._frozen:
            raise RuntimeError("Model is frozen; fit() is no longer allowed.")
        max_depth = self.config.max_depth
        eager = self.config.growth == "eager"

        for doc in documents:
            for sentence in doc:
                ids = self.alphabet.encode_sentence(sentence)
                past: List[int] = []
                for s in ids:
                    limit = min(len(past), max_depth)
                    path = self._matched_path(past, limit)

                    # (2) online code length at the currently selected context
                    sel = self._select_index(path)
                    self._online_codelen_sum_bits += -self._log2_prob(path[sel], s)

                    # (3) prequential Delta updates, pre-update counts:
                    # Delta_j += (-log2 p_child) - (-log2 p_parent)
                    for k in range(1, len(path)):
                        self._Delta_update(path[k - 1], path[k], s)

                    # (4) count updates at every node on the path
                    for node in path:
                        node.counts[s] = node.counts.get(s, 0) + 1
                        node.total += 1

                    # (5) growth: extend the path by at most one node
                    deepest = path[-1]
                    matched_depth = len(path) - 1
                    if matched_depth < limit and (
                        eager or deepest.counts[s] >= 2
                    ):
                        child = _Node(depth=matched_depth + 1)
                        child.counts[s] = 1
                        child.total = 1
                        deepest.children[past[-1 - matched_depth]] = child

                    past.append(s)
                    self.n_tokens_trained += 1
                self.n_sentences_trained += 1
            self.n_documents_trained += 1
        return self

    def _Delta_update(self, parent: _Node, child: _Node, s: int) -> None:
        child.delta += self._log2_prob(parent, s) - self._log2_prob(child, s)

    @property
    def online_entropy_rate(self) -> float:
        """Adaptive h_hat in bits/token (S&G online estimator over the fit pass).

        Finite-N caveat (S&G Eq. (28)): converges to h slowly from above;
        use only for relative comparisons at matched N.
        """
        if self.n_tokens_trained == 0:
            raise RuntimeError("Model has not been fitted.")
        return self._online_codelen_sum_bits / self.n_tokens_trained

    def freeze(self) -> "ContextTreeModel":
        """Mark the model immutable (blocks further fit); scoring is unaffected."""
        self._frozen = True
        return self

    @property
    def frozen(self) -> bool:
        return self._frozen

    # ------------------------------------------------------------------ #
    # Frozen evaluation (HEXIS extension; pure, never mutates the model)
    # ------------------------------------------------------------------ #
    def score_sentence(self, sentence: Sentence) -> SentenceScores:
        """Frozen per-position scores for one sentence.

        For each position i (0-based; available_past = i):
        descend through existing children gated by the *training-time* Delta
        values and counts (same monotone-stop rule as in fit, structure
        frozen), evaluate -log2 p_hat at the selected node and at the root
        with frozen counts. The record carries (codelen_selected,
        codelen_root, depth_selected, depth_matched, available_past) per
        position, as required by Spec section 4.3 for coverage statistics.
        """
        ids = self.alphabet.encode_sentence(sentence)
        max_depth = self.config.max_depth
        codelen: List[float] = []
        root_codelen: List[float] = []
        depth: List[int] = []
        matched: List[int] = []
        avail: List[int] = []
        past: List[int] = []
        for i, s in enumerate(ids):
            limit = min(i, max_depth)
            path = self._matched_path(past, limit)
            k = self._select_index(path)
            node = path[k]
            codelen.append(-self._log2_prob(node, s))
            root_codelen.append(-self._log2_prob(self.root, s))
            depth.append(node.depth)
            matched.append(len(path) - 1)
            avail.append(i)
            past.append(s)
        return SentenceScores(
            codelen_bits=tuple(codelen),
            root_codelen_bits=tuple(root_codelen),
            selected_depth=tuple(depth),
            matched_depth=tuple(matched),
            available_past=tuple(avail),
        )

    def score_document(self, document: Document) -> DocumentScores:
        return DocumentScores(
            sentences=tuple(self.score_sentence(s) for s in document)
        )

    def cross_entropy(self, documents: Iterable[Document]) -> float:
        """Frozen mean code length (bits/token) over all real-token positions.

        This is the P1 ingredient: CE(data | this model). Averaged over real
        tokens only; sentence-initial tokens are coded at the root.
        """
        total = 0.0
        n = 0
        for doc in documents:
            for sentence in doc:
                s_scores = self.score_sentence(sentence)
                total += sum(s_scores.codelen_bits)
                n += len(s_scores)
        if n == 0:
            raise ValueError("No positions to evaluate.")
        return total / n

    # ------------------------------------------------------------------ #
    # Diagnostics and persistence
    # ------------------------------------------------------------------ #
    def node_count(self) -> int:
        stack = [self.root]
        n = 0
        while stack:
            node = stack.pop()
            n += 1
            stack.extend(node.children.values())
        return n

    def summary(self) -> dict:
        return {
            "package_version": __version__,
            "alphabet_size": self.d,
            "beta": self.beta,
            "config": self.config.to_dict(),
            "n_documents_trained": self.n_documents_trained,
            "n_sentences_trained": self.n_sentences_trained,
            "n_tokens_trained": self.n_tokens_trained,
            "node_count": self.node_count(),
            "online_entropy_rate_bits": (
                self.online_entropy_rate if self.n_tokens_trained else None
            ),
            "frozen": self._frozen,
        }

    def save(self, path: str) -> None:
        """Persist model + provenance metadata (pickle)."""
        with open(path, "wb") as f:
            pickle.dump({"summary": self.summary(), "model": self}, f)

    @staticmethod
    def load(path: str) -> "ContextTreeModel":
        with open(path, "rb") as f:
            payload = pickle.load(f)
        return payload["model"]
