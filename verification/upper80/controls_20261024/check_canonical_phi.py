from pathlib import Path
from itertools import combinations
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));import model as m
checks=0;sharp=0;sentinels=0
for r in range(1,9):
    for X in combinations(range(1,15),r):
        phi=min([r,*[x+r-2*i for i,x in enumerate(X,1)]])
        tau=sum(X)-r*(r+1)//2;xi=X[-1]-r
        m.need(tau<=phi*max(r,xi),'Canonical minimum upper mass')
        checks+=1;sharp+=tau==phi*max(r,xi);sentinels+=phi==r
print(json.dumps(dict(status='PASS_NEW_CANONICAL_CORE_MASS',actual_cores=checks,sharp_cases=sharp,sentinel_cases=sentinels,global_upper_bound_certified=False)))
