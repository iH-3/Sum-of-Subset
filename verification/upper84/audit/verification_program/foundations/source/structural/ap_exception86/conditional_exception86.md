# SIZE86 elementary covering exceptions, rebuilt from actual-set inequalities

## Result and scope

All three conditional families below are impossible. Together they give 152 size/mode systems. The supplied SIZE87 integer multiplier vectors, unchanged, verify all 152 freshly rebuilt SIZE86 systems. Minimum contradiction magnitude: 283. A redundant finer half-step check verifies another 256 exact-even-z systems.

This is a conditional mathematical lemma, not a proof of the entire SIZE86 structural theorem and not an endpoint86 exclusion. Every use requires the preceding common-core lattice, integral D, the covering construction and its branch classification, and extreme-translate overlap/hole propagation to have been established. The G=146 inequalities are used only after those hypotheses. The separate argument establishing the half-step caps is not proved here.

The only certificate inputs are the four integer vectors in `inputs/four_integer_vectors.json`. Their applicability is established by the actual-set arguments below.

## 1. Parameters and conditional families

Write T_r=r(r+1)/2, m=69, d=78, e=70, G=146. Before an optional orientation reversal let a=34-k be the smaller core side and b=35+k the larger. Then Lambda=1226+k(k+1) and Omega=587-k(k+1). Core coefficients are distinct positive integers on the common unit lattice. Let rho_P,rho_Q be the usual nonnegative defect-adjusted excesses, mu_P the support excess, kappa the mixed excess, z the mixed hull-hole defect, c the full-cover slack, and w the number of holes in the target support FS(D). The established overlap/propagation hypothesis gives w<=4z.

The covering identity uses K=|2D|, positive and negative masses S_p,S_q of D, and two leading units plus eighteen D-units after pairing:

    c=2K+18d+85-|FS(D)|,
    |FS(D)|=S_p+S_q+1-w,
    S_p+S_q+c-2K=1488+w.

Here 1488=18*78+84; the fixed-point allowance is unchanged because the covering construction still uses four outer extrema on each sign.

### Family I: larger AP, smaller nonprimitive

Assume a,b>=15; Q has unit-step AP support; h_Q=z=0 and h_P=kappa; and P has integer gcd g>=2. For u=|FS(P)|=1+T_a+mu_P, the support lies in gZ, so its hull has at least g(u-1)+1 positions. Therefore, without assuming FS(P) is an AP,

    h_P>=(g-1)(u-1)>=T_a+mu_P.

The post-G budget gives

    c+rho_P+rho_Q+kappa+146<=Omega,
    c+mu_P+rho_P+rho_Q<=E=Omega-146-T_a.

All dropped terms are nonnegative. The complete range 0<=k<=19 has E>=0 precisely for k=7,...,15:

    k:      7  8  9 10 11 12 13 14 15
    a:     27 26 25 24 23 22 21 20 19
    b:     42 43 44 45 46 47 48 49 50
    E:      7 18 26 31 33 32 28 21 11

Equivalently 2E=-308+67k-3k^2. Thus c<=33<78. There is no need to prove FS(P) AP or g=2. In particular the SIZE87 inference mu_P<a-3 is not imported: it is false as a uniform deduction at SIZE86.

Every P coefficient is a positive multiple of g>=2. Consequently its maximum is at least 2a and its total mass is at least 2T_a. These elementary stronger rows are the essential repair.

### Family II: smaller half-step AP, larger non-AP

Assume a,b>=15 and the preceding parity-fiber argument has established, on the common integer lattice,

    FS(P)=2[0,u-1], h_P=u-1, h_Q=kappa-u+w_odd,
    z=w_odd-1, 0<=z<=12, kappa>=u-1>=T_a.

Here w_odd is the least odd Q coefficient, not the target hole count w. Assume Q is non-AP and thus rho_Q>=b-5. The valid post-G inequality T>=kappa+146-3z gives

    c<=F_z=Omega-T_a-146+3z-(b-5).

Relax to z<=12. The complete range 0<=k<=19 has F_12>=0 precisely for k=7,...,15, with caps

    F_12:   6 16 23 27 28 26 21 13  2.

