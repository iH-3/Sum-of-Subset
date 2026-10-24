"""New complete subset-sum interval propagation through distinct outer points."""
from pathlib import Path
import sys,random,json,copy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import full_window as fw,full_cover as fc,model as m
rng=random.Random(2026102408);checks=0
for _ in range(200):
    D=list(range(-6,7));values={'ONE':1,'Ss':21,'St':21}
    for side in ['s','t']:
        values.update({'M'+side:6,'X'+side:rng.randrange(2,10),'g'+side:rng.randrange(1,8),'h'+side:rng.randrange(1,8),'d'+side:rng.randrange(1,8)})
    ev=lambda row:sum(c*values[k] for k,c in row.items())
    O=[ev(row) for row in fc.outer()];order=sorted(range(8),key=lambda i:abs(O[i]));fs={0}
    for v in D:fs|={a+v for a in fs}
    lo,hi=-21,21
    for i in order:
        fs|={a+O[i] for a in fs};lo+=min(0,O[i]);hi+=max(0,O[i])
    proof=dict(lower={'ONE':lo},upper={'ONE':hi},mask=0,outer_extension=order)
    guards=fw.proof_bracket(proof,False,1,1)
    m.need(all(ev(g)<=0 for g in guards),'Outer propagation guards')
    m.need(set(range(lo,hi+1))<=fs,'Explicit complete extended interval');checks+=1
bad=[]
for label,mutate,positive,cw in [('repeated outer',lambda p:p['outer_extension'].append(p['outer_extension'][0]),False,1),('shift reuses outer',lambda p:p.update(mask=1),False,1),('unlocalized holes',lambda p:None,True,3)]:
    q=copy.deepcopy(proof);mutate(q)
    try:fw.proof_bracket(q,positive,cw,1)
    except ValueError:bad.append(label)
    else:raise ValueError('Invalid outer propagation accepted')
print(json.dumps(dict(status='PASS_NEW_WINDOW_EXTENSION',explicit_subset_sum_sets=checks,negative_controls=bad,global_upper_bound_certified=False)))
