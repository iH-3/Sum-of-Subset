#!/usr/bin/env python3
"""Exhaustively verify the finite P3 seed lemma, with exact integer bitsets."""
from itertools import combinations

def verify():
    count = 0
    for B in combinations(range(1, 18), 12):
        support = 1
        for x in B:
            support |= support << x
        total = sum(B)
        for x in range(11, total - 10):
            assert (support >> x) & 1, (B, x)
        low_holes = sum(not ((support >> x) & 1)
                        for x in range(1, (total + 1) // 2))
        assert low_holes <= 5, (B, low_holes)
        count += 1
    assert count == 6188
    print(f"PASS: all {count} twelve-element subsets of [1,17].")

if __name__ == "__main__":
    verify()
