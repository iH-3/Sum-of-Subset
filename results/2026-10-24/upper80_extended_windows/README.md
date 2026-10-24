# Incremental research verification

Latest: `gap_closure_receipt.json` certifies assembly of all 12 alternatives
of `(5,413,0)`. Only its new final alternative was freshly replayed; the
11 earlier closed records were matched to the immutable verified frontier.
`gap_packet_receipt.json` checks the unchanged assembled packet. Total:
4,651 original roots closed, three open; no global bound80 claim.

`strengthened_joint_receipt.json` verifies the newly strengthened credit51
tree for `(5,219,0)`: 1,771 nodes, 581 closed leaves, 1,071 open leaves.
The 421 previously closed leaves were preserved; only open nodes received
new discovery under 255 additional verified facts and improved credit.
`extreme_frontier_receipt.json` identifies the frozen 17-checkpoint snapshot.

The following paragraphs describe the earlier snapshots.

The new k=0, k=1 and unrestricted (5,256,0), (5,266,0), (5,268,0), (5,270,0) records each passed exact replay
before packaging. `closure_receipt.json` checks that their order-preserving
record identities match those replays. It reuses the immutable, previously
verified k=2..7 packet and its receipt. It does not rerun the old baseline or
old closed searches. The resulting five new original-root closures leave
four original roots open, and do not establish structural applicability.

`verify_extended_windows.py` can independently replay the six new records.
`--replay-prior-ranks` additionally opts into repeating the old rank replay;
that option was deliberately not used in this continuation.

The other files are new focused implementation controls and explicitly
partial partition receipts. They do not imply further original-root closure.
The first-gap core classification has new independently checked alternative
1 in addition to the previously closed alternative 3. The complete shape-capacity
partition now has an exact receipt closing cases 1,2,3 and retaining case0. In the 12-way
`(5,413,0)` partition, new alternatives 2 and 8 have exact receipts and only
alternative 3 remains open. Neither change yet closes an original root.
The completed joint trees retain all open leaves: 1,343 at depth3 for
`(5,219,0)` and 272 at depth4 for `(5,413,0)`. Those depths are not restarted.
