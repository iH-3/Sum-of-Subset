#!/usr/bin/env python3
"""Exact size-92 exclusion with an AP gate, integer center bases and trimmed sumsets."""
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
import nonap_hole_rho_full as nonap_hole_rho
import integral_centers
base=prior.base
require,add,scale=prior.require,prior.add,prior.scale
Quadratic,triangular,interval_certificate=prior.Quadratic,prior.triangular,prior.interval_certificate
ROOT=prior.ROOT
DEFAULT_CERTIFICATE=ROOT/'data/upper91_certificates.json'
FORMAT='upper91-hermite-ap-gate-trimming-mass-anchored-v1'
BANDS={'P':dict(lower=1,upper=2,cap=281,rho=65,mu_slope=1,mu_intercept=-3),
       'Q':dict(lower=3,upper=4,cap=273,rho=77,mu_slope=1,mu_intercept=6),
       'R':dict(lower=5,upper=14,cap=270,rho=100,mu_slope=2,mu_intercept=-5)}
RANGES={}
for prefix,cap,last in [('Z',342,4)]+[(k,v['cap'],v['cap']//84) for k,v in BANDS.items()]:
    for j in range(last+1):
        valid=[a for a in range(16,60) if (a-37)*(a-38)<=cap-84*j]
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
    for r in range(17,59):
        for L,H in ((15,150),(19,167),(15,15),(50,100)):
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


def row_policy(group):
    lo,hi=group['lo'],group['hi'];j=group['empty']
    Imin=min((a-37)*(a-38) for a in range(lo,hi+1))
    cap=group['high']['cmax']-84*j if 'high' in group else (BANDS[group['regime'][0]]['cap'] if group['regime'][0] in BANDS else 342)-84*j-Imin
    smallest=min(lo,75-hi)
    integral=center_integrality(group['mode'],cap<167)
    policy=dict(cap=cap,quantile='ordinary' if cap<smallest+5 else 'core' if cap<80 else 'global',
                leading_basic=cap<167,leading_nested=cap<159,leading_deep=cap<157,leading_sides=integral['leading_sides'],
                strict_outer=integral['complete'],integral_gaps=integral['integral_gaps'],integral_branch=integral['integral_branch'])
    if 'high' in group:policy['density_interval']=[group['high']['zmin'],group['high']['zmax']]
    return policy

def source_model(group,a,kind,policy_override=None):
    if not isinstance(a,Quadratic):
        require(type(a) is int and group['lo']<=a<=group['hi'],'Parameter outside group')
    regime,mode,large,j=(group[k] for k in ('regime','mode','large','empty'))
    branch,slots,member=(mode[k] for k in ('branch','slots','member'))
    b=75-a
    I=(a-37)*(a-38)
    B0=342-84*j-I
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
            require(min(group['lo'],75-group['hi'])>=band['lower']+3,'Low-band density threshold fails')
            boost=(band['lower']+1)//2
        elif high:
            rr=group['lo'] if side=='p' else 75-group['lo']
            boost=(min(group['high']['zmin'],rr-3)+1)//2
            L,H=policy['density_interval']
            lo,hi=min(L,rr-3),min(H,rr-3)
            if H>L:row('density_chord_'+side,{'R'+side:-2*(H-L),'z':hi-lo},-2*(H-L)*r-lo*(H-L)+(hi-lo)*L)
        row('G'+side,{'R'+side:-1},-r-boost)
        row('H'+side,add({'M'+side:2,'R'+side:6,'S'+side:-2},zcoeff(2)),-2*triangular(r)-12-2*eps)
        row('Hhat'+side,{'M'+side:1,'R'+side:4,'S'+side:-1},-triangular(r-1)-6)
        for i in range(1,5):row(f'I{side}{i}',{xx[i-1]:1,xx[i]:-1},-1)
        row('Hfull'+side,add(add({v:1 for v in xx[1:]},{'S'+side:-1}),zcoeff(1)),-triangular(r)-eps)
        row('Htilde'+side,add({v:1 for v in xx},{'S'+side:-1}),-triangular(r-1))
        row('Icore_min_'+side,{'C'+side:-1},-(r-1))
        row('Icore_gap_'+side,{'C'+side:1,'R'+side:-1},-1)
        row('Hfull_core_'+side,add(add({v:1 for v in xx},{'C'+side:1}),{'S'+side:-1}),-triangular(r-2))
        rmax=group['hi'] if side=='p' else 75-group['lo']
        upper=add({'S'+side:1,'C'+side:-(rmax-1)},scale(-1,{v:1 for v in xx}))
        if positive:upper=add(upper,dict(z=-1))
        row('Hfull_core_upper_'+side,upper,-triangular(r-2)-(band['lower'] if positive else 0))
    row('branch',scale(1 if branch=='A' else -1,add(bp,bq)),0 if branch=='A' or not policy['integral_branch'] else -1)
    if member!='-':
        row('pairnonempty',add(scale(-1,bp if member=='p' else bq),{'M'+member:-1}),-1)
    if positive or high:
        row('zlower',dict(z=-1),-group['high']['zmin'] if high else -band['lower'])
        row('zupper',dict(z=1),group['high']['zmax'] if high else band['upper'])
    row('cap',dict(delta=1),group['high']['cmax']-84*j if high else band['cap']-84*j-I if positive else B0)
    if high:
        excess=500-I-group['high']['rp']-group['high']['rq']-84*j
        row('cap_holes',dict(delta=1,z=1),excess)
        row('cap_constant',dict(delta=1),excess-53)
        row('cap_peeling',dict(delta=1,z=-2),excess-158)
    row('span',add(dict(Rp=1,Rq=1,delta=1),zcoeff(-4)),79+B0)
    for v in slots:
        side=v[0];other='q' if side=='p' else 'p'
        own,opp=(a,b) if side=='p' else (b,a)
        qtype=policy['quantile']
        l=add(scale(-1,centers[v]),{'l_'+v:-1})
        u=add(centers[v],{'u_'+v:-1,'S'+side:-1})
        if qtype=='global':
            l,u=add(l,{'M'+side:-1}),add(u,{'M'+other:-1})
            lr,ur=-84,-83
        elif qtype=='core':
            l,u=add(l,{'R'+side:-1}),add(u,{'R'+other:-1})
            lr,ur=-80,-79
        else:lr,ur=-(opp+5),-(own+4)
        row('L'+v,l,lr);row('U'+v,u,ur)
        # These count caps are valid in the actual-set selection, before relaxation.
        row('slotcap'+v,{'l_'+v:1,'u_'+v:1},79 if qtype=='core' else 83)
    row('loss',dict([('delta',-1)]+[(f'{end}_{v}',1) for v in slots for end in ('l','u')]),0)
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
            row('overlap_hull_'+key+'_'+v,coeff,1-76*len(vv))
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
                            add(add(hull,rest),co),2-76*(len(sub)+2))
    for v in slots:
        if v not in grouped:joint['l_'+v]=1;joint['u_'+v]=1
    if policy['leading_basic']:
        for side,c,xx,yy in (('p',cp,x,y),('q',cq,y,x)):
            if side not in policy['leading_sides']:continue
            row('lead_mass_'+side,{'S'+side:-1,'lead_'+side:-1},-167)
            row('lead_basic_lower_'+side,add(scale(-1,c),{xx[4]:-2,'lead_'+side:-1}),-167)
            row('lead_basic_upper_'+side,add(c,{'S'+side:-1,yy[4]:-2,'lead_'+side:-1}),-166)
            row('lead_Kmass_'+side,{'K':1,'S'+side:-1,'lead_'+side:-1},0)
            row('lead_Klower_'+side,add(scale(-1,c),{'K':1,xx[4]:-2,'lead_'+side:-1}),0)
            row('lead_Kupper_'+side,add(c,{'K':1,'S'+side:-1,yy[4]:-2,'lead_'+side:-1}),1)
            if policy['leading_deep']:
                other='q' if side=='p' else 'p'
                row(f'lead_lower_{side}m1',add(scale(-1,c),{'C'+side:-2,'lead_'+side:-1}),-157)
                row(f'lead_upper_{side}m1',add(c,{'S'+side:-1,'C'+other:-2,'lead_'+side:-1}),-156)
            for i in range(5) if policy['leading_nested'] else ():
                row(f'lead_lower_{side}{i}',add(scale(-1,c),{xx[i]:-2,'lead_'+side:-1}),-159-2*i)
                row(f'lead_upper_{side}{i}',add(c,{'S'+side:-1,yy[i]:-2,'lead_'+side:-1}),-158-2*i)
    row('joint_overlap',joint,0)
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
                    1+triangular(A-i)+triangular(B-h)+84*removed-triangular(removed-1))
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
    row('cardinality',add(dict(Sp=1,Sq=1,delta=1,K=-2),zcoeff(-4)),1596-84*j)
    return names,rows



