"""Extract saved research checkpoints without starting any computation."""
from pathlib import Path
import argparse,json
import record_pool as pool,model as m
ROOT=Path(__file__).resolve().parents[2]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);ap.add_argument('--packet',type=Path,default=ROOT/'data/upper80_last_root_frontier_20261024.json.gz');args=ap.parse_args()
    data=pool.read_gzip(args.packet);m.need(data['format']=='upper80-open-frontier-v1' and data['global_upper_bound_certified'] is False,'Research frontier scope')
    for entry in data['checkpoints']:
        relative=Path(entry['name']+'.json.gz');m.need(not relative.is_absolute() and '..' not in relative.parts,'Relative checkpoint path')
        target=args.destination/relative;target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists():
            m.need(pool.canonical(pool.pack(pool.read_gzip(target)))==pool.canonical(pool.pack(entry['checkpoint'])),'Refuse to overwrite a different, possibly newer checkpoint')
        else:pool.write_gzip(target,entry['checkpoint'])
    (args.destination/'resume_ledger.json').write_text(json.dumps(data['ledger'],indent=2)+'\n')
    print(json.dumps(dict(status='RESTORED_WITHOUT_SEARCH',checkpoints=len(data['checkpoints']),destination=str(args.destination))))
if __name__=='__main__':main()
