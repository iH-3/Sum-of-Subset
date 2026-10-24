"""Cover 2D by charged interval hulls, core sets, and remaining tail pairs.

Unlike a core-overlap forest, a charged hull can absorb any number of pair
points it contains, without asserting those points lie in the actual core.
"""
from itertools import combinations_with_replacement
import model as m,full_cover as fc,full_window as fw
ONE={'ONE':1}

def components():
    return [({'Rt':-2},{'Rs':2}),*[(m.add((1,t),(-1,{'Rt':1})),m.add((1,t),(1,{'Rs':1}))) for t in fc.tails()]]

def pairs():return [m.add((1,fc.tails()[a]),(1,fc.tails()[b])) for a,b in combinations_with_replacement(range(8),2)]

def derive(proof,licensed_shape=None):
    shape=proof.get('core_shape');m.need(shape is None or type(shape) is int and shape==licensed_shape,'Licensed source-hull first-gap shape')
    intervals=components();points=pairs();seen=set();covered=set();capacity={};guards=[]
    for group in proof['groups']:
        indices=group['components'];m.need(indices and len(set(indices))==len(indices) and all(type(i) is int and 0<=i<9 and i not in seen for i in indices),'Unique complete source-hull inventory');seen.update(indices)
        members=group.get('pairs',[]);m.need(len(set(members))==len(members) and all(type(i) is int and 0<=i<36 and i not in covered for i in members),'Unique source pair coverage');covered.update(members)
        if group.get('mass',False):
            m.need(len(indices)==1 and not members,'Actual-set mass charge absorbs no hull points')
            capacity=m.add((1,capacity),(1,fw.core_capacity(2,shape) if indices[0]==0 else {'ONE':65}));continue
        lo,hi=group['lower'],group['upper'];guards.append(m.add((1,lo),(-1,hi),(-1,ONE)))
        for i in indices:
            a,b=intervals[i];guards.extend([m.add((1,lo),(-1,a)),m.add((1,b),(-1,hi))])
        for i in members:guards.extend([m.add((1,lo),(-1,points[i])),m.add((1,points[i]),(-1,hi))])
        capacity=m.add((1,capacity),(1,hi),(-1,lo),(1,ONE))
    m.need(seen==set(range(9)),'Every source core component covered')
    capacity=m.add((1,capacity),(36-len(covered),ONE))
    return (m.add((1,{'K':1}),(-1,capacity)),0,'source interval-hull union capacity'),guards

def discover(search,point):
    import exact
    intervals=components();points=pairs();ev=lambda row:sum(v*point[k] for k,v in row.items());shape=getattr(search,'core_shape',None)
    groups=[];certs=[];covered=set();finished=[False]
    def guard_all(guards):
        answer=[]
        for guard in guards:
            cert,done=search.nonstrict_guard(guard)
            if done:finished[0]=True;return None
            if cert is None:return None
            answer.append(cert)
        return answer
    def visit(indices):
        if finished[0]:return
        lo=min((intervals[i][0] for i in indices),key=ev);hi=max((intervals[i][1] for i in indices),key=ev)
        guards=[m.add((1,lo),(-1,hi),(-1,ONE))]
        for i in indices:
            a,b=intervals[i];guards.extend([m.add((1,lo),(-1,a)),m.add((1,b),(-1,hi))])
        local=guard_all(guards)
        if local is None:
            if finished[0]:return
            if len(indices)==1:
                groups.append(dict(components=indices,mass=True));return
            cut=max(range(1,len(indices)),key=lambda k:ev(intervals[indices[k]][0])-ev(intervals[indices[k-1]][1]))
            visit(indices[:cut]);visit(indices[cut:]);return
        members=[];paircerts=[]
        for i,row in enumerate(points):
            if i in covered or ev(row)<ev(lo)-1e-7 or ev(row)>ev(hi)+1e-7:continue
            cc=guard_all([m.add((1,lo),(-1,row)),m.add((1,row),(-1,hi))])
            if finished[0]:return
            if cc is not None:members.append(i);paircerts.extend(cc)
        mass=sum(ev(fw.core_capacity(2,shape)) if i==0 else 65 for i in indices)
        hull=ev(hi)-ev(lo)+1
        if mass+len(members)<hull-1e-7:
            groups.extend(dict(components=[i],mass=True) for i in indices);return
        covered.update(members);groups.append(dict(components=indices,lower=lo,upper=hi,pairs=members));certs.extend(local);certs.extend(paircerts)
    order=sorted(range(9),key=lambda i:ev(intervals[i][0]));clusters=[]
    for i in order:
        if not clusters or ev(intervals[i][0])>max(ev(intervals[j][1]) for j in clusters[-1])+1+1e-7:clusters.append([i])
        else:clusters[-1].append(i)
    for cluster in clusters:visit(cluster)
    if finished[0]:return False,True
    proof=dict(groups=groups)
    if shape is not None:proof['core_shape']=shape
    row,guards=derive(proof,shape)
    m.need(len(certs)==len(guards),'Source-hull discovery guard ordering')
    if any(a==row[0] and b==0 for a,b,_ in search.rows):return False,False
    # A useful affine capacity may tighten a later LP even if this particular
    # discovery point does not violate it.
    for cert,guard in zip(certs,guards):exact.check(cert,search.rows,search.eqs,guard,strict=False)
    search.trace.append(dict(kind='source_hull_capacity',proof=proof,certificates=certs));search.rows.append(row)
    return True,False
