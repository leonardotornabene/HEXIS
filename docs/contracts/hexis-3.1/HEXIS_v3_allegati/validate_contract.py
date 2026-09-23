"""Validate plan consistency and sampling. --raw-dir adds 14+2 real pilot fits.
Python 3.12; runtime NumPy version is recorded in the output. Outputs only to --output (default current directory).
Uses the separately verified CTW reference, not HEXIS production modules.
"""
from pathlib import Path
from collections import Counter,defaultdict
import json,hashlib,argparse,math,time,platform,xml.etree.ElementTree as ET,unicodedata
import numpy as np
from protocol_contract import block_key,sample,shuffle,streams,ledger,eligible,seed_value,canonical

HERE=Path(__file__).resolve().parent

def parse_raw(path,cfg,variant):
    reg={r['source_prefix']:r for r in cfg['registry']}; records=[];alphabet=set();seen=set();ntok=0
    ap=cfg['alphabet'];mappings=ap['upos_map'];expected={r['file']:r['sha256'] for r in cfg['source_hashes']}
    for name,digest in sorted(expected.items()):
        b=(path/name).read_bytes();assert hashlib.sha256(b).hexdigest()==digest
        for sent in b.decode().strip().split('\n\n'):
            meta={};rows=[]
            for line in sent.splitlines():
                if line.startswith('# ') and ' = ' in line:
                    k,v=line[2:].split(' = ',1);meta[k]=v
                elif line and not line.startswith('#'):
                    f=line.split('\t')
                    if f[0].isdigit():rows.append(f)
            sid=meta['sent_id'];assert sid not in seen;seen.add(sid);pref,ord_=sid.rsplit('@',1);r=reg[pref]
            seq=[];coords=[]
            for f in rows:
                ntok+=1;u=mappings.get(f[3],f[3]);d=f[7].lower().split(':',1)[0]
                assert u in ap['upos_keep']+ap['upos_drop']
                if u not in ap['upos_keep']:continue
                if variant!='ud23_oth' and d not in ap['deprel_keep']:continue
                sym=u if variant=='upos_only' else u+':'+(d if d in ap['deprel_keep'] else 'oth')
                seq.append(sym);coords.append(int(f[0]));alphabet.add(sym)
            records.append({'sid':sid,'doc':r['canonical_doc_id'],'source_order':(r['part_order'],int(ord_)),
                            'seq':seq,'coords':coords})
    alphabet=sorted(alphabet);ids={s:i for i,s in enumerate(alphabet)};bydoc=defaultdict(list)
    for r in records:r['seq']=[ids[s] for s in r['seq']];bydoc[r['doc']].append(r)
    for doc,rr in bydoc.items():
        rr.sort(key=lambda r:(r['source_order'],r['sid']))
        for k,r in enumerate(rr):r['source_rank']=k
    blocks={b['block_key']:[r for d in b['docs'] for r in bydoc[d]] for b in cfg['blocks']}
    primary={d for b in cfg['blocks'] for d in b['docs']}
    probe={d:r for d,r in bydoc.items() if d not in primary}
    assert ntok==cfg['expected']['raw_tokens'] and len(records)==cfg['expected']['raw_sentences']
    assert len(alphabet)==cfg['expected']['alphabet_sizes'][variant]
    return blocks,probe,alphabet

def jsd(p,q):
    z=(p+q)/2
    return float(.5*np.sum(np.where(p>0,p*np.log2(p/z),0))+.5*np.sum(np.where(q>0,q*np.log2(q/z),0)))

