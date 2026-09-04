"""The repo gate must not disappear by deleting its own inventory file."""

from pathlib import Path

import pytest


ROOT_CONFTEST = Path(__file__).resolve().parents[1] / "conftest.py"


@pytest.mark.parametrize("marker", ["g0", "g1"])
@pytest.mark.parametrize("broken", ["missing", "unmarked"])
def test_repository_gate_rejects_a_missing_or_unmarked_inventory(
    pytester, marker, broken
):
    pytester.makeconftest(ROOT_CONFTEST.read_text(encoding="utf-8"))
    pytester.makepyprojecttoml(
        '[tool.pytest.ini_options]\nmarkers = ["g0: gate", "g1: gate"]\n'
        'testpaths = ["tests"]\nenable_assertion_pass_hook = true\n'
    )
    (pytester.path / "src" / "hexis").mkdir(parents=True)
    tests = pytester.path / "tests"
    tests.mkdir()
    for current in ("g0", "g1"):
        if current == marker and broken == "missing":
            continue
        mark = "" if current == marker else f"import pytest\npytestmark = pytest.mark.{current}\n"
        (tests / f"test_{current}_enforcement.py").write_text(
            mark + "def test_anchor(): assert True\n", encoding="utf-8"
        )

    result = pytester.runpytest_subprocess("-m", marker, "--strict-markers")

    assert result.ret != 0
    result.stderr.fnmatch_lines(
        [f"*test_{marker}_enforcement.py*inventory anchor*"]
    )
