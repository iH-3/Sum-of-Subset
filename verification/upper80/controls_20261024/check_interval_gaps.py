"""Brute interval unions independently check the conditional gap formulas."""
from pathlib import Path
import json,random,sys
root=Path(__file__).resolve().parents[3];sys.path.insert(0,str(root/'verification/upper80'))
import interval_gaps as g
rng=random.Random(802410);checks=0
for _ in range(5000):
    x={'ONE':1,'Rs':rng.randrange(1,31),'Rt':rng.randrange(1,31)};data={};states={};selected={};missed=[];fixed_new=0
    ev=lambda row:sum(c*x[k] for k,c in row.items())
    for side,other in [('s','t'),('t','s')]:
        S=x['S'+side]=rng.randrange(10,301)
        centres=sorted(rng.randrange(1-x['R'+side],S+x['R'+other]+1) for _ in range(rng.randrange(1,13)))
        values=[rng.randrange(-50,S+51) for _ in range(30)]
        data[side]=([(str(i),{'ONE':v}) for i,v in enumerate(centres)],[(str(i),{'ONE':v}) for i,v in enumerate(values)],20)
    # This lemma is valid for any ordered equal-width interval family.
    g.catalogue=lambda st,Z,side:data[side]
    for side,other in [('s','t'),('t','s')]:
        centres,points,native=data[side];S=x['S'+side];order=list(range(len(centres)))
        if any(ev(row)>0 for row in g.licenses({}, {},side,order)):raise ValueError('Synthetic interval license')
        core=set().union(*(set(range(max(1,ev(c)-x['R'+other]),min(S,ev(c)+x['R'+side])+1)) for _,c in centres))
        forms=g.gaps({}, {},side,order);selected[side]=[i for i,row in enumerate(forms) if ev(row)>0]
        if sum(ev(forms[i]) for i in selected[side])!=S-len(core):raise ValueError('Wrong exact core gap count')
        source={ev(v) for _,v in points[:native] if 1<=ev(v)<=S};fixed={ev(v) for _,v in points[native:] if 1<=ev(v)<=S}
        fixed_new+=len(fixed-(core|source));missed.append(S-len(core|source|fixed));excluded=set()
        for i,(_,v) in enumerate(points):
            choices=['low','high',*range(len(centres))]
            if any(all(ev(row)<=0 for row in g.exclusion({}, {},side,i,where)) for where in choices):excluded.add(i)
        states[side]=dict(order=order,excluded=excluded)
    x['hole_W']=max(missed)
    for subset,joint in [({'s':selected['s']},False),({'t':selected['t']},False),(selected,True)]:
        row,rhs,_=g.capacity({}, {},states,subset,84-fixed_new,joint)
        if ev(row)>rhs:raise ValueError('Gap capacity understated')
        checks+=1
print(json.dumps(dict(status='PASS_ORDERED_INTERVAL_GAPS',independent_interval_families=10000,capacity_checks=checks)))
