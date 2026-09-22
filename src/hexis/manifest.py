"""File digests and pinned package versions.

The run manifest itself is written by the 3.1 stages (§11.7): what is left here
is what they read — the digest of a file's bytes and the versions of the pinned
packages, both of which enter the run identity.
"""

import hashlib
from importlib.metadata import PackageNotFoundError, version

_PINNED = ["numpy", "pandas", "pyarrow", "conllu", "scipy", "matplotlib", "pyyaml", "pytest"]


def sha256_file(path) -> str:
    """SHA-256 hex digest of a file's bytes, read in chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _package_versions() -> dict:
    out = {}
    for pkg in _PINNED:
        try:
            out[pkg] = version(pkg)
        except PackageNotFoundError:
            out[pkg] = None
    return out
