"""Verify completed auxiliary improvements only. No proof of N <= 80."""
from pathlib import Path
import hashlib,importlib.util,json,argparse
HERE=Path(__file__).resolve().parent

def load(name):
    spec=importlib.util.spec_from_file_location('upper80_'+name,HERE/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def verify():
    results={name:load(name).verify() for name in ('density','profiles','source_bounds')}
    if any(value.get('global_upper_bound_certified') is not False for value in results.values()):
        raise ValueError('Auxiliary result must not assert a global bound')
    digest=hashlib.sha256(json.dumps(results,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return dict(status='PASS_AUXILIARY_IMPROVEMENTS_ONLY',global_upper_bound_certified=False,
                established_range=[71,81],target_upper_bound=80,finite_digest=digest,checks=results)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args()
    result=verify()
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
