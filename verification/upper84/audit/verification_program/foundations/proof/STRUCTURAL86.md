# Fresh SIZE86 common-core structural theorem

Status: fresh proof candidate, submitted for independent review. This document does not exclude SIZE86 and is not an endpoint-model or source-contract acceptance. It reconstructs the argument from the retained published upper86/SIZE87 and foundational materials; no missing N86 file, old receipt, hash-only assertion, or historical census is used as a mathematical premise.

## 1. Statement and scope

Let A be a finite set of 86 distinct integers, containing zero, with FS(A) contained in 4A; FS includes the empty subset, while 4A allows repeated summands. Remove its four largest positive and four smallest negative members to form B, set D=A\B, and peel two largest positive and two smallest negative elements from D twice, to obtain D1 and E=P union {0} union (−Q). The endpoint bootstrap below justifies these sign counts. Then there is a positive scale t such that D/t is integral. In that scale both P/t and Q/t are individually primitive (gcd one).

The sizes and complete oriented range are

    |D|=78, |D1|=74, |E|=70, |P|+|Q|=69,
    15 <= |P| <= 54, 15 <= |Q| <= 54.

After reflection put a=34−k, b=35+k, 0<=k<=19, I=k(k+1), and T_r=r(r+1)/2. Define U=FS(P), V=FS(Q), u=|U|, v=|V|, s=|FS(E)| and the size-invariant excesses

    mu_X=|FS(X)|−1−T_|X|,
    delta0(X)=#{x in X: 2x is not a distinct-element sum in X union {0}},
    rho_X=mu_X+2−2delta0(X),
    mu=mu_P+mu_Q, rho=rho_P+rho_Q,
    Lambda=1+T_a+T_b=1226+I,
    kappa=s−Lambda−mu=|U+V|−u−v+1,
    Omega=22*78+97−Lambda=587−I.

On the asserted common lattice, let h_P,h_Q,z,w be the hull-hole counts of U,V,FS(E),FS(D), respectively. Then

    h_P,h_Q <= kappa,
    z=h_P+h_Q−kappa, 0<=z<=min(h_P,h_Q)<=kappa,
    w<=4z.

The two extreme FS(E) translates from D1\E intersect, as do the two extreme FS(D1) translates from D\D1. For the nonnegative covering/peeling slacks defined below and T=kappa+ell1+ell2+g,

    rho+kappa+2theta+c+ell1+ell2+g = Omega,
    T >= kappa+146−3z >=146−2z,
    T >= z, T >=49, c+rho+T <= Omega.

No assertion is made that every element of the original outer B lies in this lattice, or that a leading 2D covering component contributes. Outer integrality is proved only inside the small-c contradiction lemmas that explicitly require it. Feasibility is never inherited by a subset. If the application starts from a real feasible set, the homogeneous rational-kernel integralization in the retained report transfers existence with a prescribed zero; it does not claim that every original real set was a rational lattice set. The already-published exclusion of size87 permits adjoining zero to a hypothetical zero-free size86 set, but that is a separate descending-cardinality argument.

## 2. Exact retained inputs and what is being reproved

The immutable source list and fresh hashes are in `source_manifest.json`. Line-number references here refer to the recovered files named there, rather than a lost N86 copy.

The following general established results are mathematical dependencies, not SIZE87 conclusions being substituted at SIZE86:

