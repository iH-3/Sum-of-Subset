"""New complete source-union formula, evaluated on actual 73-point sets."""
from pathlib import Path
import sys,json,random,copy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import source_union as su,model as m
rng=random.Random(2026102408);checks=0;rebates=0;sharp=0
for trial in range(400):
    k=rng.randrange(18);point={'ONE':1,'rank_k':k};cores=[];T=[];phis=[]
    for side,rank,sign in [('s',32-k,1),('t',32+k,-1)]:
        defects=sorted(rng.randrange(5 if trial%3 else 20) for _ in range(rank))
        if trial%4==0:defects=[0]*rank
        X=[i+d for i,d in enumerate(defects,1)];R=max(X)
        point.update({'R'+side:R,'t'+side:sum(X)-rank*(rank+1)//2,'x'+side:R-rank})
        phis.append(min([rank,*[x+rank-2*i for i,x in enumerate(X,1)]]))
        offsets=sorted(rng.sample(range(1,141),4))
        point.update({off+side:x for off,x in zip('abce',offsets)})
        cores.extend(sign*x for x in X);T.extend(sign*(R+x) for x in offsets)
    E={0,*cores};D=E|set(T);EE={a+b for a in E for b in E};DD={a+b for a in D for b in D}
    point.update(K=len(DD),F=65-sum(phis));ev=lambda row:sum(c*point[k] for k,c in row.items())
    union=EE|{a+b for a in E for b in T}
    covered=[]
    for pair in su.PAIRS:
        for witness in ('double_prefix','zero','core_s','core_t',*range(8)):
            if all(ev(g)<=0 for g in su.membership(pair,witness)):
                m.need(T[pair[0]]+T[pair[1]] in union,'Explicit tail-pair membership')
                covered.append(dict(pair=pair,witness=witness));break
    for mode in ('hull','mass'):
        proof=dict(base_capacity=mode,edges=[i for i,g in enumerate(su.gaps()) if ev(g)<point['F']],covered=covered)
        body,guards=su.derive(proof)
        m.need(all(ev(g)<=0 for g in guards) and ev(body)<=0,'Actual complete source union upper bound')
        checks+=1;rebates+=len(covered);sharp+=ev(body)==0
bad=0
for proof in [dict(base_capacity='mass',edges=[0,0],covered=[]),dict(base_capacity='mass',edges=[8],covered=[]),dict(base_capacity='mass',edges=[],covered=[dict(pair=[0,0],witness=8)]),dict(base_capacity='mass',edges=[],covered=[dict(pair=[0,0],witness='zero')]*2),dict(base_capacity='mass',edges=[],covered=[dict(pair=[1,0],witness='zero')])]:
    try:su.derive(proof)
    except ValueError:bad+=1
    else:raise ValueError('Invalid source-union inventory accepted')
print(json.dumps(dict(status='PASS_NEW_SOURCE_UNION',actual_source_sets=400,capacity_checks=checks,rebated_pair_checks=rebates,sharp_cases=sharp,negative_controls=bad,global_upper_bound_certified=False)))
