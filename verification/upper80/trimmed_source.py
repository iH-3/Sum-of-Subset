"""Complete 2D cover after removing several largest core elements.

The removed elements are actual points, enclosed by canonical mass bounds;
their coordinates need not be new model variables. Single point intervals
cost one unless absorbed by a charged hull. The remaining bulk has exactly
65-2L points. This keeps more of the core's interior holes than a whole hull.
"""
from itertools import combinations_with_replacement
import model as m,full_cover as fc
ONE={'ONE':1}

def core_bound(side,index,order):
    m.need(side in ('s','t') and type(index) is int and 1<=index<=4,'Trimmed core side and index')
    m.need(type(order) is int and 0<=order<=14,'Trimmed core canonical order')
    rank={'ONE':32-index,'rank_k':-1 if side=='s' else 1}
    included=int(index<=order)
    others={'phicore'+side:order-included,'ONE':-order*(order+1)//2+included*index}
    return (rank,m.add((1,rank),(1,{'phicore'+side:1}),(-index,ONE))),(
        m.add((1,{'R'+side:1}),(-index,ONE)),
        m.add((1,rank),(1,{'t'+side:1}),(-1,{'x'+side:1}),(-1,others)))

def components(proof):
    keep=proof['keep'];m.need(type(keep) is int and 1<=keep<=4,'Number of removed core points per side')
    for field in ('orders','lower_choice','upper_choice'):m.need(type(proof[field]) is dict and set(proof[field])==set('st'),'Both trimmed core sides')
    points=[(x,x) for x in fc.tails()];bulk={}
    for side in 'st':
        ell=proof['orders'][side]
        lower=proof['lower_choice'][side];upper=proof['upper_choice'][side]
        m.need(type(lower) is list and len(lower)==keep-1 and type(upper) is list and len(upper)==keep and all(type(c) is int and c in (0,1) for c in [*lower,*upper]),'Trimmed core bound selectors')
        core_bound(side,keep,ell)
        sign=1 if side=='s' else -1;R={'R'+side:sign};points.append((R,R))
        for j in range(1,keep+1):
            lows,highs=core_bound(side,j,ell);hi=highs[upper[j-1]]
            if j==keep:bulk[side]=hi;continue
            lo=lows[lower[j-1]]
            points.append((lo,hi) if side=='s' else (m.add((-1,hi)),m.add((-1,lo))))
    lo=m.add((-1,bulk['t']));hi=bulk['s'];n=65-2*keep
    intervals=[(m.add((2,lo)),m.add((2,hi)))];masses=[m.add((2,hi),(-2,lo),(1,ONE))]
    for a,b in points:intervals.append((m.add((1,lo),(1,a)),m.add((1,hi),(1,b))));masses.append({'ONE':n})
    for i,j in combinations_with_replacement(range(len(points)),2):
        intervals.append((m.add((1,points[i][0]),(1,points[j][0])),m.add((1,points[i][1]),(1,points[j][1]))));masses.append(ONE)
    return intervals,masses,points,(lo,hi)

def derive(proof):
    intervals,masses,_,_=components(proof);seen=set();capacity={};guards=[]
    for group in proof['groups']:
        indices=group['components']
        m.need(type(indices) is list and indices and len(set(indices))==len(indices) and all(type(i) is int and 0<=i<len(intervals) and i not in seen for i in indices),'Unique trimmed-source component inventory');seen.update(indices)
        if group.get('mass',False):
            m.need(len(indices)==1,'Trimmed-source mass cannot absorb another component')
            capacity=m.add((1,capacity),(1,masses[indices[0]]));continue
        lo,hi=group['lower'],group['upper'];guards.append(m.add((1,lo),(-1,hi),(-1,ONE)))
        for i in indices:
            a,b=intervals[i];guards.extend([m.add((1,lo),(-1,a)),m.add((1,b),(-1,hi))])
        capacity=m.add((1,capacity),(1,hi),(-1,lo),(1,ONE))
    m.need(seen==set(range(len(intervals))),'Every trimmed-source component covered')
    return (m.add((1,{'K':1}),(-1,capacity)),0,'trimmed core and uncertain-point source capacity'),guards

def recipe(point,keep=4):
    import math
    ev=lambda row:sum(v*point[k] for k,v in row.items())
    proof=dict(keep=keep,orders={},lower_choice={},upper_choice={},groups=[])
    for side in 'st':
        ell=min(14,max(0,math.floor(point['phicore'+side]+1e-7)));proof['orders'][side]=ell
        lows=[];highs=[]
        for j in range(1,keep+1):
            a,b=core_bound(side,j,ell)
            if j<keep:lows.append(int(ev(a[1])>ev(a[0])))
            highs.append(int(ev(b[1])<ev(b[0])))
        proof['lower_choice'][side]=lows;proof['upper_choice'][side]=highs
    intervals,masses,_,_=components(proof);clusters=[]
    for i in sorted(range(len(intervals)),key=lambda i:ev(intervals[i][0])):
        if not clusters or ev(intervals[i][0])>max(ev(intervals[j][1]) for j in clusters[-1])+1+1e-7:clusters.append([i])
        else:clusters[-1].append(i)
    return proof,intervals,masses,clusters

def discover(search,point,backend=None):
    import exact,sys
    backend=sys.modules[__name__] if backend is None else backend
    scale=getattr(backend,'SCALE',1)
    m.need(not search.positive,'Current trimmed-source discovery uses the zero-hole domain')
    ev=lambda row:sum(v*point[k] for k,v in row.items())
    options=[]
    for keep in range(1,5):
        result=backend.recipe(point,keep);_,intervals,masses,clusters=result
        estimate=sum(min(max(ev(intervals[i][1]) for i in g)-min(ev(intervals[i][0]) for i in g)+scale,sum(ev(masses[i]) for i in g)) for g in clusters)
        options.append((estimate,keep,result))
    _,_,(proof,intervals,masses,clusters)=min(options,key=lambda x:(x[0],-x[1]));certs=[];finished=[False]
    suggestions={}
    def visit(indices):
        if finished[0]:return
        lo=min((intervals[i][0] for i in indices),key=ev);hi=max((intervals[i][1] for i in indices),key=ev)
        if sum(ev(masses[i]) for i in indices)<=ev(hi)-ev(lo)+scale+1e-7:
            proof['groups'].extend(dict(components=[i],mass=True) for i in indices);return
        guards=[m.add((1,lo),(-1,hi),(-scale,ONE))]
        for i in indices:
            a,b=intervals[i];guards.extend([m.add((1,lo),(-1,a)),m.add((1,b),(-1,hi))])
        local=[]
        for guard in guards:
            cert,done=search.nonstrict_guard(guard)
            if done:finished[0]=True;return
            if cert is None:
                if ev(guard)<=1e-7 and any(guard.values()):
                    key=tuple(sorted((k,v) for k,v in guard.items() if v))
                    gain=(sum(ev(masses[i]) for i in indices)-(ev(hi)-ev(lo)+scale))/scale
                    if key not in suggestions or suggestions[key]['gain']<gain:
                        suggestions[key]=dict(guard={k:v for k,v in key},gain=gain,components=len(indices))
                break
            local.append(cert)
        if len(local)!=len(guards):
            if len(indices)==1:proof['groups'].append(dict(components=indices,mass=True));return
            cut=max(range(1,len(indices)),key=lambda k:ev(intervals[indices[k]][0])-ev(intervals[indices[k-1]][1]))
            visit(indices[:cut]);visit(indices[cut:]);return
        proof['groups'].append(dict(components=indices,lower=lo,upper=hi));certs.extend(local)
    for cluster in clusters:visit(cluster)
    if finished[0]:return False,True
    search.source_split_candidates=sorted(suggestions.values(),key=lambda x:x['gain'],reverse=True)[:12]
    row,guards=backend.derive(proof);m.need(len(certs)==len(guards),'Trimmed-source certificate order')
    # Do not keep generating loose global caps after failed hull licenses.
    # Save their useful missing integer guards for genuinely new branches.
    if ev(row[0])<=1e-7:return False,False
    if any(a==row[0] and b==0 for a,b,_ in search.rows):return False,False
    for cert,guard in zip(certs,guards):exact.check(cert,search.rows,search.eqs,guard,strict=False)
    search.trace.append(dict(kind=getattr(backend,'TRACE_KIND','trimmed_source_capacity'),proof=proof,certificates=certs));search.rows.append(row)
    return True,False
