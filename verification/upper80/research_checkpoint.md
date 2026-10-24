# Size-81 research checkpoint, updated 2026-10-24

**No global bound 80 is certified yet.** Main remains 71 <= N <= 81. This file
records new mathematics and arithmetic to be integrated into a complete proof,
only after all finite cases close and the interfaces below have been audited.

The later 2026-10-24 target-geometry continuation adds adaptive probe widths,
sharp first-hole thresholds 95,124,187, and all 256 outer-subset translates
against a complete 495-root/4845-leaf four-sum envelope. Its general arguments
are in `reports/upper80_target_geometry_20261024.md`; nine strengthened OPEN
premises are replayed by `verify_target_geometry.py`. No additional original
root is closed. The separate 176-node discovery frontier is not a covered
branch tree, even though 46 of its local checkpoints are closed.

## Extended-window continuation (2026-10-24)

`full_window.py` now certifies arbitrary affine complete windows, including
propagation through each of the eight unused outer points. This closed the
entire `k=0` and `k=1` slices of `(6,436,0)`, and the unrestricted root
`(5,270,0)`. Together with previously checked `k=2..7`, and the source budget
`k^2<=58`, the six-empty-cell root is now closed. Current total: 4,647 closed
original roots and seven open roots. `verify_extended_windows.py` and
`data/upper80_extended_windows_20261024.json.gz` preserve the new exact records
and immutable identities of the reused rank packet. The general argument is
in `reports/upper80_extended_windows_20261024.md`. No global 80 claim is made.

Do not rerun the earlier closed slices, baseline suites or completed target
enumerations. `window_search.py` records method and premise digests, retains
proved cuts on continuation and skips finished checkpoints. Additional target
partitions and first-gap core cases are still partial research work.

## Verified foundation improvements

1. `verification/upper80/density.py`: bounded-density theorem extends beta<=9
to beta<=24, for unbounded r>=beta+3. Exact boundary DFS, complete binomial
counts, independent brute bases beta<=9, small ranks3..8, and a false-interval
negative control. PASS, 163099562175850 boundary sets represented by certified
pruning, 227239 independent boundary cases, 1728 small-rank cases.

Pruning: partial FS contains [L,S-L], with S-2L+1>=M; every unchosen coefficient
is <=M. Adjoining any such coefficient preserves this interval shape, since
the interval and its translate overlap or abut. Count all completions exactly.
The final theorem's lower holes number <=beta because all such holes lie in
[1,2beta] subset [1,r+beta], which has only beta absent generating coefficients.
For beta>=9 the induction join at r>=beta+4 is T_(r-1)>=r+5beta+1, its difference
increases by r-1. beta<=8 uses the retained small bases and polynomial
(r*r-13*r+38)/2>=1 for r>=9. Symmetry supplies the upper holes.

2. Late-jump improvement S-6beta -> S-5beta. Suppose FS(X) has holes only in
[1,2beta] and their reflections, at most beta at each end. If x>=S-4beta:
- x<S-2beta: the preimage of new points above S avoids the lower-hole strip,
  hence at least x-beta >= S-5beta new points;
- S-2beta<=x<=S: at most 2beta total holes, hence x-2beta>=S-4beta;
- x>S: every translated support point is new, at least S+1-2beta.
When x<S-4beta the central intervals join. If x<=2beta, lower holes may fill,
but cannot increase; insisting that their exact set remain unchanged is not
necessary. This licenses density thresholds i>=beta+5 through beta24.

3. `profiles.py` independently replays 410 new synchronous claims (r15..55,
h=5,7,9,11,13,15,17,21,31,49), 13530 AP-prefix branches, 225375 updates. It uses
OLD-round budgets, new bridge T_(j-1)-5beta>j+U_j+1 and the original offscale
T_(j-2)-1>U_j. Data `data/upper80_profiles.json.gz`. Pair minima for ranks
summing64: (h,mu,rho)=(5,164,86),(7,214,122),(9,262,158),(11,308,194),
(13,352,228),(15,394,270),(17,434,310),(21,508,384),(31,658,534),(49,802,678).
The nonAP rho floor r-5 uses the previously certified threshold17.

4. Adaptive endpoint schedules in `endpoint_new.py`: B=R+1, L>=18,
2<=beta_i<=H/2 and i>=beta_i+5 if beta_i<=24, else i>=2beta_i+4,
B<=T_i+i-5beta_i-r-7. Require B<=L-6+sum(beta_i-1), and for EVERY possible
last AP prefix t=L-1..r-1,
B<=T_t-t-2+sum_{i=t+2}^r(beta_i-1).
Thus some NON-AP prefix has y_i<=beta_i. Its density follows from small-increment
inverse. A later offscale step at m+1 costs at least T_m+m-r-6 in final rho,
which exceeds the retained late-jump threshold. This avoids an unwarranted
use of the old B<=T_(L-1)-r-1 condition after changing the AP schedule.

## Size81 structure constants and proposed complete repair

D73, E65, r_s+r_t64; after reflection r_s=32-k,r_t=32+k,I=k^2.
Lambda1057+I, Omega646-I, G136, ceil(G/3)=46. rho+2theta+c+T=Omega.
At least five opposite pairs: q even, q^2<=3088, hence q<=54.
Initial a>=7; a7 nonAP is excluded by f(57)-8=44>21.
Source tau+delta<=496-73j+w-I; theta_source=73j-342-w+I+tau+delta.
K>=145, K<=M+R+1+Bs+Bt, K<=2R+C+158.

Pre-G base inner comparison C+Omega=-9-2I, where C=-655-I.
Keep the predecessor term in maximum-removal:
 max X <= r+rho_X+h_X+2-rho_Y-h_Y, Y=X without max.
