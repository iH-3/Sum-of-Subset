"""Direct-set controls of the low-span core double-sum interval."""
from pathlib import Path
import json,random,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import exact
rng=random.Random(648124);checks=0

for _ in range(1600):
    k=rng.randrange(18);rs,rt=32-k,32+k
    xs=rng.randrange(rs+1);xt=rng.randrange(rs-xs+1)
    positive=set(rng.sample(range(1,rs+xs),rs-1))|{rs+xs}
    negative=set(rng.sample(range(1,rt+xt),rt-1))|{rt+xt}
    E={0,*positive,*(-v for v in negative)};EE={a+b for a in E for b in E}
    if not set(range(-2*rt,2*rs+1))<=EE:raise ValueError('Dense doubled core interval')
    values={'xs':xs,'xt':xt,'rank_k':k,'ONE':1}
    for side in 'st':
        target=EE if side=='s' else {-v for v in EE}
        for t in range(-2*(rt if side=='s' else rs)-1,2*(rs if side=='s' else rt)+2):
            guards=exact.double_source_guards(side,{'ONE':t},'dense_core',5)
            if all(sum(c*values[key] for key,c in row.items())<=0 for row in guards):
                if t not in target:raise ValueError('Invalid dense-core witness guards')
                checks+=1
print(json.dumps(dict(status='PASS_DENSE_CORE_DOUBLE_INTERVAL',actual_core_pairs=1600,witness_guard_checks=checks)))
