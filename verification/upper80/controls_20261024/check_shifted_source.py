"""Explicit sets check every shifted-core native interval and fixed cover."""
from pathlib import Path
import json,random,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import shifted_source as u,model as m,parametric as p
rng=random.Random(942410);cases=intervals=covers=0

st=list(m.patterns(4))[142];p.build(st,4);Z=p.build.last_Z
for sample in range(250):
    k=rng.randrange(5);x={'ONE':1,'rank_k':k,'hole_W':1};sides={}
    for side,r in [('s',32-k),('t',32+k)]:
        dev=[1]*(r-3)+sorted(rng.randrange(1,5) for _ in range(3))
        core=[i+1+d for i,d in enumerate(dev)];R=core[-1];offsets=sorted(rng.sample(range(1,150),4))
        sides[side]=core+[R+d for d in offsets]
        x.update({'R'+side:R,'M'+side:R+offsets[-1],'t'+side:sum(dev),'x'+side:dev[-1],'S'+side:sum(sides[side])})
        x.update({off+side:v for off,v in zip('abce',offsets)})
        x.update({off+side:rng.randrange(1,401) for off in ('X','g','h','d')})
    if x['ts']+x['tt']+k>94:continue
    ev=lambda row:sum(c*x[key] for key,c in row.items())
    modes,data,chains=u.chains(st,Z,x);guards,_=u.catalogue(st,Z,modes)
    if any(ev(g)>0 for g in guards):raise ValueError('Shifted fixture guards')
    D={0,*sides['s'],*(-v for v in sides['t'])}
    for side in 'st':
        source=D if side=='s' else {-v for v in D};lam=x['d'+side]-2*x['M'+side]-2*x['X'+side]-x['g'+side]
        ret=[name for name,status in st.items() if status==1 and name[-1]==side]
        native={lam+a+b for a in source for b in source}|{ev(Z[name])+a for name in ret for a in source}
        for lo,hi in data[side]:
            if not set(range(ev(lo),ev(hi)+1))<=native:raise ValueError('Invalid shifted native interval')
            intervals+=1
        for label,form in m.fixed_forms().items():
            if ('+' in label)!=(side=='s'):continue
            for chain in chains[side]:
                if not ev(data[side][chain[0]][0])<=ev(form)<=ev(data[side][chain[-1]][1]):continue
                guards=u.cover_guards(st,Z,modes,side,chain,label)
                if all(ev(g)<=0 for g in guards):
                    if ev(form) not in native:raise ValueError('Invalid shifted covered fixed point')
                    covers+=1
    cases+=1
if covers==0:raise ValueError('Vacuous shifted-cover control')
print(json.dumps(dict(status='PASS_SHIFTED_CORE_NATIVE_COVER',physical_core_pairs=cases,known_native_intervals=intervals,covered_fixed_values=covers)))
