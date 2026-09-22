"""Configuration: safe YAML, no duplicate keys, and the deposited projection.

`config/default.yaml` carries no parameter of its own. It is the analytical
projection of the deposited design, compared field by field against it (§13.1),
so a divergence is an error here and not a second source of values.
"""

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
















def load_v31_config(path=None, *, registry_path=None) -> dict:
    """Load the exact active analytical projection and independently check registry."""
    from hexis.contracts import ROOT, load_contracts, validate_projection, compare
    path = Path(path) if path is not None else ROOT / 'config/default.yaml'
    registry_path = Path(registry_path) if registry_path is not None else ROOT / 'config/registry_overrides.yaml'
    design = load_contracts()['design']
    cfg = load_yaml(path)
    validate_projection(cfg, design)
    compare(load_yaml(registry_path), {'spec_version': 'HEXIS-3.1', 'registry': design['registry']}, str(registry_path))
    return cfg
