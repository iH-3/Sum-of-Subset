#!/usr/bin/env python3
"""Exact witnesses for the variable-threshold persistent-hole theorem.

General proof: reports/upper90_from91_20261018.tex. Finite audits check
the witness arithmetic; they do not replace that arbitrary-set proof.
"""
from functools import lru_cache
import nonap_hole_rho_full as previous
from nonap_sharp import require


def validate(r,z,L,B,thresholds):
    require(all(type(v) is int for v in (r,z,L,B)), 'Integer parameters required')
    require(r>=L>=18 and z>=5 and B>=0, 'Unproved parameter range')
    require(len(thresholds)==r-L+1, 'Incomplete threshold schedule')
    require(B<=L*(L-1)//2-r-1, 'AP-prefix escape not excluded')
    for i,beta in zip(range(L,r+1),thresholds):
        require(type(beta) is int and beta>=2, 'Invalid prefix threshold')
        require(2*beta<z and i>=2*beta+4, 'Unlicensed central interval')
        require(B<=i*(i+1)//2+i-6*beta-r-7, 'Large-jump escape not excluded')
    A=L-6+sum(beta-1 for beta in thresholds)
    require(A>=B, 'Increment accumulation does not reach target')
    return dict(r=r,z=z,L=L,value=B,thresholds=list(thresholds),accumulation=A,
                escape=L*(L-1)//2-r-1,route='variable-threshold')


@lru_cache(None)
def _schedule(r,z):
    best=dict(value=0,route='none')
    for L in range(18,r+1):
        def thresholds(B):
            return [min((i-4)//2,(z-1)//2,(i*(i+1)//2+i-r-7-B)//6)
                    for i in range(L,r+1)]
        lo,hi=0,max(0,L*(L-1)//2-r-1)
        while lo<hi:
            B=(lo+hi+1)//2;bs=thresholds(B)
            if min(bs)>=2 and L-6+sum(b-1 for b in bs)>=B:lo=B
            else:hi=B-1
        bs=thresholds(lo)
        if lo>best['value'] and min(bs)>=2:best=validate(r,z,L,lo,bs)
    return best


@lru_cache(None)
def witness(r,z):
    require(type(r) is int and r>=17 and type(z) is int and z>=0,'Invalid hole-rho query')
    old=previous.witness(r,z)
    new=_schedule(r,min(z,2*((r-4)//2)+1)) if z>=5 else dict(value=0,route='none')
    return new if new['value']>old['value'] else dict(old,route='previous-'+old['route'])


def lower_bound(r,z):return witness(r,z)['value']


def finite_sets():
    from itertools import combinations
    import random
    rng=random.Random(20261018);cases=eligible=0;seen=set()
    for r in range(17,48):
        for q in range(14):
            maximum=r+q
            patterns=[tuple(range(1,q+1))]
            patterns += [tuple(sorted(rng.sample(range(1,maximum),q))) for _ in range(5)]
            for absent in patterns:
                X=tuple(v for v in range(1,maximum+1) if v not in absent)
                if X in seen:continue
                seen.add(X);bits=1
                for v in X:bits|=bits<<v
                size=bits.bit_count();holes=sum(X)+1-size;cases+=1
                if not 0<holes<size-1:continue
                restricted={x+y for x,y in combinations((0,)+X,2)}
                rho=size-1-r*(r+1)//2+2-2*sum(2*v not in restricted for v in X)
                require(rho>=lower_bound(r,holes),'Scheduled floor fails on an actual finite set')
                eligible+=1
    return dict(cases=cases,strict_hole_cases=eligible,seed=20261018,
                scope='deterministic finite sanity check, not a proof for arbitrary sets')


@lru_cache(maxsize=1)
def audit():
    cases=improved=0
    for r in range(17,60):
        last=0
        for z in range(2*r+1):
            w=witness(r,z);cases+=1
            require(w['value']>=previous.lower_bound(r,z),'Inherited floor weakened')
            require(w['value']>=last,'Hole floor is not monotone');last=w['value']
            if w['route']=='variable-threshold':
                require(w==validate(w['r'],w['z'],w['L'],w['value'],w['thresholds']),'Invalid witness')
                improved+=1
    return dict(cases=cases,improved=improved,finite_sets=finite_sets(),previous=previous.audit(),
                examples=[dict(query=[r,z],witness=witness(r,z)) for r,z in ((37,15),(37,19),(37,215))])


if __name__=='__main__':
    import json
    print(json.dumps(audit(),indent=2))
