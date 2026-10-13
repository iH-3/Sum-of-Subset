# n=85 P3 terminal exclusions using the fresh universal source cap

This proof uses the new structure and the weaker consequence T=m0+A<=167 of the proved universal source theorem T<=165, where m0=-49-w and A=I+tau+delta. Thus

    A<=216+w.

The source is77 points, the core69 labelled points including zero, and a+b=68. The baseline I is(a-34)^2. Source mass is S=2K+1239+w-delta, and full-source central-fringe bound K<=M+R+21. The exact source offset bound is L>=A-57-w.

The localization/classification in `fresh_positive_notes.md` supplies the two forms A0 and A1. The dense seed lemma first gives z<=10. Five low holes among[1,10] would avoid five values of sum at most40, forcing tau>=5*68+30-80=290, impossible. Hence z<=8. For a first gap m<=3, four low holes include m and have total at most m+8+9+10<=30. They force tau>=4*68+20-60=232, whereas A<=224. Therefore z<=6, w<=6.

At m=5, the profile I+tau>=228 contradicts A<=224. At m>=6 the generic low-rank floor also contradicts the cap. At m=4 the seed lemma gives z=w=2 and sigma+delta+chi<=19 (the former notes used the weaker24); the separate normal-endpoint m=4 exclusions in the notes apply unchanged. It remains to treat m=1,2,3.

## Profile and endpoint constants

In the following table sigma is excess over the displayed minimal profile and B the sum of baseline maxima. Q61 is obtained by deleting four largest core magnitudes on each side.

| m | I+tau | B | 4f | L lower bound | mass cap |
|---|---|---|---|---|---|
|1|68+I+sigma|70|166-sigma+R|11-w+I+sigma+delta|sigma+delta+I<=148+w|
|2|101+chi+sigma|71|161-sigma+R|44-w+chi+sigma+delta|sigma+delta+chi<=115+w|
|3|132+I+sigma|72|156-sigma+R|75-w+I+sigma+delta|sigma+delta+I<=84+w|

For m=2, k is the physical unique-1 owner's size and chi=(k-34)(k-35)>=0. It need not equal the paired-resource owner. If that physical owner is side s then k=r_s; otherwise k=68-r_s.

For a native retained ordinary/sole-pair center Z on target v the nominal endpoint rows are

    Z>=73-r_v-l_Z-A_Z,
    Z<=S_v+r_o-72+h_Z+D_Z.

Normal endpoints use zero error. Write c for the selected lower or upper clipping count. An outside lower endpoint has c=73-r_v+j, with the next positive core rank j+1 if c<73; reflection gives the same upper argument. If its baseline displacement is d, then

    (73-c)d<=sigma_v.

The baseline endpoint error is at most b+d, where b=1 at m1 and b=2 at m2,m3. For a light c<73, the licensed sigma+epsilon bound gives d<=c. For c<=71 this follows from c(74-c)>=213 on the relevant interval26..71, and sigma+epsilon<=146; smaller actual side lower bounds only strengthen it. For c=72:

- A1 uses credit11, so sigma+epsilon<=148+6-11=143 at m1; the other profiles have still smaller caps.
- A0 m1 with z2 has sigma+epsilon<=142. With z4 it is<=144. With z6, the two additional low holes imply tau>=176 and delta<=46, so c72 cannot occur. A0 m2,m3 again have smaller caps.

Thus every light error is at most b+c<=b+Gamma_Z.

For a heavy c>=73, at most one relevant selected resource is heavy. In A1 epsilon<=143 at m1, and <=110,79 at m2,m3, so two73 clips are impossible. In A0, m2/m3 also have epsilon<146. At m1, z2 gives epsilon<=142; z4 implies tau>=120, delta<=100, epsilon<=92; z6 gives epsilon<=38. Thus again two73 clips are impossible.

The heavy next source magnitude is peeled. Its endpoint error is at most b+sigma_v+e_v, where e_v is the fourth peeled offset on the physical source side providing that next magnitude. This deliberately loose bound is used in A0. For A1, activity bounds the error by M_v-r_v+72-c<=M_v-r_v-1. The profile maxima are r_v+1 at m1 and at most r_v+2 at m2,m3, so the sharper heavy error is at most e_v+sigma_v+b-1. Together with the other two light errors, this is the stated aggregate3b-1 below. The native deficiency of a heavy resource is at least73, and delta>=e+c.

