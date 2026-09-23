"""Reference precondition for run_report; not a production CLI or certificate issuer.
Checks exact campaign keys, bindings and artifact bytes. Production must additionally
validate score schemas, slot identities, numerical invariants and gate attestations.
"""
from pathlib import Path
import hashlib
import json

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def expected_keys(cfg):
    fits={(c['id'],b['block_key'],s,a) for c in cfg['cells'] for s in c['seeds'] for b in cfg['blocks'] for a in c['arms']}
    docs={r['canonical_doc_id'] for r in cfg['registry'] if r['role']=='probe'}
    probes={(c['id'],b['block_key'],s,a,d) for c in cfg['cells'] if c['id'] in cfg['probe_cells'] for s in c['seeds'] for b in cfg['blocks'] for a in c['arms'] for d in docs}
    return fits,probes,set(cfg['jsd_variants'])

def require_report_ready(cfg, bindings, certificates, manifest, artifact_dir):
    """Raise ValueError before the caller computes any group contrast."""
    design_path=Path(__file__).with_name('hexis_v3_design.json')
    if digest(design_path)!=bindings.get('design_sha256') or json.loads(design_path.read_text())!=cfg:
        raise ValueError('design bytes or parsed configuration mismatch')
    if set(bindings)!={'design_sha256','implementation_commit','lock_sha256'} or not all(isinstance(v,str) and v for v in bindings.values()):
        raise ValueError('missing bindings')
    if set(certificates)!={'V0','V1','V2','V3'}:
        raise ValueError('missing gate')
    for stage,c in certificates.items():
        if c.get('stage')!=stage or c.get('status')!='PASS' or c.get('bindings')!=bindings:
            raise ValueError('invalid or stale certificate')
    if manifest.get('bindings')!=bindings:
        raise ValueError('stale campaign')
    expected=expected_keys(cfg)
    artifacts=manifest.get('artifacts',{})
    if not artifacts:raise ValueError('missing artifacts')
    root=Path(artifact_dir).resolve()
    for name,sha in artifacts.items():
        p=(root/name).resolve()
        if Path(name).is_absolute() or not p.is_relative_to(root) or not p.is_file() or digest(p)!=sha:
            raise ValueError('missing, unsafe or corrupted artifact')
    for kind,wanted in zip(('fits','probes','roots'),expected):
        rows=manifest.get(kind,[]);actual=[]
        for r in rows:
            key=r.get('key')
            if kind!='roots':
                if not isinstance(key,list):raise ValueError('invalid key')
                key=tuple(key)
            if r.get('status')!='PASS' or r.get('artifact') not in artifacts:
                raise ValueError('unverified record')
            actual.append(key)
        if len(actual)!=len(wanted) or set(actual)!=wanted:
            raise ValueError('missing, duplicate or unexpected '+kind)
    return {'status':'PASS','fits':len(expected[0]),'probes':len(expected[1]),'root_variants':len(expected[2])}