Writing J=sum(rho_Y+h_Y), the old inner comparison improves to
 -9-2I+rho-mu+2z-2J (plus conservative16 if a<=14).

For ordinary individually primitive nonAP cores r15..49:
- h49 profile already forbids z>=49 before G (paired rho678 plus kappa>=49
  exceeds Omega646-I).
- If both predecessors nonAP, J>=f(r-1)+f(s-1), so with z<=48 the inner
  margin is at least17. `preg_prefix_scan.py` checks every rank.
- Both predecessors AP impossible: rho>=T_(r-2)+T_(s-2)-4>Omega.
- One AP predecessor: rho_X>=T_(r-2)-2. The inner comparison is negative
  unless z>=Z=5+I+f(s-1). Only r29..36 remain with Z<=48, and h31 profile
  on the other (primitive) side gives rho_X+rho_Q+Z-Omega >=91.
Thus no final-overlap assumption is needed to close this pre-G step.

Failed inverse at smaller side: kappa>=T_a+mu_P-1. Hence rho_Q<=
R=Omega-T_a+1-(a-3)-f(a). New endpoint radii for a9..32 are
6,8,10,12,14,16,18,22,22,24,26,28,30,30,30,32,30,30,26,24,20,16,14,10.
For a<=28 the standard strict diameter margins hold (using actual kappa).
For a29..32 split at threshold V-4H-5 (V=T_b+b-2): 578,558,531,513.
Below it all standard margins hold. Above it both sides have small rho and
intrinsic endpoint radii (6,6),(10,8),(14,12),(16,16). Their intrinsic units
have coprime ratio (1,1),(1,2) or (2,1): three residue classes already cost
2*(min support size-1)>Omega. Ratio1 contradicts kappa<=H_P+H_Q. In ratio2,
the dense ordinary-unit side has a central interval longer than EVERY gap in
the doubled side (gap<=2*(H_doubled+1)); its translates therefore fill the
middle, leaving z<=h_ordinary<=H_ordinary. Both predecessors are nonAP because
rho caps are below T_(r-2)-2. The retained-predecessor pre-G comparison is
negative; after G, rho+kappa+136-3z>Omega in all four rows. See
`inverse_repair_scan.py`.

In the ordinary repaired branch, a28..32 pre-G can again retain both
predecessor floors: failed inverse gives mu_P<=K+1-T_a<T_(a-2), and rho_Q
is below T_(b-2)-2. For a<=27 the original -9-2I+2H(+16) is already negative.

If the smaller side is nonprimitive, conservatively kappa>=T_a+a-3.
For every 0<=z<=H, use the NEW profile only on primitive Q:
 c<=Omega-f(a)-rho_Q(z)-(T_a+a-3)-136+3z.
Maximum is98; c>=73 only for a17..24 and z<=6. Their Q central intervals
exceed every source coefficient even using w<=4z (minimum propagation margin219).
Thus w<=z<=6 and j1,delta<=25. For c<73, j0 and w<=4H<=128<154 contradict
all-retained lemma. See `nonprim_scan.py`.

AP repairs: redo old class-count and no-clipping argument with new schedules.
At most3 classes (all a8..32 margins positive), one/two offscale cases excluded.
Three classes occur a10..22; new H<=10 and c caps are strictly negative.
The no-clipping endpoint H for kappa>=2*T_a is <T_a in all these rows.
Halfstep smallest odd W>=23 fails the affine mass bound for all ranks, so
W<=21,z<=20. Refined per-rank W bounds in `ap_scan_new.py`. Both parity fibers
are complete after no-clipping. Their central width exceeds every source
coefficient using initial w<=80, so w<=z<=20. c<=180, hence j<=2,
j1 delta<=107, j2 delta<=34. Pre-G at a<=28 is strict directly (or via the
per-rank z caps); a29..32 retain rho of the nonAP predecessor, since its rho
cap is below T_(b-2)-2. The larger-AP balanced case a32 is the reflected same
halfstep case; do not use its coarser isolated c<=9 as a terminal proof.
Both AP unequal units are included in this halfstep analysis. One-class
nonprimitive possibilities give c<=158 and z=0, also covered by small slack.
These AP licenses still need to be written out and audited as one coherent
argument, especially a7/8 and the larger-AP reflection.

Small slack new independent LP interface:
F>=24, w<=32, span M>=72, j1 delta<=110: all22 patterns certified.
Same, j2 delta<=40: all66 patterns certified. Data under .work/upper80/low_c*.
F is licensed by tau<=423+32=455<T21+T21=462, so phi_s+phi_t<=41, F>=24.
No primitive-core mass floor is used. Leads have hull hits because delta<145;
full integrality is ensured by the pattern catalogue at j<=2.

Small ranks after their own lattice/primitivity proof: a8..10 excluded by
rho profiles and G46; a11..14 obtain endpoint H12,16,20,24. Actual z caps
4,8,10,12. Source propagation is strict; a11/12 mass contradicts j>=1;
a13/14 have only j1 and delta<=24,64, handled by the small-slack interface.
See `small_scan_new.py`.

High holes: second layer exact constant -129-2I. With H=kappa+z,
2L<=1586+w-2I-2c-mu-rho-2z,
M<=861+H+(rho-mu)/2+z-I-c,
W0=1056+I+mu-H,
W0-M>=-1097+4I+3c+1.5*(mu+rho)-3z.
Bands15..16,17..20,21..30,31..48 use paired profiles above. Their H caps
304,280,246,168 are below min(T_r+I)=352. For j>=1 propagation has positive
margin (first band70); j0 uses M<=2z-5 and its central strip. Once localized,
w<=z. z>=17 contradicts source mass for j>=1. z15/16 forces j1 and delta<=14,
w<=16, handled by small slack. z>=49 impossible already before G.
Lowz1..14 uses the new h49 profile to prove each core mass>H; then
W0>=676+73j-w+2I+delta, M_v<=687-73j+w-delta.
At j1,w56:693>670. Hence w<=z<=14, even, eta_s=eta_t=w/2 and tau>=58+2w.
The intended main domain is r_s15..32 and r_t64-r_s.

