"""Actual 73-point sources against disjoint charges of hulls and pair points."""
from pathlib import Path
import sys,json,random,copy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import source_hulls as sh,model as m
rng=random.Random(2026102414);checks=sharp=absorbed=0
for trial in range(300):
    k=rng.randrange(18);v={'ONE':1,'rank_k':k};D={0}
    for side,r,sign in [('s',32-k,1),('t',32+k,-1)]:
        X=[i+d for i,d in enumerate(sorted(rng.randrange(5) for _ in range(r)),1)]
        v['R'+side]=X[-1];v['t'+side]=sum(X)-r*(r+1)//2;v['x'+side]=X[-1]-r
        D.update(sign*x for x in X);last=0
        for q in 'abce':last+=rng.randrange(1,36);v[q+side]=last;D.add(sign*(X[-1]+last))
    m.need(len(D)==73,'Actual source cardinality');v['K']=len({a+b for a in D for b in D});ev=lambda row:sum(c*v[key] for key,c in row.items())
    intervals=sh.components();points=sh.pairs();order=list(range(9));rng.shuffle(order)
    groups=[];covered=set()
    while order:
        indices=order[:rng.randrange(1,min(4,len(order))+1)];del order[:len(indices)]
        lo=min((intervals[i][0] for i in indices),key=ev);hi=max((intervals[i][1] for i in indices),key=ev)
        members=[i for i,row in enumerate(points) if i not in covered and ev(lo)<=ev(row)<=ev(hi)]
        covered.update(members);groups.append(dict(components=indices,lower=lo,upper=hi,pairs=members))
    for proof in [dict(groups=groups),dict(groups=[dict(components=[i],mass=True) for i in range(9)])]:
        fact,guards=sh.derive(proof);m.need(all(ev(g)<=0 for g in guards),'Actual hull membership licenses')
        m.need(ev(fact[0])<=0,'Actual complete double-source capacity');checks+=1;sharp+=ev(fact[0])==0
    absorbed+=len(covered)
base=dict(groups=[dict(components=[i],mass=True) for i in range(9)]);bad=[]
q=copy.deepcopy(base);q['groups'].pop();bad.append(q)
q=copy.deepcopy(base);q['groups'][1]['components']=[0];bad.append(q)
q=copy.deepcopy(base);q['groups'][0]['pairs']=[0];bad.append(q)
q=copy.deepcopy(base);q['groups'][0]['components']=[9];bad.append(q)
q=copy.deepcopy(base);q['core_shape']=0;bad.append(q)
rejected=0
for q in bad:
    try:sh.derive(q)
    except ValueError:rejected+=1
    else:raise ValueError('Invalid source hull proof accepted')
print(json.dumps(dict(status='PASS_NEW_SOURCE_HULL_CAPACITIES',actual_sources=300,capacities=checks,sharp_cases=sharp,absorbed_pair_occurrences=absorbed,invalid_recipes_rejected=rejected,global_upper_bound_certified=False)))
