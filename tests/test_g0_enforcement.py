"""Subprocess tests for the repository-local G0 gate (D45/D52(iii))."""

from pathlib import Path

import pytest

ROOT_CONFTEST = Path(__file__).parents[1] / "conftest.py"
pytestmark = pytest.mark.g0


def _config(*, assertion_pass=True):
    return (
        '[tool.pytest.ini_options]\n'
        'markers = ["g0: gate"]\n'
        'xfail_strict = true\n'
        f'enable_assertion_pass_hook = {str(assertion_pass).lower()}\n'
        'addopts = "--strict-markers"\n'
    )


def _seed(pytester):
    pytester.makeconftest(ROOT_CONFTEST.read_text(encoding="utf-8"))
    pytester.makepyprojecttoml(_config())


def _run_g0(pytester):
    return pytester.runpytest_subprocess("-m", "g0", "--strict-markers")


def test_enforcement_fails_on_dynamically_skipped_g0(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.g0\ndef test_s():\n    pytest.skip('dynamic')\n"
    )
    assert _run_g0(pytester).ret != 0


def test_enforcement_fails_on_statically_skipped_g0(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.g0\n@pytest.mark.skip('static')\n"
        "def test_s():\n    assert True\n"
    )
    assert _run_g0(pytester).ret != 0


def test_enforcement_fails_on_xpass(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.g0\n@pytest.mark.xfail(reason='but passes')\n"
        "def test_x():\n    assert True\n"
    )
    assert _run_g0(pytester).ret != 0


def test_enforcement_fails_on_nonstrict_xpass(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.g0\n@pytest.mark.xfail(reason='but passes', strict=False)\n"
        "def test_x():\n    assert True\n"
    )
    assert _run_g0(pytester).ret != 0


def test_enforcement_fails_on_module_marked_assertion_free_test(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\npytestmark = pytest.mark.g0\n\ndef test_x():\n    pass\n"
    )
    assert _run_g0(pytester).ret != 0


def test_enforcement_fails_when_assertion_is_dead_code(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.g0\ndef test_x():\n"
        "    if False:\n        assert False\n"
    )
    assert _run_g0(pytester).ret != 0


def test_enforcement_fails_on_collection_time_skip(pytester):
    _seed(pytester)
    pytester.makepyfile(
        test_ok=(
            "import pytest\n\n@pytest.mark.g0\ndef test_ok():\n    assert True\n"
        ),
        test_skipped=(
            "import pytest\n\npytestmark = pytest.mark.g0\n"
            "pytest.skip('collection skip', allow_module_level=True)\n"
        ),
    )
    assert _run_g0(pytester).ret != 0


def test_collection_skip_in_non_g0_module_is_ignored(pytester):
    _seed(pytester)
    pytester.makepyfile(
        test_ok=(
            "import pytest\n\n@pytest.mark.g0\ndef test_ok():\n    assert True\n"
        ),
        test_skipped=(
            '"""This non-G0 module merely documents ``pytest.mark.g0``."""\n'
            "import pytest\npytest.skip('optional module', allow_module_level=True)\n"
        ),
    )
    assert _run_g0(pytester).ret == 0


def test_enforcement_passes_a_clean_g0_suite(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.g0\ndef test_ok():\n    assert 1 == 1\n"
    )
    assert _run_g0(pytester).ret == 0


def test_enforcement_invalidates_pyc_created_without_assertion_hook(pytester):
    pytester.makeconftest(ROOT_CONFTEST.read_text(encoding="utf-8"))
    pytester.makepyprojecttoml(_config(assertion_pass=False))
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.g0\ndef test_ok():\n    assert 1 == 1\n"
    )
    assert _run_g0(pytester).ret != 0

    pytester.makepyprojecttoml(_config(assertion_pass=True))
    assert _run_g0(pytester).ret == 0
