"""Import new verified facts into a finished partial tree without restarting it.

Closed leaves retain their certificates. Appending rows shifts only the row
indices of branch assumptions; all previously closed branches are skipped.
Open nodes are reconsidered under the strictly stronger, recorded premises.
"""
from pathlib import Path
import sys,copy,hashlib,json
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'verification/upper80'))
import record_pool as pool,exact,model as m,record_consequences as rc
from discover import Search

def prepare(old_path,source_path,target):
    m.need(not target.exists(),'Do not overwrite a strengthened joint checkpoint')
    packet=pool.read_gzip(old_path);source=pool.read_gzip(source_path)
    m.need(not source['closed'] and not packet['tree']['closed'],'Only open domains require further discovery')
    old=packet['record'];record=source['record'];rc.domain_contains(record,old)
    m.need(all(record[k]==old[k] for k in ('st','j','positive')),'Same physical original root')
    state=exact.replay(record,False,True)
    seen={(tuple(sorted(a.items())),b) for a,b,_ in packet['system_rows']};indices=[]
    for i,(row,b,_) in enumerate(state['facts']):
        key=(tuple(sorted(row.items())),b)
        if key not in seen:indices.append(i);seen.add(key)
    step=dict(kind='record_consequences',record=record,facts=indices)
    prior=exact.replay(old,False,True);credit=state['credit']
    if credit>prior['credit']:step['credit']=credit
    extra=rc.derive(step,old)
    if 'credit' in step:
        s=Search(old['st'],old['j'],old['positive'],old.get('limits'),use_planes=True,parent=old)
        extra.extend(exact.credit_rows(s.ret,credit))
    m.need(extra,'No new premises: do not revisit completed open nodes')
    offset=len(packet['system_rows']);delta=len(extra);tree=copy.deepcopy(packet['tree']);counts={'reused_closed_leaves':0,'strengthened_open_nodes':0}
    def remap(value):
        if isinstance(value,list):
            for child in value:remap(child)
        elif isinstance(value,dict):
            if 'weights' in value:
                value['weights']=[[kind,i+delta if kind=='r' and i>=offset else i,w] for kind,i,w in value['weights']]
            for key,child in value.items():
                if key!='weights':remap(child)
    def walk(node):
        if node['closed']:
            remap(node)
            def leaves(v):return sum(leaves(c['child']) for c in v['children']) if 'children' in v else 1
            counts['reused_closed_leaves']+=leaves(node);return
        node['pending']=True;counts['strengthened_open_nodes']+=1
        for child in node.get('children',[]):walk(child['child'])
    walk(tree)
    packet.update(record=dict(old,trace=[*old['trace'],step]),system_rows=[*packet['system_rows'],*extra],tree=tree,status='new_verified_premises',finished_depth=0)
    packet['strengthening']=dict(old_checkpoint_sha256=hashlib.sha256(old_path.read_bytes()).hexdigest(),source_checkpoint_sha256=hashlib.sha256(source_path.read_bytes()).hexdigest(),imported_facts=len(indices),appended_rows=delta,old_credit=prior['credit'],new_credit=credit,**counts)
    pool.write_gzip(target,packet);print(json.dumps(packet['strengthening']),flush=True)

if __name__=='__main__':prepare(*(Path(v) for v in sys.argv[1:4]))
