"""Actual extreme holes of qE and qD, with endpoint/off-by-one controls."""
from pathlib import Path
import sys,json,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import full_cover as fc,core_gap as cg,first_gap_core as fg,model as m
rng=random.Random(2026102413);checks=0;nonempty=0;probes=0;endpoints=0
for shape in (None,0,1,2,3):
    for trial in range(20):
        k=rng.randrange(18);values={'ONE':1,'rank_k':k};E={0};D={0}
        h,ps,pt=(0,0,0) if shape is None else fg.CASES[shape]
        for side,r,t,sign in [('s',32-k,ps,1),('t',32+k,pt,-1)]:
            X=([1] if t else [])+[h+i for i in range(1,r-t+1)];X[-1]+=rng.randrange(26)
            offsets=sorted(rng.sample(range(1,151),4));R=X[-1]
            values.update({'R'+side:R,'M'+side:R+offsets[-1],'t'+side:sum(X)-r*(r+1)//2,'x'+side:R-r,'X'+side:120,'g'+side:8,'h'+side:20,'d'+side:40})
            values.update({off+side:x for off,x in zip('abce',offsets)})
            E.update(sign*x for x in X);D.update(sign*x for x in X);D.update(sign*(R+x) for x in offsets)
        ev=lambda row:sum(v*values[k] for k,v in row.items())
        powers={'E':{0},'D':{0}}
        for q in range(1,5):
            root=next(i for i,a in enumerate(fc.roots()) if len(a)==4-q)
            for typ,Q,node,case in [('E',E,(root,0),shape),('D',D,(root,-1),None)]:
                powers[typ]={a+b for a in powers[typ] for b in Q}
                lo,hi=fc.interval(*node);centre=ev(lo)-q*min(Q);actual={v+centre for v in powers[typ]}
                for side in 'st':
                    left,right=cg.gap_interval(node,side,case);a,b=ev(left),ev(right)
                    m.need(not (set(range(a,b+1))&actual),'Extreme interval is empty in the actual sumset');checks+=1;nonempty+=a<=b
                    for width in (1,2,3):
                        if b-a+1>=width:
                            m.need(all(ev(g)<=0 for g in cg.guards({'ONE':a},node,width,side,case)),'Whole target probe fits empty interval');probes+=1
                    extreme=ev(hi if side=='s' else lo);m.need(extreme in actual,'Actual extreme is present')
                    m.need(any(ev(g)>0 for g in cg.guards({'ONE':extreme},node,1,side,case)),'Do not exclude the present extreme');endpoints+=1
bad=0
for node,side,shape in [((next(i for i,a in enumerate(fc.roots()) if len(a)==4),-1),'s',None),((0,0),'x',None),((0,-1),'s',0)]:
    try:cg.gap_interval(node,side,shape)
    except ValueError:bad+=1
    else:raise ValueError('Invalid extreme-gap recipe accepted')
print(json.dumps(dict(status='PASS_NEW_CORE_EXTREME_GAPS',actual_sources=100,empty_intervals=checks,nonempty_intervals=nonempty,whole_probe_checks=probes,present_endpoint_controls=endpoints,invalid_recipes=bad,global_upper_bound_certified=False)))