## New finite-model licenses

The broad model remains a research prototype until all geometry and coverage
are audited. Original uniform roots4654; most reused/new direct certificates
exist, but several j4/5/6 branches are still OPEN.

Leading hulls j1 hit by missing-component count. j>=3 has K-delta>0. For j2,
a below-target leading forces all four cross components LOW; the two
orientations for zero holes AND positive holes have separate exact certificates
`missing_leading*.json`. No leading lower-hull inequality is used in these
auxiliary systems. Above-target leading forces four own components HIGH plus
an absent P, impossible with only4 missing components.

Ownerless gap rows must NOT be inserted at initial credit8 for w0. All three
are conditionally licensed when the four margins
1+B(w)+e-3w/2, 47+e-3w/2, 8+e-3w/2, 9+e-3w/2
are positive. B(0)=-12; B(w)=min_p(max(58+2w,T_floor(p/2)+T_ceil(p/2))-4p).
e>=22 suffices. Helper `ownerless_rows` checks all w in the relevant regime.
Core hit uses upper clip<=68. Alpha zero-hole tail rows are licensed at e>=22:
each paired gap has2x>=e-3, so x>=10 and1+3x>26. At e>=42,
360-4*131+4e>0 licenses core constant64 on all twelve paired edges.

New K bounds: Q=D without both extremes, |Q|71, |2Q|<=2R+C+13.
Reinsert the two maxima and three pairs: K<=2R+C+158 minus their respective
intersections with old extremal Q translates. Each rebate is at least
max(0,F-(e_v-c_v),FD-4-(e_v-c_v)). All8 nonempty choices are recorded as a
separate proof-trace step, preserving old certificate row indices.

Internal source gap (2R_v+c_v,M_v-R_o) has e_v-c_v-R-1 integer positions.
Only six pairs from the smaller three own tails and four maximum/opposite-tail
pairs can enter it. Thus K<=3R+e_o+c_v+Bs+Bt+12 for each side, and combining
the disjoint two gaps gives K<=4R+C+Bs+Bt+23. Separate trace step.

Trimmed-source compression: removing q=1,2,3 largest points on BOTH sides gives
n=73-2q and mass TD_q=TD-sum(removed absolute values)+q*(73-q).
The existing residue compression lemma applies to each actual trimmed source.
New variables TD1,TD2,TD3 are enabled by per-record `trim_source` flag, so old
certificates reconstruct their original row inventory.

Diameter compression: for an integer set Q of n points and diameter<2x,
every residue class mod x has at most2 points, and its pair (if present) is
at distance x. Therefore |Q intersect(Q+x)|=n-number_of_classes>=n-x.
Apply to E,D,or D with1/2/3 maxima removed on each side. Diameter branches
are strict 2x>=diam+1 versus2x<=diam. Beware the equality boundary: Q={0,2},x1
shows that diameter=2x does NOT license n-x.

Order branches now allow alpha/beta against ANY retained native-chain center,
not only C5. Their common-D overlap edges enter the exact rooted forest.
This closed j3's last root with17 rank-specialized leaves (`quick3_v5.log`).

Required terminal: if j>=3, O_v absent, all outer coordinates integral and
S_v>H_v+M_v, the actual endpoint S_v belongs to FS(D_v), so one of the sixteen
fixed-tail labels must equal S_v. Complete disjunction: S<=B or 16 equalities
with S>=B+1. `terminal:s/t` is an optional explicit branch; overlapping label
choices are allowed but every choice must be covered. Initial ownerless test
on t closed15 of17 cases; t below and t=C33 remain open.

Fresh full baseline upper81 replay PASSED all4654 roots/4853 terminals,
digest8594ce625131c7fb931d4c1e20f72050054e8b71269ff640dec03b6a49fe4160.
Output `.work/upper80/baseline81.json`. Baseline -O not rerun yet.


## Additional proved source facts and current checkpoint

See the companion report for the complete proofs. Removing both core maxima gives
q_v=r_v-1+tau_v-xi_v. Every sum involving the retained core is in
[-M_t-q_t,M_s+q_s]. Count the 15 peeled same-sign pairs on each side outside
this hull. This yields K <= M+63+tau-xi+B_s^*+B_t^*, or
K <= M+tau-xi+93-u after u pair exclusions. Each exclusion has guard
1+2xi_v-tau_v+o_i+o_j-e_v <= 0. The example
D=[-31,31] union {+-40,+-41,+-42,+-43,+-85} has K=243 and equality,
whereas the old source fringe bound is259.

Source truncations q=1..4 use m=4-q, rank r+m and excess
 tau+m*xi+sum(first m offsets)-T_m.
Each removed positive p with p-gap in the retained guaranteed interval,
and each removed negative -b with gap-b in that interval, yields a distinct
intersection point. Counts from different truncation levels are combined by
MAXIMUM, not addition. The exact trace kind is extended_overlap_hit.

The new source hull and overlap facts closed positive roots (5,256,1) and
(5,268,1); exact replays have584 and463 steps respectively. There are now
NINE unresolved original roots, as listed in README.md. The large j6 research
search remains incomplete: many closed leaves do not close the root.

The pooled partial packet contains direct records, five completely closed
branch trees, and all nine explicit open-root states. Run replay_partial.py
to check its arithmetic and complementary domains. It explicitly does NOT
certify structural applicability or a new global bound. The current density,
profile and source-bound results are independently checked by check.py.

## 2026-10-24 continuation (work in progress, no new global bound)

