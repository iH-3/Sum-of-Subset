# Fresh P4 proof and cards for n85

These calculations use the fresh structure, the proved sharp raw caps, and the universal source theorem T=m0+A<=165. With j4,w2 one has m0=26, A=I+tau+delta, I=(r_s-34)^2, and

    A<=139, S=2K+1164-delta,
    2K=26+A+4R+U+2C+J,
    L=M-R>=18+A,
    K<=M+R+21.

This note includes the source-seed argument, all six resulting core-hole profiles, the exhaustive classification, and the terminal cards using their actual fresh constants. The shared positive-case prefix notation is in `fresh_positive_notes.md`.

## Source localization and profile reduction

Originally z<=14,w<=4z. If the minimum side size is<=20 then I>=196,rho>=49 and the structural T_floor48 imply delta<=244-I-rho<0. At sizes21..23, rho>=58,I>=121 and the structural floor144-2z>=116 give delta<=118-I<0. Thus both sizes>=24.

The structural H bound is H<=90+4z-I-delta<=146<T_24. The fresh inner/outer layer rows give central-strip join margins>=154 and456. Therefore w<=z, both even. In particular the loose old source bound A<=144+w<=158 gives core mass<=1348 and core maxima<=201; these intentionally conservative bounds suffice for the seven-seed argument in the notes. That argument gives w<=z<=4 and the exact six profiles.

Here is that seed argument explicitly. The greedy first-gap rule leaves total m-1 below m, with all later entries>m and no entry equal to m. First gaps>=4 have minimal I+tau>=199 (m4),228 (m5), or tau>=248 (m>=6), contradicting A<=158. At m1, two values u,v from{2,...,6} absent on both signs force tau>=214-2u-2v>=192, so at most one is absent. At m2, an absent q in{3,4,5} forces tau>=208-r-2q, where r owns the unique1; the quadratic I+tau has minimum174-2q>=164. At m3, an absent q in{4,5,6} forces tau>=206-2q>=194. Thus the following actual labelled seeds are available:

For the generic m>=6 bound, let k_v count the low occurrences on sign v. The core maximum<=201 gives m<=201 and T_(k_v)<=m-1, hence k_v<=19. At m6 the total low count is<=3, giving tau>=4(68-3)=260. At m>=7, k_v<=3 gives the side floor4(r_v-3). Otherwise m-k_v>=k_v+3; as r_v>=24 and k_v<=19, the difference (k_v+3)(r_v-k_v)-4(r_v-3) is at least k_v+7>0. Summing again gives tau>=248. The m4/m5 exact profile summations are displayed in the shared prefix lemmas.

| condition | seed | seed mass | lower holes | minimum mass of any9 core occurrences |
|---|---|---:|---|---:|
| m1,2 absent |3,4,5,6|18|1,2|43|
| m1,3 absent |2,4,5,6|17|1,3|41|
| m1,4 absent |2,3,5,6|16|1,4|39|
| m1,2,3,4,5 present |2,3,4,5|14|1|34|
| m1,2,3,4,6 present |2,3,4,6|15|1|34|
| m2 |1,3,4,5|13|2|37|
| m3 |1,1,4,5,6|17|3|39|

Direct bitset addition, or a short enumeration of each seed's sums, gives the full support except the stated lower holes and their reflections. The last column follows by taking at most two occurrences of each smallest permitted magnitude. Adjoin the remaining labelled core entries in increasing order. A failed central-interval join at next entry x means x>=T-2h, where h is the largest current lower seed-hole position. Any N remaining magnitudes at least x, multiplicity<=2, have total>=Nx+floor((N-1)^2/4). For n<=8 selected entries,N>=60; the seven resulting core-mass lower bounds are1728,1547,1366,1604,1665,1423,1547. For9<=n<=32,N>=36 and the last column applies; the bounds are1753,1607,1461,1492,1492,1531,1533. All exceed1348. For n>=33, T>=289 and x<=201<T-2h-1. Thus all joins succeed and the absolute core has at most four holes.

In the first three rows the profile baselines tau are136,134,132 respectively. For the missing4 row, missing2 on one sign would add r+1 above the baseline and force I+tau>=167>A<=148. Both opposite2 labels are therefore present, filling4; only1 remains as a lower hole. In the other rows the sole displayed first gap persists. Every peeled magnitude exceeds4, so all lower core holes persist to the source. The exact (tau,z=w) pairs are therefore(68+sigma,2) for ordinarym1, (135-r+sigma,2) for m2, (132+sigma,2) for m3, (136+sigma,4) for missing1,2, (134+sigma,4) for missing1,3, and (132+sigma,2) for missing1,4.

