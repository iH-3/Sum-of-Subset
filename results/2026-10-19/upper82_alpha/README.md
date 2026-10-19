# Conditional size83 alpha-family result

Status: `PASS_CONDITIONAL_ALPHA_SIZE83_FINITE_CERTIFICATES`.
Global interval remains **71 <= N <=83**; global upper82 is not proved.

Both commands completed successfully in an isolated Python process:

```text
python -I -S -B verification/upper82_alpha/check.py --output results/2026-10-19/upper82_alpha/check.json
python -I -S -B -O verification/upper82_alpha/check.py --output results/2026-10-19/upper82_alpha/check_O.json
```

`comparison.json` records identical output hashes, source/certificate hashes,
and unchanged source pins for the existing global83 proof and C5t package.
No full rerun of those unchanged older proofs is claimed here.

The finite replay covers3,157 systems,376 integer certificates,60 selected
resource forests, and both extra-edge orientations in all530 terminal
rank/mass pairs. Minimum integer contradiction is1. Other checks include
81,920 pointwise forest states,35,622 order statistics,5,126 concave-envelope
segments,495 formal four-term multisets, six fixed-ledger stages and eight
negative controls. The universal mathematical implications are in the report.

The five-page XeLaTeX PDF was compiled and all rendered pages inspected.
The final build has no overflow or unresolved references.
