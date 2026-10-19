#!/usr/bin/env python3
"""Check the new geometric C5t-tail exclusion, conditional on its source model.

This does NOT prove a complete size84 exclusion or N<=83.
Python 3.10+, standard library, exact integers, no solver or assert statements.
"""
import argparse
import hashlib
import importlib.util
from itertools import combinations_with_replacement, product
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'data/upper83_tail_sources.json'


def need(ok,msg):
    if not ok:raise ValueError(msg)


def load_source(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def add(*rows):return tuple(map(sum,zip(*rows)))
def scale(k,row):return tuple(k*x for x in row)
def sub(a,b):return add(a,scale(-1,b))
def basis(n,i):return tuple(int(i==j) for j in range(n))


def catalogue_checks():
    old=load_source('tail_fixed_source','verification/upper83_progress.py')
    labels,gaps,groups=old.fixed_catalogue()
    u=[basis(8,i) for i in range(8)];s,t=u[:4],u[4:]
    lam=[sub(x[0],add(*x[1:])) for x in (s,t)]
    own_O=[add(l,x[0]) for l,x in zip(lam,(s,t))]
    Hs=add(lam[0],s[1]); Ps=sub(lam[0],t[0]); Pt=sub(lam[1],s[0]); C5t=sub(lam[1],s[1])
    high0={f'C{sgn}1{i}' for sgn in '+-' for i in range(1,5)}|{'C+22','C+23','C+24'}
    low={f'C{sgn}5{i}' for sgn in '+-' for i in range(5,9)}|{'C-66','C-67','C-68'}
    for sign,x,O in (('+',s,own_O[0]),('-',t,own_O[1])):
        for i in range(1,5):need(labels[f'C{sign}1{i}']==add(O,x[i-1]),'O HIGH identity')
    for i in range(2,5):need(labels[f'C+2{i}']==add(Hs,s[i-1]),'H HIGH identity')
    for sign,P,op in (('+',Ps,t),('-',Pt,s)):
        for i in range(5,9):need(labels[f'C{sign}5{i}']==sub(P,op[i-5]),'P LOW identity')
    for i in range(6,9):need(labels[f'C-6{i}']==sub(C5t,s[i-5]),'C5t LOW identity')
    ds=sub(s[0],s[1]);gs=sub(s[2],s[3]);hs=sub(s[1],s[2])
    identities={'C+33':add(ds,gs),'U+4':hs,'U+3':add(hs,gs),
                'U+2':add(scale(2,hs),gs),'V+2':sub(add(scale(2,hs),gs),ds)}
    for k,v in identities.items():need(labels[k]==v,'new HIGH identity '+k)
    touched=sum(bool(low&set(group)) for group in groups)
    high=high0|identities.keys()
    need(len(high0)==11 and len(low)==11 and touched==9,'initial ledger')
    need(not high&low and len(high)==16,'distinct final HIGH/LOW labels')
    need(all(set(g)-high for g in groups),'negative baseline witness survives HIGH')
    need(len(high0)+len(low)-touched==13 and len(high)+len(low)-touched==18,'compatible fixed credits')
    return labels,dict(initial_HIGH=sorted(high0),LOW=sorted(low),touched_groups=touched,
                       new_HIGH=sorted(identities),credits=[13,18],final_fixed_capacity=66)


def tail_inventory(labels):
    # Nine categories: eight actual outer entries, and one arbitrary source entry.
    raw=[basis(9,i) for i in range(4)]+[scale(-1,basis(9,i)) for i in range(4,8)]+[basis(9,8)]
    offset=add(*(basis(9,i) for i in range(4)))
    label_lookup={row:name for name,row in labels.items()}
    # Ordered-gap cone: ds=gs+Xs+q, q>0. Each source entry is <=Ms.
    ms,mt,xs,xt,gs,gt,hs,ht,dt,q=[basis(10,i) for i in range(10)]
    ds=add(gs,xs,q)
    s4=add(ms,xs);s3=add(s4,gs);s2=add(s3,hs);s1=add(s2,ds)
    t4=add(mt,xt);t3=add(t4,gt);t2=add(t3,ht);t1=add(t2,dt)
    bounds=[s1,s2,s3,s4,*[scale(-1,x) for x in (t1,t2,t3,t4)],ms]
    threshold=add(scale(2,s1),s3,ms)
    fixed=set();native=set();excluded=0
    for ids in combinations_with_replacement(range(9),4):
        top=sum(i in (0,1) for i in ids)
        two_big=(top==2 and ids.count(0)==2 and all(i in (0,2,3) for i in ids))
        if top<3 and not two_big:
            certificate=sub(threshold,add(*(bounds[i] for i in ids)))
            need(all(x>=0 for x in certificate),'excluded representation cone '+str(ids))
            excluded+=1;continue
        row=sub(add(*(raw[i] for i in ids)),offset)
        if row[-1]:
            need(row[-1]==1,'exactly one free source element')
            native.add(row[:-1])
        else:
            need(row[:-1] in label_lookup,'missing fixed tail representation')
            fixed.add(label_lookup[row[:-1]])
    need(excluded==459 and len(fixed)==32 and len(native)==4,'all 495 formal multisets classified')
    u=[basis(8,i) for i in range(8)];s=u[:4]
    lam=sub(s[0],add(*s[1:]));alpha=sub(s[1],add(s[2],s[3]));beta=sub(add(scale(2,s[1])),add(s[0],s[2],s[3]))
    need(native=={add(lam,s[0]),add(lam,s[1]),alpha,beta},'four genuine native families')
    initial={f'C+1{i}' for i in range(1,5)}|{'C+22','C+23','C+24'}
    beta_six={f'V+{i}' for i in range(3,9)}
    new={'C+33','U+2','U+3','U+4','V+2'}
    ucross={f'U+{i}' for i in range(5,9)}
    need(initial<=fixed and len(initial)==7,'seven already HIGH slots')
    remaining=fixed-beta_six-initial
    need(len(remaining)==19 and new<=remaining,'initial tail 19')
    remaining-=new;need(len(remaining)==14 and ucross<=remaining,'tail 14')
    remaining-=ucross;need(len(remaining)==10,'tail 10')
    pairs=[];ds=sub(s[0],s[1])
    for i in range(5,9):
        pair=[f'C+1{i}',f'C+2{i}'];need(set(pair)<=remaining,'cross pair present')
        need(sub(labels[pair[0]],labels[pair[1]])==ds,'exact d-separated pair')
        pairs.append(pair);remaining-=set(pair)
    need(remaining=={'C+34','C+44'},'only two unpaired slots remain')
    return dict(formal_multisets=495,excluded_by_nonnegative_cones=excluded,native_families=4,
                fixed_tail=sorted(fixed),already_HIGH_removed=sorted(initial),beta_removed=sorted(beta_six),
                new_HIGH_removed=sorted(new),below_threshold_removed=sorted(ucross),cross_pairs=pairs,
                unpaired_tail=sorted(remaining),slot_counts=[32,26,19,14,10,6])


def scalar_checks():
    need(13*76+84==1072 and 1072-6*76==616,'physical source mass')
    need(616+21-71-2*(144-67)==412,'fresh beta cutoff constant')
    need(2*78-4==152 and 412-152-67==193,'fresh source substitution')
    need(9*60-193-76==271 and 271+5*13==336,'strict beta cutoff margin')
    need(325+75-118+6-241==47>0,'source side exceeds both maxima')
    need(4*68-12==260 and 260-76==184,'full-rank four-edge arm')
    need((184+13+1)//2==99 and 99-95==4,'C33 HIGH margin')
    need(2*68-2==134 and -4+1+134+13-95==49,'four extra HIGH without normality')
    need(66-14+18==70 and 70-4==66>19,'U-cross threshold bootstrap')
    need(76+10==86<218,'d-separated cross pairs fit at most once')
    need(66-6+18==78>76,'new final strict contradiction')
    # Exact linear-combination identity for the tail/star lemma.
    # Variables F, c, xi, eps, GB, GA, lb, la.
    F,c,xi,eps,GB,GA,lb,la=[basis(8,i) for i in range(8)]
    combined=add(scale(2,F),scale(-2,c),scale(-2,xi),scale(-1,eps),GB,GA,scale(-2,lb),scale(2,la))
    terminal=add(scale(2,F),scale(-2,c),scale(-2,xi),scale(-2,eps),scale(2,GA))
    remainder=add(sub(eps,add(GB,GA)),scale(2,sub(GB,lb)),scale(2,la))
    need(sub(combined,terminal)==remainder,'rebate identity, all three remainder terms nonnegative')
    states=0
    for r in range(25,43):
        I=(r-33)*(r-34)
        for tau in range(77-I):
            for delta in range(13,77-I-tau):
                for x in range(tau+1):
                    F2x=max(2*(68-x),2*(66-tau+x))
                    need(F2x>=134-tau,'same actual full-or-trim-one choice')
                    need((I+tau+delta-4)+1+F2x-(delta-13)-95>=49+I,'h HIGH scalar')
                    states+=1
    return dict(cutoff_margin=336,source_side_margin=47,C33_HIGH_margin=4,h_HIGH_margin=49,
                intermediate_mass_required=70,final_mass_required=78,allowed_mass=76,final_margin=2,
                scalar_states=states,tail_star_lemma='tau+delta >= m-2-c+e+Gamma_alpha',
                no_normality_assumption=True)


def actual_checks(labels):
    adaptive=load_source('tail_core_source','verification/upper83_fullrank/check.py')
    endpoint_tests=forest_tests=cover_values=0
    for r,ro in ((1,2),(2,3),(3,3),(4,2),(33,34)):
        for profile in range(3):
            P=tuple(i+(profile if i==r else 0) for i in range(1,r+1))
            Q=tuple(i+(profile if i==ro else 0) for i in range(1,ro+1))
            rv,rt=P[-1],Q[-1];ps=(rv+1,rv+2,rv+3,rv+7);pt=(rt+1,rt+2,rt+3,rt+8)
            D={0,*P,*(-x for x in Q),*ps,*(-x for x in pt)};E={0,*P,*(-x for x in Q)};d=len(D)
            for DD,EE,rr,rr_o,xx,xx_o in ((D,E,r,ro,profile,profile),({-x for x in D},{-x for x in E},ro,r,profile,profile)):
                S=sum(x for x in DD if x>0)
                for z in range(-max(DD)-2,S-min(DD)+3):
                    if not any(1<=z+x<=S for x in EE):continue
                    l=sum(z+x<=0 for x in DD);u=sum(z+x>S for x in DD)
                    need(z>=d-4-rr-l-xx and z<=S+rr_o-d+5+u+xx_o,'actual generic endpoint')
                    endpoint_tests+=1
            ms,mt=max(D),-min(D);xs,xt,gs,gt,hs,ht=2+profile,3,3,2,4,5
            ds=gs+xs+5;dt=gt+xt+6
            s4=ms+xs;s3=s4+gs;s2=s3+hs;s1=s2+ds
            t4=mt+xt;t3=t4+gt;t2=t3+ht;t1=t2+dt
            s=(s1,s2,s3,s4);t=(t1,t2,t3,t4);vec=s+t
            ls=s1-s2-s3-s4;lt=t1-t2-t3-t4
            SS=sum(x for x in D if x>0);ST=sum(-x for x in D if x<0)
            two={x+y for x in D for y in D};K=len(two)
            Ls={ls+x for x in two};Lt={lt-x for x in two}
            Vs={ls+s4+x for x in D};Us={ls+s3+x for x in D}
            C7t={lt-s4-x for x in D};C6t={lt-s3-x for x in D}
            a,b=adaptive.select(P),adaptive.select(Q);F=len(E)-a['phi']-b['phi']
            hit=lambda X,S:{x for x in X if 1<=x<=S}
            Dstar=K+d-len(hit(Ls|Vs,SS))+K+d-len(hit(Lt|C7t,ST))
            Darm=K+2*d-len(hit(Ls|Vs|Us,SS))+K+2*d-len(hit(Lt|C7t|C6t,ST))
            need(Dstar>=2*F-2*xs and Darm>=4*F-2*(xs+gs),'actual original-resource forest')
            forest_tests+=2
            if r<=4:
                A=sorted(D|set(s)|{-x for x in t});sums={sum(v) for v in combinations_with_replacement(A,4)}
                inventory={sum(labels[k][i]*vec[i] for i in range(8)) for k in tail_inventory(labels)['fixed_tail']}
                centers=(ls+s1,ls+s2,s2-s3-s4,2*s2-s1-s3-s4)
                cover=inventory|{z+x for z in centers for x in D}
                tail={v-sum(s) for v in sums if v-sum(s)>ds-xs}
                need(tail<=cover,'literal actual 4A tail cover')
                cover_values+=len(tail)
    # Pointwise forest inequalities, including off-target values.
    masks=0
    for bits in product((0,1),repeat=6):
        edges=sum(bits[i]*bits[j] for i,j in ((0,1),(1,2),(3,4),(4,5)))
        for inside_s,inside_t in product((0,1),repeat=2):
            deficiency=sum(bits)-inside_s*int(any(bits[:3]))-inside_t*int(any(bits[3:]))
            need(deficiency>=edges,'pointwise native forest inequality')
            masks+=1
    return dict(generic_endpoint_checks=endpoint_tests,actual_forest_checks=forest_tests,
                actual_tail_values=cover_values,pointwise_forest_masks=masks)


def guard_global_claim(upper):need(upper==84,'one geometric family does not complete the size84 exclusion')


def negative_controls():
    calls=[('omit_C33_but_claim_strict_contradiction',lambda:need(66-7+17>76,'76 is not greater than 76')),
           ('keep_seven_known_HIGH_slots',lambda:need(66-13+18>76,'retaining obsolete slots leaves only 71')),
           ('remove_both_members_of_cross_pair',lambda:need(not (0<5<=86),'one member can still lie in a short interval')),
           ('pair_separation_without_width_guard',lambda:need(100>100,'equal endpoints can both lie in a closed interval')),
           ('lose_native_rebate',lambda:need(66-6+18-30>76,'dropping reserved losses does not certify the desired row')),
           ('claim_global83',lambda:guard_global_claim(83))]
    out=[]
    for name,fn in calls:
        try:fn()
        except ValueError as ex:out.append(dict(id=name,status='REJECTED',reason=str(ex)))
        else:raise ValueError('invalid control accepted '+name)
    return out


def pins():
    obj=json.loads(MANIFEST.read_text(encoding='utf-8'));seen=set()
    need(obj['schema']=='upper83-tail-sources-v1','source schema')
    for x in obj['files']:
        p=Path(x['path']);need(not p.is_absolute() and '..' not in p.parts and str(p) not in seen,'source path')
        seen.add(str(p));need(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==x['sha256'],'source mismatch '+str(p))
    need({'verification/upper83_tail.py','reports/upper83_tail_20261019.tex',
          'verification/upper83_progress.py','verification/upper83_fullrank/check.py',
          'reports/upper83_progress_20261019.tex','reports/upper83_fullrank_20261019.tex',
          'data/fixed_cover_certificate.json',
          'verification/upper84/progress85/foundations/source_triple_fringe85.md',
          'verification/upper84/progress85/common/raw_gap_inventory.md',
          'verification/upper84/progress85/zero/zero85_z5_a1_b.md',
          'verify_upper83_tail_windows.bat'}<=seen,'required source omitted')
    return dict(files=len(seen),manifest_sha256=hashlib.sha256(MANIFEST.read_bytes()).hexdigest())


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    source=pins();labels,ledger=catalogue_checks()
    out=dict(schema='upper83-tail-v1',status='PASS_CONDITIONAL_GEOMETRIC_FAMILY',current_proved_global_upper=84,candidate_proved=False,
             conditional_family='Branch A, common integral source D of size76, complete targets; exact whole holes Os,Hs,Ot,P,C5t. Beta sole ownership is derived.',
             complete_size84_structure=False,all_zero_hole_cases_integrated=False,all_positive_hole_cases_integrated=False,
             ledger=ledger,inventory=tail_inventory(labels),scalar=scalar_checks(),actual=actual_checks(labels),controls=negative_controls(),source_pins=source)
    need(pins()==source,'source changed during verification');guard_global_claim(out['current_proved_global_upper'])
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:out[k] for k in ('status','current_proved_global_upper','candidate_proved')},ensure_ascii=False))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError) as ex:raise SystemExit('FAIL: '+str(ex))
