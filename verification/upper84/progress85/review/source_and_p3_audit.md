# Independent source and P3 audit receipt

Reviewed on 2026-10-05: `foundations/source_triple_fringe85.md`,
`positive/p3_terminal.md`, the referenced profile/localization notes, and
the matching explicit resource identities in the supplied report.

## Universal source cap

The two-maxima removal count is correct: the remaining 75-point source
has its central pair sums in an interval of `2R+C+1` positions, with only
the distinct same-sign triple fringes `P_s+P_t` outside. Reinserting two
maxima creates at most 153 new unordered pair labels. The full-source
interval has `2R+C+J+1` positions and exceptions `B_s+B_t`.

The combined mass inequalities give

    T <= 155 + sum_v(P_v+B_v-a_v-b_v).

The single-sign bound `P+B-a-b<=5` is valid over the unbounded offset
domain. For `a+b>=9` the ten-pair quartet fringe bound and `P<=6`
suffice. At sum 8, `2a<=c` gives `P<=5`. At sums 3,5,7 the written
finite triple table supplies the stated maxima. At sum 4, `P=4` occurs
only at `(1,3,4)`, whose fourth-offset fringe values are 5,5,4 before
the tail stabilizes at 4. At sum 6, `P=5` occurs only at `(2,4,5)`,
whose corresponding values are 6,6,5,5 before stabilization at 4.
The observations `c>=2b => P=3` and `e>=2c => B=4` justify the
unbounded tails; these are not numerical cutoffs.

Consequently the universal bound `T<=165` is sound. The source checker
passes. Its supplementary large enumeration is not needed as a proof
of the unbounded cases.

## P3 endpoint and forest terminals

No mathematical flaw was found in the written A0/A1 terminal deductions.
The arithmetic checker passes; the audit also checked the geometric and
resource premises which that checker expressly does not verify.

In A0, target t has its leading and seven ordinary retained resources,
of total capacity `K+539`. Its grouped deficiency is at most epsilon,
so `|F_t|>=K+539-epsilon`. Subtracting from the exact two-target mass
gives `|F_s|<=K+700-e` and `S_s<=K+700-e+w/2`. The five endpoint
resources are `P_s,alpha_s,alpha_t,C5_t,H_s`, with weights 1,2,1,1,1.
They are disjoint as whole resources from the two retained trees

    L_v--V_v--U_v, together with L_v--C7_v, on each target v.

Their six edge gaps total `2X+G`, and the Q61 intersection floor gives
`D_F>=6f-(2X+G)`. This confirms the master constant 488 and

    3M+12f+3e <= R+488+w/2+2delta+B_err.

For clipping count c<=71, `sigma_v+c<=146` and
`c(74-c)>=213` imply the stated light displacement allowance. The
remaining c=72 case is licensed by `sigma+epsilon<=144` at A0 z=2,4;
at z=6, three omitted low values include 1 and force tau>=176, hence
epsilon<=38, so c=72 is impossible. A1 has the stricter cap 143.
At most one relevant endpoint can be heavy: the z=2,4,6 A0 bounds and
the A1 profile bounds each give epsilon<146. Heavy next magnitudes are
peeled entries, so their errors are at most `b+sigma_v+e_v`. The
heavy terminal row follows by `3L-qe_v>=(3-q)L`, discarding the
additional positive constant `4q`, and the profile mass cap.

In A1 the ten retained edges are exactly

    L_s--V_s--U_s;
    L_s--C7_s--C6_s--C5_s;
    L_t--V_t--U_t--H_t;
    L_t--C7_t--C6_t.

The four-edge subforest consists of the first and fourth arms. The
two full-core stars are `L_s--V_s` and `L_t--C7_t`. Each leading has
one full capacity even when its two restricted core copies certify
different edges. The ten-edge, four-edge, and two-star inequalities
are separate valid budget consequences, combined by positive scalar
multipliers. They yield W with constant 411. The literal H_t identity
and the leading inequality used twice give the transport constant
1089. The physical source lower constants are 19,18,24,22 in the
four respective profile/orientation rows, giving scalar constants
571/2,1191/4,1167/4,305. All light/heavy reductions and the integral
quadratic minima were independently recomputed.

The terminal file originally abbreviated these explicit forest
descriptions as "same as old A1". The author has been asked to include
the labels above in the standalone proof. This is an exposition and
dependency improvement, not a detected mathematical failure.

This receipt does not independently certify the earlier finite dense
seed lemma, full owner classification, or the separate P4 terminals.
Those remain the stated prior premises of the reviewed P3 calculation.
