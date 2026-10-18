#!/usr/bin/env python3
"""Core-overlap loss for two ordinary translates on the same target side."""
from functools import lru_cache
from nonap_sharp import require


def pair_row(difference, remaining_slots, member, sign, core_size, fixed_loss=0, bonus=0):
    """Translate delta >= 2e-Rp-Rq-|u-v|-1+losses into <= form."""
    require(sign in (-1,1),'A center order is required')
    coeff={'Rp':-1,'Rq':-1,'delta':-1}
    for name,value in difference.items():coeff[name]=coeff.get(name,0)-sign*value
    for slot in (*remaining_slots,member):
        for end in ('l','u'):
            name=end+'_'+slot;coeff[name]=coeff.get(name,0)+1
    return coeff,1-2*core_size-fixed_loss-bonus


def outer_pair_alternatives(side,i,j):
    """Count the six small-tail pair labels outside the 2D central hull."""
    require(side in ('p','q') and 1<=i<=j<=3,'Invalid outer pair threshold')
    prefix='x' if side=='p' else 'y';count='outside_pairs_'+side
    threshold={'M'+side:-1,'R'+side:-1}
    for k in (i,j):threshold[prefix+str(k)]=threshold.get(prefix+str(k),0)+1
    pairs=[(a,b) for a in range(1,4) for b in range(a,4)]
    inside=sum(a<=i and b<=j for a,b in pairs)
    outside=sum(a>=i and b>=j for a,b in pairs)
    return ([(threshold,0),({count:1},10-inside)],
            [({k:-v for k,v in threshold.items()},-1),({count:-1},-4-outside)])


def order(coeff):
    """Prove a sign using the positive gaps p1-p2,...,p4 and q analogues."""
    require(set(coeff)<={side+str(i) for side in 'pq' for i in range(1,5)} and all(type(v) is int for v in coeff.values()),'Unknown center-order coordinate')
    gaps=[sum(coeff.get(side+str(k),0) for k in range(1,j+1)) for side in 'pq' for j in range(1,5)]
    if all(v>=0 for v in gaps):return 1
    if all(v<=0 for v in gaps):return -1
    return 0


