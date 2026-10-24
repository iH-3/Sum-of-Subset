"""Retain core holes through several maximum removals, then bound phi.

All conclusions are conditional on the size-81 main domain, j=4, W in
{1,2}, and certified fixed credit at least 38. No global bound is claimed.
"""
from functools import lru_cache
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import math
import profiles as p
from endpoint_schedule import endpoint

def floor(r,W):return W*r-W*(W+3)//2+1

@lru_cache(None)
def plan(W,credit,rank_hi):
    p.need(type(W) is int and W in (1,2) and type(credit) is int and 38<=credit<=84,'Positive kernel domain')
    p.need(type(rank_hi) is int and 0<=rank_hi<=17,'Positive kernel rank')
    C=204+2*W-credit
    ks=[k for k in range(rank_hi+1) if k*k+max(64,-W*W+61*W+2)<=C]
    answer={}
    for side,sign in [('s',-1),('t',1)]:
        witnesses=[];depth=0
        if not ks:
            answer[side]=dict(depth=0,witnesses=[]);continue
        for q in range(1,min(32+sign*k-15 for k in ks)+1):
            level=[]
            for k in ks:
                r=32+sign*k;n=r-q;cap=C-k*k-floor(64-r,W)
                # Every later first gap would exceed the full side budget.
                delayed=min((r-i)*(p.tri(i)+1-i) for i in range(n,r))
                if delayed<=cap:break
                # Inductively each removed maximum has deviation >= W:
                # otherwise the beta=W-1 density theorem fills all but 2W-2 holes.
                truncated_cap=cap-q*W
                if p.tri(n)<=truncated_cap:break
                try:schedule=endpoint(n,truncated_cap)
                except ValueError:break
                margin=p.tri(n)-2*schedule['H']+1-(r+cap)
                if margin<0:break
                level.append(dict(k=k,r=r,q=q,cap=cap,delayed_gap_floor=delayed,
                                  schedule=schedule,propagation_margin=margin))
            else:
                depth=q;witnesses.extend(level);continue
            break
        answer[side]=dict(depth=depth,witnesses=witnesses)
    return answer

def rows(W,side,q):
    p.need(W in (1,2) and side in 'st' and type(q) is int and q>=1,'Positive kernel row')
    sign=-1 if side=='s' else 1
    rhs=-32*W+W*q+W*(W+3)//2-1+p.tri(q-1)
    label='positive retained kernel '+str(W)+' '+side+' '+str(q)
    return [({'phicore'+side:q,'t'+side:-1,'rank_k':W*sign},rhs,label),
            ({'phicore'+side:q-1,'x'+side:1,'t'+side:-1,'rank_k':W*sign},rhs,label)]

def combined_rows(W,credit,rank_hi,q):
    import combined_holes
    spec=plan(W,credit,rank_hi)
    p.need(type(q) is int and 1<=q<=min(v['depth'] for v in spec.values()),'Combined retained kernel depth')
    ks=sorted({v['k'] for v in spec['s']['witnesses'] if v['q']==q})
    N=64-2*q;mass=N if W==1 else 2*N-2
    for k in ks:combined_holes.prove(32-k-q,32+k-q,mass-1,2*W-2)
    label='combined retained kernel '+str(W)+' '+str(q)
    return [({'ts':-1,'tt':-1,'F':-q},-mass-65*q+q*(q-1),label),
            ({'ts':-1,'tt':-1,'xs':1,'xt':1,'F':1-q},-mass-65*(q-1)+q*(q-1),label)]

def verify():
    controls=[];count=0
    for W in (1,2):
        for credit in (38,44,50,60):
            spec=plan(W,credit,10)
            for side,entry in spec.items():
                for witness in entry['witnesses']:
                    p.need(witness['propagation_margin']>=0,'Retained kernel propagation')
                    n=witness['r']-witness['q'];cap=witness['cap']-witness['q']*W
                    p.need(n>=15 and p.tri(n)>cap and witness['delayed_gap_floor']>witness['cap'],'Retained kernel structural budget')
                for q in range(1,entry['depth']+1):
                    for k in range(11):
                        r=32+(-k if side=='s' else k)
                        for phi in range(16):
                            xi=max(phi,W)+2
                            # Algebraic floors on the prefix and the last q deviations.
                            for which,(body,rhs,_) in enumerate(rows(W,side,q)):
                                tail=q*phi-p.tri(q-1) if which==0 else xi+(q-1)*phi-p.tri(q-1)
                                tau=floor(r-q,W)+tail
                                values={'phicore'+side:phi,'x'+side:xi,'t'+side:tau,'rank_k':k}
                                p.need(sum(c*values[key] for key,c in body.items())==rhs,'Exact retained kernel identity');count+=1
            controls.append(dict(W=W,credit=credit,depths={s:v['depth'] for s,v in spec.items()},witnesses=sum(len(v['witnesses']) for v in spec.values())))
            for q in range(1,min(v['depth'] for v in spec.values())+1):
                combined_rows(W,credit,10,q)
    import random
    rng=random.Random(241081);actual=0;prefixes=0;combined_checks=0
    def holes(values):
        bits=1
        for value in values:bits|=bits<<value
        return sum(values)+1-bits.bit_count()
    for W in (1,2):
        C=204+2*W-38;spec=plan(W,38,10)
        for _ in range(500):
            k=rng.randrange(8);cores={};values={'rank_k':k}
            for side,r in [('s',32-k),('t',32+k)]:
                base=list(range(2,r+2)) if W==1 else [2,*range(4,r+3)]
                extra=sorted(rng.randrange(5) for _ in range(5))
                core=base[:-5]+[x+d for x,d in zip(base[-5:],extra)]
                cores[side]=core;values['t'+side]=sum(core)-p.tri(r);values['x'+side]=core[-1]-r
                values['phicore'+side]=min([r]+[q+core[r-q-1]-(r-q) for q in range(r)])
            if k*k+values['ts']+values['tt']>C:continue
            p.need(holes(cores['s']+cores['t'])>=2*W,'Actual positive-hole test fixture')
            values['F']=65-values['phicores']-values['phicoret']
            for side,core in cores.items():
                for q in range(1,spec[side]['depth']+1):
                    p.need(holes(core[:-q])>=holes(core)>=2*W,'Actual retained predecessor holes');prefixes+=1
                    for body,rhs,_ in rows(W,side,q):
                        p.need(sum(c*values[key] for key,c in body.items())<=rhs,'Actual core retained kernel')
            for q in range(1,min(v['depth'] for v in spec.values())+1):
                p.need(holes(cores['s'][:-q]+cores['t'][:-q])>=holes(cores['s']+cores['t']),
                       'Actual combined retained holes')
                for body,rhs,_ in combined_rows(W,38,10,q):
                    p.need(sum(c*values[key] for key,c in body.items())<=rhs,'Actual combined retained kernel');combined_checks+=1
            actual+=1
    p.need(actual>400,'Nonvacuous positive-kernel set controls')
    return dict(status='PASS_CONDITIONAL_POSITIVE_KERNEL',global_upper_bound_certified=False,structural_applicability_certified=False,algebra_checks=count,actual_core_pairs=actual,actual_retained_prefixes=prefixes,actual_combined_rows=combined_checks,plans=controls)

if __name__=='__main__':
    import json
    print(json.dumps(verify(),indent=2))
