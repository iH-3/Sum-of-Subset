"""Finite mathematical foundations for the accepted upper-85 proof route.

Public API: run_checks(mode='quick'|'full') -> records.  The full run checks
all finite bases.  The quick run explicitly skips the two largest finite bases.
Only Python's standard library is used.  No external source directory is read.
"""
from contextlib import redirect_stdout
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
import copy
import io
import json
import time
import types

ROOT = Path(__file__).resolve().parent
H_THRESHOLDS = (15, 17, 21, 49)
PROFILE_KEYS = [(h, r) for h in H_THRESHOLDS for r in range(15, 55)]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def tri(r):
    return r * (r + 1) // 2


def source_module(relative):
    """Load retained auditable source with assertions enabled even under -O.

    These three historical checkers use assertions.  An explicit optimize=0
    compilation is necessary: otherwise python -O would silently remove their
    mathematical predicates.  Dense checkers and this wrapper use exceptions.
    """
    path = ROOT / 'source' / 'structural' / relative
    namespace = types.ModuleType('retained_' + path.stem)
    namespace.__file__ = str(path)
    namespace.__dict__['__name__'] = 'retained_' + path.stem
    exec(compile(path.read_text(encoding='utf-8'), str(path), 'exec', optimize=0), namespace.__dict__)
    return namespace


def generic_nonap_base():
    original = source_module('foundations/verify_small_deleted.py')
    rows = []
    total = nonfull = 0
    for r in range(10, 15):
        count = qualified = 0
        margins = []
        by_q = []
        for q in range(1, 4):
            qcount = 0
            for deleted in combinations(range(1, r + q), q):
                holes, rho, mu, defects = original.stats(r, q, deleted)
                values = [x for x in range(1, r + q + 1) if x not in deleted]
                # Independent set-valued subset sums and unordered distinct pairs.
                reached = {0}
                for value in reversed(values):
                    reached |= {s + value for s in reached}
                V = [0] + values
                pairs = {a + b for i, a in enumerate(V) for b in V[i + 1:]}
                d2 = sum(2*x not in pairs for x in values)
                mu2 = len(reached) - 1 - tri(r)
                need((holes, mu, defects, rho) ==
                     (sum(values)+1-len(reached), mu2, d2, mu2+2-2*d2),
                     'independent non-AP base algorithms disagree')
                if holes > 0:
                    need(rho >= r - 5, 'generic non-AP finite base fails')
                    qualified += 1
                    margins.append(rho - (r - 5))
                count += 1
                qcount += 1
            need(qcount == comb(r + q - 1, q), 'deleted-interval q coverage')
            by_q.append({'q': q, 'count': qcount})
        rows.append({'r': r, 'count': count, 'nonfull': qualified,
                     'minimum_margin': min(margins), 'by_q': by_q})
        total += count
        nonfull += qualified
    return {'enumerated': total, 'nonfull': nonfull, 'rows': rows,
            'domain': 'r=10..14; q=1..3; every q-deletion below retained maximum r+q',
            'algorithms': ['original bitset support', 'independent set DP',
                           'distinct unordered pair sums including zero'],
            'mathematical_scope': 'Finite base only; see nonap_defect.md for finite-to-infinite reduction'}


def structural_bootstrap():
    original = source_module('check_bootstrap_ap86.py')
    result = original.verify()
    need(result['status'] == 'PASS', 'bootstrap source did not finish')
    try:
        original.effective(0, 1, 0)
    except AssertionError:
        pass
    else:
        raise ValueError('retained assertions were disabled')
    return {'parameters': result['parameters'], 'small_boundaries': result['boundaries'],
            'k_domain': [0, 20], 'k_values_tested': 21,
            'applicable_AP_rows': len(result['ap_rows']), 'AP_rows': result['ap_rows'],
            'remaining_halfstep_rows': result['halfstep_remaining'],
            'negative_control': 'Impossible effective-hole witness rejected, including under python -O',
            'mathematical_scope': 'Exact scalar predicates supporting written STRUCTURAL86 bootstrap/AP arguments'}


def structural_inverse():
    original = source_module('inverse86/check_inverse86.py')
    text = io.StringIO()
    with redirect_stdout(text):
        original.verify()
    # Counts are derived from the source domains, not from stored receipts.
    return {'inverse_rows': len(original.DENSE),
            'endpoint_repairs': len(original.ENDPOINT),
            'dense_diameter_rows': len(range(8, 21)),
            'oriented_overlap_alternatives': 2*len(range(15)),
            'primitivity_equality_rows': [11, 12],
            'recomputed_arithmetic_log': text.getvalue(),
            'mathematical_scope': 'Exact inequalities only; lattice, inverse and actual-set applicability are written premises'}


