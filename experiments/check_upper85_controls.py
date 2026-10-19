#!/usr/bin/env python3
"""Reject invalid strengthened constants, omitted cases, and changed inputs."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def module(path,source=None):
    ns={'__name__':'negative_control','__file__':str(path)}
    exec(compile(source if source is not None else path.read_text(encoding='utf-8'),str(path),'exec'),ns)
    return ns


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();records=[]
    path=ROOT/'verification/upper85_geometry.py';source=path.read_text(encoding='utf-8')
    def reject(name,fn):
        try:fn()
        except ValueError as err:records.append({'id':name,'status':'REJECTED','reason':str(err)})
        else:raise ValueError('Accepted invalid mutation: '+name)
    for name,old,new,fn in [
        ('A_holes_overstated','tt-56 >= 2*M-34','tt-56 >= 2*M-33','zero_missing'),
        ('B_holes_overstated','2*ts0-57 >= 4*M-21','2*ts0-57 >= 4*M-20','zero_missing'),
        ('even_rounding_premature',"need(value>134,'new universal terminal bound')", "need(value>135,'new universal terminal bound')",'adaptive'),
        ('Z5_card_omitted',"patterns=[{'alpha'+p,'alpha'+t}","patterns=[{'nonexistent_resource'}",'activity')]:
        if source.count(old)!=1:raise ValueError('Mutation target changed: '+name)
        changed=source.replace(old,new)
        reject(name,lambda changed=changed,fn=fn:module(path,changed)[fn]())
    runner=module(ROOT/'verification/upper85.py')
    manifest=json.loads((ROOT/'data/upper85_adoption_sources.json').read_text())
    changed=copy.deepcopy(manifest);changed['files'][0]['sha256']='0'*64
    reject('source_byte_identity',lambda:runner['validate'](changed))
    changed=copy.deepcopy(manifest)
    changed['files']=[x for x in changed['files'] if x['path']!='verification/upper85_geometry.py']
    reject('new_checks_omitted',lambda:runner['validate'](changed))
    result={'status':'PASS_NEGATIVE_CONTROLS','mutations_rejected':len(records),'records':records,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result['status'])


if __name__=='__main__':main()
