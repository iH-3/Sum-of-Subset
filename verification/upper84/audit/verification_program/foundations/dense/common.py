"""Shared input validation, with checks that survive Python -O."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def need(condition, message):
    if not condition:
        raise ValueError(message)

def integer(value, minimum=0):
    return type(value) is int and value >= minimum

def tri(n):
    return n * (n + 1) // 2

def load(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def record_bytes(record):
    return (json.dumps(record, sort_keys=True, separators=(',', ':')) + '\n').encode('ascii')

def rejects(function, label):
    try:
        function()
    except (ValueError, KeyError, IndexError, TypeError):
        return label
    raise RuntimeError('Corruption was accepted: ' + label)

def subset_bits(values):
    bits = 1
    for value in values:
        bits |= bits << value
    return bits
