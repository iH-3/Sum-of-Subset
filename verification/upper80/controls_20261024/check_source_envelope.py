"""New source envelope: extreme points, punctured middle intervals and pairs."""
from pathlib import Path
import sys,json,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import source_envelope as se,first_gap_core as fg,model as m
rng=random.Random(2026102419);checks=0
piece_checks=sharp=0
for shape in [None,0,1,2,3]:
    for trial in range(24):
        k=rng.randrange(18);v={'ONE':1,'rank_k':k};E={0};T=[]
        for side,r,sign in [('s',32-k,1),('t',32+k,-1)]:
            h=t=0
            if shape is not None:
                h,ps,pt=fg.CASES[shape];t=ps if side=='s' else pt
            n=r-t;phi0=rng.randrange(2,14)
            d=[max(0,phi0-n+i) for i in range(1,n+1)]
            X=([1] if t else [])+[h+i+y for i,y in enumerate(d,1)]
            phi=min([r,*[x+r-2*i for i,x in enumerate(X,1)]]);E.update(sign*x for x in X)
            v.update({'R'+side:X[-1],'x'+side:X[-1]-r,'t'+side:sum(X)-r*(r+1)//2,'phicore'+side:phi})
            offsets=sorted(rng.sample(range(1,150),4));v.update({off+side:x for off,x in zip('abce',offsets)})
            T.extend(sign*(X[-1]+x) for x in offsets)
        D=E|set(T);v.update(K=len({a+b for a in D for b in D}),F=65-v['phicores']-v['phicoret'])
        ev=lambda row:sum(c*v[key] for key,c in row.items())
        proof,intervals,clusters=se.recipe(v,shape)
        EE={a+b for a in E for b in E}
        for i,Q in enumerate([EE,*[{a+x for a in E} for x in T]]):
            for x in Q:
                m.need(any(ev(lo)<=x<=ev(hi) for lo,hi in intervals[3*i:3*i+3]),'Actual source component in extreme-gap pieces')
            piece_checks+=1
        for indices in clusters:
            lo=min((intervals[i][0] for i in indices),key=ev);hi=max((intervals[i][1] for i in indices),key=ev)
            proof['groups'].append(dict(pieces=indices,lower=lo,upper=hi))
        row,guards=se.derive(proof,shape)
        m.need(all(ev(g)<=0 for g in guards) and ev(row[0])<=0,'Actual complete source-envelope bound')
        checks+=1;sharp+=ev(row[0])==0
        singleton=dict(proof,groups=[dict(pieces=[i],mass=True) for i in range(63)])
        row,_=se.derive(singleton,shape);m.need(ev(row[0])<=0,'Actual disjoint source-piece masses')
bad=0
import copy
recipes=[]
p=copy.deepcopy(proof);p['groups'][0]['pieces'].append(p['groups'][0]['pieces'][0]);recipes.append(p)
p=copy.deepcopy(proof);p['groups'].pop();recipes.append(p)
p=copy.deepcopy(proof);p['core_prefix']['s']=13;recipes.append(p)
p=copy.deepcopy(proof);p['trimmed']=['s','s'];recipes.append(p)
p=copy.deepcopy(proof);p['groups']=[dict(pieces=list(range(63)),mass=True)];recipes.append(p)
for p in recipes:
    try:se.derive(p,shape)
    except ValueError:bad+=1
    else:raise ValueError('Invalid source-envelope recipe accepted')
print(json.dumps(dict(status='PASS_NEW_SOURCE_ENVELOPE',actual_source_sets=checks,component_envelopes=piece_checks,sharp_capacities=sharp,mass_partitions=checks,invalid_recipes_rejected=bad,global_upper_bound_certified=False)))
