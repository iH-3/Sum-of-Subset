#!/usr/bin/env python3
"""Exact Size-95 exclusion with joint overlap budgets and transported holes."""
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
base=prior.base
require,add,scale=prior.require,prior.add,prior.scale
Quadratic,triangular,interval_certificate=prior.Quadratic,prior.triangular,prior.interval_certificate
ROOT=prior.ROOT
DEFAULT_CERTIFICATE=ROOT/'data/upper94_certificates.json'
FORMAT='upper94-sharp-nonap-v1'
RANGES={}
for prefix,cap,last in (('Z',286,3),('P',246,2)):
    for j in range(last+1):
        valid=[a for a in range(18,61) if (a-39)*(a-39)<=cap-87*j]
        RANGES[prefix+str(j)]=(min(valid),max(valid))


def modes(j):
    from itertools import combinations
    require(type(j) is int and 0<=j<=3,'Unsupported empty-unit count')
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

def row_policy(group):
    lo,hi=group['lo'],group['hi'];j=group['empty']
    Imin=min((a-39)**2 for a in range(lo,hi+1))
    cap=group['high']['cmax']-87*j if 'high' in group else (246 if group['regime'][0]=='P' else 286)-87*j-Imin
    smallest=min(lo,78-hi)
    return dict(cap=cap,quantile='ordinary' if cap<smallest+5 else 'core' if cap<83 else 'global',
                leading_basic=cap<173,leading_nested=cap<165,strict_outer=j<=1 or (j==2 and cap<173))

