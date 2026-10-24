"""Use the existing ownerless core-hit lemma after a proved clipping bound.

The earlier row constructor required an explicit uH<=68 branch limit.
This interface accepts the same inequality as an exact proved consequence.
"""
import model as m

def derive(st,j,positive,credit,side):
    import exact
    m.need(side in ('s','t'),'Ownerless core-hit side')
    rows=exact.ownerless_rows(st,j,positive,credit,{}, {'uH'+side:[0,68]})
    row=next(r for r in rows if r[2]=='conditional core-hit ownerless '+side)
    return row,{'uH'+side:1,'ONE':-68}

def discover(search,point):
    import exact
    changed=False
    for side in 'st':
        row,guard=derive(search.st,search.j,search.positive,search.e,side)
        if any(a==row[0] and b==row[1] for a,b,_ in search.rows):continue
        if sum(v*point[k] for k,v in guard.items())>1e-6:continue
        cert,finished=search.nonstrict_guard(guard)
        if finished:return changed,True
        if cert is None:continue
        exact.check(cert,search.rows,search.eqs,guard,strict=False)
        search.trace.append(dict(kind='ownerless_core_hit',side=side,certificate=cert));search.rows.append(row);changed=True
    return changed,False
