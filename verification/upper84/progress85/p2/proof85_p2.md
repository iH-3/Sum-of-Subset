# Complete exclusion of the positive-hole SIZE85 stratum P2

This is a fresh argument for j=2 and 1<=z<=14 at cardinality85. It assumes
the proved SIZE85 integral primitive structural theorem, the common covering
and source envelopes, native-loss/forest lemmas, and the sharp raw-gap counts.
All occurrences on opposite signs remain distinct labelled occurrences.
No canonical endpoint model or old SIZE86 activity census is used.

## 1. Source parameters

Set d=77, |E|=69, r_s+r_t=68, I=(r_s-34)², G144=144. Let
rho=rho_s+rho_t, mu=mu_s+mu_t, tau=sum(P_s)+sum(P_t)-T_rs-T_rt,
H=h_s+h_t=tau-mu. Write C_v=sum(P_v), R_v=max(P_v), R=R_s+R_t,
M_v=max(D_v), M=M_s+M_t, K=|2D|, and S=sum(D_s)+sum(D_t).
The source peel magnitudes are R_v+a_v,R_v+b_v,R_v+c_v,R_v+e_v,
with 1<=a_v<b_v<c_v<e_v. Put

    U=a_s+b_s+a_t+b_t, C=c_s+c_t,
    J=(e_s-c_s)+(e_t-c_t), A=I+tau+delta, m0=-126-w.

The source-only identities and inequalities are

    S=2K+1316+w-delta,
    2K=m0+A+4R+U+2C+J,
    J+U<=458+w-A, J>=A-144-w, U>=6, J>=2,
    A<=298+w, K-M>=R-286-w+A,
    K-delta>=16-w+I+tau.

The quantitative layers, for U0 the first four peeled masses, V0 the last
four, C0=C_s+C_t=1190+I+tau, and C1=C0+U0, give

    C0-U0>=320+2I+delta-2z,
    C1-V0>=446+2I+mu+rho+delta+2z.

Initially w<=4z<=56. The structural budget gives
delta<=302-I-rho+2z. If the smaller side were at most17, then I>=289
and rho>=49, giving delta<=-8. Hence 18<=r_v<=50; throughout this range
rho>=49 and mu>=62. Non-AP primitivity gives R_v>=r_v+1 and tau_v>=r_v-3.

## 2. Common-strip localization using the actual four inner occurrences

The source envelope gives H<=236+w-I-delta<=292-I-delta. For every
integer r, T_r+(r-34)²>=397; hence each C_v>H. The common-strip lemma
fills [H,C0-H] in the absolute core support. Its width L=C0-2H satisfies

    L>=1016+2I+delta-w>=960.

Sort the four inner occurrences as t1<=t2<=t3<=t4. All sixteen subset
choices are required. The largest consecutive gap among their subset sums
is at most max_i(t_i-sum_(h<i)t_h). The first three terms are at most
t3<=U0/2. The layer and source inequalities give

    U0<=1168+w-2I-2delta+2z<=1252,

so these three terms are at most626<L.

For the last term, t4 is necessarily one side's second occurrence R_v+b_v;
the other three contain R_v+a_v and both opposite occurrences. Thus

    t4-t1-t2-t3=b_v-a_v-2R_o-a_o-b_o
                 <=U-8-2R_o.

Crucially, use the offset sum U rather than the much larger layer mass U0.
Since J+U<=458+w-A and J>=2, U<=512. Since R_o>=19, this last gap is
at most466<L. Therefore every translate of the core central interval by
an actual inner subset sum overlaps or abuts the next, filling [H,C1-H].

For the outer occurrences, selecting none or all already suffices because

    C1-V0-2H>=-26+4I+mu+rho+3delta+2z-2w
             >=85-6z>=1.

This fills [H,S-H]. Complement symmetry in the same fixed boundary strip
now gives z,w even, w<=z<=14, and both targets have eta_v=w/2 holes.
The old coarse all-sixteen inner estimate is not needed.

After localization, H<=250-I-delta and R<=72+rho+H<=72+tau<=384-I-delta.
Thus T_r-R>=13+delta. The first absolute-core gap f is below both R_v:
if one side had all its entries below f, its total would be at most f-1<R,
contradicting C_v>=T_r>R. All peeled occurrences exceed f, so f survives
and w>=2.

Every integral ordinary center in [1-M_v,S_v] is active. To prove this
without an endpoint assumption, use R_o<=r_o+tau_o and tau_v>=r_v-3:

    S_v-H-R_o>=T_r+7r+2I-594-2w+2delta>=39+2delta.

