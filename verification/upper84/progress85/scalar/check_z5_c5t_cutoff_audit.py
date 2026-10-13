#!/usr/bin/env python3
"""Exact scalar replay of independent Z5 final-family local audit."""
import json
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[2]/'audit'/'verification_program'
sys.path.insert(0,str(BASE))
from exact_math import equal

assert 6*77==462
assert 1085-462==623
assert 623+21-72-2*(2*73-68)==416
assert 2*99+16==214
assert 416-214-68==134
equal('3*(I+tau+delta)+9*(61-(tau-xi)/4)-(134-e+4*(delta-e)+xi)',
      '415+3*I+3*tau/4+5*xi/4-delta+5*e')
equal('415+3*I+3*tau/4+5*xi/4-(60-I-tau)+5*e',
      '355+4*I+7*tau/4+5*xi/4+5*e')
assert 355+5*13==420>0

# These are literal original fixed inventory names, not centers/resources.
tail_types={
    *(f'C1{i}_s' for i in range(3,9)),
    *(f'C2{i}_s' for i in range(3,9)),
    *(f'U{i}_s' for i in range(3,9)),
    *(f'V{i}_s' for i in range(3,9)),
    'V2_s','U2_s','C22_s','C12_s','C11_s','C44_s','C34_s','C33_s',
}
beta_six={f'V{i}_s' for i in range(3,9)}
new_high={'U2_s','U3_s','U4_s','V2_s'}
assert len(tail_types)==32
assert new_high<=tail_types and not new_high&beta_six
assert len(tail_types-beta_six)==26
assert len(tail_types-beta_six-new_high)==22
assert 77+26==103 and 77+22==99
assert 99+68-2*73+1==22  # two endpoints 73-r, S+r_o-72
assert 13+len(new_high)==17
equal('67-(tau-xi)','67-tau+xi')
equal('2*(67-tau+xi)-(44+2*xi+2*(delta-e))',
      '90-2*tau-2*delta+2*e')
assert (90-2*60+2*17)==4>0

result={'status':'PASS',
        'conditional_family':'Z5 A1, exact holes O_s,H_s,O_t,P,C5_t; sole beta_s',
        'cutoff_endpoint_loss':'2*l_C5s+2*l_alphat+u_alphas',
        'cutoff_fixed_credit':13,
        'cutoff_scalar_margin':420,
        'additional_HIGH_tail_types':sorted(new_high),
        'new_fixed_credit':17,
        'remaining_fixed_tail_types':22,
        'final_scalar_margin':4,
        'scope':'Local scalar algebra and literal tail-type membership; analytical structural/activity and actual-cover premises are external.'}
Path(__file__).with_name('check_z5_c5t_cutoff_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