@lru_cache(maxsize=1)
def hole_catalogue():
    out={}
    for r in range(17,59):
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
    for r in range(17,59):
        for key,beta,C in (('Q',1,5),('R',2,r-6)):
            w=base.hole_row(r,C,beta)
            require(2*beta<BANDS[key]['lower'],'Mass floor used before strict hole threshold')
            require(r+C+1==BANDS[key]['mu_slope']*r+BANDS[key]['mu_intercept'],'Wrong affine support floor')
            mass_witnesses.append(dict(band=key,**w))
    for beta in (1,2):
        cases=[]
        for a in range(17,59):
            b=75-a;witnesses=[];floors=[]
            for r in (a,b):
                w=base.hole_row(r,catalogue[r,beta]['C'],beta)
                u=r+w['C']+1
                witnesses.append(w);floors.append(nonap_inverse.witness(r,u))
            cases.append(dict(a=a,b=b,witnesses=witnesses,inverse=floors,rho_sum=sum(v['value'] for v in floors)))
        minimum=min(v['rho_sum'] for v in cases)
        require(minimum==(77 if beta==1 else 100),'Low-hole envelope floor changed')
        rows.append(dict(beta=beta,minimum_rho_sum=minimum,cases=cases))
    for key,band in BANDS.items():
        require(band['cap']==342-band['rho']+2*band['upper'],'Wrong band cap')
    require(all(3*84<=v['cap']<4*84 for v in BANDS.values()),'Wrong empty-unit thresholds')
    old_positive=sum(sum((a-37)*(a-38)<=305-84*j for a in range(16,60))*sum(1 for _ in modes(j)) for j in range(4))
    new_positive=sum(v for k,v in LOW_COUNTS.items() if k[0] in BANDS)
    return dict(bands=BANDS,uniform_coarse_cap=305,uniform_positive_roots=old_positive,
                band_positive_roots=new_positive,rows=rows,mass_witnesses=mass_witnesses)


