# Excluding the fresh zero-hole Z3 A1 form

This is a conditional local proof for a cardinality-85 configuration after a valid integral primitive-core structural reduction. It uses only the actual Z3 A1 retention form and the common source/rank/forest lemmas. No scalar cell is assumed to be an actual set.

## Actual form and source quantities

The original source has 77 points and the core has 69 points. Write

\[
r_s+r_t=68,\quad I=(r_s-34)^2,\quad
\tau=\tau_s+\tau_t,\quad R_v=r_v+\xi_v,\quad R=68+\xi_s+\xi_t.
\]

The three missing ordinary whole units are exactly \(O_s,O_t,H_s\). The beta pair is retained and has sole actual owner \(s\); pair1 \(\{C4_s,C4_t\}\) has sole actual owner \(t\). Every unlisted ordinary singleton is retained. Both leading resources are active and all outer coordinates are integral, by the preceding actual-activity reduction.

Let \(e_s,e_t\) be the fourth peel offsets, \(L=e_s+e_t\), \(M=R+L\), and \(M_s=r_s+\xi_s+e_s\). Put \(A=I+\tau+\delta\). The following already proved source bounds suffice:

\[
A\le221,\qquad L\ge A-57,\qquad e_s\ge A-146.
\]

The stronger new cap \(A\le216\) is unnecessary here.

## Fixed credit and a whole physical side

An empty integral ordinary centre on a complete target is either at most \(-M_v\) or at least \(S_v+1\). Since \(\beta_s\) is active and

\[
H_s=\beta_s+2d_s,\qquad d_s>0,
\]

the missing \(H_s\) satisfies \(H_s\ge S_s+1\). The missing \(O_s,O_t\) are likewise HIGH. The eight \(O_v+v_i\) labels and the three \(H_s+s_i\), \(i=2,3,4\), are HIGH. A twelfth is \(\alpha_s+s_2\): beta activity gives \(s_2>d_s\), so \(\alpha_s+s_2=H_s-d_s+s_2>H_s\). Thus the compatible fixed credit is 12 and \(\epsilon=\delta-12\ge0\).

On target \(s\), group the full leading resource with these seven actual ordinary native resources:

\[
\beta_s,\ \alpha_s,\ U_s,\ V_s,\ C5_s,\ C6_s,\ C7_s.
\]

The beta capacity is licensed because its opposite paired contribution is empty. The group has original capacity \(K+7\cdot77=K+539\); its capacity deficiency is at most \(\epsilon\). Its actual union lies in the complete target, hence

\[
S_s\ge K+539-\epsilon.\tag{1}
\]

This is an actual union bound, not an assumption that the seven native resources are disjoint.

## Two endpoints and two forest inequalities

Let \(P=C4_t\), let \(\Gamma_P,\Gamma_{\beta_s}\) be the whole-unit native deficiencies, and put

\[
B=\Gamma_P+\Gamma_{\beta_s},\qquad H=\Gamma_{H_t}.
\]

The active 77-point singleton \(H_t\) has \(0\le H\le76\). On complete targets its native loss is exactly its lower plus upper clips. Use the lower endpoint of \(P\) and the upper endpoint of \(H_t\):

\[
P\ge73-r_t-l_P-b_P,\qquad
H_t\le S_t+r_s-72+h_H+b_H.
\]

Their error sources are respectively \(t,s\). Define \(E_c=l_P+h_H\le B+H\) and \(E=b_P+b_H\).

Choose one actual full or trimmed core subset attaining

\[
f=\max\left(69-\xi,\ 65-\frac{\tau-\xi}{2},\ 57-\frac{\tau-\xi}{6}\right),
\qquad\xi=\xi_s+\xi_t.
\]

In particular,

\[
f\ge\frac{199-\tau}{3},\qquad 2\tau+6f\ge398.\tag{2}
\]

The ten retained-resource edges are

\[
\begin{array}{ll}
s:& L_s-V_s-U_s,\quad L_s-C7_s-C6_s-C5_s,\\
t:& L_t-V_t-U_t-H_t,\quad L_t-C7_t-C6_t.
\end{array}
\]

Their gaps sum to \(2Q\), with \(Q=X_s+X_t+g_s+g_t+h_t\). The forest omits both paired endpoint resources, so the actual grouping budget gives

\[
Q\ge5f-\frac{\epsilon-B}{2}.
\]

The two \(X_s\) star edges \(L_s-V_s\) and \(L_t-C7_t\) omit these two paired resources and also \(H_t\), giving

\[
X_s\ge f-\frac{\epsilon-B-H}{2}.
\]

Both are valid statements about the same unchanged deficit. Adding their inequalities gives

\[
Q+X_s\ge6f-\epsilon+B+\frac H2.\tag{3}
\]

## Use the missing H directly

The literal centre identity is

\[
H_t=2d_s+\beta_s+P+2s_4+t_4+g_s+g_t+h_t.
\]

Since \(\beta_s+2d_s=H_s\ge S_s+1\), the two endpoint inequalities imply

\[
S_t\ge S_s+M+M_s+(Q+X_s)+78-E_c-E.
\]

Use (1) and the exact source mass \(S_s+S_t=2K+1239-\delta\). The result is

\[
M+M_s+(Q+X_s)\le59+\delta+E_c+E.
\]

Apply (3) and \(E_c\le B+H\). The paired-loss variable \(B\) cancels and the unchanged residual deficit gives the crucial inequality

\[
M+M_s+6f-\frac H2\le47+2\delta+E.\tag{4}
\]

No endpoint for beta is used, so all positions of its actual native translate are included automatically.

## All four endpoint positions

For a selected clip at most 72, the core rank bound gives \(b_P\le\xi_t\) or \(b_H\le\xi_s\). A selected clip at least 73 is a peeled rank and gives respectively

\[
b_P\le\xi_t+e_t-4,\qquad b_H\le\xi_s+e_s-4.
\]

Let \(p,h\in\{0,1\}\) record the latter two alternatives. Thus

\[
E\le\xi_s+\xi_t+p(e_t-4)+h(e_s-4).
\]

Put

\[
Z=r_s+2I+2\tau+\xi_s+6f-\frac H2.
\]

Substitute \(M+M_s=68+r_s+2\xi_s+\xi_t+2e_s+e_t\) into (4). The offset rows \(L\ge A-57\), \(e_s\ge A-146\) and \(A=I+\tau+\delta\) give:

| Lower P endpoint | Upper Ht endpoint | Consequence |
|---|---|---|
| core rank | core rank | \(Z\le182\) |
| peeled rank | core rank | \(Z\le267\) |
| core rank | peeled rank | \(Z\le A+32\le253\) |
| peeled rank | peeled rank | \(Z\le A+117\le338\) |

All these cancellations are exact. For the four rows the residual offset expressions after subtracting the endpoint error are respectively \(L+e_s\), \(2e_s+4\), \(L+4\), \(e_s+8\).

But (2), \(H\le76\), \(\xi_s\ge0\), and the integer identity \(r_s+2(r_s-34)^2\ge34\) give

\[
Z\ge398+34-38=394.
\]

Every upper bound is strictly smaller. Therefore every actual Z3 A1 configuration is impossible, in either physical owner orientation, including every heavy or light position of all three original endpoint resources.
