"""Exact SIZE86 AP-exception replay; imports stdlib only, no discovery search.
Rows are freshly encoded in named sparse coordinates, not loaded from SIZE87.
"""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'inputs'
T=lambda r:r*(r+1)//2

def add(*vs):
    out={}
    for v in vs:
        for x,c in v.items(): out[x]=out.get(x,0)+c
    return {x:c for x,c in out.items() if c}
def mul(c,v):return {x:c*a for x,a in v.items() if c*a}
def variable(x):return {x:1}
def rows86(a,branch,choice,family="nonprimitive",z=0,strengthen=True):
    b=69-a
    assert branch in ('A','B') and choice in (0,1)
    assert family in ('nonprimitive','halfstep','boundary14')
    assert z==0 if family in ('nonprimitive','boundary14') else 0<=z<=12
    rows={}
    def le(label,lhs,rhs):
        assert label not in rows
        rows[label]=(lhs,rhs)
    p=[variable('p'+str(i)) for i in range(1,5)]
    q=[variable('q'+str(i)) for i in range(1,5)]
    cp=add(p[0],*(mul(-1,x) for x in p[1:]))
    cq=add(q[0],*(mul(-1,x) for x in q[1:]))
    alpha=lambda xs:add(xs[1],mul(-1,xs[2]),mul(-1,xs[3]))
    beta=lambda xs:add(mul(2,xs[1]),mul(-1,xs[0]),mul(-1,xs[2]),mul(-1,xs[3]))
    pos=[add(cp,x) for x in p]+[add(cp,mul(-1,x)) for x in q]+[alpha(p),beta(p)]
    neg=[add(cq,x) for x in q]+[add(cq,mul(-1,x)) for x in p]+[alpha(q),beta(q)]
    pair2=9 if branch=='A' else 5
    centers=[(s+str(i),cs[i],s) for s,cs in [('p',pos),('q',neg)] for i in range(10) if i not in (4,pair2)]
    centers += [('pair1p',pos[4],'p'),('pair2p' if choice==0 else 'pair2q',(pos if choice==0 else neg)[pair2],'p' if choice==0 else 'q')]
    assert len(centers)==18
    for s,xs,r in [('p',p,a),('q',q,b)]:
        for i in range(3):le(f'{s}{i+1}>{s}{i+2}',add(xs[i+1],mul(-1,xs[i])),-1)
        le(s+'4>M',add(variable('M'+s),mul(-1,xs[3])),-1)
        le('M'+s+'>=R+4',{'M'+s:-1,'R'+s:1},-4)
        scale=2 if strengthen and family!='boundary14' and r==min(a,b) else 1
        le('R'+s+'>='+('a' if s=='p' else 'b'),{'R'+s:-1},-scale*r)
        le('S'+s+' mass',{'M'+s:2,'R'+s:6,'S'+s:-2},-2*(scale*T(r)+6))
    losses={'delta':-1,'Lp':1,'Lq':1}
    for label,v,s in centers:
        other='q' if s=='p' else 'p'
        low='loss '+label+' low'; high='loss '+label+' high'
        le(label+' low',add(mul(-1,v),{'M'+s:-1,low:-1}),-78)
        le(label+' high',add(v,{'S'+s:-1,'M'+other:-1,high:-1}),-77)
        losses[low]=losses[high]=1
    le('sumloss',losses,0)
    le('cardinality mass',{'Sp':1,'Sq':1,'delta':1,'K':-2},18*78+84+4*z)
    le('mixed envelope 4 4',{'K':1,'Mp':-2,'Mq':-2},1)
    k=34-min(a,b)
    E=587-k*(k+1)-146-T(min(a,b))
    if family=='halfstep':E+=3*z-(max(a,b)-5)
    if family=='boundary14':
        assert min(a,b)==14
        E=167-146
    le('AP exceptional delta cap',{'delta':1},E)
    return rows

def combine(a,item,family,z,strengthen=True):
    branch,empty,choice=item['mode'];assert empty==[]
    rows=rows86(a,branch,choice,family,z,strengthen);coeff={};rhs=0;seen=set()
    for label,w in item['weights']:
        assert label not in seen and label in rows and type(w) is int and w>0
        seen.add(label);lhs,bound=rows[label]
        coeff=add(coeff,mul(w,lhs));rhs+=w*bound
    return {'a':a,'b':69-a,'family':family,'z':z,'mode':[branch,choice],
            'rhs':rhs,'coeff':coeff,'pass':all(c>=0 for c in coeff.values()) and rhs<0}

# The old bulk runner also compared archival receipt bytes and checked redundant
# even-z cases.  It is intentionally omitted.  The package entry point invokes
# rows86/combine directly and checks the actual coefficients and RHS values.