def structural_fixed_witnesses():
    original = source_module('ap_exception86/check86_elementary.py')
    vectors = json.loads((ROOT/'source/structural/inputs/four_integer_vectors.json').read_text())
    need([v['mode'] for v in vectors] == [[s, [], q] for s in ('A', 'B') for q in (0, 1)],
         'four exact branch modes')
    allowed = {}
    results = []
    for family, z in [('nonprimitive', 0), ('halfstep', 12)]:
        allowed[family] = []
        for k in range(20):
            a, b = 34-k, 35+k
            E = 587-k*(k+1)-146-tri(a)
            if family == 'halfstep':
                E += 3*z-(b-5)
            if E < 0:
                continue
            need(E < 78, 'all units active requires c<78')
            allowed[family].append({'k': k, 'a': a, 'b': b, 'delta_cap': E})
            for oriented_a in (a, b):
                for vector in vectors:
                    record = original.combine(oriented_a, vector, family, z)
                    # Recheck the actual coefficients rather than the stored pass field.
                    need(all(type(c) is int and c >= 0 for c in record['coeff'].values())
                         and record['rhs'] < 0, 'fixed weighted row contradiction')
                    if family == 'halfstep':
                        zero = original.combine(oriented_a, vector, family, 0)
                        weights = dict(vector['weights'])
                        slope = 4*weights.get('cardinality mass', 0) + 3*weights.get('AP exceptional delta cap', 0)
                        need(slope >= 0 and zero['coeff'] == record['coeff'] and
                             record['rhs']-zero['rhs'] == 12*slope,
                             'halfstep RHS monotonicity in z')
                    record.pop('pass', None)
                    results.append(record)
    for oriented_a in (14, 55):
        for vector in vectors:
            record = original.combine(oriented_a, vector, 'boundary14', 0)
            need(all(type(c) is int and c >= 0 for c in record['coeff'].values())
                 and record['rhs'] < 0, 'boundary14 fixed weighted contradiction')
            record.pop('pass', None)
            results.append(record)
    families = []
    for family in ('nonprimitive', 'halfstep', 'boundary14'):
        records = [r for r in results if r['family'] == family]
        families.append({'family': family, 'systems': len(records),
                         'minimum_contradiction': min(-r['rhs'] for r in records)})
    return {'systems': len(results), 'families': families, 'eligible_rows': allowed,
            'coefficient_records': results,
            'halfstep_reduction': 'Only z=12 relaxation used; exact nonnegative affine RHS slopes checked',
            'omitted_redundant_checks': '256 exact-even-z halfstep cases and unstrengthened diagnostics',
            'mathematical_scope': 'Three written actual-set families only; this is no solver or endpoint search'}


def check_profile_data(claims, records):
    from .dense import profiles
    need([(x['h'], x['r']) for x in claims] == PROFILE_KEYS, 'complete 160 claim domain')
    need([(x['h'], x['r']) for x in records] == PROFILE_KEYS, 'complete 160 profile domain')
    stats = {'claims': len(claims), 'branches': 0, 'immediate': 0, 'upgrades': 0,
             'future_pairs': 0, 'bounded_new_upgrades': 0, 'max_rounds': 0}
    for claim, profile in zip(claims, records):
        result = profiles.replay_claim(claim)
        profiles.check_profile(claim, profile)
        for key, value in result.items():
            stats[key] = max(stats[key], value) if key == 'max_rounds' else stats[key]+value
    return stats


