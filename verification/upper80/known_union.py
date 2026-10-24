"""Conditional cardinality bound from explicitly known source subsets.

The exact replay checks interval hull and connected-chain guards. When the
core excess is zero these subsets are the full sources, so the bound can
recover the complete native union, including all higher multiplicities.
"""
import model as m
ONE={'ONE':1}
def add(*args):return m.add(*args)

def tail_catalogue(st,Z,side):
    m.need(side in 'st' and st.get('H'+side)==1 and st.get('O'+side)!=1,'Highest retained centre is H')
    endpoint=add((1,Z['H'+side]),(1,{'R'+side:1}))
    guards=[{k:-v for k,v in endpoint.items()},{'e'+side:1,'X'+side:-1,'g'+side:-1,'h'+side:-1}]
    points=[]
    for name,status in sorted(st.items()):
        if status==1 and name[-1]==side:
            for off in 'abce':points.append((name+':'+off,add((1,Z[name]),(1,{'R'+side:1,off+side:1}))))
    points.extend((label,point) for label,point in sorted(m.fixed_forms().items()) if ('+' in label)==(side=='s'))
    return endpoint,guards,points

def tail_exclusion(st,Z,side,index,direction):
    end,_,points=tail_catalogue(st,Z,side)
    m.need(type(index) is int and 0<=index<len(points) and direction in (0,1),'Core-tail exclusion index')
    value=points[index][1]
    return add((1,value),(-1,end)) if direction==0 else add((1,{'S'+side:1}),(1,ONE),(-1,value))

def tail_capacity(st,Z,side,excluded):
    end,_,points=tail_catalogue(st,Z,side)
    m.need(set(excluded)<=set(range(len(points))),'Core-tail excluded inventory')
    return add((1,{'S'+side:1,'hole_W':-1}),(-1,end)),len(points)-len(set(excluded)),'top core tail capacity'

def joint_tail_capacity(st,Z,excluded,credit):
    m.need(set(excluded)==set('st'),'Both core-tail licenses')
    row={'Ss':1,'St':1,'hole_W':-2};remaining=0
    for side in 'st':
        end,_,points=tail_catalogue(st,Z,side);count=4*sum(status==1 and name[-1]==side for name,status in st.items())
        m.need(set(excluded[side])<=set(range(len(points))),'Joint core-tail exclusion inventory')
        remaining+=sum(i not in excluded[side] for i in range(count));row=add((1,row),(-1,end))
    return row,remaining+84-credit,'joint top core tail capacity'

def catalogue(st,Z,modes):
    import exact
    m.need(set(modes)==set('st') and all(type(v) is int and v in (0,1) for v in modes.values()),'Known prefix modes')
    prefixes={s:({'ONE':31,'rank_k':-1 if s=='s' else 1,'t'+s:-1,'x'+s:1} if modes[s] else {}) for s in 'st'}
    output={}
    for s,o in [('s','t'),('t','s')]:
        lower={k:-v for k,v in prefixes[o].items()};upper=prefixes[s]
        points=[exact.signed_source_point(tag,s) for tag in exact.POINT_TAGS]
        lam={'d'+s:1,'M'+s:-2,'X'+s:-2,'g'+s:-1}
        leading=[(add((1,lam),(2,lower)),add((1,lam),(2,upper)))]
        leading.extend((add((1,lam),(1,pt),(1,lower)),add((1,lam),(1,pt),(1,upper))) for pt in points)
        for i,a in enumerate(points):
            for b in points[i:]:
                pt=add((1,lam),(1,a),(1,b));leading.append((pt,pt))
        all_components=list(leading);retained=sorted(name for name,status in st.items() if status==1 and name[-1]==s)
        for name in retained:
            all_components.append((add((1,Z[name]),(1,lower)),add((1,Z[name]),(1,upper))))
            for pt in points:
                value=add((1,Z[name]),(1,pt));all_components.append((value,value))
        output[s]=dict(leading=leading,components=all_components,count=len(retained))
    return prefixes,output

def recipe(st,Z,point):
    ev=lambda row:sum(v*point[k] for k,v in row.items())
    modes={s:int(31+(-1 if s=='s' else 1)*point['rank_k']-point['t'+s]+point['x'+s]>=0) for s in 'st'}
    _,data=catalogue(st,Z,modes);answer=dict(modes=modes,sides={})
    for side,entry in data.items():
        chains=[];current=[];end=None
        for i,(lo,hi) in sorted(enumerate(entry['leading']),key=lambda item:(ev(item[1][0]),ev(item[1][1]))):
            left,right=ev(lo),ev(hi)
            if end is None or left>end+1+1e-7:
                if current:chains.append(current)
                current=[i];end=right
            elif right>end+1e-7:current.append(i);end=right
        if current:chains.append(current)
        discarded=[];inside=[];S=point['S'+side]
        for i,(lo,hi) in enumerate(entry['components']):
            left,right=ev(lo),ev(hi)
            if right<1-1e-7:discarded.append((i,0))
            elif left>S+1e-7:discarded.append((i,1))
            else:inside.append((max(1,left),min(S,right),i))
        groups=[];current=[];end=None
        def finish(members):
            lo=min(members,key=lambda i:ev(entry['components'][i][0]));hi=max(members,key=lambda i:ev(entry['components'][i][1]))
            return dict(members=members,lo=lo if ev(entry['components'][lo][0])>=1 else None,hi=hi if ev(entry['components'][hi][1])<=S else None)
        for left,right,i in sorted(inside):
            # Adjacency saves no length in an upper bound; only merge overlap.
            if end is None or left>end+1e-7:
                if current:groups.append(finish(current))
                current=[i];end=right
            else:current.append(i);end=max(end,right)
        if current:groups.append(finish(current))
        answer['sides'][side]=dict(chains=chains,groups=groups,discarded=discarded)
    return answer

