#!/usr/bin/env python3
"""Reconstruct the fixed covering labels and their disjoint sign groups."""
from functools import lru_cache
import json
from pathlib import Path
from nonap_sharp import require


def add(*vectors):return tuple(sum(v[i] for v in vectors) for i in range(8))
def scale(k,v):return tuple(k*x for x in v)
def gap_coordinates(v):return tuple(sum(v[4*(j//4):j+1]) for j in range(8))


@lru_cache(None)
def catalogue():
    units=[tuple(int(i==j) for j in range(8)) for i in range(8)]
    labels={}
    for sign,side,x,y in (('+','p',units[:4],units[4:]),('-','q',units[4:],units[:4])):
        c=add(x[0],*(scale(-1,v) for v in x[1:]))
        alpha=add(x[1],scale(-1,x[2]),scale(-1,x[3]))
        beta=add(scale(2,x[1]),scale(-1,x[0]),scale(-1,x[2]),scale(-1,x[3]))
        b=x+[scale(-1,v) for v in y]
        def put(name,v):
            require(name not in labels,'Duplicate fixed label')
            labels[name]=dict(side=side,coeff=v,gaps=gap_coordinates(v))
        for i in range(8):
            for j in range(i,8):put(f'C{sign}{i+1}{j+1}',add(c,b[i],b[j]))
        for i in range(1,8):
            put(f'U{sign}{i+1}',add(alpha,b[i]));put(f'V{sign}{i+1}',add(beta,b[i]))
        forms=[add(x[2],scale(-1,x[3])),add(scale(2,x[2]),scale(-1,x[1]),scale(-1,x[3])),
               add(x[1],x[2],scale(-1,x[0]),scale(-1,x[3])),
               add(scale(2,x[2]),scale(-1,x[0]),scale(-1,x[3])),
               add(scale(3,x[2]),scale(-1,x[0]),scale(-1,x[1]),scale(-1,x[3]))]
        for i,v in enumerate(forms,1):put(f'F{sign}{i}',v)
    source=Path(__file__).resolve().parents[1]/'data/fixed_cover_certificate.json'
    groups=[];seen=set()
    for template in json.loads(source.read_text())['templates']:
        for reflect in range(1+template['also_reflect']):
            names=template['labels'];expected=tuple(template['coefficient_vector'])
            if reflect:
                names=[n.translate(str.maketrans('+-','-+')) for n in names]
                expected=expected[4:]+expected[:4]
            require(not seen.intersection(names) and len(set(names))==len(names),'Overlapping fixed groups')
            actual=gap_coordinates(add(*(labels[n]['coeff'] for n in names)))
            require(actual==expected and all(v<=0 for v in actual) and any(actual),'Unproved nonpositive group')
            groups.append(list(names));seen.update(names)
    require(len(labels)==110 and len(groups)==26,'Fixed cover inventory changed')
    return dict(labels=labels,groups=groups)


def audit():
    data=catalogue()
    return dict(labels=len(data['labels']),disjoint_groups=len(data['groups']),
                sign_known_nonpositive=sum(all(x<=0 for x in v['gaps']) for v in data['labels'].values()),
                sign_known_positive=sum(all(x>=0 for x in v['gaps']) and any(v['gaps']) for v in data['labels'].values()))
