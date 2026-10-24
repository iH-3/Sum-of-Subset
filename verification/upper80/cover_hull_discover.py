"""Discovery-only separation over a complete finite target-cover disjunction.

Every returned row carries an independent rational consequence certificate
for every surviving component. No floating convex-hull status is trusted.
"""
import copy,math
import numpy as np
from scipy.optimize import linprog
from scipy.linalg import qr
from scipy.sparse import csr_matrix,block_diag,hstack,vstack,coo_matrix
from types import SimpleNamespace
import model as m,exact,full_cover as fc
LAST_DIAGNOSTIC={}

def homogeneous(entries,names):
    seen=set();rr=[];cc=[];vv=[];columns={name:i for i,name in enumerate(names)};count=0
    for row,rhs,_ in entries:
        q=m.add((1,row),(-rhs,{'ONE':1}));q={k:v for k,v in q.items() if v}
        if not q:continue
        factor=math.gcd(*(abs(v) for v in q.values()));key=tuple(sorted((k,v//factor) for k,v in q.items()))
        if key in seen:continue
        seen.add(key);scale=max(abs(v) for v in q.values())
        for k,v in q.items():rr.append(count);cc.append(columns[k]);vv.append(v/scale)
        count+=1
    return coo_matrix((vv,(rr,cc)),shape=(count,len(names))).tocsr()

def separate(s,pid,point):
    global LAST_DIAGNOSTIC
    state=s.full_probes[pid];nodes=sorted(state['nodes']);n=len(s.names)
    if len(nodes)<2:return None
    physical=['ONE',*(k for k in s.names if k!='ONE')]
    projected=[name for name in physical if name in s.names];positions=[s.names.index(name) for name in projected];d=len(projected)-1
    # The active rows and nonnegative coordinate bounds define a cone at
    # the current LP vertex. Relaxing to this cone preserves validity and
    # avoids copying thousands of redundant consequence rows per case.
    x=np.array([point[k] for k in s.names]);vectors=[];labels=[]
    for row,rhs,_ in s.eqs:
        scale=max([1,*[abs(v) for v in row.values()]]);vectors.append([row.get(k,0)/scale for k in s.names]);labels.append(None)
    for i,value in enumerate(x):
        if abs(value)<1e-7:
            v=np.zeros(n);v[i]=1;vectors.append(v);labels.append(None)
    for i,(row,rhs,_) in enumerate(s.rows):
        scale=max([1,*[abs(v) for v in row.values()]]);v=np.array([row.get(k,0)/scale for k in s.names])
        if abs(rhs/scale-v@x)<1e-7:vectors.append(v);labels.append(i)
    _,R,pivots=qr(np.array(vectors).T,pivoting=True,mode='economic')
    rank=int(np.sum(abs(np.diag(R))>1e-9));selected=sorted({labels[i] for i in pivots[:rank] if labels[i] is not None})
    base=homogeneous([s.rows[i] for i in selected],s.names);eq=homogeneous(s.eqs,s.names)
    blocks=[]
    for node in nodes:
        extra=[(g,0,'case target containment') for g in fc.containment(state['target'],node,state['width'])]
        blocks.append(vstack([base,homogeneous(extra,s.names)],format='csr'))
    A=block_diag(blocks,format='csr');E=block_diag([eq]*len(nodes),format='csr');nall=n*len(nodes)
    pr=[];pc=[];pv=[]
    for row,pos in enumerate(positions):
        for i in range(len(nodes)):pr.append(row);pc.append(i*n+pos);pv.append(1)
        if row:
            pr.extend([row,row]);pc.extend([nall+row-1,nall+d+row-1]);pv.extend([1,-1])
    projection=coo_matrix((pv,(pr,pc)),shape=(len(projected),nall+2*d)).tocsr()
    Ae=hstack([A,csr_matrix((A.shape[0],2*d))],format='csr')
    Ee=vstack([hstack([E,csr_matrix((E.shape[0],2*d))],format='csr'),projection],format='csr')
    weights=np.array([1/max(1,abs(point[k])) for k in projected[1:]])
    rr=linprog(np.r_[np.zeros(nall),weights,weights],A_ub=Ae,b_ub=np.zeros(Ae.shape[0]),
               A_eq=Ee,b_eq=np.r_[np.zeros(E.shape[0]),[point[k] for k in projected]],bounds=(0,None),method='highs',options={'time_limit':60})
    LAST_DIAGNOSTIC=dict(status=rr.status,objective=rr.fun,variables=nall+2*d,rows=Ae.shape[0]+Ee.shape[0],active_rank=rank,active_rows=len(selected))
    if not rr.success or rr.fun<1e-7:return None
    dual=rr.eqlin.marginals[-len(projected):]
    for precision in (100000,10000000,1000000000):
        target={k:int(round(v*precision)) for k,v in zip(projected,dual) if abs(v*precision)>=0.5}
        factor=math.gcd(*(abs(v) for v in target.values())) or 1;target={k:v//factor for k,v in target.items()}
        step=common_bound(s,pid,target,point)
        LAST_DIAGNOSTIC['precision']=precision
        if step is not None:return step
    return None

def common_bound(s,pid,target,point=None):
    state=s.full_probes[pid];nodes=sorted(state['nodes'])
    cases=[];maximum=-math.inf
    for node in nodes:
        obj=copy.copy(s);obj.rows=list(s.rows)+[(g,0,'case target containment') for g in fc.containment(state['target'],node,state['width'])];obj.trace=[]
        obj.matrices();result=linprog([-target.get(k,0) for k in s.names],A_ub=obj.A,b_ub=obj.b,A_eq=obj.E,b_eq=obj.f,bounds=(0,None),method='highs')
        if result.status==2:
            obj.final();cases.append(dict(node=node,infeasible=True,certificate=obj.trace[-1]['certificate']));continue
        if result.status!=0:LAST_DIAGNOSTIC.update(failed_case=node,case_status=result.status);return None
        maximum=max(maximum,-result.fun);cases.append((node,obj,result))
    if maximum==-math.inf:
        return dict(kind='full_cover_bound',probe=pid,guard={'ONE':1},cases=cases)
    upper=math.floor(maximum+1e-7);guard=m.add((1,target),(-upper,{'ONE':1}))
    violation=sum(c*point[k] for k,c in guard.items()) if point is not None else None;LAST_DIAGNOSTIC.update(maximum=maximum,upper=upper,violation=violation)
    if point is not None and violation<=1e-5:return None
    result_cases=[]
    for item in cases:
        if isinstance(item,dict):result_cases.append(item);continue
        node,obj,result=item;unit=next(i for i,(r,b,_) in enumerate(obj.eqs) if r=={'ONE':1} and b==1)
        marginal=np.array(result.eqlin.marginals,copy=True);marginal[unit]+=(upper+1)*obj.esi[unit]
        shifted=SimpleNamespace(ineqlin=result.ineqlin,eqlin=SimpleNamespace(marginals=marginal),lower=result.lower)
        cert=obj.reconstruct(shifted,m.add((1,guard),(-1,{'ONE':1})),strict=True)
        if cert is None:LAST_DIAGNOSTIC.update(reconstruction_failed=node);return None
        result_cases.append(dict(node=node,infeasible=False,rounded=True,certificate=cert))
    return dict(kind='full_cover_bound',probe=pid,guard=guard,cases=result_cases)
