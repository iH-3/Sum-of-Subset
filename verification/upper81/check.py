#!/usr/bin/env python3
"""Exact finite replay for the companion size82 exclusion proof.

Python 3.10+; standard library only. Actual-set applicability is supplied by
 the written proof, not by a proof assistant or floating-point solver.
"""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import argparse,gzip,hashlib,json,subprocess,sys,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
import model as m,exact,parametric as p,coverage,geometry,structure,low_c
MANIFEST=ROOT/'data/upper81_sources.json'
REQUIRED={'baseline82','repairs','structure','geometry','low_c','coverage','controls'}


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()


def validate(data=None):
    data=json.loads(MANIFEST.read_text()) if data is None else data
    m.need(data.get('schema')=='upper81-sources-v1' and set(data['required_checks'])==REQUIRED,'Source obligations')
    pinned={}
    for item in data['files']:
        name=item['path'];path=Path(name)
        m.need(not path.is_absolute() and '..' not in path.parts and name not in pinned,'Pinned source path')
        m.need(sha(ROOT/path)==item['sha256'],'Source mismatch: '+name);pinned[name]=item['sha256']
    previous=json.loads((ROOT/'data/upper82_global_sources.json').read_text())
    m.need(pinned.get('data/upper82_global_sources.json')==sha(ROOT/'data/upper82_global_sources.json'),'Missing prior source manifest')
    m.need(all(pinned.get(x['path'])==x['sha256'] for x in previous['files']),'Missing transitive baseline dependency')
    repair_path='verification/upper81/repairs/repair_manifest.json'
    m.need(pinned.get(repair_path)==sha(ROOT/repair_path),'Missing repair manifest')
    repairs=json.loads((ROOT/repair_path).read_text())
    m.need(all(pinned.get(name)==value for name,value in repairs['repository_files'].items()),'Missing repair dependency')
    m.need(all(pinned.get('verification/upper81/repairs/'+name)==value for name,value in repairs['package_files'].items()),'Missing repair component')
    for name in ('check.py','coverage.py','model.py','parametric.py','exact.py','structure.py','geometry.py','low_c.py','README.md','run_windows.bat'):
        m.need('verification/upper81/'+name in pinned,'Unpinned verifier component: '+name)
    for name in ('data/upper81_certificates.json.gz','data/upper81_low_c.json','reports/upper81_complete_20261021.tex','reports/upper81_complete_20261021.pdf'):
        m.need(name in pinned,'Unpinned proof artifact: '+name)
    return data


