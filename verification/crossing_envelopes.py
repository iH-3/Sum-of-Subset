#!/usr/bin/env python3
"""Proved interval-union envelopes with external-pair membership deductions."""
from functools import lru_cache
from itertools import combinations_with_replacement
from nonap_sharp import require
CUTS=((3,1),(1,3),(3,2),(2,3),(2,2),(3,3))
X=('Rp','x1','x2','x3','Mp');Y=('Rq','y1','y2','y3','Mq')


def add(*forms):
    out={}
    for f in forms:
        for k,v in f.items():out[k]=out.get(k,0)+v
    return {k:v for k,v in out.items() if v}


def neg(f):return {k:-v for k,v in f.items()}


def sign(f):
    # x_i=sum_{j<=i} gap_j, with every gap a positive integer.
    coeff=[sum(f.get(v,0) for v in side[j:]) for side in (X,Y) for j in range(5)]
    if all(v>=0 for v in coeff):return 1
    if all(v<=0 for v in coeff) and any(coeff):return -1
    return 0


@lru_cache(maxsize=1)
def catalogue():
    cuts=[];guards={}
    for i,h in CUTS:
        external=[('p'+str(k),{X[k]:1}) for k in range(i+1,5)]+[('q'+str(l),{Y[l]:-1}) for l in range(h+1,5)]
        members=[]
        for (ak,av),(bk,bv) in combinations_with_replacement(external,2):
            f=add(av,bv);J=f'cj_{i}_{h}_{ak}_{bk}';conditions=[];known=False
            for key,center in [('base',{})]+external:
                lower=add(f,{Y[h]:2}) if key=='base' else add(f,neg(center),{Y[h]:1})
                upper=add(neg(f),{X[i]:2}) if key=='base' else add(neg(f),center,{X[i]:1})
                signs=[sign(lower),sign(upper)]
                if -1 in signs:continue
                if signs==[1,1]:known=True;break
                labels=[]
                for side,form,sgn in zip(('L','U'),(lower,upper),signs):
                    if sgn==1:continue
                    label=f'cm_{i}_{h}_{ak}_{bk}_{key}_{side}'
                    guards[label]=form;labels.append(label)
                conditions.append(labels)
            members.append(dict(pair=[ak,bk],J=J,known=known,conditions=conditions))
        cuts.append(dict(i=i,h=h,external=external,members=members))
    # Omit guards rendered redundant by a later universally containing interval.
    used={v for cut in cuts for m in cut['members'] if not m['known'] for group in m['conditions'] for v in group}
    guards={k:v for k,v in guards.items() if k in used}
    return dict(cuts=cuts,guards=guards)


def audit():
    import random
    rng=random.Random(20261018);checks=0;inside=outside=0;strict=0
    for case in range(1800):
        if case%2:
            P=sorted(rng.sample(range(1,90),8));Q=sorted(rng.sample(range(1,90),8))
        else:
            P=sorted(rng.sample([1,2,3,5,9,17,33,65,129,257,513,1025],8))
            Q=sorted(rng.sample([1,2,4,7,13,25,49,97,193,385,769,1537],8))
        point=dict(zip(X+Y,P[-5:]+Q[-5:]));D=[0]+P+[-v for v in Q]
        K=len({u+v for u in D for v in D})
        ev=lambda f:sum(point[k]*v for k,v in f.items())
        for cut in catalogue()['cuts']:
            i,h=cut['i'],cut['h'];x=[point[k] for k in X];y=[point[k] for k in Y]
            F=set(range(-y[h],x[i]+1));E=[ev(f) for _,f in cut['external']]
            intervals=[(-2*y[h],2*x[i])]+[(t-y[h],t+x[i]) for t in E]
            W=x[i]+y[h];s=len(E)
            raw=2*W+1+sum(min(W+1,x[k]-x[k-1]) for k in range(i+1,5))+sum(min(W+1,y[k]-y[k-1]) for k in range(h+1,5))
            deduction=0
            for m,(u,v) in zip(cut['members'],combinations_with_replacement(E,2)):
                actual=any(lo<=u+v<=hi for lo,hi in intervals)
                encoded=m['known'] or any(all(ev(catalogue()['guards'][name])>=0 for name in group) for group in m['conditions'])
                require(actual==encoded,'Pair-membership encoding differs')
                deduction+=actual;inside+=actual;outside+=not actual
            require(K<=raw+s*(s+1)//2-deduction,'Deduplicated interval envelope fails')
            checks+=1;strict+=deduction>0
    require(inside>0 and outside>0,'Vacuous membership checks')
    return dict(cuts=len(CUTS),guards=len(catalogue()['guards']),pair_labels=sum(len(v['members']) for v in catalogue()['cuts']),cases=1800,checks=checks,inside=inside,outside=outside,strict_improvements=strict,seed=20261018,
                scope='Finite sanity checks; general proof counts the labelled pairs outside the hull union')
