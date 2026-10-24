"""Replay certified rank slices without calling their original root closed."""
from pathlib import Path
import argparse,gzip,hashlib,json,sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE));ROOT=HERE.parents[1]
import exact,model as m,replay_partial as rp

def verify():
    path=ROOT/'data/upper80_refinements_20261024.json.gz';packet=json.loads(gzip.decompress(path.read_bytes()))
    m.need(packet['format']=='upper80-rank-refinements-v1' and packet['global_upper_bound_certified'] is False and packet['structural_applicability_certified'] is False and packet['closed_original_roots']==0,'Partial rank-refinement scope')
    m.need((packet['j'],packet['pattern_index'],packet['positive'])==(6,436,False),'Rank-refinement root')
    m.need(packet['certified_ranks']==list(range(2,8)) and packet['open_ranks']==[0,1] and len(packet['records'])==5 and len(packet['branches'])==1,'Complete claimed rank inventory with explicit open slices')
    st=([*m.patterns(6),*m.partial_patterns(6)])[436];steps=0
    for k,record in zip(range(3,8),packet['records']):
        m.need(record['st']==st and record['j']==6 and record['positive'] is False and record['limits']=={'rank_k':[k,k]},'Exact certified rank slice')
        steps+=exact.replay(record)['steps']
    branch=packet['branches'][0];m.need(branch['rank']==2 and not branch['open'] and branch['st']==st and branch['j']==6 and branch['positive'] is False,'Closed rank-two subtree')
    seen=set();splits=0
    def visit(node,limits):
        nonlocal splits,steps
        if set(node)=={'leaf'}:
            i=node['leaf'];m.need(type(i) is int and 0<=i<len(branch['leaves']) and i not in seen,'Unique refinement leaf');seen.add(i)
            record=branch['leaves'][i]
            m.need(record['st']==st and record['j']==6 and record['positive'] is False and {k:tuple(v) for k,v in record['limits'].items()}==limits,'Refinement leaf has its exact path domain')
            steps+=exact.replay(record)['steps'];return
        m.need(set(node)=={'variable','threshold','left','right'},'Complementary refinement children')
        name,cut=node['variable'],node['threshold'];lo,hi=limits.get(name,rp.domain(name,branch))
        m.need(type(cut) is int and lo<=cut<hi,'Integer refinement partition')
        left=dict(limits);left[name]=(lo,cut);right=dict(limits);right[name]=(cut+1,hi);splits+=1
        visit(node['left'],left);visit(node['right'],right)
    visit(branch['tree'],{'rank_k':(2,2)})
    m.need(seen==set(range(len(branch['leaves']))),'All refinement leaves referenced')
    return dict(status='PASS_PARTIAL_RANK_REFINEMENTS',global_upper_bound_certified=False,
                structural_applicability_certified=False,closed_original_roots=0,certified_ranks=packet['certified_ranks'],
                open_ranks=packet['open_ranks'],terminal_certificates=5+len(seen),branch_splits=splits,local_steps=steps,packet_sha256=hashlib.sha256(path.read_bytes()).hexdigest())

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args();result=verify()
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
