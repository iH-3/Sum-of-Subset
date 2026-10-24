"""Run standard-library controls, keeping partial research status explicit."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent

def verify():
    checks={}
    paths=sorted((HERE/'controls_20261024').glob('*.py'))+[HERE/'structure_arithmetic.py',HERE/'positive_holes.py',HERE/'positive_kernel.py',HERE/'combined_holes.py']
    for path in paths:
        command=[sys.executable,'-I','-S','-B']+(['-O'] if sys.flags.optimize else [])+[str(path)]
        result=subprocess.run(command,capture_output=True,text=True)
        if result.returncode:raise ValueError(path.name+' failed:\n'+result.stderr)
        checks[path.stem]=json.loads(result.stdout)
        print('PASS',path.name,flush=True,file=sys.stderr)
    digest=hashlib.sha256(json.dumps(checks,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return dict(status='PASS_NEW_RESEARCH_LEMMA_CONTROLS_ONLY',global_upper_bound_certified=False,
                structural_applicability_certified=False,established_range=[71,81],finite_digest=digest,checks=checks)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args();result=verify()
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
