#!/usr/bin/env python3
"""Complete exact finite replay for the written N<=82 proof.

Python 3.10+, standard library only. The companion proof supplies the
unbounded actual-set arguments; this is not a proof-assistant development.
"""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import model
import replay
import coverage
import geometry
import structure
import compression

MANIFEST = ROOT / 'data/upper82_global_sources.json'
PACKETS = tuple('native_j' + str(j) for j in range(1, 7)) + ('ownerless', 'endpoint_leaves', 'low_c')
REQUIRED = {'baseline83', 'alpha', 'coverage', 'packets', 'structure', 'geometry', 'compression', 'controls'}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), default=str).encode()).hexdigest()


def validate(data=None):
    data = json.loads(MANIFEST.read_text()) if data is None else data
    need(data.get('schema') == 'upper82-global-sources-v1', 'Source manifest schema')
    need(set(data['required_checks']) == REQUIRED, 'Missing verification obligation')
    pinned = {}
    for entry in data['files']:
        path = Path(entry['path'])
        need(not path.is_absolute() and '..' not in path.parts and entry['path'] not in pinned, 'Source path')
        need(sha(ROOT / path) == entry['sha256'], 'Source mismatch: ' + entry['path'])
        pinned[entry['path']] = entry['sha256']
    local = {p.relative_to(ROOT).as_posix() for p in HERE.iterdir() if p.is_file()}
    local |= {p.relative_to(ROOT).as_posix() for p in (ROOT / 'data/upper82_global').iterdir() if p.is_file()}
    local |= {'data/upper82_global_gap_inventory.json', 'reports/upper82_complete_20261019.tex', 'reports/upper82_complete_20261019.pdf'}
    need(local <= set(pinned), 'Unpinned new proof source')
    for name in ('upper83_complete', 'upper82_alpha'):
        rel = 'data/' + name + '_sources.json'
        need(rel in pinned, 'Missing prior manifest')
        old = json.loads((ROOT / rel).read_text())
        need(all(pinned.get(x['path']) == x['sha256'] for x in old['files']), 'Changed or missing transitive dependency')
    return data


def load_packets():
    out = {}
    for name in PACKETS:
        path = ROOT / 'data/upper82_global' / (name + '.json.gz')
        packet = json.loads(gzip.decompress(path.read_bytes()))
        need(packet['schema'] == 'upper82-exact-packet-v1', 'Final packet schema: ' + name)
        out[name] = packet
    trees = json.loads((ROOT / 'data/upper82_global/endpoint_trees.json').read_text())
    return out, trees


def dispatch(packets, trees):
    return coverage.verify([packets[n] for n in PACKETS[:6]], packets['ownerless'], packets['endpoint_leaves'], trees, packets['low_c'])


