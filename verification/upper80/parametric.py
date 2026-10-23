# RESEARCH PROTOTYPE: no global bound is certified by this file.
"""A relaxation covering all permitted ranks and hole parameters.

All scalar right sides are degree at most two in the rank and affine in w.
Interpolation is exact and checked coefficient-by-coefficient.  Rank k=32-r,
I=k*k, and W=w/2 are represented by nonnegative variables; the polygon
constraints relax their discrete graph, so no parameter is sampled away.
"""
from fractions import Fraction
from functools import lru_cache
import model as m

PLANE_TABLE={}
USED_PLANES=set()
PLANE_GENERATOR=None
USE_PLANES=False
SOURCE_TAIL_RANKS=False
SHARP_PLANES=False
SIDE_PLANES=False
TRIM_SOURCE=False
POINT_OVERLAP=False
CHECKED_PLANES=set()


def majorants(rank,j,e,lo,hi,positive,parameter_excess=None,minimum_tau=0):
    excess=(-14 if positive else 0) if parameter_excess is None else parameter_excess
    args=(rank,j,excess,e,lo,hi)+((minimum_tau,) if minimum_tau else ())
    key=','.join(map(str,args));USED_PLANES.add(key)
    if key not in PLANE_TABLE:
        m.need(PLANE_GENERATOR is not None,'Missing uniform endpoint planes '+key)
        PLANE_TABLE[key]=PLANE_GENERATOR(*args)
    planes=PLANE_TABLE[key];stamp=(key,tuple(tuple(x) for x in planes))
    if stamp in CHECKED_PLANES:return planes
    cap=496-73*j-excess
    points=[]
    for k in range(lo,min(hi,cap-e-minimum_tau)+1):
        for delta,tau in ((e+k,minimum_tau),(cap-minimum_tau,minimum_tau),(e+k,cap-e-k)):
            error=(Fraction(0) if k<=68-rank else Fraction(tau,69-k)) if k<69 else Fraction(651-73*j-excess-delta)
            points.append((k,delta,tau,error))
    for plane in planes:
        m.need(len(plane)==5 and all(type(c) is int for c in plane) and plane[3]>0,'Uniform plane syntax')
        m.need(all(sum(a*b for a,b in zip(plane[:4],pt))<=plane[4] for pt in points),'Uniform plane failed exact vertex check')
    CHECKED_PLANES.add(stamp)
    return planes


def interpolate(samples, positive):
    m.need(len({len(sample) for sample in samples})==1,'Nonconstant row count')
    rr=[]
    for entries in zip(*samples):
        row,b0,label=entries[0]
        m.need(all(a==row and lab==label for a,_,lab in entries),'Nonconstant row inventory')
        _,b1,_=entries[1];_,b2,_=entries[2];_,b3,_=entries[3]
        ci=Fraction(b2-2*b1+b0,2);ck=b1-b0-ci;cw=b3-b0
        m.need(all((2*x).denominator==1 for x in (ci,ck)),'Unexpected fractional interpolation')
        body=m.add((2,row),(-int(2*ck),m.var('rank_k')),(-int(2*ci),m.var('rank_I')),(-2*cw,m.var('hole_W')))
        rr.append((body,2*b0-(2*cw if positive else 0),label))
    return rr


