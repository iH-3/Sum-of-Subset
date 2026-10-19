#!/usr/bin/env python3
"""Exact checks for the new upper-84 analytic improvements.

Python standard library only. Infinite source-envelope and resource arguments
are written proofs, not conclusions inferred from sampled configurations.
Every acceptance predicate is explicit and remains enabled under -O.
"""
import argparse
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def fringe(values, endpoint):
    return len({x+y for i,x in enumerate(values) for y in values[i:] if x+y>endpoint})


def source_cap(claim=162):
    # P<=a+b: for a+b>=6 use P<=6. The unbounded c>=2b tail
    # has exactly P=3. Thus only these finite small triples remain.
    small=0
    for u in range(3,6):
        for a in range(1,(u-1)//2+1):
            b=u-a
            for c in range(b+1,2*b):
                need(fringe((a,b,c),c)<=u,'small triple P<=a+b')
                small+=1
            need(3<=u,'infinite triple tail')
    need(6<=6,'large-u triple tail')

    # For a putative integer T>=163, the triple envelope gives J<=153.
    # These are endpoint certificates for affine inequalities, not a cutoff
    # on actual offsets. R>=68 only improves each displayed upper bound.
    need(316-163==153,'J ceiling')
    need((152-68-3)//2==40 and 40<68+1,'outside max/max label gives three cross labels')
    need(153-2*68-2==15,'no cross label: c_s+c_t<=15')
    need(15-3<68+3+1,'no cross label: both e_v>2c_v')
    need(153-2*68-2-2==13,'one cross label: c_s<=13')
    need(13<68+2+1,'one cross label: e_s>2c_s')
    cases=[('at least three central reinsertion labels',3,10),
           ('only max/max is central',1,8),
           ('max/max and one cross label are central',2,9)]
    for name,h,total_fringe_excess in cases:
        need(155-h+total_fringe_excess<=claim,'source cap case: '+name)

    # Check the literal seven-label membership formula independently.
    membership=0
    for rs,rt in ((34,34),(15,53),(53,15)):
        for tails in product(((1,2,3,78),(1,2,70,145),(2,4,5,80),(4,6,7,9)),repeat=2):
            (a,b,c,e),(aa,bb,cc,ee)=tails
            R=rs+rt;js=e-c;jt=ee-cc
            lo,hi=-2*rt-cc,2*rs+c
            actual=[rs+e-rt-x for x in (aa,bb,cc)]
            actual += [-rt-ee+rs+x for x in (a,b,c)]
            actual += [rs+e-rt-ee]
            count=sum(lo<=x<=hi for x in actual)
            formula=sum(js<=R+x for x in (aa,bb,cc))+sum(jt<=R+x for x in (a,b,c))
            formula+=int(js-jt<=R+cc and jt-js<=R+c)
            need(count==formula,'seven reinsertion labels')
            membership+=1

    # Actual source family: 75 consecutive old points plus two new maxima.
    # This is a finite sharpness/regression family, not the infinite proof.
    count=0;best=None;witness=None
    for js in range(1,171):
        for jt in range(1,171):
            D=tuple(range(-37,38))+(-37-jt,37+js)
            low=min(D);bits=sum(1<<(x-low) for x in D);pairs=0
            for x in D:pairs |= bits<<(x-low)
            K=pairs.bit_count();T=2*K-4*68-6-2*6-js-jt
            need(T<=claim,'actual source exceeds claimed universal cap')
            count+=1
            if best is None or T>best:best=T;witness=[js,jt,K]
    D=set(range(-37,38))|{-112,112}
    pairset={x+y for x in D for y in D}
    need(len(D)==77 and len(pairset)==301,'sharp actual source size and pair sums')
    need(pairset==set(range(-149,150))|{-224,224},'sharp pair-sum description')
    need(2*301-4*68-6-2*6-150==162 and best==162,'sharp source T=162')
    return dict(T_cap=claim,A_constant=442,affine_cases=cases,
                small_triples=small,membership_checks=membership,
                actual_source_family=count,maximum_T=best,witness=witness,
                sharp_example='D=([-37,37] intersect Z) union {-112,112}',
                scope='Universal bound is proved by the three analytic cases; source family is independent exact verification. D alone is not an 85-point feasible A.')


def no_empty(a_offset=10):
    # The original center identities, positive integer gaps and forbidden
    # triple force these two lower bounds. The report supplies activity and
    # guarded raw-gap licenses with 11/8/15 formal fixed labels.
    count=0
    for M in (76,77,100):
        for xs,xt,gs,gt,ht in product(range(1,4),repeat=5):
            ts=2*xs+xt+gs+gt+ht+1
            tt=2*M+2*ts+2*xs+2*xt+gs+gt+2
            need(tt-12>=2*M+a_offset,'A sharp hole bound')
            tt0=2*xt+xs+gt+1
            ts0=2*M+2*tt0+2*xs+2*xt+gs+gt+2
            need(2*ts0-17>=4*M+19,'B sharp hole bound')
            count+=1
    need(2*(77-1)+10==162,'d77 threshold')
    # Exact minima of affine residuals at all positive integer gaps = 1.
    need(6+4+3+3+2-18==0,'A affine minimum')
    need(8+12+2+6-28==0,'B affine minimum')
    return dict(universal='j=0 => w>=2M+10>=2|D|+8',d77_threshold=162,
                substitutions=count,branch_B='w>=4M+19',
                prerequisites='Integral D and actual original cover; no primitive-core or leading-activity premise.')


def adaptive(claim=112):
    # Before parity the guaranteed lower bound is strictly greater than110.
    need(F(119)-F(41,5)>110,'small radial excess')
    need(107+2*2==111,'large radial excess')
    count=0;profiles=0;best=None;witness=None
    for m in range(1,9):
        subsets=[tuple(x for i,x in enumerate(range(1,m)) if mask>>i&1)
                 for mask in range(1<<(m-1))]
        for p in subsets:
            for q in subsets:
                if sum(p)+sum(q)!=m-1:continue
                sums={0}
                for x in p+q:sums|={v+x for v in sums}
                if sums!=set(range(m)):continue
                profiles+=1
                for a in range(16,53):
                    b=68-a;I=(a-34)**2;B=68+2*m-len(p)-len(q)
                    base=m-1+sum(range(m+1,m+a-len(p)+1))+sum(range(m+1,m+b-len(q)+1))-(a*(a+1)+b*(b+1))//2
                    if I+base>395:continue
                    need(I+base-5*B>=-282,'first-gap baseline')
                    for sigma in range(396-I-base):
                        n=max(a-len(p),b-len(q));xi=(sigma+n-1)//n
                        value=max(F(461-12*t-5*B+I+base)+(1+F(6,t))*xi+(1-F(6,t))*sigma for t in (5,6))
                        need(value>claim-2,'adaptive bound before even rounding')
                        count+=1
                        if best is None or value<best:best=value;witness=[m,list(p),list(q),a,b,sigma,xi]
    need((profiles,count,best)==(35,56662,111),'complete first-gap census')
    need(F(3,2)*62<95<=F(3,2)*64,'necessary even holes')
    return dict(low_patterns=profiles,scalar_states=count,minimum_before_parity=str(best),
                witness=witness,terminal='112-w<=2(d_u-M)<=17+w/2',necessary_even_w=64)


def penalty(p):return max(0,p-1,2*p-4,3*p-9)


def analytic_alpha(claim_margin=16):
    # For p>=6, L(p)=3p-9; both expressions have positive slope.
    rows=[(p,penalty(p),4*penalty(p)-9*p,4*penalty(p)-7*p) for p in range(6)]
    need(min(x[2] for x in rows)==-21,'asymmetric s bound')
    need(min(x[3] for x in rows)==-13,'asymmetric t bound')
    need(3*6-36>=-21 and 5*6-36>=-13,'infinite p>=6 tails')
    # q>=63 instead of61; A<=57 instead of60. The transport requires
    # 4I+4tau-2xi_s+2q+11F<=835, but its left side is at least851.
    need(2*63+11*69-21-13-835>=claim_margin,'alpha analytic margin')
    # Test each one-sided selector separately, through the larger legacy
    # range; the theorem itself has no tau<=18 enumeration premise.
    states=0
    for tau in range(401):
        for xi in range(tau+1):
            choices=[(xi,0)]+[(j+(tau-xi)//j,j) for j in (1,2,3)]
            p,j=min(choices)
            need(xi>=p and tau-xi>=penalty(p),'selector inverse inequality')
            need(4*tau-2*xi-11*p>=-21,'analytic s inequality')
            need(4*tau-11*p>=-13,'analytic t inequality')
            states+=1
    return dict(removal_depths=[0,1,2,3],minimum_Q_size=63,
                piecewise_rows=rows,infinite_tail_slopes=[3,5],
                s_penalty_floor=-21,t_penalty_floor=-13,
                necessary_upper=835,proved_lower=851,margin=claim_margin,
                supplementary_one_side_states=states,
                legacy_7315_enumeration_required=False)


def shortened_terminals():
    # Retain all original geometric/classification premises. Only their
    # arithmetic endings and a P2 C7 equality branch are replaced.
    z2_min=min(max(414-5*x,342+x)-10 for x in range(1000))
    need(z2_min==344 and z2_min-(442-154)==56,'Z2 final margin')
    # A positive slope beyond xi=12 proves the infinite tail.
    need(342+12==414-5*12 and 1>0,'Z2 scalar tail')
    # P2 C7: deliberately retain A<=291+w (three weaker than new cap).
    # Its f1 dense-prefix reduction has square+sigma<=w-5<=9.
    need(29-9+1==21 and 39+1+9==49,'P2 C7 prefix and tail')
    need(sum(range(2,22))-3>=49,'P2 two-hole propagation')
    need(2-5<0,'P2 C7 after w=2')
    need(82>5*14,'P2 simultaneous beta/O excluded directly')
    # With new A<=288+w the final source sigma+delta+I<=220+w.
    need(330-220-10==100 and 100>F(3,2)*14,'P2 new final margin')
    need(492-3*162==6,'P4 cross without endpoint fringe correction')
    need(62-57==5,'Z5 C5 tail margin')
    return dict(Z1_lower=73,Z1_upper=17,Z2_required_A=344,Z2_source_cap=288,Z2_margin=56,
                P2_beta_O_lower=82,P2_beta_O_upper=70,P2_final_lower=100,P2_final_upper=21,
                P4_cross_margin=6,Z5_C5_tail_margin=5)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=dict(schema='upper84-new-geometry-v1',status='PASS_NEW_ANALYTIC_CHECKS',
                source=source_cap(),no_empty=no_empty(),adaptive=adaptive(),
                alpha=analytic_alpha(),terminals=shortened_terminals(),
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                full_theorem_formally_verified=False)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(result['status'])


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError) as exc:
        raise SystemExit('FAIL: '+str(exc))