The source capacity now subtracts internal gaps. Remove the maximum of each
core; the retained core Q is in [-q_t,q_s], with either
q_v=r_v-1+tau_v-xi_v (mass family), or q_v=R_v-1 (maximum family).
The peeled points on side v are p_0=R_v,p_1=R_v+a_v,...,p_4=M_v.
For i=0..3, the open gap (p_i+q_v,p_(i+1)-q_o) can contain only sums of
peeled points. Its integer length is G= p_(i+1)-p_i-q_v-q_o-1.
There are at most 40 candidate index pairs: 15 same-sign pairs and 25 cross
pairs. Certify a pair outside by sum<=lower or sum>=upper. If v pairs are
excluded, missing positions are >=G-(40-v), even when this is negative.
Different nonempty gaps on both sides are disjoint. Never mix the two
families in one subtraction (they may overlap).

For a subset A of mass-family gaps and u trimmed outer-pair exclusions:
K-M-(1+|A|)tau+(1+|A|)xi+sum_A(pnext-p)
 <=93+103|A|-u-sum_A(v).
For maximum-family gaps combine with the original fringe row:
K-M-(1+|A|)R-B_s-B_t+sum_A(pnext-p)
 <=1+39|A|-sum_A(v).
Known equal pair sums are merged into equivalence classes; a class is outside
if any representative is certified outside. Replace 40-v by the number of
remaining classes. The trace checks both directions of each equality.

Example: positive source 1..32 plus 33,34,99,175; negative magnitudes 1..32
plus 33,34,161,207. Actual |2D|=392; previous trimmed hull 456; mass gaps 393.
2501 direct-set regression cases passed both gap families. These finite tests
are controls, not the proof of the universal counting lemma above.

Core mass ceiling tau_v <= r_v*xi_v follows because every ordered deviation
is between 0 and xi_v. In a rank interval use the largest possible r_v on
each side. This excludes spurious LP points with R_v=r_v but tau_v>0.
Source variables xs,xt,ts,tt,delta,K and all eight tail offsets may now be
branched as integers. The broad caps are tau,delta<=496-73j+14[positive],
offsets<=655-73j+14[positive], K<=4096. The last follows conservatively from
K<=2R+c_s+c_t+158 and the preceding caps for every j=1..6.

Leading-source intersection: a known exterior ordinary-source preimage can
also map into lambda+2D through any known p+I, 2I, or a consecutively joined
chain of these intervals. Count these exterior preimages together with the
old hits whose ordinary preimages lie in the retained core; the two classes
are disjoint. Different truncation levels are maximized, not added. New
leading guards, including a nonempty-interval guard for merged chains, have
passed 6000 source/edge controls and 6000 merged/truncation controls.

Fixed labels already contained in a retained ordinary Z+D or leading
lambda+2D contribute no new points. Certify membership in a guaranteed
integer interval using the same core and merged-interval witnesses. Apply
only for j>=3 and the full integer pattern (no state 3). A covered label
whose positivity is also proved cannot discharge a negative-sum group's
mandatory nonpositive label. Without positivity, conservatively allow it
to discharge that group. Count each removed label once.

Fixed-label conflicts give additional capacity bounds. Two labels cannot
both contribute distinct new values if their sum is <=1, their sum exceeds
the sum of their target endpoints, their same-target distance is >=S, or
they are equal in the same target. The latter needs two exact inequalities.
After removing proved LOW/HIGH/covered labels, retain each negative group's
mandatory deletion unless a possible LOW already removed discharges it.
Add the conflict edges. An exact minimum hitting-set recurrence bounds the
number of remaining distinct contributions. 480 small hypergraphs have
been checked against exhaustive independent subset enumeration.

A further fixed conflict comes from two ordinary-source probes. If the
positive fixed forms f_1,f_2 give distinct ordered probes 1<=p_1<p_2<=r-1
in one core side of the same retained translate, omitting both costs
2(r-1)+3-p_1-p_2 in its maximum-removed excess tau-xi. Thus
 tau-xi+p_1+p_2-2(r-1)-2 <=0
forces at least one fixed form into that native source. Add a conflict edge,
not two individually covered labels. All containment, positivity, ordering
and mass guards are explicit exact certificate targets.

Discovery now recovers endpoint hull planes from exact simplex determinants,
discarding degenerate or non-supporting candidates and deduplicating rational
planes. This reduced one endpoint family from 204 planes to 22 and a flat
family from 135 to one. The replay still independently checks every selected
majorant at every finite triangle vertex. No floating infeasibility is
accepted as a certificate.

Small-AP repair: exhaustive nondecreasing deviations of total <=2r-3 for
r=2..14 (22101 sets, independent partition count) prove rho>=0 whenever
FS(X) is an AP. Outside that range of total excess, Delta_0<=r proves the
same inequality immediately. For a7,b57,Omega21, both nonAP are excluded by
52-8>21. If the larger side is AP, kappa<=29<T57 forces the smaller support
into its unit and forbids clipping; z=0. The pre-G comparison is strict,
and G=136 contradicts Omega even with rho_small=-8. For a8,b56,Omega70,
the larger-AP case is identical with kappa<=78<T56. In the smaller-AP / larger-
nonAP case, rho_large>=51 gives kappa<=19<T8=36, hence one residue class,
no clipping, z=0, and the same contradiction. The larger-AP-only a30/31
cases have endpoint radii8/14 and strict post-G caps -90/-36. At balanced
rank32 reflect so that the AP side is the smaller-side halfstep analysis;
its refined cap is -9. These arguments still need integration with the
complete structural proof and its independent numerical checks.

Latest jobs/checkpoints live under .work/upper80/20261024. No new original
root has yet been certified closed at the time of this checkpoint. A size6
rank0 tree with fixed-cover splits reached credit58 (budget58); complementary
branches are still being checked. The old packet remains 4645/4654 closed.

