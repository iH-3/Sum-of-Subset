# Fresh n=85 positive-case prefix lemmas

This file contains the common positive-case notation, the P3 localization and activity classification, and its first-gap4 exclusion. The completed first-gap1/2/3 P3 terminals are in p3_terminal.md. The complete P4 source-seed argument, classifier, and terminals are in p4_fresh.md. There are no open transport branches in these files.

The new structure and source results are proved in inverse/proof85_inverse.md and foundations/source_triple_fringe85.md (paths relative to progress85). Throughout, the source has77 points, its core E has69 labelled points including zero, and the two positive/negative core sizes satisfy a+b=68. Its triangular baseline is1190 and I=(a-34)^2. Put A=I+tau+delta, m0=77j-280-w, T=m0+A, R=R_s+R_t, M=M_s+M_t, and L=M-R. The first two peel offsets on both signs total U; the third offsets total C and the last-minus-third offsets total J, so L=C+J.

The exact source identity and the source envelopes are

- S=2K+1470-77j+w-delta.
- 2K=m0+A+4R+U+2C+J.
- K<=2R+C+166, J+U<=332-m0-A.
- J>=m0+A-18, L>=m0+A-8.
- K-delta>=77j-142-w+I+tau.
- K-M>=R+77j-440-w+A.
- T<=165, equivalently A<=445-77j+w.

The deliberately weaker envelope A<=452-77j+w is used below where it already suffices; it follows from the same source bounds and is not a provisional assertion. Positive-core mu>=62. Use rho>=49 initially, and rho>=58 once both sizes are>=21. The new inverse identities give

- rho+kappa+delta<=456-77j+3z-I.
- U0-C0+delta-2z<=-166-2I-77j.
- V0-C1+delta+2z<=-292-2I-77j-mu-rho.

## P3 localization before a first-gap profile

Here j=3. Initially 1<=z<=14,w<=4z. The weaker source bound gives A<=221+w<=277 and H=tau-mu<=215-I-delta. The integer inequality T_r+(r-34)^2>=397 implies that each core side mass exceeds H, so the core central strip exists.

Its width L0=C0-2H is at least1037+2I+delta. The total U0 of the first two peeled magnitudes on each sign is at most1098-2I-2delta, using C0<=1467 and the inner row. For their four sorted weights, the first three gap terms are<=U0/2<=549. The other three weights at the final gap total at least72+r_min. Since A>=I+mu, r_min>=20. Thus

    L0-(t4-t1-t2-t3)>=1037-1098+2(72+20)=123.

All sixteen inner subset translates overlap. At the outer peel the none/all translates overlap because

    C1-V0-2H>=204+4I+3delta+2z>0,

using mu>=62,rho>=49. Consequently w,z are even, 0<=w<=z<=14, and the two targets have equal hole counts and localized boundary holes.

## P3 finite dense seed and boundary activity

After localization tau<=235, C0<=1425, and r_min>=21. Six absent values in[1,17] force tau>=276, so at least twelve distinct values occur there. The exact finite lemma checked by dense_seed_check.py is:

Every twelve-element subset B of[1,17], with total T_B, satisfies [11,T_B-11] subset FS(B), and its lower half has at most five holes.

The checker covers all C(17,12)=6188 subsets by integer bitset addition. To adjoin the remaining labelled core occurrences, each magnitude is<=47+235=282. For n<=33 selected occurrences, a failed join x>T_B-21 implies x>=58; at least35 remaining entries would give C0>=78+35*58>1425. For n>=34 the selected total is>=306 and x<=282<=T_B-21. Every join succeeds, and hence z<=10. The weaker source bound then gives A<=231, H<=169-I-delta, tau>=62+2z, and delta<=159-z-I.

Five low holes among[1,10] omit five singleton values of sum<=40 and force tau>=5*68+30-80=290. Therefore z<=8. For the terminal first gaps m<=3, four low holes have total<=m+8+9+10<=30 and force tau>=232. The weaker consequence T<=167 of the proved T<=165 gives A<=216+w<=224, excluding this possibility. Thus at m<=3, z,w<=6.

The source row K-delta>=89-w+I+tau proves both leadings active. From H<=169-I-delta and R<=68+tau<=299-I-delta,

    S_v-H-R_o>=T_r+5r-468+2I+2delta>=141+2delta.

