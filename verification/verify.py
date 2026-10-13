#!/usr/bin/env python3
"""Independent finite checks. This does not certify the inherited upper-84 proof."""
import argparse
import copy
import json
import sys
from itertools import combinations, combinations_with_replacement
from math import isqrt
from pathlib import Path
from exact import (VerificationError, analyze, check_certificate, family,
                   four_sum_witnesses, normalize, require, subset_sums)

ROOT = Path(__file__).resolve().parents[1]


def check_cover():
    """Reconstruct every label from its definition; do not trust stored vectors."""
    cert = json.loads((ROOT / "data/fixed_cover_certificate.json").read_text())
    zero = (0,) * 8
    def add(*vs):
        return tuple(sum(v[i] for v in vs) for i in range(8))
    def mul(k, v):
        return tuple(k * x for x in v)
    p = [tuple(int(i <= j < 4) for j in range(8)) for i in range(4)]
    q = [tuple(int(i + 4 <= j < 8) for j in range(8)) for i in range(4)]
    labels = {}
    for sign, x, y in [("+", p, q), ("-", q, p)]:
        lam = add(x[0], *[mul(-1, v) for v in x[1:]])
        alpha = add(x[1], mul(-1, x[2]), mul(-1, x[3]))
        beta = add(mul(2, x[1]), mul(-1, x[0]), mul(-1, x[2]), mul(-1, x[3]))
        b = x + [mul(-1, v) for v in y]
        for i in range(8):
            for j in range(i, 8):
                labels[f"C{sign}{i+1}{j+1}"] = add(lam, b[i], b[j])
        for i in range(1, 8):
            labels[f"U{sign}{i+1}"] = add(alpha, b[i])
            labels[f"V{sign}{i+1}"] = add(beta, b[i])
        ff = [add(x[2], mul(-1, x[3])),
              add(mul(2,x[2]),mul(-1,x[1]),mul(-1,x[3])),
              add(x[1],x[2],mul(-1,x[0]),mul(-1,x[3])),
              add(mul(2,x[2]),mul(-1,x[0]),mul(-1,x[3])),
              add(mul(3,x[2]),mul(-1,x[0]),mul(-1,x[1]),mul(-1,x[3]))]
        for i, v in enumerate(ff, 1):
            labels[f"F{sign}{i}"] = v
    used = set()
    groups = 0
    for row in cert["templates"]:
        for reflect in range(2 if row["also_reflect"] else 1):
            names = row["labels"]
            expected = tuple(row["coefficient_vector"])
            if reflect:
                names = [s.translate(str.maketrans("+-", "-+")) for s in names]
                expected = expected[4:] + expected[:4]
            require(not (used & set(names)), "Fixed-label groups overlap.")
            require(len(names) == len(set(names)), "Repeated label within group.")
            actual = add(*[labels[s] for s in names])
            require(actual == expected, "Incorrect coefficient vector.")
            require(all(v <= 0 for v in actual) and actual != zero,
                    "Group is not strictly negative for positive gaps.")
            used.update(names)
            groups += 1
    require(len(labels) == 110 and groups == 26, "Incorrect fixed-cover inventory.")
    return {"labels": len(labels), "disjoint_negative_groups": groups,
            "fixed_capacity": 110-groups}


def cross_checks():
    """Compare independent definitions on every set in [-4,4]."""
    universe = list(range(-4,5))
    count = 0
    for mask in range(1 << len(universe)):
        a = tuple(x for i,x in enumerate(universe) if mask >> i & 1)
        direct_fs = {sum(x) for k in range(len(a)+1) for x in combinations(a,k)}
        direct_four = {sum(x) for x in combinations_with_replacement(a,4)}
        require(subset_sums(a) == direct_fs, "Subset-DP disagreement.")
        require(set(four_sum_witnesses(a)) == direct_four, "2+2 disagreement.")
        count += 1
    require(analyze([-1,0,1])["feasible"], "Sanity example failed.")
    require(not analyze([-1,1])["feasible"], "Subset heredity was incorrectly assumed.")
    require(not analyze([1,2,3])["feasible"], "Translation invariance was incorrectly assumed.")
    require(analyze(["-1/3", "0", "1/3"])["feasible"], "Rational input failed.")
    for bad in ([0,0], [0.1,0.2]):
        try:
            normalize(bad)
        except VerificationError:
            pass
        else:
            raise VerificationError("Invalid input was accepted.")
    return count


def make_certificate():
    a = family(31)
    witnesses = four_sum_witnesses(a)
    return {"schema":"four-sum-certificate-v1", "A":list(a),
            "representations":[{"sum":s,"terms":list(witnesses[s])}
                               for s in sorted(subset_sums(a))]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    if args.write_certificate:
        cert = make_certificate()
        (ROOT / "data/construction71.json").write_text(json.dumps(cert, separators=(",",":"))+"\n")
    cert = json.loads((ROOT / "data/construction71.json").read_text())
    certificate_result = check_certificate(cert)
    for defect in ("bad_sum", "missing_target"):
        bad = copy.deepcopy(cert)
        if defect == "bad_sum":
            bad["representations"][0]["sum"] += 1
        else:
            bad["representations"].pop()
        try:
            check_certificate(bad)
        except VerificationError:
            pass
        else:
            raise VerificationError("Corrupted certificate was accepted.")
    cover = check_cover()
    # Exact integer quadratic, not a floating-point root calculation.
    f = lambda d: d*d-112*d-241
    require(f(114) <= 0 and f(115) > 0 and 2*115-111 > 0,
            "Elementary cardinality cutoff failed.")
    family_results=[]
    for m in (1,2,7,15,30,31,32,33,40):
        result=analyze(family(m))
        require(result["feasible"] == (m <= 31), "Family boundary failed.")
        if m>=32:
            require(54*m+1 in subset_sums(family(m)), "Missing subset-sum witness.")
            require(54*m+1 not in four_sum_witnesses(family(m)), "False obstruction.")
        family_results.append({"m":m,**result})
    out={"status":"PASS", "scope":"Finite checks only; the new universal theorems are proved in the report. The inherited upper84 chain is separate.",
         "construction":certificate_result,"fixed_cover":cover,
         "differential_small_sets":cross_checks(), "negative_controls":4,
         "family_samples":family_results,"elementary_upper_bound":122,
         "integer_bound_formula":"floor(sqrt((n+16)^(n+1)))",
         "integer_bound_at_84":str(isqrt(100**85)),
         "integer_bound_at_122":str(isqrt(138**123))}
    text=json.dumps(out,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text)
    print(text,end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
