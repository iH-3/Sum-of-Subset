"""Exact replay of an explicitly partial or complete target-cover partition.

Open leaves are retained as open. A branch is closed only when every live
component is present and every child has an exact contradiction.
"""
import json
from math import gcd
import model as m
import full_cover as fc

def branch_limits(limits,guards):
    result=dict(limits or {})
    for guard in guards:
        factor=gcd(*(abs(v) for v in guard.values())) or 1
        row={k:v//factor for k,v in guard.items() if v};multiple=1
        while True:
            key='linear_cut:'+json.dumps({k:v*multiple for k,v in row.items()},sort_keys=True,separators=(',',':'))
            if key not in result or result[key]==[0,0]:result[key]=[0,0];break
            multiple+=1
    return result

def check(tree,probes,rows,eqs,used=(),base_record=None,assumptions=(),minimum_credit=None):
    import exact
    m.need(type(tree.get('closed')) is bool,'Partition closure flag')
    if 'record' in tree:
        m.need(base_record is not None and 'children' not in tree and 'certificate' not in tree,'Conditional partition record leaf')
        expected=branch_limits(base_record.get('limits'),assumptions)
        child=tree['record'];cursor=child
        while cursor!=base_record:
            m.need(isinstance(cursor,dict) and cursor.get('limits')==expected and 'premise' in cursor,'Partition record has precisely the covered assumptions')
            cursor=cursor['premise']
        if tree['closed']:exact.replay(child,require_closed=True)
        else:
            state=exact.replay(child,require_closed=False,return_state=True)
            m.need(minimum_credit is None or state['credit']>=minimum_credit,'Every open alternative has the claimed fixed credit')
        return dict(closed=tree['closed'],closed_leaves=int(tree['closed']),open_leaves=int(not tree['closed']))
    if 'modular_certificate' in tree:
        import modular
        m.need(tree['closed'] and 'children' not in tree,'Partition modular contradiction leaf')
        modular.check(tree['modular_certificate'],rows,eqs,{})
        return dict(closed=True,closed_leaves=1,open_leaves=0)
    if 'certificate' in tree:

        m.need(tree['closed'] and 'children' not in tree,'Partition contradiction leaf')
        exact.check(tree['certificate'],rows,eqs)
        return dict(closed=True,closed_leaves=1,open_leaves=0)
    if 'children' not in tree:
        m.need(not tree['closed'],'Uncertified closed partition leaf')
        m.need(minimum_credit is None,'Missing credit proof for open alternative')
        return dict(closed=False,closed_leaves=0,open_leaves=1)
    pid=tree['probe'];m.need(type(pid) is int and 0<=pid<len(probes) and pid not in used,'Partition probe')
    state=probes[pid];inventory=[tuple(c['node']) for c in tree['children']]
    nodes={tuple(n) for n in state['nodes']}
    m.need(set(inventory)==nodes and len(inventory)==len(nodes),'Every live partition alternative retained')
    values=[]
    for entry in tree['children']:
        extra=[(g,0,'joint target containment') for g in fc.containment(state['target'],tuple(entry['node']),state['width'])]
        values.append(check(entry['child'],probes,rows+extra,eqs,(*used,pid),base_record,(*assumptions,*(g for g,_,_ in extra)),minimum_credit))
    closed=all(v['closed'] for v in values);m.need(tree['closed']==closed,'Partition closure agrees with every child')
    return dict(closed=closed,closed_leaves=sum(v['closed_leaves'] for v in values),open_leaves=sum(v['open_leaves'] for v in values))


def remove_closed_top(tree,probes):
    if 'children' not in tree:return
    state=probes[tree['probe']]
    for entry in tree['children']:
        if entry['child']['closed']:state['nodes'].remove(tuple(entry['node']))
    state['forced']=False
