"""Fault-injection checks on synthetic manifest fixtures, not final study results."""
from pathlib import Path
import copy,hashlib,json,tempfile
from report_contract import expected_keys,require_report_ready
HERE=Path(__file__).resolve().parent
cfg=json.loads((HERE/'hexis_v3_design.json').read_text())
bind={'design_sha256':hashlib.sha256((HERE/'hexis_v3_design.json').read_bytes()).hexdigest(),'implementation_commit':'synthetic-fixture-commit','lock_sha256':hashlib.sha256(b'fixture lock').hexdigest()}
cert={s:{'stage':s,'status':'PASS','bindings':dict(bind)} for s in ('V0','V1','V2','V3')}
checks=[]
with tempfile.TemporaryDirectory() as td:
    p=Path(td)/'fixture.json';p.write_text('{"fixture":true}\n');sha=hashlib.sha256(p.read_bytes()).hexdigest()
    m={'bindings':dict(bind),'artifacts':{'fixture.json':sha}}
    for kind,keys in zip(('fits','probes','roots'),expected_keys(cfg)):
        m[kind]=[{'key':list(k) if isinstance(k,tuple) else k,'status':'PASS','artifact':'fixture.json'} for k in sorted(keys)]
    assert require_report_ready(cfg,bind,cert,m,td)=={'status':'PASS','fits':1400,'probes':1680,'root_variants':3}
    checks.append('complete_synthetic_fixture')
    def reject(name,mm=None,cc=None):
        try:require_report_ready(cfg,bind,cc if cc is not None else cert,mm if mm is not None else m,td)
        except ValueError:checks.append(name)
        else:raise AssertionError(name+' accepted')
    for kind in ('fits','probes','roots'):
        x=copy.deepcopy(m);x[kind].pop();reject('missing_'+kind,x)
        x=copy.deepcopy(m);x[kind][-1]=x[kind][0];reject('duplicate_'+kind,x)
        x=copy.deepcopy(m);x[kind][0]['status']='FAIL';reject('failed_'+kind,x)
    x=copy.deepcopy(m);x['fits']=[r for r in x['fits'] if r['key'][0]!='D12'];reject('missing_cell',x)
    x=copy.deepcopy(m);x['fits'][0]['key'][2]=999;reject('unexpected_seed',x)
    x=copy.deepcopy(m);x['bindings']['design_sha256']='stale';reject('stale_campaign',x)
    for stage in cert:
        cc=copy.deepcopy(cert);del cc[stage];reject('missing_'+stage,cc=cc)
        cc=copy.deepcopy(cert);cc[stage]['bindings']['implementation_commit']='stale';reject('stale_'+stage,cc=cc)
    for field in ('design_sha256','lock_sha256'):
        cc=copy.deepcopy(cert);cc['V3']['bindings'][field]='stale';reject('stale_'+field,cc=cc)
    x=copy.deepcopy(m);x['fits'][0]['artifact']='missing.json';reject('unverified_artifact_reference',x)
    p.write_text('corrupted');reject('corrupted_bytes')
    p.unlink();reject('missing_bytes')
(HERE/'report_validation.json').write_text(json.dumps({'status':'PASS','scope':'synthetic manifest fixtures only; not V0-V3 certification or final campaign execution','checks':checks},indent=2)+'\n')
print('report contract PASS',len(checks),'checks')
