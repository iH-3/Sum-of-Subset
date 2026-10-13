#!/usr/bin/env python3
"""Reassemble the unchanged historical ZIP and optionally extract it locally."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

p=argparse.ArgumentParser(description=__doc__)
p.add_argument("--destination",type=Path,default=Path(".work/upper86"))
p.add_argument("--keep-zip",action="store_true")
args=p.parse_args()
root=Path(__file__).resolve().parents[1]
arc=root/"archive/upper86"
manifest=json.loads((arc/"manifest.json").read_text())
args.destination.mkdir(parents=True,exist_ok=True)
joined=args.destination/manifest["original_name"]
digest=hashlib.sha256()
size=0
with joined.open("wb") as out:
    for item in manifest["parts"]:
        part=arc/item["name"]
        local=hashlib.sha256()
        count=0
        with part.open("rb") as src:
            while chunk:=src.read(1024*1024):
                out.write(chunk);digest.update(chunk);local.update(chunk);count+=len(chunk)
        if count!=item["bytes"] or local.hexdigest()!=item["sha256"]:
            raise RuntimeError("Invalid archive part: "+item["name"])
        size+=count
if size!=manifest["bytes"] or digest.hexdigest()!=manifest["sha256"]:
    raise RuntimeError("Reassembled ZIP does not match the original.")
with zipfile.ZipFile(joined) as z:
    base=args.destination.resolve()
    for member in z.infolist():
        target=(base/member.filename).resolve()
        if not target.is_relative_to(base):
            raise RuntimeError("Unsafe ZIP member path.")
    z.extractall(base)
if not args.keep_zip:
    joined.unlink()
print("Original ZIP verified and extracted to",args.destination.resolve())
print("This verifies file identity only. Run verify_complete_upper86.py for mathematical replay.")
