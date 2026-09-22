"""Stage run_reference: retired from the HEXIS 3.1 destination (piano §13.2).

This entry point carried the protocol-(a) reference models and their descriptive
readings under the v2.1 design. The 3.1 instrument is one CTW pair per fold (piano §6):
no reference network, no context lexicon, no gain curve and no learning curve (§11.6).

The module is kept so the retirement is readable where the obligation used to
be; it is called by nothing and it produces nothing.
"""


def main(argv=None) -> None:
    raise SystemExit(
        'run_reference: retired in HEXIS 3.1 and part of no stage sequence; the active entry '
        'points are run_audit, run_encode, run_tree_validation, run_descriptive and '
        'run_report (piano §14.1)')


if __name__ == '__main__':
    main()
