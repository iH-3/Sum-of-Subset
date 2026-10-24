"""Independent source-set checks for enlarged union cardinalities."""
from pathlib import Path
import copy,json,random,sys
root=Path(__file__).resolve().parents[3];sys.path.insert(0,str(root/'verification/upper80'))
import cover_capacity,model as m,parametric as p
rng=random.Random(811024);st=list(m.patterns(6))[436];p.build(st,6);Z=p.build.last_Z
cases=sharp=mutations=0
for sample in range(300):
    k=rng.randrange(8);x={'ONE':1,'rank_k':k,'hole_W':0};sources={}
    for side,r in [('s',32-k),('t',32+k)]:
        dev=[0]*r if sample%3==0 else [0]*(r-8)+sorted(rng.randrange(12) for _ in range(8))
        core=[i+1+d for i,d in enumerate(dev)];R=core[-1];offsets=sorted(rng.sample(range(1,151),4))
        sources[side]=core+[R+off for off in offsets]
        x.update({'R'+side:R,'M'+side:R+offsets[-1],'S'+side:sum(sources[side])})
        x.update({off+side:v for off,v in zip('abce',offsets)})
        x.update({off+side:rng.randrange(1,401) for off in ('X','g','h','d')})
    ev=lambda row:sum(c*x[name] for name,c in row.items())
    D={0,*sources['s'],*(-v for v in sources['t'])};x['K']=len({a+b for a in D for b in D});native_hits={};full_hits={}
    for side in 'st':
        source=D if side=='s' else {-v for v in D};lam=x['d'+side]-2*x['M'+side]-2*x['X'+side]-x['g'+side]
        ret=[name for name,status in st.items() if status==1 and name[-1]==side]
        native={lam+a+b for a in source for b in source}|{ev(Z[name])+a for name in ret for a in source}
        fixed={ev(form) for label,form in m.fixed_forms().items() if ('+' in label)==(side=='s')}
        native_hits[side]=sum(1<=v<=x['S'+side] for v in native)
        full_hits[side]=sum(1<=v<=x['S'+side] for v in native|fixed)
    for mode,side in [('sumset',None),('native',None),('full','s'),('full','t')]:
        proof=cover_capacity.recipe(st,Z,x,mode,side);row,guards=cover_capacity.derive(st,Z,proof,0)
        if any(ev(g)>0 for g in guards):raise ValueError('Capacity recipe violates integer guards')
        sides='st' if mode=='native' else side
        if mode=='sumset':upper=x['K']-ev(row[0]);actual=x['K']
        else:upper=sum(x['S'+s] for s in sides)-ev(row[0]);actual=sum((native_hits if mode=='native' else full_hits)[s] for s in sides)
        if actual>upper:raise ValueError(('Cover capacity understated',sample,mode,side,actual,upper))
        if sample%3==0:
            if actual!=upper:raise ValueError('Zero-excess enlarged cover should be exact')
            sharp+=1
        bad=copy.deepcopy(proof);plan=next(iter(bad['sides'].values()))
        if plan['outside']:plan['outside'].pop()
        else:plan['groups'][0]['members'].pop()
        try:cover_capacity.derive(st,Z,bad,0)
        except ValueError:mutations+=1
        else:raise ValueError('Incomplete cover inventory accepted')
        cases+=1
print(json.dumps(dict(status='PASS_ENLARGED_COVER_CAPACITY',capacity_checks=cases,exact_zero_excess_cases=sharp,rejected_incomplete_inventories=mutations)))
