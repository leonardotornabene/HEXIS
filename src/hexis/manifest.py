"""Run-level artifact provenance (Spec §6.4; D26, D46).

One central manifest per run records the git commit, dirty flag,
resolved-config SHA-256, input hashes, package versions, timestamps, seed, and
every produced artifact with its SHA-256. Each artifact carries or is
accompanied by the minimal sidecar {run_id, sha256, entry_point}.

Interface not specified in Spec §6.2; signatures will be proposed for approval
before implementation — no invented contracts.
"""
