#!/usr/bin/env python3
"""Exact conditional size83 C5t exclusion; does NOT prove global N<=82.
Python 3.10+, standard library; supports -I -S -B and -O.
"""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import importlib.util
from itertools import combinations,product
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError(msg)

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

model=load('c5t_model',HERE/'model.py')
cert=load('c5t_certificates',HERE/'certificates.py')

def digest(data):
    return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def manifest_check():
    path=ROOT/'data/upper82_c5t_sources.json'
    data=json.loads(path.read_text())
    need(data['schema']=='upper82-c5t-sources-v1','source manifest schema')
    seen=set()
    for item in data['files']:
        p=Path(item['path'])
        need(not p.is_absolute() and '..' not in p.parts and str(p) not in seen,'source path')
        seen.add(str(p))
        need(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==item['sha256'],'source identity '+str(p))
    need({str(p.relative_to(ROOT)) for p in HERE.glob('*.py')}<=seen,'missing local source pin')
    return data

def endpoint_checks():
    count=0;strict_gains=0
    for rs in range(1,7):
        profiles=list(combinations(range(1,rs+6),rs))
        for index,pos in enumerate(profiles):
            # Reflect a different actual core to test asymmetric sources.
            neg=tuple(x+1 for x in profiles[-1-index])
            rt=len(neg);R=pos[-1];R0=neg[-1]
            offsets=(1,2,4,9);offsets0=(2,3,5,13)
            D=sorted([0,*pos,*(-x for x in neg),*(R+x for x in offsets),*(-R0-x for x in offsets0)])
            for points,r,ro,P,e in [(D,rs,rt,pos,offsets[-1]),(sorted(-x for x in D),rt,rs,neg,offsets0[-1])]:
                tau=sum(x-i for i,x in enumerate(P,1));xi=P[-1]-r;d=len(D);q=d-4
                for k,x in enumerate(points):
                    if k<q:
                        error=0 if k<=ro+4 else tau//(q-k)
                        bound=1+k+r-q+error
                        need(x<=bound,'actual next-rank mass endpoint')
                        strict_gains+=error<xi
                    else:
                        bound=1+k+r-q+xi+e-4
                        need(x<=bound,'actual heavy-tail rank endpoint')
                    count+=1
    need(strict_gains>0,'strict improvement over maximum deviation')
    # This valid monotone profile makes the old common error 29, the new one 0.
    P=tuple(range(1,33))+(62,)
    need(sum(x-i for i,x in enumerate(P,1))==29 and P[-1]-33==29,'rank witness')
    need(31<=70-33,'lower clip31 has zero mass error')
    return dict(order_statistics=count,strict_error_improvements=strict_gains,
                witness=dict(core=list(P),lower_clip=31,old_error=29,new_error=0))

def forest_checks():
    count=0
    # Each physical tree has two arms with lengths2 and3.
    edges=((0,1),(1,2),(0,3),(3,4),(4,5))
    for edge_mask in range(32):
        chosen=[edges[i] for i in range(5) if edge_mask>>i&1]
        used=set(v for row in chosen for v in row)
        for bits in product((0,1),repeat=6):
            hits=sum(bits[a]*bits[b] for a,b in chosen)
            for inside in (0,1):
                loss=sum(bits)-inside*int(any(bits))
                rebate=(1-inside)*(bits[0]+sum(bits[i] for i in range(1,6) if i not in used))
                need(hits+rebate<=loss,'pointwise rooted forest with native rebates')
                count+=1
    return dict(pointwise_checks=count,edge_subsets_per_side=32,combined_subforests=1024)

