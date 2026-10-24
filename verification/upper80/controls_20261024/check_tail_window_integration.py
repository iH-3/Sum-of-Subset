"""Check the new multi-point charge and its exclusive use in a full window."""
from pathlib import Path
import sys,json,copy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import model as m,full_window as fw,full_cover as fc
inventory=fc.initial_nodes();fc.refine(inventory,0);node=(0,0)
base=dict(mask=0,lower={},upper={'ONE':10},refined=[0],outside=[dict(node=n,direction=0) for n in sorted(inventory-{node})],inside=[node],core_edges=[],exact_one_term=True,extreme_only=[dict(node=node,side='s')])
a,ga=fw.derive(base,False,1,1)
proof=copy.deepcopy(base);proof['extreme_only'][0].update(keep=2,order=0)
b,gb=fw.derive(proof,False,1,1)
m.need(m.add((1,b),(-1,a))=={'ONE':-4},'4E from two tail elements has five possible multisets')
m.need(len(ga)==len(gb),'One complete tail threshold guard replaces the old threshold')
bad=0
for kind in ['clipped','mass_core','absorbed']:
 p=copy.deepcopy(proof)
 if kind=='clipped':p[kind]=[dict(node=node,left=0,right=0)]
 elif kind=='mass_core':p[kind]=[node]
 else:p[kind]=[dict(by=node,nodes=[])]
 try:fw.derive(p,False,1,1)
 except ValueError:bad+=1
 else:raise ValueError('Multi-point cap also given incompatible mass/hull credit')
print(json.dumps(dict(status='PASS_NEW_TAIL_WINDOW_INTEGRATION',complete_inventory=len(inventory),cardinality=5,old_cardinality=1,invalid_charge_combinations=bad,global_upper_bound_certified=False)))