The last integer quadratic has minimum39 at r26. A target hole u lies
within H of its upper endpoint, so all u-P_o are positive hull integers;
at most eta_v<=7 are missing and r_o>=18 guarantees a target hit.
For a nonpositive center u>=1-M_v, the value u+M_v lies in the complete
lower target interval, since S_v-M_v>=C_v>H. This proves the activity claim.

Finally K-delta>=16-w+I+tau>0 makes both leading translates active and
their shifts integral. A nonintegral v3 or v4 would force respectively
{own2_v,C6_o} or {own3_v,C7_o} to be the two missing singleton units.
With only these holes H_v and alpha_v remain active, contradicting the
integrality of H_v-alpha_v=lambda_v+v3+v4. Two nonintegral lower
coordinates would require four holes. A nonintegral v2 would make O_v,
H_v,alpha_v three missing singletons. All outer coordinates are integral.

## 3. The first-gap profiles and two-cap exclusion

Write t_v=d_v-M, where d_v=v1-v2, and define T_v to mean that O_v is
active or both beta_v,H_v are active. Sharp raw gaps give

    T_v => t_v<=22+w/2<=29,
    beta_v and O_v active => 2t_v<=27+w/2<=34.

Both cap predicates cannot hold. The four-star estimate is
2X+4R+delta>=548, and the high-tail count gives
d_s+d_t+G+delta-2K>=642. With
Y=2M-2K+44+w+delta, two caps and the leading counts imply

    2Y>=1190-4R-delta,
    Y<=616+3w-2R-2I-2tau-delta.

Consequently 4I+4tau+delta<=42+6w, contrary to tau>=62+2z and w<=z.
At least one O singleton is missing, and at least one cap predicate holds.

Let k_v count core entries below the first gap f and k=k_s+k_t. The greedy
first-gap rule gives their total f-1 and interval completeness below f.
The common rank lower bound is

    I+tau>=69f-1-(f+34.5)k+k²/4
                 +(r_s-34-(k_s-k_t)/2)².

Since f<R/2<=192 and k(k+2)/4<=f-1, k<=26. For f>=7,k<=4 the displayed
lower bound is at least320>312. For k>=5 it is at least
(-k³+68k²-4k+272)/4>=1827/4>312. Thus f<=6.

The complete low multisets are empty, {1}, {1,1}, {1,2}, {1,1,2}, and
at f6 either {1,1,3} or {1,2,2}. These are fixed by the total f-1,
interval completeness and multiplicity at most two. Put b for the mass
excess of the coordinatewise minimal side profiles, B for their two maxima,
and sigma=tau-b>=0. If one distinguished side has r=34+x, their constants are:

|f|I+b|B|minimum tau|
|---:|---|---:|---:|
|1|I+68|70|68|
|2|101+x(x-1)|71|85|
|3|I+132|72|132|
|4 split|I+199|74|199|
|4 together|199+(x-1)²|74|168|
|5|228+x(x-1)|75|212|
|6 both low multisets|294+x(x-1)|77|278|

In particular f>=2 implies tau>=85, and I+b-2B>=-41 in every such row.

## 4. No C7 singleton is empty

If C7_v were empty, it and at least one missing O would be the two holes,
so C6_v is active. Integral activity localization makes C7_v HIGH, hence
lambda_v>S_v+M_o. In the leading resource the entirely HIGH set
lambda_v+(D union(M_v+D)) has at least d+(r_v+4)=r_v+81 points.
At least three of the four higher native singletons V_v,U_v,H_v,O_v
are retained, and each loses r_v+5 points. Thus delta>=4r_v+96.

If f>=2, A>=I+4r_v+96+tau>=132+96+85=313>312, impossible.
Here I+4r=(r-32)²+132.

At f1 write tau=68+sigma. The source bound yields

    (r_v-32)²+sigma<=2+w<=16.

Thus 28<=r_v<=36, the opposite size is32..40, and sigma<=16. Each
side contains the consecutive prefix 2,...,r_v-sigma_v+1, at least
2,...,13; every remaining coefficient is at most r_v+1+sigma_v<=57.
The prefix support [0,L] minus{1,L-1}, with L>=90, keeps exactly those
two reflected holes under every remaining coefficient. Therefore both
side hole counts are2, the absolute core has exactly two holes, z=2, and
the persisted gap1 gives w=2.

If the missing O were opposite C7_v, all four higher v singletons would
be retained and delta>=5r_v+101. Then I+5r_v+sigma<=129+w<=131, whereas
the integer minimum of I+5r is164. Therefore O_v is the other hole.
It is HIGH, and its four fixed labels O_v+v_i are HIGH; they supply four
additional fixed credits beyond the baseline nonpositive witnesses.
Hence delta>=4r_v+100. With w2 the source gives
(r_v-32)²+sigma<=0. Thus r_v32,I4,sigma0,delta228,A300.

