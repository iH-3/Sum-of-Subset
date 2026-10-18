#!/usr/bin/env python3
"""Replay the published finite checks, recording failures without hiding them.

This driver does not certify the mathematical reduction to those checks.
Children use no site packages and explicit output files. The original baseline
retains its documented sibling-import startup; later checkers use -I as well.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['verify', 'review_checks', 'upper103', 'upper100', 'upper99',
         'upper98', 'upper97', 'upper97_simplified', 'upper96', 'upper95',
         'upper94', 'upper93', 'upper92', 'upper91', 'upper90', 'upper89',
         'upper88_progress']


def digest(data):
    return hashlib.sha256(data).hexdigest()


def replay(name, optimized, destination):
    label = name + ('_optimized' if optimized else '')
    output = destination / (label + '.json')
    # The original standalone baseline imports a sibling without adding its
    # directory to sys.path; -E preserves that documented startup behavior.
    command = [sys.executable, '-E' if name == 'verify' else '-I', '-S', '-B']
    if optimized:
        command.append('-O')
    command += [str(ROOT / 'verification' / (name + '.py')),
                '--output', str(output)]
    start = time.monotonic()
    result = subprocess.run(command, cwd=ROOT, capture_output=True)
    (destination / (label + '.stdout')).write_bytes(result.stdout)
    (destination / (label + '.stderr')).write_bytes(result.stderr)
    row = dict(name=name, optimized=optimized, returncode=result.returncode,
               seconds=round(time.monotonic()-start, 3), command=command,
               stdout_sha256=digest(result.stdout), stderr_sha256=digest(result.stderr))
    if output.is_file():
        data = output.read_bytes()
        row['output_sha256'] = digest(data)
        parsed = json.loads(data)
        row['reported_status'] = parsed.get('status', parsed.get('summary', {}).get('status'))
        expected = 'PASS_PROGRESS_ONLY' if name == 'upper88_progress' else 'PASS'
        row['expected_status'] = expected
        row['status_matches'] = row['reported_status'] == expected
        reference_name = 'proof_method' if name == 'upper97_simplified' else name
        reference = sorted((ROOT / 'results').glob('*/' + reference_name + '/result.json*'))
        if reference:
            previous = reference[-1].read_bytes()
            if reference[-1].suffix == '.gz':
                previous = gzip.decompress(previous)
            row['reference'] = str(reference[-1].relative_to(ROOT))
            row['reference_byte_equal'] = previous == data
            row['reference_json_equal'] = json.loads(previous) == parsed
    (destination / (label + '.receipt.json')).write_text(json.dumps(row, indent=2)+'\n')
    return row


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--jobs', type=int, default=4)
    p.add_argument('--optimized', action='store_true')
    p.add_argument('--names', nargs='+', choices=NAMES, default=NAMES)
    args = p.parse_args()
    if args.jobs < 1:
        p.error('--jobs must be positive')
    destination = args.output_dir.resolve()
    if destination.exists():
        p.error('Use a fresh output directory; stale outputs are not reused')
    destination.mkdir(parents=True)
    sources = {str(f.relative_to(ROOT)): digest(f.read_bytes())
               for folder in ('verification', 'data')
               for f in sorted((ROOT/folder).rglob('*'))
               if f.is_file() and f.suffix in ('.py', '.json')}
    jobs = [(name, opt) for name in args.names
            for opt in ([False, True] if args.optimized else [False])]
    rows = []
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        pending = [executor.submit(replay, name, opt, destination) for name,opt in jobs]
        for future in as_completed(pending):
            row = future.result()
            rows.append(row)
            print(row['name'], 'optimized' if row['optimized'] else 'standard',
                  'exit', row['returncode'], flush=True)
    rows.sort(key=lambda r: (r['name'], r['optimized']))
    matches = {}
    if args.optimized:
        for name in args.names:
            a, b = destination/(name+'.json'), destination/(name+'_optimized.json')
            matches[name] = a.exists() and b.exists() and a.read_bytes() == b.read_bytes()
    unchanged = all((ROOT/f).is_file() and digest((ROOT/f).read_bytes()) == h
                    for f,h in sources.items())
    passed = all(r['returncode'] == 0 and r.get('status_matches', False)
                 for r in rows) and all(matches.values()) and unchanged
    summary = dict(status='PASS_FINITE_REPLAY_ONLY' if passed else 'FAIL',
                   scope='Finite checks only; not an audit of every written implication',
                   source_sha256=sources, sources_unchanged=unchanged,
                   optimized_byte_equal=matches, runs=rows)
    (destination/'replay_summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
