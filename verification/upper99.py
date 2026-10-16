#!/usr/bin/env python3
"""Exact finite continuation from the audited upper bound 100 to 99.

Python 3.10+, standard library only. Imports the already-audited upper100
arithmetic helpers, but no archived endpoint data and no numerical optimizer.
The written report proves the actual-set-to-model reduction.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
from itertools import combinations
import json
from math import isqrt
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import upper100 as base
require,triangular,add,scale=base.require,base.triangular,base.add,base.scale
ROOT=Path(__file__).resolve().parents[1]
DEFAULT_CERTIFICATE=ROOT/'data/upper99_certificates.json'
RANGES={'Z':(32,51),'P':(34,49),'ZE':(35,48),'PE':(37,46),'ZZ':(40,43),'EE':(41,42)}


def modes(empty_count):
    require(empty_count in (1,2),'Unsupported number of empty units')
    for branch,j in (('A',9),('B',5)):
        singles=[s+str(i) for s in 'pq' for i in range(10) if i not in (4,j)]
        for missing in combinations(['pair1','pair2']+singles,empty_count):
            drop=branch=='A' and ('p5' in missing or 'q5' in missing)
            choices=['-'] if 'pair2' in missing or drop else ['p','q']
            for choice in choices:
                slots=[v for v in singles if v not in missing]
                if 'pair1' not in missing:slots.append('p4')
                if choice!='-':slots.append(choice+str(j))
                yield branch,missing,choice,slots


def case_groups():
    for regime in RANGES:
        for mode in modes(2 if regime=='EE' else 1):
            exceptions=[(v,end) for v in mode[3] for end in ('l','u')] if regime in ('ZE','PE') else [None]
            for exception in exceptions:
                key=':'.join((regime,mode[0],','.join(mode[1]),mode[2]))
                if exception:key+=':'+':'.join(exception)
                yield key,regime,mode,exception


def linear_model(regime,a,mode,exception=None):
    require(regime in RANGES and type(a) is int and RANGES[regime][0]<=a<=RANGES[regime][1],
            'Parameter outside the proved model range')
    branch,missing,choice,slots = mode
    b=83-a
    k=41-min(a,b)
    imbalance=k*(k+1)
    n=100
    double=regime=='EE'
    positive=regime in ('P','PE')
    cap=0 if double else (65 if positive else 92)-imbalance
    upper=1838 if positive else 1782
    unit_count=2 if double else 1
    bonus_p,bonus_q=(a-2,b-2) if positive else (0,0)
    a0,b0=a,b
    names = ([s+str(i) for s in "pq" for i in range(1,5)] +
             ["Mp","Mq","Rp","Rq","Sp","Sq","delta"] +
             [f"{end}_{v}" for v in slots for end in ("l","u")])
    cp = dict(p1=1,p2=-1,p3=-1,p4=-1)
    cq = dict(q1=1,q2=-1,q3=-1,q4=-1)
    bp = dict(p1=-1,p2=2,p3=-1,p4=-1)
    bq = dict(q1=-1,q2=2,q3=-1,q4=-1)
    centers = {}
    for side,c,other in (("p",cp,"q"),("q",cq,"p")):
        for i in range(4):
            centers[side+str(i)] = add(c,{side+str(i+1):1})
            centers[side+str(i+4)] = add(c,{other+str(i+1):-1})
        centers[side+"8"] = {side+"2":1,side+"3":-1,side+"4":-1}
        centers[side+"9"] = bp if side == "p" else bq
    rows = {}

    def row(label,coeff,rhs):
        require(set(coeff) <= set(names), "Unknown model variable")
        rows[label] = ([coeff.get(v,0) for v in names],rhs)

    gap=0 if double else -1
    for side in "pq":
        for i in range(1,4):
            row(f"D{side}{i}",{side+str(i+1):1,side+str(i):-1},gap)
        row(f"D{side}4",{"M"+side:1,side+"4":-1},gap)
        row("E"+side,{"R"+side:1,"M"+side:-1},-4)
    row("Gp",dict(Rp=-1),-a)
    row("Gq",dict(Rq=-1),-b)
    row("Hp",dict(Mp=2,Rp=6,Sp=-2),-2*triangular(a)-12-2*bonus_p)
    row("Hq",dict(Mq=2,Rq=6,Sq=-2),-2*triangular(b)-12-2*bonus_q)
    row("cap",dict(delta=1),cap)
    row("branch",scale(1 if branch == "A" else -1,add(bp,bq)),0 if branch == "A" or double else -1)
    for v in slots:
        side = v[0]
        own,opp = (a0,b0) if side == "p" else (b0,a0)
        if double:
            other='q' if side=='p' else 'p'
            row('L'+v,add(scale(-1,centers[v]),{'l_'+v:-1,'M'+other:1}),-1)
            row('U'+v,add(centers[v],{'u_'+v:-1,'S'+side:-1,'M'+side:1}),0)
        else:
            correction=int(regime=='ZZ')
            row('L'+v,add(scale(-1,centers[v]),{'l_'+v:-1}),-(opp+5)+correction)
            row('U'+v,add(centers[v],{'u_'+v:-1,'S'+side:-1}),-(own+4)+correction)
    if regime=='ZZ':
        row('Kp',dict(Rp=1),a+1)
        row('Kq',dict(Rq=1),b+1)
    if exception:
        require(regime in ("ZE","PE"), "Exception in the wrong regime")
        v,endpoint = exception
        require(v in slots and endpoint in ("l","u"), "Invalid exception")
        side = v[0]
        other = "q" if side == "p" else "p"
        if endpoint == "l":
            row("L"+v,add(scale(-1,centers[v]),{"l_"+v:-1,"M"+side:-1}),-(n-8))
            row("outside",{"l_"+v:-1},-((b0 if side == "p" else a0)+5))
        else:
            row("U"+v,add(centers[v],{"u_"+v:-1,"S"+side:-1,"M"+other:-1}),-(n-9))
            row("outside",{"u_"+v:-1},-((a0 if side == "p" else b0)+5))
    row("loss",dict([("delta",-1)]+[(f"{end}_{v}",1) for v in slots for end in ("l","u")]),0)
    row("Fupper",dict(Sp=1,Sq=1,delta=1,Mp=-2,Mq=-2,Rp=-2,Rq=-2),upper-unit_count*(n-8))
    return names,rows


check_integer_certificate=base.check_integer_certificate


def scalar_audit(n=100):
    require(n==100,'This continuation does not exclude the next cardinality')
    d,e,m=92,84,83
    G,t0=172,58
    qmax=isqrt(96*e+1073-e*e)
    qmax-=(qmax-e+1)%2
    paired_min=(e-1-qmax)//2
    require(paired_min==19 and 1+triangular(n-16)>24*n+77,'Sign bootstrap fails')
    catalogue=base.hole_catalogue()
    lattice,low,high,empty,witnesses=[],[],[],[],{}
    high_rejected=0
    for a in range(paired_min,m-paired_min+1):
        b=m-a
        lam=1+triangular(a)+triangular(b)
        omega=22*d+97-lam
        if omega<0:continue
        inv=triangular(min(a,b))-2-omega
        inner=2*m+4*e+14-lam+3*omega
        outer=lam-(4*d-10+omega)
        require(inv>0 and inner<0 and outer>0,'Common-lattice gate fails')
        lattice.append(dict(a=a,b=b,omega=omega,inverse=inv,inner=inner,outer=outer))
        k=41-min(a,b)
        I=k*(k+1)
        require(omega==356-I,'Incorrect imbalance identity')
        for z in range(omega+1):
            ua,ub=(0,0) if z==0 else (a-3,b-3)
            ra,rb=(0,0) if z==0 else (a-14,b-14)
            tmin=max(t0,z,G-2*z)
            if omega-ra-rb-tmin<0:continue
            if z>=15:
                bounds=[]
                for r in (a,b):
                    eligible=[row for (rr,beta),row in catalogue.items() if rr==r and 2*beta<z]
                    require(eligible,'Missing high-hole witness')
                    best=max(eligible,key=lambda row:(row['C'],-row['beta']))
                    checked=base.hole_row(r,best['C'],best['beta'])
                    witnesses[(r,best['C'],best['beta'])]=checked
                    bounds.append(r+best['C']+1)
                ua,ub=bounds
                ra,rb=max(ra,ua+2-2*a),max(rb,ub+2-2*b)
            cmax=omega-ra-rb-tmin
            if cmax<0:
                high_rejected+=int(z>=15)
                continue
            margins=base.active_margins(a,b,z,ua,ub,d)
            require(min(margins)>0,'All-active inequality fails')
            row=dict(a=a,b=b,z=z,c_upper=cmax,mu_p=ua,mu_q=ub,
                     rho_lower=ra+rb,A_margin=margins[0],B_margin=margins[1])
            if z>=15:
                require(cmax<d,'High-hole empty-unit case remains')
                high.append(row)
                continue
            low.append(row)
            if cmax<d:continue
            require(cmax<3*d,'Three empty units have not been treated')
            delta=cmax-d
            L=min(a,b)+5
            regimes=['Z' if z==0 else 'P']
            require(delta<=(92 if z==0 else 65)-I,'Residual budget fails')
            if delta>=L:
                regimes.append('ZE' if z==0 else 'PE')
            if delta>=2*L:
                require(z==0 and k in (0,1) and delta==2*L,'Two-exception rigidity fails')
                regimes.append('ZZ')
            require(delta<3*L,'Three outside centers have not been treated')
            if z>0:require(delta<2*L and ua+z>=a-2 and ub+z>=b-2,'Positive-hole reduction fails')
            if cmax>=2*d:
                require(z==0 and k==0 and cmax==2*d,'Two-empty equality fails')
                regimes.append('EE')
            for regime in regimes:
                lo,hi=RANGES[regime]
                require(lo<=a<=hi,'Regime omits an oriented side size')
            empty.append(dict(a=a,b=b,z=z,delta_upper=delta,exception_cost=L,regimes=regimes))
    require(lattice and low and high and empty,'Vacuous scalar audit')
    return dict(n=n,d=d,e=e,m=m,G=G,t0=t0,paired_min=paired_min,lattice=lattice,
                low_states=low,high_states=high,empty_states=empty,
                high_budget_rejections=high_rejected,
                witnesses=[witnesses[k] for k in sorted(witnesses)],
                summary=dict(lattice_orientations=len(lattice),low_states=len(low),high_states=len(high),
                             empty_states=len(empty),inverse_min=min(r['inverse'] for r in lattice),
                             inner_max=max(r['inner'] for r in lattice),outer_min=min(r['outer'] for r in lattice),
                             low_margin=min(min(r['A_margin'],r['B_margin']) for r in low),
                             high_margin=min(min(r['A_margin'],r['B_margin']) for r in high),
                             high_c_max=max(r['c_upper'] for r in high)))


def check_coverage(bundle):
    require(bundle.get('format')=='upper99-integer-farkas-v1','Unknown proof-data format')
    groups=list(case_groups())
    expected={g[0] for g in groups}
    require(len(expected)==len(groups),'Duplicate generated group key')
    coverage,pool=bundle['coverage'],bundle['pool']
    require(set(coverage)==expected,'Missing or extra coverage group')
    used=set()
    counts=Counter()
    details={}
    for key,regime,mode,exception in groups:
        lo,hi=RANGES[regime]
        next_a=lo
        margins=[]
        for segment in coverage[key]:
            require(isinstance(segment,list) and len(segment)==3 and all(type(i) is int for i in segment),
                    'Malformed coverage interval')
            first,last,index=segment
            require(first==next_a and first<=last<=hi,'Gap, overlap, or out-of-range coverage interval')
            require(0<=index<len(pool),'Invalid certificate index')
            used.add(index)
            for a in range(first,last+1):
                names,rows=linear_model(regime,a,mode,exception)
                check=check_integer_certificate(names,rows,pool[index])
                margins.append(check['normalized_gap'])
                counts[regime]+=1
            next_a=last+1
        require(next_a==hi+1,'Missing endpoint in coverage interval')
        details[key]=dict(systems=hi-lo+1,minimum_normalized_gap=min(margins))
    require(used==set(range(len(pool))),'Unused proof-data vector')
    require(dict(counts)==dict(Z=1360,P=1088,ZE=32312,PE=23080,ZZ=272,EE=1094),'Unexpected model universe')
    return dict(groups=len(groups),systems=sum(counts.values()),vectors=len(pool),
                regime_counts=dict(counts),minimum_normalized_gap=min(x['minimum_normalized_gap'] for x in details.values()),
                group_checks=details)


def check_small_zero_cores():
    """Finite corroboration of the written infinite equality lemma, not its proof."""
    checked=0
    equality=0
    for r in range(15,31):
        expected={tuple(range(1,r+1)),tuple(x for x in range(1,r+2) if x!=r-1)}
        actual=set()
        for q in (0,1,2):
            h=r+q
            for deleted in combinations(range(1,h),q):
                X=tuple(x for x in range(1,h+1) if x not in deleted)
                bits=1
                for x in X:bits|=bits<<x
                points=(0,)+X
                restricted={points[i]+points[j] for i in range(len(points)) for j in range(i+1,len(points))}
                defects=sum(2*x not in restricted for x in X)
                mu=bits.bit_count()-1-triangular(r)
                rho=mu+2-2*defects
                full=bits==(1<<(sum(X)+1))-1
                if full and rho==0:actual.add(X)
                checked+=1
        require(actual==expected,'Zero-core equality classification fails in finite corroboration')
        equality+=len(actual)
    return dict(status='PASS',scope='r=15..30, at most two deleted positions; corroboration only',
                sets_checked=checked,equality_cases=equality)


def negative_controls(bundle):
    rejected=[]
    def rejects(label,operation):
        try:operation()
        except (ValueError,KeyError):rejected.append(label)
        else:raise ValueError('Invalid input accepted: '+label)
    key,regime,mode,exception=next(case_groups())
    names,rows=linear_model(regime,RANGES[regime][0],mode,exception)
    rejects('invalid_hole_witness',lambda:base.hole_row(32,84,7))
    rejects('negative_weight',lambda:check_integer_certificate(names,rows,{'cap':-1}))
    rejects('noncontradictory_weight',lambda:check_integer_certificate(names,rows,{'cap':1}))
    rejects('unknown_row',lambda:check_integer_certificate(names,rows,{'invented':1}))
    partial=dict(bundle,coverage={k:v for k,v in bundle['coverage'].items() if k!=key})
    rejects('missing_group',lambda:check_coverage(partial))
    intervals=[list(x) for x in bundle['coverage'][key]]
    intervals[0][0]+=1
    gap=dict(bundle,coverage=dict(bundle['coverage'],**{key:intervals}))
    rejects('missing_integer_in_interval',lambda:check_coverage(gap))
    rejects('unproved_next_cardinality',lambda:scalar_audit(99))
    require(376-170-2*91==24,'Next-endpoint residual changed')
    return dict(rejected=rejected,next_obstruction=dict(n=99,a=41,b=41,z=0,c_upper=206,
                                                       two_empty_cost=182,residual=24))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates',type=Path,default=DEFAULT_CERTIFICATE)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    bundle=json.loads(args.certificates.read_text(encoding='utf-8'))
    finite=check_coverage(bundle)
    scalar=scalar_audit()
    corroboration=check_small_zero_cores()
    guards=negative_controls(bundle)
    summary=dict(status='PASS',conclusion='N <= 99 using the written reduction and audited N <= 100 foundation',
                 scalar_summary=scalar['summary'],linear_summary={k:v for k,v in finite.items() if k!='group_checks'},
                 zero_core_corroboration=corroboration,negative_controls=guards)
    paths=[Path(__file__),Path(base.__file__),args.certificates]
    out=dict(summary=summary,scalar_audit=scalar,group_checks=finite['group_checks'],
             sha256={str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,default=base.json_default,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,default=base.json_default,indent=2))


if __name__=='__main__':
    main()
