"""A restored closed checkpoint must replay with its original row ordering."""
from pathlib import Path
import gzip,json,sys,tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import search_frontier as f,exact
root=Path(__file__).resolve().parents[3]
packet=json.loads(gzip.decompress((root/'data/upper80_refinements_20261024.json.gz').read_bytes()))
record=packet['records'][0]
with tempfile.TemporaryDirectory() as tmp:
    f.ROOT=Path(tmp);relative=Path('.work/upper80/order_control');folder=f.ROOT/relative;folder.mkdir(parents=True)
    path=folder/'proof.json.gz';original=dict(closed=True,record=record)
    path.write_bytes(gzip.compress(f.canonical(original),mtime=0));archive=f.ROOT/'frontier.json.gz'
    stats=f.snapshot([relative],archive);path.unlink();result=f.restore(archive)
    restored=json.loads(gzip.decompress(path.read_bytes()))
    if list(restored['record']['st'])!=list(record['st']):raise ValueError('Frontier reordered pattern rows')
    exact.replay(restored['record']);again=f.restore(archive)
    if again['restored']!=0:raise ValueError('Frontier restore not idempotent')
    changed=dict(original);changed['record']=dict(record,st=dict(reversed(list(record['st'].items()))))
    if f.canonical(changed)==f.canonical(original):raise ValueError('Proof identity ignores row order')
    path.write_bytes(gzip.compress(f.canonical(changed),mtime=0))
    rejected=False
    try:f.restore(archive)
    except ValueError:rejected=True
    if not rejected:raise ValueError('Reordered existing checkpoint accepted')
print(json.dumps(dict(status='PASS_ORDER_PRESERVING_FRONTIER',restored_closed_replays=1,idempotent_restores=1,reordered_checkpoint_rejected=True)))