Also T_r-R>=98+delta. A target-hole center has at least r_o>=21 distinct positive images under opposite core entries, all within its hull, whereas it has at most w/2<=5 target holes. Nonholes use zero; a center in[1-M_v,0] uses M_v and the complete lower target interval. Every integral center in[1-M_v,S_v] is therefore active, and an empty integral center above an active lower center is HIGH>=S_v+1.

At the first failed greedy inequality, the entries below the gap m total m-1 and generate[0,m-1], while every remaining entry exceeds m. If R_v<=m, that entire side would lie in the prefix, giving C_v<=m-1<R<T_r, impossible. Thus m<min(R_s,R_t); it survives both peels, w>=2, and the target holes are exactly S_v-h for the lower source holes h.

## P3 outer integrality and exhaustive activity forms

Write U_v=own2_v, V_v=own3_v, C_iv=lambda_v-o_(i-3) for4<=i<=7, X_v=v4-M_v, X=X_s+X_t, G=g_s+g_t. The active leadings make lambda_v integral. Each lower coordinate v3 has singleton witnesses U_v,C6_o, and v4 has V_v,C7_o; the eight witnesses are distinct. Two nonintegral lower coordinates require four holes. A sole nonintegral lower coordinate requires its two witnesses and one of H_v,alpha_v missing. If alpha_v is missing, retained O_v,H_v force both top coordinates integral, a contradiction. If H_v is missing, retained O_v,alpha_v and C5_o in A or beta_v in B force v2 and then the lower coordinate integral. A nonintegral top pair would make O_v,H_v,alpha_v and C5_o in A or beta_v in B missing. All eight outer magnitudes are integral.

The branch-independent retained-resource forest rows are

    2X_v+X_o+g_v>=252-tau-delta,
    2X_v+X_o+G>=305-tau-delta,
    2X+4R+delta>=548.

The two candidate arms are leading_v--V_v--U_v and leading_o--C7_o--C6_o, both with gaps X_v,g_v. At most one vertex of one arm is empty. Restrict core translates using trim3 for the first row and trim4 for the second. Positive and negative restricted arms on one target are disjoint since M>R. Inside a target every vertex at a point is retained; outside it at most one is empty. Thus edge counts are bounded by retained-resource union deficiency, with each full leading capacity counted once. Four full-core stars give the third row.

The following five assertions exhaust the activity restrictions:

1. O_v,C6_v cannot both be active.
2. O_s,O_t cannot both be active.
3. beta_v,H_v,C6_v cannot all be active.
4. Active C5_v implies active C6_v.
5. beta_v,O_v,C7_v cannot all be active.

For1 and3, actual C6_v activity gives d_v-M>=306-tau-delta>=85-w+I; O_v activity or beta_v,H_v activity gives a raw cap<=27, impossible. For5 the lower bound is253-tau-delta>=32-w+I, exceeding the double cap<=16. These conservative raw caps follow from the proved O22+eta, beta/H21+eta, and double27/2+eta/2 counts with w<=10. For2, with Y=2M-2K+44+w+delta, the high-tail count565 and star count548 yield189+4I+4tau+delta<=6w<=60, impossible. For4, active C5_v and empty C6_v make C6_v HIGH. The leading then loses all77 points of lambda_v+D_v, and at least three retained higher singletons among C7,V,U,H,O each lose r_v+5. This forces delta>=92+3r_v, but delta<=169-I and min_r(I+3r)=100 give a contradiction.

The literal owner identities, with W=v3+v4+o3+o4>2M, are

    C4_s+C4_t=-(s2+s3+s4+t2+t3+t4),
    beta_s+beta_t+C5_s+C5_t=-2W,
    C4_v+beta_v+C5_o=-2v3-2v4-o2-o3-o4,
    C4_v+C5_o=-(beta_s+beta_t)-2W-d_o.

Comparison with the actual lower activity endpoint1-M_v proves that retained pair1 has a sole owner, the displayed triple cannot be active, and the two retained B pairs have matching sole owners.

To exhaust whole-unit holes, at least one O is missing by2. If both are missing, neither C6 can be the third A hole, because4 would also delete its C5 singleton. Both C6 are retained. An empty beta pair gives A0. Otherwise3 forces H missing on the active beta's side; the opposite beta is inactive and owner grammar puts pair1 on the opposite side, giving A1. In B, both O missing would require one further hole in each disjoint triple{beta_v,H_v,C6_v}, exceeding three holes.

