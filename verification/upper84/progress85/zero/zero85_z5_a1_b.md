# Fresh size-85 Z5: all A1 and B alternatives

This proof uses the fresh structure and the actual-retention classification
in `zero85_z4_z5_cards.md`. Its source has 77 points, core 69 points,
physical positive side sizes `r_s+r_t=68`, and no target holes. It does
not transplant the old Z5 normal-endpoint assumption.

Write

    I=(r_s-34)^2, A=I+tau+delta<=60,
    R_v=r_v+xi_v, xi=xi_s+xi_t<=tau, R=68+xi,
    M_v=R_v+e_v, L=e_s+e_t, M=R+L,
    a=s4=M_s+X_s, b=t4=M_t+X_t, G=g_s+g_t.

The source rows used below are

    S_s+S_t=2K+1085-delta, K<=M+R+21,
    L>=99+A, e_v>=A+16.

Several deliberately weaker computations use only `e_v>=A+8`.
On each physical side,

    S_v>=T_(r_v)+tau_v+4R_v+6+e_v.

All retained ordinary resources and licensed sole pair components have
a core hit, since their deficiencies are at most 60, less than 69.
With lower and upper clipping counts l_Z,u_Z and native deficiency Gamma_Z,

    Z>=73-r_v-l_Z-xi_v,
    Z<=S_v+r_o-72+u_Z+xi_o,
    Gamma_Z>=l_Z+u_Z.

These rows include centers outside the target hull. Monotonicity of
`x_i-i` bounds every core rank displacement by xi_v. No assertion that
the centers themselves are inside the target is made.

The eight O HIGH labels give fixed credit e>=8. Put epsilon=delta-e.
All compatible group deficiencies and unused native losses share this
one budget. The four extreme leaves are retained. Each of the ordinary
gap pairs contains at most one empty translate; their intersections with
an empty translate are off target and are charged only to its retained
partner's actual loss.

Delete the four largest core magnitudes on each side. The Q61 support gives

    f=61-(tau-xi)/4,
    c_s X_s+c_t X_t >= (c_s+c_t)f-max(c_s,c_t)*epsilon/2,
    c_s g_s+c_t g_t >= (c_s+c_t)f-max(c_s,c_t)*epsilon/2.

The second row uses the two disjoint ordinary pairs for each physical gap.
These star and ordinary-group inequalities are separately valid scalar
budget consequences. When endpoint resources are omitted from a grouping,
their native deficiencies can be rebated from epsilon.
The full-core star also gives `2X_v>=274-2R-epsilon`.

## Four reusable transport exclusions

### HIGH alpha_s

Suppose alpha_s is HIGH, while H_t,alpha_t,C5_t are retained. Since
alpha_s>=S_s+R_t+1, the identity

    alpha_s+C5_t=d_t-2(a+b)-G

and the endpoints of C5_t and H_t-alpha_t=d_t give

    2S_s+R_t+2X+G<=2R+976+r_t+xi+xi_t.

The three endpoint losses share epsilon. Using
`S_s>=T_r+tau_s+4R_s+10`, `2X>=4f-epsilon`, and discarding G>=0
gives

    2T_r+8r+I+2tau_s+6xi_s-2xi_t+e<=928.

Because xi_t<=tau_t and tau+delta<=60-I,

    2T_r+8r+3I+2delta+e<=1048.

For every integer r, `2T_r+8r+3(r-34)^2>=1092` (minimum at r=24).
Thus this HIGH-alpha alternative is impossible.

### Both pairs retained, opposite owners

Let beta_s and P_t be the actual sole owners. Use their lower endpoints,
the upper endpoint of V_t, and the leading-s inequality twice. The literal
identity is

    V_t=2d_s+beta_s+P_t+2a+b+g_s.

It gives

    S_s+3g_s+4X_s+2a+b
       <=935+r_s+delta-2e+xi+xi_s.

The source lower row and the separately valid bounds
`6X_s+X_t>=7f-3epsilon` and `3g_s>=3f-3epsilon/2`
yield, using the weaker e_v>=A+8,

    T_r+4r+3I+tau_s+tau/2+4xi_s+5xi/2
       <=136+5delta/2-13e/2.

The source mass cap therefore implies

    T_r+4r+11I/2+tau_s+3tau+4xi_s+5xi/2
       <=286-13e/2.

Its left side is at least `T_r+4r+3I>=626`, whereas its right side is
at most 234. Opposite owners are impossible.

### Both pairs retained, same owner, alpha_s retained

