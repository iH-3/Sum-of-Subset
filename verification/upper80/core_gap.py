"""Exclude full-cover components using guaranteed holes next to an extreme.

For qE, the predecessor mass bounds the second-highest attainable sum.
For qD, the exact gap between its two largest source tails does the same.
An entire target probe must lie in this empty integer interval.
"""
import model as m,full_cover as fc
ONE={'ONE':1}

def gap_interval(node,side,shape=None):
    m.need(side in 'st','Extreme core gap side');root,child=node
    lo,hi=fc.interval(*node);power=4-len(fc.roots()[root])
    if child<0:
        m.need(power>=1 and shape is None,'Unrefined source gap power')
        loss={'e'+side:1,'c'+side:-1,'ONE':-1}
    else:
        power-=len(fc.children(root)[child]);m.need(power>=1,'Nonsingleton core power gap')
        loss={'x'+side:2,'t'+side:-1}
        if shape is not None:
            from first_gap_core import removed_side_prefix_mass
            loss=m.add((1,loss),(1,removed_side_prefix_mass(shape,side)))
    return (m.add((1,hi),(-1,loss)),m.add((1,hi),(-1,ONE))) if side=='s' else (m.add((1,lo),(1,ONE)),m.add((1,lo),(1,loss)))

def guards(target,node,width,side,shape=None):
    m.need(type(width) is int and width>=1,'Whole integer target probe')
    lower,upper=gap_interval(node,side,shape)
    return [m.add((1,lower),(-1,target)),m.add((1,target),(width-1,ONE),(-1,upper))]

def extreme_only_guard(lower,upper,node,side,shape=None):
    a,b=gap_interval(node,side,shape)
    # Above the last predecessor bound (or below the first successor bound),
    # only the actual extreme of the component can remain in the window.
    return m.add((1,a),(-1,lower)) if side=='s' else m.add((1,upper),(-1,b))

def discover(search,point):
    import exact
    ev=lambda row:sum(v*point[k] for k,v in row.items())
    for pid,state in enumerate(search.full_probes):
        for node in sorted(state['nodes']):
            power=4-len(fc.roots()[node[0]])-(len(fc.children(node[0])[node[1]]) if node[1]>=0 else 0)
            if power<1:continue
            shape=getattr(search,'core_shape',None) if node[1]>=0 else None
            for side in 'st':
                conditions=guards(state['target'],node,state['width'],side,shape)
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
                if shape is not None:step['core_shape']=shape
                search.trace.append(step);search.rows.extend((g,0,'proved empty extreme-sum interval') for g in conditions)
                state['nodes'].remove(node);state['forced']=False
                if not state['nodes']:search.trace.append(dict(kind='full_cover_final',probe=pid));return True,True
                return True,False
    return False,False
