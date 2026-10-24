"""Upper mass from the actual minimum defining a core truncation defect.

If phi<r, choose q with phi=q+x_(r-q)-(r-q). Then 0<=q<=phi,
and tau<=(r-q)(phi-q)+q*xi. This convex quadratic in q is at most
max(r*phi,phi*xi). The sentinel phi=r follows from tau<=r*xi.
"""
import model as m

def tail_derive(side,cap,case=None,licensed_shape=None):
    """Exclude the last-index minimizer when xi>=phi+1.

    Then q>=1. The convex mass bound on 1<=q<=phi is bounded by
    xi+H*(phi-1) when r-1,xi<=H. A physical first-gap remainder
    permits the same argument after translating all its quantities.
    """
    m.need(side in ('s','t') and type(cap) is int and cap>=1,'Canonical tail cap')
    t=w=0
    if case is not None:
        import first_gap_core as fg
        m.need(type(case) is int and case==licensed_shape and 0<=case<4,'Licensed canonical tail shape')
        h,ps,pt=fg.CASES[case];t=ps if side=='s' else pt;w=h-t
    n={'ONE':32-t,'rank_k':-1 if side=='s' else 1};baseline={k:w*v for k,v in n.items()}
    guards=[m.add((1,n),(-cap-1,{'ONE':1})),{'x'+side:1,'ONE':-w-cap},
            m.add((1,{'phicore'+side:1}),(-1,n),(1,{'ONE':1})),
            {'phicore'+side:1,'x'+side:-1,'ONE':1}]
    body=m.add((1,{'t'+side:1}),(-1,baseline),(-1,{'x'+side:1}),(-cap,{'phicore'+side:1}),(w+cap*(w+1),{'ONE':1}))
    return (body,0,'canonical nonlast minimizer mass'),guards

def discover_tail(search,point):
    import math,exact,first_gap_core as fg
    changed=False;case=getattr(search,'core_shape',None)
    for side in 'st':
        t=w=0
        if case is not None:
            h,ps,pt=fg.CASES[case];t=ps if side=='s' else pt;w=h-t
        n=32+(-1 if side=='s' else 1)*point['rank_k']-t
        maximum=max(49,496-73*search.j+(14 if search.positive else 0)-search.e)
        trials=sorted(set([max(1,math.ceil(max(n-1,point['x'+side]-w)-1e-7)),31-t if side=='s' else 48-t,maximum]))
        for cap in trials:
            row,guards=tail_derive(side,cap,case,case)
            if any(a==row[0] and b==0 for a,b,_ in search.rows):continue
            if any(sum(v*point[k] for k,v in g.items())>1e-6 for g in guards):continue
            certificates=[]
            for guard in guards:
                cert,finished=search.nonstrict_guard(guard)
                if finished:return changed,True
                if cert is None:break
                certificates.append(cert)
            if len(certificates)!=len(guards):continue
            for guard,cert in zip(guards,certificates):exact.check(cert,search.rows,search.eqs,guard,strict=False)
            step=dict(kind='canonical_tail_mass',side=side,cap=cap,certificates=certificates)
            if case is not None:step['core_shape']=case
            search.trace.append(step);search.rows.append(row);changed=True;break
    return changed,False

def shifted_derive(side,cap,case,licensed_shape):
    """Apply the canonical minimum to the physically translated remainder.

    With prefix size t, n=r-t and w=h-t, phi(X)=min(n,w+phi(Y)).
    The strict nonsentinel guard identifies phi(Y)=phi(X)-w exactly.
    """
    import first_gap_core as fg
    m.need(type(case) is int and case==licensed_shape and 0<=case<4,'Licensed shifted canonical shape')
    m.need(side in ('s','t') and type(cap) is int and cap>=1,'Shifted canonical mass cap')
    h,ps,pt=fg.CASES[case];t=ps if side=='s' else pt;w=h-t;sign=-1 if side=='s' else 1
    n={'ONE':32-t,'rank_k':sign}
    baseline={key:w*value for key,value in n.items()}
    guards=[m.add((1,n),(-cap,{'ONE':1})),
            {'x'+side:1,'ONE':-cap-w},
            m.add((1,{'phicore'+side:1}),(-1,n),(1,{'ONE':1}))]
    body=m.add((1,{'t'+side:1}),(-1,baseline),(-cap,{'phicore'+side:1}),(cap*w,{'ONE':1}))
    return (body,0,'shifted canonical core minimum mass'),guards

def discover_shifted(search,point):
    import math,exact,first_gap_core as fg
    m.need(search.core_shape is not None,'Shifted canonical discovery requires physical shape')
    changed=False;case=search.core_shape;h,ps,pt=fg.CASES[case]
    for side,t in [('s',ps),('t',pt)]:
        n=32+(-1 if side=='s' else 1)*point['rank_k']-t;w=h-t
        maximum=max(49,496-73*search.j+14-search.e)
        trials=sorted(set([max(1,math.ceil(max(n,point['x'+side]-w)-1e-7)),32-t if side=='s' else 49-t,maximum]))
        for cap in trials:
            row,guards=shifted_derive(side,cap,case,case)
            if any(a==row[0] and b==0 for a,b,label in search.rows):continue
            if any(sum(v*point[k] for k,v in guard.items())>1e-6 for guard in guards):continue
            certificates=[]
            for guard in guards:
                cert,finished=search.nonstrict_guard(guard)
                if finished:return changed,True
                if cert is None:break
                certificates.append(cert)
            if len(certificates)!=len(guards):continue
            for guard,cert in zip(guards,certificates):exact.check(cert,search.rows,search.eqs,guard,strict=False)
            search.trace.append(dict(kind='shifted_canonical_phi_mass',side=side,cap=cap,core_shape=case,certificates=certificates));search.rows.append(row);changed=True;break
    return changed,False

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
