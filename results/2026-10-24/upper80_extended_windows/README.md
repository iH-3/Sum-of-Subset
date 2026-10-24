# Incremental research verification

The new k=0, k=1 and unrestricted (5,270,0) records each passed exact replay
before packaging. `closure_receipt.json` checks that their order-preserving
record identities match those replays. It reuses the immutable, previously
verified k=2..7 packet and its receipt. It does not rerun the old baseline or
old closed searches. The resulting two new original-root closures leave
seven original roots open, and do not establish structural applicability.

`verify_extended_windows.py` can independently replay the three new records.
`--replay-prior-ranks` additionally opts into repeating the old rank replay;
that option was deliberately not used in this continuation.

The other files are new focused implementation controls and explicitly
partial partition receipts. They do not imply further original-root closure.
The first-gap core classification has four alternatives and currently one
closed alternative. Partial adjacent-target enumerations retain their open
leaves in their counts.
