# Conditional cardinality-85 zero-hole reduction

These notes assume the common integral, primitive-core structural conclusion at cardinality 85. They do not claim to prove that conclusion. The original outer eight entries may initially be real. The actual-cover grouping rule and the raw 55 fixed-label inventories are unchanged.

Write `d=77`, `|E|=69`, `r_s+r_t=68`, `I=(r_s-34)^2`, `T_r=r(r+1)/2`, and `tau=sum(P_s)+sum(P_t)-T_{r_s}-T_{r_t}`. Put `R=R_s+R_t`, `xi=R-68`, so `0<=xi<=tau`. The four inner peels on side v have magnitudes `R_v+a_v`, `R_v+b_v`, `R_v+c_v`, `R_v+e_v=M_v`, with integral positive strictly increasing offsets. Define `L=e_s+e_t=M-R`, `U=a_s+b_s+a_t+b_t`, `C=c_s+c_t`, `J=L-C`, `A=I+tau+delta`.

## Fresh source envelope (all zero-hole j)

The ordinary whole-unit capacity is 77, not 78. The fixed allowance remains 84. Hence

```
S=2K+1470-77j-delta,
2K=77j-280+A+4R+U+C+L.
```

The second equality follows from the actual source mass `S=1190+I+tau+4R+U+C+L`.

Deleting both maxima leaves 75 values. Its pair-sum hull has at most `2R+C+1` positions and 12 exceptional same-sign peeled-pair labels. Reinsertion costs `2*75+3=153` labels. Therefore `K<=2R+C+166` and `J+U<=612-77j-A`.

The full source envelope is `K<=2R+L+1+B_s+B_t`. The four-offset inequalities `2B_v<=a_v+b_v+8` and `2B_v-a_v-b_v-c_v<=3` consequently give

```
J>=A+77j-298,
L>=A+77j-288,
A<=452-77j,
K-delta>=77j-142+I+tau,
K-M>=R+77j-440+A.
```

For the cap on A use `U>=6` and the two bounds on J. For `K-delta` combine its exact mass with the lower bound on L and `4R+U+C>=272+12`. For `K-M` use the upper bound on `L=C+J` and `U>=6`. In particular j>=6 is already impossible.

## Adaptive core supports

The full core has 69 points and span R, so its overlap at integral displacement q is at least `137-R-q=69-xi-q`.

After deleting the largest k positive core values on each sign, the source has `69-2k` points. The sum of deviations excluding each maximum is `tau-xi`. Monotonicity gives span at most `68-2k+(tau-xi)/k`, so its overlap is at least `f_k-q`, where

```
f_k=69-2k-(tau-xi)/k.
```

Every use of `max(f_0,f_k)` means choosing the actual one of these two subsets that attains the maximum, before constructing the forest. It does not add two overlap bounds or spend two deficit budgets.

## Z0 is excluded

All own centres are active, making all outer coordinates integral. `M>=76`; active C7 gives `d_v>=M+5>=81`. Choose an actual active beta contributor on side s. The raw two-gap bound gives `t_s=d_s-M<=57/2`; the opposite O gives `t_t<=56`. Active C4_s would imply `t_s>d_t>=81`. Active C4_t would imply `t_t>h_s+d_s>2d_s>=162`. Both contradict their caps, so pair1 has no actual contributor despite being retained.

## Z1 is excluded with a stronger adaptive endpoint

Outer integrality is proved from the same actual one-hole argument as the report: a side with all four own centres determines its outer values and lambda; opposite C6/C7 determine the other lower values; its remaining own centres determine its top values. At least one of C6/C7 is active on each side, so `d_v>=81`.

If pair1 were missing, an actual beta contributor opposite an actual C5 contributor would contradict the raw O cap. Therefore pair1 is retained. Its actual contributor forces its own O to be the unique whole hole; its beta is inactive. Branch B is impossible. In A the opposite side u has beta, H, O all active, so `2t_u<=57`. All alpha, C5, U, V, C7 resources below are retained.