Thus c<=28<78. Since every P generator belongs to 2Z, the same maximum and mass strengthenings R_P>=2a and core_mass(P)>=2T_a apply. The covering mass RHS is at most1488+48=1536. The two relaxed RHS are monotone in z, and all certificate weights are positive; verifying the z=12 relaxations suffices. For completeness the checker also verifies every budget-admissible even z in{0,2,...,12}, without claiming that every relaxation is realizable.

### Family III: the a=14 AP boundary

Assume oriented core sizes(14,55), a larger AP unit support, z=0, rho_P,rho_Q>=0, and all structural hypotheses stated above. Here k=20 and Omega=167. The post-G budget gives c<=167-146=21<78. No nonprimitive or half-step premise is made. Both core maximum/mass rows use their ordinary integer bounds R>=r and core_mass>=T_r. The two orientations and four modes give eight systems.

The nonnegative rho at size14 and the derivation of integral D with its small-prefix correction must be established before applying this conditional family; they are not consequences of these certificates.

## 2. Why all units contribute and outer elements are integral

In every family c<d=78. Each of the eighteen covering D-units has capacity d. If a unit makes no actual contribution in its designated open target half-line, the full capacity d is lost. The covering inequality would then imply c>=d. Hence j=0 and the usual missing-unit correction is zero: delta=c.

In particular all four own translates on each sign are nonempty, since neither pairing removes indices0,1,2,3. Write the outer positive magnitudes as p_1>p_2>p_3>p_4>M_p and

    c_p=p_1-p_2-p_3-p_4,
    b_i=c_p+p_i.

An actual contribution expresses each b_i as an integer target subset sum minus an integer element of D. Thus b_i is integral. The identity c_p=-b_1+b_2+b_3+b_4 proves c_p integral, and p_i=b_i-c_p is integral. The reflected argument proves every q_i integral. This uses no leading-unit contribution, rank-only integralization, or core primitivity.

The first paired unit has centers c_p-q_1 and c_q-p_1. Their sum is

    -(p_2+p_3+p_4+q_2+q_3+q_4)<-(M_p+M_q).

If both actually contributed to their positive reflected hulls, the sum would exceed -(M_p+M_q). Therefore exactly one contributes. Reflect the whole configuration so its contributor is the p component. Reflection can exchange the two core cardinalities, which is why both orientations must be checked.

For branch A the second pair is(beta_p,beta_q), with beta_p=2p_2-p_1-p_3-p_4 and its reflected analogue. The unpaired index5 cross centers both contribute. Their sum is >-(M_p+M_q), and the identity

    beta_p+beta_q=-(c_p-q_2+c_q-p_2)-2(p_3+p_4+q_3+q_4)

forces beta_p+beta_q<-(M_p+M_q). This pair therefore has exactly one contributor. For branch B, the branch premise beta_p+beta_q>0 and the rearranged identity show the index5 pair has center sum<-(M_p+M_q), again giving a sole contributor.

Thus the four relaxed modes(A,0),(A,1),(B,0),(B,1) are exhaustive. The second index is the selected contributor in the second pair. No stronger classification eliminating modes is needed. This reasoning uses j=0 and integer D, not z=0, so it applies equally to Family II.

## 3. Fresh elementary rows and their actual-set proof

All variables are nonnegative. Indices of center slots are zero-based, while the ordered outer magnitudes are numbered1,...,4. Define

    alpha_p=p_2-p_3-p_4, beta_p=2p_2-p_1-p_3-p_4,
    pos=(c_p+p_1,...,c_p+p_4,c_p-q_1,...,c_p-q_4,alpha_p,beta_p),

and define neg by interchanging p,q. Remove indices4 and9 on both sides for branch A, or4 and5 for branch B, retaining pair1p and one selected pair2 contributor. This gives eighteen actual D-slots.

1. Outer integer order gives p_i>=p_(i+1)+1 and p_4>=M_p+1, with reflected inequalities. Four distinct integral inner peeled positive points lie above the positive core maximum R_p, so M_p>=R_p+4.

