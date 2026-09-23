"""Reproduce review checks B2/S1/S3; no real between-group contrasts."""
from pathlib import Path
import argparse,json,platform,math
import numpy as np
from validate_contract import parse_raw
from protocol_contract import sample,shuffle,streams
from ctw_reference import CTW
arg=argparse.ArgumentParser();arg.add_argument('--raw-dir',required=True,type=Path);arg.add_argument('--output',required=True,type=Path);args=arg.parse_args()
here=Path(__file__).resolve().parent;cfg=json.loads((here/'hexis_v3_design.json').read_text());blocks,probes,alpha=parse_raw(args.raw_dir,cfg,'ud23')
baseline={r['held_block_key']:r for r in json.loads((here/'contract_validation.json').read_text())['real_pairs']}
census={'contributions':0,'fragment_count':0,'internal_start_count':0,'fragment_tokens':0,'direct_context_targets':0,'total_training_tokens':0};lengths=[]
for seed in range(20):
    for held in sorted(blocks):
        for bk,rr in sorted(blocks.items()):
            if held==bk:continue
            selected=sample(rr,8884,seed,held,bk);census['contributions']+=1;census['total_training_tokens']+=sum(len(r['seq']) for r in selected)
            for r in selected:
                if r['fragment']:
                    census['fragment_count']+=1;census['fragment_tokens']+=len(r['seq']);lengths.append(len(r['seq']))
                    if r['start']>0:census['internal_start_count']+=1;census['direct_context_targets']+=min(8,len(r['seq']))
census['fragment_length_range']=[min(lengths),max(lengths)];census['direct_context_fraction']=census['direct_context_targets']/census['total_training_tokens'];assert (census['contributions'],census['fragment_count'],census['internal_start_count'],census['direct_context_targets'])==(840,671,563,3477)
abl=[]
for held in sorted(blocks):
    tr=[];trsh=[];budgets=[]
    for bk,rr in sorted(blocks.items()):
        if bk==held:continue
        s=[r for r in sample(rr,8884,0,held,bk) if not r['fragment']]
        budgets.append(sum(len(r['seq']) for r in s));tr+=streams(s);trsh+=streams(shuffle(s,0,held,bk,'train'))
    ra=CTW(len(alpha)).fit(tr).evaluate(streams(blocks[held]));rb=CTW(len(alpha)).fit(trsh).evaluate(streams(shuffle(blocks[held],0,held,held,'eval')))
    base=baseline[held];q=ra['gain']-rb['gain']
    abl.append({'held_block_key':held,'training_tokens':sum(budgets),'minimum_block_tokens':min(budgets),'original':ra,'shuffled':rb,'Q':q,'delta_Q_vs_exact_budget':q-base['Q']})
    print('whole-sentence ablation',held[:10],flush=True)
def chain(n,stay,seed):
    r=np.random.default_rng(seed);x=r.integers(2,size=n);u=r.random(n)
    for i in range(1,n):x[i]=x[i-1] if u[i]<stay else 1-x[i-1]
    return x.tolist()
test=chain(100000,.9,999);toy=[]
for orientation in ('same_group_dissimilar','same_group_similar'):
    for own in (1/6,1/2):
        nown=round(53304*own);d=orientation=='same_group_dissimilar'
        tr=[chain(nown,.1 if d else .9,101),chain(53304-nown,.9 if d else .1,102)]
        rr=np.random.default_rng(103);trsh=[rr.permutation(x).tolist() for x in tr];tesh=np.random.default_rng(104).permutation(test).tolist()
        go=CTW(2).fit(tr).evaluate([test])['gain'];gs=CTW(2).fit(trsh).evaluate([tesh])['gain']
        toy.append({'orientation':orientation,'own_fraction':own,'G_original':go,'G_shuffled':gs,'Q':go-gs})
assert toy[1]['Q']<toy[0]['Q'] and toy[3]['Q']>toy[2]['Q']
r=np.random.default_rng(724);tr=[r.integers(2,size=100).tolist()];te=[r.integers(2,size=10000).tolist()];m=CTW(2).fit(tr);iid={'root_stop_weight':m.nodes[0].stop,'gain':m.evaluate(te)['gain']};assert 0<iid['root_stop_weight']<1 and abs(iid['gain'])>1e-5
out={'status':'PASS','date':'2026-09-12','python':platform.python_version(),'numpy':np.__version__,'fragment_census':census,'whole_sentence_ablation':abl,'max_abs_delta_Q':max(abs(r['delta_Q_vs_exact_budget']) for r in abl),'training_fraction_counterexample':toy,'finite_iid_counterexample':iid,'real_fits':14,'synthetic_fits':9,'limitations':['Ablation uses C0 seed 0 only; no bound on full-study effects.','Toy group labels carry no linguistic semantics; counterexample disproves a universal directional claim only.','No final group contrast or scientific gate certification.']}
args.output.write_text(json.dumps(out,indent=2)+'\n');print('revision checks PASS',out['max_abs_delta_Q'])
