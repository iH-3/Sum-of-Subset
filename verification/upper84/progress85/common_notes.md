# Local elementary exclusions at size 85

All statements below assume a valid fresh structural reduction for a size-85 configuration. Put d=77, |E|=69, r_s+r_t=68, Lambda=1191+I, I=(34-min(r_s,r_t))^2. The structural scalar budget is Omega=600-I and the restricted-sum constant is 144. These are conditional local deductions, not a proof of the imported reduction.

## General source formulas

S=2K+1470-77j+w-delta. With A=I+tau+delta and m0=77j-280-w,

2K=m0+A+4R+U+2C+J.

Deleting the two maxima leaves 75 points. The core interval and 12 exceptional three-peel pair labels, followed by 153 reinserted pair labels, give

K <= 2R+C+166,
J+U <= 332-m0-A,
A <= 445-77j+w,
K-M >= R+77j-440-w+A,
K-delta >= 77j-142-w+I+tau.

When z>0, primitive side supports are non-AP, so R_v>=r_v+1 and R>=70. The last bound improves to

K-delta >=77j-138-w+I+tau.

Quantitative layers:

V0-C1+delta+2z <= -292-2I-77j-mu-rho,
M0+delta-2z <= -166-2I-77j.

The final source cap follows from the triple and quartet fringes. For one sign let P count sums of the first three peel offsets above the third offset and B count sums of all four offsets above the fourth. The proved elementary inequality P+B-a-b<=5 combines the two-max envelope K<=2R+C+154+P_s+P_t with the full-source envelope. Their average gives m0+A<=165 and therefore A<=445-77j+w. The complete unbounded proof is in foundations/source_triple_fringe85.md.

## Sharp raw-gap counts

The exact inventories are eleven labels in the first gap, eight in the beta-active second gap, and fifteen in the beta-active union. Thus

O_v active => t_v=d_v-M<=12+eta_v,
beta_v,H_v active => t_v<=9+eta_v,
beta_v,O_v active => 2t_v<=17+eta_v.

The first implication uses the original lower guard; leading activity, H activity, or own2 activity licenses it in the corresponding applications. The other two guards are supplied by the stated active resources. The proof by d-spaced fixed-label chains and three ranges for v3/d is written in full in common/raw_gap_inventory.md. These counts imply the uniform cap t_v<=12+eta_v for the predicate “O active or beta,H active.”

## Star and two-cap constants

Four full-core star edges give 2X+4R+delta>=548. The four-top-tail count has 4*83+5=337 labels per target, so

d_s+d_t+G+delta-2K>=796-77j.

With both sharp t_v<=12+eta_v caps, the two-cap proof, using Y=2M-2K+24+w+delta, gives

4I+4tau+delta+231j <=464+6w.

At j=1, with tau>=62+2z and w<=z, the two-cap inequality would require

15+2z+4I+delta<=0,

which is impossible. In particular the P1 two-cap exclusion needs no additional four-edge estimate.

## General first-gap and terminal lemma

If the absolute core has a hull hole, both side sizes>=16, and I+tau<=395, its first missing integer f is <=8. Write k=k_s+k_t for the low coefficients. Then k<=4,k_v<=3. The high baseline maxima are B_v=r_v+f-k_v, B=68+2f-k, with baseline excess b, residual sigma=tau-b>=0. Direct summation gives

I+b=69f-1-(f+34.5)k+k^2/4+(r_s-34-(k_s-k_t)/2)^2,
I+b-5B>=-282.

Proof of f<=8 follows exactly the old argument: f<max R_v<=52+tau<=447, so k<=41; for f>=9,k<=4 the lower bound is >=65f-139>=446. For k>=5, use f>=k(k+2)/4+1 to get [-k^3+68k^2-4k+272]/4>=1827/4>395 (the polynomial increases over k=5,...,41). The baseline-minus-5B minimum is attained at f=1,k=0; f=2,3 and f=4,...,8 give larger lower bounds.

Delete six core entries per sign: the retained set has 57 points, and its certified overlap parameter satisfies

6q=750-7B+R-sigma.

The old rooted terminal forest and the source estimate at j=1 give

2t_u >=389-7B+2R+I+b-w >=107-w.

The sharp double gap gives 2t_u<=17+w/2. Thus the terminal form forces

90<=3w/2.

## P1 localization

The scalar range is 16<=r_v<=52: otherwise I>=361 while delta<=407-I-rho and rho>=49. H=h_s+h_t obeys H<=306+w-I-delta<=362-I-delta. For every physical size, T_r+I>=397, ensuring each core mass>H. Initial width >=890+2I+delta. Every inner entry is <=637, and U0>=142, so the next width is >=1032. The outer-layer row and the same H bound show C1+Q0-4H>=788+6I+4delta+2z>0, where Q0=369+mu+rho+2I+delta+2z. The last-shift gap J<=585 is smaller than the width. Thus the original common-strip argument propagates and gives z,w even, w<=z, eta_v=w/2.

Leading activity follows from K-delta>=-61-w+I+tau>=1+I+2z-w>0. At most one missing own singleton gives full outer integrality. The sharpened two-cap and terminal contradictions exclude P1.

## P5: complete source-only contradiction

The scalar range gives rho>=58, delta<=41-I, 28<=r_v<=40. Also H<=13+4z-I-delta<=69. Quantitative layers give C0-U0>=551+2I+delta-2z and C1-V0>=797+2I+delta+2z. Subtracting 2H leaves >=385 and >=687, so common-strip localization applies: w<=z<=14 and parity holds.

The final source envelope gives A<=60+w<=60+z, whereas positive core holes imply tau>=62+2z. Thus

2+z+I+delta<=0,

an immediate contradiction. This excludes P5 without any outer-coordinate integrality or paired-owner assumption.

## The entire high-hole family

Use the retained paired (mu,rho) floors (426,294), (470,338), (514,382), (554,422), respectively for z bands15-16,17-20,21-48, and z>=49. The whole-family localization proof is in foundations/highhole_localization85.md. It keeps the independently certified mu information as well as rho and requires no extension of the density threshold.

Writing W=1190+I+mu-H for the original core central-strip width, the fresh source and layer envelopes give

M<=827+H+(rho-mu)/2+z-I-c,
W-M>=-837+4I+3c+3(mu+rho)/2-3z.

The retained paired floors give W-M margins195,315,363 in the first three bands. In the tail, c+I+z<=178 gives margin at least93+7I+6c. The two individual core masses exceed H with margins171,199,131,120 in the four bands. Thus the same central strip propagates through every absolute source entry. This proves parity, eta_v=w/2 and w<=z on the entire high-hole domain, including H0.

At j>=2 the source envelope gives I+tau+delta<=291+w; with tau>=rho+2z, this would require rho+z+I+delta<=291, already impossible at rho294,z15. All H_j with j>=2 are excluded (larger j only improves the bound).

At j=1, the source envelope leaves only even z=16,18,20 and I+tau<=395. Both-leading activity follows directly after localization from K-delta>=-61-w+I+tau>=233+z+I>0. At least three own centers per sign imply outer integrality. The two-cap contradiction forces the terminal form, and 90<=3w/2<=30 is impossible.

After the same whole-domain localization, at j=0 the lower bound K-delta>=-142-w+I+tau>=152+z+I>0 makes both leadings active. All own centres are active, so outer integrality follows. The two-cap inequality gives 4I+4tau+c<=464+6w, while tau>=294+2z and w<=z would require 712+2z+4I+c<=0. Thus H0 is excluded as well.
