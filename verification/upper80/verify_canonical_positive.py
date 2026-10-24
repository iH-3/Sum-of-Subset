"""Complete positive root: new W=1 closure and immutable W=2..7 slices.

Default performs independent exact arithmetic. --reuse-receipts checks the
precise domains, complete integer coverage and unchanged saved identities,
without repeating any of the already recorded arithmetic replays.
"""
from pathlib import Path
import sys,argparse,json,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent))
import model as m,exact,record_pool as pool,verify_positive_refinements as vp,replay_partial as rp
ROOT=Path(__file__).resolve().parents[2]
PATH=ROOT/'data/upper80_canonical_positive_closure_20261024.json.gz'
PRIOR_SHA='72844b58d6c8f668d2decd1892f8bc7ea61aa9b15cff74333df5f49ba45576ea'

def verify(reuse_receipts=False):
    packet=pool.read_gzip(PATH)
    m.need(packet['format']=='upper80-canonical-positive-closure-v1' and packet['root']==[4,142,1] and packet['closed'] is True,'Complete positive root packet')
    m.need(packet['global_upper_bound_certified'] is False and packet['structural_applicability_certified'] is False,'Conditional research scope')
    prior=packet['prior'];receipt_path=ROOT/prior['receipt_path'];receipt=json.loads(receipt_path.read_text())
    m.need(prior['path']=='data/upper80_positive_refinements_20261024.json.gz' and hashlib.sha256((ROOT/prior['path']).read_bytes()).hexdigest()==prior['sha256']==PRIOR_SHA,'Immutable earlier positive slices')
    m.need(hashlib.sha256(receipt_path.read_bytes()).hexdigest()==prior['receipt_sha256'] and receipt['packet_sha256']==PRIOR_SHA and receipt['status']=='PASS_PARTIAL_POSITIVE_REFINEMENTS' and receipt['certified_W']==list(range(2,8)),'Previously verified complementary slices')
    slices=packet['slices'];old=vp.load();st=([*m.patterns(4),*m.partial_patterns(4)])[142]
    m.need([s['W'] for s in slices]==[[1,1],[2,2],[3,7]],'Complete positive slice inventory')
    m.need(rp.domain('hole_W',dict(j=4,positive=True))==(1,7),'Entire original positive-hole domain')
    covered=[];results=[]
    for i,s in enumerate(slices):
        record=s['record'];a,b=s['W'];covered.extend(range(a,b+1))
        m.need(s['closed'] is True and record['j']==4 and record['positive'] is True and record['st']==st and record['limits']=={'hole_W':[a,b]},'Exact root and unrestricted slice domain')
        digest=pool.record_digest(record)
        if i==0:
            r=s['receipt']
            m.need(r['status']=='PASS_NEW_W1_CANONICAL_GAP_CLOSURE' and r['root']==[4,142,1] and r['W']==[1,1] and r['closed'] is True and r['record_merkle_sha256']==digest,'New W1 exact replay identity')
        else:m.need(digest==s['record_merkle_sha256']==pool.record_digest(old[i]['record']),'Old closed slice unchanged')
        if not reuse_receipts:results.append(exact.replay(record,require_closed=True))
    m.need(covered==list(range(1,8)),'No gap or duplicate in integer coverage')
    return dict(status='PASS_COMPLETE_CANONICAL_POSITIVE_ROOT',root=[4,142,1],closed=True,original_roots_closed=4652,original_roots_open=2,
                remaining_roots=[[4,142,0],[5,219,0]],replayed_slices=0 if reuse_receipts else 3,reused_slices=3 if reuse_receipts else 0,
                packet_sha256=hashlib.sha256(PATH.read_bytes()).hexdigest(),global_upper_bound_certified=False,structural_applicability_certified=False,established_range=[71,81])

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--reuse-receipts',action='store_true');ap.add_argument('--output',type=Path);args=ap.parse_args()
    result=verify(args.reuse_receipts)
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
