"""New canonical-prefix mass capacity inside the complete 2D union."""
from pathlib import Path
import sys,json,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import source_union as su,first_gap_core as fg,model as m
rng=random.Random(2026102418);checks=improved=rebates=0
for shape in [None,0,1,2,3]:
    for trial in range(24):
        k=rng.randrange(18);v={'ONE':1,'rank_k':k};E={0};T=[];orders={}
        for side,r,sign in [('s',32-k,1),('t',32+k,-1)]:
            h=t=0
            if shape is not None:
                h,ps,pt=fg.CASES[shape];t=ps if side=='s' else pt
            n=r-t;phi0=rng.randrange(2,14)
            d=[max(0,phi0-n+i) for i in range(1,n+1)]
            X=([1] if t else [])+[h+i+y for i,y in enumerate(d,1)]
            phi=min([r,*[x+r-2*i for i,x in enumerate(X,1)]]);E.update(sign*x for x in X)
            v.update({'R'+side:X[-1],'x'+side:X[-1]-r,'t'+side:sum(X)-r*(r+1)//2,'phicore'+side:phi})
            orders[side]=min(12,max(0,phi-h+t-2))
            offsets=sorted(rng.sample(range(1,150),4));v.update({off+side:x for off,x in zip('abce',offsets)})
            T.extend(sign*(X[-1]+x) for x in offsets)
        D=E|set(T);v.update(K=len({a+b for a in D for b in D}),F=65-v['phicores']-v['phicoret'])
        ev=lambda row:sum(c*v[key] for key,c in row.items());covered=[]
        witnesses=[(w,'ordinary') for w in ('double_prefix','zero','core_s','core_t',*range(8))]
        if shape is not None:witnesses += [('shape_double','ordinary')]
        for pair in su.PAIRS:
            for witness,interval in witnesses:
                if all(ev(g)<=0 for g in su.membership(pair,witness,shape,interval)):
                    covered.append(dict(pair=pair,witness=witness));break
        proof=dict(base_capacity='mass',edges=[i for i,g in enumerate(su.gaps()) if ev(g)<v['F']],covered=covered,core_prefix=orders)
        if shape is not None:proof['core_shape']=shape
        row,guards=su.derive(proof,shape);old,_=su.derive({key:value for key,value in proof.items() if key!='core_prefix'},shape)
        m.need(all(ev(g)<=0 for g in guards) and ev(row)<=0,'Actual canonical complete source capacity')
        checks+=1;improved+=ev(row)>ev(old);rebates+=len(covered)
bad=0
for mode,prefix in [('mass',{'s':13}),('mass',{'z':0}),('hull',{'s':1}),('mass',[1])]:
    try:su.derive(dict(base_capacity=mode,core_prefix=prefix,edges=[],covered=[]))
    except ValueError:bad+=1
    else:raise ValueError('Invalid canonical source prefix accepted')
print(json.dumps(dict(status='PASS_NEW_CANONICAL_SOURCE_CAPACITY',actual_source_sets=checks,strictly_improved=improved,rebated_pairs=rebates,invalid_recipes_rejected=bad,global_upper_bound_certified=False)))
