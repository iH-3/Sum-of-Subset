"""New joint target coverage with persistent, exactly covered partial trees."""
from pathlib import Path
import sys,json,gzip,time,copy
from types import SimpleNamespace as NS
import numpy as np
from scipy.sparse import csr_matrix
import scipy.optimize._highspy._core as c
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'verification/upper80'))
import fast_lp;fast_lp.install()
from discover import Search
import full_cover as fc,modular,record_pool as pool
source_argument=Path(sys.argv[1]);folder=source_argument.parent;name=source_argument.name.removesuffix('.json.gz');depth_limit=int(sys.argv[2]);node_limit=int(sys.argv[3]) if len(sys.argv)>3 else 3000;target=folder/(name+'_joint_resume.json.gz');start=time.monotonic();lastsave=[start];newnodes=0
if target.exists():
 packet=pool.read_gzip(target)
 if packet['tree']['closed'] or packet.get('finished_depth',0)>=depth_limit:print('REUSED_COMPLETE_DEPTH',flush=True);raise SystemExit()
 parent=packet['parent'];s=Search(parent['st'],parent['j'],parent['positive'],parent.get('limits'),use_planes=True,parent=parent);s.rows=packet['system_rows'];s.eqs=packet['system_eqs'];assert s.names==packet['names'];probes=packet['probes']
else:
 parent=pool.read_gzip(folder/(name+'.json.gz'))['record'];s=Search(parent['st'],parent['j'],parent['positive'],parent.get('limits'),use_planes=True,parent=parent);s.omit_generated_rows=True;s.lp();probes=[dict(p,nodes=sorted(p['nodes'])) for p in s.full_probes]
 packet=dict(parent=parent,record=s.record(),system_rows=s.rows,system_eqs=s.eqs,names=s.names,probes=probes,order=sorted(range(len(probes)),key=lambda i:len(probes[i]['nodes'])),tree=dict(closed=False,pending=True),global_upper_bound_certified=False)
order=packet['order'];depth_limit=min(depth_limit,len(order));s.matrices();n=len(s.names);nr=len(s.rows);ne=len(s.eqs);guards=[];scales=[]
h=c._Highs();h.setOptionValue('output_flag',False);h.setOptionValue('threads',1);h.setOptionValue('solver','simplex');model=c.HighsLp();model.num_col_=n+1;model.num_row_=nr+ne;model.col_cost_=np.r_[np.zeros(n),1];model.col_lower_=np.zeros(n+1);model.col_upper_=np.full(n+1,np.inf)
omitted=[i for i,(_,_,label) in enumerate(s.rows) if label in ('integer CG consequence','complete target-cover consequence')];AA=s.A.copy();bb=s.b.copy();AA[omitted]=0;bb[omitted]=0;model.row_lower_=np.r_[np.full(nr,-np.inf),s.f];model.row_upper_=np.r_[bb,s.f]
A=csr_matrix(np.vstack([np.c_[AA,-np.ones(nr)],np.c_[s.E,np.zeros(ne)]]));model.a_matrix_.format_=c.MatrixFormat.kRowwise;model.a_matrix_.start_=A.indptr;model.a_matrix_.index_=A.indices;model.a_matrix_.value_=A.data;h.passModel(model)
# Keep only base rows needed for known equalities, plus rows opposite to
# a current branch guard. This relaxes modular discovery; every resulting
# certificate is still checked against the full original system.
base_extras=modular.extra_equalities(s.rows,s.eqs)
essential=set(i for entry in base_extras for cert in entry['certificates'] for kind,i,w in cert['weights'] if kind=='r')
base_keys={}
for i,(row,b,label) in enumerate(s.rows):
 key,_=modular.key(__import__('model').add((1,row),(-b,{'ONE':1})))
 base_keys.setdefault(key,i)
