#!/usr/bin/env python3
"""Run the exact, offline verification accompanying the upper-85 report.
Exit 0 means that the requested executable checks passed. It is not a claim
that the complete mathematical theorem has been formally verified.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import sys
import time

from checks import (lower_construction, check_partition, check_polynomial,
                    check_terminal, check_inventory, check_whole_units_and_forests,
                    mutation_tests, check_shared_first_gap, check_fixed_cover, fixed_cover_mutation_tests, check_p4_seeds, check_endpoint_rank_ranges)
from exact_math import equal, verify_linear_certificate, VerificationError

from chapter_checks import (p3_algebra, p3_seed_supports, p3_mutations, z5_endpoint_cards,
                            z5_fixed_ledgers, z5_algebra, z5_mutations)

BASE = Path(__file__).resolve().parent
if sys.version_info < (3,10):
    print('Python 3.10 or later is required.',file=sys.stderr)
    sys.exit(1)

ASSUMPTIONS = [
    {'id':'F-GENERAL','status':'HUMAN_PROOF_OR_EXTERNAL_INPUT',
     'description':'Established upper-86 theorem; rational-kernel existence reduction; subset-sum, stability/inverse and finite-group theorems. Their analytical proofs are not formalized by this program.'},
    {'id':'F-COVER','status':'HUMAN_PROOF',
     'description':'Completeness of the four-extreme source cover and validity of its geometrical pairing. Finite fixed-label arithmetic is checked when included, but does not replace the human covering argument.'},
    {'id':'F-STRUCT','status':'HUMAN_PROOF_PLUS_FINITE_CHECKS',
     'description':'The SIZE86 structural derivation, individual primitivity, lattice and intersection hypotheses. The packaged finite subclaims are recomputed; this program does not derive the structural theorem from all real configurations.'},
    {'id':'F-DENSE','status':'HUMAN_PROOF_PLUS_FINITE_CHECKS',
     'description':'The dense and non-AP finite-to-infinite arguments and the analytical justification of the exact bounded reductions used by the finite checks.'},
    {'id':'G-SOURCE_G-STRIP_G-GAPS_G-END1','status':'HUMAN_PROOF',
     'description':'Source-envelope set arguments, interval localization, actual activity/integrality, clipping/resource ownership, and corrected endpoint-bridge deductions.'},
    {'id':'STRATUM-ANALYTICAL-COVERAGE','status':'HUMAN_PROOF',
     'description':'Exhaustive analytical activity classifications and original-to-local implications in all 13 strata, including resource-role transport. Terminal arithmetic checks certify the supplied inequalities, not their derivation.'}
]


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--quick',action='store_true',help='default: fast exact checks; explicitly skip two large foundation families')
    mode.add_argument('--full',action='store_true',help='recompute all packaged finite foundation families and all arithmetic checks')
    parser.add_argument('--data',type=Path,default=BASE/'data'/'arithmetic.json',help='arithmetic data path, normally the bundled file')
    parser.add_argument('--output-dir',type=Path,default=BASE,help='write coverage.json and verification_log.txt here (default: program directory)')
    args=parser.parse_args(argv)
    selected='full' if args.full else 'quick'
    start=time.perf_counter()
    records=[]
    lines=[]
    def emit(message):
        lines.append(message)
        print(message,flush=True)
    def run(id,description,fn):
        began=time.perf_counter()
        try:
            details=fn()
            record={'id':id,'status':'PASS','description':description,'details':details}
        except Exception as err:
            record={'id':id,'status':'FAIL','description':description,
                    'details':{'error':type(err).__name__+': '+str(err)}}
        record['seconds']=round(time.perf_counter()-began,4)
        records.append(record)
        emit(record['status']+' | '+id+' | '+description)
        if record['status']=='FAIL': emit('  '+record['details']['error'])
        return record['status']=='PASS'
    emit('Upper-85 exact verification | mode: '+selected)
    emit('PASS means a stated executable check passed; analytical dependencies remain explicit.')
    data=None
    def read_data():
        nonlocal data
        data=json.loads(args.data.read_text(encoding='utf-8'))
        if data.get('schema')!='upper85-exact-arithmetic-v1':
            raise VerificationError('Unsupported arithmetic data schema')
        return {'schema':data['schema']}
    run('INPUT-DATA','Read required arithmetic inputs',read_data)
    run('LOWER71','Exact subset sums, exactly four summands and all 12 interval rows',lower_construction)
    def fixed_data():
        return json.loads((BASE/'data/fixed_cover_certificate.json').read_text(encoding='utf-8'))
    run('F-COVER-FIXED','Exact 110-label expansion and 26 disjoint negative-sum group certificate',lambda:check_fixed_cover(fixed_data()))
    run('F-COVER-NEGATIVE','Reject altered fixed-group coefficient and duplicated resource',lambda:fixed_cover_mutation_tests(fixed_data()))
    run('P4-PROPAGATION-SEEDS','Seven exact subset-sum seed supports and propagation mass bounds',lambda:check_p4_seeds(json.loads((BASE/'data/p4_seeds.json').read_text(encoding='utf-8'))))
    run('G-ENDPOINT-RANKS','Exact integer clipping-rank identities and interval inequalities',check_endpoint_rank_ranges)
    run('G-FIRSTGAP','Shared P1/H1 exact first-gap identity, integer ranges and baseline minimum',check_shared_first_gap)
    run('G-FOREST','Original whole-unit inventory and pointwise rooted-resource accounting',check_whole_units_and_forests)
    if data is not None:
        run('C12-PARTITION','13 disjoint exhaustive scalar-domain strata under the stated structure',lambda:check_partition(data))
        run('ARITHMETIC-INVENTORY','Every mandatory polynomial and terminal arithmetic case is present',lambda:check_inventory(data))
        for row in data.get('identities',[]):
            run(row['id'],'Exact symbolic coefficient identity',lambda row=row: (equal(row['left'],row['right']) or {'identity':row['left']+' = '+row['right']}))
        for row in data.get('polynomials',[]):
            run(row['id'],'Exact polynomial expansion, global integer minimum and physical-domain check',lambda row=row:check_polynomial(row))
        for row in data.get('terminals',[]):
            run(row['id'],'Positive terminal contradiction margin under supplied analytical premises',lambda row=row:check_terminal(row))
        for cert in data.get('linear_certificates',[]):
            run('CERT-'+cert['id'],'Exact nonnegative rational combination cancels coefficients and has negative RHS',lambda cert=cert:verify_linear_certificate(cert))
        run('NEGATIVE-CONTROLS','Reject corrupt coefficient, omitted row/case, tampered certificate and zero margin',lambda:mutation_tests(data))
    def appendix_data(name):
        return json.loads((BASE/'data'/name).read_text(encoding='utf-8'))
    run('P3-APPENDIX-ALGEBRA','Detailed P3 baseline and complete A1 exact arithmetic, including m3',lambda:p3_algebra(appendix_data('p3_appendix.json')))
    run('P3-SEEDS','Exact m4 supports and all 2380 thirteen-of-seventeen seed intervals',lambda:p3_seed_supports(appendix_data('p3_appendix.json')))
    run('P3-APPENDIX-NEGATIVE','Reject altered m3 coefficient and omitted A1 step',lambda:p3_mutations(appendix_data('p3_appendix.json')))
    run('Z5-ENDPOINT-CARDS','Exact endpoint bodies, constants, errors and retained-template resource checks',lambda:z5_endpoint_cards(appendix_data('z5_appendix.json')))
    run('Z5-FIXED-LEDGERS','Exact fixed-label credits linked to the independent original-cover certificate',lambda:z5_fixed_ledgers(appendix_data('z5_appendix.json'),fixed_data()))
    run('Z5-APPENDIX-ALGEBRA','Quadratic minima, positive terminals, eliminations and corrected affine reductions',lambda:z5_algebra(appendix_data('z5_appendix.json')))
    run('Z5-APPENDIX-NEGATIVE','Reject endpoint, ledger and affine mutations including obsolete C5 constants',lambda:z5_mutations(appendix_data('z5_appendix.json'),fixed_data()))
    try:
        from foundations import run_checks
        foundation_records=run_checks(mode=selected)
        expected_foundations={'F3_NONAP_2340','F4_BOOTSTRAP_AP','F4_INVERSE','F4_FIXED_WITNESSES','F6_H_PROFILES','F6_H_BANDS','F6_DENSE_BASES','F6_RESTRICTED_DIRECT'}
        if len(foundation_records)!=len(expected_foundations) or {r.get('id') for r in foundation_records}!=expected_foundations:
            raise VerificationError('Foundation checker omitted or duplicated a required finite family')
        for record in foundation_records:
            if selected=='full' and record.get('status')=='SKIP':
                record['status']='FAIL'
                record.setdefault('details',{})['full_mode_error']='A required executable family was skipped in full mode'
            if record.get('status') not in ('PASS','FAIL','SKIP'):
                raise VerificationError('Invalid foundation status')
            records.append(record)
            emit(record['status']+' | '+record['id']+' | '+record.get('description','Foundation check'))
    except Exception as err:
        records.append({'id':'FOUNDATIONS','status':'FAIL','description':'Required finite foundation checker',
                        'details':{'error':type(err).__name__+': '+str(err)}})
        emit('FAIL | FOUNDATIONS | '+str(err))
    failed=[r['id'] for r in records if r['status']=='FAIL']
    skipped=[r['id'] for r in records if r['status']=='SKIP']
    counts={s:sum(r['status']==s for r in records) for s in ('PASS','FAIL','SKIP')}
    duration=round(time.perf_counter()-start,3)
    report={'schema':'upper85-verification-coverage-v1','mode':selected,
            'timestamp_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),
            'platform':platform.platform(),'seconds':duration,
            'requested_executable_checks_passed':not failed,
            'full_theorem_formally_verified':False,
            'result_meaning':'Exact finite checks and conditional arithmetic only. Human and external mathematical inputs remain.',
            'counts':counts,'failed_checks':failed,'skipped_checks':skipped,
            'assumptions_and_human_proofs':ASSUMPTIONS,'checks':records}
    emit('Summary: {PASS} PASS, {FAIL} FAIL, {SKIP} SKIP; {time}s'.format(time=duration,**counts))
    emit('The complete theorem has NOT been formally verified by this program.')
    if failed:
        emit('RESULT: FAIL. One or more requested executable checks failed.')
    else:
        emit('RESULT: All requested executable checks passed'+(' (see explicit quick-mode skips).' if skipped else '.'))
    try:
        args.output_dir.mkdir(parents=True,exist_ok=True)
        (args.output_dir/'coverage.json').write_text(json.dumps(report,indent=2,ensure_ascii=True)+'\n',encoding='utf-8')
        (args.output_dir/'verification_log.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    except OSError as err:
        print('FAIL | OUTPUT | Could not write logs: '+str(err),file=sys.stderr)
        return 1
    return 1 if failed else 0

if __name__=='__main__':
    sys.exit(main())
