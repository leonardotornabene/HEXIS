"""CTW: frozen Bayesian mixture over context trees (piano §6.1–§6.5, §11.1).

Counts and Dirichlet(a) evidence on every observed context up to depth D, a BOS
arc closing a history shorter than D, one integrated weight per node, and a
prediction that mixes every admissible tree. There is no k_min, gamma, pruning,
argmax or monotone selection: the instrument averages over models, it does not
select one (§6.1).

Evidences and weights are natural logs (§6.5); `evaluate` reports bits. The two
mixture weights always come from delta = u - v, never one from `1 - other`;
forced leaves (depth D, or below BOS) get stop=1 by construction rather than by
a float that could saturate.
"""

import hashlib
import math
from dataclasses import dataclass

import numpy as np

BOS = -1  # context-only symbol; never an outcome (design representation.bos_context_only)


def _is_int(value) -> bool:
    return isinstance(value, (int, np.integer)) and not isinstance(value, bool)


def _is_real(value) -> bool:
    return _is_int(value) or isinstance(value, (float, np.floating))


@dataclass(frozen=True)
class CTWParams:
    """Frozen CTW parameters: alphabet, depth, Dirichlet mass and the two log priors."""

    m: int
    depth: int
    a: float
    log_rho: float
    log_one_minus_rho: float

    def __post_init__(self):
        if not _is_int(self.m) or self.m < 2:
            raise ValueError(f'm={self.m!r}: alphabet size must be an int >= 2')
        if not _is_int(self.depth) or self.depth < 0:
            raise ValueError(f'depth={self.depth!r}: must be an int >= 0')
        if not _is_real(self.a) or not math.isfinite(self.a) or self.a <= 0.0:
            raise ValueError(f'a={self.a!r}: Dirichlet mass per symbol must be finite and > 0')
        for name, value in (('log_rho', self.log_rho), ('log_one_minus_rho', self.log_one_minus_rho)):
            if not _is_real(value) or not math.isfinite(value) or value >= 0.0:
                raise ValueError(f'{name}={value!r}: stop/split log-prior must be finite and < 0')

    @classmethod
    def from_rho(cls, m, depth, a, rho):
        """Interior stop prior rho; both log contributions are kept separately (§6.5)."""
        if not _is_real(rho) or not math.isfinite(rho) or not 0.0 < rho < 1.0:
            raise ValueError(f'rho={rho!r}: stop prior must be interior to (0, 1)')
        return cls(m=m, depth=depth, a=a, log_rho=math.log(rho), log_one_minus_rho=math.log1p(-rho))

    @classmethod
    def from_log_split_prior(cls, m, depth, a, log_one_minus_rho):
        """Extreme priors stay in logs: 1 - 2**-(m-1) is exactly 1.0 in float64 (§6.5)."""
        if not _is_real(log_one_minus_rho) or not math.isfinite(log_one_minus_rho) or log_one_minus_rho >= 0.0:
            raise ValueError(f'log_one_minus_rho={log_one_minus_rho!r}: split log-prior must be finite and < 0')
        return cls(m=m, depth=depth, a=a, log_one_minus_rho=log_one_minus_rho,
                   log_rho=math.log1p(-math.exp(log_one_minus_rho)))


@dataclass(frozen=True)
class Mixture:
    """§9.2 decomposition of one prediction: lambda per observed node, plus the unseen mass.

    `weights` holds (lexical_context_length, lambda) in path order; BOS is not a
    lexical arc, so a BOS leaf repeats the length of its parent. `unseen_mass` is
    the mass routed to the first never-observed branch.
    """

    weights: tuple
    unseen_mass: float
    unseen_branch_encountered: bool


@dataclass(frozen=True)
class EvalResult:
    """Frozen-model evaluation: mean code lengths in bits per scored target (§8.1)."""

    n: int
    ce: float
    root_ce: float


class _Node:
    __slots__ = ('counts', 'total', 'children', 'forced',
                 'log_e', 'log_w', 'log_stop', 'log_split', 'delta')

    def __init__(self, forced: bool):
        self.counts = {}
        self.total = 0
        self.children = {}
        self.forced = forced
        self.log_e = 0.0
        self.log_w = 0.0
        self.log_stop = 0.0
        self.log_split = -math.inf
        self.delta = None


