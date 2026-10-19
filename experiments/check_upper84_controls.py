#!/usr/bin/env python3
"""Deliberate false claims and source omissions must be rejected."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[1]


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    g=runpy.run_path(str(ROOT/'verification/upper84_geometry.py'))
    v=runpy.run_path(str(ROOT/'verification/upper84_adoption.py'))
    m=json.loads((ROOT/'data/upper84_adoption_sources.json').read_text())
    records=[]
    def rejected(name,fn):
        try:fn()
        except ValueError as error:records.append(dict(id=name,status='REJECTED',reason=str(error)))
        else:raise ValueError('mutation accepted: '+name)
    rejected('source_cap_161',lambda:g['source_cap'](161))
    rejected('A_hole_offset_11',lambda:g['no_empty'](11))
    rejected('terminal_114',lambda:g['adaptive'](114))
    rejected('alpha_margin_17',lambda:g['analytic_alpha'](17))
    bad=copy.deepcopy(m);bad['files'][0]['sha256']='0'*64
    rejected('changed_source_identity',lambda:v['validate'](bad))
    bad2=copy.deepcopy(m);bad2['files']=[e for e in bad2['files'] if e['path']!='verification/upper84_geometry.py']
    rejected('new_geometry_omitted',lambda:v['validate'](bad2))
    bad3=copy.deepcopy(m);bad3['files']=[e for e in bad3['files'] if e['path']!='verification/upper84/progress85/p2/check85_p2.py']
    rejected('legacy_module_omitted',lambda:v['validate'](bad3))
    out=dict(status='PASS_NEGATIVE_CONTROLS',mutations_rejected=len(records),records=records,
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(out['status'])


if __name__=='__main__':main()
