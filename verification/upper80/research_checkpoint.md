# Size-81 research checkpoint, 2026-10-23

**No global bound 80 is certified yet.** Main remains 71 <= N <= 81. This file
records new mathematics and arithmetic to be integrated into a complete proof,
only after all finite cases close and the interfaces below have been audited.

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
