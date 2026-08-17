"""Run-level artifact provenance (Spec §6.4; D26, D46).

One central manifest per run records the git commit, dirty flag,
resolved-config SHA-256, input hashes, package versions, timestamps, seed, and
every produced artifact with its SHA-256. Each artifact carries or is
accompanied by the minimal sidecar {run_id, sha256, entry_point}.

Interface not fixed in Spec §6.2; the signatures below are chosen under the P4
authorization and were ratified by the owner on 2026-07-27, as recorded in
docs/HANDOFF.md.
"""

import datetime
import hashlib
import json
import subprocess
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

_PINNED = ["numpy", "pandas", "pyarrow", "conllu", "scipy", "matplotlib", "pyyaml", "pytest"]


def sha256_file(path) -> str:
    """SHA-256 hex digest of a file's bytes, read in chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_state() -> dict:
    """Commit and dirty flag **at the moment of the call**.

    Public because *when* it is sampled is itself provenance: a stage that writes
    artifacts into the worktree and only then asks git would record a dirtiness
    its own outputs caused. Callers capture this before their first write and hand
    it to `build_manifest(git=…)`.
    """
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, check=True
        ).stdout
        return {"commit": commit, "dirty": bool(status.strip())}
    except (subprocess.CalledProcessError, OSError) as exc:
        raise RuntimeError(
            "git state unavailable; run from a Git worktree with git on PATH"
        ) from exc


def _package_versions() -> dict:
    out = {}
    for pkg in _PINNED:
        try:
            out[pkg] = version(pkg)
        except PackageNotFoundError:
            out[pkg] = None
    return out


def _file_records(paths) -> list[dict[str, str]]:
    return [
        {"path": str(path), "sha256": sha256_file(path)}
        for path in map(Path, paths)
    ]


def build_manifest(
    run_id: str,
    config_sha256: str,
    seed: int,
    artifacts,
    entry_point: str,
    *,
    inputs=(),
    input_records=None,
    alphabet_extension=None,
    git=None,
) -> dict:
    """Assemble the central run manifest (D46): provenance + artifact hashes.

    `alphabet_extension` records the run-time alphabet extension A⁺ that D52(x)
    requires the manifest to carry (P-BOUND arms). `None` omits the key, so
    P-RESET manifests are unchanged.

    `git` accepts a state captured earlier by `git_state()`. Artifacts have to
    exist before they can be hashed, so this function necessarily runs *after* the
    stage has written into the worktree; sampling git here would then attribute
    the run's own untracked outputs to the tree it started from. `None` keeps the
    previous behaviour of sampling at assembly time.

    `input_records` accepts digests taken before the inputs were parsed, for the
    same reason: hashing `inputs` here would describe the files as they are *now*,
    not as the run read them. It takes precedence over `inputs`; `None` keeps the
    previous behaviour.
    """
    record = {
        "run_id": run_id,
        "entry_point": entry_point,
        "seed": seed,
        "config_sha256": config_sha256,
        "git": git if git is not None else git_state(),
        "package_versions": _package_versions(),
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "inputs": list(input_records) if input_records is not None else _file_records(inputs),
        "artifacts": _file_records(artifacts),
    }
    if alphabet_extension is not None:
        record["alphabet_extension"] = alphabet_extension
    return record


def _write_json_no_overwrite(dest: Path, payload: dict, force: bool) -> Path:
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)
    if force:
        dest.write_text(content, encoding="utf-8")
        return dest
    try:
        with dest.open("x", encoding="utf-8") as stream:
            stream.write(content)
    except FileExistsError:
        raise FileExistsError(
            f"refusing to overwrite {dest} without force=True (§6.4)"
        ) from None
    return dest


def write_manifest(manifest: dict, results_root, force: bool = False) -> Path:
    """Write the manifest to ``{results_root}/logs/{run_id}/manifest.json`` (§6.4)."""
    dest = Path(results_root) / "logs" / manifest["run_id"] / "manifest.json"
    return _write_json_no_overwrite(dest, manifest, force)


def sidecar(run_id: str, sha256: str, entry_point: str) -> dict:
    """The minimal per-artifact sidecar payload (D46)."""
    return {"run_id": run_id, "sha256": sha256, "entry_point": entry_point}


def write_sidecar(artifact_path, run_id: str, entry_point: str, force: bool = False) -> Path:
    """Write ``{artifact}.sidecar.json`` with the minimal {run_id, sha256, entry_point}."""
    artifact_path = Path(artifact_path)
    payload = sidecar(run_id, sha256_file(artifact_path), entry_point)
    dest = artifact_path.with_suffix(artifact_path.suffix + ".sidecar.json")
    return _write_json_no_overwrite(dest, payload, force)
