"""Exact arithmetic replay of the new conditional Z3 A1 deductions.

This checks row algebra and terminal margins. Applicability of the actual
resource group, rank rows, and forests is the accompanying written proof.
"""
from fractions import Fraction as F
import json
from pathlib import Path

def need(ok,msg):
    if not ok:raise RuntimeError(msg)

# Coefficient vectors in r,I,tau,xi_s,xi_t,e_s,e_t,f,H,delta,1.
N=11
def add(*rows):return tuple(sum(row[i] for row in rows) for i in range(N))
def mul(row,k):return tuple(k*x for x in row)
def unit(i):return tuple(F(int(i==j)) for j in range(N))
r,I,tau,xs,xt,es,et,f,H,delta,one=[unit(i) for i in range(N)]
A=add(I,tau,delta)
R=add(mul(one,68),xs,xt)
M=add(R,es,et)
Ms=add(r,xs,es)
Z=add(r,mul(I,2),mul(tau,2),xs,mul(f,6),mul(H,F(-1,2)))
base=add(M,Ms,mul(f,6),mul(H,F(-1,2)),mul(one,-47),mul(delta,-2))

def substitute(row,index,value):
    return add(row,mul(unit(index),-row[index]),mul(value,row[index]))

checks=[]
for p,h in [(0,0),(1,0),(0,1),(1,1)]:
    error=add(xs,xt,mul(add(et,mul(one,-4)),p),mul(add(es,mul(one,-4)),h))
    row=add(base,mul(error,-1))
    if (p,h)==(0,0):
        # et=L-es, then L>=A-57 and es>=A-146.
        row=substitute(row,6,add(A,mul(one,-57),mul(es,-1)))
        row=substitute(row,5,add(A,mul(one,-146)))
        expected=add(Z,mul(one,-182)); upper=182
    elif (p,h)==(1,0):
        row=substitute(row,5,add(A,mul(one,-146)))
        expected=add(Z,mul(one,-267)); upper=267
    elif (p,h)==(0,1):
        row=substitute(row,6,add(A,mul(one,-57),mul(es,-1)))
        expected=add(Z,mul(A,-1),mul(one,-32)); upper=253
    else:
        row=substitute(row,5,add(A,mul(one,-146)))
        expected=add(Z,mul(A,-1),mul(one,-117)); upper=338
    need(row==expected,f'exact terminal cancellation {(p,h)}')
    checks.append(dict(P_peeled=p,Ht_peeled=h,upper=upper,lower=394,margin=394-upper))

need(min(r+2*(r-34)**2 for r in range(-100,101))==34,'integer quadratic minimum')
need(398+34-F(76,2)==394,'shared lower bound')
f0=add(mul(one,69),mul(xs,-1),mul(xt,-1))
f2=add(mul(one,65),mul(tau,F(-1,2)),mul(xs,F(1,2)),mul(xt,F(1,2)))
convex=add(mul(f0,F(1,3)),mul(f2,F(2,3)))
need(convex==add(mul(one,F(199,3)),mul(tau,F(-1,3))),'actual adaptive-support convex combination')
need(add(mul(tau,2),mul(convex,6))==mul(one,398),'uniform shared lower row')
need(1239-2*539-78-2*12==59,'physical-side cancellation')
need(59-12==47,'forest and fixed-credit cancellation')
need(1+73+72-68==78,'endpoint rank constant')
need(7*77==539,'seven actual native resource capacities')
need(all(c['margin']>0 for c in checks),'strict margins in all endpoint positions')
result=dict(status='PASS',scope='exact local row arithmetic; resource applicability supplied by written proof',
            source_cap_used=221,active_Ht_native_loss_cap=76,endpoint_cases=checks)
print(json.dumps(result,indent=2))
Path(__file__).with_name('check_z3a1_side_union_results.json').write_text(json.dumps(result,indent=2)+'\n')
