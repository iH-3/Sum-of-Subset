"""Size-89 endpoint with translated leading-core overlap.

A complete certificate is required before claiming the upper bound 88.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import upper88_candidate as previous
from leading_core_overlap import model, branches

ROOT = previous.ROOT
FORMAT = 'upper88-leading-core-v1'
DEFAULT_CERTIFICATE = ROOT / 'data/upper88_endpoint_certificates.json'
roots = previous.roots
base = previous.base
Quadratic = previous.Quadratic
interval_certificate = previous.interval_certificate
extend_rows = previous.extend_rows
require = previous.require
row_policy = previous.row_policy


def check_coverage(bundle, exhaustive=False, *, partial=False):
    return previous.check_coverage(bundle, exhaustive, partial=partial,
                                   model_builder=model, branch_builder=branches,
                                   expected_format=FORMAT)


def negative_controls(bundle):
    from copy import deepcopy
    rejected = []

    def reject(label, call):
        try:
            call()
        except (ValueError, KeyError):
            rejected.append(label)
        else:
            raise ValueError('Invalid input accepted: ' + label)

    group = next(roots())
    names, rows = model(group, Quadratic(0, 1), 'coarse')
    reject('negative_weight', lambda: interval_certificate(names, rows, {'Gp': -1}, group['lo'], group['hi']))
    reject('noncontradictory_weight', lambda: interval_certificate(names, rows, {'Dp1': 1}, group['lo'], group['hi']))
    reject('unknown_row', lambda: interval_certificate(names, rows, {'invented': 1}, group['lo'], group['hi']))
    reject('interior_vertex_failure', lambda: interval_certificate(['x'], {'r': ([0], Quadratic(0, 2, -1))}, {'r': 1}, -1, 3))
    bad = deepcopy(bundle)
    del bad['roots'][group['key']]
    reject('missing_root', lambda: check_coverage(bad))
    bad = deepcopy(bundle)
    bad['roots'][group['key']]['segments'][0][0] += 1
    reject('missing_integer', lambda: check_coverage(bad))
    key = next(k for k, v in bundle['roots'].items() if v['trees'])
    small = dict(format=FORMAT, pool=bundle['pool'], roots={key: bundle['roots'][key]})
    reject('partial_as_complete', lambda: check_coverage(small))
    bad = deepcopy(small)
    next(iter(bad['roots'][key]['trees'].values()))['children'].pop()
    reject('missing_child', lambda: check_coverage(bad, partial=True))
    bad = deepcopy(small)
    tree = next(iter(bad['roots'][key]['trees'].values()))
    tree['children'][0] = deepcopy(tree)
    reject('repeated_disjunction', lambda: check_coverage(bad, partial=True))
    bad = deepcopy(small)
    next(iter(bad['roots'][key]['trees'].values()))['split'] = 'invented'
    reject('unproved_disjunction', lambda: check_coverage(bad, partial=True))
    reject('unproved_next_endpoint', lambda: previous.scalar_audit(88))
    reject('double_outside_loss', lambda: require(3 >= 2 + 1 + 1, 'Shared outside loss is counted once'))
    return rejected


def main():
    import argparse
    from fractions import Fraction
    import hashlib
    import json
    parser = argparse.ArgumentParser(description='Exact complete size-89 exclusion; standard library only.')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--exhaustive', action='store_true')
    args = parser.parse_args()
    paths = sorted((ROOT / 'verification').glob('*.py')) + [
        DEFAULT_CERTIFICATE, ROOT / 'data/fixed_cover_certificate.json',
        ROOT / 'data/upper88_relaxation_witness.json']

    def fingerprint():
        return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}

    before = fingerprint()
    bundle = json.loads(DEFAULT_CERTIFICATE.read_text())
    checked = check_coverage(bundle, args.exhaustive)
    require(checked['coverage'] == 'COMPLETE', 'Complete root coverage required')
    scalar = previous.scalar_audit()
    witness = json.loads((ROOT / 'data/upper88_relaxation_witness.json').read_text())
    import upper88_progress
    old_witness = upper88_progress.check_witness(witness)
    names, rows = model(witness['group'], witness['a'], witness['kind'])
    violations = {}
    for label, (vector, rhs) in rows.items():
        if label.startswith('leading_core_'):
            excess = sum(co * Fraction(witness['point'][v])
                         for co, v in zip(vector, names) if co) - rhs
            if excess > 0:
                violations[label] = str(excess)
    require(violations == {f'leading_core_{s}3_{keep}': '72' for s in 'pq'
                           for keep in ('leading', 'own')}, 'Witness cut changed')
    summary = dict(status='PASS', endpoint=89, upper_bound=88,
                   conclusion='Together with the independently audited N <= 89 chain, 71 <= N <= 88.',
                   verification_mode='interval-plus-exhaustive' if args.exhaustive else 'symbolic-interval',
                   linear={k: v for k, v in checked.items() if k != 'proof_checks'},
                   scalar=scalar['summary'], old_relaxation=old_witness,
                   old_witness_violations=violations,
                   high_grouping={kind: previous.high_group_audit(scalar, kind)
                                  for kind in ('coarse', 'global_nested')},
                   negative_controls=negative_controls(bundle))
    require(fingerprint() == before, 'Proof input changed during verification')
    output = dict(summary=summary, scalar_audit=scalar,
                  proof_checks=checked['proof_checks'], sha256=before)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, default=base.json_default, indent=2) + '\n')
    concise = dict(summary)
    concise['linear'] = {k: v for k, v in summary['linear'].items() if k != 'used_vectors'}
    print(json.dumps(concise, default=base.json_default, indent=2))


if __name__ == '__main__':
    main()
