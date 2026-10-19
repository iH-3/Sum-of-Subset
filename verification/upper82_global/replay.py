#!/usr/bin/env python3
"""Replay exact necessary-system certificates. Run check.py for full coverage."""
from collections import Counter
from pathlib import Path
import argparse,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import model as m


def need(ok,message):
    if not ok:raise ValueError(message)


def matrix(rows,eqs):
    counts=Counter();out={}
    for kind,rr in [('le',rows),('eq',eqs)]:
        for row,b,label in rr:
            base=kind+':'+label;key=base+':'+str(counts[base]);counts[base]+=1
            need(all(type(c) is int for c in row.values()) and type(b) is int,'Noninteger matrix')
            out[key]=(row,b,kind)
    return out


def forest_row(label,edges,retained,e):
    need(label.startswith('MST '),'Forest identifier')
    chosen,roots,constants=json.loads(label[4:])
    need(isinstance(chosen,list) and isinstance(roots,list) and isinstance(constants,list),'Forest syntax')
    need(not constants,'Conditional rank constants not implemented in this packet schema')
    need(len(set(chosen))==len(chosen) and all(type(i) is int and 0<=i<len(edges) for i in chosen),'Forest edge index')
    vertices=['Ls','Lt',*retained];parent={v:v for v in vertices}
    def find(v):
        while parent[v]!=v:v=parent[v]
        return v
    for i in chosen:
        x,y,gap=edges[i];a,b=find(x),find(y)
        need(a!=b,'Cyclic forest');parent[a]=b
    comp={}
    for v in vertices:comp.setdefault(find(v),[]).append(v)
    need(len(set(roots))==len(roots) and set(roots)<=set(retained),'Invalid forest root')
    for cc in comp.values():
        lead=sum(v.startswith('L') for v in cc)
        need(lead<=1,'Two leading roots in one component')
        need(sum(v in roots for v in cc)==(0 if lead else 1),'Missing or extra detached root')
    gap=m.add(*[(1,edges[i][2]) for i in chosen]) if chosen else {}
    row=m.add((len(chosen),m.var('FD')),(-1,gap),(1,{'ells':1,'ellt':1}),(1,{'D'+k:1 for k in roots}),(-1,m.var('delta')))
    return row,-e,label


def evaluate(cert,dd,target=None):
    need(isinstance(cert,dict) and set(cert)=={'weights','denominator'},'Certificate fields')
    lhs=Counter();rhs=0;keys=set()
    for key,weight in cert['weights']:
        need(key in dd and key not in keys,'Missing or repeated row '+key);keys.add(key)
        row,b,kind=dd[key]
        need(type(weight) is int and weight!=0 and (kind!='le' or weight>=0),'Certificate sign')
        for name,c in row.items():lhs[name]+=weight*c
        rhs+=weight*b
    if target is None:
        need(cert['denominator'] is None,'Unexpected target scale')
        need(rhs<0,'No strict contradiction')
    else:
        den=cert['denominator'];need(type(den) is int and den>0,'Target scale')
        for name,c in target.items():lhs[name]-=den*c
        need(rhs<=0,'Implication has positive upper bound')
    need(all(c>=0 for c in lhs.values()),'Negative residual coefficient')
    return -rhs


def replay(packet):
    need(packet['schema'] in ('EXPERIMENTAL-exact-discovery-v1','upper82-exact-packet-v1'),'Packet schema')
    m.configure_planes(packet['planes']);count=proofs=0;credits=[]
    for rec in packet['records']:
        st,j,r,w=rec['st'],rec['j'],rec['r'],rec['w'];result=rec['result'];tau=rec.get('tau');limits=rec.get('limits')
        need(result['closed'] is True,'Unclosed record')
        e=8 if m.is_ownerless(st) else 0;extra=[];low=set();high=set()
        forests=result['forests'];need(len(set(forests))==len(forests),'Repeated forest definition')
        references=[result['final']]+[step['certificate'] for stage in result['stages'] for step in stage['steps']]
        used_masks=set()
        for index in references:
            need(type(index) is int and 0<=index<len(packet['certificates']),'Certificate reference')
            for label,_ in packet['certificates'][index]['weights']:
                if label.startswith('le:forest '):used_masks.add(int(label.split(':')[1][7:]))
        forms=m.fixed_forms()
        for stage in [*result['stages'],None]:
            n,rows,eqs=m.build(st,j,r,tau,e,limits,w=w,forest_masks=used_masks)
            if rec.get('scope')=='low_c':
                rows=[row for row in rows if row[2]!='positive core floor']
                rows.append(({'delta':1},74,'low-c bridge'))
            else:need(rec.get('scope','native')=='native','Unknown packet scope')
            rows +=[forest_row(label,m.build.last_edges,m.build.last_retained,e) for label in forests]
            rows +=extra
            if stage is None:
                need(e==result['e'],'Final credit')
                evaluate(packet['certificates'][result['final']],matrix(rows,eqs));proofs+=1;break
            need(stage['e']==e,'Stage credit')
            for step in stage['steps']:
                label=step['label'];need(label in forms and label not in high|low,'Fixed label')
                form=forms[label];cert=packet['certificates'][step['certificate']]
                if step['kind']=='LOW':
                    evaluate(cert,matrix(rows,eqs),form);low.add(label)
                    row=(form,0,'fixed LOW '+label)
                else:
                    need(step['kind']=='HIGH','Fixed sign kind');side='s' if '+' in label else 't'
                    body=m.add((1,form),(-1,m.var('S'+side)))
                    evaluate(cert,matrix(rows+[(body,0,'test fixed HIGH '+label)],eqs));high.add(label)
                    row=({k:-v for k,v in body.items()},0 if 3 in st.values() else -1,'fixed HIGH '+label)
                rows.append(row);extra.append(row);proofs+=1
            touched=sum(bool(set(group)&(high|low)) for group in m.GROUPS)
            e=max(e,len(high)+len(low)-touched)
            need(e==stage['next_e'],'Unjustified fixed credit')
        count+=1;credits.append(e)
    return dict(status='PASS_EXACT_PACKETS_ONLY',global_upper_bound_certified=False,records=count,integer_combinations=proofs,credit_histogram=dict(sorted(Counter(credits).items())),planes=len(packet['planes']))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('packet',type=Path);args=parser.parse_args()
    print(json.dumps(replay(json.loads(args.packet.read_text())),indent=2))

if __name__=='__main__':main()
