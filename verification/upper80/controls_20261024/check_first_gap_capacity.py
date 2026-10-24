"""First-gap predecessor mass and qE end-gap capacity on actual cores."""
from pathlib import Path
import sys,json,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import first_gap_core as fg,full_window as fw,source_union as su,model as m
rng=random.Random(2026102410);checks=0;sharp=0
for case,(h,ps,pt) in enumerate(fg.CASES):
    for trial in range(100):
        k=rng.randrange(18);values={'ONE':1,'rank_k':k};E={0};extra=0
        for side,r,t,sign in [('s',32-k,ps,1),('t',32+k,pt,-1)]:
            d=sorted(rng.randrange(8) for _ in range(r-t)) if trial%4 else [0]*(r-t)
            X=([1] if t else [])+[h+i+z for i,z in enumerate(d,1)]
            tau=sum(X)-r*(r+1)//2;xi=X[-1]-r;B=h*(r-2) if t==0 else (h-1)*(r-3)
            m.need(sum(X[:-2])>=(r-2)*(r-1)//2+B,'Mandatory predecessor-prefix excess')
            m.need(X[-2]<=r-1+tau-xi-B,'First-gap predecessor bound')
            extra+=B;E.update(sign*x for x in X);values.update({'R'+side:X[-1],'t'+side:tau,'x'+side:xi})
        ev=lambda row:sum(v*values[k] for k,v in row.items())
        m.need(ev(fg.removed_prefix_mass(case))==extra,'Affine rank-dependent excess')
        Q={0}
        for q in range(1,5):
            Q={a+b for a in Q for b in E}
            if q>=2:
                bound=ev(fw.core_capacity(q,case));m.need(len(Q)<=bound,'Actual first-gap core power capacity');checks+=1;sharp+=len(Q)==bound
bad=0
for case in range(4):
    proof=dict(base_capacity='mass',core_shape=case,edges=[],covered=[])
    try:su.derive(proof)
    except ValueError:bad+=1
    else:raise ValueError('Unlicensed first-gap capacity accepted')
    su.derive(proof,case)
print(json.dumps(dict(status='PASS_NEW_FIRST_GAP_CAPACITY',actual_core_pairs=400,power_capacities=checks,sharp_cases=sharp,unlicensed_shapes_rejected=bad,global_upper_bound_certified=False)))
