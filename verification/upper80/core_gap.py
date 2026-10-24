"""Exclude full-cover components using guaranteed holes next to an extreme.

For qE, the predecessor mass bounds the second-highest attainable sum.
For qD, the exact gap between its two largest source tails does the same.
An entire target probe must lie in this empty integer interval.
"""
import model as m,full_cover as fc
ONE={'ONE':1}

def canonical_prefix(side,order,shape=None):
    """Extra mass of the smallest r-2 coefficients from their canonical floor.

    All physical ranks here are at least15; after a one-point prefix at
    least14 remain. Thus every order0..12 uses existing remainder indices.
    """
    m.need(side in ('s','t') and type(order) is int and 0<=order<=12,'Canonical predecessor prefix order')
    if order==0:return {}
    w=0
    if shape is not None:
        from first_gap_core import CASES
        m.need(type(shape) is int and 0<=shape<4,'Canonical predecessor physical shape')
        h,ps,pt=CASES[shape];w=h-(ps if side=='s' else pt)
    return {'phicore'+side:order,'ONE':-order*w-order*(order+3)//2}

def gap_interval(node,side,shape=None,prefix=0):
    m.need(side in ('s','t'),'Extreme core gap side');root,child=node
    lo,hi=fc.interval(*node);power=4-len(fc.roots()[root])
    if child<0:
        m.need(power>=1 and shape is None and prefix==0,'Unrefined source gap power')
        loss={'e'+side:1,'c'+side:-1,'ONE':-1}
    else:
        power-=len(fc.children(root)[child]);m.need(power>=1,'Nonsingleton core power gap')
        loss={'x'+side:2,'t'+side:-1}
        if shape is not None:
            from first_gap_core import removed_side_prefix_mass
            loss=m.add((1,loss),(1,removed_side_prefix_mass(shape,side)))
        loss=m.add((1,loss),(1,canonical_prefix(side,prefix,shape)))
    return (m.add((1,hi),(-1,loss)),m.add((1,hi),(-1,ONE))) if side=='s' else (m.add((1,lo),(1,ONE)),m.add((1,lo),(1,loss)))

def guards(target,node,width,side,shape=None,prefix=0):
    m.need(type(width) is int and width>=1,'Whole integer target probe')
    lower,upper=gap_interval(node,side,shape,prefix)
    return [m.add((1,lower),(-1,target)),m.add((1,target),(width-1,ONE),(-1,upper))]

def extreme_only_guard(lower,upper,node,side,shape=None,prefix=0):
    a,b=gap_interval(node,side,shape,prefix)
    # Above the last predecessor bound (or below the first successor bound),
    # only the actual extreme of the component can remain in the window.
    return m.add((1,a),(-1,lower)) if side=='s' else m.add((1,upper),(-1,b))

def punctures(lower,upper,node,holes,shape=None,prefixes=None):
    """Disjoint certified empty subintervals of a charged component hull."""
    m.need(isinstance(holes,list) and len({h['side'] for h in holes})==len(holes),'Distinct punctured hull sides')
    removed={};conditions=[];by_side={}
    for hole in holes:
        side=hole['side'];m.need(side in ('s','t'),'Puncture extreme side')
        a,b=hole['lower'],hole['upper'];glo,ghi=gap_interval(node,side,shape,(prefixes or {}).get(side,0) if node[1]>=0 else 0)
        conditions.extend([m.add((1,glo),(-1,a)),m.add((1,b),(-1,ghi)),m.add((1,lower),(-1,a)),m.add((1,b),(-1,upper)),m.add((1,a),(-1,b),(-1,ONE))])
        removed=m.add((1,removed),(1,b),(-1,a),(1,ONE));by_side[side]=(a,b)
    if len(holes)==2:conditions.append(m.add((1,by_side['t'][1]),(-1,by_side['s'][0]),(1,ONE)))
    return removed,conditions

def discover(search,point):
    import exact,math
    ev=lambda row:sum(v*point[k] for k,v in row.items())
    for pid,state in enumerate(search.full_probes):
        for node in sorted(state['nodes']):
            power=4-len(fc.roots()[node[0]])-(len(fc.children(node[0])[node[1]]) if node[1]>=0 else 0)
            if power<1:continue
            shape=getattr(search,'core_shape',None) if node[1]>=0 else None
            for side in 'st':
                prefix=0
                if getattr(search,'probe_canonical_gaps',False) and node[1]>=0:
                    w=0
                    if shape is not None:
                        from first_gap_core import CASES
                        h,ps,pt=CASES[shape];w=h-(ps if side=='s' else pt)
                    prefix=min(12,max(0,math.floor(point['phicore'+side]-w-2+1e-7)))
                conditions=guards(state['target'],node,state['width'],side,shape,prefix)
                if any(ev(g)>1e-7 for g in conditions):continue
                certs=[]
                for guard in conditions:
                    cert,finished=search.nonstrict_guard(guard)
                    if finished:search.final();return True,True
                    if cert is None:break
                    certs.append(cert)
                if len(certs)<2:continue
                for cert,guard in zip(certs,conditions):exact.check(cert,search.rows,search.eqs,guard,strict=False)
                step=dict(kind='full_cover_gap_exclude',probe=pid,node=node,side=side,certificates=certs)
                if prefix:step['prefix']=prefix
                if shape is not None:step['core_shape']=shape
                search.trace.append(step);search.rows.extend((g,0,'proved empty extreme-sum interval') for g in conditions)
                state['nodes'].remove(node);state['forced']=False
                if not state['nodes']:search.trace.append(dict(kind='full_cover_final',probe=pid));return True,True
                return True,False
    return False,False
