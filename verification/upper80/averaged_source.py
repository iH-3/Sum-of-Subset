"""Trimmed 2D cover with monotone suffix mass bounds, in twelfths.

The j nonmaximum defects at indices r-j,...,r-1 are at least d_(r-j).
The earlier indices supply a separate canonical prefix floor. Scaling all
endpoints by12 preserves exact integer certificate arithmetic for j<=4.
"""
from itertools import combinations_with_replacement
import math
import model as m,full_cover as fc,trimmed_source as tr
SCALE=12
TRACE_KIND='averaged_source_capacity'
ONE={'ONE':1}

def upper(side,index,order):
    m.need(side in ('s','t') and type(index) is int and 1<=index<=4,'Averaged core index')
    m.need(type(order) is int and 0<=order<=14-index,'Existing averaged prefix indices')
    rank={'ONE':32-index,'rank_k':-1 if side=='s' else 1}
    prefix={'phicore'+side:order,'ONE':-order*(order+2*index+1)//2}
    return m.add((SCALE,rank),(SCALE//index,{'t'+side:1,'x'+side:-1}),(-SCALE//index,prefix))

def components(proof):
    keep=proof['keep'];m.need(type(keep) is int and 1<=keep<=4,'Averaged removed core count')
    for field in ('orders','average_orders','lower_choice','upper_choice'):
        m.need(type(proof[field]) is dict and set(proof[field])==set('st'),'Both averaged core sides')
    points=[(m.add((SCALE,x)),m.add((SCALE,x))) for x in fc.tails()];bulk={}
    for side,sign in [('s',1),('t',-1)]:
        ell=proof['orders'][side];orders=proof['average_orders'][side]
        lows=proof['lower_choice'][side];highs=proof['upper_choice'][side]
        m.need(type(orders) is list and len(orders)==keep,'One average order per indexed point')
        m.need(type(lows) is list and len(lows)==keep-1 and all(type(c) is int and c in (0,1) for c in lows),'Averaged lower selectors')
        m.need(type(highs) is list and len(highs)==keep and all(type(c) is int and c in (0,1,2) for c in highs),'Averaged upper selectors')
        R={'R'+side:SCALE*sign};points.append((R,R))
        for j in range(1,keep+1):
            a,b=tr.core_bound(side,j,ell);choices=[*(m.add((SCALE,x)) for x in b),upper(side,j,orders[j-1])];hi=choices[highs[j-1]]
            if j==keep:bulk[side]=hi;continue
            lo=m.add((SCALE,a[lows[j-1]]))
            points.append((lo,hi) if sign==1 else (m.add((-1,hi)),m.add((-1,lo))))
    lo=m.add((-1,bulk['t']));hi=bulk['s'];n=65-2*keep
    intervals=[(m.add((2,lo)),m.add((2,hi)))];masses=[m.add((2,hi),(-2,lo),(SCALE,ONE))]
    for a,b in points:
        intervals.append((m.add((1,lo),(1,a)),m.add((1,hi),(1,b))));masses.append({'ONE':SCALE*n})
    for i,j in combinations_with_replacement(range(len(points)),2):
        intervals.append((m.add((1,points[i][0]),(1,points[j][0])),m.add((1,points[i][1]),(1,points[j][1]))));masses.append({'ONE':SCALE})
    return intervals,masses,points,(lo,hi)

def derive(proof):
    m.need(type(proof.get('nonempty_hulls',False)) is bool,'Nonempty-hull rule flag')
    intervals,masses,_,_=components(proof);seen=set();capacity={};guards=[]
    for group in proof['groups']:
        indices=group['components']
        m.need(type(indices) is list and indices and len(set(indices))==len(indices) and all(type(i) is int and 0<=i<len(intervals) and i not in seen for i in indices),'Unique averaged-source component inventory');seen.update(indices)
        if group.get('mass',False):
            m.need(len(indices)==1,'Averaged mass absorbs no other component');capacity=m.add((1,capacity),(1,masses[indices[0]]));continue
        lo,hi=group['lower'],group['upper']
        m.need(type(lo) is dict and type(hi) is dict and all(type(v) is int for row in (lo,hi) for v in row.values()),'Integer scaled hull endpoints')
        # Each component contains an actual sum. Containing at least one
        # nonempty component already forces this hull to be nonempty.
        if not proof.get('nonempty_hulls',False):guards.append(m.add((1,lo),(-1,hi),(-SCALE,ONE)))
        for i in indices:
            a,b=intervals[i];guards.extend([m.add((1,lo),(-1,a)),m.add((1,b),(-1,hi))])
        capacity=m.add((1,capacity),(1,hi),(-1,lo),(SCALE,ONE))
    m.need(seen==set(range(len(intervals))),'Every averaged-source component covered')
    return (m.add((SCALE,{'K':1}),(-1,capacity)),0,'monotone averaged trimmed-source capacity'),guards

def recipe(point,keep=4):
    ev=lambda row:sum(v*point[k] for k,v in row.items())
    proof=dict(keep=keep,orders={},average_orders={},lower_choice={},upper_choice={},groups=[])
    for side in 'st':
        phi=point['phicore'+side];ell=min(14,max(0,math.floor(phi+1e-7)));proof['orders'][side]=ell
        orders=[];lows=[];highs=[]
        for j in range(1,keep+1):
            order=min(14-j,max(0,math.floor(phi-j-1+1e-7)));orders.append(order)
            a,b=tr.core_bound(side,j,ell)
            if j<keep:lows.append(int(ev(a[1])>ev(a[0])))
            candidates=[*(m.add((SCALE,x)) for x in b),upper(side,j,order)];highs.append(min(range(3),key=lambda i:ev(candidates[i])))
        proof['average_orders'][side]=orders;proof['lower_choice'][side]=lows;proof['upper_choice'][side]=highs
    intervals,masses,_,_=components(proof);clusters=[]
    for i in sorted(range(len(intervals)),key=lambda i:ev(intervals[i][0])):
        if not clusters or ev(intervals[i][0])>max(ev(intervals[j][1]) for j in clusters[-1])+SCALE+1e-7:clusters.append([i])
        else:clusters[-1].append(i)
    return proof,intervals,masses,clusters

def discover(search,point):
    import sys
    return tr.discover(search,point,backend=sys.modules[__name__])
