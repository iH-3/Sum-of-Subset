#!/usr/bin/env python3
"""Exact continuation 99 -> 98 with symbolic quadratic interval certificates.

Python 3.10+, standard library only. The report proves the reduction from sets
and the new lemmas. This program verifies all scalar gates, complete case
coverage, and integer Farkas multipliers. No numerical optimizer is imported.
Use --exhaustive to cross-check every integer parameter independently.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from math import isqrt
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import upper100 as base
import upper99 as previous
require, add, scale = base.require, base.add, base.scale
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CERTIFICATE = ROOT / 'data/upper98_certificates.json'
RANGES = {'Z':(31,51), 'P':(32,50), 'ZE':(33,49), 'PE':(34,48),
          'ZZ':(36,46), 'EE':(37,45)}
EXPECTED_COUNTS = dict(Z=1428, P=1292, ZE=39237, PE=34620, ZZ=748, EE=4932)


class Quadratic:
    """A rational polynomial of degree at most two, built symbolically."""
    def __init__(self, c=0, b=0, a=0):
        self.coefficients = (Q(c), Q(b), Q(a))

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Quadratic) else Quadratic(value)

    def __add__(self, other):
        other = self.coerce(other)
        return Quadratic(*(x+y for x,y in zip(self.coefficients, other.coefficients)))
    __radd__ = __add__

    def __neg__(self):
        return Quadratic(*(-x for x in self.coefficients))

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) + -self

    def __mul__(self, other):
        other = self.coerce(other)
        values = [Q(0)] * 5
        for i,x in enumerate(self.coefficients):
            for j,y in enumerate(other.coefficients):
                values[i+j] += x*y
        require(not any(values[3:]), 'Polynomial degree exceeds two')
        return Quadratic(*values[:3])
    __rmul__ = __mul__

    def __truediv__(self, divisor):
        require(type(divisor) is int and divisor != 0, 'Invalid polynomial divisor')
        return Quadratic(*(x/divisor for x in self.coefficients))

    def at(self, value):
        c,b,a = self.coefficients
        return c + value*(b + value*a)

    def maximum(self, lo, hi):
        require(type(lo) is int and type(hi) is int and lo <= hi, 'Invalid interval')
        c,b,a = self.coefficients
        candidates = {lo,hi}
        if a < 0:
            vertex = -b/(2*a)
            floor_vertex = vertex.numerator // vertex.denominator
            candidates.update(x for x in (floor_vertex, floor_vertex+1) if lo <= x <= hi)
        value, location = max((self.at(x),x) for x in candidates)
        return value, location, len(candidates)


def triangular(r):
    return r*(r+1)/2 if isinstance(r,Quadratic) else base.triangular(r)


def case_groups():
    """A partition, including both discrete refinements and the |a-41| split."""
    for regime in RANGES:
        for mode in previous.modes(2 if regime == 'EE' else 1):
            branch,missing,choice,slots = mode
            exceptions = [(v,end) for v in slots for end in ('l','u')] if regime in ('ZE','PE') else [None]
            for exception in exceptions:
                key = ':'.join((regime,branch,','.join(missing),choice))
                if exception:
                    key += ':' + ':'.join(exception)
                lo,hi = RANGES[regime]
                special_ze = regime == 'ZE' and branch == 'A' and missing == ('q5',) and exception == ('p4','l')
                special_ee = regime == 'EE' and branch == 'A' and set(missing) == {'p0','q5'}
                if special_ze:
                    parts = [('ordinary-low',lo,46), ('gap4',47,47), ('gap5',47,47), ('ordinary-high',48,hi)]
                elif special_ee:
                    parts = [('pair-p',lo,hi), ('pair-q',lo,hi)]
                elif regime == 'ZZ':
                    parts = [('left',lo,41), ('right',42,hi)]
                else:
                    parts = [('',lo,hi)]
                for variant,first,last in parts:
                    yield dict(key=key+(':'+variant if variant else ''), regime=regime, mode=mode,
                               exception=exception, variant=variant, lo=first, hi=last)


def model(group, a):
    """The same formulas build either integer or symbolic right-hand sides."""
    regime,mode,exception,variant = (group[k] for k in ('regime','mode','exception','variant'))
    if not isinstance(a,Quadratic):
        require(type(a) is int and group['lo'] <= a <= group['hi'], 'Parameter outside group')
    branch,missing,choice,slots = mode
    b, imbalance = 82-a, (41-a)*(41-a)
    double,positive = regime == 'EE', regime in ('P','PE')
    cap = (24 if double else 89 if positive else 115)-imbalance
    upper = 1758 if variant == 'gap4' else 1820 if positive else 1764
    bonus_p,bonus_q = (a-2,b-2) if positive else (0,0)
    names = ([s+str(i) for s in 'pq' for i in range(1,5)] +
             ['Mp','Mq','Rp','Rq','Sp','Sq','delta'] +
             [f'{end}_{v}' for v in slots for end in ('l','u')])
    if double:
        names += [s+str(i) for s in 'xy' for i in range(1,4)] + ['K']
        names += [f'g{s}{j}{i}' for j in range(4) for i in range(j+1,5) for s in 'pq']
    cp = dict(p1=1,p2=-1,p3=-1,p4=-1)
    cq = dict(q1=1,q2=-1,q3=-1,q4=-1)
    bp = dict(p1=-1,p2=2,p3=-1,p4=-1)
    bq = dict(q1=-1,q2=2,q3=-1,q4=-1)
    centers = {}
    for side,c,other in (('p',cp,'q'),('q',cq,'p')):
        for i in range(4):
            centers[side+str(i)] = add(c,{side+str(i+1):1})
            centers[side+str(i+4)] = add(c,{other+str(i+1):-1})
        centers[side+'8'] = {side+'2':1,side+'3':-1,side+'4':-1}
        centers[side+'9'] = bp if side == 'p' else bq
    rows = {}
    def row(label,coeff,rhs):
        require(label not in rows and set(coeff) <= set(names), 'Duplicate row or unknown variable')
        require(all(type(v) is int for v in coeff.values()), 'Noninteger model matrix')
        rows[label] = ([coeff.get(v,0) for v in names],rhs)
    gap = 0 if double else -1
    for side,r,bonus in (('p',a,bonus_p),('q',b,bonus_q)):
        for i in range(1,4):
            row(f'D{side}{i}',{side+str(i+1):1,side+str(i):-1},gap)
        row(f'D{side}4',{'M'+side:1,side+'4':-1},gap)
        row('E'+side,{'R'+side:1,'M'+side:-1},-4)
        row('G'+side,{'R'+side:-1},-r)
        row('H'+side,{'M'+side:2,'R'+side:6,'S'+side:-2},-2*triangular(r)-12-2*bonus)
        row('Hhat'+side,{'M'+side:1,'R'+side:4,'S'+side:-1},-triangular(r-1)-6)
    row('cap',dict(delta=1),cap)
    row('branch',scale(1 if branch == 'A' else -1,add(bp,bq)),0 if branch == 'A' or double else -1)
    for v in slots:
        side = v[0]
        other = 'q' if side == 'p' else 'p'
        own,opp = (a,b) if side == 'p' else (b,a)
        lower = add(scale(-1,centers[v]),{'l_'+v:-1})
        upperrow = add(centers[v],{'u_'+v:-1,'S'+side:-1})
        lower_rhs,upper_rhs = -(opp+5),-(own+4)
        if regime == 'ZZ':
            lower,upperrow = add(lower,{'R'+side:-1}),add(upperrow,{'R'+other:-1})
            lower_rhs,upper_rhs = -87,-86
        if exception == (v,'l'):
            lower = add(lower,{'M'+side:-1})
            lower_rhs = -91
            row('outside',{'l_'+v:-1},-(opp+5))
        if exception == (v,'u'):
            upperrow = add(upperrow,{'M'+other:-1})
            upper_rhs = -90
            row('outside',{'u_'+v:-1},-(own+5))
        row('L'+v,lower,lower_rhs)
        row('U'+v,upperrow,upper_rhs)
    if regime == 'ZZ':
        k = 41-a if variant == 'left' else a-41
        row('twooutside',dict(delta=-1),-2*(46-k))
        row('span',dict(Rp=1,Rq=1,delta=1),199-imbalance)
    if double:
        row('span',dict(Rp=1,Rq=1,delta=1),106-imbalance)
        x,y = ['Rp','x1','x2','x3','Mp'],['Rq','y1','y2','y3','Mq']
        for side,xx,r in (('p',x,a),('q',y,b)):
            for i in range(1,5):
                row(f'I{side}{i}',{xx[i-1]:1,xx[i]:-1},-1)
            row('Htilde'+side,add({v:1 for v in xx},{'S'+side:-1}),-triangular(r-1))
        for j in range(4):
            coeff = dict(K=1)
            coeff = add(coeff,{x[j]:-2,y[j]:-2})
            for i in range(j+1,5):
                for side,xx in (('p',x),('q',y)):
                    g = f'g{side}{j}{i}'
                    row('Ag'+g,{g:1,xx[i]:-1,xx[i-1]:1},0)
                    row('Bg'+g,{g:1,x[j]:-1,y[j]:-1},1)
                    coeff[g] = -1
            t = 2*(4-j)
            row('envelope'+str(j),coeff,1+triangular(t))
        row('cardinality',dict(Sp=1,Sq=1,delta=1,K=-2),1540)
    if variant == 'gap4':
        row('gap4',dict(Mq=1,Rq=-1),4)
    if variant == 'gap5':
        row('gap5',dict(Rq=1,Mq=-1),-5)
    if variant in ('pair-p','pair-q'):
        side = variant[-1]
        row('pairnonempty',add(scale(-1,bp if side == 'p' else bq),{'M'+side:-1}),-1)
    row('loss',dict([('delta',-1)]+[(f'{end}_{v}',1) for v in slots for end in ('l','u')]),0)
    row('Fupper',dict(Sp=1,Sq=1,delta=1,Mp=-2,Mq=-2,Rp=-2,Rq=-2),upper-(182 if double else 91))
    return names,rows


def interval_certificate(names, rows, weights, lo, hi):
    require(isinstance(weights,dict) and weights, 'Empty or malformed vector')
    coefficients = [0]*len(names)
    rhs = Quadratic()
    total = 0
    for label,w in weights.items():
        require(label in rows and type(w) is int and w > 0, 'Invalid row or nonpositive weight')
        vector,b = rows[label]
        require(len(vector) == len(names), 'Matrix dimension mismatch')
        coefficients = [x+w*y for x,y in zip(coefficients,vector)]
        rhs += w*b
        total += w
    require(all(x >= 0 for x in coefficients), 'Negative combined coefficient')
    worst,at,candidates = rhs.maximum(lo,hi)
    require(worst < 0, 'Interval has no strict contradiction')
    return dict(normalized_gap=-worst/total, worst_parameter=at,
                rhs_polynomial=rhs.coefficients, extremum_points=candidates)


def rho_from_mu(r,u):
    return max(r-14, u+2-2*r, min(5*(r-14), (5*(u-22)+6)//7))


def scalar_audit(n=99):
    require(n == 99, 'This continuation does not exclude the next cardinality')
    d,e,m,G,t0 = 91,83,82,170,57
    qmax = isqrt(96*e+1073-e*e)
    qmax -= (qmax-e+1)%2
    paired_min = (e-1-qmax)//2
    require(paired_min >= 18 and 1+triangular(e)>24*n+77, 'Sign bootstrap fails')
    catalogue = base.hole_catalogue()
    lattice,low,high,empty,witnesses = [],[],[],[],{}
    high_rejected = 0
    for a in range(paired_min,m-paired_min+1):
        b = m-a
        lam = 1+triangular(a)+triangular(b)
        omega = 22*d+97-lam
        if omega < 0: continue
        inv = triangular(min(a,b))-2-omega
        inner = 2*m+4*e+14-lam+3*omega
        outer = lam-(4*d-10+omega)
        require(inv>0 and inner<0 and outer>0, 'Common-lattice gate fails')
        lattice.append(dict(a=a,b=b,omega=omega,inverse=inv,inner=inner,outer=outer))
        k,I = abs(41-a),(41-a)**2
        require(omega == 376-I, 'Imbalance identity fails')
        for z in range(omega+1):
            ua,ub = (0,0) if z == 0 else (a-3,b-3)
            ra,rb = (0,0) if z == 0 else (a-14,b-14)
            tmin = max(t0,z,G-2*z)
            if omega-ra-rb-tmin < 0: continue
            if z >= 15:
                bounds=[]
                for r in (a,b):
                    eligible = [row for (rr,beta),row in catalogue.items() if rr==r and 2*beta<z]
                    require(eligible, 'Missing high-hole witness')
                    best = max(eligible,key=lambda row:(row['C'],-row['beta']))
                    checked = base.hole_row(r,best['C'],best['beta'])
                    witnesses[(r,best['C'],best['beta'])] = checked
                    bounds.append(r+best['C']+1)
                ua,ub = bounds
                ra,rb = rho_from_mu(a,ua),rho_from_mu(b,ub)
            cmax = omega-ra-rb-tmin
            if cmax < 0:
                high_rejected += int(z>=15)
                continue
            margins = base.active_margins(a,b,z,ua,ub,d)
            require(min(margins)>0, 'All-active inequality fails')
            row=dict(a=a,b=b,z=z,c_upper=cmax,mu_p=ua,mu_q=ub,rho_lower=ra+rb,
                     A_margin=margins[0],B_margin=margins[1])
            if z >= 15:
                require(cmax<d, 'High-hole empty-unit case remains')
                high.append(row)
                continue
            low.append(row)
            if cmax < d: continue
            require(cmax < 3*d, 'Three empty units possible')
            delta,L = cmax-d,min(a,b)+5
            regimes = ['Z' if z==0 else 'P']
            require(delta <= (115 if z==0 else 89)-I, 'One-empty budget fails')
            if delta >= L: regimes.append('ZE' if z==0 else 'PE')
            if delta >= 2*L:
                require(z==0 and k<=5, 'Two-exception classification fails')
                rho_cap = 23+2*k-I
                require(rho_cap<min(a,b)-14 and rho_cap<=min(a,b)-5 and triangular(min(a,b))>24,
                        'Two-exception full-support reduction fails')
                require(delta-L<=69 and d-69>4, 'Core quantile has no core point')
                regimes.append('ZZ')
            require(delta<3*L, 'Three exceptions possible')
            if z>0: require(delta<2*L and ua+z>=a-2 and ub+z>=b-2, 'Positive-hole reduction fails')
            if cmax>=2*d:
                residual = cmax-2*d
                require(z==0 and k<=4 and residual==24-I and residual<L, 'Two-empty reduction fails')
                require(residual<min(a,b)-14 and residual<=min(a,b)-5 and triangular(min(a,b))>24,
                        'Two-empty full-support reduction fails')
                regimes.append('EE')
            for regime in regimes:
                lo,hi = RANGES[regime]
                require(lo<=a<=hi, 'Uncovered oriented side size')
            empty.append(dict(a=a,b=b,z=z,delta_upper=delta,exception_cost=L,regimes=regimes))
    require(lattice and low and high and empty, 'Vacuous scalar audit')
    return dict(n=n,d=d,e=e,m=m,G=G,t0=t0,paired_min=paired_min,lattice=lattice,
                low_states=low,high_states=high,empty_states=empty,high_budget_rejections=high_rejected,
                witnesses=[witnesses[k] for k in sorted(witnesses)],
                summary=dict(lattice_orientations=len(lattice),low_states=len(low),high_states=len(high),
                             empty_states=len(empty),inverse_min=min(r['inverse'] for r in lattice),
                             inner_max=max(r['inner'] for r in lattice),outer_min=min(r['outer'] for r in lattice),
                             low_margin=min(min(r['A_margin'],r['B_margin']) for r in low),
                             high_margin=min(min(r['A_margin'],r['B_margin']) for r in high),
                             high_c_max=max(r['c_upper'] for r in high)))


def check_coverage(bundle, exhaustive=False):
    require(bundle.get('format') == 'upper98-quadratic-farkas-v1', 'Unknown proof-data format')
    groups = list(case_groups())
    expected = {g['key'] for g in groups}
    require(len(expected) == len(groups), 'Duplicate generated group')
    coverage,pool = bundle['coverage'],bundle['pool']
    require(set(coverage) == expected, 'Missing or extra group')
    used,counts,details = set(),Counter(),{}
    interval_checks = extremum_points = 0
    for group in groups:
        key = group['key']
        names,rows = model(group,Quadratic(0,1))
        next_a,margins,segments = group['lo'],[],[]
        for segment in coverage[key]:
            require(isinstance(segment,list) and len(segment)==3 and all(type(i) is int for i in segment),
                    'Malformed coverage interval')
            first,last,index = segment
            require(first==next_a and first<=last<=group['hi'], 'Gap, overlap, or out-of-range interval')
            require(0<=index<len(pool), 'Invalid vector index')
            result = interval_certificate(names,rows,pool[index],first,last)
            used.add(index)
            margins.append(result['normalized_gap'])
            counts[group['regime']] += last-first+1
            interval_checks += 1
            extremum_points += result['extremum_points']
            segments.append(dict(first=first,last=last,vector=index,**result))
            if exhaustive:
                numeric_gaps=[]
                for a in range(first,last+1):
                    nn,rr = model(group,a)
                    require(nn==names and set(rr)==set(rows), 'Symbolic/numeric row mismatch')
                    for label,(vector,rhs) in rows.items():
                        require(rr[label][0]==vector and rr[label][1]==Quadratic.coerce(rhs).at(a),
                                'Symbolic/numeric formula mismatch')
                    check = base.check_integer_certificate(nn,rr,pool[index])
                    numeric_gaps.append(check['normalized_gap'])
                require(min(numeric_gaps)==result['normalized_gap'], 'Interval extremum mismatch')
            next_a = last+1
        require(next_a == group['hi']+1, 'Missing endpoint')
        details[key] = dict(systems=group['hi']-group['lo']+1,minimum_normalized_gap=min(margins),segments=segments)
    require(used==set(range(len(pool))), 'Unused certificate vector')
    require(dict(counts)==EXPECTED_COUNTS, 'Unexpected model universe')
    return dict(groups=len(groups),systems=sum(counts.values()),vectors=len(pool),regime_counts=dict(counts),
                interval_checks=interval_checks,extremum_points=extremum_points,
                minimum_normalized_gap=min(x['minimum_normalized_gap'] for x in details.values()),group_checks=details)


def negative_controls(bundle):
    rejected=[]
    def rejects(label,operation):
        try: operation()
        except (ValueError,KeyError): rejected.append(label)
        else: raise ValueError('Invalid input accepted: '+label)
    group = next(case_groups())
    names,rows = model(group,Quadratic(0,1))
    rejects('negative_weight',lambda:interval_certificate(names,rows,{'cap':-1},31,51))
    rejects('noncontradictory_weight',lambda:interval_certificate(names,rows,{'cap':1},31,51))
    rejects('unknown_row',lambda:interval_certificate(names,rows,{'invented':1},31,51))
    rejects('interior_vertex_failure',lambda:interval_certificate(['x'],{'r':([0],Quadratic(0,2,-1))},{'r':1},-1,3))
    rejects('degree_overflow',lambda:Quadratic(0,0,1)*Quadratic(0,1))
    partial=dict(bundle,coverage={k:v for k,v in bundle['coverage'].items() if k!=group['key']})
    rejects('missing_group',lambda:check_coverage(partial))
    intervals=[list(x) for x in bundle['coverage'][group['key']]]
    intervals[0][0]+=1
    gap=dict(bundle,coverage=dict(bundle['coverage'],**{group['key']:intervals}))
    rejects('missing_integer_in_interval',lambda:check_coverage(gap))
    special=next(g['key'] for g in case_groups() if g['variant']=='gap4')
    rejects('missing_gap_four_branch',lambda:check_coverage(dict(bundle,coverage={k:v for k,v in bundle['coverage'].items() if k!=special})))
    special_pair=next(g['key'] for g in case_groups() if g['variant']=='pair-q')
    rejects('missing_split_pair_branch',lambda:check_coverage(dict(bundle,coverage={k:v for k,v in bundle['coverage'].items() if k!=special_pair})))
    rejects('unproved_next_cardinality',lambda:scalar_audit(98))
    return dict(rejected=rejected)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates',type=Path,default=DEFAULT_CERTIFICATE)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--exhaustive',action='store_true',help='Also check every integer model and symbolic formula')
    args=parser.parse_args()
    bundle=json.loads(args.certificates.read_text(encoding='utf-8'))
    finite=check_coverage(bundle,args.exhaustive)
    scalar=scalar_audit()
    guards=negative_controls(bundle)
    summary=dict(status='PASS',conclusion='N <= 98 using the written reduction and audited N <= 99 foundation',
                 verification_mode='interval-plus-exhaustive' if args.exhaustive else 'symbolic-interval',
                 scalar_summary=scalar['summary'],linear_summary={k:v for k,v in finite.items() if k!='group_checks'},
                 negative_controls=guards)
    paths=[Path(__file__),Path(base.__file__),Path(previous.__file__),args.certificates]
    out=dict(summary=summary,scalar_audit=scalar,group_checks=finite['group_checks'],
             sha256={str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,default=base.json_default,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,default=base.json_default,indent=2))


if __name__=='__main__':
    main()
