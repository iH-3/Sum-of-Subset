#!/usr/bin/env python3
"""Exhaustive search of a stated finite integer box, never a global exclusion."""
import argparse
import json
from itertools import combinations
from exact import analyze

p=argparse.ArgumentParser(description=__doc__)
p.add_argument("--radius", type=int, required=True)
p.add_argument("--size", type=int, required=True)
p.add_argument("--require-zero", action="store_true")
args=p.parse_args()
if args.radius<0 or args.size<1:
    p.error("radius must be nonnegative and size positive")
tested=0
hits=[]
for a in combinations(range(-args.radius,args.radius+1),args.size):
    if args.require_zero and 0 not in a:
        continue
    tested+=1
    # Necessary extreme-subset constraints avoid unnecessary support enumeration.
    if sum(x for x in a if x>0)>4*a[-1] or sum(x for x in a if x<0)<4*a[0]:
        continue
    if analyze(a)["feasible"]:
        hits.append(a)
print(json.dumps({"radius":args.radius,"size":args.size,
                  "require_zero":args.require_zero,"sets_examined":tested,
                  "solutions":hits,"scope":"Exactly the displayed finite box."},indent=2))
