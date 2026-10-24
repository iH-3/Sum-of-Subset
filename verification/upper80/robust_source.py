"""Retain all individually licensed pieces of a proposed source hull.

One missing membership no longer discards the whole useful group. The
unlicensed pieces remain explicitly charged and can form later groups.
Only violated complete capacities are saved; no branch is sampled away.
"""
import model as m,averaged_source as av

def discover(search,point):
    import exact
    m.need(not search.positive,'Robust source discovery uses zero holes')
    ev=lambda row:sum(v*point[k] for k,v in row.items())
    options=[]
    for keep in range(1,5):
        result=av.recipe(point,keep);_,intervals,masses,clusters=result
        estimate=sum(min(max(ev(intervals[i][1]) for i in g)-min(ev(intervals[i][0]) for i in g)+12,sum(ev(masses[i]) for i in g)) for g in clusters)
        options.append((estimate,keep,result))
    _,_,(proof,intervals,masses,clusters)=min(options,key=lambda x:(x[0],-x[1]))
    proof['nonempty_hulls']=True;certs=[];finished=[False];suggestions={}
    def visit(indices):
        if finished[0] or not indices:return
        lo=min((intervals[i][0] for i in indices),key=ev);hi=max((intervals[i][1] for i in indices),key=ev)
        hull=ev(hi)-ev(lo)+12
        if sum(ev(masses[i]) for i in indices)<=hull+1e-7:
            proof['groups'].extend(dict(components=[i],mass=True) for i in indices);return
        retained=[];local=[];missing=[]
        for i in indices:
            a,b=intervals[i];guards=[m.add((1,lo),(-1,a)),m.add((1,b),(-1,hi))];cc=[]
            for guard in guards:
                cert,done=search.nonstrict_guard(guard)
                if done:finished[0]=True;return
                if cert is None:
                    key=tuple(sorted((k,v) for k,v in guard.items() if v))
                    if key:suggestions[key]=dict(guard=dict(key),gain=(sum(ev(masses[j]) for j in indices)-hull)/12,components=len(indices))
                    break
                cc.append(cert)
            if len(cc)==2:retained.append(i);local.extend(cc)
            else:missing.append(i)
        if retained and sum(ev(masses[i]) for i in retained)>hull+1e-7:
            proof['groups'].append(dict(components=retained,lower=lo,upper=hi));certs.extend(local)
            # Strictly fewer components remain; every one is still charged.
            visit(missing);return
        if len(indices)==1:
            proof['groups'].append(dict(components=indices,mass=True));return
        cut=max(range(1,len(indices)),key=lambda k:ev(intervals[indices[k]][0])-ev(intervals[indices[k-1]][1]))
        visit(indices[:cut]);visit(indices[cut:])
    for cluster in clusters:visit(cluster)
    if finished[0]:return False,True
    search.source_split_candidates=sorted(suggestions.values(),key=lambda x:x['gain'],reverse=True)[:12]
    row,guards=av.derive(proof);m.need(len(certs)==len(guards),'Individually licensed source membership order')
    if ev(row[0])<=1e-7:return False,False
    if any(a==row[0] and b==0 for a,b,_ in search.rows):return False,False
    for cert,guard in zip(certs,guards):exact.check(cert,search.rows,search.eqs,guard,strict=False)
    search.trace.append(dict(kind=av.TRACE_KIND,proof=proof,certificates=certs));search.rows.append(row)
    return True,False
