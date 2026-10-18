#!/usr/bin/env python3
"""Collect fresh audit outputs without promoting finite checks to a theorem.

The inputs are the directory layout documented in proof_audit_20261018.md.
This is a receipt packager, not an independent mathematical verifier.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['verify', 'review_checks', 'upper103', 'upper100', 'upper99',
         'upper98', 'upper97', 'upper97_simplified', 'upper96', 'upper95',
         'upper94', 'upper93', 'upper92', 'upper91', 'upper90', 'upper89',
         'upper88_progress']


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work-dir', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    args = p.parse_args()
    work, out = args.work_dir.resolve(), args.output_dir.resolve()
    need(not out.exists(), 'Use a fresh output directory')
    files = {}

    def retain(path, label):
        files[label] = path.read_bytes()

    retain(work/'primary_source_receipt.json', 'primary_sources.json')
    guard = read(work/'archive_optimization_guard.json')
    need(guard['status'] == 'PASS_CANONICAL_GUARDS_WITH_INNER_GUARD_LIMITATION'
         and guard['inspected_sources_unchanged'], 'Archive optimization guards changed')
    retain(work/'archive_optimization_guard.json', 'upper86/optimization_guard.json')
    for name in ('upper86_replay.log', 'upper86_clean_replay.log'):
        retain(work/name, 'execution_history/'+name)
    retain(work/'environment_quarantine/receipt.json',
           'execution_history/archive_environment_receipt.json')

    rows = []
    for name in NAMES:
        base = work/('baseline_supported' if name == 'verify' else 'replay')
        a, b = base/(name+'.json'), base/(name+'_optimized.json')
        data = a.read_bytes()
        parsed = json.loads(data)
        status = parsed.get('status', parsed.get('summary', {}).get('status'))
        expected = 'PASS_PROGRESS_ONLY' if name == 'upper88_progress' else 'PASS'
        need(status == expected and data == b.read_bytes(), name+': status or -O mismatch')
        for suffix in ('', '_optimized'):
            receipt = base/(name+suffix+'.receipt.json')
            r = read(receipt)
            need(r['returncode'] == 0 and r['output_sha256'] == sha(data), name+': receipt mismatch')
            retain(receipt, 'chain/'+receipt.name)
        row = dict(name=name, status=status, output_sha256=sha(data), optimized_byte_equal=True)
        refname = 'proof_method' if name == 'upper97_simplified' else name
        refs = sorted((ROOT/'results').glob('*/'+refname+'/result.json*'))
        if refs:
            ref = refs[-1]
            old = ref.read_bytes()
            if ref.suffix == '.gz':
                old = gzip.decompress(old)
            need(old == data, name+': differs from published reference')
            row.update(reference=str(ref.relative_to(ROOT)), reference_byte_equal=True)
        else:
            files['chain/'+name+'.json.gz'] = gzip.compress(data, mtime=0)
        rows.append(row)
    for folder in ('replay', 'baseline_supported', 'driver_smoke', 'final_driver_smoke'):
        summary = work/folder/'replay_summary.json'
        need(read(summary)['sources_unchanged'], folder+': sources changed')
        retain(summary, 'execution_history/'+folder+'.json')
    need(read(work/'driver_smoke/replay_summary.json')['status'] == 'PASS_FINITE_REPLAY_ONLY',
         'Final driver smoke run failed')
    need(read(work/'final_driver_smoke/replay_summary.json')['status'] == 'PASS_FINITE_REPLAY_ONLY',
         'Final reference-aware driver smoke run failed')
    for suffix in ('', '_optimized'):
        for extension in ('.receipt.json', '.stderr', '.stdout'):
            f = work/'replay'/('verify'+suffix+extension)
            retain(f, 'execution_history/initial_'+f.name)

    exhaustive = read(work/'upper89_exhaustive_receipt.json')
    retain(work/'upper89_exhaustive_receipt.json', 'upper89/exhaustive_receipt.json')
    reference = read(work/'replay/upper89.json')
    actual = read(work/'upper89_exhaustive.json')
    # The published sharded driver already performs the complete comparison.
    need(exhaustive.get('status') == 'PASS', 'Exhaustive upper89 replay failed')
    need(actual['summary']['verification_mode'] == 'interval-plus-exhaustive',
         'Wrong exhaustive mode')
    actual['summary']['verification_mode'] = 'symbolic-interval'
    need(reference == actual, 'Upper89 exhaustive and interval output differ')
    for f in sorted((work/'exhaustive_parts').glob('*.json.gz')):
        retain(f, 'upper89/exhaustive_parts/'+f.name)
    geometry = read(work/'upper89_geometry.json')
    need(geometry['status'] == 'PASS_FINITE_GEOMETRY_ONLY', 'Geometry checks failed')
    retain(work/'upper89_geometry.json', 'upper89/geometry.json')

    upper84 = ROOT/'verification/upper84/verification_results'
    r84, r85 = read(upper84/'summary.json'), read(upper84/'retained_full/coverage.json')
    need(r84['status'] == 'PASS' and r84['finite_checks_passed'] == 11
         and r84['full_retained_replay'], 'Upper84 full replay failed')
    need(r85['counts'] == {'PASS': 140, 'FAIL': 0, 'SKIP': 0}
         and r85['mode'] == 'full', 'Retained upper85 replay incomplete')
    for f in sorted(upper84.rglob('*')):
        if f.is_file():
            retain(f, 'upper84/'+str(f.relative_to(upper84)))
    retain(work/'upper84_replay.log', 'upper84/driver.log')

    arc = work/'archive_compositional'
    archive = read(arc/'summary.json')
    need(archive['status'] == 'PASS_FINITE_COMPOSITION_ONLY'
         and archive['complete_finite_replay'], 'Archive finite replay incomplete')
    for f in sorted(arc.rglob('*')):
        if f.is_file():
            retain(f, 'upper86/'+str(f.relative_to(arc)))

    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    source_hashes = {name: sha((ROOT/name).read_bytes()) for name in tracked if name
                     and name.startswith(('verification/', 'data/', 'reports/'))
                     and not name.endswith(('.pdf', '.zip'))}
    driver_hashes = {str(f.relative_to(ROOT)): sha(f.read_bytes())
                     for f in (ROOT/'experiments').glob('*proof_audit.py')}
    for name in ('audit_upper_bound_chain.py', 'audit_archived_upper86.py', 'audit_upper89_geometry.py',
                 'audit_archive_entrypoints.py'):
        f = ROOT/'experiments'/name
        driver_hashes[str(f.relative_to(ROOT))] = sha(f.read_bytes())
    summary = dict(
        status='PASS_LISTED_FINITE_CHECKS_ONLY',
        audited_commit='702b78476185eb1554a1f679c1117f3b2eb8bf25',
        full_theorem_formally_verified=False,
        independent_bound_claim=89, archived_bound_claim=84,
        archived_universal_reduction_audit_complete=False,
        chain=rows, successful_standard_and_optimized_runs=34,
        upper89_exhaustive=exhaustive,
        geometry_checks=sum(geometry['checks'].values()), geometry_cases=geometry['cases'],
        upper84_suites=11, retained_upper85_checks=r85['counts'],
        archived_finite_replay=archive['status'],
        archive_optimization_guard=guard['status'],
        source_sha256=source_hashes, audit_driver_sha256=driver_hashes,
        execution_corrections=[
            'Initial baseline -I startup could not import its sibling exact module; supported -E rerun passed.',
            'Initial extraction inventory included environment residue absent from the original ZIP; preserved outside the immutable extraction.',
            'A serial archive run was interrupted and is not counted as complete; only the fresh compositional run is counted.',
            'Initial chain receipts predate nested status extraction; final statuses above are read from the fresh result files.'
        ])
    out.mkdir(parents=True)
    (out/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    manifest = {name: sha(data) for name,data in sorted(files.items())}
    (out/'evidence_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    with zipfile.ZipFile(out/'evidence.zip', 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name,data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026,10,18,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data, compresslevel=9)
    print(json.dumps({'status': summary['status'], 'evidence_files': len(files),
                      'evidence_zip_sha256': sha((out/'evidence.zip').read_bytes())}))


if __name__ == '__main__':
    main()