def derive(st,Z,proof,credit):
    prefixes,data=catalogue(st,Z,proof['modes']);guards=[{k:-v for k,v in row.items()} for row in prefixes.values()]
    body={'delta':-1};m.need(set(proof['sides'])==set('st'),'Both known-union sides')
    for side,entry in data.items():
        specification=proof['sides'][side];leading=entry['leading'];components=entry['components'];previous_end=None;used=set()
        lower_bound={}
        for chain in specification['chains']:
            m.need(chain and all(type(i) is int and 0<=i<len(leading) and i not in used for i in chain) and len(chain)==len(set(chain)),'Known leading chain')
            used.update(chain);first=leading[chain[0]][0];end=None
            for i in chain:
                lo,hi=leading[i];guards.append(add((1,lo),(-1,hi)))
                if end is not None:guards.extend([add((1,end),(-1,hi)),add((1,lo),(-1,end),(-1,ONE))])
                end=hi
            if previous_end is not None:guards.append(add((1,previous_end),(-1,first),(1,ONE)))
            previous_end=end;lower_bound=add((1,lower_bound),(1,end),(-1,first),(1,ONE))
        seen=set();upper_bound={};S={'S'+side:1}
        for i,direction in specification['discarded']:
            m.need(type(i) is int and 0<=i<len(components) and i not in seen and direction in (0,1),'Discarded known component')
            seen.add(i);lo,hi=components[i]
            guards.append(hi if direction==0 else add((1,S),(1,ONE),(-1,lo)))
        for group in specification['groups']:
            members=group['members'];m.need(members and len(members)==len(set(members)),'Known upper group')
            m.need(all(type(i) is int and 0<=i<len(components) and i not in seen for i in members),'Known upper component inventory');seen.update(members)
            li,ui=group['lo'],group['hi']
            m.need(li is None or type(li) is int and li in members,'Known lower hull anchor')
            m.need(ui is None or type(ui) is int and ui in members,'Known upper hull anchor')
            lo=ONE if li is None else components[li][0];hi=S if ui is None else components[ui][1]
            guards.append(add((1,lo),(-1,hi),(-1,ONE)))
            for i in members:
                a,b=components[i]
                if li is not None:guards.append(add((1,lo),(-1,a)))
                if ui is not None:guards.append(add((1,b),(-1,hi)))
            upper_bound=add((1,upper_bound),(1,hi),(-1,lo),(1,ONE))
        m.need(seen==set(range(len(components))),'Complete known upper union')
        size=add((1,prefixes['s']),(1,prefixes['t']),(11,ONE))
        body=add((1,body),(1,lower_bound),(entry['count'],size),(-1,upper_bound))
    unique=[];seen=set()
    for row in guards:
        key=tuple(sorted(row.items()))
        if key not in seen:seen.add(key);unique.append(row)
    return (body,-credit,'known native union capacity'),unique

def cover_chains(st,Z,point):
    ev=lambda row:sum(v*point[k] for k,v in row.items())
    modes={s:int(31+(-1 if s=='s' else 1)*point['rank_k']-point['t'+s]+point['x'+s]>=0) for s in 'st'}
    _,data=catalogue(st,Z,modes);answer={}
    for side,entry in data.items():
        chains=[];chain=[];end=None
        for i,(lo,hi) in sorted(enumerate(entry['components']),key=lambda item:(ev(item[1][0]),ev(item[1][1]))):
            left,right=ev(lo),ev(hi)
            if end is None or left>end+1+1e-7:
                if chain:chains.append(chain)
                chain=[i];end=right
            elif right>end+1e-7:chain.append(i);end=right
        if chain:chains.append(chain)
        answer[side]=chains
    return modes,data,answer

def cover_guards(st,Z,modes,side,chain,label):
    forms=m.fixed_forms();m.need(label in forms and side in 'st' and ('+' in label)==(side=='s'),'Known fixed-cover side')
    prefixes,data=catalogue(st,Z,modes);items=data[side]['components'];seen=set();end=None
    m.need(chain and len(chain)==len(set(chain)) and all(type(i) is int and 0<=i<len(items) for i in chain),'Known fixed-cover chain')
    guards=[{k:-v for k,v in row.items()} for row in prefixes.values()];start=items[chain[0]][0]
    for i in chain:
        lo,hi=items[i];guards.append(add((1,lo),(-1,hi)))
        if end is not None:guards.extend([add((1,end),(-1,hi)),add((1,lo),(-1,end),(-1,ONE))])
        end=hi
    guards.extend([add((1,start),(-1,forms[label])),add((1,forms[label]),(-1,end))])
    return guards
