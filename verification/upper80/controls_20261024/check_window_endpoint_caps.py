"""New endpoint-hole and window clipping bounds against explicit sumsets."""
from pathlib import Path
import sys,random,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import model as m,full_window as fw
rng=random.Random(2026102407);checks=0;clipped_checks=0
for _ in range(400):
    pos=sorted(rng.sample(range(1,21),rng.randrange(2,10)))
    neg=sorted(rng.sample(range(1,21),rng.randrange(2,10)))
    core={0,*pos,*(-a for a in neg)};values={'ONE':1}
    for side,data in [('s',pos),('t',neg)]:
        r=len(data);values.update({'R'+side:max(data),'x'+side:max(data)-r,'t'+side:sum(data)-r*(r+1)//2})
    sums={0}
    for q in range(1,5):
        sums={a+b for a in sums for b in core}
        if q>=2:
            capacity=sum(c*values[k] for k,c in fw.core_capacity(q).items())
            m.need(len(sums)<=capacity,'Explicit core sumset endpoint-hole bound');checks+=1
        lo,hi=min(sums),max(sums)
        L=rng.randint(lo-10,hi);U=rng.randint(L,hi+10)
        for left in (0,1):
            for right in (0,1):
                a=L if left else lo;b=U if right else hi
                if b-a+1>=0:
                    m.need(len({x for x in sums if L<=x<=U})<=b-a+1,'Explicit clipped hull capacity');clipped_checks+=1
bad=0
for power in (0,1,5,2.0,True):
    try:fw.core_capacity(power)
    except ValueError:bad+=1
    else:raise ValueError('Invalid core power accepted')
print(json.dumps(dict(status='PASS_NEW_WINDOW_ENDPOINT_CAPS',explicit_sumsets=checks,clipped_hulls=clipped_checks,negative_controls=bad,global_upper_bound_certified=False)))
