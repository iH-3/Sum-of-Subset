#!/usr/bin/env python3
"""SIZE86 bootstrap/AP arithmetic; Python standard library only."""
from fractions import Fraction
from math import isqrt
import json


def tri(n):
    return n * (n + 1) // 2


def effective(r, beta, cap):
    # Enumerate integer threshold definitions independently of model helpers.
    K = 3
    while (K + 1) * (K - 2) // 2 <= cap + 1:
        K += 1
    D = cap + max(3, K)
    M = max(2 * beta, 1 + (1 + isqrt(9 + 8 * (D + 1 + 6 * beta))) // 2)
    J = max(K + 1, 2 * beta + 5, M)
    margins = ((r - J + 1) * beta - D, tri(J - 1) - 1 - D)
    assert min(margins) > 0
    return {"K": K, "D": D, "M": M, "J": J, "margins": margins}


def rho_inverse(r, u):
    # Direct enumeration in the stated flexible inequality, no quotient formula.
    values = [r - 14, u + 2 - 2 * r]
    for beta in range(2, 11):
        threshold = (beta - 1) * (r - 14)
        t = 0
        while t < threshold and t + 4 * beta - 2 + 2 * (t // (beta - 1)) < u:
            t += 1
        values.append(t)
    return max(values)


def verify():
    n = 86
    d, e, m = n - 8, n - 16, n - 17
    G = 2 * d - 10
    L0 = 1 + tri(m // 2) + tri(m - m // 2)
    O0 = 22 * d + 97 - L0
    C0 = 2 * m + 4 * e + 14 - L0
    assert (d, e, m, G, L0, O0, C0) == (78, 70, 69, 146, 1226, 587, -794)
    assert 1 + tri(70) > 24 * n + 77
    # If a sign disappeared under a provisional four-nonzero peel, its
    # size70 one-sided core would also contradict the n86 core bound.
    assert 1 + tri(69) > 24 * d + 77
    q_sq = 96 * e + 1073 - e * e
    assert q_sq == 2893 and 53 ** 2 <= q_sq < 55 ** 2
    assert (m - 53) // 2 == 8
    assert [k for k in range(27) if O0 - k * (k + 1) >= -8] == list(range(24))
    boundaries = []
    for a in (11, 12, 13, 14):
        b, k = m - a, 34 - a
        I = k * (k + 1)
        O = O0 - I
        rp = -8 if a < 14 else 0
        cap = O - rp
        assert cap < tri(b) - 1
        d1 = C0 + O0 - 2 * I + 2 * cap + 16
        outer = L0 + I - (4 * d - 10 + cap)
        assert d1 < 0 and outer > 0
        if a == 11:
            assert rp + b - 5 > O  # non-AP Q impossible already
            assert G > cap        # AP Q gives z=0 after alignment
        elif a == 12:
            assert cap - (b - 5) < tri(a) - 1
            assert (G + 2) // 3 + rp + b - 5 > O
            assert G > cap
        elif a == 13:
            assert cap - (b - 5) < tri(a) - 1
            assert G > cap
            z_min = (G + rp + b - 5 - O + 1) // 2
            assert z_min == 32 and z_min > 2 * 5
            witness = effective(b, 5, 143)
            assert rho_inverse(b, b + 144) == 134 > O - rp
        else:
            # Both-nonAP dense branch is proved in inverse86; in the strict
            # inverse branch z>=15 licenses the following exact contradiction.
            z_min = (G + b - 5 - O + 1) // 2
            assert z_min == 15 and z_min > 2 * 7
            witness = effective(b, 7, 202)
            assert rho_inverse(b, b + 203) == 180 > O
            assert O - G == 21 < d  # AP-Q boundary goes to elementary rows
        boundaries.append(dict(a=a, b=b, k=k, I=I, Omega=O, cap=cap,
                               d1_upper=d1, outer_strict_margin=outer))
    ap_rows = []
    halfstep_remaining = []
    for k in range(21):  # includes a14 boundary
        a, b = 34 - k, 35 + k
        I = k * (k + 1)
        O = O0 - I
        assert O < tri(b) - 1 and O < 2 * tri(a)
        if O < tri(a):
            continue
        u = tri(a) + 1
        dominant = tri(a) + tri(b - 2) + 2 - 2 * b - O
        mass = Fraction(b * b - 11 * b, 2) + 2 * u + 7 - O
        # The sufficient condition u>2b fails at a14. The actual derivative
        # at t=2 is positive already when u+7-2b>0, which all rows satisfy.
        derivative = u + 7 - 2 * b
        w15 = 7 * b - Fraction(289, 8) - (2 * b + O - tri(a) - 3)
        d1 = 2393 + 2 * a - 4 * tri(a) - 2 * tri(b)
        assert dominant > 0 and mass > 0 and derivative > 0 and w15 > 0 and d1 < 0
        cap = O - tri(a) - G + 36 - (b - 5)
        if cap >= 0:
            halfstep_remaining.append((k, a, b, cap))
            assert cap < d
        ap_rows.append(dict(k=k, a=a, b=b, Omega=O, dominant_margin=dominant,
                            mass_margin=str(mass), quadratic_derivative_margin=derivative,
                            w15_margin=str(w15), d1_upper=d1, halfstep_c_cap=cap))
    assert [x[0] for x in halfstep_remaining] == list(range(7, 16))
    assert [x[3] for x in halfstep_remaining] == [6,16,23,27,28,26,21,13,2]
    assert L0 > 4 * d - 10 + O0
    return dict(schema="fresh-size86-bootstrap-ap-exact-v1", status="PASS",
                parameters=dict(n=n,d=d,e=e,m=m,G=G,Lambda0=L0,Omega0=O0,C0=C0),
                boundaries=boundaries, ap_rows=ap_rows,
                halfstep_remaining=halfstep_remaining,
                finite_assertions_only=True, models_built=0, numerical_calls=0,
                scope="Arithmetic support, not an independent acceptance of mathematical applicability")


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
