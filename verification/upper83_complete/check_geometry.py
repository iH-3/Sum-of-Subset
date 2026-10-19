"""Literal affine identities, ledgers and exhaustive component dispatch.
The listed geometric activity implications are hypotheses proved in the report.
"""
from collections import Counter
import importlib.util
from pathlib import Path
from itertools import combinations
ROOT=Path(__file__).resolve().parents[2]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

g=load('activity_base83','verification/upper85_geometry.py')
need=g.need

def identities():
    Z=g.centers();add=g.add;lin=g.lin;n=0
    for s,t in [('s','t'),('t','s')]:
        a=lin(**{'M'+s:1,'X'+s:1});b=lin(**{'M'+t:1,'X'+t:1})
        ds=lin(**{'d'+s:1});dt=lin(**{'d'+t:1});gs=lin(**{'g'+s:1});G=lin(gs=1,gt=1)
        expressions=[
            (Z['H'+s],add((1,Z['P'+s]),(2,Z['alpha'+s]),(1,Z['alpha'+t]),(1,Z['C5'+t]),(4,a),(4,b),(2,G))),
            (Z['V'+t],add((2,ds),(1,Z['beta'+s]),(1,Z['P'+t]),(2,a),(1,b),(1,gs))),
            (Z['U'+s],add((1,Z['P'+s]),(1,Z['alpha'+t]),(1,Z['C6'+t]),(2,a),(4,b),(2,G))),
            (add((1,Z['alpha'+s]),(1,Z['C5'+t])),add((1,dt),(-2,a),(-2,b),(-1,G))),
            (add((1,Z['alpha'+s]),(1,Z['H'+t]),(-2,Z['beta'+s]),(-1,Z['alpha'+t]),(-1,Z['C5'+t])),add((2,ds),(2,a),(2,b),(1,G))),
            (add((1,Z['alpha'+s]),(1,Z['V'+t]),(-2,Z['alpha'+t]),(-2,Z['C5'+s]),(-2,Z['beta'+s]),(-1,Z['C5'+t])),add((6,a),(5,b),(3,gs),(2,lin(**{'g'+t:1})))),
            (add((1,Z['alpha'+s]),(1,Z['H'+t]),(-2,Z['beta'+s]),(-1,Z['C5'+t]),(-2,Z['C5'+s])),add((6,a),(3,b),(3,G),(3,lin(**{'h'+t:1})))),
            (add((1,Z['alpha'+s]),(-1,Z['P'+s])),add((1,Z['beta'+s]),(1,Z['beta'+t]),(2,dt),(2,a),(2,b),(1,G))),
        ]
        for left,right in expressions:need(left==right,'physical endpoint identity '+str(n));n+=1
    return n

def ledgers():
    p=load('fixed_base83','verification/upper83_progress.py')
    labels,gaps,groups=p.fixed_catalogue()
    # P5 A1 empty-P: all choices of the last hole share these labels.
    high={f'C{v}{i}{j}' for v in '+-' for i,j in [(1,1),(1,2),(1,3),(1,4)]}
    high|={f'C+{i}{j}' for i,j in [(2,2),(2,3),(2,4)]}
    low={f'C{v}5{i}' for v in '+-' for i in range(5,9)}
    low|={f'V-{i}' for i in range(5,9)}|{f'F{v}{i}' for v in '+-' for i in range(3,6)}
    need(high|low<=set(labels),'actual P5 labels')
    need(not high&low and not any(high&set(row) for row in groups),'HIGH independent of baseline')
    touched=sum(bool(low&set(row)) for row in groups)
    need((len(high),len(low),touched)==(11,18,17),'P5 exact credit12')
    # Ownerless initial32 LOW labels occupy25 groups; three reflected pairs
    # each add a witness in an already occupied group, and C25 is untouched.
    low0={f'C{v}5{i}' for v in '+-' for i in range(5,9)}
    low0|={f'V{v}{i}' for v in '+-' for i in range(3,9)}
    low0|={f'U{v}{i}' for v in '+-' for i in range(5,8)}
    low0|={f'F{v}{i}' for v in '+-' for i in range(3,6)}
    need(len(low0)==32 and sum(bool(low0&set(row)) for row in groups)==25,'ownerless baseline')
    for label in ('V{}2','C{}35','C{}45'):
        for sign in '+-':
            x=label.format(sign);need(x not in low0,'new witness')
            need(any(x in row and low0&set(row) for row in groups),'already touched witness group')
    need(8+32+3+1-26==18,'ownerless credit18')
    return dict(P5_empty_P_credit=12,ownerless_credit=18)