@lru_cache(maxsize=1)
def audit():
    from itertools import combinations
    import random
    rng=random.Random(20261018);checks=0;strict=0;tail_checks=0;quantile_checks=0;pair_hull_checks=0;joint_checks=0;matching_checks=0
    for sample in range(2400):
        E={0}|set(rng.sample(range(-12,13),rng.randrange(2,18)))
        if min(E)>=0 or max(E)<=0:continue
        extras={min(E)-i for i in (1,3,8,17)}|{max(E)+i for i in (1,4,10,23)}
        D=E|extras;e=len(E);d=len(D);R=max(E)-min(E)
        point2={'K':len({x+y for x in D for y in D}),
                'Rp':max(E),'Rq':-min(E),'Mp':max(D),'Mq':-min(D)}
        for side,tail in (('p',sorted(x for x in extras if x>max(E))),
                          ('q',sorted(-x for x in extras if x<min(E)))):
            cutoff=point2['M'+side]+point2['R'+side]
            point2['outside_pairs_'+side]=sum(tail[i]+tail[j]>cutoff for i in range(4) for j in range(i,4))
            for i,value in enumerate(tail[:3],1):point2[('x' if side=='p' else 'y')+str(i)]=value
            for i in range(1,4):
                for j in range(i,4):
                    alternatives=outer_pair_alternatives(side,i,j)
                    require(any(all(sum(v*point2[k] for k,v in c.items())<=b for c,b in rr) for rr in alternatives),
                            'Outer-pair counting dichotomy fails')
                    pair_hull_checks+=1
        require(point2['K']<=point2['Mp']+point2['Mq']+point2['Rp']+point2['Rq']+1+
                point2['outside_pairs_p']+point2['outside_pairs_q'],'Two-sum pair hull fails')
        S=rng.randrange(1,100);F=set(range(1,S+1))
        centers=rng.sample(range(-70,110),4)
        supports=[{c+x for x in D} for c in centers]
        losses=[len(W-F) for W in supports]
        for c,W in zip(centers,supports):
            lower=sum(x<1 for x in W);upper=sum(x>S for x in W)
            for i in range(1,min(6,len(D))+1):
                low=c+sorted(D)[i-1];high=c+sorted(D)[-i]-S
                require((low<=0 and lower>=i) or (low>=1 and lower<=i-1),
                        'Two-way lower quantile dichotomy fails')
                require((high>=1 and upper>=i) or (high<=0 and upper<=i-1),
                        'Two-way upper quantile dichotomy fails')
                quantile_checks+=2
        total_deficit=4*d-len(set.union(*supports)&F)
        matching=sum(len((supports[i]&supports[j])&F) for i,j in ((0,1),(2,3)))
        require(total_deficit>=sum(losses)+matching,'Disjoint-pair intersection allocation fails')
        matching_checks+=1
        for i,j in combinations(range(4),2):
            pair_deficit=2*d-len((supports[i]|supports[j])&F)
            raw=2*e-R-abs(centers[i]-centers[j])-1
            for k in (i,j):
                bound=raw+losses[k]
                require(pair_deficit>=bound,'Two-translate core bound fails')
                rest=sum(losses[t] for t in range(4) if t not in (i,j))
                require(total_deficit>=bound+rest,'Cross-group allocation fails')
                # Evaluate the actual matrix row on arbitrary set configurations.
                # This catches a sign error in moving the hull width to the left.
                sign=1 if centers[i]>=centers[j] else -1
                coeff,rhs=pair_row({'c'+str(i):1,'c'+str(j):-1},
                    tuple(str(t) for t in range(4) if t not in (i,j)),str(k),sign,e)
                point={'Rp':max(E),'Rq':-min(E),'delta':total_deficit}
                for t in range(4):
                    point['c'+str(t)]=centers[t]
                    point['l_'+str(t)]=sum(x<1 for x in supports[t])
                    point['u_'+str(t)]=sum(x>S for x in supports[t])
                require(sum(value*point[name] for name,value in coeff.items())<=rhs,
                        'The matrix row does not follow from the set inequality')
                hi,lo=(i,j) if centers[i]>=centers[j] else (j,i)
                distance=centers[hi]-centers[lo]
                positive=sorted(x for x in extras if x>max(E))
                negative=sorted(-x for x in extras if x<min(E))
                bonus=sum(x<=distance+max(E) for x in positive)+sum(y<=distance-min(E) for y in negative)
                cc,bb=pair_row({'c'+str(hi):1,'c'+str(lo):-1},
                    tuple(str(t) for t in range(4) if t not in (i,j)),str(k),1,e,bonus=bonus)
                require(sum(v*point[n] for n,v in cc.items())<=bb,'Joint absorbed-tail matrix row fails')
                joint_checks+=1
                for tail,core in ((positive,max(E)),(negative,-min(E))):
                    for count,value in enumerate(tail,1):
                        if value>distance+core:continue
                        cc,bb=pair_row({'c'+str(hi):1,'c'+str(lo):-1},
                            tuple(str(t) for t in range(4) if t not in (i,j)),str(k),1,e,bonus=count)
                        require(sum(v*point[n] for n,v in cc.items())<=bb,
                                'Absorbed-tail matrix row fails on actual sets')
                        tail_checks+=1
                checks+=1
            strict+=raw+max(losses[i],losses[j])>losses[i]+losses[j]
    require(strict>0,'No strict overlap example')
    # Every nonempty subset of [1,16]; a single hull hole forces a disjoint last step.
    single=positive_overlap=0
    for mask in range(1,1<<16):
        X=[i+1 for i in range(16) if mask>>i&1];bits=1
        for v in X[:-1]:bits|=bits<<v
        overlap=bool(bits&(bits<<X[-1]));whole=bits|(bits<<X[-1])
        holes=sum(X)+1-whole.bit_count()
        if holes==1:single+=1;require(not overlap,'A single hole has overlapping last translates')
        if overlap and holes:positive_overlap+=1;require(holes>=2,'Missing two-hole floor')
    return dict(core_pair_checks=checks,matrix_row_checks=checks,absorbed_tail_checks=tail_checks,
                two_way_quantile_checks=quantile_checks,strict_overlap_examples=strict,seed=20261018,
                outer_pair_hull_checks=pair_hull_checks,
                joint_absorption_checks=joint_checks,disjoint_pair_checks=matching_checks,
                single_hole=dict(subsets=65535,single_hole_sets=single,positive_hole_overlaps=positive_overlap),
                scope='Finite sanity checks supplement the arbitrary-set container and single-hole proofs')


if __name__=='__main__':
    import json
    print(json.dumps(audit(),indent=2))
