# Exploratory searches

These searches are heuristic. No unsuccessful run is used to exclude a cardinality.

`search.cpp` searches a consecutive integer core `[-l,r]` plus four negative and four positive tails. Its score is the number of integer-hull targets not covered by the exact union of four-sum intervals. A score of zero is a sufficient condition, but a positive score need not disprove feasibility for an arbitrary candidate with holes in its subset support. The saved best 72-point candidate was separately checked against its actual subset support with `verification/exact.py`.

```bash
g++ -O3 -std=c++17 experiments/search.cpp -o .work/search
.work/search 31 32 2000000
```

`family_search.cpp` searches five positive integral tail coefficients, with their negatives, around the continuous core `[-1,1]`. It maximizes the guaranteed continuous coverage radius minus the sum of positive coefficients. The reported `predicted_n` is a construction size suggested by that coverage calculation, not a global bound or an optimality claim. Any successful improvement must be separately instantiated and certified.

```bash
g++ -O3 -std=c++17 experiments/family_search.cpp -o .work/family_search
.work/family_search 5 500000
```

The seeds are fixed in the source. Numerical annealing probabilities affect search choices only; all interval endpoints and the final candidate check use exact integer arithmetic. These programs are not dependencies of any upper-bound proof.
