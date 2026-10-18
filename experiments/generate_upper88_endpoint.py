#!/usr/bin/env python3
"""Discover exact size-89 endpoint certificates; incomplete output is never a proof."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verification'))
sys.path.insert(0,str(Path(__file__).resolve().parent))
import upper88_endpoint as proof
import generate_upper100_certificates as discovery
_original_linprog=linprog

def bounded_linprog(*args,**kwargs):
    last=None
    for method,presolve in (('highs',True),('highs-ipm',True),('highs-ds',False)):
        options=dict(kwargs.get('options') or {},maxiter=10000,time_limit=15,presolve=presolve)
        current=dict(kwargs,method=method,options=options)
        last=_original_linprog(*args,**current)
        if last.status in (0,2,3):return last
    raise RuntimeError('All discovery solver attempts failed: '+last.message)

discovery.linprog=bounded_linprog
linprog=bounded_linprog


def discover(names, rows):
    """Retry rational reconstruction before using exact elimination on the support."""
    from fractions import Fraction as F
    from math import gcd, lcm
    labels=list(rows);vectors=[rows[k][0] for k in labels];rhs=[rows[k][1] for k in labels]
    sol=linprog([1]*len(labels),A_ub=-np.array(vectors,dtype=float).T,
                b_ub=np.zeros(len(names)),A_eq=[rhs],b_eq=[-1],bounds=(0,None))
    if not sol.success:raise RuntimeError('No dual certificate: '+sol.message)
    support=[i for i,w in enumerate(sol.x) if w>1e-10]
    def accept(values):
        denominator=lcm(*(x.denominator for x in values))
        integers=[int(x*denominator) for x in values];divisor=gcd(*integers)
        if divisor==0:return None
        cert={labels[i]:w//divisor for i,w in zip(support,integers) if w}
        try:proof.base.check_integer_certificate(names,rows,cert)
        except ValueError:return None
        return cert
    for limit in (100,1000,10000,100000,1000000,10000000,1000000000):
        cert=accept([F(float(sol.x[i])).limit_denominator(limit) for i in support])
        if cert is not None:return cert
    for tolerance in (1e-9,1e-7,1e-5):
        equations=[[F(rhs[i]) for i in support]+[F(-1)]]
        for j in range(len(names)):
            if abs(sum(vectors[i][j]*sol.x[i] for i in support))<tolerance:
                equations.append([F(vectors[i][j]) for i in support]+[F(0)])
        rank=0;pivots=[];width=len(support)
        for column in range(width):
            pivot=next((r for r in range(rank,len(equations)) if equations[r][column]),None)
            if pivot is None:continue
            equations[rank],equations[pivot]=equations[pivot],equations[rank]
            factor=equations[rank][column];equations[rank]=[v/factor for v in equations[rank]]
            for r in range(len(equations)):
                if r==rank or not equations[r][column]:continue
                factor=equations[r][column]
                equations[r]=[v-factor*w for v,w in zip(equations[r],equations[rank])]
            pivots.append(column);rank+=1
            if rank==width:break
        if rank!=width:continue
        reconstructed=[F(0)]*width
        for r,c in enumerate(pivots):reconstructed[c]=equations[r][-1]
        cert=accept(reconstructed)
        if cert is not None:return cert
    raise RuntimeError('Exact reconstruction failed; no certificate accepted')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=proof.DEFAULT_CERTIFICATE)
    parser.add_argument('--log',type=Path)
    parser.add_argument('--checkpoint',type=Path,help='Resume only a checkpoint with identical model source hashes')
    parser.add_argument('--group',help='Search one canonical group only')
    parser.add_argument('--seed',type=Path,default=ROOT/'data/upper88_partial_certificates.json')
    parser.add_argument('--shard',type=int,default=0)
    parser.add_argument('--shards',type=int,default=1)
    args=parser.parse_args()
    if args.log:args.log.parent.mkdir(parents=True,exist_ok=True);args.log.write_text('')
    def progress(record):
        line=json.dumps(record,default=str)
        if args.log:
            with args.log.open('a',encoding='utf-8') as f:f.write(line+'\n')
        print(line,flush=True)
    if not 0<=args.shard<args.shards:raise ValueError('Invalid shard')
    seed=json.loads(args.seed.read_text())
    pool,routing=seed['pool'],seed['roots']
    lookup={tuple(sorted(w.items())):i for i,w in enumerate(pool)}
    stats=Counter();start=time.monotonic()
    sources=sorted((ROOT/'verification').glob('*.py'))+[Path(__file__),Path(discovery.__file__),ROOT/'data/fixed_cover_certificate.json']
    fingerprint={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    if args.checkpoint and args.checkpoint.exists():
        saved=json.loads(args.checkpoint.read_text())
        if saved['fingerprint']!=fingerprint:raise ValueError('Checkpoint model changed; use another path')
        pool,routing=saved['pool'],saved['roots']
        lookup={tuple(sorted(w.items())):i for i,w in enumerate(pool)}
        stats.update(saved['stats']);progress(dict(resumed_roots=len(routing)))
    def checkpoint():
        if args.checkpoint:
            args.checkpoint.parent.mkdir(parents=True,exist_ok=True)
            temporary=args.checkpoint.with_suffix('.tmp')
            temporary.write_text(json.dumps(dict(fingerprint=fingerprint,pool=pool,roots=routing,stats=dict(stats))))
            temporary.replace(args.checkpoint)
    def intern(w):
        signature=tuple(sorted(w.items()))
        if signature not in lookup:lookup[signature]=len(pool);pool.append(dict(signature))
        return lookup[signature]
    def certificate(n,r):
        stats['certificate_searches']+=1
        try:return intern(discover(n,r))
        except RuntimeError:stats['unsuccessful_searches']+=1;return None
    def feasible(n,r):
        stats['primal_searches']+=1;A,b=zip(*r.values())
        objective=np.zeros(len(n))
        if 'fixed_extra' in n:objective[n.index('delta')]=1
        res=linprog(objective,A_ub=A,b_ub=b,bounds=(0,None),method='highs')
        if res.status not in (0,2):raise RuntimeError(res.message)
        return res
    def tree(g,a,n,r):
        available=proof.branches(g,a,n)
        def terminal(rr):
            index=certificate(n,rr)
            if index is None:raise RuntimeError('Numerical/exact leaf mismatch')
            return dict(vector=index)
        def rec(rr,used,depth,res=None):
            stats['tree_nodes_visited']+=1
            if stats['tree_nodes_visited']%100==0:progress(dict(search_root=g['key'],a=a,depth=depth,**stats,seconds=round(time.monotonic()-start,2)))
            if depth>256:raise RuntimeError('Tree depth exceeded')
            if res is None:res=feasible(n,rr)
            if res.status==2:return terminal(rr)
            available_here=dict(available)
            scores=[]
            for key,parts in available_here.items():
                if key in used:continue
                vals=[max(sum(co*x for co,x in zip(v,res.x))-b for v,b in part) for part in parts]
                if min(vals)>1e-7:scores.append((min(vals),max(vals),key))
            if not scores:
                obstruction=args.output.with_suffix('.stuck.json')
                obstruction.parent.mkdir(parents=True,exist_ok=True)
                obstruction.write_text(json.dumps(dict(group=g,a=a,point=dict(zip(n,res.x)),used=sorted(used),rows=rr),indent=2))
                raise RuntimeError('No violated disjunction: '+g['key']+' a='+str(a))
            scores.sort(reverse=True);candidates=[]
            for score,large,key in scores[:8]:
                rows=[proof.extend_rows(rr,key,side,part) for side,part in enumerate(available_here[key])]
                results=[feasible(n,t) for t in rows];closed=sum(x.status==2 for x in results)
                if closed==2:return dict(split=key,children=[terminal(t) for t in rows])
                bound=min((v.fun for v in results if v.status==0),default=0)
                candidates.append((closed,bound,score,large,key,rows,results))
            candidates.sort(key=lambda x:x[:5],reverse=True)
            closed,bound,score,large,key,rows,results=candidates[0]
            return dict(split=key,children=[rec(t,used|{key},depth+1,v) for t,v in zip(rows,results)])
        result=rec(r,set(),0);progress(dict(tree_closed=g['key'],a=a,kind='binary',seconds=round(time.monotonic()-start,2)))
        return result
    def solve(g,kind,allow_tree=False):
        lo,hi=g['lo'],g['hi'];n,r=proof.model(g,proof.Quadratic(0,1),kind)
        for i,w in enumerate(pool):
            if not set(w)<=set(r):continue
            try:proof.interval_certificate(n,r,w,lo,hi)
            except ValueError:continue
            return dict(kind=kind,segments=[[lo,hi,i]],trees={})
        chosen={};witnesses=[];trees={}
        for a in sorted(range(lo,hi+1),key=lambda a:(abs(2*a-lo-hi),a)):
            nn,rr=proof.model(g,a,kind);index=None
            for i in witnesses:
                try:proof.base.check_integer_certificate(nn,rr,pool[i])
                except ValueError:continue
                index=i;break
            if index is None:
                index=certificate(nn,rr)
                if index is None:
                    if not allow_tree:return None
                    trees[str(a)]=tree(g,a,nn,rr);continue
                witnesses.append(index)
            chosen[a]=index
        segments=[]
        for a in sorted(chosen):
            if segments and segments[-1][1]==a-1 and segments[-1][2]==chosen[a]:segments[-1][1]=a
            else:segments.append([a,a,chosen[a]])
        return dict(kind=kind,segments=segments,trees=trees)
    for ordinal,g in enumerate(proof.roots()):
        if ordinal%args.shards!=args.shard:continue
        if args.group and g['key']!=args.group:continue
        if g['key'] in routing:continue
        try:
            node=solve(g,'coarse')
            if node is None:node=solve(g,'global_nested',True)
        except Exception:
            checkpoint()
            raise
        routing[g['key']]=node
        if len(routing)%100==0:
            checkpoint()
            progress(dict(roots=len(routing),routing=dict(Counter(v['kind'] for v in routing.values())),**stats,seconds=round(time.monotonic()-start,2)))
    def leaves():
        for node in routing.values():
            yield from node['children'].values() if node['kind']=='split' else [node]
    def tree_nodes(node):
        if 'vector' in node:yield node
        else:
            for child in node['children']:yield from tree_nodes(child)
    used=set()
    for node in leaves():
        used.update(s[2] for s in node['segments'])
        for t in node['trees'].values():used.update(x['vector'] for x in tree_nodes(t))
    used=sorted(used);remap={old:new for new,old in enumerate(used)};pool=[pool[i] for i in used]
    for node in leaves():
        for s in node['segments']:s[2]=remap[s[2]]
        for t in node['trees'].values():
            for x in tree_nodes(t):x['vector']=remap[x['vector']]
    bundle=dict(format=proof.FORMAT,pool=pool,roots=routing)
    checked=proof.check_coverage(bundle,partial=bool(args.group) or args.shards>1)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(bundle,separators=(',',':'))+'\n',encoding='utf-8')
    progress(dict(status='PARTIAL' if args.group or args.shards>1 else 'PASS',**{k:v for k,v in checked.items() if k not in ('proof_checks','used_vectors')},discovery=dict(stats),seconds=round(time.monotonic()-start,2)))


if __name__=='__main__':main()
