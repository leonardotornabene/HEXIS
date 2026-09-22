"""V0: frozen contracts, strict application projection and historical isolation."""
import copy
import json
import shutil
from pathlib import Path

import pytest
import yaml

from hexis.config import load_v31_config, load_yaml
from hexis.contracts import BUNDLE, load_contracts, validate_projection

pytestmark = pytest.mark.v31


def test_deposit_and_application_projection_match():
    bundle = load_contracts()
    cfg = load_v31_config()
    assert cfg['spec_version'] == 'HEXIS-3.1'
    assert cfg['cells'] == bundle['design']['cells']
    assert cfg['registry'] == bundle['design']['registry']
    assert bundle['expected']['expected'] == bundle['report']['expected']
    assert [cell['m'] for cell in cfg['cells']] == [100, 100, 100, 100, 105, 11]


@pytest.mark.parametrize('value', [True, 8.0, -1, float('nan'), float('inf'), '8'])
def test_schema_refuses_wrong_numeric_types_and_values(value):
    cfg = load_v31_config()
    cfg['cells'][0]['D'] = value
    with pytest.raises(ValueError, match='cells') as exc:
        validate_projection(cfg, load_contracts()['design'])
    assert 'D' in str(exc.value)


@pytest.mark.parametrize('change', ['extra', 'missing', 'seed', 'cell', 'block', 'retired'])
def test_application_contract_rejects_drift(change):
    cfg = load_v31_config()
    if change == 'extra': cfg['unknown'] = 1
    if change == 'missing': del cfg['rng']
    if change == 'seed': cfg['cells'][0]['seeds'].append(0)
    if change == 'cell': cfg['cells'].append(copy.deepcopy(cfg['cells'][0]))
    if change == 'block': cfg['blocks'][0]['docs'].append('unknown')
    if change == 'retired': cfg['context_tree'] = {'k_min': 2}
    with pytest.raises(ValueError) as exc:
        validate_projection(cfg, load_contracts()['design'])
    assert str(exc.value)


def test_yaml_rejects_duplicate_keys_and_registry_drift(tmp_path):
    cfg = tmp_path / 'config.yaml'
    cfg.write_text('spec_version: HEXIS-3.1\nspec_version: HEXIS-3.1\n')
    with pytest.raises(ValueError, match='duplicate') as exc:
        load_v31_config(cfg)
    assert str(cfg) in str(exc.value)
    registry = tmp_path / 'registry.yaml'
    registry.write_text('spec_version: HEXIS-3.1\nregistry: []\n')
    with pytest.raises(ValueError, match='registry') as exc:
        load_v31_config(registry_path=registry)
    assert str(exc.value)


@pytest.mark.parametrize('fault', ['altered', 'missing', 'extra'])
def test_deposit_refuses_altered_missing_extra_contracts(tmp_path, fault):
    root = tmp_path / 'deposit'
    shutil.copytree(BUNDLE.parent, root)
    bundle = root / BUNDLE.name
    path = bundle / 'alphabets_v3.1.json'
    if fault == 'altered': path.write_text('{}')
    if fault == 'missing': path.unlink()
    if fault == 'extra': (bundle / 'extra.json').write_text('{}')
    with pytest.raises(ValueError) as exc:
        load_contracts(bundle)
    assert str(exc.value)


def test_the_alphabet_reads_the_active_projection_only():
    """The mapping refuses any configuration that is not the deposited 3.1 one."""
    from hexis.alphabet import map_token
    with pytest.raises(ValueError, match='HEXIS-3.1') as exc:
        map_token('NOUN', 'nsubj', {'spec_version': 'HEXIS-2.1', 'alphabet': {}})
    assert str(exc.value)


# --- YAML reader cases carried over from the v2.1 audit suite --------------------


@pytest.mark.parametrize('body', ['spec_version: HEXIS-3.1\nspec_version: HEXIS-3.1\n',
                                  'registry:\n- source_prefix: a\n  part_order: 0\n  part_order: 1\n'],
                         ids=['top-level', 'nested'])
def test_duplicate_yaml_keys_are_rejected_at_every_depth(tmp_path, body):
    path = tmp_path/'duplicate.yaml'
    path.write_text(body)
    with pytest.raises(ValueError, match='duplicate') as exc:
        load_yaml(path)
    assert str(path) in str(exc.value)


def test_a_yaml_error_names_the_original_file_and_keeps_its_snippet(tmp_path):
    """The stage parses a private copy, whose temporary path is gone by the time
    anyone reads the message: the error must name the original and keep the
    parser's line, column and caret."""
    original = tmp_path/'unparseable.yaml'
    original.write_text('alpha: [unclosed\n')
    staged = tmp_path/'0000_unparseable.yaml'
    staged.write_bytes(original.read_bytes())
    with pytest.raises(ValueError) as exc:
        load_yaml(original, source=staged)
    message = str(exc.value)
    assert staged.name not in message
    assert f'in "{original}", line 1, column 8' in message
    assert 'alpha: [unclosed' in message and '^' in message
    assert '<unicode string>' not in message
