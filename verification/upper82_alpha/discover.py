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
OUT=ROOT/'data/upper82_alpha_certificates.json'

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
    masks={0,4095,8191,4096}
    masks|={1<<i for i in range(13)}
    masks|={(1<<i)|(1<<j) for i in range(13) for j in range(i)}
    for state in states():
        names,data=system(state,build,sorted(masks));index=None
        for i in range(len(pool)-1,-1,-1):
            if evaluate(pool[i],data,strict=False) is not None:index=i;break
        if index is None:
            try:cert=discover(names,data)
            except ValueError:
                names,data=system(state,build)
                try:cert=discover(names,data)
                except ValueError:
                    print('OPEN STATE',state,flush=True);raise
                for key,_ in cert:
                    if key.startswith('le:forest '):masks.add(int(key.split(':')[1].split()[1]))
            index=len(pool);pool.append(cert)
        margin=evaluate(pool[index],data)
        records.append(dict(state=state,certificate=index,margin=margin));count+=1
        if count%100==0:print(count,'states',len(pool),'rays',len(masks),'masks',round(time.monotonic()-start,1),'s',flush=True)
    used=sorted({int(key.split(':')[1].split()[1]) for ray in pool for key,_ in ray if key.startswith('le:forest ')})
    OUT.write_text(json.dumps(dict(schema='upper82-alpha-integer-rays-v1',
        scope='Conditional exclusion of size83 alpha-hole family; NOT a global upper82 proof',
        forest_masks=used,certificates=pool,records=records),ensure_ascii=False,separators=(',',':'))+'\n')
    print('SAVED',len(records),'states',len(pool),'integer rays',len(used),'forests',OUT,flush=True)

if __name__=='__main__':main()
