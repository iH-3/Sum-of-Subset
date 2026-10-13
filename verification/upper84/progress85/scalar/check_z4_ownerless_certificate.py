#!/usr/bin/env python3
"""Exact scalar replay of the new conditional Z4 ownerless certificate.

This checks constants, algebra, and the four terminal contradictions.
It does not certify the source theorem, fixed-label signs, or activity
classification. Those premises are written explicitly in the TeX proof.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sys
BASE=Path(__file__).resolve().parents[2]/'audit'/'verification_program'
sys.path.insert(0,str(BASE))
from exact_math import equal

eta=18

# Source sizes and fresh complete-target constants.
equal('2*67-1-(66+tau-xi)','67-tau+xi')
assert 2*73-68==78
assert 2*73>137-eta
assert 137-eta==119
assert 137-eta-73==46

# Both-core/all-light terminal row, after the loss eliminations.
equal('4*(67-tau+xi)+2*I+2*tau+2*18+ell-(64+4*xi)',
      '240+2*I+ell-2*tau')
light_margin=2  # tau <=119-I gives residual >=2+4I+ell.

# Both-core/one-heavy row: retain the opposing source depth.
equal('(2*(67-tau+xi)+2*ev+2*73+ell)-(52+2*xi+2*(delta-18))',
      '2*ev+264+ell-2*tau-2*delta')
heavy_depth_upper=F(274-264,2)
heavy_delta_min=eta+73
heavy_depth_lower=heavy_delta_min-69
assert heavy_depth_lower==22>heavy_depth_upper==5

# One non-core H, with its native loss used once in the forest rebate.
equal('(2*ev+4*(67-tau+xi)+2*u+ell+34)-(2*(68+xi)+2*xi+2*(delta-18))',
      '2*ev+202+2*u+ell-4*tau-2*delta')
one_H_right_upper=4*137-2*(eta+73)
one_H_depth_upper=F(one_H_right_upper-202-2*73,2)
assert one_H_right_upper==366
assert heavy_depth_lower==22>one_H_depth_upper==9

# Two non-core H native losses exceed the complete source budget.
assert 2*73>137

result={
    'status':'PASS',
    'conditional_family':'Z4 ownerless: P,B,O_s,O_t empty',
    'source':{'A_cap':137,'L_floor':'A+20','individual_depth_floor':'A-69'},
    'actual_trim_source':{'size':67,'span_bound':'66+tau-xi','overlap_constant':'67-tau+xi'},
    'fixed_credit':eta,
    'terminal_margins':{
        'both H core-hit, alpha clips light':'2+4I+ell',
        'both H core-hit, one heavy':str(heavy_depth_lower-heavy_depth_upper),
        'one H without core hit':str(heavy_depth_lower-one_H_depth_upper),
        'two H without core hits':2*73-137,
    },
    'scope':'Exact scalar algebra; structural, actual-cover, and label-sign premises remain analytical.'
}
out=Path(__file__).with_name('check_z4_ownerless_certificate_results.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