def z5_dispatch():
    names=g.NAMES;B=g.BITS;allmask=g.ALL;pair1=g.PAIR1;counts=Counter()
    def a(mask,x):return bool(mask&B[x])
    def owner(mask,p):
        hits=[s for s in ('s','t') if a(mask,p+s)]
        return hits[0] if len(hits)==1 else None
    for branch in ('A','B'):
        pair2=B['betas']|B['betat'] if branch=='A' else B['C5s']|B['C5t']
        singles=allmask^(pair1|pair2)
        for mask in range(1<<20):
            if 16-(mask&singles).bit_count()+int(not(mask&pair1))+int(not(mask&pair2))!=5:continue
            if a(mask,'Os') or a(mask,'Ot'):continue
            if a(mask,'Ps') and a(mask,'Pt'):continue
            if all(a(mask,k) for k in ('betas','betat','C5s','C5t')):continue
            if any(all(a(mask,k+s) for k in ('beta','H')) for s in ('s','t')):continue
            if any(all(a(mask,k) for k in ('P'+s,'beta'+s,'C5'+t)) for s,t in [('s','t'),('t','s')]):continue
            if branch=='B' and (a(mask,'C5s') and a(mask,'C5t') or any(a(mask,'P'+s) and a(mask,'C5'+t) for s,t in [('s','t'),('t','s')])):continue
            if any(a(mask,x+s) and not a(mask,y+s) for s in ('s','t') for x,y in [('P','C5'),('C5','C6'),('C6','C7'),('H','U'),('U','V')]):continue
            if any(a(mask,'beta'+s) and not a(mask,'U'+s) and a(mask,'alpha'+s) for s in ('s','t')):continue
            # The last implication is HIGH U => alpha HIGH if beta active.
            paired={'P','beta' if branch=='A' else 'C5'}
            holes={x+s for s in ('s','t') for x in names if x not in paired and not a(mask,x+s)}
            for x in paired:
                if not(a(mask,x+'s') or a(mask,x+'t')):holes.add(x)
            p=owner(mask,'P');bs=[s for s in ('s','t') if a(mask,'beta'+s)]
            if branch=='A' and not bs:counts['A0']+=1;continue
            card=None
            if branch=='A' and len(bs)==2:
                if p and holes=={'Os','Ot','Hs','Ht','C5'+('t' if p=='s' else 's')}:card='split_beta'
            elif branch=='A':
                s=bs[0];t='t' if s=='s' else 's'
                if p is None:
                    extra=holes-{'Os','Ot','H'+s,'P'}
                    if len(extra)==1 and extra<={'alpha'+s,'H'+t,'alpha'+t,'C5'+s,'C5'+t,'U'+s}:card='empty_P'
                elif p==t:card='opposite'
                elif a(mask,'alpha'+s):card='same'
                elif holes=={'Os','Ot','H'+s,'alpha'+s,'C5'+t}:card='four'
            else:
                s=owner(mask,'C5');t='t' if s=='s' else 's'
                if s and (p is None or p==s):
                    if a(mask,'alpha'+s):card='branch_B'
                    elif p==s and a(mask,'alpha'+t) and all(a(mask,x+v) for v in ('s','t') for x in ('U','V','C6','C7')):card='four_B'
            need(card is not None,'uncovered Z5 configuration '+str((branch,holes,p,bs)))
            counts[card]+=1
    need(dict(counts)=={'A0':32,'same':6,'empty_P':10,'opposite':18,'four':2,'split_beta':2,'branch_B':32,'four_B':8},'complete Z5 inventory')
    return dict(assignments=2*(1<<20),counts=dict(counts))

def verify():
    return dict(status='PASS',identities=identities(),ledgers=ledgers(),retained_dispatch=g.activity(),Z5=z5_dispatch(),pointwise_forests=g.forest_points())

if __name__=='__main__':
    import json
    print(json.dumps(verify(),indent=2,default=str))
