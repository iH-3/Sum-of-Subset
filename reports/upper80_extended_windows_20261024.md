# Extended subset-sum windows: continuation toward 80

This is a research-model result, not a proof of the global bound 80. The
established range remains **71 ≤ N ≤ 81**. The structural interfaces listed in
`verification/upper80/research_checkpoint.md` still require a complete audit.

The new argument below closes both remaining rank slices of the six-empty-cell
root `(6,436,0)`. Its `k=2..7` slices were already certified; they are reused
without restarting their search. The source budget gives `k²≤58`, so `k≥8`
is impossible. Together with the new unrestricted contradictions for `(5,256,0)`,
`(5,266,0)`, `(5,268,0)` and `(5,270,0)`, this brings the current total to
4,650 closed original roots and four open roots at that checkpoint. The later
extreme-gap continuation below closes `(5,413,0)` completely, bringing the
current total to **4,651 closed and three open original roots**.

## Complete interval propagation

Let an integer interval `[L,U]` be contained in the subset sums of a set `B`.
Let `a` be an unused element, with `0<|a|≤U−L+1`. The intervals `[L,U]` and
`a+[L,U]` overlap or are adjacent. Their union therefore contains every integer
between `L+min(0,a)` and `U+max(0,a)`. Both intervals consist of actual subset
sums of `B∪{a}`. Iterating uses each additional element exactly once.

For the 73-point source `D`, zero holes give the initial interval
`[−S_t,S_s]`. A previously licensed complete interior for the single-hole
regime gives `[−S_t+m,S_s−m]` instead. The proof stores an explicit ordering
of the eight unused outer points, and an exact certificate for
`|a|≤U−L+1` at each extension. It then certifies the two bounds placing the
requested window inside the resulting interval. No sampling or assumption
that all subset sums are consecutive is used.

Unlike a fixed-offset target, a window endpoint may move with a four-sum
component endpoint. For a numerical gap between two non-singleton component
hulls, the discovery code proposes the affine endpoints immediately after
one hull and before the other. The verifier accepts them only after all
necessary inequalities have exact rational certificates.

## Capacity of a window in the complete four-sum cover

The catalogue partitions all four-sum representations by their multiset of
outer summands. There are 495 coarse types. Refining the source summands into
its eight tails and the 65-point core yields 4,845 terminal types.

For each window, the saved inventory accounts for every type exactly once:

* An outside component has a certified strict integer separation from the
  window, on one specified side.
* A retained component is charged the size of an enclosing integer interval,
  or a licensed cardinality upper bound: 73 for a translate of `D`, 65 for
  a translate of the core `E`, and `K` for a translate of `2D`.
* Several types may be absorbed into one retained interval hull, with two
  certified containment inequalities for each absorbed type. That retained
  interval is then charged its full hull length, including when its actual
  core translate would have only 65 points.

The number of required subset sums in the window cannot exceed this capacity.
Thus its length, minus any still-allowed source holes, is bounded by the sum
of the charged capacities. Negative right sides or an empty window do not
create a spurious positive requirement.

Additional optional improvements have explicit scope checks:

1. A component's intersection with the window can be charged a clipped hull.
   Each endpoint is chosen from the component or the window; the selected
   hull length must be nonnegative. Clipped components are excluded from
   full-core overlap rebates.
2. Write the largest positive/negative core elements as `R_v=r_v+xi_v`, and
   their excess masses as `tau_v`. Removing the maximum gives predecessor
   at most `r_v−1+tau_v−xi_v`. Consequently every `qE`, `q≥2`, misses at
   least `max(0,2xi_v−tau_v)` positions next to each extreme. The two strips
   are disjoint because the core contains zero and points of both signs.
   Hence `|qE|≤q(R_s+R_t)+1−2(xi_s+xi_t)+tau_s+tau_t`. For `q=2` this is
   `129+tau_s+tau_t`.
3. The core intersection kernel `|E∩(E+x)|≥F−x` gives
   `|qE∩(qE+x)|≥qF−q+1−x`. When the claimed bound is positive, split the
   nonnegative integer `x` into `q` pieces at most `F−1`, and add the `q`
   nonempty intersections. The elementary integer sumset inequality gives
   the displayed bound. When the bound is nonpositive it is automatic.
   Rebates are combined only along an explicitly acyclic forest of translates
   of the same `qE`.

## Complete disjunctions and integer consequences

