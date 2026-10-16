#!/usr/bin/env python3
"""Optional SciPy discovery for the selective proof; exact checks decide acceptance."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verification'))
sys.path.insert(0,str(Path(__file__).resolve().parent))
import upper97_simplified as proof
from generate_upper100_certificates import discover


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=proof.DEFAULT_CERTIFICATE)
    parser.add_argument('--log',type=Path)
    args=parser.parse_args()
    if args.log:
        args.log.parent.mkdir(parents=True,exist_ok=True);args.log.write_text('')
    def progress(record):
        line=json.dumps(record)
        if args.log:
            with args.log.open('a',encoding='utf-8') as f:f.write(line+'\n')
        print(line,flush=True)
    pool,lookup,routing=[],{},{}
    calls=failed=0;start=time.monotonic()
    def solve(g,kind):
        nonlocal calls,failed
        lo,hi=g['lo'],g['hi'];n,r=proof.model(g,proof.Quadratic(0,1),kind)
        for i,w in enumerate(pool):
            if not set(w)<=set(r):continue
            try:proof.interval_certificate(n,r,w,lo,hi)
            except ValueError:continue
            return [[lo,hi,i]]
        chosen={};witnesses=[]
        for a in sorted(range(lo,hi+1),key=lambda a:(abs(2*a-lo-hi),a)):
            nn,rr=proof.model(g,a,kind);index=None
            for i in witnesses:
                try:proof.base.check_integer_certificate(nn,rr,pool[i])
                except ValueError:continue
                index=i;break
            if index is None:
                calls+=1
                try:w=discover(nn,rr)
                except RuntimeError:
                    failed+=1;return None
                signature=tuple(sorted(w.items()))
                if signature not in lookup:
                    lookup[signature]=len(pool);pool.append(dict(signature))
                index=lookup[signature];witnesses.append(index)
            chosen[a]=index
        segments=[]
        for a in range(lo,hi+1):
            if segments and segments[-1][1]==a-1 and segments[-1][2]==chosen[a]:segments[-1][1]=a
            else:segments.append([a,a,chosen[a]])
        return segments
    for g in proof.roots():
        first=solve(g,'coarse')
        if first is not None:node=dict(kind='coarse',segments=first)
        elif g['empty']==2:
            node=None
            for kind in ('core','core_nested'):
                seq=solve(g,kind)
                if seq is not None:node=dict(kind=kind,segments=seq);break
            if node is None:raise RuntimeError('Unclosed two-empty root: '+g['key'])
        elif g['empty']==1:
            kids={}
            for key,h in proof.children(g):
                child=None
                for kind in ('loss','loss_nested'):
                    seq=solve(h,kind)
                    if seq is not None:child=dict(kind=kind,segments=seq);break
                if child is None:raise RuntimeError('Unclosed loss child: '+h['key'])
                kids[key]=child
            node=dict(kind='split',children=kids)
        else:raise RuntimeError('Unclosed root: '+g['key'])
        routing[g['key']]=node
        if len(routing)%100==0:
            progress(dict(roots=len(routing),routing=dict(Counter(v['kind'] for v in routing.values())),
                          optimizer_calls=calls,failed_attempts=failed,seconds=round(time.monotonic()-start,2)))
    def segments(node):
        return [x['segments'] for x in node['children'].values()] if node['kind']=='split' else [node['segments']]
    used=sorted({s[2] for node in routing.values() for seq in segments(node) for s in seq})
    remap={old:new for new,old in enumerate(used)}
    pool=[pool[i] for i in used]
    for node in routing.values():
        for seq in segments(node):
            for s in seq:s[2]=remap[s[2]]
    bundle=dict(format=proof.FORMAT,pool=pool,roots=routing)
    result=proof.check_coverage(bundle)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(bundle,indent=2)+'\n',encoding='utf-8')
    progress(dict(status='PASS',optimizer_calls=calls,failed_attempts=failed,
                  **{k:v for k,v in result.items() if k not in ('details','minimum_normalized_gap')},
                  minimum_normalized_gap=str(result['minimum_normalized_gap']),
                  seconds=round(time.monotonic()-start,2)))


if __name__=='__main__':main()
