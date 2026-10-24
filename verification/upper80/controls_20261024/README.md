# Controls for the new research lemmas

These programs use only the Python standard library. Run them directly with
`python` or `python -O`. They exercise the source-gap, overlap, fixed-label,
and explicit target-cover implementations against independently constructed
sets. They are regression controls for the written universal arguments in
`../research_checkpoint.md`, not an exhaustive proof of the global bound.

`ap_small.py` is different: it exhaustively checks the complete finite range
needed to prove nonnegative AP defect at ranks 2–14, with an independent
partition count. `check_hitting.py` independently enumerates all subsets of
each tested small hypergraph. The probe boundary check compares the formulas directly against integer
interval membership in 10,000 generated cases.

The global status remains **71 <= N <= 81** until all original finite roots
and the complete structural reduction have been certified.
