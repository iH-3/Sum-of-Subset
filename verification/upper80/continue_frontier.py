"""Incremental discovery from raw or pooled checkpoints; never a global proof.

Finished outputs are never restarted, even after an unrelated code change.
Interrupted outputs retain all proved consequences and become the next premise.
A genuinely new method or stronger system must use a new output path.
"""
from pathlib import Path
import argparse,hashlib,json,time,gzip
import fast_lp;fast_lp.install()
from discover import Search
import record_pool as pool,full_window as fw,source_union as su,canonical_phi as cm,core_gap as cg,source_hulls as sh,ownerless_hit as oh,source_envelope as se

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('output',type=Path)
    ap.add_argument('--method',choices=['windows','integer_windows','gap_windows','integer_gap_windows','punctured_windows','integer_punctured_windows','canonical_gap_windows','native','source','canonical_source','source_hulls','source_envelope','canonical','canonical_tail','shifted_canonical','ownerless','coverage','core_gaps'],default='windows');ap.add_argument('--cycles',type=int,default=20);ap.add_argument('--broad',action='store_true');ap.add_argument('--seed-point',type=Path);args=ap.parse_args()
    modules=[Path(__file__),Path(fw.__file__),Path(su.__file__),Path(cm.__file__),Path(cg.__file__),Path(sh.__file__),Path(oh.__file__),Path(se.__file__),*[Path(__file__).with_name(n+'.py') for n in ('discover','exact','first_gap_core','parametric','model')]]
    digest=hashlib.sha256(b''.join(p.read_bytes() for p in modules)+json.dumps([args.method,args.broad]).encode()).hexdigest()
    old=None
    if args.output.exists():
        envelope=json.loads(gzip.decompress(args.output.read_bytes()))
        metadata=envelope['payload'] if envelope.get('schema')=='upper80-nested-record-pool-v1' else envelope
        if metadata.get('closed') or metadata.get('status')=='stalled':
            print('REUSED_FINISHED_CHECKPOINT',str(args.output),flush=True);return
        old=pool.unpack(envelope) if envelope.get('schema')=='upper80-nested-record-pool-v1' else envelope
        if old.get('method') not in (None,args.method):raise ValueError('Use a new output path for a different discovery method')
    data=pool.read_gzip(args.source);parent=old['record'] if old is not None else data['record']
    seed=pool.read_gzip(args.seed_point).get('point') if args.seed_point else None
    if args.seed_point and seed is None:raise ValueError('Requested saved discovery point is absent')
    if data.get('closed'):raise ValueError('Do not search a closed source')
    s=Search(parent['st'],parent['j'],parent['positive'],parent.get('limits'),use_planes=True,parent=parent)
    s.omit_generated_rows=True;s.window_affine_only=not args.broad;s.max_full_probes=0
    s.window_extreme_gaps=args.method in ('gap_windows','integer_gap_windows','punctured_windows','integer_punctured_windows','canonical_gap_windows')
    s.window_punctures=args.method in ('punctured_windows','integer_punctured_windows','canonical_gap_windows')
    s.window_canonical_gaps=args.method=='canonical_gap_windows'
    s.source_canonical_gaps=args.method=='canonical_source'
    if args.method=='native':s.full_cover_step=lambda point:(False,False)
    start=time.monotonic();last=[start,0];point=None;closed=False;new=False
    def save(status):
        pool.write_gzip(args.output,dict(record=s.record(),point=point,closed=closed,status=status,method=args.method,method_digest=digest))
    original=s.lp
    def logged(target=None):
        result=original(target)
        if time.monotonic()-last[0]>30 and len(s.trace)>last[1]:
            save('progress');last[:]=[time.monotonic(),len(s.trace)]
            print('CHECKPOINT',len(s.trace),s.e,round(time.monotonic()-start,2),flush=True)
        return result
    s.lp=logged
    try:
        if args.method=='native':
            closed=s.run();point=getattr(s,'point',None)
        else:
            for cycle in range(args.cycles):
                r=s.lp()
                if r.status==2:s.final();closed=True;break
                point=dict(zip(s.names,r.x))
                seeded=cycle==0 and seed is not None
                if seeded:point=seed;print('REUSED_SAVED_DISCOVERY_POINT',flush=True)
                if args.method in ('integer_windows','integer_gap_windows','integer_punctured_windows'):
                    import numpy as np
                    from scipy.optimize import milp,Bounds,LinearConstraint
                    s.matrices();keep=[i for i,(_,_,label) in enumerate(s.rows) if label not in ('integer CG consequence','complete target-cover consequence')]
                    A=np.vstack([s.A[keep],s.E]);lower=np.r_[np.full(len(keep),-np.inf),s.f];upper=np.r_[s.b[keep],s.f]
                    result=milp(np.zeros(len(s.names)),integrality=np.ones(len(s.names)),bounds=Bounds(np.zeros(len(s.names)),np.full(len(s.names),np.inf)),constraints=LinearConstraint(A,lower,upper),options=dict(time_limit=8,mip_rel_gap=0))
                    print('MIP_DISCOVERY_ONLY',cycle,result.status,flush=True)
                    if result.x is None:break
                    point=dict(zip(s.names,result.x));changed,finished=fw.discover(s,point)
                elif args.method=='coverage':changed,finished=s.full_cover_step(point)
                else:changed,finished={'windows':fw.discover,'gap_windows':fw.discover,'punctured_windows':fw.discover,'canonical_gap_windows':fw.discover,'source':su.discover,'canonical_source':su.discover,'source_hulls':sh.discover,'source_envelope':se.discover,'canonical':cm.discover,'canonical_tail':cm.discover_tail,'shifted_canonical':cm.discover_shifted,'ownerless':oh.discover,'core_gaps':cg.discover}[args.method](s,point)
                print('CYCLE',cycle,changed,finished,len(s.trace),flush=True)
                if finished:
                    if args.method not in ('coverage','core_gaps') or not changed:s.final()
                    closed=True;break
                new=changed;save('progress' if changed or seeded else 'stalled')
                if not changed and not seeded:break
            else:save('budget_reached');return
        save('closed' if closed else 'stalled');print('RESULT',closed,len(s.trace),s.e,round(time.monotonic()-start,2),flush=True)
    except BaseException:save('interrupted');raise

if __name__=='__main__':main()
