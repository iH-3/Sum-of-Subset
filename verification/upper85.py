#!/usr/bin/env python3
"""Replay all upper-85 finite obligations and the new analytic checks offline.

The written applicability proofs remain mathematical inputs. A PASS does not
mean proof-assistant formal verification. Python 3.10+, standard library only.
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
MANIFEST=ROOT/'data/upper85_adoption_sources.json'


def need(ok,message):
    if not ok:raise ValueError(message)


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(manifest):
    need(manifest.get('schema')=='upper85-adoption-sources-v1','manifest schema')
    paths=set()
    for entry in manifest['files']:
        relative=Path(entry['path'])
        need(not relative.is_absolute() and '..' not in relative.parts,'unsafe source path')
        need(entry['path'] not in paths,'duplicate source path')
        paths.add(entry['path'])
        path=ROOT/relative
        need(path.is_file() and sha(path)==entry['sha256'],'source mismatch: '+entry['path'])
    need('verification/upper85_geometry.py' in paths,'new mathematical checks omitted')
    return paths


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--work-dir',type=Path,help='parent of a fresh isolated replay directory')
    args=p.parse_args();started=time.perf_counter()
    need(sys.version_info>=(3,10),'Python 3.10 or later required')
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
    paths=validate(manifest)
    if args.work_dir:args.work_dir.mkdir(parents=True,exist_ok=True)
    work=Path(tempfile.mkdtemp(prefix='upper85-',dir=args.work_dir))
    for rel in sorted(paths):
        target=work/'source'/rel;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/rel,target)
        need(sha(target)==sha(ROOT/rel),'copy mismatch')
    source=work/'source'
    suite=source/'verification/upper84/audit/verification_program'
    flags=['-I','-S','-B']+(['-O'] if sys.flags.optimize else [])
    # -I removes script-directory imports. Add exactly the frozen suite path.
    code="import runpy,sys; sys.path.insert(0,sys.argv.pop(1)); sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0],run_name='__main__')"
    commands=[('full_suite',[sys.executable,*flags,'-c',code,str(suite),str(suite/'verify.py'),
                            '--full','--output-dir',str(work/'full')]),
              ('new_geometry',[sys.executable,*flags,str(source/'verification/upper85_geometry.py'),
                               '--output',str(work/'geometry.json')])]
    tasks=[]
    for name,cmd in commands:
        began=time.perf_counter();log=work/(name+'.log')
        print('RUN',name,flush=True)
        with log.open('w',encoding='utf-8') as handle:
            result=subprocess.run(cmd,cwd=work,stdout=handle,stderr=subprocess.STDOUT,check=False)
        tasks.append(dict(name=name,command=cmd,exit_code=result.returncode,
                          seconds=round(time.perf_counter()-began,3),log_sha256=sha(log)))
        need(result.returncode==0,'replay failed; inspect '+str(log))
    full=json.loads((work/'full/coverage.json').read_text())
    need(full['mode']=='full' and full['counts']=={'PASS':140,'FAIL':0,'SKIP':0},'full coverage count')
    ids=[c['id'] for c in full['checks']]
    need(len(set(ids))==140 and sorted(ids)==manifest['required_suite_check_ids'],'required check inventory')
    need(all(c['status']=='PASS' for c in full['checks']),'nonpassing finite obligation')
    geometry=json.loads((work/'geometry.json').read_text())
    need(geometry['status']=='PASS_NEW_ANALYTIC_LEMMAS_AND_CLASSIFICATIONS','new checks not complete')
    # Recheck original and copied inputs after execution; receipts are never inputs.
    validate(manifest)
    for entry in manifest['files']:
        need(sha(source/entry['path'])==entry['sha256'],'copied source changed during execution')
    report=dict(schema='upper85-full-replay-v1',status='PASS_ALL_REQUESTED_FINITE_CHECKS',
                timestamp_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),
                platform=platform.platform(),optimization=sys.flags.optimize,
                seconds=round(time.perf_counter()-started,3),work_dir=str(work),tasks=tasks,
                source_files=len(paths),source_manifest_sha256=sha(MANIFEST),
                suite_counts=full['counts'],geometry=geometry,
                full_theorem_formally_verified=False,
                mathematical_scope='Complete stated finite checks. General theorems, source geometry, and exhaustive analytic reductions are written proofs in the adoption report and pinned sources.',
                old_152_systems='Replayed as a regression check; the new no-empty-unit lemma removes this certificate dependency from the structural proof.')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(report['status'],flush=True)


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError) as err:
        print('FAIL:',err,file=sys.stderr)
        sys.exit(1)
