#!/usr/bin/env python3
"""Optional certificate discovery. Requires SciPy; verification does not.

The optimizer proposes nonnegative weights. Every proposed vector is converted
to integers and checked exactly before being written. Failure to reconstruct a
vector is an error, never an infeasibility conclusion.
"""
import argparse
from fractions import Fraction
import json
from math import gcd, lcm
from pathlib import Path
import sys

from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT / "verification"))
import upper100 as proof


def discover(names,rows):
    labels=list(rows)
    columns=[[-rows[label][0][j] for label in labels] for j in range(len(names))]
    rhs=[rows[label][1] for label in labels]
    solution=linprog([1]*len(labels),A_ub=columns,b_ub=[0]*len(names),
                     A_eq=[rhs],b_eq=[-1],bounds=(0,None),method="highs")
    if not solution.success:
        raise RuntimeError("No certificate discovered: "+solution.message)
    rational=[Fraction(float(w)).limit_denominator(10**7) for w in solution.x]
    denominator=lcm(*(w.denominator for w in rational))
    weights=[int(w*denominator) for w in rational]
    divisor=gcd(*weights)
    if divisor == 0:
        raise RuntimeError("Optimizer returned zero weights")
    certificate={label:w//divisor for label,w in zip(labels,weights) if w}
    proof.check_integer_certificate(names,rows,certificate)
    return certificate


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=proof.DEFAULT_CERTIFICATE)
    args=parser.parse_args()
    pool,lookup,assignments=[],{},{}
    for key,regime,mode,exception in proof.all_cases():
        certificate=discover(*proof.linear_model(regime,mode,exception))
        signature=tuple(sorted(certificate.items()))
        if signature not in lookup:
            lookup[signature]=len(pool)
            pool.append(dict(signature))
        assignments[key]=lookup[signature]
    bundle=dict(format="upper100-integer-farkas-v1",pool=pool,assignments=assignments)
    proof.check_cover(bundle)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(bundle,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(dict(exactly_checked_models=len(assignments),integer_vectors=len(pool))))


if __name__ == "__main__":
    main()
