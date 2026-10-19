#!/usr/bin/env python3
"""Fresh complete size-87 finite replay, conditional on the written reductions.

Uses immutable archive certificates; requires unoptimized Python 3.10+.
Runs every ordinary root, all 22 supplemental components, all added finite
prerequisites, and the independently reconstructed strengthened c >= 32 lemma.
A clean output directory is mandatory. Saved success receipts are not inputs.
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
MANIFEST_SHA = '56ade7ee005f36b500f9b69deff830ae7222895778c1e05229ec229d2b343b37'
ARCHIVE_ROOT = 'subset_sums_upper86_complete_verification_20261005'
N = 1615300


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
        require(Path(part['name']).name == part['name'], 'Invalid part name')
        raw = (folder/part['name']).read_bytes()
        require(len(raw) == part['bytes'] and sha(raw) == part['sha256'],
                'Archive part differs: '+part['name'])
        chunks.append(raw)
    raw = b''.join(chunks)
    require(len(raw) == manifest['bytes'] and
            sha(raw) == manifest['sha256'] == ARCHIVE_SHA, 'Wrong archive')
    seen = set()
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for item in archive.infolist():
            if item.is_dir():
                continue
            name = item.filename
            path = PurePosixPath(name)
            require(path.parts[0] == ARCHIVE_ROOT and not path.is_absolute()
                    and '..' not in path.parts and '\\' not in name
                    and ':' not in name and name not in seen, 'Unsafe member')
            seen.add(name)
            target = destination.joinpath(*path.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(item))
    source = destination/ARCHIVE_ROOT
    endpoint = source/'payload/subset_sum_verification/proofs/exact86'
    require(sha((endpoint/'portable_manifest.json').read_bytes()) == MANIFEST_SHA,
            'Wrong endpoint manifest')
    return source, len(seen)


def replay(work, jobs):
    started = time.monotonic()
    require(not work.exists(), 'Use a fresh work directory')
    work.mkdir(parents=True)
    source, file_count = extract(work/'source')
    endpoint = source/'payload/subset_sum_verification/proofs/exact86'
    logs = work/'logs'
    logs.mkdir()
    receipts = work/'endpoint_receipts'
    py = [sys.executable, '-I', '-S', '-B', '-u', '-X', 'utf8']
    own = {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in
           (Path(__file__).resolve(), ROOT/'verification/upper86_geometry.py')}

    def execute(name, script, args=(), marker=None):
        before = time.monotonic()
        command = py+[str(script), *map(str,args)]
        path = logs/(name+'.log')
        with path.open('wb') as stream:
            code = subprocess.run(command, cwd=script.parent,
                                  stdout=stream, stderr=subprocess.STDOUT).returncode
        raw = path.read_bytes()
        rec = dict(name=name, command=command, returncode=code,
                   seconds=round(time.monotonic()-before,3), log_sha256=sha(raw),
                   marker=marker, marker_present=marker is None or marker.encode() in raw)
        (logs/(name+'.receipt.json')).write_text(json.dumps(rec,indent=2)+'\n')
        print(name, 'exit',code,'marker',rec['marker_present'],flush=True)
        require(code == 0 and rec['marker_present'], 'Failed stage: '+name)
        return rec

    integrity = source/'verify_complete_upper86.py'
    initial = execute('initial_integrity', integrity,
                      ['--integrity-only','--output-parent',work/'initial'],
                      'INTEGRITY ONLY PASSED.')
    intervals = [(N*i//jobs,N*(i+1)//jobs) for i in range(jobs)]
    controller = endpoint/'controller.py'
    prefix = ['--expected-manifest',MANIFEST_SHA]
    apbase = source/'payload/subset_sum_verification/proofs/exact92'
    tasks = [('apfree_base',apbase/'verify_apfree_blocks.py',[],
              'PASS: exact AP-free maxima through 30')]
    for length,bound in [(35,13),(39,14),(50,16),(70,20)]:
        tasks.append(('apfree_'+str(length),apbase/'verify_bounded_ap.py',
                      [length,bound],f'PASS r3({length})<={bound}'))
    for i,(lo,hi) in enumerate(intervals):
        tasks.append(('ordinary_'+str(i),controller,prefix+['range','--start',lo,
                      '--stop',hi,'--receipts',receipts],f'PASS ordinary-{lo:07d}-{hi:07d}'))
    for i in range(22):
        tasks.append((f'supplement_{i:02}',controller,prefix+['supplement',
                      '--component',i,'--receipts',receipts],f'PASS supplement-{i:02d}'))
    tasks.insert(0,('auxiliary',integrity,['--auxiliary-only','--output-parent',work/'auxiliary'],
                    'PARTIAL AUXILIARY CHECKS PASSED.'))
    tasks.append(('report_arithmetic', source/'payload/subset_sum_verification/report/verify_report86_arithmetic.py',[],
                  'PASS all 35 five-point profiles'))
    tasks.append(('new_geometry',ROOT/'verification/upper86_geometry.py',
                  ['--output',work/'geometry.json'],'PASS_STRENGTHENED_ANALYTIC_AND_GEOMETRY'))
    records = []
    with ThreadPoolExecutor(max_workers=jobs+1) as executor:
        pending = [executor.submit(execute,*task) for task in tasks]
        for future in as_completed(pending):
            records.append(future.result())
    assembled = execute('assemble',controller,prefix+['assemble','--receipts',receipts],
                        '"fresh_complete_ordinary_arithmetic": true')
    union = json.loads((receipts/'complete_union.json').read_text())
    require(union['verified'] is True and union['fresh_complete_ordinary_arithmetic'] is True
            and union['root_interval']==[0,N], 'Incomplete endpoint union')
    require([(r['start'],r['stop']) for r in union['ordinary_ranges']]==intervals,
            'Unexpected range partition')
    expected = dict(original_roots=N,ordinary_leaves=1614434,supplemental_parents=866,
                    supplemental_children=1042,supplemental_splits=10163,
                    supplemental_leaves=11205,total_leaves=1625639)
    require(all(union['counts'][k]==v for k,v in expected.items()), 'Wrong census')
    final = execute('final_integrity',integrity,
                    ['--integrity-only','--output-parent',work/'final'],'INTEGRITY ONLY PASSED.')
    require(all(sha((ROOT/p).read_bytes())==h for p,h in own.items()),
            'New verifier source changed during replay')
    return dict(status='PASS_COMPLETE_ENDPOINT_FINITE_REPLAY',
                mathematical_adoption='reports/upper86_adoption_20261019.tex',
                prior_independent_upper_bound=87,conditional_result=86,
                proof_assistant_formalization=False,archive_sha256=ARCHIVE_SHA,
                portable_manifest_sha256=MANIFEST_SHA,extracted_files=file_count,
                source_sha256=own,counts=expected,union=union,
                initial_integrity=initial,final_integrity=final,assembly=assembled,
                records=sorted(records,key=lambda r:r['name']),
                seconds=round(time.monotonic()-started,3))


def main():
    require(__debug__, 'Run without -O: archived assertions must remain enabled')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=4)
    parser.add_argument('--work-dir',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    require(1<=args.jobs<=32,'jobs must be between 1 and 32')
    if args.work_dir:
        result = replay(args.work_dir.resolve(),args.jobs)
    else:
        with tempfile.TemporaryDirectory(prefix='upper86-') as temp:
            result = replay(Path(temp)/'replay',args.jobs)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'], 'original roots',N,flush=True)


if __name__=='__main__':
    main()
