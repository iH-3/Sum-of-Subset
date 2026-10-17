#!/usr/bin/env python3
"""Run every upper-89 numerical cross-check in independent standard-library batches.

The per-group checks below mirror upper89.check_coverage(..., exhaustive=True).
Only global coverage and used-vector checks move to the parent aggregator.
The complete merged result must equal the standard result except for its mode.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import datetime

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verification'))
import upper89 as proof
require=proof.require
base=proof.base
model=proof.model
Quadratic=proof.Quadratic
interval_certificate=proof.interval_certificate
row_policy=proof.row_policy
extend_rows=proof.extend_rows
branches=proof.branches


def digest(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, data):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(data,default=base.json_default,indent=2)+'\n')
    temporary.replace(path)


def fingerprint(reference):
    hashes={str(k):digest((ROOT/k).read_bytes()) for k in reference['sha256']}
    require(hashes==reference['sha256'],'Reference proof inputs changed')
    hashes[str(Path(__file__).relative_to(ROOT))]=digest(Path(__file__).read_bytes())
    return hashes


def check_groups(groups, routing, pool):
    exhaustive=True
    counts=Counter();root_counts=Counter();details={};used=set();gaps=[];split_types=Counter()
    for g in groups:root_counts[g['regime']]+=g['hi']-g['lo']+1

    max_depth=0
    def weight(index):
        require(type(index) is int and 0<=index<len(pool),'Invalid certificate index')
        used.add(index);return pool[index]
    def tree_check(g,a,n,r,node,available,path=(),depth=0):
        nonlocal max_depth
        max_depth=max(max_depth,depth)
        require(isinstance(node,dict),'Malformed tree')
        if set(node)=={'vector'}:
            result=base.check_integer_certificate(n,r,weight(node['vector']))
            gaps.append(result['normalized_gap']);counts['tree_leaves']+=1
            return dict(vector=node['vector'],normalized_gap=result['normalized_gap'])
        require(set(node)=={'split','children'} and isinstance(node['children'],list) and len(node['children'])==2,'Both children required')
        split=node['split'];require(split in available and split not in path,'Invalid or repeated disjunction')
        parts=available[split]
        counts['binary_splits']+=1;split_types[split.split(':')[0]]+=1
        kids=[]
        for side,extra in enumerate(parts):
            rr=extend_rows(r,split,side,extra)
            kids.append(tree_check(g,a,n,rr,node['children'][side],available,path+(split,),depth+1))
        return dict(split=split,children=kids)
    def leaf(g,node,allowed):
        require(set(node)=={'kind','segments','trees'} and node['kind'] in allowed,'Invalid leaf model')
        kind=node['kind'];n,r=model(g,Quadratic(0,1),kind);covered=set();segments=[];tree_results={}
        require(isinstance(node['segments'],list) and isinstance(node['trees'],dict),'Malformed leaf coverage')
        last=g['lo']-1
        for item in node['segments']:
            require(isinstance(item,list) and len(item)==3 and all(type(x) is int for x in item),'Malformed interval')
            lo,hi,index=item;require(g['lo']<=lo<=hi<=g['hi'] and lo>last,'Invalid interval order')
            points=set(range(lo,hi+1));require(not covered&points,'Overlapping intervals');covered|=points;last=hi
            result=interval_certificate(n,r,weight(index),lo,hi)
            counts['interval_checks']+=1;counts['extremum_points']+=result['extremum_points'];gaps.append(result['normalized_gap'])
            segments.append(dict(first=lo,last=hi,vector=index,**result))
            if exhaustive:
                point_gaps=[]
                for a in range(lo,hi+1):
                    nn,rr=model(g,a,kind)
                    require(nn==n and set(rr)==set(r),'Symbolic/numeric matrix shape differs')
                    for label,(v,b) in r.items():
                        require(rr[label][0]==v and rr[label][1]==Quadratic.coerce(b).at(a),'Symbolic/numeric formula differs')
                    point_gaps.append(base.check_integer_certificate(nn,rr,pool[index])['normalized_gap'])
                require(min(point_gaps)==result['normalized_gap'],'Wrong interval maximum')
        for key,node_tree in node['trees'].items():
            require(key==str(int(key)),'Noncanonical integer parameter')
            a=int(key);require(g['lo']<=a<=g['hi'] and a not in covered,'Duplicate or out-of-range tree')
            require(kind.endswith('_nested'),'Tree uses unsupported coarse coordinates')
            covered.add(a);counts['tree_roots']+=1
            nn,rr=model(g,a,kind)
            if exhaustive:
                require(nn==n and set(rr)==set(r),'Tree base matrix differs')
                for label,(v,b) in r.items():
                    require(rr[label][0]==v and rr[label][1]==Quadratic.coerce(b).at(a),'Tree base formula differs')
            tree_results[key]=tree_check(g,a,nn,rr,node_tree,branches(g,a,nn))
        require(covered==set(range(g['lo'],g['hi']+1)),'Missing integer parameter')
        counts['parameter_systems']+=len(covered);counts['leaf_groups']+=1;counts['kind/'+kind]+=1
        return dict(kind=kind,lo=g['lo'],hi=g['hi'],policy=row_policy(g),variables=len(n),rows=len(r),segments=segments,trees=tree_results)
    for g in groups:
        node=routing[g['key']];kind=node.get('kind');counts['route/'+str(kind)]+=1
        details[g['key']]=leaf(g,node,('coarse','global_nested'))
    require(counts['tree_leaves']==counts['tree_roots']+counts['binary_splits'],'Broken binary tree identity')
    return dict(root_groups=len(groups),root_systems=sum(root_counts.values()),root_counts=dict(root_counts),
                counts=dict(counts),certified_systems=counts['parameter_systems']+counts['binary_splits'],
                vectors=len(pool),maximum_tree_depth=max_depth,split_types=dict(split_types),
                minimum_normalized_gap=min(gaps),proof_checks=details,used_vectors=sorted(used))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference',type=Path,required=True,help='Completed symbolic output from verification/upper89.py')
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--work-dir',type=Path,required=True)
    parser.add_argument('--receipt',type=Path,required=True)
    parser.add_argument('--jobs',type=int,default=4)
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--worker',type=int,default=None,help=argparse.SUPPRESS)
    args=parser.parse_args()
    require(1<=args.jobs<=32,'Use between 1 and 32 batches')
    reference=json.loads(args.reference.read_text())
    require(reference['summary']['status']=='PASS' and reference['summary']['verification_mode']=='symbolic-interval','A successful symbolic reference is required')
    hashes=fingerprint(reference)
    hashes['reference_output_sha256']=digest(args.reference.read_bytes())
    bundle=json.loads(proof.DEFAULT_CERTIFICATE.read_text())
    require(bundle['format']==proof.FORMAT,'Wrong certificate format')
    groups=list(proof.roots())
    require(len({g['key'] for g in groups})==len(groups),'Duplicate reconstructed roots')
    require(set(bundle['roots'])=={g['key'] for g in groups},'Incomplete root universe')
    expected_counts=Counter()
    for g in groups:expected_counts[g['regime']]+=g['hi']-g['lo']+1
    require({k:v for k,v in expected_counts.items() if k[0]!='H'}==proof.LOW_COUNTS,'Wrong low root universe')
    args.work_dir.mkdir(parents=True,exist_ok=True)
    if args.worker is not None:
        require(0<=args.worker<args.jobs,'Invalid batch')
        selected=groups[args.worker::args.jobs]
        checked=check_groups(selected,bundle['roots'],bundle['pool'])
        require(fingerprint(reference)=={k:v for k,v in hashes.items() if k!='reference_output_sha256'},'Proof source changed during a batch')
        result=dict(status='PASS',part=args.worker,parts=args.jobs,input_sha256=hashes,
                    group_keys_sha256=digest(json.dumps([g['key'] for g in selected]).encode()),checked=checked)
        dump(args.work_dir/f'part-{args.worker}.json',result)
        return

    started=datetime.datetime.now(datetime.timezone.utc).isoformat();clock=time.monotonic()
    def run_part(part):
        path=args.work_dir/f'part-{part}.json';receipt=args.work_dir/f'part-{part}-receipt.json'
        if args.resume and path.exists() and receipt.exists():
            prior=json.loads(path.read_text());record=json.loads(receipt.read_text())
            require(prior['input_sha256']==hashes and prior['part']==part and prior['parts']==args.jobs,'Stale batch checkpoint')
            require(record['exit_code']==0 and record['output_sha256']==digest(path.read_bytes()),'Changed batch checkpoint')
            return record
        command=[sys.executable,'-I','-S','-B',str(Path(__file__)),
                 '--reference',str(args.reference.resolve()),'--output',str(args.output.resolve()),
                 '--work-dir',str(args.work_dir.resolve()),'--receipt',str(args.receipt.resolve()),
                 '--jobs',str(args.jobs),'--worker',str(part)]
        begin=datetime.datetime.now(datetime.timezone.utc).isoformat();tick=time.monotonic()
        with (args.work_dir/f'part-{part}.stdout').open('w') as stream:
            completed=subprocess.run(command,stdout=stream,stderr=subprocess.STDOUT)
        record=dict(part=part,command=command,started_at=begin,
                    finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    seconds=round(time.monotonic()-tick,3),exit_code=completed.returncode)
        require(completed.returncode==0,'Batch failed: '+str(part))
        record['output_sha256']=digest(path.read_bytes())
        dump(receipt,record)
        print(json.dumps(dict(batch_completed=part,seconds=record['seconds'])),flush=True)
        return record
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures=[executor.submit(run_part,part) for part in range(args.jobs)]
        records=[future.result() for future in as_completed(futures)]

    counts=Counter();root_counts=Counter();splits=Counter();details={};used=set();gaps=[]
    root_groups=root_systems=certified_systems=max_depth=0
    archives=[];archive_dir=args.receipt.parent/'exhaustive_parts'
    archive_dir.mkdir(parents=True,exist_ok=True)
    for part in range(args.jobs):
        path=args.work_dir/f'part-{part}.json';raw=path.read_bytes();result=json.loads(raw)
        require(result['status']=='PASS' and result['part']==part and result['parts']==args.jobs,'Wrong batch result')
        require(result['input_sha256']==hashes,'Batch proof inputs differ')
        keys=[g['key'] for g in groups[part::args.jobs]]
        require(result['group_keys_sha256']==digest(json.dumps(keys).encode()),'Batch partition differs')
        checked=result['checked'];require(set(checked['proof_checks'])==set(keys),'Missing batch root')
        require(not set(details)&set(keys),'Overlapping batches')
        details.update(checked['proof_checks']);used.update(checked['used_vectors'])
        counts.update(checked['counts']);root_counts.update(checked['root_counts']);splits.update(checked['split_types'])
        root_groups+=checked['root_groups'];root_systems+=checked['root_systems'];certified_systems+=checked['certified_systems']
        max_depth=max(max_depth,checked['maximum_tree_depth']);gaps.append(Fraction(checked['minimum_normalized_gap']))
        packed=gzip.compress(raw,compresslevel=9,mtime=0)
        archive=archive_dir/f'part-{part}.json.gz';archive.write_bytes(packed)
        archives.append(dict(part=part,path=str(archive.relative_to(ROOT) if archive.is_absolute() else archive),
                             output_sha256=digest(raw),archive_sha256=digest(packed),groups=len(keys),
                             integer_roots=checked['root_systems'],certified_systems=checked['certified_systems']))
    require(set(details)=={g['key'] for g in groups},'Merged coverage is incomplete')
    require(used==set(range(len(bundle['pool']))),'Unused certificate vector')
    require(counts['tree_leaves']==counts['tree_roots']+counts['binary_splits'],'Broken tree identity')
    linear=dict(root_groups=root_groups,root_systems=root_systems,root_counts=dict(root_counts),counts=dict(counts),
                certified_systems=certified_systems,vectors=len(bundle['pool']),maximum_tree_depth=max_depth,
                split_types=dict(splits),minimum_normalized_gap=str(min(gaps)))
    require(linear==reference['summary']['linear'],'Merged statistics differ from the symbolic check')
    require(details==reference['proof_checks'],'Per-root numerical/interval results differ')
    require(fingerprint(reference)=={k:v for k,v in hashes.items() if k!='reference_output_sha256'},'Proof inputs changed during validation')
    reference['summary']['verification_mode']='interval-plus-exhaustive'
    dump(args.output,reference)
    record=dict(status='PASS',method='all integer matrices and certificates checked in independent batches',
                jobs=args.jobs,started_at=started,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                seconds=round(time.monotonic()-clock,3),input_sha256=hashes,runs=sorted(records,key=lambda r:r['part']),
                archives=archives,linear=linear,output_sha256=digest(args.output.read_bytes()),
                all_roots_partitioned_exactly_once=True,all_numerical_rows_equal_symbolic_rows=True,
                all_integer_certificates_checked=True,all_per_root_results_equal_standard=True)
    dump(args.receipt,record)
    print(json.dumps({k:record[k] for k in ('status','jobs','seconds','output_sha256')}),flush=True)


if __name__=='__main__':
    main()
