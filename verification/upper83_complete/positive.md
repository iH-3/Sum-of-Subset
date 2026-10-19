# Positive-hole activity and terminal proofs

Common integral primitive source and 1<=z<=14 are supplied by structure.md.
The uniform localization in localization_p12.md gives even w<=z<=14
and eta_v=w/2 for every j>=1. The exact finite replays are in
check_positive.py. P0 is excluded by the unlocalized no-empty bound;
positive j>=6 is impossible from A<=w<=56<tau.

## One dense seed and a ternary prefix census

After localization and j>=3, A<=242, C0<=1398, r_min>=21, and each
core entry<=276. Six values missing from both sides in[1,17] cost
tau>=6*67+42-2*(12+13+14+15+16+17)=270>242. Thus at least twelve
distinct values occur there. The retained exact6188-seed lemma gives
[11,T_B-11] in FS(B) and at most five lower holes. Adjoin the other
labelled core occurrences in sorted order. For a current n>=34,
its total is at least2T17=306, so x<=276<=T-21. For n<=33 a
failed join x>T-21 implies x>=58 and at least34 remaining entries, forcing C0>=78+34*58=2050>1398. Thus every join succeeds and all
lower holes are in[1,10].

The exact59049-pattern census enumerates multiplicities0,1,2 at
1,...,10, then fills the remaining67-count slots from11 upwards,
at multiplicity at most2. It rigorously lower-bounds I+tau without
requiring an assignment to physical sides. Four lower holes cost
at least256; three cost at least195; the first gap2 costs at least99.
Consequently:

* j3: z<=6, w<=6, A<=234.
* j4: z<=4, w<=4, A<=156; possible lower-hole sets are precisely
  a subset of { {1}, {1,2}, {1,3}, {2}, {3} }.
* j5: the only lower hole is1. Hence z=w=2, all positive core
  entries omit1, tau=67+sigma, and I+sigma+delta<=11.

For j4, tau-xi>=65. At first gap1 every rank deviation is>=1, so
removing the two maxima leaves at least65 mass. At first gap2 the
low multiset is {1}; the other entries exceed2, giving an even
larger bound. At first gap3 it is {1,1}; the remaining entries
exceed3, again giving at least65. This proves the bound directly
for every listed profile.

## Activity interval (j>=3)

The bounds above give
S_v-H-R_o>=T_r+5r-480+2I+2delta>=113+2delta.
Also S_v-H-M_v>0 from the source side mass. A target-hole centre
in[S_v-H,S_v] has at least r_o>=21 distinct opposite-core images
strictly inside the target hull, more than eta_v<=7 holes. Thus it
is active. Other centres in[1,S_v] use zero, and centres in
[1-M_v,0] use M_v in the complete lower target strip. Therefore
every integral centre in[1-M_v,S_v] is active. An empty centre
above an active one is HIGH>S_v. This supplies the positive-case
activity rules used by the zero-case classifiers without assuming
complete targets.

## Fresh two-cap identity and j3/j4 grammar

The four-top tail has at most4*(76+6)+5=333 values per sign:
d_s+d_t+G+delta-2K>=786-76j. The four full-core stars give
2X+4R+delta>=540. With both caps t_v<=12+eta_v, put
Y=2M-2K+24+w+delta. Then G+2X<=Y, G>=786-76j-Y, and
Y<=932-152j+3w-2R-2I-2tau-delta. Hence, whenever the stars are
licensed,

    4I+4tau+delta+228j<=538+6w.

This excludes j3 for w<=6. For j4, before integrality or the stars,
the first two inequalities give2Y>482, but Y<=190+3w<=202, so
two cap predicates are already impossible.

The cardinality-independent residue classifier in Appendix D now
works with fresh strict arm bounds. For j3 the two-witness argument
immediately gives integrality. For j4, two nonintegral lower
coordinates use four holes and leave both O active. With just one
nonintegral lower coordinate of residue theta and top residue b,
the five residues H,O,alpha,beta,C5_opposite are
b,b+theta,b-theta,b-2theta,-b. If b!=0 the actual branch-A/B
hole counts again leave both O active. If b=0 the exact holes are
the two witnesses,O_v,alpha_v. The original four integral-gap
aggregate edges give at least248-tau-delta>=96-w>=92; either
active opposite O,C6 or beta,O,C7 contradicts caps<=14. A
nonintegral top pair after lower integrality costs four holes and
the five-edge bound300-tau-delta>=148-w>=144 contradicts the
retained opposite O,C6. Thus all outer coordinates are integral.

The separated-arm pointwise rule allows one empty vertex per arm
with zero capacity; failure to find an arm at j4 is exactly the
four-hole witness configuration already excluded. Therefore active
C6 forces t>=301-tau-delta, and active C7 forces
t>=249-tau-delta. At j3,w<=6 these are at least67 and15;
at j4,w<=4 they are at least145 and93. They exclude O/C6,
beta/H/C6 and beta/O/C7 simultaneous activity.

A HIGH cross makes leading loss at least r_v+80. At j3, empty
C6 above active C5 leaves at least three higher native resources,
each losing r_v+5. The ten positive-positive fixed labels are HIGH
and compatible with all baseline groups. Thus A>=I+4r+105>=235,
contradicting A<=234. At j4 the C4=>C5 and C5=>C6 implications
have A>=I+3r+90>=188>156. C6=>C7 uses one higher resource
and the ten HIGH labels: A>=I+2r+95>=161>156.

