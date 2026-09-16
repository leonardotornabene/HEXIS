import math, json, time, gc, resource
from pathlib import Path
import numpy as np
from ctw import CTW
OUT=Path(__file__).resolve().parent

def generate(kind,n,seed,m=2):
    r=np.random.default_rng(seed)
    if kind=='iid': return r.integers(m,size=n).tolist(),math.log2(m)
    if kind=='cycle': return (np.arange(n)%m).tolist(),0.
    x=r.integers(m,size=n).tolist(); prob=r.random(n)
    if kind=='order1':
        for i in range(1,n): x[i]=x[i-1] if prob[i]<.8 else 1-x[i-1]
        target=-.8*math.log2(.8)-.2*math.log2(.2)
    elif kind=='lag2':
        for i in range(2,n): x[i]=x[i-2] if prob[i]<.9 else 1-x[i-2]
        target=-.9*math.log2(.9)-.1*math.log2(.1)
    elif kind=='variable':
        # Context 0 -> Bernoulli .2; context 01 -> .1; context 11 -> .9.
        ll=[]
        for i in range(2,n):
            p=.2 if x[i-1]==0 else (.1 if x[i-2]==0 else .9)
            x[i]=int(prob[i]<p); ll.append(-math.log2(p if x[i] else 1-p))
        target=sum(ll)/len(ll)
    elif kind=='lag2_full':
        for i in range(2,n): x[i]=x[i-2] if prob[i]<.9 else x[i]
        p=.9+.1/m; target=-p*math.log2(p)-(m-1)*(.1/m)*math.log2(.1/m)
    elif kind=='lag2_core':
        # 90% frequent binary core; 10% rare independent symbols.
        z=r.integers(2,size=n).tolist()
        for i in range(2,n): z[i]=z[i-2] if prob[i]<.9 else 1-z[i-2]
        rare=r.random(n)<.1
        x=[int(r.integers(2,m)) if rare[i] else z[i] for i in range(n)]
        target=None
    else: raise ValueError(kind)
    return x,target

def main():
    rows=[]
    cases=[('iid',4),('cycle',3),('order1',2),('lag2',2),('variable',2),('iid',106),('lag2_full',106),('lag2_core',106)]
    for kind,m in cases:
      for seed in range(5 if m<106 else 3):
        x,_=generate(kind,53304,seed,m); y,target=generate(kind,100000,10000+seed,m)
        variants=[('C0',.5,.5,None)]
        if m==106: variants += [('a_total1',1/m,.5,None),('rho09',.5,.9,None),('rho_literature',.5,None,-(m-1)*math.log(2))]
        t0=time.perf_counter(); model=CTW(m).fit([x]); fitsec=time.perf_counter()-t0
        for cell,a,rho,logsplit in variants:
            model.reweight(a=a,rho=rho,log_split=logsplit)
            t0=time.perf_counter(); res=model.evaluate([y]); evalsec=time.perf_counter()-t0
            row={'kind':kind,'m':m,'seed':seed,'cell':cell,'target':target,'fit_s':fitsec,'eval_s':evalsec,**res,**model.diagnostics()}
            if kind in ['iid','cycle','order1','lag2','variable'] and m<106:
                row['analytic_pass']=abs(res['ce']-target)<(.02 if kind=='cycle' else .03)
            rows.append(row)
            print(kind,m,seed,cell,'CE',round(res['ce'],6),'root',round(res['root_ce'],6),'depth',round(res['weighted_depth'],3),flush=True)
        del model; gc.collect()
        (OUT/'synthetic_results.json').write_text(json.dumps({'rows':rows,'peak_rss_MiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024},indent=2))

if __name__=='__main__': main()
