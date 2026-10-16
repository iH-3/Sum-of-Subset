#!/usr/bin/env python3
"""Integer-exact prefix inverse using the audited threshold-17 non-AP lemma.

The report proves the prefix dichotomy. This module checks its finite parameter
choices and exact integer inversion, rather than assuming sampled cases prove it.
"""
from functools import lru_cache
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import nonap_sharp
from upper97 import flexible_inverse
require=nonap_sharp.require


def inverse_step(v,k):
    require(type(v) is int and v>=0 and type(k) is int and k>=1,'Invalid inverse parameters')
    q,s=divmod(v,k+2)
    return k*q+min(s,k)


@lru_cache(None)
def old_floor(r,u):
    require(type(r) is int and r>=17 and type(u) is int,'Invalid old inverse inputs')
    return max(r-5,u+2-2*r,*(flexible_inverse(r,u,beta) for beta in range(2,11)))


@lru_cache(None)
def witness(r,u):
    require(type(r) is int and r>=17 and type(u) is int,'Invalid prefix inverse inputs')
    best=dict(value=old_floor(r,u),route='old')
    R=r-5
    for L in range(17,r+1):
        M=L*(L+1)//2-r
        C=old_floor(r,M+1)
        for beta in range(3,min(10,L-4)+1):
            A=R+(beta-2)*(r-L)
            v=max(0,u-R-4*beta+2)
            B=R+inverse_step(v,beta-2)
            value=min(A,B,C)
            if value>best['value']:
                best=dict(value=value,route='prefix',L=L,beta=beta,M=M,A=A,B=B,C=C)
    return best


def lower_bound(r,u):return witness(r,u)['value']


@lru_cache(maxsize=1)
def audit():
    nonap_sharp.finite_base()
    cases=0;strict_improvements=0
    for k in range(1,10):
        for v in range(601):
            t=inverse_step(v,k)
            require(t+2*(t//k)>=v,'Inverse does not reach target')
            require(t==0 or t-1+2*((t-1)//k)<v,'Inverse is not minimal')
            cases+=1
    for r in range(17,61):
        for u in range(r-3,301):
            w=witness(r,u)
            require(w['value']>=old_floor(r,u),'New inverse weakens inherited bound')
            strict_improvements+=w['value']>old_floor(r,u)
    return dict(integer_inverse_cases=cases,strict_improvement_cases=strict_improvements,
                example=witness(38,165),minimum_size=17,beta_range=[3,10])


if __name__=='__main__':
    import json
    print(json.dumps(audit(),indent=2))