For the six-edge trees `L_v-V_v-U_v` and `L_v-C7_v`, across both signs, choose

```
f=max(137-R,57-(tau-xi)/6).
```

Designate the full leading on u as root. Its native loss is ell_u. The actual-cover forest inequality yields `6f-2X-G+ell_u<=delta`. Active C7_u supplies a positive leading maximum, so `d_u>=K+2X_u+g_u-ell_u`. Active alpha_v and C5_u also give `t_u>=2X+G+2`. Adding produces

```
2t_u>=K-M-delta+6f+2
     >=I+max(121-5xi+tau,49+2xi)
     >=I+max(121-4xi,49+2xi)
     >=73+I.
```

The last minimum is attained at xi=12. This contradicts `2t_u<=57`. The six-rank support exists because the structural/source size bounds give at least 15 entries on each core side (and the source cap alone gives at least 15 for j=1).

## Z2 common activity reductions

Here `A<=298` and `K-delta>=12+I+tau`, so both leading resources are active. The same two-witness residue argument proves outer integrality.

The four-edge physical arm bound is freshly `2X_v+X_o+g_v>=252-tau-delta`: trim three ranks per side, whose span uses the fourth terminal deviation, giving each edge the lower overlap `63-tau/4`.

Suppose both cap predicates T_s,T_t hold. The four-top tail contains at most `4*(77+6)+5=337` values on each side, so `d_s+d_t+G+delta-2K>=796-77j`. Four full-core stars give `2X+4R+delta>=548`. With the exact mass and source envelope these two bounds give, at j=2,

```
4I+4tau+delta<=178.
```

If any C7_v is active, the four-edge activity implication gives `t_v>=253-tau-delta>=75`, contradicting the cap `t_v<=56`. If neither C7 is active, those are the exact two holes; both lower C6 are active, making each missing C7 HIGH. Each corresponding full leading has at least `r_v+81` off-target points: the entire shifted set `D_v union (M_v+D_v)` is HIGH and has at least `77+(r_v+4)` distinct points. Thus `delta>=r_s+r_t+162=230`, contradicting the bound 178. Hence T_s,T_t cannot both hold.

An active C4_v forces C5_v activity in branch A. Otherwise that missing C5 is HIGH above C4; its leading and at least five retained higher singletons lose at least `r_v+81` and five copies of `r_v+5`, respectively. This gives `delta>=6r_v+106`; but `I+6r_v>=195` for integral r_v, so `A>=301>298`. The actual-owner grammar follows from the unchanged literal centre identities and the active lower bound `u>-M_v`.

These statements reproduce the eight-row actual Z2 cover classification, with no new owner selected for empty or split paired resources.

## Z2 beta/O simultaneous-hit cards

Assume beta_v and O_v are active. The double raw gap gives `t_v<=57/2`, and opposite O_o is the first hole. Let W be the other whole hole. Use the report's four retained-resource cards, but every forest now selects `f=max(137-R,61-(tau-xi)/4)`.

1. If W is not V_v,C7_v,C7_o, the retained unused C7_v has at most 20 core target hits and all four negative peel images miss. Its native deficiency is therefore at least `69-20+4=53`. The rooted three-edge arm gives

   `t_v>=I+max(42-2xi+tau,18+7xi/4+tau/4)>=I+max(42-xi,18+2xi)>=34+I`.

2. If W=V_v, its HIGH status makes alpha_v,H_v,O_v each lose at least r_v+5 native points. Two retained shortcut edges and the full-core support give `t_v>=-65+I+3r_v>=35`; the integer minimum of `I+3r_v` is 100.

3. If W=C7_v, it is HIGH above retained C6_v. The three unused U_v,H_v,O_v losses give `t_v>=max(104-xi,80+2xi)>=96`.

4. If W=C7_o, its HIGH leading loses at least r_o+81 points and V_o,U_o,H_o lose at least r_o+5 each. Two edges with both leading roots yield `t_v>=16+I+4r_o>=148`.

