#!/usr/bin/env python3
"""Exact local checks under explicit geometric hypotheses; not a global83 proof."""
import argparse
from fractions import Fraction as Q
from functools import lru_cache
import importlib.util
from itertools import product
import json
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def T(n):
    return n*(n+1)//2


@lru_cache(None)
def cap(tau, xi):
    """Upper bound on min_j(7j+6d_(r-j)) for a real monotone core."""
    best = 0
    for cost in range(1, 6*xi+1):
        required = xi + sum(max(0, (cost-7*j+5)//6)
                            for j in range(1, (cost-1)//7+1))
        if required > tau:
            break
        best = cost
    return best


def weighted_checks():
    records = []
    for weight in (2, 3):
        single = [0]
        for tau in range(1, 50):
            single.append(min(weight*tau-xi-cap(tau, xi)
                              for xi in range(1, tau+1)))
        best = min((7*68+single[s]+single[t], s, t)
                   for s in range(50) for t in range(50-s))
        expected = 458 if weight == 2 else 466
        need(best[0] == expected, 'weighted inverse minimum')
        records.append(dict(weight=weight, minimum=best[0], side_masses=best[1:]))
    need(466+4*27-559 == 15, 'B order margin')
    need(458+3*35-559 == 4, 'D order margin')
    return records


def ledger_checks():
    groups = [{'C25_s','C25_t'}, {'C58_s','C58_t'},
              {'U6_s','U6_t'}, {'V6_s','V6_t'}]
    rows = [('C48','F3'), ('C77','F4'), ('C15','F1','@C55'),
            ('C26','@C57','@V4'), ('C35','V3','@C46'),
            ('C36','U4','@U5'), ('C44','U8','F5'),
            ('C45','V8','@C67'), ('C47','V7','F2'),
            ('C56','V2','@C66'), ('C68','U3','@V5')]
    for row in rows:
        for v,o in [('s','t'),('t','s')]:
            groups.append({x.lstrip('@')+'_'+(o if x.startswith('@') else v)
                           for x in row})
    need(len(groups)==26 and sum(map(len,groups))==len(set().union(*groups)),
         '26 disjoint baseline groups')
    def both(labels):
        return {x+'_'+v for x in labels for v in ('s','t')}
    high=both(['C11','C12','C13','C14'])
    low=both(['C55','C56','C57','C58','V5','V6','V7','V8','F3','F4','F5'])
    low|={x+'_s' for x in ['U5','U6','U7','U8','V2','V3','V4']}
    records=[]
    def stage(name, expected):
        need(not high&low and not high&set().union(*groups), 'ledger compatibility')
        touched=sum(bool(low&g) for g in groups)
        actual=(len(high),len(low),touched,len(high)+len(low)-touched)
        need(actual==expected, 'ledger stage '+name+': '+str(actual))
        records.append(dict(name=name, high=actual[0], low=actual[1],
                            touched=actual[2], credit=actual[3]))
    stage('initial',(8,29,23,14))
    high|=both(['C22','C23','C24','C16','C17','C18'])|{'C33_s'}
    stage('tail_before_normality',(21,29,23,27))
    low|={x+'_t' for x in ['U5','U6','U7','U8','V3','V4']}
    stage('B_below_a',(21,35,25,31))
    low|={x+'_s' for x in ['C66','C67','C68','C35']}
    stage('C_below_b',(21,39,25,35))
    low|={x+'_t' for x in ['C66','C67','C68']}
    stage('D_below_a',(21,42,25,38))
    low|={'C25_s','C25_t','C35_t','C45_s','C45_t'}
    stage('complete_LOW',(21,47,26,42))
    return records


def geometry_arithmetic():
    # Exact whole-side capacities and generic endpoint constants.
    source=13*76+84
    need(source==1072 and source-7*76==540 and source-6*76==616,
         'physical target capacities')
    need(540-71+21==490 and 616-71+21==566,'two physical endpoint rows')
    need(490-72+67==485 and 566-72+67==561,'separate B and D order constants')
    need(485-78+2*76==559 and 561-78+76==559,'order master constants')
    # Unbounded one-side rank kernels T_p-2p>=-1 and T_p-p>=0.
    need(all(T(p)-2*p>=-1 and T(p)-p>=0 for p in range(8)), 'small rank kernels')
    need(8-1>0, 'rank kernel increments are positive for all p>=8')
    need(2*68-2==134 and (134-62)//2==36,'initial X and g floors')
    need(68-62==6,'initial h floor')
    need(1+4+36+36+6==83>26 and 1+4+72+36==113>16,'strict tail tests')
    need(3*134-3*49==255>2*116,'prefix leading strictly above C')
    need(134-49==85 and (85+1)//2-1==42>26,'fixed-only prefix too long')
    # The final transport retains the actual source fringe.
    need(9*76+94==778,'transport constant before 2B_fr')
    need(13*76-110-4*84==542,'source coupled terminal constant')
    need(542+2*(2*76+18)==882<13*68==884,'strict final contradiction')
    states=0
    for k in range(9):
        I=k*(k+1)
        for tau in range(max(0,35-I)):
            for delta in range(42,77-I-tau):
                eps=delta-42
                need(38-k>eps,'normality only after credit42')
                for xi in range(tau+1):
                    need(68-xi-eps>=tau,'initial ordinary gap')
                    need(2*(68-xi)-eps>=2*tau,'initial star gap')
                    need(66-eps>tau and 2*66-eps>2*tau,'strict long-gap bootstrap')
                    states+=1
    return dict(states=states,B_margin=15,D_margin=4,terminal_margin=2)


def low_hole_census():
    """Safe relaxed I+tau minima: multiplicity <=2, total count67."""
    minima={}
    by_holes={}
    count=0
    for counts in product(range(3),repeat=10):
        bits=1
        mass=number=0
        for x,c in enumerate(counts,1):
            for _ in range(c):
                bits|=bits<<x
            number+=c
            mass+=x*c
        holes=tuple(x for x in range(1,11) if not (bits>>x)&1)
        if holes:
            remaining=67-number
            # Smallest remaining multiset from11 upwards with two slots/value.
            p=remaining//2
            floor=mass+10*remaining+T(p)+T(remaining-p)-1156
            key=(holes[0],len(holes))
            minima[key]=min(floor,minima.get(key,floor))
            by_holes[holes]=min(floor,by_holes.get(holes,floor))
        count+=1
    need(count==59049,'complete ternary low-prefix domain')
    need(min(v for (m,h),v in minima.items() if h>=4)==256,'four low holes floor')
    need(min(v for (m,h),v in minima.items() if m>=6)==289,'first gap6 floor')
    need(min(v for (m,h),v in minima.items() if h>=3)==195,'three low holes floor')
    need(min(v for (m,h),v in minima.items() if m==2)==99,'first hole2 floor')
    need({k for k,v in by_holes.items() if v<=156}=={(1,),(1,2),(1,3),(2,),(3,)},'P4 exact relaxed profiles')
    need({k for k,v in by_holes.items() if v<=90}=={(1,)},'P5 exact relaxed profiles')
    need(minima[(5,1)]==224 and minima[(4,1)]==196,'new boundary profiles')
    return dict(patterns=count,at_least_four_lower_holes_minimum=256,
                first_gap_at_least_six_minimum=289,
                feasible_below_243=[dict(holes=k,min_I_plus_tau=v)
                    for k,v in sorted(by_holes.items()) if v<=242],
                minima=[dict(first_gap=m,lower_holes=h,min_I_plus_tau=v)
                        for (m,h),v in sorted(minima.items())])


def z5_transports():
    path=Path(__file__).resolve().parents[1]/'upper83_fullrank/check.py'
    spec=importlib.util.spec_from_file_location('fullrank_source',path)
    core=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(core)
    # name,beta,qweight,xi coefficients,mass coefficients,peel coefficients,
    # delta coefficient,credit coefficient,credit,constant,quadratic weight.
    cards=[
      ('opposite',10,0,4,0,1,0,(3,1),Q(-11,2),Q(13,2),8,851,1),
      ('same',8,0,-2,2,0,1,(1,1),Q(-5,2),Q(7,2),8,1006,1),
      ('four',10,0,-3,1,0,1,(0,3),-3,4,8,1022,1),
      ('highalpha',4,0,5,-3,2,0,(2,0),-1,2,14,1087,2),
      ('C5s_or_Us',12,0,-1,-1,0,0,(2,2),Q(-11,2),Q(13,2),11,709,0),
      ('Ht',16,0,-3,-3,0,0,(4,3),Q(-11,2),Q(13,2),11,669,0),
      ('alpha_t',15,3,-3,-3,0,0,(4,1),-7,8,11,813,0),
      ('split_beta',12,0,0,4,0,1,(1,2),Q(-13,2),Q(9,2),14,847,1),
      ('branch_B',9,0,-1,3,0,1,(1,2),-3,4,8,1011,1)]
    out=[]
    for name,beta,qw,cs,ct,ms,mt,peels,dc,ec,e,const,poly in cards:
        radial=core.radial(76-e,beta,qw,cs,ct,ms,mt)
        best=None
        states=0
        for r in (range(1,67) if poly else [33]):
            I=(r-33)*(r-34)
            for A in range(I+e,77):
                peel=core.peel_min(*peels,max(4,A-4),241-A,A+76)
                for tau in range(A-I-e+1):
                    delta=A-I-tau
                    value=(poly*(T(r)+4*r)+peel[0]+(beta+qw)*68
                           +radial[tau][0]+dc*delta+ec*e-const)
                    states+=1
                    if best is None or value<best[0]:
                        best=(value,dict(r=r,I=I,A=A,tau=tau,delta=delta,
                                        peels=peel,radial=radial[tau]))
        need(best is not None and best[0]>0,'Z5 actual transport '+name)
        out.append(dict(card=name,minimum=best[0],witness=best[1],states=states))
    need([x['minimum'] for x in out]==[Q(811,2),Q(203,2),258,230,
         Q(91,2),Q(1105,2),305,415,223],'Z5 transport inventory')
    return out


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=dict(status='PASS_LOCAL_ARITHMETIC',global_upper83_proved=False,
                hypotheses='See z5_alpha.md; common integral source and exact alpha-hole family',
                weighted=weighted_checks(),ledger=ledger_checks(),
                geometry=geometry_arithmetic(),low_prefix=low_hole_census(),
                z5_transports=z5_transports())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','global_upper83_proved','geometry')}))


if __name__=='__main__':
    main()
