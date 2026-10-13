# Fresh SIZE85 inverse alignment and final-support overlap

This companion proves the inverse portion of a SIZE85 structural argument.
Its general mathematical inputs are the previously established covering and
peeling identities, prefix defect recurrence, counted-hole lemma, effective
hole lemma, flexible defect inverse, and Stanchescu's two distinct-set theorems.
It additionally invokes the SIZE85 no-empty-unit obstruction after lattice
forcing and G144; that obstruction must be proved in the common source.
The checker `check85_inverse.py` checks only the explicit finite arithmetic.

## 1. Parameters and exact pre-lattice budget

Use m=68,d=77,e=69,G=144. After reflection a=34-k,b=34+k,I=k².
Put T_r=r(r+1)/2, Lambda=1+T_a+T_b=1191+I, Omega=600-I, and

    C=2m+4e+14-Lambda=-765-I, C+Omega=-165-2I.

For U=FS(P),V=FS(Q), write u=1+T_a+muP,v=1+T_b+muQ and
kappa=|U+V|-u-v+1. The exact budget is

    rhoP+rhoQ+kappa+2theta+c+ell1+ell2+g=Omega.

The non-AP support floors used below are n(r)=r-5 for r>=21 and
n(r)=r-14 for 14<=r<=20. At r=13, the sharper non-AP floor is -1.
All mu values are nonnegative, and non-AP mu_X>=r-3. Also rho<=mu.
The main range is a>=15, k0..19. The a14 and a13 boundaries are included
and closed explicitly below; smaller boundaries are treated in the bootstrap.

The larger-side sufficient strict inverse condition is automatic because
Omega-n(a)-n(b)<T_b+b-4=v_min-2 for every k0..21.
Do not replace this with Omega<T_b-1: that unnecessarily stronger inequality
is false at balanced k0, where Omega=600,T34-1=594.

The sufficient small-side condition is

    muP+rhoP+rhoQ>Omega-T_a+2.

Its floor margin is positive exactly at k0,1,2 and nonpositive at k3..21.
Whenever the actual condition fails, the following fresh cardinality bounds hold:

    rhoQ<=R=Omega-T_a+2-(a-3)-n(a),
    kappa<=Kmax=Omega-n(a)-n(b), u<=Umax=Kmax+3,
    v>=Vmin=T_b+b-2, u>=Umin=T_a+a-2.

## 2. Two counted-endpoint repairs

The original repair starts with rho14>=0. Given rhoQ<=R, fix beta>=3
with (beta-1)(b-14)>R. Some index j>=15 has y_j<=beta; take the last one.
The recurrence rho_i>=rho_(i-1)+y_i-2 and nonnegative prefix defects give

    j>=j0=b-floor(R/(beta-1)).

The counted-hole lemma applies if j0>=2beta+5. It supplies, on an intrinsic
prefix lattice, a deleted interval with at most beta lower holes in [1,2beta]
and their reflections. That prefix is primitive on its own lattice because
j elements among j+beta positive positions cannot all be divisible by 2.

Assume T_j0-b-1>R. A first later coefficient off this lattice has disjoint
support translates and raises rho above R; the subsequent increments, all
at least beta+1, cannot undo this. Thus every coefficient is on that lattice.
Every later increment is at most R+2. If a current m-prefix has sum L and
the next coefficient x satisfies x>=L-4beta, the new translate adds above L
at least min(x,L+1)-2beta>=L-6beta>=T_m-6beta points.
When T_m-6beta>m+R+3, this exceeds its allowed increment.
Therefore x<=L-4beta-1. Also x>max(prefix)>=m>2beta.
The central intervals join, the lower holes remain unchanged, and reflection
supplies the upper holes. Induction gives final hQ<=H=2beta and a central
interval [2beta+1,L_Q-2beta-1].

The strengthened repair uses a non-AP prefix floor, which is essential in
several SIZE85 rows. Suppose the final Q support is non-AP, rhoQ<=R, and
q>=20 satisfies T_q-b-1>R. Then every prefix of size at least q is non-AP.
Indeed, if a last AP-support prefix had size l>=q, the next support must
break the progression by disjoint translates. At that step y>=T_l-l.
Every later increment is positive by the zero-increment equality theorem.
The prefix recurrence, starting from rho_l>=0, gives

    rhoQ>=T_l-b-1>=T_q-b-1>R,

a contradiction. Hence rho_q>=n(q), and rho_j>=j-5 at j>=max(q,21).

