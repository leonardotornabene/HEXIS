#!/usr/bin/env python3
"""Minimal, dependency-free test runner.

The test files under tests/ are plain pytest-style modules (functions named
``test_*`` using bare ``assert``). In an environment with pytest installed,
run ``pytest tests/`` instead; this runner exists only so the suite can be
executed with the standard library alone.
"""

from __future__ import annotations

import importlib.util
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def discover_and_run() -> int:
    test_files = sorted((ROOT / "tests").glob("test_*.py"))
    passed, failed = 0, 0
    failures: list[tuple[str, str]] = []
    t0 = time.time()
    for path in test_files:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        for name in sorted(dir(module)):
            if not name.startswith("test_"):
                continue
            fn = getattr(module, name)
            if not callable(fn):
                continue
            label = f"{path.stem}::{name}"
            try:
                fn()
            except Exception:
                failed += 1
                failures.append((label, traceback.format_exc()))
                print(f"FAIL {label}")
            else:
                passed += 1
                print(f"ok   {label}")
    dt = time.time() - t0
    print(f"\n{passed} passed, {failed} failed in {dt:.2f}s")
    for label, tb in failures:
        print(f"\n--- {label} ---\n{tb}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(discover_and_run())
