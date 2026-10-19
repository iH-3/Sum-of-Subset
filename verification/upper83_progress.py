#!/usr/bin/env python3
"""Exact finite checks for new source/trim theorems and partial size-84 work.

This is deliberately a PROGRESS verifier: it does not prove N <= 83.
The universal arguments and all geometric licenses are in the report.
Python 3.10+, standard library only; all predicates survive -O.
"""
import argparse
from itertools import combinations, product
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'data/upper83_progress_sources.json'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def source_data(P, Q, s, t):
    rs, rt = max(P), max(Q)
    D = (0,) + tuple(P) + tuple(-x for x in Q)
    D += tuple(rs+x for x in s) + tuple(-rt-x for x in t)
    need(len(D) == len(set(D)), 'source must be a set')
    lo = min(D)
    bits = sum(1 << (x-lo) for x in D)
    pairs = 0
    for x in D:
        pairs |= bits << (x-lo)
    K = pairs.bit_count()
    fringe = lambda v: len({x+y for x in v for y in v if x+y > v[-1]})
    B = fringe(s) + fringe(t)
    a, b, c, e = s
    aa, bb, cc, ee = t
    theta = 2*K - 4*(rs+rt) - a-b-aa-bb-c-cc-e-ee
    return dict(d=len(D), K=K, theta=theta, B=B, joint=theta+B)


def sharp_source(d, kind):
    r = (d-9)//2
    P, Q = range(1, r+1), range(1, d-8-r)
    tails = (1, 2, 3, d+1) if kind == 'theta' else (1, 2, d-1, 2*d-5)
    return source_data(P, Q, tails, tails)


