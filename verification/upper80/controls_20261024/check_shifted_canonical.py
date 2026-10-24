"""Actual first-gap remainders, including the necessary sentinel guard."""
from pathlib import Path
from itertools import combinations
import json,sys,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import canonical_phi as cm,first_gap_core as fg,model as m
def phi(X):
    r=len(X);return min([r,*[x+r-2*i for i,x in enumerate(X,1)]])
identities=inequalities=sharp=sentinel=0
for h,t in [(1,0),(2,1),(2,0),(3,1)]:
    for n in range(1,7):
        for Y in combinations(range(1,11),n):
            X=([1] if t else [])+[h+y for y in Y];r=len(X);w=h-t
            p=phi(X);py=phi(Y);tau=sum(X)-r*(r+1)//2;xi=X[-1]-r;B=w*n
            m.need(p==min(n,w+py),'Exact translated canonical minimum');identities+=1
            if p<n:
                H=max(n,xi-w);m.need(tau-B<=H*(p-w),'Translated canonical mass');inequalities+=1;sharp+=tau-B==H*(p-w)
            else:sentinel+=1
rng=random.Random(2026102413);affine=0
for case,(h,ps,pt) in enumerate(fg.CASES):
    for _ in range(100):
        k=rng.randrange(18)
        for side,t,sgn in [('s',ps,-1),('t',pt,1)]:
            r=32+sgn*k;n=r-t;Y=[i+d for i,d in enumerate(sorted(rng.randrange(6) for _ in range(n)),1)]
            X=([1] if t else [])+[h+y for y in Y];p=phi(X);w=h-t;H=max(n,Y[-1]-n)
            values={'ONE':1,'rank_k':k,'x'+side:X[-1]-r,'t'+side:sum(X)-r*(r+1)//2,'phicore'+side:p}
            fact,guards=cm.shifted_derive(side,H,case,case);ev=lambda row:sum(v*values[key] for key,v in row.items())
            if all(ev(g)<=0 for g in guards):m.need(ev(fact[0])<=0,'Affine physical shifted mass');affine+=1
bad=0
for args in [('s',40,0,None),('s',40,0,1),('s',40,4,4),('q',40,0,0),('s',0,0,0)]:
    try:cm.shifted_derive(*args)
    except ValueError:bad+=1
    else:raise ValueError('Invalid translated mass recipe accepted')
# X=[h+1] has phi(X)=n=1. Omitting the nonsentinel guard would
# assert 0 <= 1*(1-h), false for h=2: the guard is mathematically needed.
m.need(0>1*(phi([3])-2),'Sentinel counterexample to unguarded formula')
print(json.dumps(dict(status='PASS_NEW_SHIFTED_CANONICAL_MASS',identities=identities,inequalities=inequalities,sharp_cases=sharp,sentinel_cases=sentinel,affine_checks=affine,invalid_recipes_rejected=bad,global_upper_bound_certified=False)))