Let both sole owners be s and put r=r_t. Since alpha_t=h_t-b>-b,
the identity

    alpha_s-P_s=beta_s+beta_t+2d_t+2(a+b)+G

gives the strict lower relation
`alpha_s-P_s>beta_s+d_t+2a+b+G`. Use the endpoints of the three
retained s-resources and one leading-t inequality. The transport is

    S_t+M_s+2X_s+3X_t+g_s+2g_t
       <=R+1023-r-e+2xi_s+xi_t.

Here the source row is
`S_t+M_s>=T_r+3r+tau_t+4xi_t+xi_s+173+A`.
Together with `2X_s+3X_t>=5f-3epsilon/2`,
`g_s+2g_t>=3f-epsilon`, and e_v>=A+8 imply

    T_r+4r+5I/2+tau_t+tau/2+4xi_t<=520-7e/2.

The left side is at least `T_r+4r+5(r-34)^2/2>=608`,
while the right side is at most 492. This alternative is impossible.

### The branch-independent four-endpoint exclusion

Suppose pair1 has sole owner s, alpha_t is retained, and all eight lower
own/cross singletons are retained. The literal identity

    U_s=P_s+alpha_t+C6_t+2a+4b+2G

uses four distinct endpoints. Their losses share epsilon, giving

    S_t+2M_t+2X_s+4X_t+2G
       <=904+2r_t+2R-e+xi_s+3xi_t.

Use `S_t+2M_t>=T_r+tau_t+6R_t+18`,
`2X_s+4X_t>=6f-2epsilon`, and `2G>=4f-epsilon`. Then

    T_r+4r+3I+tau_t+tau/2-xi_s/2+7xi_t/2<=592-4e.

Since xi_s<=tau_s, its remaining excess terms are nonnegative.
Again the left side is at least 626 and the right side at most 560.
This exclusion uses no beta capacity, endpoint, or ownership.

## A1 with pair1 empty

The sole beta owner is s. The base holes are O_s,H_s,O_t,pair1 and
the remaining hole eta is exactly one of

    alpha_s, H_t, alpha_t, C5_s, C5_t, U_s.

For eta=alpha_s, emptiness above an active beta makes alpha_s HIGH;
the HIGH-alpha exclusion applies. Explicitly beta_s has a core hit,
so beta_s>=1-R_s. The leading inequality and A<=60 imply
`d_s-R_s>=93-r_s+I>0`, hence alpha_s=d_s+beta_s>0. Since
`S_s>R_t`, an empty alpha_s cannot have
`S_s<alpha_s<=S_s+R_t`: its image at source point -R_t would be a
target hit. Thus alpha_s>=S_s+R_t+1, as the exclusion requires.

For eta=C5_s or U_s, the retained endpoints are
alpha_s,beta_s,H_t,alpha_t,C5_t. The identities
alpha_s-beta_s=d_s, H_t-alpha_t=d_t, and
beta_s+C5_t=d_t-d_s-2(a+b)-G, followed by two leading-s bounds, give

    2M+6X_s+2X_t+3g_s+g_t
       <=853+delta-2e+3xi.

All endpoint and leading loss coefficients are at most two on distinct
resources. The weighted star and gap bounds give `12f-9epsilon/2`
for the gap part, so the source cap implies

    3+11I/2+5tau/2+13e/2<=0.

This is impossible. The ordinary gap pairs may contain the empty U_s;
its intersection is paid solely by the retained V_s loss.

For eta=H_t, use lower alpha_t,C5_s,beta_s,C5_t and upper alpha_s,V_t.
Their identities give

    4M_s+3M_t+6X_s+5X_t+3g_s+2g_t
       <=2R+744+r_s+delta-2e+4xi+xi_s.

The source lower bound is
`4M_s+3M_t>=3R+305+r_s+xi_s+4A`, using e_v>=A+8.
The gap part is at least `16f-9epsilon/2`. Consequently

    537+R+4I-3delta/2+13e/2<=0,

contradicting R>=68 and delta<=60.

For eta=alpha_t, use upper alpha_s,H_t and lower beta_s,C5_t,C5_s.
The latter beta and C5_s clipping coefficients are two. The exact transport is

    4M_s+M_t+6X_s+3X_t+3G+3h_t
       <=2R+754+3r_s+delta-2e+5xi_s+2xi_t.