## A0: physical-target capacity replaces the old total-mass transport

Let s be the actual sole pair1 owner, and e=8, epsilon=delta-e. The original unit holes are beta-pair,O_s,O_t. Target t receives exactly its leading and seven retained ordinary resources H,U,V,C5,C6,C7,alpha, with capacity K+539. Their grouping gives

    |F_t|>=K+539-epsilon,
    |F_s|<=K+700-e,
    S_s<=K+700-e+w/2.

The literal identity is

    H_s=P+2alpha_s+alpha_t+C5_t+4M+4X+2G.

Use endpoint resources P,alpha_s,alpha_t,C5_t,H_s with clipping/error weights1,2,1,1,1. Their nominal lower/upper constants give

    S_s>=233+4M+4X+2G-E_clip-B_err.

On each target v the retained tree is leading_v--V_v--U_v, with the extra edge leading_v--C7_v. Its three gaps are X_v,g_v,X_o. For the positive edge restrict the full leading to lambda_v+M_v+Q_v; for the negative edge use lambda_v-M_o+Q_v, where Q_s=Q61 and Q_t=-Q61. Ordinary vertices are restricted to their matching Q_v translates. Each edge contributes at least f minus its gap. Both restricted copies remain subsets of one full leading capacity K. Across the two targets these six edges have total gap2X+G, so their grouped deficiency satisfies D_F>=6f-(2X+G). They are disjoint from the five endpoint resources, and E_clip+2D_F<=2epsilon. Combining the last three displays with K<=M+R+21 yields the master inequality

    3M+12f+3e<=R+488+w/2+2delta+B_err.

All target holes are already in these native/grouped deficiencies.

Let l,D,Mcap,chi0,b be the following constants:

| m | l | D=3(4f constant)-488 | Mcap | chi0 | b |
|---|---|---|---|---|---|
|1|11|10|148|I|1|
|2|44|-5|115|chi|2|
|3|75|-20|84|I|2|

The master uses M>=R+L, L>=l-w+chi0+sigma+delta, and R>=70,71,72 respectively.

If every endpoint is light, B_err<=6b+2epsilon. Direct substitution forces

    5R+4chi0+sigma+5e <= Mcap+6b-3l-D+(9/2)w.

The maximum right sides are138,27,-82 respectively; the left side is at least350+40,355+40,360+40. Thus no all-light case survives.

If there is one heavy endpoint of weight q in{1,2}, then

    B_err<=6b+2epsilon-qc+q sigma+q e_v.

Cancel q e_v against qL and use the mass cap. The exact terminal row is

    5R+(3+q)chi0+(q-1)delta+5e+qc+(3-q)l+D-6b
        <=2q Mcap+(7/2+q)w.

For m1 a heavy forces w<=4. For q1, left>=489 and right<=314. For q2, delta>=e+c>=81 gives left>=632 and right<=614. For m2 the q1/q2 left floors are539,649 and right ceilings257,493. For m3 they are591,670 and ceilings195,369. All are strict contradictions. Hence all A0 first gaps are excluded.

## A1: the same ten-edge forest applies to all three profiles

Let s be physical beta owner, t actual pair1 owner, r=r_s, e=11 and epsilon=delta-e. Reserve b_*=Gamma_beta_s+Gamma_P_t and h_*=Gamma_H_t.

The ten-edge forest consists of these retained arms:

    on s: leading_s--V_s--U_s;
          leading_s--C7_s--C6_s--C5_s;
    on t: leading_t--V_t--U_t--H_t;
          leading_t--C7_t--C6_t.

Its literal edge inventory is:

| target | edge | gap |
|---|---|---|
|s|leading_s,V_s|X_s|
|s|V_s,U_s|g_s|
|s|leading_s,C7_s|X_t|
|s|C7_s,C6_s|g_t|
|s|C6_s,C5_s|h_t|
|t|leading_t,V_t|X_t|
|t|V_t,U_t|g_t|
|t|U_t,H_t|h_t|
|t|leading_t,C7_t|X_s|
|t|C7_t,C6_t|g_s|