def build(st,j,positive=False,e=0,limits=None,forest_masks=None):
    m.DISABLE_PLANES=True;m.free_planes.cache_clear();m.fixed_planes2.cache_clear()
    w0=2 if positive else 0
    samples=[m.build(st,j,r,None,e,limits,w=w,forest_masks=forest_masks)
             for r,w in ((32,w0),(31,w0),(30,w0),(32,w0+2))]
    # In the zero-hole regime the fourth sample introduces the positive-floor
    # row. Remove it: that regime sets W=0 and never uses its mass premise.
    if not positive:
        names,rows,eqs=samples[-1]
        samples[-1]=(names,[row for row in rows if row[2]!='positive core floor'],eqs)
        # The alpha tail applies only to zero holes; reproduce its w=0 rows
        # in the unused fourth sample, as W is set to zero in this regime.
        alpha_rows=[row for row in samples[0][1] if row[2].startswith('alpha ') ]
        if alpha_rows:
            at=next(i for i,row in enumerate(samples[0][1]) if row[2].startswith('alpha '))
            fourth=list(samples[-1][1]);fourth[at:at]=alpha_rows
            samples[-1]=(names,fourth,eqs)
    rows=interpolate([x[1] for x in samples],positive)
    eqs=interpolate([x[2] for x in samples],positive)
    cap=496-73*j-e-(60 if positive else 0)
    kmax=max((k for k in range(18) if k*k<=cap),default=0)
    rows += [({'rank_k':1},kmax,'parameter rank range'),
             ({'rank_I':1,'rank_k':-kmax},0,'parameter rank chord')]
    for q in range(17):
        rows.append(({'rank_k':2*q+1,'rank_I':-1},q*(q+1),'parameter rank tangent '+str(q)))
    if positive:
        rows += [({'hole_W':-1},-1,'parameter positive holes'),({'hole_W':1},7,'parameter hole cap')]
    else:eqs.append(({'hole_W':1},0,'parameter zero holes'))
    if USE_PLANES:
        Z=m.build.last_Z
        klo,khi=(limits or {}).get('rank_k',(0,17))
        wlo,whi=(limits or {}).get('hole_W',(1,7) if positive else (0,0))
        excess=klo*klo-2*whi
        for name,status in st.items():
            if status!=1:continue
            s=name[-1]
            for typ in 'lu':
                lo,hi=(limits or {}).get(typ+name,(0,72))
                side=s if typ=='l' else ('t' if s=='s' else 's')
                # The smaller core rank is at most 32; the other is at most 50.
                rankmax=32-klo if side=='s' else 32+khi
                for index,(kc,dc,tc,ec,rhs) in enumerate(majorants(rankmax,j,e,lo,hi,positive,excess,58+4*wlo if SHARP_PLANES and positive else 0)):
                    if typ=='l':
                        # -ec*(Z+clip) + kc*clip + dc*delta+tc*tau
                        # <= rhs-ec*(69-rank).
                        body=m.add((-ec,Z[name]),(kc-ec,m.var(typ+name)),(dc,m.var('delta')),
                                   (tc,{'ts':1,'tt':1}),(ec if side=='s' else -ec,m.var('rank_k')))
                        bound=rhs-ec*37
                    else:
                        body=m.add((ec,Z[name]),(-ec,m.var('S'+s)),(kc-ec,m.var(typ+name)),
                                   (dc,m.var('delta')),(tc,{'ts':1,'tt':1}),
                                   (ec if side=='s' else -ec,m.var('rank_k')))
                        bound=rhs+ec*-36
                    rows.append((body,bound,'uniform endpoint '+typ+name+':'+str(index)))
                if SIDE_PLANES:
                    # The next surviving core point uses the deviation mass
                    # of its own side. Its feasible (delta,t_side) triangle
                    # follows by discarding the nonnegative opposite mass.
                    for index,(kc,dc,tc,ec,rhs) in enumerate(majorants(rankmax,j,e,lo,hi,positive,excess)):
                        if typ=='l':
                            body=m.add((-ec,Z[name]),(kc-ec,m.var(typ+name)),(dc,m.var('delta')),
                                       (tc,m.var('t'+side)),(ec if side=='s' else -ec,m.var('rank_k')))
                            bound=rhs-ec*37
                        else:
                            body=m.add((ec,Z[name]),(-ec,m.var('S'+s)),(kc-ec,m.var(typ+name)),
                                       (dc,m.var('delta')),(tc,m.var('t'+side)),
                                       (ec if side=='s' else -ec,m.var('rank_k')))
                            bound=rhs+ec*-36
                        rows.append((body,bound,'uniform endpoint side '+typ+name+':'+str(index)))
    for name in ('rank_k','hole_W'):
        if name not in (limits or {}):continue
        lo,hi=limits[name];maximum=17 if name=='rank_k' else 7
        m.need(type(lo) is int and type(hi) is int and 0<=lo<=hi<=maximum,'Parameter branch interval')
        rows += [({name:-1},-lo,'parameter branch lower '+name),({name:1},hi,'parameter branch upper '+name)]
        if name=='rank_k':
            rows.append(({'rank_I':1,'rank_k':-lo-hi},-lo*hi,'parameter branch chord'))
    for side in 'st':
        name='B'+side
        if name not in (limits or {}):continue
        lo,hi=limits[name]
        m.need(type(lo) is int and type(hi) is int and 4<=lo<=hi<=10,'Quartet fringe branch interval')
        rows += [({name:-1},-lo,'quartet branch lower '+side),({name:1},hi,'quartet branch upper '+side)]
        if lo>=5:
            # All pair sums involving e exceed e, giving four values. A fifth
            # value must be a sum from {a,b,c}, whose maximum is 2c.
            rows.append(({'e'+side:1,'c'+side:-2},-1,'fifth quartet fringe '+side))
    for attr in ('edges','retained','Z','long'):setattr(build,'last_'+attr,getattr(m.build,'last_'+attr))
    build.last_edges=list(build.last_edges)
    for key,interval in (limits or {}).items():
        if not key.startswith('order:'):continue
        parts=key.split(':');m.need(len(parts)==4,'Ordinary order branch key')
        _,first,second,side=parts
        m.need(side in 'st' and first in ('alpha','beta') and second in m.CHAIN,'Ordinary order branch names')
        a,b=first+side,second+side
        m.need(st.get(a)==st.get(b)==1,'Order branch resources must be retained')
        lo,hi=interval;m.need((lo,hi) in ((0,0),(1,1)),'Ordinary order branch interval')
        difference=m.add((1,build.last_Z[a]),(-1,build.last_Z[b]))
        if lo==0:
            rows.append((difference,0,'ordinary order '+key))
            gap={k:-v for k,v in difference.items()};build.last_edges.append((a,b,gap))
        else:
            rows.append(({k:-v for k,v in difference.items()},-1,'ordinary order '+key))
            build.last_edges.append((b,a,difference))
    if SOURCE_TAIL_RANKS:
        for side in 'st':
            for off,constant in [('c',-2),('b',0),('a',2)]:
                rows.append(({'phisource'+side:1,'x'+side:-1,off+side:-1},constant,'exact source phi tail '+side+off))
            for weight in range(1,11):
                chi='chi'+str(weight)+side
                for removed,off in [(1,'c'),(2,'b'),(3,'a')]:
                    rows.append(({chi:1,'x'+side:-1,off+side:-1},weight*removed-(4-removed),
                                 'exact source block tail '+chi+off))
                rows.append(({chi:1,'x'+side:-1},4*weight,'source block core maximum '+chi))
                rows.append(({chi:1,'phicore'+side:-weight},4*weight,'source block core truncation '+chi))
    build.last_compression={}
    for key,interval in (limits or {}).items():
        if not key.startswith('compression:'):continue
        pieces=key.split(':');m.need(len(pieces)==5,'Compression branch syntax')
        _,source,a,b,kk=pieces
        m.need(source in ('core','source','trim1','trim2','trim3') and kk.isdigit(),'Compression branch source')
        k=int(kk);n={'core':65,'source':73,'trim1':71,'trim2':69,'trim3':67}[source]
        m.need(0<=k<n and tuple(interval) in ((0,0),(1,1)),'Compression branch interval')
        matches=[(i,gap) for i,(v,w,gap) in enumerate(build.last_edges) if (v,w)==(a,b)]
        m.need(len(matches)==1,'Compression branch actual edge')
        i,gap=matches[0];mass={'ts':1,'tt':1} if source=='core' else {('TD' if source=='source' else 'TD'+source[-1]):1}
        body=m.add((1,mass),(-k-1,gap))
        if interval[0]==1:
            rows.append((body,-1,'compression branch long '+key))
            build.last_compression[i]=max(build.last_compression.get(i,0),n-k)
        else:rows.append(({v:-c for v,c in body.items()},0,'compression branch short '+key))
    for key,interval in (limits or {}).items():
        if not key.startswith('diameter:'):continue
        import exact
        pieces=key.split(':');m.need(len(pieces)==4 and tuple(interval) in ((0,0),(1,1)),'Diameter branch syntax')
        _,source,a,b=pieces;n,span=exact.diameter_source(source)
        matches=[(i,gap) for i,(v,w,gap) in enumerate(build.last_edges) if (v,w)==(a,b)]
        m.need(len(matches)==1,'Diameter branch edge');i,gap=matches[0];body=m.add((1,span),(-2,gap))
        if interval[0]==1:
            rows.append((body,-1,'diameter branch yes '+key));build.last_compression[i]=max(build.last_compression.get(i,0),n)
        else:rows.append(({v:-c for v,c in body.items()},0,'diameter branch no '+key))
    for key,interval in (limits or {}).items():
        if not key.startswith('hit:'):continue
        import exact
        pieces=key.split(':');m.need(POINT_OVERLAP and len(pieces)==5 and tuple(interval) in ((0,0),(1,1)),'Point-hit branch syntax')
        _,tag,a,b,index=pieces;m.need(index in ('0','1'),'Point-hit guard index')
        matches=[gap for v,w,gap in build.last_edges if (v,w)==(a,b)]
        m.need(len(matches)==1,'Point-hit branch actual edge');body=exact.point_overlap_guards(matches[0],tag)[int(index)]
        if interval[0]==0:rows.append((body,0,'point-hit branch inside '+key))
        else:rows.append(({k:-v for k,v in body.items()},-1,'point-hit branch outside '+key))
    for key,interval in (limits or {}).items():
        if not key.startswith('trim_pair:'):continue
        import exact
        parts=key.split(':');m.need(POINT_OVERLAP and len(parts)==4 and tuple(interval) in ((0,0),(1,1)),'Trim pair branch syntax')
        _,side,a,b=parts;body=exact.trim_pair_guard(side,(a,b))
        if interval[0]==0:rows.append((body,0,'trim pair branch inside '+key))
        else:rows.append(({k:-v for k,v in body.items()},-1,'trim pair branch outside '+key))
    for key,interval in (limits or {}).items():
        if not key.startswith('extended_hit:'):continue
        import exact
        parts=key.split(':');m.need(POINT_OVERLAP and len(parts)==6 and tuple(interval) in ((0,0),(1,1)),'Extended hit branch syntax')
        _,q,tag,a,b,index=parts;m.need(q in ('1','2','3','4') and index in ('0','1'),'Extended hit indices')
        matches=[gap for v,w,gap in build.last_edges if (v,w)==(a,b)]
        m.need(len(matches)==1,'Extended hit actual edge');body=exact.extended_guards(matches[0],int(q),tag)[int(index)]
        if interval[0]==0:rows.append((body,0,'extended hit branch inside '+key))
        else:rows.append(({k:-v for k,v in body.items()},-1,'extended hit branch outside '+key))
    if POINT_OVERLAP:eqs.append(({'ONE':1},1,'unit constant'))
    if TRIM_SOURCE:
        for q in (1,2,3):
            body={'TD'+str(q):1,'TD':-1,'Ms':1,'Mt':1}
            if q>=2:body=m.add((1,body),(q-1,{'Rs':1,'Rt':1}),(1,{'cs':1,'ct':1}))
            if q>=3:body=m.add((1,body),(1,{'bs':1,'bt':1}))
            eqs.append((body,q*(73-q),'trimmed source mass '+str(q)))
    for side in 'st':
        key='terminal:'+side
        if key not in (limits or {}):continue
        import exact
        lo,hi=limits[key]
        m.need(j>=3 and st['O'+side]!=1 and 3 not in st.values() and type(lo) is int and lo==hi and 0<=lo<=16,'Required endpoint branch scope')
        S={'S'+side:1};B=exact.tail_endpoint(side,build.last_Z)
        if lo==0:
            rows.append((m.add((1,S),(-1,B)),0,'required endpoint below tail '+side))
        else:
            label=sorted(exact.tail_labels(side))[lo-1]
            rows.append((m.add((-1,S),(1,B)),-1,'required endpoint above tail '+side))
            eqs.append((m.add((1,S),(-1,m.fixed_forms()[label])),0,'required endpoint representation '+label))
    names=sorted({k for row,_,_ in rows+eqs for k in row})
    return names,rows,eqs


def specialize(rows,k,w):
    answer=[]
    params={'rank_k':k,'rank_I':k*k,'hole_W':w//2}
    for row,b,label in rows:
        answer.append(({x:c for x,c in row.items() if x not in params and c},b-sum(row.get(x,0)*v for x,v in params.items()),label))
    return answer


def check_interpolation(st,j,positive=False,e=0,limits=None):
    _,rows,eqs=build(st,j,positive,e,limits)
    rows=[x for x in rows if not x[2].startswith('parameter ')]
    eqs=[x for x in eqs if not x[2].startswith('parameter ')]
    for r in range(15,33):
        for w in (range(2,15,2) if positive else (0,)):
            _,expected_rows,expected_eqs=m.build(st,j,r,None,e,limits,w=w)
            for actual,expected in ((specialize(rows,32-r,w),expected_rows),(specialize(eqs,32-r,w),expected_eqs)):
                expected=[({k:2*c for k,c in row.items() if c},2*b,label) for row,b,label in expected]
                m.need(actual==expected,'Parameter interpolation changed a necessary row')
    return True
