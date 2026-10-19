# Conditional size83 C5t verification

The new result excludes only the stated common-source, complete-target C5t
family. **Global N<=82 is not proved; the global interval remains71<=N<=83.**

`check.json` and `check_O.json` are byte-identical outputs from the isolated
standard-library verifier in ordinary and optimized Python modes.

| Check | Result |
| --- | ---: |
| Necessary systems | 6,706 |
| Cutoff stage | 2,463 |
| Strict-gap bootstrap stage | 1,780 |
| Full-core terminal stage | 2,463 |
| Integer multiplier certificates | 275 |
| Smallest integer contradiction | 1 |
| Actual source order-statistic checks | 35,622 |
| Strict endpoint-error improvements in those checks | 22,793 |
| Pointwise forest and rebate checks | 4,096 |
| Rank/mass parameter pairs | 1,007 |
| Deliberately invalid cases rejected | 7 |

Finite replay SHA256:
`3d7afa93b50d2da67200fb1e3c3a7b08c532feaa7e9ef904073eaaaba7bb9b3e`.

The prior complete83 proof's139 pinned source files remained unchanged.
Its full historical finite suite was not unnecessarily rerun: the new work
adds separate files and changes only README/status prose in the baseline.
The new source manifest pins24 inputs, including its proof and certificates.

The PDF was compiled twice with XeLaTeX, with no remaining overfull boxes
or unresolved references, and all five rendered pages were inspected.
`review.md` records the mathematical scope and resource-accounting review.
