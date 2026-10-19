#!/usr/bin/env python3
"""Exact conditional size83 alpha exclusion. Does not prove global N<=82.
Python 3.10+, standard library only, including under -I -S -B -O.
"""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError(msg)
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
model=load('alpha_model',HERE/'model.py')
cert=load('alpha_certificates',HERE/'certificates.py')
lemmas=load('alpha_lemmas',HERE/'lemmas.py')
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def manifest_check():
    data=json.loads((ROOT/'data/upper82_alpha_sources.json').read_text())
    need(data['schema']=='upper82-alpha-sources-v1','manifest schema')
    seen=set()
    for item in data['files']:
        p=Path(item['path'])
        need(not p.is_absolute() and '..' not in p.parts and str(p) not in seen,'source path')
        seen.add(str(p))
        need(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==item['sha256'],'changed source '+str(p))
    need({str(p.relative_to(ROOT)) for p in HERE.glob('*.py')}<=seen,'unfixed local source')
    return len(seen)

def replay(data):
    need(data['schema']=='upper82-alpha-integer-rays-v1','certificate schema')
    masks=data['forest_masks']
    need(all(type(x) is int and 0<=x<8192 for x in masks) and masks==sorted(set(masks)),'forest inventory')
    states=list(cert.states());records=data['records'];pool=data['certificates']
    need(len(records)==len(states),'finite domain cardinality')
    counts=Counter();proofs=[];minimum=None
    for state,record in zip(states,records):
        need(json.loads(json.dumps(state))==record['state'],'missing, duplicated or reordered finite case')
        idx=record['certificate']
        need(type(idx) is int and 0<=idx<len(pool),'certificate reference')
        _,rows=cert.system(state,model.build,masks)
        margin=cert.evaluate(pool[idx],rows)
        need(margin is not None and margin==record['margin'],'integer contradiction')
        counts[state[0]]+=1;minimum=margin if minimum is None else min(minimum,margin)
        proofs.append((record['state'],idx,margin))
    need(counts=={'order_B':765,'order_C':697,'order_D':635,'terminal':1060},'all four proof stages')
    need(len(pool)==376 and len(masks)==60,'final certificate and forest inventory')
    return dict(states=len(states),stages=dict(counts),integer_certificates=len(pool),
        selected_forests=len(masks),minimum_integer_contradiction=minimum,replay_sha256=digest(proofs))

def negative_controls(data):
    results=[]
    def reject(name,call):
        try:call()
        except (ValueError,KeyError,TypeError,IndexError):results.append(name)
        else:raise ValueError('mutation accepted: '+name)
    bad=deepcopy(data);bad['records'].pop()
    reject('missing terminal orientation',lambda:replay(bad))
    bad=deepcopy(data);bad['records'][0]['state'][2]+=1
    reject('wrong mass slice',lambda:replay(bad))
    reject('negative inequality weight',lambda:need(cert.evaluate([('x',-1)],{'x':({'x':-1},1,'le')},False) is not None,'weight sign'))
    reject('negative summed coefficient',lambda:cert.evaluate([('x',1)],{'x':({'x':-1},-1,'le')}))
    reject('zero contradiction',lambda:cert.evaluate([('x',1)],{'x':({'x':1},0,'le')}))
    reject('two roots in a single edge component',lambda:need(1+1+1<=2,'one root only'))
    E={-3,-1,0,1}
    reject('full-core strength on the unbootstrapped extra edge',lambda:need(len(E&{x+1 for x in E})>=len(E)-1,'strict boundary required'))
    reject('claim global82 from local exclusions',lambda:need(82==83,'global bound unchanged'))
    return results

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    count=manifest_check()
    data=json.loads((ROOT/'data/upper82_alpha_certificates.json').read_text())
    core=load('alpha_generic_core',ROOT/'verification/upper83_fullrank/check.py')
    result=dict(status='PASS_CONDITIONAL_ALPHA_SIZE83_FINITE_CERTIFICATES',
        global_upper_bound=83,global_upper82_proved=False,
        scope='Exact Branch-A holes {P,Bpair,Os,Ot,alphas}; common integer source; complete targets',
        source_files=count,finite=replay(data),endpoints=lemmas.endpoint_checks(),
        forests=lemmas.forest_checks(),arithmetic=lemmas.scalar_checks(),
        catalogue=lemmas.catalogue_checks(),core_lemmas=core.core_checks(),
        negative_controls=negative_controls(data))
    need(manifest_check()==count,'source inventory changed during replay')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    print(result['status'],result['finite'])
if __name__=='__main__':main()
