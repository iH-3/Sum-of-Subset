"""Research-only explicit interval cover of the retained source resources.

This is a necessary cover of a physical target, not a global theorem.
A bracketed interval of width 1 (zero holes) or 8 (at most seven holes)
must intersect at least one component.
The core hull may contain extra points. Ordinary and leading resources are
therefore enlarged, which is safe when proving that a target point is missing.
"""
import model as m


def catalogue(st,Z,side):
    m.need(side in 'st','Physical cover side');other='t' if side=='s' else 's'
    lower={'R'+other:-1};upper={'R'+side:1};tails=[]
    for physical in (side,other):
        sign=1 if physical==side else -1
        for off in 'abce':tails.append({ 'R'+physical:sign,off+physical:sign })
    result=[]
    def append(name,lo,hi):result.append((name,lo,hi))
    for name in sorted(key for key,status in st.items() if status==1 and key[-1]==side):
        center=Z[name]
        append(name+':core',m.add((1,center),(1,lower)),m.add((1,center),(1,upper)))
        for i,tail in enumerate(tails):
            point=m.add((1,center),(1,tail));append(name+':tail'+str(i),point,point)
    lam={'d'+side:1,'M'+side:-2,'X'+side:-2,'g'+side:-1}
    append('L:core',m.add((1,lam),(2,lower)),m.add((1,lam),(2,upper)))
    for i,tail in enumerate(tails):
        append('L:coretail'+str(i),m.add((1,lam),(1,tail),(1,lower)),m.add((1,lam),(1,tail),(1,upper)))
    for i,first in enumerate(tails):
        for j,second in enumerate(tails[i:],i):
            point=m.add((1,lam),(1,first),(1,second));append('L:pair'+str((i,j)),point,point)
    for label,point in sorted(m.fixed_forms().items()):
        if ('+' in label)==(side=='s'):append(label,point,point)
    return result


def probe(components,index):
    m.need(type(index) is int and 0<=index<len(components),'Coverage probe endpoint')
    return m.add((1,components[index][2]),(1,{'ONE':1}))


def bracket(components,side,index,width=1):
    target=probe(components,index)
    return [m.add((1,{'ONE':1}),(-1,target)),m.add((1,target),(width-1,{'ONE':1}),(-1,{'S'+side:1}))]


def exclusion(components,index,component,direction,width=1):
    m.need(type(component) is int and 0<=component<len(components) and direction in (0,1),'Coverage exclusion component')
    target=probe(components,index);_,lo,hi=components[component]
    return m.add((1,target),(-1,lo),(width,{'ONE':1})) if direction==0 else m.add((1,hi),(-1,target),(1,{'ONE':1}))


def containment(components,index,component,width=1):
    m.need(type(component) is int and 0<=component<len(components),'Coverage remaining component')
    target=probe(components,index);_,lo,hi=components[component]
    return [m.add((1,lo),(-1,target),(1-width,{'ONE':1})),m.add((1,target),(-1,hi))]