1. The fixed covering and four-extreme peeling inequalities, published report lines141–218: |FS(D)|<=2|2D|+18d+85, |FS(F)|>=|FS(F')|+|R(F)|−1, and s<=24d+77, where R uses distinct summands. The fixed 110 slots and 26 disjoint deletion groups underlying the first inequality are retained in the foundational report.
2. The increasing-chain lower bound mu_X>=0; uniform rho_X>=−8; rho_X>=0 for |X|>=14; support stability mu_X>=|X|−3 when FS(X) is not an AP; non-AP rho_X>=n(|X|), where n(r)=r−5 for r>=21 and r−14 below21. The strengthened non-AP proof and its finite deleted-interval checker are retained; the old bounds are in foundational report lines580–815.
3. Stanchescu's simultaneous inverse, in the deliberately stricter form |U+V|<u+v+min(u,v)−3: it places U,V on a common difference lattice with h_P,h_Q<=kappa. Equivalently the sufficient test is kappa<min(u,v)−2. The source correction is foundational report lines1235–1249. Its short-diameter Theorem4 says that integer sets containing their hull endpoints, with max(diam U,diam V)<=u+v−2−delta (delta=1 if diameters agree, 0 otherwise), have |U+V|>=u+v−1+max(h_U,h_V). There is no separate gcd assumption in this short-diameter theorem. The retained dense-summand proof states and checks that distinction.
4. The small-increment/counted-hole lemma: if a positive prefix of size j has nonnegative excess increment y<=beta and j>=2beta+5, on some scale its coefficients form an initial interval with at most beta deletions, and its subset sums miss at most beta lower points in [1,2beta] and their reflections. The global prefix rho bounds and recurrence rho_i>=rho_(i−1)+y_i−2 also hold.
5. The effective-hole lemma with explicit integer tests: for beta>=1,C>=0 let K=max{k>=3:k(k−3)/2<=C+1}, D=C+max(3,K), M=max(2beta,1+floor((1+sqrt(9+8(D+1+6beta)))/2)), J=max(K+1,2beta+5,M). If (r−J+1)beta>D and T_(J−1)−1>D, then 2beta<h<|FS(X)|−1 gives mu_X>=r+C+1. The same conclusion holds without the upper-hole bound if X is already primitive on the specified integer lattice: in the retained proof that upper bound was used only to infer primitivity. A primitive AP support would be a full interval and cannot have h>0. The remaining prefix, off-scale, and endpoint-bridge arguments are unchanged. This proof mechanism is also restated in the inverse companion, not inferred from an N87 result.
6. The flexible defect inverse (foundational report lines3690–3730): for each 2<=gamma<=10, mu>=u implies rho>=min((gamma−1)(r−14), (gamma−1)q+min(s,gamma−1)), where max(0,u−4gamma+2)=(gamma+1)q+s, 0<=s<=gamma. Also rho>=u+2−2r. We use only r>=15, and only non-AP supports when using the separate r−14 floor.
7. The sharp four-extreme theorem, published report lines220 onward: for integral F of size d−4 and its four-extreme extension D, restricted-sum hull holes satisfy eta_D+eta_F+g>=2d−10. It is used below only after lattice forcing and overlap.
8. The elementary retained-cover endpoint counts and actual-member losses in the conditional exception companion. Their size-specific constants are freshly derived with d=78. All involved coordinates are nonnegative reals; a matrix solution is never treated as an actual set.

A complete proof relative to these previously proved general lemmas follows. Every additional finite inequality has an optimizer-free exact checker. The theorem is not being made conditional on the vanished N86 source or a historical count.

## 3. Bootstrap and pre-lattice identities

Use the established provisional four-nonzero-extreme peel if a sign is deficient, taking extra points from the available sign. If |B|<=7, the remaining core is one-sided with at least70 nonzero elements; its support has at least1+T_70=2486 points, contradicting s<=24*86+77=2141. A disappearing sign under subsequent provisional peeling is likewise impossible: a one-sided size70 core has at least1+T_69=2416>24*78+77=1949. Thus the actual two-by-two sign peels exist and d=78,e=70,m=69.

The unpaired absolute-value inequality (foundational report lines936–974), combined with the core bound, gives q²<=96e+1073−e²=2893. Since q has the odd parity of m, q<=53, so at least(69−53)/2=8 opposite pairs lie in E. In particular zero is not a diagonal exception and a,b>=8.

Define theta=delta0(P)+delta0(Q)+8−Delta(D), c=2|2D|+18d+85−|FS(D)|, ell1=|FS(D)|−|FS(D1)|−|R(D)|+1, ell2=|FS(D1)|−s−|R(D1)|+1, and g=4d−10−(|R(D)|−|R(D1)|). All are nonnegative: theta counts only surviving diagonal exceptions, the peeling inequalities give ell_i>=0, and there are at most4(d−4)+6 new distinct-element pairs in the first peeled layer. Cancellation gives

    rho+kappa+2theta+c+ell1+ell2+g=22d+97−Lambda=Omega.       (B)

The cancellation does not require a,b>=14; only nonnegativity of rho would require that. Reflection makes a=34−k<=b=35+k. Since b>=35, rho_Q>=0, while rho_P>=−8, so Omega>=−8 implies k<=23 and a>=11. Also each side has its maximum as a diagonal defect, whence rho<=mu.

Once a common lattice with exact hole bounds has been obtained, set C=2m+4e+14−Lambda=−794−I. Delete the maximum from a side X of size r to give Y, and let nu count old defects destroyed. Exact cancellation of mass, excess and defects gives

    R_X=r+rho_X+h_X+2−rho_Y−h_Y−2nu.                       (M)

For r>=15, rho_Y>=0, so R_X<=r+rho_X+h_X+2. For a small side r<=14 use rho_Y>=−8, adding eight to that side and sixteen to the D1 comparison. No integrality of the added peeled points is needed to count at most4e+6 new restricted sums. Therefore

    |FS(D1)|−2s <= C+Omega+rho−mu+2z+epsilon
                <=−207−2I+2z+epsilon,                    (L)

where epsilon=16 only if a<=14, otherwise 0. This bound is pre-G. Whenever it is strict, an off-lattice point of D1\E would give two disjoint s-point supports inside FS(D1), impossible.

For the outer layer, a sufficient strict comparison is Lambda>4d−10+S, where S bounds the available non-rho slack Omega−rho. Indeed the exact first peel and g>=0 imply |FS(D)|−|FS(D1)|<=|R(D1)|+4d−11+S, while |FS(D1)|>=Lambda+|R(D1)|−1. In the main range S<=Omega<=587 and 1226>302+587=889. In small boundaries use the explicit S cap below. This proves D-integrality after the D1 comparison; it also gives the extreme-translate intersections used in Section7.

## 4. Small boundaries a=11,12,13

The freshly computed (a,b,k,I,Omega,S) rows are

    (11,58,23,552,35,43),
    (12,57,22,506,81,89),
    (13,56,21,462,125,133),
    (14,55,20,420,167,167).

The last row is retained for later closure. For a11, a non-AP Q would give rho_P+rho_Q>=−8+53=45>35; hence Q is AP. A larger AP support has at leastT_b+1 points. Since kappa<=S<T_b, residue counting forces P onto its lattice, and the AP-plus-set formula gives h_Q=0,h_P=kappa,z=0 (details in Section5).

For a12 or a13 and non-AP Q, kappa<=S−(b−5)=37 or82, respectively, strictly below T_a−1 (77 or90) and T_b−1. Thus the simultaneous inverse supplies a common lattice and both exact strict hole bounds. If Q is AP use the preceding residue/gap argument.

The conservative D1 upper bounds from (L), using z<=S and epsilon16, are −1209,−1025,−849 in these three rows. The outer comparison margins Lambda−(302+S) are1433,1341,1253. Thus D is integral and the Section7 post-lattice conclusion G146 applies, without having been used to obtain the lattice.

At a11, post-lattice T>=49>S43 excludes the row. At a12, non-AP Q gives T+rho>=49−8+52=93>81; AP Q gives z0 and T>=146>S89. At a13, AP Q again gives T>=146>S133. For non-AP Q, T>=146−2z and rho>=−8+51 force z>=32. The strict inverse upper-hole premise is available for Q. The effective witness (r,beta,C)=(56,5,143) has both strict tests positive and gives mu_Q>=200; the old flexible inverse gives rho_Q>=134. This exceeds Omega−rho_P<=133. Thus all these boundaries are excluded and henceforth a>=14,k<=20, and both rho values are nonnegative.

## 5. AP supports, including all half-step cases

For integer W={w_1<...<w_v} and J=[0,u−1], interval addition gives

    |W+J|=u+v−1+sum_i min(w_(i+1)−w_i−1,u−1).            (A)

On an arbitrary step use (A) separately in each occupied residue class; with t classes the excess is at least(t−1)(u−1). This remains valid while the other set is real/rational, by grouping modulo the stated lattice.

If the larger support is an AP, its length is at leastT_35+1=631>Omega+1. The residue count gives one class, and kappa<T_b precludes any clipped gap in (A), so h_Q=0,h_P=kappa,z0. This includes both-AP cases. Formula(L) is then strict, including epsilon16 at a14, and the outer comparison is strict. Consequently this branch reaches G146 without an inverse or primitive-core premise.

Suppose instead that only smaller U is AP and Q is non-AP. For every k0..20, exact arithmetic gives Omega<2T_a, so V occupies at most two classes modulo the step of U. If there is just one class, (A) permits at most one gap of length>=u. The largest subset-sum gap is max_i(x_i−sum_(j<i)x_j). A positive prefix gap and its reflected gap are distinct unless the gap is final and central; hence a unique gap of length>=u forces the last Q coefficient to exceed the sum of its predecessors. Its final supports are disjoint, giving mu_Q>=T_(b−2), rho_Q>=T_(b−2)+2−2b. Exactly one off-scale Q coefficient yields the same two disjoint copies of the remaining support. In either case retain the essential kappa>=u−1>=T_a. The checked margin

    T_a+T_(b−2)+2−2b−Omega >=501

is positive throughout all possible rows Omega>=T_a (k1..20). Neither exception occurs. The one-class case therefore has h_P=0,h_Q=kappa,z0 and reaches integral D by(L).

With two or more coefficients in the unique nonzero residue, their sum must occupy one of the same two residues, forcing that residue to have order two. Normalize to U=2[0,u−1]. Let w0 be the least odd coefficient of Q, and let t>=2 count odd coefficients. All within-parity gaps are short: a long one would cost an additional u−1 beyond the obligatory two-residue cost u−1, contrary to kappa<2(u−1). Let eta be the combined holes in the two parity-fiber hulls. The two fiber applications of(A), and reflection of their endpoints, give

    kappa=u−1+eta, h_P=u−1,
    h_Q=kappa−u+w0, z=w0−1.                              (H)

These identities do not initially imply h_Q<=kappa. Prove that next. Distinct even and odd coefficients give

    sum Q >=(b−t)(b−t+1)+t*w0+t(t−1).                    (Q)

If w0>u, use w0>=u+1. The derivative of the quadratic after subtracting w0 at t=2 is at least u+7−2b; its minimum across the relevant rows is3, including a14. Thus its minimum for t>=2 is at2. Consequently |V|>=b²−3b+2u+6−kappa, whereas rho_P>=0, delta0(Q)<=b and(B) give |V|<=T_b+Omega+2b−1−kappa. Their difference is at least884. This contradiction proves w0<=u, and(H) now gives h_P,h_Q<=kappa.

If w0>=15, substitute15 for the coefficient of t−1 in(Q) and minimize over real t; then sum Q−w0−T_b>=7b−289/8. But the exact identity mu_Q+kappa=sum Q+u−w0−T_b and the budget bound that expression above by2b+Omega−T_a−3. The minimum contradiction margin is119/8. Hence w0<=13 and z<=12.

Before G, use AP-specific bounds R_P<=2(a+mu_P) and the distinct-integer-generator bound R_Q<=b+mu_Q+h_Q. Formula(H) then yields

    R_P+R_Q<=m+a+mu+kappa−T_a+12.

In the exact comparison |FS(D1)|−2s<=2(R_P+R_Q)+4e+6+ell2−s, substitute s=Lambda+mu+kappa, mu<=rho+2m−4, and rho+kappa+ell2<=Omega once. This gives

    |FS(D1)|−2s<=2393+2a−4T_a−2T_b<=−827.

The outer layer is strict as before, so D is integral and the Section7 G146 conclusion is now valid. In particular

    c<=Omega−T_a−146+3z−(b−5)
      <=Omega−T_a−146+36−(b−5).                          (HC)

Nonnegative right sides occur exactly at k7..15, with respective caps6,16,23,27,28,26,21,13,2. Each is less than78. Section8's conditional elementary half-step lemma excludes all of these, using only the proved integral D, w<=4z<=48, and the even smaller core. Therefore every surviving AP branch has z0. This argument covers a14 also; its half-step cap is negative.

## 6. Both supports non-AP: complete initial alignment

Throughout this section a>=14. Set n(r)=r−5 for r>=21, r−14 for14<=r<=20. The larger-side inverse threshold follows from Omega<T_b−1. A sufficient small-side test is

    mu_P+rho_P+rho_Q > Omega−T_a+2.                       (I)

Indeed the budget gives kappa<=Omega−rho, and(I) gives kappa<u−2 with room to spare. The retained inverse supplies h_P,h_Q<=kappa and the strict h_P<u−1,h_Q<v−1. Substitution of mu_P>=a−3 and rho_X>=n(|X|) proves(I) except at k4..20, exactly17 rows. If(I) actually fails, algebra gives

    rho_Q<=R=Omega−T_a+2−(a−3)−n(a),
    kappa<=Kmax=Omega−n(a)−n(b),
    u<=Umax=Kmax+3,
    v>=Vmin=T_b+b−2, u>=Umin=T_a+a−2.                  (F)

The complete explicit table, all witnesses, and the independent arithmetic replay are in `inverse86/proof_inverse86.md`, `inverse86/arithmetic_tables.md`, and `inverse86/check_inverse86.py`. The following reproduces their mathematical construction rather than treating a numeric pass as applicability.

For k8..20 normalize the integer Q by its intrinsic gcd. It is primitive, so the primitive effective-hole extension applies even before any bound h_Q<v−1 is known. The explicit (beta,C) pairs for k8..20 are

    (8,143),(8,154),(8,162),(8,165),(8,167),(7,162),(7,167),
    (7,156),(6,140),(5,123),(4,99),(3,72),(2,40).

Both strict parameter tests hold in each row, and if h_Q>2beta the resulting mu_Q>=b+C+1 would force rho_Q>=R+1 by the old exact inverse. Therefore h_Q<=H=2beta. Partition U into residues modulo this Q lattice. If it occupied t classes, |U+V|>=u+t(v−1), so kappa>=(t−1)(v−1). The checked Vmin−1−Kmax>0 forces one class; since0 belongs to U, P is on the same lattice.

If diam U>diam V, the endpoint translates V and diam(U)+V would be disjoint, contradicting |U+V|=u+v−1+kappa because Vmin−Umax−Kmax+1>0. Hence diam U<=diam V. The two endpoint hulls of V cover the whole sumset hull; their at most2h_Q missing points give h_P<=kappa+h_Q<=kappa+H. The additional strictly positive margins Vmin−Kmax−H−2 and Umin−H−2 imply both diameters<=u+v−3. Stanchescu's short-diameter theorem now gives exact h_P,h_Q<=kappa, and z<=h_Q<=H<=16. It uses no primitivity of P.

At k4..7 the preceding diameter-order margin fails and is not used. Apply a counted-endpoint bridge with beta=4,4,5,6 respectively. The b,R,j=b−floor(R/(beta−1)) tuples are

    (39,52,22), (40,74,16), (41,93,18), (42,109,21).

If all y_i>=beta+1 for15<=i<=b, rho_Q>R. Choose the last y_j<=beta; the recurrence gives the stated lower bound on j. The counted-hole lemma gives a primitive prefix lattice with at most beta lower holes H0 in[1,2beta] and their reflections. Its prefix is primitive since j elements among j+beta positive positions cannot all be divisible by2 (or a larger integer).

A first subsequent off-scale coefficient would cause disjoint support translates and rho>=T_j−b−1>R; later increments are at leastbeta+1 and cannot undo this. Thus all remaining coefficients are on the prefix scale. Every later y_i<=R+2. If current prefix size t>=j has total L and next coefficient x>=L−4beta, at least L−6beta>=T_t−6beta>t+R+3 points are added above L, exceeding the allowed increment t+1+y_(t+1). Therefore x<=L−4beta−1. Since x>max(prefix)>=t>2beta, the central intervals join and lower holes stay unchanged; reflection handles upper holes. Consequently final Q has h_Q<=2beta and contains[2beta+1,L_Q−2beta−1].

That central interval has length at least v−alpha, alpha=4beta+2. Residue counting aligns P as before. Its AP-plus-set formula yields h_P<=kappa+alpha, because the checked kappa+alpha<v−alpha−1 makes a clipped gap impossible. The checked inequalities Kmax+alpha+2<=Vmin and Umin>=2beta+2 give both diameters<=u+v−3; the short-diameter theorem recovers h_P,h_Q<=kappa and z<=2beta. The strict bridge inequalities and all finite t=j..b−1 are explicitly checked. No G, D-integrality, or primitive P is used anywhere in this section.

## 7. Force the layers, propagate holes, then use G146

Every remaining case now has a common core lattice and the exact hole bounds. AP cases with z0 or the excluded half-step construction already reach integral D. For both-nonAP repaired cases, z<=16 makes(L) strict; at the a14 boundary z<=4 and the required +16 is retained.

For unrepaired strict-inverse cases a>=15, (L) is strict whenever z<=103+I. If it is not yet strict, integer z>=Z=104+I. Since kappa>=z and rho>=n(a)+n(b), the budget excludes k15..19; the a14 case is separately strict from z<=kappa<=167 and(L) with epsilon16. Thus only k0..14 remain, precisely30 choices of which side's last supports might be disjoint. Such a large-hole branch cannot have arisen from an AP or dense repair, hence both original strict inverse upper-hole bounds are available.

If the last two supports of a side with r coefficients were disjoint, mu_X>=T_(r−2), so rho_X>=T_(r−2)+2−2r. Add kappa>=Z and the other side's non-AP floor. This already contradicts(B) except possibly the smaller side at k1..10. There the other Q support has strict holes Z<=h_Q<v−1. Effective-hole witnesses (beta,C), in k order, are

    (3,51),(5,79),(6,100),(7,112),(7,119),
    (7,119),(6,114),(5,100),(4,81),(3,55).

All satisfy Z>2beta and both strict tests. Their old-rho lower bounds are48,69,85,96,102,103,99,90,76,57. In each of these ten rows the final budget contradiction margin is1; all other oriented rows have larger positive margins. The table checks all30, not just the potentially difficult ten.

Thus both actual final support pairs intersect. Their maximum-deleted hulls cover the entire side hull, giving h_X<=2h_Y. Equation(M), rho_Y>=0 and nu>=0 improve to R_X<=r+rho_X+h_X/2+2. The original comparison consequently becomes

    |FS(D1)|−2s<=C+2rho−mu+z+ell2
               <=C+Omega+rho−mu<=−207−2I<0,

using z<=kappa and(B) only once. This is a pre-G argument. It proves D1-integrality; the outer comparison proves D-integrality. The same strict cardinality comparisons force intersections between the extreme FS(E) translates in FS(D1) and between the extreme FS(D1) translates in FS(D).

Now the lattice argument may count holes. The two extreme core translates cover the whole D1 subset-sum hull and leave at most2z holes. If their endpoint separation is u2, their union has at least s+u2−z points. The exact peel gives |FS(D1)|=s+u2−eta2+ell2, hence eta2<=z+ell2, where eta2 counts holes of R(D1). Repeating at the outer layer gives w<=4z and eta1<=2z+ell1 for R(D). Only now apply the integral sharp four-extreme theorem:

    eta1+eta2+g>=2d−10=146.

It follows that T=kappa+ell1+ell2+g>=kappa+146−3z>=146−2z. Also T>=kappa>=z, so3T>=146 and T>=49. Combining with(B) gives c+rho+T<=Omega. These deductions justify every earlier reference to the post-lattice conclusion, on a branch only after its own lattice and overlap arguments were complete.

## 8. Conditional elementary structural exceptions

The full explicit actual-set proof and pure integer row checker are in `ap_exception86/conditional_exception86.md` and `ap_exception86/check86_elementary.py`. Here is the logical linkage and complete cover.

Whenever the branch has c<d=78, every one of the18 ordinary covering units contributes: an empty unit alone would cost78. Therefore j0 and delta=c. All four own centers b_i=c_p+p_i contribute and are integral, since both their target and D support are integral. With c_p=p1−p2−p3−p4, the exact identity c_p=−b1+b2+b3+b4 gives every p_i=b_i−c_p integral. The reflected q identity does the same. This proves outer integrality without core primitivity or leading-2D contribution.

A nonempty first paired unit has some actual contributing component. Reflection makes a p component the selected one; both oriented side sizes are explicitly included after this reflection. The covering lemma leaves branches A/B and either selected second-pair contributor, giving four covering modes. The companion reconstructs actual rows: integral outer/inner order, R>=r, main mass S>=T_r+M+3R+6, actual component endpoint losses at d/(d−1)=78/77, sum of actual losses<=c, K=|2D|<=2M_P+2M_Q+1, and the upper half of the exact identity

    S_P+S_Q+c−2K=18*78+84+w=1488+w.

No leading endpoint row is used. If the smaller core is nonprimitive (or even in the half-step normalization), replace its ordinary rank/mass facts by R>=2r and core mass>=2T_r, since its r distinct positive integer coefficients are all multiples of an integer>=2. These are valid even if its subset-sum support is not AP. All loss and unused auxiliary coordinates have joint actual nonnegative realizations as described in that companion. The supplied four retained integer multiplier vectors are input witnesses; each coefficient and right side is checked anew against these freshly constructed SIZE86 rows. They are not old N86 vectors or receipts.

Three independently derived finite families suffice:

* Larger AP, smaller nonprimitive, a>=15: z0, h_P=kappa>=T_a+mu_P, rho_P,rho_Q>=0 give c<=Omega−146−T_a. Nonnegative cases are exactly k7..15, with caps7,18,26,31,33,32,28,21,11, all<78. The smaller side need not be AP. Nine size pairs, two orientations and four modes give72 systems; the minimum strict contradiction is283.
* Half-step from Section5: k7..15, the nine caps(HC), z<=12 and w<=48. Use nonprimitive smaller-core rank/mass, the relaxed upper cardinality1488+48, and the proved cap. Another72 systems, minimum strict contradiction288. The uniform z12 relaxation includes every actual allowed smaller z; supplemental exact even-z checks are not needed for completeness.
* Remaining a14 with larger Q AP: z0 and rho>=0 give c<=167−146=21<78. No nonprimitive assumption is made. The two orientations(14,55),(55,14), four modes, ordinary rank/mass, and w0 give8 systems, minimum strict contradiction295.

These152 systems constitute a fresh structural exception cover. Its number is an output of this derivation, not an inherited premise. The four integer row combinations sum to a componentwise nonnegative coefficient vector with a strictly negative right-hand side, impossible for the nonnegative actual-set coordinates. Therefore every listed branch is excluded.

## 9. Eliminate a14 and prove individual primitivity

The a14/AP-Q branch and the half-step branch are already excluded by Section8. If Q is non-AP and P is AP, the one-residue case has z0, h_Q=kappa and thus T>=146; with rho_Q>=50 this exceeds Omega167. If both supports are non-AP, its failed-inverse repaired row has z<=4, giving T+rho>=146−8+50=188>167. If its sufficient inverse test holds, then both strict upper-hole bounds apply. The post-lattice budget gives z>=ceil((146+50−167)/2)=15. The strict effective witness(r,beta,C)=(55,7,202) gives mu_Q>=258 and oldrho_Q>=180>167. Thus a14 is excluded. The complete reflected range is now0<=k<=19, a>=15,b>=35, or15<=a<=54 without reflection.

The strict simultaneous-inverse branches are individually primitive: a coefficient gcd>=2 gives h_X>=(|FS(X)|−1), contrary to the strict hole bound.

In a dense-Q repair Q is primitive by construction. Suppose P had gcd g>=2 on this lattice. Both supports are non-AP. On its intrinsic P lattice let h0 be its hull holes; h0>=1, since h0=0 would make its support AP. Exact rescaling gives

    h_P=(g−1)(T_a+mu_P)+g*h0>=T_a+mu_P+2>=T_a+a−1.

Using kappa>=h_P, z<=H, and both rho floors in the post-G budget gives

    Omega >= c+n(a)+n(b)+T_a+a−1+146−3H.                 (P)

The explicit repair-table margins show(P) impossible in every repaired row except equality at k11,12. Equality forces g2, h0=1, mu_P=a−3, rho_P=a−5, rho_Q=b−5, c0, z=h_Q=H16, and kappa=h_P. But the intrinsic P span is T_a+mu_P+h0=297 or273, respectively, an odd integer. Subset-sum reflection pairs each intrinsic hole h with L−h; when L is odd there is no integer fixed point, so exactly one hole is impossible. This excludes the equalities. Independently, a unique hole is a unique central gap; the largest-gap argument would force final disjoint supports and mu_P>=T_(a−2)>a−3, giving the same contradiction. Thus P is primitive.

For surviving AP branches z0: if the smaller support defines the unit AP step, it is primitive because its support contains1, and the larger side is primitive because h_Q=kappa<=Omega<T_b<=v−1. If the larger AP defines the unit step, it too is primitive, while any nonprimitive smaller P was excluded by Section8's first family. All AP/non-AP and half-step alternatives have now been covered.

This proves the statement relative to the explicitly listed retained general lemmas. There is no remaining claimed inference from SIZE87 parameters alone. Independent mathematical review of the fresh assembly and row applicability remains required before an endpoint adapter is adopted.

## 10. Reproduction and limitations

Run the three standalone checkers with Python standard library only:

    python -I -S -B check_bootstrap_ap86.py
    python -I -S -B inverse86/check_inverse86.py
    python -I -S -B ap_exception86/check86_elementary.py

The first derives constants, bootstrap, boundary and AP inequalities. The second checks explicit inverse witnesses, bridges, all30 overlap alternatives and primitivity equalities without discovering models. The third reconstructs only the finite elementary structural-exception rows and densely sums the retained positive integer multipliers. Their successful arithmetic is necessary but does not replace the mathematical applicability proof above and in the companions. No optimizer, SciPy, endpoint adapter, canonical-root enumeration, numerical proof campaign, or lost-receipt replay is part of this work.
