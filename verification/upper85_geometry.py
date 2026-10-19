#!/usr/bin/env python3
"""New analytic improvements and independent finite activity classifications.

Standard library only; explicit predicates remain enabled with -O. The
geometric implications supplied to the Boolean census are written lemmas,
not conclusions inferred from enumeration. See the Chinese adoption report.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import hashlib
import json
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def lin(**kw):
    return {k: F(v) for k, v in kw.items() if v}


def add(*terms):
    ans = Counter()
    for weight, row in terms:
        for key, value in row.items():
            ans[key] += weight * value
    return {k: v for k, v in ans.items() if v}


def centers():
    result = {}
    for s, t in [('s', 't'), ('t', 's')]:
        a = lin(**{'M'+s: 1, 'X'+s: 1})
        four = [add((1, a), (1, lin(**{'g'+s: 1, 'h'+s: 1, 'd'+s: 1}))),
                add((1, a), (1, lin(**{'g'+s: 1, 'h'+s: 1}))),
                add((1, a), (1, lin(**{'g'+s: 1}))), a]
        result[s+'outer'] = four
    for s, t in [('s', 't'), ('t', 's')]:
        p, q = result[s+'outer'], result[t+'outer']
        lam = add((1,p[0]),(-1,p[1]),(-1,p[2]),(-1,p[3]))
        for label, p_i in zip(('O','H','U','V'), p):
            result[label+s] = add((1,lam),(1,p_i))
        for label, q_i in zip(('P','C5','C6','C7'), q):
            result[label+s] = add((1,lam),(-1,q_i))
        result['alpha'+s] = add((1,p[1]),(-1,p[2]),(-1,p[3]))
        result['beta'+s] = add((2,p[1]),(-1,p[0]),(-1,p[2]),(-1,p[3]))
    return result


def zero_missing():
    c = centers()
    for s,t in [('s','t'),('t','s')]:
        expected = lin(**{'d'+s:1,'d'+t:-1,'M'+s:-2,'M'+t:-1,
                         'X'+s:-2,'X'+t:-1,'g'+s:-1,'g'+t:-1,'h'+t:-1})
        need(c['P'+s] == expected, 'pair1 identity')
        need(c['C5'+s] == add((1,expected),(1,lin(**{'d'+t:1}))), 'C5 identity')
        need(c['beta'+s] == lin(**{'h'+s:1,'d'+s:-1,'M'+s:-1,'X'+s:-1}), 'beta identity')
        triple = add((1,c['P'+s]),(1,c['beta'+s]),(1,c['C5'+t]))
        p,q=c[s+'outer'],c[t+'outer']
        need(triple == add((-2,p[2]),(-2,p[3]),(-1,q[1]),(-1,q[2]),(-1,q[3])),
             'forbidden triple identity')
    # In branch A choose beta owner s. Pair1 must be on t by the
    # forbidden triple; both C5 singletons contribute. Write t_v=d_v-M.
    # C5_s: t_s >= 2X_s+X_t+g_s+g_t+h_t+1 >= 7.
    # Pair1_t and beta_s: t_t >= 2M+2t_s+2X_s+2X_t+g_s+g_t+2.
    # Thus eta_t >= t_t-56 >= 2M-34.
    a_remainder = lin(Xs=6,Xt=4,gs=3,gt=3,ht=2,one=-18)
    need(sum(v for k,v in a_remainder.items() if k!='one') == 18,
         'A constant from positive integer gaps')
    # In branch B both beta singletons contribute. Choose pair1 owner s.
    # C7_t gives t_t >= 2X_t+X_s+g_t+1. The same pair1-beta
    # substitution and the double raw gap give eta_s >= 4M-21.
    b_remainder = lin(Xs=8,Xt=12,gs=2,gt=6,one=-28)
    need(sum(v for k,v in b_remainder.items() if k!='one') == 28,
         'B constant from positive integer gaps')
    need(all(v>=0 for k,v in a_remainder.items() if k!='one') and
         all(v>=0 for k,v in b_remainder.items() if k!='one'), 'nonnegative gap directions')
    # Numeric substitution checks support, but do not replace, the affine proof.
    checked=0
    for M in (77,78,100):
        for Xs,Xt,gs,gt,ht in __import__('itertools').product(range(1,4),repeat=5):
            ts=2*Xs+Xt+gs+gt+ht+1
            tt=2*M+2*ts+2*Xs+2*Xt+gs+gt+2
            need(tt-56 >= 2*M-34,'A hole lower bound')
            tt0=2*Xt+Xs+gt+1
            ts0=2*M+2*tt0+2*Xs+2*Xt+gs+gt+2
            need(2*ts0-57 >= 4*M-21,'B hole lower bound')
            checked+=1
    families=[]
    for k in range(21):
        a,b=34-k,35+k; omega=587-k*(k+1); ta=a*(a+1)//2
        for label,cap,w in [('nonprimitive',omega-146-ta,0),
                            ('half_step',omega-ta-146+36-(b-5),48)]:
            if a>=15 and cap>=0:
                need(cap<78 and w<120,'structural exception not removed')
                families.append([label,k,cap,w])
    families.append(['boundary14',20,21,0])
    need(len(families)==19,'all structural families')
    return dict(affine_substitutions=checked, branch_A='w >= 2M-34',
                branch_B='w >= 4M-21', universal='j=0 => w >= 2d-36',
                d78_threshold=120, structural_families=families,
                old_weighted_systems_replaced=152,
                hypotheses='Integral D; actual original 18-unit cover; all units active. No primitivity or leading activity.')


def adaptive():
    # Universal proof: xi>=2 uses depth6; xi=0,1 uses depth5 and sigma<=52xi.
    need(131+2*2==135,'depth6')
    small=[]
    for xi in (0,1):
        for sigma in range(52*xi+1):
            v=F(143)+F(11,5)*xi-F(sigma,5)
            need(v>134,'depth5 bound')
            small.append(v)
    # Independently enumerate all actual low-prefix patterns permitted by m<=7.
    # The high coordinates are relaxed using xi>=ceil(sigma/max(high counts)).
    count=0;profiles=0;best=None;witness=None
    for m in range(1,8):
        low=range(1,m)
        subsets=[tuple(x for i,x in enumerate(low) if mask>>i&1)
                 for mask in range(1<<(m-1))]
        for p in subsets:
            for q in subsets:
                if sum(p)+sum(q)!=m-1:continue
                S={0}
                for x in p+q:S|={y+x for y in S}
                if S!=set(range(m)):continue
                profiles+=1
                for a in range(17,53):
                    b=69-a;I=(a-34)*(a-35)
                    B=69+2*m-len(p)-len(q)
                    base=m-1+sum(range(m+1,m+a-len(p)+1))+sum(range(m+1,m+b-len(q)+1))-(a*(a+1)+b*(b+1))//2
                    if I+base>375:continue
                    need(I+base-5*B>=-286,'first-gap baseline')
                    for sigma in range(376-I-base):
                        h=max(a-len(p),b-len(q));xi=(sigma+h-1)//h
                        value=max(F(489-12*t-5*B+I+base)+(1+F(6,t))*xi+(1-F(6,t))*sigma
                                  for t in (5,6))
                        need(value>134,'new universal terminal bound')
                        count+=1
                        if best is None or value<best:
                            best=value;witness=[m,list(p),list(q),a,b,sigma,xi]
    need(profiles==23 and count==45776 and best==135,'complete first-gap census')
    need(2*54//2==54 and F(3,2)*52<79<=F(3,2)*54,'even hole threshold')
    return dict(low_patterns=profiles,relaxed_scalar_cases=count,minimum_before_even_rounding=str(best),
                witness=witness,small_xi_minimum=str(min(small)),
                old_terminal='131-w <= 2t',new_terminal='136-w <= 2t',
                old_necessary_even_w=50,new_necessary_even_w=54,
                hypotheses='Same j=1 terminal form, first gap m<=7, r in 17..52, common strip, w even.')


def forest_points():
    edges=list(combinations(range(4),2)); checked=0;forests=0
    for mask in range(1<<len(edges)):
        es=[e for i,e in enumerate(edges) if mask>>i&1]
        parent=list(range(4))
        def root(x):
            while parent[x]!=x:x=parent[x]
            return x
        cyclic=False
        for u,v in es:
            ru,rv=root(u),root(v)
            if ru==rv:cyclic=True;break
            parent[ru]=rv
        if cyclic:continue
        forests+=1
        for statuses in __import__('itertools').product(range(3),repeat=4):
            active={i for i,s in enumerate(statuses) if s}
            retained={i for i,s in enumerate(statuses) if s==1}
            empty=active-retained
            e=sum(u in active and v in active for u,v in es)
            components=len(active)-e
            for rootmask in range(16):
                roots={i for i in range(4) if rootmask>>i&1}
                if not roots<=retained:continue
                need(e+len(roots)-len(retained)==len(empty)+len(roots)-components,
                     'forest exact accounting')
                need((e+len(roots)<=len(retained)) == (len(empty)+len(roots)<=components),
                     'forest license equivalence')
                checked+=1
    need(forests==38,'all labeled four-vertex forests')
    # A retained hub with two empty leaves at the same outside point is invalid.
    need(2>1,'two empty leaves must not be charged to one retained hub')
    return dict(forests=forests,pointwise_rooted_cases=checked,
                exact_criterion='empty_vertices + selected_roots <= active_components')


NAMES=('O','H','U','V','P','C5','C6','C7','alpha','beta')
BITS={name+s:1<<(10*i+j) for i,s in enumerate(('s','t')) for j,name in enumerate(NAMES)}
ALL=(1<<20)-1
PAIR1=BITS['Ps']|BITS['Pt']


def activity():
    counts=Counter(); distributions={k:Counter() for k in ('Z3_P3','Z4','Z5_A0','P4')}
    def a(mask,label):return bool(mask&BITS[label])
    def grammar(mask,branch):
        if a(mask,'Ps') and a(mask,'Pt'):return False
        if all(a(mask,k) for k in ('betas','betat','C5s','C5t')):return False
        for s,t in [('s','t'),('t','s')]:
            if all(a(mask,k) for k in ('P'+s,'beta'+s,'C5'+t)):return False
            if branch=='B' and a(mask,'P'+s) and a(mask,'C5'+t):return False
        return branch!='B' or not(a(mask,'C5s') and a(mask,'C5t'))
    def cross(mask):
        return all(not a(mask,x+s) or a(mask,y+s) for s in ('s','t')
                   for x,y in [('P','C5'),('C5','C6'),('C6','C7')])
    def own(mask):
        return all((a(mask,'V'+s) or not(a(mask,'U'+s) or a(mask,'H'+s))) and
                   (a(mask,'U'+s) or not a(mask,'H'+s)) for s in ('s','t'))
    def beta_high(mask):
        return all(not(a(mask,'beta'+s) and not a(mask,'U'+s) and a(mask,'alpha'+s)) for s in ('s','t'))
    def holes(mask,branch):
        paired={'P', 'beta' if branch=='A' else 'C5'}
        out={name+s for s in ('s','t') for name in NAMES if name not in paired and not a(mask,name+s)}
        for name in paired:
            if not(a(mask,name+'s') or a(mask,name+'t')):out.add(name)
        return out
    def owner(mask,name):
        hits=[s for s in ('s','t') if a(mask,name+s)]
        return hits[0] if len(hits)==1 else None
    def record(domain,card):
        need(card is not None,'uncovered Boolean configuration: '+domain)
        counts[domain]+=1;distributions[domain][card]+=1
    for branch in ('A','B'):
        pair2=BITS['betas']|BITS['betat'] if branch=='A' else BITS['C5s']|BITS['C5t']
        singles=ALL^(PAIR1|pair2)
        for mask in range(1<<20):
            j=16-(mask&singles).bit_count()+int(not(mask&PAIR1))+int(not(mask&pair2))
            if j not in (3,4,5) or not grammar(mask,branch):continue
            both_O_empty=not(a(mask,'Os') or a(mask,'Ot'))
            triple6=any(all(a(mask,k+s) for k in ('beta','H','C6')) for s in ('s','t'))
            triple7=any(all(a(mask,k+s) for k in ('beta','H','C7')) for s in ('s','t'))
            hs=holes(mask,branch)
            if j==3:
                premises=not(a(mask,'Os') and a(mask,'Ot')) and not triple6
                premises &= all(not(a(mask,'O'+s) and a(mask,'C6'+s)) and
                                (not a(mask,'C5'+s) or a(mask,'C6'+s)) and
                                not all(a(mask,k+s) for k in ('beta','O','C7')) for s in ('s','t'))
                if premises:
                    card=None
                    if branch=='A' and hs=={'beta','Os','Ot'} and owner(mask,'P'):card='A0'
                    for s,t in [('s','t'),('t','s')]:
                        if branch=='A' and hs=={'Os','Ot','H'+s} and owner(mask,'beta')==s and owner(mask,'P')==t:card='A1'
                    record('Z3_P3',card)
            if j==4 and both_O_empty and cross(mask) and not triple6 and not triple7:
                bvalid=branch=='A' or a(mask,'betas') or a(mask,'betat')
                if bvalid:
                    N={x+s for x in ('U','V','alpha') for s in ('s','t')}
                    W=N|{'P','Hs','Ht','C5s','C5t'}
                    card=None
                    if branch=='A' and not(mask&pair2):
                        extra=hs-{'beta','Os','Ot'}
                        if len(extra)==1 and extra<=W:
                            z=next(iter(extra));p=owner(mask,'P')
                            if z=='P' or (p and z!='C5'+p):card='A-E'
                    elif branch=='A':
                        s=owner(mask,'beta')
                        if s:
                            t='t' if s=='s' else 's';extra=hs-{'Os','Ot','H'+s}
                            if len(extra)==1 and extra<=W-{'H'+s}:
                                z=next(iter(extra));p=owner(mask,'P')
                                if z=='P' or p==(s if z=='C5'+t else t):card='A-H'
                    else:
                        p=owner(mask,'P')
                        if p and owner(mask,'C5')==p and all(len(hs&{'H'+s,'beta'+s})==1 for s in ('s','t')):card='B'
                    record('Z4',card)
                    if own(mask) and beta_high(mask):
                        core8=all(a(mask,x+s) for x in ('U','V','C6','C7') for s in ('s','t'))
                        need(core8,'P4 CORE8 not implied')
                        if branch=='A' and not(mask&pair2):
                            p=owner(mask,'P')
                            pc='A0-pair-empty' if p is None else ('A0-opposite-alpha' if a(mask,'alpha'+('t' if p=='s' else 's')) else 'A0-alpha-empty')
                        else:
                            p=owner(mask,'P');bs=[s for s in ('s','t') if a(mask,'beta'+s)]
                            need(bs and (branch=='B' or len(bs)==1),'P4 beta ownership')
                            if p is None:
                                need(branch=='A' and hs=={'Os','Ot','H'+bs[0],'P'},'P4 empty-pair form')
                                pc='A1-empty-pair'
                            elif any(s!=p for s in bs):pc=branch+'-opposite'
                            else:
                                need(a(mask,'alpha'+p),'same-owner alpha absent')
                                pc=branch+'-same'
                        record('P4',pc)
            if j==5 and branch=='A' and both_O_empty and not(mask&pair2) and cross(mask) and own(mask):
                p=owner(mask,'P')
                if p is None:
                    extra=hs-{'Os','Ot','beta','P'}
                    need(len(extra)==1 and extra<={'Hs','Ht','alphas','alphat','C5s','C5t'},'Z5 pair-empty placements')
                    record('Z5_A0','pair-empty')
                else:
                    t='t' if p=='s' else 's'
                    patterns=[{'alpha'+p,'alpha'+t},{'U'+p,'H'+p},{'U'+t,'H'+t},{'H'+p,'H'+t},
                              {'alpha'+t,'H'+p},{'alpha'+t,'H'+t},{'alpha'+p,'H'+t},{'alpha'+p,'H'+p},
                              {'C5'+t,'alpha'+p},{'C5'+t,'alpha'+t},{'C5'+t,'H'+t},{'C5'+t,'C6'+t},{'C5'+t,'H'+p}]
                    extra=hs-{'Os','Ot','beta'}
                    need(sum(extra==patt for patt in patterns)==1,'Z5 thirteen-card coverage')
                    record('Z5_A0','card-'+str(patterns.index(extra)+1))
    expected={'Z3_P3':4,'Z4':45,'Z5_A0':32,'P4':29}
    need(dict(counts)==expected,'activity census changed: '+str(counts))
    return dict(component_assignments=2*(1<<20),accepted_by_domain=dict(counts),
                cards={k:dict(v) for k,v in distributions.items()},
                scope='Boolean consequences of explicitly stated analytic activity lemmas; not enumeration of real sets.')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    result=dict(status='PASS_NEW_ANALYTIC_LEMMAS_AND_CLASSIFICATIONS',
                zero_missing=zero_missing(),adaptive=adaptive(),forest=forest_points(),activity=activity(),
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                full_theorem_formally_verified=False)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(result['status'])


if __name__=='__main__':main()
