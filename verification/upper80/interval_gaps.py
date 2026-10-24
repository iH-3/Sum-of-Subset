"""Cardinality of holes between ordered, equal-width core hull translates.

The leading double-core interval is the union of its two endpoint translates.
Hence all non-singleton native components can use one common core hull.
"""
import model as m
ONE={'ONE':1}

def catalogue(st,Z,side):
    m.need(side in 'st','Ordered interval side');other='t' if side=='s' else 's'
    tails=[]
    for physical in (side,other):
        sign=1 if physical==side else -1
        for off in 'abce':tails.append({'R'+physical:sign,off+physical:sign})
    centres=[];points=[]
    for name in sorted(n for n,status in st.items() if status==1 and n[-1]==side):
        centres.append((name,Z[name]))
        points.extend((name+':tail'+str(i),m.add((1,Z[name]),(1,tail))) for i,tail in enumerate(tails))
    lam={'d'+side:1,'M'+side:-2,'X'+side:-2,'g'+side:-1}
    offsets=[{'R'+other:-1},{'R'+side:1},*tails]
    centres.extend(('L:'+str(i),m.add((1,lam),(1,value))) for i,value in enumerate(offsets))
    for i,first in enumerate(tails):
        for j,second in enumerate(tails[i:],i):
            points.append(('L:pair'+str((i,j)),m.add((1,lam),(1,first),(1,second))))
    native_count=len(points)
    points.extend((label,form) for label,form in sorted(m.fixed_forms().items()) if ('+' in label)==(side=='s'))
    return centres,points,native_count

def licenses(st,Z,side,order):
    centres,_,_=catalogue(st,Z,side);other='t' if side=='s' else 's'
    m.need(len(order)==len(centres) and set(order)==set(range(len(centres))) and all(type(i) is int for i in order),'Complete interval centre order')
    rows=[m.add((1,centres[a][1]),(-1,centres[b][1])) for a,b in zip(order,order[1:])]
    rows.extend([m.add((1,ONE),(-1,centres[order[0]][1]),(-1,{'R'+side:1})),
                 m.add((1,centres[order[-1]][1]),(-1,{'R'+other:1,'S'+side:1}))])
    return rows

def exclusion(st,Z,side,index,where):
    centres,points,_=catalogue(st,Z,side);other='t' if side=='s' else 's'
    m.need(type(index) is int and 0<=index<len(points),'Gap singleton inventory');point=points[index][1]
    if where=='low':return [point]
    if where=='high':return [m.add((1,{'S'+side:1}),(1,ONE),(-1,point))]
    m.need(type(where) is int and 0<=where<len(centres),'Gap singleton containing interval')
    centre=centres[where][1]
    return [m.add((1,centre),(-1,{'R'+other:1}),(-1,point)),m.add((1,point),(-1,centre),(-1,{'R'+side:1}))]

def gaps(st,Z,side,order):
    centres,_,_=catalogue(st,Z,side);other='t' if side=='s' else 's'
    licenses(st,Z,side,order)
    result=[m.add((1,centres[order[0]][1]),(-1,{'R'+other:1}),(-1,ONE))]
    result.extend(m.add((1,centres[b][1]),(-1,centres[a][1]),(-1,{'Rs':1,'Rt':1}),(-1,ONE)) for a,b in zip(order,order[1:]))
    result.append(m.add((1,{'S'+side:1}),(-1,centres[order[-1]][1]),(-1,{'R'+side:1})))
    return result

def capacity(st,Z,states,selected,credit,joint):
    m.need(set(selected)==set('st') if joint else len(selected)==1 and set(selected)<=set('st'),'Gap capacity sides')
    row={'hole_W':-len(selected)};rhs=84-credit if joint else 0
    for side,indices in selected.items():
        m.need(side in states,'Unlicensed ordered cover');state=states[side]
        forms=gaps(st,Z,side,state['order']);m.need(len(indices)==len(set(indices)) and all(type(i) is int and 0<=i<len(forms) for i in indices),'Gap interval inventory')
        row=m.add((1,row),*[(1,forms[i]) for i in indices])
        _,points,native=catalogue(st,Z,side);excluded=set(state['excluded'])
        m.need(excluded<=set(range(len(points))),'Gap singleton exclusions')
        rhs+=sum(i not in excluded for i in range(native if joint else len(points)))
    return row,rhs,'ordered core interval gap capacity'
