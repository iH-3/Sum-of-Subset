"""Save/restore discovery checkpoints without claiming a covered root.

Shared premises are stored once. Branch.visit replays a restored closed
checkpoint before using it; this file itself certifies no theorem.
"""
from pathlib import Path,PurePosixPath
import argparse,gzip,hashlib,json
ROOT=Path(__file__).resolve().parents[2]

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def snapshot(paths,output):
    records={};entries={}
    def intern(record):
        body={k:v for k,v in record.items() if k!='premise'}
        if 'premise' in record:body['premise_ref']=intern(record['premise'])
        key=hashlib.sha256(canonical(body)).hexdigest();records[key]=body;return key
    for directory in paths:
        for path in sorted((ROOT/directory).glob('*.json.gz')):
            value=json.loads(gzip.decompress(path.read_bytes()))
            entries[path.relative_to(ROOT).as_posix()]=dict(closed=value['closed'],record_ref=intern(value['record']))
    packet=dict(schema='upper80-discovery-frontier-v1',global_upper_bound_certified=False,
                structural_applicability_certified=False,root_coverage_certified=False,entries=entries,records=records)
    output.write_bytes(gzip.compress(canonical(packet),mtime=0))
    return dict(checkpoints=len(entries),shared_records=len(records),closed_checkpoints=sum(e['closed'] for e in entries.values()),bytes=output.stat().st_size)

def restore(path):
    packet=json.loads(gzip.decompress(path.read_bytes()))
    if packet['schema']!='upper80-discovery-frontier-v1' or any(packet[k] is not False for k in ('global_upper_bound_certified','structural_applicability_certified','root_coverage_certified')):raise ValueError('Discovery-only frontier scope')
    pool=packet['records'];memo={};visiting=set()
    def expand(key):
        if key in memo:return memo[key]
        if key in visiting or key not in pool:raise ValueError('Invalid frontier premise graph')
        body=pool[key]
        if hashlib.sha256(canonical(body)).hexdigest()!=key:raise ValueError('Frontier record identity')
        visiting.add(key);record={k:v for k,v in body.items() if k!='premise_ref'}
        if 'premise_ref' in body:record['premise']=expand(body['premise_ref'])
        visiting.remove(key);memo[key]=record;return record
    prepared=[]
    for name,entry in packet['entries'].items():
        relative=PurePosixPath(name)
        if relative.is_absolute() or '..' in relative.parts or relative.parts[:2]!=('.work','upper80') or not name.endswith('.json.gz'):raise ValueError('Frontier checkpoint path')
        if type(entry['closed']) is not bool:raise ValueError('Frontier checkpoint status')
        value=dict(closed=entry['closed'],record=expand(entry['record_ref']));destination=ROOT/name
        if destination.exists():
            if json.loads(gzip.decompress(destination.read_bytes()))!=value:raise ValueError('Existing checkpoint differs: '+name)
        else:prepared.append((destination,value))
    for destination,value in prepared:
        destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(gzip.compress(canonical(value),mtime=0))
    return dict(restored=len(prepared),checkpoints=len(packet['entries']),root_coverage_certified=False)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);parser.add_argument('--restore',type=Path);parser.add_argument('paths',nargs='*');args=parser.parse_args()
    if args.restore and not args.output and not args.paths:result=restore(args.restore)
    elif args.output and args.paths and not args.restore:result=snapshot(args.paths,args.output)
    else:parser.error('Use --output PATH DIRECTORIES... or --restore PATH')
    print(json.dumps(result))