Full native graph: the new `full_edges` record flag adds every pair of retained
ordered chain translates and a leading-anchor edge to every retained chain
translate. Original edges keep their indices; additional edges are appended.
Every ordinary difference is positive by the native chain order. Leading
left/right differences use the same extreme embedded D anchors as before.
The exact forest lemma applies to any acyclic subset, so this needs no new
union bound; it makes the existing point and compression witnesses available
for nonadjacent translates. Older records reconstruct their original graph.

### Explicit necessary target coverage (2026-10-24)

`cover_geometry.py` constructs a deliberately enlarged, explicit union, independently
of cardinality accounting. On physical side v subtract the sum of the four
positive outer points v1>v2>v3>v4>M_v from 4A. Every positive remaining value
belongs to lambda+2D_v, one of ten ordinary Z+D_v translates, or one of the
55 fixed labels. Here lambda=v1-v2-v3-v4, alpha=v2-v3-v4,
beta=2v2-v1-v3-v4. Proof by number of source terms:

* Four or three source terms are strictly negative after the subtraction.
* With two source terms, every outer pair except 2v1 is bounded above by
  v1+v2, leaving 2M_v-v3-v4<0. The only surviving source resource is lambda+2D_v.
* With one source term, at least two copies of v1 give the eight lambda+b_i
  centres. With exactly one v1 only the pair 2v2 survives, giving alpha.
  With no v1 only 3v2 survives, giving beta. The next possible outer sums
  are strictly negative after adding M_v and subtracting the four extremes.
* With zero source terms, at least two v1 give 36 C labels. Exactly one v1
  and at least two v2 give seven U labels. With no v1 and at least three v2
  there are seven V labels. The five remaining potentially positive maxima
  are F1=v3-v4, F2=2v3-v2-v4, F3=v2+v3-v1-v4,
  F4=2v3-v1-v4, F5=3v3-v1-v2-v4. Every next smaller pattern is nonpositive.

Discarding ordinary translates whose full hull is LOW or HIGH is legitimate.
Enlarge the core E to [-R_o,R_v]. Each retained ordinary translate is now
one interval plus eight singleton tails. The leading resource is enlarged
into nine intervals and 36 singleton pair sums. Include all 55 fixed labels.
There are 154 components per side in the six-empty root. Direct comparison
with the actual 4A (bitsets, not this catalogue) passed 240 physical targets
and 30462 four-sum values. This is a regression control for the classification.

A probe is the interval of integers starting one unit after a component's
right endpoint. Its width is 1 in the zero-hole regime, and 8 in the positive
regime because each physical target has at most seven holes. Prove its
bracketing inside [1,S_v] by exact certificates. Every candidate component
can be excluded only by proving its whole interval lies strictly before or
after the probe. If every component is excluded, the target has too many
holes: this is the new `coverage_final` combinatorial terminal. If precisely
one component remains, it must intersect the probe, giving two new necessary
linear rows (`coverage_force`). All guard branches are complementary integer
inequalities; no numerical infeasibility or sampled gap is accepted as proof.

Discovery only: use an existing uncovered probe before inventing more probes,
and branch on an unproved exclusion. This prevents trying to certify hundreds
of unrelated target points before resolving the first actual uncovered region.

### Integer witnesses, exact rounding and modular exclusions

In a full integer pattern, all twenty ordinary centres are integral. Thus
g=U-V, h=H-U, d=O-H and p=h-alpha are integers, and X=p-M is integral.
The source parameters, its mass, K, delta and all fixed forms are integral.
This license is used only for j>=3 with no state3 in the pattern.

The finite model also admits integral *witness variables* for an actual set:
phi=min_t(t+d_(r-t)) and chi_b=min_t(bt+d_(r-t)) are minima of integer
expressions. Therefore F=|E|-phi_Es-phi_Et, FD=|D|-phi_Ds-phi_Dt and
GB_b=b|D|-chi_bs-chi_bt are integers. The ell, D, l and u variables are
cardinalities of omitted points; LS and LT are the deficits between the
nominal total resource cardinality and its actual native union. They too
are integers. TD and TD1..3 are integer mass excesses. These choices satisfy
the original necessary rows, so imposing their integrality loses no actual
configuration. This is not an assumption that an arbitrary relaxed LP
solution has integral coordinates.

An `integer_guard` step proves g-1<0 by an ordinary exact Farkas certificate,
checks that g has integer coefficients and only licensed integral variables,
then appends g<=0. Generic `integer_cut:name:m` branches are the complementary
conditions name<=m and name>=m+1; there is no arbitrary upper cutoff.
Discovery optionally rounds bounds on F, FD, GB_b and the four phi variables.

For a zero-hole target probe, a singleton component contributes only if its
value equals the probe. `modular.py` may exclude this equality by an integer
linear combination of exact model equalities, modulo an integer m>=2.
An inequality pair may supply an extra equality only after both directions
are certified. Normalization divides each equation by an exactly checked
common divisor. Replay checks that every combined coefficient is divisible
by m while its right side is not. This is impossible for integral variables.
Singleton modular exclusions are not used for width-eight positive-hole
probes. Standalone modular controls check 8400 targets against bounded
integer enumeration and reject 6130 mutated certificates.

`structure_arithmetic.py` now independently checks the rank tables, adaptive
endpoint schedules, repaired high-kappa range, small ranks, AP ranges and
high-hole bands recorded above. This remains conditional arithmetic, not a
completed structural proof. The larger strict inverse inequality is used
only after the high-kappa alternatives have been excluded; it is false as
an unconditional statement at the balanced endpoint.

