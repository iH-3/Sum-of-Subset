#!/usr/bin/env python3
"""Exact continuation 103 -> 100; Python 3.10+, standard library only.

The written report proves that actual sets satisfy these models. This program
checks the complete finite reduction and integer Farkas certificates, not the
external additive-combinatorial theorems. No optimizer is used by verification.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CERTIFICATE = ROOT / "data/upper100_certificates.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def triangular(r):
    return r * (r + 1) // 2


def hole_row(r, C, beta):
    require(r >= 1 and C >= 0 and beta >= 1, "Invalid hole parameters")
    K = 3
    while (K + 1) * (K - 2) // 2 <= C + 1:
        K += 1
    D = C + K
    E = D + 1
    M = max(2 * beta, 1 + (1 + isqrt(9 + 8 * (E + 6 * beta))) // 2)
    J = max(K + 1, 2 * beta + 5, M)
    require(triangular(M) - 6 * beta > M + 1 + E, "Non-strict bridge")
    require(beta * (r - J + 1) > D, "No small increment forced")
    require(triangular(J - 1) - 1 > D, "Off-scale exclusion fails")
    return dict(r=r, C=C, beta=beta, K=K, D=D, E=E, M=M, J=J)


def hole_catalogue():
    """A finite witness search, not a claim of optimal parameters.

    Keeping the largest valid C in this explicitly bounded search is only a
    convenience. Every row actually used is individually checked again.
    """
    out = {}
    for r in range(20, 65):
        for beta in range(7, 21):
            best = None
            for C in range(601):
                try:
                    best = hole_row(r, C, beta)
                except ValueError:
                    continue
            if best is not None:
                out[r, beta] = best
    return out


def active_margins(a, b, z, ua, ub, d):
    fa = Q(triangular(a), 2) + triangular(b) + 6*a + 8*b + 85
    fb = Q(2*triangular(a), 3) + triangular(b) + 6*a + Q(22*b+236, 3)
    upper = 18*d + 126 + 4*z
    return (fa + Q(ua+z, 2) + ub+z - upper,
            fb + Q(2*(ua+z), 3) + ub+z - upper)


def scalar_audit(n, catalogue):
    require(n in (101, 102, 103), "Unproved cardinality requested")
    d, e, m = n-8, n-16, n-17
    G = 2*d-12
    t0 = (G+2)//3
    qmax = isqrt(96*e+1073-e*e)
    qmax -= (qmax-e+1) % 2
    paired_min = (e-1-qmax)//2
    require(paired_min >= 20, "Sign bootstrap is insufficient")
    require(1+triangular(n-16) > 24*n+77, "One-sided bootstrap fails")
    lattice, low, high, empty, witnesses = [], [], [], [], {}
    high_budget_rejections = 0
    for a in range(paired_min, m-paired_min+1):
        b = m-a
        lam = 1+triangular(a)+triangular(b)
        omega = 22*d+97-lam
        if omega < 0:
            continue
        inv = triangular(min(a,b))-2-omega
        inner = 2*m+4*e+14-lam+3*omega
        outer = lam-(4*d-10+omega)
        require(inv > 0 and inner < 0 and outer > 0, "Lattice gate fails")
        lattice.append(dict(a=a,b=b,omega=omega,inverse=inv,inner=inner,outer=outer))
        # z <= kappa <= T <= omega; both orientations are included.
        for z in range(omega+1):
            ua, ub = ((0,0) if z == 0 else (a-3,b-3))
            ra, rb = ((0,0) if z == 0 else (a-14,b-14))
            tm = max(t0,z,G-2*z)
            if omega-ra-rb-tm < 0:
                continue
            if z >= 15:
                bounds = []
                for r in (a,b):
                    eligible = [row for (rr,beta),row in catalogue.items()
                                if rr == r and 2*beta < z]
                    require(eligible, "High-hole side has no witness")
                    best = max(eligible, key=lambda row: (row["C"],-row["beta"]))
                    checked = hole_row(r,best["C"],best["beta"])
                    witnesses[(r,best["C"],best["beta"])] = checked
                    bounds.append(r+best["C"]+1)
                ua, ub = bounds
                ra, rb = max(ra,ua+2-2*a), max(rb,ub+2-2*b)
            cmax = omega-ra-rb-tm
            if cmax < 0:
                high_budget_rejections += int(z >= 15)
                continue
            margins = active_margins(a,b,z,ua,ub,d)
            require(min(margins) > 0, "Active-center contradiction fails")
            row = dict(a=a,b=b,z=z,c_upper=cmax,mu_p=ua,mu_q=ub,
                       rho_lower=ra+rb,A_margin=margins[0],B_margin=margins[1])
            if z >= 15:
                require(cmax < d, "A high-hole empty-unit case remains")
                high.append(row)
                continue
            low.append(row)
            if cmax < d:
                continue
            require(cmax < 2*d, "Two empty units are possible")
            delta = cmax-d
            small, large = min(a,b),max(a,b)
            if n == 103:
                require(z == 0 and 39 <= small <= large <= 47 and delta <= 21,
                        "103 model range does not cover this state")
                require(delta < small+5, "103 permits an outside center")
                regimes = ["N103"]
            elif n == 102:
                require(36 <= small <= large <= 49 and delta <= 45,
                        "102 model range does not cover this state")
                require(delta < small+5, "102 permits an outside center")
                regimes = ["N102"]
            elif z > 0:
                require(36 <= small <= large <= 48 and delta <= 41,
                        "101 positive-hole model range fails")
                require(delta < small+5, "101 positive holes permit an exception")
                require(ua+z >= a-2 and ub+z >= b-2, "Missing mass bonus")
                regimes = ["P"]
            else:
                require(34 <= small <= large <= 50 and delta <= 69,
                        "101 zero-hole model range fails")
                require(delta < 2*(small+5), "Two outside centers are possible")
                regimes = ["Z"]
                if delta >= small+5:
                    require(37 <= small <= large <= 47, "Exception range fails")
                    regimes.append("E")
            empty.append(dict(a=a,b=b,z=z,delta_upper=delta,regimes=regimes))
    require(lattice and low, "Empty scalar audit")
    return dict(n=n,d=d,e=e,m=m,G=G,t0=t0,paired_min=paired_min,
                lattice=lattice,low_states=low,high_states=high,empty_states=empty,
                high_budget_rejections=high_budget_rejections,
                witnesses=[witnesses[k] for k in sorted(witnesses)],
                summary=dict(lattice_orientations=len(lattice),low_states=len(low),
                             high_states=len(high),empty_states=len(empty),
                             inverse_min=min(x["inverse"] for x in lattice),
                             inner_max=max(x["inner"] for x in lattice),
                             outer_min=min(x["outer"] for x in lattice),
                             low_margin=min(min(x["A_margin"],x["B_margin"]) for x in low),
                             high_margin=min((min(x["A_margin"],x["B_margin"]) for x in high),default=None),
                             high_c_max=max((x["c_upper"] for x in high),default=None)))


# a0,b0,tmax,delta_max,tangent_slope,tangent_intercept,F_upper,n
REGIMES = {
    "N103": (39,47,8,21,87,1849,1836,103),
    "N102": (36,49,13,45,85,1764,1874,102),
    "Z": (34,50,16,69,85,1764,1800,101),
    "P": (36,48,12,41,87,1768,1856,101),
    "E": (37,47,10,69,85,1764,1800,101),
}


def basic_modes():
    for branch,j in (("A",9),("B",5)):
        singles = [s+str(i) for s in "pq" for i in range(10) if i not in (4,j)]
        for missing in ["pair1","pair2"]+singles:
            split = branch == "A" and missing in ("p5","q5")
            choices = ["-"] if missing == "pair2" or split else ["p","q"]
            for choice in choices:
                slots = [v for v in singles if v != missing]
                if missing != "pair1":
                    slots.append("p4")
                if choice != "-":
                    slots.append(choice+str(j))
                yield branch,missing,choice,slots


def all_cases():
    for regime in REGIMES:
        for mode in basic_modes():
            exceptions = [(v,e) for v in mode[3] for e in ("l","u")] if regime == "E" else [None]
            for exception in exceptions:
                key = ":".join((regime,*mode[:3]))
                if exception:
                    key += ":"+":".join(exception)
                yield key,regime,mode,exception


def add(*ds):
    out = {}
    for d in ds:
        for k,v in d.items():
            out[k] = out.get(k,0)+v
    return {k:v for k,v in out.items() if v}


def scale(c,d):
    return {k:c*v for k,v in d.items() if c*v}


def linear_model(regime,mode,exception=None):
    branch,missing,choice,slots = mode
    a0,b0,tmax,cap,slope,intercept,upper,n = REGIMES[regime]
    names = ([s+str(i) for s in "pq" for i in range(1,5)] +
             ["Mp","Mq","Rp","Rq","Sp","Sq","delta","t"] +
             [f"{end}_{v}" for v in slots for end in ("l","u")])
    cp = dict(p1=1,p2=-1,p3=-1,p4=-1)
    cq = dict(q1=1,q2=-1,q3=-1,q4=-1)
    bp = dict(p1=-1,p2=2,p3=-1,p4=-1)
    bq = dict(q1=-1,q2=2,q3=-1,q4=-1)
    centers = {}
    for side,c,other in (("p",cp,"q"),("q",cq,"p")):
        for i in range(4):
            centers[side+str(i)] = add(c,{side+str(i+1):1})
            centers[side+str(i+4)] = add(c,{other+str(i+1):-1})
        centers[side+"8"] = {side+"2":1,side+"3":-1,side+"4":-1}
        centers[side+"9"] = bp if side == "p" else bq
    rows = {}

    def row(label,coeff,rhs):
        require(set(coeff) <= set(names), "Unknown model variable")
        rows[label] = ([coeff.get(v,0) for v in names],rhs)

    for side in "pq":
        for i in range(1,4):
            row(f"D{side}{i}",{side+str(i+1):1,side+str(i):-1},-1)
        row(f"D{side}4",{"M"+side:1,side+"4":-1},-1)
        row("E"+side,{"R"+side:1,"M"+side:-1},-4)
    row("Gp",dict(Rp=-1,t=1),-a0)
    row("Gq",dict(Rq=-1,t=-1),-b0)
    row("Hp",dict(Mp=2,Rp=6,Sp=-2,t=slope),-(slope*a0-intercept+12))
    row("Hq",dict(Mq=2,Rq=6,Sq=-2,t=-slope),-(slope*b0-intercept+12))
    row("cap",dict(delta=1),cap)
    row("range",dict(t=1),tmax)
    row("branch",scale(1 if branch == "A" else -1,add(bp,bq)),0 if branch == "A" else -1)
    for v in slots:
        side = v[0]
        own,opp = (a0,b0) if side == "p" else (b0,a0)
        row("L"+v,add(scale(-1,centers[v]),{"l_"+v:-1,"t":-1 if side == "p" else 1}),-(opp+5))
        row("U"+v,add(centers[v],{"u_"+v:-1,"S"+side:-1,"t":1 if side == "p" else -1}),-(own+4))
    if exception:
        require(regime == "E", "Exception in the wrong regime")
        v,endpoint = exception
        require(v in slots and endpoint in ("l","u"), "Invalid exception")
        side = v[0]
        other = "q" if side == "p" else "p"
        if endpoint == "l":
            row("L"+v,add(scale(-1,centers[v]),{"l_"+v:-1,"M"+side:-1}),-(n-8))
            row("outside",{"l_"+v:-1,"t":-1 if side == "p" else 1},-((b0 if side == "p" else a0)+5))
        else:
            row("U"+v,add(centers[v],{"u_"+v:-1,"S"+side:-1,"M"+other:-1}),-(n-9))
            row("outside",{"u_"+v:-1,"t":1 if side == "p" else -1},-((a0 if side == "p" else b0)+5))
    row("loss",dict([("delta",-1)]+[(f"{end}_{v}",1) for v in slots for end in ("l","u")]),0)
    row("Fupper",dict(Sp=1,Sq=1,delta=1,Mp=-2,Mq=-2,Rp=-2,Rq=-2),upper-(n-8))
    return names,rows


def check_integer_certificate(names,rows,weights):
    require(isinstance(weights,dict) and weights, "Empty certificate")
    require(set(weights) <= set(rows), "Certificate uses an absent row")
    require(all(type(w) is int and w > 0 for w in weights.values()), "Weights must be positive integers")
    coeff = [sum(w*rows[k][0][j] for k,w in weights.items()) for j in range(len(names))]
    rhs = sum(w*rows[k][1] for k,w in weights.items())
    require(min(coeff) >= 0, "Negative coefficient in Farkas residual")
    require(rhs < 0, "Certificate does not give a strict contradiction")
    return dict(rhs=rhs,normalized_gap=Q(-rhs,sum(weights.values())))


def check_cover(bundle):
    require(bundle.get("format") == "upper100-integer-farkas-v1", "Unknown certificate format")
    expected = {case[0] for case in all_cases()}
    assignments,pool = bundle["assignments"],bundle["pool"]
    require(set(assignments) == expected, "Incomplete or extra case coverage")
    require(all(type(i) is int and 0 <= i < len(pool) for i in assignments.values()), "Invalid pool index")
    require(set(assignments.values()) == set(range(len(pool))), "Unused certificate in pool")
    results = {}
    for key,regime,mode,exception in all_cases():
        names,rows = linear_model(regime,mode,exception)
        results[key] = check_integer_certificate(names,rows,pool[assignments[key]])
    return results


def negative_controls(bundle):
    failures = []

    def rejects(label,operation):
        try:
            operation()
        except (ValueError,KeyError):
            failures.append(label)
        else:
            raise ValueError("Negative control accepted: "+label)

    rejects("invalid_hole_witness",lambda:hole_row(32,84,7))
    key,regime,mode,exception = next(all_cases())
    names,rows = linear_model(regime,mode,exception)
    rejects("zero_certificate",lambda:check_integer_certificate(names,rows,{"cap":0}))
    rejects("noncontradictory_certificate",lambda:check_integer_certificate(names,rows,{"cap":1}))
    rejects("negative_weight",lambda:check_integer_certificate(names,rows,{"cap":-1}))
    rejects("absent_row",lambda:check_integer_certificate(names,rows,{"invented":1}))
    partial = dict(bundle,assignments={k:v for k,v in bundle["assignments"].items() if k != key})
    rejects("missing_case",lambda:check_cover(partial))
    rejects("unproved_next_cardinality",lambda:scalar_audit(100,{}))
    # At n=100, z=0, a=41,b=42 the current budget allows two empty units.
    d=92
    cmax=22*d+97-(1+triangular(41)+triangular(42))-(2*d-12)
    require(cmax == 2*d == 184, "Next obstruction changed")
    return dict(rejected=failures,next_obstruction=dict(n=100,a=41,b=42,z=0,c_upper=cmax,unit_capacity=d))


def json_default(value):
    if isinstance(value,Q):
        return str(value)
    raise TypeError(type(value).__name__)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificates",type=Path,default=DEFAULT_CERTIFICATE)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    bundle=json.loads(args.certificates.read_text(encoding="utf-8"))
    certificates=check_cover(bundle)
    catalogue=hole_catalogue()
    scalars=[scalar_audit(n,catalogue) for n in (103,102,101)]
    counts=Counter(key.split(":")[0] for key in certificates)
    require(dict(counts) == dict(N103=68,N102=68,Z=68,P=68,E=2308), "Mode generation count changed")
    guards=negative_controls(bundle)
    summary=dict(status="PASS",conclusion="N <= 100, using the written reduction and audited N <= 103 foundation",
                 scalar_summaries=[dict(n=s["n"],**s["summary"]) for s in scalars],
                 linear_models=len(certificates),certificate_vectors=len(bundle["pool"]),regime_counts=dict(counts),
                 minimum_normalized_gap=min(r["normalized_gap"] for r in certificates.values()),
                 negative_controls=guards)
    out=dict(summary=summary,scalar_audits=scalars,certificate_checks=certificates,
             sha256={"verification/upper100.py":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     "data/upper100_certificates.json":hashlib.sha256(args.certificates.read_bytes()).hexdigest()})
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,default=json_default,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,default=json_default,indent=2))


if __name__ == "__main__":
    main()
