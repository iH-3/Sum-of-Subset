"""New first-gap compression against explicit positive cores and subset sums."""
from pathlib import Path
from itertools import combinations
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import model as m,first_gap_core as fg
checks=0
for h,t in sorted({(h,t) for h,a,b in fg.CASES for t in (a,b)}):
 for r in range(2,9):
  for rest in combinations(range(h+1,h+r-t+7),r-t):
   X=([1] if t else [])+list(rest);tau=sum(X)-r*(r+1)//2;xi=max(X)-r
   phi=min([r,*[x+r-2*i for i,x in enumerate(X,1)]]);baseline=h*r if t==0 else (h-1)*(r-1);weight=h-t
   m.need(tau>=baseline and xi>=weight and tau-xi>=baseline-weight,'Explicit first-gap mass and maximum')
   for q in range(1,12):
    m.need(q*phi-tau+baseline<=q*weight+q*(q-1)//2,'Shifted staircase')
    m.need(q*phi-tau+xi+baseline<=(q+1)*weight+q*(q+1)//2,'Shifted maximum staircase')
   checks+=1
cores=[c for r in range(1,5) for c in combinations(range(1,8),r)];covered=0
for a in cores:
 for b in cores:
  sums={0}
  for x in (*a,*b):sums|={v+x for v in sums}
  h=next((i for i in range(1,4) if i not in sums),None)
  if h is None:continue
  matched=[]
  for index,(hh,ps,pt) in enumerate(fg.CASES):
   if hh!=h:continue
   if all(list(c[:p])==([1] if p else []) and all(v>=h+1 for v in c[p:]) for c,p in [(a,ps),(b,pt)]):matched.append(index)
  m.need(len(matched)==1,'Complete four-case first-gap classification');covered+=1
print(json.dumps(dict(status='PASS_NEW_FIRST_GAP_CORE',explicit_cores=checks,classified_core_pairs=covered,global_upper_bound_certified=False)))
