# Non-progression defect theorem

Dependencies: the uniform rho>=-8 estimate, small-increment inverse, prefix recurrence, and Lev central-interval theorem, all stated in the accompanying foundational excerpts.

Claim: for every positive real set X of r>=21 elements whose subset-sum support is not an arithmetic progression, rho(X)>=r-5. Equality is attained by {1,3,4,...,r+1}.

## Deleted intervals with at most three deletions
For j>=10, q<=3, let Y=[1,j+q] minus H, where |H|=q and j+q is present. If its subset-sum support is non-AP, claim rho(Y)>=j-5.

For q=0 the support is full. For q>=1 put h=j+q. Lev's central-interval theorem applies because h<=3j/2-2 for j>=10,q<=3. It gives the central interval [2q+1,sumY-(2q+1)]. Hence the number of subset-sum holes is twice the number of missing subset sums in [1,2q]; this is determined solely by H intersect[1,2q]. Density gives gcd(Y)=1, so non-AP support is equivalent to a positive hole count.

The existing deleted-interval defect localization puts every positive diagonal defect in [1,q] or [j,j+q]. Low defects are determined by the present positions0..2q; high defects are determined by present depths0..2q from h. Thus the defect count is determined by the two signatures H_low=H intersect[1,2q] and H_high={h-d:d inH,1<=h-d<=2q}.

For j>=14 these bands are disjoint. Let l=|H_low|,u=|H_high|,t=q-l-u. Every middle deletion has depth at least2q+1; their distinct depths have total at least(2q+1)+...+(2q+t). The hole count is positive only if l>=1.

Match these two signatures at j0=14, use the same high depths and low positions, and choose middle depths2q+1,...,2q+t. They all fit the middle band at j0: for q<=3 it has at leastq available depths. This is a valid deleted interval Y0 of14 elements with the same positive hole count and same defect count. Writing each deletion by its depth gives exactly
mu(Y)=sum_{d inH}(h-d)-T_{q-1}-holes(Y).
Therefore
rho(Y)-j >= rho(Y0)-14 + (l-1)(j-14) >=rho(Y0)-14.

The finite checker verifies all deletion sets at j=10,11,12,13,14 and q=1,2,3, with maximum retained, and obtains rho-j>=-5 whenever holes>0. This proves the deleted-interval claim for every j>=10; the finite computation is not a sample of larger j because the preceding signature/depth reduction covers every larger size.

## General positive real sets
Order X and use prefixes X_i and integer increments y_i from the report. The exact recurrence implies rho_i>=rho_{i-1}+y_i-2. The global defect estimate gives rho_i>=-8 for every i.

If every y_i>=4 for10<=i<=r, then rho_r>=-8+2(r-9)=2r-26>=r-5 because r>=21.

Otherwise take the last j>=10 with y_j<=3. The old small-increment inverse applies since3<=j-5; up to positive scaling X_j is a deleted interval with at most3 deletions and maximum retained. All later increments are at least4.

If FS(X_j) is non-AP, the deleted-interval claim gives rho_j>=j-5; the recurrence then gives rho_r>=j-5+2(r-j)>=r-5.

If FS(X_j) is AP but FS(X_r) is not, let k>j be the first non-AP support. FS(X_{k-1}) is a progression starting at0. If it intersects its translate by x_k, the translation is an integral number of progression steps and their union is again a progression. Thus non-AP at k forces the two translates to be disjoint. Hence y_k=|FS(X_{k-1})|-k>=1+T_{k-1}-k, so
rho_k>=-8+y_k-2>=T_{k-1}-k-9>=k-5
for k>=11. All subsequent increments are at least4, yielding rho_r>=r-5 again.

This proves the claim, conditional only on the independently checkable finite certificate and the general lemmas supplied with this package.
