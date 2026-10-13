#!/usr/bin/env python3
"""Exact arithmetic for fresh SIZE85 inverse alignment and overlap repairs.
No historical SIZE86 witnesses, row receipts, optimizer or external packages.
The written proof licenses the inequalities; this checks the finite parameters.
"""
from fractions import Fraction
T=lambda r:r*(r+1)//2
def n(r):
    return r-5 if r>=21 else (r-14 if r>=14 else -1)
def effective(r,beta,C):
    K=3
    while (K+1)*(K-2)//2<=C+1:K+=1
    D=C+max(3,K);M=2*beta
    while T(M)-6*beta<=M+D+2:M+=1
    J=max(K+1,2*beta+5,M)
    margins=((r-J+1)*beta-D,T(J-1)-1-D)
    assert min(margins)>0
    return (K,D,M,J,*margins)
def oldrho(r,mu):
    values=[n(r),mu+2-2*r]
    for g in range(2,11):
        q,s=divmod(max(0,mu-4*g+2),g+1)
        values.append(min((g-1)*(r-14),(g-1)*q+min(s,g-1)))
    return max(values)
def row(k):
    a,b=34-k,34+k;I=k*k;O=600-I;rp,rq=n(a),n(b)
    assert a+b==68 and 1+T(a)+T(b)==1191+I
    assert O==22*77+97-(1191+I)
    return dict(k=k,a=a,b=b,I=I,O=O,rp=rp,rq=rq,
        R=O-T(a)+2-(a-3)-rp,Kmax=O-rp-rq,
        Umax=O-rp-rq+3,Vmin=T(b)+b-2,Umin=T(a)+a-2,
        F=(a-3)+rp+rq-(O-T(a)+2))
# Entries (beta, starting prefix q). q14 uses rho14>=0; q20/q21
# additionally use the proved last-AP argument and nonAP prefix floors.
INVERSE={3:(3,14),4:(4,14),5:(6,14),6:(6,14),7:(7,14),
    8:(8,14),9:(8,14),10:(8,20),11:(8,14),12:(8,14),
    13:(7,21),14:(7,21),15:(7,14),16:(7,14),17:(6,14),
    18:(5,14),19:(5,14),20:(4,14)}
OVERLAP={0:5,1:7,2:8,3:8,4:9,5:9,6:9,7:8,8:8,9:7,10:6,11:5,12:4}
def endpoint(b,R,beta,q):
    assert beta>=3 and q in (14,20,21)
    if q==14:
        startfloor=0;j=b-R//(beta-1)
    else:
        assert T(q)-b-1>R
        startfloor=n(q)
        # rho_j>=j-5 and the beta-1 later increments give this index.
        j=max(q+1,21,((beta-1)*b-R-5+beta-3)//(beta-2))
    margins=(startfloor+(beta-1)*(b-q)-R,j-(2*beta+5),
        T(j)-b-1-R,T(j)-6*beta-j-R-3)
    assert margins[0]>0 and margins[1]>=0 and min(margins[2:])>0
    assert j<=b and j>=15 and j>2*beta
    for size in range(j,b):assert T(size)-6*beta>size+R+3
    return j,margins
def verify():
    rows=[row(k) for k in range(22)]
    assert [x['k'] for x in rows if x['F']<=0]==list(range(3,22))
    # The larger-side strict inverse threshold uses both nonAP floors.
    # The stronger but unnecessary Omega<T_b-1 test fails at k0.
    for x in rows:assert x['Kmax']<x['Vmin']-2
    print('k a b Omega R beta q j zcap D1upper nonprimitive_c_cap')
    primitive_caps=[]
    for k,(beta,q) in INVERSE.items():
        x=row(k);j,_=endpoint(x['b'],x['R'],beta,q)
        H=2*beta;alpha=4*beta+2
        margins=(x['Vmin']-1-x['Kmax'],
            x['Vmin']-x['Kmax']-2*alpha-1,
            x['Vmin']-x['Kmax']-alpha-2,x['Umin']-H-2)
        assert min(margins)>0
        d1=-165-2*x['I']+2*H+(16 if k==20 else 0)
        assert d1<0
        cap=x['O']-x['rp']-x['rq']-T(x['a'])-x['a']+1-144+3*H
        assert cap<77 and 4*H<=104
        primitive_caps.append(cap)
        print(k,x['a'],x['b'],x['O'],x['R'],beta,q,j,H,d1,cap)
    assert max(primitive_caps)==28
    # Separate a13 failed-inverse boundary, using its sharper rho13 floor.
    x=row(21);pars=effective(55,2,52)
    assert x['R']==61 and oldrho(55,108)==62
    H=4
    assert min(x['Vmin']-1-x['Kmax'],
        x['Vmin']-x['Umax']-x['Kmax']+1,
        x['Vmin']-x['Kmax']-H-2,x['Umin']-H-2)>0
    assert -165-2*x['I']+2*H+16<0
    assert -1+50+144-2*H>159
    print('a13 effective',pars,'excluded after G144')
    # The complementary actual sufficient inverse branch has primitive
    # sides, pre-G strict D1, and post-G z>=17. Its higher-hole witness
    # is independent of the failed-inverse witness above.
    assert x['Kmax']==110
    assert -165-2*x['I']+2*x['Kmax']+16<0
    assert -1+50+144-2*16>159
    pars=effective(55,4,119)
    assert pars==(17,136,19,19,12,34)
    assert oldrho(55,175)==113
    assert -1+113+48>159
    print('a13 strict effective',pars,'excluded after G144')
    # Outer integralization and overlap comparison.
    assert 1191>4*77-10+600
    # Unrepaired strict-inverse branches: D1 is strict for z<=82+I.
    for k in range(16,20):
        x=row(k);assert 83+x['I']+x['rp']+x['rq']>x['O']
    count=0;repaired=0
    print('Large-hole final-support overlap: k side Z base-margin endpoint-beta j')
    for k in range(16):
        x=row(k);Z=83+x['I']
        for side,r,s in [('P',x['a'],x['b']),('Q',x['b'],x['a'])]:
            cost=T(r-2)+2-2*r
            base=cost+n(s)+Z-x['O']
            beta=j=None
            if base<=0:
                assert side=='P' or k==0
                beta=OVERLAP[k];R=x['O']-cost-Z
                j,_=endpoint(s,R,beta,20)
                assert 2*beta<Z
                repaired+=1
            count+=1;print(k,side,Z,base,beta,j)
    assert count==32 and repaired==14
    # Separate a14 strict-inverse closure. Every z>=13 costs rhoQ>=153;
    # z<=12 gives c<=31<d and w<=48 for the common j0 obstruction.
    pars=effective(54,6,168)
    assert oldrho(54,223)==153
    assert 153+48>200
    assert 200-49-(144-24)==31<77
    # Its failed-inverse branch has H8 and cap c23<d.
    assert 200-49-(144-16)==23<77
    print('a14 effective',pars,'both strict and repaired branches excluded by j0')
    print('PASS: 18 endpoint inverse rows, both a13 effective boundaries, 32 overlap alternatives, 14 endpoint overlap repairs, and a14 closure.')
if __name__=='__main__':verify()
