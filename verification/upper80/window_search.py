"""Checkpointed discovery of new complete-window consequences.

Existing finished checkpoints with the same method digest are reused. An
unfinished checkpoint becomes the premise for continuation, so proved cuts
are retained. This script is a search aid, not a verification command.
"""
from pathlib import Path
import argparse,gzip,hashlib,json,time
import fast_lp
fast_lp.install()
from discover import Search
import full_window as fw

def read(path):return json.loads(gzip.decompress(path.read_bytes()))
def digest(value):return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('output',type=Path);ap.add_argument('--cycles',type=int,default=30);args=ap.parse_args()
    method=hashlib.sha256(Path(fw.__file__).read_bytes()).hexdigest();data=read(args.source);parent=data['record'];initial=digest(parent)
    if args.output.exists():
        old=read(args.output)
        if old.get('closed') or old.get('status')=='stalled' and old.get('method_digest')==method:
            print(json.dumps(dict(status='REUSED_FINISHED_CHECKPOINT',output=str(args.output))),flush=True);return
        parent=old['record']
    if data.get('closed'):
        raise ValueError('Do not search an already closed source')
    s=Search(parent['st'],parent['j'],parent['positive'],parent.get('limits'),use_planes=True,parent=parent)
    s.omit_generated_rows=True;s.window_affine_only=True;start=time.monotonic();point=None;cycle=-1
    def save(status):
        result=dict(record=s.record(),point=point,closed=status=='closed',status=status,source_digest=initial,method_digest=method,cycle=cycle)
        temp=args.output.with_suffix('.tmp');temp.write_bytes(gzip.compress(json.dumps(result,separators=(',',':')).encode(),mtime=0));temp.replace(args.output)
    try:
        for cycle in range(args.cycles):
            result=s.lp()
            if result.status==2:s.final();save('closed');print('CLOSED',cycle,flush=True);return
            point=dict(zip(s.names,result.x));changed,finished=fw.discover(s,point)
            if finished:s.final();save('closed');print('CLOSED',cycle,flush=True);return
            save('progress' if changed else 'stalled');print('WINDOW',cycle,changed,len(s.trace),round(time.monotonic()-start,2),flush=True)
            if not changed:return
        save('budget_reached')
    except BaseException:
        save('interrupted');raise
if __name__=='__main__':main()
