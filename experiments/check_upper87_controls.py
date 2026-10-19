#!/usr/bin/env python3
"""Small adversarial checks of the exact arithmetic and public launch guard."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    path=args.source.resolve()/'ordinary_verifier.py'
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!='c2ebe9dc385c0e84237cd57a51fc7ce11efffd886b60a618e8003fa129ec3a42':
        raise ValueError('Unexpected frozen arithmetic source')
    spec=importlib.util.spec_from_file_location('upper87_arithmetic_control',path)
    v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    accepted=[]
    def rejects(name,fn):
        try:fn()
        except ValueError:accepted.append(name)
        else:raise ValueError('Negative control accepted: '+name)
    model=([[1]],[-1],[0],['row'],{'x':0})
    v.validate_certificate([['row',1]])
    value,_=v.check_system(model,[['row',1]],v.DOMAIN)
    if value!=1:raise ValueError('Positive arithmetic control failed')
    for name,weights in [('negative_multiplier',[['row',-1]]),
                         ('floating_multiplier',[['row',1.0]]),
                         ('boolean_multiplier',[['row',True]]),
                         ('duplicate_label',[['row',1],['row',1]]),
                         ('empty_certificate',[])]:
        rejects(name,lambda w=weights:v.validate_certificate(w))
    rejects('unknown_current_row',lambda:v.check_system(model,[['absent',1]],v.DOMAIN))
    rejects('negative_combined_coefficient',lambda:v.check_system(
        ([[-1]],[-1],[0],['row'],{'x':0}),[['row',1]],v.DOMAIN))
    rejects('nonstrict_rhs',lambda:v.check_system(
        ([[1]],[0],[0],['row'],{'x':0}),[['row',1]],v.DOMAIN))
    rejects('floating_matrix',lambda:v.check_system(
        ([[1.0]],[-1],[0],['row'],{'x':0}),[['row',1]],v.DOMAIN))
    rejects('floating_rhs',lambda:v.check_system(
        ([[1]],[-1.0],[0],['row'],{'x':0}),[['row',1]],v.DOMAIN))
    command=[sys.executable,'-O','-I','-S','-B',str(ROOT/'verification/upper87.py')]
    guard=subprocess.run(command,capture_output=True)
    if guard.returncode==0 or b'Run without -O' not in guard.stderr:
        raise ValueError('Optimized public entry was not rejected')
    accepted.append('optimized_public_entry_rejected')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(dict(status='PASS',negative_controls=accepted,
        optimized_guard=dict(command=command,returncode=guard.returncode,
        stderr=guard.stderr.decode()),arithmetic_source_sha256=hashlib.sha256(raw).hexdigest(),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n')
    print('PASS',len(accepted),'negative controls')


if __name__=='__main__':main()
