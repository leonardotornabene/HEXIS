import sys, json, math, copy, itertools
from pathlib import Path
from statistics import mean, stdev
from fractions import Fraction as F
sys.path.insert(0, sys.argv[1])
import numpy as np
from ctw_reference import CTW, logadd
from resolved_diagnostics import resolved
base=Path(sys.argv[2])
pilot=json.loads((base/'pilot_C0.json').read_text())['rows']
shuffle=json.loads((base/'shuffle_results.json').read_text())['real']
print('EVIDENCE COVERAGE',json.dumps({'original_C0':len(pilot),'shuffle_C0':len(shuffle),'shuffle_seeds_code':[0], 'other_pilots':{p.stem:len(json.loads(p.read_text())['rows']) for p in sorted(base.glob('pilot_*.json'))}}))
contrast=lambda rows:mean(r['gain'] for r in rows if r['held'] in ['B0','B1'])-mean(r['gain'] for r in rows if r['held'] not in ['B0','B1'])
dg=[contrast([r for r in pilot if r['seed']==s]) for s in range(20)]
print('DG',mean(dg),stdev(dg),min(dg),max(dg))
print('C0 root weights',sorted(set(r['root_stop'] for r in pilot)))
for name in ['D6','D12','rho09','rho_literature','bound','upos']:
    rows=json.loads((base/f'pilot_{name}.json').read_text())['rows']; orig=[r for r in pilot if r['seed']==0]
    print('PILOT DELTAS',name,[(r['held'],r['gain']-next(x for x in orig if x['held']==r['held'])['gain']) for r in rows])
# Independently enumerate the four depth-2 binary ordinary branches plus BOS.
def trees(path,D):
    if len(path)==D or path[-1:]==(-1,):return [(F(1),(path,))]
    ans=[(F(1,2),(path,))]
    for c in itertools.product(*(trees(path+(x,),D) for x in [-1,0,1])):
        ans.append((F(1,2)*math.prod(z[0] for z in c),sum((z[1] for z in c),())))
    return ans
ss=[[0,0,1],[1,0],[1]];mod=CTW(2,D=2).fit(ss);weighted=[]
for prior,leaves in trees((),2):
    counts={s:[0,0] for s in leaves};w=prior
    for seq in ss:
        for i,x in enumerate(seq):
            ctx=tuple(reversed(seq[max(0,i-2):i]))+(-1,)
            leaf=next(s for s in leaves if ctx[:len(s)]==s); cs=counts[leaf]
            w*=F(2*cs[x]+1,2*sum(cs)+2);cs[x]+=1
    weighted.append((w,leaves,counts))
z=sum(t[0] for t in weighted);err=0.
for n in range(4):
    for hist in itertools.product([0,1],repeat=n):
        ctx=tuple(reversed(hist[-2:]))+(-1,)
        for x in [0,1]:
            ans=F(0)
            for w,leaves,counts in weighted:
                s=next(s for s in leaves if ctx[:len(s)]==s);cs=counts[s]
                ans+=w*F(2*cs[x]+1,2*sum(cs)+2)
            err=max(err,abs(mod.predict(hist,x)-float(ans/z)))
assert err<1e-12
print('RATIONAL FROZEN ENUM',len(weighted),'prediction_max_error',err,'logevidence_error',abs(math.log(float(z))-mod.nodes[0].lw))
# de Bruijn sequence of order 9: dependencies genuinely exceed depth 8.
def debruijn(k,n):
    a=[0]*(k*n);seq=[]
    def db(t,p):
        if t>n:
            if n%p==0:seq.extend(a[1:p+1])
        else:
            a[t]=a[t-p];db(t+1,p)
            for j in range(a[t-p]+1,k):a[t]=j;db(t+1,t)
    db(1,1);return seq
seq=debruijn(2,9);tr=[seq*40];te=[seq*8]
models={d:CTW(2,D=d).fit(tr) for d in [6,8,12]}
print('DEEP SYNTHETIC', {d:models[d].evaluate(te,min_past=12)['ce'] for d in models})
# Derivation from count tree works ONLY after terminal flags and evidence reweighting.
truncated=copy.deepcopy(models[12]);truncated.D=8
for node in truncated.nodes:
    if node.depth==8:node.terminal=True
truncated.reweight()
maxerr=max(abs(truncated.predict(seq[i-8:i],seq[i])-models[8].predict(seq[i-8:i],seq[i])) for i in range(8,len(seq)))
print('TRUNCATION to D8 maxerror',maxerr)
# Changing rho genuinely changes finite-sample posterior and frozen prediction.
rng=np.random.default_rng(100);ss=[rng.integers(2,size=30).tolist()]
print('RHO EFFECT',[(r,CTW(2,D=3,rho=r).fit(ss).predict([0,0,0],1)) for r in [.1,.5,.9,.999999]])
print('FLOAT',{'rho105_is_one':1.-2.**-105==1.,'logsplit105':-105*math.log(2),'exp_minus37':math.exp(-37),'log1p_exp_minus37':math.log1p(math.exp(-37)), 'exp_minus745':math.exp(-745),'exp_minus746':math.exp(-746),'large_logadd_loses_delta25':logadd(-192272.7,-192272.7-25)==-192272.7})
# Mixture mass is distinct from responsibility for the actually observed symbol.
masses=resolved(mod,[0,0]); print('RESOLVED',masses)
# Defined finite-sample sensitivity cannot be universal threshold.
band={b:mean(r['past_buckets']['past8plus']['gain'] for r in pilot if r['held']==b) for b in [f'B{i}' for i in range(7)]}
print('PAST8 D_G',mean(band[b] for b in ['B0','B1'])-mean(band[b] for b in ['B2','B3','B4','B5','B6']))
print('SEED0 D_G/D_Q',contrast([r for r in pilot if r['seed']==0]),mean(r['excess_gain_diagnostic'] for r in shuffle if r['held'] in ['B0','B1'])-mean(r['excess_gain_diagnostic'] for r in shuffle if r['held'] not in ['B0','B1']))
print('ALLCELLS fit budget6',2*7*(20+5*10),'count builders if optimized',2*7*20+2*7*10*3)
q=mod.predict([0,0],1);w2=masses['mass_by_lexical_length'][2];p2=.75
print('MASS VS RESPONSIBILITY',{'depth2_mass':w2,'local_p1':p2,'full_p1':q,'depth2_responsibility':w2*p2/q})