def profiles_H_only():
    from .dense import profiles
    claims = json.loads((ROOT/'dense/data/certificate.json').read_text())
    records = json.loads((ROOT/'dense/data/profiles.json').read_text())
    stats = check_profile_data(claims, records)
    rejected = []
    def rejection(function, label):
        try:
            function()
        except (ValueError, KeyError, IndexError, TypeError):
            rejected.append(label)
            return
        raise ValueError('mutation accepted: '+label)
    def corrupt(label, change, index=0):
        altered = copy.deepcopy(claims[index]); change(altered)
        rejection(lambda: profiles.replay_claim(altered), label)
    corrupt('missing AP branch', lambda c: c['branches'].pop())
    corrupt('mandatory initial AP cost removed', lambda c: c['branches'][1]['states'][0].__setitem__(0, 0))
    corrupt('unsupported upgrade', lambda c: c['branches'][0]['states'][1].__setitem__(0, 1000))
    corrupt('terminal contradiction removed', lambda c: c['branches'][0]['states'].pop())
    corrupt('false mu', lambda c: c.__setitem__('mu', c['mu']+1))
    corrupt('boolean in place of integer', lambda c: c.__setitem__('C', True))
    corrupt('unchanged synchronous round', lambda c: c['branches'][0]['states'].insert(1, c['branches'][0]['states'][0].copy()))
    i = next(i for i, c in enumerate(claims) if c['h'] == 21 and c['r'] == 15)
    corrupt('beta9 invalid relaxed threshold', lambda c: c['branches'][0]['states'][1].__setitem__(14-c['branches'][0]['start'], 9), i)
    found = False
    for c in claims:
        for bi, b in enumerate(c['branches']):
            for si, (old, new) in enumerate(zip(b['states'], b['states'][1:])):
                if sum(new) > b['D']:
                    continue
                accelerated, _ = profiles.expected_round(new, b['start'], b['D'], c['h'])
                if accelerated != new:
                    altered = copy.deepcopy(c)
                    altered['branches'][bi]['states'][si+1] = accelerated
                    rejection(lambda: profiles.replay_claim(altered), 'NEW-vector self-justification')
                    found = True
                    break
            if found: break
        if found: break
    need(found, 'NEW-vector adversarial control exists')
    rejection(lambda: check_profile_data(claims[:-1], records), 'missing claim')
    altered_profile = copy.deepcopy(records[0]); altered_profile['rho'] += 1
    rejection(lambda: profiles.check_profile(claims[0], altered_profile), 'false rho output')
    need(not profiles.offscale_ok(7, tri(5)-1) and profiles.offscale_ok(7, tri(5)-2), 'strict offscale boundary')
    need(not profiles.bridge_ok(7, 1, tri(6)-6-7-1) and profiles.bridge_ok(7, 1, tri(6)-6-7-2), 'strict bridge boundary')
    need(not profiles.permitted(2, 4, 7, [], {}), 'strict hole boundary')
    need(not profiles.permitted(9, 21, 14, [], {}) and profiles.permitted(8, 21, 13, [], {}), 'beta8/beta9 size threshold')
    return {'thresholds': list(H_THRESHOLDS), 'r_domain': [15, 54], 'stats': stats,
            'mutations_rejected': rejected, 'strict_boundary_controls': 4,
            'all_upper_budgets_use': 'OLD vector',
            'mathematical_scope': 'Complete supplied proof traces for the 160 H claims, not profile discovery or maximization'}


def H_pair_and_band_arithmetic():
    records = json.loads((ROOT/'dense/data/profiles.json').read_text())
    need([(x['h'], x['r']) for x in records] == PROFILE_KEYS, 'H arithmetic profile domain')
    lookup = {(x['h'], x['r']): x for x in records}
    pairs = []
    minima = {}
    for h in H_THRESHOLDS:
        local = []
        for a in range(15, 55):
            b = 69-a
            # The elementary conversion alone suffices; no stronger inverse floor is needed.
            rho = (lookup[h, a]['mu']+2-2*a) + (lookup[h, b]['mu']+2-2*b)
            local.append(rho)
            pairs.append({'h': h, 'a': a, 'b': b, 'elementary_rho_pair': rho})
        minima[str(h)] = min(local)
    need(list(minima.values()) == [300, 345, 391, 436], 'H paired floors')
    bands = []
    for lo, hi, h in [(15,16,15), (17,20,17), (21,48,21)]:
        need(all(146-2*z >= max(49,z) for z in range(lo,hi+1)), 'low band active term')
        cap = 587-minima[str(h)]-(146-2*hi)
        bands.append({'z_min': lo, 'z_max': hi, 'profile_h': h, 'c_plus_I_cap': cap})
    need([x['c_plus_I_cap'] for x in bands] == [173,136,146], 'finite band caps')
    need(3*49 >= 146 and 587-minima['49'] == 151, 'unbounded z>=49 affine tail')
    need(78*3 > max([x['c_plus_I_cap'] for x in bands]+[151-49]), 'all j>=3 excluded')
    cells = []
    for a in range(15,55):
        b = 69-a; s = min(a,b); I = (34-s)*(35-s)
        for z in (15,16):
            delta_cap = 2*z-15-I
            if delta_cap >= 0:
                need(31 <= a <= 38 and 31 <= b <= 38, 'H2 direct theorem cardinalities')
                lower = 8*a-112+8*b-112+156+146-2*z
                upper = 587-I
                need(lower > upper, 'strict H2 contradiction')
                cells.append({'a': a, 'b': b, 'z': z, 'I': I, 'delta_cap': delta_cap,
                              'budget_lower': lower, 'budget_upper': upper, 'margin': lower-upper})
    need(len(cells) == 16 and min(x['margin'] for x in cells) == 11, 'complete H2 scalar domain')
    return {'pair_count': len(pairs), 'paired_floor_minima': minima, 'pairs': pairs,
            'finite_bands': bands, 'tail': 'For all integers z>=49, c+I+z<=151',
            'H2_cells': cells, 'H2_minimum_margin': min(x['margin'] for x in cells),
            'j_ge_3_margin': 234-173,
            'omitted': 'The historical 22920-cell grid is unnecessary; the four bands cover every z>=15',
            'mathematical_scope': 'Conditional on primitive cores, h(P),h(Q)>=z, exact structural budget and c>=78j+delta'}


