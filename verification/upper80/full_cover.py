"""All four-sum hulls and arbitrary outer-subset target translates.

A=E union T union O, where E is the 65-point signed core, T consists
of eight source tails, and O consists of the eight outer points.
The catalogue first uses D=E union T as one hull. A root with k D
summands can be refined by the COMPLETE multisets of its T summands.
These are upper covers, and require no additional additive structure.
"""
from functools import lru_cache
from itertools import combinations_with_replacement
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import model as m
ONE={'ONE':1}

@lru_cache(None)
def outer():
    answer=[]
    for side,sign in [('s',1),('t',-1)]:
        row={'M'+side:sign,'X'+side:sign};answer.append(dict(row))
        for letter in 'ghd':row=m.add((1,row),(sign,{'%s%s'%(letter,side):1}));answer.append(row)
    return answer

@lru_cache(None)
def tails():
    return [{'R'+side:sign,off+side:sign} for side,sign in [('s',1),('t',-1)] for off in 'abce']

@lru_cache(None)
def roots():
    return tuple(chosen for q in range(5) for chosen in combinations_with_replacement(range(8),q))

@lru_cache(None)
def children(root):
    k=4-len(roots()[root]);m.need(k>0,'A four-outer singleton cannot be refined')
    return tuple(chosen for q in range(k+1) for chosen in combinations_with_replacement(range(8),q))

@lru_cache(None)
def interval(root,child=-1):
    m.need(type(root) is int and 0<=root<len(roots()),'Complete four-sum root index')
    selected=roots()[root];k=4-len(selected);centre=m.add(*[(1,outer()[i]) for i in selected])
    if child==-1:
        return m.add((1,centre),(-k,{'Mt':1})),m.add((1,centre),(k,{'Ms':1}))
    m.need(type(child) is int and 0<=child<len(children(root)),'Complete source refinement index')
    chosen=children(root)[child];k-=len(chosen);centre=m.add((1,centre),*[(1,tails()[i]) for i in chosen])
    return m.add((1,centre),(-k,{'Rt':1})),m.add((1,centre),(k,{'Rs':1}))

@lru_cache(None)
def leaves():
    return tuple((i,j) for i,chosen in enumerate(roots()) for j in (range(len(children(i))) if len(chosen)<4 else [-1]))

def shift(mask):
    m.need(type(mask) is int and 0<=mask<256,'An actual subset of eight outer points')
    return m.add(*[(1,row) for i,row in enumerate(outer()) if mask>>i&1])

def bracket(target,mask,width,margin=0):
    m.need(type(width) is int and width>=1 and type(margin) is int and margin>=0,'Full target bracket parameters')
    centre=shift(mask)
    return [m.add((1,centre),(-1,{'St':1}),(margin,ONE),(-1,target)),
            m.add((1,target),(width-1+margin,ONE),(-1,centre),(-1,{'Ss':1}))]

def exclusion(target,node,direction,width):
    m.need(direction in (0,1),'Full-cover exclusion direction');lo,hi=interval(*node)
    return m.add((1,target),(width,ONE),(-1,lo)) if direction==0 else m.add((1,hi),(1,ONE),(-1,target))

def containment(target,node,width):
    lo,hi=interval(*node)
    return [m.add((1,lo),(-1,target),(1-width,ONE)),m.add((1,target),(-1,hi))]

def initial_nodes():return {(i,-1) for i in range(len(roots()))}

def profile(positive,width,bracket_width):
    if not positive:return 1,0
    if width==1:return 1,bracket_width-1
    return 2*(width-1)+1,0

def copy_probes(probes):
    return [dict(target=dict(p['target']),mask=p['mask'],width=p['width'],margin=p['margin'],
                 nodes={tuple(n) for n in p['nodes']},forced=p['forced']) for p in probes]

def export_probes(probes):
    return [dict(p,nodes=sorted(p['nodes'])) for p in probes]

def refine(nodes,root):
    m.need((root,-1) in nodes and len(roots()[root])<4,'A live refinable four-sum root')
    nodes.remove((root,-1));nodes.update((root,i) for i in range(len(children(root))))

def candidate(point,width,margin,used):
    """Discovery heuristic only; every returned bracket must be certified."""
    ev=lambda row:sum(c*point[k] for k,c in row.items())
    ordered=sorted((ev(interval(*node)[0]),ev(interval(*node)[1]),node) for node in leaves())
    gaps=[];end=ordered[0][1];end_node=ordered[0][2]
    for lo,hi,node in ordered:
        if lo-end-1>=width-1e-7:gaps.append((end+1,lo-1,end_node))
        if hi>end:end=hi;end_node=node
    answer=[]
    for mask in range(256):
        centre=shift(mask);value=ev(centre);L=value-point['St']+margin;R=value+point['Ss']-margin
        for a,b,node in gaps:
            lo,hi=max(a,L),min(b,R)
            if hi-lo+1<width-1e-7:continue
            target=m.add((1,interval(*node)[1]),(1,ONE)) if a>=L else m.add((1,centre),(-1,{'St':1}),(margin,ONE))
            key=(tuple(sorted((k,c) for k,c in target.items() if c)),mask)
            if key in used:continue
            answer.append((hi-lo+1,mask,target))
    return sorted(answer,key=lambda x:(-x[0],x[1]))[:8]

def verify():
    import random
    rng=random.Random(81261024);checks=0
    m.need(len(roots())==495 and len(leaves())==4845,'Complete stars-and-bars four-sum catalogues')
    for trial in range(100):
        x={'ONE':1};actual=[]
        for side,sign in [('s',1),('t',-1)]:
            r=rng.randrange(2,8);core=sorted(rng.sample(range(1,r+5),r));R=core[-1]
            offs=sorted(rng.sample(range(1,30),4));source=core+[R+a for a in offs]
            x.update({'R'+side:R,'M'+side:R+offs[-1],'S'+side:sum(source)})
            x.update({key+side:value for key,value in zip('abce',offs)})
            x.update({key+side:rng.randrange(1,25) for key in 'Xghd'})
            actual.extend(sign*a for a in source)
        ev=lambda row:sum(c*x[k] for k,c in row.items())
        actual=[0,*actual,*(ev(row) for row in outer())]
        two={a+b for a in actual for b in actual};four={a+b for a in two for b in two}
        enlarged=set()
        for node in leaves():
            lo,hi=interval(*node);enlarged.update(range(ev(lo),ev(hi)+1))
        m.need(four<=enlarged,'Every actual four-sum is in the refined catalogue')
        frontier=initial_nodes()
        for i,chosen in enumerate(roots()):
            if len(chosen)<4:refine(frontier,i)
        m.need(frontier==set(leaves()),'Every refinement child is retained')
        checks+=1
    rejected=False
    try:refine(set(),0)
    except ValueError:rejected=True
    m.need(rejected,'Missing-root refinement must be rejected')
    return dict(status='PASS_COMPLETE_FOUR_SUM_ENVELOPE',global_upper_bound_certified=False,
                physical_set_checks=checks,root_components=495,refined_components=4845,negative_controls=1)

if __name__=='__main__':
    import json
    print(json.dumps(verify()))
