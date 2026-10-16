#!/usr/bin/env python3
"""Discover exact integer certificates for all upper-99 models (SciPy required).

Coverage intervals are a storage compression only: the verifier rebuilds and
checks each integer value of a in every interval. Optimizer output is never
accepted without the exact coefficient check.
"""
import argparse
import json
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verification'))
sys.path.insert(0,str(Path(__file__).resolve().parent))
import upper99 as proof
from generate_upper100_certificates import discover


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=proof.DEFAULT_CERTIFICATE)
    args=parser.parse_args()
    pool,lookup,coverage=[],{},{}
    started=time.monotonic()
    previous=None
    solved=0
    for key,regime,mode,exception in proof.case_groups():
        if previous!=regime:
            if previous is not None:
                print(json.dumps(dict(completed_regime=previous,groups=len(coverage),
                                      optimizer_calls=solved,vectors=len(pool),
                                      elapsed_seconds=round(time.monotonic()-started,2))),flush=True)
            previous=regime
        lo,hi=proof.RANGES[regime]
        witnesses=[]
        chosen={}
        # Start near the middle; an exact check decides every other a.
        for a in sorted(range(lo,hi+1),key=lambda a:(abs(2*a-lo-hi),a)):
            names,rows=proof.linear_model(regime,a,mode,exception)
            index=None
            for candidate in witnesses:
                try:
                    proof.check_integer_certificate(names,rows,pool[candidate])
                except ValueError:
                    continue
                index=candidate
                break
            if index is None:
                weights=discover(names,rows)
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
            if intervals and intervals[-1][1]==a-1 and intervals[-1][2]==chosen[a]:
                intervals[-1][1]=a
            else:
                intervals.append([a,a,chosen[a]])
        coverage[key]=intervals
    bundle=dict(format='upper99-integer-farkas-v1',pool=pool,coverage=coverage)
    proof.check_coverage(bundle)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(bundle,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(groups=len(coverage),optimizer_calls=solved,vectors=len(pool),
                          elapsed_seconds=round(time.monotonic()-started,2))),flush=True)


if __name__=='__main__':
    main()
