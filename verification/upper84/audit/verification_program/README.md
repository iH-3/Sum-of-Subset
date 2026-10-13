# Exact verification for the consolidated upper-85 proof

This is an offline, standard-library Python verification program accompanying the English proof of the bound **71 <= N <= 85** for finite real sets with FS(A) contained in 4A. Empty subsets are allowed in FS(A); repetition is allowed in 4A.

## What a successful run means

**Exit code 0 means all executable checks requested in that mode passed. It does not mean the entire theorem has been formally verified.** The analytical cover, structural reductions, infinite reductions, endpoint geometry, activity classifications, and cited general theorems remain written mathematical inputs. The program states these boundaries in every result JSON.

The program does real finite mathematics: exact subset sums and pair sums, polynomial expansion and integer minimization, nonnegative rational certificate recombination, complete bounded foundation families, and certificate inference checks. It does not infer mathematical truth from hashes, receipt status, or the presence of a row in a ledger.

## Requirements and Windows instructions

- Python **3.10 or later**, with its standard library only
- No package installation, network access, solver, account, or original research directory
- Extract the ZIP to a writable folder before running it; do not run inside the ZIP viewer

On Windows, double-click `run_windows.bat` for the full verification. It looks for the Python launcher `py -3`, then for `python`. It keeps the window open and preserves the verifier's exit code. `verify_quick.bat` runs the faster mode; `verify_full.bat` is an explicit full-mode shortcut.

Alternatively, open a terminal in this folder and run:

```
py -3 verify.py --full
py -3 verify.py --quick
```

On Linux or macOS:

```
python3 verify.py --full
python3 verify.py --quick
```

Without a mode flag the program uses `--quick`. Full mode is recommended when checking the proof's finite inputs. Python's `-O` flag is supported: explicit mathematical predicates remain active, including the retained structural assertions, which are compiled with optimization disabled.

Paths containing spaces and non-ASCII characters are supported. The Windows launchers are statically checked portable batch files; this delivery was tested on Linux, not on an actual Windows installation. See `TEST_REPORT.json` for the exact completed platform and isolation tests.

## Output and exit codes

Every check prints `PASS`, `FAIL`, or `SKIP`. The program writes these files next to `verify.py`, regardless of the terminal's working directory:

- `verification_log.txt`: concise readable results
- `coverage.json`: detailed counts, exact margins, witnesses, dependencies, and verification limits

An existing pair of logs is replaced on each run. To preserve results from several runs, use `--output-dir "my results"` with a different folder for each run. `sample_results/` contains actual delivery-run logs; these are examples, never inputs to the checker.

Exit code 0 means all requested executable checks passed. Exit code 1 means a mathematical, input, dependency, or output failure. Invalid command-line syntax uses Python argparse's exit code 2. Full mode treats a missing required family or a skipped required executable check as a failure. Human mathematical inputs are listed separately; they are never disguised as passed tests.

## Scope and approximate runtime

On the delivery Linux computer, quick mode takes about **9 seconds**, and full mode about **30 seconds**. Hardware and Python version affect runtime; a slower computer may take several minutes. Both modes perform the following:

1. Construct all 3,349 subset sums of the explicit 71-element set, and all 3,495 fourfold sums by a separate set convolution. Check containment and all 12 printed interval rows
2. Reconstruct all 110 fixed-label formulas and verify the 26 disjoint negative-sum groups, proving the fixed allowance 84 under the human covering premise. Check the exact original 18-whole-unit inventory on both branches and 4,096 rooted-forest pointwise membership cases, plus the narrowly licensed single-missing-leaf count
3. Check the 13-row partition over 50,562 admissible scalar tuples in a finite superset of the structural domain, including both physical size orientations and all boundaries. This is a scalar check, not a source-configuration census
4. Expand the listed exact algebraic identities, independently check stored polynomial coefficients and factorizations, and compute global integer quadratic minima by exact rational vertices and integer neighbors
5. Check positive final arithmetic margins from all 13 strata. These are conditional on the analytical inequalities and classifications in the report. They do not constitute a formalization of every intermediate argument or every historical transported leaf
6. Check the shared P1/H1 first-gap scalar identity and 1,400 scalar baseline cases, together with its cubic monotonicity bound. The seven original P4 propagation seeds are also checked by independent exact support calculations, nine-entry minima, and both failure-mass bounds
7. Recombine an actual final P4/A0 rational contradiction certificate, obtaining zero variable coefficients and right side -7/2
8. Run mathematical negative controls: changed coefficients, an omitted partition row, an omitted arithmetic case, a corrupted certificate multiplier, and a zero contradiction margin must fail. Additional fixed-cover controls reject a wrong coefficient and a reused resource label
9. Recompute the generic non-AP finite base, structural bootstrap/inverse arithmetic, fixed structural integer witnesses, and the four needed H-profile thresholds with their own negative controls

