"""Exact arithmetic and domain coverage of an explicitly PARTIAL research model.

This cannot establish a global N bound, even if all currently stored roots close:
the companion research checkpoint lists unresolved structural applicability.
"""
from pathlib import Path
from collections import Counter
from math import isqrt
import sys,gzip,json,argparse
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(HERE))
import model as m,exact

def key(r):return r['j'],r['positive'],tuple(sorted(r['st'].items()))

def load_packet():
    packet=json.loads(gzip.decompress((ROOT/'data/upper80_partial_research.json.gz').read_bytes()))
    m.need(packet.get('format')=='upper80-partial-research-v1' and packet.get('global_upper_bound_certified') is False,'Partial packet scope')
    pool=[]
    def expand(record):
        r=dict(record);m.need('premise' not in r,'Unpooled premise');i=r.pop('premise_ref',None)
        if i is not None:
            m.need(type(i) is int and 0<=i<len(pool),'Forward premise or cycle');r['premise']=pool[i]
        return r
    for r in packet['premises']:pool.append(expand(r))
    packet['records']=[expand(r) for r in packet['records']]
    packet['branches']=[dict(b,leaves=[expand(r) for r in b['leaves']]) for b in packet['branches']]
    return packet

def domain(name,root):
    if name=='rank_k':return 0,min(17,isqrt(496-73*root['j']-(60 if root['positive'] else 0)))
    if name=='hole_W':return (1,7) if root['positive'] else (0,0)
    if name in ('Bs','Bt'):return 4,10
    if name.startswith(('order:','compression:','diameter:','hit:','extended_hit:','trim_pair:')):return 0,1
    m.need(name[:1] in ('l','u') and root['st'].get(name[1:])==1,'Unknown integer branch domain')
    return 0,72

def branch(root):
    m.need(not root.get('open'),'Stored branch tree is incomplete');seen=set();splits=0
    def visit(node,limits):
        nonlocal splits
        if set(node)=={'leaf'}:
            i=node['leaf'];m.need(type(i) is int and 0<=i<len(root['leaves']) and i not in seen,'Leaf index')
            r=root['leaves'][i];seen.add(i);m.need(key(r)==key(root),'Leaf root changed')
            m.need({k:tuple(v) for k,v in (r.get('limits') or {}).items()}==limits,'Leaf domain does not equal branch path')
            exact.replay(r);return
        m.need(set(node)=={'variable','threshold','left','right'},'Missing complementary branch')
        name,cut=node['variable'],node['threshold'];lo,hi=limits.get(name,domain(name,root))
        m.need(type(cut) is int and lo<=cut<hi,'Noncomplementary integer split')
        left=dict(limits);left[name]=(lo,cut);right=dict(limits);right[name]=(cut+1,hi)
        splits+=1;visit(node['left'],left);visit(node['right'],right)
    visit(root['tree'],{})
    m.need(seen==set(range(len(root['leaves']))),'Unreferenced leaves')
    return len(seen),splits

def verify():
    packet=load_packet();expected=set()
    for j in range(1,7):
        for positive in ((False,) if j==6 else (False,True)):
            for st in [*m.patterns(j),*m.partial_patterns(j)]:
                k=key(dict(j=j,positive=positive,st=st));m.need(k not in expected,'Duplicate catalogue root');expected.add(k)
    inventory=[key(r) for name in ('records','branches','open') for r in packet[name]]
    m.need(len(inventory)==len(set(inventory)) and set(inventory)==expected and len(expected)==4654,'Complete research inventory including explicit open roots')
    terminals=splits=0
    for i,r in enumerate(packet['records']):
        m.need(not r.get('limits'),'Restricted direct root');exact.replay(r);terminals+=1
        if i%500==0:print('REPLAY',i,'direct records',flush=True)
    for r in packet['branches']:
        n,s=branch(r);terminals+=n;splits+=s;print('BRANCH',r['j'],n,'leaves',flush=True)
    return dict(status='PASS_PARTIAL_RESEARCH_REPLAY',global_upper_bound_certified=False,
                structural_applicability_certified=False,uniform_roots=len(expected),
                closed_roots=len(packet['records'])+len(packet['branches']),open_roots=len(packet['open']),
                terminal_certificates=terminals,branch_splits=splits,
                open_inventory=[dict(j=r['j'],pattern_index=r['i'],positive=r['positive']) for r in packet['open']])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output');args=p.parse_args();result=verify()
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
