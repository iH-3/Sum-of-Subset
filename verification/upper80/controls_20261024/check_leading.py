from pathlib import Path
import sys,random,json
root=Path(__file__).resolve().parents[3];sys.path.insert(0,str(root/'verification/upper80'))
import exact
rng=random.Random(20261024);checks=hits=improvements=0
for case in range(1500):
 k=rng.randrange(18);point={'ONE':1,'rank_k':k};sides={}
 for side,r in [('s',32-k),('t',32+k)]:
  defects=[0]*(r-4)+sorted(rng.randrange(5) for _ in range(4));core=[i+1+d for i,d in enumerate(defects)];R=core[-1]
  offsets=sorted(rng.sample(range(1,181),4));sides[side]=core+[R+off for off in offsets]
  point.update({'R'+side:R,'M'+side:R+offsets[-1],'t'+side:sum(defects),'x'+side:defects[-1]})
  point.update({off+side:value for off,value in zip('abce',offsets)})
 D={0,*sides['s'],*(-a for a in sides['t'])};gap=rng.randrange(1,181);point['test_gap']=gap
 ordinary=set()
 for tag in exact.POINT_TAGS:
  if all(sum(c*point[v] for v,c in g.items())<=0 for g in exact.point_overlap_guards({'test_gap':1},tag)):ordinary.add(tag)
 for side in 'st':
  source=D if side=='s' else {-a for a in D};DD={a+b for a in source for b in source}
  for right,name in [(True,'V'),(False,'C7')]:
   edge=('L'+side,name+side,{'test_gap':1});_,other,_,shift=exact.leading_geometry(edge);center=sum(c*point[v] for v,c in shift.items());leading=set()
   for tag in exact.POINT_TAGS:
    if tag[0]!=(other if right else side):continue
    for witness in ('double_core','zero',*exact.POINT_TAGS):
     guards=exact.leading_point_guards(edge,tag,witness)
     if all(sum(c*point[v] for v,c in g.items())<=0 for g in guards):
      actual=center+sum(c*point[v] for v,c in exact.signed_source_point(tag,side).items())
      if actual not in DD:raise ValueError('False leading membership')
      leading.add(tag);break
   claimed=exact.edge_point_count(edge,ordinary,{}, {},leading)
   actual=len(DD&{center+a for a in source})
   if claimed>actual:raise ValueError(('False combined overlap',claimed,actual))
   checks+=1;hits+=len(leading);improvements+=claimed>len(ordinary)
if improvements<100:raise ValueError('Regression did not exercise new improvement')
print(json.dumps(dict(status='PASS_LEADING_OVERLAP_REGRESSION',cases=checks,certified_exterior_hits=hits,strict_improvements=improvements)))
