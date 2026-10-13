#!/usr/bin/env python3
"""Exact arithmetic certificates for fresh P4 cards.

This checks the arithmetic following the explicitly proved resource
and endpoint inequalities; it does not substitute for their proofs.
"""
from fractions import Fraction as F

def min_integer_quad(a,b,c):
    v=-b/(2*a);p=v.numerator//v.denominator
    return min((a*r*r+b*r+c,r) for r in (p,p+1))

def run():
    # Exact omitted-singleton profile minima used to license the seeds.
    assert min(214-2*u-2*v for u in range(2,7) for v in range(u+1,7))==192
    for q in (3,4,5):
        value,r=min_integer_quad(F(1),F(-69),F(1364-2*q))
        assert value==174-2*q and value>=164
    assert min(206-2*q for q in (4,5,6))==194
    value,r=min_integer_quad(F(1),F(-67),F(1289))
    assert value==167  # missing4 profile plus one missing2 occurrence
    print('PASS exact profile minima licensing the seven source seeds')

    seeds=[((3,4,5,6),(1,2),43),((2,4,5,6),(1,3),41),
           ((2,3,5,6),(1,4),39),((2,3,4,5),(1,),34),
           ((2,3,4,6),(1,),34),((1,3,4,5),(2,),37),
           ((1,1,4,5,6),(3,),39)]
    for B,H,L9 in seeds:
        bits=1
        for x in B:bits|=bits<<x
        total=sum(B);holes=set(H)|{total-h for h in H}
        for x in range(total+1):assert bool((bits>>x)&1)==(x not in holes)
        h=max(H)
        assert total+60*(total-2*h)+870>1348
        assert L9+36*(L9-2*h)+306>1348
    print('PASS seven source seeds and both propagation failure bounds')

    rows=[['Cs25','Ct25'],['Cs48','Fs3'],['Cs58','Ct58'],
          ['Cs77','Fs4'],['Us6','Ut6'],['Vs6','Vt6'],
          ['Cs15','Fs1','Ct55'],['Cs26','Ct57','Vt4'],
          ['Cs35','Vs3','Ct46'],['Cs36','Us4','Ut5'],
          ['Cs44','Us8','Fs5'],['Cs45','Vs8','Ct67'],
          ['Cs47','Vs7','Fs2'],['Cs56','Vs2','Ct66'],
          ['Cs68','Us3','Vt5']]
    starred={1,3,6,7,8,9,10,11,12,13,14};groups=[]
    for i,row in enumerate(rows):
        groups.append(set(row))
        if i in starred:
            groups.append({x.replace('s','@').replace('t','s').replace('@','t') for x in row})
    assert len(groups)==26
    low={f'F{v}{i}' for v in 'st' for i in (3,4,5)}
    low|={f'Vt{i}' for i in range(5,9)}
    low|={f'C{v}{ij}' for v in 'st' for ij in ('55','56','57','58')}
    low|={'Vt3','Vt4'}
    high={f'C{v}{ij}' for v in 'st' for ij in ('11','12','13','14')}
    high|={'Cs22','Cs23','Cs24'}
    assert len(low)==20 and len(high)==11 and not low&high
    assert sum(bool(g&low) for g in groups)==18
    assert all(not (g&high) for g in groups)
    assert len(high)+len(low)-18==13
    print('PASS T5 exact fixed-label incidence credit13')

    # These are global minima over all integers, not samples of side sizes.
    cases=[('opposite',F(6),F(-737,2),F(6358),F(1401,2)),
           ('same',F(29,8),F(-207),F(7225,2),F(5265,8)),
           ('m2cross_t',F(17,2),F(-1091,2),F(9248),F(496)),
           ('m2cross_s',F(17,2),F(-1061,2),F(9248),F(971))]
    for name,a,b,c,expected in cases:
        value,r=min_integer_quad(a,b,c)
        assert value==expected,(name,value,expected)
        print('PASS quadratic',name,value,r)

    # Owner cards retain the actual additional credit8.
    assert F(1401,2)+F(13,2)*8-1 > 553
    assert F(5265,8)+F(7,2)*8 > F(1355,2)
    assert F(5265,8)+F(7,2)*8-1 > F(5419,8)
    assert 496+5*9 > 537
    assert 971+5*9 > 1012

    # T5 uses a positive scalar combination of actual overlap floors.
    for eta,constant,target in [(0,F(793),F(930)),(1,F(1575,2),F(924))]:
        weights=(F(13,2),F(11,2))
        assert sum(weights)==12
        assert weights[0]*67+weights[1]*(65-eta)==constant
        # xi >= eta; after adding 2R=140+2xi the left is
        # 140+constant+xi, with nonnegative I contribution.
        assert 140+constant+eta > target
        print('PASS T5',eta,'gap',140+constant+eta-target)

    # A0 empty-pair1 weighted bounds cancel both sigma and xi.
    weights=(5,1,8)
    assert sum(weights)==14
    assert -weights[0]+weights[1]+F(weights[2],2)==0
    assert -weights[1]-F(weights[2],2)==-5
    assert weights[0]*67+weights[1]*65+weights[2]*63==904
    assert weights[0]*66+weights[1]*64+weights[2]*62==890
    assert 904>891
    # I-h >= -34, but the necessary row requires 890+5I<=556+5h.
    assert 890-556+5*(-34)>0

    # A0 case3: tau>=68, I,delta>=0.
    assert -273+6*68>0
    print('PASS all fresh P4 arithmetic cards')

if __name__=='__main__':run()
