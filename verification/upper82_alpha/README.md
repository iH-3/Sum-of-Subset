# Exact size83 alpha-hole exclusion (conditional)

This package excludes only the Branch-A whole-hole family
`{P, Bpair, O_s, O_t, alpha_s}` with a 75-point common integer source,
complete physical target intervals, and all thirteen remaining singleton
resources retained. Reflection is covered by relabelling the physical sides.
The global proved interval is **71 <= N <= 83**. Global upper82 is not proved.

## Proof changes

- All six gaps X_s, X_t, g_s, g_t, h_s, h_t occur twice in the two
  physical trees. Credit14 already implies every one is at least26.
- The initial tail argument uses only actual source hits. It does not
  assume core hits, light clips or normal centres. It gives credit27;
  light clips follow afterwards from epsilon <=68.
- Each detached forest component keeps one native loss at a designated
  root. The additional edge joins alpha_t and C5_t. It uses generic F
  even when the original twelve edges have the stronger full-core bound67.
- The source tail span satisfies L >= A+56 after credit27 and
  L >= A+57 after credit31. The latter excludes a central missing interval.
- The order tests B<a, C<b, D<a are independent finite refutations at
  successive credits27,31,35. No early normality assumption is used.
- Credit42 gives an analytic two-step bootstrap of all six base gaps to
  x>tau. Both orientations of the extra edge are then checked.

See `reports/upper82_alpha_20261019.tex` and `.pdf` for the universal
geometric implications and full scope. Integer certificates verify only
the finite linear contradictions; they are not a proof-assistant formalization.

## Reproduce (Python 3.10+, standard library)

From the repository root:

```text
python -I -S -B verification/upper82_alpha/check.py --output results/local/upper82_alpha.json
python -I -S -B -O verification/upper82_alpha/check.py --output results/local/upper82_alpha_O.json
```

Windows: run `verify_upper82_alpha_windows.bat`.
No SciPy, NumPy, network, optimizer or nonstandard package is needed to verify.

The verifier independently reconstructs 3,157 cases (765 +697 +635 +1060),
checks 376 integer rays, and reconstructs the60 selected genuine forests.
Every nonnegative inequality multiplier and summed variable coefficient is
checked with integers, and every summed right side is strictly negative.
It also checks exact order statistics, all81,920 pointwise forest states,
source/tail arithmetic, the495 formal four-term multisets and fixed ledgers.

`discover.py` is optional: it needs NumPy/SciPy to find certificates, but
all numerical weights are reconstructed and checked exactly before saving.
The selected forests are only necessary inequalities; no enumeration of
geometric configurations is being claimed. See `next_steps.md` for remaining
size83 work.
