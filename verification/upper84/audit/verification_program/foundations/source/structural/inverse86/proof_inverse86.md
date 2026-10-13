# Conditional SIZE86 inverse-gap repairs and large-hole overlap

Status: conditional proof companion for the independently reviewed SIZE86 structural theorem. The main range assumes a,b>=15; the boundary a=14,b=55 is treated separately. The post-G individual-primitivity argument is separated from pre-lattice work.

## 1. Scope, inputs, and source boundary

Use the established initial integralization, covering/peeling identities, global/prefix defect inequalities, non-AP stability `mu_X>=r-3`, and non-AP defect floor

    n(r)=r-5 for r>=21, n(r)=r-14 for 14<=r<21.

The conditional parameters are

    m=69, d=78, e=70, G=146,
    a=34-k, b=35+k, I=k(k+1),
    Lambda=1+T_a+T_b=1226+I,
    Omega=22d+97-Lambda=587-I,
    C=2m+4e+14-Lambda=-794-I,
    C+Omega=-207-2I.

Let `U=FS(P)`, `V=FS(Q)`, `u=1+T_a+muP`, `v=1+T_b+muQ`, and `kappa=|U+V|-u-v+1`. Subset-sum reflection identifies the sum and difference cardinalities. The exact pre-lattice budget is

    rhoP+rhoQ+kappa+2theta+c+ell1+ell2+g=Omega.

All terms used as slacks are nonnegative, and `rhoP+rhoQ<=muP+muQ`. Once a lattice is established, write `hP,hQ` for support hull holes, `z=hP+hQ-kappa`; the exact inverse conclusion is `hP,hQ<=kappa`, hence `0<=z<=min(hP,hQ)`.

The foundational excerpts supply the counted-hole, endpoint-bridge, effective-hole and flexible-inverse lemmas. `foundations/lattice_lemmas.md` states the primitive effective-hole extension and the short-diameter Stanchescu theorem. Original source hashes and portable-file transformations appear in `source_provenance.json`.

The checker uses fixed explicit witnesses, reconstructs all threshold and inverse arithmetic with Python integers, and imports no prior checker.


## 2. Complete failed sufficient inverse range

Assume both supports are non-AP and `a,b>=15`, so `0<=k<=19`. The large-side strict inverse threshold is automatic since `Omega<T_b-1` in every row. The deliberately conservative sufficient small-side test is

    muP+rhoP+rhoQ>Omega-T_a+2.

Its lower-floor test has margin

    F=(a-3)+n(a)+n(b)-(Omega-T_a+2).

The exact full table in `arithmetic_tables.md` gives positive margins for `k=0,1,2,3` and nonpositive margins for every `k=4,...,19`, with no other possibility. Thus there are sixteen main conditional failed-test rows. The boundary `k20,a14,b55` adds a seventeenth, with `F=-3`.

When the actual sufficient test fails, not merely its floor test, it gives

    R = Omega-T_a+2-(a-3)-n(a) >= rhoQ,
    Umax = Omega-n(a)-n(b)+3 >= u,
    Kmax = Omega-n(a)-n(b) >= kappa,
    Vmin = T_b+b-2 <= v,
    Umin = T_a+a-2 <= u.

These use only pre-lattice cardinalities. In particular the boundary cap is `R=53`, not56.

## 3. Generic effective-hole / old-rho witnesses

For each fixed witness `(r,beta,C_h)`, define

    K=max{j>=3:j(j-3)/2<=C_h+1},
    D=C_h+max(3,K), E=D+1,
    M=min{m>=2beta:T_m-6beta>m+1+E},
    J=max(K+1,2beta+5,M).

The two required strict margins are `(r-J+1)beta-D>0` and `T_(J-1)-1-D>0`. This `M` is exactly the foundational endpoint-bridge threshold written without radicals. The original effective-hole lemma states

    2beta<h<|FS|-1  =>  mu>=r+C_h+1.

