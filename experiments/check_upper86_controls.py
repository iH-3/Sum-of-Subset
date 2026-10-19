#!/usr/bin/env python3
"""Guard controls for the new size-87 replay entry; no endpoint claim alone."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]

def need(ok,message):
    if not ok:raise ValueError(message)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    with tempfile.TemporaryDirectory(prefix='upper86-controls-') as folder:
        work=Path(folder);records=[]
        checks=[('optimized_entry',['-O'],[], 'Run without -O'),
                ('reused_directory',[],['--work-dir',str(work)],'Use a fresh work directory'),
                ('invalid_jobs',[],['--jobs','0'],'jobs must be between 1 and 32')]
        for name,flags,extra,marker in checks:
            result=subprocess.run([sys.executable,*flags,'-I','-S','-B',str(ROOT/'verification/upper86.py'),
                                   '--output',str(work/'unexpected.json'),*extra],capture_output=True)
            need(result.returncode!=0 and marker.encode()in result.stderr,'Guard accepted: '+name)
            need(not(work/'unexpected.json').exists(),'Failed guard wrote success')
            records.append(dict(name=name,rejected=True,returncode=result.returncode,
                                stderr_sha256=hashlib.sha256(result.stderr).hexdigest()))
        normal=work/'normal.json';optimized=work/'optimized.json'
        for flags,dest in [([],normal),(['-O'],optimized)]:
            result=subprocess.run([sys.executable,*flags,'-I','-S','-B',str(ROOT/'verification/upper86_geometry.py'),
                                   '--output',str(dest)],capture_output=True)
            need(result.returncode==0,'Geometry positive control failed')
        need(normal.read_bytes()==optimized.read_bytes(),'Geometry -O differs')
        geometry=json.loads(normal.read_text())
        need(len(geometry['analytic']['negative_controls'])==3,'Missing algebra controls')
        result=dict(status='PASS_GUARDS_AND_OPTIMIZATION_INVARIANCE',guards=records,
                    geometry_negative_controls=geometry['analytic']['negative_controls'],
                    geometry_sha256=hashlib.sha256(normal.read_bytes()).hexdigest())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'])


if __name__=='__main__':main()
