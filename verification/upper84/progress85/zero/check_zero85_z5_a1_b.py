#!/usr/bin/env python3
"""Exact finite arithmetic in the fresh Z5 A1/B proof.

This checker does not establish the retention grammar, native-loss
licenses, physical-target unions, or upper-tail inventory. Those are
written deductions in zero85_z5_a1_b.md and its independent receipt.
"""
from fractions import Fraction as F

def triangular(r):
    return r*(r+1)//2

def minimum(poly):
    # Recover the coefficients of the explicitly displayed quadratic and
    # check the two nearest integers to its exact rational vertex. This
    # proves the minimum on all integers, not a bounded source sample.
    c = F(poly(0))
    a = (F(poly(1))+F(poly(-1))-2*c)/2
    b = (F(poly(1))-F(poly(-1)))/2
    assert a > 0
    vertex = -b/(2*a)
    floor = vertex.numerator // vertex.denominator
    return min((a*r*r+b*r+c, r) for r in (floor, floor+1))

def verify():
    rows = [
        ('HIGH alpha', lambda r: 2*triangular(r)+8*r+3*(r-34)**2, F(1092)),
        ('Q3', lambda r: triangular(r)+4*r+3*(r-34)**2, F(626)),
        ('Q4', lambda r: triangular(r)+4*r+4*(r-34)**2, F(649)),
        ('same owner', lambda r: triangular(r)+4*r+F(5,2)*(r-34)**2, F(608)),
        ('split beta', lambda r: triangular(r)+4*r+F(13,2)*(r-34)**2, F(1357,2)),
    ]
    for name, poly, expected in rows:
        actual, r = minimum(poly)
        assert actual == expected, (name, actual, expected)
        print('PASS minimum', name, actual, 'at', r)

    e = 8
    assert 1092+e > 1048
    assert 626 > 286-F(13,2)*e
    assert 608 > 520-F(7,2)*e
    assert 626 > 592-4*e
    assert 3+F(13,2)*e > 0
    assert 537+68-F(3,2)*60+F(13,2)*e > 0
    assert 219+8*e > 0
    assert 626 > 427-4*e
    assert F(1357,2) > 316

    # Final C5_t family: six retained ordinary t-resources, exact
    # 77-point native capacities, and the stronger physical-target cutoff.
    assert 6*77 == 462
    assert 1085-462 == 623
    assert 623+21-228 == 416
    assert 2*99+16 == 214
    assert 202-68 == 134
    assert 9*61-134-60 == 355
    assert 355+5*13 == 420 > 0

    # Initial fixed ledger; all four new HIGH types are among the
    # 26 fixed types left after the beta cutoff.
    assert 11+11-9 == 13
    assert 15+11-9 == 17
    assert 32-6 == 26
    assert 26-4 == 22
    assert 77+26 == 103
    assert 77+22 == 99
    assert 99-77 == 22
    assert -8+13+13 > 0

    # The actual one-rank trim has 67 points and the native-loss rebate
    # makes 2f1 <= 44+2xi+2epsilon.
    assert 69-2 == 67
    assert 2*67-(66+1) == 67
    assert (2*67-2*22)//2 == 45
    assert 45+17 == 62 > 60
    print('PASS: fresh Z5 A1/B terminal minima, union constants, '
          'cutoff, fixed ledger and trim-one contradiction.')

if __name__ == '__main__':
    verify()
