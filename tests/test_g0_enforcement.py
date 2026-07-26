"""G0 gate enforcement — mechanizes the D45/D52(iii) criterion (no methodological content).

Two layers, neither reading the pytest summary by eye:
  * runtime (root ``conftest.py``): the session exits non-zero if any ``g0``-marked
    test is skipped — statically or via a dynamic ``pytest.skip`` — or xfailed;
    ``xfail_strict`` turns an xpass into a failure; ``--strict-markers`` rejects
    unregistered markers.
  * static (this file): an AST meta-test fails if any ``g0`` test body carries no
    effective assertion (``assert`` / ``with pytest.raises`` / an ``assert*`` call
    such as ``np.testing.assert_allclose`` or ``pandas.testing.assert_frame_equal``).

The AST predicate is exercised directly; the skip and xpass session behaviours are
proven with ``pytester`` subprocesses seeded from the real root ``conftest.py``.
"""

import ast
import pathlib

import pytest

TESTS_DIR = pathlib.Path(__file__).parent
ROOT_CONFTEST = TESTS_DIR.parent / "conftest.py"


# --- AST predicate --------------------------------------------------------------


def _decorator_is_g0(dec: ast.expr) -> bool:
    target = dec.func if isinstance(dec, ast.Call) else dec
    return (
        isinstance(target, ast.Attribute)
        and target.attr == "g0"
        and isinstance(target.value, ast.Attribute)
        and target.value.attr == "mark"
    )


def _callee_name(func: ast.expr) -> str | None:
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _has_effective_assertion(func: ast.AST) -> bool:
    for node in ast.walk(func):
        if isinstance(node, ast.Assert):
            return True
        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call) and _callee_name(ctx.func) == "raises":
                    return True
        if isinstance(node, ast.Call):
            name = _callee_name(node.func)
            if name and name.startswith("assert"):
                return True
    return False


def _g0_functions(src: str):
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and any(
            _decorator_is_g0(d) for d in node.decorator_list
        ):
            yield node


# --- the G0 static gate (itself a g0 test) --------------------------------------


@pytest.mark.g0
def test_all_g0_tests_carry_an_effective_assertion():
    offenders = []
    for pyfile in sorted(TESTS_DIR.glob("test_*.py")):
        for func in _g0_functions(pyfile.read_text()):
            if not _has_effective_assertion(func):
                offenders.append(f"{pyfile.name}::{func.name}")
    assert offenders == [], f"g0 tests lacking an effective assertion: {offenders}"


# --- predicate unit tests (infra, not part of the g0 set) -----------------------


def test_predicate_accepts_assert_statement():
    (func,) = ast.parse("def t():\n    assert 1 == 1\n").body
    assert _has_effective_assertion(func)


def test_predicate_accepts_pytest_raises():
    src = "def t():\n    with pytest.raises(ValueError):\n        raise ValueError()\n"
    (func,) = ast.parse(src).body
    assert _has_effective_assertion(func)


def test_predicate_accepts_assert_call():
    (a,) = ast.parse("def t():\n    np.testing.assert_allclose(1.0, 1.0)\n").body
    (b,) = ast.parse("def t():\n    assert_frame_equal(x, y)\n").body
    assert _has_effective_assertion(a)
    assert _has_effective_assertion(b)


def test_predicate_rejects_assertion_free_body():
    (func,) = ast.parse("def t():\n    x = 1\n    return x\n").body
    assert not _has_effective_assertion(func)


def test_meta_scan_flags_assertion_free_g0(tmp_path):
    bad = tmp_path / "test_bad.py"
    bad.write_text("import pytest\n\n@pytest.mark.g0\ndef test_x():\n    pass\n")
    offenders = [f.name for f in _g0_functions(bad.read_text()) if not _has_effective_assertion(f)]
    assert offenders == ["test_x"]


# --- runtime enforcement, proven via pytester subprocess ------------------------


def _seed(pytester):
    pytester.makeconftest(ROOT_CONFTEST.read_text())
    pytester.makepyprojecttoml(
        '[tool.pytest.ini_options]\n'
        'markers = ["g0: gate"]\n'
        'xfail_strict = true\n'
        'addopts = "--strict-markers"\n'
    )


def test_enforcement_fails_on_dynamically_skipped_g0(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.g0\ndef test_s():\n    pytest.skip('dynamic')\n"
    )
    assert pytester.runpytest_subprocess().ret != 0


def test_enforcement_fails_on_statically_skipped_g0(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.g0\n@pytest.mark.skip('static')\n"
        "def test_s():\n    assert True\n"
    )
    assert pytester.runpytest_subprocess().ret != 0


def test_enforcement_fails_on_xpass(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.xfail(reason='but passes')\n"
        "def test_x():\n    assert True\n"
    )
    assert pytester.runpytest_subprocess().ret != 0


def test_enforcement_passes_a_clean_g0_suite(pytester):
    _seed(pytester)
    pytester.makepyfile(
        "import pytest\n\n@pytest.mark.g0\ndef test_ok():\n    assert 1 == 1\n"
    )
    assert pytester.runpytest_subprocess().ret == 0
