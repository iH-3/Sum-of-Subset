#!/usr/bin/env python3
"""Evaluate emitted geometric rows on independently constructed finite sets.

This checks row encoding, not the existence of feasible 90-element sets. The
global cardinality budget and activity classification are deliberately outside
this finite test; each conditional geometric row uses its actual-set guard.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'verification'))
import upper89 as proof


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    group = next(g for g in proof.roots() if g['key']=='Z4:A:pair1,pair2,p0,q0:-:-')
    names, rows = proof.model(group, 36, 'global_nested')
    alternatives = proof.branches(group, 36, names)
    slots = group['mode']['slots']
    forms = proof.centers()
    rng = random.Random(2026101802)
    counts = Counter()
    minimum = {}

    def value(row, point):
        vector, rhs = row
        return rhs-sum(c*point[v] for c,v in zip(vector,names))

    def check(label, point, family):
        margin = value(rows[label], point)
        proof.require(margin >= 0, 'Actual-set row failure: '+label)
        counts[family] += 1
        minimum[family] = min(minimum.get(family, margin), margin)

    for case in range(120):
        core = {s:sorted(rng.sample(range(1, r+1+(case%4)*20), r))
                for s,r in [('p',36),('q',37)]}
        tails = {s:[core[s][-1]+v for v in sorted(rng.sample(range(1,82),4))] for s in 'pq'}
        D = {0}|set(core['p']+tails['p'])|{-v for v in core['q']+tails['q']}
        two = {x+y for x in D for y in D}
        point = dict.fromkeys(names, 0)
        point['K'] = len(two)
        lead_centers = {}
        for s in 'pq':
            point.update({'R'+s:core[s][-1], 'C'+s:core[s][-2],
                          'M'+s:tails[s][-1], 'S'+s:sum(core[s]+tails[s])})
            for i,x in enumerate(tails[s][:-1],1):
                point[('x' if s=='p' else 'y')+str(i)] = x
            lower = sorted([tails[s][-1]+v for v in rng.sample(range(1,70),3)],reverse=True)
            cp = [-lower[1]-lower[2]+1, 0, 1, point['S'+s]//2,
                  point['S'+s]-1,point['S'+s],point['S'+s]+1][(case+(s=='q'))%7]
            outer = [sum(lower)+cp]+lower
            proof.require(outer[0]>outer[1], 'Unordered generated outer points')
            for i,x in enumerate(outer,1):point[s+str(i)] = x
            lead_centers[s] = cp
        centers = {k:sum(c*point[v] for v,c in f.items()) for k,f in forms.items()}
        supports = {}
        hits = {}
        for s in 'pq':
            directed = D if s=='p' else {-x for x in D}
            directed_two = two if s=='p' else {-x for x in two}
            supports['lead_'+s] = {lead_centers[s]+x for x in directed_two}
            for v in slots:
                if v[0]==s:supports[v] = {centers[v]+x for x in directed}
        for v,W in supports.items():
            s = v[-1] if v.startswith('lead_') else v[0]
            S = point['S'+s]
            hits[v] = {x for x in W if 1<=x<=S}
            if v.startswith('lead_'):point[v] = len(W)-len(hits[v])
            else:
                point['l_'+v] = sum(x<1 for x in W)
                point['u_'+v] = sum(x>S for x in W)
        def deficit(members):
            return sum(len(supports[v]) for v in members)-len(set().union(*(hits[v] for v in members)))
        for s in 'pq':
            for start in (0,4):
                vv = [v for v in slots if v[0]==s and start<=int(v[1:])<start+4]
                if len(vv)>=2 or (start==0 and vv):
                    point['overlap_'+s+str(start)] = deficit((['lead_'+s] if start==0 else [])+vv)
            members = [v for v in slots if v[0]==s and (int(v[1:])<4 or int(v[1:]) in (6,7))]
            point['full_'+s] = deficit(['lead_'+s]+members)
        point['delta'] = sum(deficit(['lead_'+s]+[v for v in slots if v[0]==s]) for s in 'pq')+8
        for t in range(4):
            cuts = {s:[core[s][-1]]+tails[s] for s in 'pq'}
            width = cuts['p'][t]+cuts['q'][t]+1
            for i in range(t+1,5):
                for s in 'pq':point[f'g{s}{t}{i}'] = min(cuts[s][i]-cuts[s][i-1], width)

        for label in rows:
            if label.startswith(('tails_', 'envelope', 'Ag', 'Bg')) or label=='coarse2D':
                check(label, point, 'double_sum_envelopes')
            elif label.startswith(('overlap_sum_', 'overlap_hull_', 'leading_group_')):
                check(label, point, 'core_group_deficits')
            elif label in ('loss','joint_overlap','full_joint'):
                check(label, point, 'disjoint_group_allocation')
            elif (label.startswith('full_') and '_raw_' in label) or label in ('full_p_sum','full_q_sum'):
                check(label, point, 'full_translate_raw')
            elif label.startswith('full_') and '_clip_' in label:
                # All clipped subgroups contain the leading resource.
                s = label.split('_')[2] if label.startswith('full_own_') else label.split('_')[1]
                if hits['lead_'+s]:check(label, point, 'full_translate_clipped')

        for label, parts in alternatives.items():
            if not label.startswith(('core:','ordinary:','inner:')):continue
            v = label.split(':')[1]
            if not hits[v]:continue
            proof.require(any(all(value(row,point)>=0 for row in part) for part in parts),
                          'Nonexhaustive actual-set alternative: '+label)
            counts['alternatives_'+label.split(':')[0]] += 1

    # Tiny, independent counterexamples catch the exact logical hazards: two
    # native losses may not both be charged with a raw overlap, and a paired
    # resource cannot receive two full capacities.
    A={0,1};B={1,2};F=set()
    G=len(A)+len(B)-len((A|B)&F)
    proof.require(len(A&B)+len(A-F)+len(B-F)>G, 'Double-loss negative control failed')
    pair_capacity = 2
    pair_target = (A|B)&F
    proof.require(len(pair_target)<=pair_capacity, 'Invalid toy paired capacity')
    pair_deficit = pair_capacity-len(pair_target)
    proof.require(len(A-F)+len(B-F)>pair_deficit, 'Paired-capacity negative control failed')
    proof.require(all(counts[k]>0 for k in ('double_sum_envelopes','core_group_deficits',
                  'disjoint_group_allocation','full_translate_raw','full_translate_clipped',
                  'alternatives_core','alternatives_ordinary','alternatives_inner')), 'Vacuous family')
    paths = ['verification/upper89.py', str(Path(__file__).relative_to(ROOT))]
    result = dict(status='PASS_FINITE_GEOMETRY_ONLY',cases=120,seed=2026101802,
                  checks=dict(counts),minimum_margin=minimum,negative_controls=2,
                  scope=__doc__,sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