Now m0=-128,T=m0+A=172. Source envelopes give J+U<=160,J>=154,U>=6,
so U6,J154. Both signs have (a,b)=(1,2), for which the four-offset fringe
counts F_s,F_t are at most5 per sign. These F values are distinct from
the baseline core-maximum sum B in the profile table. The full fringe comparison gives

    T+U<=J+2+2(F_s+F_t),

and would require178<=154+2+20=176. This excludes the final equality.
Therefore every C7 singleton is retained.

## 5. Rooted forests reduce to f1 and exclude simultaneous beta/O activity

Trim the four largest core entries on each sign, leaving an actual61-point
set Q. Its rank-certified overlap constant q satisfies

    4q=516-5B-sigma+R.

On a cap side v use the positive arm L_v-V_v-U_v and the negative arm
L_o-C7_o-C6_o. If V_v is retained, C7_o is also retained and at most
one of U_v,C6_o can be empty. Thus choose one full two-edge arm and
the first edge of the other; every selected resource is retained.
Designate L_v as a root. The same original deficiency budget then gives

    t_v>=K-M+3q-delta
       >=101-w+I+b-2B+sigma/4.

For every f>=2 this is at least60-w>=46>29, contradicting the cap.

If V_v is empty, the other hole must be O_o: choosing O_v instead would
leave both O_o and beta_v,H_v active, giving two caps. Both H singletons
are retained. Branch B would retain both beta singletons and again give
two caps; in A the retained beta pair is sole on v. Hence beta_v,O_v
are active and the sharp double-gap upper bound is t_v<=17.
The empty V_v is HIGH, since leading activity implies V_v>1-M_v.
Both H_v,O_v are retained HIGH resources and each loses r_v+5 native
points. Use edges L_v-U_v and L_o-C7_o, root L_v and include those two
unused losses. This gives

    t_v>=-18-w+I+b-B+2r_v+sigma/2.

The f1 integer minimum is47-w>=33; every f>=2 is at least48-w>=34.
Both contradict17. Thus every cap side has V_v retained, and f=1.

At f1 the rooted lower bound is t_v>=29-w+I+sigma/4. If beta_v and
O_v were simultaneously active, the double gap would force

    4I+sigma<=5w-62<=8.

For w<=12 this is already impossible. For w14, I<=2 and sigma<=8;
the consecutive core prefixes and small final coefficients then preserve
exactly the two side holes as in the preceding dense-profile argument.
This gives z=w2, which contradicts the same inequality. No side has
both beta_v and O_v active.

## 6. Exhaustive activity forms and the terminal contradiction

If both O singletons are missing, B is impossible because both beta,H
caps would hold; in A the retained beta pair has a sole actual owner.
If exactly O_v is missing, O_o is active, hence beta_o is inactive. B
would make beta_o the other hole and leave beta_v,H_v active, giving
two caps. In A, either H_v is the other hole or the whole beta pair is
empty; every other choice would again leave both cap sides active.
Thus exactly the following A whole-hole forms remain:

    {O_v,beta pair}, {O_s,O_t}, {O_v,H_v}.

All unlisted whole units are retained. In the first and third forms choose
the side u opposite the missing O_v; in the middle choose the sole beta
owner. That side has the cap predicate. The retained singleton centers
alpha_o,C5_u and their exact identity imply t_u>=2X+G+2. Hence

    2X+G<=20+w/2.

At f1 write sigma_v=sum_i(x_vi-i-1), xi_v=R_v-r_v-1>=0, and
sigma=sigma_s+sigma_t,xi=xi_s+xi_t. Source mass gives

    I+sigma+delta<=230+w.

Trim six largest core entries per sign, leaving57 actual points. Its span
is at most58+(sigma-xi)/6, so the certified intersection lower bound at
gapq is55-(sigma-xi)/6-q. All U_v,V_v,C7_v are retained in every form.
On each target the retained tree L_v-V_v-U_v with edge L_v-C7_v has
three gaps X_v,g_v,X_o. Both targets together give, in one budget,

    2X+G>=330-sigma+xi-delta.

Combining these three inequalities forces

    80+I+xi<=3w/2<=21,

a contradiction. This excludes the whole P2 stratum, including all
positions of empty endpoints and all paired-unit ownership choices.

## 7. Exact finite arithmetic replay

`check85_p2.py` checks the range, width, activity quadratics, first-gap
polynomial and profile minima, C7 equality, rooted-forest scalar margins,
and terminal contradiction. It is an arithmetic checker of these written
lemmas, not an enumeration of actual source sets or activity descriptors.
