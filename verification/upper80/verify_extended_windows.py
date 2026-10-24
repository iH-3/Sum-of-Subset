"""Incremental six-empty-root and direct-root window certificates.

Only the new records are replayed by default. Old closed rank slices are
identified by their immutable packet and stored verification receipt.
--reuse-new-receipts verifies packaging against already obtained new replays;
--replay-prior-ranks explicitly opts into replaying the old rank certificates.
This never certifies structural applicability or a global bound of 80.
"""
from pathlib import Path
import argparse,gzip,hashlib,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import exact,model as m,record_pool as pool
ROOT=Path(__file__).resolve().parents[2]
PATH=ROOT/'data/upper80_extended_windows_20261024.json.gz'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def verify(reuse_new_receipts=False,replay_prior_ranks=False):
    raw=json.loads(gzip.decompress(PATH.read_bytes()));packet=pool.unpack(raw)
    m.need(packet['format']=='upper80-extended-windows-v1' and packet['global_upper_bound_certified'] is False and packet['structural_applicability_certified'] is False,'Conditional window packet scope')
    expected=[(6,436,False,0),(6,436,False,1),(5,270,False,None)]
    m.need([(e['j'],e['index'],e['positive'],e['rank']) for e in packet['entries']]==expected,'Exact new closure inventory')
    checks=[]
    for entry in packet['entries']:
        record=entry['record'];j,index,positive=entry['j'],entry['index'],entry['positive'];st=([*m.patterns(j),*m.partial_patterns(j)])[index]
        limits={} if entry['rank'] is None else {'rank_k':[entry['rank'],entry['rank']]}
        m.need(record['st']==st and record['j']==j and record['positive']==positive and (record.get('limits') or {})==limits,'Closed record root and exact rank domain')
        m.need(entry['closed'] is True,'Explicit new closed record')
        if reuse_new_receipts:
            receipt=entry['receipt'];m.need(receipt['record_sha256']==hashlib.sha256(pool.canonical(record)).hexdigest() and receipt['status'].startswith('PASS_NEW_'),'Unchanged previously replayed new record')
            result=receipt['replay']
        else:result=exact.replay(record,require_closed=True)
        checks.append(dict(j=j,index=index,rank=entry['rank'],closed=True,replay=result))
    prior=packet['prior_ranks'];path=ROOT/prior['packet'];receipt_path=ROOT/prior['receipt'];receipt=json.loads(receipt_path.read_text())
    m.need(sha(path)==prior['packet_sha256']==receipt['packet_sha256'] and sha(receipt_path)==prior['receipt_sha256'],'Immutable previously checked rank packet and receipt')
    old=json.loads(gzip.decompress(path.read_bytes()))
    m.need((old['j'],old['pattern_index'],old['positive'])==(6,436,False) and old['certified_ranks']==receipt['certified_ranks']==list(range(2,8)) and receipt['status']=='PASS_PARTIAL_RANK_REFINEMENTS','Previously certified complementary rank slices')
    # The existing source budget is tau+delta+k^2 <= 496-73j, with
    # nonnegative tau and delta. Thus k>=8 is impossible for j=6.
    m.need(7*7<=496-73*6<8*8,'Exhaustive feasible rank interval')
    if replay_prior_ranks:
        import verify_refinements
        verify_refinements.verify()
    return dict(status='PASS_INCREMENTAL_EXTENDED_WINDOWS',global_upper_bound_certified=False,structural_applicability_certified=False,
                established_range=[71,81],newly_closed_original_roots=[[5,270,False],[6,436,False]],
                closed_original_roots=4647,open_original_roots=7,records=checks,
                new_record_replays=0 if reuse_new_receipts else len(checks),reused_new_replays=len(checks) if reuse_new_receipts else 0,
                reused_prior_ranks=list(range(2,8)),prior_ranks_replayed=replay_prior_ranks,
                pooled_records=len(raw['records']),packet_sha256=sha(PATH))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--reuse-new-receipts',action='store_true');ap.add_argument('--replay-prior-ranks',action='store_true');ap.add_argument('--output',type=Path);args=ap.parse_args()
    result=verify(args.reuse_new_receipts,args.replay_prior_ranks)
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
