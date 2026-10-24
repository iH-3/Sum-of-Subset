"""Compare conditional union cardinality with explicitly constructed sources."""
from pathlib import Path
import json,random,sys
root=Path(__file__).resolve().parents[3];sys.path.insert(0,str(root/'verification/upper80'))
import exact,known_union,model as m,parametric as p
rng=random.Random(8106424);cases=sharp=tail_cases=joint_cases=0
st=list(m.patterns(6))[436];p.build(st,6);Z=p.build.last_Z
for sample in range(300):
    k=rng.randrange(8);x={'ONE':1,'rank_k':k,'delta':0};sides={}
    for side,r in [('s',32-k),('t',32+k)]:
        dev=[0]*r if sample%3==0 else [0]*(r-8)+sorted(rng.randrange(12) for _ in range(8))
        core=[i+1+d for i,d in enumerate(dev)];R=core[-1];offsets=sorted(rng.sample(range(1,151),4))
        sides[side]=core+[R+off for off in offsets]
        x.update({'R'+side:R,'M'+side:R+offsets[-1],'t'+side:sum(dev),'x'+side:dev[-1],'S'+side:sum(sides[side])})
        x.update({off+side:v for off,v in zip('abce',offsets)})
        x.update({off+side:rng.randrange(1,401) for off in ('X','g','h','d')})
    ev=lambda row:sum(c*x[k] for k,c in row.items())
    proof=known_union.recipe(st,Z,x);row,guards=known_union.derive(st,Z,proof,0)
    if any(ev(g)>0 for g in guards):raise ValueError('Recipe violates its own integer guards')
    D={0,*sides['s'],*(-v for v in sides['t'])};K=len({a+b for a in D for b in D});loss=0;tail_excluded={};represented_tail=0;new_fixed=0
    for side in 'st':
        source=D if side=='s' else {-v for v in D};lam=x['d'+side]-2*x['M'+side]-2*x['X'+side]-x['g'+side]
        ret=[name for name,status in st.items() if status==1 and name[-1]==side]
        native={lam+a+b for a in source for b in source}|{ev(Z[name])+a for name in ret for a in source}
        hits=sum(1<=v<=x['S'+side] for v in native);loss+=K+73*len(ret)-hits
        fixed={ev(form) for label,form in m.fixed_forms().items() if ('+' in label)==(side=='s')}
        new_fixed+=sum(1<=v<=x['S'+side] for v in fixed-native)
        end,licenses,points=known_union.tail_catalogue(st,Z,side)
        if all(ev(g)<=0 for g in licenses):
            fixed={ev(form) for label,form in m.fixed_forms().items() if ('+' in label)==(side=='s')}
            target={v for v in native|fixed if ev(end)<v<=x['S'+side]}
            allowed={ev(value) for _,value in points}
            if not target<=allowed:raise ValueError('Missing core-tail representation')
            excluded={i for i in range(len(points)) if any(ev(known_union.tail_exclusion(st,Z,side,i,d))<=0 for d in (0,1))}
            if len(target)>len(points)-len(excluded):raise ValueError('Core-tail capacity understated')
            tail_excluded[side]=excluded;represented_tail+=len(target)
            tail_cases+=1
    bound=ev(row[0])
    if bound>loss:raise ValueError(('Overstated native loss',sample,bound,loss))
    if sample%3==0:
        if bound!=loss:raise ValueError(('Zero-excess source should be exact',bound,loss))
        sharp+=1
    if set(tail_excluded)==set('st'):
        _,bound,_=known_union.joint_tail_capacity(st,Z,tail_excluded,84-new_fixed)
        if represented_tail>bound:raise ValueError('Joint core-tail capacity understated')
        joint_cases+=1
    cases+=1
if not tail_cases:raise ValueError('No licensed top-core tails tested')
print(json.dumps(dict(status='PASS_KNOWN_NATIVE_UNION',physical_sources=cases,exact_zero_excess_cases=sharp,licensed_core_tails=tail_cases,joint_core_tails=joint_cases)))