def source_checks(theta_offset=8, joint_offset=18):
    # Affine endpoint proofs for all d>=21 (theta), and r_s,r_t>=4 (joint).
    need((21+4)//2 < 21-8, 'theta: outside max/max gives three central labels')
    need(21-5 > 12 and 21-6 > 13, 'theta: long jumps make quartet fringe four')
    need(all(1+f-h <= theta_offset for f,h in [(10,3),(8,1),(9,2)]), 'theta three cases')
    need((31+14)//2 < 31-8, 'joint: outside max/max gives three central labels')
    need(31-5 > 22 and 31-6 > 23, 'joint: two short-cross cases')
    # H=pi+2B-u <=14. H>10 implies u<=15 and j<b<=14,
    # giving at least min(r_op+3,d-18)>=7 central old-negative labels.
    # One large H: other H<=10. Two large H: these two tag sets are disjoint.
    need(1+24-7 <= joint_offset and 1+28-14 <= joint_offset, 'joint: large H cases')
    need(all(1+f-h <= joint_offset for f,h in [(20,3),(16,1),(18,2)]), 'joint remaining cases')
    examples = []
    for d in range(21,121):
        v = sharp_source(d, 'theta')
        need(v['theta'] == 2*d+8 and v['K'] == 4*d-7, 'sharp theta family')
        need(v['theta'] <= 2*d+theta_offset, 'claimed theta offset')
        if d >= 31:
            q = sharp_source(d, 'joint')
            need(q['theta'] == 2*d+8 and q['B'] == 10 and q['K'] == 6*d-17, 'sharp joint family')
            need(q['joint'] <= 2*d+joint_offset, 'claimed joint offset')
        if d in (39,76,77,120):
            examples.append(dict(d=d,theta=v,joint=sharp_source(d,'joint')))

    # Supplementary actual-set regressions, not the unbounded proofs.
    count = 0
    tails = list(combinations(range(1,9),4))
    for d in (31,39,76,77):
        r = 4 if d == 31 else (d-9)//2
        s = d-9-r
        for profile in range(3):
            P = list(range(1,r+1)); Q = list(range(1,s+1))
            if profile:
                P[-3:] = [r-1,r+1,r+3]
                Q[-2:] = [s,s+2]
            if profile == 2:
                P[-1] += 5; Q[-1] += 3
            for a,b in product(tails,repeat=2):
                v = source_data(P,Q,a,b)
                need(v['theta'] <= 2*d+theta_offset and v['joint'] <= 2*d+joint_offset, 'actual source regression')
                count += 1
    best = (-10**9,None)
    for c in range(3,151):
        for j in range(1,151):
            t = (1,2,c,c+j)
            v = source_data(range(1,34),range(1,35),t,t)
            need(v['joint'] <= 152+joint_offset, 'large-offset source regression')
            count += 1
            if v['joint'] > best[0]:
                best = (v['joint'],dict(tails=t,**v))
    return dict(theta='Theta <= 2d+8 for d>=21',joint='Theta+B_s+B_t <= 2d+18 for d>=31 and both core sides have >=4 points',
                sharp_examples=examples,actual_regression_sources=count,large_offset_maximum=best,
                finite_scope='The sample families check implementations and sharpness; the written central-label argument proves universality.')


def kernel_rows(a, mass=4, q_weight=2, overlap_weight=11, depth=3):
    step = q_weight+overlap_weight
    need(a+mass*depth >= overlap_weight, 'kernel requires a nonnegative infinite-tail increment')
    end = depth*step+overlap_weight-1
    rows=[]
    for k in range(end+1):
        ceilings=[max(0,(k-step*j+overlap_weight-1)//overlap_weight) for j in range(depth+1)]
        value=a*ceilings[0]+mass*sum(ceilings[1:])-k
        rows.append(dict(k=k,ceilings=ceilings,value=value))
    return rows, a+mass*depth-overlap_weight


def select_side(P):
    r=len(P)
    need(r>=3 and tuple(sorted(set(P)))==tuple(P) and P[0]>0, 'positive ordered core')
    dev=[0]+[x-i for i,x in enumerate(P,1)]
    cost,j=min((13*j+11*dev[r-j],j) for j in range(4))
    return dict(tau=sum(dev),xi=dev[-1],cost=cost,trim=j,
                p=j+dev[r-j],values=P[:r-j])


def core_pair(r,s):
    P=list(range(1,r+1));Q=list(range(1,s+1))
    P[-3:]=[r-1,r+1,r+3]
    Q[-2:]=[s,s+2]
    return P,Q


def weighted_checks(penalty_claim=25):
    s,step_s=kernel_rows(2);t,step_t=kernel_rows(4)
    need(min(x['value'] for x in s)==-15 and min(x['value'] for x in t)==-10, 'exact rank-tail minima')
    need(step_s==3 and step_t==5, 'unbounded rank-tail increments')
    need(15+10<=penalty_claim, 'claimed joint penalty')
    direct=0;support_checks=0;samples=[]
    for r in range(3,9):
        for P in combinations(range(1,r+7),r):
            v=select_side(P)
            need(4*v['tau']-2*v['xi']-v['cost']>=-15, 'actual s inequality')
            need(4*v['tau']-v['cost']>=-10, 'actual t inequality')
            direct+=1
            if len(samples)<200 and direct%17==0:samples.append(P)
    for i,P in enumerate(samples):
        Q=samples[-1-i]
        u,v=select_side(P),select_side(Q)
        actual={0,*u['values'],*(-x for x in v['values'])}
        m=len(P)+len(Q)+1
        q=m-u['trim']-v['trim'];F=m-u['p']-v['p']
        need(len(actual)==q and 2*q+11*F==13*m-u['cost']-v['cost'], 'same actual Q retains weighted size')
        for x in range(max(actual)-min(actual)+2):
            need(len(actual & {y+x for y in actual})>=F-x, 'literal translated intersection')
            support_checks+=1
    witnesses=[]
    for r,s0 in ((33,34),(34,34)):
        P,Q=core_pair(r,s0);u,v=select_side(P),select_side(Q);m=r+s0+1
        lhs=4*(u['tau']+v['tau'])-2*u['xi']+13*m-u['cost']-v['cost']
        need(lhs==13*m-25, 'sharp actual core witness')
        witnesses.append(dict(r_s=r,r_t=s0,tau_s=u['tau'],tau_t=v['tau'],xi_s=u['xi'],xi_t=v['xi'],
                              trim_s=u['trim'],trim_t=v['trim'],q=m-u['trim']-v['trim'],F=m-u['p']-v['p'],lhs=lhs))
    return dict(theorem='4tau-2xi_s+2|Q|+11F >= 13|E|-25',rows_s=s,rows_t=t,
                infinite_tail_increments=[step_s,step_t],actual_one_side_cores=direct,
                actual_intersection_checks=support_checks,sharp_witnesses=witnesses,
                size69_lower_before=851,size69_lower_after=872)


def fixed_catalogue():
    unit=[tuple(int(i==j) for i in range(8)) for j in range(8)]
    add=lambda *vs:tuple(sum(v[i] for v in vs) for i in range(8))
    scale=lambda k,v:tuple(k*x for x in v)
    labels={}
    for sign,x,y in (('+',unit[:4],unit[4:]),('-',unit[4:],unit[:4])):
        lam=add(x[0],*(scale(-1,v) for v in x[1:]))
        alpha=add(x[1],scale(-1,x[2]),scale(-1,x[3]))
        beta=add(scale(2,x[1]),scale(-1,x[0]),scale(-1,x[2]),scale(-1,x[3]))
        b=x+[scale(-1,v) for v in y]
        for i in range(8):
            for j in range(i,8):labels[f'C{sign}{i+1}{j+1}']=add(lam,b[i],b[j])
        for i in range(1,8):
            labels[f'U{sign}{i+1}']=add(alpha,b[i]);labels[f'V{sign}{i+1}']=add(beta,b[i])
        forms=[add(x[2],scale(-1,x[3])),add(scale(2,x[2]),scale(-1,x[1]),scale(-1,x[3])),
               add(x[1],x[2],scale(-1,x[0]),scale(-1,x[3])),
               add(scale(2,x[2]),scale(-1,x[0]),scale(-1,x[3])),
               add(scale(3,x[2]),scale(-1,x[0]),scale(-1,x[1]),scale(-1,x[3]))]
        for i,v in enumerate(forms,1):labels[f'F{sign}{i}']=v
    gaps=lambda v:tuple(sum(v[4*(j//4):j+1]) for j in range(8))
    need(len(labels)==110 and len(set(labels.values()))==110,'all formal labels')
    seen=set();groups=[]
    data=json.loads((ROOT/'data/fixed_cover_certificate.json').read_text())
    for template in data['templates']:
        for reflect in range(1+template['also_reflect']):
            names=template['labels']
            if reflect:names=[n.translate(str.maketrans('+-','-+')) for n in names]
            need(not seen.intersection(names),'baseline groups disjoint')
            row=gaps(add(*(labels[n] for n in names)))
            need(all(x<=0 for x in row) and any(row),'strictly negative group sum')
            groups.append(names);seen.update(names)
    need(len(groups)==26,'26 baseline groups')
    need(not seen.intersection({f'C{s}1{i}' for s in '+-' for i in range(1,5)}),'four HIGH labels are outside every baseline group')
    return labels,gaps,groups


def fixed_checks(cap=84):
    labels,gaps,groups=fixed_catalogue()
    original=(24,36,1,1,132,4,5,1)
    g=tuple(10**12*x+17**i for i,x in enumerate(original))
    values={k:sum(a*b for a,b in zip(gaps(row),g)) for k,row in labels.items()}
    positive={k:v for k,v in values.items() if v>0}
    need(len(positive)==len(set(positive.values()))==84,'84 distinct positive fixed values')
    need(len(positive)<=cap,'claimed unconditional fixed allowance')
    need(0 not in values.values(),'strict sign witness')
    return dict(unconditional_sharp_allowance=84,labels=110,baseline_groups=26,
                seed_gaps=original,perturbed_gaps=g,positive_labels=sorted(positive),
                positive_distinct_values=len(set(positive.values())),
                scope='Only the eight strictly ordered positive outer magnitudes are constrained. This is not a feasible A or an endpoint counterexample.')


def endpoint_checks():
    tri=lambda n:n*(n+1)//2
    budget=[]
    for n in (84,85):
        d=n-8;m=d-9;r=m//2;s=m-r;base=tri(r)+tri(s)
        B=18*d+84-base;cap=B+2*d+8
        budget.append(dict(n=n,d=d,core_size=m+1,base_mass=base,source_identity_offset=-B,
                           A_caps_zero=[cap-d*j for j in range(7)]))
    need(budget[0]['A_caps_zero']==[456,380,304,228,152,76,0],'fresh size84 budgets')
    need(budget[1]['A_caps_zero']==[442,365,288,211,134,57,-20],'previous budgets')
    # j=6,w=0 forces I=tau=delta=0 and Theta=160.
    need(304+24-160==168 and 160-18==142,'Z6 U+J and J bounds')
    need(-1052+6*6+8*142==120,'Z6 strict HIGH comparison')
    # General one-hole shape is proved afresh in the report.
    need(max(99-4*12,27+2*12)==51 and 51>17,'Z1 two affine terminal lines')
    need(max(408-5*12,336+12)-10==338 and 338-304==34,'conditional Z2 six-edge terminal')
    need(61>2*14,'positive low-core j>=6 budget exclusion, conditional on structure')
    # Alpha exact transport retains its actual quartet fringe B, not B<=20.
    alpha=[]
    for n in (84,85):
        d=n-8;m=d-8;r=(m-1)//2;s=m-1-r
        B0=18*d+84-tri(r)-tri(s);H=5*d-B0
        rhs=13*d-110-4*H+2*(2*d+18)
        lhs=13*m-25
        alpha.append(dict(n=n,H=H,joint_source_cap=2*d+18,necessary_upper=rhs,proved_lower=lhs,margin=lhs-rhs))
    need(alpha[1]['margin']==57 and alpha[0]['margin']==-23,'do not confuse size85 and size84')
    # A scalar witness shows these scalar rows do not exclude the next alpha case.
    r,s=33,34;I=0;ts,tt=6,3;xs,xt=3,2;delta=67;theta=160;B=10;e=72;q=68;F=63
    need(I+ts+tt+delta==76 and theta+B==170 and delta>=42,'relaxed alpha witness source rows')
    lhs=4*(ts+tt)-2*xs+2*q+11*F
    need(lhs==859 and lhs<=882,'next endpoint scalar obstruction must be retained')
    # Another local old activity implication fails at the new budget.
    need((30-33)*(30-34)+6*30+105==297<=304,'C4/C5 old HIGH contradiction is not portable')
    return dict(budgets=budget,zero_target_hole_j0='excluded by general no-empty lemma',
                zero_target_hole_j1=dict(lower=51,upper=17),
                zero_target_hole_j6=dict(forced='I=tau=delta=0',HIGH_sum_margin=120,extra_fixed_loss=4),
                zero_target_hole_remaining_j=[2,3,4,5],
                conditional_Z2=dict(required_A=338,available_A=304,margin=34,classification_complete=False),
                alpha=alpha,alpha84_relaxation_witness=dict(r_s=r,r_t=s,I=I,tau_s=ts,tau_t=tt,xi_s=xs,xi_t=xt,
                    delta=delta,theta=theta,B=B,e_t=e,q=q,F=F,lhs=lhs,upper=882,
                    scope='Necessary scalar rows only; no actual source simultaneously realizing theta and B is asserted.'),
                earlier_activity_obstruction=dict(r_s=30,r_t=37,I=12,tau=0,delta=285,A=297,cap=304),
                full_size84_structural_reduction_completed=False)


def guard_global_claim(upper):
    need(upper==84,'the size84 exclusion is incomplete; N<=83 is not proved')


def negative_controls():
    records=[]
    calls=[('source_offset_7',lambda:source_checks(theta_offset=7)),
           ('joint_offset_17',lambda:source_checks(joint_offset=17)),
           ('weighted_penalty_24',lambda:weighted_checks(24)),
           ('fixed_allowance_83',lambda:fixed_checks(83)),
           ('partial_progress_as_upper83',lambda:guard_global_claim(83)),
           ('kernel_without_tail_gate',lambda:kernel_rows(1,mass=1,depth=1))]
    for name,call in calls:
        try:call()
        except ValueError as exc:records.append(dict(id=name,status='REJECTED',reason=str(exc)))
        else:raise ValueError('invalid claim accepted: '+name)
    return records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    manifest=json.loads(MANIFEST.read_text())
    paths=[entry['path'] for entry in manifest['files']]
    need(len(paths)==len(set(paths)),'duplicate manifest paths')
    for e in manifest['files']:need(sha(ROOT/e['path'])==e['sha256'],'changed proof source: '+e['path'])
    out=dict(schema='upper83-progress-v1',status='PASS_PROGRESS_ONLY',current_proved_global_upper=84,
             candidate_global_upper=83,candidate_proved=False,source=source_checks(),weighted_core=weighted_checks(),
             fixed_allowance=fixed_checks(),endpoint=endpoint_checks(),negative_controls=negative_controls(),
             source_manifest_sha256=sha(MANIFEST),source_files=len(paths),full_theorem_formally_verified=False)
    guard_global_claim(out['current_proved_global_upper'])
    for e in manifest['files']:need(sha(ROOT/e['path'])==e['sha256'],'proof source changed during run')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:out[k] for k in ('status','current_proved_global_upper','candidate_proved')},ensure_ascii=False))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError) as exc:raise SystemExit('FAIL: '+str(exc))
