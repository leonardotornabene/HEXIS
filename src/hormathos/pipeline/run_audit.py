"""HORMATHOS corpus audit: read, validate and census the three pinned inputs."""
from hormathos.pipeline.corpus_run import main as _main


def main(argv=None):
    return _main('audit', argv)


if __name__ == '__main__':
    main()
