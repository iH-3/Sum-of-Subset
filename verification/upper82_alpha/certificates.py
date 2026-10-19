"""Complete finite cases and exact, nonnegative-variable Farkas checking."""
from collections import Counter
from math import gcd

def need(ok,msg):
    if not ok:raise ValueError(msg)

def states():
    for stage,e in [('order_B',27),('order_C',31),('order_D',35),('terminal',42)]:
        for r in range(24,43):
            I=(r-33)**2
            cap=95-e-I
            for tau in range(cap+1):
                choices=[0,1] if stage=='terminal' else [None]
                for choice in choices:yield (stage,r,tau,choice)

def system(state,build,masks=None):
    stage,r,tau,choice=state
    e={'order_B':27,'order_C':31,'order_D':35,'terminal':42}[stage]
    order={'order_B':(), 'order_C':('alphat',),
           'order_D':('alphat','C5s'), 'terminal':('alphat','C5s','C5t')}[stage]
    names,rows,eqs=build(r,tau,e=e,
        tail=True,longrank=stage=='terminal',
        order=order,negorder={'order_B':'alphat','order_C':'C5s','order_D':'C5t'}.get(stage),
        orientation=choice if stage=='terminal' else (1 if stage=='order_D' else None),forest_masks=masks)
    counts=Counter();data={}
    for kind,rs in [('le',rows),('eq',eqs)]:
        for row,rhs,label in rs:
            key=kind+':'+label+':'+str(counts[kind+':'+label]);counts[kind+':'+label]+=1
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
