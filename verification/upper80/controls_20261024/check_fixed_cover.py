from pathlib import Path
import sys,json,random
root=Path(__file__).resolve().parents[3];sys.path.insert(0,str(root/'verification/upper80'));import exact,model as m,parametric as p
rng=random.Random(242024);hits=tests=positive=0
st=list(m.patterns(6))[436];p.POINT_OVERLAP=True;p.build(st,6);Z=p.build.last_Z;forms=m.fixed_forms()
for sample in range(120):
 k=rng.randrange(18);point={'ONE':1,'rank_k':k};sides={}
 for side,r in [('s',32-k),('t',32+k)]:
  dev=[0]*(r-5)+sorted(rng.randrange(5) for _ in range(5));core=[i+1+d for i,d in enumerate(dev)];R=core[-1]
  offsets=sorted(rng.sample(range(1,151),4));sides[side]=core+[R+off for off in offsets]
  point.update({'R'+side:R,'M'+side:R+offsets[-1],'t'+side:sum(dev),'x'+side:dev[-1]})
  point.update({off+side:v for off,v in zip('abce',offsets)})
  point.update({off+side:rng.randrange(1,600) for off in ('X','g','h','d')})
 ev=lambda row:sum(c*point[name] for name,c in row.items())
 for side,other in [('s','t'),('t','s')]:
  D={0,*sides[side],*(-x for x in sides[other])};DD={a+b for a in D for b in D};lam=point['d'+side]-2*point['M'+side]-2*point['X'+side]-point['g'+side]
  labels=[label for label in forms if ('+' in label)==(side=='s')]
  for _ in range(50):
   label=rng.choice(labels);resource=rng.choice([name for name in Z if name[-1]==side]+['L'+side]);q=rng.randrange(1,6)
   witness=rng.choice(exact.LEADING_WITNESSES) if resource[0]=='L' else None
   guards=exact.fixed_cover_guards(label,resource,q,witness,Z);tests+=1
   if max(map(ev,guards))>0:continue
   actual={lam+x for x in DD} if resource[0]=='L' else {ev(Z[resource])+x for x in D}
   if ev(forms[label]) not in actual:raise ValueError(('False fixed cover',sample,label,resource,q,witness))
   hits+=1;positive+=ev(forms[label])>=1
print(json.dumps(dict(status='PASS_FIXED_SOURCE_CONTAINMENT',cases=tests,certified_hits=hits,positive_hits=positive)))
