"""Discovery-only persistent HiGHS basis; saved proofs remain exact integer rows."""
import numpy as np
from types import SimpleNamespace as NS
from math import gcd
import scipy.optimize._highspy._core as c

def install():
 from discover import Search,guard_key
 original=Search.lp
 def lp(self,target=None):
  n=len(self.names);cost=np.array([-target.get(k,0) for k in self.names],float) if target else np.zeros(n)
  def identity(entry):
   row,b,_=entry;factor=gcd(b,*(v for v in row.values())) or 1
   return tuple(sorted((k,v//factor) for k,v in row.items() if v)),b//factor
  def sparse(rr):
   index=[];value=[];start=[0];bounds=[];scales=[];columns={k:i for i,k in enumerate(self.names)}
   for row,b,label in rr:
    scale=max([1,*[abs(v) for v in row.values()]]);scales.append(scale);bounds.append(b/scale)
    for k,v in row.items():
     if v:index.append(columns[k]);value.append(v/scale)
    start.append(len(index))
   return np.array(start,dtype=np.int32),np.array(index,dtype=np.int32),np.array(value,float),np.array(bounds,float),scales
  for iteration in range(100):
   if not hasattr(self,'_engine'):
    h=c._Highs();h.setOptionValue('output_flag',False);h.setOptionValue('threads',1);h.setOptionValue('solver','simplex')
    unique=[];self._engine_seen=set();self._rpositions=[]
    for row in self.rows:
     key=identity(row)
     if key in self._engine_seen:self._rpositions.append(-1)
     else:self._engine_seen.add(key);self._rpositions.append(len(unique));unique.append(row)
    rr=unique+self.eqs;start,index,value,bounds,scales=sparse(rr);nr=len(unique);ne=len(self.eqs)
    model=c.HighsLp();model.num_col_=n;model.num_row_=len(rr);model.col_cost_=cost;model.col_lower_=np.zeros(n);model.col_upper_=np.full(n,np.inf)
    model.row_lower_=np.r_[np.full(nr,-np.inf),bounds[nr:]];model.row_upper_=bounds
    model.a_matrix_.format_=c.MatrixFormat.kRowwise;model.a_matrix_.start_=start;model.a_matrix_.index_=index;model.a_matrix_.value_=value
    h.passModel(model);self._engine=h;self._engine_rows=len(self.rows);self._epositions=list(range(nr,nr+ne));self.rsi=[max([1,*[abs(v) for v in row.values()]]) for row,_,_ in self.rows];self.esi=scales[nr:]
   h=self._engine
   if len(self.rows)>self._engine_rows:
    rr=[];offset=h.getNumRow()
    for row in self.rows[self._engine_rows:]:
     self.rsi.append(max([1,*[abs(v) for v in row[0].values()]]));key=identity(row)
     if key in self._engine_seen:self._rpositions.append(-1)
     else:self._engine_seen.add(key);self._rpositions.append(offset+len(rr));rr.append(row)
    if rr:
     start,index,value,bounds,scales=sparse(rr)
     h.addRows(len(rr),np.full(len(rr),-np.inf),bounds,len(value),start,index,value)
    self._engine_rows=len(self.rows)
   h.changeColsCost(n,np.arange(n,dtype=np.int32),cost);self.calls+=1;h.run();status=h.getModelStatus()
   if status not in (c.HighsModelStatus.kOptimal,c.HighsModelStatus.kInfeasible):
    return original(self,target)
   sol=h.getSolution();x=np.array(sol.col_value,float);rowdual=np.array(sol.row_dual,float)
   result=NS(status=0 if status==c.HighsModelStatus.kOptimal else 2,success=status==c.HighsModelStatus.kOptimal,
             fun=float(cost@x),x=x,message=h.modelStatusToString(status),
             # A duplicate row gets zero dual weight. Assigning it the first
             # row's weight again would invalidate exact reconstruction.
             ineqlin=NS(marginals=np.array([rowdual[i] if i>=0 else 0.0 for i in self._rpositions])),eqlin=NS(marginals=rowdual[self._epositions]),lower=NS(marginals=np.array(sol.col_dual,float)))
   if result.status!=0:return result
   if not self.cut(dict(zip(self.names,x))):
    if target and result.fun>=-1e-8:self.known_nonpositive.add(guard_key(target))
    return result
  raise ValueError('Persistent forest separation did not settle')
 Search.lp=lp
