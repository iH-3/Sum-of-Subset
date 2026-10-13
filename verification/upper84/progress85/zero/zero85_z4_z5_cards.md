# Fresh Z4/Z5 reductions at cardinality 85

Conditional structural notation and basic cover are in zero85_reduction.md. The stronger source theorem now supplies A<=137 for Z4 and A<=60 for Z5. Below proofs sometimes keep the weaker Z4 cap143, so they remain valid.

All forests/groupings are original full resources. Repeated inequalities may use separate copies of the same deficit; endpoint rebates are made only when the endpoint resources are disjoint from that particular forest/group.

## Z4 source and classification

Fresh rows: S=2K+1162-delta, L>=A+20, e_v>=max(4,A-69), e_v<=301-A; f=61-(tau-xi)/4. A complete-target rank endpoint has lower constant73-r_v and upper constant S_v+r_o-72. Light clip<73 has error<=xi_source; a heavy clip>=73 has error<=xi_source+e_source-4. At most one heavy endpoint is possible in any selected native loss budget<=delta-8<=135. For light outside-hull clips k, b<=k follows from tau_v<=135-k and k(74-k)>=144 on 28<=k<=72.

Both O are absent. Two cap predicates already contradict the five-/four-top tail and source depth. If beta_v,O_v were simultaneously active, their opposite O and their own C7,C6 are holes, since active C7 gives t_v>=110+I while O's raw cap is12. The negative physical-v arm L_o-C7_o-C6_o is fully retained. A retained positive star L_v-V_v plus that arm, rooted at L_v, gives t_v>=K-M+3f-delta+4. With full-core support this is >=147-xi+I; with the four-rank support it is >=123+2xi+I, so it exceeds the double-gap cap27/2. If V_v is the fourth hole, it is HIGH; alpha_v,H_v,O_v are three retained HIGH resources. Use the two shortcuts L_v-U_v,L_o-C7_o, root L_v, and their three unused losses. Full-core overlap gives t_v>=93+I+3r_v>=193. Thus beta/O coexistence is impossible. The remaining one-active-O grammar forces a retained beta/H/C7 triple on the opposite sign, again impossible. Both O are holes and eight HIGH fixed labels give epsilon=delta-8.

The exact A-E/A-H/B retention table follows from the actual cross
chains and beta/H incompatibilities. Put
`N={U_s,U_t,V_s,V_t,alpha_s,alpha_t}` and
`W=N union {P,H_s,H_t,C5_s,C5_t}`. Every unlisted unit is retained.

| Type | Exact whole holes | Actual paired status |
|---|---|---|
| A-E | B,O_s,O_t,Z; Z in W | P empty when Z=P; owner opposite v when Z=C5_v; either actual owner otherwise |
| A-H | O_s,O_t,H_v,Z; Z in W except H_v | B sole on v; P empty when Z=P, owner v when Z=C5_opposite, owner opposite otherwise |
| B | O_s,O_t,X_r,Y_opposite; X_r in {beta_r,H_r}, Y_opposite in {beta_opposite,H_opposite} | Both paired units retained, P sole on r |

For completeness the two-beta-hole B exclusion has a fresh scalar
check. Suppose the beta opposite the active pair1 owner were HIGH.
The exact centre/leading bounds give
`2S_v+K+3g_v+6X_v<=M_o+1161+delta`.
All the relevant ordinary vertices are retained, so the actual
three-edge arm gives `2X_v+g_v>=189-3tau/4-delta`.
Use `K-M>=R-132+A`, `S_v>=T_r+4r+10+tau_v`,
`M_v>=r+4`, the conservative `A<=143`, and R>=68.
The necessary consequence is
`2T_r+9r+4I+7tau/4+2tau_v<=1063`.
But the integral minimum of `2T_r+9r+4(r-34)^2` is1192,
at r=26. Hence that beta is LOW. On the pair1-owner side,
HIGH beta and retained H would give2d<=M_o-1, whereas actual
pair1 activity gives d>M. That beta is LOW too. Their sum cannot
then have branch-B's positive sign, excluding both beta holes.
The literal dispatch is:
A-E retained P uses F for the four U,V holes or H_t, E-H for H_s,
E-alpha for either alpha, E-C5 for C5_t after naming its owner s.
A-H uses F for U,V or empty P, O for opposite-owner choices
H_t,C5_s,alpha_s,alpha_t, and S for C5_t. The three B cases
HH,beta_rH_opposite,H_rbeta_opposite use O,O,S respectively.
The only ownerless residual is A-E with Z=P.

