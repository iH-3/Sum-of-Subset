#!/usr/bin/env python3
"""A short proof spine for N <= 97: endpoint transport and selective refinement.

Only the standard library is used. The mathematical reductions are in
reports/proof_method_20261016.pdf. The previous structural/scalar lemmas are
reused; no previous endpoint certificate file is read.
"""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import upper97 as prior
base=prior.base
require,Quadratic,interval_certificate=prior.require,prior.Quadratic,prior.interval_certificate
ROOT=prior.ROOT
DEFAULT_CERTIFICATE=ROOT/'data/upper97_simplified_certificates.json'
FORMAT='upper97-selective-refinement-v1'
ROOT_COUNTS=dict(Z0=120,P0=112,Z1=1680,P1=1540,Z2=8092,P2=5780,H1=140)


def roots():
    for g in prior.case_groups():
        if g['regime'] not in ('ZL','PL'):yield g


def children(g):
    """All outcomes of the integer loss threshold, not a supplied leaf list."""
    require(g['empty']==1 and g['regime'] in ('Z1','P1'),'Invalid loss refinement')
    yield '-',g
    regime=g['regime'][0]+'L'
    lo,hi=prior.RANGES[regime]
    for v in g['mode']['slots']:
        yield v,dict(g,key=g['key']+'/'+v,regime=regime,large=v,lo=lo,hi=hi)


def source_model(g,a,kind):
    require(kind in ('coarse','core','core_nested','loss','loss_nested'),'Unknown model kind')
    if kind.startswith('core'):require(g['empty']==2,'Core refinement needs two empty units')
    if kind.startswith('loss'):require(g['empty']==1 and g['regime'] in ('Z1','P1','ZL','PL'),'Invalid loss model')
    n,r=prior.model(g,a)
    if kind=='coarse' and g['regime']!='H1':
        # Obtain global rows for the same centers, without importing j=0 budgets.
        nn,rr=prior.model(dict(g,empty=0,large=None),a)
        for v in g['mode']['slots']:
            for label in ('L'+v,'U'+v):
                vector,rhs=rr[label]
                r[label]=([vector[nn.index(x)] for x in n],rhs)
    return n,r


def model(g,a,kind):
    n,r=source_model(g,a,kind)
    # The report proves the transport z -> 14, S_s -> S_s + 14-z.
    # This is not substitution at an arbitrary sample point.
    if 'z' in n:
        zi=n.index('z')
        for label,(v,b) in r.items():
            direction=v[n.index('Sp')]+v[n.index('Sq')]+v[zi]
            if label=='zupper':
                require(v[zi]==1 and sum(abs(x) for x in v)==1 and b==14,'Wrong transport endpoint')
            else:require(direction<=0,'Mass transport can violate a row: '+label)
        r={k:(v,b-14*v[zi]) for k,(v,b) in r.items()}
    drop={'cap','span','zlower','zupper'}
    drop.update(k for k in r if k.startswith('slotcap'))
    if kind in ('coarse','core','loss'):
        drop.update(k for k in r if k.startswith(('Ag','Bg','envelope','I','Hfull','Htilde')))
        drop.add('coarse2D')
        v,b=r['cardinality'];cv,cb=r['coarse2D']
        r['cardinality']=([x+2*y for x,y in zip(v,cv)],b+2*cb)
        remove={'K','x1','x2','x3','y1','y2','y3','z'}
        remove.update(x for x in n if x.startswith('g'))
    else:
        # Hp/Hhat follow from exposed mass + the first three inner gaps.
        drop.update(('Hp','Hq','Hhatp','Hhatq','Ep','Eq','envelope0','envelope4'))
        drop.update(k for k in r if k.startswith(('Aggp0','Aggq0','Bggp0','Bggq0')))
        remove={'z'}|{x for x in n if x.startswith(('gp0','gq0'))}
    r={k:v for k,v in r.items() if k not in drop}
    keep=[i for i,x in enumerate(n) if x not in remove]
    for label,(v,_) in r.items():
        require(all(v[i]==0 or n[i]=='z' for i in range(len(n)) if i not in keep),
                'Projection would discard a nonzero coordinate: '+label)
    return [n[i] for i in keep],{k:([v[i] for i in keep],b) for k,(v,b) in r.items()}


