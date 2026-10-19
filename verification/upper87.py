#!/usr/bin/env python3
"""Replay the size-88 endpoint in the immutable archive using only stdlib.

This is a fresh composition of its documented ordinary-range interface and
ALL supplemental/structural checks, not a replay of saved success logs.
The mathematical adoption and prior bound N <= 88 are separate prerequisites;
see reports/upper87_adoption_20261019.tex. Never run this program with -O.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_SHA = '390d390c1172471ff97f04113d54937de2ae070cabcb272f5529f08a19a069df'
PAYLOAD_SHA = '9e3631ce91c9ab07caba32b8ed55c3b0c011870ebf6a5b887206ecd3cab86c75'
PREFIX = ('subset_sums_upper86_complete_verification_20261005/'
          'payload/subset_sum_verification/proofs/exact87/')
N = 1128280


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def extract(destination):
    folder = ROOT/'archive/upper86'
    manifest = json.loads((folder/'manifest.json').read_text())
    chunks = []
    for part in manifest['parts']:
        require(Path(part['name']).name == part['name'], 'Invalid archive part')
        raw = (folder/part['name']).read_bytes()
        require(len(raw) == part['bytes'] and sha(raw) == part['sha256'],
                'Archive part differs: '+part['name'])
        chunks.append(raw)
    raw = b''.join(chunks)
    require(len(raw) == manifest['bytes'] and
            sha(raw) == manifest['sha256'] == ARCHIVE_SHA, 'Wrong archive')
    count = 0
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        seen = set()
        for item in archive.infolist():
            if not item.filename.startswith(PREFIX) or item.is_dir():
                continue
            relative = item.filename[len(PREFIX):]
            path = PurePosixPath(relative)
            require(not path.is_absolute() and '..' not in path.parts and
                    '\\' not in relative and relative not in seen,
                    'Unsafe or repeated archive member')
            seen.add(relative)
            target = destination.joinpath(*path.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(item))
            count += 1
    require(sha((destination/'payload_manifest.json').read_bytes()) == PAYLOAD_SHA,
            'Wrong endpoint manifest')
    return count


def combine(ranges, expected):
    require(len(ranges) == len(expected), 'Missing range')
    ordered = sorted(ranges, key=lambda r: r['range_start'])
    require([(r['range_start'], r['range_stop_exclusive']) for r in ordered]
            == expected, 'Missing, repeated or overlapping range')
    require(expected[0][0] == 0 and expected[-1][1] == N and
            all(a[1] == b[0] for a, b in zip(expected, expected[1:])),
            'Nonexhaustive requested partition')
    for r, (lo, hi) in zip(ordered, expected):
        require(r['verified'] is True and r['original_roots'] == N,
                'Unverified range')
        require(set(r['checked_counts']) <= {'certified', 'supplemental'} and
                sum(r['checked_counts'].values()) == hi-lo,
                'Range census mismatch')
    for key in ('compact_sha256', 'source_bundle_sha256', 'canonical_manifest_sha256'):
        require(len({r[key] for r in ordered}) == 1, 'Range identity mismatch')
    require(sum(r['checked_counts'].get('certified', 0) for r in ordered) == 1127649,
            'Ordinary arithmetic incomplete')
    require(sum(r['checked_counts'].get('supplemental', 0) for r in ordered) == 631,
            'Supplement complement mismatch')
    return ordered


def replay(work, jobs):
    started = time.monotonic()
    require(not work.exists(), 'Use a fresh work directory; saved logs are not inputs')
    work.mkdir(parents=True)
    source = work/'exact87'
    file_count = extract(source)
    logs = work/'logs'
    logs.mkdir()
    py = [sys.executable, '-I', '-E', '-S', '-B', '-u', '-X', 'utf8']
    own_sources = {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in
                   (Path(__file__).resolve(), ROOT/'verification/upper87_geometry.py')}

    def execute(name, script, arguments=(), marker=None):
        command = py+[str(source/script), *arguments]
        before = time.monotonic()
        path = logs/(name+'.log')
        with path.open('wb') as stream:
            code = subprocess.run(command, cwd=source, stdout=stream,
                                  stderr=subprocess.STDOUT).returncode
        raw = path.read_bytes()
        rec = dict(name=name, command=command, returncode=code,
                   seconds=round(time.monotonic()-before, 3),
                   log_sha256=sha(raw), marker=marker,
                   marker_present=marker is None or marker.encode() in raw)
        (logs/(name+'.receipt.json')).write_text(json.dumps(rec, indent=2)+'\n')
        print(name, 'exit', code, 'marker', rec['marker_present'], flush=True)
        require(code == 0 and rec['marker_present'], 'Failed stage: '+name)
        return rec

    initial = execute('initial_integrity', 'verify_integrity.py',
                      marker='PASS 984 frozen payload files')
    intervals = [(N*i//jobs, N*(i+1)//jobs) for i in range(jobs)]
    records = []
    with ThreadPoolExecutor(max_workers=jobs+1) as executor:
        pending = [executor.submit(execute, 'supplements', 'verify_exact87.py',
                   ['--supplements-and-union-only'], 'PARTIAL ONLY:')]
        for i, (lo, hi) in enumerate(intervals):
            pending.append(executor.submit(execute, 'ordinary_'+str(i),
                           'frozen_runner.py', ['verify_compact_ordinary.py',
                           '--start', str(lo), '--stop', str(hi)]))
        for future in as_completed(pending):
            records.append(future.result())
    ranges = []
    for i in range(jobs):
        lines = (logs/('ordinary_'+str(i)+'.log')).read_text().splitlines()
        ranges.append(json.loads(next(line for line in reversed(lines)
                                      if line.startswith('{'))))
    ranges = combine(ranges, intervals)
    negative = []
    for label, altered in [('missing_range', ranges[:-1]),
                           ('duplicate_range', ranges+[ranges[0]])]:
        try:
            combine(altered, intervals)
        except ValueError:
            negative.append(label)
        else:
            raise ValueError('Negative control accepted: '+label)
    final = execute('final_integrity', 'verify_integrity.py',
                    marker='PASS 984 frozen payload files')
    require(all(sha((ROOT/p).read_bytes()) == h for p,h in own_sources.items()),
            'New verifier source changed during replay')
    return dict(status='PASS_COMPLETE_ENDPOINT_FINITE_REPLAY',
                mathematical_adoption='reports/upper87_adoption_20261019.tex',
                prior_independent_upper_bound=88, conditional_result=87,
                proof_assistant_formalization=False,
                execution='Fresh parallel composition of all documented ranges and all supplemental stages',
                archive_sha256=ARCHIVE_SHA, payload_manifest_sha256=PAYLOAD_SHA,
                extracted_files=file_count, original_roots=N, ordinary_leaves=1127649,
                supplemental_parents=631, supplemental_children=743,
                supplemental_splits=4352, supplemental_leaves=5095,
                total_leaves=1132744, ranges=ranges,
                negative_controls=negative, source_sha256=own_sources,
                initial_integrity=initial, final_integrity=final,
                records=sorted(records, key=lambda r:r['name']),
                seconds=round(time.monotonic()-started,3))


def main():
    require(__debug__, 'Run without -O: archived assertion checks must remain enabled')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--jobs', type=int, default=4)
    p.add_argument('--work-dir', type=Path)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    require(1 <= args.jobs <= 32, 'jobs must be between 1 and 32')
    if args.work_dir:
        result = replay(args.work_dir.resolve(), args.jobs)
    else:
        with tempfile.TemporaryDirectory(prefix='upper87-') as temp:
            result = replay(Path(temp)/'replay', args.jobs)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'], 'original roots', N, flush=True)


if __name__ == '__main__':
    main()
