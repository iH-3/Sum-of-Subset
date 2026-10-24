"""The proved-guard interface must match the existing restricted-domain lemma."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import exact,ownerless_hit as oh,model as m
st=([*m.patterns(4),*m.partial_patterns(4)])[142]
for positive in (False,True):
    for side in 'st':
        row,guard=oh.derive(st,4,positive,46,side)
        m.need(row in exact.ownerless_rows(st,4,positive,46,{}, {'uH'+side:[0,68]}) and guard=={'uH'+side:1,'ONE':-68},'Same existing lemma and exact cutoff')
bad=0
for j,credit,side in [(5,46,'s'),(4,8,'s'),(4,46,'')]:
    try:oh.derive(st,j,True,credit,side)
    except ValueError:bad+=1
    else:raise ValueError('Unlicensed ownerless hit accepted')
print(json.dumps(dict(status='PASS_NEW_PROVED_OWNERLESS_HIT_INTERFACE',existing_lemma_row_matches=4,invalid_scopes_rejected=bad,global_upper_bound_certified=False)))