Every target-hole center is active: its hole offset is at most4 and subtracting any of the at least25 opposite core magnitudes produces distinct positive hull images well below the top two holes. Nonpositive centers in[1-M_v,0] use source M_v. Hence every integral center in[1-M_v,S_v] is active before any endpoint license.

Both leading resources are active by K-delta>=166-w+I+tau>0. If both O were active, their sharp caps give d_s+d_t<=2M+44+w. Set Y=2M-2K+44+w+delta. The leading and high-tail counts imply 2Y>488, while K-M>=R-132-w+A and R>=70,tau>=68,w<=4 give Y<=44, contradiction.

If one O_v were active, its sharp cap and leading row imply

    2X_v+g_v<=154+3w/2-R-I-tau.

An active lower-coordinate witness makes that coordinate integral. The two full-core overlaps with the two leading resources (allowing an empty mate with zero capacity) then give q>=137-R-delta/2. Since q<=2X_v+g_v, this would force I+tau<=17+3w/2+delta/2<=63, using the conservative delta<=80-I. This contradicts tau>=68. Thus all four lower-coordinate witnesses would be empty, forcing both O active, already excluded. Consequently both O are empty.

Their two known holes leave only two others. A nonintegral lower coordinate forces two witness holes and additionally H_v or alpha_v nonintegral, impossible. After lower integrality, a nonintegral v2 forces H_v,alpha_v and also C5_o in A or beta_v in B missing. Thus all outer coordinates are integral. O_v>-M_v by positive leading activity, so each empty O is HIGH. Its four fixed labels C11,C12,C13,C14 are HIGH and outside every baseline group. These eight labels license credit8: delta>=8 and epsilon=delta-8.

The universal source cap A<=137+w now eliminates all extra high-mass profiles immediately. First-gap3 and missing1,4 have tau>=132,w2, hence delta<=7. Missing1,3 has tau>=134,w4, delta<=7. Missing1,2 has tau>=136,w4, delta<=5. Each contradicts credit8.

Only the ordinary first-gap1 profile and first-gap2 profile remain, with exact target support F_v=[1,S_v] minus{S_v-m}. At first gap1, tau=68+sigma and I+sigma+delta<=71, so both physical sizes lie in[26,42]. At first gap2, unique1 owner h satisfies h in[29,40] and true profile excess sigma obeys I+sigma+delta<=h+4. In both profiles delta<=71 and epsilon<=63.

## Empty-center rule, endpoints and CORE8 classification

Source U obeys U<=350-2T, so U<=162. The first opposite peeled magnitude is<=R_o+U<=304. On both profiles S_v>=469 and R<=142. The points M_v,0,-R_o give activity throughout[1-M_v,S_v+R_o], except possibly at S_v+R_o-m. There the first opposite peel produces a positive hit below S_v-m (at least163). Thus an empty integral center is LOW<=-M_v or HIGH>=S_v+R_o+1.

An empty own center cannot be LOW by leading activity. A retained singleton above any HIGH center loses at least73 source points: all positive points, zero, and all opposite core points. Such a loss exceeds epsilon<=63. An empty cross center cannot be HIGH, since it would put all77 points of lambda_v+D_v above the target. Cross activity is upward closed C4=>C5=>C6=>C7.

Before CORE8 retention, the target-independent separated-arm forests give

    2X_v+X_o+g_v>=252-tau-delta,
    2X_v+X_o+G>=305-tau-delta.

The arm choices involve at most one empty vertex at each point, and positive/negative restricted supports are disjoint because M>R. If beta_v,H_v are active, the sharp beta/H raw cap is d_v-M<=21+w/2<=22. Activity of C7_v or C6_v would instead give d_v-M>=253-tau-delta>=114 or306-tau-delta>=167. Thus neither triple beta_v,H_v,C7_v nor beta_v,H_v,C6_v can be wholly active.

These rules reproduce the exhaustive whole-unit classification with the fresh native-loss threshold73:

