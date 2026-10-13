#!/usr/bin/env python3
"""Replay the finite checks accompanying the written upper-84 supplement.

This is not a formal proof checker for the infinite mathematical inputs.
Each child interpreter runs without -O, so its assertions remain enabled.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def validate_checks(manifest, root):
    approved = json.loads((root / 'check_list.json').read_text())
    expected_names = {
        'ap_bootstrap', 'inverse_and_boundaries', 'highhole_localization',
        'source_fringe', 'zero_low_indices', 'zero_endpoint_cards',
        'z3_side_union', 'p2_activity_and_forests', 'dense_seed_6188',
        'p3_terminal', 'p4_cards', 'p4_cross', 'z4_ownerless',
        'z5_thirteen_cards', 'z5_alpha_final', 'z5_a1_b', 'z5_c5t_cutoff'}
    children = {'zero_low_indices', 'z3_side_union', 'z4_ownerless',
                'z5_thirteen_cards', 'z5_alpha_final', 'z5_a1_b',
                'z5_c5t_cutoff'}
    require(len(approved) == 17 and
            {row['name'] for row in approved} == expected_names,
            'The approved finite-check inventory must contain all 17 modules.')
    require(manifest['finite_module_count'] == 17 and
            manifest['finite_check_modules'] == approved,
            'The manifest does not match the approved 17-module inventory.')
    require(len(manifest['aggregate_children']) == 7 and
            set(manifest['aggregate_children']) == children,
            'The seven aggregate children must be retained exactly.')
    expected_top = [row for row in approved if row['name'] not in children]
    require(manifest['finite_checks'] == expected_top,
            'A top-level finite check was omitted, changed, or added.')
    require('check_list.json' in manifest['sha256'] and
            all(row['script'] in manifest['sha256'] for row in approved),
            'An approved check input is missing from the integrity inventory.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full', action='store_true',
                        help='also run the inherited full upper-85 verification suite')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'COVERAGE85.json').read_text())
    validate_checks(manifest, root)
    required = {f'Z{j}' for j in range(6)} | {f'P{j}' for j in range(6)} | {'H'}
    require(set(manifest['written_case_coverage']) == required,
            'The written case coverage must include exactly Z0-Z5, P0-P5, H.')
    require(all(row['status'] == 'excluded' for row in
                manifest['written_case_coverage'].values()),
            'An unresolved written case remains in the coverage manifest.')
    for relative, digest in manifest['sha256'].items():
        path = root / relative
        require(path.is_file(), f'Missing proof/check input: {relative}')
        require(hashlib.sha256(path.read_bytes()).hexdigest() == digest,
                f'Proof/check input has changed: {relative}')
    results_dir = root / 'verification_results'
    results_dir.mkdir(exist_ok=True)
    checks = list(manifest['finite_checks'])
    if args.full:
        checks.append({'name': 'retained_upper85_full',
                       'script': 'audit/verification_program/verify.py',
                       'args': ['--full', '--output-dir', str(results_dir / 'retained_full')]})
    results = []
    for check in checks:
        script = root / check['script']
        start = time.monotonic()
        result = subprocess.run(
            [sys.executable, '-E', '-S', '-B', str(script), *check.get('args', [])],
            cwd=script.parent, capture_output=True, text=True)
        elapsed = time.monotonic() - start
        log = result.stdout + ('\nSTDERR:\n' + result.stderr if result.stderr else '')
        (results_dir / (check['name'] + '.txt')).write_text(log)
        record = {'name': check['name'], 'returncode': result.returncode,
                  'seconds': round(elapsed, 4)}
        results.append(record)
        print(f"{'PASS' if result.returncode == 0 else 'FAIL'}  {check['name']}")
        if result.returncode:
            print(log)
            break
    passed = sum(row['returncode'] == 0 for row in results)
    complete = len(results) == len(checks) and passed == len(checks)
    summary = {'status': 'PASS' if complete else 'FAIL',
               'finite_checks_passed': passed, 'finite_checks_requested': len(checks),
               'full_retained_replay': args.full,
               'proof_scope': manifest['proof_scope'], 'results': results}
    (results_dir / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(f"{summary['status']}: {passed}/{len(checks)} finite check suites.")
    print('The infinite inputs and actual-set-to-inequality arguments remain written proofs.')
    return 0 if complete else 1


if __name__ == '__main__':
    raise SystemExit(main())
