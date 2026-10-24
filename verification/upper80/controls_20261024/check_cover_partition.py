from pathlib import Path
import sys,copy,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import model as m,cover_partition as cp,full_cover as fc
probe=dict(target={},width=1,nodes=[(494,-1)]);probes=[probe]
tree=dict(closed=False,probe=0,children=[dict(node=(494,-1),child=dict(closed=False))])
m.need(cp.check(tree,probes,[],[])==dict(closed=False,closed_leaves=0,open_leaves=1),'Open leaf preserved')
bad=[]
for label,mutate in [('missing child',lambda t:t.update(children=[])),('duplicate child',lambda t:t['children'].append(t['children'][0])),('false closure',lambda t:t.update(closed=True)),('unsupported closed leaf',lambda t:t['children'][0]['child'].update(closed=True)),('wrong probe',lambda t:t.update(probe=1))]:
 q=copy.deepcopy(tree);mutate(q)
 try:cp.check(q,probes,[],[])
 except ValueError:bad.append(label)
 else:raise ValueError('Invalid partition accepted: '+label)
base=dict(limits={'rank_k':[1,1]});guards=fc.containment(probe['target'],(494,-1),1)
expected=cp.branch_limits(base['limits'],guards)
m.need(len(expected)==3,'Exact two-guard conditional domain')
q=dict(closed=False,record=dict(limits={'rank_k':[1,1]},premise=base))
try:cp.check(q,probes,[],[],base_record=base,assumptions=guards)
except ValueError:bad.append('missing covered assumptions')
else:raise ValueError('Accepted mismatched conditional record')
print(json.dumps(dict(status='PASS_NEW_COVER_PARTITION_CONTROLS',negative_controls=bad,global_upper_bound_certified=False)))
