"""Upper mass from the actual minimum defining a core truncation defect.

If phi<r, choose q with phi=q+x_(r-q)-(r-q). Then 0<=q<=phi,
and tau<=(r-q)(phi-q)+q*xi. This convex quadratic in q is at most
max(r*phi,phi*xi). The sentinel phi=r follows from tau<=r*xi.
"""
import model as m

def derive(side,cap):
    m.need(side in 'st' and type(cap) is int and cap>=1,'Canonical core mass cap')
    guards=[{'ONE':32-cap,'rank_k':-1 if side=='s' else 1},{'x'+side:1,'ONE':-cap}]
    return ({'t'+side:1,'phicore'+side:-cap},0,'canonical core minimum mass'),guards

def discover(search,point):
    import math,exact
    changed=False
    for side in 'st':
        r=32+(-1 if side=='s' else 1)*point['rank_k']
        maximum=max(49,496-73*search.j+(14 if search.positive else 0)-search.e)
        trials=sorted(set([max(1,math.ceil(max(r,point['x'+side])-1e-7)),32 if side=='s' else 49,maximum]))
        for cap in trials:
            row,guards=derive(side,cap)
            if any(a==row[0] and b==0 for a,b,label in search.rows):continue
            if any(sum(v*point[k] for k,v in guard.items())>1e-6 for guard in guards):continue
            certificates=[]
            for guard in guards:
                cert,finished=search.nonstrict_guard(guard)
                if finished:return changed,True
                if cert is None:break
                certificates.append(cert)
            if len(certificates)!=2:continue
            for guard,cert in zip(guards,certificates):exact.check(cert,search.rows,search.eqs,guard,strict=False)
            search.trace.append(dict(kind='canonical_phi_mass',side=side,cap=cap,certificates=certificates));search.rows.append(row);changed=True;break
    return changed,False