def controls(packets, trees, manifest):
    rejected = []
    def reject(label, fn):
        try:
            fn()
        except (ValueError, KeyError, TypeError, IndexError):
            rejected.append(label)
        else:
            raise ValueError('Invalid mutation accepted: ' + label)
    bad = dict(packets)
    bad['native_j1'] = dict(packets['native_j1'], records=packets['native_j1']['records'][1:])
    reject('missing native root', lambda: dispatch(bad, trees))
    badtree = deepcopy(trees)
    next(t['tree'] for t in badtree if 'right' in t['tree']).pop('right')
    reject('missing complementary endpoint branch', lambda: dispatch(packets, badtree))
    badowner = dict(packets['ownerless'], records=packets['ownerless']['records'][1:])
    reject('missing ownerless status', lambda: coverage.verify_ownerless(badowner, coverage.expected_main()[1]))
    badroot = deepcopy(packets['native_j1']['records'][0]); badroot['tau'] = 0
    reject('undispatched fixed core mass', lambda: coverage.collect_roots([{'records': [badroot]}]))
    reject('negative inequality multiplier', lambda: replay.evaluate({'weights': [['x', -1]], 'denominator': None}, {'x': ({'x': 1}, 1, 'le')}))
    reject('negative residual coefficient', lambda: replay.evaluate({'weights': [['x', 1]], 'denominator': None}, {'x': ({'x': -1}, -1, 'le')}))
    reject('zero contradiction margin', lambda: replay.evaluate({'weights': [['x', 1]], 'denominator': None}, {'x': ({'x': 1}, 0, 'le')}))
    badrec = deepcopy(packets['native_j1']['records'][0]); badrec['result']['e'] += 1
    badpacket = dict(packets['native_j1'], records=[badrec])
    reject('unproved fixed-label credit', lambda: replay.replay(badpacket))
    model.configure_planes({'free:33,1,0,0,0,74': [[0, 0, 0, 1, -1]]})
    reject('invalid endpoint majorant', lambda: model.check_planes('free', (33, 1, 0, 0, 0, 74)))
    badmanifest = deepcopy(manifest); badmanifest['files'][0]['sha256'] = '0' * 64
    reject('modified pinned source', lambda: validate(badmanifest))
    # Literal interval counterexample: a full pair-sum resource has only its
    # minimum at S. The correct leading upper endpoint has RHS +1, not -1.
    D = set(range(-37, 38)); pair = {a + b for a in D for b in D}
    S = sum(x for x in D if x > 0); lam = S + 74
    loss = len(pair) - sum(1 <= lam + x <= S for x in pair)
    endpoint = lam + len(pair) - S - 74 - loss
    need(endpoint == 1, 'Exact leading-upper boundary')
    reject('leading upper endpoint RHS minus one', lambda: need(endpoint <= -1, 'Wrong endpoint'))
    # Check the actual hole parameter at every supplied packet root. This is
    # a regression for accidental loop-variable shadowing in model.build.
    parameter_rows = 0
    p = packets['native_j1']; model.configure_planes(p['planes'])
    for w in range(0, 15, 2):
        rec = next(r for r in p['records'] if r['w'] == w and r['st']['Os'] == 1)
        _, rows, _ = model.build(rec['st'], 1, rec['r'], None, 0, w=w, forest_masks=[])
        rhs = {label: b for _, b, label in rows}
        need(rhs['raw O cap s'] == 12 + w // 2, 'Hole count must survive rank-kernel loop')
        need(rhs['leading upper s'] == 1, 'Leading upper convention')
        need(rhs['physical capacity s'] == 75 * sum(k[-1] == 's' and v == 1 for k, v in rec['st'].items()) + 84 + w // 2, 'Physical hole count')
        parameter_rows += 3
    reject('replace positive hole count by six', lambda: need(12 + 14 // 2 == 12 + 6 // 2, 'Shadowed hole count'))
    return dict(rejected=rejected, exact_parameter_rows=parameter_rows, leading_upper_boundary=endpoint)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--new-only', action='store_true', help='Skip prior replay; explicitly reports partial verification')
    args = parser.parse_args()
    need(sys.version_info >= (3, 10), 'Python 3.10 or later required')
    started = time.perf_counter(); manifest = validate(); initial_manifest_sha = sha(MANIFEST)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    detail = args.output.parent / (args.output.stem + '_details'); detail.mkdir(parents=True, exist_ok=True)
    results = {}; tasks = []
    def save(name, result, start):
        results[name] = result
        (detail / (name + '.json')).write_text(json.dumps(result, indent=2, ensure_ascii=False, default=str) + '\n', encoding='utf-8')
        tasks.append(dict(name=name, seconds=round(time.perf_counter() - start, 3)))
        print('PASS', name, flush=True)
    if not args.new_only:
        for name, path in [('baseline83', 'verification/upper83_complete/check.py'), ('alpha', 'verification/upper82_alpha/check.py')]:
            print('RUN', name, flush=True); start = time.perf_counter()
            dest = detail / (name + '.json'); log = detail / (name + '.log')
            command = [sys.executable, '-I', '-S', '-B', *(['-O'] if sys.flags.optimize else []), str(ROOT / path), '--output', str(dest.resolve())]
            with log.open('w', encoding='utf-8') as stream:
                proc = subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
            need(proc.returncode == 0, 'Prior replay failed; see ' + str(log))
            result = json.loads(dest.read_text())
            wanted = 'PASS_COMPLETE_FINITE_REPLAY' if name == 'baseline83' else 'PASS_CONDITIONAL_ALPHA_SIZE83_FINITE_CERTIFICATES'
            need(result['status'] == wanted, 'Prior status: ' + name)
            results[name] = result; tasks.append(dict(name=name, seconds=round(time.perf_counter() - start, 3), log_sha256=sha(log)))
            print('PASS', name, flush=True)
    packets, trees = load_packets()
    start = time.perf_counter(); save('coverage', dispatch(packets, trees), start)
    for name, module in [('structure', structure), ('geometry', geometry), ('compression', compression)]:
        print('RUN', name, flush=True); start = time.perf_counter(); save(name, module.verify(), start)
    packet_results = {}
    for name in PACKETS:
        print('RUN', name, len(packets[name]['records']), flush=True); start = time.perf_counter()
        result = replay.replay(packets[name]); packet_results[name] = result
        (detail / (name + '.json')).write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        tasks.append(dict(name=name, seconds=round(time.perf_counter() - start, 3)))
        print('PASS', name, result['integer_combinations'], flush=True)
    results['packets'] = packet_results
    start = time.perf_counter(); save('controls', controls(packets, trees, manifest), start)
    validate(); need(sha(MANIFEST) == initial_manifest_sha, 'Source manifest changed during replay')
    wanted = REQUIRED - ({'baseline83', 'alpha'} if args.new_only else set())
    need(set(results) == wanted, 'Incomplete replay inventory')
    finite = {name: results[name] for name in ('coverage', 'structure', 'geometry', 'compression', 'packets', 'controls')}
    previous = {} if args.new_only else {'baseline83': results['baseline83']['finite_digest'], 'alpha': results['alpha']['finite']['replay_sha256']}
    report = dict(schema='upper82-global-replay-v1', status='PASS_NEW_FINITE_CHECKS_ONLY' if args.new_only else 'PASS_COMPLETE_FINITE_REPLAY',
                  written_upper_bound=None if args.new_only else 82, formal_proof_assistant_verified=False,
                  scope='Exact finite dependencies and complete state dispatch; unbounded actual-set applicability is supplied by the companion proof.',
                  optimization=sys.flags.optimize, timestamp_utc=datetime.now(timezone.utc).isoformat(),
                  seconds=round(time.perf_counter() - started, 3), source_files=len(manifest['files']),
                  source_manifest_sha256=sha(MANIFEST), finite_digest=digest(finite), prior_finite_digests=previous,
                  coverage=results['coverage'], integer_combinations=sum(x['integer_combinations'] for x in packet_results.values()),
                  controls=results['controls'], tasks=tasks, detail_directory=str(detail.resolve()))
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(report['status'], report['finite_digest'], flush=True)


if __name__ == '__main__':
    main()
