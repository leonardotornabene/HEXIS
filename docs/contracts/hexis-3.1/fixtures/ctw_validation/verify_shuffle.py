"""Same CTW under within-stream order destruction, a diagnostic not a p-value."""
import json,time,math
from pathlib import Path
import numpy as np
from ctw import CTW
from pilot import load_data,fold_data
from verify_synthetic import generate
ROOT=Path(__file__).resolve().parent

def shuffled(ss,seed):
    r=np.random.default_rng(seed)
    return [r.permutation(s).tolist() for s in ss]

def pair(train,test,m,seed):
    st=shuffled(train,800000+seed);se=shuffled(test,900000+seed)
    t=CTW(m).fit(train);c=CTW(m).fit(st)
    assert t.nodes[0].counts==c.nodes[0].counts
    r=t.evaluate(test);s=c.evaluate(se)
    assert r['n_eval']==s['n_eval']
    return {'observed':r,'shuffled':s,'excess_gain_diagnostic':r['gain']-s['gain']}

def main():
    out={'synthetic':[],'real':[]}
    for seed in range(3):
        rng=np.random.default_rng(9723+seed)
        blocks=[(rng.random(8884)<p).astype(int).tolist() for p in [.1,.1,.1,.9,.9,.9,.9]]
        for held in [0,6]:
            p=.1 if held==0 else .9
            te=(np.random.default_rng(72931+seed+held).random(100000)<p).astype(int).tolist()
            res=pair([b for i,b in enumerate(blocks) if i!=held],[te],2,seed+100*held)
            out['synthetic'].append({'source':'heterogeneous_iid','seed':seed,'held':held,**res})
        train,_=generate('lag2',53304,seed);test,_=generate('lag2',100000,10000+seed)
        out['synthetic'].append({'source':'lag2','seed':seed,**pair([train],[test],2,seed)})
    blocks,probe,meta=load_data()
    for held in sorted(blocks):
        tr,te,led=fold_data(blocks,held,0,8884)
        # One diagnostic permutation at the fixed pilot seed: feasibility, not a calibrated null.
        t0=time.perf_counter();res=pair(tr,te,meta['m'],int(held[1:])+321)
        out['real'].append({'held':held,'seconds':time.perf_counter()-t0,**res})
        (ROOT/'shuffle_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({'synthetic':[(r['source'],r['excess_gain_diagnostic']) for r in out['synthetic']],
                      'real_excess_range':[min(r['excess_gain_diagnostic'] for r in out['real']),max(r['excess_gain_diagnostic'] for r in out['real'])]}))

if __name__=='__main__':main()
