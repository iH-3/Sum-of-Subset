# A sharper elementary source envelope at size 85

This deduction concerns the **77-point source** in the fresh size-85 reduction. It does not use the computed fixed-label tables. The 69-point inner source has zero, positive maximum `R_s`, negative absolute maximum `R_t`, and four further entries on each sign

\[
 R_v+a_v,\quad R_v+b_v,\quad R_v+c_v,\quad R_v+e_v,
 \qquad 1\le a_v<b_v<c_v<e_v.
\]

Write

\[
 R=R_s+R_t,\quad U=a_s+b_s+a_t+b_t,\quad C=c_s+c_t,
 \quad J=(e_s-c_s)+(e_t-c_t).
\]

Let `K` be the number of distinct pair sums of this 77-point source, with repetition. The previously derived mass identity, with `T=77j-280-w+I+tau+delta`, is

\[
 2K=T+4R+U+2C+J.                                      \tag{1}
\]

For a positive integer quartet `a<b<c<e`, define the distinct fringes

\[
 P=|\{x+y>c:x,y\in\{a,b,c\}\}|,
 \qquad B=|\{x+y>e:x,y\in\{a,b,c,e\}\}|.
\]

The elementary quartet fringe lemma already used in the source reduction says

\[
 2B\le a+b+8-p,\qquad p=(a+b)\bmod2.                 \tag{2}
\]

## The single-sign improvement

For every such quartet,

\[
                         P+B-a-b\le5.                \tag{3}
\]

Here is a short proof, including its two exceptional small cases. Put `u=a+b`. There are at most six unordered pair sums of the triple, so `P<=6`. For `u>=9`, (2) gives

\[
 P+B-u\le6+\lfloor(u+8)/2\rfloor-u\le5.
\]

For `u=8`, necessarily `a<=3`, hence `2a<=c`; at least this triple pair lies outside its upper fringe. Thus `P<=5`, and (2) gives `B<=8`. For `u=7`, `P<=5` and `B<=7`; for `u=5`, `P<=4` and `B<=6`; for `u=3`, `P=3` and `B<=5`. These stated triple counts are the complete small cases tabulated below.

For `u=4`, the only way `P=4` is `(a,b,c)=(1,3,4)`. Its possible values of `B` at `e=5,6,7` are `5,5,4`; at all `e>=8=2c`, `B=4`. Thus `P+B-u<=5`. For `u=6`, the only way `P=5` is `(a,b,c)=(2,4,5)`. Its values of `B` at `e=6,7,8,9` are `6,6,5,5`; at all `e>=10=2c`, `B=4`. This also gives (3). If these respective triple maxima do not occur, (2) already gives (3).

The complete triple counts at `u<=7` are finite: when `c>=2b`, exactly `a+c,b+c,2c` exceed `c`, so `P=3`; the remaining values are:

| `(a,b)` | `c` below `2b` and corresponding `P` |
| --- | --- |
| `(1,2)` | `3:3` |
| `(1,3)` | `4:4, 5:3` |
| `(1,4)` | `5:4, 6:4, 7:3` |
| `(2,3)` | `4:4, 5:4` |
| `(1,5)` | `6:4, 7:4, 8:4, 9:3` |
| `(2,4)` | `5:5, 6:3, 7:4` |
| `(1,6)` | `7:4, 8:4, 9:4, 10:4, 11:3` |
| `(2,5)` | `6:5, 7:4, 8:3, 9:4` |
| `(3,4)` | `5:5, 6:5, 7:4` |

In particular the weaker triple fringe inequality `2P<=u+4-p` also holds universally: for `u>=8` use `P<=6`, and otherwise use this table, followed by rounding to an even integer.

## Two exact source envelopes

Remove the largest entry on each sign from the 77-point source. The remaining source has 75 points. Its pair sums lie in

\[
 [-2R_t-c_t,\ 2R_s+c_s]
\]

except for distinct same-sign sums between the three respective tails whose offset sum exceeds `c_v`. The interval has `2R+C+1` integer positions, and there are at most `P_s+P_t` distinct exceptions. Reinserting two entries creates at most

\[
 2\cdot75+3=153
\]

unordered pair labels, including repetition. Hence

\[
 K\le2R+C+154+P_s+P_t.                               \tag{4}
\]

The analogous interval for the full source is

\[
 [-2R_t-e_t,\ 2R_s+e_s],
\]

with `2R+C+J+1` integer positions. Only pairs between the four same-sign tails can lie outside it, yielding

\[
 K\le2R+C+J+1+B_s+B_t.                               \tag{5}
\]

Combining (1) with (4) and (5) gives

\[
 T\le308+2(P_s+P_t)-U-J,
 \qquad T\le2+2(B_s+B_t)-U+J.
\]

Add these inequalities and divide by two. Using (3) separately on both signs,

\[
 T\le155+(P_s+B_s-a_s-b_s)+(P_t+B_t-a_t-b_t)
   \le\boxed{165}.                                  \tag{6}
\]

Consequently the source budget improves to

\[
               I+\tau+\delta\le445-77j+w.             \tag{7}
\]

This deduction is uniform in the source core, all offsets, and the outer coefficients. No integrality of the outer coefficients is used beyond the existing integer source reduction.

## A sharper one-maximum envelope

Remove only the maximum on sign `v`; write `o` for the opposite sign. Its
76-point remainder has a pair-sum central interval with `2R+c_v+e_o+1`
integer positions, and its exceptions have at most `P_v+B_o` distinct values.
Reinsertion creates at most77 unordered pair labels. Therefore

\[
 K\le2R+c_v+e_o+78+P_v+B_o.                          \tag{9}
\]

Put `j_v=e_v-c_v`, so `J=j_s+j_t`, and `p=p_s+p_t`. Combining (9)
with (1), `2P_v<=a_v+b_v+4-p_v`, and (2) on sign `o` gives

\[
 T+j_v-j_o\le168-p.
\]

The reflected inequality and `J>=T-18+p` consequently give

\[
 j_v\ge T-93+p.
\]

For every positive strictly increasing triple, `c_v+p_v>=4`: the sole
possibility with `c_v=3` is `(a_v,b_v)=(1,2)`, for which `p_v=1`.
Since `p>=p_v`, this proves the uniform endpoint row

\[
                         e_v\ge\max(4,T-89).         \tag{10}
\]

For `Z5`, `w=0,j=5` and `T=105+I+tau+delta=105+A`, so this is
`e_v>=A+16` on **both physical signs**. This improves the earlier crude
one-maximum floor `e_v>=A+8` without an activity, normality, or ownership
assumption.

## Fringe bound at the possible endpoint `T=165`

The original weaker two-maximum envelope `K<=2R+C+166`, combined with (1), gives `T+U+J<=332`. Summing (2) over both signs, with `p=p_s+p_t`, and using (5) gives `J>=T-18+p`. Therefore

\[
 2T+U+p\le350.
\]

If `T=165`, this says `U+p<=20`, so

\[
                 B_s+B_t\le(U+16-p)/2\le18.          \tag{8}
\]

Thus the endpoint fringe saves four in a scalar estimate which had used `B_s+B_t<=20`. The local scalar computation supplied by the separate audit agent has raw margin at least `1` for `T<=164` and margin `-2` at `T=165`; (8) increases the latter margin to at least `2`.

## Exact verification

`source_triple_fringe85.py` checks every finite small case needed by (3), the two exceptional quartet tables, and the displayed algebra. The unbounded domains are reduced by the explicit `c>=2b` and `e>=2c` observations above. It also performs a larger independent numerical sanity check; that numerical check is supplementary, not the justification for the unbounded statement.
