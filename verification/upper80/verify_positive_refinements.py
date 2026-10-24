"""Replay all W slices, preserving the one explicitly open positive slice."""
from pathlib import Path
import argparse,gzip,hashlib,json,sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE));ROOT=HERE.parents[1]
import exact,model as m
PATH=ROOT/'data/upper80_positive_refinements_20261024.json.gz'

def load():
    packet=json.loads(gzip.decompress(PATH.read_bytes()));pool=[]
    m.need(packet['format']=='upper80-positive-refinements-v1' and all(packet[k] is False for k in ('global_upper_bound_certified','structural_applicability_certified','root_closed')),'Partial positive refinement scope')
    m.need((packet['j'],packet['pattern_index'],packet['positive'])==(4,142,True),'Positive refinement root')
    for body in packet['premises']:
        record=dict(body);m.need('premise' not in record,'Unpooled positive premise');ref=record.pop('premise_ref',None)
        if ref is not None:
            m.need(type(ref) is int and 0<=ref<len(pool),'Positive premise forward reference');record['premise']=pool[ref]
        pool.append(record)
    m.need([(e['W'],e['closed']) for e in packet['slices']]==[([1,1],False),([2,2],True),([3,7],True)],'Complete positive-hole slice inventory')
    st=([*m.patterns(4),*m.partial_patterns(4)])[142];entries=[]
    for entry in packet['slices']:
        ref=entry['record_ref'];m.need(type(ref) is int and 0<=ref<len(pool),'Positive slice record reference')
        record=pool[ref]
        m.need(record['st']==st and record['j']==4 and record['positive'] is True and record['limits']=={'hole_W':entry['W']},'Exact positive slice domain')
        entries.append(dict(entry,record=record))
    return entries

def verify():
    entries=load();counts=[]
    for entry in entries:
        result=exact.replay(entry['record'],require_closed=entry['closed']);counts.append(dict(W=entry['W'],closed=entry['closed'],local_steps=result['steps']))
    return dict(status='PASS_PARTIAL_POSITIVE_REFINEMENTS',global_upper_bound_certified=False,
                structural_applicability_certified=False,closed_original_roots=0,certified_W=[2,3,4,5,6,7],open_W=[1],
                slices=counts,packet_sha256=hashlib.sha256(PATH.read_bytes()).hexdigest())

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output');parser.add_argument('--export-open');args=parser.parse_args();result=verify()
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    if args.export_open:
        target=Path(args.export_open);target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(load()[0]['record'],separators=(',',':'))+'\n')
    print(json.dumps(result))
