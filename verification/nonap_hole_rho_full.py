#!/usr/bin/env python3
"""Persistent-hole rho bounds using the full-prefix central interval theorem."""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from nonap_sharp import require


def row(r,beta,L,anchored=False):
    require(all(type(v) is int for v in (r,beta,L)),'Integer hole-rho parameters required')
    require(beta>=2 and r>=L>=max(17,2*beta+4),'Unproved hole-rho parameters')
    require(type(anchored) is bool and (not anchored or L>=18),'Unproved sharp prefix anchor')
    T=L*(L+1)//2
    A=(beta-1)*(r-L+1)+(L-6 if anchored else 0)
    C1=T-(L if anchored else 0)-r-1
    C2=T+L-6*beta-r-7
    return dict(r=r,beta=beta,L=L,anchored=anchored,A=A,C1=C1,C2=C2,value=min(A,C1,C2))


@lru_cache(None)
def beta_witness(r,beta):
    candidates=[row(r,beta,L,anchored) for L in range(max(17,2*beta+4),r+1)
                for anchored in (False,True) if not anchored or L>=18]
    require(candidates,'Empty hole-rho range')
    return max(candidates,key=lambda w:(w['value'],-w['L'],w['anchored']))


@lru_cache(None)
def witness(r,z):
    require(type(r) is int and r>=17 and type(z) is int and z>=0,'Invalid hole-rho query')
    out=dict(value=0,route='none')
    for beta in range(2,min(20,(r-4)//2,(z-1)//2)+1):
        w=beta_witness(r,beta)
        if w['value']>out['value']:out=dict(w,route='persistent-holes')
    return out


def lower_bound(r,z):return witness(r,z)['value']


@lru_cache(maxsize=1)
def full_prefix_base():
    """Finite boundary check; the arbitrary-size statement is proved in the report."""
    cases=0
    for beta in range(2,7):
        size=2*beta+4
        for deletions in range(beta+1):
            maximum=size+deletions
            for missing in combinations(range(1,maximum),deletions):
                absent=set(missing);support=1;total=0
                for x in range(1,maximum+1):
                    if x not in absent:support|=support<<x;total+=x
                lower=[h for h in range(1,2*beta+1) if not (support>>h)&1]
                require(len(lower)<=deletions,'Too many lower endpoint holes')
                expected=(1<<(total+1))-1
                for h in lower:expected&=~((1<<h)|(1<<(total-h)))
                require(support==expected,'Full-prefix endpoint description fails')
                cases+=1
    return dict(cases=cases,beta_range=[2,6],size='2*beta+4',
                deletions='0..beta; maximum retained',status='PASS')


@lru_cache(maxsize=1)
def audit():
    cases=0
    for r in range(17,60):
        for beta in range(2,min(20,(r-4)//2)+1):
            w=beta_witness(r,beta)
            require(w==row(r,beta,w['L'],w['anchored']),'Malformed hole-rho witness')
            for L in range(max(17,2*beta+4),r+1):
                for anchored in (False,True):
                    if anchored and L<18:continue
                    v=row(r,beta,L,anchored);cases+=1
                    require(w['value']>=v['value'],'Witness is not the searched maximum')
            require(witness(r,2*beta+1)['value']>=w['value'],'Hole threshold omitted')
    return dict(parameter_rows=cases,beta_max=20,minimum_size=17,
                full_prefix_base=full_prefix_base(),
                examples=[dict(z=z,**witness(r,z)) for r,z in ((36,19),(40,19),(38,19))],
                scope='exact parameter checks; the general contradiction proof is in the report')


if __name__=='__main__':
    import json
    print(json.dumps(audit(),indent=2))
