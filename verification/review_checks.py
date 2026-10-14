#!/usr/bin/env python3
"""Independent, bounded regression checks for the 2026-10-14 proof review.

No archived checker is imported. PASS does not certify the global upper-84
proof. The exact domains below are intentionally reported in the output.
"""
import argparse
from fractions import Fraction
from itertools import combinations, combinations_with_replacement
import json
from math import gcd
from pathlib import Path
import random


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def fs(values):
    sums = {0}
    for x in values:
        sums |= {s + x for s in sums}
    return sums


def restricted(values):
    return {x + y for x, y in combinations(values, 2)}


def peeling():
    example = (-3, -2, 0, 1, 2)
    alpha, beta, modulus = -5, 3, 8
    old = {0}
    shifted = {alpha, beta}
    require(not any(x % modulus == 0 for x in shifted),
            "The counterexample no longer refutes the literal sentence.")
    require(len(shifted) == len(old) + 1, "Corrected translated-class count failed.")
    count = 0
    universe = tuple(range(-6, 0)) + tuple(range(1, 7))
    for size in range(4, 13):
        for nonzero in combinations(universe, size):
            a = sorted((0,) + nonzero)
            neg = [x for x in a if x < 0]
            pos = [x for x in a if x > 0]
            removed = set(neg[:2] + pos[-2:])
            # Any additional nonzero entries are allowed by the old lemma.
            removed.update([x for x in nonzero if x not in removed][:4-len(removed)])
            rest = [x for x in a if x not in removed]
            lo = sum(x for x in removed if x < 0)
            hi = sum(x for x in removed if x > 0)
            require(min(restricted(a)) >= lo and max(restricted(a)) <= hi,
                    f"Peeling hull failed: {a}")
            require(len(fs(a)) >= len(fs(rest)) + len(restricted(a)) - 1,
                    f"Peeling inequality failed: {a}")
            count += 1
    return {"counterexample_set": example, "alpha": alpha, "beta": beta,
            "modulus": modulus, "old_residue": 0, "new_residue": 3,
            "literal_sentence_false": True, "corrected_lemma_small_sets": count,
            "domain": "all F in [-6,6], 0 in F, |F|>=5"}


def positive_stats(xs):
    bits = 1
    before_last = 1
    for x in xs:
        before_last = bits
        bits |= bits << x
    r = len(xs)
    mu = bits.bit_count() - 1 - r * (r + 1) // 2
    pairs = restricted((0,) + xs)
    defect = sum(2*x not in pairs for x in xs)
    rho = mu + 2 - 2*defect
    step = 0
    for x in xs:
        step = gcd(step, x)
    ap = bits.bit_count() == sum(xs)//step + 1
    increment = bits.bit_count() - before_last.bit_count() - r
    return mu, rho, ap, increment, step


def defects():
    counts = {"all_sets": 0, "threshold14": 0, "nonap_old_bound": 0,
              "small_increment": 0, "deleted_interval_nonap21": 0}
    for r in range(1, 19):
        for xs in combinations(range(1, 19), r):
            mu, rho, ap, y, step = positive_stats(xs)
            require(mu >= 0 and rho >= -8, f"Uniform defect failed: {xs}")
            counts["all_sets"] += 1
            if r >= 14:
                require(rho >= 0, f"Threshold14 failed: {xs}")
                counts["threshold14"] += 1
            if r >= 6 and not ap:
                require(rho >= r-14, f"Non-AP bound failed: {xs}")
                counts["nonap_old_bound"] += 1
            if r >= 6 and 0 <= y <= r-5:
                require(r <= xs[-1]//step <= r+y,
                        f"Small-increment inverse failed: {xs}")
                counts["small_increment"] += 1
    for r in (21, 22, 31, 34, 50):
        for q in (1, 2, 3):
            h = r + q
            for holes in combinations(range(1, h), q):
                xs = tuple(x for x in range(1, h+1) if x not in holes)
                _, rho, ap, _, _ = positive_stats(xs)
                if not ap:
                    require(rho >= r-5, f"Sharper non-AP bound failed: {xs}")
                    counts["deleted_interval_nonap21"] += 1
    return {"domain": "all nonempty X in [1,18]; plus stated deleted intervals",
            "deleted_interval_sizes": [21, 22, 31, 34, 50],
            "deletions": [1, 2, 3], "counts": counts}