@lru_cache(maxsize=1)
def scalar_audit(n=92):
    require(n==92,'This proof does not exclude size 91')
    nonap_sharp.finite_base()
    d,e,m,G,t0=84,76,75,158,53
    qmax=isqrt(96*e+1073-e*e);qmax-=(qmax-e+1)%2
    paired_min=(e-1-qmax)//2
    require(paired_min==13 and 1+triangular(e)>24*n+77,'Sign bootstrap fails')
    catalogue=hole_catalogue()
    lattice,low,high,witnesses,merged=[],[],[],{},{}
    lattice_witness=[]
    for a in range(paired_min,m-paired_min+1):
        b=m-a;I=(a-37)*(a-38);omega=500-I
        if min(a,b)==13:
            require(omega < -8,'Size-13 side not excluded by the general rho floor')
            continue
        if omega<0:continue
        lam=1+triangular(a)+triangular(b);C=2*m+4*e+14-lam
        inv=triangular(min(a,b))-2-omega
        inner0=C+omega+28
        innerP=C+3*omega-(nonap_sharp.nonap_floor(a)+nonap_sharp.nonap_floor(b)+m-6)
        prefix_witness=[]
        if innerP>=0:
            require(min(a,b)>=28,'Effective lattice witness outside range')
            ww=[base.hole_row(r,catalogue[r,7]['C'],7) for r in (a,b)]
            lattice_witness.extend(ww)
            us=[v['r']+v['C']+1 for v in ww]
            prefix_witness=[dict(r=r,u=u,value=max(nonap_inverse.lower_bound(r,u),nonap_hole_rho.lower_bound(r,15)),prefix=nonap_inverse.witness(r,u),holes=nonap_hole_rho.witness(r,15)) for r,u in zip((a,b),us)]
            innerP=C+3*omega-sum(us)-sum(v['value'] for v in prefix_witness)
        outer=lam-(4*d-10+omega)
        inverse_case=dict(route='direct',margin=inv)
        if inv<=0:
            r,t=min(a,b),max(a,b)
            inverse_case=dict(route='nonap-or-progression',small_nonap=inv+2*r-8,large_nonap=inv+t-5,
                ap_no_collision=triangular(r)*triangular(t)-omega,ap_large_step=triangular(t)-omega,
                ap_small_step_three=2*triangular(r)-omega,ap_double_remaining=omega-triangular(r),
                ap_double_peeling_margin=G-(omega-triangular(r)))
            require(all(inverse_case[k]>0 for k in ('small_nonap','large_nonap','ap_no_collision','ap_large_step','ap_small_step_three','ap_double_peeling_margin')),'Conditional inverse gate fails')
        require(inner0<0 and innerP<0 and outer>0,'Common-lattice gate fails')
        lattice.append(dict(a=a,b=b,omega=omega,inverse=inv,inner_low=inner0,inner_high=innerP,outer=outer,prefix_inverse=prefix_witness,inverse_case=inverse_case))
        for z in range(omega+1):
            ua,ub=(0,0) if z==0 else (a-3,b-3)
            ra,rb=(0,0) if z==0 else (nonap_sharp.nonap_floor(a),nonap_sharp.nonap_floor(b))
            tmin=max(t0,z,G-2*z)
            if omega-ra-rb-tmin<0:continue
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
            cmax=omega-ra-rb-tmin
            if cmax<0:continue
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
    exceptional=[v['inverse_case'] for v in lattice if v['inverse']<=0]
    summary=dict(lattice_orientations=len(lattice),raw_inverse_min=min(v['inverse'] for v in lattice),
                 conditional_inverse_orientations=len(exceptional),small_nonap_margin=min(v['small_nonap'] for v in exceptional),
                 large_nonap_margin=min(v['large_nonap'] for v in exceptional),ap_double_remaining_max=max(v['ap_double_remaining'] for v in exceptional),
                 ap_double_peeling_margin=min(v['ap_double_peeling_margin'] for v in exceptional),
                 inner_low_max=max(v['inner_low'] for v in lattice),inner_high_max=max(v['inner_high'] for v in lattice),
                 outer_min=min(v['outer'] for v in lattice),low_states=len(low),high_states=len(high),
                 high_c_max=max(v['c_upper'] for v in high),high_active_remaining=sum(s['active_margin']<=0 for s in high),
                 high_empty_states=sum(s['c_upper']>=d for s in high),high_two_empty_states=sum(s['c_upper']>=2*d for s in high),high_merged_groups=len(high_groups))
    return dict(summary=summary,lattice=lattice,lattice_witness=lattice_witness,low_envelope=low_hole_envelope_audit(),low_states=low,high_states=high,high_groups=high_groups,
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
    out={};cent=centers();b=75-a;indices={v:i for i,v in enumerate(n)}
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
        out['core:'+v]=(rows([({'l_'+v:-1,'u_'+v:-1},-80)]),
            rows([({'l_'+v:1,'u_'+v:1},79),
                  (add(scale(-1,cent[v]),{'l_'+v:-1,'R'+s:-1}),-80),
                  (add(cent[v],{'u_'+v:-1,'S'+s:-1,'R'+t:-1}),-79)]))
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
        sole=rows([(loss,0),(add(scale(-1,cent[v]),{'l_star':-1,'M'+s:-1}),-84),
                   (add(cent[v],{'u_star':-1,'S'+s:-1,'M'+t:-1}),-83)])
        out['pair:both_or_sole']=(both,sole)
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
        counts['binary_splits']+=1;split_types[split.split(':')[0]]+=1
        kids=[]
        for side,extra in enumerate(available[split]):
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


def high_group_audit(scalar):
    """Every actual state's rows imply the common model with its same hole variable."""
    lookup={(v['a'],v['z']):v for v in scalar['high_states']};row_checks=0
    for high in scalar['high_groups']:
        a,j=high['a'],high['j'];mode=next(modes(j))
        for side in 'pq':
            proof=high['rho_proof_'+side]
            require(max(proof['prefix'],proof['holes']['value'])==high['r'+side],'Unproved common rho floor')
        g=dict(regime='H'+str(j),mode=mode,large=None,lo=a,hi=a,empty=j,high=high)
        n,end=source_model(g,a,'coarse')
        for z in high['z_values']:
            state=lookup[a,z]
            require(high['zmin']<=z<=high['zmax'],'Hole outside group interval')
            require(state['mu_p']==high['up'] and state['mu_q']==high['uq'],'Merged masses disagree')
            require(state['rho_p']==high['rp'] and state['rho_q']==high['rq'],'Merged rho floors disagree')
            start_high=dict(high,zmin=z,zmax=z,cmax=state['c_upper'])
            nn,start=source_model(dict(g,high=start_high),a,'coarse',row_policy(g))
            require(nn==n and set(start)==set(end),'Grouped model shape mismatch')
            for label,(v,b) in start.items():
                ev,eb=end[label];require(ev==v,'Grouping changes the matrix')
                require(b<=eb,'Grouped row does not follow from state: '+label)
                row_checks+=1
            excess=500-(a-37)*(a-38)-high['rp']-high['rq']
            require(state['c_upper']==min(excess-z,excess-53,excess-158+2*z),'Coupled cap differs from scalar cap')
    return dict(groups=len(scalar['high_groups']),states=sum(len(g['z_values']) for g in scalar['high_groups']),row_checks=row_checks,method='retain-common-hole-variable')


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
    rejects('unproved_next_cardinality',lambda:scalar_audit(91))
    rejects('invalid_two_empty_core_shortcut',lambda:require(342-2*84<80,'Z2 can have a large loss'))
    rejects('invalid_one_large_shortcut',lambda:require(342-84<2*80,'Z1 can have two large losses'))
    require(scalar_audit()['summary']['high_c_max']<157,'Anchored floor no longer licenses high leading quantiles')
    require(scalar_audit()['summary']['high_c_max']-84<80,'Anchored floor no longer licenses H1 core quantiles')
    rejects('raw_inverse_without_dichotomy',lambda:require(scalar_audit()['summary']['raw_inverse_min']>0,'Fourteen orientations need the AP/non-AP dichotomy'))
    rejects('unproved_nonap_size16',lambda:require(nonap_sharp.nonap_floor(16)==11,'New theorem starts at 17'))
    sharp=nonap_sharp.invariants((1,)+tuple(range(3,19)))
    rejects('false_r_minus4_bound',lambda:require(sharp['rho']>=17-4,'Sharpness counterexample'))
    rejects('unproved_prefix_size16',lambda:nonap_inverse.witness(16,50))
    rejects('nonminimal_integer_inverse',lambda:require(nonap_inverse.inverse_step(1,3)==0,'Integer inverse must reach target'))
    h=next(v for v in scalar_audit()['high_groups'] if v['cmax']+v['zmax']>
           500-(v['a']-37)*(v['a']-38)-v['rp']-v['rq'])
    excess=500-(h['a']-37)*(h['a']-38)-h['rp']-h['rq']
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
    rejects('unproved_dense_prefix_threshold',lambda:nonap_hole_rho.row(36,8,19))
    rejects('unproved_anchor_size17',lambda:nonap_hole_rho.row(36,6,17,True))
    rejects('nonstrict_hole_threshold',lambda:require(nonap_hole_rho.lower_bound(36,18)>=136,'The beta-9 route needs more than 18 holes'))
    evens=nonap_sharp.invariants(tuple(range(2,42,2)))
    rejects('density_without_size_condition',lambda:require(evens['holes']<=2*(40-20),'The density hypothesis cannot be dropped'))
    rejects('invalid_band_endpoint',lambda:require(BANDS['P']['upper']>=14,'Band P cannot transport a hole count of 14 to endpoint 2'))
    trim_example=(-3,0,1);twoD={x+y for x in trim_example for y in trim_example}
    rejects('trimmed_increment_missing_one_pair',lambda:require(len(twoD)<=1+2*len(trim_example)-2,'Two removed extremes can create 2d-1 new sums'))
    state=next(v for v in scalar_audit()['high_states'] if v['active_margin']<=0<min(v['reflected_margins']))
    reflected=min(state['reflected_margins'])
    rejects('arbitrary_reflection_shortcut',lambda:require(state['active_margin']==reflected,'First contributor fixes orientation'))
    return dict(rejected=rejected,orientation_counterexample=dict(a=state['a'],z=state['z'],valid_margin=state['active_margin'],invalid_best_margin=reflected),
                uncoupled_extrema=dict(a=h['a'],b=75-h['a'],cmax=h['cmax'],zmax=h['zmax'],upper_c_plus_z=excess))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates',type=Path,default=DEFAULT_CERTIFICATE)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--exhaustive',action='store_true')
    args=parser.parse_args()
    bundle=json.loads(args.certificates.read_text(encoding='utf-8'))
    scalar=scalar_audit();transport=high_group_audit(scalar)
    checked=check_coverage(bundle,args.exhaustive);guards=negative_controls(bundle)
    summary=dict(status='PASS',conclusion='N <= 91, continuing the audited N <= 92 foundation',
                 verification_mode='interval-plus-exhaustive' if args.exhaustive else 'symbolic-interval',
                 scalar=scalar['summary'],nonap_finite_base=nonap_sharp.finite_base(),prefix_inverse=nonap_inverse.audit(),hole_rho=nonap_hole_rho.audit(),progression_sumsets=progression_audit(),center_integrality=center_integrality_audit(),core_cutoff=core_cutoff_audit(),density=density_audit(),high_grouping=transport,
                 linear={k:v for k,v in checked.items() if k!='proof_checks'},negative_controls=guards)
    paths=[Path(__file__),Path(prior.__file__),Path(prior.prior.__file__),Path(base.__file__),Path(nonap_sharp.__file__),Path(nonap_inverse.__file__),Path(nonap_hole_rho.__file__),Path(integral_centers.__file__),args.certificates]
    out=dict(summary=summary,scalar_audit=scalar,proof_checks=checked['proof_checks'],
             sha256={str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,default=base.json_default,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,default=base.json_default,indent=2))


if __name__=='__main__':main()