A one-point window licensed by the extension lemma is an actual integer
subset sum. It must belong to at least one type in the complete four-sum
cover. The new extended target trace preserves the complete catalogue and
uses the same exact exclusion, refinement and conditional containment checks
as the earlier full-cover targets.

`cover_partition.py` verifies that every live alternative is present exactly
once. A closed leaf requires an exact contradiction; an open leaf stays open.
Conditional records must have exactly the path assumptions, and their premise
chain must reach the precise pre-partition record. A common fixed-loss credit
may be raised only if every alternative is closed or independently proves at
least that credit. This gave credit 50 throughout the `j=6,k=1` slice before
its new window contradiction was found.

The optional Chvátal–Gomory trace uses nonnegative rational inequality weights
and arbitrary equality weights. All variables are licensed nonnegative
integers. After moving the fixed unit variable to the right-hand side, both
coefficient and right-hand-side floors are recomputed with integer arithmetic.
Discovery simplex tableaux propose multipliers only. They are not proof data.
Numerically troublesome generated cuts may be omitted from discovery LPs;
the corresponding exact certificates then have zero weight on those rows.

## Scope and reuse

The earlier baseline replays, old closed rank slices, old hole slices and
completed target enumerations were not restarted. New certificates were
checked against their required premises. A partial cover tree, a feasible
LP point, or a collection of closed local leaves is never counted as a closed
original root without complete coverage.

The new helper controls include 1,200 explicit core sumsets, 6,381 clipped
hulls and 200 independently computed subset-sum extensions. These controls
support implementation checks; the general arguments above supply the
mathematical licenses.

## First missing value and a shifted core compression

For a positive rank-`r` integer core `X={x_1<...<x_r}`, write
`phi(X)=min(r,min_i(x_i+r−2i))`. This is the truncation defect used by the
existing core intersection kernel. Suppose its first `t` elements form the
prescribed prefix (either empty or `{1}`), and the rest are at least `h+1`.
Put `Y={x_(t+1)−h,...,x_r−h}`. The same truncation index in `Y` gives
`phi(X)≤h−t+phi(Y)`.

If the first missing subset sum of the two positive core magnitude lists is
at most 3, their possibilities are exactly:

| First missing value `h` | Prefix on side s | Prefix on side t | Remaining values |
|---|---|---|---|
| 1 | empty | empty | at least 2 |
| 2 | `{1}` | empty | at least 3 |
| 2 | empty | `{1}` | at least 3 |
| 3 | `{1}` | `{1}` | at least 4 |

To see completeness, the total of all coefficients below the first missing
value is `h−1`. For `h=2` there is exactly one coefficient 1; for `h=3` there
are exactly two coefficients 1, since a coefficient 2 together with a 1
would already represent 3. Distinctness on each physical side places the two
1s on different sides.

The baseline excess mass is `b=h*r` for `t=0` and
`b=(h−1)*(r−1)` for `t=1`. Thus `tau(Y)=tau(X)−b` and
`xi(Y)=xi(X)−(h−t)`. Applying the existing staircase inequalities to `Y`,
for every positive integer `q`, gives

`q phi(X)−tau(X)+b ≤ q(h−t)+q(q−1)/2`,

`q phi(X)−tau(X)+xi(X)+b ≤ (q+1)(h−t)+q(q+1)/2`.

The maximum also satisfies `xi≥h−t` and `tau−xi≥b−(h−t)`.
The complete four-case rule is admitted only after exact certificates for
`W=1` and `tau_s+tau_t+I≤186`, using the previously proved first-gap threshold
187. The two core ranks are affine in `k`, so all displayed rows are linear
in the existing model variables. No extra variable is sampled.

The new focused controls checked 19,716 explicit positive cores and all 4,921
small core pairs whose first missing value is 1, 2 or 3. These are additional
implementation checks, not the proof of the displayed general inequalities.

## Reusing consequences across branches

`record_consequences.py` reuses a previously proved linear fact without
repeating its search. The source and target must have exactly the same
physical pattern, sign regime and size parameter. Every source restriction
must be present in the target with a contained parameter interval; a fact
proved under an extra branch assumption cannot be imported into its parent.
The source record is checked exactly before any selected fact is admitted.
A fixed-loss credit can also be imported, up to the source's verified credit.

