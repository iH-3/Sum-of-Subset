"""Independent bounded enumeration and mutation controls for modular proofs."""
from pathlib import Path
import copy,itertools,json,random,sys
root=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(root/'verification/upper80'))
import modular

rng=random.Random(81080);cases=0;certificates=0;rejected=0
names=('xs','xt','ts')
points=[dict(zip(names,p),ONE=1) for p in itertools.product(range(6),repeat=3)]
ev=lambda row,p:sum(v*p[k] for k,v in row.items())
for _ in range(700):
    witness=rng.choice(points)
    eqs=[({'ONE':1},1,'unit')];rows=[]
    for i in range(rng.randrange(1,5)):
        row={name:rng.randrange(-5,6) for name in names};rhs=ev(row,witness)
        if rng.randrange(2):eqs.append((row,rhs,'sample equality'))
        else:rows.extend([(row,rhs,'opposite row'),({k:-v for k,v in row.items()},-rhs,'opposite row')])
    if rng.randrange(4)==0:
        for name in names:
            if witness[name]==0:rows.append(({name:2},0,'nonnegative zero'))
    basis=modular.Basis(rows,eqs)
    feasible=[p for p in points if all(ev(row,p)==rhs for row,rhs,_ in eqs) and all(ev(row,p)<=rhs for row,rhs,_ in rows)]
    if not feasible:raise ValueError('Missing construction witness')
    for i in range(12):
        target={name:rng.randrange(-5,6) for name in names};target['ONE']=rng.randrange(-10,11)
        cert=basis.exclude(target);cases+=1
        if cert is None:continue
        modular.check(cert,rows,eqs,target);certificates+=1
        if any(ev(target,p)==0 for p in feasible):raise ValueError('Excluded an actual integer solution')
        bad=copy.deepcopy(cert)
        for term in bad['equations']:term[2]=0
        try:modular.check(bad,rows,eqs,target)
        except ValueError:rejected+=1
        else:raise ValueError('Accepted mutated zero-weight certificate')
# A rational solution can fail parity, and opposite inequalities license a
# new integer equality. This obstruction is invisible to ordinary LP.
rows=[({'xs':2,'xt':-2},1,'upper'),({'xs':-2,'xt':2},-1,'lower')]
eqs=[({'ONE':1},1,'unit')]
cert=modular.Basis(rows,eqs).exclude({'ts':1})
if cert is None:raise ValueError('Missed inconsistent parity')
modular.check(cert,rows,eqs,{'ts':1})
if modular.Basis([],eqs).exclude({'unlicensed_real':2,'ONE':-1}) is not None:raise ValueError('Admitted unlicensed real variable')
print(json.dumps(dict(status='PASS_MODULAR_EXCLUSIONS',cases=cases,certificates=certificates,mutations_rejected=rejected)))
