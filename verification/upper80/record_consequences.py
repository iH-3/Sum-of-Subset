"""Reuse exact consequences proved in a containing parameter domain.

All variables refer to the same canonical physical quantities of the fixed
pattern. A narrower branch may use any previously proved linear fact from
that pattern; it may not import a fact proved under extra assumptions.
"""
import model as m

def domain_contains(source,target):
    for name,interval in (source.get('limits') or {}).items():
        other=(target.get('limits') or {}).get(name)
        m.need(other is not None and len(interval)==len(other)==2 and interval[0]<=other[0]<=other[1]<=interval[1],'Imported record has no additional parameter assumption')

def derive(step,target):
    import exact
    source=step['record'];m.need(all(source.get(k)==target.get(k) for k in ('st','j','positive')),'Imported consequence has the same physical pattern')
    domain_contains(source,target)
    state=exact.replay(source,require_closed=False,return_state=True);indices=step['facts']
    if 'credit' in step:m.need(type(step['credit']) is int and 0<=step['credit']<=state['credit'],'Imported fixed credit is proved in the containing domain')
    m.need(len(set(indices))==len(indices) and all(type(i) is int and 0<=i<len(state['facts']) for i in indices),'Distinct licensed imported facts')
    return [(state['facts'][i][0],state['facts'][i][1],'imported exact consequence') for i in indices]
