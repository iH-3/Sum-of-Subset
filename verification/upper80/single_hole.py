"""Locate the single upper target hole by the first missing subset sum.

Conditional main domain: two positive cores of ranks 32-k and 32+k,
0<=k<=17, total excess tau, and rank penalty I=k*k.  If the source
has exactly one positive target hole on each side, a small first-gap
bound puts that hole in a short interval at the top of the target.
"""
from functools import lru_cache
import json

def need(ok,message):
    if not ok:raise ValueError(message)

def tri(n):return n*(n+1)//2

@lru_cache(None)
def gap_floor(H):
    need(type(H) is int and 1<=H<=3,'Single-hole first-gap range')
    minimum=None;witness=None;cases=0
    for k in range(18):
        r,s=32-k,32+k
        for p in range(r+1):
            for q in range(s+1):
                if (p,q)==(r,s):continue
                # A complete prefix with first missing value > H has
                # sum S>=H. The unchosen coefficients are >=S+2, and
                # increase by at least one within each physical core.
                S=max(H,tri(p)+tri(q));a,b=r-p,s-q
                value=S-tri(p)-tri(q)+a*(S+1-p)+b*(S+1-q)+k*k
                if minimum is None or value<minimum:minimum=value;witness=[k,p,q,S]
                cases+=1
    return dict(H=H,mass_rank_floor=minimum,witness=witness,cases=cases)

def guards(H):
    bound=gap_floor(H)['mass_rank_floor']-1
    return [{'hole_W':1,'ONE':-1},
            {'ts':1,'tt':1,'rank_I':1,'ONE':-bound}]

def verify():
    floors=[gap_floor(H) for H in (1,2,3)]
    need([v['mass_rank_floor'] for v in floors]==[95,124,187],'Exact first-gap floors')
    examples=[([1,*range(3,34)],list(range(3,35))),
              ([1,*range(4,35)],[1,*range(4,35)]),
              ([1,*range(5,36)],[2,*range(5,36)])]
    for H,(A,B),entry in zip((1,2,3),examples,floors):
        need(len(A)==len(B)==32,'Sharp single-hole ranks')
        bits=1
        for value in A+B:bits|=bits<<value
        S=sum(A+B);missing=[i for i in range(S+1) if not bits>>i&1]
        need(missing==[H+1,S-H-1],'Sharp first-hole positions')
        need(S-2*tri(32)==entry['mass_rank_floor'],'Sharp first-gap mass')
    return dict(status='PASS_SINGLE_HOLE_LOCATION',global_upper_bound_certified=False,
                structural_applicability_certified=False,floors=floors,sharp_examples=3)

if __name__=='__main__':print(json.dumps(verify(),indent=2))