The variables being joined here are the canonical cardinalities, clipping
losses and integer truncation minima of the same actual configuration. They
are not independently chosen existential witnesses. A later branch may thus
combine its earlier conditional facts with newer facts proved for the whole
root. Saved records form an acyclic dependency graph: new branch proofs may
refer to an earlier global proof which in turn refers to the old branch
proofs, but never to the new proof itself.

Equal translates of the same `qE` may also be deduplicated inside a window.
Two opposite exact endpoint comparisons certify equality of their centres.
Both components must have the same residual core power. This retains the
65-point charge for identical `E` translates; mere hull containment would
instead require the full hull charge. New focused controls cover 192 actual
equal translates and three invalid recipes.

After window cuts, applying the original source and fixed-loss propagation
again produced additional unrestricted root contradictions `(5,256,0)`,
`(5,266,0)` and `(5,268,0)`. Their exact replays have respectively 92, 71
and 33 final-record steps, with fixed-loss credits 78, 56 and 52. This brings
the current total to **4,650 closed original roots and four open roots**.
These are new, strengthened systems; the old completed searches were not
restarted.

## Complete double-source union and mixed-power overlaps

Write `D=E∪{T_0,...,T_7}`. The complete double sum is the union of `2E`,
the eight sets `E+T_i`, and the 36 unordered tail-pair types. The positive
tail translates form a chain rooted at `E+R_s⊂2E`, with successive gaps
`a_s,b_s−a_s,c_s−b_s,e_s−c_s`; the negative side has the reflected chain
rooted at `E−R_t⊂2E`. Any selection of these eight edges is acyclic and
saves at least `F−gap` per edge. Start with either the hull capacity of
`2E` or its mass capacity `129+tau_s+tau_t`, then add `8*65+36` and subtract
the selected rebates.

The excess-mass prefix lemma gives `[−L_t,L_s]⊂E`, where `L_v=r_v−tau_v`.
The assertion remains valid when this interval is empty or lies entirely
on one side of zero. A tail-pair point `p` adds no cost if `p−u` is in this
interval, for an actual point `u∈{0,R_s,−R_t,T_0,...,T_7}`. It also adds no
cost if `p∈[−2L_t,2L_s]⊂2E`. Two exact affine comparisons license each
membership; each of the 36 index pairs can be rebated only once. The rule
in `source_union.py` checked 400 actual 73-point sources, with 800 capacity
checks (180 sharp) and five malformed-inventory negative controls. The
first unrestricted discovery attempt produced no new cut in the four
remaining roots; that outcome is retained, not counted as a closure.

For `1≤p<q≤4`, choose `c=iR_s−jR_t` with nonnegative integers `i+j≤q−p`.
Then `c+pE⊂qE`, since every anchor summand is an actual core point (and
unused summands are zero). Therefore

`|(a+pE)∩(b+qE)| ≥ pF−p+1−|b+c−a|`.

The saved orientation has an exact nonnegative-distance certificate. These
edges share one forest with the same-power edges, so cycles cannot double
subtract an intersection. Clipped components are excluded. The new controls
check 1,280 actual mixed-power intersections and four invalid recipes.

Nested certificate replay now restores the caller's endpoint-plane table,
feature flags and geometry, including on exceptions. This fixes a newly
encountered failure when an imported root record was followed by a stronger
conditional endpoint-credit update. Cache identities also preserve dictionary
insertion order, because branch-row order affects certificate indices. A
focused regression rejects a reordered cached record and checks restoration
on both successful and failed replay. Existing closed searches were not
restarted for this repair.

## First-gap shape strengthens every core power capacity

The four physical first-gap alternatives can now be retained as an explicit
branch label, rather than only as their necessary linear compression rows.
The complete four-case partition verifies this label; unrestricted records
cannot use its additional geometry. Facts and contradictions from an older
containing domain are reused with the same domain-containment checks.

Let `b_v` be the mandatory extra mass of the smallest `r_v−2` core elements.
For the first-gap shape `(h,t_v)`, it equals `h(r_v−2)` if `t_v=0`, and
`(h−1)(r_v−3)` if `t_v=1`. Removing the largest two elements leaves mass at
least `T_(r_v−2)+b_v`. Thus the predecessor of `R_v` is at most
`r_v−1+tau_v−xi_v−b_v`, and the gap below `qR_v` in every `qE`, `q≥2`,
has at least `max(0,2xi_v−tau_v+b_v)` positions. Consequently

`|qE| ≤ q(R_s+R_t)+1−2(xi_s+xi_t)+tau_s+tau_t−b_s−b_t`.

