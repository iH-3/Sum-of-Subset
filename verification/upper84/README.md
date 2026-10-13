# Upper bound 84: proof supplement and finite verification

This package continues the supplied upper-85 report on finite real sets
`A` satisfying `FS(A) subseteq 4A`, with repeated summands allowed in `4A`.
The new written proof excludes cardinality 85 and gives `71 <= N <= 84`,
using the original report's declared mathematical inputs and preceding bound.

Read `proof/report.pdf` for the full English supplement. Its editable LaTeX
source is `proof/report.tex`. The fresh proof components and exact arithmetic
programs are under `progress85/`. The supplied verification program and its
mathematical sources are retained under `audit/verification_program/`.

## Run the checks

Use Python 3.10 or later. No third-party Python packages are required.
Extract the whole ZIP before running the driver.

```sh
python3 verify84.py --full
```

On Windows:

```bat
py -3 verify84.py --full
```

Without `--full`, the driver runs the new finite components only. With
`--full`, it also runs the inherited full verification suite. Each child
interpreter ignores Python environment overrides, disables site packages, and
runs with assertions enabled, including when the driver itself is launched
with `-O`.
The driver checks the complete 17-module inventory and its seven aggregate
children, checks that every written family Z0-Z5, P0-P5 and H is present,
and checks the byte identity of the reviewed proof and program inputs.

`COVERAGE85.json` identifies each written case proof and the scope of each
finite check. Detailed logs and a machine-readable summary are written to
`verification_results/`.

## What a successful run means

The programs check the listed finite arithmetic, offset inventories, dense
seed lemma, paired profile minima, native-label incidence and scalar
certificates. They do not formalize the infinite inverse theorems or prove
that a prose activity/forest argument has been correctly derived from an
actual feasible set. Those arguments are supplied in the written supplement
and retain the input boundary of the original report.

The inherited upper-86 theorem remains an original mathematical input, as
in the supplied upper-85 report. Its complete proof or an identifying citation
is absent from the supplied attachments, so the improved global upper bound
retains that dependency. The lower construction is unchanged.

The archived exploratory searches and provisional scalar witnesses are not
used by the final verifier. No numerical optimizer is needed to replay the
new proof's specified finite components.
