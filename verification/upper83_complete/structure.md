# Size84 structural reduction and all high-hole strata

Base cf26c50. These arguments, the common source interface and all local terminals form the size84 exclusion in the companion report.
General dependencies: size85 foundation lemmas, source Theta<=2d+8, all-rank kernel. Their proofs are cardinality independent; finite size85 rows are NOT imported.

## Fresh parameters and layer identities
n84,d76,e68,m67,a=33-k,b=34+k,I=k(k+1).
Lambda=1157+I; Omega=612-I; C=2m+4e+14-Lambda=-737-I.
C+Omega=-125-2I. G=142. T>=max(48,z,142-2z), T>=kappa+142-3z.
Unpaired bound2977, odd q<=53, at least7 opposite pairs.
Provisional deficient sign: 1+T68=2347>24*84+77=2093.
Disappearing sign:1+T67=2279>24*76+77=1901.
Uniform rhoP>=-8, rhoQ>=0 gives k<=24,a>=9.

Once common core lattice exists, exact pre-G D1 bound is -125-2I+2z (+16 for a<=14). Outer comparison Lambda>294+Omega-rho is strict even with rhoP=-8.
For a,b>=15, maximum removal R<=71+rho+kappa+z. Restrict R(E)<=2R-1, giving fresh:
F2-2F1=-251-2I-c-rho-mu-2kappa-2theta-2ell2-2g;
F1-2F0<=-127-2I+rho-mu+2z-c-2theta-ell1-g.
After actual source layer overlap:
C0-U0>=126+2I+c-2z;
C1-V0>=250+2I+c+mu+rho+2z;
c=76j+delta. C0=1156+I+tau.

## Small boundaries
A larger AP Q yields z0 and common lattice by residue counting; strict pre-layer comparisons then G142. At a9 Omega12, nonAP Q costs -8+53>12, and AP costs T>=142>20. At a10 Omega60, nonAP Q has kappa<=16<T10-1; strict inverse, T48+52-8>60. AP costs142>68.
At a11 Omega106, nonAP Q has kappa<=63<T11-1. Strict inverse, G142 yields z>=40. Reuse universal effective witness (r56,beta5,C132), hQ>10 =>muQ>=189=>rhoQ>=125>106+8. AP costs142>114.
At a12 Omega150: both nonAP, actual sufficient inverse failure gives rhoQ<=73. Endpoint repair beta3,q14,j19,H6 (see check_structure.py), obtains joint lattice. Pre-layer strict. Then T>=142-12 and rho>=-8+50 imply cost172>150. In actual strict inverse branch kappa<=108, D1<=-817. G142 gives z>=17; effective (55,4,119) =>rhoQ>=113; T48+113-8=153>150. AP branches handled by general AP argument below (their c caps are negative).
At a13 Omega192: failed inverse R94 beta4,q14,j23,H8; cost c<=192-48-(142-16)=18<76,w<=32, j0 obstruction. Strict inverse: if z>=13, effective (54,6,168) givesrhoQ153 and48+153-1=200>192. Otherwise c<=26<76,w48, j0.
At a14 Omega232: failed inverse R118 beta5,q14,j24,H10 gives c<=62<76,w40. Strict branch coarse pre-layer strict since kappa<=184. If z>=15, independently certified primitive r53 h15 profile gives rhoQ>=269>232 (no D/G circularity). Otherwise c<=70<76,w56. j0 in both.
So surviving sizes15..52.

