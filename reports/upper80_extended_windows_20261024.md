# Extended subset-sum windows: continuation toward 80

This is a research-model result, not a proof of the global bound 80. The
established range remains **71 ≤ N ≤ 81**. The structural interfaces listed in
`verification/upper80/research_checkpoint.md` still require a complete audit.

The new argument below closes both remaining rank slices of the six-empty-cell
root `(6,436,0)`. Its `k=2..7` slices were already certified; they are reused
without restarting their search. The source budget gives `k²≤58`, so `k≥8`
is impossible. This closes one original root, beyond the previous 4,645 closed
roots. Results for the other original roots will be recorded separately.

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
