"""Incremental discovery from raw or pooled checkpoints; never a global proof.

Finished same-method outputs are skipped. Interrupted outputs retain all
proved consequences and become the next premise. Only new systems are run.
"""
from pathlib import Path
import argparse,hashlib,json,time
import fast_lp;fast_lp.install()
from discover import Search
import record_pool as pool,full_window as fw,source_union as su,canonical_phi as cm

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('output',type=Path)
    ap.add_argument('--method',choices=['windows','integer_windows','native','source','canonical','coverage'],default='windows');ap.add_argument('--cycles',type=int,default=20);ap.add_argument('--broad',action='store_true');args=ap.parse_args()
    modules=[Path(__file__),Path(fw.__file__),Path(su.__file__),Path(cm.__file__),*[Path(__file__).with_name(n+'.py') for n in ('discover','exact','first_gap_core','parametric','model')]]
    digest=hashlib.sha256(b''.join(p.read_bytes() for p in modules)+json.dumps([args.method,args.broad]).encode()).hexdigest()
    data=pool.read_gzip(args.source);parent=data['record']
    if args.output.exists():
        old=pool.read_gzip(args.output)
        if old.get('closed') or old.get('status')=='stalled' and old.get('method_digest')==digest:
            print('REUSED_FINISHED_CHECKPOINT',str(args.output),flush=True);return
        parent=old['record']
    if data.get('closed'):raise ValueError('Do not search a closed source')
    s=Search(parent['st'],parent['j'],parent['positive'],parent.get('limits'),use_planes=True,parent=parent)
    s.omit_generated_rows=True;s.window_affine_only=not args.broad;s.max_full_probes=0
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
        if args.method=='native':closed=s.run()
        else:
            for cycle in range(args.cycles):
                r=s.lp()
                if r.status==2:s.final();closed=True;break
                point=dict(zip(s.names,r.x))
                if args.method=='integer_windows':
                    import numpy as np
                    from scipy.optimize import milp,Bounds,LinearConstraint
                    s.matrices();keep=[i for i,(_,_,label) in enumerate(s.rows) if label not in ('integer CG consequence','complete target-cover consequence')]
                    A=np.vstack([s.A[keep],s.E]);lower=np.r_[np.full(len(keep),-np.inf),s.f];upper=np.r_[s.b[keep],s.f]
                    result=milp(np.zeros(len(s.names)),integrality=np.ones(len(s.names)),bounds=Bounds(np.zeros(len(s.names)),np.full(len(s.names),np.inf)),constraints=LinearConstraint(A,lower,upper),options=dict(time_limit=8,mip_rel_gap=0))
                    print('MIP_DISCOVERY_ONLY',cycle,result.status,flush=True)
                    if result.x is None:break
                    point=dict(zip(s.names,result.x));changed,finished=fw.discover(s,point)
                elif args.method=='coverage':changed,finished=s.full_cover_step(point)
                else:changed,finished={'windows':fw.discover,'source':su.discover,'canonical':cm.discover}[args.method](s,point)
                print('CYCLE',cycle,changed,finished,len(s.trace),flush=True)
                if finished:
                    if args.method!='coverage' or not changed:s.final()
                    closed=True;break
                new=changed;save('progress' if changed else 'stalled')
                if not changed:break
            else:save('budget_reached');return
        save('closed' if closed else 'stalled');print('RESULT',closed,len(s.trace),s.e,round(time.monotonic()-start,2),flush=True)
    except BaseException:save('interrupted');raise

if __name__=='__main__':main()
