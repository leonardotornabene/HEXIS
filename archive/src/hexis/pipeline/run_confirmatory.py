"""Stage run_confirmatory: retired from the HEXIS 3.1 destination (piano §13.2).

This entry point carried P1/P2 confirmatory inference and the S1 secondary reading under
the v2.1 design. HEXIS 3.1 is descriptive and finite-corpus: it declares no inference at
all (piano §1, §13.1), so there is no confirmatory stage to run.

The module is kept so the retirement is readable where the obligation used to
be; it is called by nothing and it produces nothing.
"""


def main(argv=None) -> None:
    raise SystemExit(
        'run_confirmatory: retired in HEXIS 3.1 and part of no stage sequence; the active entry '
        'points are run_audit, run_encode, run_tree_validation, run_descriptive and '
        'run_report (piano §14.1)')


if __name__ == '__main__':
    main()
