"""Exhaustive finite-domain coverage and exact terminal-certificate replay."""
from pathlib import Path
from collections import Counter
import hashlib,json,gzip
import model as m
import exact
ROOT=Path(__file__).resolve().parents[2]


def key(rec):
    return rec['j'],rec['positive'],tuple(sorted(rec['st'].items()))


def expected():
    roots={};by_j={};total=0
    for j in range(1,7):
        full=list(m.patterns(j));partial=list(m.partial_patterns(j));patterns=full+partial
        m.need(len({tuple(sorted(st.items())) for st in patterns})==len(patterns),'Duplicate generated pattern')
        count=0
        for positive in ((False,) if j==6 else (False,True)):
            for st in patterns:
                root=dict(j=j,positive=positive,st=st);roots[key(root)]=root
                for r in range(15,33):
                    for w in (range(2,15,2) if positive else (0,)):
                        if (32-r)*(33-r)+(59+2*w if positive else 0)<=483-74*j+w:count+=1
        by_j[str(j)]=dict(full=len(full),partial=len(partial),parameter_roots=count)
        total+=count
    m.need(len(roots)==4654 and total==121403,'Full size82 parameter census')
    return roots,by_j,total


def domain(variable,root):
    if variable in ('rank_k','hole_W'):
        return (0,17) if variable=='rank_k' else ((1,7) if root['positive'] else (0,0))
    if variable in ('Bs','Bt'):return (4,10)
    if variable.startswith('compression:'):
        pieces=variable.split(':');m.need(len(pieces)==5,'Branch compression syntax')
        _,source,a,b,kk=pieces
        m.need(source in ('core','source') and kk.isdigit() and 0<=int(kk)<(66 if source=='core' else 74),'Branch compression source')
        return (0,1)
    if variable.startswith('order:'):
        parts=variable.split(':')
        m.need(len(parts)==4,'Branch order key')
        _,first,second,side=parts
        m.need(first in ('alpha','beta') and second=='C5' and side in ('s','t'),'Branch order names')
        m.need(root['st'].get(first+side)==root['st'].get(second+side)==1,'Branch order active resources')
        return (0,1)
    m.need(variable[:1] in ('l','u') and root['st'].get(variable[1:])==1,'Unlicensed branch variable')
    return (0,73)


def branch(root):
    m.need(not root.get('open'),'Unproved open branch')
    leaves=root['leaves'];seen=set();stats=Counter();terminal=[]
    def visit(node,limits):
        if set(node)=={'leaf'}:
            i=node['leaf'];m.need(type(i) is int and 0<=i<len(leaves) and i not in seen,'Branch leaf reference')
            seen.add(i);rec=leaves[i]
            m.need(key(rec)==key(root),'Branch leaf root')
            actual={k:tuple(v) for k,v in (rec.get('limits') or {}).items()}
            m.need(actual==limits,'Branch leaf changed its path domain')
            result=exact.replay(rec);stats.update(result);stats['leaves']+=1;terminal.append(rec)
            return
        m.need(set(node)=={'variable','threshold','left','right'},'Branch node syntax')
        name=node['variable'];cut=node['threshold'];lo,hi=limits.get(name,domain(name,root))
        m.need(type(cut) is int and lo<=cut<hi,'Noncomplementary integer branch')
        if name.startswith('compression:'):
            import parametric as p
            saved=p.USE_PLANES;p.USE_PLANES=False
            try:
                p.build(root['st'],root['j'],root['positive'],8 if m.is_ownerless(root['st']) else 0,limits)
                _,_,a,b,_=name.split(':')
                m.need(sum((u,v)==(a,b) for u,v,_ in p.build.last_edges)==1,'Compression split has no parent-domain edge')
            finally:p.USE_PLANES=saved
        left=dict(limits);left[name]=(lo,cut);right=dict(limits);right[name]=(cut+1,hi)
        stats['splits']+=1;visit(node['left'],left);visit(node['right'],right)
    visit(root['tree'],{})
    m.need(seen==set(range(len(leaves))),'Unreferenced branch leaf')
    return stats,terminal


def load_packet(path=None):
    path=ROOT/'data/upper81_certificates.json.gz' if path is None else Path(path)
    raw=gzip.decompress(path.read_bytes()) if path.suffix=='.gz' else path.read_bytes()
    packet=json.loads(raw);m.need(packet.get('format')=='upper81-exact-v1','Packet format')
    if 'premises' not in packet:return packet
    pool=[];links=[];used=set()
    def expand(record,maximum):
        m.need('premise' not in record,'Embedded premise in pooled packet')
        out=dict(record);index=out.pop('premise_ref',None)
        if index is not None:
            m.need(type(index) is int and 0<=index<maximum,'Premise reference or cycle')
            out['premise']=pool[index]
        return out,index
    for item in packet['premises']:
        rec,parent=expand(item,len(pool));pool.append(rec);links.append(parent)
    def root_record(record):
        rec,index=expand(record,len(pool))
        while index is not None and index not in used:
            used.add(index);index=links[index]
        return rec
    packet['records']=[root_record(r) for r in packet['records']]
    packet['branches']=[dict(r,leaves=[root_record(leaf) for leaf in r['leaves']]) for r in packet['branches']]
    m.need(used==set(range(len(pool))),'Unused premise records')
    return packet


def verify(path=None,verbose=False):
    packet=load_packet(path)
    roots,by_j,total=expected();inventory(packet,roots);seen=set();stats=Counter();digest=hashlib.sha256()
    for kind in ('records','branches'):
        for rec in packet[kind]:
            k=key(rec);m.need(k in roots and k not in seen,'Extraneous or repeated root');seen.add(k)
            if kind=='records':
                m.need(not rec.get('limits'),'Direct root has a restricted domain')
                result=exact.replay(rec);stats.update(result);stats['leaves']+=1;stats['direct_roots']+=1
            else:
                result,_=branch(rec);stats.update(result);stats['branch_roots']+=1
            digest.update(json.dumps(rec,sort_keys=True,separators=(',',':')).encode())
            if verbose and (len(seen)%500==0 or kind=='branches'):
                print('REPLAY',len(seen),'/',len(roots),'roots;',stats['leaves'],'terminal certificates',flush=True)
    m.need(seen==set(roots),'Missing root states: '+str(len(set(roots)-seen)))
    return dict(status='PASS_ALL_SIZE82_TERMINALS',uniform_roots=len(roots),parameter_roots=total,
                by_j=by_j,statistics=dict(stats),certificate_digest=digest.hexdigest())


def inventory(packet,roots=None):
    roots=expected()[0] if roots is None else roots
    seen=set()
    for kind in ('records','branches'):
        for rec in packet[kind]:
            k=key(rec);m.need(k in roots and k not in seen,'Extraneous or repeated root');seen.add(k)
    m.need(seen==set(roots),'Missing root states: '+str(len(set(roots)-seen)))
    return len(seen)

if __name__=='__main__':print(json.dumps(verify(),indent=2))
