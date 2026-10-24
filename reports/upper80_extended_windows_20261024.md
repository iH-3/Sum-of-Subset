# Extended subset-sum windows: continuation toward 80

This is a research-model result, not a proof of the global bound 80. The
established range remains **71 ≤ N ≤ 81**. The structural interfaces listed in
`verification/upper80/research_checkpoint.md` still require a complete audit.

The new argument below closes both remaining rank slices of the six-empty-cell
root `(6,436,0)`. Its `k=2..7` slices were already certified; they are reused
without restarting their search. The source budget gives `k²≤58`, so `k≥8`
is impossible. Together with the new unrestricted contradictions for `(5,256,0)`,
`(5,266,0)`, `(5,268,0)` and `(5,270,0)`, this brings the current total to
4,650 closed original roots and four open roots.

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
