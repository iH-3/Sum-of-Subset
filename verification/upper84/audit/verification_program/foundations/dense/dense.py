"""All dense boundary bases, with independent set-valued DP."""
from itertools import combinations
from math import comb
import hashlib
from .common import need, rejects, subset_bits

BETA9_DIGEST = 'b335335df22c3319d85dbec34cbde2e0f334fdd41277dcb090ff8ddbfd3e64f8'

def set_sums(values):
    reached = {0}
    for value in reversed(values):
        reached.update({total + value for total in reached})
    return reached

def check(values, beta, independent=True):
    r = len(values)
    need(tuple(sorted(set(values))) == values and values[0] > 0, 'dense set')
    need(0 <= beta <= 9 and r >= beta + 3 and values[-1] == r + beta,
         'dense hypotheses')
    total = sum(values)
    lo, hi = 2 * beta + 1, total - 2 * beta - 1
    need(lo <= hi, 'nonempty central interval')
    bits = subset_bits(values)
    mask = ((1 << (hi - lo + 1)) - 1) << lo
    need(bits & mask == mask, 'central interval')
    lower = [s for s in range(1, lo) if not bits >> s & 1]
    holes = total + 1 - bits.bit_count()
    need(len(lower) <= beta and holes == 2 * len(lower), 'endpoint holes')
    if independent:
        reached = set_sums(values)
        need(len(reached) == bits.bit_count(), 'DP cardinality disagreement')
        need(all(s in reached for s in range(lo, hi + 1)), 'independent central interval')
        actual_holes = set(range(total + 1)) - reached
        need(actual_holes == set(lower) | {total - s for s in lower},
             'independent exact holes')
    return total, lower, holes

def verify():
    # Exhaustive powerset tests anchor both distinct DP implementations.
    for mask in range(256):
        values = tuple(i + 1 for i in range(8) if mask >> i & 1)
        direct = {sum(values[i] for i in range(len(values)) if m >> i & 1)
                  for m in range(1 << len(values))}
        need(set_sums(values) == direct, 'set DP powerset test')
        bits = subset_bits(values)
        need({i for i in range(sum(values) + 1) if bits >> i & 1} == direct,
             'bitset DP powerset test')
    rows = []
    beta9 = hashlib.sha256()
    import json
    for beta in range(10):
        r, maximum = beta + 3, 2 * beta + 3
        count = 0
        # Omissions give a complete one-to-one parametrization retaining maximum.
        for omitted in combinations(range(1, maximum), beta):
            deleted = set(omitted)
            values = tuple(i for i in range(1, maximum + 1) if i not in deleted)
            total, lower, holes = check(values, beta)
            if beta == 9:
                beta9.update((json.dumps([omitted, total, lower, holes],
                                         separators=(',', ':')) + '\n').encode('ascii'))
            count += 1
        need(count == comb(maximum - 1, beta), 'dense boundary coverage')
        rows.append(dict(beta=beta, r=r, maximum=maximum, count=count))
    need(sum(row['count'] for row in rows) == 227239, 'total dense boundary cases')
    need(beta9.hexdigest() == BETA9_DIGEST, 'audited beta9 digest')
    small = []
    for r in range(3, 9):
        count = 0
        for beta in range(r - 2):
            maximum = r + beta
            for omitted in combinations(range(1, maximum), beta):
                deleted = set(omitted)
                check(tuple(i for i in range(1, maximum + 1) if i not in deleted), beta)
                count += 1
        small.append(dict(r=r, count=count))
    need(sum(row['count'] for row in small) == 1728, 'small-r total')
    controls = [rejects(lambda: check((1, 4, 5, 6), 2), 'insufficient density')]
    need(8 not in set_sums((1, 4, 5, 6)), 'negative witness hole at 8')
    controls.append(rejects(lambda: check((1, 2, 3, 5), 0), 'wrong deficit'))
    # These arithmetic checks accompany, rather than replace, the induction proof.
    need(all(r * (r - 1) // 2 >= r + 46 for r in range(13, 200)),
         'beta9 overlap induction arithmetic')
    return dict(status='PASS', boundary_rows=rows, boundary_total=227239,
                small_rows=small, small_total=1728, independent_algorithm='set-valued DP',
                powerset_self_tests=256, beta9_record_sha256=beta9.hexdigest(),
                rejected_controls=controls)