The two end strips are disjoint, as in the original core-capacity proof.
For `q=2`, the four bounds are respectively `69+tau`, `40+tau−k`,
`40+tau+k`, and `13+tau`. In particular the first-gap-1 branch improves
the former mass capacity by 60. Focused controls check 1,200 actual core
power sumsets, with 300 sharp cases, and reject all four unlicensed shapes.
When `W=1` is fixed, the actual first-gap label also locates the sole end
hole directly, allowing the complete interior margin `h+1`.

The combined first-gap partition subsequently passed exact replay with cases
1, 2 and 3 closed, and only case 0 open. This is a statement about the entire
`W=1` slice, not an additional original-root closure. The surviving physical
shape and its already verified linear facts can be inherited: any actual
configuration in the parent must belong to that sole surviving alternative.
Its interior margin is now 2. The pooled checkpoint records that inference
explicitly and keeps the remaining case open.

For a physical first-gap shape, shifting the unprescribed remainder down by
`h` gives a guaranteed core interval `[h+1,h+L_v]`, where
`L_v=r_v−t_v−tau_v+b_v^{full}` and `b_v^{full}` is the baseline excess of
the whole rank-`r_v` core. The reflected negative interval is also contained
in `E`. If both `L_v≥2h+2`, their three pair-sum intervals join, showing
`[−2h−2L_t,2h+2L_s]⊂2E`. These optional source-pair membership witnesses
have explicit interval and joining guards; no unproved density assumption
is used.

## Upper mass from the canonical truncation minimum

For `X={x_1<...<x_r}`, the truncation parameter is the actual minimum
`phi=min(r,min_i(x_i+r−2i))`. If `phi<r`, choose a minimizing index `r−q`.
Then `0≤q≤phi`, the first `r−q` deviations are at most `phi−q`, and the
last `q` deviations are at most `xi`. Therefore

`tau ≤ (r−q)(phi−q)+q*xi ≤ phi*max(r,xi)`.

The second inequality maximizes a convex quadratic over `0≤q≤phi` at an
endpoint. If `phi=r`, the same conclusion follows from `tau≤r*xi`.
Whenever exact guards prove `r≤H` and `xi≤H`, the linear consequence
`tau≤H*phi` is thus valid. In particular a zero canonical defect cannot
coexist with positive excess mass. The new controls check 12,910 actual
cores, including 3,431 sentinel-minimum cases and 175 sharp instances.

Additional conditional progress does not alter the four-open-root count:
the saved 12-alternative partition of `(5,413,0)` now has new exact
contradictions for alternatives 2 and 8, leaving only alternative 3.
Their new final records have respectively 37 and 785 steps. The first-gap
alternative 1 of the positive root also closed in a new 20-step record.
The three-target enumeration for `(5,219,0)` is complete at depth 3:
1,891 nodes, 421 closed leaves and 1,343 open leaves. Its open leaves are
retained; that completed depth must not be restarted.

## Empty extreme intervals and one-point window charges

Let `Q` have maximum `M` and second-largest element at most `P`. In `qQ`,
the largest sum is `qM`; every other sum is at most `(q−1)M+P`. Thus
`[qM−(M−P−1),qM−1]` is empty. Reflection gives the analogous lower gap.
For a source power `qD`, the gap length is exactly `e_v−c_v−1`. For a
core power `qE`, the earlier predecessor estimate gives a gap length at
least `2xi_v−tau_v`; a licensed first-gap shape adds its mandatory
`r_v−2` prefix excess to that length. Negative lengths assert no hole.

`core_gap.py` first applies this to existing complete-cover probes: a whole
probe lying in an empty interval cannot be hit by that component. The first
application to the four remaining strengthened domains made no deletion,
and those finished attempts are retained.

The window rule is stronger in two ways. It can discard a component when
the entire window lies in an extreme gap. It can also charge a component
only one point when the window lies above its nonextreme upper bound (or
below its nonextreme lower bound): only the actual extreme can occur there.
This latter charge also applies to unrefined `qD` components. One-point
components cannot simultaneously be charged a clipped/full core capacity,
act as absorbing hulls, or participate in full-set overlap rebates.

Discovery forms new windows after removing these guaranteed holes from
the numerical component envelopes. The two actual extreme points are kept
in the candidate singleton inventory. Saved integer discovery points are
reused as seeds; they are not solved again. Every final interval and
one-point charge still requires its own exact affine guards.

