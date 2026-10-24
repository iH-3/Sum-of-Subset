"""Reject cross-branch assumptions when reusing previously proved facts."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import record_consequences as rc
pairs=[({'limits':{}},{'limits':{'rank_k':[2,2]}}),({'limits':{'rank_k':[1,4]}},{'limits':{'rank_k':[2,3],'hole_W':[1,1]}})]
for source,target in pairs:rc.domain_contains(source,target)
negatives=[({'limits':{'rank_k':[2,2]}},{'limits':{}}),({'limits':{'rank_k':[2,2]}},{'limits':{'rank_k':[1,3]}}),({'limits':{'hole_W':[1,1]}},{'limits':{'hole_W':[2,2]}}),({'limits':{'linear_cut:{"xs":1}':[0,0]}},{'limits':{'rank_k':[0,0]}})]
for source,target in negatives:
 try:rc.domain_contains(source,target)
 except ValueError:pass
 else:raise ValueError('A stronger source domain was accepted')
print(json.dumps(dict(status='PASS_NEW_IMPORTED_FACT_SCOPE',containing_domains=len(pairs),negative_controls=len(negatives),global_upper_bound_certified=False)))
