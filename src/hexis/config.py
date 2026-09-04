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
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode


class _UniqueKeyLoader(yaml.SafeLoader):
    """SafeLoader that refuses YAML's silent last-duplicate-wins behaviour."""


def _construct_unique_mapping(loader, node, deep=False):
    if not isinstance(node, MappingNode):
        raise ConstructorError(None, None, "expected a mapping node", node.start_mark)
    loader.flatten_mapping(node)
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def _find_default_config() -> Path:
    for base in [Path.cwd(), *Path.cwd().parents]:
        candidate = base / "config" / "default.yaml"
        if candidate.exists():
            return candidate
    raise FileNotFoundError("config/default.yaml not found from the working directory upward")


def load_yaml(path, *, source=None):
    """Safely load YAML while rejecting duplicate keys at every mapping depth."""
    path = Path(path)
    try:
        return yaml.load(
            Path(source or path).read_text(encoding="utf-8"), Loader=_UniqueKeyLoader
        )
    except yaml.YAMLError as exc:
        detail = str(exc).replace("<unicode string>", str(path))
        raise ValueError(f"{path}: not valid YAML — {detail}") from exc


def load_config(path=None) -> dict:
    """Load a nonempty YAML mapping (defaults to config/default.yaml)."""
    path = Path(path) if path is not None else _find_default_config()
    data = load_yaml(path)
    if not isinstance(data, dict) or not data:
        raise ValueError(
            f"{path}: a configuration must be a nonempty mapping, not "
            f"{type(data).__name__}"
        )
    return data


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
    for section in sorted(set(cfg) | set(reference), key=repr):
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
            missing.extend(f"{section}.{key}" for key in sorted(want, key=repr))
            continue
        for key in sorted(set(have) | set(want), key=repr):
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
    _check_g1_shapes(cfg, reference)


def _check_g1_shapes(cfg: dict, reference: dict) -> None:
    """Validate only structures consumed by the G1 audit; later stages own theirs."""
    languages = cfg["corpus"]["languages"]
    if not isinstance(languages, list) or not languages:
        raise ValueError("corpus.languages must be a nonempty list of strings")
    if any(not isinstance(language, str) or not language.strip() for language in languages):
        raise ValueError("corpus.languages must contain only nonempty strings")
    if len(languages) != len(set(languages)):
        raise ValueError("corpus.languages must contain unique language codes")

    contrast = cfg["corpus"]["primary_contrast"]
    if not isinstance(contrast, dict):
        raise ValueError("corpus.primary_contrast must be a mapping keyed by language")
    unknown = sorted(
        set(contrast) - set(reference["corpus"]["primary_contrast"]), key=repr
    )
    if unknown:
        raise ValueError(f"corpus.primary_contrast has unknown language(s) {unknown}")
    missing = sorted(set(languages) - set(contrast))
    if missing:
        raise ValueError(
            f"corpus.primary_contrast is missing configured language(s) {missing}"
        )
    for language in languages:
        pair = contrast[language]
        if (
            not isinstance(pair, list)
            or len(pair) != 2
            or any(not isinstance(side, str) or not side.strip() for side in pair)
        ):
            raise ValueError(
                f"corpus.primary_contrast.{language} must contain exactly two "
                "nonempty strings"
            )

    string_lists = (
        ("alphabet", "upos_keep"),
        ("alphabet", "upos_drop"),
        ("alphabet", "deprel_keep"),
        ("stats", "family"),
    )
    for section, key in string_lists:
        value = cfg[section][key]
        if not isinstance(value, list) or any(
            not isinstance(item, str) or not item.strip() for item in value
        ):
            raise ValueError(f"{section}.{key} must be a list of nonempty strings")

    curve = cfg["scores"]["learning_curve_T"]
    if not isinstance(curve, list) or any(
        isinstance(item, bool) or not isinstance(item, int) for item in curve
    ):
        raise ValueError("scores.learning_curve_T must be a list of integers")

    seed = cfg["seeds"]["global"]
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seeds.global must be an integer (not a boolean)")
    minimum = cfg["scores"]["min_available_past"]
    if isinstance(minimum, bool) or not isinstance(minimum, int) or minimum < 0:
        raise ValueError("scores.min_available_past must be a non-negative integer")
    threshold = cfg["alphabet"]["gate_a_threshold"]
    if isinstance(threshold, bool) or not isinstance(threshold, (int, float)):
        raise ValueError("alphabet.gate_a_threshold must be numeric")


def config_hash(cfg: dict) -> str:
    """SHA-256 of the canonical JSON serialization (sorted keys) of the resolved config."""
    canonical = json.dumps(cfg, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def derive_seed(analysis_id: str, global_seed: int) -> int:
    """Per-analysis seed = global XOR crc32(analysis_id) (§6.3)."""
    return global_seed ^ (zlib.crc32(analysis_id.encode("utf-8")) & 0xFFFFFFFF)
