#!/usr/bin/env python3
"""Run exact finite consequences of the conditional n85 zero-hole proof.

The checker reconstructs scalar arithmetic and labeled fixed incidence.
Written actual-cover, activity, owner, and forest lemmas are its premises.
No result here is a machine certification of those analytical lemmas.
"""
from fractions import Fraction as F
from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO
import json
import runpy

HERE=Path(__file__).resolve().parent


def checked_script(relative):
    path=HERE/relative
    output=StringIO()
    with redirect_stdout(output):
        runpy.run_path(str(path.resolve()),run_name='__main__')
    return {'path':relative,'status':'PASS'}


def quadratic_min(weight):
    # The quadratic is strictly convex. The actual side sizes lie in[0,68].
    return min(F(r*(r+1),2)+4*r+weight*(r-34)**2 for r in range(69))


def check_z4_finishes():
    rows={}
    def record(name,lower,upper):
        lower,upper=F(lower),F(upper)
        assert lower>upper,(name,lower,upper)
        rows[name]={'lower':str(lower),'upper':str(upper),
                    'strict_margin':str(lower-upper)}

    q3,q4,q5=map(quadratic_min,(F(3),F(4),F(5)))
    assert (q3,q4,q5)==(626,649,665)
    beta_low_min=min(r*(r+1)+9*r+4*(r-34)**2 for r in range(69))
    assert beta_low_min==1192
    record('B two beta holes: HIGH opposite impossible',beta_low_min,1063)
    # Card F keeps the conservative A143 and the original e8 budget.
    # A heavy selected clip is at least73; its native loss requires
    # delta>=e+73=81. The upper rows follow from its fresh229 master.
    e=8
    record('F light',q3+4*e,332)
    record('F heavy weight1',q4+81+4*e+73,332+306)
    record('F heavy weight2',q5+2*81+4*e+2*73,332+2*306)
    # O uses the separately proved adaptive 4tau+10f>=1990/3.
    base=q4+F(1990,3)
    record('O heavy source s',base+68,F(2183,2))
    record('O heavy source t',base,1142)
    record('O all light A<=73',base+68,1137)
    record('O all light A>=73',base+68,1207)
    # S: both rows retain the negative delta term; delta<=143-I-tau.
    # In the heavy row N>=73.
    record('S light',-F(3*143,4)+4*11,-F(577,4))
    record('S heavy',-F(3*143,4)+4*11+2*73,F(43,4))
    record('E-H no heavy lower',3*e,-F(469,2))
    record('E-H heavy lower',3*e+73,-F(159,2))
    record('E-alpha owner light',3*e,-F(9,2))
    record('E-alpha owner heavy source t',3*e,-F(1,2))
    record('E-alpha owner heavy source s',81+3*e+73,12)
    for weight in (1,2):
        record('E-alpha opposite weight'+str(weight),3*e+4*weight,-F(83,4))
    record('E-C5 light',3*e,0)
    record('E-C5 heavy',3*e+73,-F(111,4))
    return rows


def check_z5_empty_H_C5():
    # Exact substitutions in M+7f<=R+489-e+2epsilon+2xi:
    # M>=R+99+A, f=61-(tau-xi)/4, epsilon=delta-e.
    # After A=I+tau+delta, xi<=tau, and delta<=60-I-tau,
    # the necessary consequence is2I+3e<=23. e8 already contradicts it.
    assert F(99)+7*61-489==37
    assert F(37)-60==-23
    assert 3*8>23
    return {'native_group':'alpha_s, alpha_t/C5_t, H_t',
            'lower':24,'upper':23,'strict_margin':1}


def main():
    scripts=[
        'check_zero85.py',
        '../common/check_z3a1_side_union.py',
        '../scalar/check_z4_ownerless_certificate.py',
        '../foundations/zero_audit85.py',
        '../foundations/z5_alpha_final85.py',
        'check_zero85_z5_a1_b.py',
        '../scalar/check_z5_c5t_cutoff_audit.py',
    ]
    checks=[checked_script(p) for p in scripts]
    rows=check_z4_finishes()
    out={'status':'PASS','conditional_cardinality':85,
         'coverage':['Z0','Z1','Z2','Z3-A0','Z3-A1',
                     'Z4-retention-cards','Z4-ownerless',
                     'Z5-A0-all13-retained-P','Z5-A0-empty-P-H/C5',
                     'Z5-A0-empty-P-alpha','Z5-A1','Z5-B'],
         'standalone_checks':checks,'Z4_scalar_finishes':rows,
         'Z5_empty_P_H_C5':check_z5_empty_H_C5(),
         'scope':'Exact finite consequences and fixed-label incidence. '
                 'Structural theorem and written activity/owner/forest prerequisites '
                 'are not machine certified.'}
    HERE.joinpath('check_zero_cards85_results.json').write_text(
        json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','conditional_cardinality':85,
                      'standalone_checks':len(checks),
                      'Z4_scalar_rows':len(rows),
                      'coverage':out['coverage']},indent=2))


if __name__=='__main__':
    main()