No empty pair is assigned an owner. Exact endpoint/forest predicates
are in Appendix D of the retained report, labels sec:z4-cardF,
sec:z4-cardO,sec:z4-cardS,sec:z4-cardEH,sec:z4-cardEA,
sec:z4-cardEC and the immediately following dispatch (source lines
1962–2158). The calculations below use these literal lists with
fresh capacity77 and source mass1162; their formulas are derived
again from actual target union bounds.

## Z4 Card F

The five weighted endpoint identity has constant233. Its six-edge forest gives the fresh master

`T_r+4r+tau_res+2L-3tau+2e <=229+delta+B`.

For all light endpoints B<=2epsilon. For one heavy endpoint of weight q=1,2 and clip c>=73, B<=2epsilon-qc+q*tau+q*e_v. Since e_v<=L, source L>=A+20 and A<=143 give respectively

```
Q3+tau_res+4e <=332,
Q_(3+q)+tau_res+q*delta+4e+q*c <=332+306q.
```

The integer minima are Q3>=626,Q4>=649,Q5>=665. At e=8 the light lower bound658 exceeds332; q1 lower835 exceeds638; q2 lower1005 exceeds944. All Card F predicates close.

## Z4 Card O

Use the common actual opposite-owner predicate; e=12, epsilon=delta-12. Source-side s has at least six native ordinary resources. The independent common-agent route uses H_s HIGH and V_t=H_s+P_t+2a+b+g_s. Together with the physical side union and four-star/double-arm forest it proves all four endpoint-heavy flags; see the common-agent proof file. A direct new endpoint master is also

`T_r+4r+5xi_s+tau_s+R+L+2e_s+10f+60+4B+(7/2)H <=1006+4delta+Eerr`.

With f=max(137-R,65-(tau-xi)/2,57-(tau-xi)/6), 4tau+10f>=1990/3. Heavy source-s gives upper1091.5, heavy source-t gives1142, all-light A<=73 gives1137, all-light A>=73 gives1207, against respective minima1380+1/3 or1312+1/3. Thus Card O is closed independently.

## Z4 Card S: stronger physical union proof

Same owner of beta_s and P_s forces C5_t inactive. Target t has six actual ordinary native resources H,U,V,C6,C7,alpha, in either branch. Grouping them with its leading gives S_s<=K+700-e, with e=11.

The endpoint identity alpha_s=P_s+beta_s+alpha_t+d_t+2(M+X)+G has constant155. Leading t and the disjoint six- and three-edge forests therefore give

`2M+9f+4e+2N <=545+3delta+B`.

Baseline errors B<=2xi_s+2xi_t. In the all-light case the radial residual is nonnegative, and L>=A+20 implies

`(9/4)I-(3/4)delta+4e+2N <=-577/4`.

Since delta<=143-I-tau and e=11, its left side is at least
`-253/4`, larger by81. In a heavy case cancel e_v-4 from 2L,
retaining L+e_o>=A+24. The resulting row is

`(9/4)I-(3/4)delta+4e+2N <=43/4`.

Since N>=73, delta<=143-I-tau and e=11, its left side is at least331/4, exceeding43/4.

## Z4 empty-beta Cards E-H, E-alpha, E-C5

All side caps come from the actual opposite physical target union, rather than a syntactically chosen set of centres.

### E-H

Physical t has seven native resources, so S_s<=K+623-e. Five endpoints and the two forests give

`R+2L+xi_t+e_t+10f+3e <=416+2delta+Jstar`.

If no lower endpoint is heavy, Jstar<=xi_t+e_t-4. Source L>=A+20 gives `(5/2)I+delta/2+3e<=-469/2`, impossible. If a lower endpoint has heavy clip c, Jstar<=xi_t+xi_v+e_v-4-c; 2L+e_t-e_v>=A+28 gives `(5/2)I+delta/2+3e+c<=-159/2`, also impossible.

### Owner alpha_s missing

Physical t again has seven native resources, so S_s<=K+623-e. The raw-order identity with alpha_s>=1-a and the endpoint/ten-edge forests gives