def sharp_defect():
    def value(d):
        f = d[2:-2]
        rd, rf = restricted(d), restricted(f)
        holes_d = max(rd)-min(rd)+1-len(rd)
        holes_f = max(rf)-min(rf)+1-len(rf)
        g = 4*len(f)+6-(len(rd)-len(rf))
        return holes_d + holes_f + g
    count = 0
    for d in combinations(range(16), 11):
        require(value(d) >= 12, f"Sharp four-extreme bound failed: {d}")
        count += 1
    for m in range(7, 41):
        d = (-m-2, -1) + tuple(range(m)) + (m, 2*m+1)
        require(value(d) == 2*m-2, f"Sharpness example failed: {m}")
    return {"domain": "all 11-element D in [0,15], F=D[2:-2]",
            "sets": count, "equality_sizes_m": [7, 40]}


def fringes():
    count = 0
    largest = -1
    for a, b, c, e in combinations(range(1, 33), 4):
        p = len({x+y for x, y in combinations_with_replacement((a,b,c),2)
                 if x+y > c})
        bcount = len({x+y for x, y in combinations_with_replacement((a,b,c,e),2)
                      if x+y > e})
        require(2*bcount <= a+b+8-(a+b)%2, "Quartet fringe bound failed.")
        require(p+bcount-a-b <= 5, "Source fringe improvement failed.")
        largest = max(largest, p+bcount-a-b)
        count += 1
    return {"domain": "all 1<=a<b<c<e<=32", "quartets": count,
            "maximum_P_plus_B_minus_a_minus_b": largest}


def gap_inventory():
    rng = random.Random(20261014)
    eligible = [0, 0, 0]
    maxima = [0, 0, 0]
    for _ in range(12000):
        mv, mo = rng.randrange(1, 31), rng.randrange(1, 31)
        den = rng.choice((1, 2, 3, 5))
        y = mv + Fraction(rng.randrange(1, 151), den)
        x = y + Fraction(rng.randrange(1, 151), den)
        h = Fraction(rng.randrange(1, 501), den)
        d = Fraction(rng.randrange(1, 301), den)
        v = (x+h+d, x+h, x, y)
        o = tuple(sorted((mo+Fraction(k,den)
                          for k in rng.sample(range(1, 601),4)), reverse=True))
        lam = v[0]-v[1]-v[2]-v[3]
        alpha = v[1]-v[2]-v[3]
        beta = 2*v[1]-v[0]-v[2]-v[3]
        b = v + tuple(-z for z in o)
        labels = [lam+z+w for z,w in combinations_with_replacement(b,2)]
        labels += [alpha+z for z in b[1:]] + [beta+z for z in b[1:]]
        total = sum(v)
        labels += [v[0]+v[1]+2*v[2]-total,
                   v[0]+3*v[2]-total, 2*v[1]+2*v[2]-total,
                   v[1]+3*v[2]-total, 4*v[2]-total]
        require(len(labels) == 55, "Wrong raw fixed-label count.")
        H, O = lam+v[1], lam+v[0]
        def inside(z, left, right):
            return left < z < right
        gap1 = lambda z: inside(z, H+mv, O-mo)
        gap2 = lambda z: inside(z, alpha+mv, H-mo)
        if d <= mv+mo:
            continue
        if H+mv > 0:
            n = sum(map(gap1, labels))
            require(n <= 11, "Eleven-label first-gap bound failed.")
            eligible[0] += 1
            maxima[0] = max(maxima[0], n)
        if beta+mv >= 1:
            n2 = sum(map(gap2, labels))
            n12 = sum(gap1(z) or gap2(z) for z in labels)
            require(n2 <= 8 and n12 <= 15, "Beta gap inventory failed.")
            eligible[1] += 1
            eligible[2] += 1
            maxima[1] = max(maxima[1], n2)
            maxima[2] = max(maxima[2], n12)
    require(all(eligible), "A raw-gap test domain was empty.")
    return {"scope": "seeded rational samples, not exhaustive and not feasible A",
            "seed": 20261014, "samples": 12000,
            "eligible_first_second_union": eligible,
            "largest_label_counts_first_second_union": maxima}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    out = {"scope": "Bounded independent checks only; see proof_review_20261014.md",
           "peeling": peeling(), "defects": defects(),
           "sharp_four_extreme": sharp_defect(), "source_fringes": fringes(),
           "raw_gaps": gap_inventory()}
    out["status"] = "PASS"
    data = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data, encoding="utf-8")
    print(data, end="")


if __name__ == "__main__":
    main()
