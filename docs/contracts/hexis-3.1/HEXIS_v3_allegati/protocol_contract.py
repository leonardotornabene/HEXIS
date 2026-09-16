"""Executable specification of HEXIS 3 sampling/RNG; not production code.
No project imports. Input records use seq (ordinary integer symbols), coords
(raw integer token IDs), sid, doc, source_order and source_rank.
"""
import hashlib,json
import numpy as np

MASTER=20260706
VERSION='hexis-v3-rng-1'

def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')

def block_key(doc_ids):
    return hashlib.sha256(canonical(sorted(doc_ids))).hexdigest()

def seed_value(seed,held,block,purpose,sid='',start=0,end=0):
    obj={'version':VERSION,'master':MASTER,'seed':seed,'held':held,'block':block,
         'purpose':purpose,'sid':sid,'start':start,'end':end}
    return int.from_bytes(hashlib.sha256(canonical(obj)).digest()[:16],'big')

def rng(seed,held,block,purpose,sid='',start=0,end=0):
    return np.random.Generator(np.random.PCG64(seed_value(seed,held,block,purpose,sid,start,end)))

def ordered(records):
    return sorted(records,key=lambda r:(r['doc'],*r['source_order'],r['sid']))

def sample(records,q,seed,held,block):
    if type(q) is not int or q<=0:raise ValueError('q must be positive integer')
    records=ordered(records)
    if sum(len(r['seq']) for r in records)<q:raise ValueError('insufficient tokens')
    # Include empty sentences in permutation: stable keys across representations.
    order=rng(seed,held,block,'sample').permutation(len(records)); chosen=[];left=q
    for i in order:
        if left==0:break
        r=records[int(i)];n=len(r['seq'])
        if n==0:continue
        take=min(left,n)
        start=int(rng(seed,held,block,'fragment',r['sid']).integers(n-take+1)) if take<n else 0
        chosen.append({**r,'seq':r['seq'][start:start+take],'coords':r['coords'][start:start+take],
                       'start':start,'end':start+take,'fragment':take<n})
        left-=take
    if left:raise RuntimeError('incomplete sample')
    return chosen

def shuffle(records,seed,held,block,role):
    if role not in ('train','eval','probe'):raise ValueError('unknown permutation role')
    out=[]
    for r in records:
        st=r.get('start',0);en=r.get('end',len(r['seq']))
        perm=rng(seed,held,block,'shuffle_'+role,r['sid'],st,en).permutation(len(r['seq']))
        out.append({**r,'seq':[r['seq'][int(i)] for i in perm],
                    'origin_coords':[r['coords'][int(i)] for i in perm],
                    'permutation':[int(i) for i in perm]})
    return out

def streams(records,bound=False):
    if not bound:return [list(r['seq']) for r in ordered(records) if r['seq']]
    out=[];last=None
    for r in ordered(records):
        if not r['seq']:last=None;continue
        adjacent=(last is not None and r['doc']==last['doc'] and
                  r['sid'].rsplit('@',1)[0]==last['sid'].rsplit('@',1)[0] and
                  r['source_rank']==last['source_rank']+1 and
                  r['source_order'][0]==last['source_order'][0] and
                  r['source_order'][1]==last['source_order'][1]+1 and
                  not r.get('fragment',False) and not last.get('fragment',False))
        if adjacent:out[-1].extend([-2]+r['seq'])
        else:out.append(list(r['seq']))
        last=r
    return out

def ledger(records):
    return [{'sid':r['sid'],'start':r['start'],'end':r['end'],'fragment':r['fragment']}
            for r in records]

def eligible(records):return sum(max(0,len(r['seq'])-4) for r in records)
