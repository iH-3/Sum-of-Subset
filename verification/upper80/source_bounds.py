"""Direct regression checks for proved source lemmas; not a global N bound.

The general arguments are in reports/upper80_progress_20261023.tex.
Small exhaustive and seeded checks are regression tests, not a replacement for
those arguments. Every check uses exact integers and explicit sets.
"""
from itertools import combinations
from random import Random
import json


def need(ok, message):
    if not ok:
        raise ValueError(message)


def trim_bound(positive, negative, rs, rt):
    """Delete each core maximum; put all ten peeled points back explicitly."""
    D={0,*positive,*(-x for x in negative)}
    K=len({a+b for a in D for b in D})
    endpoints=[];fringes=[]
    for side,r in ((positive,rs),(negative,rt)):
        R=side[r-1];tau=sum(side[:r])-r*(r+1)//2;xi=R-r
        q=r-1+tau-xi
        peeled=side[r-1:]
        need(len(peeled)==5,'Exactly five peeled points per side')
        endpoints.append(q)
        fringes.append(sum(a+b>side[-1]+q for i,a in enumerate(peeled) for b in peeled[i:]))
    bound=positive[-1]+negative[-1]+sum(endpoints)+1+sum(fringes)
    need(K<=bound,'Trimmed source hull inequality')
    return K,bound


def verify():
    missing=0
    for n in range(1,8):
        for values in combinations(range(1,n+7),n):
            absent=[x for x in range(1,n+1) if x not in values]
            tau=sum(values)-n*(n+1)//2
            for q in range(1,len(absent)+1):
                need(tau>=q*n+q*(q+1)//2-sum(absent[-q:]),'Missing-probe mass bound')
                missing+=1
    diameter=0
    for mask in range(1<<10):
        Q={0}|{i+1 for i in range(10) if mask>>i&1}
        for x in range(1,12):
            if max(Q)>=2*x:continue
            need(len(Q&{v+x for v in Q})>=len(Q)-x,'Strict diameter overlap')
            diameter+=1
    Q={0,2}
    need(len(Q&{v+1 for v in Q})<len(Q)-1,'Diameter equality negative control')
    exhaustive=0
    for r in (1,2,3):
        sets=list(combinations(range(1,10),r+4))
        for p in sets:
            for n in sets:
                trim_bound(p,n,r,r);exhaustive+=1
    rng=Random(20261023);seeded=0;prefixes=0;nonempty_hits=0
    for _ in range(5000):
        rs=rng.randrange(8,36);rt=rng.randrange(8,36)
        def make_side(r):
            defects=[0]*(r-4)+sorted(rng.randrange(4) for _ in range(4))
            core=[i+1+d for i,d in enumerate(defects)]
            offsets=([1,2]+sorted(rng.sample(range(3,151),2))) if rng.randrange(2) else sorted(rng.sample(range(1,151),4))
            return core+[core[-1]+off for off in offsets]
        p=make_side(rs);n=make_side(rt)
        trim_bound(p,n,rs,rt);seeded+=1
        D={0,*p,*(-x for x in n)}
        for q in range(1,6):
            parts=[];outside=[]
            for values,r in ((p,rs),(n,rt)):
                core=values[:-q];rank=len(core);mass=sum(core)-rank*(rank+1)//2
                L=rank-mass
                need(all(x in core for x in range(1,L+1)),'Mass-forced prefix')
                parts.append(L);outside.append(values[-q:])
            for gap in (1,17,49,69):
                hits={a for a in outside[0] if -parts[1]<=a-gap<=parts[0]}
                hits|={gap-b for b in outside[1] if -parts[1]<=gap-b<=parts[0]}
                counted=sum(-parts[1]<=a-gap<=parts[0] for a in outside[0])+sum(-parts[1]<=gap-b<=parts[0] for b in outside[1])
                need(len(hits)==counted and hits<=D&{v+gap for v in D},'Distinct exterior overlap points')
                prefixes+=1;nonempty_hits+=bool(hits)
    need(nonempty_hits>1000,'Exterior overlap tests must exercise actual hits')
    side=list(range(1,32))+[40,41,42,43,85]
    K,bound=trim_bound(side,side,32,32)
    need((K,bound)==(243,243),'Sharp trimmed-source example')
    old=2*85+2*40+1+8
    need(old==259 and K>bound-1,'Sharpness negative control')
    return dict(status='PASS_SOURCE_LEMMAS',global_upper_bound_certified=False,
                missing_probe_checks=missing,diameter_checks=diameter,
                exhaustive_sources=exhaustive,seeded_sources=seeded,
                exterior_overlap_checks=prefixes,nonempty_overlap_checks=nonempty_hits,
                sharp_example=dict(cardinality=73,actual_sumset=K,new_upper_bound=bound,old_upper_bound=old),
                negative_controls=2)

if __name__=='__main__':
    print(json.dumps(verify(),indent=2))
