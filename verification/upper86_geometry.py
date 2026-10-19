#!/usr/bin/env python3
"""Independent exact c>=32 certificate and density/defect geometry checks.

No archive model code or numerical solver is imported. Finite geometry examples
supplement the universal proofs in reports/upper86_adoption_20261019.tex.
Every check uses explicit exceptions and remains active under Python -O.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path


def need(ok,message):
    if not ok:
        raise ValueError(message)


def tri(r):
    return r*(r+1)//2


def form(**terms):
    return terms


def add(*terms):
    out = Counter()
    for weight,row in terms:
        for key,value in row.items():
            out[key] += weight*value
    return {k:v for k,v in out.items() if v}


def rows(a,branch,choice,E=31):
    b=70-a
    result={}
    centers={}
    for s,t in [('p','q'),('q','p')]:
        c=form(**{s+'1':1,s+'2':-1,s+'3':-1,s+'4':-1})
        for i in range(4):
            centers[s+str(i)]=(s,add((1,c),(1,form(**{s+str(i+1):1}))))
            centers[s+str(i+4)]=(s,add((1,c),(-1,form(**{t+str(i+1):1}))))
        centers[s+'8']=(s,form(**{s+'2':1,s+'3':-1,s+'4':-1}))
        centers[s+'9']=(s,form(**{s+'2':2,s+'1':-1,s+'3':-1,s+'4':-1}))
    j=9 if branch=='A' else 5
    selected={key:value for key,value in centers.items() if int(key[1:]) not in (4,j)}
    selected['1']=centers['p4']
    selected['2']=centers[('p' if choice==0 else 'q')+str(j)]
    for s,r in [('p',a),('q',b)]:
        result['O'+s]=(form(**{'M'+s:1,s+'4':-1}),-1)
        result['D'+s]=(form(**{s+'4':1,s+'3':-1}),-1)
        result['H'+s]=(form(**{'R'+s:1,'M'+s:-1}),-4)
        result['J'+s]=(form(**{'R'+s:-1}),-r)
        result['F'+s]=(form(**{'M'+s:2,'R'+s:6,'S'+s:-2}),-2*tri(r)-12)
    loss=form(Lp=1,Lq=1)
    for label,(s,c) in selected.items():
        t='q' if s=='p' else 'p'
        loss['l'+label]=1;loss['u'+label]=1
        result['L'+label]=(add((-1,c),(-1,form(**{'l'+label:1,'M'+s:1}))),-79)
        result['U'+label]=(add((1,c),(-1,form(**{'u'+label:1,'S'+s:1,'M'+t:1}))),-78)
    result['C']=(form(delta=1),E)
    result['Q']=(form(Sp=1,Sq=1,delta=1,K=-2),1506)
    result['K']=(form(K=1,Mp=-2,Mq=-2),1)
    result['B']=(add((1,loss),(-1,form(delta=1))),0)
    return result,loss


WEIGHTS={
 'A0':{'C':1,'Op':2,'L1':1,'L2':1,'Oq':2,'Lq5':1,'Lq8':1,'B':1},
 'A1':{'C':56,'Hp':6,'Jp':24,'Jq':12,'Fp':3,'Fq':2,'Q':14,'K':28,
       'Up0':8,'Dp':74,'Op':152,'Lp8':70,'L1':16,'L2':26,'Uq0':10,'Dq':70,'Oq':148,'Lq5':62,'B':70},
 'B0':{'C':11,'Hp':12,'Hq':12,'Jp':12,'Jq':18,'Fq':1,'Q':4,'K':8,
       'Up0':4,'Dp':19,'Op':46,'Lp9':4,'L1':12,'Uq0':2,'Lq2':6,'Dq':32,'Oq':74,'Lq6':9,'Lq7':15,'Lq9':14,'B':15},
 'B1':{'C':1,'Op':2,'Lp9':1,'L1':1,'L2':1,'Lq2':1,'Oq':3,'Lq9':1,'B':1}}


def combine(matrix,weights):
    need(weights and all(type(w)is int and w>0 and k in matrix for k,w in weights.items()),
         'Invalid exact nonnegative combination')
    lhs=add(*[(w,matrix[k][0])for k,w in weights.items()])
    rhs=sum(w*matrix[k][1]for k,w in weights.items())
    need(all(v>=0 for v in lhs.values()) and rhs<0,'Not an exact contradiction')
    return lhs,rhs


def analytic():
    minima={}
    for mode,weights in WEIGHTS.items():
        values=[]
        for a in range(15,56):
            b=70-a;matrix,loss=rows(a,mode[0],int(mode[1]))
            lhs,rhs=combine(matrix,weights)
            if mode=='A0':
                wanted=add((1,loss),(1,form(p3=2,q3=2,l1=-1,l2=-1,lq5=-1,lq8=-1)))
                expected=31-320
            elif mode=='A1':
                wanted=add((70,loss),(1,form(p3=4,q3=8,up0=-8,lp8=-70,l1=-16,l2=-26,uq0=-10,lq5=-62)))
                expected=56*31+5434-24*a-12*b-6*tri(a)-4*tri(b)
                need(expected==-5*a*a+267*a-3610,'A1 polynomial')
                need(Fraction(-911,20)<0,'A1 continuous maximum')
            elif mode=='B0':
                wanted=add((15,loss),(1,form(p3=2,q3=4,up0=-4,lp9=-4,l1=-12,uq0=-2,lq2=-6,lq6=-9,lq7=-15,lq9=-14)))
                expected=11*31+545-12*a-18*b-2*tri(b)
                need(expected==46-b*b-7*b and b>=15,'B0 polynomial')
            else:
                wanted=add((1,loss),(1,form(p3=2,q3=2,lp9=-1,l1=-1,l2=-1,lq2=-1,lq9=-1)))
                expected=31-400
            need(lhs==wanted and rhs==expected,'Symbolic row identity differs')
            values.append(-rhs)
        minima[mode]=min(values)
    need(minima=={'A0':289,'A1':46,'B0':284,'B1':369},'Four-mode margins')
    # This is a bound supplied by these vectors, not a claim of optimality.
    matrix,_=rows(27,'A',1,E=32)
    need(sum(w*matrix[k][1] for k,w in WEIGHTS['A1'].items())==10,
         'Expected limitation at c=32')
    need(max(574-k*k-148-tri(35-k)for k in range(21))==6,'Nonprimitive AP cap')
    negatives=[]
    good,_=rows(27,'A',1)
    for label,modified in [('negative_weight',{**WEIGHTS['A1'],'C':-1}),
                           ('missing_budget',{k:v for k,v in WEIGHTS['A1'].items() if k!='B'})]:
        try: combine(good,modified)
        except ValueError: negatives.append(label)
        else: raise ValueError('Accepted invalid control: '+label)
    try: combine(matrix,WEIGHTS['A1'])
    except ValueError: negatives.append('nonnegative_rhs_at_32')
    else: raise ValueError('Accepted noncontradictory RHS')
    return dict(checked_systems=164,slack_lower_bound=32,margins=minima,
                A1_continuous_margin='911/20',negative_controls=negatives)


def density():
    universe=list(range(-5,0))+list(range(1,6))
    comparisons=0;strict_trim=0
    for mask in range(1<<len(universe)):
        D={0}|{x for i,x in enumerate(universe) if mask>>i&1}
        p=sorted(x for x in D if x>0);q=sorted(-x for x in D if x<0)
        score=lambda X:max([0]+[2*j-x for j,x in enumerate(X,1)])
        optimum=2+score(p)+score(q)
        subsets=list(D-{0});best=-10**9
        for sub in range(1<<len(subsets)):
            F={0}|{x for i,x in enumerate(subsets) if sub>>i&1}
            value=2*len(F)-max(F)+min(F)
            need(value<=optimum,'Density envelope violated')
            best=max(best,value);comparisons+=1
        need(best==optimum,'Density envelope unattained')
        strict_trim += optimum>2*len(D)-max(D)+min(D)
    # Explicit removal of a far core maximum, compatible with positive holes.
    P=[1,2,3,30];R=30;C=sum(P);one=2*R-C+tri(len(P)-2)-2
    need(one==25 and R-P[-2]-2==one and one>4,'One-point gain example')
    return dict(sets=1024,subset_comparisons=comparisons,strict_trim_examples=strict_trim,
                unbounded_gain_example=one)


def defects():
    checked=0;profiles=[]
    for L in range(1,13):
        for mask in range(1<<(L-1)):
            S={0,L}|{x for x in range(1,L)if mask>>(x-1)&1}
            bad={x for x in S if not any(y<z and y+z==2*x for y in S for z in S)}
            n=len(S)
            need(all(x<=L-n+1 or x>=n-1 for x in bad),'Boundary localization')
            need(not any(x<y<z and x+z==2*y for x in bad for y in bad for z in bad),
                 'Defective set is not AP-free')
            checked+=1
    for w in range(4,8):
        counts=[]
        for inner in combinations(range(1,w),3):
            pts=(0,*inner,w)
            nu=[int(any(x+y==2*t for x,y in combinations(pts,2)))for t in inner]
            need(w+sum(nu)>=7 and w+2*sum(nu)>=8,'Global midpoint inequality')
            need(all(nu[i-1]+pts[i+1]-pts[i-1]>=3 for i in range(1,4)),
                 'Local midpoint inequality')
            counts.append(sum(nu))
        profiles.append([w,len(counts),min(counts)])
    need(profiles==[[4,1,3],[5,4,2],[6,10,1],[7,20,1]],'Profile census')
    return dict(boundary_sets=checked,five_point_profiles=profiles)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=dict(status='PASS_STRENGTHENED_ANALYTIC_AND_GEOMETRY',
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                analytic=analytic(),density=density(),defects=defects(),
                scope='Exact finite checks; universal proofs and endpoint replay are separate obligations')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'])


if __name__=='__main__':main()
