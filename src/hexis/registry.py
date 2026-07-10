"""Document registry: doc_id derivation and regime assignment (Spec §2.3, §3.3; D03, D04)."""


def build_registry(prefix_counts, overrides):
    """Build the document registry from sent_id prefixes + human-verified overrides.

    G1 procedure (Spec §3.3): enumerate sent_id prefixes with sentence/token
    counts; apply config/registry_overrides.yaml assignments (author, work,
    regime, meter, period, flags), cross-checked against Spec §2.3; fail on any
    unassigned sentence. Registry schema per Spec §2.3. Exact signature
    finalized at implementation (Fase 1).
    """
    raise NotImplementedError
