"""New uncertain-point source decomposition, checked on actual73-point sets."""
from pathlib import Path
import sys,json,random,copy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import model as m,trimmed_source as tr
rng=random.Random(2026102421);bounds=capacities=components=sharp=0
for trial in range(80):
 k=rng.randrange(18);v={'ONE':1,'rank_k':k};cores={};T=[]
 for side,r,sign in [('s',32-k,1),('t',32+k,-1)]:
  phi0=rng.randrange(12)
  d=sorted(rng.randrange(13) for _ in range(r)) if trial%3==0 else [max(0,phi0-r+i) for i in range(1,r+1)]
  if trial%2:d[-1]+=rng.randrange(20,71)
  X=[i+y for i,y in enumerate(d,1)];cores[side]=X
  phi=min([r,*[x+r-2*i for i,x in enumerate(X,1)]]);v.update({'R'+side:X[-1],'x'+side:d[-1],'t'+side:sum(d),'phicore'+side:phi})
  offsets=sorted(rng.sample(range(1,151),4));v.update({off+side:x for off,x in zip('abce',offsets)});T.extend(sign*(X[-1]+x) for x in offsets)
  ev=lambda row:sum(c*v[key] for key,c in row.items())
  for j in range(1,5):
   for ell in range(15):
    low,high=tr.core_bound(side,j,ell);actual=X[-1-j]
    m.need(all(ev(a)<=actual for a in low) and all(ev(a)>=actual for a in high),'Actual indexed core bounds');bounds+=1
 D={0,*cores['s'],*(-x for x in cores['t']),*T};DD={a+b for a in D for b in D};v['K']=len(DD)
 for keep in range(1,5):
  proof,intervals,masses,clusters=tr.recipe(v,keep);B={0,*cores['s'][:-keep],*(-x for x in cores['t'][:-keep])};points=[*T,*cores['s'][-1:-keep-1:-1],*(-x for x in cores['t'][-1:-keep-1:-1])]
  from itertools import combinations_with_replacement
  actual=[{a+b for a in B for b in B},*[{a+x for a in B} for x in points],*[{a+b} for a,b in combinations_with_replacement(points,2)]]
  m.need(len(actual)==len(intervals),'Complete physical trimmed-source inventory')
  for Q,(lo,hi),mass in zip(actual,intervals,masses):
   m.need(ev(lo)<=min(Q)<=max(Q)<=ev(hi) and len(Q)<=ev(mass),'Actual component bound and intrinsic mass');components+=1
  m.need(set().union(*actual)==DD,'Exact complete physical2D decomposition')
  for indices in clusters:
   lo=min((intervals[i][0] for i in indices),key=ev);hi=max((intervals[i][1] for i in indices),key=ev)
   if sum(ev(masses[i]) for i in indices)<=ev(hi)-ev(lo)+1:proof['groups'].extend(dict(components=[i],mass=True) for i in indices)
   else:proof['groups'].append(dict(components=indices,lower=lo,upper=hi))
  row,guards=tr.derive(proof);m.need(all(ev(g)<=0 for g in guards) and ev(row[0])<=0,'Complete uncertain-point source capacity');capacities+=1;sharp+=ev(row[0])==0
bad=0;invalid=[]
p=copy.deepcopy(proof);p['keep']=5;invalid.append(p)
p=copy.deepcopy(proof);p['orders']['s']=15;invalid.append(p)
p=copy.deepcopy(proof);p['lower_choice']['s']=[True]*3;invalid.append(p)
p=copy.deepcopy(proof);p['groups'].pop();invalid.append(p)
p=copy.deepcopy(proof);p['groups'][0]['components'].append(p['groups'][0]['components'][0]);invalid.append(p)
p=copy.deepcopy(proof);p['groups']=[dict(components=list(range(len(intervals))),mass=True)];invalid.append(p)
for p in invalid:
 try:tr.derive(p)
 except ValueError:bad+=1
 else:raise ValueError('Invalid trimmed-source recipe accepted')
print(json.dumps(dict(status='PASS_NEW_TRIMMED_SOURCE',actual_sources=80,indexed_core_bounds=bounds,complete_decompositions=capacities,component_bounds=components,sharp_capacities=sharp,invalid_recipes_rejected=bad,global_upper_bound_certified=False)))
