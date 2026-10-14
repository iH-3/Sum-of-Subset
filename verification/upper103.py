#!/usr/bin/env python3
"""Exact arithmetic for the unified descent from the audited cap 115 to 103.

The report proves the necessary inequalities and their applicability. This
program checks every integer parameter state in those explicit relaxations;
it does not enumerate all feasible real sets or import any archived verifier.
Python 3.10+, standard library only. Checks remain active under python -O.
"""
import argparse
from fractions import Fraction as Q
import json
from math import isqrt
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def triangular(r):
    return r*(r+1)//2


# Witnesses only: no claim that this list is optimal is needed.
HOLE_C = (83, 89, 96, 102, 109, 110, 116, 122, 128, 129, 135, 142,
          147, 149, 155, 162, 167, 168, 175, 182, 187, 188, 195, 202)


def hole_parameters(C, beta=7):
    require(C >= 0 and beta >= 1, "Invalid hole parameters.")
    K = 3
    while (K+1)*(K-2)//2 <= C+1:
        K += 1
    D = C+K
    E = D+1
    M = max(2*beta, 1+(1+isqrt(9+8*(E+6*beta)))//2)
    J = max(K+1, 2*beta+5, M)
    return K, D, E, M, J


def check_hole_row(r, C):
    K, D, E, M, J = hole_parameters(C)
    require(K*(K-3)//2 <= C+1 < (K+1)*(K-2)//2, "K is not exact.")
    require(triangular(M)-42 > M+1+E, "Endpoint bridge is not strict.")
    require(7*(r-J+1) > D, f"No small increment forced at size {r}.")
    require(triangular(J-1)-1 > D, f"Off-scale exclusion failed at size {r}.")
    return {"r": r, "C": C, "K": K, "D": D, "E": E, "M": M, "J": J,
            "window_margin": 7*(r-J+1)-D,
            "off_scale_margin": triangular(J-1)-1-D}


def FA(a, b):
    return Q(triangular(a), 2)+triangular(b)+6*a+8*b+85


def FB(a, b):
    return Q(2*triangular(a), 3)+triangular(b)+6*a+Q(22*b+236, 3)


def symbolic_centres():
    """Rebuild the two exact centre identities from the eight outer entries."""
    def add(*vectors):
        return tuple(sum(v[i] for v in vectors) for i in range(8))
    def scale(c, v):
        return tuple(c*x for x in v)
    basis = [tuple(Q(i == j) for j in range(8)) for i in range(8)]
    p, q = basis[:4], basis[4:]
    def centres(v, o):
        lam = add(v[0], *[scale(-1,x) for x in v[1:]])
        alpha = add(v[1], scale(-1,v[2]), scale(-1,v[3]))
        beta = add(scale(2,v[1]), *[scale(-1,v[i]) for i in (0,2,3)])
        return lam, alpha, beta, [add(lam,scale(-1,x)) for x in o]
    lp, ap, bp, cp = centres(p,q)
    lq, aq, bq, cq = centres(q,p)
    top = add(lp,p[0])
    A = add(scale(Q(1,2),top), *[scale(-1,v) for v in (cp[0],cq[1],cq[2],ap,bq)])
    B = add(scale(Q(1,3),top), *[scale(-1,v) for v in (cp[0],cq[2],cq[3],bq)],
            scale(Q(-1,3),bp))
    require(A == (0,Q(1,2),Q(5,2),Q(3,2),0,0,3,3), "Certificate A identity failed.")
    require(B == (0,0,2,2,0,0,3,3), "Certificate B identity failed.")
    require(bp == add(scale(-1,add(cp[0],cq[1])),scale(-2,p[2]),scale(-2,p[3]),
                      *[scale(-1,x) for x in q[1:]]), "Branch A owner identity failed.")
    require(add(p[1],scale(-1,q[0])) == add(cp[0],bp,scale(2,p[2]),scale(2,p[3])),
            "Branch B owner identity failed.")
    # After subtracting all possible out-of-hull errors, the unused span
    # coefficients are nonnegative (q_p<=U and q_q>=0 are used in A).
    require(3-2-Q(1,2) == Q(1,2) and 5-Q(7,2) == Q(3,2), "A span absorption failed.")
    require(Q(8,3)-Q(4,3) == Q(4,3) and 5-Q(10,3) == Q(5,3), "B span absorption failed.")
    return {"identities_checked": 4, "span_absorption": "PASS"}


def audit_n(n, hole_rows, require_exclusion=True):
    d, e, m = n-8, n-16, n-17
    G, t0 = 2*d-12, (2*d-10)//3  # ceil(G/3)
    # The unpaired-absolute-value argument forces at least 23 opposite pairs.
    qmax = isqrt(96*e+1073-e*e)
    while (qmax-(e-1)) % 2:
        qmax -= 1
    paired_min = (e-1-qmax)//2
    require(paired_min >= 23 or not require_exclusion, "Sign bootstrap failed.")
    lattice = []
    low = []
    high = []
    high_initial = 0
    rejected_high_by_budget = 0
    for a in range(23, m-22):
        b = m-a
        lam = 1+triangular(a)+triangular(b)
        omega = 22*d+97-lam
        if omega < 0:
            continue
        inv = triangular(min(a,b))-2-omega
        inner = 2*m+4*e+14-lam+3*omega
        outer = lam-(4*d-10+omega)
        require(inv > 0 and inner < 0 and outer > 0, "Core lattice margin failed.")
        lattice.append((a,b,omega,inv,inner,outer))
        for z in range(15):
            rho = 0 if z == 0 else m-28
            tmin = max(t0,z,G-2*z)
            cmax = omega-rho-tmin
            if cmax < 0:
                continue
            ua, ub = ((0,0) if z == 0 else (a-3,b-3))
            ha, hb = ((0,0) if z == 0 else (z,z))
            margins = (FA(a,b)+Q(ua+ha,2)+ub+hb-(18*d+126+4*z),
                       FB(a,b)+Q(2*(ua+ha),3)+ub+hb-(18*d+126+4*z))
            if require_exclusion:
                require(cmax < d, f"An empty unit is possible: n={n}, a={a}, z={z}.")
                require(min(margins) > 0, f"Low-hole certificate fails: n={n}, a={a}, z={z}.")
            low.append({"a":a,"b":b,"z":z,"c_upper":cmax,
                        "A_margin":margins[0],"B_margin":margins[1]})
        if omega-(m-28) < t0:
            continue
        high_initial += 1
        require(a in hole_rows and b in hole_rows, "A high-hole side lacks an effective witness.")
        ua, ub = a+hole_rows[a]["C"]+1, b+hole_rows[b]["C"]+1
        ra, rb = max(a-14,ua+2-2*a), max(b-14,ub+2-2*b)
        H = omega-ra-rb
        if H < t0:
            rejected_high_by_budget += 1
            continue
        cmax = H-t0
        margins = (FA(a,b)+Q(ua,2)+ub-(18*d+126)-Q(5*H,2),
                   FB(a,b)+Q(2*ua,3)+ub-(18*d+126)-Q(7*H,3))
        if require_exclusion:
            require(cmax < d, f"High-hole active-unit condition fails: n={n}, a={a}.")
            require(min(margins) > 0, f"High-hole certificate fails: n={n}, a={a}.")
        high.append({"a":a,"b":b,"mu_a_lower":ua,"mu_b_lower":ub,
                     "rho_lower":ra+rb,"H":H,"c_upper":cmax,
                     "A_margin":margins[0],"B_margin":margins[1]})
    require(lattice, "Vacuous lattice audit.")
    return {"n":n,"d":d,"e":e,"m":m,"G":G,"t0":t0,
            "opposite_pairs_lower":paired_min,
            "lattice_orientations":len(lattice),
            "inverse_margin_min":min(row[3] for row in lattice),
            "inner_comparison_max":max(row[4] for row in lattice),
            "outer_comparison_min":min(row[5] for row in lattice),
            "low_states":low,"high_initial_orientations":high_initial,
            "high_rejected_by_budget":rejected_high_by_budget,"high_states":high,
            "low_c_upper":max((r["c_upper"] for r in low),default=None),
            "low_margin_min":min((min(r["A_margin"],r["B_margin"]) for r in low),default=None),
            "high_c_upper":max((r["c_upper"] for r in high),default=None),
            "high_margin_min":min((min(r["A_margin"],r["B_margin"]) for r in high),default=None)}


def negative_controls():
    rejected = 0
    for r,C in ((32,84),(35,103)):
        try:
            check_hole_row(r,C)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("Invalid effective-hole witness was accepted.")
    # Cardinality 103 at balanced sizes and z=0 has allowance 116>=95.
    # The active-unit proof must not silently certify this next endpoint.
    n,a,b=103,43,43
    d=n-8
    cmax=22*d+97-(1+triangular(a)+triangular(b))-(2*d-12)
    require(cmax==116 and cmax>=d, "The 103 obstruction control changed.")
    return {"bad_hole_rows_rejected":rejected,
            "next_endpoint_unproved":{"n":103,"a":a,"b":b,"z":0,
                                        "c_upper":cmax,"unit_capacity":d}}


def encode(value):
    if isinstance(value,Q):
        return str(value)
    raise TypeError(type(value).__name__)


def tex_value(value):
    if value is None:
        return r"\text{--}"
    if isinstance(value,Q) and value.denominator != 1:
        return rf"\frac{{{value.numerator}}}{{{value.denominator}}}"
    return str(value)


def latex_tables(rows,holes):
    def table(spec,head,body):
        return ("\\begin{center}\\small\n\\begin{tabular}{"+spec+"}\n\\toprule\n"+
                head+"\\\\\\midrule\n"+"\n".join(body)+
                "\n\\bottomrule\n\\end{tabular}\n\\end{center}\n")
    lattice=table("rrrrrr",r"$n$ & oriented pairs & paired minimum & inverse & inner & outer",
                  [" & ".join(str(r[k]) for k in ("n","lattice_orientations","opposite_pairs_lower",
                                                 "inverse_margin_min","inner_comparison_max","outer_comparison_min"))+r"\\"
                   for r in reversed(rows)])
    profile=table("rrrrrrr",r"$r$ & $C$ & $K$ & $D$ & $J$ & window margin & off-scale margin",
                  [" & ".join(str(holes[r][k]) for k in ("r","C","K","D","J","window_margin","off_scale_margin"))+r"\\"
                   for r in sorted(holes)])
    endpoint=table("rrrrrrr",r"$n$ & low states & $c_{\rm low}$ & low margin & high states & $c_{\rm high}$ & high margin",
                   [str(r["n"])+" & "+str(len(r["low_states"]))+" & $"+tex_value(r["low_c_upper"])+
                    "$ & $"+tex_value(r["low_margin_min"])+"$ & "+str(len(r["high_states"]))+
                    " & $"+tex_value(r["high_c_upper"])+"$ & $"+tex_value(r["high_margin_min"])+"$"+r"\\"
                    for r in reversed(rows)])
    return {"LATTICE":lattice,"PROFILE":profile,"ENDPOINT":endpoint}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    parser.add_argument("--tables-json",type=Path)
    args=parser.parse_args()
    holes={r:check_hole_row(r,C) for r,C in zip(range(32,56),HOLE_C)}
    rows=[audit_n(n,holes) for n in range(104,116)]
    out={"status":"PASS","conclusion":"N <= 103, conditional on the written reduction and audited 115 foundation",
         "scope":"All scalar states specified in upper103_from115_20261014.tex; no set enumeration or numerical solver",
         "symbolic":symbolic_centres(),"hole_rows":list(holes.values()),
         "cardinalities":rows,"negative_controls":negative_controls()}
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,default=encode,indent=2)+"\n",encoding="utf-8")
    if args.tables_json:
        args.tables_json.parent.mkdir(parents=True,exist_ok=True)
        args.tables_json.write_text(json.dumps(latex_tables(rows,holes),indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":out["status"],"cardinalities_excluded":[r["n"] for r in rows],
                      "lattice_orientations":sum(r["lattice_orientations"] for r in rows),
                      "low_hole_states":sum(len(r["low_states"]) for r in rows),
                      "high_initial_orientations":sum(r["high_initial_orientations"] for r in rows),
                      "high_terminal_orientations":sum(len(r["high_states"]) for r in rows),
                      "hole_witnesses":len(holes),"negative_controls":out["negative_controls"]},indent=2))


if __name__=="__main__":
    main()
