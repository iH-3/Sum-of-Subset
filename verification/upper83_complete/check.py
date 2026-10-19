#!/usr/bin/env python3
"""Complete finite replay supporting the written N<=83 proof.
Standard library, Python3.10+. Infinite applicability is a written proof,
not a theorem proved by this executable or by checking a coverage flag.
"""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/'data/upper83_complete_sources.json'
REQUIRED={'baseline84','source_progress','fullrank','tail','structure','geometry','positive','local'}

def need(ok,msg):
    if not ok:raise ValueError(msg)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def validate(data=None):
    data=json.loads(MANIFEST.read_text()) if data is None else data
    need(data.get('schema')=='upper83-complete-sources-v1','manifest schema')
    need(set(data['required_checks'])==REQUIRED,'missing finite obligation')
    paths=set()
    for entry in data['files']:
        p=Path(entry['path'])
        need(not p.is_absolute() and '..' not in p.parts and entry['path'] not in paths,'source path')
        paths.add(entry['path']);need(sha(ROOT/p)==entry['sha256'],'source mismatch '+str(p))
    local={str(p.relative_to(ROOT)) for p in Path(__file__).parent.glob('*.py')}
    need(local<=paths,'new verifier omitted from source pins')
    for name in ('upper84_adoption','upper83_progress','upper83_fullrank','upper83_tail'):
        rel='data/'+name+'_sources.json'
        need(rel in paths,'dependency manifest omitted')
        old=json.loads((ROOT/rel).read_text())
        need({x['path'] for x in old['files']}<=paths,'transitive dependency omitted')
    return data

def load(name):
    p=Path(__file__).parent/(name+'.py')
    spec=importlib.util.spec_from_file_location('complete83_'+name,p)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def coverage(results):
    need(set(results)==REQUIRED,'incomplete replay inventory')
    need(results['baseline84']['status']=='PASS_ALL_REQUESTED_FINITE_CHECKS','baseline replay')
    for name in ('structure','geometry','positive'):need(results[name]['status']=='PASS','new '+name)
    need(results['local']['status']=='PASS_LOCAL_ARITHMETIC','local replay')
    need(results['fullrank']['status'].startswith('PASS'),'fullrank replay')
    need(results['source_progress']['status'].startswith('PASS'),'source replay')
    need(results['tail']['status'].startswith('PASS'),'tail replay')
    need(len(results['structure']['inverse_rows'])==20,'20 failed-test rows')
    need(results['positive']['seed_count']==6188,'all dense seeds')
    need(results['local']['low_prefix']['patterns']==59049,'complete low prefix')
    need(results['geometry']['Z5']['assignments']==2097152,'complete two-branch masks')
    need(len(results['positive']['P3'])==12 and len(results['positive']['P4'])==7,'all endpoint cards')
    return dict(zero_hole_j=list(range(7)),zero_j_above6='negative source budget',
                positive_low_j=list(range(6)),positive_j_at_least6='positive core mass',
                positive_high='all z>=15',structural_exceptions='AP, nonprimitive and a9..14',
                mathematical_licenses='Companion report and pinned proof notes; not inferred from Boolean enumeration.')

def controls(results,manifest):
    rejected=[]
    def reject(fn,label):
        try:fn()
        except (ValueError,KeyError,TypeError):rejected.append(label)
        else:raise ValueError('invalid mutation accepted '+label)
    altered=dict(results);altered.pop('structure')
    reject(lambda:coverage(altered),'omit size84 structure')
    altered2=deepcopy(results);altered2['positive']['P3'].pop()
    reject(lambda:coverage(altered2),'omit one heavy endpoint pattern')
    m=deepcopy(manifest);m['required_checks'].remove('tail')
    reject(lambda:validate(m),'omit exact C5t tail obligation')
    m2=deepcopy(manifest);m2['files'][0]['sha256']='0'*64
    reject(lambda:validate(m2),'change a pinned proof source')
    reject(lambda:need(192+2<2*91,'false both-AP uniform threshold'),'invalid AP threshold at a13')
    reject(lambda:need(151>156,'cross HIGH without ten fixed labels'),'omit ten HIGH labels in P4 chain')
    reject(lambda:need(11+18-17>=13,'inflated ledger'),'claim13 from P5 credit12 ledger')
    return rejected

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    need(sys.version_info>=(3,10),'Python3.10+')
    started=time.perf_counter();manifest=validate();args.output.parent.mkdir(parents=True,exist_ok=True)
    run=args.output.parent/(args.output.stem+'_details');run.mkdir(parents=True,exist_ok=True)
    results={};tasks=[]
    scripts=[('baseline84','verification/upper84_adoption.py'),('source_progress','verification/upper83_progress.py'),('fullrank','verification/upper83_fullrank/check.py'),('tail','verification/upper83_tail.py'),('local','verification/upper83_complete/check_local.py')]
    for name,script in scripts:
        print('RUN',name,flush=True);dest=run/(name+'.json');log=run/(name+'.log');t=time.perf_counter()
        command=[sys.executable,'-I','-S','-B',*(['-O'] if sys.flags.optimize else []),str(ROOT/script),'--output',str(dest.resolve())]
        with log.open('w') as f:ret=subprocess.run(command,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
        need(ret.returncode==0,'failed '+name+': '+str(log))
        results[name]=json.loads(dest.read_text());tasks.append(dict(name=name,seconds=round(time.perf_counter()-t,3),log_sha256=sha(log)))
    for name in ('structure','geometry','positive'):
        print('RUN',name,flush=True);t=time.perf_counter();results[name]=load('check_'+name).verify()
        (run/(name+'.json')).write_text(json.dumps(results[name],indent=2,default=str)+'\n')
        tasks.append(dict(name=name,seconds=round(time.perf_counter()-t,3)))
    cover=coverage(results);negative=controls(results,manifest);validate()
    # Stable digest excludes only timing and baseline environment receipts.
    finite={k:results[k] for k in ('structure','geometry','positive','local')}
    stable=json.dumps(finite,sort_keys=True,default=str,separators=(',',':'))
    report=dict(schema='upper83-complete-replay-v1',status='PASS_COMPLETE_FINITE_REPLAY',
                written_upper_bound=83,formal_proof_assistant_verified=False,
                scope='All finite dependencies and fresh checks replayed; infinite actual-set applicability is proved in the companion report.',
                optimization=sys.flags.optimize,timestamp_utc=datetime.now(timezone.utc).isoformat(),
                seconds=round(time.perf_counter()-started,3),source_files=len(manifest['files']),
                source_manifest_sha256=sha(MANIFEST),finite_digest=hashlib.sha256(stable.encode()).hexdigest(),
                coverage=cover,rejected_controls=negative,tasks=tasks,
                detail_directory=str(run.resolve()))
    args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(report['status'],report['finite_digest'],flush=True)

if __name__=='__main__':main()
