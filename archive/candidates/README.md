# candidates/ — quarantined, non-canonical (D47)

Nothing here is part of the HEXIS pipeline. `src/hexis` must never import from
this directory, and pytest must never collect from it (`norecursedirs` in
`pyproject.toml`).

## hexis-ctree v0.1.0 (session artifact, 2026-07-07)

Pure-Python candidate context-tree implementation with its own test runner
(`run_tests.py`; not pytest). Ingested as evidence, not as code in use.

Promotion to `src/hexis/model/context_tree.py` requires BOTH (D47):
 (a) conformance to Spec §4.1–4.3, or to a ratified amendment; and
 (b) passing the four analytic targets of §4.7 at G3.

Neither condition is met today. `ASSUMPTIONS.pdf` §B3 declares a deviation from
the §4.1 growth policy, filed as amendment D18-A1 (PROPOSED, not ratified;
decision at the Phase-2 mathematical-supervisor touchpoint). Its own suite
covers only one of the four §4.7 targets at the Spec's parameters.

Caution: the value 0.4690 bits appears in this package as an order-1 Markov
result (p_stay = 0.9). It is NOT the §4.7 order-2 XOR target, which happens to
share the same number because H(0.9) = H(0.1). The XOR fixture is absent.