- A1 retained beta: two contributing betas would require one further hole in each{H_v,C6_v}; then both C5 singletons are active and the four-center identity beta_s+beta_t+C5_s+C5_t=-2W contradicts their activity lower bounds. Thus beta is sole on s. Active H_s would force both C6_s,C5_s empty, leaving C7_s active and contradicting the forbidden triple. Hence the known holes are O_s,H_s,O_t, with one further Z. CORE8 is retained by the cross chain and the higher-retained73-loss rule. Z lies in{H_t,alpha_s,alpha_t,C5_s,C5_t,pair1}. Pair1 is sole if retained because its two centers sum<-3M. If it is empty, use T5 below. If retained with opposite owner, use the opposite-owner card. If same owner s, the triple C4_s,beta_s,C5_t is impossible, so Z=C5_t and alpha_s is retained; use same-owner card.
- B: U,V must be retained by the higher-retained rule, and the forbidden triples plus cross chain force C6,C7 retained. The two further holes are one from each{H_s,beta_s},{H_t,beta_t}. Both alphas and both pairs remain. Empty beta is LOW. They cannot both be empty because beta_s+beta_t>0. Pair1 and C5 pair have sole matching owners by the literal center identities. Any active beta on the opposite owner is excluded by the opposite-owner card, and the remaining active beta on the common owner with retained alpha is excluded by the same-owner card.
- A0 beta-pair empty: CORE8 is retained. Its one further hole Z belongs to{H_s,H_t,alpha_s,alpha_t,C5_s,C5_t,pair1}. If pair1 is retained it is sole; normalize owner s. Then C5_s is retained and Z lies in{H_s,H_t,alpha_s,alpha_t,C5_t}. At least one of H_v,alpha_v is retained above each empty beta, so both beta components are LOW. V6_s,V6_t are LOW and meet one baseline group. With the eight HIGH O labels the fixed credit is9.

First-gap1 charged endpoints have uniform allowance1: I+sigma+epsilon<=63<73 makes the next core rank exact. First-gap2 has delta<=38 and epsilon<=30, while an outside-hull center clips at least33 source points, so charged endpoints are normal. With a=1 for m1,a=0 for m2, both are

    Z>=73-r_v-l_Z-a,
    Z<=S_v+r_o-72+h_Z+a.

## Common source/rank bounds for the terminal cards

Here sigma=tau-68 is the generic excess; at m1 each sigma_v>=0, at m2 sigma_v>=-1 and sigma>=27. Put eta=0 at m1 and eta=1 at m2. The penultimate core estimate gives

    K<=C+312+sigma+eta,
    2R+I+delta<=224+eta<=225.

Q61 overlap floor is f_eta=(166-eta-sigma+R)/4. Full-core69 overlap floor is137-R. Ordinary gaps and stars can use any actual common trimmed core, with no change to capacities. At m1, writing xi=R-70, three available overlap floors are

    F0=67-xi, F1=65-sigma+xi, F2=63-sigma/2+xi/2.

At m2 using the true profile excess sigma' and xi'=R-71 they are

    F0=66-xi', F1=64-sigma'+xi', F2=62-sigma'/2+xi'/2.

The same full resources certify all these floors; each scalar inequality may use the maximum F.

## Opposite-owner card

Suppose beta_s and P_t=C4_t are licensed capacity77 native resources and CORE8 is retained. The identity V_t=2d_s+beta_s+P_t+2s4+t4+g_s and three endpoint rows followed by the leading-s inequality twice give

    S_s+3g_s+4X_s+2s4+t4<=1014+3a+r_s+delta-2e.

Two ordinary gap-g_s pairs give3g_s>=3f_eta-3epsilon/2. The stars give6X_s+X_t>=959-7R-3epsilon. Combining these with the source mass, L>=86+I+sigma+delta and the radial bound yields

    T_r+5r+29I/8+sigma/4+sigma_s+13e/2
      <=827/2+27eta/8+15delta/8+3a.

Use delta<=71-I, eta<=1,a<=1 and sigma_s>=-1. Then

    T_r+5r+11I/2+sigma/4+sigma_s+13e/2<=553.

The global integral quadratic minimum T_r+5r+11(r-34)^2/2 is1401/2. Credit e>=8 and sigma_s>=-1 give left>=1503/2>553. Thus opposite owners are impossible.

## Same-owner card with active alpha

Suppose alpha_s,P_s,beta_s are licensed distinct native resources. The literal identity and outer order give

    alpha_s-P_s-beta_s> d_t+2s4+t4+G.

Three endpoints and the distinct leading-t loss give

    S_t+g_t+2X_t+2s4+t4+G<=K+1082+3a-r_t-e.

Three disjoint ordinary pairs give g_s+2g_t>=3f_eta-epsilon, while stars give2X_s+3X_t>=685-5R-3epsilon/2. Source and radial substitution gives

    T_r+5r+25I/8+sigma/4+sigma_t+5delta/8+7e/2
      <=1349/2+23eta/8+3a.

At m1 the right is677.5, sigma_t>=0; at m2 it is677.375, sigma_t>=-1. The quadratic part has exact integer minimum5265/8=658.125. Credit8 makes the respective left floors5489/8=686.125 and5481/8=685.125. Both exceed the right side.

## T5: sole retained beta, empty pair1

