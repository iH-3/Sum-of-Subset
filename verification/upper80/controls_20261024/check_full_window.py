"""New full-window counting lemma: direct sets and invalid inventories."""
from pathlib import Path
import sys,copy,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import model as m,full_cover as fc,full_window as fw
checks=0
for hole_case in (False,True):
    x={'ONE':1};D=[0];O=[]
    for side,sign in [('s',1),('t',-1)]:
        core=list(range(2,6)) if hole_case else list(range(1,5));R=max(core);offsets=[2,3,4,5];tails=[R+v for v in offsets]
        source=core+tails;x.update({'R'+side:R,'M'+side:max(source),'S'+side:sum(source),'X'+side:13,'g'+side:17,'h'+side:19,'d'+side:23})
        x.update({a+side:b for a,b in zip('abce',offsets)});D.extend(sign*v for v in source)
    ev=lambda row:sum(c*x[k] for k,c in row.items())
    O=[ev(row) for row in fc.outer()];A=D+O;two={a+b for a in A for b in A};four={a+b for a in two for b in two}
    fs={0}
    for v in D:fs|={a+v for a in fs}
    holes=set(range(-x['St'],x['Ss']+1))-fs;x['hole_W']=(len(holes)+1)//2
    for localized in ([False,True] if hole_case else [False]):
        margin=2 if localized else 0;cw=1 if localized or not hole_case else 2;bw=3 if localized else cw
        for mask,start,size in [(0,5,8),(1,7,15),(15,2,31),(29,4,20)]:
            lower=m.add((1,fc.shift(mask)),(-1,{'St':1}),(start,{'ONE':1}));upper=m.add((1,lower),(size-1,{'ONE':1}))
            proof=dict(mask=mask,lower=lower,upper=upper,refined=[i for i,a in enumerate(fc.roots()) if len(a)<4],outside=[],inside=[])
            for node in fc.leaves():
                direction=next((d for d in (0,1) if ev(fw.exclusion(lower,upper,node,d))<=0),None)
                if direction is None:proof['inside'].append(node)
                else:proof['outside'].append(dict(node=node,direction=direction))
            row,guards=fw.derive(proof,hole_case,cw,bw);m.need(all(ev(g)<=0 for g in guards),'Actual-set window guards')
            lo,hi=ev(lower),ev(upper);required=hi-lo+1-(0 if localized else 2*x['hole_W'])
            cap=required-ev(row)
            m.need(cap>=len(four & set(range(lo,hi+1))),'Full-cover window capacity is an upper bound')
            translated={v+ev(fc.shift(mask)) for v in fs}
            m.need(required<=len(translated & set(range(lo,hi+1))),'Required subset-sum window count');checks+=1
bad=[]
for label,mutate in [('missing component',lambda q:q['outside'].pop()),('duplicate component',lambda q:q['outside'].append(q['outside'][0])),('duplicate refinement',lambda q:q['refined'].append(q['refined'][0])),('noninteger endpoint',lambda q:q['lower'].update(ONE=0.5)),('invalid direction',lambda q:q['outside'][0].update(direction=2))]:
    q=copy.deepcopy(proof);mutate(q)
    try:fw.derive(q,hole_case,cw,bw)
    except ValueError:bad.append(label)
    else:raise ValueError('Invalid window proof accepted: '+label)
print(json.dumps(dict(status='PASS_NEW_FULL_WINDOW_CAPACITY',direct_set_checks=checks,negative_controls=bad,global_upper_bound_certified=False)))