Latest verified rank refinement of the open j6 root: k=3,4,5,6,7 each has an
exact terminal certificate. The new joint top-core-tail row closes k=2 with
three complementary splits and four terminal certificates. These are saved
in data/upper80_refinements_20261024.json.gz and independently replayed by
verify_refinements.py, including the exact branch-path domains. The k=0,1
subdomains remain open. The original-root count is still nine.

### Known native unions and the top-core tail (2026-10-24)

For each side choose L_v either zero or r_v-1-tau_v+xi_v, licensing L_v>=0
in the second case. The max-removed core has r_v-1 coefficients and excess
tau_v-xi_v, hence contains [1,L_v]. Add its known maximum and four tails.
The resulting B subset D has exactly L_s+L_t+11 points: its central interval
and ten distinct exterior points are disjoint. Each ordinary translate
contains Z+B, and the leading resource contains lambda+2B.

`known_union.py` constructs all these explicit integer intervals and points.
For lambda+2B, connected chains of component intervals certify a lower bound
J_v on its cardinality. Consecutive components must join or abut and extend
the right endpoint; different counted hulls are proved disjoint. For the
union of all known resources inside [1,S_v], every component is either
proved outside the target or assigned to a certified containing hull, whose
length is nonnegative. This gives an upper bound U_v without requiring those
upper hulls to be disjoint. Therefore the actual native loss is at least

    sum_v [ J_v + n_v (L_s+L_t+11) - U_v ],

where n_v is the number of retained ordinary translates on that side. To
see this, the unknown remainder of the leading has at most K-J_v points,
and each ordinary unknown remainder has 73-|B| points. After adding the
fixed credit e, append this expression minus delta <= -e. No intersection
is subtracted twice. If tau=0, B=D; the exact connected components recover
the complete native union. Direct checks passed 300 physical sources, with
equality in all 100 zero-excess cases. This includes higher multiplicities
missed by the rooted-forest estimate.

A simpler consequence applies whenever H_v is retained and O_v is absent.
All retained ordinary centres are <=H_v, since alpha=H-d, beta=H-2d and
the native chain is ordered. Put T_v=H_v+R_v and certify T_v>=0. Every
ordinary source point except its four positive tails is <=T_v. If
e_v-X_v-g_v-h_v<=0, the full leading resource also ends at or below T_v,
because lambda+2M-T=e-X-g-h. Hence every represented target integer above
T_v is one of the four positive tail points from each retained translate,
or one of the 55 fixed forms. Prove a candidate <=T_v or >=S_v+1 to remove
it. If q candidates remain, even counting duplicates separately is safe:

    S_v - T_v - hole_W <= q.

This does not require zero holes; at most hole_W target values can be absent.
The trace licenses both inequalities first, records each candidate exclusion
with an exact certificate, and only then uses the capacity row.

If both sides are licensed, let q_src count only their remaining ordinary
source-tail candidates. All fixed points which are already native-covered
are accounted for there. The total number of new fixed values is <=84-e.
Consequently the stronger joint row is

    S_s+S_t-T_s-T_t-2 hole_W <= q_src+84-e.

Negative S_v-T_v only weakens the left side, so no extra T_v<=S_v premise is
needed. The actual-set control includes373 licensed single tails and119
joint tails, as well as the300 known-union checks.

Discovery-only diagnostic: an all-integer relaxed k=0 point with tau=0,
K=279 and delta49 has the actual source tails (33,34,37,110) and
(33,34,38,94). Its actual |2D| is275, the two native targets have55 and40
missing values, and every in-target fixed value is already natively covered.
This is not a solution of the original problem. It motivates the new union
and top-core-tail rows; the numerical MIP result itself is never a proof.

## Enlarged union capacity

`cover_capacity.py` complements the preceding lower bounds on native loss.
Enlarge the core to its full integer hull [-R_t,R_s], retaining the eight
exterior source points. Ordinary resources are then one interval and eight
points, and each leading resource is nine intervals and 36 pair points.
These are precisely the native components of `cover_geometry.catalogue`.
They contain every actual native point, even when the core has holes.

To bound their union in [1,S_v], prove each component outside the target or
assign it to a containing integer hull. Endpoint comparisons certify the
containment; anchors at 1 or S_v use the target intersection. Every component
is assigned exactly once. Each hull has nonnegative integer length, and the
sum U_v of these lengths bounds the union whether or not hulls overlap.
The previously proved credit e bounds all new fixed values by 84-e. Hence

    S_s+S_t-2 hole_W-U_s-U_t <= 84-e.

Alternatively include all fixed forms in a single side's component inventory;
then S_v-hole_W-U_v <= 0, with no fixed credit needed. Finally remove the
leading translation lambda and use its 45 components without target clipping:
the same complete hull assignment proves K<=U for the actual source sumset
2D. This combines holes from both sides in one bound. Source-sum recipes may
neither discard components nor use target endpoints as hull anchors.

Every comparison is independently replayed before its capacity row is added.
Independent set controls passed 1200 capacity checks, including exact equality
in 400 zero-excess cases and rejection of 1200 incomplete inventories. These
controls supplement the general containing-hull proof, not replace it.

Known native components also certify fixed items collectively. Choose a chain
of actual known intervals with nondecreasing right endpoints and each next
left endpoint at most the previous right endpoint plus one. Their union
contains every integer from the first left endpoint through the last right
endpoint. Any fixed form proved between these endpoints is already native;
record it as covered before recomputing fixed credit. This includes the ten
known source points and all leading source-pair points, as well as intervals.
It need not identify a single translate that always contains the fixed form.
The existing positive-covered check still distinguishes negative-group credit.
Independent source controls verified 4,848 such covered fixed items; an empty
chain is rejected by the trace verifier.

## Positive holes and retained predecessors (conditional main domain)