The detailed P3 and Z5 appendix checks are also integrated into both modes:

- P3: nine baseline identities, all 35 A1 arithmetic steps (including the complete m=3 chain), its eight terminal comparisons and exact integer minimum 748, both m=4 seed supports, and all 2,380 thirteen-element subsets of {1,...,17} for the precise interval [9,sum(seed)-9]. This last finite check is not a proof of Lev's general theorem
- Z5: 11 literal endpoint cards, retention of their endpoints in all 13 listed pair1-retained templates, 11 fixed-label credit ledgers linked to the independently checked 26-group cover certificate, six quadratic minima, three nonnegative linear eliminations, and 14 affine reductions with their coefficient directions checked
- The corrected C5 zero-loss constant is independently reconstructed as 999 and linked to the resulting constant 7. A mutation replacing them with the obsolete 1039/47 pair is explicitly rejected, even though that altered affine identity would be internally consistent on its own
- Seven additional mathematical mutations test the P3/Z5 ports. The analytical selection, ownership, clipping and exhaustive-classification arguments remain human proofs

Full mode additionally recomputes both large finite foundation families:

- The bounded-density boundary and small-cardinality bases: 227,239 and 1,728 cases respectively, with overlap explicitly documented
- The restricted direct-defect bases: 43,758 and 48,620 deletion patterns, and 91,875 complete sets

Quick mode explicitly marks these last two families `SKIP`. It is not a full finite-foundation replay. See `foundations/README.md` for exact domains, multiplicities, independent algorithms, the 160 H-profile claims, and the retained finite-to-infinite proof boundary.

## Files to inspect

- `verify.py`: CLI, logs, result semantics, and human-input boundary
- `exact_math.py`: small exact polynomial and rational-certificate kernel
- `checks.py`: construction, partition, resource-counting, first-gap, and mutation checks
- `data/arithmetic.json`: readable formulas, domains, factorizations, expected margins, and the rational certificate
- `chapter_checks.py`, `chapter_expected.py`, and `data/p3_appendix.json` / `data/z5_appendix.json`: integrated standard-library appendix checks and required row inventories
- `data/p4_seeds.json`: seven exact propagation seed cases
- `proof/report.tex`: the standalone source of the accompanying consolidated English proof
- `proof/SOURCE_GUIDE.md`: where each proof and verification dependency is documented
- `expected_cases.py`: mandatory arithmetic case inventory; removing a case is a failure
- `COVERAGE_MAP.json`: report lemma/stratum to checker/dependency map
- `SOURCE_MAP.json`: stable source identifiers and hashes for the arithmetic transcription
- `data/chapter_provenance.json`: appendix source identities and documented portable adaptations
- `foundations/`: self-contained finite-foundation code, data, written dependencies and coverage map

`--data PATH` permits checking an alternate arithmetic JSON with the same schema; the default is the bundled file. Required check IDs remain fixed in the program. This option is useful for independent negative tests. No integrity hash is used to short-circuit the mathematical checks.

## Deliberately excluded work

This program does not run a historical multi-million descriptor census, launch an LP/Farkas search, discover new profiles, search for a larger construction, or explore upper bounds below 85. The finite loops only verify the stated bounded families and supplied proof data. No assertion that a geometric resource is retained, that a classifier is exhaustive, or that a cited theorem is applicable is inferred merely from numerical success.
