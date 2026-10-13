# Complete SIZE85 structure: integration and dependency check

The fresh structural argument is complete relative to the general mathematical
inputs already stated and audited in the supplied upper85 foundation sources.
It does not import a SIZE86 inverse row or finite exception census. The two
companion proofs are `structure85_ap_bootstrap.md` and
`../inverse/proof85_inverse.md`. The additional strict-inverse a13 closure is
now included in the latter and its exact checker.

## Entry: a prescribed zero and rationalization

Assume the already established upper bound `|A|<=85`. If a hypothetical
85-element feasible real set did not contain zero, adjoining zero would keep
every subset sum feasible: its subset sums are unchanged and its fourfold
sumset only grows. This would give a feasible 86-element set, a contradiction.
Thus a hypothetical size85 set contains zero.

To pass from its existence to an integral feasible example, enumerate the
85 coordinates and choose one fourfold representation of every subset sum.
These finitely many identities form a homogeneous linear system with integer
coefficients. Include the equation setting the distinguished zero coordinate
equal to zero. Its real kernel has a basis over the rationals; rational points
are dense in that kernel. Take a rational kernel point sufficiently close to
the original point to preserve all strict coordinate orders and nonzero signs.
The chosen identities preserve feasibility, and the added zero equation
preserves the prescribed zero exactly. A positive common-denominator scale
then gives 85 distinct integers. This argument transfers existence; it does
not claim that the original real coordinates themselves lie on a lattice.

## Exact resulting theorem

After the outer four-on-each-sign deletion and two further two-on-each-sign
peels, a positive normalization gives integral source sets of sizes

\[
 |D|=77,\quad |D_1|=73,\quad
 E=P\cup\{0\}\cup(-Q),\quad |E|=69,
 \quad a+b=68,\quad15\le a,b\le53.
\]

Both positive core sides are individually primitive. With
`T_r=r(r+1)/2`, `k=34-min(a,b)` and `I=k^2`,

\[
 \Lambda=1191+I,\quad \Omega=600-I,
 \quad0\le k\le19.
\]

On this common integer lattice the hull-hole counts satisfy

\[
 h_P,h_Q\le\kappa,\quad z=h_P+h_Q-\kappa,
 \quad0\le z\le\min(h_P,h_Q)\le\kappa,
 \quad0\le w\le4z.
\]

The actual extreme subset-sum translates in both peels intersect. If
`calT=kappa+ell1+ell2+g`, then

\[
 c+\rho+\mathcal T\le600-I,
 \quad\mathcal T\ge\kappa+144-3z,
 \quad\mathcal T\ge\max(48,z,144-2z).
\]

Each `rho_X>=0`. A non-AP side support obeys `mu_X>=r-3` and
`rho_X>=r-14` for `15<=r<=20`, or `rho_X>=r-5` for `r>=21`.
Maximum removal gives

\[
 R_X\le r+\rho_X+h_X+2,
 \qquad R_P+R_Q\le72+\rho+\kappa+z.
\]

In particular, if `z>0`, both supports are non-AP and

\[
 \mu\ge62,\quad\tau=\mu+h_P+h_Q\ge62+2z,
 \quad\rho\ge\begin{cases}58,&\min(a,b)\ge21,\\49,&15\le\min(a,b)\le20.\end{cases}
\]

No outer-integrality or leading-activity assertion is part of this theorem.

## Exhaustive branch checklist

