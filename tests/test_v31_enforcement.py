"""Active V0–V1 must collect all required tests and execute real assertions."""
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

import pytest

pytestmark = pytest.mark.v31
ROOT_CONFTEST = Path(__file__).resolve().parents[1]/'conftest.py'

REQUIRED = {'test_v31_config.py': ['test_deposit_and_application_projection_match',
                        'test_schema_refuses_wrong_numeric_types_and_values',
                        'test_application_contract_rejects_drift',
                        'test_yaml_rejects_duplicate_keys_and_registry_drift',
                        'test_deposit_refuses_altered_missing_extra_contracts',
                        'test_legacy_executors_refuse_active_config'],
 'test_v31_docs.py': ['test_active_authority_and_instructions_are_aligned',
                      'test_history_and_deposit_are_byte_preserved',
                      'test_test_inventory_explicitly_tracks_future_obligations'],
 'test_v31_enforcement.py': ['test_v31_actual_collection_covers_required_behaviors',
                             'test_v31_inventory_rejects_missing_test_and_marker',
                             'test_v31_enforcement_rejects_vacuity_skip_and_xfail',
                             'test_v31_enforcement_accepts_executed_assert']}


def missing_coverage(items, required):
    collected=defaultdict(set)
    for item in items:
        if item.get_closest_marker('v31') is not None:
            collected[Path(item.path).name].add(getattr(item,'originalname',None) or item.name.split('[',1)[0])
    return {file:sorted(set(names)-collected[file]) or ['empty inventory']
            for file,names in required.items() if not names or set(names)-collected[file]}


def test_v31_actual_collection_covers_required_behaviors(request):
    assert REQUIRED
    assert not missing_coverage(request.session.items,REQUIRED)


def test_v31_inventory_rejects_missing_test_and_marker():
    item=SimpleNamespace(path=Path('test_a.py'),name='test_a',get_closest_marker=lambda marker:None)
    assert missing_coverage([item],{'test_a.py':['test_a']})=={'test_a.py':['test_a']}
    assert missing_coverage([],{'test_a.py':[]})=={'test_a.py':['empty inventory']}


@pytest.mark.parametrize('body',[
    'def test_bad(): pass',
    'def test_bad():\n    if False: assert True',
    'def test_bad(): pytest.skip("no")',
    '@pytest.mark.xfail\ndef test_bad(): assert False',
    'pytest.skip("no", allow_module_level=True)\ndef test_bad(): assert True',
])
def test_v31_enforcement_rejects_vacuity_skip_and_xfail(pytester,body):
    pytester.makeconftest(ROOT_CONFTEST.read_text())
    pytester.makepyprojecttoml('[tool.pytest.ini_options]\nmarkers=["v31: active"]\nenable_assertion_pass_hook=true\n')
    pytester.makepyfile('import pytest\npytestmark=pytest.mark.v31\n'+body)
    result=pytester.runpytest_subprocess('-m','v31','--strict-markers')
    assert result.ret!=0


def test_v31_enforcement_accepts_executed_assert(pytester):
    pytester.makeconftest(ROOT_CONFTEST.read_text())
    pytester.makepyprojecttoml('[tool.pytest.ini_options]\nmarkers=["v31: active"]\nenable_assertion_pass_hook=true\n')
    pytester.makepyfile('import pytest\npytestmark=pytest.mark.v31\ndef test_good(): assert 2+2==4')
    result=pytester.runpytest_subprocess('-m','v31','--strict-markers')
    assert result.ret==0
