#!/usr/bin/env python3
"""Check emitted geometric matrix rows against actual translated finite sets."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verification'))
import upper88_candidate as proof

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    key='Z4:A:pair1,pair2,p0,q0:-:-'
    g=next(g for g in proof.roots() if g['key']==key)
    names,root_rows=proof.model(g,36,'global_nested')
    alternatives=proof.branches(g,36,names)
    centers=proof.centers();rng=random.Random(2026101801)
    counts={'root_pair_rows':0,'intersection_rows':0,'absorption_count_rows':0,
            'outer_pair_rows':0,'two_way_quantile_rows':0,'disjoint_allocations':0}
    def check(row,point,label):
        vector,rhs=row
        proof.require(sum(c*point[v] for c,v in zip(vector,names))<=rhs,'Actual-set row failure: '+label)
    for case in range(150):
        P=sorted(rng.sample(range(1,146),36));Q=sorted(rng.sample(range(1,146),36))
        xp=[P[-1]+d for d in sorted(rng.sample(range(1,121),4))]
        yq=[Q[-1]+d for d in sorted(rng.sample(range(1,121),4))]
        D={0}|set(P+xp)|{-v for v in Q+yq}
        point=dict.fromkeys(names,0)
        point.update(Rp=P[-1],Rq=Q[-1],Cp=P[-2],Cq=Q[-2],Mp=xp[-1],Mq=yq[-1],
                     Sp=rng.randrange(100,4001),Sq=rng.randrange(100,4001))
        for side,tail in (('p',xp),('q',yq)):
            for i,x in enumerate(tail[:3],1):point[('x' if side=='p' else 'y')+str(i)]=x
            outer=sorted(rng.sample(range(tail[-1]+1,tail[-1]+2001),4),reverse=True)
            for i,x in enumerate(outer,1):point[side+str(i)]=x
            cutoff=point['M'+side]+point['R'+side]
            point['outside_pairs_'+side]=sum(tail[i]+tail[j]>cutoff for i in range(4) for j in range(i,4))
        values={k:sum(v*point[n] for n,v in form.items()) for k,form in centers.items()}
        supports={};inside={}
        for slot in g['mode']['slots']:
            side=slot[0];c=values[slot];S=point['S'+side]
            W={c+(x if side=='p' else -x) for x in D};supports[slot]=W
            inside[slot]={x for x in W if 1<=x<=S}
            point['l_'+slot]=sum(x<1 for x in W);point['u_'+slot]=sum(x>S for x in W)
        covered=sum(len(set.union(*(inside[v] for v in inside if v[0]==s))) for s in 'pq')
        point['delta']=len(inside)*len(D)-covered+proof.row_policy(g)['fixed_loss']
        for side in 'pq':
            u,v=side+'5',side+'8';point['pair_overlap_'+side]=len(inside[u]&inside[v])
            for hi,lo in ((u,v),(v,u)):
                gap=values[hi]-values[lo]
                plus,minus=(xp,yq) if side=='p' else (yq,xp)
                other='q' if side=='p' else 'p'
                point[f'abs_{hi}_{lo}_lower']=sum(x<=gap+point['R'+side] for x in plus)
                point[f'abs_{hi}_{lo}_upper']=sum(x<=gap+point['R'+other] for x in minus)
        for label,row in root_rows.items():
            if label.startswith('core_pair_'):
                check(row,point,label);counts['root_pair_rows']+=1
        check(root_rows['disjoint_pair_loss'],point,'disjoint_pair_loss');counts['disjoint_allocations']+=1
        for label,parts in alternatives.items():
            if label.startswith('outer_pairs:'):
                matched=[part for part in parts if sum(c*point[v] for c,v in zip(part[0][0],names))<=part[0][1]]
                proof.require(len(matched)==1,'Nonexhaustive outer-pair threshold')
                for row in matched[0]:check(row,point,label);counts['outer_pair_rows']+=1
            elif label.startswith('inner:'):
                # The emitted branches each include a position and a count condition.
                proof.require(any(all(sum(c*point[v] for c,v in zip(row[0],names))<=row[1] for row in part) for part in parts),
                              'Nonexhaustive two-way quantile: '+label)
                counts['two_way_quantile_rows']+=1
            elif label.startswith(('core_pair:','core_tail:')):
                for part in parts:
                    if sum(c*point[v] for c,v in zip(part[0][0],names))>part[0][1]:continue
                    for row in part[1:]:
                        vector,_=row
                        if any(vector[i] for i,v in enumerate(names) if v.startswith('pair_overlap_')):
                            check(row,point,label);counts['intersection_rows']+=1
                        elif any(vector[i] for i,v in enumerate(names) if v.startswith('abs_')):
                            check(row,point,label);counts['absorption_count_rows']+=1
    proof.require(all(v>0 for v in counts.values()),'Vacuous matrix family check')
    paths=['verification/upper88_candidate.py','verification/ordinary_core_overlap.py','verification/crossing_envelopes.py',
           'verification/fixed_scores.py','verification/fixed_score_order.py',str(Path(__file__).relative_to(ROOT))]
    result=dict(status='PASS',cases=150,seed=2026101801,checks=counts,
                scope='Independent actual-set evaluation of emitted rows; supplemental to the general proofs',
                sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
