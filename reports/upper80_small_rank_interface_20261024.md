# Core ranks 7 and 8: the AP boundary interface

This note resolves the rank7/8 core cases and their two-stage source-lattice
interface. It is not a complete size-81 structural adoption and does not
certify the bound80. The larger-AP balanced case and other structural domains
still require their complete adoption arguments.

Write `a+b=64`, `I=(32−a)^2`, `Omega=646−I`, and
`U=FS(P)`, `V=FS(Q)`, including zero in each support. Let their cardinalities
be `u,v`. The already established peeling budget gives

    rho_P + rho_Q + kappa <= Omega,
    kappa = |U+V|−u−v+1 >= 0.

The universal small-side defect floor is `rho_P>=−8`. A non-AP large
support has `rho_Q>=b−5`; an AP large support has `rho_Q>=0`. Also
`u−1>=T_a` and `v−1>=T_b`.

## Interval summands and the exact clipping cost

Suppose one support is `[0,v−1]` in its intrinsic unit. If the other support
occupies `c` residue classes modulo that unit, classwise sumset counting gives
`kappa>=(c−1)(v−1)`. Thus `kappa<v−1` forces one class. Since the support
contains zero, all its points are integers in the interval's unit.

Let `g_i` be the number of missing integers in each gap of that integer
support. Successively adjoining the intervals of length `v` gives exactly

    kappa = sum_i min(g_i,v−1).

If `kappa<v−1`, no gap is clipped. Therefore `kappa=sum_i g_i`, and the
combined core has `z=0`. This argument does not assume that the other core
is primitive in the chosen unit, or that it too has AP support.

## Rank 7

Here `(b,I,Omega)=(57,625,21)`. If the large support is non-AP, then

    rho_P+rho_Q >= −8+52 = 44 > 21,

already contradicting the pre-lattice budget. If the large support is AP,
then `kappa<=29<T_57=1653`. The interval-summand argument above gives a
common core unit and `z=0`, including the case in which both supports are
AP. No separate halfstep assumption is needed at this boundary.

## Rank 8

Here `(b,I,Omega)=(56,576,70)`.

If the large support is AP, `kappa<=78<T_56=1596`; the same argument gives
a common core unit and `z=0`.

If only the small support is AP, the non-AP floor on the other side gives
`kappa<=70+8−51=27<T_8=36`. Interchanging the two supports in the
interval-summand argument again gives a common core unit and `z=0`.

If both supports are non-AP, the same cap `kappa<=27` lies strictly below
both existing short-diameter inverse thresholds: already
`u−2>=T_8+8−4=40` and `v−2` is larger. The ordinary strict inverse branch
therefore supplies a common core unit with both hole counts at most
`kappa`; in particular `z<=27`. This uses the same inverse theorem as
the ordinary structural branch, without invoking the post-lattice budget.

## The retained-predecessor inner comparison

In the new inner comparison

    −9−2I+rho−mu+2z−2J,

retain the optional conservative `+16` for small ranks. From the definitions,
`rho−mu=4−2Delta_0(P)−2Delta_0(Q)<=4`. Each predecessor defect is at least
`−8`, and each predecessor hole count is nonnegative in the common core
unit, so `J>=−16`. Hence the inner comparison is at most

    43−2I+2z.

It is at most `−1207` for rank 7 and `−1055` for rank 8. Thus the inner
comparison needs neither a later source-overlap assumption nor a positive
core-hole profile in these boundary cases.

## Outer-source lattice propagation without a primitive-side assumption

The exact peeling identity used in the earlier complete proofs gives

    |FS(D)|−2|FS(D1)| <= 4d−10+ell1−ell2−|FS(E)|.

Here `d=73`, `|FS(E)|=Lambda+mu+kappa`, and
`rho+2theta+c+kappa+ell1+ell2+g=Omega`. The quantities other thanrho
are nonnegative, includingmu. Consequently the right-hand side is at most

    282+Omega−Lambda−rho = −129−2I−rho <= −113−2I < 0,

where the last inequality uses only the universal two-side floor
`rho>=−16`. This comparison therefore holds for every rank under discussion,
including AP and nonprimitive cores. It does not useG, hole propagation or
a later source-overlap premise. The general peeling identity and strict
factor-two argument are in `upper103_from115_20261014.tex`, equations
labelled `eq:budget`, `eq:inner` and `eq:outer`; retainingrho above makes the
small-rank allowance explicit rather than importing the oldrho>=0 premise.

The preceding inner comparison first putsD1 on the established core unit:
an added point outside that unit would place two disjoint copies ofFS(E)
inFS(D1), contradicting its strict factor-two bound. WithD1 integral, the
outer comparison putsD on that unit by the same disjoint-translate argument.
This proves the missing source-lattice interface for ranks7 and8.

The sharp four-extreme estimate can now be used in its licensed order:
`G>=max(46,136−2z)`. The terminal contradictions are immediate.
An AP case has `z=0` and `rho>=−8`, giving `rho+G>=128>70>=Omega`.
For the rank-8 two-non-AP case, `rho+G>=−8+51+46=89>70`.

The remaining adoption tasks include the larger-AP balanced reflection and
the other structural domains listed in
`verification/upper80/research_checkpoint.md`. Closing this boundary does not
replace those arguments or the two still-open finite roots.

## Balanced AP orientation: exact reflection

At `(a,b)=(32,32)`, if the AP support is on the second labelled side,
replaceA by−A and interchange the side labels. This preserves feasibility
because `FS(−A)=−FS(A)` and `4(−A)=−4A`. Both peeling operations commute
with reflection, soE,D1,D are reflected as well. The new positive core is
the old negative core with its sign removed, and conversely. Thus the AP
side can be namedfirst without changinga,b orI. The sumsmu andrho, the
sumset excesskappa, the total holesz, and all peeling cardinalities and
slacks are unchanged. Individual extrema, hole counts and tail sequences
are exchanged, not identified.

Consequently a proved AP-first halfstep or no-clipping argument with
`a<=b` applies at equality to either labelled AP side, with identical
constants. Every use of a side-specific predecessor or endpoint witness
must be exchanged along with that side; no floor for a non-AP predecessor
may be moved onto the AP predecessor. This is the full symmetry transport
needed at the balanced larger-AP boundary. It introduces no new numerical
exception and does not use the isolated coarse estimatec<=9. The AP-first
halfstep/no-clipping proof and its interfaces must still be assembled in
the complete adoption before a global80 claim can be made.
