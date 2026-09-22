"""Stage run_null_calibration: retired from the HEXIS 3.1 destination (piano §13.2).

This entry point carried the empirical type-I calibration of the P1 chain (O7/sign-flip)
under the v2.1 design. With no inferential claim there is no null to calibrate and no
sign-flip to resolve: O7 and the v2.1 gates G0–G7 are declared not applicable to 3.1
(piano §13.1), not silently satisfied.

The module is kept so the retirement is readable where the obligation used to
be; it is called by nothing and it produces nothing.
"""


def main(argv=None) -> None:
    raise SystemExit(
        'run_null_calibration: retired in HEXIS 3.1 and part of no stage sequence; the active entry '
        'points are run_audit, run_encode, run_tree_validation, run_descriptive and '
        'run_report (piano §14.1)')


if __name__ == '__main__':
    main()
