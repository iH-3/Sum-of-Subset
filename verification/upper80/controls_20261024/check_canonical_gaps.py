"""Mandatory prefix mass from the actual canonical minimum, with shapes."""
from pathlib import Path
import sys,json,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import core_gap as cg,first_gap_core as fg,full_window as fw,model as m
rng=random.Random(2026102417);prefixes=powers=empty=sharp=0
for case in [None,0,1,2,3]:
    for trial in range(40):
        k=rng.randrange(18);v={'ONE':1,'rank_k':k};E={0};orders={}
        for side,r,sign in [('s',32-k,1),('t',32+k,-1)]:
            h=t=0
            if case is not None:
                h,ps,pt=fg.CASES[case];t=ps if side=='s' else pt
            n=r-t;w=h-t;phi0=rng.randrange(1,10)
            d=[max(0,phi0-n+i) for i in range(1,n+1)] if trial%2==0 else sorted(rng.randrange(10) for _ in range(n))
            X=([1] if t else [])+[h+i+y for i,y in enumerate(d,1)];phi=min([r,*[x+r-2*i for i,x in enumerate(X,1)]]);E.update(sign*x for x in X)
            v.update({'R'+side:X[-1],'x'+side:X[-1]-r,'t'+side:sum(X)-r*(r+1)//2,'phicore'+side:phi})
            ev=lambda row:sum(c*v[key] for key,c in row.items());base=ev(fg.removed_side_prefix_mass(case,side)) if case is not None else 0
            actual=sum(X[:-2])-(r-2)*(r-1)//2
            for order in range(13):m.need(base+ev(cg.canonical_prefix(side,order,case))<=actual,'Canonical mandatory predecessor prefix');prefixes+=1
            orders[side]=min(12,max(0,phi-w-2))
        ev=lambda row:sum(c*v[key] for key,c in row.items());Q={0}
        for q in range(1,5):
            Q={a+b for a in Q for b in E}
            if q>=2:
                cap=ev(fw.core_capacity(q,case,orders));m.need(len(Q)<=cap,'Actual canonically strengthened qE capacity');powers+=1;sharp+=len(Q)==cap
            if q==4:
                for side in 'st':
                    lo,hi=cg.gap_interval((0,0),side,case,orders[side]);a,b=ev(lo),ev(hi)
                    m.need(not any(a<=x<=b for x in Q),'Canonical extreme interval contains no sum');empty+=1
bad=0
for side,order,shape in [('s',13,None),('s',-1,None),('',1,None),('s',1,4)]:
    try:cg.canonical_prefix(side,order,shape)
    except ValueError:bad+=1
    else:raise ValueError('Unlicensed canonical prefix accepted')
print(json.dumps(dict(status='PASS_NEW_CANONICAL_EXTREME_GAPS',actual_core_pairs=200,prefix_mass_checks=prefixes,core_power_capacities=powers,sharp_capacities=sharp,empty_intervals=empty,invalid_recipes_rejected=bad,global_upper_bound_certified=False)))