| Core branch | Alignment and pre-lattice argument | Boundary or primitivity closure |
| --- | --- | --- |
| Initial deficient sign | Provisional available-sign peel; use `24*85+77=2117` before fixing `d=77` | One-sided 70-point lower count `2416` excludes it |
| Sign disappearing in later peel | Fixed `d=77`, one-sided 69-point core | Lower `2347` exceeds upper `1925` |
| `a=10` | Larger support must be AP, residue count and strict layer rows | `G144` contradicts budget `Omega+8=32` |
| `a=11` | AP branch or strict simultaneous inverse, with small-side `+16` correction | `G144`, or `T48+rho52-8=92>71` |
| `a=12` | AP branch or strict inverse, with `+16` correction | `z>=36`; effective `(56,5,132)` forces `rhoQ125>124` |
| Larger support AP, `a>=13` | AP-plus-set formula, one residue, unclipped gaps, `z=0`; layers then `G144` | Any nonprimitive smaller side has `c<=59<77`, `w=0`; `j0` obstruction; boundaries `a13,a14` also have `c<77` |
| Only smaller support AP, one residue, clipped gap or unique off-scale coefficient | Final disjoint supports cost `T_a+T_(b-2)+2-2b+rhoP` | Exact budget contradiction throughout |
| Only smaller support AP, one residue, no gap | `z=0`, `hQ=kappa`; both primitive | `a13`: `192>159`; `a14`: `c<=7<77,w=0`, `j0` obstruction |
| Smaller AP, two residues | Order-two residue, exact parity-fiber identity before hole bound; odd coefficient `W<=15`; strict AP-specific layers | `G144` gives `c<=61<77,w<=56`; `j0` obstruction |
| Both supports non-AP, sufficient inverse test fails, `k3..20` | Fresh 18 counted-endpoint repairs, including strengthened non-AP prefix bounds; short-diameter theorem | `z<=16`; strict layers before `G144`; nonprimitive `P` gives `c<=28<77,w<=64`, hence `j0` |
| Both supports non-AP, failed-test `a13` | Intrinsic primitive Q effective `(55,2,52)` gives `hQ<=4`; residue and short diameter | `G144`: `T+rho>=185>159` |
| Both supports non-AP, sufficient inverse test holds | Strict common lattice and hole bounds; all32 large-hole final-overlap orientations repaired before `G144` | Strict hole bounds imply individual primitivity |
| Both supports non-AP, strict-test `a13` | `kappa<=110`; corrected layer bound `-811<0`; then `G144`, `z>=17` | Effective `(55,4,119)` gives `rhoQ>=113`; `48-1+113=160>159` |
| Both supports non-AP, repaired `a14` | Endpoint `H<=8`; corrected strict pre-layer | `c<=23<77,w<=32`, `j0` |
| Both supports non-AP, strict-test `a14` | Corrected strict pre-layer; `G144` | If `z>=13`, effective `(54,6,168)` gives `rhoQ153`; otherwise `c<=31,w<=48`; both impossible |

Reflection is used only to order the scalar core sizes; both physical sign
orientations are included in every actual-owner statement. AP support type,
actual strict-test success/failure, and the boundary rows partition the entire
bootstrap range `a>=10`; no actual test is replaced by its sufficient floor.

## Dependency ordering: no use of integer holes before its lattice

1. The covering, peeling, `mu/rho` estimates, exact budget, inverse tests,
   residue counts, and counted-endpoint repairs are cardinality statements
   and valid before common-source integrality.
2. The short-diameter theorem is used on the proved common core lattice,
   and does not require unproved individual primitivity of the other side.
3. The pre-G comparisons use `C+Omega=-165-2I`, plus `16` exactly when
   the small-side maximum-deletion prefix has fewer than14 elements.
   Large-hole overlap is supplied independently of `G144`.
4. A strict comparison proves lattice alignment of the next layer and the
   intersection of its two extreme support translates. This is applied to
   both layers before counting their integer restricted-sum hull holes.
5. Only then use the sharp integral four-extreme inequality `G=144`, derive
   `w<=4z` and the structural T bounds, and invoke the conditional `j0`
   obstruction where the already proved caps supply `c<77,w<=104`.
6. Individual primitivity follows after these steps in the repaired branches;
   it is available immediately from strict hole bounds in strict-inverse
   branches. Thus neither residue repair nor `G144` assumes primitivity of P.

The remaining retained inputs are the general inverse/stability/defect,
restricted-sum and cover lemmas, not fresh finite cardinality-specific rows.
The exact checkers `ap_bootstrap85.py` and `../inverse/check85_inverse.py`
both pass; their arithmetic checks supplement the actual-set applicability
arguments in the written companion proofs.