`L+2e_t+2xi_t+10f+3e+N <=419+2delta+B`.

All-light baseline B<=xi_s+3xi_t leaves 610-(5/2)tau radially; L+2e_t>=A+28 yields `(5/2)I+delta/2+3e+N<=-9/2`.

A heavy error on source t cancels e_t-4; L+e_t>=A+24 yields the same row with RHS -1/2. A heavy error on source s can only be P_s; cancelling e_s leaves3e_t>=3A-207 and yields `3I+tau/2+delta+3e+N<=12`. Here delta>=e+73 and N>=73, so it is impossible.

### Opposite alpha_t missing

Physical t has six native resources, so S_s<=K+700-e. The weighted endpoint identity and eleven edges give

`R+2L+xi_s+e_s+11f+3e <=492+2delta+B`.

Baseline errors are3xi_s+2xi_t, leaving739-(11/4)tau. All light offsets satisfy2L+e_s>=2A+44 and give a negative upper bound. A heavy endpoint of weightq=1,2 satisfies2L+e_s-q e_v>=A+24; its remaining inequality is `(11/4)I+(3/4)delta+3e+4q<=-83/4`, impossible.

### E-C5

Physical t has six native resources H,U,V,C6,C7,alpha, so S_s<=K+700-e. Five endpoints and eleven edges give

`R+2L+xi_t+e_t+11f+3e+N <=493+2delta+B`.

Baseline errors2xi_s+3xi_t leave739-(11/4)tau. Light offsets2L+e_t>=2A+44 yield a negative upper bound. A unique heavy error leaves2L+e_t-e_v>=A+28 and gives `(11/4)I+(3/4)delta+3e+N<=-111/4`. Thus this card is closed.

All displayed Z4 retention rows are excluded. The final ownerless
family `{P,B,O_s,O_t}` has seven actual native ordinary resources on
each physical sign. Its complete independent geometric and scalar
certificate is `../scalar/z4_ownerless_certificate.tex`, checked by
`../scalar/check_z4_ownerless_certificate.py`.
The fresh four-edge arm gives115+I rather than the old131+I; this
still yields X+g>=58 and d-h-X>=3>0, enough for the literal ten-label
gap. The original eighteen-credit ledger is therefore valid.
Deleting the two largest core values gives the actual67-point support
with f=67-(tau-xi); this stronger support closes all four H core-hit
statuses. Both empty pairs remain ownerless throughout that proof.

## Z5 common activity and endpoints

Here S=2K+1085-delta, A<=60, K-M>=R-55+A, K>=153. Every retained singleton has at least17 hits, exceeding all eight source peels together; thus it has an actual core hit. Once sole pair ownership is proved, the same assertion holds for that whole paired capacity. All actual retained endpoint errors are<=xi_source because their selected clips are<73.

Both O are empty before outer integrality: an active O has raw t<=12, whereas leading activity gives t>=R-55+I+tau+2X+g>13.

If beta_v,H_v were both active, its raw cap21 would give2X_v+g_v<=8-I-tau, so tau<8. If either U_v or C6_o were active then q=X_v+g_v would be integral. The two opposite leading/core shortcut intersections give2q>=2(137-R)-delta>=78+I-tau>70, contradiction q<8. If either V_v or C7_o were active the same argument with q=X_v contradicts the cap. Therefore these four ordinary singleton units are all holes; together with the two O holes they exceed j=5. So beta/H cannot both be active.

The report's literal one- or two-coordinate residue classifier then proves outer integrality; the actual cross chains and HIGH own-chain rules prove extreme-leaf retention and the A0/A1/B hole lists. The four outer-coordinate identities used there are unchanged. An empty cross centre is LOW because a HIGH cross loses at least r_v+81>delta leading points.

An empty alpha below a retained H is LOW without a normality bootstrap. A retained H has a core hit, so H<=S_v+R_o. The leading bound gives d_v>=153-delta+g_v+2X_v>R_o (since R_o<=r_o+tau_o, r_o<=41 and delta+tau<=60). Therefore alpha=H-d<S_v. Its emptiness forces alpha<=-M_v, giving h_v<=X_v.

