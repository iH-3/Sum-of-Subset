#!/usr/bin/env python3
"""Exact checks for full-rank/long-gap lemmas and CONDITIONAL size-84 cards.

No solver, floats, or disabled assertions. Python 3.10+, standard library.
A PASS is not a size-84 structural reduction or a proof of N <= 83.
"""
import argparse
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
import importlib.util
from itertools import combinations, product
import json
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'data/upper83_fullrank_sources.json'
T = lambda x: x*(x+1)//2


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def phi_cap(tau, xi):
    need(0 <= xi <= tau and (tau == 0) == (xi == 0), 'rank domain')
    return min(xi, 1+(isqrt(1+8*(tau-xi))-1)//2)


def select(P, beta=1, qweight=0):
    need(P and tuple(sorted(set(P))) == tuple(P) and P[0] > 0, 'positive core')
    r = len(P)
    dev = [0]+[x-i for i,x in enumerate(P,1)]
    cost, j = min(((beta+qweight)*j+beta*dev[r-j], j) for j in range(r+1))
    return dict(tau=sum(dev), xi=dev[-1], cost=cost, trim=j,
                phi=j+dev[r-j], values=P[:r-j])


@lru_cache(None)
def weighted_cap(tau, xi, beta, qweight):
    if qweight == 0:
        return beta*phi_cap(tau, xi)
    step = beta+qweight
    best = 0
    for k in range(1, beta*xi+1):
        mass = xi+sum(max(0, (k-step*j+beta-1)//beta)
                      for j in range(1, (k-1)//step+1))
        if mass > tau:
            break
        best = k
    return best


@lru_cache(None)
def profiles(limit, beta, qweight, coeff, mass=0):
    need(isinstance(beta, int) and beta > 0 and qweight >= 0, 'integer weights')
    out = [(0,0,0)]
    for tau in range(1, limit+1):
        out.append(min((mass*tau+coeff*xi-weighted_cap(tau,xi,beta,qweight),
                        xi, weighted_cap(tau,xi,beta,qweight)) for xi in range(1,tau+1)))
    return tuple(out)


@lru_cache(None)
def radial(limit, beta, qweight, cs, ct, ms=0, mt=0):
    s,t = profiles(limit,beta,qweight,cs,ms),profiles(limit,beta,qweight,ct,mt)
    return tuple(min((s[ts][0]+t[tau-ts][0], ts, s[ts], t[tau-ts])
                     for ts in range(tau+1)) for tau in range(limit+1))


def peel_min(p,q,lo,hi,total):
    candidates=[]
    for es in range(lo,hi+1):
        et=max(lo,total-es) if q >= 0 else hi
        if et <= hi and es+et >= total:
            candidates.append((p*es+q*et,es,et))
    need(candidates, 'empty peel polygon')
    return min(candidates)


def core_checks():
    samples=[]; n=0
    for r in range(1,7):
        for P in combinations(range(1,r+6),r):
            v=select(P); p=v['cost']; tau=v['tau']; xi=v['xi']
            need(p <= phi_cap(tau,xi), 'inverse staircase cap')
            need(tau-4*p >= -6, 'sharp kernel tau-4phi')
            need(2*tau-2*xi-7*p >= -16, 'sharp kernel 2tau-2xi-7phi')
            for beta,qw in ((6,1),(11,2),(12,0),(9,5)):
                u=select(P,beta,qw)
                need(u['cost'] <= weighted_cap(tau,xi,beta,qw), 'weighted inverse cap')
            if n % 11 == 0: samples.append(P)
            n+=1
    intersections=unions=0
    for i,P in enumerate(samples):
        P2=samples[-1-i]; a,b=select(P),select(P2)
        E={0,*P,*(-x for x in P2)};m=len(E);tau=a['tau']+b['tau']
        core={0,*a['values'],*(-x for x in b['values'])}
        F=m-a['phi']-b['phi']
        for x in range(max(E)-min(E)+3):
            need(len(core & {v+x for v in core}) >= F-x, 'actual common-Q intersection')
            if x >= tau:
                need(len(E & {v+x for v in E}) >= m-x-2, 'boundary-safe overlap')
            if x > tau:
                need(len(E & {v+x for v in E}) >= m-x, 'strict long-gap overlap')
            intersections+=1
        for gaps in ((tau+1,tau+1),(tau+1,tau+3),(tau+3,tau+2)):
            centers=(0,gaps[0],sum(gaps))
            union=set().union(*({v+c for v in E} for c in centers))
            need(len(union) <= m+centers[-1], 'outer holes survive union')
            unions+=1
    # Equality examples, and a strict-boundary counterexample.
    P=(2,4,6); v=select(P)
    need(v['tau']-4*v['cost'] == -6, 'first sharp kernel witness')
    v=select((2,4,6,8))
    need(2*v['tau']-2*v['xi']-7*v['cost'] == -16, 'second sharp kernel witness')
    E={-3,-1,0,1}
    need(len(E & {x+1 for x in E}) == 2 < len(E)-1, 'strict-boundary counterexample')
    P=(1,2,3,4,10,11,12,13); v=select(P)
    need(v['cost']==4 and v['trim']==4, 'all-rank choice beats depths zero through three')
    return dict(actual_one_side_cores=n,actual_intersections=intersections,actual_unions=unions,
                sharp_kernel_minima=[-6,-16],strict_boundary_counterexample=dict(E=sorted(E),tau=1,shift=1,intersection=2,invalid_lower=3))


def source_checks():
    cases=[]
    for a,b,c in combinations(range(1,19),3):
        if a+b+c > 18: continue
        # e>=2c has exactly the four e-containing sums, Q<=2.
        for e in range(c+1,2*c+1):
            offsets=(a,b,c,e)
            B=len({x+y for x in offsets for y in offsets if x+y>e})
            Qv=2*B-a-b-c
            need(Qv<=3, 'quartet Q<=3 finite core')
            if Qv==3:cases.append(offsets)
    need(cases==[(1,2,4,5),(1,3,5,6)], 'quartet equality characterization')
    # a+b+c>=19 implies Q<=20-19=1. For e>=2c, Q=8-a-b-c<=2.
    need(20-19<=3 and 8-6<=2, 'quartet infinite tails')
    # At L=A+77, equality forces a small e<=6, and then a large (1,2,3,e).
    need(77-12-7-67 == -9, 'central missing-interval constant')
    need(10-9 > 0, 'delta>=10 excludes equality')
    # Ownerless H/C5 scalar row after the strengthened L>=A+78.
    need(7*68-32+3*13 == 483 > 482, 'ownerless terminal margin')
    return dict(quartet_equality=cases,sharpened_L='L >= A+78 for j=5, w=0, delta>=10',
                ownerless_conditional=dict(lower=483,upper=482,margin=1))


def fixed_checks():
    path=ROOT/'verification/upper83_progress.py'
    spec=importlib.util.spec_from_file_location('frozen_progress',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    labels,gaps,groups=module.fixed_catalogue()
    outcomes=[]
    for sign in '+-':
        H={f'C{sign}{i}{j}' for i in range(1,5) for j in range(i,5)}
        need(len(H)==10 and H<=labels.keys(), 'ten distinct HIGH labels')
        need(all(set(group)-H for group in groups), 'negative witness outside HIGH remains')
        outcomes.append(dict(sign=sign,high=sorted(H),baseline_groups_touching=sum(bool(H&set(g)) for g in groups),
                             fixed_capacity=110-26-len(H),credit=len(H)))
    equality=module.source_data(range(1,34),range(1,35),(1,2,3,77),(1,2,3,77))
    need(equality['theta']==160 and 2*77==76+78, 'sharp source L witness')
    minimum=min(((r-33)*(r-34)+6*r+115,r) for r in range(1,67))
    need(minimum[0]==307>304, 'repaired C4/C5 HIGH obstruction')
    return dict(sides=outcomes,conditional_activity_minimum=minimum,activity_budget=304,sharp_L_source=dict(**equality,A=76,delta=76,L=154))


def z3_cards():
    out=[]
    for a,ns,nt in product((0,1),(0,1),range(4)):
        e=10 if a else 8;clip=72*a+70*(ns+nt)
        if e+clip>228: continue
        p,q=2-2*a-ns,2-nt
        rad=radial(220,12,0,-2-ns,4-nt,0,1)
        best=None; count=0
        for r in range(1,67):
            I=(r-33)*(r-34)
            for A in range(I+e+clip,229):
                peel=peel_min(p,q,max(4,A-156),393-A,max(8,A-76))
                for tau in range(A-I-e-clip+1):
                    delta=A-I-tau
                    value=T(r)+4*r+peel[0]+12*68+rad[tau][0]-1026+2*e-delta+4*(2*a+ns+nt)+70*(ns+nt)
                    count+=1
                    if best is None or value<best[0]:
                        best=(value,dict(r=r,I=I,A=A,tau=tau,delta=delta,peel=peel[1:],radial=rad[tau]))
        need(best is not None and best[0]>0,'Z3 conditional scalar certificate')
        out.append(dict(a=a,ns=ns,nt=nt,e=e,minimum=best[0],witness=best[1],states=count))
    expected=[180,242,304,371,150,290,463,106,178,363,65,269]
    need([v['minimum'] for v in out]==expected,'Z3 complete pattern inventory, including three heavy others')
    return out


Z4=[
 ('F',12,-3,1,(2,2),-934,1,8,[('s',1),('s',2),('t',1),('t',1),('t',1)],True,0,1,0,[]),
 ('S',9,0,0,(2,2),-361,3,11,[('s',1),('s',1),('t',1),('t',1)],False,0,0,2,[]),
 ('EH',10,-1,-1,(2,3),-321,2,8,[('s',1),('s',1),('t',1),('t',1),('t',1)],False,0,0,0,[]),
 ('EA_owner',10,-1,-1,(1,3),-391,2,8,[('s',1),('t',1),('t',1),('t',1)],False,0,0,1,[]),
 ('EA_opposite',11,-1,-1,(3,2),-396,2,8,[('s',1),('s',2),('t',1),('t',1)],False,0,0,0,[]),
 ('EC5',11,-1,-1,(2,3),-397,2,8,[('s',1),('s',1),('t',1),('t',1),('t',1)],False,0,0,1,[]),
 ('O',10,4,0,(3,1),-867,4,12,[('s',1),('t',1),('s',1)],True,1,0,0,[288,288,252])]


def z4_cards():
    out=[]
    for name,beta,cs,ct,peels,const,dc,e,endpoints,poly,ms,mt,nc,extra in Z4:
        rad=radial(152,beta,0,cs,ct,ms,mt); records=[]
        for flags in product((0,1),repeat=len(endpoints)):
            h=sum(flags)
            if e+72*h>152:continue
            ps=sum(w for f,(side,w) in zip(flags,endpoints) if f and side=='s')
            pt=sum(w for f,(side,w) in zip(flags,endpoints) if f and side=='t')
            ex=sum(f*v for f,v in zip(flags,extra))
            best=None; count=0
            for A in range(e+72*h,153):
                peel=peel_min(peels[0]-ps,peels[1]-pt,max(4,A-80),317-A,max(8,A))
                # For cards without a side quadratic, setting I=0 enlarges the domain.
                for r in (range(1,67) if poly else [33]):
                    I=(r-33)*(r-34)
                    for tau in range(A-I-e-72*h+1):
                        delta=A-I-tau
                        val=peel[0]+beta*68+rad[tau][0]+const-dc*delta+4*(ps+pt)+nc*72*h+ex
                        if poly:val+=T(r)+4*r
                        count+=1
                        if best is None or val<best[0]:best=(val,dict(r=r,I=I,A=A,tau=tau,delta=delta,peel=peel[1:],radial=rad[tau]))
            need(best is not None and best[0]>0,'Z4 conditional scalar certificate: '+name)
            records.append(dict(flags=flags,minimum=best[0],witness=best[1],states=count))
        out.append(dict(card=name,minimum=min(v['minimum'] for v in records),patterns=records))
    need([v['minimum'] for v in out]==[306,81,253,163,204,295,123], 'Z4 inventory')
    return out


def z5_cards():
    # Literal affine endpoint identities, coordinates Ms Mt Xs Xt gs gt hs ht ds dt.
    names=('Ms','Mt','Xs','Xt','gs','gt','hs','ht','ds','dt')
    v=lambda **kw:tuple(Q(kw.get(k,0)) for k in names)
    Z={'P':v(ds=1,dt=-1,Ms=-2,Xs=-2,Mt=-1,Xt=-1,gs=-1,gt=-1,ht=-1),
       'C5t':v(dt=1,Mt=-2,Xt=-2,Ms=-1,Xs=-1,gs=-1,gt=-1,hs=-1),
       'C6t':v(dt=1,Mt=-2,Xt=-2,Ms=-1,Xs=-1,gs=-1,gt=-1),
       'C7t':v(dt=1,Mt=-2,Xt=-2,Ms=-1,Xs=-1,gt=-1),
       'Us':v(ds=1,Ms=-1,Xs=-1),'Ut':v(dt=1,Mt=-1,Xt=-1),
       'Vs':v(ds=1,Ms=-1,Xs=-1,gs=-1),'Vt':v(dt=1,Mt=-1,Xt=-1,gt=-1),
       'Hs':v(ds=1,hs=1,Ms=-1,Xs=-1),'Ht':v(dt=1,ht=1,Mt=-1,Xt=-1),
       'as':v(hs=1,Ms=-1,Xs=-1),'at':v(ht=1,Mt=-1,Xt=-1)}
    side={k:('s' if k.endswith('s') or k=='P' else 't') for k in Z}
    cards=[('A',['Vs','Vt'],{'P':1,'C5t':2,'as':2,'at':1}),
           ('B',['Vs','Ht'],{'P':1,'C5t':2,'as':2}),
           ('C',['Hs','Ut'],{'P':1,'C5t':2,'as':3}),
           ('D',['Hs','Ht'],{'P':1,'C5t':2}),
           ('E',['Hs','Ut'],{'P':1,'C5t':2,'at':1}),
           ('F',['Us','Ht'],{'P':1,'C5t':2,'at':2}),
           ('G',['Hs','Ht'],{'P':1,'C6t':2,'at':2}),
           ('H',['Hs','Ht'],{'P':1,'C6t':2,'as':1}),
           ('I',['Hs','Ut'],{'P':1,'C6t':2,'as':1,'at':1}),
           ('J',['Hs','Ht'],{'P':1,'C7t':2,'as':1,'at':2}),
           ('K',['Us','Ht'],{'P':1,'C6t':2,'at':2})]
    out=[]
    for name,upper,lower in cards:
        body=tuple(sum(Z[k][i] for k in upper)-sum(w*Z[k][i] for k,w in lower.items())-(2 if i<2 else 0) for i in range(10))
        p,q,ca,cb,cg,dg,ch,dh,ds,dt=body
        need(ds==dt==0, 'literal d cancellation')
        beta=ca+cb+cg+dg; qw=0
        loss=max(ca,cb)/2+max(cg,dg)/2+max(lower.values())
        if name=='D':
            need((cg,dg,ch,dh)==(3,3,3,2),'D actual two triples')
            beta=ca+cb+6;qw=5;loss=max(ca,cb)/2+3+max(lower.values())
        else:need(ch>=0 and dh>=0,'nonnegative discarded h')
        need(beta.denominator==1,'integer overlap weight');beta=int(beta)
        ws=sum(w for k,w in lower.items() if side[k]=='s')+sum(side[k]=='t' for k in upper)
        wt=sum(w for k,w in lower.items() if side[k]=='t')+sum(side[k]=='s' for k in upper)
        rad=radial(68,beta,qw,p-2-ws,q-2-wt)
        # E additionally assumes H_t HIGH, giving three more fixed labels.
        e=11 if name=='E' else 8
        best=None;count=0
        for r in range(1,67):
            ro=67-r;I=(r-33)*(r-34)
            endpoint=sum(w*(72-(r if side[k]=='s' else ro)) for k,w in lower.items())+sum(71-(ro if side[k]=='s' else r) for k in upper)
            for A in range(I+e,77):
                peel=peel_min(p,q,max(4,A-4),241-A,A+76)
                for tau in range(A-I-e+1):
                    delta=A-I-tau
                    val=p*r+q*ro-134+peel[0]+(beta+qw)*68+rad[tau][0]-1114+endpoint+(1-loss)*delta+e*loss
                    count+=1
                    if best is None or val<best[0]:best=(val,dict(r=r,I=I,A=A,tau=tau,delta=delta,peel=peel[1:],radial=rad[tau]))
        need(best is not None and best[0]>0,'Z5 conditional scalar certificate: '+name)
        out.append(dict(card=name,upper=upper,lower=lower,body=dict(zip(names,body)),beta=beta,qweight=qw,loss=loss,
                        errors=[ws,wt],credit=e,minimum=best[0],witness=best[1],states=count))
    need([v['minimum'] for v in out]==[321,141,324,59,7,167,167,25,203,257,167], 'Z5 card inventory')
    return out


def alpha_checks():
    count=0
    for I in range(35):
        for tau in range(35-I):
            for delta in range(42,77-I-tau):
                eps=delta-42
                for xi in range(tau+1):
                    need(68-xi-eps>=tau, 'initial ordinary gap >=tau')
                    need(2*(68-xi)-eps>=2*tau, 'initial star gap >=tau')
                    need(66-eps>tau and 2*66-eps>2*tau, 'strict-gap bootstrap')
                    need(4*I+4*tau-2*xi+13*68>=884>882,'conditional alpha terminal')
                    count+=1
    return dict(scope='Assumes compatible credit 42, all required actual resources, their normal endpoints and the stated transport.',
                states=count,full_core_lower=884,transport_upper=882,margin=2,
                credit42_derived_by_this_checker=False)


def guard_global_claim(upper):
    need(upper == 84, 'size84 structure and all branches have not been completed')


def negative_controls():
    checks=[]
    # Evaluate the original E row at its concrete relaxed witness, with credit 8.
    r,ro,es,et,tau,delta,xi,phi=33,34,80,72,12,64,3,3
    endpoint=(72-r)+2*(72-ro)+(72-ro)+(71-ro)+(71-r)
    old_E=r+3*ro-134+es+3*et+14*(68-2*phi)-3*xi-3*xi-1114+endpoint-5*delta+6*8
    need(old_E == -11, 'old E witness reconstructed')
    invalid=[('non_strict_long_gap',2>=3),
             ('staircase_missing_top_rank',phi_cap(1,1)<=0),
             ('kernel_penalty_15',-16>=-15),
             ('eleven_HIGH_from_ten_labels',10>=11),
             ('old_Z5_E_credit8_is_enough',old_E>0),
             ('omit_three_heavy_endpoints',8+3*70>228),
             ('source_gap_at_delta9_is_strict',9-9>0),
             ('claim_global83_without_structure',False)]
    for name,predicate in invalid:
        try:need(predicate, 'rejected invalid assertion: '+name)
        except ValueError as exc:checks.append(dict(id=name,status='REJECTED',reason=str(exc)))
        else:raise ValueError('negative control accepted: '+name)
    try:guard_global_claim(83)
    except ValueError:pass
    else:raise ValueError('global83 guard failed')
    # Independently compare the optimized peel minimization to complete tiny polygons.
    for p,q in product(range(-2,4),repeat=2):
        for total in range(4,13):
            actual=min((p*x+q*y,x,y) for x in range(2,9) for y in range(2,9) if x+y>=total)
            need(peel_min(p,q,2,8,total)[0]==actual[0], 'peel optimization cross-check')
    return checks


def source_pins():
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
    need(manifest['schema']=='upper83-fullrank-sources-v1','source schema')
    paths=set()
    for item in manifest['files']:
        path=Path(item['path'])
        need(not path.is_absolute() and '..' not in path.parts and str(path) not in paths,'source path')
        paths.add(str(path))
        need(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==item['sha256'],'changed source: '+str(path))
    need({'verification/upper83_fullrank/check.py','reports/upper83_fullrank_20261019.tex'}<=paths,'mandatory sources')
    return dict(files=len(paths),manifest_sha256=hashlib.sha256(MANIFEST.read_bytes()).hexdigest())


def json_value(obj):
    if isinstance(obj,Q):return str(obj)
    raise TypeError(type(obj).__name__)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    pins=source_pins()
    result=dict(schema='upper83-fullrank-v1',status='PASS_CONDITIONAL_PROGRESS_ONLY',current_proved_global_upper=84,
                candidate_global_upper=83,candidate_proved=False,full_size84_structural_reduction_completed=False,
                full_zero_hole_geometric_classification_certified=False,
                core=core_checks(),source=source_checks(),fixed=fixed_checks(),z3=z3_cards(),z4=z4_cards(),z5_a0=z5_cards(),
                alpha_conditional=alpha_checks(),negative_controls=negative_controls(),source_pins=pins)
    guard_global_claim(result['current_proved_global_upper'])
    need(source_pins()==pins,'sources changed during verification')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=json_value)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','current_proved_global_upper','candidate_proved')},ensure_ascii=False))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError) as exc:raise SystemExit('FAIL: '+str(exc))
