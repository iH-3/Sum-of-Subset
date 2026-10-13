#!/usr/bin/env python3
"""Check an explicitly given set using exact integers or rational strings."""
import argparse
import json
from pathlib import Path
from exact import analyze, check_certificate

p=argparse.ArgumentParser(description=__doc__)
g=p.add_mutually_exclusive_group(required=True)
g.add_argument("--elements", nargs="+")
g.add_argument("--input", type=Path, help="JSON containing an A array")
g.add_argument("--certificate", type=Path)
p.add_argument("--max-states",type=int,default=1000000)
args=p.parse_args()
if args.certificate:
    out=check_certificate(json.loads(args.certificate.read_text()))
else:
    a=args.elements if args.elements is not None else json.loads(args.input.read_text())["A"]
    out=analyze(a,max_states=args.max_states)
print(json.dumps(out,indent=2))
