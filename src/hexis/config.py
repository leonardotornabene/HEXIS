"""Configuration loading: config/default.yaml, single source of parameters (Spec §6.3).

Signatures chosen under the P4 authorization (not fixed in §6.2); recorded in
docs/HANDOFF.md as PROPOSED. ``config/default.yaml`` is not packaged into the
wheel, so it is located by walking up from the working directory (the pipeline
and the test suite both run from the repository root).
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


def config_hash(cfg: dict) -> str:
    """SHA-256 of the canonical JSON serialization (sorted keys) of the resolved config."""
    canonical = json.dumps(cfg, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def derive_seed(analysis_id: str, global_seed: int) -> int:
    """Per-analysis seed = global XOR crc32(analysis_id) (§6.3)."""
    return global_seed ^ (zlib.crc32(analysis_id.encode("utf-8")) & 0xFFFFFFFF)
