"""Replay strengthened OPEN research premises; certify no new closed root."""
from pathlib import Path
import argparse,gzip,hashlib,json,sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE));ROOT=HERE.parents[1]
import exact,model as m
PATH=ROOT/'data/upper80_target_geometry_20261024.json.gz'
EXPECTED=[(4,142,False),(4,142,True),*[(5,i,False) for i in (219,256,266,268,270,413)],(6,436,False)]

def canonical(value):return json.dumps(value,separators=(',',':')).encode()

def load():
    packet=json.loads(gzip.decompress(PATH.read_bytes()))
    m.need(packet['schema']=='upper80-target-geometry-v1' and packet['global_upper_bound_certified'] is False
           and packet['structural_applicability_certified'] is False and packet['closed_original_roots']==0,'Open target-geometry scope')
    m.need([(e['j'],e['index'],e['positive']) for e in packet['entries']]==EXPECTED,'All nine original open obligations')
    pool=packet['records'];memo={};visiting=set()
    def expand(key):
        if key in memo:return memo[key]
        m.need(key in pool and key not in visiting,'Valid premise graph');body=pool[key]
        m.need(hashlib.sha256(canonical(body)).hexdigest()==key and 'premise' not in body,'Order-preserving premise identity')
        visiting.add(key);record={k:v for k,v in body.items() if k!='premise_ref'}
        if 'premise_ref' in body:record['premise']=expand(body['premise_ref'])
        visiting.remove(key);memo[key]=record;return record
    result=[]
    for entry in packet['entries']:
        j,index,positive=entry['j'],entry['index'],entry['positive'];record=expand(entry['record_ref'])
        m.need(entry['closed'] is False and type(positive) is bool,'Explicitly open local record')
        st=([*m.patterns(j),*m.partial_patterns(j)])[index]
        m.need(record['st']==st and record['j']==j and record['positive']==positive,'Exact research root identity')
        limits=record.get('limits') or {}
        m.need(limits==({'hole_W':[1,1]} if positive else {}),'Open root or exact W=1 subdomain')
        result.append(dict(entry,record=record))
    m.need(set(memo)==set(pool),'Every pooled premise is referenced')
    return result,len(pool)

def verify(export_directory=None):
    entries,pool_size=load();checks=[]
    for entry in entries:
        record=entry['record'];state=exact.replay(record,require_closed=False,return_state=True)
        checks.append(dict(j=entry['j'],index=entry['index'],positive=entry['positive'],closed=False,
                           local_steps=len(record['trace']),credit=state['credit'],coverage_width=state['coverage_width'],
                           coverage_bracket_width=state['coverage_bracket_width'],
                           full_probe_components=[len(p['nodes']) for p in state['full_probes']]))
        if export_directory:
            export_directory.mkdir(parents=True,exist_ok=True)
            name=f"{entry['j']}_{entry['index']}_{int(entry['positive'])}_parent.json"
            (export_directory/name).write_bytes(canonical(record)+b'\n')
    return dict(status='PASS_OPEN_TARGET_GEOMETRY_PREMISES',global_upper_bound_certified=False,
                structural_applicability_certified=False,established_range=[71,81],closed_original_roots=0,
                open_original_roots=9,shared_records=pool_size,records=checks,
                packet_sha256=hashlib.sha256(PATH.read_bytes()).hexdigest())

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);parser.add_argument('--export-directory',type=Path)
    args=parser.parse_args();result=verify(args.export_directory)
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
