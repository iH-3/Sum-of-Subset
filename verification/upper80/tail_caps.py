"""Count q-sums using only the last L elements above a certified threshold.

If every summand outside the last L is at most B, every q-sum above
(q-1)max+B uses only those L elements. There are at most C(q+L-1,q)
multisets. The same statement holds at the reflected minimum.
"""
from math import comb
import model as m,full_cover as fc
ONE={'ONE':1}

def core_prefix(side,keep,order,shape=None):
    """Lower excess mass of the smallest r-keep-1 core elements."""
    m.need(side in ('s','t') and type(keep) is int and 1<=keep<=4,'Core tail-cap side and count')
    m.need(type(order) is int and 0<=order<=13-keep,'Core tail-cap canonical prefix order')
    w=t=0
    if shape is not None:
        from first_gap_core import CASES
        m.need(type(shape) is int and 0<=shape<4,'Physical tail-cap shape')
        h,ps,pt=CASES[shape];t=ps if side=='s' else pt;w=h-t
    base={'ONE':w*(31-keep-t),'rank_k':w*(-1 if side=='s' else 1)}
    extra={'phicore'+side:order,'ONE':-order*w-order*(order+2*keep+1)//2}
    return {key:value for key,value in m.add((1,base),(1,extra)).items() if value}

def derive(lower,upper,node,side,keep,order=0,shape=None):
    m.need(side in ('s','t') and type(keep) is int and 1<=keep<=4,'Tail-cap side and count')
    root,child=node;lo,hi=fc.interval(*node)
    q=4-len(fc.roots()[root])-(len(fc.children(root)[child]) if child>=0 else 0)
    m.need(1<=q<=4,'Positive tail-cap sum power')
    distance=m.add((1,hi),(-1,lower)) if side=='s' else m.add((1,upper),(-1,lo))
    if child<0:
        m.need(shape is None and type(order) is int and order==0,'Coarse source cap has no core prefix')
        gap={'e'+side:1}
        if keep<4:gap['cba'[keep-1]+side]=-1
        guard=m.add((1,distance),(-1,gap),(1,ONE))
    else:
        prefix=core_prefix(side,keep,order,shape)
        # keep*d_(r-keep) <= tau-xi-prefix. The +1 below ensures the
        # scaled window threshold is strictly beyond every excluded sum.
        guard=m.add((keep,distance),(-(keep+1),{'x'+side:1}),(1,{'t'+side:1}),(-1,prefix),(1-keep*keep,ONE))
    return guard,comb(q+keep-1,q)
