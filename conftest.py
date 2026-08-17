"""Repository-level enforcement for the pytest gate selections (D45/D52(iii))."""

import ast
from pathlib import Path

pytest_plugins = ["pytester"]

# Markers under gate enforcement. D52(ii)–(iii) define the G0 set and the rule:
# no test in a gate selection may be skipped, xfail, xpass, or collected without
# an effective assertion, and the enforcement must not depend on reading the
# pytest summary by eye. `g1` extends the same mechanics to the G1 audit tests
# (D55 §xiv, convention 13; PROPOSED). The rule is identical for both, so the
# marker name is data here rather than a second implementation.
GATE_MARKERS = ("g0", "g1")

_ASSERTED: set[str] = set()
_COLLECTION_SKIPPED: set[str] = set()
_SKIPPED: set[str] = set()
_XPASSED: set[str] = set()
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
    _ASSERTED.clear()
    _COLLECTION_SKIPPED.clear()
    _SKIPPED.clear()
    _XPASSED.clear()


def _is_gated(item) -> bool:
    return any(item.get_closest_marker(marker) is not None for marker in GATE_MARKERS)


def pytest_assertion_pass(item, lineno, orig, expl):
    if _is_gated(item):
        _ASSERTED.add(item.nodeid)


def _source_declares_gate(nodeid: str) -> bool:
    path = Path(nodeid.split("::", 1)[0])
    if not path.is_absolute():
        path = _ROOT / path
    if path.suffix != ".py" or not path.is_file():
        return False
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return any(
        isinstance(node, ast.Attribute)
        and node.attr in GATE_MARKERS
        and (
            isinstance(node.value, ast.Name)
            and node.value.id == "mark"
            or isinstance(node.value, ast.Attribute)
            and node.value.attr == "mark"
        )
        for node in ast.walk(tree)
    )


def pytest_collectreport(report):
    if report.skipped and _source_declares_gate(report.nodeid):
        _COLLECTION_SKIPPED.add(report.nodeid)


def pytest_runtest_logreport(report):
    if not any(marker in report.keywords for marker in GATE_MARKERS):
        return
    if report.skipped:
        _SKIPPED.add(report.nodeid)
    if report.passed and hasattr(report, "wasxfail"):
        _XPASSED.add(report.nodeid)


def pytest_sessionfinish(session, exitstatus):
    # --collect-only runs no test, so every gated item would look assertion-free.
    # Introspecting the selection is not a gate run; only the real one enforces.
    if session.config.getoption("collectonly", False):
        return
    selected = {item.nodeid for item in session.items if _is_gated(item)}
    missing_assertion = selected - _ASSERTED
    failures = {
        "collection skip": _COLLECTION_SKIPPED,
        "skip/xfail": _SKIPPED,
        "xpass": _XPASSED,
        "no executed assert": missing_assertion,
    }
    failures = {kind: nodeids for kind, nodeids in failures.items() if nodeids}
    if not failures:
        return
    reporter = session.config.pluginmanager.getplugin("terminalreporter")
    if reporter is not None:
        # The nodeid names the file, and the file names its gate — so the line
        # does not guess at a gate number it would sometimes get wrong.
        for kind, nodeids in failures.items():
            reporter.write_line(
                f"GATE FAILURE — {kind}: " + ", ".join(sorted(nodeids)),
                red=True,
            )
    if session.exitstatus == 0:
        session.exitstatus = 1
