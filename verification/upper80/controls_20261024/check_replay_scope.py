"""Nested replay restores caller state; cached certificates retain row order."""
from pathlib import Path
import sys,json,copy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import exact,model as m,parametric as p
st=([*m.patterns(5),*m.partial_patterns(5)])[413]
limits={'integer_cut:as:10':[0,0],'integer_cut:bs:20':[0,0]}
p.POINT_OVERLAP=True
_,rows,eqs=p.build(st,5,False,0,limits)
index=next(i for i,(_,_,label) in enumerate(rows) if label=='integer cut lower integer_cut:as:10')
unit=next(i for i,(_,_,label) in enumerate(eqs) if label=='unit constant')
source=dict(st=st,j=5,positive=False,limits=None,trace=[],point_overlap=True)
record=dict(st=st,j=5,positive=False,limits=limits,point_overlap=True,trace=[dict(kind='record_consequences',record=source,facts=[]),dict(kind='integer_guard',guard={'as':1,'ONE':-10},certificate=dict(weights=[('r',index,1),('e',unit,-11)],denominator=1))])
marker={'sentinel':[]};p.PLANE_TABLE=marker;p.build.last_Z={'caller':'geometry'}
exact.replay(record,False,True)
m.need(p.PLANE_TABLE is marker and p.build.last_Z=={'caller':'geometry'},'Nested and outer replay restore caller state')
wrong=copy.deepcopy(record);wrong['limits']=dict(reversed(list(wrong['limits'].items())))
try:exact.replay(wrong,False,True)
except ValueError:pass
else:raise ValueError('Reordered row inventory reused cached verification')
m.need(p.PLANE_TABLE is marker and p.build.last_Z=={'caller':'geometry'},'Failed replay restores caller state')
print(json.dumps(dict(status='PASS_REPLAY_SCOPE_AND_ORDER',nested_scope_restored=True,error_scope_restored=True,reordered_inventory_rejected=True,global_upper_bound_certified=False)))
