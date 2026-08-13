"""Tests for the repository-local G0 gate: enforcement (D45/D52(iii)) and
mandatory-coverage inventory (D52(ii))."""

import ast
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).parent
ROOT_CONFTEST = TESTS_DIR.parent / "conftest.py"
pytestmark = pytest.mark.g0

# D52(ii) minimum mandatory coverage, plus the §7 scoring-boundary case gated at
# G0, mapped onto D52(ii)'s "expected minimum file organization". The clause
# permits tests to be "split, merged or parametrized differently provided the
# mandatory coverage stays explicit and traceable" — reorganizing therefore
# means editing this map, which is what keeps the inventory traceable.
G0_REQUIRED_COVERAGE = {
    "conllu_reader": "test_conllu_reader.py",
    "total alphabet mapping (§3.4)": "test_alphabet.py",
    "registry construction and validation": "test_registry.py",
    "sequence construction under both P-RESET and P-BOUND (§3.5, D52(x))": "test_sequences.py",
    "sentence-aligned document-safe blocks": "test_blocks.py",
    "exact document-label permutation and sign-flip utilities": "test_permutation.py",
    "bootstrap reproducibility and Holm correction": "test_bootstrap_holm.py",
    "seed derivation, resolved-config hash, run manifest, sidecar, overwrite refusal": "test_determinism.py",
    "label-free scoring core signature (§7 scoring-boundary case 1)": "test_scores.py",
}


def _mentions_g0(node: ast.AST) -> bool:
    return any(
        isinstance(sub, ast.Attribute) and sub.attr == "g0" for sub in ast.walk(node)
    )


def _g0_test_count(path: Path) -> int:
    """Number of test functions in `path` carrying the g0 marker."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    module_marked = any(
        isinstance(node, ast.Assign)
        and any(getattr(target, "id", None) == "pytestmark" for target in node.targets)
        and _mentions_g0(node.value)
        for node in tree.body
    )
    return sum(
        1
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_")
        and (module_marked or any(_mentions_g0(dec) for dec in node.decorator_list))
    )


def test_g0_set_covers_every_mandatory_area():
    """G0 cannot close on a subset: `-m g0` must stay red until every mandatory
    D52(ii) area declares g0 coverage. Without this, deselection makes an
    incomplete set look green (the marker set is a subset by construction)."""
    missing = {
        area: filename
        for area, filename in G0_REQUIRED_COVERAGE.items()
        if not (TESTS_DIR / filename).is_file()
        or _g0_test_count(TESTS_DIR / filename) == 0
    }
    assert not missing, "mandatory D52(ii) coverage with no g0 test: " + "; ".join(
        f"{area} -> tests/{filename}" for area, filename in sorted(missing.items())
    )


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