The holes are O_s,H_s,O_t,pair1, beta sole owner s. Credit13 follows by an exact label ledger. Leading K-delta>=164+I+tau>R gives d_v>g_v, so F3,F4,F5 are LOW. Empty beta_t is LOW by retained alpha_t. Both empty C4 are LOW, giving C55,C56,C57,C58 LOW on each sign. Genuine beta_s,C5_t imply d_t>d_s; C5_s gives t2<d_s, so V3_t,V4_t LOW. There are20 LOW labels meeting18 baseline groups, and11 HIGH labels from O_s,H_s,O_t outside those groups. Thus e=11+20-18=13, with no extra hole allowance.

Upper endpoints alpha_s,H_t, lower endpoints alpha_t and twice beta_s, plus C5_t, together with the leading-s inequality twice give

    2M+6X_s+2X_t+3g_s+g_t<=932+6a+delta-2e.

The weighted native losses are<=2epsilon and the six endpoint allowances are exactly6a. Stars and pairs using overlap F give6X_s+2X_t>=8F-3epsilon and3g_s+g_t>=4F-3epsilon/2. Since M>=R+86+I+sigma+delta and I+sigma+delta<=71,

    2R+11I/2+11sigma/2+12F<=924+6a.

At m1, R=70+xi and13F0/2+11F1/2 implies12F+2xi+11sigma/2>=793+xi, so the left>=933>930. At m2, use generic sigma,xi=R-70, F0=67-xi,F1=64-sigma+xi; the same combination gives a left floor927.5+xi>=928.5>924. This excludes T5.

## A0 case1: pair1 empty

All H,alpha,C5 and CORE8 are retained, with credit9. Pair-sum joint-loss counting and the two H identities, using uniformly weakened endpoints72-r_v and S_v+r_o-71, give

    S>=4M+4X+2G+302+2F-3epsilon.

The source upper bound S<=2M+2R+1206-delta and the stars/pairs with overlap F then give

    14F+2I+2tau<=814+3delta.

At m1, mass I+sigma+delta<=71 forces14F+5I+5sigma<=891. But5F0+F1+8F2 gives14F+5sigma>=904, contradiction.

At m2 with true excess sigma' and unique1 owner h, tau=135-h+sigma' and I+sigma'+delta<=h+4. Thus14F+5sigma'+5I<=556+5h. Yet5F0+F1+8F2 gives14F+5sigma'>=890, forcing I-h<=-334/5, while min[(h-34)^2-h]=-34. Contradiction.

## A0 case2: retained pair1, opposite alpha retained

The conservative transport being used is

    T_k+4k+128-tau_s<=7R+3delta,

where k=r_t is the side opposite the pair1 owner. Its ordinary first-gap1 proof uses the sharper actual fringe bound B_s+B_t<=min(20,183-T); the root's common-source certificate gives positive margins3,2,1 for T<=163,T164,T165. This is a separate licensed source lemma, not an assumed129 transport.

At m2, use R<=71+sigma' and the unique1-owner mass cap. If h=k, tau_s=136-2k+sigma_s and I+sigma'+delta<=k+4. The conservative row forces

    T_k-2k+8I+5delta<=537.

Its quadratic part is at least496, and delta>=9 makes the left>=541. If h=68-k, tau_s=67-k+sigma_s and the cap is I+sigma'+delta<=72-k. The resulting row is

    T_k+13k+8I+5delta<=1012.

Its quadratic minimum is971, and delta>=9 gives left>=1016. Thus both physical unique1 owners are excluded with margin4.

## A0 case3: retained pair1, opposite alpha empty

Every other H,alpha_s,C5 and CORE8 resource is retained. The same seven weighted endpoint uses as the old identity, now with the fresh weakened constants, give

    S>=5s4+4t4+2g_s+3g_t+2h_t+298-r_s-E,
    E<=2epsilon.

Hence

    2M+M_s+5X_s+4X_t+2g_s+3g_t+2h_t
      <=2R+908+r_s-delta+2epsilon.

Use f=(233+R-tau)/4, which is valid for both profiles. The disjoint ordinary groups give2g_s+3g_t+2h_t>=5f+122-2epsilon. Stars give5X_s+4X_t>=1233-9R-5epsilon/2. Also2M+M_s>=2R+41+r_s+2I+2tau+2delta. Thus

    488+2I+2tau+5f+3delta<=9R+13epsilon/2,
    3351/4+2I+3tau/4<=31R/4+7delta/2.

Use2R+I+delta<=225. This forces

    -273+47I+6tau+3delta<=0.

Since tau>=68, the left is at least135. Contradiction.

All original P4 configurations are exhausted by these owner/empty-pair cases and the A0 three-case split.
