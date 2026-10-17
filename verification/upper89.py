#!/usr/bin/env python3
"""Exact size-90 exclusion by retained prefixes and ordered fixed scores."""
import argparse
from collections import Counter
from copy import deepcopy
from functools import lru_cache
import hashlib
import json
from math import isqrt
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import upper97 as prior
import nonap_sharp
import nonap_inverse
import nonap_hole_rho_schedule as nonap_hole_rho
import integral_centers
import fixed_scores
import fixed_score_order
import retained_prefix
base=prior.base
require,add,scale=prior.require,prior.add,prior.scale
Quadratic,triangular,interval_certificate=prior.Quadratic,prior.triangular,prior.interval_certificate
ROOT=prior.ROOT
DEFAULT_CERTIFICATE=ROOT/'data/upper89_certificates.json'
FORMAT='upper89-prefix-retention-v1'
BANDS={'P':dict(lower=1,upper=2,cap=318,rho=63,mu_slope=1,mu_intercept=-3),
       'Q':dict(lower=3,upper=4,cap=310,rho=75,mu_slope=1,mu_intercept=6),
       'R':dict(lower=5,upper=14,cap=309,rho=96,mu_slope=2,mu_intercept=-5)}
RANGES={}
for prefix,cap,last in [('Z',377,4)]+[(k,v['cap'],v['cap']//82) for k,v in BANDS.items()]:
    for j in range(last+1):
        valid=[a for a in range(14,60) if (a-36)*(a-37)<=cap-82*j]
        RANGES[prefix+str(j)]=(min(valid),max(valid))


def modes(j):
    from itertools import combinations
    require(type(j) is int and 0<=j<=4,'Unsupported empty-unit count')
    for branch,i in (('A',9),('B',5)):
        singles=[s+str(t) for s in 'pq' for t in range(10) if t not in (4,i)]
        for missing in combinations(['pair1','pair2']+singles,j):
            split=branch=='A' and 'pair2' not in missing and ('p5' in missing or 'q5' in missing)
            choices=['-'] if 'pair2' in missing or split else ['p','q']
            for choice in choices:
                slots=[v for v in singles if v not in missing]
                if 'pair1' not in missing:slots.append('p4')
                if choice!='-':slots.append(choice+str(i))
                for member in ('p','q') if split else ('-',):
                    yield dict(branch=branch,missing=missing,choice=choice,member=member,slots=slots)

LOW_COUNTS={key:(hi-lo+1)*sum(1 for _ in modes(int(key[-1]))) for key,(lo,hi) in RANGES.items()}


def centers():
    out={}
    for s,t in (('p','q'),('q','p')):
        c={s+'1':1,s+'2':-1,s+'3':-1,s+'4':-1}
        for i in range(4):
            out[s+str(i)]=add(c,{s+str(i+1):1})
            out[s+str(i+4)]=add(c,{t+str(i+1):-1})
        out[s+'8']={s+'2':1,s+'3':-1,s+'4':-1}
        out[s+'9']={s+'1':-1,s+'2':2,s+'3':-1,s+'4':-1}
    return out

def center_integrality(mode,leading_available):
    sides=[side for side in 'pq' if leading_available and any(side+str(i) in mode['slots'] for i in range(4))]
    return integral_centers.derive(mode,sides)


@lru_cache(maxsize=1)
def center_integrality_audit():
    counts={};incomplete=[];examples=[]
    for j in range(5):
        total=complete=ordinary_only=0
        for mode in modes(j):
            out=center_integrality(mode,True);plain=center_integrality(mode,False)
            total+=1;complete+=out['complete'];ordinary_only+=plain['complete']
            if j==4 and not out['complete']:incomplete.append(dict(mode=mode,proof=out))
            if j==3 and mode['branch']=='B' and mode['missing']==('p0','p1','p8') and mode['choice']=='p':
                examples.append(dict(mode=mode,proof=plain))
        counts[j]=dict(total=total,complete=complete,ordinary_only=ordinary_only)
    require(all(v['complete']==v['total']==v['ordinary_only'] for j,v in counts.items() if j<=3),'Ordinary-center integral basis failed')
    require(counts[4]==dict(total=10880,complete=10850,ordinary_only=10812),'Four-empty integral audit changed')
    H=integral_centers.row_hermite([(2,0),(0,1)],2)
    require(not integral_centers.contains(H,[1,0]) and integral_centers.contains(H,[0,1]),'Nonunit pivot divided away')
    return dict(counts=counts,incomplete_four_empty=incomplete,previous_exception_examples=examples,
                rule='integer row lattice; every basis row checked as an integer combination of contributing centers')


@lru_cache(maxsize=1)
def core_cutoff_audit():
    """Independent finite sanity check of the general two-tail counting proof."""
    from itertools import combinations
    candidates=list(combinations((1,2,3,40,41,42,43,100),6))
    sets=checks=strict=trim_checks=trim_strict=0
    for p in candidates:
        for q in candidates:
            D=(0,)+p+tuple(-v for v in q)
            sums={x+y for x in D for y in D};old=[];new=[];sets+=1
            for i in range(6):
                for h in range(6):
                    lower=-(q[-1]+q[h]);upper=p[-1]+p[i]
                    tails=triangular(5-i)+triangular(5-h)
                    bound=upper-lower+1+tails
                    require(sum(v<lower or v>upper for v in sums)<=tails,'Tail pair count failed')
                    require(len(sums)<=bound,'Two-tail cutoff bound failed')
                    new.append(bound);checks+=1
                    if i>=1 and h>=1:old.append(bound)
            require(min(new)<=min(old),'Extra cutoff weakened the bound')
            strict+=min(new)<min(old)
            trimmed=[]
            for kp,kq in ((1,0),(0,1),(1,1)):
                A,B=5-kp,5-kq;removed=kp+kq
                F=(0,)+p[:A+1]+tuple(-v for v in q[:B+1])
                twoF={x+y for x in F for y in F}
                increment=removed*len(D)-triangular(removed-1)
                require(len(sums)<=len(twoF)+increment,'Trimmed cardinal increment failed')
                for i in range(A+1):
                    for h in range(B+1):
                        bound=p[A]+q[B]+p[i]+q[h]+1+triangular(A-i)+triangular(B-h)+increment
                        require(len(sums)<=bound,'Trimmed cutoff bound failed')
                        trimmed.append(bound);trim_checks+=1
            trim_strict+=min(trimmed)<min(new)
    return dict(sets=sets,cutoff_checks=checks,strict_improvement_examples=strict,
                trimmed_cutoff_checks=trim_checks,trimmed_strict_improvement_examples=trim_strict,
                cutoff_positions=6,tail_rows=36,trimmed_tail_rows=85,inner_loss_cutoffs=6,
                scope='finite sanity check; arbitrary-set proof is in the report')


@lru_cache(maxsize=1)
def density_audit():
    from itertools import combinations
    count=0;maximum_holes=0
    for r in range(6,15):
        for q in range((r-4)//2+1):
            R=r+q
            for deleted in combinations(range(1,R),q):
                x=tuple(v for v in range(1,R+1) if v not in deleted)
                bits=1
                for v in x:bits|=bits<<v
                h=sum(x)+1-bits.bit_count()
                require(2*R<=3*r-4 and h<=2*q,'Dense span finite check failed')
                count+=1;maximum_holes=max(maximum_holes,h)
    chords=0
    for r in range(17,58):
        for L,H in ((15,150),(19,163),(15,15),(50,100)):
            for z in range(L,H+1):
                if H>L:
                    lo,hi=min(L,r-3),min(H,r-3)
                    require(lo*(H-L)+(hi-lo)*(z-L)<=min(z,r-3)*(H-L),'Chord exceeds the concave floor')
                chords+=1
    return dict(dense_sets=count,maximum_holes=maximum_holes,chord_points=chords,
                necessary_bound='2R >= 2r + min(z,r-3)',
                scope='finite checks supplement the general central-interval proof')


@lru_cache(maxsize=1)
def progression_audit():
    """Independent small AP sums; the arbitrary-length residue proof is in the report."""
    from math import gcd
    cases=0
    for u in range(2,16):
        for v in range(2,16):
            for p in range(1,9):
                for q in range(1,9):
                    if gcd(p,q)!=1:continue
                    actual=len({p*i+q*j for i in range(u) for j in range(v)})
                    expected=u*v if p>=v or q>=u else p*u+q*v-p*q
                    require(actual==expected,'Progression residue formula failed')
                    cases+=1
    return dict(cases=cases,formula='uv if p>=v or q>=u; otherwise pu+qv-pq',
                scope='finite sanity check; general proof uses residue classes')


@lru_cache(maxsize=1)
def progression_gap_audit():
    from itertools import combinations
    gaps=dominant=fibers=0
    for r in range(2,7):
        for x in combinations(range(1,13),r):
            support={0}
            for v in x:support|={u+v for u in support}
            ordered=sorted(support)
            differences=[v-u for u,v in zip(ordered,ordered[1:])]
            total=0;prefix=[]
            for v in x:prefix.append(v-total);total+=v
            require(max(differences)==max(prefix),'Largest subset-sum gap formula fails')
            for u in range(2,9):
                actual=len({v+j for v in support for j in range(u)})
                expected=len(support)+u-1+sum(min(d-1,u-1) for d in differences)
                require(actual==expected,'AP gap formula fails');gaps+=1
                if sum(d>=u for d in differences)==1:
                    require(x[-1]>sum(x[:-1]),'Unique large gap is not dominant')
                    require(len(support)-1-triangular(r)>=triangular(r-2),'Dominant support floor fails')
                    dominant+=1
                if sum(v%2 for v in x)<2:continue
                two_sum={2*j+v for j in range(u) for v in support}
                kappa=len(two_sum)-u-len(support)+1
                if kappa>=2*(u-1):continue
                holes=[]
                for parity in (0,1):
                    f=sorted(v for v in support if v%2==parity)
                    require(all(v-w<2*u for w,v in zip(f,f[1:])),'Unsaturated fiber has a long gap')
                    holes.append((f[-1]-f[0])//2+1-len(f))
                w=min(v for v in x if v%2)
                require(kappa==u-1+sum(holes),'Two-fiber excess identity fails')
                require(total+1-len(support)==kappa-u+w,'Two-fiber hull-hole identity fails')
                require(total+2*(u-1)+1-len(two_sum)==w-1,'Two-fiber sumset holes fail')
                fibers+=1
    return dict(gap_checks=gaps,unique_gap_checks=dominant,two_fiber_checks=fibers,
                scope='finite sanity checks; arbitrary-length proofs are in the report')


@lru_cache(maxsize=1)
def empty_own_audit():
    from itertools import combinations
    from verify import check_cover
    cases=high_checks=fixed_checks=0
    for mask in range(1<<8):
        universe=(-4,-3,-2,-1,1,2,3,4)
        D=(0,)+tuple(v for i,v in enumerate(universe) if mask>>i&1)
        if max(D)<=0 or min(D)>=0:continue
        support={0}
        for v in D:support|={u+v for u in support}
        if len(support)!=max(support)-min(support)+1:continue
        S=sum(v for v in D if v>0)
        for ascending in combinations([max(D)+v for v in (1,2,3,4,5,8,12,20)],4):
            p=ascending[::-1];c=p[0]-sum(p[1:]);u=[c+v for v in p]
            active=[any(1<=v+x<=S for x in D) for v in u];cases+=1
            for i in range(3):
                if not active[i] and any(active[i+1:]):
                    require(u[i]>=S+1,'Empty own center is not high');high_checks+=1
                    if i==0:
                        require(all(c+p[0]+v>S for v in p),'Fixed high label fails')
                        fixed_checks+=4
    require(high_checks>0 and fixed_checks>0,'Vacuous empty-center audit')
    return dict(cases=cases,high_checks=high_checks,fixed_checks=fixed_checks,
                fixed_cover=check_cover(),labels=['C'+s+'1'+str(i) for s in '+-' for i in range(1,5)],
                scope='finite checks supplement the general empty-center and disjoint loss proof')


@lru_cache(maxsize=1)
def full_group_audit():
    checks=cases=0
    universe=(-4,-2,-1,1,3,5)
    for mask in range(1<<len(universe)):
        D={0}|{v for i,v in enumerate(universe) if mask>>i&1}
        if min(D)>=0 or max(D)<=0:continue
        P,Q=max(D),-min(D);d=len(D);two={x+y for x in D for y in D};K=len(two)
        fs={0}
        for x in D:fs|={s+x for s in fs}
        target={x for x in fs if x>0};S=sum(x for x in D if x>0)
        p=[P+t for t in (12,7,3,1)];q=[Q+t for t in (3,1)];c=p[0]-sum(p[1:])
        W={'lead':{c+x for x in two}}
        for i,x in enumerate(p):W['p'+str(i)]={c+x+y for y in D}
        for i,x in enumerate(q):W['q'+str(i)]={c-x+y for y in D}
        own=[v for v in W if v.startswith('p') and W[v]&target]
        cross=[v for v in W if v.startswith('q') and W[v]&target]
        members=['lead']+own+cross;C=K+d*(len(members)-1)
        G=C-len(set().union(*(W[v] for v in members))&target)
        loss={v:len(W[v]-target) for v in members};cases+=1
        require(G>=sum(loss.values()),'Union deficit does not dominate separate losses')
        for i in range(len(own)+1):
            for j in range(len(cross)+1):
                I,J=own[i:],cross[j:];sub=['lead']+I+J
                if len(sub)==1:continue
                U=c+(p[int(I[0][1:])]+P if I else 2*P)
                L=c-(q[int(J[0][1:])]+Q if J else 2*Q)
                capacity=K+d*(len(sub)-1);rest=sum(loss[v] for v in members if v not in sub)
                union=set().union(*(W[v] for v in sub))
                require(min(union)>=L and max(union)<=U and union&target,'Unlicensed full hull')
                for v in sub:
                    require(G>=capacity-(U-L+1)+loss[v]+rest,'Raw subgroup loss double-counted');checks+=1
                for clipped in (capacity-U,capacity-S+L-1,capacity-S):
                    require(G>=clipped+rest,'Clipped subgroup bound fails');checks+=1
    return dict(cases=cases,inequalities=checks,scope='finite sanity check of full-translate common-deficit bounds')


def row_policy(group):
    lo,hi=group['lo'],group['hi'];j=group['empty']
    Imin=min((a-36)*(a-37) for a in range(lo,hi+1))
    cap=group['high']['cmax']-82*j if 'high' in group else (BANDS[group['regime'][0]]['cap'] if group['regime'][0] in BANDS else 377)-82*j-Imin
    smallest=min(lo,73-hi)
    integral=center_integrality(group['mode'],cap<163)
    policy=dict(cap=cap,quantile='ordinary' if cap<smallest+5 else 'core' if cap<78 else 'global',
                leading_basic=cap<163,leading_nested=cap<155,leading_deep=cap<153,leading_sides=integral['leading_sides'],
                strict_outer=integral['complete'],integral_gaps=integral['integral_gaps'],integral_branch=integral['integral_branch'])
    policy['empty_own_high']=[s+str(i) for s in 'pq' for i in range(3)
        if group['regime'].startswith('Z') and integral['complete']
        and s+str(i) in group['mode']['missing']
        and any(s+str(h) in group['mode']['slots'] for h in range(i+1,4))]
    policy['fixed_loss']=4*sum(s+'0' in policy['empty_own_high'] for s in 'pq')
    policy['fixed_scores']=group['regime']=='Z4' and integral['complete'] and set(group['mode']['missing'])=={'pair1','pair2','p0','q0'}
    if 'high' in group:policy['density_interval']=[group['high']['zmin'],group['high']['zmax']]
    return policy

def source_model(group,a,kind,policy_override=None):
    if not isinstance(a,Quadratic):
        require(type(a) is int and group['lo']<=a<=group['hi'],'Parameter outside group')
    regime,mode,large,j=(group[k] for k in ('regime','mode','large','empty'))
    branch,slots,member=(mode[k] for k in ('branch','slots','member'))
    b=73-a
    I=(a-36)*(a-37)
    B0=377-82*j-I
    positive=regime[0] in BANDS
    band=BANDS[regime[0]] if positive else None
    high=regime.startswith('H')
    epsp,epsq=tuple(band['mu_slope']*r+band['mu_intercept'] for r in (a,b)) if positive else (0,0)
    if high:epsp,epsq=group['high']['up'],group['high']['uq']
    names=([s+str(i) for s in 'pq' for i in range(1,5)]+
           ['Mp','Mq','Rp','Rq','Cp','Cq','Sp','Sq','delta','l_star','u_star']+
           [f'{end}_{v}' for v in slots for end in ('l','u')]+
           [s+str(i) for s in 'xy' for i in range(1,4)]+['K']+
           [f'g{s}{t}{i}' for t in range(4) for i in range(t+1,5) for s in 'pq'])
    blocks=[]
    for side in 'pq':
        for start in (0,4):
            vv=[side+str(i) for i in range(start,start+4) if side+str(i) in slots]
            if len(vv)>=2 or (start==0 and vv):
                # Centers 0..3 decrease; centers 4..7 increase.
                low,high_v=(vv[-1],vv[0]) if start==0 else (vv[0],vv[-1])
                blocks.append((side+str(start),vv,low,high_v))
    policy=policy_override or row_policy(group)
    names+=['lead_p','lead_q']
    names += ['overlap_'+key for key,_,_,_ in blocks]
    if kind=='global_nested' and policy['strict_outer']:names+=['full_p','full_q']
    score_data=fixed_scores.catalogue() if kind=='global_nested' and policy['fixed_scores'] else None
    charged_scores={f'C{s}1{i}' for s in '+-' for i in range(1,5)}
    if score_data:
        names+=['fixed_extra']+['hi_'+v for v in score_data['labels'] if v not in charged_scores]+['nonpos_'+v for v in score_data['labels']]
    if positive or high:names.append('z')
    cp=dict(p1=1,p2=-1,p3=-1,p4=-1)
    cq=dict(q1=1,q2=-1,q3=-1,q4=-1)
    bp=dict(p1=-1,p2=2,p3=-1,p4=-1)
    bq=dict(q1=-1,q2=2,q3=-1,q4=-1)
    centers={}
    for side,c,other in (('p',cp,'q'),('q',cq,'p')):
        for i in range(4):
            centers[side+str(i)]=add(c,{side+str(i+1):1})
            centers[side+str(i+4)]=add(c,{other+str(i+1):-1})
        centers[side+'8']={side+'2':1,side+'3':-1,side+'4':-1}
        centers[side+'9']=bp if side=='p' else bq
    rows={}
    indices={v:i for i,v in enumerate(names)}
    require(len(indices)==len(names),'Duplicate model variable')
    def row(label,coeff,rhs):
        require(label not in rows and coeff.keys()<=indices.keys(),'Duplicate row or unknown variable')
        require(all(type(x) is int for x in coeff.values()),'Noninteger model matrix')
        vector=[0]*len(names)
        for name,value in coeff.items():vector[indices[name]]=value
        rows[label]=(vector,rhs)
    def zcoeff(value):return {'z':value} if positive or high else {}
    x,y=['Rp','x1','x2','x3','Mp'],['Rq','y1','y2','y3','Mq']
    for side,r,eps,xx in (('p',a,epsp,x),('q',b,epsq,y)):
        for i in range(1,4):row(f'D{side}{i}',{side+str(i+1):1,side+str(i):-1},-1 if side+str(i) in policy['integral_gaps'] else 0)
        row(f'D{side}4',{'M'+side:1,side+'4':-1},-1 if side+'4' in policy['integral_gaps'] else 0)
        row('E'+side,{'R'+side:1,'M'+side:-1},-4)
        boost=0
        if positive:
            require(min(group['lo'],73-group['hi'])>=band['lower']+3,'Low-band density threshold fails')
            boost=(band['lower']+1)//2
        elif high:
            rr=group['lo'] if side=='p' else 73-group['lo']
            boost=(min(group['high']['zmin'],rr-3)+1)//2
            L,H=policy['density_interval']
            lo,hi=min(L,rr-3),min(H,rr-3)
            if H>L:row('density_chord_'+side,{'R'+side:-2*(H-L),'z':hi-lo},-2*(H-L)*r-lo*(H-L)+(hi-lo)*L)
        row('G'+side,{'R'+side:-1},-r-boost)
        row('H'+side,add({'M'+side:2,'R'+side:6,'S'+side:-2},zcoeff(2)),-2*triangular(r)-12-2*eps)
        if positive or high:
            row('Hhat'+side,add({'M'+side:2,'R'+side:8,'S'+side:-2},zcoeff(1)),-2*triangular(r-1)-12-2*(r-4))
        else:row('Hhat'+side,{'M'+side:1,'R'+side:4,'S'+side:-1},-triangular(r-1)-6)
        for i in range(1,5):row(f'I{side}{i}',{xx[i-1]:1,xx[i]:-1},-1)
        row('Hfull'+side,add(add({v:1 for v in xx[1:]},{'S'+side:-1}),zcoeff(1)),-triangular(r)-eps)
        if positive or high:
            row('Htilde'+side,add(add({v:2 for v in xx},{'S'+side:-2}),zcoeff(1)),-2*triangular(r-1)-2*(r-4))
        else:row('Htilde'+side,add({v:1 for v in xx},{'S'+side:-1}),-triangular(r-1))
        row('Icore_min_'+side,{'C'+side:-1},-(r-1))
        row('Icore_gap_'+side,{'C'+side:1,'R'+side:-1},-1)
        if positive or high:
            row('Hfull_core_'+side,add(add(add({v:4 for v in xx},{'C'+side:4}),{'S'+side:-4}),zcoeff(1)),-4*triangular(r-2)-4*(r-5))
        else:row('Hfull_core_'+side,add(add({v:1 for v in xx},{'C'+side:1}),{'S'+side:-1}),-triangular(r-2))
        rmax=group['hi'] if side=='p' else 73-group['lo']
        upper=add({'S'+side:1,'C'+side:-(rmax-1)},scale(-1,{v:1 for v in xx}))
        if positive:upper=add(upper,dict(z=-1))
        row('Hfull_core_upper_'+side,upper,-triangular(r-2)-(band['lower'] if positive else 0))
    row('branch',scale(1 if branch=='A' else -1,add(bp,bq)),0 if branch=='A' or not policy['integral_branch'] else -1)
    if member!='-':
        row('pairnonempty',add(scale(-1,bp if member=='p' else bq),{'M'+member:-1}),-1)
    if positive or high:
        row('zlower',dict(z=-1),-group['high']['zmin'] if high else -band['lower'])
        row('zupper',dict(z=1),group['high']['zmax'] if high else band['upper'])
    row('cap',dict(delta=1),group['high']['cmax']-82*j if high else band['cap']-82*j-I if positive else B0)
    if high:
        excess=531-I-group['high']['rp']-group['high']['rq']-82*j
        row('cap_holes',dict(delta=1,z=1),excess)
        row('cap_constant',dict(delta=1),excess-52)
        row('cap_peeling',dict(delta=1,z=-2),excess-154)
    row('span',add(dict(Rp=1,Rq=1,delta=1),zcoeff(-3)),77+B0-(61 if positive or high else 0))
    for v in policy['empty_own_high']:
        row('empty_own_high_'+v,add(scale(-1,centers[v]),{'S'+v[0]:1}),-1)
    for v in slots:
        side=v[0];other='q' if side=='p' else 'p'
        own,opp=(a,b) if side=='p' else (b,a)
        qtype=policy['quantile']
        l=add(scale(-1,centers[v]),{'l_'+v:-1})
        u=add(centers[v],{'u_'+v:-1,'S'+side:-1})
        if qtype=='global':
            l,u=add(l,{'M'+side:-1}),add(u,{'M'+other:-1})
            lr,ur=-82,-81
        elif qtype=='core':
            l,u=add(l,{'R'+side:-1}),add(u,{'R'+other:-1})
            lr,ur=-78,-77
        else:lr,ur=-(opp+5),-(own+4)
        row('L'+v,l,lr);row('U'+v,u,ur)
        # These count caps are valid in the actual-set selection, before relaxation.
        row('slotcap'+v,{'l_'+v:1,'u_'+v:1},77 if qtype=='core' else 81)
    row('loss',dict([('delta',-1)]+[(f'{end}_{v}',1) for v in slots for end in ('l','u')]),-policy['fixed_loss'])
    grouped=set();joint={'delta':-1}
    for key,vv,low,high_v in blocks:
        var='overlap_'+key;grouped.update(vv);joint[var]=1
        loss={f'{end}_{v}':1 for v in vv for end in ('l','u')}
        if key[-1]=='0':loss['lead_'+key[0]]=1
        row('overlap_sum_'+key,add(loss,{var:-1}),0)
        for v in vv:
            coeff=add({'Rp':-1,'Rq':-1,var:-1,'l_'+v:1,'u_'+v:1},
                      add(centers[low],scale(-1,centers[high_v])))
            if key[-1]=='0':coeff=add(coeff,{'lead_'+key[0]:1})
            row('overlap_hull_'+key+'_'+v,coeff,1-74*len(vv))
        if key[-1]=='0':
            from itertools import combinations
            side=key[0];other='q' if side=='p' else 'p'
            for count in range(1,len(vv)+1):
                for sub in combinations(vv,count):
                    rest={f'{end}_{v}':1 for v in vv if v not in sub for end in ('l','u')}
                    # vv is ordered by decreasing outer magnitude.
                    pmax=side+str(int(sub[0][1:])+1)
                    hull={var:-1,pmax:-1,'R'+side:-1,'R'+other:-2}
                    for v in ('lead',)+sub:
                        co={'lead_'+side:1} if v=='lead' else {'l_'+v:1,'u_'+v:1}
                        row('leading_group_'+key+'_'+','.join(sub)+'_'+v,
                            add(add(hull,rest),co),2-74*(len(sub)+2))
                    if kind=='global_nested' and policy['strict_outer']:
                        raw={'K':1,var:-1,pmax:-1,'M'+side:-1,'M'+other:-2}
                        prefix='full_own_'+side+'_'+','.join(sub)
                        for v in ('lead',)+sub:
                            co={'lead_'+side:1} if v=='lead' else {'l_'+v:1,'u_'+v:1}
                            row(prefix+'_raw_'+v,add(add(raw,rest),co),1-82*len(sub))
                        lead=cp if side=='p' else cq
                        clipped=[(add({'K':1,var:-1,pmax:-1,'M'+side:-1},scale(-1,lead)),-82*len(sub)),
                                 (add({'K':1,var:-1,'S'+side:-1,'M'+other:-2},lead),1-82*len(sub)),
                                 ({'K':1,var:-1,'S'+side:-1},-82*len(sub))]
                        for i,(co,rhs) in enumerate(clipped):row(prefix+'_clip_'+str(i),add(co,rest),rhs)
    for v in slots:
        if v not in grouped:joint['l_'+v]=1;joint['u_'+v]=1
    if policy['leading_basic']:
        for side,c,xx,yy in (('p',cp,x,y),('q',cq,y,x)):
            if side not in policy['leading_sides']:continue
            row('lead_mass_'+side,{'S'+side:-1,'lead_'+side:-1},-163)
            row('lead_basic_lower_'+side,add(scale(-1,c),{xx[4]:-2,'lead_'+side:-1}),-163)
            row('lead_basic_upper_'+side,add(c,{'S'+side:-1,yy[4]:-2,'lead_'+side:-1}),-162)
            row('lead_Kmass_'+side,{'K':1,'S'+side:-1,'lead_'+side:-1},0)
            row('lead_Klower_'+side,add(scale(-1,c),{'K':1,xx[4]:-2,'lead_'+side:-1}),0)
            row('lead_Kupper_'+side,add(c,{'K':1,'S'+side:-1,yy[4]:-2,'lead_'+side:-1}),1)
            if policy['leading_deep']:
                other='q' if side=='p' else 'p'
                row(f'lead_lower_{side}m1',add(scale(-1,c),{'C'+side:-2,'lead_'+side:-1}),-153)
                row(f'lead_upper_{side}m1',add(c,{'S'+side:-1,'C'+other:-2,'lead_'+side:-1}),-152)
            for i in range(5) if policy['leading_nested'] else ():
                row(f'lead_lower_{side}{i}',add(scale(-1,c),{xx[i]:-2,'lead_'+side:-1}),-155-2*i)
                row(f'lead_upper_{side}{i}',add(c,{'S'+side:-1,yy[i]:-2,'lead_'+side:-1}),-154-2*i)
    row('joint_overlap',joint,-policy['fixed_loss'])
    if kind=='global_nested' and policy['strict_outer']:
        full_joint={'delta':-1,'full_p':1,'full_q':1};matched=set()
        for side,other,lead in (('p','q',cp),('q','p',cq)):
            own=[v for v in slots if v[0]==side and int(v[1:])<4]
            cross=[v for v in slots if v in (side+'6',side+'7')]
            members=own+cross;matched.update(members);var='full_'+side
            losses={end+'_'+v:1 for v in members for end in ('l','u')}
            row(var+'_sum',add(losses,{var:-1,'lead_'+side:1}),0)
            for i in range(len(own)+1):
                for h in range(len(cross)+1):
                    I,J=own[i:],cross[h:];sub=I+J
                    if not sub:continue
                    rest={end+'_'+v:1 for v in members if v not in sub for end in ('l','u')}
                    U=add(lead,{side+str(int(I[0][1:])+1):1,'M'+side:1}) if I else add(lead,{'M'+side:2})
                    L=add(lead,{other+str(int(J[0][1:])-3):-1,'M'+other:-1}) if J else add(lead,{'M'+other:-2})
                    raw=add(add({'K':1,var:-1},L),scale(-1,U));prefix=var+f'_{i}_{h}'
                    for v in ['lead']+sub:
                        co={'lead_'+side:1} if v=='lead' else {'l_'+v:1,'u_'+v:1}
                        row(prefix+'_raw_'+v,add(add(raw,rest),co),1-82*len(sub))
                    clipped=[(add({'K':1,var:-1},scale(-1,U)),-82*len(sub)),
                             (add({'K':1,var:-1,'S'+side:-1},L),1-82*len(sub)),
                             ({'K':1,var:-1,'S'+side:-1},-82*len(sub))]
                    for t,(co,rhs) in enumerate(clipped):row(prefix+'_clip_'+str(t),add(co,rest),rhs)
        for v in slots:
            if v not in matched:full_joint['l_'+v]=1;full_joint['u_'+v]=1
        row('full_joint',full_joint,-policy['fixed_loss'])
    for i in range(-1,5):
        for h in range(-1,5):
            cutp='Cp' if i==-1 else x[i];cutq='Cq' if h==-1 else y[h]
            row(f'tails_{i}_{h}',add(dict(K=1,Mp=-1,Mq=-1),{cutp:-1,cutq:-1}),
                1+triangular(4-i)+triangular(4-h))
    # Remove one or both extremes first; charge new pairs by cardinality.
    xx,yy=['Cp']+x,['Cq']+y
    for kp,kq in ((1,0),(0,1),(1,1)):
        A,B=5-kp,5-kq;removed=kp+kq
        for i in range(A+1):
            for h in range(B+1):
                coeff=add(dict(K=1),add(scale(-1,{xx[A]:1,yy[B]:1}),scale(-1,{xx[i]:1,yy[h]:1})))
                row(f'tails_trim_{kp}_{kq}_{i}_{h}',coeff,
                    1+triangular(A-i)+triangular(B-h)+82*removed-triangular(removed-1))
    for t in range(5):
        coeff=add(dict(K=1),{x[t]:-2,y[t]:-2})
        for i in range(t+1,5):
            for side,xx in (('p',x),('q',y)):
                g=f'g{side}{t}{i}'
                row('Ag'+g,{g:1,xx[i]:-1,xx[i-1]:1},0)
                row('Bg'+g,{g:1,x[t]:-1,y[t]:-1},1)
                coeff[g]=-1
        row('envelope'+str(t),coeff,1+triangular(2*(4-t)))
    row('coarse2D',dict(K=1,Mp=-1,Mq=-1,Rp=-1,Rq=-1),21)
    row('cardinality',add(dict(Sp=1,Sq=1,delta=1,K=-2),zcoeff(-4)),1560-82*j)
    if score_data:
        require(policy['fixed_loss']==8,'Fixed score allocation needs both charged sides')
        extra={'fixed_extra':-1}
        for label,entry in score_data['labels'].items():
            N='nonpos_'+label;row(N+'_cap',{N:1},1);extra[N]=1
            if all(v<=0 for v in entry['gaps']):row(N+'_known',{N:-1},-1)
            elif (all(v>=0 for v in entry['gaps']) and any(entry['gaps'])) or label in charged_scores:row(N+'_known',{N:1},0)
            if label not in charged_scores:
                H='hi_'+label;row(H+'_cap',{H:1},1);extra[H]=1
        for i,labels in enumerate(score_data['groups']):row('nonpos_group_'+str(i),{'nonpos_'+v:-1 for v in labels},-1)
        for edge in fixed_score_order.catalogue()['edges']:
            lo,hi=edge['lower'],edge['upper']
            row('score_order_N_'+lo+'_'+hi,{'nonpos_'+hi:1,'nonpos_'+lo:-1},0)
            if edge['same_target']:
                if lo in charged_scores and hi not in charged_scores:row('score_order_H_'+lo+'_'+hi,{'hi_'+hi:-1},-1)
                elif lo not in charged_scores and hi not in charged_scores:row('score_order_H_'+lo+'_'+hi,{'hi_'+lo:1,'hi_'+hi:-1},0)
        for i,clause in enumerate(fixed_score_order.sign_clauses()['clauses']):
            row('score_sign_clause_'+str(i),{'nonpos_'+v:-1 for v in clause['labels']},-1)
        for label in score_data['labels']:
            if label not in charged_scores:row('score_events_disjoint_'+label,{'hi_'+label:1,'nonpos_'+label:1},1)
        row('fixed_extra_allocation',extra,26)
        for label in ('loss','joint_overlap','full_joint'):
            vector,rhs=rows[label];vector[indices['fixed_extra']]=1
    return names,rows



@lru_cache(maxsize=1)
def hole_catalogue():
    out={}
    for r in range(17,58):
        for beta in range(1,21):
            for C in range(601):
                try:out[r,beta]=base.hole_row(r,C,beta)
                except ValueError:pass
    return out


@lru_cache(maxsize=1)
def low_hole_envelope_audit():
    """Three proved hole bands, preserving support excess as well as defect caps."""
    rows=[];catalogue=hole_catalogue()
    mass_witnesses=[]
    for r in range(17,58):
        for key,beta,C in (('Q',1,5),('R',2,r-6)):
            w=base.hole_row(r,C,beta)
            require(2*beta<BANDS[key]['lower'],'Mass floor used before strict hole threshold')
            require(r+C+1==BANDS[key]['mu_slope']*r+BANDS[key]['mu_intercept'],'Wrong affine support floor')
            mass_witnesses.append(dict(band=key,**w))
    for beta in (1,2):
        cases=[]
        for a in range(17,57):
            b=73-a;witnesses=[];floors=[]
            for r in (a,b):
                w=base.hole_row(r,catalogue[r,beta]['C'],beta)
                u=r+w['C']+1
                witnesses.append(w);floors.append(nonap_inverse.witness(r,u))
            cases.append(dict(a=a,b=b,witnesses=witnesses,inverse=floors,rho_sum=sum(v['value'] for v in floors)))
        minimum=min(v['rho_sum'] for v in cases)
        require(minimum==(75 if beta==1 else 96),'Low-hole envelope floor changed')
        rows.append(dict(beta=beta,minimum_rho_sum=minimum,cases=cases))
    for key,band in BANDS.items():
        require(band['cap']==377-band['rho']+2*band['upper'],'Wrong band cap')
    require(all(3*82<=v['cap']<4*82 for v in BANDS.values()),'Wrong empty-unit thresholds')
    old_positive=sum(sum((a-36)*(a-37)<=342-82*j for a in range(14,60))*sum(1 for _ in modes(j)) for j in range(5))
    new_positive=sum(v for k,v in LOW_COUNTS.items() if k[0] in BANDS)
    return dict(bands=BANDS,uniform_coarse_cap=342,uniform_positive_roots=old_positive,
                band_positive_roots=new_positive,rows=rows,mass_witnesses=mass_witnesses)


@lru_cache(maxsize=1)
def scalar_audit(n=90):
    require(n==90,'This proof does not exclude size 89')
    nonap_sharp.finite_base()
    d,e,m,G,t0=82,74,73,154,52
    qmax=isqrt(96*e+1073-e*e);qmax-=(qmax-e+1)%2
    paired_min=(e-1-qmax)//2
    require(paired_min==11 and 1+triangular(e)>24*n+77,'Sign bootstrap fails')
    catalogue=hole_catalogue()
    lattice,low,high,witnesses,merged=[],[],[],{},{}
    lattice_witness=[];prefix_checks=[];small_boundary=[]
    for a in range(paired_min,m-paired_min+1):
        b=m-a;I=(a-36)*(a-37);omega=531-I
        if min(a,b)<14:
            require(omega < -8,'Small side not excluded by the general rho floor')
            continue
        if omega<0:continue
        lam=1+triangular(a)+triangular(b);C=2*m+4*e+14-lam
        inv=triangular(min(a,b))-2-omega
        # The one-budget comparison handles all z <= 191 + I.
        cutoff=192+I
        inner0=C+omega+2*(cutoff-1)
        innerP=C+3*omega-(nonap_sharp.nonap_floor(a)+nonap_sharp.nonap_floor(b)+m-6)
        prefix_witness=[]
        if innerP>=0:
            require(min(a,b)>=25,'Effective lattice witness outside range')
            prefix_witness=[dict(r=r,value=nonap_hole_rho.lower_bound(r,cutoff),holes=nonap_hole_rho.witness(r,cutoff)) for r in (a,b)]
            innerP=C+3*omega-2*sum(v['value'] for v in prefix_witness)
        outer=lam-(4*d-10+omega)
        # Both supports non-AP: keep both defect floors before inversion.
        r,t=min(a,b),max(a,b)
        inverse_case=dict(route='both-nonap-or-progression',
            both_nonap_small=inv+r-3+nonap_sharp.nonap_floor(r)+nonap_sharp.nonap_floor(t),
            both_nonap_large=triangular(t)-2-omega,
            ap_two_classes=2*triangular(r)-omega,
            ap_large_side=triangular(37)-omega,
            ap_remaining=omega-triangular(r),
            ap_length=triangular(r)+1-2*t,
            dominant_defect=triangular(t-2)+2-2*t-omega,
            odd_large_mass=(t*t-11*t)//2+2*(triangular(r)+1)+7-omega,
            odd_small_mass_eighths=56*t-289-8*(2*t+72),
            half_step_inner=2513+2*r-4*triangular(r)-2*triangular(t),
            half_step_peeling_margin=154-36-(omega-triangular(r)))
        require(all(inverse_case[k]>0 for k in ('both_nonap_small','both_nonap_large','ap_two_classes','ap_large_side','dominant_defect','odd_small_mass_eighths','half_step_peeling_margin')),'Progression/non-progression gate fails')
        require(inverse_case['ap_remaining']<=75 and inverse_case['half_step_inner']<0,'Half-step repair fails')
        if omega>=triangular(r):
            require(inverse_case['ap_length']>0 and inverse_case['odd_large_mass']>0,'Two-fiber mass gate fails')
        if min(a,b)==14:inner0=innerP=C+3*omega+16
        require(inner0<0 and innerP<0 and outer>0,'Common-lattice gate fails')
        lattice.append(dict(a=a,b=b,omega=omega,inverse=inv,inner_low=inner0,inner_high=innerP,outer=outer,cutoff=cutoff,prefix_inverse=prefix_witness,inverse_case=inverse_case))
        for z in range(omega+1):
            ua,ub=(0,0) if z==0 else (a-3,b-3)
            ra,rb=(0,0) if z==0 else (nonap_sharp.nonap_floor(a),nonap_sharp.nonap_floor(b))
            tmin=max(t0,z,G-2*z)
            if omega-ra-rb-tmin<0:continue
            if z>0 and min(a,b)<17:
                require(min(a,b)==16,'Unhandled small positive-hole side')
                large=max(a,b)
                bound=nonap_hole_rho.lower_bound(large,z)
                require(bound+nonap_sharp.nonap_floor(16)+tmin>omega,'Size-16 side not excluded')
                small_boundary.append(dict(a=a,z=z,large_side=large,large_rho=bound,peeling=tmin,omega=omega))
                continue
            if z>0:require(min(a,b)>=17,'Prefix inverse used below its proved range')
            if z>=3:
                u=[]
                for r in (a,b):
                    eligible=[v for (rr,gamma),v in catalogue.items() if rr==r and 2*gamma<z]
                    require(eligible,'Missing positive-hole witness')
                    best=max(eligible,key=lambda v:(v['C'],-v['beta']))
                    witness=base.hole_row(r,best['C'],best['beta']);witnesses[r,best['C'],best['beta']]=witness
                    u.append(r+best['C']+1)
                ua,ub=u
                ra=nonap_inverse.lower_bound(a,ua)
                rb=nonap_inverse.lower_bound(b,ub)
            if z>0:
                ra=max(ra,nonap_hole_rho.lower_bound(a,z))
                rb=max(rb,nonap_hole_rho.lower_bound(b,z))
                ua=max(ua,ra);ub=max(ub,rb)
            cmax=omega-ra-rb-tmin
            if cmax<0:continue
            if z>0:
                for r0,other in ((a,rb),(b,ra)):
                    surplus=triangular(r0-1)-r0-1+other+tmin-omega
                    second_surplus=triangular(r0-2)-r0-1+other+tmin-omega
                    require(r0>=19 and second_surplus>0,'Second retained prefix not licensed')
                    require(r0>=18 and surplus>0,'AP penultimate prefix survives or sharp floor out of range')
                    prefix_checks.append(dict(a=a,z=z,side_size=r0,other_rho=other,peeling=tmin,omega=omega,retention=retained_prefix.witness(r0,omega-other-tmin,2),surplus=surplus,second_surplus=second_surplus,rho_prefix=r0-6,mu_prefix=r0-4,mu_second_prefix=r0-5))
            if z<=14:
                require(cmax<5*d,'Five empty units possible')
                bandkey=next(k for k,v in BANDS.items() if v['lower']<=z<=v['upper']) if z>0 else None
                if z>0:require(cmax<=BANDS[bandkey]['cap']-I,'Low-hole envelope fails')
                regimes=[]
                for j in range(cmax//d+1):
                    regime=('Z' if z==0 else bandkey)+str(j);regimes.append(regime)
                    lo,hi=RANGES[regime];require(lo<=a<=hi,'Missing low parameter')
                low.append(dict(a=a,b=b,z=z,c_upper=cmax,regimes=regimes))
                continue
            margins=base.active_margins(a,b,z,ua,ub,d)
            reflected=base.active_margins(b,a,z,ub,ua,d)
            active_margin=min(margins)
            require(cmax<3*d,'Three high-hole empty units possible')
            state=dict(a=a,b=b,z=z,c_upper=cmax,mu_p=ua,mu_q=ub,rho_p=ra,rho_q=rb,
                       margins=margins,reflected_margins=reflected,active_margin=active_margin)
            high.append(state)
            for j in range(cmax//d+1):
                if j==0 and active_margin>0:continue
                merged.setdefault((a,j,ua,ub,ra,rb),[]).append(state)
    high_groups=[]
    for (a,j,up,uq,rp,rq),states in sorted(merged.items()):
        high_groups.append(dict(key=f'H{j}:{a}:{up}:{uq}:{rp}:{rq}',a=a,j=j,up=up,uq=uq,rp=rp,rq=rq,
            zmin=min(s['z'] for s in states),zmax=max(s['z'] for s in states),cmax=max(s['c_upper'] for s in states),z_values=[s['z'] for s in states],
            rho_proof_p=dict(prefix=nonap_inverse.lower_bound(a,up),holes=nonap_hole_rho.witness(a,min(s['z'] for s in states))),
            rho_proof_q=dict(prefix=nonap_inverse.lower_bound(m-a,uq),holes=nonap_hole_rho.witness(m-a,min(s['z'] for s in states)))))
    cases=[v['inverse_case'] for v in lattice]
    summary=dict(lattice_orientations=len(lattice),raw_inverse_min=min(v['inverse'] for v in lattice),
                 both_nonap_small_min=min(v['both_nonap_small'] for v in cases),
                 both_nonap_large_min=min(v['both_nonap_large'] for v in cases),
                 ap_remaining_max=max(v['ap_remaining'] for v in cases),
                 half_step_inner_max=max(v['half_step_inner'] for v in cases),
                 half_step_peeling_min=min(v['half_step_peeling_margin'] for v in cases),
                 inner_low_max=max(v['inner_low'] for v in lattice),inner_high_max=max(v['inner_high'] for v in lattice),
                 outer_min=min(v['outer'] for v in lattice),prefix_checks=len(prefix_checks),prefix_surplus_min=min(v['surplus'] for v in prefix_checks),second_prefix_surplus_min=min(v['second_surplus'] for v in prefix_checks),small_boundary_checks=len(small_boundary),low_states=len(low),high_states=len(high),
                 high_c_max=max(v['c_upper'] for v in high),high_active_remaining=sum(s['active_margin']<=0 for s in high),
                 high_empty_states=sum(s['c_upper']>=d for s in high),high_two_empty_states=sum(s['c_upper']>=2*d for s in high),high_merged_groups=len(high_groups))
    return dict(summary=summary,lattice=lattice,prefix_checks=prefix_checks,small_boundary=small_boundary,lattice_witness=lattice_witness,low_envelope=low_hole_envelope_audit(),low_states=low,high_states=high,high_groups=high_groups,
                witnesses=[witnesses[k] for k in sorted(witnesses)])


def mode_key(mode):
    return ':'.join((mode['branch'],','.join(mode['missing']) or '-',mode['choice'],mode['member']))


def roots():
    for regime,(lo,hi) in RANGES.items():
        j=int(regime[-1])
        for mode in modes(j):
            yield dict(key=regime+':'+mode_key(mode),regime=regime,mode=mode,large=None,lo=lo,hi=hi,empty=j)
    for high in scalar_audit()['high_groups']:
        j=high['j'];regime='H'+str(j)
        for mode in modes(j):
            yield dict(key=high['key']+':'+mode_key(mode),regime=regime,mode=mode,large=None,
                       lo=high['a'],hi=high['a'],empty=j,high=high)


def model(g,a,kind):
    require(kind in ('coarse','global_nested'),'Unknown model kind')
    n,r=source_model(g,a,kind)
    transport=g['regime'][0] in BANDS
    endpoint=BANDS[g['regime'][0]]['upper'] if transport else None
    if transport:
        zi=n.index('z')
        for label,(v,b) in r.items():
            if label=='zupper':require(b==endpoint,'Wrong transport endpoint')
            else:require(v[n.index('Sp')]+v[n.index('Sq')]+v[zi]<=0,'Invalid endpoint transport')
        r={k:(v,b-endpoint*v[zi]) for k,(v,b) in r.items()}
    drop={'zlower','zupper'} if transport else set()
    # Retain loss/span budgets at this endpoint; they support the new refinements.
    if kind=='coarse':
        drop.update(k for k in r if k.startswith(('Ag','Bg','envelope','I','Hfull','Htilde','tails_','lead_K')))
        drop.update(k for k in r if k.startswith(('lead_lower_','lead_upper_')) and k[-1] in '123')
        v,b=r['cardinality'];cv,cb=r['coarse2D']
        r['cardinality']=([x+2*y for x,y in zip(v,cv)],b+2*cb);drop.add('coarse2D')
        remove={'K','Cp','Cq','x1','x2','x3','y1','y2','y3','l_star','u_star'}|{x for x in n if x.startswith('g')}
        if transport:remove.add('z')
    else:
        # Retain all five nested levels at this endpoint.

        remove={'z'} if transport else set()
    r={k:v for k,v in r.items() if k not in drop}
    if not remove:return n,r
    keep=[i for i,x in enumerate(n) if x not in remove]
    removed=[i for i,x in enumerate(n) if x in remove]
    for label,(v,_) in r.items():
        require(all(v[i]==0 or n[i]=='z' for i in removed),'Invalid elimination: '+label)
    return [n[i] for i in keep],{k:([v[i] for i in keep],b) for k,(v,b) in r.items()}


def branches(g,a,n):
    """Proved disjunctions for actual (possibly transported) configurations."""
    require(type(a) is int and g['lo']<=a<=g['hi'],'Invalid branch parameter')
    require('K' in n,'Disjunctions need the nested model')
    out={};cent=centers();b=73-a;indices={v:i for i,v in enumerate(n)}
    def rows(items):
        result=[]
        for coeff,rhs in items:
            require(coeff.keys()<=indices.keys(),'Unknown branch coordinate')
            vector=[0]*len(n)
            for name,value in coeff.items():vector[indices[name]]=value
            result.append((vector,rhs))
        return result
    if g['regime'].startswith('H'):
        for side,rsize in (('p',a),('q',b)):
            out['density:'+side]=(rows([(dict(z=1),rsize-3),({'R'+side:-2,'z':1},-2*rsize)]),
                rows([(dict(z=-1),-(rsize-3)),({'R'+side:-2},-(3*rsize-3))]))
    for v in g['mode']['slots']:
        s=v[0];t='q' if s=='p' else 'p';own,opp=(a,b) if s=='p' else (b,a)
        xx=['C'+s,'R'+s]+[('x' if s=='p' else 'y')+str(i) for i in range(1,4)]+['M'+s]
        yy=['C'+t,'R'+t]+[('x' if t=='p' else 'y')+str(i) for i in range(1,4)]+['M'+t]
        out['core:'+v]=(rows([({'l_'+v:-1,'u_'+v:-1},-78)]),
            rows([({'l_'+v:1,'u_'+v:1},77),
                  (add(scale(-1,cent[v]),{'l_'+v:-1,'R'+s:-1}),-78),
                  (add(cent[v],{'u_'+v:-1,'S'+s:-1,'R'+t:-1}),-77)]))
        out['ordinary:'+v+':lower']=(rows([(add(scale(-1,cent[v]),{'l_'+v:-1}),-opp-5)]),
            rows([({'l_'+v:-1},-opp-5),(cent[v],-1)]))
        out['ordinary:'+v+':upper']=(rows([(add(cent[v],{'u_'+v:-1,'S'+s:-1}),-own-4)]),
            rows([({'u_'+v:-1},-own-5),(add(scale(-1,cent[v]),{'S'+s:1}),-1)]))
        for i in range(1,7):
            out[f'inner:{v}:lower:{i}']=(rows([({'l_'+v:-1},-i)]),
                rows([(add(scale(-1,cent[v]),{yy[6-i]:1}),-1)]))
            out[f'inner:{v}:upper:{i}']=(rows([({'u_'+v:-1},-i)]),
                rows([(add(cent[v],{'S'+s:-1,xx[6-i]:1}),0)]))
    member=g['mode']['member']
    if member!='-':
        s=member;t='q' if s=='p' else 'p';v=s+'9';other=t+'9'
        both=rows([(add(scale(-1,cent[other]),{'M'+t:-1}),-1)])
        loss=dict([('delta',-1),('l_star',1),('u_star',1)]+[(f'{e}_{v}',1) for v in g['mode']['slots'] for e in ('l','u')])
        if 'fixed_extra' in n:loss['fixed_extra']=1
        sole=rows([(loss,-row_policy(g)['fixed_loss']),(add(scale(-1,cent[v]),{'l_star':-1,'M'+s:-1}),-82),
                   (add(cent[v],{'u_star':-1,'S'+s:-1,'M'+t:-1}),-81)])
        out['pair:both_or_sole']=(both,sole)
    if 'fixed_extra' in n:
        outer=[s+str(i) for s in 'pq' for i in range(1,5)]
        for label,entry in fixed_scores.catalogue()['labels'].items():
            f={v:c for v,c in zip(outer,entry['coeff']) if c};S='S'+entry['side']
            H='hi_'+label;N='nonpos_'+label
            if H in n:
                out['fixed_high:'+label]=(rows([(add(f,{S:-1}),0),({H:1},0)]),
                    rows([(add(scale(-1,f),{S:1}),-1),({H:-1},-1)]))
            out['fixed_nonpositive:'+label]=(rows([(f,0),({N:-1},-1)]),
                rows([(scale(-1,f),-1),({N:1},0)]))
    return out


def extend_rows(rows,split,side,extra):
    out=dict(rows)
    for i,row in enumerate(extra):
        label=f'split/{split}/{side}/{i}'
        require(label not in out,'Repeated split on path')
        out[label]=row
    return out


def check_coverage(bundle,exhaustive=False):
    require(bundle.get('format')==FORMAT,'Unknown certificate format')
    groups=list(roots());routing,pool=bundle['roots'],bundle['pool']
    require(set(routing)=={g['key'] for g in groups} ,'Missing or extra root')
    counts=Counter();root_counts=Counter();details={};used=set();gaps=[];split_types=Counter()
    for g in groups:root_counts[g['regime']]+=g['hi']-g['lo']+1
    require({k:v for k,v in root_counts.items() if k[0]!='H'}==LOW_COUNTS,'Low root universe changed')

    max_depth=0
    def weight(index):
        require(type(index) is int and 0<=index<len(pool),'Invalid certificate index')
        used.add(index);return pool[index]
    def tree_check(g,a,n,r,node,available,path=(),depth=0):
        nonlocal max_depth
        max_depth=max(max_depth,depth)
        require(isinstance(node,dict),'Malformed tree')
        if set(node)=={'vector'}:
            result=base.check_integer_certificate(n,r,weight(node['vector']))
            gaps.append(result['normalized_gap']);counts['tree_leaves']+=1
            return dict(vector=node['vector'],normalized_gap=result['normalized_gap'])
        require(set(node)=={'split','children'} and isinstance(node['children'],list) and len(node['children'])==2,'Both children required')
        split=node['split'];require(split in available and split not in path,'Invalid or repeated disjunction')
        parts=available[split]
        counts['binary_splits']+=1;split_types[split.split(':')[0]]+=1
        kids=[]
        for side,extra in enumerate(parts):
            rr=extend_rows(r,split,side,extra)
            kids.append(tree_check(g,a,n,rr,node['children'][side],available,path+(split,),depth+1))
        return dict(split=split,children=kids)
    def leaf(g,node,allowed):
        require(set(node)=={'kind','segments','trees'} and node['kind'] in allowed,'Invalid leaf model')
        kind=node['kind'];n,r=model(g,Quadratic(0,1),kind);covered=set();segments=[];tree_results={}
        require(isinstance(node['segments'],list) and isinstance(node['trees'],dict),'Malformed leaf coverage')
        last=g['lo']-1
        for item in node['segments']:
            require(isinstance(item,list) and len(item)==3 and all(type(x) is int for x in item),'Malformed interval')
            lo,hi,index=item;require(g['lo']<=lo<=hi<=g['hi'] and lo>last,'Invalid interval order')
            points=set(range(lo,hi+1));require(not covered&points,'Overlapping intervals');covered|=points;last=hi
            result=interval_certificate(n,r,weight(index),lo,hi)
            counts['interval_checks']+=1;counts['extremum_points']+=result['extremum_points'];gaps.append(result['normalized_gap'])
            segments.append(dict(first=lo,last=hi,vector=index,**result))
            if exhaustive:
                point_gaps=[]
                for a in range(lo,hi+1):
                    nn,rr=model(g,a,kind)
                    require(nn==n and set(rr)==set(r),'Symbolic/numeric matrix shape differs')
                    for label,(v,b) in r.items():
                        require(rr[label][0]==v and rr[label][1]==Quadratic.coerce(b).at(a),'Symbolic/numeric formula differs')
                    point_gaps.append(base.check_integer_certificate(nn,rr,pool[index])['normalized_gap'])
                require(min(point_gaps)==result['normalized_gap'],'Wrong interval maximum')
        for key,node_tree in node['trees'].items():
            require(key==str(int(key)),'Noncanonical integer parameter')
            a=int(key);require(g['lo']<=a<=g['hi'] and a not in covered,'Duplicate or out-of-range tree')
            require(kind.endswith('_nested'),'Tree uses unsupported coarse coordinates')
            covered.add(a);counts['tree_roots']+=1
            nn,rr=model(g,a,kind)
            if exhaustive:
                require(nn==n and set(rr)==set(r),'Tree base matrix differs')
                for label,(v,b) in r.items():
                    require(rr[label][0]==v and rr[label][1]==Quadratic.coerce(b).at(a),'Tree base formula differs')
            tree_results[key]=tree_check(g,a,nn,rr,node_tree,branches(g,a,nn))
        require(covered==set(range(g['lo'],g['hi']+1)),'Missing integer parameter')
        counts['parameter_systems']+=len(covered);counts['leaf_groups']+=1;counts['kind/'+kind]+=1
        return dict(kind=kind,lo=g['lo'],hi=g['hi'],policy=row_policy(g),variables=len(n),rows=len(r),segments=segments,trees=tree_results)
    for g in groups:
        node=routing[g['key']];kind=node.get('kind');counts['route/'+str(kind)]+=1
        details[g['key']]=leaf(g,node,('coarse','global_nested'))
    require(used==set(range(len(pool))),'Unused certificate vector')
    require(counts['tree_leaves']==counts['tree_roots']+counts['binary_splits'],'Broken binary tree identity')
    return dict(root_groups=len(groups),root_systems=sum(root_counts.values()),root_counts=dict(root_counts),
                counts=dict(counts),certified_systems=counts['parameter_systems']+counts['binary_splits'],
                vectors=len(pool),maximum_tree_depth=max_depth,split_types=dict(split_types),
                minimum_normalized_gap=min(gaps),proof_checks=details)


def high_group_audit(scalar,kind='coarse'):
    require(kind in ('coarse','global_nested'),'Unknown grouping model')
    """Every actual state's rows imply the common model with its same hole variable."""
    lookup={(v['a'],v['z']):v for v in scalar['high_states']};row_checks=0
    for high in scalar['high_groups']:
        a,j=high['a'],high['j'];mode=next(modes(j))
        for side in 'pq':
            proof=high['rho_proof_'+side]
            require(max(proof['prefix'],proof['holes']['value'])==high['r'+side],'Unproved common rho floor')
        g=dict(regime='H'+str(j),mode=mode,large=None,lo=a,hi=a,empty=j,high=high)
        n,end=source_model(g,a,kind)
        for z in high['z_values']:
            state=lookup[a,z]
            require(high['zmin']<=z<=high['zmax'],'Hole outside group interval')
            require(state['mu_p']==high['up'] and state['mu_q']==high['uq'],'Merged masses disagree')
            require(state['rho_p']==high['rp'] and state['rho_q']==high['rq'],'Merged rho floors disagree')
            start_high=dict(high,zmin=z,zmax=z,cmax=state['c_upper'])
            nn,start=source_model(dict(g,high=start_high),a,kind,row_policy(g))
            require(nn==n and set(start)==set(end),'Grouped model shape mismatch')
            for label,(v,b) in start.items():
                ev,eb=end[label];require(ev==v,'Grouping changes the matrix')
                require(b<=eb,'Grouped row does not follow from state: '+label)
                row_checks+=1
            excess=531-(a-36)*(a-37)-high['rp']-high['rq']
            require(state['c_upper']==min(excess-z,excess-52,excess-154+2*z),'Coupled cap differs from scalar cap')
    return dict(groups=len(scalar['high_groups']),states=sum(len(g['z_values']) for g in scalar['high_groups']),row_checks=row_checks,method='retain-common-hole-variable',model=kind)


def negative_controls(bundle):
    rejected=[]
    def rejects(label,f):
        try:f()
        except (ValueError,KeyError):rejected.append(label)
        else:raise ValueError('Invalid input accepted: '+label)
    g=next(roots());n,r=model(g,Quadratic(0,1),'coarse')
    rejects('negative_weight',lambda:interval_certificate(n,r,{'Gp':-1},g['lo'],g['hi']))
    rejects('noncontradictory_weight',lambda:interval_certificate(n,r,{'Dp1':1},g['lo'],g['hi']))
    rejects('unknown_row',lambda:interval_certificate(n,r,{'invented':1},g['lo'],g['hi']))
    rejects('interior_vertex_failure',lambda:interval_certificate(['x'],{'r':([0],Quadratic(0,2,-1))},{'r':1},-1,3))
    bad=deepcopy(bundle);del bad['roots'][g['key']]
    rejects('missing_root',lambda:check_coverage(bad))
    bad=deepcopy(bundle);bad['roots'][g['key']]['segments'][0][0]+=1
    rejects('missing_integer',lambda:check_coverage(bad))
    def first_tree(data):
        return next(t for node in data['roots'].values() for t in node['trees'].values())
    bad=deepcopy(bundle);first_tree(bad)['children'].pop()
    rejects('missing_disjunction_child',lambda:check_coverage(bad))
    bad=deepcopy(bundle);t=first_tree(bad);t['children'][0]=deepcopy(t)
    rejects('repeated_disjunction',lambda:check_coverage(bad))
    bad=deepcopy(bundle);first_tree(bad)['split']='invented'
    rejects('unproved_disjunction',lambda:check_coverage(bad))
    for label,condition in (('missing_third_empty_unit',lambda g:g['empty']==3),
                            ('missing_high_one_empty_unit',lambda g:g['regime']=='H1'),
                            ('missing_positive_three_empty_unit',lambda g:g['regime']=='P3'),
                            ('missing_actual_contributor',lambda g:g['mode']['member']=='q')):
        bad=deepcopy(bundle);del bad['roots'][next(h['key'] for h in roots() if condition(h))]
        rejects(label,lambda:check_coverage(bad))
    rejects('unproved_next_cardinality',lambda:scalar_audit(89))
    rejects('invalid_two_empty_core_shortcut',lambda:require(377-2*82<78,'Z2 can have a large loss'))
    rejects('invalid_one_large_shortcut',lambda:require(377-82<2*78,'Z1 can have two large losses'))
    require(scalar_audit()['summary']['high_c_max']<163,'High cap no longer licenses basic leading quantiles')
    require(all(row_policy(g)['quantile']!='core' or row_policy(g)['cap']<78 for g in roots() if g['regime']=='H1'),'Unlicensed high core quantile')
    rejects('raw_inverse_without_dichotomy',lambda:require(scalar_audit()['summary']['raw_inverse_min']>0,'The progression support repair is required'))
    rejects('unproved_nonap_size16',lambda:require(nonap_sharp.nonap_floor(16)==11,'New theorem starts at 17'))
    sharp=nonap_sharp.invariants((1,)+tuple(range(3,19)))
    rejects('false_r_minus4_bound',lambda:require(sharp['rho']>=17-4,'Sharpness counterexample'))
    rejects('unproved_prefix_size16',lambda:nonap_inverse.witness(16,50))
    rejects('nonminimal_integer_inverse',lambda:require(nonap_inverse.inverse_step(1,3)==0,'Integer inverse must reach target'))
    h=next(v for v in scalar_audit()['high_groups'] if v['cmax']+v['zmax']>
           531-(v['a']-36)*(v['a']-37)-v['rp']-v['rq'])
    excess=531-(h['a']-36)*(h['a']-37)-h['rp']-h['rq']
    rejects('uncoupled_hole_and_cap_extrema',lambda:require(h['cmax']+h['zmax']<=excess,'Separate maxima violate the common-hole cap'))
    H=integral_centers.row_hermite([(2,0),(0,1)],2)
    rejects('illegal_nonunit_division',lambda:require(integral_centers.contains(H,[1,0]),'A half-integral coordinate is possible'))
    incomplete=center_integrality_audit()['incomplete_four_empty'][0]['mode']
    rejects('universal_four_empty_integrality',lambda:require(center_integrality(incomplete,True)['complete'],'Unrecovered four-empty modes need partial gaps'))
    for regime in ('Z4','Q3','R3'):
        bad=deepcopy(bundle);del bad['roots'][next(h['key'] for h in roots() if h['regime']==regime)]
        rejects('missing_'+regime,lambda:check_coverage(bad))
    uncharged=next(h for h in roots() if h['regime']=='Z4' and len(row_policy(h)['leading_sides'])<2)
    absent=next(side for side in 'pq' if side not in row_policy(uncharged)['leading_sides'])
    _,rr=source_model(uncharged,uncharged['lo'],'global_nested')
    rejects('uncharged_leading_quantile',lambda:require('lead_basic_lower_'+absent in rr,'An absent own block does not charge its leading loss'))
    rejects('unproved_hole_rho_size16',lambda:nonap_hole_rho.witness(16,19))
    rejects('unproved_dense_prefix_threshold',lambda:nonap_hole_rho.previous.row(36,8,19))
    rejects('unproved_anchor_size17',lambda:nonap_hole_rho.previous.row(36,6,17,True))
    w=nonap_hole_rho.witness(37,215)
    rejects('nonstrict_schedule_hole_threshold',lambda:nonap_hole_rho.validate(37,2*max(w['thresholds']),w['L'],w['value'],w['thresholds']))
    rejects('incomplete_schedule',lambda:nonap_hole_rho.validate(37,215,w['L'],w['value'],w['thresholds'][:-1]))
    rejects('ap_escape_without_margin',lambda:nonap_hole_rho.validate(37,215,w['L'],w['escape']+1,w['thresholds']))
    rejects('false_accumulation',lambda:nonap_hole_rho.validate(37,215,w['L'],w['value'],[2]*len(w['thresholds'])))
    evens=nonap_sharp.invariants(tuple(range(2,42,2)))
    rejects('density_without_size_condition',lambda:require(evens['holes']<=2*(40-20),'The density hypothesis cannot be dropped'))
    rejects('invalid_band_endpoint',lambda:require(BANDS['P']['upper']>=14,'Band P cannot transport a hole count of 14 to endpoint 2'))
    pg=next(g for g in roots() if g['regime']=='P1' and 'p0' in g['mode']['missing'])
    rejects('empty_own_rule_with_holes',lambda:require(row_policy(pg)['fixed_loss']>0,'The empty-own rule needs a full target'))
    fg=next(g for g in roots() if row_policy(g)['fixed_scores'])
    fn,fr=model(fg,37,'global_nested')
    rejects('double_count_charged_high_label',lambda:require('hi_C+11' in fn,'Eight guaranteed high losses are already charged'))
    rejects('missing_fixed_nonpositive_group',lambda:require(len([v for v in fr if v.startswith('nonpos_group_')])==25,'All 26 disjoint groups are required'))
    rejects('clipped_bound_plus_member_loss',lambda:require(4>=5-1+2,'Clipping already includes the target loss'))
    rejects('nonstrict_retention_budget',lambda:retained_prefix.witness(37,triangular(35)-38,2))
    rejects('unproved_second_prefix_size16',lambda:retained_prefix.witness(18,0,2))
    rejects('lost_prefix_hole_factor',lambda:require(2>=4,'A retained prefix can have half the final holes'))
    edge=fixed_score_order.catalogue()['edges'][0]
    rejects('reversed_score_order',lambda:fixed_score_order.validate_edge(edge['upper'],edge['lower']))
    rejects('reversed_nonpositive_indicators',lambda:require(1<=0,'Lower score -1, upper score 1 gives N_lower=1, N_upper=0'))
    rejects('overlapping_high_and_nonpositive',lambda:require(1+1<=1,'The two score events are disjoint'))
    rejects('dropped_mu_rho_compatibility',lambda:require(148>=184,'At size 36 the defect floor already forces support excess at least 184'))
    require(len([v for v in fr if v.startswith('score_sign_clause_')])==fixed_score_order.sign_clauses()['retained_clauses'],'Missing sign clauses')
    trim_example=(-3,0,1);twoD={x+y for x in trim_example for y in trim_example}
    rejects('trimmed_increment_missing_one_pair',lambda:require(len(twoD)<=1+2*len(trim_example)-2,'Two removed extremes can create 2d-1 new sums'))
    state=next(v for v in scalar_audit()['high_states'] if v['active_margin']<=0<min(v['reflected_margins']))
    reflected=min(state['reflected_margins'])
    rejects('arbitrary_reflection_shortcut',lambda:require(state['active_margin']==reflected,'First contributor fixes orientation'))
    return dict(rejected=rejected,orientation_counterexample=dict(a=state['a'],z=state['z'],valid_margin=state['active_margin'],invalid_best_margin=reflected),
                uncoupled_extrema=dict(a=h['a'],b=73-h['a'],cmax=h['cmax'],zmax=h['zmax'],upper_c_plus_z=excess))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates',type=Path,default=DEFAULT_CERTIFICATE)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--exhaustive',action='store_true')
    args=parser.parse_args()
    bundle=json.loads(args.certificates.read_text(encoding='utf-8'))
    scalar=scalar_audit();transport={kind:high_group_audit(scalar,kind) for kind in ('coarse','global_nested')}
    checked=check_coverage(bundle,args.exhaustive);guards=negative_controls(bundle)
    summary=dict(status='PASS',conclusion='N <= 89, continuing the audited N <= 90 foundation',
                 verification_mode='interval-plus-exhaustive' if args.exhaustive else 'symbolic-interval',
                 scalar=scalar['summary'],nonap_finite_base=nonap_sharp.finite_base(),prefix_inverse=nonap_inverse.audit(),hole_rho=nonap_hole_rho.audit(),progression_sumsets=progression_audit(),progression_gaps=progression_gap_audit(),empty_own=empty_own_audit(),full_groups=full_group_audit(),fixed_scores=fixed_scores.audit(),fixed_score_order=fixed_score_order.catalogue(),sign_clauses=fixed_score_order.sign_clauses(),retained_prefix=retained_prefix.audit(),center_integrality=center_integrality_audit(),core_cutoff=core_cutoff_audit(),density=density_audit(),high_grouping=transport,
                 linear={k:v for k,v in checked.items() if k!='proof_checks'},negative_controls=guards)
    paths=[Path(__file__),Path(prior.__file__),Path(prior.prior.__file__),ROOT/'verification/upper99.py',Path(base.__file__),Path(nonap_sharp.__file__),Path(nonap_inverse.__file__),Path(nonap_hole_rho.__file__),Path(nonap_hole_rho.previous.__file__),Path(integral_centers.__file__),Path(fixed_scores.__file__),Path(fixed_score_order.__file__),Path(retained_prefix.__file__),ROOT/'verification/verify.py',ROOT/'verification/exact.py',ROOT/'data/fixed_cover_certificate.json',args.certificates]
    out=dict(summary=summary,scalar_audit=scalar,proof_checks=checked['proof_checks'],
             sha256={str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,default=base.json_default,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,default=base.json_default,indent=2))


if __name__=='__main__':main()
