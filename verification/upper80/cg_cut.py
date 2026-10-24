"""Exact Chvatal-Gomory rounding for physically integral nonnegative variables.

Discovery uses a simplex basis only to propose rational multipliers.
The verifier recomputes the integer floors without any simplex assumptions.
"""
from math import gcd,lcm,ceil
from fractions import Fraction
from collections import defaultdict
import model as m
from modular import INTEGER_NAMES

def derive(proof,rows,eqs):
    m.need(any({k:v for k,v in row.items() if v}=={'ONE':1} and b==1 for row,b,_ in eqs),'CG licensed unit constant')
    den=proof['denominator'];m.need(type(den) is int and den>0,'CG positive denominator')
    body=defaultdict(int);rhs=0;seen=set()
    for kind,i,weight in proof['weights']:
        source=rows if kind=='r' else eqs
        m.need(kind in ('r','e') and type(i) is int and 0<=i<len(source) and (kind,i) not in seen,'CG source inventory');seen.add((kind,i))
        m.need(type(weight) is int and weight!=0 and (kind=='e' or weight>0),'CG nonnegative inequality weight')
        row,b,_=source[i];m.need(set(k for k,c in row.items() if c)<=INTEGER_NAMES and all(type(c) is int for c in row.values()) and type(b) is int,'CG physical integer row')
        rhs+=weight*(b-row.get('ONE',0))
        for k,c in row.items():
            if k!='ONE':body[k]+=weight*c
    cut={k:c//den for k,c in body.items() if c//den};bound=rhs//den
    factor=gcd(*(abs(v) for v in cut.values())) or 1
    return ({k:v//factor for k,v in cut.items()},bound//factor,'integer CG consequence')

def basic_roundings(s):
    answer=[]
    for i,(row,b,_) in enumerate(s.rows):
        d=gcd(*(abs(v) for k,v in row.items() if k!='ONE')) or 1
        if d>1 and (b-row.get('ONE',0))%d:
            proof=dict(weights=[('r',i,1)],denominator=d);answer.append(proof)
    return answer

def solve_exact(matrix,rhs):
    n=len(matrix);a=[list(row)+[b] for row,b in zip(matrix,rhs)];previous=1
    for col in range(n):
        pivot=next((i for i in range(col,n) if a[i][col]),None)
        if pivot is None:raise ValueError('Singular exact basis')
        a[col],a[pivot]=a[pivot],a[col];lead=a[col][col]
        for i in range(col+1,n):
            v=a[i][col]
            for j in range(col+1,n+1):
                q,r=divmod(lead*a[i][j]-v*a[col][j],previous)
                if r:raise ValueError('Nonintegral basis elimination')
                a[i][j]=q
            a[i][col]=0
        previous=lead
    x=[Fraction(0)]*n
    for i in range(n-1,-1,-1):x[i]=(Fraction(a[i][-1])-sum(a[i][j]*x[j] for j in range(i+1,n)))/a[i][i]
    return x

def tableau(s,point,limit=3):
    import scipy.optimize._highspy._core as c
    if not hasattr(s,'_engine'):return []
    basis=s._engine.getBasis();basic=[i for i,status in enumerate(basis.col_status) if status==c.HighsBasisStatus.kBasic]
    source={pos:('r',i) for i,pos in enumerate(s._rpositions) if pos>=0};source.update({pos:('e',i) for i,pos in enumerate(s._epositions)})
    active=[source[i] for i,status in enumerate(basis.row_status) if status!=c.HighsBasisStatus.kBasic]
    if len(active)!=len(basic):return []
    rows=[(s.rows if kind=='r' else s.eqs)[i][0] for kind,i in active]
    matrix=[[row.get(s.names[j],0) for row in rows] for j in basic]
    fractional=sorted(((abs(point[s.names[j]]-round(point[s.names[j]])),k) for k,j in enumerate(basic)),reverse=True)
    answer=[]
    for distance,index in fractional[:limit]:
        if distance<1e-7:continue
        try:lam=solve_exact(matrix,[int(k==index) for k in range(len(basic))])
        except ValueError:continue
        weights=[]
        for (kind,i),value in zip(active,lam):
            weight=ceil(value)-value if kind=='r' else -value
            if weight:weights.append((kind,i,weight))
        den=lcm(*(v.denominator for _,_,v in weights));proof=dict(weights=[(kind,i,int(v*den)) for kind,i,v in weights],denominator=den)
        row,b,_=derive(proof,s.rows,s.eqs)
        if sum(v*point[k] for k,v in row.items())>b+1e-7:answer.append(proof)
    return answer

def discover(s,point):
    used=getattr(s,'_cg_used',set());s._cg_used=used;changed=False
    for proof in [*basic_roundings(s),*tableau(s,point)]:
        row=derive(proof,s.rows,s.eqs);key=(tuple(sorted(row[0].items())),row[1])
        if key in used:continue
        used.add(key);s.trace.append(dict(kind='integer_cg',proof=proof));s.rows.append(row);changed=True
    return changed