New controls check 1,600 actual empty extreme intervals (1,536 nonempty),
4,472 whole target probes, and 1,600 present-extreme boundary controls.
Four additional sharp actual windows check the one-point charge, and six
malformed window inventories/capacity combinations are rejected.

The new rule closes case 3, the final open alternative in the complete
12-case target partition of `(5,413,0)`. Its 25-step continuation at credit53
passed independent exact replay. Assembly checks all 12 original nodes and
their exact conditional domains against the frozen parent; the other 11
closed records are reused unchanged from the immutable verified frontier.
`data/upper80_extreme_gap_closure_20261024.json.gz` contains the full closed
record, its new replay receipt, the earlier receipts and record identities.
`verify_extreme_gap.py --reuse-receipt` checks the packaging without repeating
completed arithmetic; its default mode supports a fresh full exact replay.
The remaining original roots are `(4,142,0)`, `(4,142,1)` and `(5,219,0)`.

## Canonical mass after the physical first-gap translation

Let the actual first-gap shape prescribe height `h` and a prefix with
`t=0` or `t=1` points. Put `n=r−t`, `w=h−t`, and translate the remaining
points down by `h` to form a positive `n`-point set `Y`. Directly from
`phi(X)=min(r,min_i(x_i+r−2i))`,

    phi(X) = min(n, w+phi(Y)),
    tau(Y) = tau(X)−wn,    xi(Y) = xi(X)−w.

For `t=0`, the term `n` is the sentinel; for `t=1`, the initial point 1
gives that term. Thus, under the certified guard `phi(X)≤n−1`, the equality
`phi(Y)=phi(X)−w` holds. Applying the canonical mass inequality to `Y`,
and separately certifying `n≤H` and `xi(X)−w≤H`, gives the affine row

    tau(X)−wn ≤ H (phi(X)−w).

The physical shape and all three guards are mandatory. Omitting the
nonsentinel guard is false, for example at `X={3},h=2,t=0`. Actual-set
controls check 3,388 translated minimum identities, 1,124 nonsentinel mass
inequalities, 800 physical-rank affine inequalities and five rejected
recipes. The new rows are applied only to the surviving physical `h=1`
domain; they do not constitute a closure by themselves.

## Hull charges for the complete double-source union

The set `2D` is the union of `2E`, eight translates `E+u` by source tails,
and the 36 tail-pair types. Partition the nine core components into groups.
For each group, certify a containing integer interval `[L,U]` and charge
`U−L+1`. Every tail-pair point certified to belong to this interval may be
absorbed without an additional charge, even if it is absent from the actual
core components. Alternatively, a singleton core component may use its actual
mass bound (`|E|=65` or the earlier `2E` capacity); such a component cannot
absorb extra points. Charge one for each remaining tail-pair type.

This is an upper cover of the entire union. Overlap between charged groups
can only increase the estimate, so disjointness and actual intersection
claims are unnecessary. The verifier requires every core component exactly
once and every absorbed pair type at most once. All interval containment
inequalities have exact certificates. Independent controls check 600
capacities on 300 actual 73-point sources, 6,653 absorbed pair occurrences,
and five invalid proof recipes. This rule is distinct from the earlier
overlap-forest source-union attempt.

For the saved `(5,219,0)` joint tree, the new credit51 premises can be
imported while preserving its old row inventory. New verified facts are
appended, and only branch-assumption row indices in old certificates are
shifted by the number of appended rows. The 421 old closed leaves are
retained and skipped; only open nodes are reconsidered under stronger
premises. This preserves completed work without treating old open leaves
as closed.

## Partially visible extreme gaps and proved core hits

A charged clipped component hull `[L,U]` can also subtract a certified
subinterval of one of its empty extreme gaps. The verifier checks that
each removed interval belongs both to `[L,U]` and to that component's
guaranteed empty interval, and has nonnegative integer length. If both
extremes contribute, their removed intervals must be disjoint. Only a
component charged by its own hull may use this subtraction: no actual-set
mass charge, absorbing hull, or full-set overlap rebate can also use it.
The controls include 640 actual component windows, 480 sharp cases,
314 partially visible gap removals, and four rejected recipes.

