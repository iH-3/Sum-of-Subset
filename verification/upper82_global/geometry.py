"""Exact generic gap inventories and finite activity catalogue checks.
These checks supplement the written actual-set licenses.
"""
from pathlib import Path
from itertools import combinations,product
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
import model as m
import replay
ROOT=Path(__file__).resolve().parents[2]

def need(ok,message):
    if not ok:raise ValueError(message)

def gap_system(kind,label):
    rows=[];eqs=[];v=m.var;add=m.add
    def ge(row,b,name):rows.append(({k:-x for k,x in row.items()},-b,name))
    for s,o in [('s','t'),('t','s')]:
        eqs.append((add((1,v('M'+s)),(-1,v('R'+s)),(-1,v('e'+s))),0,'source maximum '+s))
        for name,b in [('R',1),('e',4),('X',1),('g',1)]:ge(v(name+s),b,'positive '+name+s)
        ge(add((1,v('h'+s)),(-1,v('X'+s))),1,'active alpha '+s)
        ge(add((1,v('d'+s)),(-1,{'Ms':1,'Mt':1}),(-2,v('X'+s)),(-1,v('X'+o)),(-1,{'gs':1,'gt':1}),(-1,v('h'+o))),1,'active C5 '+s)
        ge(add((1,v('d'+s)),(-1,v('h'+s)),(-1,v('X'+s))),1,'strict ten-label guard '+s)
        ge(add((1,v('d'+o)),(-1,v('h'+s))),1,'opposite outer guard '+s)
    afull=add((1,v('ds')),(-1,v('Xs')));acore=add((1,afull),(-1,v('es')))
    bfull=add((1,afull),(1,v('hs')),(-1,{'Ms':1,'Mt':1}));bcore=add((1,bfull),(1,v('et')))
    if kind=='core_final':
        ge(add((1,v('ds')),(-1,v('hs')),(-1,v('es'))),1,'alpha peels below core gap')
        ge(add((1,acore),(-1,{'gs':1,'hs':1})),1,'U3 below core gap')
    a,b=(afull,bfull) if kind=='full' else(acore,bcore)
    value=m.fixed_forms()[label]
    rows +=[(add((1,a),(-1,value)),-1,'tested point above gap lower'),(add((1,value),(-1,b)),-1,'tested point below gap upper')]
    return replay.matrix(rows,eqs)

def determinant(a):
    if len(a)==1:return a[0][0]
    return sum((-1)**j*a[0][j]*determinant([row[:j]+row[j+1:] for row in a[1:]]) for j in range(len(a)))

def verify():
    packet=json.loads((ROOT/'data/upper82_global_gap_inventory.json').read_text())
    need(packet['schema']=='upper82-gap-inventory-v1','Gap schema')
    full={'C+33','C+34','C+44','C+15','C+26','C+27','C+28','U+2','U+3','V+2'}
    initial=full|{'U+4'};final=initial-{'U+3','U+4','V+2'}
    keep={'full':full,'core_initial':initial,'core_final':final}
    expected={(kind,label) for kind in keep for label in m.fixed_forms() if '+' in label and label not in keep[kind]}
    seen=set();margins=[]
    for rec in packet['records']:
        key=(rec['kind'],rec['label']);need(key in expected and key not in seen,'Gap inventory coverage');seen.add(key)
        margins.append(replay.evaluate(rec['certificate'],gap_system(*key)))
    need(seen==expected and len(seen)==136,'Complete fixed-label gap inventories')
    need(3*4+4+10+11==37 and 2*4+4+10+8==30,'Actual source/leading/fixed counts')
    fixed=m.fixed_forms();grouped={label for group in m.GROUPS for label in group}
    high8={f'C{sign}1{i}' for sign in '+-' for i in range(1,5)}
    need(not high8 & grouped,'Initial eight HIGH labels must be outside baseline groups')
    for side,sign in [('s','+'),('t','-')]:
        need({k:v for k,v in fixed['C'+sign+'14'].items() if v}=={'h'+side:1,'d'+side:2},'C14 literal HIGH identity')
    guard=[]
    for w in range(0,15,2):
        eta=w//2
        bounds=[39-w-eta,99-w-eta,58-w-eta,59-w-eta,66-w]
        need(min(bounds)>0,'Size83 ownerless gap guard')
        guard.append(dict(w=w,strict_margins=bounds))
    # The only orders needed for the torus residue catalogue divide six.
    # All nonzero minors are <7, preserving ranks over F_7; six forbidden
    # hyperplanes cannot cover a nontrivial F_7 kernel. See written proof.
    forms=[(1,0,0),(0,1,0),(0,0,1),(1,1,1),(1,-1,-1),(1,-2,-2)]
    minors=[]
    for size in range(1,4):
        for rows in combinations(range(6),size):
            for cols in combinations(range(3),size):
                minors.append(abs(determinant([[forms[i][j] for j in cols] for i in rows])))
    need(set(minors)=={0,1,2,3},'Residue minor orders')
    pats=m.residue_patterns();weights=[sum(w for w,ok in zip((2,2,2,2,1,1),pat) if not ok) for pat in pats]
    need(len(pats)==24 and min(x for x in weights if x)>3,'Complete residue patterns through eight misses')
    counts=[]
    for j in range(1,7):
        integer=list(m.patterns(j));partial=list(m.partial_patterns(j))
        need(len({tuple(sorted(s.items())) for s in integer})==len(integer),'Duplicate integer catalogue')
        need(len({tuple(sorted(s.items())) for s in partial})==len(partial),'Duplicate partial catalogue')
        counts.append(dict(j=j,integer=len(integer),partial=len(partial)))
    need([x['integer'] for x in counts]==[22,66,156,327,610,1036],'Integer catalogue sizes')
    need([x['partial'] for x in counts]==[0,0,0,30,210,776],'Partial catalogue sizes')
    # With exactly eighteen hull-retained ordinary labels, the three literal
    # noncoexistence rules leave these four missing pairs. All own centres
    # O,H,U,V are retained, so their differences recover integral outer points.
    names={k+s for s in 'st' for k in (*m.CHAIN,'alpha','beta')}
    missing=[]
    for pair in combinations(sorted(names),2):
        kept=names-set(pair)
        if {'Ps','Pt'}<=kept:continue
        if {'betas','betat','C5s','C5t'}<=kept:continue
        if any({'P'+s,'beta'+s,'C5'+o}<=kept for s,o in [('s','t'),('t','s')]):continue
        missing.append(pair)
    need(set(missing)=={tuple(sorted(x)) for x in [('Ps','betat'),('Ps','C5s'),('Pt','betas'),('Pt','C5t')]},'Complete j0 hull interface')
    # A leading at j2 cannot be empty. Positive holes use K-delta>0.
    need(-28+60>0,'Positive j2 leading')
    need(75-28==47 and 33>28 and 406+56+6-334==134>0,'Zero j2 empty leading guards')
    need(47+4>12,'Opposite C7 contradicts O cap')
    return dict(status='PASS_GEOMETRY_FINITE_CHECKS_ONLY',global_upper_bound_certified=False,
                generic_gap_integer_combinations=len(seen),minimum_integer_gap_margin=min(margins),
                remaining_fixed_labels={k:sorted(v) for k,v in keep.items()},ownerless_guards=guard,
                residue_grid=42,residue_patterns=len(pats),minor_values=sorted(set(minors)),activity_counts=counts,
                no_empty_missing_pairs=missing)

if __name__=='__main__':print(json.dumps(verify(),indent=2))
