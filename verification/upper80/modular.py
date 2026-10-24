"""Exact modular obstructions for singleton target-cover components.

Only physically integral variables are admitted. Every extra equality has
both directions certified by the ordinary integer Farkas checker.
"""
from math import gcd
import model as m

INTEGER_NAMES={'ONE','rank_k','rank_I','hole_W','K','delta','Bs','Bt'}|{prefix+side for side in 'st' for prefix in ('t','x','R','M','S','a','b','c','e','X','g','h','d')}
# These are actual cardinalities or minima/maxima of finitely many integer
# truncation expressions. In a full integer pattern the physical assignment
# can use these exact integer witnesses, even though the LP relaxes them.
INTEGER_NAMES |= {'F','FD','TD','TD1','TD2','TD3','LS','LT','ells','ellt'}
INTEGER_NAMES |= {'GB'+str(i) for i in range(1,11)}
INTEGER_NAMES |= {name+side for side in 'st' for name in ('phicore','phisource',*('chi'+str(i) for i in range(1,11)))}
INTEGER_NAMES |= {prefix+name+side for prefix in ('D','l','u') for name in (*m.CHAIN,'alpha','beta') for side in 'st'}


def key(row):
    clean={k:v for k,v in row.items() if v};factor=gcd(*(abs(v) for v in clean.values())) or 1
    return tuple(sorted((k,v//factor) for k,v in clean.items())),factor


def extra_equalities(rows,eqs):
    unit=next(i for i,(row,b,_) in enumerate(eqs) if {k:v for k,v in row.items() if v}=={'ONE':1} and b==1)
    known=set()
    for row,b,_ in eqs:
        a=m.add((1,row),(-b,{'ONE':1}));k,_=key(a);known.add(k);known.add(tuple((x,-v) for x,v in k))
    facts={};extras=[]
    for i,(row,b,_) in enumerate(rows):
        a=m.add((1,row),(-b,{'ONE':1}));k,factor=key(a)
        if not k or not set(dict(k))<=INTEGER_NAMES:continue
        weights=[('r',i,1)]
        if b:weights.append(('e',unit,-b))
        facts.setdefault(k,dict(weights=weights,denominator=factor))
        if b==0 and all(v>=0 for v in row.values()):
            for name,c in row.items():
                if c<=0 or name not in INTEGER_NAMES:continue
                facts.setdefault(((name,1),),dict(weights=[('r',i,1)],denominator=c))
                facts.setdefault(((name,-1),),dict(weights=[],denominator=1))
    for k,certificate in facts.items():
        opposite=tuple((name,-v) for name,v in k)
        if k in known or opposite not in facts:continue
        extras.append(dict(row=dict(k),certificates=[certificate,facts[opposite]]));known.add(k);known.add(opposite)
    return extras


class Basis:
    def __init__(self,rows,eqs):
        self.base_count=len(eqs);self.extras=extra_equalities(rows,eqs)
        augmented=list(eqs)+[(entry['row'],0,'derived integer equality') for entry in self.extras]
        normalized=[];self.divisors={}
        for i,(row,b,_) in enumerate(augmented):
            if not set(k for k,v in row.items() if v)<=INTEGER_NAMES:continue
            divisor=gcd(*(abs(v) for v in row.values()),abs(b)) or 1
            normalized.append((i,{k:v//divisor for k,v in row.items() if v},b//divisor));self.divisors[i]=divisor
        self.bases=[]
        for modulus in (2,3,5,7,11,13):
            basis={};failure=None
            for i,row,rhs in normalized:
                row={k:v%modulus for k,v in row.items() if v%modulus};rhs%=modulus;weights={i:1}
                while row:
                    pivot=min(row);value=row[pivot]
                    if pivot not in basis:
                        inverse=pow(value,-1,modulus)
                        basis[pivot]=({k:v*inverse%modulus for k,v in row.items()},rhs*inverse%modulus,{k:v*inverse%modulus for k,v in weights.items() if v*inverse%modulus})
                        break
                    source,b,combination=basis[pivot]
                    row={k:(row.get(k,0)-value*source.get(k,0))%modulus for k in row.keys()|source.keys()};row={k:v for k,v in row.items() if v}
                    rhs=(rhs-value*b)%modulus
                    weights={k:(weights.get(k,0)-value*combination.get(k,0))%modulus for k in weights.keys()|combination.keys()};weights={k:v for k,v in weights.items() if v}
                else:
                    if rhs:failure=weights;break
            self.bases.append((modulus,basis,failure))

    def exclude(self,target):
        if not set(k for k,v in target.items() if v)<=INTEGER_NAMES:return None
        target_divisor=gcd(*(abs(v) for v in target.values())) or 1
        for modulus,basis,failure in self.bases:
            if failure is not None:weights=failure;target_weight=0;rhs=1;row={}
            else:
                row={k:(v//target_divisor)%modulus for k,v in target.items() if (v//target_divisor)%modulus};rhs=0;weights={};target_weight=1
                while row and min(row) in basis:
                    pivot=min(row);value=row[pivot];source,b,combination=basis[pivot]
                    row={k:(row.get(k,0)-value*source.get(k,0))%modulus for k in row.keys()|source.keys()};row={k:v for k,v in row.items() if v}
                    rhs=(rhs-value*b)%modulus
                    weights={k:(weights.get(k,0)-value*combination.get(k,0))%modulus for k in weights.keys()|combination.keys()};weights={k:v for k,v in weights.items() if v}
            if row or not rhs:continue
            used=sorted(i-self.base_count for i in weights if i>=self.base_count)
            remap={old:self.base_count+j for j,old in enumerate(used)}
            return dict(modulus=modulus,target_divisor=target_divisor,target_weight=target_weight,
                        equations=[[i if i<self.base_count else remap[i-self.base_count],self.divisors[i],weight] for i,weight in sorted(weights.items())],
                        extras=[self.extras[i] for i in used])
        return None


def check(certificate,rows,eqs,target):
    import exact
    modulus=certificate['modulus'];m.need(type(modulus) is int and modulus>=2,'Modular certificate modulus')
    augmented=list(eqs)
    for entry in certificate.get('extras',[]):
        row=entry['row'];m.need(set(row)<=INTEGER_NAMES and all(type(v) is int for v in row.values()) and len(entry['certificates'])==2,'Derived integer equality scope')
        for guard,cert in zip((row,{k:-v for k,v in row.items()}),entry['certificates']):exact.check(cert,rows,eqs,guard,strict=False)
        augmented.append((row,0,'derived integer equality'))
    combined={};rhs=0;seen=set()
    def add(row,b,divisor,weight):
        nonlocal rhs
        m.need(type(divisor) is int and divisor>0 and type(weight) is int and all(type(v) is int and v%divisor==0 for v in row.values()) and b%divisor==0,'Exact modular normalization')
        m.need(set(k for k,v in row.items() if v)<=INTEGER_NAMES,'Modular variable must be physically integral')
        for k,v in row.items():combined[k]=combined.get(k,0)+weight*(v//divisor)
        rhs+=weight*(b//divisor)
    for index,divisor,weight in certificate['equations']:
        m.need(type(index) is int and 0<=index<len(augmented) and index not in seen and weight!=0,'Modular equality index');seen.add(index)
        row,b,_=augmented[index];add(row,b,divisor,weight)
    add(target,0,certificate['target_divisor'],certificate['target_weight'])
    m.need(all(v%modulus==0 for v in combined.values()) and rhs%modulus!=0,'No exact modular contradiction')
    return True