Eight O HIGH fixed labels give epsilon=delta-8. After the outer-integrality classifier every extreme star leaf is retained. On every chosen core support with overlap f, weighted stars give ca*X_s+cb*X_t>=(ca+cb)f-max(ca,cb)*epsilon/2. The four disjoint ordinary groups, including the one-empty form when U or C6 is missing, give cg*g_s+dg*g_t>=(cg+dg)f-max(cg,dg)*epsilon/2. These are separate valid scalar inequalities, not a claim that stars and pairs are disjoint.

Source-only sharpenings needed below are

```
M>=R+99+A,
e_v>=A+16.
```

The first uses the quartet Q<=3 equality case and central-gap
correction, with fresh mass coefficient105: L>=103+A-Q_s-Q_t;
both Q=3 would force L<=12, so L>=98+A. Equality implies a huge
offset with c<=15, leaving a central gap of at least11+I+delta;
hence L>=99+A. These are the same actual exceptional-pair counts
and equality conditions of Appendix E, with the new source mass.

For the second, the sharpened one-maximum envelope is
`K<=2R+c_v+e_o+78+P_v+B_o`.
The actual distinct exceptional triples and pairs satisfy
`2P_v<=a_v+b_v+4-p_v` and
`2B_o<=a_o+b_o+8-p_o`, where p_v records quartet equality.
Consequently `T+J_v-J_o<=168-p`, with `T=105+A`.
Combined with `J>=A+87+p`, this gives `J_v>=A+12+p`.
Since `c_v+p>=4`, it follows that `e_v>=A+16`.
The endpoint tables below deliberately use the weaker `e_v>=A+8`
to preserve their independently audited residuals. The alpha-hole
terminal proof uses the stronger floor16.

## All thirteen Z5 A0 retained-P templates

Keep the report's literal endpoint lists, which are exhaustive after its now freshly proved retention grammar. The fresh constants and baseline rank-error weights are:

Here P=C4_s is the actual sole pair1 owner, a=s4, b=t4, and
G=g_s+g_t. These are the literal endpoint identities; each upper
list is summed with unit weight and each number in the lower list
is its coefficient. No empty pair appears as a resource.

| Card | Upper endpoints | Lower endpoints with weights | Centre identity body |
|---|---|---|---|
| A | V_s,V_t | P,2C5_t,2alpha_s,alpha_t | 5a+5b+2G |
| B | V_s,H_t | P,2C5_t,2alpha_s | 5a+4b+2g_s+3g_t+2h_t |
| C | H_s,U_t | P,2C5_t,3alpha_s | 6a+4b+3G+h_t |
| D | H_s,H_t | P,2C5_t | 3a+4b+3G+3h_s+2h_t |
| E | H_s,U_t | P,2C5_t,alpha_t | 3a+5b+3G+3h_s |
| F | U_s,H_t | P,2C5_t,2alpha_t | 3a+6b+3G+2h_s |
| G | H_s,H_t | P,2C6_t,2alpha_t | 3a+6b+3G+h_s |
| H | H_s,H_t | P,2C6_t,alpha_s | 4a+4b+3G+2h_t |
| I | H_s,U_t | P,2C6_t,alpha_s,alpha_t | 4a+5b+3G |
| J | H_s,H_t | P,2C7_t,alpha_s,2alpha_t | 4a+6b+g_s+3g_t |
| K | U_s,H_t | P,2C6_t,2alpha_t | 3a+6b+3G |

All templates have base holes B,O_s,O_t. The two extra holes are
respectively: D(alpha_s,alpha_t); A(U_s,H_s), A(U_t,H_t),
A(H_s,H_t); B(alpha_t,H_s); C(alpha_t,H_t);
E(alpha_s,H_t); F(alpha_s,H_s); G(C5_t,alpha_s);
H(C5_t,alpha_t); I(C5_t,H_t); J(C5_t,C6_t);
K(C5_t,H_s). This is all thirteen templates, including both
physical owner orientations under reflection.

| Card | Constant | Error weights (s,t) | Maximum native clip weight |
|---|---|---|---:|
| A |310|4,4|2|
| B |305-r|4,3|2|
| C |378-2r|5,3|3|
| D |159+r|2,3|2|
| E |164+2r|2,4|2|
| F,G,K |169+3r|2,5|2|
| H |232|3,3|2|
| I |237+r|3,4|2|
| J |242+2r|3,5|2|