def controls(manifest):
    rejected=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,KeyError,TypeError,IndexError):rejected.append(label)
        else:raise ValueError('Invalid mutation accepted: '+label)
    packet=coverage.load_packet()
    bad=dict(packet,records=packet['records'][1:]);reject('missing root',lambda:coverage.inventory(bad))
    bad=dict(packet,records=packet['records']+[packet['records'][0]]);reject('repeated root',lambda:coverage.inventory(bad))
    if packet['branches']:
        tree=next((r for r in packet['branches'] if 'right' in r['tree']),None)
        m.need(tree is not None,'Expected a complementary branch')
        bad=dict(tree,tree=dict(tree['tree']));bad['tree'].pop('right')
        reject('missing complementary branch',lambda:coverage.branch(bad))
    reject('negative multiplier',lambda:exact.check({'weights':[('r',0,-1)],'denominator':None},[({'x':1},-1,'row')],[]))
    reject('negative residual',lambda:exact.check({'weights':[('r',0,1)],'denominator':None},[({'x':-1},-1,'row')],[]))
    reject('zero contradiction',lambda:exact.check({'weights':[('r',0,1)],'denominator':None},[({'x':1},0,'row')],[]))
    rec=deepcopy(packet['records'][0]);rec['trace']=[dict(kind='credit',e=999)]+rec['trace']
    reject('unproved fixed credit',lambda:exact.replay(rec))
    p.PLANE_TABLE={'32,1,0,0,0,73':[[0,0,0,1,-1]]};p.PLANE_GENERATOR=None;p.CHECKED_PLANES.clear()
    reject('invalid endpoint plane',lambda:p.majorants(32,1,0,0,73,False,0))
    bad=deepcopy(manifest);bad['files'][0]['sha256']='0'*64
    reject('modified proof source',lambda:validate(bad))
    D=set(range(-36,38));DD={a+b for a in D for b in D};S=sum(x for x in D if x>0);lam=S+72
    loss=len(DD)-sum(1<=lam+x<=S for x in DD)
    m.need(lam+len(DD)-S-72-loss==1,'Leading upper endpoint must retain +1')
    reject('leading endpoint minus one',lambda:m.need(lam+len(DD)-S-72-loss<=-1,'Wrong endpoint'))
    return dict(rejected=rejected,leading_upper_boundary=1)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--new-only',action='store_true',help='Explicitly reports partial verification; skips the prior global bound')
    args=ap.parse_args();m.need(sys.version_info>=(3,10),'Python 3.10+ required')
    started=time.perf_counter();manifest=validate();manifest_sha=sha(MANIFEST)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    detail=args.output.parent/(args.output.stem+'_details');detail.mkdir(parents=True,exist_ok=True)
    results={};tasks=[]
    def run_external(name,relative,extra=()):
        begin=time.perf_counter();destination=detail/(name+'.json');log=detail/(name+'.log')
        cmd=[sys.executable,'-I','-S','-B',*(['-O'] if sys.flags.optimize else []),str(ROOT/relative),*extra,'--output',str(destination.resolve())]
        print('RUN',name,flush=True)
        with log.open('w',encoding='utf-8') as stream:proc=subprocess.run(cmd,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
        m.need(proc.returncode==0,'Failed '+name+'; see '+str(log))
        result=json.loads(destination.read_text());expected='PASS_COMPLETE_FINITE_REPLAY' if name=='baseline82' else 'PASS_TARGETED_PROOF_REPAIRS'
        m.need(result['status']==expected,'Unexpected prior verification status')
        results[name]=result;tasks.append(dict(name=name,seconds=round(time.perf_counter()-begin,3)));print('PASS',name,flush=True)
    if not args.new_only:run_external('baseline82','verification/upper82_global/check.py')
    run_external('repairs','verification/upper81/repairs/check_repairs.py',('--repo',str(ROOT)))
    for name,fn in [('structure',structure.verify),('geometry',geometry.verify),('low_c',low_c.verify),('coverage',lambda:coverage.verify(verbose=True)),('controls',lambda:controls(manifest))]:
        print('RUN',name,flush=True);begin=time.perf_counter();result=fn();results[name]=result
        (detail/(name+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
        tasks.append(dict(name=name,seconds=round(time.perf_counter()-begin,3)));print('PASS',name,flush=True)
    m.need(set(results)==REQUIRED-({'baseline82'} if args.new_only else set()),'Incomplete verification inventory')
    validate();m.need(sha(MANIFEST)==manifest_sha,'Sources changed during verification')
    finite={k:results[k] for k in sorted(REQUIRED-{'baseline82'})}
    # Runtime and output locations are excluded from the finite digest.
    result=dict(schema='upper81-replay-v1',status='PASS_NEW_FINITE_CHECKS_ONLY' if args.new_only else 'PASS_COMPLETE_FINITE_REPLAY',
                written_upper_bound=None if args.new_only else 81,formal_proof_assistant_verified=False,
                finite_digest=digest(finite),baseline_finite_digest=None if args.new_only else results['baseline82']['finite_digest'],
                source_manifest_sha256=manifest_sha,source_files=len(manifest['files']),optimization=sys.flags.optimize,
                timestamp_utc=datetime.now(timezone.utc).isoformat(),seconds=round(time.perf_counter()-started,3),
                coverage=results['coverage'],controls=results['controls'],tasks=tasks)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(result['status'],result['finite_digest'],flush=True)
if __name__=='__main__':main()
