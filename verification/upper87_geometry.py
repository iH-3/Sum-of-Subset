#!/usr/bin/env python3
"""Fresh finite checks of simultaneous dense stars and size-88 scalar margins.

The arbitrary-set proofs are in the accompanying report. These checks alone
do not exclude size 88. All arithmetic is integral and checks survive -O.
"""
import argparse
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from math import isqrt
from pathlib import Path
import random


def need(ok, message):
    if not ok:
        raise ValueError(message)


def tri(r):
    return r*(r+1)//2


def scalar():
    # Deliberately use the weaker already proved floor of the adopted model.
    def rho(r):
        return r-5 if r >= 21 else r-14
    failed = []
    margins = []
    for a in range(15,36):
        b=71-a; k=35-a; imbalance=tri(a)+tri(b)-tri(35)-tri(36)
        need(imbalance == k*(k+1), 'Wrong imbalance')
        lam=1+tri(a)+tri(b); omega=22*80+97-lam
        C=2*71+4*72+14-lam
        need(lam==1297+imbalance and omega==560-imbalance and
             C==-853-imbalance and C+omega==-293-2*imbalance,
             'Endpoint identity failed')
        need(omega < tri(b)-1 and omega < 2*tri(a), 'Inverse gate')
        if a-3+rho(a)+rho(b) <= omega-tri(a)+2:
            failed.append(k)
        if omega>=tri(a):
            ap=[tri(b-2)+2-2*b-omega,
                Fraction(b*b-11*b,2)+2*(tri(a)+1)+7-omega,
                7*b-Fraction(289,8)-(2*b+125),
                -(2453+2*a-4*tri(a)-2*tri(b)),
                tri(a)+114+(b-5)-omega]
            need(min(ap)>0,'AP/half-step margin')
            margins.append(ap)
        if k>=13:
            need(147+imbalance+rho(a)+rho(b)>omega,'High-hole exclusion')
        else:
            for r,s in ((a,b),(b,a)):
                need(tri(r-2)+2-2*r+s-5+147+imbalance>omega,
                     'Pre-lattice translate-overlap margin')
    need(sorted(failed)==list(range(7,19)), 'Inverse repair coverage')
    low_counts=[]
    mode_counts=[]
    for j in range(6):
        count=0
        for branch, paired in [('A',9),('B',5)]:
            singles=[s+str(i) for s in 'pq' for i in range(10) if i not in (4,paired)]
            for missing in combinations(['pair1','pair2']+singles,j):
                split=branch=='A' and 'pair2' not in missing and ('p5' in missing or 'q5' in missing)
                count += 1 if 'pair2' in missing else 2
                # A split variant chooses the actual beta contributor instead
                # of a nominal pair member, also giving exactly two modes.
                need(not split or 'pair2' not in missing, 'Invalid mode split')
        mode_counts.append(count)
        zero=sum((a-35)*(a-36)<=410-80*j for a in range(15,57))*count
        positive=(sum((a-35)*(a-36)<=395-80*j for a in range(15,57))*count if j<=4 else 0)
        low_counts.append(dict(j=j,zero=zero,positive=positive))
    need(mode_counts==[4,70,578,2992,10880,29512], 'Mode census')
    need(sum(x['zero']+x['positive'] for x in low_counts)==781308,'Low-root census')
    # Exact scalar finite cover, including all 14 large-loss alternatives.
    caps=[410-(a-35)*(a-36)-4*80-8 for a in range(32,40)]
    children=[1 if C<76 else 15 for C in caps]
    need(caps==[70,76,80,82,82,80,76,70] and sum(children)==92,
         'Loss cover is incomplete')
    for a,C in zip(range(32,40),caps):
        need(C<152 and (C<76 or C-76<min(a,71-a)+5),'Loss-cover quantile gate')
    return dict(side_pairs=21,inverse_repairs=sorted(failed),
                ap_minima=[str(min(row[i] for row in margins)) for i in range(5)],
                mode_counts=mode_counts,low_counts=low_counts,
                loss_cover_caps=caps,required_loss_cover_children=sum(children))


