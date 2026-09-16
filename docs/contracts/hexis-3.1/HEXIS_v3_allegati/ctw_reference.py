"""Isolated multi-symbol CTW reference prototype. No HEXIS source imports.

All log evidence uses natural logs internally; external losses use bits.
Context edges follow newest-to-oldest history. BOS=-1 is context-only and
forces a leaf. Its counts partition sentence-initial cases exactly.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from math import exp, log, log1p, lgamma, fsum
import hashlib
import numpy as np

@dataclass(slots=True)
class Node:
    counts: dict = field(default_factory=dict)
    children: dict = field(default_factory=dict)
    n: int = 0
    depth: int = 0
    terminal: bool = False
    le: float = 0.
    lw: float = 0.
    stop: float = 1.

def logadd(a,b):
    hi,lo=(a,b) if a>=b else (b,a)
    return hi+log1p(exp(lo-hi))

class CTW:
    def __init__(self,m,D=8,a=.5,rho=.5,log_split=None):
        if m<2 or D<0 or a<=0: raise ValueError('invalid model parameters')
        self.m,self.D,self.a=int(m),int(D),float(a)
        if log_split is None:
            if not 0<rho<1: raise ValueError('rho must be in (0,1)')
            self.lstop,self.lsplit=log(rho),log1p(-rho)
        else:
            if not log_split<0: raise ValueError('invalid log split prior')
            self.lsplit=float(log_split)
            self.lstop=log1p(-exp(log_split))
        self.nodes=[Node(terminal=D==0)]

    def fit(self,streams):
        self.nodes=[Node(terminal=self.D==0)]
        for seq in streams:
            hist=[]
            for x in seq:
                x=int(x)
                if x==-2: # supplied sentence separator, context only
                    hist.append(x)
                    if len(hist)>self.D: del hist[0]
                    continue
                if not 0<=x<self.m: raise ValueError('outcome outside frozen alphabet')
                path=[0]; idx=0
                for edge in list(reversed(hist))+[-1]:
                    if self.nodes[idx].terminal: break
                    ch=self.nodes[idx].children
                    if edge not in ch:
                        child=len(self.nodes); ch[edge]=child
                        depth=self.nodes[idx].depth+1
                        self.nodes.append(Node(depth=depth,terminal=edge==-1 or depth==self.D))
                    idx=ch[edge]; path.append(idx)
                for idx in path:
                    node=self.nodes[idx]; node.n+=1
                    node.counts[x]=node.counts.get(x,0)+1
                hist.append(x)
                if len(hist)>self.D: del hist[0]
        self.reweight()
        return self

    def reweight(self,a=None,rho=None,log_split=None):
        if a is not None:
            if a<=0: raise ValueError('a must be positive')
            self.a=float(a)
        if rho is not None:
            if not 0<rho<1: raise ValueError('rho must be in (0,1)')
            self.lstop,self.lsplit=log(rho),log1p(-rho)
        if log_split is not None:
            self.lsplit=log_split; self.lstop=log1p(-exp(log_split))
        a=self.a; base=lgamma(self.m*a); ga=lgamma(a)
        for node in reversed(self.nodes):
            node.le=base-lgamma(node.n+self.m*a)+fsum(lgamma(c+a)-ga for c in node.counts.values())
            if node.terminal:
                node.lw=node.le; node.stop=1.
            else:
                sl=self.lstop+node.le
                sp=self.lsplit+fsum(self.nodes[j].lw for j in node.children.values())
                node.lw=logadd(sl,sp)
                node.stop=min(1.,exp(sl-node.lw))
        return self

    def predict(self,history,x,diagnostic=False):
        x=int(x)
        if not 0<=x<self.m: raise ValueError('outcome outside frozen alphabet')
        edges=list(reversed(history[-self.D:] if self.D else []))+[-1]
        idx=0; prob=0.; remaining=1.; expected_depth=0.; matched=0; unseen=0.
        for depth in range(self.D+1):
            node=self.nodes[idx]
            w=remaining*node.stop
            prob+=w*(node.counts.get(x,0)+self.a)/(node.n+self.m*self.a)
            expected_depth+=w*min(depth,len(history)) # BOS itself is not a past token
            remaining*=1.-node.stop
            matched=min(depth,len(history))
            if node.terminal: break
            edge=edges[depth]
            if edge not in node.children:
                prob+=remaining/self.m
                expected_depth+=remaining*min(depth+1,len(history))
                unseen=remaining
                break
            idx=node.children[edge]
        if diagnostic: return prob,expected_depth,matched,unseen
        return prob

    def evaluate(self,streams,min_past=4,positions=False):
        nr=self.nodes[0]; losses=[]; roots=[]; depths=[]; matches=[]; unseen=[]; pasts=[]
        for seq in streams:
            hist=[]; pos=0
            for x in seq:
                if x==-2:
                    hist.append(-2)
                    if len(hist)>self.D: del hist[0]
                    pos=0
                    continue
                if pos>=min_past:
                    p,d,mat,u=self.predict(hist,x,True)
                    losses.append(-log(p,2)); roots.append(-log((nr.counts.get(int(x),0)+self.a)/(nr.n+self.m*self.a),2))
                    depths.append(d); matches.append(mat); unseen.append(u); pasts.append(pos)
                hist.append(int(x))
                if len(hist)>self.D: del hist[0]
                pos+=1
        n=len(losses)
        if not n: raise ValueError('no eligible evaluation positions')
        result={'n_eval':n,'ce':fsum(losses)/n,'root_ce':fsum(roots)/n,
                'gain':(fsum(roots)-fsum(losses))/n,'weighted_depth':fsum(depths)/n,
                'mean_matched_depth':fsum(matches)/n,'unseen_branch_weight':fsum(unseen)/n}
        if positions:
            result['positions']={k:np.asarray(v) for k,v in [('loss',losses),('root_loss',roots),('weighted_depth',depths),('matched_depth',matches),('unseen_weight',unseen),('past',pasts)]}
        return result

    def fingerprint(self):
        h=hashlib.sha256(repr((self.m,self.D,self.a,self.lstop,self.lsplit)).encode())
        def walk(i,path):
            node=self.nodes[i]
            h.update(repr((path,node.n,sorted(node.counts.items()),node.le,node.lw,node.stop)).encode())
            for key in sorted(node.children): walk(node.children[key],path+(key,))
        walk(0,())
        return h.hexdigest()

    def diagnostics(self):
        depth={}
        for node in self.nodes:
            d=depth.setdefault(node.depth,{'nodes':0,'count1':0,'count_lt5':0,'observations':0})
            d['nodes']+=1; d['count1']+=node.n==1; d['count_lt5']+=node.n<5; d['observations']+=node.n
        return {'nodes':len(self.nodes),'root_stop':self.nodes[0].stop,'train_tokens':self.nodes[0].n,'by_depth':depth}