Every lower bound exceeds 57/2. All roots and unused native losses belong to distinct original retained resources; no paired capacity is added in these cards.

## Z2 final six-edge contradiction

After that exclusion the same three literal hole families remain: `{O_v,B}`, `{O_s,O_t}`, and `{O_v,H_v}` with their actual forced owners. Every alpha,C5,U,V,C7 singleton is retained. At least one T_u is true. The unchanged identity `alpha_o+C5_u=d_u-2(M+X)-G` gives `2X+G<=54`.

Use the retained six-edge trees and the adaptive support `f=max(137-R,57-(tau-xi)/6)`. The actual cover gives `2X+G>=6f-delta`. Hence

```
A=I+tau+delta>=I+tau+6f-54
 >=I+max(414-5xi,342+xi)-54
 >=300+I,
```

because the minimum of that maximum is 354, at xi=12. This contradicts `A<=298`. Thus every actual Z2 configuration is excluded, with margin 2 at the balanced worst case.

## Sharper source interface and the later families

The independently proved joint triple/fringe source theorem in
`../foundations/source_triple_fringe85.md` gives `T<=165` and
`A<=445-77j` when there are zero holes. Thus the current bounds are
`A<=214,137,60` for Z3,Z4,Z5.
The Z3 argument retains the harmless weaker cap221 for its arithmetic.
Fresh complete-target rank constants are73-r and S+r_other-72.

A BAD ordinary centre has loss at least `73-max(r_s,r_t)`.
The old Z5 initial fixed ledgers with credits13 or14 do not by
themselves justify normality at cardinality85. The retained-P cards
and two empty-P cards below handle these endpoints directly. Only the
alpha-hole card obtains normality, after establishing its actual
credit27 independently of normality.

Z4 and Z5 calculations and literal endpoint lists are in
`zero85_z4_z5_cards.md`. The common Z3 A1 calculation is summarized
at the end of this file.

## Further result: the Z3 A0 family is excluded

At j=3 the source cap is A<=221 and the source-only rank rows, freshly derived from deletion of one maximum or two same-sign maxima, are

```
L>=A-57,
e_v>=max(4,A-146),
e_v<=378-A.
```

The one-maximum envelope is `K<=2R+c_v+e_o+94`, because its 76-point remainder has 16 exceptional pairs and reinsertion cost 77. It yields `|j_s-j_t|<=237-A-U`. Combining with `J>=A-67` and `U>=6` gives the lower e bound. The two-same-sign-maximum envelope is `K<=2R+b_v+e_o+167`: 75 remaining points, 13 exceptional labels, reinsertion 153. Combining with `J+U<=381-A` gives `e_v<=382-A-a_v-a_o-b_o<=378-A`.

The common j3 activity grammar still follows without any new raw-gap strengthening. Two cap predicates violate `4I+4tau+delta<=640-231j=-53`. The five-edge physical-arm bound is now `X_o+2X_v+G>=305-tau-delta`; active C6 gives `t_v>=85+I>56`. The four-edge bound gives active C7 `t_v>=32+I>57/2`. A HIGH C6 above retained C5 has native and higher-singleton losses at least `4r_v+96`; its sum with I has minimum 228, exceeding the source cap 221. These prove the same exhaustive two A families: A0 with holes B,O_s,O_t and pair1 owner s; A1 with holes O_s,O_t,H_s and beta owner s, pair1 owner t.

For A0 use the five endpoint resources C4_s,alpha_s,alpha_t,C5_t,H_s with weights 1,2,1,1,1. The complete-target lower endpoint is now `Z>=73-r_v-k-b`; the upper is `Z<=S_v+r_o-72+k+b`. Thus the endpoint identity has constant 233. Use six retained edges with `f=61-(tau-xi)/4`, giving gap 2X+G. The source mass constant 1239 and the forest baseline 12f=732-3tau+3xi cancel to give the same master constant:

```
T_r+4r+tau_t+2L-3tau+3xi_s+7xi_t <= 290+delta+Bstar,
Q3=T_r+4r+3I >=626 (r=28,29).
```