def structural_audit():
    groups=list(roots());counts=Counter()
    for g in groups:counts[g['regime']]+=g['hi']-g['lo']+1
    require(len(groups)==1374 and dict(counts)==ROOT_COUNTS,'Root universe changed')
    scalar=prior.scalar_audit()
    # Cover all actual low states before using any certificate routing choices.
    for state in scalar['low_states']:
        a,z=state['a'],state['z']
        for regime in state['regimes']:
            if regime.endswith('L'):continue
            lo,hi=prior.RANGES[regime]
            require(lo<=a<=hi and (z==0 if regime[0]=='Z' else 1<=z<=14),'Missing actual root')
    return dict(root_groups=len(groups),root_systems=sum(counts.values()),root_counts=dict(counts),
                transport_endpoint=14,scalar_summary=scalar['summary']),scalar



def check_coverage(bundle,exhaustive=False):
    require(bundle.get('format')==FORMAT,'Unknown proof-data format')
    groups=list(roots());expected={g['key'] for g in groups}
    routing,pool=bundle['roots'],bundle['pool']
    require(set(routing)==expected,'Missing or extra root')
    used=set();kinds=Counter();leaf_counts=Counter();details={}
    checks=extrema=systems=leaves=0
    def check_leaf(g,kind,segments):
        nonlocal checks,extrema,systems,leaves
        n,r=model(g,Quadratic(0,1),kind);next_a=g['lo'];out=[];margins=[]
        require(isinstance(segments,list) and segments,'Empty leaf')
        for segment in segments:
            require(isinstance(segment,list) and len(segment)==3 and all(type(x) is int for x in segment),'Malformed interval')
            lo,hi,index=segment
            require(lo==next_a and lo<=hi<=g['hi'],'Gap, overlap, or out-of-range interval')
            require(0<=index<len(pool),'Invalid vector index')
            result=interval_certificate(n,r,pool[index],lo,hi)
            used.add(index);checks+=1;extrema+=result['extremum_points']
            systems+=hi-lo+1;margins.append(result['normalized_gap'])
            out.append(dict(first=lo,last=hi,vector=index,**result))
            if exhaustive:
                gaps=[]
                for a in range(lo,hi+1):
                    nn,rr=model(g,a,kind)
                    require(nn==n and set(rr)==set(r),'Symbolic/numeric row mismatch')
                    for label,(v,b) in r.items():
                        require(rr[label][0]==v and rr[label][1]==Quadratic.coerce(b).at(a),'Symbolic/numeric formula mismatch')
                    gaps.append(base.check_integer_certificate(nn,rr,pool[index])['normalized_gap'])
                require(min(gaps)==result['normalized_gap'],'Wrong interval extremum')
            next_a=hi+1
        require(next_a==g['hi']+1,'Missing endpoint')
        leaves+=1;leaf_counts[kind]+=1
        return dict(kind=kind,systems=g['hi']-g['lo']+1,variables=len(n),rows=len(r),
                    minimum_normalized_gap=min(margins),segments=out)
    for g in groups:
        node=routing[g['key']];kind=node.get('kind');kinds[kind]+=1
        require(kind in ('coarse','core','core_nested','split'),'Invalid refinement rule')
        if kind=='split':
            require(set(node)=={'kind','children'},'Malformed refinement node')
            kids=dict(children(g))
            require(set(node['children'])==set(kids),'Missing or extra loss outcome')
            checked={}
            for v,h in kids.items():
                child=node['children'][v]
                require(set(child)=={'kind','segments'} and child['kind'] in ('loss','loss_nested'),'Malformed loss leaf')
                checked[v]=check_leaf(h,child['kind'],child['segments'])
            details[g['key']]=dict(kind=kind,children=checked)
        else:
            require(set(node)=={'kind','segments'},'Malformed terminal node')
            details[g['key']]=check_leaf(g,kind,node['segments'])
    require(used==set(range(len(pool))),'Unused vector')
    all_leaves=[v for x in details.values() for v in (x['children'].values() if 'children' in x else [x])]
    return dict(root_groups=len(groups),root_systems=sum(ROOT_COUNTS.values()),routing_counts=dict(kinds),
                leaf_groups=leaves,leaf_counts=dict(leaf_counts),systems=systems,vectors=len(pool),
                interval_checks=checks,extremum_points=extrema,
                minimum_normalized_gap=min(v['minimum_normalized_gap'] for v in all_leaves),
                details=details)


