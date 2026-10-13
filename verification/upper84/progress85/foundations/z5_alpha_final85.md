# Complete Z5 A0 alpha-hole finish at size 85

This is the A0 family with both paired units empty and exact whole-unit holes
`{pair1,pair2,O_s,O_t,alpha_s}`. There is no assigned paired owner. All thirteen
remaining ordinary singleton units are retained. The fresh structural and
retention arguments have already given integral outer coordinates, leading
activity, `w=0`, and the source notation

\[
 r_s+r_t=68,\quad R_v=r_v+\xi_v,\quad
 0\le\xi_v\le\tau_v,\quad \tau_s+\tau_t=\tau,
 \quad A=I+\tau+\delta\le60.
\]

Write `a=s_4=M_s+X_s`, `b=t_4=M_t+X_t`, `G=g_s+g_t`,
`B=alpha_t`, `C=C5_s`, `D=C5_t`. The alpha hole is LOW, so
`h_s<=X_s`. The generic retained-core-hit argument and complete-target
rank bounds apply before normality; they do not import the old Z5 normality
bound. The refined source lemma gives `e_v>=A+16` on both signs.

## Fixed credit and the order in which normality is established

The following stages are the fresh tail/order deductions proved in the
zero-case companion. They are listed here with their actual labels and
incidence so the final loss budget can be checked.

Initially all retained singleton deficiencies are at most60, giving at least17
target hits, more than the eight peeled source entries; each has a core hit.
All selected native clips are below73, so the generic rank errors are bounded
by the appropriate `xi_v`. Both paired components and the alpha hole are LOW.

The initial ledger gives `e=14`. Its source support obtained by trimming four
core ranks on both signs has `q=61` and overlap at least
`f=61-(tau-xi_s-xi_t)/4`. The stars, g pairs, leading, and the retained
`{H_s,U_s}` pair then give

\[
 X_v,g_v\ge38,\quad h_s\ge15,
 \quad d_v\ge107+g_v+2X_v.
\]

These inequalities and the exact32-type upper-tail inventory give
`S_s<=H_s+M_s+2` and `S_t<=H_t+M_t+16`, yielding the additional13 HIGH
labels below. The two places requiring cross-centre lower endpoints use the
proved core-hit lower bound `C5_v>=1-R_v`; they have strict margins larger
than26 and16. The consecutive-tail argument needs `h_s>2`, supplied by15.
Thus this step gives `e=27` without assuming normality.

Now a BAD ordinary centre has deficiency at least
`73-max(r_s,r_t)`. Put `k=|r_s-34|`, so `I=k^2`. Its excess over the available
budget `epsilon=delta-27` is at least

\[
 73-(34+k)-(60-k^2-\tau-27)
   =k^2-k+6+\tau>0.
\]

Hence every retained centre is normal. The native upper endpoints and
unused-loss rebates prove `B,D<a`; the fixed-only prefix count proves `C<b`.
All three retained centres `B,C,D` are now positive.

The complete HIGH set is

\[
 \mathcal H=\{C_{11},C_{12},C_{13},C_{14}\}^{s,t}
 \cup\{C_{22},C_{23},C_{24},C_{16},C_{17},C_{18}\}^{s,t}
 \cup\{C_{33}^{s}\},\qquad|\mathcal H|=21.
\]

It meets no baseline group. The LOW stages and exact incidence are:

| Stage | Added LOW labels | `H` | `L` | Groups touched | Credit |
| --- | --- | ---: | ---: | ---: | ---: |
| Initial | `C55,C56,C57,C58,V5,V6,V7,V8` on both signs; `U5,U6,U7,U8,V2,V3,V4` on `s`; `F3,F4,F5` on both signs | 8 | 29 | 23 | 14 |
| Tail | No new LOW labels;13 HIGH additions | 21 | 29 | 23 | 27 |
| `B,D<a` | `U5,U6,U7,U8,V3,V4,C66,C67,C68` on `t` | 21 | 38 | 25 | 34 |
| `C<b` | `C66,C67,C68,C35` on `s` | 21 | 42 | 25 | 38 |
| Two cross labels | `C25` on both signs | 21 | 44 | 26 | 39 |
| Remaining three | `C35_t,C45_s,C45_t` | 21 | 47 | 26 | 42 |

For the last two stages the literal identities are

\[
 \begin{aligned}
 C25_s&=C-D-2b-g_t,&C25_t&=D-C-2a-g_s,\\
 C35_t&=C25_t-h_t,&C45_s&=C35_s-g_s,&C45_t&=C35_t-g_t.
 \end{aligned}
\]

All are negative because `1<=C<b`, `1<=D<a`, and the outer gaps are positive.
The `C25_s,C25_t` group is the sole previously untouched unstarred baseline
row1, so two new labels cost one new touched group. `C35_t` is in the reflected
row9 already touched by `V3_t`; the two `C45` labels are in the two row12
groups already touched by `V8_s,V8_t`. Thus the final compatible fixed credit
is **42**, and all native losses below share `epsilon=delta-42>=0`.

