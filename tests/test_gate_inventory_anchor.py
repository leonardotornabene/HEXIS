"""The gate must not disappear by deleting or unmarking its own inventory file."""

from pathlib import Path

import pytest


ROOT_CONFTEST = Path(__file__).resolve().parents[1] / "conftest.py"

pytestmark = pytest.mark.v31


@pytest.mark.parametrize("broken", ["missing", "unmarked"])
def test_repository_gate_rejects_a_missing_or_unmarked_inventory(pytester, broken):
    pytester.makeconftest(ROOT_CONFTEST.read_text(encoding="utf-8"))
    pytester.makepyprojecttoml(
        '[tool.pytest.ini_options]\nmarkers = ["v31: active"]\n'
        'testpaths = ["tests"]\nenable_assertion_pass_hook = true\n'
    )
    (pytester.path / "src" / "hexis").mkdir(parents=True)
    tests = pytester.path / "tests"
    tests.mkdir()
    if broken == "unmarked":
        (tests / "test_v31_enforcement.py").write_text(
            "def test_anchor(): assert True\n", encoding="utf-8"
        )

    result = pytester.runpytest_subprocess("-m", "v31", "--strict-markers")

    assert result.ret != 0
    result.stderr.fnmatch_lines(["*test_v31_enforcement.py*inventory anchor*"])
