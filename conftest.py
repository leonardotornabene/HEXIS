"""Repository-level enforcement for the G0 pytest gate (D45/D52(iii))."""

import ast
from pathlib import Path

pytest_plugins = ["pytester"]

_ASSERTED_G0: set[str] = set()
_COLLECTION_SKIPPED_G0: set[str] = set()
_SKIPPED_G0: set[str] = set()
_XPASSED_G0: set[str] = set()
_ROOT = Path()


def pytest_configure(config):
    global _ROOT
    _ROOT = Path(config.rootpath)
    for configured in config.getini("testpaths") or ["."]:
        test_root = _ROOT / configured
        if test_root.is_dir():
            for cache in test_root.rglob("*-pytest-*.pyc"):
                cache.unlink(missing_ok=True)


def pytest_sessionstart(session):
    _ASSERTED_G0.clear()
    _COLLECTION_SKIPPED_G0.clear()
    _SKIPPED_G0.clear()
    _XPASSED_G0.clear()


def pytest_assertion_pass(item, lineno, orig, expl):
    if item.get_closest_marker("g0") is not None:
        _ASSERTED_G0.add(item.nodeid)


def _source_declares_g0(nodeid: str) -> bool:
    path = Path(nodeid.split("::", 1)[0])
    if not path.is_absolute():
        path = _ROOT / path
    if path.suffix != ".py" or not path.is_file():
        return False
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return any(
        isinstance(node, ast.Attribute)
        and node.attr == "g0"
        and (
            isinstance(node.value, ast.Name)
            and node.value.id == "mark"
            or isinstance(node.value, ast.Attribute)
            and node.value.attr == "mark"
        )
        for node in ast.walk(tree)
    )


def pytest_collectreport(report):
    if report.skipped and _source_declares_g0(report.nodeid):
        _COLLECTION_SKIPPED_G0.add(report.nodeid)


def pytest_runtest_logreport(report):
    if "g0" not in report.keywords:
        return
    if report.skipped:
        _SKIPPED_G0.add(report.nodeid)
    if report.passed and hasattr(report, "wasxfail"):
        _XPASSED_G0.add(report.nodeid)


def pytest_sessionfinish(session, exitstatus):
    # --collect-only runs no test, so every G0 item would look assertion-free.
    # Introspecting the selection is not a gate run; only the real one enforces.
    if session.config.getoption("collectonly", False):
        return
    selected = {
        item.nodeid for item in session.items if item.get_closest_marker("g0") is not None
    }
    missing_assertion = selected - _ASSERTED_G0
    failures = {
        "collection skip": _COLLECTION_SKIPPED_G0,
        "skip/xfail": _SKIPPED_G0,
        "xpass": _XPASSED_G0,
        "no executed assert": missing_assertion,
    }
    failures = {kind: nodeids for kind, nodeids in failures.items() if nodeids}
    if not failures:
        return
    reporter = session.config.pluginmanager.getplugin("terminalreporter")
    if reporter is not None:
        for kind, nodeids in failures.items():
            reporter.write_line(
                f"G0 GATE FAILURE — {kind}: " + ", ".join(sorted(nodeids)),
                red=True,
            )
    if session.exitstatus == 0:
        session.exitstatus = 1