def dense_bases():
    from .dense import dense
    result = dense.verify()
    overlap = sum(comb(2*beta+2,beta) for beta in range(6))
    result['small_boundary_overlap'] = overlap
    result['distinct_cases_in_union'] = result['boundary_total']+result['small_total']-overlap
    # Exact base plus forward difference proves these for all unbounded r,
    # supplementing the finite arithmetic loop in the retained checker.
    need((9*9-13*9+38)//2 == 1 and 9-6 > 0, 'beta<=8 joining polynomial')
    need(13*12//2-13-46 == 19 and 13-1 > 0, 'beta9 joining polynomial')
    result['unbounded_induction_polynomials'] = [
        {'expression': '(r^2-13r+38)/2', 'r_min': 9, 'base': 1, 'forward_difference': 'r-6 > 0'},
        {'expression': 'r(r-1)/2-r-46', 'r_min': 13, 'base': 19, 'forward_difference': 'r-1 > 0'}]
    result['mathematical_scope'] = 'Finite density bases; written induction and endpoint-hole counting prove unbounded r'
    return result


def restricted_direct_defect():
    from .dense import h15
    result = h15.verify()
    result['low_deletion_enumeration'] = {'q8': comb(18,8), 'q9': comb(18,9)}
    result['mathematical_scope'] = ('Finite lemma rho>=8j-44 on exactly the three deletion families, j=14..38; '
                                  'the written small-increment/tail/scale reduction proves primitive r=31..38, h>=15 => rho>=8r-112')
    return result


STAGES = [
    ('F3_NONAP_2340', 'Generic non-AP deleted-interval finite base', generic_nonap_base, False),
    ('F4_BOOTSTRAP_AP', 'STRUCTURAL86 bootstrap and AP/halfstep scalar predicates', structural_bootstrap, False),
    ('F4_INVERSE', 'STRUCTURAL86 inverse, endpoint repair, overlap and primitivity arithmetic', structural_inverse, False),
    ('F4_FIXED_WITNESSES', 'Four fixed integer witnesses over the complete three-family domain', structural_fixed_witnesses, False),
    ('F6_H_PROFILES', 'H-only synchronous profile proof traces at four hole thresholds', profiles_H_only, False),
    ('F6_H_BANDS', 'H paired floors, four analytic bands, j>=3 and H2 contradiction', H_pair_and_band_arithmetic, False),
    ('F6_DENSE_BASES', 'Bounded-density complete boundary and small-cardinality bases', dense_bases, True),
    ('F6_RESTRICTED_DIRECT', 'Complete restricted direct-defect base with independent algorithms', restricted_direct_defect, True),
]


def run_checks(mode='quick'):
    need(mode in ('quick', 'full'), 'mode must be quick or full')
    records = []
    for identity, description, function, full_only in STAGES:
        if full_only and mode != 'full':
            records.append({'id': identity, 'status': 'SKIP', 'description': description,
                            'details': {'reason': 'Full mode required; quick mode is not a complete finite foundation replay'}})
            continue
        start = time.perf_counter()
        try:
            details = function()
            record = {'id': identity, 'status': 'PASS', 'description': description, 'details': details}
        except Exception as error:
            record = {'id': identity, 'status': 'FAIL', 'description': description,
                      'details': {'error_type': type(error).__name__, 'error': str(error)}}
        record['elapsed_seconds'] = round(time.perf_counter()-start, 6)
        records.append(record)
    return records
