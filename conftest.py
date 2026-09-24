"""Repository-level enforcement of the active acceptance (plan §12).

Every collected test is v31 acceptance: no skip, no xfail, no xpass, and no test
collected without an executed assert. The rule is enforced here rather than read
off a pytest summary by eye.
"""

import ast
import importlib.util
from pathlib import Path

import pytest

pytest_plugins = ["pytester"]

# One acceptance, one marker. The inventory anchor must exist and must carry the
# marker, or the enforcement would certify nothing.
GATE_MARKERS = ("v31",)
GATE_INVENTORIES = {"v31": "test_v31_enforcement.py"}

_ASSERTED: set[str] = set()
_COLLECTION_SKIPPED: set[str] = set()
_SKIPPED: set[str] = set()
_XPASSED: set[str] = set()
_ROOT = Path()


class _CollectionGate:
    def pytest_collectreport(self, report):
        if report.skipped:
            _COLLECTION_SKIPPED.add(report.nodeid)


def pytest_configure(config):
    global _ROOT
    _ROOT = Path(config.rootpath)
    config.pluginmanager.register(_CollectionGate(), name="hormathos-collection-gate")
    # Only the HORMATHOS repository has this trust anchor. Pytester copies this
    # conftest into synthetic projects, which must remain free to define tiny gates.
    if (_ROOT / "src" / "hormathos").is_dir():
        for marker, filename in GATE_INVENTORIES.items():
            path = _ROOT / "tests" / filename
            if not path.is_file() or not _declares_module_marker(path, marker):
                raise pytest.UsageError(
                    f"{path}: missing or unmarked {marker} inventory anchor"
                )
    for configured in config.getini("testpaths") or ["."]:
        test_root = _ROOT / configured
        if test_root.is_dir():
            for source in test_root.rglob("*.py"):
                cache = Path(importlib.util.cache_from_source(str(source)))
                if cache.parent.is_dir():
                    for compiled in cache.parent.glob(f"{source.stem}.*.pyc"):
                        compiled.unlink(missing_ok=True)


def _declares_module_marker(path: Path, marker: str) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not any(
            isinstance(target, ast.Name) and target.id == "pytestmark"
            for target in node.targets
        ):
            continue
        return any(
            isinstance(part, ast.Attribute)
            and part.attr == marker
            and isinstance(part.value, ast.Attribute)
            and part.value.attr == "mark"
            and isinstance(part.value.value, ast.Name)
            and part.value.value.id == "pytest"
            for part in ast.walk(node.value)
        )
    return False


def pytest_sessionstart(session):
    _ASSERTED.clear()
    _COLLECTION_SKIPPED.clear()
    _SKIPPED.clear()
    _XPASSED.clear()


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(session, config, items):
    """Active acceptance is the whole suite: a collected test without the marker
    would run outside `-m v31`, where nothing checks it (plan §12)."""
    unmarked = sorted(item.nodeid for item in items if item.get_closest_marker("v31") is None)
    if unmarked:
        raise pytest.UsageError(
            "every collected test must carry pytest.mark.v31; unmarked: "
            + ", ".join(unmarked[:10])
            + (f" (+{len(unmarked) - 10} more)" if len(unmarked) > 10 else "")
        )


def _is_gated(item) -> bool:
    return any(item.get_closest_marker(marker) is not None for marker in GATE_MARKERS)


def pytest_assertion_pass(item, lineno, orig, expl):
    if _is_gated(item):
        _ASSERTED.add(item.nodeid)


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