def stars():
    seed=2026101901; rng=random.Random(seed)
    cases=overlaps=dense=rows=allocations=0
    strict=0
    for case in range(240):
        p=sorted(rng.sample(range(1,35),rng.randrange(4,11)))
        q=sorted(rng.sample(range(1,35),rng.randrange(4,11)))
        E={0,*p,*(-v for v in q)}; rp=max(p); rq=max(q)
        # Include dense examples as well as deliberately sparse tails.
        xp=[rp+i for i in range(1,5)] if case%3==0 else sorted(rng.sample(range(rp+1,rp+31),4))
        yq=[rq+i for i in range(1,5)] if case%4==0 else sorted(rng.sample(range(rq+1,rq+31),4))
        D=E|set(xp)|{-v for v in yq}; mp=max(D); mq=-min(D)
        gp=max([0]+[2*j+rp-x for j,x in enumerate(xp,1)])
        gq=max([0]+[2*j+rq-y for j,y in enumerate(yq,1)])
        j=max(range(5),key=lambda j:0 if j==0 else 2*j+rp-xp[j-1])
        k=max(range(5),key=lambda k:0 if k==0 else 2*k+rq-yq[k-1])
        F=E|set(xp[:j])|{-v for v in yq[:k]}
        need(0<=gp<=4 and 0<=gq<=4,'Dense gain bound')
        need(2*len(F)-(max(F)-min(F))==2*len(E)-rp-rq+gp+gq,
             'Simultaneous dense core identity')
        strict += gp+gq>0; dense+=1
        outerp=sorted(rng.sample(range(mp+1,mp+25),4),reverse=True)
        outerq=sorted(rng.sample(range(mq+1,mq+25),4),reverse=True)
        for reflected in (False,True):
            dd={-v for v in D} if reflected else D
            pp,qq=(outerq,outerp) if reflected else (outerp,outerq)
            mm,nn=(mq,mp) if reflected else (mp,mq)
            c=pp[0]-sum(pp[1:]); hub={c+x+y for x in dd for y in dd}
            leaves=[{c+x+y for y in dd} for x in pp]+[{c-x+y for y in dd} for x in qq[2:]]
            bounds=[2*len(E)-1-rp-rq-x+mm+gp+gq for x in pp]+[
                    2*len(E)-1-rp-rq-x+nn+gp+gq for x in qq[2:]]
            for leaf,H in zip(leaves,bounds):
                need(len(hub&leaf)>=H,'Dense raw overlap')
                overlaps+=1
            allsets=[hub]+leaves; union=set().union(*allsets)
            # Targets need not be intervals, and can contain holes.
            target={v for v in union if v>0 and rng.randrange(4)!=0}
            for mask in (1,3,7,15,31,63):
                chosen=[leaves[i] for i in range(6) if mask>>i&1]
                deficit=len(hub)+sum(map(len,chosen))-len((hub|set().union(*chosen))&target)
                intersections=sum(len(hub&leaf) for leaf in chosen)
                for member in [hub]+chosen:
                    need(deficit>=intersections+len(member-target),'Star plus one loss')
                    rows+=1
            total=sum(map(len,allsets))-len(union&target)
            full_group=allsets[:5]
            sub=sum(map(len,full_group))-len(set().union(*full_group)&target)
            need(total>=sub+sum(len(v-target) for v in allsets[5:]),
                 'Group allocation double counts capacity')
            allocations+=1
        cases+=1
    # A complete pointwise proof check for stars of every degree up to 8.
    incidence=0
    for t in range(1,9):
        for bits in product((0,1),repeat=t+1):
            multiplicity=sum(bits); edges=bits[0]*sum(bits[1:])
            for inside in (False,True):
                deficit=multiplicity-int(inside and multiplicity>0)
                for selected in range(t+1):
                    need(deficit>=edges+(0 if inside else bits[selected]),
                         'Pointwise star inequality')
                    incidence+=1
    A={0,1}; target={1}; deficit=2*len(A)-len(A&target)
    need(deficit<len(A)+2*len(A-target),'Double outside-loss negative control')
    need(strict>0,'No strict dense-core example exercised')
    return dict(seed=seed,sets=cases,dense_identities=dense,
                strict_dense_examples=strict,raw_overlaps=overlaps,
                star_rows=rows,allocation_rows=allocations,
                exhaustive_pointwise_checks=incidence,
                negative_controls=['adding_two_outside_losses_rejected'])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    out=dict(status='PASS_FINITE_SCALAR_AND_GEOMETRY_CHECKS',
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             scalar=scalar(),geometry=stars(),
             scope='Finite checks supplement the general proof; no endpoint exclusion alone')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'])


if __name__=='__main__':
    main()
