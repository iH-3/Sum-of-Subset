"""Dense first-gap prefix memberships, including the joined 2E interval."""
from pathlib import Path
import sys,random,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import source_union as su,first_gap_core as fg,model as m
rng=random.Random(2026102412);counts={'shape_double':0,'shape_s':0,'shape_t':0}
for case,(h,ps,pt) in enumerate(fg.CASES):
    for trial in range(30):
        k=rng.randrange(18);x={'ONE':1,'rank_k':k};E={0};T=[]
        for side,r,t,sign in [('s',32-k,ps,1),('t',32+k,pt,-1)]:
            d=[0]*(r-t-5)+sorted(rng.randrange(4) for _ in range(5));X=([1] if t else [])+[h+i+v for i,v in enumerate(d,1)]
            x.update({'R'+side:max(X),'t'+side:sum(X)-r*(r+1)//2});E.update(sign*v for v in X)
            offsets=sorted(rng.sample(range(1,91),4));x.update({off+side:v for off,v in zip('abce',offsets)});T.extend(sign*(max(X)+v) for v in offsets)
        EE={a+b for a in E for b in E};U=EE|{a+b for a in E for b in T};ev=lambda row:sum(v*x[k] for k,v in row.items())
        for pair in su.PAIRS:
            choices=[('shape_double','ordinary')]+[(w,mode) for mode in ('shape_s','shape_t') for w in ('zero','core_s','core_t',*range(8))]
            for w,mode in choices:
                if all(ev(g)<=0 for g in su.membership(pair,w,case,mode)):
                    m.need(T[pair[0]]+T[pair[1]] in U,'Actual shape-source membership')
                    counts[w if w=='shape_double' else mode]+=1
m.need(all(v>100 for v in counts.values()),'Each new shape membership must be exercised')
print(json.dumps(dict(status='PASS_NEW_DENSE_SHAPE_SOURCE_MEMBERSHIPS',actual_core_pairs=120,memberships=counts,global_upper_bound_certified=False)))
