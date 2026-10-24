"""The complete (5,413,0) partition, with optional reuse of saved replays.

Default: exact replay of the complete record. --reuse-receipt checks the
unchanged assembly/new-branch identities and the immutable earlier frontier;
it does not repeat arithmetic that already has a saved verification receipt.
Neither mode certifies structural applicability or the global bound 80.
"""
from pathlib import Path
import argparse,hashlib,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import exact,model as m,record_pool as pool
ROOT=Path(__file__).resolve().parents[2]
PATH=ROOT/'data/upper80_extreme_gap_closure_20261024.json.gz'
PRIOR_SHA='34af6e9d27b93183fb22926b2781117f1dd9279599f8c68abce7757a991f8cb2'

def digest(value):return hashlib.sha256(pool.canonical(value)).hexdigest()

def verify(reuse_receipt=False):
    packet=pool.read_gzip(PATH);record=packet['record'];receipt=packet['receipt']
    m.need(packet['format']=='upper80-extreme-gap-closure-v1' and packet['closed'] is True,'Complete extreme-gap partition packet')
    m.need(packet['global_upper_bound_certified'] is False and packet['structural_applicability_certified'] is False,'Conditional research scope')
    pattern=([*m.patterns(5),*m.partial_patterns(5)])[413]
    m.need(record['st']==pattern and record['j']==5 and not record['positive'] and not record.get('limits'),'Exact unrestricted original root')
    m.need(receipt['status']=='PASS_INCREMENTAL_COMPLETE_413_GAP_PARTITION' and receipt['record_sha256']==digest(record),'Unchanged verified assembly')
    prior=packet['prior_frontier'];prior_path=ROOT/prior['path']
    m.need(prior['path']=='data/upper80_open_frontier_20261024.json.gz' and hashlib.sha256(prior_path.read_bytes()).hexdigest()==prior['sha256']==PRIOR_SHA,'Immutable previously verified frontier')
    old=pool.read_gzip(prior_path);saved={v['name']:v['checkpoint'] for v in old['checkpoints']}
    base=saved['hull_5_413_0_window_affine_extended_cases/parent']['record']
    m.need(dict(record,trace=record['trace'][:-1])==base and record['trace'][-1]['kind']=='full_cover_partition','Frozen complete partition parent')
    tree=record['trace'][-1]['tree'];sources=packet['sources']
    m.need(tree['closed'] is True and len(tree['children'])==12 and [s['case'] for s in sources]==list(range(12)),'Every recorded alternative retained')
    m.need(tree['probe']==saved['hull_5_413_0_window_affine_extended_cases/parent']['probe'],'Same complete target')
    for source,child in zip(sources,tree['children']):
        m.need(source['node']==child['node'] and child['child']['closed'] is True and source['record_sha256']==digest(child['child']['record']),'Unchanged exact conditional child')
        if source['case']==3:
            r=packet['new_case_receipt']
            m.need(r['status']=='PASS_NEW_CONDITIONAL_413_EXTREME_GAP_CLOSURE' and r['closed'] is True and r['record_sha256']==source['record_sha256'],'New branch exact replay receipt')
        else:
            old_child=saved[source['checkpoint']]
            m.need(old_child['closed'] is True and digest(old_child['record'])==source['record_sha256'],'Previously verified closed child reused unchanged')
    m.need(len({tuple(c['node']) for c in tree['children']})==12,'No repeated partition alternative')
    for reference in packet['prior_receipts']:
        m.need(hashlib.sha256((json.dumps(reference['receipt'])+'\n').encode()).hexdigest()==reference['sha256'],'Unchanged prior arithmetic receipt')
    replay=receipt if reuse_receipt else exact.replay(record,require_closed=True)
    return dict(status='PASS_COMPLETE_EXTREME_GAP_ROOT',root=[5,413,0],closed=True,original_roots_closed=4651,original_roots_open=3,
                remaining_roots=[[4,142,0],[4,142,1],[5,219,0]],replayed_complete_record=not reuse_receipt,
                reused_closed_cases=list(range(12)) if reuse_receipt else [],packet_sha256=hashlib.sha256(PATH.read_bytes()).hexdigest(),
                global_upper_bound_certified=False,structural_applicability_certified=False,established_range=[71,81])

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--reuse-receipt',action='store_true');ap.add_argument('--output',type=Path);args=ap.parse_args()
    result=verify(args.reuse_receipt)
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
