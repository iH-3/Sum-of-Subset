#!/usr/bin/env python3
"""Verify local improvements, partial certificates and the exact relaxation obstruction.

PASS_PROGRESS_ONLY explicitly does not assert N <= 88. The audited bound remains 89.
"""
import argparse
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import upper88_candidate as proof
ROOT=proof.ROOT
WITNESS=ROOT/'data/upper88_relaxation_witness.json'


def check_witness(data):
    require=proof.require
    require(data['status']=='EXACT_RELAXATION_WITNESS','Wrong witness status')
    g=next((g for g in proof.roots() if g['key']==data['group']['key']),None)
    require(g is not None and json.loads(json.dumps(g))==data['group'],'Noncanonical witness group')
    a=data['a'];require(type(a) is int and g['lo']<=a<=g['hi'],'Invalid integer parameter')
    require(data['kind']=='global_nested','Wrong witness model')
    names,rows=proof.model(g,a,data['kind'])
    require(set(data['point'])==set(names),'Missing or extra witness coordinate')
    point={k:Fraction(v) for k,v in data['point'].items()}
    require(all(v>=0 for v in point.values()),'Negative witness variable')
    def valid(row):
        v,b=row
        return sum(c*point[k] for c,k in zip(v,names))<=b
    require(all(valid(row) for row in rows.values()),'Witness violates a root row')
    branches=proof.branches(g,a,names)
    require(set(data['selected_disjunctions'])==set(branches),'Missing or extra disjunction')
    branch_rows=0
    for label,parts in branches.items():
        choice=data['selected_disjunctions'][label]
        require(type(choice) is int and choice in (0,1),'Invalid branch choice')
        require(all(valid(row) for row in parts[choice]),'Witness violates a selected branch')
        branch_rows+=len(parts[choice])
    return dict(status='EXACT_RELAXATION_WITNESS',group=g['key'],a=a,variables=len(names),
                root_rows=len(rows),disjunctions=len(branches),selected_branch_rows=branch_rows,
                all_arithmetic='fractions.Fraction',
                implication='The current relaxation and all listed dichotomies cannot exclude this root.',
                limitation='This is not a feasible set or a counterexample to the original problem.')


def negative_controls(bundle,witness):
    rejected=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,KeyError):rejected.append(label)
        else:raise ValueError('Invalid input accepted: '+label)
    reject('partial_is_not_full_coverage',lambda:proof.check_coverage(bundle))
    bad=deepcopy(witness);bad['point']['K']='1000000000'
    reject('violated_root_inequality',lambda:check_witness(bad))
    bad=deepcopy(witness);bad['point']['K']='-1'
    reject('negative_witness_coordinate',lambda:check_witness(bad))
    bad=deepcopy(witness);bad['selected_disjunctions'].pop(next(iter(bad['selected_disjunctions'])))
    reject('omitted_disjunction',lambda:check_witness(bad))
    bad=deepcopy(witness);key=next(iter(bad['selected_disjunctions']));bad['selected_disjunctions'][key]=1-bad['selected_disjunctions'][key]
    reject('wrong_branch_choice',lambda:check_witness(bad))
    reject('unproved_cardinality_88',lambda:proof.scalar_audit(88))
    reject('unsupported_prefix_size13',lambda:proof.retained_prefix.witness(17,0,4))
    reject('invalid_outer_pair_order',lambda:proof.ordinary_core_overlap.outer_pair_alternatives('p',3,1))
    g=next(g for g in proof.roots() if g['key'] in bundle['roots'])
    n,r=proof.model(g,proof.Quadratic(0,1),bundle['roots'][g['key']]['kind'])
    reject('negative_certificate_weight',lambda:proof.interval_certificate(n,r,{'Gp':-1},g['lo'],g['hi']))
    reject('noncontradictory_certificate',lambda:proof.interval_certificate(n,r,{'Dp1':1},g['lo'],g['hi']))
    reject('interior_quadratic_failure',lambda:proof.interval_certificate(['x'],{'r':([0],proof.Quadratic(0,2,-1))},{'r':1},-1,3))
    return dict(rejected=rejected)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--exhaustive',action='store_true')
    args=parser.parse_args()
    bundle=json.loads(proof.PARTIAL_CERTIFICATE.read_text())
    proof.require(bundle['status']=='PARTIAL','This progress verifier requires an explicitly partial bundle')
    witness=json.loads(WITNESS.read_text());obstruction=check_witness(witness)
    scalar=proof.scalar_audit()
    checked=proof.check_coverage(bundle,args.exhaustive,partial=True)
    proof.require(checked['used_vectors']==list(range(len(bundle['pool']))),'Unused partial certificate vector')
    groups=list(proof.roots());all_keys={g['key'] for g in groups}
    proof.require(witness['group']['key'] not in bundle['roots'],'Obstructed root falsely marked excluded')
    universe=dict(groups=len(groups),integer_systems=sum(g['hi']-g['lo']+1 for g in groups),
                  covered_groups=len(bundle['roots']),uncovered_groups=len(all_keys-set(bundle['roots'])),
                  complete=False,uncovered_keys_sha256=hashlib.sha256(json.dumps(sorted(all_keys-set(bundle['roots']))).encode()).hexdigest())
    summary=dict(status='PASS_PROGRESS_ONLY',
        conclusion='Audited global bound remains N <= 89; N <= 88 is not proved.',
        local_improvement='R-band cap 329-I -> 313-I; its four-empty family is excluded before covering models.',
        verification_mode='interval-plus-exhaustive' if args.exhaustive else 'symbolic-interval',
        universe=universe,obstruction=obstruction,scalar=scalar['summary'],
        linear={k:v for k,v in checked.items() if k!='proof_checks'},
        retained_prefix=proof.retained_prefix.audit(),ordinary_core_overlap=proof.ordinary_core_overlap.audit(),
        crossing_envelopes=proof.crossing_envelopes.audit(),
        high_grouping={kind:proof.high_group_audit(scalar,kind) for kind in ('coarse','global_nested')},
        negative_controls=negative_controls(bundle,witness))
    modules=[proof,proof.prior,proof.prior.prior,proof.base,proof.nonap_sharp,proof.nonap_inverse,
             proof.nonap_hole_rho,proof.nonap_hole_rho.previous,proof.integral_centers,
             proof.retained_prefix,proof.retained_prefix.previous,proof.ordinary_core_overlap,
             proof.crossing_envelopes,proof.fixed_scores,proof.fixed_score_order]
    paths=[Path(__file__),*[Path(m.__file__) for m in modules],ROOT/'verification/upper99.py',
           ROOT/'verification/verify.py',ROOT/'verification/exact.py',ROOT/'data/fixed_cover_certificate.json',
           proof.PARTIAL_CERTIFICATE,WITNESS]
    out=dict(summary=summary,scalar_audit=scalar,proof_checks=checked['proof_checks'],
             sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,default=proof.base.json_default,indent=2)+'\n')
    print(json.dumps(summary,default=proof.base.json_default,indent=2))


if __name__=='__main__':main()