def arithmetic_checks():
    rows=[]
    for r in range(24,43):
        I=(r-33)**2
        for tau in range(83-I):
            if 4*tau<132+3*I:
                # First force x>=tau by integer rounding, then use safe m-2.
                need(126+3*I+2*tau>6*(tau-1),'first long-gap bootstrap')
                need(48+I>tau,'second strict long-gap bootstrap')
            if 82-I-tau>=71:
                need(4*tau<132+3*I,'every heavy state bootstraps early')
            for rv in (r,66-r):
                for heavy in (False,True):
                    L=min(70,82-I-tau-71*heavy)
                    if L<0:continue
                    points=[(k,0 if k<=70-rv else tau//(71-k)) for k in range(L+1)]
                    hull=[]
                    for k,y in points:
                        while len(hull)>=2 and (hull[-1][1]-hull[-2][1])*(k-hull[-1][0]) <= (y-hull[-1][1])*(hull[-1][0]-hull[-2][0]):hull.pop()
                        hull.append((k,y))
                    for (a,b),(c,d) in zip(hull,hull[1:]):
                        need(all((c-a)*y<=(d-b)*k+(c-a)*b-(d-b)*a for k,y in points),'global upper concave-envelope segment')
            rows.append((r,tau))
    need(min(r*(r+1)//2+4*r+(r-33)**2 for r in range(1,66))==459,'target-span quadratic')
    need(459-318==141 and 2*75+8-63==95,'fresh size83 source constants')
    need(13*75+84==1059 and 1059-6*75==609 and 1059-7*75==534,'physical capacities')
    need(4*67-12-95==161,'pre-owner four-edge bound')
    return dict(rank_mass_pairs=len(rows),physical_capacities=[609,534],target_span_margin=141)

def replay(data):
    need(data['schema']=='upper82-c5t-integer-rays-v1','certificate schema')
    states=list(cert.states());records=data['records'];pool=data['certificates']
    need(len(records)==len(states),'complete finite inventory size')
    counts=Counter();minimum=None;proofs=[]
    for state,record in zip(states,records):
        need(json.loads(json.dumps(state))==record['state'],'missing, duplicate or reordered state')
        index=record['certificate']
        need(type(index) is int and 0<=index<len(pool),'certificate index')
        _,system=cert.system(state,model.build)
        margin=cert.evaluate(pool[index],system)
        need(margin is not None and margin==record['margin'],'exact certificate margin')
        counts[state[0]]+=1;minimum=margin if minimum is None else min(minimum,margin)
        proofs.append((record['state'],index,margin))
    need(counts=={'cutoff':2463,'bootstrap':1780,'terminal':2463},'all three proof stages')
    need(len(pool)==275,'certificate inventory')
    return dict(states=len(states),stages=dict(counts),integer_certificates=len(pool),
                minimum_integer_contradiction=minimum,replay_sha256=digest(proofs))

def controls(data):
    out=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,KeyError,IndexError,TypeError):out.append(label)
        else:raise ValueError('invalid mutation accepted: '+label)
    bad=deepcopy(data);bad['records'].pop()
    reject('omit a finite state',lambda:replay(bad))
    bad2=deepcopy(data);bad2['records'][0]['state'][1]+=1
    reject('wrong physical rank',lambda:replay(bad2))
    reject('negative inequality multiplier',lambda:need(cert.evaluate([('row',-1)],{'row':({'x':-1},1,'le')},False) is not None,'reject sign'))
    reject('negative variable coefficient',lambda:cert.evaluate([('row',1)],{'row':({'x':-1},-1,'le')}))
    reject('nonnegative right side',lambda:cert.evaluate([('row',1)],{'row':({'x':1},0,'le')}))
    E={-3,-1,0,1}
    reject('use strict long-gap bound at equality',lambda:need(len(E&{x+1 for x in E})>=len(E)-1,'strict boundary'))
    reject('claim global82 from one local family',lambda:need(82==83,'global bound is unchanged'))
    return out

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    manifest=manifest_check()
    data=json.loads((ROOT/'data/upper82_c5t_certificates.json').read_text())
    old=load('c5t_old_tail',ROOT/'verification/upper83_tail.py')
    labels,ledger=old.catalogue_checks();inventory=old.tail_inventory(labels)
    core=load('c5t_old_core',ROOT/'verification/upper83_fullrank/check.py')
    result=dict(status='PASS_CONDITIONAL_C5T_SIZE83_FINITE_CERTIFICATES',global_upper_bound=83,
        global_upper82_proved=False,scope='The exact C5t family with common integer source and complete targets',
        source_files=len(manifest['files']),finite=replay(data),endpoints=endpoint_checks(),
        forests=forest_checks(),arithmetic=arithmetic_checks(),ledger=ledger,
        tail_inventory=inventory,core_lemmas=core.core_checks(),negative_controls=controls(data))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print(result['status'],result['finite'])

if __name__=='__main__':main()
