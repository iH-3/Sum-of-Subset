"""Mixed-power forest edges: actual sumsets and invalid recipe controls."""
from pathlib import Path
import sys,json,random,copy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import full_window as fw,full_cover as fc,model as m
rng=random.Random(2026102409);checks=0
nodes={q:next(n for n in fc.leaves() if n[1]>=0 and fw.core_power(n)==q) for q in range(1,5)}
for trial in range(80):
    k=rng.randrange(18);E={0};phi=0;values={'ONE':1}
    for side,r,sign in [('s',32-k,1),('t',32+k,-1)]:
        X=[i+d for i,d in enumerate(sorted(rng.randrange(5) for _ in range(r)),1)]
        E.update(sign*x for x in X);phi+=min([r,*[x+r-2*i for i,x in enumerate(X,1)]])
        values['R'+side]=max(X)
    F=65-phi;powers={0:{0}}
    for q in range(1,5):powers[q]={a+b for a in powers[q-1] for b in E}
    for p in range(1,4):
        for q in range(p+1,5):
            for i in range(q-p+1):
                j=q-p-i;anchor=i*values['Rs']-j*values['Rt'];shift=rng.randrange(-200,201)
                actual=len(powers[p]&{x+shift for x in powers[q]})
                bound=p*F-p+1-abs(shift+anchor)
                m.need(actual>=bound,'Explicit mixed-power core intersection');checks+=1
values.update({key:1 for row in fc.outer() for key in row if key not in values})
for side in 'st':values.update({off+side:i for i,off in enumerate('abce',1)})
ev=lambda row:sum(c*values[k] for k,c in row.items())
a,b=nodes[1],nodes[2]
edge=dict(small=a,large=b,anchor=[1,0],direction=1)
gap=fw.mixed_gap(a,b,[1,0],1)
expected=ev(fc.interval(*b)[0])+2*values['Rt']+values['Rs']-ev(fc.interval(*a)[0])-values['Rt']
m.need(ev(gap)==expected,'Hull-to-centre conversion')
proof=dict(mask=0,lower={},upper={'ONE':1},exact_one_term=True,refined=[i for i,r in enumerate(fc.roots()) if len(r)<4],inside=[a,b],outside=[dict(node=n,direction=0) for n in fc.leaves() if n not in (a,b)],mixed_core_edges=[edge])
fw.derive(proof,False,1,1);bad=0
for change in ('cycle','anchor','orientation','power'):
    other=copy.deepcopy(proof)
    if change=='cycle':other['mixed_core_edges']*=2
    if change=='anchor':other['mixed_core_edges'][0]['anchor']=[2,0]
    if change=='orientation':other['mixed_core_edges'][0]['direction']=0
    if change=='power':other['mixed_core_edges'][0].update(small=b,large=a)
    try:fw.derive(other,False,1,1)
    except ValueError:bad+=1
    else:raise ValueError('Invalid mixed forest accepted')
print(json.dumps(dict(status='PASS_NEW_MIXED_CORE_WINDOWS',actual_intersections=checks,negative_controls=bad,global_upper_bound_certified=False)))