If n(q)+(beta-1)(b-q)>R, there is a last j>=q+1 with y_j<=beta.
The later increments yield

    R>=rho_j+(beta-1)(b-j)
      >=(j-5)+(beta-1)(b-j),

and thus

    j>=j0=max(q+1,21,ceil(((beta-1)b-R-5)/(beta-2))).

Now apply exactly the same counted-hole, off-scale, and bridge arguments.
This strengthens the index bound without imposing a new hypothesis on Q.

## 3. All failed-inverse rows acquire a common lattice

The explicit choices (k,b,R,beta,q,j0,H) are:

|k|b|R|beta|q|j0|H|
|---:|---:|---:|---:|---:|---:|---:|
|3|37|43|3|14|16|6|
|4|38|69|4|14|15|8|
|5|39|92|6|14|21|12|
|6|40|112|6|14|18|12|
|7|41|129|7|14|20|14|
|8|42|143|8|14|22|16|
|9|43|154|8|14|21|16|
|10|44|162|8|20|24|16|
|11|45|167|8|14|22|16|
|12|46|169|8|14|22|16|
|13|47|168|7|21|22|14|
|14|48|173|7|21|22|14|
|15|49|166|7|14|22|14|
|16|50|156|7|14|24|14|
|17|51|143|6|14|23|12|
|18|52|127|5|14|21|10|
|19|53|108|5|14|26|10|
|20|54|86|4|14|26|8|

Every strict tail/off-scale/bridge margin and every intermediate m in
j0..b-1 is checked with integers. For k10, T20-b-1-R=3; for k13,k14,
T21-b-1-R=15,9. These are the three uses of the strengthened repair.

Residue counting gives kappa>=(t-1)(v-1) if U occupies t residue classes
modulo Q's prefix lattice. Since Kmax<Vmin-1, U has only one class, and
0 in U places P on the same lattice. Set alpha=4beta+2. Q's central
interval has length l=L_Q-4beta-1=v+hQ-alpha>=v-alpha.
Apply the AP-plus-set formula to that interval and U. Since it is a subset
of V, its clipped gap sum is at most kappa+alpha. The checked inequality

    Vmin-Kmax-2alpha-1>0

makes kappa+alpha<l-1, so no gap can be clipped; hence hP<=kappa+alpha.
The further positive inequalities

    Vmin-Kmax-alpha-2>0, Umin-H-2>0

give both diameters at most u+v-3. Stanchescu's short-diameter theorem
therefore gives the exact hP,hQ<=kappa, and z=hP+hQ-kappa<=H.
No individual primitivity of P has been assumed.

The pre-G D1 comparison is bounded by -165-2I+2H, with the required +16
correction at a14; every row is strict. The outer comparison is strict
since 1191>4*77-10+600. This proves D1,D integral and the extreme support
intersections before any integer-hole G144 estimate is used.

At a13/b55, the actual failed sufficient test gives rhoQ<=61. Normalize
Q by its intrinsic gcd. The primitive effective-hole witness
(r,beta,C_h)=(55,2,52) has (K,D,M,J)=(11,63,13,13), strict margins23,14,
and forces muQ>=108, rhoQ>=62 whenever hQ>4. Hence hQ<=4.
Residue counting, endpoint hulls and the same short-diameter theorem give
hP,hQ<=kappa and z<=4; all required dense-diameter margins are positive.
The D1 comparison with +16 is -1023. After G144,
rhoP+rhoQ+T>=-1+50+144-8=185>159, so this boundary is impossible.

The remaining a13/b55 branch is the actual sufficient strict inverse
branch. Its strict hole bounds give individual primitivity on the joint
lattice. Here kappa<=159-(-1)-50=110, so the rough D1 comparison is
at most -165-2*441+2*110+16=-811<0; the outer comparison is strict as
above. Thus lattice forcing and G144 are established without using any
later hole estimate. The post-G budget gives

    -1+50+144-2z<=159,

so z>=17 and hQ>=z>8. The fresh primitive effective-hole witness
(r,beta,C_h)=(55,4,119) has (K,D,M,J)=(17,136,19,19), strict margins
12,34, and forces muQ>=175 whenever hQ>8. The flexible defect inverse
then gives rhoQ>=113 (the g7,8,9,10 rows each give 113). Since T>=48,

    rhoP+rhoQ+T>=-1+113+48=160>159.

Consequently both actual inverse branches at a13 are excluded.

## 4. Large-hole final-support overlap: all 32 orientations