Use the common eight O HIGH fixed labels, so epsilon=delta-8. Define heavy selected clips as k>=72. For k<=71 the error is at most both xi_source and k, by `(73-k)b<=tau_source` and `tau+epsilon<=213-I`; at k=71 equality in `k(74-k)>=213` is allowed. Heavy tail error is at most xi_source+e_source-4, including k=72 where the stronger core-maximum error xi_source is available.

The five nonexceptional scalar finishes (the r-polynomial is the new Q3) are

| Endpoint pattern | Upper inequality | Lower bound |
|---|---|---:|
| alpha_s light, none heavy | Q3+tau_t+2delta<=625 | 642 |
| alpha_s light, one heavy c | Q3+tau_t+2delta+c<=781 | 858 |
| alpha_s light, two heavy H | Q3+tau_t+2delta+H<=945 | 1074 |
| alpha_s heavy, other source t | Q3+tau_t+2delta+c<=866 | 1002 |
| alpha_s heavy, other C4_s | Q3+tau_t+2delta+c<=948 | 1002 |

For the last two lower bounds it is enough to allow clips 72, so delta>=152 and c>=72. Each table row follows from the displayed master and, respectively, `2L>=2A-114`, `2L-e_v>=A-53`, `2L-e_v-e_w>=0`, `e_t>=A-146`, and `2e_t-e_s>=3A-670`.

The sole-heavy-alpha row needs a new fixed ledger. If its clip is exactly 72, the endpoint is the core maximum and has error at most xi_s; absorb it radially and use the first row, which is already contradictory. If its clip is at least 73, alpha_s<=0. The eleven fixed labels

```
U5_s,U6_s,U7_s,U8_s,V5_s,V6_s,V7_s,V8_s,F3_s,F4_s,F5_s
```

are LOW. The U labels are negative because alpha_s<=0. The V labels are negative because beta_s=alpha_s-d_s<0. The F labels are negative because the leading bound and `K-delta>=89+I+tau` imply `d_s>g_s`. Those 11 labels touch exactly 9 baseline groups: U7 has no baseline group, and U8/F5 share one. Together with the eight O HIGH labels, the compatible credit is 10. Replacing delta-8 by delta-10 lowers the master right-hand constant from 290 to 286. Cancel the heavy alpha error and use `2e_t>=2A-292`; the resulting exact row is

```
Q3+tau_t+2delta<=791.
```

But the native clip requires `delta>=10+73=83`, so its left-hand side is at least `626+166=792`. This strictly excludes the last A0 pattern. It is a new argument, not an automatic translation of the old report.

## Z3 A1 is excluded by the actual physical-side union

The full derivation and exact four-pattern checker are
`../common/z3a1_side_union.md` and
`../common/check_z3a1_side_union.py`.
The actual holes are O_s,O_t,H_s; beta is sole on s and pair1 sole
on t. The missing H_s is HIGH because H_s=beta_s+2d_s and beta_s
is active. Twelve compatible HIGH labels give epsilon=delta-12.
Grouping the leading and its seven actual native resources on s
gives `S_s>=K+539-epsilon`.

Let H be the native deficiency of active H_t, so H<=76.
Lower P_t and upper H_t are the only endpoints. Their actual clips
and the two separate forest rebates, on one chosen actual source
with `2tau+6f>=398`, give

```
M+M_s+6f-H/2<=47+2delta+E,
E<=xi_s+xi_t+p(e_t-4)+h(e_s-4), p,h in {0,1}.
```

Use L>=A-57 and e_s>=A-146. For
`Z=r_s+2I+2tau+xi_s+6f-H/2`, the four endpoint positions yield
upper bounds182,267,A+32,A+117. Even with A<=221 their largest
bound is338, whereas `Z>=398+34-38=394`.
This excludes all actual light/heavy positions of both endpoints;
no endpoint or error assumption is made on the beta translate.
Together with the preceding A0 proof it completes Z3.
