#!/usr/bin/env python3
"""Replay upper-84 finite obligations from frozen sources in a fresh directory.

Written applicability and infinite mathematical inputs remain proofs, not
executable conclusions. Legacy checks always retain assertions, even when
this launcher is invoked with -O. Python 3.10+, standard library only.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'data/upper84_adoption_sources.json'
LEGACY='verification/upper84/'


def need(ok,message):
    if not ok:raise ValueError(message)


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(manifest,root=ROOT):
    need(manifest.get('schema')=='upper84-adoption-sources-v1','manifest schema')
    paths=set()
    for entry in manifest['files']:
        rel=Path(entry['path'])
        need(not rel.is_absolute() and '..' not in rel.parts,'unsafe source path')
        need(entry['path'] not in paths,'duplicate source path')
        paths.add(entry['path'])
        p=root/rel
        need(p.is_file() and sha(p)==entry['sha256'],'source mismatch: '+entry['path'])
    need('verification/upper84_geometry.py' in paths,'new geometry omitted')
    archive=json.loads((root/(LEGACY+'COVERAGE85.json')).read_text(encoding='utf-8'))
    need(set(LEGACY+p for p in archive['sha256']) <= paths,'legacy source omitted')
    need(LEGACY+'verify84.py' in paths and LEGACY+'COVERAGE85.json' in paths,'legacy entry omitted')
    return paths


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--work-dir',type=Path,help='parent of a new isolated replay directory')
    args=parser.parse_args();started=time.perf_counter()
    need(sys.version_info>=(3,10),'Python 3.10 or later required')
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8'));paths=validate(manifest)
    if args.work_dir:args.work_dir.mkdir(parents=True,exist_ok=True)
    work=Path(tempfile.mkdtemp(prefix='upper84-',dir=args.work_dir));source=work/'source'
    for rel in sorted(paths):
        target=source/rel;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/rel,target)
        need(sha(target)==sha(ROOT/rel),'source copy mismatch')
    old=source/LEGACY
    flags=['-I','-S','-B']
    commands=[('legacy_full',[sys.executable,*flags,str(old/'verify84.py'),'--full']),
              ('new_geometry',[sys.executable,*flags,*(['-O'] if sys.flags.optimize else []),
                               str(source/'verification/upper84_geometry.py'),'--output',str(work/'geometry.json')])]
    tasks=[]
    for name,cmd in commands:
        began=time.perf_counter();log=work/(name+'.log')
        print('RUN',name,flush=True)
        with log.open('w',encoding='utf-8') as handle:
            result=subprocess.run(cmd,cwd=work,stdout=handle,stderr=subprocess.STDOUT,check=False)
        tasks.append(dict(name=name,command=cmd,returncode=result.returncode,
                          seconds=round(time.perf_counter()-began,3),log_sha256=sha(log)))
        need(result.returncode==0,'replay failed: '+str(log))
    old_results=old/'verification_results'
    suites=json.loads((old_results/'summary.json').read_text())
    need(suites['status']=='PASS' and suites['finite_checks_passed']==11 and
         suites['finite_checks_requested']==11 and suites['full_retained_replay'],'incomplete legacy suites')
    need([r['name'] for r in suites['results']]==manifest['required_suite_names'],'suite inventory changed')
    full=json.loads((old_results/'retained_full/coverage.json').read_text())
    need(full['counts']=={'PASS':140,'FAIL':0,'SKIP':0},'retained full coverage')
    ids=[c['id'] for c in full['checks']]
    need(len(set(ids))==140 and sorted(ids)==manifest['required_retained_check_ids'],'retained check inventory')
    need(all(c['status']=='PASS' for c in full['checks']),'nonpassing retained check')
    zero=json.loads((old/'progress85/zero/check_zero_cards85_results.json').read_text())
    children=zero['standalone_checks']
    need(len(children)==7 and sorted(c['path'] for c in children)==manifest['required_aggregate_paths']
         and all(c['status']=='PASS' for c in children),'aggregate child inventory')
    geometry=json.loads((work/'geometry.json').read_text())
    need(geometry['status']=='PASS_NEW_ANALYTIC_CHECKS','new checks incomplete')
    validate(manifest)
    for entry in manifest['files']:
        need(sha(source/entry['path'])==entry['sha256'],'copied input changed: '+entry['path'])
    report=dict(schema='upper84-adoption-replay-v1',status='PASS_ALL_REQUESTED_FINITE_CHECKS',
                timestamp_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),
                platform=platform.platform(),optimization=sys.flags.optimize,
                legacy_assertions_enabled=True,seconds=round(time.perf_counter()-started,3),
                work_dir=str(work),tasks=tasks,source_files=len(paths),
                source_manifest_sha256=sha(MANIFEST),legacy_suites_passed=11,
                fresh_legacy_modules=17,aggregate_children=7,retained_counts=full['counts'],
                geometry=geometry,full_theorem_formally_verified=False,
                mathematical_scope='Written structure, activity, resource and infinite proofs plus the complete stated finite checks. The old 7315-state alpha enumeration is retained only as a regression check.')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(report['status'],flush=True)


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError) as exc:
        raise SystemExit('FAIL: '+str(exc))