def main():
    arg=argparse.ArgumentParser();arg.add_argument('--raw-dir',type=Path);arg.add_argument('--output',type=Path,default=Path.cwd());args=arg.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    cfg=json.loads((HERE/'hexis_v3_design.json').read_text());out={'design_sha256':hashlib.sha256((HERE/'hexis_v3_design.json').read_bytes()).hexdigest(),'status':'RUNNING','python':platform.python_version(),'numpy':np.__version__,'tests':{},'real_pairs':[]}
    blocks=cfg['blocks'];cells=cfg['cells'];assert len(blocks)==7 and len(cells)==9
    assert sum(len(c['seeds'])*len(c['arms'])*7 for c in cells)==1400
    assert 90*109108+10*109716+140*12769==cfg['expected']['paired_position_rows_with_probes']
    assert Counter(b['group'] for b in blocks)=={'HEX':2,'PROSE_ALL':5}
    assert sum(b['kept']['ud23'] for b in blocks)==154300
    assert sum(b['eligible']['ud23'] for b in blocks)==109108
    assert len(cfg['registry'])==18 and len({r['canonical_doc_id'] for r in cfg['registry']})==17
    keys=[]
    for seed in range(20):
      for b in blocks:
       for other in blocks:
        if b is other:continue
        for purpose in ('sample','fragment','shuffle_train','shuffle_eval'):
            keys.append(seed_value(seed,b['block_key'],other['block_key'],purpose))
    assert len(keys)==len(set(keys))
    out['tests']['derived_seed_keys']=len(keys)
    fixture=[{'doc':'fixture','sid':f'fixture@{i+1}','source_order':(0,i+1),'source_rank':i,
              'seq':[j%3 for j in range(n)],'coords':list(range(1,n+1))} for i,n in enumerate([5,8,0,2,7,6])]
    k=block_key(['fixture']);h=block_key(['held']);s=sample(fixture,17,0,h,k)
    assert sum(len(r['seq']) for r in s)==17 and sum(r['fragment'] for r in s)<=1
    assert ledger(s)==ledger(sample(list(reversed(fixture)),17,0,h,k))
    assert ledger(sample(fixture,17,0,h,k))==ledger(s)
    sh=shuffle(s,0,h,k,'train')
    for a,b in zip(s,sh):assert Counter(a['seq'])==Counter(b['seq']) and sorted(b['permutation'])==list(range(len(a['seq'])))
    assert sum(s.count(-2) for s in streams(fixture,True))==3 # empty sentence breaks both sides
    assert eligible(sh)==eligible(s)
    p=np.array([.2,.3,.5]);q=np.array([.4,.1,.5]);assert abs(jsd(p,q)-jsd(q,p))<1e-14 and abs(jsd(p,p))<1e-14
    out['tests']['budget_order_boundary_shuffle_jsd']='PASS'
    out['rng_reference_vector']={'seed':0,'held':h,'block':k,'purpose':'sample','uint128':str(seed_value(0,h,k,'sample')),'sentence_order':[r['sid'] for r in s],'ledger':ledger(s)}
    if args.raw_dir:
      from ctw_reference import CTW
      data={v:parse_raw(args.raw_dir,cfg,v) for v in cfg['expected']['alphabet_sizes']}
      original,probe,alph=data['ud23'];upos=data['upos_only'][0]
      for bk,rr in original.items():
          assert [r['coords'] for r in rr]==[r['coords'] for r in upos[bk]]
      out['tests']['three_alphabets_and_upos_coordinates']='PASS'
      for held in sorted(original):
        chosen=[];first_ledger={}
        for bk,rr in sorted(original.items()):
          if bk==held:continue
          s=sample(rr,8884,0,held,bk);assert not {r['sid'] for r in s}&{r['sid'] for r in original[held]}
          chosen.extend(s);first_ledger[bk]=ledger(s)
        tr=streams(chosen);tr_sh=[]
        for bk,rr in sorted(original.items()):
          if bk!=held:tr_sh+=streams(shuffle(sample(rr,8884,0,held,bk),0,held,bk,'train'))
        te=streams(original[held]);tesh=streams(shuffle(original[held],0,held,held,'eval'))
        assert sum(map(len,tr))==53304 and Counter(x for r in tr for x in r)==Counter(x for r in tr_sh for x in r)
        t0=time.perf_counter();a=CTW(len(alph)).fit(tr);b=CTW(len(alph)).fit(tr_sh)
        assert a.nodes[0].counts==b.nodes[0].counts
        af=a.fingerprint();bf=b.fingerprint();ra=a.evaluate(te);rb=b.evaluate(tesh)
        assert ra['n_eval']==rb['n_eval']==eligible(original[held]);assert a.fingerprint()==af and b.fingerprint()==bf
        Q=ra['gain']-rb['gain'];assert math.isfinite(Q)
        out['real_pairs'].append({'held_block_key':held,'seed':0,'n_eval':ra['n_eval'],'original':ra,'shuffled':rb,'Q':Q,'seconds':time.perf_counter()-t0,'sample_hash':hashlib.sha256(canonical(first_ledger)).hexdigest()})
        # Probe: all 6 documents, both arms, no fit. Scores checked, not interpreted.
        for doc,rr in sorted(probe.items()):
          pa=a.evaluate(streams(rr));pb=b.evaluate(streams(shuffle(rr,0,held,block_key([doc]),'probe')))
          assert pa['n_eval']==pb['n_eval']==eligible(rr)
        if held==sorted(original)[0]:
          btr=[]
          for bk,rr in sorted(original.items()):
            if bk!=held:btr+=shuffle(sample(rr,8884,0,held,bk),0,held,bk,'train')
          # Exercise separator preservation after shuffling individual sentences.
          ba=CTW(len(alph)).fit(streams(chosen,True));bb=CTW(len(alph)).fit(streams(btr,True))
          assert ba.nodes[0].counts==bb.nodes[0].counts
          br=ba.evaluate(streams(original[held],True));bs=bb.evaluate(streams(shuffle(original[held],0,held,held,'eval'),True))
          assert br['n_eval']==bs['n_eval']==eligible(original[held])
          out['bound_pair']={'original':br,'shuffled':bs,'Q':br['gain']-bs['gain']}
        print('verified pair',held[:12],flush=True)
      out['tests']['real_fit_count']=16;out['tests']['probe_evaluations']=84
    out['status']='PASS'
    (args.output/'contract_validation.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'tests':out['tests']}))
if __name__=='__main__':main()
