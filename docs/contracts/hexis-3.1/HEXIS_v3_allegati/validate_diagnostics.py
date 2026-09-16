from pathlib import Path
import itertools,json,math
from ctw_reference import CTW
from resolved_diagnostics import resolved
out={'status':'PASS','histories_checked':0}
for D in (0,1,3):
 for seq in ([],[[0,1,0,2,1,0]],[[0,-2,1,0,-2,2,2]]):
  model=CTW(3,D).fit(seq)
  for n in range(4):
   for h in itertools.product([0,1,2,-2],repeat=n):
    r=resolved(model,list(h));out['histories_checked']+=1
    assert abs(sum(r['mass_by_lexical_length'].values())+r['unseen_mass']-1)<1e-12
    if r['resolved_mean'] is not None:assert 0<=r['resolved_mean']<=min(D,n)
    if model.nodes[0].n:assert abs(r['unseen_mass']-model.predict(list(h),0,True)[3])<1e-12
    else:assert r['unseen_mass']==1 and r['resolved_mean'] is None
# Explicit non-cancellation of root CE when the first four slots are excluded.
m=CTW(2).fit([[0]*6+[1]*2]);a=m.evaluate([[0,0,0,0,1,1,1,1]]);b=m.evaluate([[1,1,1,1,0,0,0,0]])
assert a['root_ce']!=b['root_ce']
q=a['gain']-b['gain'];shortcut=b['ce']-a['ce'];assert abs(q-shortcut)>1
out['root_non_cancellation']={'Q':q,'incorrect_shortcut':shortcut,'root_difference':a['root_ce']-b['root_ce']}
Path(__file__).with_name('diagnostics_validation.json').write_text(json.dumps(out,indent=2)+'\n')
print(out)
