#!/usr/bin/env python3
"""Optional discovery tool (NumPy/SciPy); never used by the exact verifier."""
import json
import time
from pathlib import Path
from fractions import Fraction
from math import lcm
import numpy as np
from scipy.optimize import linprog
from model import build
from certificates import states,system,evaluate,normalize,need

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/upper82_c5t_certificates.json'

def discover(names,data):
    le=[(key,row,b) for key,(row,b,kind) in data.items() if kind=='le']
    eq=[(key,row,b) for key,(row,b,kind) in data.items() if kind=='eq']
    A=np.array([[row.get(k,0) for k in names] for _,row,_ in le],dtype=float)
    b=np.array([b for _,_,b in le],dtype=float)
    E=np.array([[row.get(k,0) for k in names] for _,row,_ in eq],dtype=float)
    f=np.array([b for _,_,b in eq],dtype=float)
    # Phase I: relax every inequality by one nonnegative common slack.
    # Equality rows remain exact. Its dual supplies a contradiction.
    result=linprog(np.r_[np.zeros(len(names)),1.0],
        A_ub=np.c_[A,-np.ones(len(le))],b_ub=b,
        A_eq=np.c_[E,np.zeros(len(eq))],b_eq=f,
        bounds=[(0,None)]*(len(names)+1),method='highs')
    need(result.success and result.fun>1e-7,'no numerical contradiction')
    weights=[(key,-float(w)) for (key,_,_),w in zip(le,result.ineqlin.marginals)]
    weights += [(key,-float(w)) for (key,_,_),w in zip(eq,result.eqlin.marginals)]
    for limit in (1000,10000,1000000,100000000):
        rational=[(key,Fraction(w).limit_denominator(limit)) for key,w in weights if abs(w)>1e-9]
        den=lcm(*(w.denominator for _,w in rational))
        cert=normalize([(key,int(w*den)) for key,w in rational])
        if evaluate(cert,data,strict=False) is not None:return cert
    raise ValueError('numerical ray did not reconstruct exactly')

def main():
    start=time.monotonic();pool=[];records=[];count=0
    for state in states():
        names,data=system(state,build);index=None
        for i in range(len(pool)-1,-1,-1):
            if evaluate(pool[i],data,strict=False) is not None:index=i;break
        if index is None:
            cert=discover(names,data);index=len(pool);pool.append(cert)
        margin=evaluate(pool[index],data)
        records.append(dict(state=state,certificate=index,margin=margin));count+=1
        if count%250==0:print(count,'states',len(pool),'rays',round(time.monotonic()-start,1),'s',flush=True)
    OUT.write_text(json.dumps(dict(schema='upper82-c5t-integer-rays-v1',
        scope='Conditional exclusion of size83 C5t family; NOT a global upper82 proof',
        certificates=pool,records=records),ensure_ascii=False,separators=(',',':'))+'\n')
    print('SAVED',len(records),'states',len(pool),'integer rays',OUT,flush=True)

if __name__=='__main__':main()
