"""Determinism & provenance tests (Spec §7, gate G0; §6.3, §6.4/D46).

Config/manifest signatures were not fixed in §6.2 ("proposed before
implementation"); chosen here under the P4 authorization and recorded in
docs/HANDOFF.md as PROPOSED interfaces awaiting ratification.
"""

import hashlib
import json

import pytest

from hexis.config import config_hash, derive_seed, load_config, resolve_config
from hexis.manifest import build_manifest, sha256_file, write_manifest, write_sidecar


@pytest.mark.g0
def test_seed_derivation_matches_spec_formula():
    # derived seed = global XOR crc32(analysis_id.utf-8)  (§6.3)
    assert derive_seed("P1", 20260706) == 2877909235
    assert derive_seed("P2", 20260706) == 847264073
    assert derive_seed("P1", 20260706) == derive_seed("P1", 20260706)  # deterministic
    assert derive_seed("P1", 20260706) != derive_seed("P2", 20260706)  # analysis-specific
    assert 0 <= derive_seed("anything", 20260706) < 2**32


@pytest.mark.g0
def test_load_config_reads_frozen_defaults():
    cfg = load_config()
    assert cfg["seeds"]["global"] == 20260706
    assert cfg["blocks"]["n_block"] == 1000
    assert cfg["blocks"]["min_frac"] == 0.5
    assert cfg["context_tree"]["k_min"] == 2
    assert cfg["stats"]["family"] == ["P1", "P2"]


@pytest.mark.g0
def test_config_hash_canonical_and_sensitive():
    a = {"x": 1, "y": {"a": 1, "b": 2}}
    b = {"y": {"b": 2, "a": 1}, "x": 1}  # same content, different key order
    assert config_hash(a) == config_hash(b)  # canonicalized → key-order-independent
    assert config_hash(a) == hashlib.sha256(
        json.dumps(a, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    assert config_hash({"x": 2, "y": {"a": 1, "b": 2}}) != config_hash(a)  # value-sensitive
    assert len(config_hash(a)) == 64


@pytest.mark.g0
def test_resolve_config_deep_merges_without_mutating_base():
    base = {"a": 1, "nested": {"p": 1, "q": 2}}
    merged = resolve_config({"nested": {"q": 9}, "b": 3}, base=base)
    assert merged == {"a": 1, "b": 3, "nested": {"p": 1, "q": 9}}
    assert base == {"a": 1, "nested": {"p": 1, "q": 2}}  # base untouched


@pytest.mark.g0
def test_sha256_file_matches_hashlib(tmp_path):
    p = tmp_path / "a.bin"
    p.write_bytes(b"hello")
    assert sha256_file(p) == hashlib.sha256(b"hello").hexdigest()


@pytest.mark.g0
def test_build_manifest_carries_d46_fields_and_artifact_hashes(tmp_path):
    art = tmp_path / "scores.parquet"
    art.write_bytes(b"DATA")
    m = build_manifest("run-1", "cfg-sha", 2877909235, [art], "hexis.pipeline.run_x")
    for key in (
        "run_id", "entry_point", "seed", "config_sha256",
        "git", "package_versions", "created_utc", "artifacts",
    ):
        assert key in m
    assert m["git"].keys() >= {"commit", "dirty"}  # D46 git commit + dirty flag
    assert m["package_versions"]["conllu"] == "6.0.0"  # pinned env cross-check
    assert m["artifacts"] == [
        {"path": "scores.parquet", "sha256": hashlib.sha256(b"DATA").hexdigest()}
    ]


@pytest.mark.g0
def test_write_manifest_central_path_and_refuses_overwrite(tmp_path):
    m = build_manifest("run-1", "cfg-sha", 1, [], "hexis.pipeline.run_x")
    dest = write_manifest(m, tmp_path)
    assert dest == tmp_path / "logs" / "run-1" / "manifest.json"  # results/logs/{run_id}/ (§6.4)
    assert json.loads(dest.read_text())["run_id"] == "run-1"
    with pytest.raises(FileExistsError):
        write_manifest(m, tmp_path)  # no silent overwrite without --force
    assert write_manifest(m, tmp_path, force=True) == dest  # force allowed


@pytest.mark.g0
def test_write_sidecar_is_minimal_and_refuses_overwrite(tmp_path):
    art = tmp_path / "scores.parquet"
    art.write_bytes(b"DATA")
    side = write_sidecar(art, "run-1", "hexis.pipeline.run_x")
    assert side == tmp_path / "scores.parquet.sidecar.json"
    payload = json.loads(side.read_text())
    assert payload == {
        "run_id": "run-1",
        "sha256": hashlib.sha256(b"DATA").hexdigest(),
        "entry_point": "hexis.pipeline.run_x",
    }
    assert set(payload) == {"run_id", "sha256", "entry_point"}  # minimal, no metadata dup (D46)
    with pytest.raises(FileExistsError):
        write_sidecar(art, "run-1", "hexis.pipeline.run_x")
