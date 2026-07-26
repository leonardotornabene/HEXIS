"""Root pytest configuration: G0 gate enforcement + pytester enablement.

Mechanizes the D45 / D52(iii) criterion — engineering only, no methodological
content. The session exits non-zero if any ``g0``-marked test is skipped
(statically or via a dynamic ``pytest.skip``) or xfailed; ``xfail_strict`` and
``--strict-markers`` (pyproject) handle xpass and unregistered markers; the AST
meta-test in ``tests/test_g0_enforcement.py`` rejects assertion-free g0 tests.
Nothing here reads the pytest summary by eye.

Located at the repository root because ``pytest_plugins`` (``pytester``, used by
the enforcement self-tests) is honoured only in the root conftest.
"""

pytest_plugins = ["pytester"]

_SKIPPED_G0: set[str] = set()


def pytest_runtest_logreport(report):
    if report.skipped and "g0" in report.keywords:
        _SKIPPED_G0.add(report.nodeid)


def pytest_sessionfinish(session, exitstatus):
    if not _SKIPPED_G0:
        return
    reporter = session.config.pluginmanager.getplugin("terminalreporter")
    if reporter is not None:
        reporter.write_line(
            "G0 GATE FAILURE — skipped/xfail g0 test(s): " + ", ".join(sorted(_SKIPPED_G0)),
            red=True,
        )
    if session.exitstatus == 0:
        session.exitstatus = 1