Each constant is constructed as76+sum(weight*(73-r_side)), with r_t=68-r. Use f=61-(tau-xi)/4 and the mass lower bounds M>=R+99+A, M_v>=r_v+xi_v+A+8. Drop positive h terms, except in D. Use the independent weighted star/pair rows and Eclip<=maxweight*epsilon. The residual lower-minus-upper polynomial, after applying delta<=60-I-tau, is bounded below as follows:

| Card | Strict positive lower residual |
|---|---|
| A |356+(9/2)I+tau+xi/2|
| B |166+5I+(3/2)tau+xi/2|
| C |351+(13/2)I+(5/2)tau+xi|
| E |2+5I+(3/2)tau+xi/2|
| F,G,K |178+(11/2)I+(7/4)tau+(3/4)xi|
| H |51+(9/2)I+tau+xi/2|
| I |227+5I+(5/4)tau+(3/4)xi|
| J |281+(11/2)I+2tau+xi/2|

For D both alpha resources are missing and LOW. The two retained HUV triples and cross g_t pair are distinct, with native group deficiencies Psi_s,Psi_t,Omega. Their common f support gives

`3G+3h_s+2h_t>=305+6f-3Psi_s-2Psi_t-Omega>=305+6f-3epsilon`.

This replaces the weaker3G bound. The final residual is at least `53+6I+(11/4)tau+xi/4>0`. Thus all thirteen literal A0 retained-P templates are excluded without assuming any retained endpoint is normal.

## A0 both pairs empty, H_s or C5_s extra hole

Physical side s has six native resources; the other side has seven. Grouping side s gives S_t<=K+623-e. Let A0=alpha_s, B=alpha_t, D=C5_t. The identity H_t=2(a+b)+G+A0+B+D, the generic upper endpoint, and K<=M+R+21 give

`M+2X+G+A0+B+D<=R+572+r_s-e+u_Ht+xi_s`.

Alpha_s is retained. Lower it generically; pack B+D in its actual two-resource group Gamma, giving B+D>=2(73-r_t)+f-2Gamma-2xi_t. Hence

`M+2X+G+f<=R+489-e+u_Ht+l_alpha_s+2Gamma+2xi`.

Let N=Gamma+Gamma_Ht+Gamma_alpha_s. All these endpoints avoid the stars and the four ordinary g groups. Their independent rebates give2X>=4f-(epsilon-N), G>=2f-(epsilon-N)/2. Since the endpoint weighted loss is<=2N, combination yields

`M+7f<=R+489-e+2epsilon+2xi`.

Substitute M>=R+99+A, f=61-(tau-xi)/4, xi<=tau and A<=60 to obtain `2I+3e<=23`. Already e=8 gives24<=23, impossible. Thus both cases close without the old normality assumption or extra fixed ledgers.

## A0 both pairs empty, alpha_s extra hole

Initial fixed ledger e=14 remains valid without normality because both paired components are LOW, the alpha hole is LOW, and d>g proves all F3,F4,F5 labels LOW. With epsilon=delta-14, the leading/stars/pairs give d>=107+g+2X, X_v,g_v>=38, and h_s>=15.

The exact32-type upper-tail classification can therefore reproduce the HIGH21,LOW29,touched23 ledger and e=27 before normality. Two places previously using C5_v>0 are replaced by actual core-hit lower C5_v>=1-R_v: C5_s+s3+h_s>26 follows from e_s+X_s+g_s+h_s+1>26, and C5_t+M_t+2X_t+g_t>16 follows from e_t+2X_t+g_t+1>16. The tail argument only needs h_s>2, not29, to exclude d_s+1,d_s+2. Once e=27, the BAD native-loss floor73-max(r_s,r_t) exceeds epsilon=delta-27 uniformly, so all retained centres are normal.

At e27, the target caps are S_s<=K+546-e and S_t<=K+623-e. If B=alpha_t>=a or D=C5_t>=a, the normal H_t endpoint and lower endpoint of the other centre give M+2X+G+h_s<=R+567-e+endpointloss. Rebate those unused endpoint losses N in both the four-star and triple/pair gap bounds to get A+6f+N<=407+delta-3e. With adaptive f=max(137-R,65-(tau-xi)/2) one has2tau+6f>=398; A<=60 then forces2I+N+3e<=69, impossible at e27. Thus B,D<a. The nine further LOW labels give e34. The fixed-only prefix argument, now with X_t>=38, gives C=C5_s<b and the four further LOW labels give e38.