On a specified primitive integer lattice, its upper-hole hypothesis may be replaced by primitivity. That upper-hole condition was used only to infer primitivity in the proof. All counted-hole, tail, off-scale, and bridge steps then remain valid. The source discussion is included in `foundations/lattice_lemmas.md`; the extension is not asserted for an arbitrary nonprimitive lattice.

At an integer lower bound `mu>=u0`, use the old flexible inverse for each `gamma=2,...,10`. Writing

    max(0,u0-4gamma+2)=(gamma+1)q+s, 0<=s<=gamma,

it gives

    rho >= min((gamma-1)(r-14), (gamma-1)q+min(s,gamma-1)).

Maximize these with the applicable non-AP floor `r-14` and `u0+2-2r`. Every use here has `r>=15`, and every parameter is within the retained lemma's range. The table lists every maximizing gamma, not just a claimed optimized value.

Normalize the initial integralized Q by its own gcd. This makes Q primitive while P may initially be real/rational. For all seventeen `k4..20` the table supplies an effective witness whose forced old-rho value is exactly `R+1`; hence `hQ<=2beta` on this intrinsic Q lattice. The small `(beta,C_h)` pairs are

    k4..7: (3,55),(5,84),(6,108),(7,127),
    k8..12: (8,143),(8,154),(8,162),(8,165),(8,167),
    k13..16: (7,162),(7,167),(7,156),(6,140),
    k17..20: (5,123),(4,99),(3,72),(2,40).

The first four witnesses are sound, but do not by themselves complete the diameter recovery: the diameter-order margins are respectively `-201,-140,-74,-3`. These are not silently treated as positive. Section5 supplies separate endpoint repairs.

## 4. Dense-summand diameter recovery for k8..20

Use the preceding Q witnesses, with `H=2beta`. Residue counting gives

    kappa >= (number of occupied U residues-1)(v-1).

The checked positive margin `Vmin-1-Kmax` forces P onto Q's primitive lattice. Write `A=diam U,B=diam V`.

If `A>B`, the two endpoint translates `V` and `A+V` are disjoint, so `|U+V|>=2v`. The positive margin `Vmin-Umax-Kmax+1` contradicts this, giving `A<=B`. The endpoint hulls `[0,B]` and `[A,A+B]` then cover the full sum hull. Each endpoint support misses at most `hQ` points from its own hull, giving

    |U+V|>=A+B+1-2hQ=A+v-hQ,
    hP=A-u+1<=kappa+hQ<=kappa+H.

The remaining checked margins

    Vmin-Kmax-H-2>0, Umin-H-2>0

make both support diameters at most `u+v-3`. Stanchescu Theorem4's exact short-diameter bound is `max(A,B)<=u+v-2-delta`, with `delta=1` when the diameters agree and0 otherwise. Our stronger bound satisfies both alternatives. That theorem requires no unproved primitivity for P and yields `hP,hQ<=kappa` exactly. Consequently `z<=hQ<=H`.

All four margins and every strict effective parameter margin are listed. Their minima across `k8..20` are respectively530,73,513,111. The maximum H is16.

## 5. Generalized counted-endpoint repair for k4..7

These four rows use `(b,R,beta)=(39,52,4),(40,74,4),(41,93,5),(42,109,6)`, independently of the effective witnesses in §3. Put

    j0=b-floor(R/(beta-1)).

The values are `j0=22,16,18,21`. The table verifies:

    R<(beta-1)(b-14), j0>=2beta+5,
    T_j0-b-1>R,
    T_m-6beta>m+R+3 for every j0<=m<b,
    j0>2beta.

Let `y_i` be the nonnegative support-excess increments. If all `y_i>=beta+1` for `15<=i<=b`, the recurrence `rho_i>=rho_(i-1)+y_i-2`, beginning with `rho14>=0`, contradicts the first strict inequality. Choose the last `j>=15` with `y_j<=beta`. The later increments give `j>=j0`.

The counted-hole lemma supplies a normalized deleted interval prefix

    Q_j=t([1,j+e]\D), e=y_j<=beta, |D|=e,
    FS(Q_j/t)=[0,L]\(H0 union(L-H0)),
    H0 subset [1,2beta], |H0|<=beta.

