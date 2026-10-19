# Fresh geometric derivations for Z3/Z4 terminal cards

These are local terminals, assuming the actual retention forms and
common integral source. The classifiers in positive.md, z5.md and check_geometry.py provide
the actual retention predicates separately from these scalar terminals.

## Z3 A0

S=2K+1224-delta, A<=228, L>=A-76,
max(4,A-156)<=e_v<=393-A. The five weighted endpoints are
P_s,2alpha_s,alpha_t,C5_t,H_s. Their literal identity is
H_s=P_s+2alpha_s+alpha_t+C5_t+4(M+X)+2G.
The endpoint constant is5*72+71-3*67=230. The residual physical
source mass is at least T_r+4r+tau_t+4xi_t+10. With K<=M+R+21
and the six-edge retained forest, the exact master is

    T_r+4r+tau_t+2L+4xi_t+12F<=1026-2e+delta+B_*.

The common grouping rebates every endpoint's unused native loss
except the algebraically doubled alpha_s. Consequently
B_*=2b_alpha_s+sum_(other heavy Z)(b_Z-k_Z).
Call other endpoints heavy at clip70; alpha_s's flag a is reserved
for a peeled clip>=72. If a=0 its error<=xi_s. All other light
errors satisfy b<=k: outside-hull clips have24<=k<=69, and
k(73-k)>=276>220>=tau+k. The next-rank inequality
(72-k)b<=tau proves the claim. Normal endpoints have error0.
Every heavy error is at most xi_v+e_v-4, including core ranks70,71.
When a=1, alpha_s<=0 and the eleven LOW labels
U5:8_s,V5:8_s,F3:5_s touch nine groups. With the eight O HIGHs,
this gives compatible e10. Otherwise use e8.

Thus with n_s in{0,1}, n_t in{0,1,2,3},

    B_*<=2xi_s+(2a+n_s)(e_s-4)+n_t(e_t-4)
          +n_s xi_s+n_t xi_t-70(n_s+n_t),
    delta>=e+72a+70(n_s+n_t).

These are precisely the twelve scalar systems exhaustively checked
by the full-rank verifier, with minimum margin65. The actual five
resources and the six-edge forest have been specified; no additional
capacity is assigned to an inactive component.

## Z3 A1

The actual holes are O_s,O_t,H_s; beta_s and P_t are sole resources.
The same twelve HIGH labels as in the former physical-union proof
give e12. Group leading s and its seven native resources:
S_s>=K+532-eps. Lower P_t and upper H_t are the only endpoints.
Let B=Gamma_Pt+Gamma_beta_s and H=Gamma_Ht<=75.
The ten-edge forest and the two X_s star edges give, on one Q,
Qgap+X_s>=6F-eps+B+H/2. The identity
H_t=H_s+P_t+2s4+t4+g_s+g_t+h_t and HIGH H_s imply
S_t>=S_s+M+M_s+Qgap+X_s+77-Eclip-Eerr.
As Eclip<=B+H, the source sum1224 gives exactly

    M+M_s+6F-H/2<=47+2delta+Eerr.

The four endpoint flags p,h have
Eerr<=xi_s+xi_t+p(e_t-4)+h(e_s-4). Define
Z=r_s+2I+2tau+xi_s+6F-H/2. The source peel bounds give, respectively,
Z<=212,288,A+52<=280,A+128<=356.
But2tau+6F>=396, r_s+2I>=33 and H<=75 give Z>=783/2=391.5.
All endpoint positions are excluded with margin at least71/2.

## Z4 physical capacities and masters

S=2K+1148-delta, A<=152, L>=A,
max(4,A-80)<=e_v<=317-A. The generic rank constants are72-r_v
and S_v+r_o-71. A native clip<72 has error<=xi_v; a heavier
one has error<=xi_v+e_v-4 and costs at least72. All heavy flags
allowed by e+72h<=152 must be included, in particular two flags
when e8. No unproved assertion that at most one is heavy is used.

The original endpoint/forest lists for F,S,EH,EA-own,EA-opp,EC5
are retained literally. Physical t with seven native resources gives
S_s<=K+616-e; six gives S_s<=K+692-e. These are union-deficiency
bounds, not claims that their images are disjoint. Direct substitution
of the endpoint identities gives these fresh masters (E is the
actual weighted error, N the listed endpoints' native loss):

* F: T_r+4r+tau_t+2L+4xi_t+12F<=950+delta-2e+E.
  The nominal constant is230. The six-edge forest avoids all five
  endpoints and Eclip<=2N. There may be one empty ordinary vertex,
  charged by the separated-arm one-empty rule, with zero capacity.
* S: 2M+9F+4e+2N<=539+3delta+E. Nominal constant153;
  physical t has six resources. The leading-t, six-edge and
  three-edge forest budgets rebate all four endpoints.
* EH: R+2L+xi_t+e_t+10F+3e+N-h<=412+2delta+E,
  where h is the upper V_s deficiency. Nominal constant225-r_t;
  physical t has seven resources. The six-edge forest avoids all
  endpoints, while the four stars contain V_s only. Drop N-h>=0.
* EA-own: L+2e_t+2xi_t+10F+3e+N<=415+2delta+E.
  Use alpha_s>=1-a and physical t's seven resources. All four
  endpoints avoid both the eight-edge and two-star systems.
* EA-opp: R+2L+xi_s+e_s+11F+3e<=487+2delta+E.
  Use alpha_t>=1-b; nominal constant159+r_t; physical t has six
  resources. The six-/five-edge forests avoid all weighted endpoints.
* EC5: R+2L+xi_t+e_t+11F+3e+N<=488+2delta+E.
  Nominal constant225-r_t; physical t has six resources. Its
  seven-/four-edge forests avoid the five endpoints.

Subtract baseline rank errors and each actual heavy increment e_v-4.
Use N>=72h where it occurs. The resulting systems are exactly the
six first Z4 cards in the full-rank verifier. Their margins are
306,81,253,163,204,295.

## Z4 O: deriving the previously conditional constant994

Its predicate is both O and H_s empty, beta_s native and P_t sole,
all eight lower own/cross resources retained. The twelve HIGH labels
give e12. Put B=Gamma_beta_s+Gamma_Pt, H=Gamma_Vt. The actual
three forest rows are

    X_s+g_s>=2F-(eps-B-H)/2,
    X_s>=F-(eps-B-H)/2,
    X_s+X_t>=2F-(eps-B)/2.

Three, two and one copies give
6X_s+X_t+3g_s>=10F-3eps+3B+5H/2.
The endpoint identity V_t=2d_s+beta_s+P_t+2a+b+g_s, with twice
leading s, has Eclip+2ell_s<=2eps-(B+H). Consequently

    S_s+3g_s+4X_s+2a+b
    <=1000+r_s+delta-2e-B-H+Eerr.

Insert S_s>=T_r+tau_s+4R_s+6+e_s and the forest row. This yields

    T_r+4r+5xi_s+tau_s+R+L+2e_s+10F+60+4B+7H/2
    <=994+4delta+Eerr.

Thus994 is derived from the actual physical resources, rather than
extrapolated from1006. Baseline Eerr<=2xi_s+xi_t. A heavy beta_s
or P_t costs4*72=288, a heavy upper V_t costs(7/2)*72=252;
subtract its source e_v-4. This is exactly the seventh full-rank
Z4 system, with verified margin123.

The exact ownerless family, to which none of these cards applies,
has its separate proof in z4_ownerless.md. The preceding activity lemmas and the independent component census supply
the exhaustive size84 classification; terminal arithmetic alone would not do so.