Group the two g_s pairs with total deficiency Omega and the triple
{H_t,U_t,V_t} with deficiency Psi. The triple has
`g_t+h_t>=61+f-Psi`; hence
`3G+3h_t>=6f+183-3epsilon`. Separately the stars give
`6X_s+3X_t>=9f-3epsilon`. The physical source lower row
`4M_s+M_t>=R+123+3r_s+3xi_s+4A` then implies

    219+7I+13tau/4+3xi/4+8e<=0,

again impossible. No LOW-alpha endpoint assumption is needed.

## The final A1 hole eta=C5_t

The exact holes are O_s,H_s,O_t,pair1,C5_t. All eight lower own/cross
singletons, alpha_s,alpha_t,H_t,C5_s and sole beta_s are retained.

Initially the eight O labels and C22_s,C23_s,C24_s are HIGH. The LOW
labels are C55,C56,C57,C58 on both signs and C66_t,C67_t,C68_t.
There are 11 HIGH, 11 LOW, and 9 baseline groups touched by LOW,
giving compatible fixed credit e=13.

### The beta cutoff, with actual physical-target capacity

We first prove `beta_s+s3<d_s-X_s`. Suppose the reverse. Since
`d_s=2(a+b)+G+C5_s+alpha_t`, it forces

    alpha_s>=3M_s+4M_t+2X_s+4X_t+g_s+2g_t
                 +2C5_s+2alpha_t.

Target t has its leading and exactly six retained ordinary resources
H_t,alpha_t,U_t,V_t,C6_t,C7_t. Their total capacity is K+462.
Their grouped deficiency is at most epsilon, so the exact two-target
mass gives `S_s<=K+623-e`. The endpoint inequality above therefore gives

    2M_s+3M_t+2X_s+4X_t+g_s+2g_t
       <=R+416+r_t-e+E+2xi_s+3xi_t,

where `E=2l_(C5_s)+2l_(alpha_t)+u_(alpha_s)`.
The source gives `2M_s+3M_t>=2R+R_t+214+3A`.
The weighted stars give `2X_s+4X_t>=6f-2epsilon`.
If Omega is the weighted ordinary-gap deficiency, then
`g_s+2g_t>=3f-Omega` and `E+Omega<=2epsilon`, because those
ordinary groups avoid the three endpoints. Thus

    3A+9f<=134-e+4epsilon+xi.

The source cap turns this into

    355+4I+7tau/4+5xi/4+5e<=0,

an immediate contradiction. This proves the beta cutoff.

### The complete actual upper-tail inventory

Put t0=d_s-X_s>0 and add the four s-outer magnitudes to a target value
u>t0. A four-term representation with at most one top-two occurrence
is at most s1+3s3. With exactly two and not both s1, it is at most
s1+s2+2s3. Both lie below the required total, since
`d_s-g_s-X_s>=K-native_leading_loss+X_s>0`.
If both are s1, both remaining entries must be s3 or s4; otherwise
the total is at most the threshold. This gives three types C33,C34,C44.
Exactly three top-two occurrences give the four source families
O_s+D_s,H_s+D_s,alpha_s+D_s,beta_s+D_s, plus 24 free-outer types.
Exactly four give five further fixed types.

The complete 32 non-source types, in the original fixed inventory, are

    C13,C14,C15,C16,C17,C18,
    C23,C24,C25,C26,C27,C28,
    U3,U4,U5,U6,U7,U8,
    V3,V4,V5,V6,V7,V8,
    V2,U2,C22,C12,C11,C44,C34,C33,

all on target s. O_s and H_s source families are empty. The cutoff
removes beta_s+D_s and the six V3..V8 fixed types. Thus only the
retained alpha_s source family and at most 26 fixed types cover the
tail. Writing Gamma_alpha for its native deficiency,

    S_s<=d_s-X_s+103-Gamma_alpha.

The inequality is automatic when S_s<=t0.

### Four extra HIGH types and the sharper tail

The core hit of beta_s gives beta_s>=1-R_s. Since
`h_s=d_s+a+beta_s`, the preceding tail bound and the full-core star give

    h_s-S_s>=e_s+1+2X_s-103+Gamma_alpha
             >=52+I+tau-2xi+e
             >=-8+2I+delta+e>0.

Thus U4_s=h_s and U3_s=h_s+g_s are HIGH. Also
`h_s-d_s=a+beta_s>=e_s+X_s+1>0`, so
V2_s=2h_s+g_s-d_s and U2_s=2h_s+g_s are HIGH.
These four distinct labels are disjoint from the previous HIGH ledger,
which now has 15 HIGH, 11 LOW, touched 9: the credit is e=17.