def negative_controls(bundle):
    rejected=[]
    def rejects(label,f):
        try:f()
        except (ValueError,KeyError):rejected.append(label)
        else:raise ValueError('Invalid input accepted: '+label)
    g=next(roots());n,r=model(g,Quadratic(0,1),'coarse')
    rejects('negative_weight',lambda:interval_certificate(n,r,{'Gp':-1},g['lo'],g['hi']))
    rejects('noncontradictory_weight',lambda:interval_certificate(n,r,{'Dp1':1},g['lo'],g['hi']))
    rejects('unknown_row',lambda:interval_certificate(n,r,{'cap':1},g['lo'],g['hi']))
    rejects('interior_vertex_failure',lambda:interval_certificate(['x'],{'r':([0],Quadratic(0,2,-1))},{'r':1},-1,3))
    bad=deepcopy(bundle);del bad['roots'][g['key']]
    rejects('missing_root',lambda:check_coverage(bad))
    bad2=deepcopy(bundle);bad2['roots'][g['key']]['segments'][0][0]+=1
    rejects('missing_integer',lambda:check_coverage(bad2))
    losskey=next(k for k,v in bundle['roots'].items() if v['kind']=='split')
    bad3=deepcopy(bundle);child=next(k for k in bad3['roots'][losskey]['children'] if k!='-')
    del bad3['roots'][losskey]['children'][child]
    rejects('missing_large_loss_choice',lambda:check_coverage(bad3))
    bad4=deepcopy(bundle);bad4['roots'][losskey]['kind']='core'
    rejects('malformed_refinement',lambda:check_coverage(bad4))
    rejects('unjustified_core_quantiles',lambda:model(g,40,'core'))
    split=next(g['key'] for g in roots() if g['mode']['member']=='q')
    bad5=deepcopy(bundle);del bad5['roots'][split]
    rejects('missing_actual_contributor_choice',lambda:check_coverage(bad5))
    rejects('unproved_next_cardinality',lambda:prior.scalar_audit(97))
    # Opposite transport increases the cardinality row; detect this from its matrix.
    pg=next(h for h in roots() if h['regime']=='P0')
    nn,rr=source_model(pg,40,'coarse');v,_=rr['cardinality']
    wrong=-sum(v[nn.index(x)] for x in ('Sp','Sq','z'))
    rejects('wrong_endpoint_transport',lambda:require(wrong<=0,'Transport to zero can violate cardinality'))
    return rejected


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates',type=Path,default=DEFAULT_CERTIFICATE)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--exhaustive',action='store_true')
    args=parser.parse_args()
    bundle=json.loads(args.certificates.read_text(encoding='utf-8'))
    structural,scalar=structural_audit()
    finite=check_coverage(bundle,args.exhaustive);guards=negative_controls(bundle)
    summary=dict(status='PASS',conclusion='N <= 97; simplified proof, unchanged numerical bound',
                 verification_mode='interval-plus-exhaustive' if args.exhaustive else 'symbolic-interval',
                 structural=structural,linear={k:v for k,v in finite.items() if k!='details'},negative_controls=guards)
    paths=[Path(__file__),Path(prior.__file__),Path(prior.prior.__file__),Path(base.__file__),args.certificates]
    out=dict(summary=summary,scalar_audit=scalar,proof_checks=finite['details'],
             sha256={str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,default=base.json_default,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,default=base.json_default,indent=2))


if __name__=='__main__':main()
