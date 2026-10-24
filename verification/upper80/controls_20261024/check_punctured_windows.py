"""Clipped actual powers with whole or partial empty extreme intervals."""
from pathlib import Path
import sys,json,random,copy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import full_cover as fc,full_window as fw,core_gap as cg,model as m
rng=random.Random(2026102415);checks=sharp=partial=0
for trial in range(40):
    v={'ONE':1};E={0};D={0}
    for side,sign in [('s',1),('t',-1)]:
        X=list(range(1,32))+[32+rng.randrange(2,16)];E.update(sign*x for x in X)
        v['R'+side]=X[-1];v['x'+side]=X[-1]-32;v['t'+side]=X[-1]-32
        offsets=sorted(rng.sample(range(1,40),3))+[rng.randrange(60,90)]
        for letter,a in zip('abce',offsets):v[letter+side]=a;D.add(sign*(X[-1]+a))
        v['M'+side]=X[-1]+offsets[-1]
    D|=E
    for typ,Q,node in [('E',E,(0,0)),('D',D,(0,-1))]:
        four={0}
        for _ in range(4):four={a+b for a in four for b in Q}
        ev=lambda row:sum(c*v[key] for key,c in row.items());lo,hi=fc.interval(*node)
        for side in 'st':
            ga,gb=cg.gap_interval(node,side);a,b=ev(ga),ev(gb)
            for left,right in [(ev(lo),ev(hi)),(a-10,(a+b)//2),((a+b)//2,b+20),(a,b)]:
                clippedlo=max(left,ev(lo));clippedhi=min(right,ev(hi));holes=[]
                for s in 'st':
                    u,w=cg.gap_interval(node,s);u,w=max(clippedlo,ev(u)),min(clippedhi,ev(w))
                    if u<=w:holes.append(dict(side=s,lower={'ONE':u},upper={'ONE':w}));partial+=u>ev(cg.gap_interval(node,s)[0]) or w<ev(cg.gap_interval(node,s)[1])
                rebate,guards=cg.punctures({'ONE':clippedlo},{'ONE':clippedhi},node,holes)
                m.need(all(ev(g)<=0 for g in guards),'Actual puncture licenses')
                cap=clippedhi-clippedlo+1-ev(rebate);size=sum(clippedlo<=x<=clippedhi for x in four)
                m.need(size<=cap,'Actual punctured component capacity');checks+=1;sharp+=size==cap
                inventory=fc.initial_nodes();refined=[]
                if node[1]>=0:fc.refine(inventory,0);refined=[0]
                proof=dict(mask=0,lower={'ONE':clippedlo},upper={'ONE':clippedhi},refined=refined,inside=[node],outside=[dict(node=n,direction=0) for n in sorted(inventory) if n!=node],clipped=[dict(node=node,left=1,right=1,holes=holes)])
                row,licenses=fw.derive(proof,False,1,1)
                m.need(ev(row)==ev(rebate),'Full-window clipped rebate arithmetic')
                m.need(all(ev(g)<=0 for g in licenses[-len(guards):]) if guards else True,'Full-window puncture guard ordering')
bad=0
for holes,node in [([dict(side='s',lower={},upper={})]*2,(0,0)),([dict(side='',lower={},upper={})],(0,0)),([dict(side='s',lower={},upper={})],next(n for n in fc.leaves() if len(fc.roots()[n[0]])==4))]:
    try:cg.punctures({}, {}, node, holes)
    except ValueError:bad+=1
    else:raise ValueError('Invalid punctured hull recipe accepted')
# A removal extending outside its charged hull must have a positive guard.
_,guards=cg.punctures({'ONE':10},{'ONE':20},(0,0),[dict(side='s',lower={'ONE':9},upper={'ONE':20})])
m.need(any(ev(g)>0 for g in guards),'Out-of-hull removal rejected by its license');bad+=1
print(json.dumps(dict(status='PASS_NEW_PUNCTURED_WINDOW_CAPACITIES',actual_component_windows=checks,sharp_cases=sharp,partial_gap_removals=partial,negative_controls=bad,global_upper_bound_certified=False)))
