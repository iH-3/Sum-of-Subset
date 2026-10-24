from pathlib import Path
import sys,random,json
root=Path(__file__).resolve().parents[3];sys.path.insert(0,str(root/'verification/upper80'));import exact
rng=random.Random(24601);cases=0
for n in range(1,13):
 for _ in range(40):
  edges=tuple(sorted({sum(1<<i for i in rng.sample(range(n),rng.randrange(1,min(3,n)+1))) for _ in range(rng.randrange(1,15))}))
  expected=min(mask.bit_count() for mask in range(1<<n) if all(mask&edge for edge in edges))
  if exact._minimum_hitting(edges)!=expected:raise ValueError('Wrong fixed-label transversal')
  cases+=1
print(json.dumps(dict(status='PASS_FIXED_CONFLICT_CAPACITY',exhaustive_graph_checks=cases)))
