"""Known native intervals when the positive first gap forces both cores above1."""
import model as m
import exact
ONE={'ONE':1}

def catalogue(st,Z,modes):
    m.need(set(modes)==set('st') and all(type(v) is int and v in (0,1) for v in modes.values()),'Shifted prefix modes')
    L={s:{'ONE':63,'rank_k':-2 if s=='s' else 2,'t'+s:-1,'x'+s:1} for s in 'st'}
    guards=[{'hole_W':-1,'ONE':1},{'ts':1,'tt':1,'rank_k':1,'ONE':-94}]
    guards.extend(m.add((2,ONE),(-1,L[s])) for s in 'st' if modes[s])
    out={}
    for side,other in [('s','t'),('t','s')]:
        parts=[({}, {})]
        if modes[side]:parts.append(({'ONE':2},L[side]))
        if modes[other]:parts.append(({k:-v for k,v in L[other].items()},{'ONE':-2}))
        parts.extend((exact.signed_source_point(tag,side),exact.signed_source_point(tag,side)) for tag in exact.POINT_TAGS)
        lam={'d'+side:1,'M'+side:-2,'X'+side:-2,'g'+side:-1}
        items=[]
        for i,(a,b) in enumerate(parts):
            for c,d in parts[i:]:items.append((m.add((1,lam),(1,a),(1,c)),m.add((1,lam),(1,b),(1,d))))
        for name in sorted(name for name,status in st.items() if status==1 and name[-1]==side):
            items.extend((m.add((1,Z[name]),(1,a)),m.add((1,Z[name]),(1,b))) for a,b in parts)
        out[side]=items
    return guards,out

def chains(st,Z,point):
    ev=lambda row:sum(c*point[k] for k,c in row.items())
    modes={s:int(63+(-2 if s=='s' else 2)*point['rank_k']-point['t'+s]+point['x'+s]>=2-1e-7) for s in 'st'}
    guards,data=catalogue(st,Z,modes);out={}
    for side,items in data.items():
        chunks=[];chunk=[];end=None
        for i,(lo,hi) in sorted(enumerate(items),key=lambda v:(ev(v[1][0]),ev(v[1][1]))):
            a,b=ev(lo),ev(hi)
            if end is None or a>end+1+1e-7:
                if chunk:chunks.append(chunk)
                chunk=[i];end=b
            elif b>end+1e-7:chunk.append(i);end=b
        if chunk:chunks.append(chunk)
        out[side]=chunks
    return modes,data,out

def cover_guards(st,Z,modes,side,chain,label):
    forms=m.fixed_forms();m.need(label in forms and side in 'st' and ('+' in label)==(side=='s'),'Shifted fixed label')
    guards,data=catalogue(st,Z,modes);items=data[side]
    m.need(chain and len(chain)==len(set(chain)) and all(type(i) is int and 0<=i<len(items) for i in chain),'Shifted known chain')
    start=items[chain[0]][0];end=None
    for i in chain:
        a,b=items[i];guards.append(m.add((1,a),(-1,b)))
        if end is not None:guards.extend([m.add((1,end),(-1,b)),m.add((1,a),(-1,end),(-1,ONE))])
        end=b
    guards.extend([m.add((1,start),(-1,forms[label])),m.add((1,forms[label]),(-1,end))])
    return guards