For unrepaired strict-inverse main branches, D1 is immediately strict when
z<=82+I. Therefore only z>=Z=83+I needs an extra argument.
Every repaired branch has z<=16<Z and cannot enter this large-hole case.
The strict inverse upper-hole bounds hX<|FS(X)|-1 are retained here.
The budget kappa>=z and both non-AP floors exclude k16..19 directly.
The remaining k0..15 have 32 oriented possible disjoint-final-support sides.

If the side X has r coefficients and its final prefix translates are
disjoint, muX>=T_(r-2), so rhoX>=T_(r-2)+2-2r.
The elementary contradiction margin is

    T_(r-2)+2-2r+n(s)+Z-Omega.

It is positive in 18 orientations. The remaining 14 comprise P at k0..12
and also Q at balanced k0. Put R=Omega-(T_(r-2)+2-2r)-Z; the budget
forces the other side's defect at most R. Apply the strengthened repair
with q20 using the following exact (k,s,R,beta,j0) choices:

|k|s|R|beta|j0|
|---:|---:|---:|---:|---:|
|0|34|55|5|26|
|1|35|83|7|25|
|2|36|106|8|24|
|3|37|124|8|22|
|4|38|137|9|24|
|5|39|145|9|24|
|6|40|148|9|24|
|7|41|146|8|23|
|8|42|139|8|25|
|9|43|127|7|26|
|10|44|110|6|27|
|11|45|88|5|29|
|12|46|61|4|36|

All strict margins hold, including T20-s-1>R; the final support has
at most 2beta<=18 holes, whereas h_other>=z>=Z>=83, a contradiction.
Thus both sides' actual final prefix support translates intersect.
This is a fresh endpoint argument; the weaker effective-hole tests alone
do not close k2..8 at SIZE85.

Let Y remove the largest coefficient from an r-side X. Intersecting final
support hulls cover the full side hull, so hX<=2hY. The exact maximum-deletion
identity, with rhoY>=0 and destroyed-defect count nu>=0, gives

    max X<=r+rhoX+hX/2+2.

The common D1 comparison becomes

    |FS(D1)|-2s<=C+2rho-mu+z+ell2
               <=C+Omega+rho-mu<=-165-2I<0.

Here the one budget is used via rho+kappa+ell2<=Omega and z<=kappa.
Together with the outer comparison, this finishes pre-G non-AP lattice
forcing without circular use of G144.

## 5. Post-G individual primitivity and a14 closure

Only after the proved lattice and overlap steps use

    T>=kappa+144-3z, c+rhoP+rhoQ+T<=Omega, w<=4z.

In a strict simultaneous-inverse branch, an individual gcd>=2 would imply
hX>=|FS(X)|-1, contradicting the strict inverse upper-hole bound.
In an endpoint-repaired branch, Q is primitive on the constructed prefix
lattice. If P had gcd g>=2, its intrinsic support is non-AP and has h0>=1.
Rescaling gives

    hP=(g-1)(T_a+muP)+g*h0>=T_a+a-1.

Thus

    c<=Omega-n(a)-n(b)-T_a-a+1-144+3H.

The exact caps for k3..20 are

    -119,-88,-54,-35,-13,6,16,23,27,28,20,24,16,5,-15,-38,-58,-87.

Negative caps exclude immediately. In the remaining rows c<=28<77,
so all 18 ordinary covering units contribute (j0), and w<=4H<=64.
The SIZE85 no-empty-unit obstruction, valid for w<=104, excludes these.
Hence P is individually primitive in every surviving repaired main row.

For a14/b54, the repaired branch has z<=8, so
c<=200-49-(144-16)=23<77 and w<=32; j0 excludes it entirely.
In the strict-inverse branch, if z>=13, the witness
(r,beta,C_h)=(54,6,168) has (K,D,M,J)=(19,187,22,22), strict margins11,43.
It yields muQ>=223, rhoQ>=153. Since T>=48, the budget would require
200>=153+48=201. Therefore z<=12. Then c<=31<77,w<=48, and j0 again
excludes the branch. This closes a14 without using P primitivity first.

## 6. Verification boundary

Run `python -I -S -B check85_inverse.py`. It reconstructs all SIZE85
parameters, all 18 endpoint inverse rows, both a13 effective
boundary, all 32 overlap orientations and 14 endpoint repairs, nonprimitive
caps, and the a14 effective closure. The mathematical passage from actual
sets to the displayed inequalities, the retained published general theorems,
the bootstrap/AP branches and the no-empty-unit obstruction remain written
proofs. No SIZE86 row combination or old exception census is reused.
