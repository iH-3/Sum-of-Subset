# Size81: order of the structural lattice implications

This note assembles the ordinary primitive non-AP lattice step and the
unconditional outer step. It is not a completed structural adoption and
does not assert the upper bound80. The AP/no-clipping and one-sided inverse
repairs must retain their own hypotheses; the last finite root is also open.
All numerical tables below are read from the existing exact receipt
`results/2026-10-24/upper80_research/lemmas_normal.json`, under
`checks.structure_arithmetic`. That arithmetic was not rerun.

## Quantities available before the source lattice

After integer replacement of a hypothetical size81 set and the two
peelings, write E=P union{0}union(-Q), |E|=65, a+b=64,
I=(32-a)^2, Lambda=1057+I and Omega=646-I. The inherited exact budget is

    rho+2*theta+c+kappa+ell1+ell2+g = Omega,
    |FS(E)| = Lambda+mu+kappa.

All terms except rho are nonnegative. The universal floor rho>=-16
is available without individual primitivity. This budget can be used
before D1 or D has been placed on the common unit of E. In contrast,
G>=max(46,z,136-2z) and G>=kappa+136-3z require their separate
lattice/overlap licenses and are not inputs to the following argument.

For a positive integer core X of size r, let Y be X without its maximum.
The exact maximum-removal defect identity gives

    max X <= r+rho_X+h_X+2-rho_Y-h_Y.

It is essential to keep the predecessor terms. Set
J=(rho_(P-minus-max)+h_(P-minus-max))
 +(rho_(Q-minus-max)+h_(Q-minus-max)). The inner factor-two comparison
has upper bound

    -9-2I+rho-mu+2z-2J.

For small ranks one may conservatively add16. The maximum is a diagonal
defect, so rho_X<=mu_X; using rho-mu<=0 is valid at ordinary ranks.
The rank7/8 argument in the companion boundary note uses the weaker
rho-mu<=4 and J>=-16 and is therefore safe without this improvement.

## Ordinary individually primitive non-AP cores

Assume the core unit and the short-diameter conclusions have already been
established, both cores are individually primitive and non-AP, and
15<=a,b<=49. In particular 0<=z<=min(h_P,h_Q). The persistent-hole
profile at49 applies to both cores if z>=49. Its paired defect floor678
already exceeds Omega<=646. This excludes z>=49 before any use ofG.

Use f(r)=-8 for r<=12, f(13)=-1, f(r)=r-14 for14<=r<=16,
and f(r)=r-5 for r>=17, on non-AP supports only.

If both predecessors are non-AP, J>=f(a-1)+f(b-1). With z<=48,
the inner comparison is bounded by

    -9-2I+96-2*(f(a-1)+f(b-1)) < 0.

This is the saved `Two nonAP predecessors` check for all orientations.
If both predecessors are AP, the final non-AP extension costs at least
T_(a-2)-2 and T_(b-2)-2 in defect. Their sum exceeds Omega; the case
is impossible from the pre-lattice budget.

If only the predecessor on the r-side is AP, the other predecessor is
non-AP. The same final-extension identity gives rho_X>=T_(r-2)-2,
and J>=f(s-1), where s=64-r. A nonnegative inner comparison would require

    z >= Z = 5+I+f(s-1).

If Z>48 it is already impossible. Otherwise the saved census has exactly
r=29,...,36. A persistent-hole profile on the other primitive core then
gives the following excess over Omega, including the cost kappa>=z>=Z.

| r | Z | Excess over Omega |
|---:|---:|---:|
|29|43|91|
|30|37|94|
|31|33|102|
|32|31|115|
|33|31|133|
|34|33|156|
|35|37|184|
|36|43|217|

Thus every case has a strict inner factor-two bound. If an added point
of D1 lay outside the established core lattice, FS(E) and its translate
by that point would be disjoint subsets of FS(D1), contradicting that
strict bound. Therefore D1 lies on the core unit. No post-lattice lower
bound forG was used.

## The outer step is uniform

The exact peeling inequality is

    |FS(D)|-2|FS(D1)| <= 4*73-10+ell1-ell2-|FS(E)|.

Eliminate ell1 with the exact budget, and discard only nonnegative terms.
The right side is at most

    282+Omega-Lambda-rho = -129-2I-rho <= -113-2I < 0.

Once D1 is integral in the core unit, any point of D outside that unit
again creates two disjoint translates of FS(D1), a contradiction. Thus D
is integral. This outer implication is uniform: it does not require either
core to be primitive or non-AP, and it does not assume source-hole
localization. It applies whenever a preceding argument has licensed the
inner step. Its derivation is the exact two-stage peeling identity in
`upper103_from115_20261014.tex`, with the size81 constants substituted.

## Interfaces that are still separate

This ordinary argument does not supply a common core unit by itself. The
failed-small-inverse repair first needs the endpoint schedule, the larger
strict inverse, and the no-clipping/short-diameter argument. The saved
high-kappa exceptional rows are a=29,30,31,32, with respective thresholds
578,558,531,513 and endpoint pairs(6,6),(10,8),(14,12),(16,16).
Their ratio-two gap-filling argument must be presented before importing
the ordinary short-diameter conclusions.

For nonprimitive cores, persistent-hole profiles may only be used on the
primitive side. The saved capacity census leaves a=17,...,24, with
z<=6 and c<=98, to the small-slack bridge. For AP cases, first establish
the residue-class census and no-clipping licenses; only then use the
parity-fiber mass inequality and its W<=21,z<=20 consequences. Reflection
at a=b=32 exchanges all side-specific witnesses, as detailed in
`upper80_small_rank_interface_20261024.md`.

The low-slack bridge requires no individual primitivity: its uniform
domains are j=1,delta<=110 or j=2,delta<=40, with even w<=32 and F>=24.
The license forF is tau<=455<T21+T21=462, hence phi_s+phi_t<=41 and
F=65-phi_s-phi_t>=24. This is an interface to the already checked88
conditional certificates, not a new replay of those certificates.

The remaining full adoption must join these cases, the small-rank note,
the high/low-hole localization and every finite-model applicability gate.
The current finite count4653/4654 cannot replace those arguments.
