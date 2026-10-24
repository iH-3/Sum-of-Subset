"""Focused controls for omitting a redundant nonempty-hull guard."""
from pathlib import Path
import sys,json,copy
from itertools import combinations_with_replacement
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import model as m,averaged_source as av
sets=groups=members=0
for t in range(12):
    k=t%6;v={'ONE':1,'rank_k':k};cores={};tails=[]
    for side,r,sign in [('s',32-k,1),('t',32+k,-1)]:
        d=[max(0,t-r+i) for i in range(1,r+1)];d[-1]+=2*t+5
        X=[i+x for i,x in enumerate(d,1)];cores[side]=X
        v.update({'R'+side:X[-1],'x'+side:d[-1],'t'+side:sum(d),'phicore'+side:min([r,*[x+r-2*i for i,x in enumerate(X,1)]])})
        offsets=[1,4+t,10+2*t,45+3*t];v.update({off+side:x for off,x in zip('abce',offsets)});tails.extend(sign*(X[-1]+x) for x in offsets)
    D={0,*cores['s'],*(-x for x in cores['t']),*tails};DD={x+y for x in D for y in D};v['K']=len(DD);ev=lambda row:sum(c*v[key] for key,c in row.items())
    for keep in (2,4):
        proof,intervals,masses,clusters=av.recipe(v,keep);proof['nonempty_hulls']=True
        # Retain every other component in a licensed hull, and charge all
        # omitted members separately. This exercises partial membership.
        for cluster in clusters:
            selected=cluster[::2];other=cluster[1::2]
            lo=min((intervals[i][0] for i in selected),key=ev);hi=max((intervals[i][1] for i in selected),key=ev)
            proof['groups'].append(dict(components=selected,lower=lo,upper=hi));proof['groups'].extend(dict(components=[i],mass=True) for i in other);groups+=1;members+=len(selected)
        row,guards=av.derive(proof);m.need(all(ev(g)<=0 for g in guards) and ev(row[0])<=0,'Partial hull membership covers actual double source')
        old=copy.deepcopy(proof);old['nonempty_hulls']=False;oldrow,oldguards=av.derive(old)
        m.need(oldrow==row and len(oldguards)==len(guards)+len(clusters),'Only the redundant guard was removed');sets+=1
bad=0
for flag in (1,'yes',[]):
    p=copy.deepcopy(proof);p['nonempty_hulls']=flag
    try:av.derive(p)
    except ValueError:bad+=1
    else:raise ValueError('Invalid nonempty-hull flag')
print(json.dumps(dict(status='PASS_NEW_NONEMPTY_SOURCE_HULLS',actual_capacities=sets,partial_groups=groups,licensed_components=members,invalid_flags_rejected=bad,global_upper_bound_certified=False)))
