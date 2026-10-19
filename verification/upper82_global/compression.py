"""Exact checks for the residue-compression overlap lemma.

This module proves no global cardinality bound by itself. The unbounded
argument is in proof.md; the finite checks test its implementation.
Python 3.10+, standard library only; no assertions are used.
"""
from itertools import combinations, product


def need(condition, message):
    if not condition:
        raise ValueError(message)


def triangle(n):
    return n * (n + 1) // 2


def defect(points):
    points = set(points)
    need(0 in points, 'zero belongs to the set')
    p = sum(x > 0 for x in points)
    q = sum(x < 0 for x in points)
    return sum(abs(x) for x in points) - triangle(p) - triangle(q)


def overlap(points, shift):
    return len(points & {x + shift for x in points})


def compress(points, shift):
    """Produce and check the literal inward moves used in the proof."""
    points = set(points)
    need(type(shift) is int and shift > 0, 'positive integer shift')
    initial = set(points)
    mass = defect(points)
    p = sum(x > 0 for x in points)
    q = sum(x < 0 for x in points)
    steps = 0
    while True:
        candidates = [(x, x - shift) for x in sorted(points)
                      if x > shift and x - shift not in points]
        candidates += [(x, x + shift) for x in sorted(points)
                       if x < -shift and x + shift not in points]
        if not candidates:
            break
        old, new = candidates[0]
        before = overlap(points, shift)
        before_mass = sum(abs(x) for x in points)
        points.remove(old)
        points.add(new)
        need(sum(abs(x) for x in points) == before_mass - shift,
             'one move costs exactly one shift of mass')
        need(overlap(points, shift) <= before + 1,
             'an adjacent move gains at most one edge')
        need(sum(x > 0 for x in points) == p
             and sum(x < 0 for x in points) == q,
             'both sign counts are preserved')
        steps += 1
    classes = {}
    for x in points:
        classes.setdefault(x % shift, []).append(x)
    for values in classes.values():
        values.sort()
        need(all(b - a == shift for a, b in zip(values, values[1:])),
             'each occupied residue is one chain')
    need(overlap(points, shift) == len(points) - len(classes),
         'final edges equal vertices minus chains')
    need(steps * shift <= mass, 'baseline mass bounds the move count')
    need(overlap(initial, shift) >= len(initial) - shift - mass // shift,
         'mass-compression overlap bound')
    return steps


def verify():
    intersections = 0
    compressions = 0
    total_moves = 0
    for p, q in product(range(1, 6), repeat=2):
        positive = list(combinations(range(1, p + 5), p))
        negative = list(combinations(range(1, q + 5), q))
        for index, (pos, neg) in enumerate(product(positive, negative)):
            points = {0, *pos, *(-x for x in neg)}
            mass = defect(points)
            for shift in range(1, len(points) + 3):
                need(overlap(points, shift) >= len(points) - shift - mass // shift,
                     'actual finite intersection')
                intersections += 1
                if index % 101 == 0:
                    total_moves += compress(points, shift)
                    compressions += 1
    need(intersections == 716103, 'complete advertised finite range')
    # Equality also refutes the stronger false bound with no mass penalty.
    sharp = {-3, -1, 0, 1}
    need(defect(sharp) == 1 and overlap(sharp, 1) == 2,
         'sharp boundary example')
    need(overlap(sharp, 1) < len(sharp) - 1,
         'reject missing boundary penalty')
    # The affine branch is strict. Replacing >=1 with >=0 is unsound.
    need(1 * 1 - defect(sharp) == 0 and overlap(sharp, 1) < 4 - 1,
         'reject nonstrict compression license')
    return dict(status='PASS_LEMMA_CHECKS_ONLY',
                intersections=intersections,
                compression_replays=compressions,
                checked_inward_moves=total_moves,
                formula='|E intersection (E+x)| >= |E|-x-floor(tau/x)',
                global_upper_bound_certified=False)


if __name__ == '__main__':
    import json
    print(json.dumps(verify(), indent=2))
