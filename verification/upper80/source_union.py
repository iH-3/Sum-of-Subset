"""Complete 2D capacity: 2E, eight core translates and 36 tail pairs.

The selected edges form two chains rooted in 2E. Each edge saves F-gap.
Tail-pair points already in these sets have no additional cost. Every
membership assertion is an independently checked affine implication.
"""
from itertools import combinations_with_replacement
import model as m
from full_window import core_capacity
ONE={'ONE':1}
PAIRS=tuple(combinations_with_replacement(range(8),2))

def tails():
    return [m.add((sign,{'R'+side:1}),(sign,{off+side:1}))
            for side,sign in [('s',1),('t',-1)] for off in 'abce']

def gaps():
    return [m.add((1,{off+side:1}),(-1,{} if i==0 else {'abce'[i-1]+side:1}))
            for side in 'st' for i,off in enumerate('abce')]

def shape_lengths(case):
    from first_gap_core import CASES
    m.need(type(case) is int and 0<=case<4,'First-gap core prefix shape')
    h,ps,pt=CASES[case];answer={}
    for side,t,sign in [('s',ps,-1),('t',pt,1)]:
        weight=h-t;baseline={'ONE':32*weight-(h-1)*t,'rank_k':weight*sign}
        answer[side]=m.add((1,{'ONE':32-t,'rank_k':sign,'t'+side:-1}),(1,baseline))
    return h,answer

def membership(pair,witness,first_gap_case=None,interval='ordinary'):
    m.need(tuple(pair) in PAIRS,'Ordered source tail-pair inventory')
    points=tails();p=m.add(*[(1,points[i]) for i in pair])
    ls={'ONE':32,'rank_k':-1,'ts':-1};lt={'ONE':32,'rank_k':1,'tt':-1}
    if witness=='shape_double':
        h,lengths=shape_lengths(first_gap_case)
        # The three prefix-pair intervals overlap/abut when each length
        # is at least 2h+2, and then fill this entire double-core interval.
        return [m.add(((2*h+2),ONE),(-1,lengths[s])) for s in 'st']+[
            m.add((1,p),(-2,lengths['s']),(-2*h,ONE)),m.add((-1,p),(-2,lengths['t']),(-2*h,ONE))]
    if witness=='double_prefix':
        return [m.add((1,p),(-2,ls)),m.add((-1,p),(-2,lt))]
    if witness=='zero':u={}
    elif witness=='core_s':u={'Rs':1}
    elif witness=='core_t':u={'Rt':-1}
    else:
        m.need(type(witness) is int and 0<=witness<8,'Actual source shift witness')
        u=points[witness]
    v=m.add((1,p),(-1,u))
    if interval!='ordinary':
        h,lengths=shape_lengths(first_gap_case)
        m.need(interval in ('shape_s','shape_t'),'First-gap prefix interval selector')
        if interval=='shape_s':return [m.add(((h+1),ONE),(-1,v)),m.add((1,v),(-h,ONE),(-1,lengths['s']))]
        return [m.add((1,v),((h+1),ONE)),m.add((-1,v),(-h,ONE),(-1,lengths['t']))]
    return [m.add((1,v),(-1,ls)),m.add((-1,v),(-1,lt))]

def derive(proof,first_gap_case=None):
    shape=proof.get('core_shape');m.need(shape is None or type(shape) is int and shape==first_gap_case,'Licensed first-gap source capacity')
    mode=proof['base_capacity'];m.need(mode in ('hull','mass'),'Core double-sum capacity')
    prefix=proof.get('core_prefix',{})
    m.need(type(prefix) is dict and set(prefix)<=set('st'),'Canonical source prefix inventory')
    m.need(not prefix or mode=='mass','Canonical source prefix requires mass capacity')
    base=core_capacity(2,shape,prefix) if mode=='mass' else {'Rs':2,'Rt':2,'ONE':1}
    edges=proof['edges'];m.need(len(edges)==len(set(edges)) and all(type(i) is int and 0<=i<8 for i in edges),'Two rooted source chains, no repeated edge')
    body=m.add((1,{'K':1}),(-1,base),(-556,ONE))
    for i in edges:body=m.add((1,body),(1,{'F':1}),(-1,gaps()[i]))
    guards=[];seen=set()
    for item in proof['covered']:
        pair=tuple(item['pair']);m.need(pair not in seen,'Each tail pair is rebated once');seen.add(pair)
        guards.extend(membership(pair,item['witness'],shape,item.get('interval','ordinary')))
        body=m.add((1,body),(1,ONE))
    return body,guards

def discover(search,point):
    import exact
    from first_gap_core import shape_case
    shape=getattr(search,'core_shape',None)
    if shape is None:shape=shape_case(dict(j=search.j,positive=search.positive,limits=search.limits))
    ev=lambda row:sum(c*point[k] for k,c in row.items())
    edges=[i for i,g in enumerate(gaps()) if ev(g)<point['F']-1e-7]
    prefix={}
    if getattr(search,'source_canonical_gaps',False):
        import math,first_gap_core
        for side in 'st':
            w=0
            if shape is not None:
                h,ps,pt=first_gap_core.CASES[shape];w=h-(ps if side=='s' else pt)
            prefix[side]=min(12,max(0,math.floor(point['phicore'+side]-w-2+1e-7)))
    mode='mass' if ev(core_capacity(2,shape,prefix))<2*(point['Rs']+point['Rt'])+1 else 'hull'
    proof=dict(base_capacity=mode,edges=edges,covered=[]);certificates=[]
    if prefix and mode=='mass':proof['core_prefix']=prefix
    if shape is not None:proof['core_shape']=shape
    witnesses=[(w,'ordinary') for w in ('double_prefix','zero','core_s','core_t',*range(8))]
    if shape is not None:witnesses=[('shape_double','ordinary'),*witnesses,*[(w,interval) for interval in ('shape_s','shape_t') for w in ('zero','core_s','core_t',*range(8))]]
    for pair in PAIRS:
        for witness,interval in witnesses:
            guards=membership(pair,witness,shape,interval)
            if any(ev(g)>1e-6 for g in guards):continue
            local=[]
            for guard in guards:
                cert,finished=search.nonstrict_guard(guard)
                if finished:return False,True
                if cert is None:break
                local.append(cert)
            if len(local)==len(guards):
                item=dict(pair=pair,witness=witness)
                if interval!='ordinary':item['interval']=interval
                proof['covered'].append(item);certificates.extend(local);break
    body,guards=derive(proof,shape)
    if ev(body)<=1e-7:return False,False
    if any(row==body and rhs==0 for row,rhs,_ in search.rows):return False,False
    for guard,cert in zip(guards,certificates):exact.check(cert,search.rows,search.eqs,guard,strict=False)
    search.trace.append(dict(kind='source_union_capacity',proof=proof,certificates=certificates))
    search.rows.append((body,0,'complete double-source union capacity'))
    return True,False
