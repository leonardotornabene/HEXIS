"""Independent all-tree enumeration and sequential leaf likelihood oracle."""
import itertools, math, json
from collections import Counter
from pathlib import Path
import numpy as np
from ctw import CTW

def trees(m,D,rho,path=()):
    if len(path)==D or (path and path[-1]==-1): return [(1.,(path,))]
    out=[(rho,(path,))]
    parts=[trees(m,D,rho,path+(j,)) for j in range(-1,m)]
    for combo in itertools.product(*parts):
        out.append(((1-rho)*math.prod(p for p,l in combo),sum((l for p,l in combo),())))
    return out

def leaf_for(leaves,hist,D):
    context=tuple(reversed(hist[-D:] if D else []))+(-1,)
    return next(s for s in leaves if context[:len(s)]==s)

def oracle(streams,m,D,a,rho):
    models=[]
    for prior,leaves in trees(m,D,rho):
        counts={s:Counter() for s in leaves}; prob=prior
        for seq in streams:
            for i,x in enumerate(seq):
                s=leaf_for(leaves,seq[:i],D); c=counts[s]
                prob*=(c[x]+a)/(sum(c.values())+m*a); c[x]+=1
        models.append((prob,leaves,counts))
    z=math.fsum(p for p,_,_ in models)
    def predict(hist,x):
        return math.fsum(p*(c[leaf_for(l,hist,D)][x]+a)/(sum(c[leaf_for(l,hist,D)].values())+m*a) for p,l,c in models)/z
    return z,predict

def main():
    rng=np.random.default_rng(1321); errors=[]; assertions=0
    for m,D in [(2,0),(2,1),(2,2),(2,3),(3,2)]:
      for a,rho in [(.5,.5),(1/m,.9),(.2,.1)]:
       assert abs(sum(p for p,l in trees(m,D,rho))-1)<1e-12
       for k in range(8):
        ss=[rng.integers(m,size=int(rng.integers(0,9))).tolist() for _ in range(3)]
        t=CTW(m,D,a,rho).fit(ss); z,p=oracle(ss,m,D,a,rho)
        errors.append(abs(t.nodes[0].lw-math.log(z)))
        assert errors[-1]<1e-10
        for n in range(D+2):
          for h in itertools.product(range(m),repeat=n):
            probs=[t.predict(h,x) for x in range(m)]
            assert abs(sum(probs)-1)<1e-12; assertions+=1
            for x,pr in enumerate(probs):
                err=abs(pr-p(h,x)); errors.append(err)
                assert err<1e-11; assertions+=1
        before=t.fingerprint(); t.evaluate([[0,1,0,1,1]],min_past=0)
        assert before==t.fingerprint(); assertions+=1
        tr=CTW(m,D,a,rho).fit(ss[::-1]); assert t.fingerprint()==tr.fingerprint(); assertions+=1
        perm=rng.permutation(m); tp=CTW(m,D,a,rho).fit([[int(perm[x]) for x in s] for s in ss])
        for h in [[],[0],[0,1],[0,1,0,1]]:
            for x in range(m):
                assert abs(t.predict(h,x)-tp.predict([int(perm[x]) for x in h],int(perm[x])))<1e-11; assertions+=1
    # Prequential identity, using complete refits on every prefix (not an update helper).
    seq=rng.integers(3,size=45).tolist(); loss=0.
    for i,x in enumerate(seq):
        tt=CTW(3,3).fit([seq[:i]])
        loss-=math.log(tt.predict(seq[:i],x))
    final=CTW(3,3).fit([seq]); err=abs(loss+final.nodes[0].lw)
    assert err<1e-10
    # Counter partition including start-of-sentence leaf at every nonterminal.
    for nd in final.nodes:
        if not nd.terminal:
            total=Counter()
            for j in nd.children.values(): total.update(final.nodes[j].counts)
            assert total==nd.counts; assertions+=1
    # Empty alphabet-support outcomes and entirely unseen histories remain proper.
    for a in [.5,1/106]:
        t=CTW(106,8,a).fit([[0,1]*100])
        for h in [[],[105],[105]*8,[0,1]*4]:
            ps=[t.predict(h,x) for x in range(106)]
            assert min(ps)>0 and abs(sum(ps)-1)<1e-11; assertions+=1
    logsp=-105*math.log(2)
    assert 1.-2.**-105==1. # naive construction really rounds to one
    t=CTW(106,8,log_split=logsp).fit([[0,1]*100])
    assert math.isfinite(t.nodes[0].lw) and math.isfinite(t.lsplit)
    out={'status':'PASS','enumeration_cases':120,'assertions':assertions,
         'max_enumeration_error':max(errors),'prequential_identity_error':err,
         'naive_rho106_rounds_to_one':True,'log_split106':logsp}
    Path(__file__).with_name('exact_results.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out))

if __name__=='__main__': main()
