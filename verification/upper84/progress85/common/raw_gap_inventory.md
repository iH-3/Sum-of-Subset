# Sharp fixed-label inventories in the raw gaps

This proof does not depend on cardinality 85. It applies to the original four-extreme cover with positive outer magnitudes
\(v_1>v_2>v_3>v_4>M_v>0\), opposite outer magnitudes \(o_i>M_o>0\), and the same 55 raw fixed labels on target v.

Write
\[
d=v_1-v_2,\quad h=v_2-v_3,\quad x=v_3,\quad y=v_4,
\quad M=M_v+M_o.
\]
The ordinary centre identities are
\[
\lambda=d-x-y,\quad\alpha=h-y,\quad\beta=h-d-y,
\quad H=d+h-y,\quad O=H+d.
\]

The raw fixed labels are C labels \(\lambda+b_i+b_j\) for unordered pairs in \(\{v_1,v_2,v_3,v_4,-o_1,-o_2,-o_3,-o_4\}\); U labels \(\alpha+b_i\) and V labels \(\beta+b_i\), excluding \(b_i=v_1\); and the five F labels of the original cover.

All statements below count formal labels. Colliding or nonintegral values only reduce the ability to cover integer target points.

## First gap: at most eleven labels

Assume the first gap
\[
(H+M_v,O-M_o)
\]
is guarded inside the positive target. Its length is \(t=d-M\), and the lower guard gives \(H+M_v>0\).

Subtract \(\lambda\). A C label in the interval must be either one of the six positive pairs among \(v_2,v_3,v_4\), or one of the four cross pairs \(v_1-o_i\). All other pairs are below or above the interval. A U or V label can use only \(v_2,v_3,v_4\), giving three candidates of each kind.

The seventeen internal candidates split into the following five chains, each with consecutive difference d:
\[
\{C22,U2,V2\},\quad\{C23,U3,V3\},\quad\{C24,U4,V4\},
\quad\{C33,F1,F3\},\quad\{F2,F4\},
\]
and three remaining labels \(C34,C44,F5\). Since \(t<d\), each chain meets the gap at most once.

After subtracting H, the last two labels have values
\[
C44-H=y-h-(x-y),\qquad F5-H=y+(x-y)-3h-2d.
\]
The guard is \(y<d+h+M_v\). If C44 is above the lower endpoint, then \(y>M_v+h+(x-y)\), hence \(x-y<d\). Consequently
\[
F5-H<M_v+(x-y)-2h-d<M_v.
\]
Thus C44 and F5 cannot both meet the gap. There are at most seven internal labels and four cross labels: eleven in total. The original covering gap argument therefore gives
\[
t\le12+\eta_v.\tag{1}
\]

## Beta-active second gap: at most eight labels

Assume beta is active. Since \(\beta+M_v\ge1\),
\[
h\ge d+y-M_v+1>d.
\]
After subtracting alpha, the second gap is
\[
J=(M_v,d-M_o).
\]

Its internal candidate labels, expressed relative to alpha, are:

| Chain or singleton | Relative values |
|---|---|
| D: C33,F1,F3 | \(d+x-h,\ x-h,\ x-h-d\) |
| G: F2,F4 | \(x-2h,\ x-2h-d\) |
| B: U3,V3 | \(x,\ x-d\) |
| C: U4,V4 | \(y,\ y-d\) |
| V2 | \(x+h-d\) |
| F5 | \(x-3h-d\) |

The label U2 has value \(x+h>d\), so it cannot occur. C34 and C44 are below the lower endpoint because
\[
C34-\alpha=d+y-h<M_v,\qquad C44-\alpha<C34-\alpha.
\]
The only cross candidates are C labels using \(v_1-o_i\) or \(v_2-o_i\). For each i the two values differ by d, so their total contribution to J is at most four.

Each of the four internal chains contributes at most one. If V2 lies in J, then \(x+h<2d\), hence \(x<2d-h\); G and F5 are below zero. This leaves V2 and the three other chains, at most four labels. If F5 lies in J, then \(x>3h+d+M_v\); B,D,G and V2 are above J, leaving only chain C and F5, at most two. If neither singleton occurs, the four chains give at most four. Thus the second gap has at most four internal and four cross labels, eight in total.

When H is active its upper guard is valid and the second gap therefore gives
\[
t\le9+\eta_v.\tag{2}
\]

## Beta-active union: at most fifteen labels

After subtracting alpha, the union of the two raw gaps is \(J\cup(J+d)\). Its whole hull has length \(2d-M<2d\). The candidate internal labels are the five d-spaced chains
\[
\begin{array}{ll}
A:& C22,U2,V2=(d+x+h,\ x+h,\ x+h-d),\\
B:& C23,U3,V3=(d+x,\ x,\ x-d),\\
C:& C24,U4,V4=(d+y,\ y,\ y-d),\\
D:& C33,F1,F3=(d+x-h,\ x-h,\ x-h-d),\\
G:& F2,F4=(x-2h,\ x-2h-d),
\end{array}
\]
and singleton F5, with value \(x-3h-d\). Each chain has at most two values in the union.

- If \(x<d\), A,B,C have at most two each; D has at most one; G and F5 are below zero. Total at most seven.
- If \(d\le x\le2d\), A has at most one; B,C,D at most two each; G and F5 are below zero. Total at most seven.
- If \(x>2d\), A is absent; B has at most one; C,D,G at most two each. If F5 is absent, the total is seven. If F5 occurs, then \(x>3h+d+M_v>4d\), which makes B absent; the total is again seven.

The cross pairs \(v_1-o_i,v_2-o_i\) give at most eight labels across the union. All other candidates are excluded exactly as above. Thus both disjoint gaps together have at most fifteen labels.

When O and beta are active, both intervals are guarded inside the target, regardless of H activity. They must share these fifteen labels and the same \(\eta_v\) holes. Therefore
\[
2(t-1)\le15+\eta_v,\qquad
2t\le17+\eta_v.\tag{3}
\]

Nonpositive gap lengths make all three bounds automatic. Leading activity, or the other established lower guards from the original common lemma, licenses (1) whenever O is active. These inventories imply the uniform cap \(t\le12+\eta_v\) for the predicate “O active or beta,H active.”
