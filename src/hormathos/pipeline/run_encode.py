"""HORMATHOS corpus encoding and verified sentence/coordinate artifacts."""
from hormathos.pipeline.corpus_run import main as _main


def main(argv=None):
    return _main('encode', argv)


if __name__ == '__main__':
    main()
