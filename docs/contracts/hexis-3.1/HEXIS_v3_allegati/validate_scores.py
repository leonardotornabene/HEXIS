from pathlib import Path
import json,math
from score_contract import jsd,pooled_gain,contrast
assert jsd([1,0],[0,1])[0]==1
assert jsd([.2,.3,.5],[.2,.3,.5])[0]==0
v,t=jsd([.2,.3,.5],[.4,.1,.5]);w,_=jsd([.4,.1,.5],[.2,.3,.5]);assert v==w and v==math.fsum(t) and 0<=v<=1
assert jsd([1,0,0],[.5,.5,0])[0]>=0
rows=[{'n':1,'root_sum':5.,'ctw_sum':1.},{'n':3,'root_sum':3.,'ctw_sum':3.}]
assert pooled_gain(rows)==1. # Document mean would be 2: that is not our estimand.
b={'h1':1.,'h2':3.,'p1':0.,'p2':1.,'p3':2.,'p4':3.,'p5':4.}
assert contrast(b,['h1','h2'],['p1','p2','p3','p4','p5'])==0
# Shuffle decomposition with non-cancelling roots.
G_o=3.-2.;G_r=2.5-2.25;Q=G_o-G_r;assert Q==.75 and Q!=(2.25-2.)
Path(__file__).with_name('scores_validation.json').write_text(json.dumps({'status':'PASS','checks':['JSD_disjoint_1','JSD_identical_0','JSD_symmetry','JSD_contribution_sum','shared_zero_support','token_weight_within_block','equal_block_weight_between_groups','four_term_Q']},indent=2)+'\n')
print('score contract PASS')
from score_contract import token_weighted_contrast
h=['h1','h2'];p=['p1','p2','p3','p4','p5'];n={k:1 for k in b};n['h2']=3
assert token_weighted_contrast(b,n,h,p)==.5 and contrast(b,h,p)==0
# The caller passes eligible counts, not kept-token counts.
kept={k:5 for k in b};kept['h2']=7
assert token_weighted_contrast(b,kept,h,p)!=token_weighted_contrast(b,n,h,p)
go={k:v+1 for k,v in b.items()};gs={k:float(i)/8 for i,k in enumerate(b)};q={k:go[k]-gs[k] for k in b}
assert abs(token_weighted_contrast(q,n,h,p)-(token_weighted_contrast(go,n,h,p)-token_weighted_contrast(gs,n,h,p)))<1e-14
for bad in (0,-1,True,1.5):
    nn=dict(n);nn['h1']=bad
    try:token_weighted_contrast(b,nn,h,p)
    except ValueError:pass
    else:raise AssertionError('invalid count accepted')
out=Path(__file__).with_name('scores_validation.json');r=json.loads(out.read_text());r['checks']+=['eligible_weight_secondary','kept_count_is_different_estimand','weighted_four_term_Q','reject_invalid_eligible_counts'];out.write_text(json.dumps(r,indent=2)+'\n')
print('secondary weighting PASS')