Their gaps total2X_s+2X_t+2g_s+2g_t+2h_t. Restricted positive and negative hub copies are lambda_v+M_v+Q_v and lambda_v-M_o+Q_v; each stays inside the same full leading vertex. Ordinary vertices use Q_v translates. Omitting both paired resources leaves deficit at most epsilon-b_*, and hence

    X_s+X_t+g_s+g_t+h_t>=5f-(epsilon-b_*)/2.

The four-edge subforest uses leading_s--V_s--U_s and leading_t--C7_t--C6_t. It omits both pairs and H_t, so

    X_s+g_s>=2f-(epsilon-b_*-h_*)/2.

The two stars leading_s--V_s and leading_t--C7_t use the full core E69, whose span is R, and give

    X_s>=137-R-(epsilon-b_*-h_*)/2.

Add the ten-edge row, twice the four-edge row and three times the two-star row. The resulting positive scalar combination gives

    W=6X_s+X_t+3g_s+g_t+h_t
      >=9f+411-3R-3epsilon+3b_*+(5/2)h_*.

The center identity H_t=2d_s+beta_s+P_t+2s4+t4+g_s+g_t+h_t and its three endpoint rows, followed by the leading-s bound twice, give

    S_s+3g_s+4X_s+2s4+t4+g_t+h_t
      <=1089+w+r+delta-2e+E_err.

All-light E_err<=3b+b_*+h_*. One-heavy E_err<=e_u+sigma_u+(3b-1)+G_light, and

    3b_*+(5/2)h_*-G_light>=365/2,
    L-e_u>=4, sigma_s-sigma_u>=-sigma.

The physical source lower rows are exactly Tr+6r+19 at m1, Tr+6r+18 for m2,k=r, Tr+7r+24 for m2,k=68-r, and Tr+7r+22 at m3, plus sigma_s+R+L+6X_s+X_t. Hence the resulting scalar right constants are571/2,1191/4,1167/4,305 respectively, in the shared form

    Tr+c_r r+sigma_s-9sigma/4+R/4+L+5e+3b_*+5h_*/2
      <=constant+w+4delta+E_err,

with c_r=5,5,6,6 respectively.

### m1

All-light substitution gives

    Tr+5r+4I+7sigma/4+sigma_s+R/4+5e<=1443/2+5w.

For integer r, Tr+5r+4(r-34)^2>=679. R>=70 and5e55 give a left floor1503/2=751.5. For w<=4 the right is<=741.5. If w6, three low holes include1 and force tau>=176, so sigma>=108 and the left is strictly larger than751.5, whereas the right is at most751.5.

One-heavy gives

    Tr+5r+4I+3sigma/4+R/4+5e<=693+5w<=723,

contradicting the same left floor751.5.

### m2: both physical unique-1 owners

If k=r, all-light gives

    Tr+4r+I+3(r-34)(r-35)+7sigma/4+sigma_s+R/4+5e
      <=2283/4+5w<=2403/4.

Its quadratic part is at least661. If k=68-r the corresponding row is

    Tr+7r+I+3(r-34)(r-33)+7sigma/4+sigma_s+R/4+5e
      <=2531/4+5w<=2651/4,

whose quadratic part is at least723. Both contradict even without the other positive terms.

One-heavy gives the two rows

    Tr+5r+4(r-34)(r-35)+3sigma/4+R/4+5e<=2305/4+5w<=2425/4,
    Tr+6r+4(r-34)(r-33)+3sigma/4+R/4+5e<=2281/4+5w<=2401/4.

Their quadratic parts have minima695 and689 respectively.

### m3

All-light gives

    Tr+6r+4I+7sigma/4+sigma_s+R/4+5e<=488+5w<=518.

One-heavy gives

    Tr+6r+4I+3sigma/4+R/4+5e<=919/2+5w<=979/2.

Here Tr+6r+4(r-34)^2>=709. Thus neither alternative survives. Together with the normal-endpoint m4 exclusions, A1 is impossible.

Every use of repeated scalar inequalities is a positive linear combination of separately valid budget consequences. Each forest vertex keeps only its original full resource capacity.
