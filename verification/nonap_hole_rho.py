#!/usr/bin/env python3
"""Direct rho lower bounds from persistent holes; general proof is in the report."""
from functools import lru_cache
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from nonap_sharp import require


def row(r,beta,L):
    require(all(type(v) is int for v in (r,beta,L)),'Integer hole-rho parameters required')
    require(beta>=2 and r>=L>=max(17,2*beta+5),'Unproved hole-rho parameters')
    T=L*(L+1)//2
    A=(beta-1)*(r-L+1)
    C1=T-r-1
    C2=T+L-6*beta-r-7
    return dict(r=r,beta=beta,L=L,A=A,C1=C1,C2=C2,value=min(A,C1,C2))


@lru_cache(None)
def beta_witness(r,beta):
    candidates=[row(r,beta,L) for L in range(max(17,2*beta+5),r+1)]
    require(candidates,'Empty hole-rho range')
    return max(candidates,key=lambda w:(w['value'],-w['L']))


@lru_cache(None)
def witness(r,z):
    require(type(r) is int and r>=17 and type(z) is int and z>=0,'Invalid hole-rho query')
    out=dict(value=0,route='none')
    for beta in range(2,min(20,(r-5)//2,(z-1)//2)+1):
        w=beta_witness(r,beta)
        if w['value']>out['value']:out=dict(w,route='persistent-holes')
    return out


def lower_bound(r,z):return witness(r,z)['value']


@lru_cache(maxsize=1)
def audit():
    cases=0
    for r in range(17,60):
        for beta in range(2,min(20,(r-5)//2)+1):
            w=beta_witness(r,beta)
            require(w==row(r,beta,w['L']),'Malformed hole-rho witness')
            for L in range(max(17,2*beta+5),r+1):
                v=row(r,beta,L);cases+=1
                require(w['value']>=v['value'],'Witness is not the searched maximum')
            require(witness(r,2*beta+1)['value']>=w['value'],'Hole threshold omitted')
    return dict(parameter_rows=cases,beta_max=20,minimum_size=17,
                examples=[dict(z=z,**witness(r,z)) for r,z in ((36,19),(40,19),(38,19))],
                scope='exact parameter checks; the general contradiction proof is in the report')


if __name__=='__main__':
    import json
    print(json.dumps(audit(),indent=2))
