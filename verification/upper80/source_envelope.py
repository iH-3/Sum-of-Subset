"""Cover 2D while retaining both extreme gaps of every core component.

The nine core components each split into their two actual extreme points
and an interval containing all other points. The other36 pieces are tail
pairs. Every piece is charged once; interval hulls may absorb singleton
pieces, while a mass charge can cover only a single piece.
"""
import model as m,source_hulls as sh,core_gap as cg,first_gap_core as fg
ONE={'ONE':1}

def pieces(proof,licensed_shape=None):
    shape=proof.get('core_shape')
    m.need(shape is None or type(shape) is int and shape==licensed_shape,'Licensed source-envelope core shape')
    prefix=proof.get('core_prefix',{})
    m.need(type(prefix) is dict and set(prefix)<=set('st'),'Source-envelope canonical prefix inventory')
    floors={side:cg.canonical_prefix(side,prefix.get(side,0),shape) for side in 'st'}
    trimmed=proof['trimmed']
    m.need(type(trimmed) is list and len(set(trimmed))==len(trimmed) and set(trimmed)<=set('st'),'Distinct source-envelope gap sides')
    losses={}
    for side in 'st':
        loss=m.add((1,{'x'+side:2,'t'+side:-1}),(1,floors[side]))
        if shape is not None:loss=m.add((1,loss),(1,fg.removed_side_prefix_mass(shape,side)))
        losses[side]=loss if side in trimmed else {}
    answer=[]
    for lo,hi in sh.components():
        answer.extend([(lo,lo),(m.add((1,lo),(1,losses['t']),(1,ONE)),m.add((1,hi),(-1,losses['s']),(-1,ONE))),(hi,hi)])
    answer.extend((x,x) for x in sh.pairs())
    return answer

def mass(index,intervals):
    # Every E translate has65 points and its two extremes are distinct.
    if index<27 and index%3==1 and index//3>0:return {'ONE':63}
    lo,hi=intervals[index]
    # The middle interval contains the translated core zero, so its length
    # is nonnegative even if the affine relaxation does not infer that fact.
    return m.add((1,hi),(-1,lo),(1,ONE))

def derive(proof,licensed_shape=None):
    intervals=pieces(proof,licensed_shape);seen=set();guards=[];capacity={}
    for group in proof['groups']:
        indices=group['pieces']
        m.need(type(indices) is list and indices and len(set(indices))==len(indices) and all(type(i) is int and 0<=i<63 and i not in seen for i in indices),'Unique complete source-envelope pieces')
        seen.update(indices)
        if group.get('mass',False):
            m.need(len(indices)==1,'Source-envelope mass absorbs no other piece')
            capacity=m.add((1,capacity),(1,mass(indices[0],intervals)));continue
        lo,hi=group['lower'],group['upper'];guards.append(m.add((1,lo),(-1,hi),(-1,ONE)))
        for i in indices:
            a,b=intervals[i];guards.extend([m.add((1,lo),(-1,a)),m.add((1,b),(-1,hi))])
        capacity=m.add((1,capacity),(1,hi),(-1,lo),(1,ONE))
    m.need(seen==set(range(63)),'Every source-envelope piece covered')
    return (m.add((1,{'K':1}),(-1,capacity)),0,'source extreme-gap envelope capacity'),guards

def recipe(point,shape=None):
    import math
    ev=lambda row:sum(v*point[k] for k,v in row.items());prefix={};trimmed=[]
    for side in 'st':
        w=0
        if shape is not None:
            h,ps,pt=fg.CASES[shape];w=h-(ps if side=='s' else pt)
        prefix[side]=min(12,max(0,math.floor(point['phicore'+side]-w-2+1e-7)))
        loss=m.add((1,{'x'+side:2,'t'+side:-1}),(1,cg.canonical_prefix(side,prefix[side],shape)))
        if shape is not None:loss=m.add((1,loss),(1,fg.removed_side_prefix_mass(shape,side)))
        if ev(loss)>1e-7:trimmed.append(side)
    proof=dict(core_prefix=prefix,trimmed=trimmed,groups=[])
    if shape is not None:proof['core_shape']=shape
    intervals=pieces(proof,shape);clusters=[]
    for i in sorted(range(63),key=lambda i:ev(intervals[i][0])):
        if not clusters or ev(intervals[i][0])>max(ev(intervals[j][1]) for j in clusters[-1])+1+1e-7:clusters.append([i])
        else:clusters[-1].append(i)
    return proof,intervals,clusters

def discover(search,point):
    import exact
    shape=getattr(search,'core_shape',None);proof,intervals,clusters=recipe(point,shape)
    ev=lambda row:sum(v*point[k] for k,v in row.items());certs=[];finished=[False]
    def visit(indices):
        if finished[0]:return
        lo=min((intervals[i][0] for i in indices),key=ev);hi=max((intervals[i][1] for i in indices),key=ev)
        if len(indices)==1 and ev(mass(indices[0],intervals))<=ev(hi)-ev(lo)+1+1e-7:
            proof['groups'].append(dict(pieces=indices,mass=True));return
        guards=[m.add((1,lo),(-1,hi),(-1,ONE))]
        for i in indices:
            a,b=intervals[i];guards.extend([m.add((1,lo),(-1,a)),m.add((1,b),(-1,hi))])
        local=[]
        for guard in guards:
            cert,done=search.nonstrict_guard(guard)
            if done:finished[0]=True;return
            if cert is None:break
            local.append(cert)
        if len(local)!=len(guards):
            if len(indices)==1:proof['groups'].append(dict(pieces=indices,mass=True));return
            cut=max(range(1,len(indices)),key=lambda k:ev(intervals[indices[k]][0])-ev(intervals[indices[k-1]][1]))
            visit(indices[:cut]);visit(indices[cut:]);return
        proof['groups'].append(dict(pieces=indices,lower=lo,upper=hi));certs.extend(local)
    for cluster in clusters:visit(cluster)
    if finished[0]:return False,True
    row,guards=derive(proof,shape);m.need(len(certs)==len(guards),'Source-envelope certificate ordering')
    if any(a==row[0] and b==0 for a,b,_ in search.rows):return False,False
    for cert,guard in zip(certs,guards):exact.check(cert,search.rows,search.eqs,guard,strict=False)
    search.trace.append(dict(kind='source_envelope_capacity',proof=proof,certificates=certs));search.rows.append(row)
    return True,False
