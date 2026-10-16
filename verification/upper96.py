#!/usr/bin/env python3
"""Exact size-97 exclusion with transported holes and selective disjunctions."""
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
base=prior.base
require,add,scale=prior.require,prior.add,prior.scale
Quadratic,triangular,interval_certificate=prior.Quadratic,prior.triangular,prior.interval_certificate
ROOT=prior.ROOT
DEFAULT_CERTIFICATE=ROOT/'data/upper96_certificates.json'
FORMAT='upper96-transported-disjunctions-v1'
RANGES={'Z0':(25,55),'P0':(26,54),'Z1':(28,52),'P1':(29,51),
        'ZL':(32,48),'PL':(33,47),'Z2':(32,48),'P2':(34,46)}
LOW_COUNTS=dict(Z0=124,P0=116,Z1=1750,P1=1610,Z2=9826,P2=7514)


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

def source_model(group,a,kind):
    if not isinstance(a,Quadratic):
        require(type(a) is int and group['lo']<=a<=group['hi'],'Parameter outside group')
    regime,mode,large,j=(group[k] for k in ('regime','mode','large','empty'))
    branch,slots,member=(mode[k] for k in ('branch','slots','member'))
    b=80-a
    I=(a-40)*(a-40)
    B0=248-89*j-I
    positive=regime[0]=='P'
    high=regime.startswith('H')
    epsp,epsq=(a-3,b-3) if positive else (0,0)
    if high:epsp,epsq=group['high']['up']+group['high']['zmax'],group['high']['uq']+group['high']['zmax']
    names=([s+str(i) for s in 'pq' for i in range(1,5)]+
           ['Mp','Mq','Rp','Rq','Sp','Sq','delta','l_star','u_star']+
           [f'{end}_{v}' for v in slots for end in ('l','u')]+
           [s+str(i) for s in 'xy' for i in range(1,4)]+['K']+
           [f'g{s}{t}{i}' for t in range(4) for i in range(t+1,5) for s in 'pq'])
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
    gap=-1 if j<=1 else 0
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
    row('branch',scale(1 if branch=='A' else -1,add(bp,bq)),0 if branch=='A' or j==2 else -1)
    if member!='-':
        row('pairnonempty',add(scale(-1,bp if member=='p' else bq),{'M'+member:-1}),-1)
    if positive:
        row('zlower',dict(z=-1),-1)
        row('zupper',dict(z=1),14)
    row('cap',add(dict(delta=1),zcoeff(-2)),group['high']['cmax']-89*j if high else B0-52 if positive else B0)
    row('span',add(dict(Rp=1,Rq=1,delta=1),zcoeff(-4)),332-I-89*j+4*group['high']['zmax'] if high else 84+B0)
    for v in slots:
        side=v[0];other='q' if side=='p' else 'p'
        own,opp=(a,b) if side=='p' else (b,a)
        qtype='ordinary' if regime=='H1' else 'global' if kind in ('coarse','global_nested') or j==0 or v==large else 'core'
        l=add(scale(-1,centers[v]),{'l_'+v:-1})
        u=add(centers[v],{'u_'+v:-1,'S'+side:-1})
        if qtype=='global':
            l,u=add(l,{'M'+side:-1}),add(u,{'M'+other:-1})
            lr,ur=-89,-88
        elif qtype=='core':
            l,u=add(l,{'R'+side:-1}),add(u,{'R'+other:-1})
            lr,ur=-85,-84
        else:lr,ur=-(opp+5),-(own+4)
        row('L'+v,l,lr);row('U'+v,u,ur)
        # These count caps are valid in the actual-set selection, before relaxation.
        row('slotcap'+v,{'l_'+v:1,'u_'+v:1},84 if qtype=='core' else 88)
    if large:row('large',{'l_'+large:-1,'u_'+large:-1},-85)
    row('loss',dict([('delta',-1)]+[(f'{end}_{v}',1) for v in slots for end in ('l','u')]),0)
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
    row('cardinality',add(dict(Sp=1,Sq=1,delta=1,K=-2),zcoeff(-4)),1686-89*j+(4*group['high']['zmax'] if high else 0))
    return names,rows



