#!/usr/bin/env python3
"""Exact arithmetic checks for new conditional Z0--Z2 and Z3-A0 notes.

This script checks arithmetic, minima, and one fixed-ledger incidence.
It does not certify the structural conclusion or analytical classifiers.
"""
from fractions import Fraction as F
from pathlib import Path
import json

def min_quadratic(weight):
    return min((F(r*(r+1),2)+4*r+weight*(r-34)**2,r)
               for r in range(-100,101))

assert min_quadratic(F(3)) == (F(626),28)
assert min_quadratic(F(4)) == (F(649),30)
assert min(( (r-34)**2+3*r,r) for r in range(-100,101)) == (100,32)
assert min(( (r-34)**2+4*r,r) for r in range(-100,101)) == (132,32)
assert min(( (r-34)**2+6*r,r) for r in range(-100,101)) == (195,31)

# The maxima are affine piecewise-linear convex functions. Their minima
# occur at the intersections shown here, and branch slopes point inward.
assert F(121-4*12) == F(49+2*12) == 73
assert F(414-5*12) == F(342+12) == 354
assert F(42-8) == F(18+2*8) == 34
assert F(104-8) == F(80+2*8) == 96
assert 354-54 == 300 > 298

z3_rows = [
    ('all light',626+2*8,625),
    ('one heavy other',626+2*80+72,781),
    ('two heavy other',626+2*152+144,945),
    ('heavy alpha and t',626+2*152+72,866),
    ('heavy alpha and C4s',626+2*152+72,948),
    ('sole heavy alpha, new credit',626+2*83,791),
]
for name,lo,hi in z3_rows:
    assert lo>hi,(name,lo,hi)

# Incidence is recomputed against the actual 26 labeled baseline groups.
root=Path(__file__).resolve().parents[2]
appendix=root/'audit/verification_program/data/z5_appendix.json'
groups=list(map(set,json.loads(appendix.read_text())['fixed_groups']))
low={f'{kind}{i}_s' for kind in ('U','V') for i in range(5,9)}
low|={f'F{i}_s' for i in (3,4,5)}
touched=sum(bool(g&low) for g in groups)
assert len(low)==11 and touched==9
assert 8+len(low)-touched==10

print(json.dumps({'conditional_cases_excluded':['Z0','Z1','Z2','Z3-A0'],
                  'Z3_A0_scalar_margins':{name:lo-hi for name,lo,hi in z3_rows},
                  'new_ledger':{'high':8,'low':11,'touched':touched,'credit':10},
                  'additional_proofs':['../common/z3a1_side_union.md',
                                       'zero85_z4_z5_cards.md',
                                       'zero85_z5_a1_b.md'],
                  'scope':'Exact arithmetic and labeled incidence; analytical hypotheses remain conditional.'},
                 indent=2))
