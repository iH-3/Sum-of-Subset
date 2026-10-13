# Fresh structural deductions at cardinality 85

These deductions concern a hypothetical zero-containing **integral feasible**
set A of size 85. Zero follows only after the preceding exclusion of all sizes
at least 86 has been accepted: a zero-free size-85 example could otherwise be
extended by adjoining zero. The general inverse/stability/defect theorems are
the imported mathematical inputs identified in the audited upper-85 package.
This is an intermediate proof supplement, not yet the complete STRUCTURE85
theorem; the both-non-AP inverse and overlap repairs are supplied separately.

## 1. Bootstrap, derived from the new cardinality

Four-on-each-sign outer deletion and two four-element peels give
d=77, e=69, m=68. If an outer sign had fewer than four elements, provisional
peeling from the available sign gives a one-sided core with at least 70 points,
whose subset-sum count is at least 1+T_69=2416. Before the outer deletion size
has been fixed, use the safe upper bound s<=24|D|+77<=24*85+77=2117, not a
premature substitution |D|=77. If a sign disappears
under the further peels, a one-sided 69-point core gives s>=1+T_68=2347,
whereas s<=24*77+77=1925. Thus both physical signs actually support all the
required extreme deletions.

The unpaired-absolute-value estimate gives q^2<=96e+1073-e^2=2936. Here q is
even, so q<=54; at least (68-54)/2=7 opposite pairs remain in E. In particular
zero is not a diagonal exception and both core sides have at least 7 elements.

Reflect only in scalar analysis and write a=34-k, b=34+k. Then
Lambda=1+T_a+T_b=1191+k^2 and Omega=22*77+97-Lambda=600-k^2.
The larger-side adjusted defect is nonnegative; the smaller-side uniform
bound is rho_P>=-8. The exact slack identity therefore implies k^2<=608,
so k<=24 and a>=10. The initial small rows are:

| a | b | k | Omega | Omega+8 |
|---|---|---|---|---|
|10|58|24|24|32|
|11|57|23|71|79|
|12|56|22|116|124|
|13|55|21|159|167|
|14|54|20|200|208|

At a=14 the threshold-14 theorem improves the last slack bound to Omega=200.
At a=13, the actual threshold-14 induction table gives Phi_13<=4,
hence rho_P>=-2; if its support is non-AP, the general non-AP theorem gives
the stronger rho_P>=-1.

## 2. Exact layer constants

On a common core lattice, maximum removal gives
R_s+R_t<=72+rho+kappa+z when both core sizes are at least 15. A smaller side
requires adding 8 to this maximum bound, or 16 to a two-span comparison.
The conservative pre-lattice D1 comparison has constant

    C=2m+4e+14-Lambda=-765-k^2,
    C+Omega=-165-2k^2.

Thus F1-2F0<=-165-2k^2+2z, with an additional +16 if a<=14.
After the source layers and their actual overlaps have been established,
the sharp restricted-sum inequality is G=2d-10=144. It gives

    T>=kappa+144-3z, T>=144-2z, T>=z, T>=48,
    c+rho+T<=600-k^2, w<=4z.

The quantitative layer rows, using |R(E)|<=2R-1 instead of the conservative
2R+1 bound, are freshly derived as follows:

    F2-2F1=-293-2k^2-c-rho-mu-2kappa-2theta-2ell2-2g;
    V0-C1+delta+2z<=-292-2k^2-77j-mu-rho;
    F1-2F0<=-167-2k^2+rho-mu+2z-c-2theta-ell1-g;
    U0-C0+delta-2z<=-166-2k^2-77j, U0-C0<=0.

The last two rows assume the maximum-removal bound with core sizes >=15;
they are not silently applied on small boundaries.

## 3. Boundaries 10, 11 and 12

At a=10 a non-AP larger Q would give rho>=-8+(58-5)=45>Omega=24.
Hence Q is AP. Its intrinsic step forces P onto the same lattice by residue
counting, because kappa<=32<T_58. The AP-plus-set formula precludes a clipped
gap and gives h_Q=z=0,h_P=kappa. The conservative D1 comparison with +16 is
strict, as is the outer comparison Lambda>4d-10+(Omega+8). Consequently D is
integral on this lattice and G144 applies. But T>=144>Omega+8, impossible.

At a=11 and non-AP Q, rho_Q>=52, so kappa<=71+8-52=27<T_11-1=65.
The strict simultaneous inverse supplies the common lattice and both hole
bounds. The layer comparisons are strict even with z<=79 and +16; G144 is
therefore available. Then T+rho>=48+52-8=92>71. If Q is AP, the preceding
z=0 argument gives T>=144>79.

At a=12 and non-AP Q, rho_Q>=51 and kappa<=116+8-51=73<T_12-1=77.
The strict inverse again supplies the common lattice and strict Q upper-hole
bound; both layer comparisons are strict. From G144 and rho>=43 we obtain
144-2z+43<=116, hence z>=36. Therefore h_Q>=36. The parameterized effective
hole witness (r,beta,C)=(56,5,132) has

    K=17,D=149,E=150,M=20,J=20,
    (r-J+1)beta-D=36>0,
    T_(J-1)-1-D=40>0.

