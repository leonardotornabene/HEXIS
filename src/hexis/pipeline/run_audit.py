"""HEXIS 3.1 corpus audit; historical v2.1 audit is isolated in legacy_audit."""
from hexis.pipeline.corpus_run import main as _main


def main(argv=None):
    return _main('audit', argv)


if __name__ == '__main__':
    main()
