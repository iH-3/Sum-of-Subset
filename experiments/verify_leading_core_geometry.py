#!/usr/bin/env python3
"""Evaluate the new emitted inequalities on actual finite sets (stdlib only)."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'verification'))
import leading_core_overlap as extension
proof = extension.previous


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    rng = random.Random(2026101803)
    counts = {'leading_core': 0, 'whole_side': 0, 'allocation': 0}
    cases = 0
    for branch in ('A', 'B'):
        key = 'Z4:' + branch + ':pair1,pair2,p0,q0:-:-'
        group = next(g for g in proof.roots() if g['key'] == key)
        names, rows = extension.model(group, 36, 'global_nested')
        for _ in range(120):
            p = sorted(rng.sample(range(1, 171), 36))
            q = sorted(rng.sample(range(1, 171), 36))
            tails = {s: [core[-1] + t for t in sorted(rng.sample(range(1, 131), 4))]
                     for s, core in (('p', p), ('q', q))}
            d = set(p + tails['p']) | {-v for v in q + tails['q']} | {0}
            dd = {v + w for v in d for w in d}
            point = dict.fromkeys(names, 0)
            point.update(Rp=p[-1], Rq=q[-1], Mp=max(d), Mq=-min(d), K=len(dd))
            for side in 'pq':
                outer = sorted(rng.sample(range(point['M' + side] + 1,
                                               point['M' + side] + 2001), 4), reverse=True)
                point.update({side + str(i): v for i, v in enumerate(outer, 1)})
                point['S' + side] = rng.randrange(1, 4001)
            centers = {v: sum(co * point[k] for k, co in form.items())
                       for v, form in proof.centers().items()}
            whole_deficits = []
            for side in 'pq':
                sign = 1 if side == 'p' else -1
                leading = point[side + '1'] - sum(point[side + str(i)] for i in (2, 3, 4))
                s = point['S' + side]
                raw = {leading + sign * v for v in dd}
                lead_inside = {v for v in raw if 1 <= v <= s}
                point['lead_' + side] = len(raw) - len(lead_inside)
                inside = {}
                for slot in group['mode']['slots']:
                    if slot[0] != side:
                        continue
                    raw = {centers[slot] + sign * v for v in d}
                    inside[slot] = {v for v in raw if 1 <= v <= s}
                    point['l_' + slot] = sum(v <= 0 for v in raw)
                    point['u_' + slot] = sum(v > s for v in raw)
                full_members = [v for v in inside if int(v[1:]) < 4 or int(v[1:]) in (6, 7)]
                full_union = lead_inside.union(*(inside[v] for v in full_members))
                point['full_' + side] = len(dd) + len(d) * len(full_members) - len(full_union)
                whole_union = lead_inside.union(*inside.values())
                point['whole_' + side] = len(dd) + len(d) * len(inside) - len(whole_union)
                whole_deficits.append(point['whole_' + side])
            point['delta'] = sum(whole_deficits) + proof.row_policy(group)['fixed_loss']
            for label, (vector, rhs) in rows.items():
                family = ('leading_core' if label.startswith('leading_core_') else
                          'whole_side' if label.startswith('whole_') else
                          'allocation' if label == 'full_joint' else None)
                if family:
                    proof.require(sum(co * point[v] for co, v in zip(vector, names)) <= rhs,
                                  'Invalid actual-set inequality: ' + label)
                    counts[family] += 1
            cases += 1
    witness = json.loads((ROOT / 'data/upper88_relaxation_witness.json').read_text())
    names, rows = extension.model(witness['group'], witness['a'], witness['kind'])
    violations = {}
    for label, (vector, rhs) in rows.items():
        if label.startswith('leading_core_'):
            excess = sum(co * Fraction(witness['point'][v])
                         for co, v in zip(vector, names) if co) - rhs
            if excess > 0:
                violations[label] = str(excess)
    proof.require(violations == {f'leading_core_{s}3_{keep}': '72'
                                for s in 'pq' for keep in ('leading', 'own')},
                  'Previous witness is not excluded as expected')
    # A raw pair with one shared outside point has deficit 3, not 4.
    u = {0, 1}; target = {1}
    deficit = 2 * len(u) - len(u & target)
    proof.require(deficit == 3 and len(u & u) + 2 * len(u - target) == 4,
                  'Double-outside-loss negative control failed')
    paths = [Path(__file__), ROOT / 'verification/leading_core_overlap.py',
             ROOT / 'verification/upper88_candidate.py',
             ROOT / 'data/upper88_relaxation_witness.json']
    result = dict(status='PASS_GEOMETRY_ONLY', cases=cases, seed=2026101803,
                  checks=counts, old_witness_violations=violations,
                  negative_controls=['adding_both_outside_losses'],
                  scope='Finite actual-set checks supplement the general proof; no global upper bound follows from this run.',
                  sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