It gives mu_Q>=189; the retained flexible defect inverse gives rho_Q>=125.
But the budget gives rho_Q<=116+8=124. The AP-Q branch has z=0 and is already
excluded by T>=144>124. Thus every surviving core has a>=13.

## 4. A general no-empty-unit obstruction

This uses only the original 55-fixed-label raw gap bounds, not any newly
strengthened gap count. Once D is integral, suppose j=0 and w<=104. All four
own centers on both signs are active, so all outer magnitudes are integral.
The source maxima satisfy M>=m+8=76; active C7 gives t_v=d_v-M>=5, hence
d_v>=81. Choose a genuinely contributing beta sign s (the beta pair supplies
one in branch A, and both beta singletons contribute in branch B). Then

    t_s<=(57+eta_s)/2<=(57+w)/2<=80.5,
    t_t<=56+eta_t<=56+w<=160.

An active C4_s forces t_s>d_t>=81. An active C4_t forces
t_t>h_s+d_s>2d_s>=162. Both alternatives are impossible, although pair1
must contribute when j=0. Thus every aligned configuration with j=0,w<=104
is excluded. In particular this applies whenever c<77 and w<=104.

## 5. Complete AP-branch simplification for a>=13

The larger-AP case forces one common residue and gives z=0 as before.
If its smaller side is nonprimitive, h_P>=T_a+mu_P, and hence
c<=Omega-144-T_a-rho_P. The maximum cap over all a>=13 is 59; the a=13
universal floor rho_P>=-2 is included. Therefore c<77 and the no-empty-unit
obstruction excludes every such branch, without 152 auxiliary certificate
systems. The larger unit-step AP side is intrinsically primitive. A smaller
primitive side is the remaining legitimate z=0 structural alternative.
At a=13, Q AP also gives c<=159+2-144=17, and at a=14, Q AP gives
c<=200-144=56; both boundaries are excluded by the same obstruction.

Suppose only the smaller support is AP. The residue-count inequality
kappa>= (#residues-1)(u-1), with u>=T_a+1, and Omega<2T_a over all the
present rows permits at most two residue classes. A one-residue clipped gap
or a unique off-scale generator forces final disjoint supports of Q and
mu_Q>=T_(b-2). The necessary budget cost

    T_a+T_(b-2)+2-2b+rho_P

strictly exceeds Omega in every row; the executable checks these margins.
If there is one residue and no clipped gap, z=0,h_Q=kappa,h_P=0. The larger
side is primitive because h_Q<=Omega-rho<T_b<=|FS(Q)|-1, and the smaller
unit-step AP support is primitive. This is another legitimate z=0 alternative.
Its a=13 boundary is impossible because T+rho>=144+50-2=192>159. At a=14,
c<=200-144-49=7<77 and w=0, so the no-empty-unit obstruction excludes it.

In the remaining two-residue case, at least two nonzero-residue generators
force that residue to have order two. Normalize U=2[0,u-1]. Let W be the
least odd Q coefficient and t>=2 the number of odd Q generators. The
parity-fiber identity, before using a hole bound, is

    kappa=u-1+eta, h_P=u-1,
    h_Q=kappa-u+W, z=W-1,
    mu_Q+kappa=sum(Q)+u-W-T_b.

Distinct even and odd generators give

    sum(Q)>=(b-t)(b-t+1)+tW+t(t-1).

The exact finite minimization in ap_bootstrap85.py proves that W>=17
contradicts mu_Q+kappa<=Omega+2b-2-rho_P, with minimum contradiction
margin 22. It uses the floor rho_P>=0 for a>=14 and rho_P>=-2 for a=13.
Since W is odd, W<=15, hence z<=14; also W<u, so h_P,h_Q<=kappa.

For this half-step branch, distinct-generator bounds give

    R_P+R_Q<=m+a+mu+kappa-T_a+14.

The conservative D1 comparison therefore gives

    F1-2F0<=2367+2a-4T_a-2T_b<=-761<0.

The outer-layer strict comparison likewise holds. D is integral and its
extreme support translates intersect; w<=4z<=56 and G144 apply.
Using rho_Q>=b-5 then gives

    c<=Omega-T_a-144+42-(b-5)-rho_P<=61<77.

The no-empty-unit obstruction excludes every half-step branch. This includes
the smaller-AP a=13 boundary. The only remaining a=13 or a=14 possibilities
have both supports non-AP; their inverse repairs are treated separately.

## 6. Executable scope

ap_bootstrap85.py checks every scalar row k=0,...,21, the exact odd-coefficient
mass minimum, half-step and nonprimitive caps, lattice-comparison constants,
and one-residue contradiction margins. It supplies no computational proof
of the general inverse theorem or the actual-set parity-fiber identities.
The result file is ap_bootstrap85_results.json.
