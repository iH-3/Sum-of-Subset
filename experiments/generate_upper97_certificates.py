#!/usr/bin/env python3
"""Optional SciPy discovery; the saved proof is checked using exact arithmetic.

A certificate is first tried across the entire symbolic parameter interval.
Global reuse keeps the proof pool compact. If needed, new weights are found at
an uncovered integer, checked exactly, and assigned to all integers they cover.
Only the standard-library verifier decides acceptance.
"""
import argparse
import json
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verification'))
sys.path.insert(0,str(Path(__file__).resolve().parent))
import upper97 as proof
from generate_upper100_certificates import discover


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=proof.DEFAULT_CERTIFICATE)
    parser.add_argument('--log',type=Path,help='Persist discovery progress independently of solver output')
    args=parser.parse_args()
    if args.log:
        args.log.parent.mkdir(parents=True,exist_ok=True)
        args.log.write_text('',encoding='utf-8')
    def progress(record):
        line=json.dumps(record)
        if args.log:
            with args.log.open('a',encoding='utf-8') as handle:handle.write(line+'\n')
        print(line,flush=True)
    pool,lookup,coverage=[],{},{}
    started=time.monotonic()
    previous=None
    solved=0
    for group in proof.case_groups():
        key,regime,lo,hi=(group[k] for k in ('key','regime','lo','hi'))
        if previous!=regime:
            if previous is not None:
                progress(dict(completed_regime=previous,groups=len(coverage),optimizer_calls=solved,
                              vectors=len(pool),elapsed_seconds=round(time.monotonic()-started,2)))
            previous=regime
        names,symbolic=proof.model(group,proof.Quadratic(0,1))
        candidate=None
        for index,weights in enumerate(pool):
            if not set(weights)<=set(symbolic):continue
            try:proof.interval_certificate(names,symbolic,weights,lo,hi)
            except ValueError:continue
            candidate=index
            break
        if candidate is not None:
            coverage[key]=[[lo,hi,candidate]]
            continue
        chosen={}
        witnesses=[]
        for a in sorted(range(lo,hi+1),key=lambda a:(abs(2*a-lo-hi),a)):
            nn,rr=proof.model(group,a)
            index=None
            for candidate in witnesses:
                try:proof.base.check_integer_certificate(nn,rr,pool[candidate])
                except ValueError:continue
                index=candidate
                break
            if index is None:
                try:weights=discover(nn,rr)
                except RuntimeError as error:raise RuntimeError(f'{key}, a={a}: {error}') from error
                solved+=1
                signature=tuple(sorted(weights.items()))
                if signature not in lookup:
                    lookup[signature]=len(pool)
                    pool.append(dict(signature))
                index=lookup[signature]
                witnesses.append(index)
            chosen[a]=index
        intervals=[]
        for a in range(lo,hi+1):
            if intervals and intervals[-1][1]==a-1 and intervals[-1][2]==chosen[a]:intervals[-1][1]=a
            else:intervals.append([a,a,chosen[a]])
        coverage[key]=intervals
    # Discovery may create a vector later superseded inside the same group.
    used=sorted({segment[2] for segments in coverage.values() for segment in segments})
    remap={old:new for new,old in enumerate(used)}
    pool=[pool[i] for i in used]
    for segments in coverage.values():
        for segment in segments:segment[2]=remap[segment[2]]
    bundle=dict(format='upper97-quadratic-farkas-v1',pool=pool,coverage=coverage)
    checked=proof.check_coverage(bundle)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(bundle,indent=2)+'\n',encoding='utf-8')
    progress(dict(status='PASS',groups=len(coverage),optimizer_calls=solved,vectors=len(pool),
                  interval_checks=checked['interval_checks'],systems=checked['systems'],
                  elapsed_seconds=round(time.monotonic()-started,2)))


if __name__=='__main__':main()