If just O_o is missing, active O_v forces empty C6_v and C5_v by1 and4. In A these are all three holes: the beta owner is v and pair1 owner o; active beta_v,O_v,C7_v contradict5. In B the holes are{O_v,C6_o,Z} with Z in{beta_v,H_v,C6_v}; pair owners are v, and4 excludes Z=C6_v. In either remaining choice beta_o,O_o,C7_o are active, contradict5. Exactly these two forms remain:

| form | whole-unit holes | actual owners |
|---|---|---|
|A0|beta pair,O_s,O_t|pair1 sole owner s or t|
|A1|O_s,O_t,H_v|beta sole owner v, pair1 sole owner o|

All unlisted whole units are retained. The fixed HIGH/LOW label counts give credits8 for A0 and11 for A1; the terminal proofs retain their exact native/grouped deficiencies.

## P3 first-gap profiles and the gap4 exclusion

The first-gap5 low multiset must be{1,1,2}. If k is the side containing1,2, its profiles are(1,2,6,...,k+3) and(1,6,...,q+4), q=68-k. Therefore

    I+tau>=228+(k-34)(k-35)>=228>A<=224.

For m6, the total count below m is<=3, giving tau>=4(68-3)=260. The dense seed puts every lower hole in[1,10], so the first gap satisfies m<=10. Thus T_(k_v)<=m-1<=9 gives k_v<=3. For7<=m<=10, each side floor (m-k_v)(r_v-k_v) is at least4(r_v-3), yielding tau>=4(68-6)=248, again impossible. Hence m<=4.

At m4 the low multiset is{1,2}, either split or together. The minimal I+tau is199+chi+sigma, with chi=I if split and chi=(k-35)^2 if k is the together side. A value x in[5,12] absent from both cores adds at least76-2x>=52 to the baseline, exceeding even the weaker true-excess cap32. Hence the actual seed{1,2,5,...,12} is present; it has exactly the hole4 and its reflection. Every remaining magnitude is<=83. While selected total is below92, a failed join x>T_B-9 implies x>=63 and at least54 remaining occurrences would force mass>1425; once T_B>=92, x<=83<=T_B-9. All joins succeed, so z=w=2. The weaker T<=167 cap gives chi+sigma+delta<=19; below we retain the still weaker24, since it already suffices. Charged endpoints are normal because delta<=24<r_min+5.

In A0 let s be sole pair1 owner. The identity H_s=P+alpha_s+alpha_t+d_t+2V+G gives S_s>=d_t+2V+G+155-E. The opposite leading and K<=M+R+21 give

    S_t+M+(2X+G)+(2X_t+g_t)<=R+1105+w-e.

The six- and three-edge forests use f=(146-sigma+R)/4 and yield

    S_t+M+5R/4-9sigma/4-2delta+3e<=1553/2+w.

The physical baseline tau_t>=2r_t-4, R_t>=r_t+2 gives S_t+M>=T_r+6r+R+L+14. With R>=74, L>=142-w+chi+sigma+delta, and chi+sigma+delta<=24,

    T_r+6r+9chi/4+3e<=488.

As a function of physical r, chi is(r-34)^2 in the split placement and(r-35)^2 or(r-33)^2 in the together placements. All three integer quadratic minima exceed600, contradicting488.

In A1 let s be beta owner and t pair1 owner. Normal endpoints at beta_s,P_t,V_t give S_s+3g_s+4X_s+2s4+t4<=1089+w+r_s+delta-2e. Source mass, the ordinary gap pair and stars imply

    T_r+6r+chi+sigma/4+283/2-2w+2e<=21R/4+9epsilon/2.

The profile radial estimate is2R+chi+delta<=178+w, derived from K<=C+2B+174+sigma with B74 and J>=A-67-w. Using w2 and chi+sigma+delta<=24 yields

    T_r+6r+11chi/2+17sigma/8+13e/2<=380.

Each physical orientation has a larger global integer quadratic minimum. Thus m4 is excluded in both forms. Together with the complete first-gap1/2/3 proof in p3_terminal.md, this excludes P3.

## P4 proof reference

p4_fresh.md contains the full seven-seed availability and propagation proof, all six resulting profiles, the exact CORE8 classifier, and every terminal card. check_p4_cards.py checks the stated exact seed supports, propagation mass bounds, fixed-label incidence ledger, adaptive scalar combinations, integer quadratics, and terminal arithmetic.
