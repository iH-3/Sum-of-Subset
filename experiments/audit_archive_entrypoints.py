#!/usr/bin/env python3
"""Check archived optimization guards without running an optimized proof.

The documented full entrypoints must reject -O. The older internal size-89
entrypoint has an assertion-only guard, which Python itself erases under -O.
This limitation does not invalidate an unoptimized run through the full guards.
"""
import argparse
import ast
import dis
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    root = args.source.resolve()
    relative = ['verify_complete_upper86.py',
                'payload/subset_sum_verification/verify_all.py',
                'payload/subset_sum_verification/proofs/exact88/verify_exact88.py']
    before = {name: digest(root/name) for name in relative}
    records = []
    for name, message in zip(relative[:2], ('ordinary unoptimized Python', 'Python optimization')):
        command = [sys.executable, '-I', '-S', '-B', '-O', str(root/name)]
        result = subprocess.run(command, capture_output=True, text=True)
        need(result.returncode == 2 and message in result.stdout+result.stderr,
             'Canonical entry did not explicitly reject optimized Python')
        records.append(dict(path=name, command=command, exit_code=result.returncode,
                            stdout=result.stdout, stderr=result.stderr, sha256=before[name]))
    source = root/relative[2]
    guards = [n for n in ast.walk(ast.parse(source.read_text()))
              if isinstance(n, ast.Assert) and isinstance(n.test, ast.Name)
              and n.test.id == '__debug__']
    need(len(guards) == 1, 'The archived internal guard changed; review it again')
    node = guards[0]
    module = ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[]))
    code = compile(module, str(source), 'exec', optimize=1)
    exec(code, {})  # Only the isolated assertion is executed, not the proof.
    opcodes = [i.opname for i in dis.get_instructions(code)]
    need('LOAD_ASSERTION_ERROR' not in opcodes, 'Unexpected optimized assertion')
    need(before == {name: digest(root/name) for name in relative}, 'Source changed')
    result = dict(status='PASS_CANONICAL_GUARDS_WITH_INNER_GUARD_LIMITATION',
                  canonical_entry_checks=records,
                  inner=dict(path=relative[2], line=node.lineno,
                             source_sha256=before[relative[2]], guard=ast.unparse(node),
                             optimized_guard_raises=False, optimized_opcodes=opcodes),
                  scope=__doc__, inspected_sources_unchanged=True,
                  optimized_full_proof_attempted=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'])


if __name__ == '__main__':
    main()