This prefix is primitive in its own scale, since any gcd>=2 could retain at most `floor((j+e)/2)<j` positions. A first later coefficient off this scale has disjoint final translates and forces `rho_i>=T_j-b-1>R`. Later increments are all at least `beta+1`, so rho cannot fall back to R. Thus every later coefficient stays on the prefix's primitive lattice.

For every later step, monotonicity after j and prefix nonnegativity give `y_i<=R+2`. Suppose a current m-prefix has the stated endpoint support and next integral coefficient x. If `x>=L-4beta`, at least

    min(x,L+1)-2beta >= L-6beta >= T_m-6beta

points in the new translate lie above L. The strict bridge inequality says this exceeds the allowed support increment `m+1+y_(m+1)<=m+R+3`. Therefore `x<=L-4beta-1`. Also `x>max Q_m>=m>2beta`. The two central intervals join or are adjacent, while the lower holes remain H0 and reflection supplies the upper holes. Induction proves the final endpoint state, with total holes at most `H=2beta`.

Put `alpha=4beta+2`. Its central interval has length

    l=L-4beta-1=v+hQ-alpha>=v-alpha.

Residue counting, with `Kmax<Vmin-1`, aligns P. The AP-plus-set gap formula applied to this central interval gives

    sum min(g_i-1,l-1)<=kappa+alpha.

The checked margin `Vmin-Kmax-2alpha-1>0` ensures `kappa+alpha<l-1`; hence all terms are uncapped and `hP<=kappa+alpha`. The further margins `Vmin-Kmax-alpha-2>0` and `Umin-H-2>0` again give both diameters at most `u+v-3`. Stanchescu Theorem4 sharpens to `hP,hQ<=kappa`, and `z<=H`.

The final H values are8,8,10,12. All hypotheses are proved before any use of G146.

## 6. Pre-G layer forcing and the conditional boundary

In every repaired main row, the established one-budget comparison gives

    |FS(D1)|-2s <= C+Omega+rho-mu+2z
                 <= -207-2I+2H <0.

The table lists the exact bounds. For the boundary `a14,b55,k20`, use the mandatory maximum-deleted small-prefix correction `+16`, giving `-1023<0`. The other peeled layer is strict because `1226>4*78-10+587`. Thus the repaired cases have the required layer integrality and extreme-translate overlap before G is used.

For the boundary alone, once G is valid, `T>=146-2z`, `rhoQ>=50`, and `rhoP>=0` give `z>=15` from the budget Omega167. But the repaired branch gives `z<=4`. This excludes the failed-test boundary branch. The corresponding strict-inverse boundary branch is proved in `STRUCTURAL86.md`; it is not silently covered by the failed-test assumption here.

## 7. Large-hole final-support overlap: thirty complete cases

The ordinary main-range comparison is strict for `z<=103+I`. Thus the only remaining large-hole threshold is

    z>=Z=104+I.

This section assumes a common core lattice with both supports non-AP. It applies to the strict inverse branches: every failed-test repaired branch has `z<=16<Z`, so a large-hole branch cannot be a repair. Hence both sides retain the original strict inverse hole bounds `hP<u-1,hQ<v-1`, and the original effective-hole lemma is legitimate without the primitive extension.

The budget `kappa>=z`, together with both non-AP floors, rules out every `k15..19`. The remaining range is exactly `k0..14`. Both orientations are checked, producing thirty cases; in `k14` the side of size20 correctly uses `n(20)=6`, not15.

If the final translates for an r-side X were disjoint, then

    muX>=T_(r-2), rhoX>=T_(r-2)+2-2r.

With the other side of size s, the naive lower-minus-budget margin is

    T_(r-2)+2-2r+n(s)+Z-Omega.

It is strictly positive in twenty of the thirty cases. The only missing cases have the smaller P side disjoint and `k1..10`; their base margins are `-16,-36,-51,-61,-66,-66,-61,-51,-36,-16`.

