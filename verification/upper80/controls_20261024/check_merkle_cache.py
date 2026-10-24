"""Cache identities preserve nested content and order, independent of sharing."""
from pathlib import Path
import sys,json,copy,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import record_pool as pool,exact,model as m,parametric as p
base=dict(st={'P':0,'Q':1},j=4,positive=False,trace=[],limits={'a':[0,0],'b':[1,1]})
record=dict(base,trace=[dict(kind='import',record=base)],premise=base)
different_sharing=json.loads(pool.canonical(record))
m.need(pool.record_digest(record)==pool.record_digest(different_sharing),'Sharing-independent content identity')
mutations=[]
q=copy.deepcopy(record);q['premise']['limits']['a']=[0,1];mutations.append(q)
q=copy.deepcopy(record);q['limits']=dict(reversed(list(q['limits'].items())));mutations.append(q)
q=copy.deepcopy(record);q['premise']['st']=dict(reversed(list(q['premise']['st'].items())));mutations.append(q)
q=copy.deepcopy(record);q['trace'][0]['kind']='other';mutations.append(q)
for q in mutations:m.need(pool.record_digest(q)!=pool.record_digest(record),'Every nested content/order mutation changes cache identity')
# A deep diamond would require more than a billion unpooled copies.
diamond=base
for _ in range(30):diamond=dict(st=base['st'],j=4,positive=False,trace=[dict(kind='import',record=diamond)],premise=diamond)
start=time.monotonic();packed=pool.pack(diamond);key=pool.record_digest(diamond)
m.need(len(packed['records'])==31 and key==packed['payload']['$record'],'Each shared ancestor is hashed once')
# Direct verifier cache separation after an actual row-order change.
st=([*m.patterns(5),*m.partial_patterns(5)])[413];limits={'integer_cut:as:10':[0,0],'integer_cut:bs:20':[0,0]};p.POINT_OVERLAP=True
_,rows,eqs=p.build(st,5,False,0,limits);index=next(i for i,(_,_,label) in enumerate(rows) if label=='integer cut lower integer_cut:as:10');unit=next(i for i,(_,_,label) in enumerate(eqs) if label=='unit constant')
r=dict(st=st,j=5,positive=False,limits=limits,point_overlap=True,trace=[dict(kind='integer_guard',guard={'as':1,'ONE':-10},certificate=dict(weights=[('r',index,1),('e',unit,-11)],denominator=1))])
exact.replay(r,False,True);wrong=copy.deepcopy(r);wrong['limits']=dict(reversed(list(limits.items())))
try:exact.replay(wrong,False,True)
except ValueError:pass
else:raise ValueError('Changed row inventory reused a cached state')
print(json.dumps(dict(status='PASS_NEW_MERKLE_REPLAY_CACHE',nested_mutations_rejected=len(mutations),sharing_independent=True,shared_records=31,unpooled_occurrences=2**31-1,reordered_actual_certificate_rejected=True,seconds=time.monotonic()-start,global_upper_bound_certified=False)))