The existing ownerless lemma gives `h_v<=R_s+R_t+31+W` when `uH_v<=68`
and its earlier strict guards hold. Its original interface looked only at
an explicit branch limit. `ownerless_hit.py` permits the same premise to be
supplied by an exact consequence certificate. Both sides of the surviving
positive root now have these certified premises. For the zero-hole root,
where they are not proved globally, the complementary domains are
`uHs<=68,uHt<=68`; `uHs>=69`; and `uHs<=68,uHt>=69`. An open domain in
this split remains open unless its own contradiction is recorded.

## Reusing shared verification history

Open-premise cache keys now use the record pool's order-sensitive recursive
content identity. Each parent reference commits to its child's complete
content through its hash; dictionary and row order still affect identity.
This avoids repeatedly expanding shared ancestors into unpooled JSON and
does not change any mathematical replay rule. A control with 31 shared
records represents 2,147,483,647 unpooled occurrences without expanding them;
nested content/order changes and a reordered actual certificate are rejected.

The separate small-rank note `upper80_small_rank_interface_20261024.md`
spells out the rank7/8 core-level AP distinction. It explicitly leaves the
outer-source comparison and the rest of structural adoption unfinished.

## A nonlast canonical minimizer and stronger predecessor mass

If `xi>=phi+1`, the last-index term cannot attain the canonical minimum.
Under `phi<=r−1`, choose an attaining index `r−q`. Then `1<=q<=phi` and

    tau <= (r−q)(phi−q)+q xi.

This convex quadratic in `q` is bounded by its two endpoint values on
`[1,phi]`. If `r−1<=H` and `xi<=H`, both are at most
`xi+H(phi−1)`. Therefore the new guarded affine row is

    tau <= xi+H(phi−1).

For a physical first-gap remainder, substitute `n=r−t`, `phi−w`, `xi−w`,
and `tau−wn` as before, also licensing `phi<=n−1`. The four complementary
integer cases distinguish `xi_v>=phi_v+1` from `xi_v=phi_v` on each side.
The latter equality follows from the existing universal `phi_v<=xi_v`.
This partition is retained explicitly; a single closed alternative does
not close the root. New controls check 6,048 actual cores (151 sharp),
1,000 physical affine instances and four invalid recipes.

There is also an unconditional lower mass bound for the prefix remaining
after removing the two largest core coefficients. From the definition of
`phi`, its last `ell` excesses have sum at least

    ell phi − ell(ell+3)/2.

In a physical first-gap shape, add its earlier mandatory prefix mass and
replace `phi` in this expression by `phi−w`. Indeed the translated
remainder always has canonical defect at least `phi−w`, even in the
sentinel case. Orders `0<=ell<=12` are valid throughout the present ranks,
including a rank15 core with a one-point prescribed prefix.

Adding this floor to the predecessor estimate strengthens each empty
extreme interval and the corresponding complete `qE` capacity. It is a
valid affine inequality for every chosen order, so discovery may select
the order without partitioning the parameter domain. The independent
actual-set controls check 5,200 prefix floors, 600 core-power capacities
and 400 empty extreme intervals. Proof recipes store the chosen orders
and the licensed physical shape; old records default to order zero.


## Complete positive-root closure from canonical predecessor gaps

The canonical prefix floor closed the entire `W=1` domain of `(4,142,1)`.
Its new36-step record, with credit48, passed an independent exact replay.
The complete original root is assembled from the exact domains `W=1`,
`W=2` and `W=3..7`; the latter two use the immutable previously verified
positive-refinement packet. The assembly checks domains and record identities
without rerunning old searches or arithmetic. The total is now4652 closed
original roots, leaving `(4,142,0)` and `(5,219,0)`.

The four canonical-minimizer cases for `(5,219,0)` are the product of
`xi_v>=phi_v+1` and `xi_v=phi_v`, for the two sides. Their union is complete
because the parameters are integers and the existing canonical definition
gives `phi_v<=xi_v`. Case0 (both nonlast) is closed and independently replayed;
the other three remain open. This conditional result does not close the root.

## Source capacity retaining each component's extreme gaps

The same prefix floor now applies to the mass base of `source_union.py`.
The stronger complete source envelope additionally keeps the extreme gaps
of **each** component in `2D=2E union (E+tails) union (tail+tail)`.
For each of its nine core components, write its hull as `[l,u]` and let
`L_s,L_t` be either zero or the certified affine lower bounds for the gaps
immediately below its maximum and above its minimum. Every point belongs to

    {l}, [l+L_t+1,u-L_s-1], {u}.