@lru_cache(maxsize=1)
def scalar_audit(n=97):
    require(n==97,'This proof does not exclude size 96')
    d,e,m,G,t0=89,81,80,166,56
    qmax=isqrt(96*e+1073-e*e);qmax-=(qmax-e+1)%2
    paired_min=(e-1-qmax)//2
    require(paired_min==17 and 1+triangular(e)>24*n+77,'Sign bootstrap fails')
    catalogue=base.hole_catalogue()
    lattice,low,high,witnesses,merged=[],[],[],{},{}
    for a in range(paired_min,m-paired_min+1):
        b=m-a;I=(a-40)**2;omega=414-I
        if omega<0:continue
        lam=1+triangular(a)+triangular(b);C=2*m+4*e+14-lam
        inv=triangular(min(a,b))-2-omega
        inner0=C+2*omega;innerP=C+3*omega-(2*m-34);outer=lam-(4*d-10+omega)
        require(inv>0 and inner0<0 and innerP<0 and outer>0,'Common-lattice gate fails')
        lattice.append(dict(a=a,b=b,omega=omega,inverse=inv,inner_zero=inner0,inner_positive=innerP,outer=outer))
        for z in range(omega+1):
            ua,ub=(0,0) if z==0 else (a-3,b-3)
            ra,rb=(0,0) if z==0 else (a-14,b-14)
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
                ra=max(a-14,ua+2-2*a,*(prior.flexible_inverse(a,ua,beta) for beta in range(2,11)))
                rb=max(b-14,ub+2-2*b,*(prior.flexible_inverse(b,ub,beta) for beta in range(2,11)))
            cmax=omega-ra-rb-tmin
            if cmax<0:continue
            if z<=14:
                require(cmax<3*d,'Three empty units possible')
                regimes=[]
                for j in range(cmax//d+1):
                    delta=cmax-j*d;prefix='Z' if z==0 else 'P';regime=prefix+str(j)
                    regimes.append(regime)
                    require(delta<=(248-j*d-I if z==0 else 196-j*d-I+2*z),'Low budget identity fails')
                    if j==1:
                        require(delta<2*(d-4),'Two large losses possible')
                        if delta>=d-4:regimes.append(prefix+'L')
                    if j==2:require(delta<d-4,'Two-empty core quantile invalid')
                for regime in regimes:
                    lo,hi=RANGES[regime];require(lo<=a<=hi,'Missing low parameter')
                low.append(dict(a=a,b=b,z=z,c_upper=cmax,regimes=regimes))
                continue
            # For j=0, orient the first pair's actual contributor positively before defining a.
            # The active lemma is valid in that orientation; a reflected estimate is not interchangeable.
            margins=base.active_margins(a,b,z,ua,ub,d)
            reflected=base.active_margins(b,a,z,ub,ua,d)
            active_margin=min(margins)
            require(cmax<2*d,'Two high-hole empty units possible')
            state=dict(a=a,b=b,z=z,c_upper=cmax,mu_p=ua,mu_q=ub,
                       margins=margins,reflected_margins=reflected,active_margin=active_margin)
            high.append(state)
            for j in (0,1):
                if (j==0 and active_margin>0) or (j==1 and cmax<d):continue
                if j==1:require(cmax-d<min(a,b)+5,'H1 ordinary quantile invalid')
                key=(a,j,ua,ub)
                merged.setdefault(key,[]).append(state)
    high_groups=[]
    for (a,j,up,uq),states in sorted(merged.items()):
        zmax=max(s['z'] for s in states);cmax=max(s['c_upper'] for s in states)
        high_groups.append(dict(key=f'H{j}:{a}:{up}:{uq}',a=a,j=j,up=up,uq=uq,
                                zmax=zmax,cmax=cmax,z_values=[s['z'] for s in states]))
    require(len(high_groups)==17,'Unexpected merged high universe')
    h0=[s for s in high if s['active_margin']<=0]
    h1=[s for s in high if s['c_upper']>=d]
    require(len(h0)==117 and {s['a'] for s in h0}==set(range(40,48)),'H0 oriented state list changed')
    summary=dict(lattice_orientations=len(lattice),inverse_min=min(v['inverse'] for v in lattice),
                 inner_zero_max=max(v['inner_zero'] for v in lattice),inner_positive_max=max(v['inner_positive'] for v in lattice),
                 outer_min=min(v['outer'] for v in lattice),low_states=len(low),high_states=len(high),
                 high_c_max=max(v['c_upper'] for v in high),high_active_remaining=len(h0),high_empty_states=len(h1),
                 high_merged_groups=len(high_groups))
    return dict(summary=summary,lattice=lattice,low_states=low,high_states=high,high_groups=high_groups,
                witnesses=[witnesses[k] for k in sorted(witnesses)])


def mode_key(mode):
    return ':'.join((mode['branch'],','.join(mode['missing']) or '-',mode['choice'],mode['member']))


def roots():
    for regime,(lo,hi) in RANGES.items():
        if regime.endswith('L'):continue
        j=int(regime[-1])
        for mode in prior.modes(j):
            yield dict(key=regime+':'+mode_key(mode),regime=regime,mode=mode,large=None,lo=lo,hi=hi,empty=j)
    for high in scalar_audit()['high_groups']:
        j=high['j'];regime='H'+str(j)
        for mode in prior.modes(j):
            yield dict(key=high['key']+':'+mode_key(mode),regime=regime,mode=mode,large=None,
                       lo=high['a'],hi=high['a'],empty=j,high=high)


def children(g):
    require(g['regime'] in ('Z1','P1'),'Invalid loss refinement')
    yield '-',g
    regime=g['regime'][0]+'L';lo,hi=RANGES[regime]
    for v in g['mode']['slots']:
        yield v,dict(g,key=g['key']+'/'+v,regime=regime,lo=lo,hi=hi,large=v)


def model(g,a,kind):
    require(kind in ('coarse','global_nested','core','core_nested','loss','loss_nested'),'Unknown model kind')
    if kind.startswith('core'):require(g['empty']==2,'Core quantiles not justified')
    if kind.startswith('loss'):require(g['regime'] in ('Z1','P1','ZL','PL'),'Invalid loss model')
    n,r=source_model(g,a,kind)
    if 'z' in n:
        zi=n.index('z')
        for label,(v,b) in r.items():
            if label=='zupper':require(b==14,'Wrong transport endpoint')
            else:require(v[n.index('Sp')]+v[n.index('Sq')]+v[zi]<=0,'Invalid endpoint transport')
        r={k:(v,b-14*v[zi]) for k,(v,b) in r.items()}
    drop={'zlower','zupper'}
    # Retain loss/span budgets at this endpoint; they support the new refinements.
    if kind in ('coarse','core','loss'):
        drop.update(k for k in r if k.startswith(('Ag','Bg','envelope','I','Hfull','Htilde')))
        v,b=r['cardinality'];cv,cb=r['coarse2D']
        r['cardinality']=([x+2*y for x,y in zip(v,cv)],b+2*cb);drop.add('coarse2D')
        remove={'K','x1','x2','x3','y1','y2','y3','z','l_star','u_star'}|{x for x in n if x.startswith('g')}
    else:
        # The delivered proof needs only envelope levels 1, 2 and 3.
        drop.update(('envelope0','envelope4'))
        drop.update(k for k in r if k.startswith(('Aggp0','Aggq0','Bggp0','Bggq0')))
        remove={'z'}|{x for x in n if x.startswith(('gp0','gq0'))}
    r={k:v for k,v in r.items() if k not in drop}
    keep=[i for i,x in enumerate(n) if x not in remove]
    for label,(v,_) in r.items():
        require(all(v[i]==0 or n[i]=='z' for i in range(len(n)) if i not in keep),'Invalid elimination: '+label)
    return [n[i] for i in keep],{k:([v[i] for i in keep],b) for k,(v,b) in r.items()}


def branches(g,a,n):
    """Proved disjunctions for actual (possibly transported) configurations."""
    require(type(a) is int and g['lo']<=a<=g['hi'],'Invalid branch parameter')
    require('K' in n,'Disjunctions need the nested model')
    out={};cent=centers();b=80-a
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
    if g['empty']==2 and member!='-':
        s=member;t='q' if s=='p' else 'p';v=s+'9';other=t+'9'
        both=rows([(add(scale(-1,cent[other]),{'M'+t:-1}),-1)])
        loss=dict([('delta',-1),('l_star',1),('u_star',1)]+[(f'{e}_{v}',1) for v in g['mode']['slots'] for e in ('l','u')])
        sole=rows([(loss,0),(add(scale(-1,cent[v]),{'l_star':-1,'R'+s:-1}),-85),
                   (add(cent[v],{'u_star':-1,'S'+s:-1,'R'+t:-1}),-84)])
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
    require(set(routing)=={g['key'] for g in groups} and len(groups)==1966,'Missing or extra root')
    counts=Counter();root_counts=Counter();details={};used=set();gaps=[];split_types=Counter()
    for g in groups:root_counts[g['regime']]+=g['hi']-g['lo']+1
    require({k:v for k,v in root_counts.items() if k[0]!='H'}==LOW_COUNTS,'Low root universe changed')
    require(root_counts['H0']==32 and root_counts['H1']==630,'High root universe changed')
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
        return dict(kind=kind,lo=g['lo'],hi=g['hi'],variables=len(n),rows=len(r),segments=segments,trees=tree_results)
    for g in groups:
        node=routing[g['key']];kind=node.get('kind');counts['route/'+str(kind)]+=1
        if kind=='split':
            require(set(node)=={'kind','children'},'Malformed loss refinement')
            expected=dict(children(g));require(set(node['children'])==set(expected),'Missing large-loss outcome')
            details[g['key']]=dict(kind=kind,children={v:leaf(h,node['children'][v],('loss','loss_nested')) for v,h in expected.items()})
        else:details[g['key']]=leaf(g,node,('coarse','global_nested','core','core_nested'))
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
        a,j=high['a'],high['j'];mode=next(prior.modes(j))
        g=dict(regime='H'+str(j),mode=mode,large=None,lo=a,hi=a,empty=j,high=high)
        n,end=source_model(g,a,'coarse')
        for z in high['z_values']:
            state=lookup[a,z]
            require(state['mu_p']==high['up'] and state['mu_q']==high['uq'],'Merged masses disagree')
            start_high=dict(high,zmax=z,cmax=state['c_upper'])
            nn,start=source_model(dict(g,high=start_high),a,'coarse')
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
    bad2=deepcopy(bundle);bad2['roots'][g['key']]['segments'][0][0]+=1
    rejects('missing_integer',lambda:check_coverage(bad2))
    split=next(k for k,v in bundle['roots'].items() if v['kind']=='split')
    bad3=deepcopy(bundle);del bad3['roots'][split]['children']['p0' if 'p0' in bad3['roots'][split]['children'] else next(k for k in bad3['roots'][split]['children'] if k!='-')]
    rejects('missing_large_loss_choice',lambda:check_coverage(bad3))
    def first_tree(data):
        for node in data['roots'].values():
            for leaf in node['children'].values() if node['kind']=='split' else [node]:
                if leaf['trees']:return next(iter(leaf['trees'].values()))
        raise ValueError('No tree')
    bad4=deepcopy(bundle);first_tree(bad4)['children'].pop()
    rejects('missing_disjunction_child',lambda:check_coverage(bad4))
    bad5=deepcopy(bundle);t=first_tree(bad5);t['children'][0]=deepcopy(t)
    rejects('repeated_disjunction',lambda:check_coverage(bad5))
    bad6=deepcopy(bundle);first_tree(bad6)['split']='invented'
    rejects('unproved_disjunction',lambda:check_coverage(bad6))
    rejects('unjustified_core_quantiles',lambda:model(g,40,'core'))
    member=next(g['key'] for g in roots() if g['mode']['member']=='q')
    bad7=deepcopy(bundle);del bad7['roots'][member]
    rejects('missing_actual_contributor',lambda:check_coverage(bad7))
    rejects('unproved_next_cardinality',lambda:scalar_audit(96))
    rejects('invalid_P2_ordinary_shortcut',lambda:require(46<40+5,'P2 budget crosses ordinary threshold'))
    # This real scalar state is retained in the valid orientation but would be
    # incorrectly discarded by selecting the larger of reflected estimates.
    state=next(v for v in scalar_audit()['high_states'] if v['a']==47 and v['z']==112)
    reflected=max(min(state['margins']),min(state['reflected_margins']))
    require(state['active_margin']<=0 and reflected>0,'Orientation counterexample changed')
    rejects('arbitrary_reflection_shortcut',lambda:require(state['active_margin']==reflected,'First contributor fixes orientation'))
    return dict(rejected=rejected,orientation_counterexample=dict(a=47,z=112,valid_margin=state['active_margin'],invalid_best_margin=reflected))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates',type=Path,default=DEFAULT_CERTIFICATE)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--exhaustive',action='store_true')
    args=parser.parse_args()
    bundle=json.loads(args.certificates.read_text(encoding='utf-8'))
    scalar=scalar_audit();transport=high_transport_audit(scalar)
    checked=check_coverage(bundle,args.exhaustive);guards=negative_controls(bundle)
    summary=dict(status='PASS',conclusion='N <= 96, continuing the audited N <= 97 foundation',
                 verification_mode='interval-plus-exhaustive' if args.exhaustive else 'symbolic-interval',
                 scalar=scalar['summary'],high_transport=transport,
                 linear={k:v for k,v in checked.items() if k!='proof_checks'},negative_controls=guards)
    paths=[Path(__file__),Path(prior.__file__),Path(prior.prior.__file__),Path(base.__file__),args.certificates]
    out=dict(summary=summary,scalar_audit=scalar,proof_checks=checked['proof_checks'],
             sha256={str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,default=base.json_default,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,default=base.json_default,indent=2))


if __name__=='__main__':main()