Five additional distinct labels are LOW:

```
C25_s=C-D-2b-g_t<0,       C25_t=D-C-2a-g_s<0,
C35_t=C25_t-h_t<0,
C45_s=C35_s-g_s<0,        C45_t=C35_t-g_t<0.
```

Normality gives C,D>=1, while the proved bounds C<b,D<a give the
two strict signs. C25_s,C25_t occupy their one previously untouched
baseline group; the other three labels lie in groups already
occupied respectively by V3_t,V8_s,V8_t. Thus the ledger has
HIGH21,LOW47,touched26 and genuine compatible credit42.
This counts the eight O HIGH labels once. The labeled incidence is
recomputed against the original26 baseline groups by the checker.

For completeness the actual endpoint/group transport is as follows.
Pack B=alpha_t and D=C5_t in their two-resource group Gamma.
The retained H_s,U_s,V_s form a three-resource group Psi.
The two g_t pairs U_t,V_t and C6_s,C7_s form Omega.
The separate C=C5_s and H_t endpoint losses are unused by these
groups. All these are original77-point native resources. The
source Q chosen below is common to their packing and the stars.
If its size is q>=61 and its overlap is f, then

```
2B+D>=3(73-r_t)+f-3Gamma,
G+h_s>=q+f-Psi-Omega/2.
```

Use the two normal H upper endpoints, the normal C lower endpoint,
and the exact H centre identities. Rebate the distinct native losses
in the group bounds and in the separately valid weighted-star
bound `2X_s+4X_t>=6f-2epsilon`. Their combination gives

```
2M_t+2q+11f<=2R+827+2r_t-delta+5epsilon.
```

In particular q>=61 permits the conservative constant122.
Substitute M_t>=r_t+xi_t+A+16, epsilon=delta-42,
and delta<=60-I-tau. The necessary scalar inequality becomes

```
4I+4tau+11F-2xi_s+210<=929.
```

For each sign choose independently whether to retain all core
values or delete its largest j=1,2,3,4 magnitudes. Define
`phi_v=min(xi_v,min_j(j+floor((tau_v-xi_v)/j)))` and
`F=69-phi_s-phi_t`. The minimizing choices give one actual common
Q of size at least61 with overlap at least F at zero displacement;
all displacements subtract their integral gap. Hence this is an
actual source selection, not a combination of different budgets.
Credit42 and A<=60 restrict tau<=18. Exact enumeration of every
nonnegative integer tau_s,tau_t,xi_s,xi_t with xi_v<=tau_v and
tau<=18 has minimum

```
4tau+11F-2xi_s+210=935>929.
```

Dropping the nonnegative4I only enlarges the domain, so this finite
certificate excludes every size and every residual mass. The
independent derivation, labeled ledger, all7315 relaxed scalar
states, and exact checker are in
`../foundations/z5_alpha_final85.md` and
`../foundations/z5_alpha_final85.py`. The scalar checker verifies
the displayed finite consequence; the geometric prerequisites
above remain written actual-resource arguments.

## Z5 A1 and branch B

The activity/outer-integrality classifier is the literal Appendix E
classifier following equation(z5-crosschain). It is valid with the
fresh base reductions above. For split beta the whole paired unit
alone is charged: its hit count N obeys77-delta<=N<=77 and
beta_s+beta_t>=N-M. There is no selected-component capacity.
For sole beta, normalize s to its actual owner; its base holes are
O_s,H_s,O_t. When pair1 is empty, the final extra hole is exactly
alpha_s,H_t,alpha_t,C5_s,C5_t,or U_s.
The independent fresh exclusions for all split, retained-pair1,
empty-pair1 and branch-B alternatives are in
`zero85_z5_a1_b.md`, with exact arithmetic in
`check_zero85_z5_a1_b.py`.
The final C5_t case's cutoff and32-type tail received the
independent receipt `../scalar/z5_c5t_cutoff_audit.md`, checked by
`../scalar/check_z5_c5t_cutoff_audit.py`.