For those ten rows, Q has `hQ>=z>=Z>2beta` and the strict upper-hole bound. The effective-hole/old-rho witnesses are

    k1..10: (beta,C_h)=
    (3,51),(5,79),(6,100),(7,112),(7,119),
    (7,119),(6,114),(5,100),(4,81),(3,55).

Their forced Q rho floors are48,69,85,96,102,103,99,90,76,57. Each raises the contradiction margin to exactly1. Every effective parameter, strict margin, old-rho gamma, base margin, and resulting margin appears in the full table. Thus the actual final supports intersect for both sides in every large-hole case.

Write R_X=max X, and let Y remove the maximum from X. The intersecting final prefix hulls cover the full X hull, so `hX<=2hY`. The exact maximum-removal recurrence, together with `rhoY>=0` and nonnegative destroyed defects, gives

    R_X<=r+rhoX+hX/2+2.

The established D1 comparison therefore becomes

    |FS(D1)|-2s<=C+2rho-mu+z+ell2
               <=C+Omega+rho-mu<=-207-2I<0.

The budget is used once via `rho+kappa+ell2<=Omega` and `z<=kappa`. Again G has not been used to prove its own lattice hypotheses. Together with the other-layer inequality above this finishes the conditional non-AP pre-G lattice work.

## 8. Post-G individual primitivity in every repaired main row

This addendum assumes that the preceding integrality and the established propagation theorem have legitimately supplied

    T>=kappa+146-3z, c+rhoP+rhoQ+T<=Omega.

Q is already primitive on the constructed lattice. The naive bound `kappa<=Omega-(146-3H)-n(a)-n(b)` need not be below T_a: its margins fail at k8..15. Those failures are recorded, not hidden.

Suppose P has gcd `gP>=2`. On its own primitive lattice write `h0` for its support holes. P is non-AP, so `h0>=1`. Since support cardinality is invariant,

    hP=gP(u-1+h0)+1-u
      =(gP-1)(u-1)+gP*h0
      >=T_a+muP+2>=T_a+a-1.

Combining this with `hP<=kappa`, the post-G budget, and `z<=H` gives

    T_a+a-1+146-3H+n(a)+n(b)+c<=Omega.

The table shows strict contradiction in every repaired row except k11 and k12, where the margin is exactly0. In either equality case all inequalities must be equalities: `c=0,z=hQ=16`, `gP=2,h0=1`, `muP=a-3`, `rhoP=a-5`, `rhoQ=b-5`, and `kappa=hP=T_a+a-1`. The intrinsic P hull spans are respectively

    k11: a23, muP20, span=T23+20+1=297,
    k12: a22, muP19, span=T22+19+1=273.

Both spans are odd. Subset-sum reflection pairs every intrinsic integer hole with a distinct hole when the total span is odd. Thus `h0=1` is impossible. This proves P primitive in both remaining rows, without any additional finite certificate system.

As an independent elementary alternative, any integer subset-sum support with exactly one hull hole has disjoint final translates. To see this, let j be the first coefficient violating interval coverage, and L the sum of its predecessors. Previous subset sums fill `[0,L]`, and `L+1` is a permanent hole. Since the hole is unique and reflection preserves it, the final sum is `2L+2`. But the violating coefficient is at least `L+2`, so equality forces it to be final. Hence `mu>=T_(a-2)`. This contradicts the forced `mu=a-3` here by margins211 and191. Parity alone is already sufficient.

## 9. Reproduction and scope

Run `python -I -S -B inverse86/check_inverse86.py` from the package root, or run the checker by its absolute filename from any directory. It verifies local mathematical source hashes and every fixed inequality and prints the tables in `arithmetic_tables.md`.

There are sixteen failed sufficient inverse rows for a>=15, one separate a14 row, four generalized endpoint repairs, thirteen dense-diameter repairs including the boundary, and thirty large-hole overlap cases. The repaired-row individual-primitivity argument uses the valid post-integrality G conclusion and the equality/parity contradiction. Bootstrap and AP branches are proved in the other companions.