Write W=w/2 in 1..7. Each primitive core has h_v>=z>=2W holes.
The new h=3 synchronous packet adds 41 claims, for ranks15..55; replay uses
exactly the same complete AP-prefix mechanism as the existing profiles.
Together, for W=2..7 and r15..49, the profiles give
mu_(2W-1)(r)=Wr-W(W+7)/2+1. For W=1, non-AP gives mu>=r-3.
Since tau_v=mu_v+h_v, this proves

    tau_v >= W r_v-W(W+3)/2+1,
    tau_s+tau_t >= -W^2+61W+2.

The paired floors for W1..7 are62,120,176,230,282,332,380. A chord on any
integer W interval is a valid linear lower bound because the quadratic is
concave. In a side chord based at lo, the remaining product
(W-lo)*r_v is bounded below with r_s>=15 and r_t>=32. All integer W/rank
values are checked; the exact proof trace first certifies the W interval.

A second bound uses the first gap in the sorted multiset P_s union P_t.
If a complete prefix has p and q elements of the two cores and sum S, the
next coefficient is at least S+2. S>=T_p+T_q, and monotonicity then gives

    tau >= (r_s-p)(T_p+T_q+1-p)
           +(r_t-q)(T_p+T_q+1-q).

The complete finite minimization over prefix counts is64; over nonempty
prefixes it is95-k. Both minima are explicitly checked for every k0..17.
If tau_v<r_v, that core contains1, so the prefix is nonempty. Otherwise
its side mass itself is at least r_v. Combining this dichotomy with
both tau_v>=r_v-1 gives, for any certified k<=b and c=31-b,

    tau >=64,       tau+c*tau_s >=64+c*(32-k),
                   tau+c*tau_t >=64+c*(32+k).

For j>=3, remove the maximum R_v and call the predecessor Y_v. If FS(Y_v)
is complete but FS(P_v) is not, R_v>=sum(Y_v)+2. Thus
 tau_v>=T_(r_v-1)+2-r_v.
Adding the other side's floor r_o-1 and k^2 has minimum352, whereas the
main budget is at most510-73j<352. Hence FS(Y_v) is not complete. Applying
the one-core first-gap argument gives tau(Y_v)>=r_v-2, or

    tau_s-xs >=30-k,        tau_t-xt >=30+k.

At j4 and certified fixed credit e>=38, the budget improves to
I+tau<=218-38=180. Since tau>=64, k<=10 and each rank is22..42.
A nonprimitive Y_v would cost tau(Y_v)>=T_(r_v-1); adding the opposite
floor and k^2 has minimum372>180. Hence both predecessors are primitive.
Their rho is at most cap=180-k^2-(r_o-1). For all21 ranks, the independently
checked endpoint schedule at rank r_v-1 and this cap supplies a central
interval of length at least T_(r_v-1)-2H+1. This exceeds r_v+cap>=R_v;
the minimum verified margin is128. Therefore FS(Y_v) meets every residue
mod R_v. For each residue, adjoining R_v creates a new support value above
its old maximum. At least R_v points are gained, so the number of holes
cannot increase: h(Y_v)>=h(P_v)>=2W.

Apply the same profiles to Y_v. This strengthens the retained floors to

    tau_v-xi_v >= W(r_v-1)-W(W+3)/2+1,
    tau_s+tau_t-xs-xt >= -W^2+59W+2.

The side chords use r_s-1>=21 and r_t-1>=31. The trace requires j4,
positive holes, e>=38 and exact W-range guards. The checks record all21
endpoint witnesses and all restricted side/joint chord evaluations.
These are conditional main-domain lemmas, not a completed structural proof.

## Ordered enlarged interval gaps

The enlarged core hull is C=[-R_o,R_v]. A leading double-core interval is
the union of C translated by its two endpoint offsets -R_o and R_v.
Thus the entire enlarged native cover consists of equal-width C translates,
ordinary exterior singleton points, and leading pairs of exterior points.
Its union agrees exactly with the earlier enlarged cover catalogue.

Certify a complete nondecreasing order z_1,...,z_m of the centres and
z_1+R_v>=1, z_m-R_o<=S_v. Every interval then hits [1,S_v]. The missing
integer count of their union is the sum of positive parts of

    z_1-R_o-1;  z_(i+1)-z_i-R_s-R_t-1;  S_v-z_m-R_v.

For any selected subset of these forms, their sum is a lower bound on
that count, without needing to decide each form's sign. Each remaining
singleton can fill at most one of these positions. Remove a singleton
only after proving it outside the target or inside one enlarged interval.
Including all fixed forms gives a one-side capacity inequality. Combining
both sides and counting only native singletons uses the existing bound
84-e on new fixed values. This yields a joint inequality after subtracting
2W. Being inside an enlarged interval is NOT a fixed-credit certificate.

Exact replay separately verifies the complete centre permutation, its
ordering/target guards, each singleton exclusion, and the selected gap
inventory. Independent controls compare10000 interval families and15000
capacities to explicit integer unions. In240 physical source targets,
the ordered envelope also equals the original enlarged cover exactly.

Retaining holes also strengthens the truncation parameter phi, which is
min_{0<=q<=r}(q+xi_(r-q)), with the empty prefix giving r. For fixed W=1
or2 and fixed credit e>=38, let C=204+2W-e. The actual budget is
k^2+tau<=C. `positive_kernel.py` checks successive removals, separately for
every permitted integer rank. At a proposed prefix n=r-q it verifies:

* Every first gap after a prefix of size at least n has side excess greater
  than C-k^2-floor(r_o,W). Thus this prefix cannot have complete subset sums.
* Each previously removed maximum has deviation at least W. Otherwise the
  beta=W-1 density lemma would give at most2W-2 holes in that preceding
  prefix, contrary to the induction. (For W1, beta0 is just [1,n].)
* The new prefix's excess is at most cap=C-k^2-floor(r_o,W)-qW.
  Since T_n>cap, it is primitive. Its checked endpoint schedule yields a
  central interval at least as long as the full original core maximum.
  Adjoining all removed maxima therefore cannot increase holes.

