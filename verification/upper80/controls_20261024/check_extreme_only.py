"""One-point end-cap charges, including coarse qD and invalid full-set rebates."""
from pathlib import Path
import sys,json,copy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import full_cover as fc,full_window as fw,core_gap as cg,model as m
E={0,*range(1,32),40,*range(-32,0)};D=E|{41,50,60,100,-33,-35,-37,-150}
values={'ONE':1,'Rs':40,'Rt':32,'xs':8,'xt':0,'ts':8,'tt':0,'Ms':100,'Mt':150,'es':60,'cs':20,'et':118,'ct':5}
checks=0
for typ,Q,node in [('E',E,(0,0)),('D',D,(0,-1))]:
    power={0}
    for q in range(4):power={a+b for a in power for b in Q}
    for side in 'st':
        lo,hi=cg.gap_interval(node,side);ev=lambda row:sum(v*values[k] for k,v in row.items())
        left,right=(ev(lo),max(power)+50) if side=='s' else (min(power)-50,ev(hi))
        m.need(all(v in (min(power),max(power)) for v in power if left<=v<=right),'Only an extreme remains in the actual window')
        m.need(len({v for v in power if left<=v<=right})==1,'Sharp one-point capacity');checks+=1
        guard=cg.extreme_only_guard({'ONE':left},{'ONE':right},node,side)
        m.need(ev(guard)<=0,'Actual end-cap guard')
        inventory=fc.initial_nodes();refined=[]
        if node[1]>=0:fc.refine(inventory,0);refined=[0]
        proof=dict(mask=0,lower={'ONE':left},upper={'ONE':right},refined=refined,inside=[node],outside=[dict(node=n,direction=0) for n in sorted(inventory) if n!=node],extreme_only=[dict(node=node,side=side)])
        row,guards=fw.derive(proof,False,1,1);m.need(row=={'ONE':right-left} and guards[-1]==guard,'Exactly one unit charged')
bad=0
for change in ('clipped','mass','absorber'):
    node=(0,0);inventory=fc.initial_nodes();fc.refine(inventory,0)
    p=dict(mask=0,lower={},upper={'ONE':1},refined=[0],inside=[node],outside=[dict(node=n,direction=0) for n in sorted(inventory) if n!=node],extreme_only=[dict(node=node,side='s')])
    if change=='clipped':p['clipped']=[dict(node=node,left=0,right=0)]
    if change=='mass':p['mass_core']=[node]
    if change=='absorber':p['absorbed']=[dict(by=node,nodes=[(0,1)])]
    try:fw.derive(p,False,1,1)
    except ValueError:bad+=1
    else:raise ValueError('Double use of an end-cap accepted')
print(json.dumps(dict(status='PASS_NEW_EXTREME_ONLY_CAPACITIES',sharp_actual_windows=checks,negative_controls=bad,global_upper_bound_certified=False)))
