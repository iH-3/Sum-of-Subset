#!/usr/bin/env python3
"""Reconstruct the order of fixed scores from positive outer-gap coordinates."""
from functools import lru_cache
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import fixed_scores
from nonap_sharp import require


def validate_edge(lower,upper):
    labels=fixed_scores.catalogue()['labels']
    require(lower in labels and upper in labels and lower!=upper,'Invalid score labels')
    lo,hi=labels[lower],labels[upper]
    difference=[v-u for u,v in zip(lo['gaps'],hi['gaps'])]
    require(all(v>=0 for v in difference) and any(difference),'Unproved fixed-score ordering')
    return dict(lower=lower,upper=upper,gap_difference=difference,same_target=lo['side']==hi['side'])


@lru_cache(maxsize=1)
def catalogue():
    labels=fixed_scores.catalogue()['labels'];edges=set()
    for u,lo in labels.items():
        for v,hi in labels.items():
            if u!=v and all(x<=y for x,y in zip(lo['gaps'],hi['gaps'])):
                validate_edge(u,v);edges.add((u,v))
    covers=sorted((u,v) for u,v in edges if not any((u,w) in edges and (w,v) in edges for w in labels))
    closure=set(covers)
    while True:
        expanded=closure|{(u,w) for u,v in closure for x,w in closure if v==x}
        if expanded==closure:break
        closure=expanded
    require(closure==edges,'Cover graph lost an ordering')
    return dict(labels=len(labels),ordered_pairs=len(edges),cover_relations=len(covers),
                edges=[validate_edge(u,v) for u,v in covers],
                rule='score lower < score upper implies N_upper <= N_lower; on the same target H_lower <= H_upper')


@lru_cache(maxsize=1)
def sign_clauses():
    """Compress valid nonpositive pairs/triples using the verified score order."""
    from itertools import combinations
    labels=fixed_scores.catalogue()['labels'];names=sorted(labels)
    index={v:i for i,v in enumerate(names)}
    upward={u:sum(1<<index[v] for v in names
                  if all(a<=b for a,b in zip(labels[u]['gaps'],labels[v]['gaps']))) for u in names}
    unique={};counts={}
    for size in (2,3):
        count=0
        for original in combinations(names,size):
            total=[sum(labels[v]['gaps'][i] for v in original) for i in range(8)]
            if not all(v<=0 for v in total):continue
            count+=1
            clause=tuple(u for u in original if not any(v!=u and upward[v]>>index[u]&1 for v in original))
            mask=0
            for u in clause:mask|=upward[u]
            candidate=dict(labels=list(clause),source_labels=list(original),source_gap_sum=total)
            if mask not in unique or original<tuple(unique[mask]['source_labels']):unique[mask]=candidate
        counts[size]=count
    kept=[]
    for mask,c in sorted(unique.items(),key=lambda x:(x[0].bit_count(),x[1]['labels'])):
        if not any(m&mask==m for m,_ in kept):kept.append((mask,c))
    require(all(any(m&mask==m for m,_ in kept) for mask in unique),'Sign-clause compression lost an implication')
    for _,c in kept:
        require(all(v<=0 for v in c['source_gap_sum']),'Unproved sign clause')
        require(all(any(upward[u]>>index[v]&1 for u in c['labels']) for v in c['source_labels']),'Invalid clause lowering')
    return dict(pair_clauses=counts[2],triple_clauses=counts[3],distinct_upward_sets=len(unique),
                retained_clauses=len(kept),clauses=[c for _,c in kept],
                rule='A nonpositive score sum forces at least one nonpositive indicator; score-order implications compress the clauses')


if __name__=='__main__':
    import json
    print(json.dumps(catalogue(),indent=2))
