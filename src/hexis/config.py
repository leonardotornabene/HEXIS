"""Configuration loading: config/default.yaml, single source of parameters (Spec §6.3).

Signatures chosen under the P4 authorization (not fixed in §6.2) and ratified
by the owner on 2026-07-27, as recorded in docs/HANDOFF.md.
``config/default.yaml`` is not packaged into the wheel, so it is located by
walking up from the working directory (the pipeline and the test suite both run
from the repository root).
"""

import copy
import hashlib
import json
import zlib
from pathlib import Path

import yaml


def _find_default_config() -> Path:
    for base in [Path.cwd(), *Path.cwd().parents]:
        candidate = base / "config" / "default.yaml"
        if candidate.exists():
            return candidate
    raise FileNotFoundError("config/default.yaml not found from the working directory upward")


def load_config(path=None) -> dict:
    """Load the YAML configuration (defaults to config/default.yaml)."""
    path = Path(path) if path is not None else _find_default_config()
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _deep_merge(base: dict, overrides: dict) -> dict:
    out = copy.deepcopy(base)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = copy.deepcopy(value)
    return out


def resolve_config(overrides=None, base=None) -> dict:
    """Deep-merge ``overrides`` into ``base`` (default config) without mutating either."""
    if base is None:
        base = load_config()
    return _deep_merge(base, overrides or {})


def check_against_default(cfg: dict, *, reference: dict | None = None) -> None:
    """Reject a resolved config whose key set differs from the default's (§6.3).

    `resolve_config` merges anything, so `context_tree.dmax` is accepted, read by
    nothing, and still changes `config_hash` — a misparameterized run whose own
    identity does not say so. A *missing* declared key is the same failure from
    the other side: the run takes a default the operator never saw.

    The check is deliberately not inside `resolve_config`: that function's
    partial-override semantics are attested at G0, and `stats/` merges fragments
    against synthetic bases that are not the full config.

    Two levels only — top-level sections and their immediate keys. Below that the
    keys are values (regime lists, symbol maps) and a schema check would reject
    legitimate data — `corpus.primary_contrast` is keyed by language and its keys
    are never inspected for that reason. It carried a named exemption until
    2026-09-03; since the check never descends that far the exemption bought
    nothing and only stopped the key *itself* from being required.
    """
    if reference is None:
        reference = load_config()
    unknown, missing = [], []
    for section in sorted(set(cfg) | set(reference)):
        if section not in reference:
            unknown.append(section)
            continue
        if section not in cfg:
            missing.append(section)
            continue
        want, have = reference[section], cfg[section]
        if not isinstance(want, dict):
            continue
        if not isinstance(have, dict):
            # A declared section replaced by a scalar or a list has no keys to
            # compare, and skipping it accepts the misparameterisation this
            # function exists to refuse: every key it should carry is absent.
            missing.extend(f"{section}.{key}" for key in sorted(want))
            continue
        for key in sorted(set(have) | set(want)):
            if key not in want:
                unknown.append(f"{section}.{key}")
            elif key not in have:
                missing.append(f"{section}.{key}")
    if unknown or missing:
        raise ValueError(
            "resolved config does not match config/default.yaml — unknown key(s): "
            f"{unknown}; missing key(s): {missing}. An unknown key is read by "
            "nothing yet still changes config_hash; a missing one lets the run "
            "take a default its own config never showed (§6.3)."
        )


def config_hash(cfg: dict) -> str:
    """SHA-256 of the canonical JSON serialization (sorted keys) of the resolved config."""
    canonical = json.dumps(cfg, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def derive_seed(analysis_id: str, global_seed: int) -> int:
    """Per-analysis seed = global XOR crc32(analysis_id) (§6.3)."""
    return global_seed ^ (zlib.crc32(analysis_id.encode("utf-8")) & 0xFFFFFFFF)
