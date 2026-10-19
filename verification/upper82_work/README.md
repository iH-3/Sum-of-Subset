# Size83 C5t family: exact conditional exclusion

This package does **not** establish the global bound N <= 82.
The published global bound remains **71 <= N <= 83**.

The new local theorem excludes size83 configurations with a common integer
source of size75, complete physical targets, and exact Branch-A whole holes
`{Os,Hs,Ot,P,C5t}`. The proof supplies outer integrality, sole beta ownership,
fixed credit13, rank-dependent endpoints, and all finite systems' applicability.

The method uses the actual clip rank to bound its error by remaining rank mass.
An upper concave envelope keeps that error coupled to the clip cost. Five
actual gap types first bootstrap to strict long shifts, permitting the same
full core in all forest inequalities. Only19 fixed tail slots are needed.

Run from the repository root, with Python3.10+ and no third-party packages:

```sh
python -I -S -B verification/upper82_work/check.py --output .work/upper82_c5t.json
python -I -S -B -O verification/upper82_work/check.py --output .work/upper82_c5t_O.json
```

Windows users can run `verify_upper82_c5t_windows.bat`.

The verifier reconstructs all6706 systems and checks275 integer multiplier
certificates. Inequality multipliers must be nonnegative; equality multipliers
may have either sign. Every resulting variable coefficient must be nonnegative
and the right side strictly negative. The domain is generated independently of
the certificate file, including all permitted heavy clips and both orientations.

`discover.py` is an optional NumPy/SciPy search utility. It is never imported
by the standard-library verifier. It reconstructs and exactly checks each
numerical ray before saving it. The proof is in
`reports/upper82_c5t_20261019.tex`, with a rendered PDF alongside.

Unfinished global82 obligations include the new size83 structural reduction,
positive target holes, the new six-hole range, cross-HIGH exceptions in three/
four-hole strata, and the other five-hole families. Earlier size84 classifiers
and numerical budgets cannot simply be reused at size83.
