from pathlib import Path
import sys,json,random,itertools
root=Path(__file__).resolve().parents[3];sys.path.insert(0,str(root/'verification/upper80'));import exact,model as m,parametric as p
rng=random.Random(240026);cases=probe_tests=probe_hits=0
st=list(m.patterns(6))[436];p.POINT_OVERLAP=True;p.FULL_EDGES=True;p.build(st,6);Z=p.build.last_Z;forms=m.fixed_forms()
for sample in range(120):
 k=rng.randrange(18);point={'ONE':1,'rank_k':k};sides={}
 for side,r in [('s',32-k),('t',32+k)]:
  dev=[0]*(r-5)+sorted(rng.randrange(5) for _ in range(5));core=[i+1+d for i,d in enumerate(dev)];R=core[-1]
  offsets=sorted(rng.sample(range(1,101),4));sides[side]=core+[R+off for off in offsets]
  point.update({'R'+side:R,'M'+side:R+offsets[-1],'t'+side:sum(dev),'x'+side:dev[-1],'S'+side:sum(sides[side])})
  point.update({off+side:v for off,v in zip('abce',offsets)})
  point.update({off+side:rng.randrange(1,101) for off in ('X','g','h','d')})
 ev=lambda row:sum(c*point[name] for name,c in row.items());values={label:ev(form) for label,form in forms.items()};sources={};unions={}
 for side,other in [('s','t'),('t','s')]:
  D={0,*sides[side],*(-v for v in sides[other])};sources[side]=D
  lam=point['d'+side]-2*point['M'+side]-2*point['X'+side]-point['g'+side]
  unions[side]={lam+a+b for a in D for b in D}|{ev(Z[name])+a for name in Z if name[-1]==side for a in D}
 low={label for label,v in values.items() if v<=0};high={label for label,v in values.items() if v>point['S'+('s' if '+' in label else 't')]}
 covered={label for label,v in values.items() if v in unions['s' if '+' in label else 't']};pos={label for label in covered if values[label]>=1}
 actual=sum(len({v for label,v in values.items() if ('+' in label)==(side=='s') and 1<=v<=point['S'+side] and v not in unions[side]}) for side in 'st')
 if any(not(set(group)&low) for group in m.GROUPS):raise ValueError('Negative baseline group failed')
 known_low={x for x in sorted(low) if rng.randrange(2)};known_high={x for x in sorted(high) if rng.randrange(2)};known_cover={x for x in sorted(covered) if rng.randrange(4)==0};known_pos={x for x in sorted(known_cover&pos) if rng.randrange(2)}
 pairs=set()
 for a,b in rng.sample(list(itertools.combinations(sorted(forms),2)),200):
  modes=['low','high']+(['apart','equal'] if ('+' in a)==('+' in b) else [])
  if any(all(ev(g)<=0 for g in exact.fixed_pair_guards(a,b,mode)) for mode in modes):pairs.add((a,b))
 credit=exact.credit(known_low,known_high,0,known_cover,known_pos,pairs)
 if actual>84-credit:raise ValueError(('False fixed credit',sample,actual,credit))
 cases+=1
 for resource in Z:
  side=resource[-1];center=ev(Z[resource]);labels=[label for label,v in values.items() if ('+' in label)==(side=='s') and v>=1]
  for core_side in 'st':
   sign=1 if core_side==side else -1;n=31+(-k if core_side=='s' else k)
   selected=sorted((sign*(values[label]-center),label) for label in labels if 1<=sign*(values[label]-center)<=n)
   for (v,a),(w,b) in itertools.combinations(selected,2):
    if v==w:continue
    guards=exact.fixed_probe_pair_guards(a,b,resource,core_side,Z);probe_tests+=1
    if max(map(ev,guards))>0:continue
    if not any(values[label]-center in sources[side] for label in (a,b)):raise ValueError(('False probe conflict',sample,a,b))
    probe_hits+=1
if not probe_hits:raise ValueError('Probe regression had no hits')
print(json.dumps(dict(status='PASS_FIXED_CAPACITY_AND_PROBES',source_cases=cases,probe_pair_tests=probe_tests,probe_pair_hits=probe_hits)))
