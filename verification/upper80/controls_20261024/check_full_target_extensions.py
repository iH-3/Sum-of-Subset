"""Only the newly added actual-subset and cover-disjunction rules."""
from pathlib import Path
import sys,json,random,copy
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'verification/upper80'))
import model as m,exact,full_cover as fc
rng=random.Random(80261024);checks=0
for _ in range(20):
    x={'ONE':1};blocks=[];cores=[];outers=[]
    for side,sign in [('s',1),('t',-1)]:
        core=sorted(rng.sample(range(1,20),8));R=max(core);offs=sorted(rng.sample(range(1,35),4))
        tails=[R+a for a in offs];x.update({'R'+side:R,'M'+side:tails[-1],'S'+side:sum(core+tails)})
        x.update({a+side:b for a,b in zip('abce',offs)});x.update({a+side:rng.randrange(1,12) for a in 'Xghd'})
        blocks.extend([[sign*a] for a in tails]);cores.append([sign*a for a in core])
        p=tails[-1]+x['X'+side];outer=[p,p+x['g'+side],p+x['g'+side]+x['h'+side],p+x['g'+side]+x['h'+side]+x['d'+side]]
        outers.extend(sign*a for a in outer)
    blocks.extend(cores);flat=[v for b in blocks for v in b]+outers
    m.need(len(flat)==len(set(flat)),'Physical source blocks and outer points are disjoint')
    for _ in range(100):
        om=rng.randrange(256);sm=rng.randrange(1024)
        actual=sum(v for i,v in enumerate(outers) if om>>i&1)+sum(sum(b) for i,b in enumerate(blocks) if sm>>i&1)
        m.need(sum(c*x[k] for k,c in fc.known_target(om,sm).items())==actual,'Actual subset target identity');checks+=1
st=([*m.patterns(6),*m.partial_patterns(6)])[436]
base=dict(st=st,j=6,positive=False,limits={},trace=[dict(kind='full_cover_known_probe',mask=0,source_mask=0)])
exact.replay(base,require_closed=False);negative=[]
def reject(name,step):
    rec=copy.deepcopy(base);rec['trace'].append(step)
    try:exact.replay(rec,require_closed=False)
    except (ValueError,KeyError,IndexError,TypeError):negative.append(name)
    else:raise ValueError('Accepted invalid new rule: '+name)
reject('invalid source mask',dict(kind='full_cover_known_probe',mask=0,source_mask=1024))
reject('noninteger source mask',dict(kind='full_cover_known_probe',mask=0,source_mask=True))
reject('invalid outer mask',dict(kind='full_cover_known_probe',mask=256,source_mask=0))
reject('subsumption by refinable hull',dict(kind='full_cover_subsume',probe=0,node=[494,-1],by=[0,-1],certificates=[]))
reject('self subsumption',dict(kind='full_cover_subsume',probe=0,node=[494,-1],by=[494,-1],certificates=[]))
reject('modular interval deletion',dict(kind='full_cover_modular_exclude',probe=0,node=[0,-1],certificate={}))
reject('incomplete disjunction',dict(kind='full_cover_bound',probe=0,guard={'ONE':-1},cases=[]))
cases=[dict(node=list(node),infeasible=False,certificate=dict(weights=[],denominator=1)) for node in sorted(fc.initial_nodes())]
valid=copy.deepcopy(base);valid['trace'].append(dict(kind='full_cover_bound',probe=0,guard={'ONE':-1},cases=cases));exact.replay(valid,require_closed=False)
reject('false common bound',dict(kind='full_cover_bound',probe=0,guard={'ONE':1},cases=cases))
reject('duplicate cover alternative',dict(kind='full_cover_bound',probe=0,guard={'ONE':-1},cases=[*cases,cases[0]]))
print(json.dumps(dict(status='PASS_NEW_FULL_TARGET_RULES',actual_subset_checks=checks,negative_controls=negative,global_upper_bound_certified=False)))
