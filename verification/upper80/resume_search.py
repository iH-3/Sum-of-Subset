"""Resume one original root or one rank slice from restored checkpoints."""
from pathlib import Path
import argparse,json,sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE));ROOT=HERE.parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('j',type=int);parser.add_argument('index',type=int)
    parser.add_argument('--positive',action='store_true');parser.add_argument('--rank',type=int)
    parser.add_argument('--hole-W',type=int,dest='hole_W');parser.add_argument('--parent',type=Path)
    parser.add_argument('--integer-priority',type=int,default=3000)
    parser.add_argument('--integer-first',action='store_true');parser.add_argument('--cache',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    import fast_lp;fast_lp.install()
    import model as m,replay_partial as rp
    from branch_discover import Branch
    st=([*m.patterns(args.j),*m.partial_patterns(args.j)])[args.index]
    obj=Branch(st,args.j,args.positive);obj.prefix_dir=args.cache;obj.prefix_dir.mkdir(parents=True,exist_ok=True)
    obj.integer_first=args.integer_first;obj.integer_priority=args.integer_priority
    limits={} if args.rank is None else {'rank_k':[args.rank,args.rank]}
    if args.hole_W is not None:
        lo,hi=rp.domain('hole_W',dict(j=args.j,positive=args.positive));m.need(lo<=args.hole_W<=hi,'Hole slice domain')
        limits['hole_W']=[args.hole_W,args.hole_W]
    if args.rank is not None:
        lo,hi=rp.domain('rank_k',dict(j=args.j,positive=args.positive));m.need(lo<=args.rank<=hi,'Rank slice domain')
    parent=json.loads(args.parent.read_text()) if args.parent else None
    tree=obj.visit(limits,parent=parent)
    result=dict(st=st,j=args.j,positive=args.positive,initial_limits=limits,tree=tree,leaves=obj.leaves,open=obj.opens,
                global_upper_bound_certified=False,structural_applicability_certified=False)
    if not obj.opens:result['replay_counts']=rp.branch(result,limits)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,separators=(',',':'))+'\n')
    print(json.dumps(dict(nodes=obj.count,leaves=len(obj.leaves),open_leaves=len(obj.opens),rank=args.rank,global_upper_bound_certified=False)))

if __name__=='__main__':main()
