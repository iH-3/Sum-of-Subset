"""Full-window extreme-gap inventory and a concrete newly exposed window."""
from pathlib import Path
import sys,json,copy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import full_cover as fc,full_window as fw,core_gap as cg,model as m
node=(0,0);lower,upper=cg.gap_interval(node,'s')
proof=dict(mask=0,lower=lower,upper=upper,refined=[0],inside=[],outside=[dict(node=n,direction=0) for n in sorted((fc.initial_nodes()-{(0,-1)})|{(0,i) for i in range(len(fc.children(0)))} ) if n!=node],gap_outside=[dict(node=node,side='s')])
row,guards=fw.derive(proof,False,1,1)
m.need(len(guards)==2+len(proof['outside'])+2,'Every gap component has two correctly ordered guards')
m.need(all(not any(g.values()) for g in guards[-2:]),'Identical proposed and excluded gap bounds')
bad=0
for change in ('duplicate','missing','singleton'):
    p=copy.deepcopy(proof)
    if change=='duplicate':p['gap_outside']*=2
    if change=='missing':p['gap_outside']=[]
    if change=='singleton':
        q=next((0,i) for i,c in enumerate(fc.children(0)) if len(c)==4)
        p['gap_outside']=[dict(node=q,side='s')];p['outside']=[v for v in p['outside'] if tuple(v['node'])!=q]+[dict(node=node,direction=0)]
    try:fw.derive(p,False,1,1)
    except ValueError:bad+=1
    else:raise ValueError('Invalid gap-window inventory accepted')
print(json.dumps(dict(status='PASS_NEW_GAP_WINDOW_INVENTORY',guard_order_checked=True,negative_controls=bad,global_upper_bound_certified=False)))