Consequently that prefix still has at least2W holes and excess at least
floor(n,W)=Wn-W(W+3)/2+1. The last q ordered deviations sum to at least
q*phi-T_(q-1), or to xi+(q-1)*phi-T_(q-1). These yield the two new rows

    tau_v >= floor(r_v-q,W)+q*phi_v-T_(q-1),
    tau_v >= floor(r_v-q,W)+xi_v+(q-1)*phi_v-T_(q-1).

At e38 and k<=10, certified depths are(3,6) for W1 and(6,9) for W2,
with the two coordinates denoting s/t. Tighter proved ranks or greater credit
can allow deeper removal. Replay recomputes every schedule and every rank
license; it does not trust the discovery-selected depth. Independent controls
check the row identities and actual finite core pairs and their predecessors.

A further leading-source witness needs only the core spans. Put
xi=xs+xt and assume xi<=min(r_s,r_t)=32-k. If B is an integer subset of
[0,L] with xi missing positions, a pigeonhole count gives
[2xi,2L-2xi] subset 2B: every target in this range has at least2xi+1
ordered positions in [0,L] whose partners are also in [0,L]. Apply this
first to the full signed core E (translated to start0), then to its
positive and negative halves with0 adjoined. The full-core central interval
is [-2r_t+2xs,2r_s-2xt]; the positive-half interval is[2xs,2r_s], and the
negative-half interval is[-2r_t,-2xt]. The span hypothesis makes these
three intervals meet. Therefore

    [-2r_t,2r_s] subset 2E subset 2D.

The new `dense_core` leading witness checks the span hypothesis and target
membership in this interval before recording any hit or covered fixed item.
It is independent of the selected ordinary-source truncation level, so the
old disjointness rules for exterior preimages still apply.1600 actual core
pairs and412800 witness-guard evaluations independently check this lemma.

## Combined-core hole floors and the w4 closure

The individual profiles lose information: a hole in one core can be filled
by the other. `combined_holes.py` instead merges the two sorted cores and
tracks the exact subset-sum bitset of a short prefix. If the prefix has p/q
items and sum S, and a=r-p,b=s-q items remain, the next merged coefficient
is at most

    floor((C+T_r+T_s-S-T_(a-1)-T_(b-1))/(a+b))

whenever the final total excess is at most C. Otherwise the minimum
completion, with each core increasing by at least1, already exceeds C.
Equal coefficients are allowed only across the two cores and are ordered
s before t, giving a complete disjoint enumeration. The separate minimum
completion after each chosen prefix uses its two actual last coefficients.

When the prefix has at most h holes and contains [H,S-H], propagation is
certified for EVERY later pair of prefix counts. Use S>=T_p+T_q in the
same next-coefficient bound and require S-2H+1 at least that bound. The
central interval and its translate then meet at every subsequent step;
its lower-hole count cannot increase, and symmetry gives at most h holes
at completion. These checks use only integer arithmetic and no LP solver.

The complete checks, which stop after at most7 merged coefficients, prove:
for total rank N=64 (k0..17) and N=62 (k0..10),

    z>=2 implies total excess >=N;
    z>=4 implies total excess >=2N-2.

Both floors are sharp: take each core [2,r+1], or {2} union [4,r+2].
Their combined subset sums have exactly2 or4 holes. For N62 the two
predecessors have a central interval long enough to propagate BOTH removed
maxima, by the already checked predecessor schedules. Thus the combined
predecessor still has at least z holes. On integer W in1..2 this gives

    tau >=62W+2,      tau-xs-xt >=60W+2.

The new rows exactly close the W2 (w4) part of original root (4,142,positive).
W3..7 was already closed by the individual mass profiles. W1 remains open
unless and until a complete exact certificate is recorded. This statement
does not close the original root, or change the global bound81.

The same merged-prefix verifier can apply after q removals from BOTH sides,
when the positive-kernel schedules license that depth. Write N=64-2q and
B=N for W1, B=2N-2 for W2. Then

    tau+qF >= B+65q-q(q-1),
    tau-xs-xt+(q-1)F >= B+65(q-1)-q(q-1).

Every rank-specific combined-prefix obligation is recomputed during exact
replay. The common central interval of the two truncated cores has length
at least R_s+R_t-1, hence all removed maxima propagate without increasing
the combined hole count. These joint rows strengthen the individual
retained-core inequalities; they do not assume holes coincide across sides.

## Shifted known core intervals

For positive holes, tau+k<=94 excludes a nonempty first-gap prefix because
its mass floor is95-k. Thus neither core contains1. Subtract1 from every
coefficient in its maximum-removed prefix. Its rank is r_v-1 and excess is
tau_v-xi_v-(r_v-1). The elementary missing-coefficient bound then proves

    [2, 2r_v-1-tau_v+xi_v] subset P_v without its maximum,

provided the displayed right endpoint is at least2. `shifted_source.py`
uses either this interval or no interval on each side, includes0 and all
ten known maxima/tails, and forms their ordinary translates and all their
leading pair sums. Connected chains of these actual integer intervals can
certify that a fixed item is already native-covered. The positive-hole and
first-gap mass guards, each nonempty prefix, all chain joins, and the final
membership comparisons are checked before increasing fixed credit.

Proof serialization preserves the insertion order of pattern keys. The row
inventory uses that order, so sorting JSON keys can invalidate indexed
certificates even though the resulting dictionaries compare equal. Frontier
v2 hashes and restores order-preserving encodings; its control replays an
actual restored closed certificate, checks idempotency, and rejects an
existing node whose pattern order differs. Older v1 frontier files must be
re-exported from the original checkpoints; their serialization alone was
never evidence of a closed root.