All four labels belong to the 26 remaining types in the displayed tail
inventory. Removing them leaves at most 22 fixed types, giving

    S_s<=d_s-X_s+99-Gamma_alpha.

The generic endpoint rows of beta_s and alpha_s now imply

    X_s<=22+l_beta-l_alpha+xi.

### The final trim-one stars, with native rebates

Remove the largest core magnitude on each sign. The actual Q67 support
has span at most `66+tau-xi`, so

    |Q67 intersect (Q67+q)|>=f1-q, f1=67-tau+xi.

The two physical-s stars {L_s,V_s} and {L_t,C7_t} are retained and
avoid beta_s,alpha_s. Their original-budget inequality is

    2X_s>=2f1-epsilon+Gamma_beta+Gamma_alpha.

Combine this with the upper bound on X_s and use
`Gamma_beta>=l_beta`, `Gamma_alpha>=l_alpha`, and
`Gamma_beta+Gamma_alpha<=epsilon`. It yields

    2f1<=44+2xi+2epsilon,
    tau+delta>=45+e=62.

This contradicts `tau+delta<=60-I`. All ranks, outside-hull endpoints,
and possible numerical coincidences are included; no normality
assumption is needed.

## Routing the retained-pair1 A1 alternatives

First exclude the initially split beta case using only its whole paired
capacity. Both beta components active force the holes
`O_s,O_t,H_s,H_t,C5_t`, with pair1's actual sole owner s and every
lower own/cross resource and both alphas retained. The whole-pair total
hit count N satisfies

    77-delta<=N<=77, beta_s+beta_t>=N-M.

Use the endpoints of P_s,alpha_s and the identity
`alpha_s-P_s=beta_s+beta_t+2d_t+2(a+b)+G`.
Two leading-t inequalities then give

    S_t+M+2X_s+6X_t+g_s+3g_t<=931+2delta+xi.

The native endpoint and leading losses have coefficient at most two;
no selected beta component receives its own capacity or deficiency.
The weaker physical-source row
`S_t+M>=T_r+4r+R+109+A+tau_t+4xi_t`, together with
`2X_s+6X_t>=8f-3epsilon` and
`g_s+3g_t>=4f-3epsilon/2`, implies

    T_r+4r+13I/2+7tau/2+tau_t+3xi+4xi_t<=316.

But `T_r+4r+13(r-34)^2/2>=1357/2` for all integers r.
This excludes split beta before any sole-beta native loss is licensed.

If pair1 is retained, opposite owners are excluded above. Same owners
with alpha_s retained are excluded above. If alpha_s is empty, the
owner identity forces C5_t empty; the exact remaining holes are
O_s,H_s,O_t,alpha_s,C5_t. Pair1,alpha_t and all eight lower resources
are retained, so the branch-independent four-endpoint exclusion applies.
Together with the six pair1-empty placements this exhausts A1.

## Branch B

In B, beta_s,beta_t are singleton units, and C5_s,C5_t form a retained
paired unit with actual sole owner s. Pair1, when retained, has the same
owner. The classification proves integrality and extreme-leaf retention
before any native endpoint is used.

If alpha_s is retained, branch B's strict sign gives

    alpha_s-C5_s> d_t+2(a+b)+G.

Use its two endpoints and one leading-t inequality. The transport is

    S_t+M+2X_s+4X_t+g_s+2g_t
       <R+1029-e+xi.

The physical source lower row and the star/gap bounds, with the weaker
e_v>=A+8, imply

    T_r+4r+3I+tau_t+3tau/4+4xi_t+5xi/4<427-4e.

The left side is at least 626 and the right side at most 395.

If alpha_s is empty, it is the only extra hole outside the mandatory
beta/H choices. Consequently pair1,alpha_t and all eight lower resources
are retained, and pair1 has sole owner s. The branch-independent
four-endpoint exclusion applies. It borrows no beta-pair capacity from A.
These alternatives exhaust B.

The exact arithmetic checker is `check_zero85_z5_a1_b.py`. It checks
the displayed integral minima and terminal margins; the physical-target,
inventory, endpoint, and budget deductions are the written proof above.
The independent final-family audit is
`../scalar/z5_c5t_cutoff_audit.md`, with standalone checker
`../scalar/check_z5_c5t_cutoff_audit.py`. It independently confirms the
physical-target cutoff, all four additional HIGH types, the 26-to-22
tail pruning and the generic-endpoint trim-one contradiction.
