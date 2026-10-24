from pathlib import Path
import sys,json,random
from itertools import product
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import cg_cut as cg,model as m
rng=random.Random(80);checks=0;eqs=[({'ONE':1},1,'unit')]
for _ in range(100):
    rows=[({'xs':rng.randrange(-5,6),'xt':rng.randrange(-5,6),'ONE':rng.randrange(-5,6)},rng.randrange(-5,16),'sample') for i in range(3)]
    weights=[('r',i,rng.randrange(1,9)) for i in range(3)]+[('e',0,rng.choice([-3,-2,-1,1,2,3]))]
    proof=dict(weights=weights,denominator=rng.randrange(1,10));row,b,_=cg.derive(proof,rows,eqs)
    for x,y in product(range(8),repeat=2):
        point=dict(xs=x,xt=y,ONE=1)
        if any(sum(c*point[k] for k,c in r.items())>rhs for r,rhs,_ in rows):continue
        m.need(sum(c*point[k] for k,c in row.items())<=b,'Exact CG consequence on integer point');checks+=1
rows=[({'xs':2},3,'half integral')];proof=dict(weights=[('r',0,1)],denominator=2)
m.need(cg.derive(proof,rows,eqs)[:2]==({'xs':1},1),'Sharp half-integer CG rounding')
bad=[]
for label,p,r,e in [('negative multiplier',dict(weights=[('r',0,-1)],denominator=2),rows,eqs),('zero denominator',dict(weights=[('r',0,1)],denominator=0),rows,eqs),('missing unit',proof,rows,[]),('unknown variable',proof,[({'unknown':2},3,'invalid')],eqs),('duplicate multiplier',dict(weights=[('r',0,1),('r',0,1)],denominator=2),rows,eqs)]:
    try:cg.derive(p,r,e)
    except ValueError:bad.append(label)
    else:raise ValueError('Invalid CG certificate accepted: '+label)
m.need(cg.solve_exact([[2,1],[1,3]],[1,0])==[cg.Fraction(3,5),cg.Fraction(-1,5)],'Rational basis elimination')
print(json.dumps(dict(status='PASS_NEW_INTEGER_CG',integer_point_checks=checks,negative_controls=bad,global_upper_bound_certified=False)))
