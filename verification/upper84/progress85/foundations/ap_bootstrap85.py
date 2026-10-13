#!/usr/bin/env python3
"""Exact arithmetic for fresh cardinality-85 bootstrap/AP deductions.

This checks finite scalar minima, not actual-set applicability or imported
general additive theorems. Run with standard Python; no packages are needed.
"""
import json


def T(r):
    return r * (r + 1) // 2


def require(predicate, message):
    if not predicate:
        raise ValueError(message)


def main():
    d, e, m = 77, 69, 68
    require(22 * d + 97 == 1791, "budget total")
    require(96 * e + 1073 - e * e == 2936, "unpaired bound")
    require(54 * 54 <= 2936 < 56 * 56, "even unpaired threshold")
    require((m - 54) // 2 == 7, "opposite-pair minimum")
    require(24 * 24 <= 600 + 8 < 25 * 25, "preliminary k range")

    rows = []
    for k in range(22):
        a, b = 34 - k, 34 + k
        I, O = k * k, 600 - k * k
        require(1 + T(a) + T(b) == 1191 + I, "Lambda")
        rp = -2 if a == 13 else 0
        u = 1 + T(a)
        # In the half-step branch, >=2 odd coefficients have least odd
        # value W. Distinct even/odd generators give the actual mass floor.
        W = 17
        normalized_mass_excess = min(
            (b - t) * (b - t + 1) + t * W + t * (t - 1) - W - T(b)
            for t in range(2, b + 1)
        )
        odd17_margin = u + normalized_mass_excess - (O + 2 * b - 2 - rp)
        require(odd17_margin > 0, "least odd >=17 must contradict budget")
        # Thus W<=15, z=W-1<=14. These relaxed caps are valid before
        # using j=0 and the first-pair obstruction.
        halfstep_cap = O - T(a) - 144 + 3 * 14 - (b - 5) - rp
        nonprimitive_cap = O - 144 - T(a) - rp
        halfstep_D1_upper = 2367 + 2 * a - 4 * T(a) - 2 * T(b)
        require(halfstep_D1_upper < 0, "half-step D1 lattice forcing")
        one_residue_margin = T(a) + T(b - 2) + 2 - 2 * b + rp - O
        require(one_residue_margin > 0, "one clipped gap/off-scale exclusion")
        require(1191 + I > 4 * d - 10 + O - rp, "outer lattice forcing")
        rows.append(dict(k=k, a=a, b=b, I=I, Omega=O,
                         rhoP_floor=rp, odd17_margin=odd17_margin,
                         halfstep_c_cap=halfstep_cap,
                         nonprimitive_c_cap=nonprimitive_cap,
                         halfstep_D1_upper=halfstep_D1_upper,
                         one_residue_margin=one_residue_margin))

    require(min(x['odd17_margin'] for x in rows) == 22, "odd margin minimum")
    require(max(x['halfstep_c_cap'] for x in rows) == 61, "half-step cap")
    require(max(x['nonprimitive_c_cap'] for x in rows) == 59, "nonprimitive cap")
    require(max(x['halfstep_D1_upper'] for x in rows) == -761, "D1 maximum")
    require((57 + 104) / 2 < 81 and 56 + 104 < 162,
            "j0 obstruction endpoint checks")
    print(json.dumps(dict(status="PASS", rows=rows), indent=2))


if __name__ == '__main__':
    main()
