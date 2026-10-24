"""Strict, complete synchronous replay. Every upper budget uses the OLD vector."""
import copy
from pathlib import Path
import gzip,json
ROOT=Path(__file__).resolve().parents[2]
def need(ok,message):
    if not ok:raise ValueError(message)
def integer(x,lo=0):return type(x) is int and x>=lo
def tri(x):return x*(x+1)//2

HS = (5, 7, 9, 11, 13, 15, 17, 21, 31, 49)
KEYS = [(h, r) for h in HS for r in range(15, 56)]

def offscale_ok(j, upper):
    return tri(j - 2) - 1 > upper

def bridge_ok(j, beta, upper):
    return tri(j - 1) - 5 * beta > j + upper + 1

def permitted(beta, h, i, later, uppers):
    if not integer(beta, 1) or not 2 * beta < h:
        return False
    if i < (beta + 5 if beta <= 24 else 2 * beta + 5):
        return False
    return all(offscale_ok(j, uppers[j]) and bridge_ok(j, beta, uppers[j]) for j in later)

def expected_round(old, start, D, h):
    ids = list(range(start, start + len(old)))
    # Frozen OLD sum; never replace it while looping through coordinates.
    old_sum = sum(old)
    upper = {j: D - old_sum + old[p] for p, j in enumerate(ids)}
    expected = old.copy()
    for p, i in enumerate(ids):
        for beta in range(1, (h - 1) // 2 + 1):
            if permitted(beta, h, i, ids[p + 1:], upper):
                expected[p] = max(expected[p], beta)
    return expected, upper

def replay_claim(claim,allowed_hs=HS):
    need(set(claim) == {'r', 'h', 'C', 'mu', 'branches'}, 'claim fields')
    r, h, C = claim['r'], claim['h'], claim['C']
    need(integer(r, 15) and r <= 55 and integer(h, 1) and h in allowed_hs,
         'claim domain integers')
    need(integer(C) and integer(claim['mu']) and claim['mu'] == r + C + 1, 'mu floor')
    branches = claim['branches']
    need(type(branches) is list and [b['k'] for b in branches] == [None] + list(range(3, r)),
         'complete branch coverage')
    stats = dict(branches=0, immediate=0, upgrades=0, future_pairs=0,
                 bounded_new_upgrades=0, max_rounds=0)
    for branch in branches:
        need(set(branch) == {'k', 'start', 'D', 'states'}, 'branch fields')
        k = branch['k']
        need(k is None or integer(k, 3), 'branch integer')
        start = 4 if k is None else k + 1
        D = C + (3 if k is None else k)
        need(type(branch['start']) is int and type(branch['D']) is int and
             branch['start'] == start and branch['D'] == D, 'branch budget')
        n = r - start + 1
        initial = [0] * n
        if k is not None:
            initial[0] = tri(k) - k - 1
        states = branch['states']
        need(type(states) is list and len(states) > 0, 'nonempty states')
        need(all(type(v) is list and len(v) == n and all(integer(x) for x in v)
                 for v in states), 'all state vectors are nonnegative integer vectors')
        need(states[0] == initial, 'mandatory initial AP cost')
        stats['branches'] += 1
        stats['immediate'] += len(states) == 1
        stats['max_rounds'] = max(stats['max_rounds'], len(states) - 1)
        for old, new in zip(states, states[1:]):
            need(sum(old) <= D, 'no round after contradiction')
            need(old != new, 'no empty round')
            expected, upper = expected_round(old, start, D, h)
            need(new == expected, 'exact complete synchronous OLD-vector update')
            for p, (lo, hi) in enumerate(zip(old, new)):
                need(hi >= lo, 'coordinate monotonicity')
                if hi > lo:
                    stats['upgrades'] += 1
                    stats['future_pairs'] += n - p - 1
                    stats['bounded_new_upgrades'] += start + p < 2 * hi + 5
                    # Explicit direct tests, as well as exact whole-round equality.
                    need(permitted(hi, h, start + p, range(start + p + 1, r + 1), upper),
                         'direct strict update tests')
        need(sum(states[-1]) > D, 'strict terminal contradiction')
    return stats

def check_profile(claim, profile):
    r,h,mu=claim['r'],claim['h'],claim['mu']
    inverse=[]
    for g in range(2,11):
        saturation=(g-1)*(r-14)
        possible=[v for v in range(saturation) if mu<=v+4*g-2+2*(v//(g-1))]
        inverse.append(min(possible+[saturation]))
    elementary=mu+2-2*r
    nonap=r-5 if r>=17 else r-14
    need(profile['elementary_rho']==elementary and profile['rho']==max(elementary,nonap,*inverse),'Exact new profile floors')

def verify():
    data=json.loads(gzip.decompress((ROOT/'data/upper80_profiles.json.gz').read_bytes()))
    need([(r['h'],r['r']) for r in data]==KEYS,'Complete profile catalogue')
    stats=[];profiles={}
    for row in data:
        need(set(row)=={'r','h','C','mu','branches','rho','elementary_rho'},'Profile packet fields')
        claim={k:row[k] for k in ('r','h','C','mu','branches')}
        stats.append(replay_claim(claim));check_profile(claim,row);profiles[row['h'],row['r']]=row
    bad=copy.deepcopy({k:data[0][k] for k in ('r','h','C','mu','branches')});bad['mu']+=1
    rejected=False
    try:replay_claim(bad)
    except ValueError:rejected=True
    need(rejected,'Profile negative control')
    pairs=[]
    for h in HS:
        pairs.append(dict(h=h,mu=min(profiles[h,r]['mu']+profiles[h,64-r]['mu'] for r in range(15,50)),
                          rho=min(profiles[h,r]['rho']+profiles[h,64-r]['rho'] for r in range(15,50))))
    return dict(status='PASS_DENSITY24_PROFILES',global_upper_bound_certified=False,claims=len(data),
                branches=sum(s['branches'] for s in stats),upgrades=sum(s['upgrades'] for s in stats),paired=pairs,negative_controls=1)

if __name__=='__main__':print(json.dumps(verify(),indent=2))
