#!/usr/bin/env python3
"""Small exact arithmetic checker for p4_cross_certificate.tex.

The actual source, END1 endpoints, loss forests and T<=165 are written
mathematical premises. This checks the new constants, symbolic transport,
integer quadratic minimum, five small cases, floor residue identities,
and the final strictly positive margin; it does not replace those premises.
"""
from fractions import Fraction as F
from pathlib import Path
import sys,json
BASE=Path(__file__).resolve().parents[2]/"audit"/"verification_program"
sys.path.insert(0,str(BASE))
from exact_math import equal,parse,quadratic_integer_min,require

def main():
    equal("(k+4)+2*(68-k+4)+(68-k+3)","219-2*k")
    equal("2*(k+5)+4*(k+1)-2*k","4*k+14")
    require(219+10+14==243,"endpoint/source243")
    require(1166-4*9-243==887,"raw transport887")
    require(887+2*20==927,"conservative raw927")
    equal("L+2*(20-B)","L+40-2*B")
    # Substitute T=26+I+tau+delta, tau=R+Es+Et-2, f=67-ps-pt.
    equal("q+zeta-927-2*R-3*delta+6*Fs+4*(67-ps-pt)+3*(26+I+R+Es+Et-2+delta)",
          "q+3*I-855+zeta+3*(Es+Et)+R+6*Fs+4*(67-ps-pt)")
    equal("q+3*I-855+zeta+3*(Es+Et)+R+6*Fs+4*(67-ps-pt)-(q+3*I-115+3*Es-9*ps+zeta+3*Et-9*pt)",
          "6*Fs-(137-R)-5*(67-ps-pt)")
    equal("3*(3*a+b)-9*(3+a)","3*b-27")
    equal("(3*a+b+1)+3*(3*a+b)-9*(3+a)","3*a+4*b-26")
    small=[]
    for E,j in ((1,1),(2,2),(3,2),(4,2),(5,3)):
        phi=j+E//j
        v=E+1+3*E-9*phi
        require(v>=-20,"opposite small-case bound")
        small.append({"E":E,"trim":j,"margin_bound":v})
    require([r["margin_bound"] for r in small]==[-13,-18,-14,-19,-15],"opposite five cases")
    equal("T(k)+5*k+3*(k-34)**2","654+(7*(k-28)**2-5*(k-28))/2")
    minimum,at=quadratic_integer_min(parse("T(k)+5*k+3*(k-34)**2"),"k")
    require(minimum==654 and at==[28],"integer quadratic minimum")
    require(654-115-27-20==492,"raw certificate492")
    # All unbounded T<=163 are handled by the increasing strict lower bound.
    require(492-3*163==3,"unbounded lower T branch")
    tails=[]
    for T in (164,165):
        Bcap=183-T
        gap=492-3*T+2*(20-Bcap)
        require(gap>0,"positive endpoint margin")
        tails.append({"T":T,"Bsum_cap":Bcap,"positive_margin":gap})
    require([r["positive_margin"] for r in tails]==[2,1],"terminal margins")
    out={"status":"PASS_EXACT_LOCAL_ARITHMETIC","quadratic_minimum":"654","minimizer":28,
         "small_opposite_cases":small,"raw_bound":"492-3T","terminal_margins":tails,
         "lower_T_margin_at_163":3,
         "written_premises":["normalized first-gap1 P4 A0 cross configuration and physical ranks",
                             "valid nominal END1 native endpoints and fixed credit9",
                             "actual leading/ordinary trimmed copies and rooted loss budgets",
                             "source mass and source/cardinality fringes",
                             "new universal source theorem T<=165"]}
    Path(__file__).with_name("check_p4_cross_certificate_results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))

if __name__=="__main__":main()
