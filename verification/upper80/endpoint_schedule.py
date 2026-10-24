"""Exact adaptive endpoint schedules used in the size-81 research reduction.

This checks numerical licenses; the universal set-theoretic argument is
recorded in research_checkpoint.md. It does not certify a global bound.
"""
from functools import lru_cache

def tri(n):return n*(n+1)//2
def need(ok,message):
    if not ok:raise ValueError(message)

def check(witness):
    r,R,B,H,L=(witness[k] for k in ('r','R','B','H','L'))
    bs=witness['thresholds']
    need(all(type(v) is int for v in (r,R,B,H,L,*bs)),'Integer schedule')
    need(B==R+1 and 18<=L<=r and len(bs)==r-L+1 and H>=4 and H%2==0,'Schedule shape')
    for i,b in zip(range(L,r+1),bs):
        need(2<=b<=H//2 and i>=(b+5 if b<=24 else 2*b+4),'Density schedule license')
        need(B<=tri(i)+i-5*b-r-7,'Strict late-jump license')
    need(B<=L-6+sum(b-1 for b in bs),'No-AP-prefix budget')
    for t in range(L-1,r):
        need(B<=tri(t)-t-2+sum(bs[i-L]-1 for i in range(t+2,r+1)),'Every last-AP-prefix budget')
    return True

@lru_cache(None)
def endpoint(r,R):
    B=R+1
    for H in range(4,2*r,2):
        for L in range(18,r+1):
            bs=[min(max(min(24,i-5),(i-4)//2),H//2,(tri(i)+i-r-7-B)//5) for i in range(L,r+1)]
            witness=dict(r=r,R=R,B=B,H=H,L=L,thresholds=bs)
            try:check(witness)
            except ValueError:continue
            return witness
    raise ValueError(('No endpoint schedule',r,R))