The literal owner identities and hole counts therefore give the
same complete j3 A0/A1 and j4 A-E/A-H/B tables as Appendix D.
For j4's beta/O exclusion, the three-edge rooted arm when V_v is
retained gives t>=119-w+I+xi; if V_v is missing, its HIGH status
and three unused higher native losses give t>=68-w+I+3r_v.
Both exceed the sharp double cap. Consequently both O are holes.
The remaining two-beta-hole B alternative has necessary row
2T_r+9r+4I+7tau/4+2tau_v<=1104+4w<=1120, while its integer
quadratic minimum is1160. It follows from the actual HIGH-beta
master2S_v+K+3g_v+6X_v<=M_o+1147+w+delta and the three-edge
bound186-3tau/4-delta. The owner-side HIGH beta contradicts
2d_v<=M_o-1 and actual P activity d_v>M. Thus neither extra
beta-hole alternative is omitted.

## j3 terminal bridge

The A0 geometric master in z34_cards.md only changes1026 to1026+w.
Use the relaxed common domain A<=234, L>=max(8,A-82),
max(4,A-162)<=e_v<=399-A, and keep the heavy thresholds70/72.
The light-rank product276 still exceeds tau+eps<=226.
The exact twelve minima at w6 are
162,224,285,330,126,266,422,88,158,313,41,220, all positive.

For A1, the same actual side-union argument gives47+w in place
of47. Its four Z upper bounds become212+3w,288+3w,
A+52+2w,A+128+2w. Their largest value is374, below
Z>=391.5. Thus all j3 positive-hole forms are excluded without
individual first-gap terminal cards.

## j4 terminal bridge

Each of the seven Z4 actual masters in z34_cards.md gains at most w
on its right. Use A<=156, L>=max(8,A-4),
max(4,A-84)<=e_v<=321-A. Include every heavy flag allowed by
e+72h<=156 (even two in Card O if needed). The seven finite minima
are290,65,237,151,164,283,103, all positive.

For the exact ownerless family use z4_ownerless.md with target
hole allowances. The initial four-arm bound is116+I-w; hence
X+g_v>=57. Use the stronger active-C5 identity to obtain
d_v-h_v-X_v>=X+G+h_o-55-eta_v>0 even at w4. Thus the ten-label
gap yields h_v<=M+11+eta_v. The same e18 ledger works:
V2_s+V2_t<=20+w-3X-G<0. The core gap has at most30+eta_v
positions, so h_v<=R+31+eta_v with a core hit, or
h_v<=R_v+M_o+30+eta_v otherwise.
Both H core-hit, light alphas imply xi>=94+I-2w>=86+I.
But the positive profile has tau-xi>=65 and tau<=134+w-I<=138-I,
contradiction. One heavy alpha gives100+2I<=3w<=12.
One H with no core hit gives tau>=19+u+I-2w>=83+I, while
delta>=90 gives tau<=66-I. Two non-core-hit H losses144 exceed
eps<=138. Thus the ownerless positive family is excluded as well.

## j5 complete terminal

The prefix census leaves just lower hole1. Thus z=w=2,
tau=67+sigma and I+sigma+delta<=11. All core entries omit1:
xi_s=1+xi'_s,xi_t=1+xi'_t,xi'_s+xi'_t<=sigma. In particular
r_s,r_t are between31 and36. Before outer integrality,
K-M-delta>=R-76+I+tau>=58. The leading inequality rules out
active O and active beta/H because their raw caps are13 and10.
The residue argument and literal owner identities of z5.md now
apply. A HIGH cross loses r_v+80>delta leading points, supplying
the same cross chains. Both O provide fixed credit8. Every retained
singleton or actual sole pair is normal: a BAD centre loses at
least72-max(r_s,r_t)>=36, while eps<=3. In particular all own
chains and actual endpoint lists are licensed.

The source rows are freshly

    S=2K+1074-delta, A=I+67+sigma+delta<=78,
    L>=A+74, max(4,A-6)<=e_v<=243-A.

Do not import the zero-hole strengthened bound L>=A+78.
Use the actual full core q=68,F=68-xi_s-xi_t>=63.
For A0 with empty P, the fixed ledgers for H/C5 extras have
credit13 and the alpha extra has credit14, each exceedingdelta11.
Split beta has both H HIGH and credit14, also impossible.

For A1 with empty P, the shared HIGH11 ledger from O_s,O_t,H_s
combines with these18 LOW labels:
C55,C56,C57,C58 on both signs; V5,V6,V7,V8 on the inactive-beta
sign t; F3,F4,F5 on both signs. They touch17 baseline groups, so
credit=11+18-17=12>delta. Pair1 is LOW, since a HIGH component
would lose r_v+80>delta leading points. Beta_t is LOW because one
of H_t,alpha_t is retained and normal. The F signs follow from
d_v>g_v. These signs hold for every possible final companion hole.
No inactive paired component is assigned native capacity.

Retained-P A0 uses the same eleven exact affine cards as z5.md,
with normal endpoint errors zero. Their full-core minima, in A--K
order, are608,452,723,428,344,504,504,307,515,597,504.
Card E uses credit11 from HIGH H_t; others usecredit8. Card D
uses both actual triples on this same full core, giving5q+6F.
For remaining A1/B, use opposite/same/four-endpoint/branch-B
physical masters from z5.md with their right side increased by2.
Even retaining their old nonnegative xi error allowances and
omitting the nonnegative side-mass terms, the minima are
761,326,501,461. check_positive.py enumerates the entire integer
domain I+sigma+delta<=11,xi_v>=1,xi_s+xi_t<=2+sigma and the
full peel polygon. This closes every P5 form.
