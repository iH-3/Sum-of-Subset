#!/usr/bin/env python3
"""Fresh compositional replay of the archived 19 stages and added prerequisites.

The archive is immutable. Only its documented range/partial interfaces are used.
Partial results are never promoted until every required range and stage passes.
This supplies finite premises only, not the universal mathematical reductions.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--jobs', type=int, default=8)
    args = parser.parse_args()
    source, out = args.source.resolve(), args.output_dir.resolve()
    need(not out.exists(), 'Use a fresh output directory; old receipts are not reused')
    out.mkdir(parents=True)
    payload = source/'payload/subset_sum_verification'
    pin = json.loads((payload/'ENDPOINT86_LAUNCH.json').read_text())['manifest_sha256']
    endpoint = payload/'proofs/exact86'
    size88 = payload/'proofs/exact87'
    py = [sys.executable, '-I', '-S', '-B', '-u']
    tasks = []
    # Start the longest unchanged endpoint first. Stages 15 and 16 are sizes
    # 89 and 88 respectively; archived bound names are one smaller.
    for number in [15] + list(range(1,15)) + [17,18]:
        tasks.append((f'stage_{number:02}', py+[str(payload/'verify_all.py'),
                      '--steps', str(number), '--report', str(out/f'stage_{number:02}.report')],
                      f'SELECTED CHECKS PASSED: stages [{number}]'))
    tasks.insert(1, ('stage_16_supplements', py+[str(size88/'verify_exact87.py'),
                    '--supplements-and-union-only'], 'PARTIAL ONLY:'))
    ranges88 = [(1128280*i//4,1128280*(i+1)//4) for i in range(4)]
    for i,(lo,hi) in enumerate(ranges88):
        tasks.insert(2+i, (f'stage_16_range_{i}', py+[str(size88/'frozen_runner.py'),
                     'verify_compact_ordinary.py', '--start', str(lo), '--stop', str(hi)], None))
    receipts = out/'endpoint87_receipts'
    controller = py+[str(endpoint/'controller.py'), '--expected-manifest', pin]
    for i in range(8):
        lo,hi=1615300*i//8,1615300*(i+1)//8
        tasks.insert(6+i, (f'stage_19_range_{i}',controller+['range','--start',str(lo),
                    '--stop',str(hi),'--receipts',str(receipts)],f'PASS ordinary-{lo:07d}-{hi:07d}'))
    for i in range(22):
        tasks.append((f'stage_19_supplement_{i:02}',controller+['supplement','--component',
                      str(i),'--receipts',str(receipts)],f'PASS supplement-{i:02d}'))
    tasks.append(('auxiliary',py+[str(source/'verify_complete_upper86.py'),
                  '--auxiliary-only','--output-parent',str(out/'auxiliary_runs')],
                  'PARTIAL AUXILIARY CHECKS PASSED.'))

    def execute(task):
        name,command,expected=task
        start=time.monotonic()
        log=out/(name+'.log')
        with log.open('wb') as stream:
            code=subprocess.run(command,cwd=size88 if name.startswith('stage_16') else source,
                                stdout=stream,stderr=subprocess.STDOUT).returncode
        raw=log.read_bytes()
        result=dict(name=name,command=command,returncode=code,
                    seconds=round(time.monotonic()-start,3),log_sha256=hashlib.sha256(raw).hexdigest(),
                    expected_marker=expected,marker_present=expected is None or expected.encode() in raw)
        (out/(name+'.receipt.json')).write_text(json.dumps(result,indent=2)+'\n')
        print(name, 'exit', code, 'marker', result['marker_present'], flush=True)
        return result

    initial=execute(('initial_integrity',py+[str(source/'verify_complete_upper86.py'),
                     '--integrity-only','--output-parent',str(out/'initial_inventory')],
                     'INTEGRITY ONLY PASSED.'))
    need(initial['returncode']==0 and initial['marker_present'],'Initial archive inventory failed')
    records=[]
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures=[executor.submit(execute,t) for t in tasks]
        for future in as_completed(futures):
            records.append(future.result())
    complete=all(r['returncode']==0 and r['marker_present'] for r in records)
    ranges=[]
    if complete:
        for i,(lo,hi) in enumerate(ranges88):
            lines=(out/f'stage_16_range_{i}.log').read_text().splitlines()
            r=json.loads(next(line for line in reversed(lines) if line.startswith('{')))
            need(r['verified'] is True and r['range_start']==lo and r['range_stop_exclusive']==hi,
                 'Size-88 range does not match requested partition')
            ranges.append(r)
        for key in ('compact_sha256','source_bundle_sha256','canonical_manifest_sha256'):
            need(len({r[key] for r in ranges})==1,'Range source identity mismatch')
        need(sum(r['checked_counts'].get('certified',0) for r in ranges)==1127649,
             'Size-88 ordinary coverage incomplete')
        need(sum(r['checked_counts'].get('supplemental',0) for r in ranges)==631,
             'Size-88 supplemental parent count mismatch')
        assembled=execute(('stage_19_assemble',controller+['assemble','--receipts',str(receipts)],
                           '"fresh_complete_ordinary_arithmetic": true'))
        records.append(assembled)
        complete &= assembled['returncode']==0 and assembled['marker_present']
    final=execute(('final_integrity',py+[str(source/'verify_complete_upper86.py'),
                   '--integrity-only','--output-parent',str(out/'final_inventory')],
                   'INTEGRITY ONLY PASSED.'))
    complete &= final['returncode']==0 and final['marker_present']
    summary=dict(status='PASS_FINITE_COMPOSITION_ONLY' if complete else 'FAIL',
                 complete_finite_replay=complete,analytic_proof_formalization=False,
                 execution='Fresh parallel composition; not one default serial invocation',
                 stage_16_ranges=ranges,initial_integrity=initial,final_integrity=final,
                 records=sorted(records,key=lambda r:r['name']))
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return 0 if complete else 1


if __name__=='__main__':
    raise SystemExit(main())
