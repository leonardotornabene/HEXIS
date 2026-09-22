"""HEXIS 3.1 corpus audit: read, validate and census the three pinned inputs."""
from hexis.pipeline.corpus_run import main as _main


def main(argv=None):
    return _main('audit', argv)


if __name__ == '__main__':
    main()
