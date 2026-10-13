"""Exact arithmetic for FS(A) subseteq 4A; Python standard library only."""
from fractions import Fraction
from itertools import combinations_with_replacement


class VerificationError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def scalar(value):
    require(isinstance(value, (int, str, Fraction)) and not isinstance(value, bool),
            "Use integers or rational strings, never floats.")
    return Fraction(value)


def normalize(values):
    a = tuple(sorted(scalar(v) for v in values))
    require(len(set(a)) == len(a), "A must have distinct elements.")
    return a


def subset_sums(a, max_states=1000000):
    support = {0}
    for x in a:
        support |= {s + x for s in support}
        if max_states is not None and len(support) > max_states:
            raise RuntimeError("Subset-support limit exceeded; result is inconclusive.")
    return support


def four_sum_witnesses(a):
    """The 2+2 construction covers all four-term multisets, including repetition."""
    pairs = {}
    for x, y in combinations_with_replacement(a, 2):
        pairs.setdefault(x + y, (x, y))
    out = {}
    for s, t in combinations_with_replacement(sorted(pairs), 2):
        out.setdefault(s + t, pairs[s] + pairs[t])
    return out


def analyze(a, max_states=1000000):
    a = normalize(a)
    support = subset_sums(a, max_states)
    witnesses = four_sum_witnesses(a)
    missing = sorted(support - witnesses.keys())
    return {"n": len(a), "subset_sum_count": len(support),
            "four_sum_count": len(witnesses), "feasible": not missing,
            "missing_count": len(missing),
            "first_missing": str(missing[0]) if missing else None}


def family(m):
    require(isinstance(m, int) and m >= 1, "m must be a positive integer.")
    return tuple(sorted(set(range(-m, m + 1)) |
                        {s * k * m for s in (-1, 1) for k in (3, 5, 7, 23)}))


def check_certificate(data):
    """Independent witness checking: it never constructs 4A itself."""
    require(data.get("schema") == "four-sum-certificate-v1", "Unknown schema.")
    a = normalize(data["A"])
    aset = set(a)
    target = subset_sums(a)
    rows = data["representations"]
    keys = set()
    for row in rows:
        t = scalar(row["sum"])
        q = [scalar(v) for v in row["terms"]]
        require(t not in keys, "Duplicate target in certificate.")
        require(len(q) == 4 and all(v in aset for v in q), "Invalid four summands.")
        require(sum(q) == t, "False sum identity.")
        keys.add(t)
    require(keys == target, "Certificate must cover exactly the subset-sum support.")
    return {"n": len(a), "identities_checked": len(keys), "status": "PASS"}
