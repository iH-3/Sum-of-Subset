#!/usr/bin/env python3
"""Exact continuation 98 -> 97 with a unified hole/loss/span model.

Python 3.10+, standard library only. The report proves the structural reduction;
this program verifies its finite gates and complete integer certificates.
Quadratic interval checking is inherited from upper98. --exhaustive also checks
every integer side size and compares every symbolic and numerical row.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from math import isqrt
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import upper100 as base
import upper98 as prior
require,add,scale=base.require,base.add,base.scale
Quadratic,triangular,interval_certificate=prior.Quadratic,prior.triangular,prior.interval_certificate
ROOT=Path(__file__).resolve().parents[1]
DEFAULT_CERTIFICATE=ROOT/'data/upper97_certificates.json'
RANGES={'Z0':(26,55),'P0':(27,54),'Z1':(29,52),'P1':(30,51),
        'ZL':(34,47),'PL':(36,45),'Z2':(34,47),'P2':(36,45),'H1':(40,41)}
EXPECTED_COUNTS=dict(Z0=120,P0=112,Z1=1680,P1=1540,ZL=16604,PL=11860,Z2=8092,P2=5780,H1=140)


def modes(empty_count):
    require(type(empty_count) is int and empty_count in (0,1,2),'Unsupported empty-unit count')
    for branch,j in (('A',9),('B',5)):
        singles=[s+str(i) for s in 'pq' for i in range(10) if i not in (4,j)]
        for missing in combinations(['pair1','pair2']+singles,empty_count):
            split=branch=='A' and 'pair2' not in missing and ('p5' in missing or 'q5' in missing)
            choices=['-'] if 'pair2' in missing or split else ['p','q']
            for choice in choices:
                slots=[v for v in singles if v not in missing]
                if 'pair1' not in missing:slots.append('p4')
                if choice!='-':slots.append(choice+str(j))
                for member in ('p','q') if split else ('-',):
                    yield dict(branch=branch,missing=missing,choice=choice,member=member,slots=slots)


def case_groups():
    for regime,(lo,hi) in RANGES.items():
        empty=1 if regime[-1]=='L' else int(regime[-1])
        for mode in modes(empty):
            for large in mode['slots'] if regime[-1]=='L' else (None,):
                key=':'.join((regime,mode['branch'],','.join(mode['missing']) or '-',mode['choice'],mode['member']))
                if large:key+=':'+large
                yield dict(key=key,regime=regime,mode=mode,large=large,lo=lo,hi=hi,empty=empty)


def model(group,a):
    if not isinstance(a,Quadratic):
        require(type(a) is int and group['lo']<=a<=group['hi'],'Parameter outside group')
    regime,mode,large,j=(group[k] for k in ('regime','mode','large','empty'))
    branch,slots,member=(mode[k] for k in ('branch','slots','member'))
    b=81-a
    I=(a-40)*(a-41)
    B0=227-90*j-I
    positive=regime[0]=='P'
    high=regime=='H1'
    epsp,epsq=(a-3,b-3) if positive else (0,0)
    if high:epsp,epsq=240+9*(a-40),249-9*(a-40)
    names=([s+str(i) for s in 'pq' for i in range(1,5)]+
           ['Mp','Mq','Rp','Rq','Sp','Sq','delta']+
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
    row('cap',add(dict(delta=1),zcoeff(-2)),1 if high else B0-53 if positive else B0)
    row('span',add(dict(Rp=1,Rq=1,delta=1),zcoeff(-4)),450 if high else 85+B0)
    for v in slots:
        side=v[0];other='q' if side=='p' else 'p'
        own,opp=(a,b) if side=='p' else (b,a)
        qtype='global' if j==0 or v==large else 'ordinary' if regime in ('P2','H1') else 'core'
        l=add(scale(-1,centers[v]),{'l_'+v:-1})
        u=add(centers[v],{'u_'+v:-1,'S'+side:-1})
        if qtype=='global':
            l,u=add(l,{'M'+side:-1}),add(u,{'M'+other:-1})
            lr,ur=-90,-89
        elif qtype=='core':
            l,u=add(l,{'R'+side:-1}),add(u,{'R'+other:-1})
            lr,ur=-86,-85
        else:lr,ur=-(opp+5),-(own+4)
        row('L'+v,l,lr);row('U'+v,u,ur)
        # These count caps are valid in the actual-set selection, before relaxation.
        row('slotcap'+v,{'l_'+v:1,'u_'+v:1},85 if qtype=='core' else 89)
    if large:row('large',{'l_'+large:-1,'u_'+large:-1},-86)
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
    row('cardinality',add(dict(Sp=1,Sq=1,delta=1,K=-2),zcoeff(-4)),1842 if high else 1704-90*j)
    return names,rows


def flexible_inverse(r,u,beta):
    require(type(r) is int and r>=15 and type(u) is int and type(beta) is int and 2<=beta<=10,
            'Invalid flexible inverse parameters')
    q,s=divmod(max(0,u-4*beta+2),beta+1)
    return min((beta-1)*(r-14),(beta-1)*q+min(s,beta-1))


def scalar_audit(n=98):
    require(n==98,'This continuation does not exclude the next cardinality')
    d,e,m,G,t0=90,82,81,168,56
    qmax=isqrt(96*e+1073-e*e);qmax-=(qmax-e+1)%2
    paired_min=(e-1-qmax)//2
    require(paired_min==17 and 1+triangular(e)>24*n+77,'Sign bootstrap fails')
    catalogue=base.hole_catalogue()
    lattice,low,high,high_empty,witnesses=[],[],[],[],{}
    high_rejected=0
    for a in range(paired_min,m-paired_min+1):
        b=m-a;I=(a-40)*(a-41)
        lam=1+triangular(a)+triangular(b);omega=22*d+97-lam
        if omega<0:continue
        require(omega==395-I,'Imbalance identity fails')
        C=2*m+4*e+14-lam
        inv=triangular(min(a,b))-2-omega
        inner0=C+2*omega
        innerP=C+3*omega-(2*m-34)
        outer=lam-(4*d-10+omega)
        require(inv>0 and inner0<0 and innerP<0 and outer>0,'Refined common-lattice gate fails')
        lattice.append(dict(a=a,b=b,omega=omega,inverse=inv,inner_zero=inner0,inner_positive=innerP,
                            old_inner=C+3*omega,outer=outer))
        for z in range(omega+1):
            ra,rb=(0,0) if z==0 else (a-14,b-14)
            ua,ub=(0,0) if z==0 else (a-3,b-3)
            tmin=max(t0,z,G-2*z)
            if omega-ra-rb-tmin<0:continue
            if z>=15:
                bounds=[]
                for r in (a,b):
                    eligible=[row for (rr,beta),row in catalogue.items() if rr==r and 2*beta<z]
                    require(eligible,'Missing high-hole witness')
                    best=max(eligible,key=lambda row:(row['C'],-row['beta']))
                    witness=base.hole_row(r,best['C'],best['beta'])
                    witnesses[(r,best['C'],best['beta'])]=witness
                    bounds.append(r+best['C']+1)
                ua,ub=bounds
                ra=max(a-14,ua+2-2*a,*(flexible_inverse(a,ua,beta) for beta in range(2,11)))
                rb=max(b-14,ub+2-2*b,*(flexible_inverse(b,ub,beta) for beta in range(2,11)))
            cmax=omega-ra-rb-tmin
            if cmax<0:
                high_rejected+=int(z>=15)
                continue
            if z>=15:
                margins=base.active_margins(a,b,z,ua,ub,d)
                require(min(margins)>0 and cmax<2*d,'High-hole reduction fails')
                row=dict(a=a,b=b,z=z,c_upper=cmax,mu_p=ua,mu_q=ub,A_margin=margins[0],B_margin=margins[1])
                high.append(row)
                if cmax>=d:
                    require(a in (40,41) and z in (56,57) and cmax-d<=1,'Uncovered high empty-unit state')
                    ep,eq=240+9*(a-40),249-9*(a-40)
                    require(ua+z>=ep and ub+z>=eq,'Coarse high mass bonus fails')
                    require(m+4+omega-G-d+4*z<=450 and 18*d+84-d+4*z<=1842,'Coarse high budget fails')
                    require(cmax-d<min(a,b)+5,'High center can be outside')
                    high_empty.append(row)
                continue
            require(cmax<3*d,'Three low-hole empty units possible')
            regimes=[]
            for j in range(cmax//d+1):
                delta=cmax-j*d;prefix='Z' if z==0 else 'P'
                regime=prefix+str(j);regimes.append(regime)
                B0=227-j*d-I
                require(delta<=(B0 if z==0 else B0-53+2*z),'Low loss budget fails')
                if j==1:
                    require(delta<2*(d-4),'Two large-loss centers possible')
                    if delta>=d-4:regimes.append(prefix+'L')
                if j==2:
                    require(delta<d-4,'Two-empty core count insufficient')
                    if z>0:require(delta<min(a,b)+5,'P2 ordinary quantile unjustified')
            for regime in regimes:
                lo,hi=RANGES[regime];require(lo<=a<=hi,'Low parameter omitted')
            low.append(dict(a=a,b=b,z=z,c_upper=cmax,regimes=regimes))
    expected={(a,z) for a in (40,41) for z in (56,57)}
    require({(r['a'],r['z']) for r in high_empty}==expected,'High state list changed')
    require(lattice and low and high,'Vacuous audit')
    return dict(n=n,d=d,e=e,m=m,G=G,t0=t0,paired_min=paired_min,lattice=lattice,
                low_states=low,high_states=high,high_empty_states=high_empty,
                high_budget_rejections=high_rejected,witnesses=[witnesses[k] for k in sorted(witnesses)],
                summary=dict(lattice_orientations=len(lattice),inverse_min=min(r['inverse'] for r in lattice),
                             inner_zero_max=max(r['inner_zero'] for r in lattice),
                             inner_positive_max=max(r['inner_positive'] for r in lattice),
                             old_inner_max=max(r['old_inner'] for r in lattice),outer_min=min(r['outer'] for r in lattice),
                             low_states=len(low),high_states=len(high),high_empty_states=len(high_empty),
                             high_margin=min(min(r['A_margin'],r['B_margin']) for r in high),
                             high_c_max=max(r['c_upper'] for r in high)))


def check_coverage(bundle,exhaustive=False):
    require(bundle.get('format')=='upper97-quadratic-farkas-v1','Unknown proof-data format')
    groups=list(case_groups());expected={g['key'] for g in groups}
    require(len(expected)==len(groups),'Duplicate generated group')
    coverage,pool=bundle['coverage'],bundle['pool']
    require(set(coverage)==expected,'Missing or extra group')
    used,counts,details=set(),Counter(),{}
    checks=extrema=0
    for group in groups:
        key=group['key'];names,rows=model(group,Quadratic(0,1))
        next_a=group['lo'];margins=[];segments=[]
        for segment in coverage[key]:
            require(isinstance(segment,list) and len(segment)==3 and all(type(x) is int for x in segment),'Malformed interval')
            first,last,index=segment
            require(first==next_a and first<=last<=group['hi'],'Gap, overlap, or out-of-range interval')
            require(0<=index<len(pool),'Invalid vector index')
            result=interval_certificate(names,rows,pool[index],first,last)
            used.add(index);margins.append(result['normalized_gap']);counts[group['regime']]+=last-first+1
            checks+=1;extrema+=result['extremum_points']
            segments.append(dict(first=first,last=last,vector=index,**result))
            if exhaustive:
                gaps=[]
                for a in range(first,last+1):
                    nn,rr=model(group,a)
                    require(nn==names and set(rr)==set(rows),'Symbolic/numeric row mismatch')
                    for label,(vector,rhs) in rows.items():
                        require(rr[label][0]==vector and rr[label][1]==Quadratic.coerce(rhs).at(a),'Symbolic/numeric formula mismatch')
                    gaps.append(base.check_integer_certificate(nn,rr,pool[index])['normalized_gap'])
                require(min(gaps)==result['normalized_gap'],'Wrong interval extremum')
            next_a=last+1
        require(next_a==group['hi']+1,'Missing endpoint')
        details[key]=dict(systems=group['hi']-group['lo']+1,minimum_normalized_gap=min(margins),segments=segments)
    require(used==set(range(len(pool))),'Unused vector')
    require(dict(counts)==EXPECTED_COUNTS,'Unexpected model universe')
    return dict(groups=len(groups),systems=sum(counts.values()),vectors=len(pool),regime_counts=dict(counts),
                interval_checks=checks,extremum_points=extrema,
                minimum_normalized_gap=min(v['minimum_normalized_gap'] for v in details.values()),group_checks=details)


def negative_controls(bundle):
    rejected=[]
    def rejects(label,operation):
        try:operation()
        except (ValueError,KeyError):rejected.append(label)
        else:raise ValueError('Invalid input accepted: '+label)
    g=next(case_groups());names,rows=model(g,Quadratic(0,1))
    rejects('negative_weight',lambda:interval_certificate(names,rows,{'cap':-1},g['lo'],g['hi']))
    rejects('noncontradictory_weight',lambda:interval_certificate(names,rows,{'cap':1},g['lo'],g['hi']))
    rejects('unknown_row',lambda:interval_certificate(names,rows,{'invented':1},g['lo'],g['hi']))
    rejects('interior_vertex_failure',lambda:interval_certificate(['x'],{'r':([0],Quadratic(0,2,-1))},{'r':1},-1,3))
    rejects('missing_group',lambda:check_coverage(dict(bundle,coverage={k:v for k,v in bundle['coverage'].items() if k!=g['key']})))
    intervals=[list(v) for v in bundle['coverage'][g['key']]];intervals[0][0]+=1
    rejects('missing_integer',lambda:check_coverage(dict(bundle,coverage=dict(bundle['coverage'],**{g['key']:intervals}))))
    split=next(g['key'] for g in case_groups() if g['mode']['member']=='q')
    rejects('missing_actual_contributor_choice',lambda:check_coverage(dict(bundle,coverage={k:v for k,v in bundle['coverage'].items() if k!=split})))
    rejects('invalid_flexible_threshold',lambda:flexible_inverse(40,184,11))
    rejects('unrefined_lattice_gate',lambda:require(-1178+3*395<0,'Old gate fails at balanced size 98'))
    rejects('unproved_next_cardinality',lambda:scalar_audit(97))
    # Exact inverse boundaries: independent direct inversion on all used ranges.
    inverse_checks=0
    for beta in range(2,11):
        for v in range(601):
            q,s=divmod(v,beta+1);t=(beta-1)*q+min(s,beta-1)
            require(t+2*(t//(beta-1))>=v and (t==0 or t-1+2*((t-1)//(beta-1))<v),'Integer inverse boundary fails')
            inverse_checks+=1
    return dict(rejected=rejected,integer_inverse_boundary_checks=inverse_checks)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates',type=Path,default=DEFAULT_CERTIFICATE)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--exhaustive',action='store_true')
    args=parser.parse_args()
    bundle=json.loads(args.certificates.read_text(encoding='utf-8'))
    finite=check_coverage(bundle,args.exhaustive);scalar=scalar_audit();guards=negative_controls(bundle)
    summary=dict(status='PASS',conclusion='N <= 97 using the written reduction and audited N <= 98 foundation',
                 verification_mode='interval-plus-exhaustive' if args.exhaustive else 'symbolic-interval',
                 scalar_summary=scalar['summary'],linear_summary={k:v for k,v in finite.items() if k!='group_checks'},negative_controls=guards)
    paths=[Path(__file__),Path(prior.__file__),Path(base.__file__),args.certificates]
    out=dict(summary=summary,scalar_audit=scalar,group_checks=finite['group_checks'],
             sha256={str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,default=base.json_default,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,default=base.json_default,indent=2))


if __name__=='__main__':main()
