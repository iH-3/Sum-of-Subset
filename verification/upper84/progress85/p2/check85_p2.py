#!/usr/bin/env python3
"""Fresh exact SIZE85 P2 arithmetic. No optimizer or activity census."""
from fractions import Fraction
T=lambda r:r*(r+1)//2
n=lambda r:r-5 if r>=21 else r-14
def core(r,low,f):
    return sorted(low+[f+1+i for i in range(r-len(low))])
def verify():
    # Initial cardinality range, with the correct low-side defect floors.
    for a in (15,16,17):
        b=68-a;I=(a-34)**2
        assert 302-I-n(a)-n(b)+28<0
    assert min(n(r)+n(68-r) for r in range(18,51))==49
    assert min(T(r)+(r-34)**2 for r in range(18,51))==397
    assert 1190+62-236-56==960
    assert (1168+56+28)//2==626
    assert 456+56-8-2*19==466
    assert 960>max(626,466)
    assert -26+62+49+2*14-2*56==1
    print('Localization: width >=960; inner gaps <=626 or466; outer margin >=1.')
    # Activity bound after localization; delta is nonnegative and helps.
    act=[T(r)+7*r+2*(r-34)**2-594-28 for r in range(18,51)]
    assert min(act)==39
    assert 397-384==13
    assert 16-14+62>0
    print('Activity: upper-strip subtraction margin >=39, first-gap margin >=13.')
    # Two cap predicates would violate the structural source budget.
    for z in range(2,15,2):
        for w in range(2,z+1,2):
            assert 4*(62+2*z)>42+6*w
    # First-gap rank lower bound. The low count is <=26.
    assert Fraction(27*29,4)>190
    for k in range(5,27):
        value=Fraction(-k**3+68*k*k-4*k+272,4)
        assert value>=Fraction(1827,4)>312
    for k in range(5):
        value=69*7-1-Fraction(83*k,2)+Fraction(k*k,4)
        assert value>=320>312
    # All profile distributions up to reflection, generated as real sets.
    profiles=[(1,[],[]),(2,[1],[]),(3,[1],[1]),
        (4,[1],[2]),(4,[1,2],[]),(5,[1,2],[1]),
        (6,[1,3],[1]),(6,[1,2],[2])]
    expected={1:(68,70),2:(101,71),3:(132,72),
        4:(199,74),5:(228,75),6:(294,77)}
    totals=[]
    rooted_min=[];twoedge_min=[]
    for f,ls,lo in profiles:
        massmin=None;amin=None;bs=set();rmins=[];twomin=[]
        for r in range(18,51):
            q=68-r;P,Q=core(r,ls,f),core(q,lo,f)
            assert len(P)==r and len(Q)==q and len(set(P))==r and len(set(Q))==q
            b=sum(P)+sum(Q)-T(r)-T(q);I=(r-34)**2;B=max(P)+max(Q)
            amin=I+b if amin is None else min(amin,I+b)
            massmin=b if massmin is None else min(massmin,b)
            bs.add(B)
            rmins.append(101-14+I+b-2*B)
            for rv in (r,q):twomin.append(-18-14+I+b-B+2*rv)
        assert amin==expected[f][0] and bs=={expected[f][1]}
        if f>=2:assert massmin>=85 and min(rmins)>29
        assert min(twomin)>17
        totals.append((f,ls,lo,amin,next(iter(bs)),massmin,min(rmins),min(twomin)))
        if f>=2:rooted_min.append(min(rmins))
        twoedge_min.append(min(twomin))
    assert min(rooted_min)==46 and min(twoedge_min)==33
    for row in totals:print('profile',row)
    # Native losses if C7 is HIGH.
    assert min((r-34)**2+4*r for r in range(18,51))==132
    assert min((r-34)**2+5*r for r in range(18,51))==164
    assert 132+96+85==313>312
    assert 28-16+1==13 and sum(range(2,14))==90 and 40+1+16==57
    assert 57<90-3
    assert 164>129+2
    equality=[]
    for r in range(28,37):
        for sigma in range(17):
            if (r-34)**2+4*r+sigma<=130+2:equality.append((r,sigma))
    assert equality==[(32,0)]
    I=4;delta=4*32+100;A=I+68+delta
    assert delta==228 and A==300
    m0=154-280-2;sourceT=m0+A
    assert sourceT==172 and 332-sourceT==160
    U,J=6,154
    assert U+J==160 and sourceT+U==178>J+2+2*(5+5)==176
    print('C7 equality is impossible: fringe178>176.')
    # At first-gap1, simultaneous beta/O would force tiny total deviation.
    survivors=[]
    for r in range(18,51):
        I=(r-34)**2
        for w in range(2,15,2):
            for sigma in range(245):
                if 4*I+sigma<=5*w-62:survivors.append((r,w,sigma))
    assert survivors and all(w==14 and sigma<=8 and (r-34)**2<=2 for r,w,sigma in survivors)
    assert 33-8+1>=13 and 35+1+8<=57
    assert 4*0+0>5*2-62
    # Trim-six: 57 actual points, baseline span58, overlap55.
    assert 2*57-58-1==55 and 6*55==330
    assert 298-68==230
    assert 330-20-230==80>Fraction(3*14,2)==21
    print('Terminal contradiction80<=3w/2<=21 is impossible.')
    print('PASS: fresh SIZE85 P2 localization, profiles, activity and terminal arithmetic.')
if __name__=='__main__':verify()
