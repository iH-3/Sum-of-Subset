"""Exact conditional upper bounds for the enlarged target-cover union.

Every component is assigned to a containing integer hull or proved outside
the target. Hulls may overlap: their summed lengths remain an upper bound.
The native mode uses the separately certified global fixed-item credit.
"""
import cover_geometry as geometry
import model as m
import copy

ONE={'ONE':1}

def components(st,Z,side,mode):
    m.need(mode in ('native','full','sumset'),'Cover capacity mode')
    items=geometry.catalogue(st,Z,side)
    if mode=='sumset':
        lam={'d'+side:1,'M'+side:-2,'X'+side:-2,'g'+side:-1}
        return [(name,m.add((1,lo),(-1,lam)),m.add((1,hi),(-1,lam))) for name,lo,hi in items if name.startswith('L:')]
    if mode=='native':
        fixed=m.fixed_forms();items=[entry for entry in items if entry[0] not in fixed]
    return items

def recipe(st,Z,point,mode='native',side=None):
    ev=lambda row:sum(v*point[k] for k,v in row.items())
    sides='st' if mode=='native' else 's' if mode=='sumset' else side
    m.need(sides in ('st','s','t'),'Cover capacity sides')
    answer=dict(mode=mode,sides={})
    for side in sides:
        items=components(st,Z,side,mode);S=point['S'+side];outside=[];inside=[]
        for i,(_,lo,hi) in enumerate(items):
            left,right=ev(lo),ev(hi)
            if mode=='sumset':inside.append((left,right,i))
            elif right<1-1e-7:outside.append((i,0))
            elif left>S+1e-7:outside.append((i,1))
            else:inside.append((max(1,left),min(S,right),i))
        groups=[];members=[];end=None
        def finish(ids):
            lo=min(ids,key=lambda i:ev(items[i][1]));hi=max(ids,key=lambda i:ev(items[i][2]))
            return dict(members=ids,lo=lo if mode=='sumset' or ev(items[lo][1])>=1 else None,hi=hi if mode=='sumset' or ev(items[hi][2])<=S else None)
        for left,right,i in sorted(inside):
            # Joining merely adjacent integer intervals saves no capacity.
            # Keep them separate to avoid proving irrelevant adjacency guards.
            if end is None or left>end+1e-7:
                if members:groups.append(finish(members))
                members=[i];end=right
            else:members.append(i);end=max(end,right)
        if members:groups.append(finish(members))
        answer['sides'][side]=dict(outside=outside,groups=groups)
    return answer

def derive(st,Z,proof,credit):
    mode=proof['mode'];sides=proof['sides']
    m.need((mode=='native' and set(sides)==set('st')) or (mode=='full' and len(sides)==1 and set(sides)<=set('st')) or (mode=='sumset' and set(sides)=={'s'}),'Cover capacity domain')
    body={'K':1} if mode=='sumset' else {'hole_W':-len(sides)};guards=[]
    for side,plan in sides.items():
        items=components(st,Z,side,mode);seen=set();S={'S'+side:1};upper={}
        m.need(mode!='sumset' or not plan['outside'],'No discarded source-sum components')
        for i,direction in plan['outside']:
            m.need(type(i) is int and 0<=i<len(items) and i not in seen and type(direction) is int and direction in (0,1),'Cover outside inventory')
            seen.add(i);_,lo,hi=items[i]
            guards.append(hi if direction==0 else m.add((1,S),(1,ONE),(-1,lo)))
        for group in plan['groups']:
            ids=group['members']
            m.need(ids and len(set(ids))==len(ids) and all(type(i) is int and 0<=i<len(items) and i not in seen for i in ids),'Cover hull inventory')
            seen.update(ids);li,ui=group['lo'],group['hi']
            m.need(mode!='sumset' or li is not None and ui is not None,'Source-sum hull anchors')
            m.need(li is None or type(li) is int and li in ids,'Cover lower anchor')
            m.need(ui is None or type(ui) is int and ui in ids,'Cover upper anchor')
            lo=ONE if li is None else items[li][1];hi=S if ui is None else items[ui][2]
            guards.append(m.add((1,lo),(-1,hi),(-1,ONE)))
            for i in ids:
                if li is not None:guards.append(m.add((1,lo),(-1,items[i][1])))
                if ui is not None:guards.append(m.add((1,items[i][2]),(-1,hi)))
            upper=m.add((1,upper),(1,hi),(-1,lo),(1,ONE))
        m.need(seen==set(range(len(items))),'Complete cover capacity inventory')
        body=m.add((1,body),(-1,upper),*([(1,S)] if mode!='sumset' else []))
    unique=[];seen=set()
    for row in guards:
        row={k:v for k,v in row.items() if v};key=tuple(sorted(row.items()))
        if key not in seen:unique.append(row);seen.add(key)
    return (body,84-credit if mode=='native' else 0,'enlarged cover union capacity'),unique

def relax_guard(st,Z,proof,failed):
    """Discovery-only: replace an unproved assignment by whole components.

    Removing a claimed exclusion or intersection loses sharpness but retains
    the complete inventory. The resulting recipe is verified from scratch.
    """
    key=lambda row:tuple(sorted((k,v) for k,v in row.items() if v))
    wanted=key(failed);answer=copy.deepcopy(proof);mode=proof['mode']
    for side,plan in answer['sides'].items():
        items=components(st,Z,side,mode);S={'S'+side:1}
        def single(i):return dict(members=[i],lo=i,hi=i)
        for index,(i,direction) in enumerate(plan['outside']):
            _,lo,hi=items[i];guard=hi if direction==0 else m.add((1,S),(1,ONE),(-1,lo))
            if key(guard)==wanted:
                plan['outside'].pop(index);plan['groups'].append(single(i));return answer
        for index,group in enumerate(plan['groups']):
            ids=group['members'];li,ui=group['lo'],group['hi']
            lo=ONE if li is None else items[li][1];hi=S if ui is None else items[ui][2]
            if key(m.add((1,lo),(-1,hi),(-1,ONE)))==wanted:
                plan['groups'].pop(index);plan['groups'].extend(single(i) for i in ids);return answer
            for i in ids:
                comparisons=[]
                if li is not None:comparisons.append(m.add((1,lo),(-1,items[i][1])))
                if ui is not None:comparisons.append(m.add((1,items[i][2]),(-1,hi)))
                if any(key(g)==wanted for g in comparisons):
                    # If this component is an anchor, dissolve the whole group.
                    if i in (li,ui):
                        plan['groups'].pop(index);plan['groups'].extend(single(j) for j in ids)
                    else:ids.remove(i);plan['groups'].append(single(i))
                    return answer
    return None