def source_model(group,a,kind,policy_override=None):
    if not isinstance(a,Quadratic):
        require(type(a) is int and group['lo']<=a<=group['hi'],'Parameter outside group')
    regime,mode,large,j=(group[k] for k in ('regime','mode','large','empty'))
    branch,slots,member=(mode[k] for k in ('branch','slots','member'))
    b=78-a
    I=(a-39)*(a-39)
    B0=286-87*j-I
    positive=regime[0]=='P'
    high=regime.startswith('H')
    epsp,epsq=(a-3,b-3) if positive else (0,0)
    if high:epsp,epsq=group['high']['up']+group['high']['zmax'],group['high']['uq']+group['high']['zmax']
    names=([s+str(i) for s in 'pq' for i in range(1,5)]+
           ['Mp','Mq','Rp','Rq','Sp','Sq','delta','l_star','u_star']+
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
    if positive:names.append('z')
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
    def row(label,coeff,rhs):
        require(label not in rows and set(coeff)<=set(names),'Duplicate row or unknown variable')
        require(all(type(x) is int for x in coeff.values()),'Noninteger model matrix')
        rows[label]=([coeff.get(v,0) for v in names],rhs)
    def zcoeff(value):return {'z':value} if positive else {}
    gap=-1 if policy['strict_outer'] else 0
    x,y=['Rp','x1','x2','x3','Mp'],['Rq','y1','y2','y3','Mq']
    for side,r,eps,xx in (('p',a,epsp,x),('q',b,epsq,y)):
        for i in range(1,4):row(f'D{side}{i}',{side+str(i+1):1,side+str(i):-1},gap)
        row(f'D{side}4',{'M'+side:1,side+'4':-1},gap)
        row('E'+side,{'R'+side:1,'M'+side:-1},-4)
        row('G'+side,{'R'+side:-1},-r)
        row('H'+side,add({'M'+side:2,'R'+side:6,'S'+side:-2},zcoeff(2)),-2*triangular(r)-12-2*eps)
        row('Hhat'+side,{'M'+side:1,'R'+side:4,'S'+side:-1},-triangular(r-1)-6)
        for i in range(1,5):row(f'I{side}{i}',{xx[i-1]:1,xx[i]:-1},-1)
        row('Hfull'+side,add(add({v:1 for v in xx[1:]},{'S'+side:-1}),zcoeff(1)),-triangular(r)-eps)
        row('Htilde'+side,add({v:1 for v in xx},{'S'+side:-1}),-triangular(r-1))
    row('branch',scale(1 if branch=='A' else -1,add(bp,bq)),0 if branch=='A' or not policy['strict_outer'] else -1)
    if member!='-':
        row('pairnonempty',add(scale(-1,bp if member=='p' else bq),{'M'+member:-1}),-1)
    if positive:
        row('zlower',dict(z=-1),-1)
        row('zupper',dict(z=1),14)
    row('cap',add(dict(delta=1),zcoeff(-2)),group['high']['cmax']-87*j if high else B0-68 if positive else B0)
    row('span',add(dict(Rp=1,Rq=1,delta=1),zcoeff(-4)),368-I-87*j+4*group['high']['zmax'] if high else 82+B0)
    for v in slots:
        side=v[0];other='q' if side=='p' else 'p'
        own,opp=(a,b) if side=='p' else (b,a)
        qtype=policy['quantile']
        l=add(scale(-1,centers[v]),{'l_'+v:-1})
        u=add(centers[v],{'u_'+v:-1,'S'+side:-1})
        if qtype=='global':
            l,u=add(l,{'M'+side:-1}),add(u,{'M'+other:-1})
            lr,ur=-87,-86
        elif qtype=='core':
            l,u=add(l,{'R'+side:-1}),add(u,{'R'+other:-1})
            lr,ur=-83,-82
        else:lr,ur=-(opp+5),-(own+4)
        row('L'+v,l,lr);row('U'+v,u,ur)
        # These count caps are valid in the actual-set selection, before relaxation.
        row('slotcap'+v,{'l_'+v:1,'u_'+v:1},82 if qtype=='core' else 86)
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
            row('overlap_hull_'+key+'_'+v,coeff,1-79*len(vv))
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
                            add(add(hull,rest),co),2-79*(len(sub)+2))
    for v in slots:
        if v not in grouped:joint['l_'+v]=1;joint['u_'+v]=1
    if policy['leading_basic']:
        for side,c,xx,yy in (('p',cp,x,y),('q',cq,y,x)):
            row('lead_mass_'+side,{'S'+side:-1,'lead_'+side:-1},-173)
            row('lead_basic_lower_'+side,add(scale(-1,c),{xx[4]:-2,'lead_'+side:-1}),-173)
            row('lead_basic_upper_'+side,add(c,{'S'+side:-1,yy[4]:-2,'lead_'+side:-1}),-172)
            row('lead_Kmass_'+side,{'K':1,'S'+side:-1,'lead_'+side:-1},0)
            row('lead_Klower_'+side,add(scale(-1,c),{'K':1,xx[4]:-2,'lead_'+side:-1}),0)
            row('lead_Kupper_'+side,add(c,{'K':1,'S'+side:-1,yy[4]:-2,'lead_'+side:-1}),1)
            for i in range(5) if policy['leading_nested'] else ():
                row(f'lead_lower_{side}{i}',add(scale(-1,c),{xx[i]:-2,'lead_'+side:-1}),-165-2*i)
                row(f'lead_upper_{side}{i}',add(c,{'S'+side:-1,yy[i]:-2,'lead_'+side:-1}),-164-2*i)
    row('joint_overlap',joint,0)
    for i in range(5):
        for h in range(5):
            row(f'tails_{i}_{h}',add(dict(K=1,Mp=-1,Mq=-1),{x[i]:-1,y[h]:-1}),
                1+triangular(4-i)+triangular(4-h))
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
    row('cardinality',add(dict(Sp=1,Sq=1,delta=1,K=-2),zcoeff(-4)),1650-87*j+(4*group['high']['zmax'] if high else 0))
    return names,rows



