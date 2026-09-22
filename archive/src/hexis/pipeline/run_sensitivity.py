"""Stage run_sensitivity: retired from the HEXIS 3.1 destination (piano §13.2).

This entry point carried the separate sensitivity orchestrator under the v2.1 design.
The five sensitivity cells are selected by the one executor, `run_descriptive.py --cell
<name>` (piano §13.2, §14.1): no second orchestrator.

The module is kept so the retirement is readable where the obligation used to
be; it is called by nothing and it produces nothing.
"""


def main(argv=None) -> None:
    raise SystemExit(
        'run_sensitivity: retired in HEXIS 3.1 and part of no stage sequence; the active entry '
        'points are run_audit, run_encode, run_tree_validation, run_descriptive and '
        'run_report (piano §14.1)')


if __name__ == '__main__':
    main()