## One actual adaptive core support

The final credit and `A<=60` imply `I+tau<=18`. Let
`E_v=tau_v-xi_v`. For `j_v` in `0,1,2,3,4`, remove that many largest positive
core coefficients on sign `v`. For zero removals use the excess `xi_v`. For
positive removals, monotonicity of the core deviations gives the retained
maximum at most

\[
 r_v-j_v+\lfloor E_v/j_v\rfloor.
\]

Choose on each sign a minimizing removal count for

\[
 \phi_v=\min\left(\xi_v,
       \min_{1\le j\le4}\{j+\lfloor E_v/j\rfloor\}\right).
\]

This determines one **actual** subset `Q` of the core, containing zero. It has
`q=69-j_s-j_t>=61`. Its integer displacement overlap is at least `F-u`, where

\[
 F=69-\phi_s-\phi_t.
\]

Both physical targets use this same subset and its reflection. All group
inequalities below use this chosen support; no overlaps of different subsets
are added or charged to the same budget. The triple bound keeps `q>=61`
explicitly, so replacing the old overlap by `F` does not discard its source
cardinality condition.

## Disjoint groups and exact transport

Use the following original retained singleton groups, and no paired capacity:

| Group | Resources | Deficiency |
| --- | --- | --- |
| Pair | `B,D` | `Gamma` |
| Triple | `H_s,U_s,V_s` | `Psi` |
| Two ordinary pairs | `U_t,V_t` and `C6_s,C7_s` | Summed `Omega` |
| Singleton | `C=C5_s` | `Gamma_C` |
| Singleton | `H_t` | `Gamma_Ht` |

They contain eleven distinct retained singleton units. Their actual union
deficiencies sum to at most `epsilon`. The joint counting lemma gives

\[
 2B+D\ge3(73-r_t)+F-3\Gamma,
 \quad g_s+h_s\ge q+F-\Psi,
 \quad2g_t\ge2F-\Omega.
\]

The first row combines `B+D>=2(73-r_t)+F-2Gamma` with the normal native lower
bound `B>=73-r_t-Gamma`; it uses the same `Gamma` throughout. Also
`l_C<=Gamma_C`, `u_Ht<=Gamma_Ht`, and `u_Hs<=Psi`.

The literal centre identities and normal upper endpoints are

\[
 H_s=a+2b+G+h_s+B+C,\quad
 H_t=a+2b+G+h_s+B+D,
 \quad H_v\le S_v+r_o-72+u_{H_v}.
\]

Use the exact source mass `S=2K+1085-delta` and
`K<=M+R+21`. Adding the upper endpoints and subtracting the packed lower
endpoints gives precisely

\[
 2M_t+2X_s+4X_t+2(G+h_s)+F
 \le2R+827+2r_t-\delta+3\Gamma+l_C+u_{H_s}+u_{H_t}.
\]

Insert the two gap inequalities. The loss terms are bounded by
`3Gamma+3Psi+Omega+Gamma_C+Gamma_Ht<=3epsilon`, so

\[
 2M_t+2X_s+4X_t+2q+5F
 \le2R+827+2r_t-\delta+3\epsilon.
\]

Separately valid weighted stars on the same support give
`2X_s+4X_t>=6F-2epsilon`. Combining these scalar inequalities does not assert
that the star grouping is disjoint from the displayed eleven-unit grouping.
Finally use `q>=61` to obtain

\[
 2M_t+122+11F\le2R+827+2r_t-\delta+5\epsilon.        \tag{*}
\]

## Exact finite scalar contradiction

Since `M_t=r_t+xi_t+e_t` and `e_t>=A+16`, (*) would require

\[
 2I+2\tau-2\delta-2\xi_s+11F+5\cdot42-809\le0.
\]

Using `delta<=60-I-tau`, its left side is at least

\[
 4I+4\tau-2\xi_s+11F-719.
\]

The nonnegative `4I` may be omitted. The complete remaining finite domain is
`0<=tau<=18`, `tau_s+tau_t=tau`, `0<=xi_s<=tau_s`,
`0<=xi_t<=tau_t`, all integers. It has7315 tuples. The exact checker finds

\[
 \min(4\tau-2\xi_s+11F-719)=6,
\]

attained in the relaxed domain at `(tau,tau_s,tau_t,xi_s,xi_t,F)` equal to
`(16,11,5,5,3,61)`. Relaxing unrealizable core parameters only enlarges the
domain, so a positive minimum on this domain suffices. This contradicts (*),
and excludes the final A0 alpha-hole family.

The companion `z5_alpha_final85.py` reconstructs every baseline group,
checks all staged incidence counts and literal new-label identities, selects
one actual trimming prescription per tuple, and checks this exact finite
minimum. It does not substitute arithmetic for the preceding actual-cover,
normality, and joint-deficiency arguments.