@lru_cache(maxsize=1)
def scalar_audit(n=95):
    require(n==95,'This proof does not exclude size 94')
    nonap_sharp.finite_base()
    d,e,m,G,t0=87,79,78,164,55
    qmax=isqrt(96*e+1073-e*e);qmax-=(qmax-e+1)%2
    paired_min=(e-1-qmax)//2
    require(paired_min==15 and 1+triangular(e)>24*n+77,'Sign bootstrap fails')
    catalogue=base.hole_catalogue()
    lattice,low,high,witnesses,merged=[],[],[],{},{}
    lattice_witness=base.hole_row(33,89,7)
    for a in range(paired_min,m-paired_min+1):
        b=m-a;I=(a-39)*(a-39);omega=450-I
        if omega<0:continue
        lam=1+triangular(a)+triangular(b);C=2*m+4*e+14-lam
        inv=triangular(min(a,b))-2-omega
        inner0=C+omega+28
        innerP=C+3*omega-(2*m-34)
        if innerP>=0:
            require(min(a,b)>=33,'Effective lattice witness outside range')
            for r in (a,b):base.hole_row(r,89,7)
            innerP=C+3*omega-((m-28)+(m+180))
        outer=lam-(4*d-10+omega)
        require(inv>0 and inner0<0 and innerP<0 and outer>0,'Common-lattice gate fails')
        lattice.append(dict(a=a,b=b,omega=omega,inverse=inv,inner_low=inner0,inner_high=innerP,outer=outer))
        for z in range(omega+1):
            ua,ub=(0,0) if z==0 else (a-3,b-3)
            ra,rb=(0,0) if z==0 else (nonap_sharp.nonap_floor(a),nonap_sharp.nonap_floor(b))
            tmin=max(t0,z,G-2*z)
            if omega-ra-rb-tmin<0:continue
            if z>=15:
                u=[]
                for r in (a,b):
                    eligible=[v for (rr,gamma),v in catalogue.items() if rr==r and 2*gamma<z]
                    require(eligible,'Missing high-hole witness')
                    best=max(eligible,key=lambda v:(v['C'],-v['beta']))
                    witness=base.hole_row(r,best['C'],best['beta']);witnesses[r,best['C'],best['beta']]=witness
                    u.append(r+best['C']+1)
                ua,ub=u
                ra=max(nonap_sharp.nonap_floor(a),ua+2-2*a,*(prior.flexible_inverse(a,ua,beta) for beta in range(2,11)))
                rb=max(nonap_sharp.nonap_floor(b),ub+2-2*b,*(prior.flexible_inverse(b,ub,beta) for beta in range(2,11)))
            cmax=omega-ra-rb-tmin
            if cmax<0:continue
            if z<=14:
                require(cmax<4*d,'Four empty units possible')
                if z>0:require(cmax<3*d,'Positive three-empty family was not eliminated')
                regimes=[]
                for j in range(cmax//d+1):
                    regime=('Z' if z==0 else 'P')+str(j);regimes.append(regime)
                    lo,hi=RANGES[regime];require(lo<=a<=hi,'Missing low parameter')
                low.append(dict(a=a,b=b,z=z,c_upper=cmax,regimes=regimes))
                continue
            margins=base.active_margins(a,b,z,ua,ub,d)
            reflected=base.active_margins(b,a,z,ub,ua,d)
            active_margin=min(margins)
            require(cmax<2*d,'Two high-hole empty units possible')
            state=dict(a=a,b=b,z=z,c_upper=cmax,mu_p=ua,mu_q=ub,
                       margins=margins,reflected_margins=reflected,active_margin=active_margin)
            high.append(state)
            for j in (0,1):
                if (j==0 and active_margin>0) or (j==1 and cmax<d):continue
                merged.setdefault((a,j,ua,ub),[]).append(state)
    high_groups=[]
    for (a,j,up,uq),states in sorted(merged.items()):
        high_groups.append(dict(key=f'H{j}:{a}:{up}:{uq}',a=a,j=j,up=up,uq=uq,
            zmax=max(s['z'] for s in states),cmax=max(s['c_upper'] for s in states),z_values=[s['z'] for s in states]))
    summary=dict(lattice_orientations=len(lattice),inverse_min=min(v['inverse'] for v in lattice),
                 inner_low_max=max(v['inner_low'] for v in lattice),inner_high_max=max(v['inner_high'] for v in lattice),
                 outer_min=min(v['outer'] for v in lattice),low_states=len(low),high_states=len(high),
                 high_c_max=max(v['c_upper'] for v in high),high_active_remaining=sum(s['active_margin']<=0 for s in high),
                 high_empty_states=sum(s['c_upper']>=d for s in high),high_merged_groups=len(high_groups))
    return dict(summary=summary,lattice=lattice,lattice_witness=lattice_witness,low_states=low,high_states=high,high_groups=high_groups,
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
    if 'z' in n:
        zi=n.index('z')
        for label,(v,b) in r.items():
            if label=='zupper':require(b==14,'Wrong transport endpoint')
            else:require(v[n.index('Sp')]+v[n.index('Sq')]+v[zi]<=0,'Invalid endpoint transport')
        r={k:(v,b-14*v[zi]) for k,(v,b) in r.items()}
    drop={'zlower','zupper'}
    # Retain loss/span budgets at this endpoint; they support the new refinements.
    if kind=='coarse':
        drop.update(k for k in r if k.startswith(('Ag','Bg','envelope','I','Hfull','Htilde','tails_','lead_K')))
        drop.update(k for k in r if k.startswith(('lead_lower_','lead_upper_')) and k[-1] in '123')
        v,b=r['cardinality'];cv,cb=r['coarse2D']
        r['cardinality']=([x+2*y for x,y in zip(v,cv)],b+2*cb);drop.add('coarse2D')
        remove={'K','x1','x2','x3','y1','y2','y3','z','l_star','u_star'}|{x for x in n if x.startswith('g')}
    else:
        # Retain all five nested levels at this endpoint.

        remove={'z'}
    r={k:v for k,v in r.items() if k not in drop}
    keep=[i for i,x in enumerate(n) if x not in remove]
    for label,(v,_) in r.items():
        require(all(v[i]==0 or n[i]=='z' for i in range(len(n)) if i not in keep),'Invalid elimination: '+label)
    return [n[i] for i in keep],{k:([v[i] for i in keep],b) for k,(v,b) in r.items()}


def branches(g,a,n):
    """Proved disjunctions for actual (possibly transported) configurations."""
    require(type(a) is int and g['lo']<=a<=g['hi'],'Invalid branch parameter')
    require('K' in n,'Disjunctions need the nested model')
    out={};cent=centers();b=78-a
    def rows(items):
        result=[]
        for coeff,rhs in items:
            require(set(coeff)<=set(n),'Unknown branch coordinate')
            result.append(([coeff.get(v,0) for v in n],rhs))
        return result
    for v in g['mode']['slots']:
        s=v[0];t='q' if s=='p' else 'p';own,opp=(a,b) if s=='p' else (b,a)
        xx=['R'+s]+[('x' if s=='p' else 'y')+str(i) for i in range(1,4)]+['M'+s]
        yy=['R'+t]+[('x' if t=='p' else 'y')+str(i) for i in range(1,4)]+['M'+t]
        out['core:'+v]=(rows([({'l_'+v:-1,'u_'+v:-1},-83)]),
            rows([({'l_'+v:1,'u_'+v:1},82),
                  (add(scale(-1,cent[v]),{'l_'+v:-1,'R'+s:-1}),-83),
                  (add(cent[v],{'u_'+v:-1,'S'+s:-1,'R'+t:-1}),-82)]))
        out['ordinary:'+v+':lower']=(rows([(add(scale(-1,cent[v]),{'l_'+v:-1}),-opp-5)]),
            rows([({'l_'+v:-1},-opp-5),(cent[v],-1)]))
        out['ordinary:'+v+':upper']=(rows([(add(cent[v],{'u_'+v:-1,'S'+s:-1}),-own-4)]),
            rows([({'u_'+v:-1},-own-5),(add(scale(-1,cent[v]),{'S'+s:1}),-1)]))
        for i in range(1,5):
            out[f'inner:{v}:lower:{i}']=(rows([({'l_'+v:-1},-i)]),
                rows([(add(scale(-1,cent[v]),{yy[5-i]:1}),-1)]))
            out[f'inner:{v}:upper:{i}']=(rows([({'u_'+v:-1},-i)]),
                rows([(add(cent[v],{'S'+s:-1,xx[5-i]:1}),0)]))
    member=g['mode']['member']
    if member!='-':
        s=member;t='q' if s=='p' else 'p';v=s+'9';other=t+'9'
        both=rows([(add(scale(-1,cent[other]),{'M'+t:-1}),-1)])
        loss=dict([('delta',-1),('l_star',1),('u_star',1)]+[(f'{e}_{v}',1) for v in g['mode']['slots'] for e in ('l','u')])
        sole=rows([(loss,0),(add(scale(-1,cent[v]),{'l_star':-1,'M'+s:-1}),-87),
                   (add(cent[v],{'u_star':-1,'S'+s:-1,'M'+t:-1}),-86)])
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


def high_transport_audit(scalar):
    """Check endpoint dominance on every retained high state; rows cover both signs."""
    lookup={(v['a'],v['z']):v for v in scalar['high_states']};row_checks=0
    for high in scalar['high_groups']:
        a,j=high['a'],high['j'];mode=next(modes(j))
        g=dict(regime='H'+str(j),mode=mode,large=None,lo=a,hi=a,empty=j,high=high)
        n,end=source_model(g,a,'coarse')
        for z in high['z_values']:
            state=lookup[a,z]
            require(state['mu_p']==high['up'] and state['mu_q']==high['uq'],'Merged masses disagree')
            start_high=dict(high,zmax=z,cmax=state['c_upper'])
            nn,start=source_model(dict(g,high=start_high),a,'coarse',row_policy(g))
            require(nn==n and set(start)==set(end),'Transport model shape mismatch')
            t=high['zmax']-z;require(t>=0,'Negative mass transport')
            for label,(v,b) in start.items():
                ev,eb=end[label];require(ev==v,'Transport changes the matrix')
                require(b+t*(v[n.index('Sp')]+v[n.index('Sq')])<=eb,'High transport fails: '+label)
                row_checks+=1
    return dict(groups=len(scalar['high_groups']),states=sum(len(g['z_values']) for g in scalar['high_groups']),row_checks=row_checks)


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
                            ('missing_actual_contributor',lambda g:g['mode']['member']=='q')):
        bad=deepcopy(bundle);del bad['roots'][next(h['key'] for h in roots() if condition(h))]
        rejects(label,lambda:check_coverage(bad))
    rejects('unproved_next_cardinality',lambda:scalar_audit(94))
    rejects('invalid_two_empty_core_shortcut',lambda:require(112<83,'Z2 can have a large loss'))
    rejects('invalid_one_large_shortcut',lambda:require(199<2*83,'Z1 can have two large losses'))
    rejects('invalid_H1_core_shortcut',lambda:require(84<83,'High residual loss can reach 84'))
    rejects('invalid_high_nested_leading',lambda:require(171<165,'Nested threshold is smaller than basic threshold'))
    rejects('unproved_nonap_size16',lambda:require(nonap_sharp.nonap_floor(16)==11,'New theorem starts at 17'))
    sharp=nonap_sharp.invariants((1,)+tuple(range(3,19)))
    rejects('false_r_minus4_bound',lambda:require(sharp['rho']>=17-4,'Sharpness counterexample'))
    state=next(v for v in scalar_audit()['high_states'] if v['active_margin']<=0<min(v['reflected_margins']))
    reflected=min(state['reflected_margins'])
    rejects('arbitrary_reflection_shortcut',lambda:require(state['active_margin']==reflected,'First contributor fixes orientation'))
    return dict(rejected=rejected,orientation_counterexample=dict(a=state['a'],z=state['z'],valid_margin=state['active_margin'],invalid_best_margin=reflected))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates',type=Path,default=DEFAULT_CERTIFICATE)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--exhaustive',action='store_true')
    args=parser.parse_args()
    bundle=json.loads(args.certificates.read_text(encoding='utf-8'))
    scalar=scalar_audit();transport=high_transport_audit(scalar)
    checked=check_coverage(bundle,args.exhaustive);guards=negative_controls(bundle)
    summary=dict(status='PASS',conclusion='N <= 94, continuing the audited N <= 95 foundation',
                 verification_mode='interval-plus-exhaustive' if args.exhaustive else 'symbolic-interval',
                 scalar=scalar['summary'],nonap_finite_base=nonap_sharp.finite_base(),high_transport=transport,
                 linear={k:v for k,v in checked.items() if k!='proof_checks'},negative_controls=guards)
    paths=[Path(__file__),Path(prior.__file__),Path(prior.prior.__file__),Path(base.__file__),Path(nonap_sharp.__file__),args.certificates]
    out=dict(summary=summary,scalar_audit=scalar,proof_checks=checked['proof_checks'],
             sha256={str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,default=base.json_default,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,default=base.json_default,indent=2))


if __name__=='__main__':main()
