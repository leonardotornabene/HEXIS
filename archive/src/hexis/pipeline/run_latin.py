"""Stage run_latin: retired from the HEXIS 3.1 destination (piano §13.2).

This entry point carried the Latin replication L1 and its matched Greek subsampling
under the v2.1 design. HEXIS 3.1 studies the fixed Greek corpus alone (piano §2): Latin
is outside the declared scope, not postponed inside it.

The module is kept so the retirement is readable where the obligation used to
be; it is called by nothing and it produces nothing.
"""


def main(argv=None) -> None:
    raise SystemExit(
        'run_latin: retired in HEXIS 3.1 and part of no stage sequence; the active entry '
        'points are run_audit, run_encode, run_tree_validation, run_descriptive and '
        'run_report (piano §14.1)')


if __name__ == '__main__':
    main()
