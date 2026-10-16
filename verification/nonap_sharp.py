#!/usr/bin/env python3
"""Exact finite base for rho(X) >= |X|-5 when |X| >= 17 and FS(X) is not an AP.

The report proves the reduction to these deleted intervals; finite enumeration
alone does not establish the theorem for arbitrary sets or arbitrary sizes.
"""
from functools import lru_cache
from itertools import combinations
import hashlib
import json


def require(condition,message):
    if not condition:raise ValueError(message)


def invariants(elements):
    x=tuple(sorted(elements));r=len(x)
    require(r==len(set(x)) and all(type(v) is int and v>0 for v in x),'Positive distinct integers required')
    support={0};bits=1
    for v in x:
        support|={s+v for s in support};bits|=bits<<v
    require(bits.bit_count()==len(support) and all((bits>>s)&1 for s in support),'Independent support computations disagree')
    restricted={u+v for u,v in combinations((0,)+x,2)}
    defects=[v for v in x if 2*v not in restricted]
    holes=sum(x)+1-len(support);mu=len(support)-1-r*(r+1)//2
    return dict(cardinality=len(support),holes=holes,mu=mu,defects=defects,rho=mu+2-2*len(defects))


@lru_cache(maxsize=1)
def finite_base():
    counts=[];digest=hashlib.sha256();total=nonfull=0;sharp=[]
    for j in range(8,15):
        count=non=0;minimum=None;example=None
        for q in range(1,4):
            h=j+q
            for deleted in combinations(range(1,h),q):
                x=tuple(v for v in range(1,h+1) if v not in deleted)
                inv=invariants(x);count+=1
                # Both the central interval and the defect-band reduction are
                # checked on every base case in addition to the target inequality.
                support={0}
                for v in x:support|={s+v for s in support}
                low_holes=sum(v not in support for v in range(1,2*q+1))
                if j>=10:require(inv['holes']==2*low_holes,'Central interval finite check failed')
                require(all(v<=q or v>=j for v in inv['defects']),'Defect outside endpoint bands')
                require(inv['mu']==sum(h-v for v in deleted)-q*(q-1)//2-inv['holes'],'Deleted-depth identity fails')
                if inv['holes']:
                    non+=1;margin=inv['rho']-j
                    require(margin>=-5,'Sharp non-AP base fails')
                    if minimum is None or margin<minimum:minimum=margin;example=deleted
                digest.update((json.dumps([j,q,deleted,inv],sort_keys=True,separators=(',',':'))+'\n').encode())
        counts.append(dict(size=j,total=count,nonfull=non,min_rho_minus_size=minimum,example_deleted=example))
        total+=count;nonfull+=non
        require(minimum==-5,'Expected sharp finite witness absent')
    require([v['total'] for v in counts]==[164,219,285,363,454,559,679],'Finite domain incomplete')
    require([v['nonfull'] for v in counts]==[88,108,130,154,180,208,238],'Unexpected nonfull count')
    for r in (17,18,21,39,78):
        inv=invariants((1,)+tuple(range(3,r+2)))
        require(inv['rho']==r-5 and inv['holes']==2,'Sharpness family fails')
        sharp.append(dict(size=r,rho=inv['rho'],mu=inv['mu'],defects=inv['defects']))
    return dict(total=total,nonfull=nonfull,by_size=counts,enumeration_sha256=digest.hexdigest(),sharpness=sharp)


def nonap_floor(r):
    require(type(r) is int and r>=14,'Unproved non-AP range')
    return r-5 if r>=17 else r-14


if __name__=='__main__':print(json.dumps(finite_base(),indent=2))