def modular_obstruction():
 selected=set(essential)
 for guard in guards:
  key,_=modular.key(guard);opposite=tuple((k,-v) for k,v in key)
  if opposite in base_keys:selected.add(base_keys[opposite])
 indices=sorted(selected)+list(range(nr,nr+len(guards)))
 augmented=s.rows+[(g,0,'joint target containment') for g in guards]
 proof=modular.Basis([augmented[i] for i in indices],s.eqs).exclude({})
 if proof is None:return None
 for entry in proof.get('extras',[]):
  for cert in entry['certificates']:
   cert['weights']=[(kind,indices[i] if kind=='r' else i,w) for kind,i,w in cert['weights']]
 modular.check(proof,augmented,s.eqs,{})
 return proof
class Pause(Exception):pass
def normalize(node):
 if 'children' in node:
  values=[normalize(x['child']) for x in node['children']];node['closed']=all(values)
 return node['closed']
def counts(node):
 if 'children' not in node:return (1,int(node['closed']),int(not node['closed']),int(node.get('pending',False)))
 values=[counts(c['child']) for c in node['children']];return (1+sum(x[0] for x in values),sum(x[1] for x in values),sum(x[2] for x in values),sum(x[3] for x in values))
def save(status):
 normalize(packet['tree']);packet['status']=status;packet['counts']=counts(packet['tree']);pool.write_gzip(target,packet);lastsave[0]=time.monotonic();print('CHECKPOINT',status,packet['counts'],'new',newnodes,round(time.monotonic()-start,2),flush=True)
def certify():
 obj=copy.copy(s);obj.rows=s.rows+[(g,0,'joint target containment') for g in guards];obj.rsi=s.rsi+scales;obj.trace=[];solution=h.getSolution();dual=np.array(solution.row_dual,float);dual[omitted]=0
 fake=NS(ineqlin=NS(marginals=np.r_[dual[:nr],dual[nr+ne:]]),eqlin=NS(marginals=dual[nr:nr+ne]),lower=NS(marginals=np.array(solution.col_dual[:-1])));cert=obj.reconstruct(fake)
 if cert is not None:return cert
 obj.final();return obj.trace[-1]['certificate']
def walk(node,depth):
 global newnodes
 if node['closed']:return
 if time.monotonic()-lastsave[0]>15:save('progress')
 if node.get('pending',False):
  if newnodes>=node_limit:raise Pause()
  h.run();newnodes+=1;status=h.getModelStatus()
  if status==c.HighsModelStatus.kOptimal and h.getObjectiveValue()>1e-7:
   cert=certify();node.clear();node.update(closed=True,certificate=cert);return
  if status!=c.HighsModelStatus.kOptimal:raise ValueError(str(status))
  obstruction=modular_obstruction()
  if obstruction is not None:
   modular.check(obstruction,s.rows+[(g,0,'joint target containment') for g in guards],s.eqs,{});node.clear();node.update(closed=True,modular_certificate=obstruction);return
  node.update(pending=False)
 if depth>=depth_limit:return
 if 'children' not in node:
  pid=order[depth];node.update(probe=pid,children=[dict(node=q,child=dict(closed=False,pending=True)) for q in probes[pid]['nodes']])
 pid=node['probe'];state=probes[pid]
 for entry in node['children']:
  if entry['child']['closed']:continue
  extra=fc.containment(state['target'],tuple(entry['node']),state['width']);sizes=[max([1,*[abs(v) for v in g.values()]]) for g in extra]
  rr=csr_matrix(np.array([[*[g.get(k,0)/size for k in s.names],-1] for g,size in zip(extra,sizes)]));offset=h.getNumRow();h.addRows(2,np.full(2,-np.inf),np.zeros(2),len(rr.data),rr.indptr,rr.indices,rr.data);guards.extend(extra);scales.extend(sizes)
  try:walk(entry['child'],depth+1)
  finally:h.deleteRows(2,np.array([offset,offset+1],dtype=np.int32));del guards[-2:];del scales[-2:]
 node['closed']=all(c['child']['closed'] for c in node['children'])
print('START',order[:depth_limit],[len(probes[i]['nodes']) for i in order[:depth_limit]],flush=True)
try:
 walk(packet['tree'],0);packet['finished_depth']=depth_limit;save('closed' if packet['tree']['closed'] else 'depth_complete')
except Pause:save('budget_reached')
except BaseException:save('interrupted');raise