A negative affine gap bound remains safe: it enlarges the middle interval.
The middle interval contains the translated core zero. A single E-translate
has exactly65 elements, so its middle part also has cardinality at most63.
Together with the36 tail-pair singletons this is a fixed inventory of63
pieces. Partition those pieces into charged hulls, checking all endpoint
containments, or charge a single piece by its intrinsic mass. A mass group
may not absorb any other piece. Summing the charges bounds `K=|2D|`.

`source_envelope.py` reconstructs every piece from the licensed physical
shape and canonical prefix orders. The exact replayer checks the complete,
nonduplicated inventory and every affine hull guard. New controls cover120
actual73-point sources,1080 component envelopes,120 single-piece mass
partitions and five malformed recipes. At the previously saved j5 discovery
point, this new recipe lowers the geometric capacity303 to294; this is a
recipe evaluation at that point, not a universally certified cut or a
contradiction. Discovery must certify its guards on the current domain.

None of these additions certifies global80 until both remaining finite roots
and the structural applicability obligations have been resolved.


The later structural note now explicitly derives the universal outer-source
comparison `|FS(D)|-2|FS(D1)|<=-113-2I<0`, using onlyrho>=-16.
Together with its inner bound this closes the rank7/8 source-lattice gate.
It also spells out the exact reflection transporting a balanced `(32,32)`
AP-first argument to either labelled side. The complete AP-first no-clipping
and halfstep adoption remains a separate obligation.

## Finite-tail endcaps beyond a one-point window charge

For a finite ordered setQ with maximumM, letB bound every element outside
its largestL elements. Any point ofqQ above `(q-1)M+B` uses only theseL
values. Its multiplicity-free cardinality is therefore at most
`binomial(q+L-1,q)`. Reflecting gives the same bound at the lower extreme.
ForqD andL=1,2,3,4, the omitted-next values are the source tailc,b,a and
core maximumR, respectively. These are actual ordered source points.

For a core, writex_i=i+d_i, with nondecreasingd_i. Putxi=d_r and letP be a
lower bound on the excess mass of the first`r-L-1` elements. Monotonicity gives

    L*d_(r-L) <= tau-xi-P,
    x_(r-L) <= r-L+(tau-xi-P)/L.

The canonical minimum gives, for any permittedell,

    P >= ell*phi-ell*(ell+2L+1)/2.

With a licensed first-gap prefix of sizet and translationw=h-t, replaceP
by `w*(r-L-1-t)+ell*(phi-w)-ell*(ell+2L+1)/2`. The translated canonical
minimum is at leastphi-w, including its sentinel case. Since every remainder
has rank at least14, everyell in0..13-L is valid forL=1..4.

For a translatedqE component with upper extremeu, the scaled sufficient
upper-window guard is

    L*(u-lower)-(L+1)*xi+tau-P+1-L^2 <= 0.

Its added1 makes the excluded-summand threshold strictly smaller than the
windowlower. This argument does not require rounding a nonintegral outer
shift. AtL=1 it reproduces the previous one-point guard exactly. A finite-tail
charge cannot also use clipping, a mass charge, an absorbing hull or a full
component overlap forest. Equal actual core components may still share their
one retained representative.

`tail_caps.py` implements these guards and their binomial cardinalities;
`tail_cap_windows` enables them only on a new continuation path. New controls
check2560 actual capacities (965 sharp),3680 prefix floors,640 exact matches
to the old one-point rule and nine invalid recipes. A separate full-window
integration check covers989 components, verifies the five-point charge of
4-sums from two retained values, and rejects three incompatible combined
charges. These controls do not rerun any prior search or baseline suite.


## Complete canonical-minimizer closure of j5_219

All four cases have now passed independent exact replays. In bit order
`(nonlast,last)=(0,1)` on each side, the cases00,01,10,11 have local trace
lengths22,24,23,30 and final credits54,54,52,52. Case10 was closed by the
new finite-tail window bound; its decisive window has threeL=4 endcaps.
The other three cases use the preceding canonical and source-envelope rules.

`verify_canonical_minimizer.py --reuse-receipts` checks the complete binary
tree, exact limits of every leaf and ancestor to their common unrestricted
parent, and all four unchanged replay identities. No old search or arithmetic
is repeated. The finite total is now4653/4654 with sole remaining original
root `(4,142,0)`. All former j5_219 joint trees and partial partitions are
superseded. Complete structural adoption and this last finite root remain
necessary before claiming80.
