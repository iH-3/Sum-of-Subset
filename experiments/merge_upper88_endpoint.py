#!/usr/bin/env python3
"""Merge discovery shards; accept the result only after exact complete verification."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'verification'))
import upper88_endpoint as proof


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inputs', nargs='+', type=Path)
    parser.add_argument('--output', type=Path, default=proof.DEFAULT_CERTIFICATE)
    args = parser.parse_args()
    pool, lookup, roots = [], {}, {}

    def intern(vector):
        signature = tuple(sorted(vector.items()))
        if signature not in lookup:
            lookup[signature] = len(pool)
            pool.append(dict(signature))
        return lookup[signature]

    def remap_tree(tree, remap):
        if set(tree) == {'vector'}:
            tree['vector'] = remap[tree['vector']]
        else:
            proof.require(set(tree) == {'split', 'children'} and len(tree['children']) == 2,
                          'Malformed tree')
            for child in tree['children']:
                remap_tree(child, remap)

    for path in args.inputs:
        bundle = json.loads(path.read_text())
        proof.require(bundle['format'] == proof.FORMAT, 'Wrong format')
        remap = [intern(vector) for vector in bundle['pool']]
        for key, raw in bundle['roots'].items():
            node = deepcopy(raw)
            for item in node['segments']:
                item[2] = remap[item[2]]
            for tree in node['trees'].values():
                remap_tree(tree, remap)
            proof.require(key not in roots or roots[key] == node,
                          'Inconsistent overlapping shard: ' + key)
            roots[key] = node
    merged = dict(format=proof.FORMAT, pool=pool, roots=roots)
    checked = proof.check_coverage(merged)
    proof.require(checked['coverage'] == 'COMPLETE', 'Incomplete merged coverage')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(merged, separators=(',', ':')) + '\n')
    print(json.dumps({k: v for k, v in checked.items()
                      if k not in ('used_vectors', 'proof_checks')},
                     default=proof.base.json_default, indent=2))


if __name__ == '__main__':
    main()
