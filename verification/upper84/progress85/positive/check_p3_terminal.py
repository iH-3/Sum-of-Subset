#!/usr/bin/env python3
"""Exact checks for the arithmetic terminals of the fresh P3 proof.

The program does not establish the resource grouping or forest premises.
It verifies global integral quadratic minima and the stated terminal gaps.
"""
from fractions import Fraction as F

def integer_minimum(a, b, c):
    assert a > 0
    vertex = -b/(2*a)
    floor = vertex.numerator // vertex.denominator
    candidates = [(a*r*r+b*r+c, r) for r in (floor, floor+1)]
    return min(candidates)

def run():
    quadratics = [
        ('m1', F(9,2), F(-533,2), F(4624), F(679)),
        ('m2_s_light', F(9,2), F(-541,2), F(4726), F(661)),
        ('m2_t_light', F(9,2), F(-523,2), F(4522), F(723)),
        ('m2_s_heavy', F(9,2), F(-541,2), F(4760), F(695)),
        ('m2_t_heavy', F(9,2), F(-523,2), F(4488), F(689)),
        ('m3', F(9,2), F(-531,2), F(4624), F(709)),
        ('m4_chi33', F(11,4), F(-568,4), F(9801,4), F(2469,4)),
        ('m4_chi34', F(11,4), F(-586,4), F(10404,4), F(2601,4)),
        ('m4_chi35', F(11,4), F(-604,4), F(11025,4), F(684)),
    ]
    for name,a,b,c,expected in quadratics:
        actual,r = integer_minimum(a,b,c)
        assert actual == expected, (name,actual,expected)
        print('PASS quadratic', name, 'min', actual, 'at', r)

    # A0 follows its single derived terminal template.
    parameters = [(1,11,10,148,1,70,4),
                  (2,44,-5,115,2,71,6),
                  (3,75,-20,84,2,72,6)]
    e = 8
    for m,l,d,mcap,b,rmin,wheavy in parameters:
        max_all_light = mcap+6*b-3*l-d+F(9,2)*6
        min_all_light = 5*rmin+5*e
        assert min_all_light > max_all_light
        for q in (1,2):
            c = 73
            delta = e+c
            lower = (5*rmin+(q-1)*delta+5*e+q*c
                     +(3-q)*l+d-6*b)
            upper = 2*q*mcap+(F(7,2)+q)*wheavy
            assert lower > upper, ('A0 heavy',m,q,lower,upper)
            print('PASS A0 heavy', m, q, 'gap', lower-upper)

    # A1 rows: positive omitted terms are unnecessary except the w6
    # first-gap1 light case, where its source holes force sigma>=108.
    a1 = [('m1_light_w4',F(679)+F(70,4)+55,F(1443,2)+20),
          ('m1_light_w6',F(679)+F(70,4)+55+F(7,4)*108,F(1443,2)+30),
          ('m1_heavy',F(679)+F(70,4)+55,F(693)+30),
          ('m2_s_light',F(661),F(2283,4)+30),
          ('m2_t_light',F(723),F(2531,4)+30),
          ('m2_s_heavy',F(695),F(2305,4)+30),
          ('m2_t_heavy',F(689),F(2281,4)+30),
          ('m3_light',F(709),F(488)+30),
          ('m3_heavy',F(709),F(919,2)+30)]
    for name,lower,upper in a1:
        assert lower > upper, (name,lower,upper)
        print('PASS A1', name, 'gap', lower-upper)

if __name__ == '__main__':
    run()