class CTW:
    """Fit once on integer streams, then predict and evaluate without mutation."""

    def __init__(self, params: CTWParams):
        if not isinstance(params, CTWParams):
            raise ValueError(f'params={params!r}: CTWParams required')
        self.params = params
        self._root = _Node(forced=params.depth == 0)
        self._fitted = False

    @property
    def fitted(self) -> bool:
        return self._fitted

    @property
    def log_evidence(self) -> float:
        """log W at the root, in nats: the integrated evidence of the mixture (§6.3)."""
        self._require_fitted()
        return self._root.log_w

    def fit(self, streams) -> 'CTW':
        """Count every context up to D (BOS closes short histories), then freeze the weights."""
        if self._fitted:
            raise ValueError('model is frozen: fit() runs once per CTW')
        depth, root = self.params.depth, self._root
        for index, stream in enumerate(streams):
            symbols = self._validated(stream, f'stream {index}')
            for position, target in enumerate(symbols):
                node = root
                node.counts[target] = node.counts.get(target, 0) + 1
                node.total += 1
                for step in range(depth):
                    back = position - step - 1
                    symbol = symbols[back] if back >= 0 else BOS
                    child = node.children.get(symbol)
                    if child is None:
                        child = node.children[symbol] = _Node(forced=symbol == BOS or step + 1 == depth)
                    child.counts[target] = child.counts.get(target, 0) + 1
                    child.total += 1
                    node = child
                    if symbol == BOS:  # BOS is terminal: nothing is counted below it (§6.2)
                        break
        self._freeze()
        self._fitted = True
        return self

    def predict_proba(self, history) -> np.ndarray:
        """Normalized q_CTW over the alphabet for the given history; the model is untouched."""
        path, unseen, _ = self._mixture(self._history(history))
        m, a = self.params.m, self.params.a
        ma = m * a
        q = np.full(m, unseen / m)
        for node, weight, _ in path:
            scale = weight / (node.total + ma)
            q += a * scale
            for symbol, count in node.counts.items():
                q[symbol] += count * scale
        return q

    def mixture(self, history) -> Mixture:
        """The §9.2 weights behind `predict_proba` for the same history."""
        path, unseen, encountered = self._mixture(self._history(history))
        return Mixture(weights=tuple((lexical, weight) for _, weight, lexical in path),
                       unseen_mass=unseen, unseen_branch_encountered=encountered)

    def evaluate(self, streams, *, min_available_past) -> EvalResult:
        """Mean CTW and root code lengths in bits over targets with enough past (§8.1)."""
        if not _is_int(min_available_past) or min_available_past < 0:
            raise ValueError(f'min_available_past={min_available_past!r}: must be an int >= 0')
        self._require_fitted()
        root, depth = self._root, self.params.depth
        m, a = self.params.m, self.params.a
        ma = m * a
        uniform = 1.0 / m
        # ponytail: one mixture per distinct context, rebuilt per call so nothing
        # is cached across models; drop the memo if evaluation ever needs per-node output.
        memo = {}
        ctw_bits = root_bits = 0.0
        n = 0
        for index, stream in enumerate(streams):
            symbols = self._validated(stream, f'stream {index}')
            for position in range(min_available_past, len(symbols)):
                target = symbols[position]
                key = tuple(symbols[max(0, position - depth):position]) if depth else ()
                resolved = memo.get(key)
                if resolved is None:
                    path, unseen, _ = self._mixture(key)
                    resolved = memo[key] = ([(node.counts, node.total, weight) for node, weight, _ in path],
                                            unseen)
                path, unseen = resolved
                q = unseen * uniform
                for counts, total, weight in path:
                    q += weight * (counts.get(target, 0) + a) / (total + ma)
                ctw_bits -= math.log2(q)
                root_bits -= math.log2((root.counts.get(target, 0) + a) / (root.total + ma))
                n += 1
        if n == 0:
            raise ValueError(f'evaluate: no target with min_available_past={min_available_past}')
        return EvalResult(n=n, ce=ctw_bits / n, root_ce=root_bits / n)

    def root_distribution(self) -> np.ndarray:
        """q_0(x) = (n(x) + a) / (N + ma) on the same global counts (§6.4)."""
        self._require_fitted()
        mass = self.params.m * self.params.a + self._root.total
        q = np.full(self.params.m, self.params.a / mass)
        for symbol, count in self._root.counts.items():
            q[symbol] += count / mass
        return q

    def diagnostics(self) -> dict:
        """Supports and the §6.5 root record, under the report-contract names; delta in nats (u - v)."""
        self._require_fitted()
        root = self._root
        by_depth, histograms, level = [], [], [root]
        while level:
            by_depth.append(sum(1 for node in level if node.total))  # §9.1: observed nodes only
            histogram = dict.fromkeys(('1', '2to4', '5to9', '10plus'), 0)
            for node in level:
                if node.total:
                    bucket = ('1' if node.total == 1 else '2to4' if node.total < 5
                              else '5to9' if node.total < 10 else '10plus')
                    histogram[bucket] += 1
            histograms.append(histogram)
            level = [child for node in level for child in node.children.values()]
        return {'nodes': sum(by_depth), 'node_count_by_structural_depth': by_depth,
                'support_histogram_1_2to4_5to9_10plus_by_depth': histograms,
                'root_observed_symbol_count': len(root.counts),
                'root_unseen_symbol_count': self.params.m - len(root.counts),
                'root_stop': math.exp(root.log_stop), 'delta_root_nats_stop_minus_split': root.delta,
                'delta_root_reason': 'forced_leaf' if root.forced else None,
                'log_evidence': root.log_w}

    def inspect(self, context) -> dict | None:
        """One node by context (most recent symbol first, BOS only as the last arc)."""
        self._require_fitted()
        node = self._root
        for symbol in context:
            node = node.children.get(symbol)
            if node is None:
                return None
        return {'counts': dict(node.counts), 'total': node.total, 'support': len(node.counts),
                'forced': node.forced, 'log_evidence': node.log_e, 'log_weight': node.log_w,
                'log_stop': node.log_stop, 'log_split': node.log_split, 'delta': node.delta}

    def fingerprint(self) -> str:
        """SHA-256 of parameters, counts, evidences and weights in canonical order (§11.3)."""
        self._require_fitted()
        params = self.params
        digest = hashlib.sha256()
        digest.update((f'{params.m}|{params.depth}|' + '|'.join(
            float(value).hex() for value in (params.a, params.log_rho, params.log_one_minus_rho))).encode())

        def walk(context, node):
            digest.update(('|'.join([
                repr(context), str(node.total),
                ','.join(f'{symbol}:{node.counts[symbol]}' for symbol in sorted(node.counts)),
                *(float(value).hex() for value in
                  (node.log_e, node.log_w, node.log_stop, node.log_split))]) + '\n').encode())
            for symbol in sorted(node.children):
                walk(context + (symbol,), node.children[symbol])

        walk((), self._root)
        return digest.hexdigest()

    # --- internals ---------------------------------------------------------

    def _require_fitted(self):
        if not self._fitted:
            raise ValueError('model is not fitted: call fit() before prediction')

    def _validated(self, symbols, where, offset=0) -> list:
        m = self.params.m
        values = []
        for position, value in enumerate(symbols):
            if not _is_int(value) or not 0 <= value < m:
                raise ValueError(f'{where} position {position + offset}: symbol {value!r} outside [0, {m})')
            values.append(int(value))
        return values

    def _history(self, history) -> list:
        """Only the last D symbols decide the path, so only that tail is validated (a full
        evaluation run passes 100k-symbol prefixes); the reported error position is still
        absolute in the full history, not relative to the validated tail."""
        self._require_fitted()
        depth = self.params.depth
        if depth == 0:
            return []
        tail = history[-depth:]
        return self._validated(tail, f'history (within the last {depth} symbols)',
                                offset=max(0, len(history) - depth))

    def _mixture(self, history):
        """Walk the frozen path: [(node, lambda, lexical length)] and the unseen mass."""
        node = self._root
        if node.total == 0:  # empty training: uniform prediction, all mass unseen (§9.2)
            return [], 1.0, True
        path, log_acc, depth, lexical = [], 0.0, 0, 0
        while True:
            if node.forced:  # stop = 1 by construction (§6.5)
                path.append((node, math.exp(log_acc), lexical))
                return path, 0.0, False
            path.append((node, math.exp(log_acc + node.log_stop), lexical))
            log_acc += node.log_split
            symbol = history[-1 - depth] if depth < len(history) else BOS
            child = node.children.get(symbol)
            if child is None:  # never-observed subtree: q = 1/m (§6.4), mass unseen (§9.2)
                return path, math.exp(log_acc), True
            node, depth = child, depth + 1
            if symbol != BOS:
                lexical += 1

    def _freeze(self):
        """Evidence and both weights per node, bottom-up, in sorted-symbol order."""
        params = self.params
        a, ma = params.a, params.m * params.a
        log_gamma_ma, log_gamma_a = math.lgamma(ma), math.lgamma(a)
        log_rho, log_split_prior = params.log_rho, params.log_one_minus_rho

        def weigh(node):
            node.log_e = log_gamma_ma - math.lgamma(node.total + ma) + sum(
                math.lgamma(node.counts[symbol] + a) - log_gamma_a for symbol in sorted(node.counts))
            if node.forced:
                node.log_w, node.log_stop, node.log_split, node.delta = node.log_e, 0.0, -math.inf, None
                return node.log_w
            children = sum(weigh(node.children[symbol]) for symbol in sorted(node.children))
            u = log_rho + node.log_e
            v = log_split_prior + children
            node.delta = delta = u - v
            node.log_stop = -np.logaddexp(0.0, -delta)
            node.log_split = -np.logaddexp(0.0, delta)
            node.log_w = u - node.log_stop  # = logaddexp(u, v), from the same two contributions
            return node.log_w

        weigh(self._root)
