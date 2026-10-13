"""Restricted high-hole family, using independent interval-union subset sums."""
from itertools import combinations
import hashlib
from .common import need, rejects, subset_bits, tri, record_bytes

EXPECTED_DIGEST = '1adc2997eb96abb9ea8fac6a3c07cbfbfeab211422f085e00dc34c4a78133f38'

def low_bitset_patterns(q):
    found = []
    count = 0
    for deleted in combinations(range(1, 19), q):
        D = set(deleted)
        bits = subset_bits([x for x in range(1, 19) if x not in D])
        count += 1
        if sum(not (bits >> s & 1) for s in range(1, 19)) >= 8:
            found.append(deleted)
    need(count == {8: 43758, 9: 48620}[q], 'complete low combination family')
    return found

def low_boolean_patterns():
    # Independent mask enumeration, descending Boolean DP, no bitset sums.
    result = {8: [], 9: []}
    counts = {8: 0, 9: 0}
    for mask in range(1 << 18):
        q = mask.bit_count()
        if q not in counts: continue
        counts[q] += 1
        dp = [False]*19; dp[0] = True
        deleted = []
        for value in range(1, 19):
            if mask >> (value-1) & 1:
                deleted.append(value)
            else:
                for total in range(18, value-1, -1):
                    dp[total] = dp[total] or dp[total-value]
        if sum(not dp[s] for s in range(1, 19)) >= 8:
            result[q].append(tuple(deleted))
    need(counts == {8: 43758, 9: 48620}, 'complete independent mask family')
    return {q: sorted(patterns) for q, patterns in result.items()}

def interval_sums(values):
    """Exact unions of closed integer intervals; distinct from a bitset or set DP."""
    intervals = [(0, 0)]
    for value in values:
        candidates = sorted(intervals + [(a+value, b+value) for a, b in intervals])
        merged = []
        for lo, hi in candidates:
            if merged and lo <= merged[-1][1] + 1:
                a, b = merged[-1]
                merged[-1] = (a, max(b, hi))
            else:
                merged.append((lo, hi))
        intervals = merged
    return intervals

def direct_record(j, q, deleted):
    D = set(deleted)
    values = [x for x in range(1, j+q+1) if x not in D]
    need(len(values) == j and values[-1] == j+q and len(D) == q, 'finite family domain')
    bits = subset_bits(values)
    count = bits.bit_count()
    holes = sum(values)+1-count
    V = set(values)|{0}
    defects = sum(not any(2*x-a in V and a != x for a in V) for x in values)
    mu = count-1-tri(j)
    rho = mu+2-2*defects
    return dict(j=j, q=q, D=list(deleted), h=holes, mu=mu, delta0=defects, rho=rho), values

def independent_record(j, q, deleted, values):
    intervals = interval_sums(values)
    count = sum(hi-lo+1 for lo, hi in intervals)
    V = [0]+values
    pairs = {a+b for i, a in enumerate(V) for b in V[i+1:]}
    defects = sum(2*x not in pairs for x in values)
    mu = count-1-tri(j)
    return dict(j=j, q=q, D=list(deleted), h=sum(values)+1-count,
                mu=mu, delta0=defects, rho=mu+2-2*defects)

def check_record(record):
    need(record['h'] >= 15, 'restricted high-hole filter')
    need(record['rho'] >= 8*record['j']-44, 'finite high-hole inequality')

def verify():
    # Exhaustive powerset self-tests for the independent interval representation.
    for mask in range(256):
        values = tuple(i+1 for i in range(8) if mask >> i & 1)
        direct = {sum(values[i] for i in range(len(values)) if m >> i & 1)
                  for m in range(1 << len(values))}
        intervals = interval_sums(values)
        need({s for a, b in intervals for s in range(a, b+1)} == direct,
             'interval DP powerset test')
    producer = {q: low_bitset_patterns(q) for q in (8, 9)}
    independent = low_boolean_patterns()
    need(producer == independent, 'independent full low-pattern family')
    need([len(producer[q]) for q in (8, 9)] == [151, 1108], 'accepted low patterns')
    digest = hashlib.sha256(); independent_digest = hashlib.sha256()
    rows = []; total = 0
    for j in range(14, 39):
        count = 0; minimum = 10**9; maximum_holes = 0
        for q in (8, 9):
            patterns = producer[8] if q == 8 else producer[9] + [
                d+(e,) for d in producer[8] for e in range(19, j+9)]
            need(len(patterns) == len(set(patterns)), 'no repeated finite records')
            for deleted in patterns:
                record, values = direct_record(j, q, deleted)
                other = independent_record(j, q, deleted, values)
                need(record == other, 'independent full-record disagreement')
                check_record(record); check_record(other)
                digest.update(record_bytes(record)); independent_digest.update(record_bytes(other))
                minimum = min(minimum, record['rho']-(8*j-44))
                maximum_holes = max(maximum_holes, record['h'])
                count += 1
        need(count == 151*j-251 and minimum == 0, 'exact finite row summary')
        rows.append(dict(j=j, count=count, minimum_margin=minimum, maximum_holes=maximum_holes))
        total += count
    need(total == 91875, 'total restricted cases')
    need(digest.hexdigest() == independent_digest.hexdigest() == EXPECTED_DIGEST,
         'audited complete high-hole record digest')
    scales = [tri(j-1)-(8*j-95) for j in range(14, 39)]
    bridges = [tri(m)-m-8*j+40 for j in range(14, 39) for m in range(j, 38)]
    need(min(scales) == 74 and min(bridges) == 19, 'universal reduction scale and bridge margins')
    negative = {'j': 14, 'h': 15, 'rho': 8*14-45}
    rejected = [rejects(lambda: check_record(negative), 'rho one below finite bound')]
    negative2 = {'j': 14, 'h': 14, 'rho': 8*14-44}
    rejected.append(rejects(lambda: check_record(negative2), 'below high-hole filter'))
    return dict(status='PASS_RESTRICTED_FINITE_LEMMA', count=total, rows=rows,
                low_pattern_counts={str(q): len(producer[q]) for q in (8, 9)},
                record_sha256=digest.hexdigest(), independent_record_sha256=independent_digest.hexdigest(),
                independent_algorithms=['18-bit mask enumeration and Boolean DP for low patterns',
                                        'interval-union DP for full subset sums',
                                        'unordered distinct-pair sums for diagonal defects'],
                powerset_self_tests=256, scale_minimum_margin=74, bridge_minimum_margin=19,
                rejected_controls=rejected,
                completeness_dependency='bounded-beta9 endpoint-hole theorem')
