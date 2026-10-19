# Complete size-84 exclusion / upper bound 83

Start from the independently checked upper bound84 at commit
`cf26c50489e114029010d9ab83b24669aa3b257b`. The accompanying report proves
that a hypothetical84-element feasible set is impossible, giving71<=N<=83.

Run from the repository root:

```sh
python -I -S -B verification/upper83_complete/check.py --output .work/upper83.json
python -I -S -B -O verification/upper83_complete/check.py --output .work/upper83_O.json
```

Python3.10+, standard library only. The entry point checks pinned sources,
replays the full upper84 dependency suite, and recomputes every new finite
check. It does not treat archived PASS fields as proofs.
`PASS_COMPLETE_FINITE_REPLAY` is a finite verification result; the infinite
inverse, source, activity and actual-resource arguments are written proofs.
This is not a proof-assistant formalization.

| File | Mathematical role |
|---|---|
| structure.md | All AP/nonAP branches, inverse repairs, small boundaries, primitivity, high holes |
| localization_p12.md | Uniform low-hole localization and one-hole terminal |
| z2_p2.md | Empty-leading repair, prefix defect32, four beta/O exclusions, common two-hole terminal |
| positive.md | Dense seed, low-prefix census, fresh activity licenses and P3/P4/P5 terminals |
| z34_cards.md | Actual physical derivation of every Z3/Z4 scalar master |
| z4_ownerless.md | Credit18, two-trim bootstrap and one-trim ownerless contradiction |
| z5.md | Outer integrality, complete Z5 owner grammar and nine new transports |
| z5_alpha.md | Ordered credit14->27->31->35->38->42, then normality and884>882 |
| check_structure.py | Exact20 inverse repair rows, AP tails, universal profile replay and interval margins |
| check_geometry.py | Literal endpoint identities, compatible ledgers and full Boolean dispatch |
| check_positive.py | All6188 seeds,12 P3 patterns,7 P4 masters,11+4 P5 cards |
| check_local.py | Weighted inverse minima, alpha stages,59049 low prefixes and9 Z5 transports |

The exact Z5 A1 empty-P/C5t terminal is imported with its full hypotheses
from `reports/upper83_tail_20261019.tex`; its verifier is rerun. Universal
full-rank and coupled-source results are imported from the immediately
preceding reports. Their old conditional-status wording is historical and
is intentionally retained. The new report supplies the missing global
applicability and branch coverage.
