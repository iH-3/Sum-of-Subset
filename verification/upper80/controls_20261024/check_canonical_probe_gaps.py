"""New canonical-prefix interface for existing exact target probes."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import model as m,full_cover as fc,core_gap as cg
v={'ONE':1,'rank_k':0};sets={}
for side,phi,jump in [('s',8,30),('t',6,23)]:
    d=[max(0,phi-32+i) for i in range(1,33)];d[-1]+=jump;X=[i+a for i,a in enumerate(d,1)];sets[side]=X
    v.update({'R'+side:X[-1],'x'+side:d[-1],'t'+side:sum(d),'phicore'+side:min([32,*[x+32-2*i for i,x in enumerate(X,1)]])})
    v.update({'M'+side:X[-1]+20,'X'+side:1,'g'+side:1,'h'+side:1,'d'+side:1})
    v.update({o+side:a for o,a in zip('abce',[1,3,8,20])})
ev=lambda row:sum(a*v[k] for k,a in row.items());E={0,*sets['s'],*(-x for x in sets['t'])};Q={0};checked=nonempty=0
for power in range(1,5):
    Q={a+b for a in Q for b in E};root=next(i for i,r in enumerate(fc.roots()) if len(r)==4-power and all(j==0 for j in r));node=(root,0)
    centre=ev(fc.interval(*node)[0])+power*v['Rt'];actual={x+centre for x in Q}
    for side in 'st':
        for prefix in (0,1,4,7,12):
            lo,hi=cg.gap_interval(node,side,None,prefix);a,b=ev(lo),ev(hi)
            if b>=a:
                target={'ONE':a};guards=cg.guards(target,node,b-a+1,side,None,prefix)
                m.need(all(ev(g)<=0 for g in guards) and not any(a<=x<=b for x in actual),'Canonical probe lies wholly in an actual empty interval');nonempty+=1
            checked+=1
bad=0
for node,prefix in [((0,-1),1),((0,0),13),((0,0),True)]:
    try:cg.guards({},node,1,'s',None,prefix)
    except ValueError:bad+=1
    else:raise ValueError('Unlicensed canonical probe prefix')
print(json.dumps(dict(status='PASS_NEW_CANONICAL_PROBE_INTERFACE',guard_domains=checked,actual_empty_windows=nonempty,invalid_prefixes_rejected=bad,global_upper_bound_certified=False)))
