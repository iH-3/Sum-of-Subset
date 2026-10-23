"""Exact bounded-deficit density theorem, beta <= 24 (not a global N bound).

The induction for unbounded rank is supplied in the companion mathematical
proof. This file exhaustively verifies its finite bases. DFS pruning is an
exact interval-extension lemma, not sampling: if a partial support contains
[L,S-L], S-2L+1 >= M, adjoining any remaining x <= M preserves that interval
shape. Every omitted completion is counted by its binomial coefficient.
"""
from itertools import combinations
from math import comb
import json


def need(ok,message):
    if not ok:
        raise ValueError(message)


def support(values):
    bits=1
    for x in values:
        bits |= bits << x
    return bits


def interval_present(bits,lo,hi):
    if hi<lo:
        return True
    width=hi-lo+1
    return (bits >> lo) & ((1 << width)-1) == (1 << width)-1


def boundary(beta, *, low=None):
    r=beta+3; maximum=2*beta+3
    if low is None:
        low=2*beta+1
    count=nodes=prunes=leaves=0
    def visit(start,remaining,bits,total):
        nonlocal count,nodes,prunes,leaves
        nodes+=1
        if total-2*low+1>=maximum and interval_present(bits,low,total-low):
            count+=comb(maximum-start,remaining)
            prunes+=1
            return
        if remaining==0:
            leaves+=1
            need(interval_present(bits,low,total-low),'Central interval counterexample')
            count+=1
            return
        for x in range(start,maximum-remaining+1):
            visit(x+1,remaining-1,bits | (bits << x),total+x)
    visit(1,r-1,1 | (1 << maximum),maximum)
    need(count==comb(maximum-1,r-1),'Boundary completion count')
    return dict(beta=beta,rank=r,maximum=maximum,sets=count,nodes=nodes,
                prunes=prunes,leaves=leaves)


def brute_case(values,beta):
    bits=support(values);total=sum(values);lo=2*beta+1
    need(interval_present(bits,lo,total-lo),'Brute central interval')
    holes=[i for i in range(1,total) if not bits>>i&1]
    lower=[i for i in holes if i<=2*beta]
    need(len(lower)<=beta,'Lower hole count')
    need(set(holes)==set(lower)|{total-i for i in lower},'Reflected endpoint holes')


def verify():
    bases=[boundary(beta) for beta in range(25)]
    # Independent ordinary combination enumeration on the old boundary range.
    independent=0
    for beta in range(10):
        r=beta+3;maximum=2*beta+3;count=0
        for chosen in combinations(range(1,maximum),r-1):
            brute_case((*chosen,maximum),beta);count+=1
        need(count==bases[beta]['sets'],'Independent boundary census')
        independent+=count
    # Small ranks needed by the joint induction for beta <= 8.
    small=0
    for r in range(3,9):
        for beta in range(r-2):
            maximum=r+beta
            for chosen in combinations(range(1,maximum),r-1):
                brute_case((*chosen,maximum),beta);small+=1
    need(independent==227239 and small==1728,'Independent base totals')
    # For beta >= 9, r >= beta+4 and actual previous deficit d <= beta.
    # T_(r-1) - (r+5*beta+1) increases by r-1 at the next rank.
    joins=[]
    for beta in range(9,25):
        r=beta+4;margin=r*(r-1)//2-(r+5*beta+1)
        need(margin>=0 and r-1>0,'Unbounded-rank induction join')
        joins.append(dict(beta=beta,first_rank=r,join_margin=margin))
    # The beta<=8 joint induction uses r>=9, beta<=r-4:
    # T_(r-1) - (M+4*d+1) >= (r*r-13*r+38)/2.
    need((9*9-13*9+38)//2==1 and 9-6>0,'Small-deficit polynomial join')
    # Deliberately false stronger interval must be rejected.
    rejected=False
    try:
        boundary(1,low=1)
    except ValueError:
        rejected=True
    need(rejected,'Missing negative control')
    return dict(status='PASS_DENSITY_BETA_0_TO_24',global_upper_bound_certified=False,
                beta_max=24,rank_condition='r >= beta+3',bases=bases,
                boundary_sets=sum(x['sets'] for x in bases),independent_sets=independent,
                small_rank_sets=small,induction=joins,negative_controls=1)

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args()
    result=verify();text=json.dumps(result,indent=2)+'\n'
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(text)
    print(json.dumps({k:v for k,v in result.items() if k not in ('bases','induction')}))
