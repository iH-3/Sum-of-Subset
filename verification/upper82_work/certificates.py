"""Exact finite domain and integer Farkas-certificate checking."""
from collections import Counter
from math import gcd

RETAINED=('Us','Vs','alphas','betas','C5s','C6s','C7s',
          'Ht','Ut','Vt','alphat','C6t','C7t')
GAPS=('Xs','Xt','gs','gt','ht')

def need(ok,msg):
    if not ok: raise ValueError(msg)

def states():
    for stage in ('cutoff','bootstrap','terminal'):
        for r in range(24,43):
            I=(r-33)**2
            for tau in range(83-I):
                early=4*tau<132+3*I
                if stage=='bootstrap':
                    if early: continue
                    for gap in GAPS: yield (stage,r,tau,None,gap)
                else:
                    choices=[None]
                    if 82-I-tau>=71:
                        choices += [(name,end) for name in RETAINED for end in 'lu']
                    for heavy in choices: yield (stage,r,tau,heavy,None)

def system(state,build):
    stage,r,tau,heavy,gap=state
    I=(r-33)**2
    names,rows,eqs=build(r=r,taueq=tau,
        heavy=None if heavy is None else tuple(heavy),
        tail=stage!='cutoff',cutoff=stage!='cutoff',negcutoff=stage=='cutoff',
        longrank=stage=='terminal' or 4*tau<132+3*I,guard=gap)
    counts=Counter(); data={}
    for kind,rs in [('le',rows),('eq',eqs)]:
        for row,rhs,label in rs:
            key=kind+':'+label+':'+str(counts[kind+':'+label])
            counts[kind+':'+label]+=1
            data[key]=(row,rhs,kind)
    return names,data

def evaluate(cert,data,strict=True):
    lhs=Counter();rhs=0
    for key,weight in cert:
        if key not in data: return None
        row,b,kind=data[key]
        if type(weight) is not int or (kind=='le' and weight<0):return None
        for name,c in row.items():lhs[name]+=weight*c
        rhs+=weight*b
    if any(x<0 for x in lhs.values()) or rhs>=0:
        if strict:raise ValueError('invalid integer contradiction')
        return None
    return -rhs

def normalize(cert):
    divisor=0
    for _,w in cert:divisor=gcd(divisor,abs(w))
    need(divisor>0,'empty certificate')
    return sorted((key,w//divisor) for key,w in cert if w)
