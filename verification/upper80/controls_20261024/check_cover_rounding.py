"""Focused controls for integer rounding in a complete cover consequence."""
from pathlib import Path
import sys,copy,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import model as m,parametric as p,exact,full_cover as fc
st=([*m.patterns(6),*m.partial_patterns(6)])[436]
base=dict(st=st,j=6,positive=False,point_overlap=True,limits={},trace=[dict(kind='full_cover_known_probe',mask=0,source_mask=0)])
p.POINT_OVERLAP=True
_,_,eqs=p.build(st,6,False,8,{})
unit=next(i for i,(row,rhs,_) in enumerate(eqs) if row=={'ONE':1} and rhs==1)
# 0 is integer and 0-1<0, so the rounded consequence 0<=0 is valid.
cert=dict(weights=[('e',unit,-1)],denominator=1)
cases=[dict(node=list(node),infeasible=False,rounded=True,certificate=cert) for node in sorted(fc.initial_nodes())]
step=dict(kind='full_cover_bound',probe=0,guard={},cases=cases)
rec=copy.deepcopy(base);rec['trace'].append(step);exact.replay(rec,require_closed=False)
rejected=[]
for label,mutate in [
    ('false rounded bound',lambda q:q.update(guard={'ONE':1})),
    ('noninteger rounding flag',lambda q:q['cases'][0].update(rounded=1)),
    ('rounding infeasible alternative',lambda q:q['cases'][0].update(infeasible=True)),
    ('unlicensed variable',lambda q:q.update(guard={'not_an_integer_variable':1})),
    ('missing strict margin',lambda q:[c.update(certificate=dict(weights=[],denominator=1)) for c in q['cases']])]:
    q=copy.deepcopy(step);mutate(q);r=copy.deepcopy(base);r['trace'].append(q)
    try:exact.replay(r,require_closed=False)
    except ValueError:rejected.append(label)
    else:raise ValueError('Accepted invalid integer cover consequence: '+label)
print(json.dumps(dict(status='PASS_NEW_COVER_ROUNDING',positive_controls=1,negative_controls=rejected,global_upper_bound_certified=False)))
