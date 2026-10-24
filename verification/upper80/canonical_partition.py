"""Incremental four-case canonical-minimizer partition, never a global proof.

Each actual integer core has phi<=xi. Split xi>=phi+1 versus xi=phi
independently on its two sides, preserving all four alternatives. Finished
stages are skipped by continue_frontier; a changed parent is rejected.
"""
from pathlib import Path
import argparse,json,itertools,sys
import fast_lp
fast_lp.install()
import record_pool as pool,continue_frontier
from discover import Search

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('directory',type=Path)
    ap.add_argument('--methods',nargs='+',choices=['canonical_tail','source_envelope','native','tail_cap_windows','canonical_gap_windows','punctured_windows'],default=['canonical_tail','source_envelope','native','tail_cap_windows'])
    args=ap.parse_args();value=pool.read_gzip(args.source)
    if value.get('closed'):print('SKIPPED_CLOSED_PARENT',args.source,flush=True);return
    base=value['record'];digest=pool.record_digest(base);args.directory.mkdir(parents=True,exist_ok=True)
    variables=['linear_cut:'+json.dumps({'ONE':1,'phicore'+s:1,'x'+s:-1},sort_keys=True,separators=(',',':')) for s in 'st']
    for case,bits in enumerate(itertools.product((0,1),repeat=2)):
        limits=dict(base.get('limits') or {})
        if any(v in limits for v in variables):raise ValueError('Canonical cuts are already present; use their existing partition')
        limits.update({v:[bit,bit] for v,bit in zip(variables,bits)})
        path=args.directory/f'{case}_parent.json.gz'
        if path.exists():
            parent=pool.read_gzip(path)['record']
            if parent.get('limits')!=limits or pool.record_digest(parent['premise'])!=digest:raise ValueError('Different parent: use a new partition directory')
        else:
            search=Search(base['st'],base['j'],base['positive'],limits,use_planes=True,parent=base)
            pool.write_gzip(path,dict(record=search.record(),closed=False,status='complete_canonical_minimizer_case',case=case,bits=bits))
        print('CANONICAL_CASE',case,bits,flush=True)
        for method in args.methods:
            target=args.directory/f'{case}_{method}.json.gz'
            sys.argv=['continue_frontier',str(path),str(target),'--method',method]
            continue_frontier.main();value=pool.read_gzip(target);path=target
            if value['closed']:print('CLOSED_CANONICAL_CASE',case,method,flush=True);break
        print('FINAL_CANONICAL_CASE',case,value['closed'],path,flush=True)

if __name__=='__main__':main()
