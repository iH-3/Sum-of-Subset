"""Complete j5_219 canonical-minimizer partition; original root only.

Default independently replays all four leaves. --reuse-receipts performs
the exact integer-domain coverage and saved-identity checks without
repeating arithmetic already recorded in the four new replay receipts.
"""
from pathlib import Path
import sys,json,hashlib,argparse,itertools
sys.path.insert(0,str(Path(__file__).resolve().parent))
import model as m,record_pool as pool,replay_partial as rp
ROOT=Path(__file__).resolve().parents[2]
PATH=ROOT/'data/upper80_canonical_minimizer_closure_20261024.json.gz'

def verify(reuse_receipts=False):
    p=pool.read_gzip(PATH);branch=p['branch'];base=p['base'];receipts=p['receipts']
    m.need(p['format']=='upper80-canonical-minimizer-closure-v1' and p['root']==[5,219,0] and p['closed'] is True,'Complete canonical-minimizer root')
    m.need(p['global_upper_bound_certified'] is False and p['structural_applicability_certified'] is False,'Conditional research scope')
    pattern=([*m.patterns(5),*m.partial_patterns(5)])[219]
    for r in [base,branch]:m.need(r['st']==pattern and r['j']==5 and r['positive'] is False and not r.get('limits'),'Exact unrestricted original root')
    variables=['linear_cut:'+json.dumps({'ONE':1,'phicore'+side:1,'x'+side:-1},sort_keys=True,separators=(',',':')) for side in 'st']
    expected=dict(variable=variables[0],threshold=0,left=dict(variable=variables[1],threshold=0,left=dict(leaf=0),right=dict(leaf=1)),right=dict(variable=variables[1],threshold=0,left=dict(leaf=2),right=dict(leaf=3)))
    m.need(p['variables']==variables and branch['tree']==expected and not branch['open'] and len(branch['leaves'])==len(receipts)==4,'Complete two-level complementary partition')
    m.need(all(rp.domain(v,branch)==(0,1) for v in variables),'Full integer linear-cut domains')
    packed=pool.pack(p);ancestor=packed['payload']['base']['$record']
    for i,(record,bits,receipt) in enumerate(zip(branch['leaves'],itertools.product((0,1),repeat=2),receipts)):
        limits={v:[bit,bit] for v,bit in zip(variables,bits)};digest=packed['payload']['branch']['leaves'][i]['$record']
        m.need(receipt['status']=='PASS_NEW_CANONICAL_MINIMIZER_CASE' and receipt['root']==[5,219,0] and receipt['case']==i and receipt['bits']==list(bits) and receipt['closed'] is True and receipt['record_merkle_sha256']==digest,'Unchanged independently replayed conditional record')
        key=digest
        while key!=ancestor:
            cursor=packed['records'][key]
            m.need(cursor['st']==pattern and cursor['j']==5 and cursor['positive'] is False and cursor['limits']==limits and 'premise' in cursor,'Exact conditional domain to the common unrestricted parent')
            key=cursor['premise']['$record']
    old=p['prior_root_receipt'];path=ROOT/old['path'];r=json.loads(path.read_text())
    m.need(hashlib.sha256(path.read_bytes()).hexdigest()==old['sha256'] and r['status']=='PASS_COMPLETE_CANONICAL_POSITIVE_ROOT' and r['original_roots_closed']==4652,'Prior complete-root ledger')
    m.need(hashlib.sha256((ROOT/'data/upper80_canonical_positive_closure_20261024.json.gz').read_bytes()).hexdigest()==r['packet_sha256'],'Prior positive root packet unchanged')
    if not reuse_receipts:m.need(rp.branch(branch)==(4,3),'Independent complete branch replay')
    return dict(status='PASS_COMPLETE_CANONICAL_MINIMIZER_ROOT',root=[5,219,0],closed=True,original_roots_closed=4653,original_roots_open=1,remaining_roots=[[4,142,0]],
                exact_cases=4,integer_splits=3,replayed_cases=0 if reuse_receipts else 4,reused_cases=4 if reuse_receipts else 0,
                packet_sha256=hashlib.sha256(PATH.read_bytes()).hexdigest(),global_upper_bound_certified=False,structural_applicability_certified=False,established_range=[71,81])

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--reuse-receipts',action='store_true');ap.add_argument('--output',type=Path);args=ap.parse_args()
    result=verify(args.reuse_receipts)
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
