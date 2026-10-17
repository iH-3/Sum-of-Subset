#!/usr/bin/env python3
"""Exact arithmetic and sanity checks for retained-prefix inequalities.

The general proof is in reports/upper89_from90_20261018.tex.
Finite examples do not replace that proof.
"""
from functools import lru_cache
from math import gcd
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from nonap_sharp import invariants, require


def witness(r, rho_upper, depth=2):
    require(all(type(v) is int for v in (r, rho_upper, depth)), 'Integer parameters required')
    require(depth >= 1 and r-depth >= 17, 'Sharp retained prefix out of range')
    escape = (r-depth)*(r-depth+1)//2-r-1
    require(rho_upper < escape, 'A disjoint prefix step has not been excluded')
    return dict(size=r, depth=depth, rho_upper=rho_upper, escape=escape,
                surplus=escape-rho_upper, prefix_size=r-depth,
                rho_floor=r-depth-5, mu_floor=r-depth-3,
                hole_denominator=2**depth)


def support(x):
    out={0}
    for v in x:out |= {s+v for s in out}
    return out


@lru_cache(maxsize=1)
def audit():
    import random
    rng=random.Random(20261018)
    cases=intersections=disjoint=eligible=0
    seen=set()
    for r in range(19,35):
        for q in range(10):
            for sample in range(5):
                deleted=set(rng.sample(range(1,r+q),q))
                x=tuple(v for v in range(1,r+q+1) if v not in deleted)
                for scale,last in ((1,x[-1]),(1,sum(x[:-1])-1),(1,sum(x[:-1])+1),(2,2*x[-1]+1)):
                    X=tuple(scale*v for v in x[:-1])+(last,)
                    if X[-1]<=X[-2] or X in seen:continue
                    seen.add(X);Y=X[:-1];R=X[-1]
                    sx,sy=support(X),support(Y)
                    ix,iy=invariants(X),invariants(Y);cases+=1
                    y=len(sx)-len(sy)-r
                    require(ix['rho']>=iy['rho']+y-2,'Defect recurrence fails')
                    require(R==r+y+ix['holes']-iy['holes'],'Maximum-removal identity fails')
                    require(R<=r+ix['rho']+ix['holes']+2-iy['rho']-iy['holes'],'Retained span fails')
                    intersects=bool(sy & {R+v for v in sy})
                    if intersects:
                        intersections+=1
                        require(ix['holes']<=2*iy['holes'],'Two-copy hole inequality fails')
                        require(gcd(*X)==gcd(*Y),'Intersection changed the coefficient gcd')
                        if gcd(*X)==1 and ix['holes']>0:
                            require(iy['holes']>0,'Non-progression did not persist backwards')
                    else:
                        disjoint+=1
                        require(ix['rho']>=r*(r-1)//2-r-1,'Disjoint-step escape fails')
                    if gcd(*X)!=1 or ix['holes']==0:continue
                    for depth in (1,2):
                        try:w=witness(r,ix['rho'],depth)
                        except ValueError:continue
                        Z=X[:-depth];iz=invariants(Z);eligible+=1
                        require(gcd(*Z)==1 and iz['holes']>0,'Retained prefix is not primitive/non-AP')
                        require(iz['rho']>=w['rho_floor'] and iz['mu']>=w['mu_floor'],'Sharp retained prefix floor fails')
                        require(2**depth*iz['holes']>=ix['holes'],'Iterated hole bound fails')
    # The factor two cannot in general be replaced by one.
    Y=(1,)+tuple(range(3,20));R=sum(Y)-1;X=Y+(R,)
    ix,iy=invariants(X),invariants(Y)
    require(support(Y)&{R+s for s in support(Y)},'Hole-factor example is disjoint')
    require(ix['holes']==2*iy['holes']>iy['holes'],'Missing sharp hole-factor example')
    return dict(cases=cases,intersections=intersections,disjoint=disjoint,
                retained_prefix_checks=eligible,seed=20261018,
                sharp_hole_factor=dict(prefix=list(Y),last=R,holes=ix['holes'],prefix_holes=iy['holes']),
                scope='Finite sanity checks supplement the arbitrary-size proof')


if __name__=='__main__':
    import json
    print(json.dumps(audit(),indent=2))
