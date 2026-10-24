"""Actual cores whose last-index term cannot minimize the canonical defect."""
from pathlib import Path
from itertools import combinations
import sys,json,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import canonical_phi as cm,first_gap_core as fg,model as m
checks=sharp=rank_one=0
for r in range(2,9):
    for X in combinations(range(1,15),r):
        phi=min([r,*[x+r-2*i for i,x in enumerate(X,1)]]);xi=X[-1]-r;tau=sum(X)-r*(r+1)//2
        if phi>=r or xi<phi+1:continue
        H=max(r-1,xi);m.need(tau<=xi+H*(phi-1),'Canonical nonlast mass');checks+=1;sharp+=tau==xi+H*(phi-1)
        if phi==1:m.need(tau==xi,'Defect-one isolated tail is exact');rank_one+=1
rng=random.Random(2026102416);affine=0
for case in [None,0,1,2,3]:
    for trial in range(100):
        k=rng.randrange(18)
        for side,sign in [('s',-1),('t',1)]:
            r=32+sign*k;h=t=0
            if case is not None:
                h,ps,pt=fg.CASES[case];t=ps if side=='s' else pt
            n=r-t;d=sorted(rng.randrange(6) for _ in range(n));d[-1]+=rng.randrange(2,12)
            X=([1] if t else [])+[h+i+z for i,z in enumerate(d,1)];phi=min([r,*[x+r-2*i for i,x in enumerate(X,1)]]);w=h-t
            v={'ONE':1,'rank_k':k,'phicore'+side:phi,'x'+side:X[-1]-r,'t'+side:sum(X)-r*(r+1)//2};H=max(n-1,v['x'+side]-w)
            fact,guards=cm.tail_derive(side,H,case,case);ev=lambda row:sum(c*v[key] for key,c in row.items())
            if all(ev(g)<=0 for g in guards):m.need(ev(fact[0])<=0,'Physical affine canonical tail mass');affine+=1
bad=0
for args in [('s',40,0,None),('s',40,0,1),('',40,None,None),('s',0,None,None)]:
    try:cm.tail_derive(*args)
    except ValueError:bad+=1
    else:raise ValueError('Invalid canonical tail premise accepted')
print(json.dumps(dict(status='PASS_NEW_CANONICAL_NONLAST_MASS',actual_cores=checks,sharp_cases=sharp,defect_one_exact_tails=rank_one,physical_affine_checks=affine,invalid_recipes_rejected=bad,global_upper_bound_certified=False)))
