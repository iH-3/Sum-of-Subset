"""Equal core translates are deduplicated without upgrading their capacity."""
from pathlib import Path
from collections import defaultdict
import sys,json,copy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import full_cover as fc,full_window as fw,model as m
values={'ONE':1}
for side in 'st':
 values.update({'R'+side:5,'M'+side:9,'S'+side:44,'X'+side:10,'g'+side:7,'h'+side:13,'d'+side:29})
 values.update({a+side:i for i,a in enumerate('abce',1)})
ev=lambda row:sum(c*values[k] for k,c in row.items())
groups=defaultdict(list)
for node in fc.leaves():
 if node[1]<0:continue
 q=4-len(fc.roots()[node[0]])-len(fc.children(node[0])[node[1]])
 if q:groups[(q,ev(fc.interval(*node)[0]))].append(node)
E={-5,-4,-3,-2,0,2,3,4,5};powers={0:{0}}
for q in range(1,5):powers[q]={a+b for a in powers[q-1] for b in E}
checks=0
for (q,low),nodes in groups.items():
 if len(nodes)<2:continue
 a,b=nodes[:2];centres=[ev(fc.interval(*n)[0])+q*values['Rt'] for n in (a,b)]
 m.need({x+centres[0] for x in powers[q]}=={x+centres[1] for x in powers[q]},'Explicit equal core translates');checks+=1
 if q==1:pair=(a,b)
a,b=pair
proof=dict(mask=0,lower={'ONE':0},upper={'ONE':1},exact_one_term=True,refined=[i for i,r in enumerate(fc.roots()) if len(r)<4],inside=[a],outside=[dict(node=n,direction=0) for n in fc.leaves() if n not in (a,b)],equal_core=[dict(by=a,nodes=[b])])
row,guards=fw.derive(proof,False,1,1)
m.need(row=={'ONE':-63} or {k:v for k,v in row.items() if v}=={'ONE':-63},'Identical E remains charged 65, not its hull')
bad=0
for change in ['repeat','different_power','missing_representative']:
 p=copy.deepcopy(proof)
 if change=='repeat':p['equal_core'][0]['nodes'].append(b)
 elif change=='different_power':
  candidate=next(n for n in fc.leaves() if n[1]>=0 and 4-len(fc.roots()[n[0]])-len(fc.children(n[0])[n[1]])==2)
  p['equal_core'][0]['nodes']=[candidate];p['outside']=[v for v in p['outside'] if tuple(v['node'])!=candidate];p['outside'].append(dict(node=b,direction=0))
 else:p['equal_core'][0]['by']=b
 try:fw.derive(p,False,1,1)
 except ValueError:bad+=1
 else:raise ValueError('Invalid equal-core recipe accepted')
print(json.dumps(dict(status='PASS_NEW_EQUAL_CORE_WINDOWS',explicit_equal_translates=checks,negative_controls=bad,global_upper_bound_certified=False)))