## AP branches and low-c lemma
Both-AP branches must be divided at a=33. For12<=a<=32,
kappa<=Omega-rhoP<T_b, so residue counting on the larger AP gives
one residue. The AP-plus-set formula then has no clipped gap:
z=0,hQ=0,hP=kappa. This holds for any integer intrinsic step of P;
no two-residue bound is needed here. A nonprimitive P is excluded
by the low-c argument below. In the only remaining balanced case
a33,b34, Omega612<2T33=1122. On the common rational scale let p,q
be coprime intrinsic AP steps. The two residue counts force p,q<=2,
leaving(1,1),(1,2),(2,1). Unequal steps have z0 and kappa equal to
one AP support length minus1, hence at leastT33. Strict pre-G
layers and G142 give c<=612-142-T33<152,w0, and the low-c lemma
excludes them. Thus the surviving both-AP case has common unit step.
When ONLY the smaller support is AP, the larger nonAP floor is
rhoQ>=b-5. The correct bound is kappa<=Omega-rhoP-(b-5)<2T_a,
checked in every row12<=a<=33. This is the premise for its at-most-two
residue alternatives, including the parity-fiber calculation below.
When ONLY larger Q is AP, use rhoP>=n(a), so kappa<=Omega-n(a)<T_b in every row. This licenses the claimed one-residue branch without the false balanced Omega<T_b assertion.
For a>=12, one clipped residue or unique off-scale generator costs T_a+T_(b-2)+2-2b+rhoP>Omega (rhoP -8 for12,-2 for13,0 afterwards).
Larger AP or one-residue unclipped smaller AP gives z0. Nonprimitive small side cap c<=Omega-142-T_a-rhoP<=85<152. Since w0, j0/j1 are impossible by already proved zero-hole lemmas; their use only needs common integral source, not individual primitivity.
Two-residue smaller AP: normalize U=2[0,u-1], least odd W, t>=2 odd Q generators. Exact mass floor
muQ+kappa>=u+(b-t)(b-t+1)+tW+t(t-1)-W-T_b.
Against Omega+2b-2-rhoP, finite minimization forces W<=17, hence z=W-1<=16 and W<u. Exact parity-fiber identity gives hP,hQ<=kappa. The general pre-G D1 comparison (-125-2I+2z plus small16) is already strict; no special half-step layer constant is needed. G142 gives c<=93<152,w<=64.
If c<152, either j0 (contradicts w>=2d+8=160) or j1 with delta<=75. For j1,w<=64, K>=2d-1=151 makes leading active. The original one-hole actual owner grammar (using raw first cap12+eta<=76, double17+eta<=81, and active C7 d>=M+5>=80) gives the standard six-edge terminal and beta/O owner side. The raw caps remain sufficient at w64: single cap12+eta could76 when eta<=w, so still <80; double<=81 gives t<=40.5. Thus same pair arguments hold.
Source cap tau<=380+w<=444. All-rank phi_s+phi_t cannot reach42 since min(Tp+Tq,p+q=42)=462>444, so F>=27. Six-edge forest gives2X+G>=162-delta>=87. Owner identity and beta/O cap give2X+G<= (17+w)/2-2<=38.5 (use eta<=w; no localization needed). Contradiction. This excludes every half-step branch. IMPORTANT: use eta<=w, not w/2 before localization.

## Both nonAP inverse repairs
Actual sufficient test holds automatically on larger side. Small test floor succeeds k0,1; failures k2..21 use endpoint choices specified and verified in check_structure.py. Same proof as previous endpoint repair, but q can be any>=20 satisfying Tq-b-1>R, allowing prefix floor n(q).
Fresh main repaired rows k2..18 have H<=18; diameter margins positive. Pre-G D1 strict. Repaired Q is primitive; if P nonprimitive its cap c<=65<76, w<=72<160, so j0 obstruction excludes. Thus P primitive.
For STRICT inverse main branches, z<=62+I makes D1 strict. If z>=63+I, both cores individually primitive already (strict inverse hole bound). We can use the UNIVERSAL dense h49 certificate BEFORE D-integrality; it does not depend on G142. If one final support splits disjointly, it costs rhoX>=T_(r-2)+2-2r, while other hasrho>=profile49(s). Across all38 oriented sizes15..52, cost+profile49(s)+(63+I)-Omega>=77. Hence both final translates intersect. Maximum-removal hX/2 sharpening gives D1<=-125-2I<0. This replaces all large-hole endpoint repairs and is noncircular. Original source outer layer then aligns and intersects.

## Complete high-hole stratum
With sizes15..52 and primitive cores, paired universal floors over a+b67:
h15: (mu,rho_elementary)=(418,288);
h17: (461,331); h21:(503,373); h49:(539,409).
Use independently verified profile table (all relevant r15..52 present).
Two-max source gives J+U<=624+w-I-tau-c. Outer layer gives2L<=1530+w-2I-2c-mu-rho-2z.
Then M<=836+H+(rho-mu)/2+z-I-c; core central width W0=1156+I+mu-H satisfies
W0-M>=-904+4I+3c+3(mu+rho)/2-3z.
Bands15..16,17..20,21..48 give positive margins107,224,266.
Their I+c caps214,179,191 and H caps246,219,289 give individual core mass minusH minima139,166,96.
Tailz>=49: kappa<=203-I-c, H<=406-2I-2c, I+c<=154, so each coremass>H (compute minimum). If j>=1,c>=76, then z<=127-I-(c-76), width margin>=518+3c-3z>=365+3I+6(c-76)>0. If j0, use unlocalized universal raw bound w>=2M+10 and w<=4z to getM<=2z-5<=401; W0>=mu+2rho-68+3I+2c>=1289. Hence same strip propagates in all cases, w<=z and even. For j>=1 source A<=380+w but tau>=418+2z, contradiction (stronger in later bands). For j0 and z<=48, w<=48 contradicts no-empty w>=160; in tail tau>=539+2z and A<=456+w<=456+z contradict. All high-hole families gone without old first-gap H1 transport.
