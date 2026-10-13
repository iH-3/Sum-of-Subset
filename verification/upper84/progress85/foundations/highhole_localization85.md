# Cardinality-85 localization of the entire high-hole family

Assume the fresh size-85 structural theorem: d=77, e=69, a+b=68,
15<=a,b<=53, I=(34-min(a,b))^2, c>=0, individually primitive integer
cores, and

    kappa+rho+c+I<=600,
    T>=kappa+144-3z, T>=z, T>=144-2z, w<=4z.

Put H=h(P)+h(Q)=kappa+z, mu=mu(P)+mu(Q). The retained verified profile
certificates give the following **two** lower bounds, not just adjusted
defect floors:

| z range | mu floor | rho floor | scalar cap |
|---|---:|---:|---|
|15--16|426|294|c+I<=194|
|17--20|470|338|c+I<=158|
|21--48|514|382|c+I<=170|
|>=49|554|422|c+I+z<=178|

These are minima over every oriented pair a+b=68. The mu values are direct
profile outputs; they do not follow merely from rho<=mu. Keeping the mu
information fixes the failure of the weaker single-maximum comparison in
the last band.

## 1. Source width versus every peeled coefficient

The core's absolute-multiset support has mass

    C0=1190+I+tau=1190+I+mu+H.

If each core mass exceeds H, the elementary sumset-hole lemma fills
[H,C0-H]. Write W=C0-2H=1190+I+mu-H for its endpoint displacement.

Use source offsets alpha_v<beta_v<gamma_v<epsilon_v, one quadruple on
each physical sign. Write

    u=sum(alpha_v+beta_v), C=gamma_s+gamma_t,
    J=sum(epsilon_v-gamma_v), L=C+J=M-R.

The two-maximum source envelope, freshly at d=77, is

    K<=2R+C+166,
    J+u<=612+w-I-tau-c.

Here the central interval, twelve exceptional peeled-pair labels, and
reinsertion of two maxima contribute 1+12+(2*75+3)=166.
The freshly derived outer-layer inequality is

    2C+J<=C0+u-292-2I-c-mu-rho-2z.

Adding the J upper bound gives

    2L<=1510+w-2I-2c-mu-rho-2z.

Maximum removal gives R<=72+rho+H. Thus

    M<=827+H+(rho-mu)/2+w/2-I-c-z
      <=827+H+(rho-mu)/2+z-I-c,

using only the original w<=4z, before any localization.

Subtract from W and use H=kappa+z and the original single budget:

    W-M >= 363+2I+c+3mu/2-rho/2-2kappa-3z
         >= -837+4I+3c+3(mu+rho)/2-3z.                 (1)

Every coefficient has the correct sign; no slack is spent twice. Substituting
the paired mu and rho floors gives minimum margins

    195, 315, 363

in the first three bands. In the tail, (1) gives

    W-M>=627+4I+3c-3z
         >=93+7I+6c>0,

because z<=178-I-c. Therefore every one of the eight absolute peeled
coefficients is at most M<W. The enlarged interval has even greater width
after adjoining each entry, so all eight entries obey the propagation
criterion x<=current_mass-2H+1.

## 2. Each core mass exceeds H

The original budget and T>=kappa+144-3z give

    H<=456-rho-I-c+4z.

In the first three bands this yields respectively

    H<=226-I-c, 198-I-c, 266-I-c.

Their scalar I caps give k<=13,12,13 respectively, where a=34-k is the
smaller side. Exact minimization of T_a-H over those integer ranges gives
lower bounds 171,199,131. No use of side relabeling occurs in the covering
argument; these are symmetric mass bounds.

In the tail, rho>=422 gives kappa<=178-I-c; also z<=kappa. Hence

    H<=356-2I-2c.

Since z>=49, I+c<=129, so k<=11. The exact minimum of
T_(34-k)-(356-2k^2) for 0<=k<=11 is 120, attained at k=7.
Thus both individual core masses exceed H in every high-hole band.

## 3. Localization conclusion

The core sumset-hole lemma supplies [H,C0-H]. Section 1 propagates this
same boundary strip through all eight absolute entries. Complement symmetry
and inclusion of the old absolute support in the new one then give

    z and w are even,
    0<=w<=z,
    eta_s=eta_t=w/2.

This proves localization on the **entire** size-85 high-hole domain. It
uses only original structural bounds before establishing these stronger
conclusions. It in fact does not need the covering index to be zero; the
full slack c is kept throughout.

## 4. Verification scope

highhole_localization85.py reads the already verified retained profile
table and recomputes every paired mu/rho minimum over all 39 oriented sizes.
It independently checks the new scalar and core-mass minima and the exact
integer source constants. This arithmetic accompanies the written interval
propagation proof; it does not replace it.
