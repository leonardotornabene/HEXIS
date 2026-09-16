"""Check whether pooled context gain uniquely identifies within-document dependence."""
from pathlib import Path
import json
import numpy as np
from ctw import CTW

def main():
    rows=[]
    for seed in range(3):
      r=np.random.default_rng(9723+seed)
      blocks=[(r.random(8884)<p).astype(int).tolist() for p in [.1,.1,.1,.9,.9,.9,.9]]
      for held in [0,6]:
        p=.1 if held==0 else .9
        test=(np.random.default_rng(72931+seed+held).random(100000)<p).astype(int).tolist()
        pooled=CTW(2,8).fit([b for i,b in enumerate(blocks) if i!=held]).evaluate([test])
        homogeneous=CTW(2,8).fit([b for i,b in enumerate(blocks) if i!=held and (i<3)==(held<3)]).evaluate([test])
        rows.append({'seed':seed,'held_probability1':p,'pooled':pooled,'same_distribution':homogeneous})
    Path(__file__).with_name('heterogeneity_results.json').write_text(json.dumps(rows,indent=2))
    print(json.dumps({'rows':len(rows),'pooled_gain_range':[min(r['pooled']['gain'] for r in rows),max(r['pooled']['gain'] for r in rows)],'homogeneous_gain_range':[min(r['same_distribution']['gain'] for r in rows),max(r['same_distribution']['gain'] for r in rows)]}))

if __name__=='__main__':main()
