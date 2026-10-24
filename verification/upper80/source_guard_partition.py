"""Two complementary integer branches at a missing source-hull license.

This is an explicitly partial continuation. It never increments the original
root count. Its frozen plan and final child paths permit later exact tree
assembly, and every completed stage is retained and skipped on restart.
"""
from pathlib import Path
import sys,argparse,json,math
import fast_lp
fast_lp.install()
import model as m,record_pool as pool,continue_frontier
from discover import Search

def normalize(row):
    out=dict(row)
    for side,sign in [('s',-1),('t',1)]:
        c=out.pop('M'+side,0)
        if c:out=m.add((1,out),(c,{'R'+side:1,'e'+side:1}))
        c=out.pop('R'+side,0)
        if c:out=m.add((1,out),(c,{'ONE':32,'rank_k':sign,'x'+side:1}))
    out={k:v for k,v in out.items() if v};g=0
    for v in out.values():g=math.gcd(g,abs(v))
    m.need(g>0 and all(type(v) is int for v in out.values()),'Nonzero integer source guard')
    return {k:v//g for k,v in sorted(out.items())}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('directory',type=Path);ap.add_argument('--index',type=int,default=0);args=ap.parse_args()
    value=pool.read_gzip(args.source)
    if value.get('closed'):print('SKIPPED_CLOSED_PARENT',flush=True);return
    base=value['record'];suggestions=value['source_split_candidates'];m.need(0<=args.index<len(suggestions),'Saved missing source guard')
    guard=normalize(suggestions[args.index]['guard']);variable='linear_cut:'+json.dumps(guard,sort_keys=True,separators=(',',':'))
    m.need(variable not in (base.get('limits') or {}),'This guard is already split in the parent')
    args.directory.mkdir(parents=True,exist_ok=True);plan=dict(parent_merkle=pool.record_digest(base),guard=guard,variable=variable,threshold=0,source=str(args.source))
    path=args.directory/'plan.json'
    if path.exists():m.need(json.loads(path.read_text())==plan,'Changed source partition: use a new directory')
    else:path.write_text(json.dumps(plan,indent=2)+'\n')
    print('NEW_COMPLEMENTARY_SOURCE_GUARD',json.dumps(guard),flush=True);results=[]
    for bit in (0,1):
        limits=dict(base.get('limits') or {});limits[variable]=[bit,bit];current=args.directory/f'{bit}_parent.json.gz'
        if not current.exists():
            search=Search(base['st'],base['j'],base['positive'],limits,use_planes=True,parent=base)
            pool.write_gzip(current,dict(record=search.record(),closed=False,status='complementary_source_guard',bit=bit))
        else:
            saved=pool.read_gzip(current)['record'];m.need(saved['limits']==limits and pool.record_digest(saved['premise'])==plan['parent_merkle'],'Frozen source branch parent')
        for method in ['canonical_tail','trimmed_source','native','tail_cap_windows']:
            target=args.directory/f'{bit}_{method}.json.gz';sys.argv=['continue_frontier',str(current),str(target),'--method',method]
            continue_frontier.main();child=pool.read_gzip(target);current=target
            if child['closed']:print('CLOSED_SOURCE_GUARD_CHILD',bit,method,flush=True);break
        results.append(dict(bit=bit,closed=child['closed'],path=str(current)))
        summary=dict(plan=plan,children=results,closed=len(results)==2 and all(x['closed'] for x in results),global_upper_bound_certified=False)
        (args.directory/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
        print('FINAL_SOURCE_GUARD_CHILD',bit,child['closed'],current,flush=True)

if __name__=='__main__':main()
