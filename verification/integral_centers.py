#!/usr/bin/env python3
"""Integer row operations on contributing-center forms (standard library only)."""
from functools import lru_cache


def require(condition,message):
    if not condition:raise ValueError(message)


def row_hermite(forms,dimension=8,with_transform=False):
    """Preserve the integer row lattice; never divide a row by a nonunit."""
    require(type(dimension) is int and dimension>0,'Invalid dimension')
    rows=[list(v) for v in forms]
    require(all(len(v)==dimension and all(type(x) is int for x in v) for v in rows),'Noninteger form')
    original=[v[:] for v in rows]
    transform=[[int(i==j) for j in range(len(rows))] for i in range(len(rows))]
    def swap(i,j):
        rows[i],rows[j]=rows[j],rows[i]
        transform[i],transform[j]=transform[j],transform[i]
    def subtract(i,j,q):
        rows[i]=[x-q*y for x,y in zip(rows[i],rows[j])]
        transform[i]=[x-q*y for x,y in zip(transform[i],transform[j])]
    pivot=0
    for col in range(dimension):
        candidate=next((i for i in range(pivot,len(rows)) if rows[i][col]),None)
        if candidate is None:continue
        swap(pivot,candidate)
        for j in range(pivot+1,len(rows)):
            while rows[j][col]:
                q=rows[pivot][col]//rows[j][col]
                subtract(pivot,j,q)
                swap(pivot,j)
        if rows[pivot][col]<0:
            rows[pivot]=[-x for x in rows[pivot]]
            transform[pivot]=[-x for x in transform[pivot]]
        for j in range(pivot):
            q=rows[j][col]//rows[pivot][col]
            subtract(j,pivot,q)
        pivot+=1
    H,U=rows[:pivot],transform[:pivot]
    require(all(row==[sum(c*v[k] for c,v in zip(combination,original)) for k in range(dimension)]
                for row,combination in zip(H,U)),'Invalid integer basis combination')
    return (H,U) if with_transform else H


def contains(H,target):
    remaining=list(target)
    for row in H:
        pivot=next(i for i,v in enumerate(row) if v)
        q,remainder=divmod(remaining[pivot],row[pivot])
        if remainder:return False
        remaining=[x-q*y for x,y in zip(remaining,row)]
    return not any(remaining)


@lru_cache(None)
def certify(forms):
    H,U=row_hermite(forms,with_transform=True)
    known=[i for i in range(8) if contains(H,[int(j==i) for j in range(8)])]
    gaps=[]
    for side,offset in (('p',0),('q',4)):
        for i in range(4):
            target=[0]*8;target[offset+i]=1
            if i<3:target[offset+i+1]=-1
            if contains(H,target):gaps.append(side+str(i+1))
    return dict(rank=len(H),hermite=H,basis_combinations=U,known=known,complete=len(known)==8,
                integral_gaps=gaps,integral_branch=contains(H,[-1,2,-1,-1,-1,2,-1,-1]))


def derive(mode,leading_sides):
    return derive_cached(tuple(mode['slots']),mode['member'],tuple(sorted(leading_sides)))


@lru_cache(None)
def derive_cached(slots,member,leading_sides):
    names=[s+str(i) for s in 'pq' for i in range(1,5)]
    forms=[]
    def add(co):forms.append(tuple(co.get(n,0) for n in names))
    def merge(a,b):return {n:a.get(n,0)+b.get(n,0) for n in set(a)|set(b)}
    centers={}
    for side,other in (('p','q'),('q','p')):
        lead={side+'1':1,side+'2':-1,side+'3':-1,side+'4':-1}
        if side in leading_sides:add(lead)
        for i in range(4):
            centers[side+str(i)]=merge(lead,{side+str(i+1):1})
            centers[side+str(i+4)]=merge(lead,{other+str(i+1):-1})
        centers[side+'8']={side+'2':1,side+'3':-1,side+'4':-1}
        centers[side+'9']={side+'1':-1,side+'2':2,side+'3':-1,side+'4':-1}
    for v in slots:add(centers[v])
    if member!='-':add(centers[member+'9'])
    result=certify(tuple(forms))
    return dict(result,leading_sides=sorted(leading_sides),known_names=[names[i] for i in result['known']])
