from pathlib import Path
import sys,json,random
root=Path(__file__).resolve().parents[3];sys.path.insert(0,str(root/'verification/upper80'));import cover_geometry as coverage,model as m,parametric as p
rng=random.Random(241226);cases=points=0
st=list(m.patterns(6))[436];p.POINT_OVERLAP=True;p.build(st,6);Z=p.build.last_Z
for sample in range(120):
 k=rng.randrange(18);x={'ONE':1,'rank_k':k};sides={};outer={}
 for side,r in [('s',32-k),('t',32+k)]:
  dev=[0]*(r-5)+sorted(rng.randrange(5) for _ in range(5));core=[i+1+d for i,d in enumerate(dev)];R=core[-1]
  offsets=sorted(rng.sample(range(1,121),4));sides[side]=core+[R+off for off in offsets]
  x.update({'R'+side:R,'M'+side:R+offsets[-1],'t'+side:sum(dev),'x'+side:dev[-1],'S'+side:sum(sides[side])})
  x.update({off+side:v for off,v in zip('abce',offsets)})
  x.update({off+side:rng.randrange(1,301) for off in ('X','g','h','d')})
  a=x['M'+side]+x['X'+side];b=a+x['g'+side];c=b+x['h'+side];d=c+x['d'+side];outer[side]=[a,b,c,d]
 ev=lambda row:sum(c*x[name] for name,c in row.items());actual_st={}
 for name,center in Z.items():
  side=name[-1];o='t' if side=='s' else 's';value=ev(center)
  actual_st[name]=0 if value+x['M'+side]<=0 else 2 if value-x['M'+o]>x['S'+side] else 1
 for side,other in [('s','t'),('t','s')]:
  A={0,*sides[side],*outer[side],*(-v for v in sides[other]),*(-v for v in outer[other])};amin=min(A)
  bits=sum(1<<(a-amin) for a in A);two=0
  for a in A:two|=bits<<(a-amin)
  four=0;positions=two
  while positions:
   bit=positions&-positions;positions-=bit;four|=two<<(bit.bit_length()-1)
  S=x['S'+side];start=sum(outer[side])+1-4*amin;actual=(four>>start)&((1<<S)-1);envelope=0
  components=coverage.catalogue(actual_st,Z,side)
  for name,lo,hi in components:
   a=max(1,ev(lo));b=min(S,ev(hi))
   if a<=b:envelope|=((1<<(b-a+1))-1)<<(a-1)
  missed=actual&~envelope
  if missed:raise ValueError(('Incomplete four-sum cover',sample,side,(missed&-missed).bit_length()))
  cases+=1;points+=actual.bit_count()
print(json.dumps(dict(status='PASS_EXPLICIT_FOUR_SUM_COVER',physical_targets=cases,covered_four_sum_values=points)))