2. An r-point integral core has R>=r and mass>=T_r. If it is the smaller nonprimitive/half-step side in Families I,II, every coefficient is a multiple of an integer >=2, giving R>=2r and mass>=2T_r. Put t=2 for that side and t=1 otherwise. The three inner peeled positive points other than M_p are at least R_p+1,R_p+2,R_p+3. Hence

       S_p>=t*T_a+M_p+3R_p+6.

   The exact selected rows are -R_p<=-t*a and 2M_p+6R_p-2S_p<=-2(t*T_a+6), with reflected analogues. Historical row labels are retained for certificate compatibility; their SIZE86 right-hand sides are rebuilt with the appropriate t. Nothing presumes gcd1.

3. For a retained active integral p-center v, let l count its v+D points below1 and u count those above S_p. There are d-l distinct integer points above0, all at most v+M_p. There are d-u distinct integer points at most S_p, all at least v-M_q. Nonemptiness of the target intersection ensures the interval orientations. Consequently

       -v-M_p-l<=-78,
        v-S_p-M_q-u<=-77.

   The reflected q inequalities have the same form. For paired units the selected contributor is the sole actual contributor, as proved above, so its ordinary hull losses apply without a split-pair error.

4. Each retained D-slot contributes at most d-l-u points to its target hull. Choose leading losses L_p,L_q as K minus each leading unit's actual target-hull count. They are nonnegative, without assuming those units nonempty. The cover and the fixed-point allowance imply

       sum(l+u)+L_p+L_q<=delta.

   Duplicate covered points merely weaken the covering upper bound. No endpoint row for a leading component is used.

5. D is integral in[-M_q,M_p], so 2D lies in[-2M_q,2M_p]. Therefore K<=2M_p+2M_q+1.

6. Since delta=c, the exact covering identity and w<=4z give

       S_p+S_q+delta-2K<=1488+4z.

   Families I and III use z=0 and Family II uses z<=12. This is why zero-hole propagation is not silently imported in the half-step family.

7. The final row is the respective delta cap E,F_12,or21 from Section1.

No selected row uses an inverse theorem, a primitive-core hole bound, an AP-free span bound, a parity defect inequality, a new lifted geometry, or initial outer integrality before j=0 proves it.

## 4. Exact certificate replay

The supplied multiplier lists contain four positive integer row combinations. check86_elementary.py independently encodes the rows above as sparse dictionaries indexed by semantic variable names. It imports only Python standard-library modules. It does not import or execute the SIZE87 builder or any generic endpoint model. The pinned source vectors are read as numerical inputs only.

For each oriented parameter row and each mode it checks unique existing labels and positive integral weights, sums every coefficient and right-hand side exactly, and verifies a componentwise nonnegative total coefficient vector with a strictly negative total right-hand side. This contradicts nonnegativity of every variable.

Minimum contradiction magnitudes by family and mode:

    family                A/0    A/1    B/0    B/1
    I: nonprimitive        283   2002   1378    362
    II: half-step          288   1666   1274    367
    III: boundary14        295   1236    352    374

Families I and II each have nine imbalances times two orientations times four modes=72 systems. Family III has8. All152 pass. The exact-even-z half-step replay has256 systems and also passes.

As a diagnostic, merely transplanting the weaker SIZE87 integer-core rows would not close Family I: A/1 at oriented a=24,23,22 has summed right-hand sides54,138,44. The elementary divisibility strengthening is logically necessary for this replay and is explicitly justified above. Neither a passing unchanged numerical transplant nor the historical count152 is used as evidence of completeness.

## 5. Files and reproducibility

The four exact integer multiplier lists are in `inputs/four_integer_vectors.json`. `check86_elementary.py` constructs every inequality above and compares each exact coefficient sum and right side with `expected/elementary_results.json`. `expected/elementary_output.txt` is its complete expected text output.

Run `python -I -S -B ap_exception86/check86_elementary.py` from the package root. The checker verifies the local vector SHA256 and does not write files. The full package command is `python -I -S -B verify_package86.py`.

This lemma is conditional on the preceding structural and branch-cap hypotheses, which are proved in `STRUCTURAL86.md`. Within each stated family the elementary contradiction is closed.
