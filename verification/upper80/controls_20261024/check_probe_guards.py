"""Independent integer interval checks for zero and positive-hole probes."""
from pathlib import Path
import sys,json,random
root=Path(__file__).resolve().parents[3];sys.path.insert(0,str(root/'verification/upper80'))
import cover_geometry as cover
rng=random.Random(246024);cases=0
for width in (1,8):
 for _ in range(5000):
  end=rng.randrange(-20,21);lo=rng.randrange(-20,21);hi=lo+rng.randrange(0,21);S=rng.randrange(1,61)
  x={'ONE':1,'end':end,'lo':lo,'hi':hi,'Ss':S};components=[('probe',{'end':1},{'end':1}),('candidate',{'lo':1},{'hi':1})]
  ev=lambda row:sum(c*x[k] for k,c in row.items());start=end+1;stop=start+width-1
  bracket=all(ev(row)<=0 for row in cover.bracket(components,'s',0,width))
  if bracket!=(1<=start<=stop<=S):raise ValueError('Wrong target bracket')
  excluded=any(ev(cover.exclusion(components,0,1,direction,width))<=0 for direction in (0,1))
  intersects=all(ev(row)<=0 for row in cover.containment(components,0,1,width))
  expected=not(hi<start or stop<lo)
  if intersects!=expected or excluded==expected:raise ValueError('Wrong component/probe boundary')
  cases+=1
# Seven consecutive holes do not force a hit; eight points with only seven
# holes do. This control guards the positive-regime width used by the replay.
target=set(range(1,10))-{1,2,3,4,5,6,7}
if target&set(range(1,8)) or not target&set(range(1,9)):raise ValueError('Hole-width control failed')
print(json.dumps(dict(status='PASS_TARGET_PROBE_GUARDS',integer_interval_checks=cases,positive_width=8)))
