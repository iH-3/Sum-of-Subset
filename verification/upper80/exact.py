# RESEARCH PROTOTYPE: no global bound is certified by this file.
"""Standard-library integer certificates and rooted-forest reconstruction."""
from collections import Counter
from math import gcd
import json
import model as m
PREMISE_CACHE={}


def check(cert,rows,eqs,target=None,strict=True):
    lhs=Counter();rhs=0;seen=set()
    for kind,i,weight in cert['weights']:
        m.need(kind in ('r','e') and type(i) is int and i>=0,'Certificate row type')
        m.need((kind,i) not in seen,'Repeated certificate row');seen.add((kind,i))
        source=rows if kind=='r' else eqs
        m.need(i<len(source),'Missing certificate row')
        m.need(type(weight) is int and weight!=0 and (kind=='e' or weight>0),'Certificate sign')
        row,b,_=source[i]
        for k,v in row.items():lhs[k]+=weight*v
        rhs+=weight*b
    if target is not None:
        den=cert['denominator'];m.need(type(den) is int and den>0,'Target scale')
        for k,c in target.items():lhs[k]-=den*c
    else:m.need(cert['denominator'] is None,'Unexpected target scale')
    valid=all(x>=0 for x in lhs.values()) and (rhs<0 if target is None or strict else rhs<=0)
    m.need(valid,'Invalid exact integer consequence')
    return -rhs


def forest(edges,ret,chosen,roots,e,constants=None,point_edges=None):
    point_edges={} if point_edges is None else {int(i):n for i,n in point_edges.items()}
    m.need(set(point_edges)<=set(chosen) and all(type(v) is int and 0<=v<=10 for v in point_edges.values()),'Point overlap forest syntax')
    constants={} if constants is None else {int(i):n for i,n in constants.items()}
    m.need(set(constants)<=set(chosen) and all(type(v) is int for v in constants.values()),'Forest constants')
    m.need(len(set(chosen))==len(chosen) and all(type(i) is int and 0<=i<len(edges) for i in chosen),'Forest edge index')
    vertices=['Ls','Lt',*ret];parent={v:v for v in vertices}
    def find(v):
        while parent[v]!=v:v=parent[v]
        return v
    for i in chosen:
        a,b,_=edges[i];aa,bb=find(a),find(b)
        m.need(aa!=bb,'Cyclic forest');parent[aa]=bb
    comps={}
    for v in vertices:comps.setdefault(find(v),[]).append(v)
    m.need(len(set(roots))==len(roots) and set(roots)<=set(ret),'Forest root index')
    for cc in comps.values():
        lead=sum(v.startswith('L') for v in cc)
        m.need(lead<=1 and sum(v in roots for v in cc)==(0 if lead else 1),'Forest roots per component')
    m.need(not set(constants)&set(point_edges),'Duplicate edge overlap source')
    body=m.add((len(chosen)-len(constants)-len(point_edges),m.var('FD')),*[(-1,edges[i][2]) for i in chosen if i not in point_edges],
               (1,{'ells':1,'ellt':1}),(1,{'D'+v:1 for v in roots}),(-1,m.var('delta')))
    return body,-e-sum(constants.values())-sum(point_edges.values()),'additional forest'


def credit(low,high,initial=0):
    return max(initial,len(low)+len(high)-sum(bool(set(group)&low) for group in m.GROUPS))


def credit_rows(ret,e):
    return [(m.add((1,{'ells':1,'ellt':1}),(1,{'D'+v:1 for v in ret}),(-1,m.var('delta'))),-e,'proved fixed credit'),
            ({'LS':1,'LT':1,'delta':-1},-e,'proved block fixed credit')]

TAIL_SUFFIXES=('C11','C12','C13','C14','C15','C16','C17','C18','C22','C23','C24','C33','C34','C44','U2','V2')

def tail_labels(side):
    sign='+' if side=='s' else '-'
    return {name[0]+sign+name[1:] for name in TAIL_SUFFIXES}

def tail_endpoint(side,Z):return m.add((1,Z['H'+side]),(1,m.var('M'+side)))

def tail_row(side,Z,removed):
    return m.add((1,m.var('S'+side)),(-1,tail_endpoint(side,Z)),(-1,m.var('hole_W'))),16-removed,'proved tail capacity '+side

def quartet_rows(side,lower):
    rows=[]
    for threshold,terms,rhs in [(5,{'c':-2},4),(6,{'b':-1,'c':-1},5),
                               (8,{'b':-2},7),(8,{'a':-1,'c':-1},7),
                               (9,{'a':-1,'b':-1},8),(10,{'a':-2},9)]:
        if lower>=threshold:
            row={'e'+side:1,'B'+side:1};row.update({k+side:v for k,v in terms.items()})
            rows.append((row,rhs,'quartet fringe count '+side+':'+str(threshold)+':'+str(len(rows))))
    return rows

def tail_removed(side, absent, pairs):
    """Exact maximum independent set of the at most sixteen remaining slots."""
    from functools import lru_cache
    labels=sorted(tail_labels(side)-absent);index={v:i for i,v in enumerate(labels)}
    neighbors=[0]*len(labels)
    for a,b in pairs:
        if a in index and b in index:
            i,j=index[a],index[b];neighbors[i]|=1<<j;neighbors[j]|=1<<i
    @lru_cache(None)
    def alpha(mask):
        if not mask:return 0
        isolated=sum(1<<i for i,n in enumerate(neighbors) if mask>>i&1 and not n&mask)
        if isolated:return isolated.bit_count()+alpha(mask^isolated)
        i=max((i for i in range(len(labels)) if mask>>i&1),key=lambda i:(neighbors[i]&mask).bit_count())
        rest=mask^(1<<i)
        return max(alpha(rest),1+alpha(rest&~neighbors[i]))
    return 16-alpha((1<<len(labels))-1)


POINT_TAGS=tuple(side+off for side in 'st' for off in ('R','a','b','c','e'))

def point_overlap_guards(gap,tag):
    m.need(tag in POINT_TAGS,'Point overlap tag')
    side,off=tag
    point={'R'+side:1}
    if off!='R':point=m.add((1,point),(1,{off+side:1}))
    h=m.add((1,point),(-1,gap)) if side=='s' else m.add((1,gap),(-1,point))
    # A one-max-removed core contains every integer from
    # -(31+k-tt+xt) to 31-k-ts+xs. Known extrema lie outside it.
    return [m.add((-1,h),(1,{'tt':1,'xt':-1,'rank_k':-1,'ONE':-31})),
            m.add((1,h),(1,{'ts':1,'xs':-1,'rank_k':1,'ONE':-31}))]

def point_group_guards(gap,tags,core_side,q):
    m.need(core_side in 'st' and type(q) is int and 1<=q<=len(tags) and len(set(tags))==len(tags) and all(tag in POINT_TAGS for tag in tags),'Point group syntax')
    peel_side=tags[0][0];m.need(all(tag[0]==peel_side for tag in tags),'Point group one known side')
    ordered=sorted(tags,key=POINT_TAGS.index)
    if peel_side!=core_side:ordered.reverse()
    values=[]
    for tag in ordered:
        side,off=tag;point={'R'+side:1}
        if off!='R':point=m.add((1,point),(1,{off+side:1}))
        h=m.add((1,point),(-1,gap)) if side=='s' else m.add((1,gap),(-1,point))
        values.append(h if core_side=='s' else {k:-v for k,v in h.items()})
    lower=m.add((1,{'ONE':1}),(-1,values[0]))
    upper=m.add((1,values[-1]),(1,{'ONE':-31,'rank_k':1 if core_side=='s' else -1}))
    mass=m.add((1,{'t'+core_side:1,'x'+core_side:-1,'ONE':-31*q-q*(q+1)//2,'rank_k':q if core_side=='s' else -q}),*[(1,value) for value in values[-q:]])
    return lower,upper,mass

from functools import lru_cache
@lru_cache(None)
def _point_pack(hits,groups):
    choices=[(1<<POINT_TAGS.index(tag),1) for tag in hits]
    choices += [(sum(1<<POINT_TAGS.index(tag) for tag in tags),count) for tags,count in groups]
    dp={0:0}
    for mask,count in choices:
        for used,value in list(dp.items()):
            if used&mask:continue
            key=used|mask;dp[key]=max(dp.get(key,0),value+count)
    return max(dp.values())

def point_overlap_count(hits,groups,extended=None):
    return max(_point_pack(tuple(sorted(hits)),tuple(sorted((tuple(tags),count) for tags,count in groups.items()))),max((len(tags) for tags in (extended or {}).values()),default=0))

def extended_tags(q):
    m.need(type(q) is int and 1<=q<=4,'Extended core trim count')
    return tuple(side+off for side in 'st' for off in 'abce'[4-q:])

def extended_guards(gap,q,tag):
    m.need(tag in extended_tags(q),'Extended core exterior tag')
    m0=4-q
    side,off=tag;point={'R'+side:1,off+side:1}
    h=m.add((1,point),(-1,gap)) if side=='s' else m.add((1,gap),(-1,point))
    guards=[]
    for core_side,scale in [('t',-1),('s',1)]:
        # Prefix length r+m0 - (tau+m0*xi+sum(offsets)-T_m0).
        body={'ONE':-32-m0-m0*(m0+1)//2,'rank_k':1 if core_side=='s' else -1,'t'+core_side:1,'x'+core_side:m0}
        for off0 in 'abc'[:m0]:body=m.add((1,body),(1,{off0+core_side:1}))
        guards.append(m.add((scale,h),(1,body)))
    return guards

TRIM_PAIRS=tuple((a,b) for i,a in enumerate('Rabce') for b in 'Rabce'[i:])

def trim_pair_guard(side,pair):
    m.need(side in 'st' and tuple(pair) in TRIM_PAIRS,'Trim-hull pair')
    row={'ONE':1,'x'+side:2,'t'+side:-1,'e'+side:-1}
    for off in pair:
        if off!='R':row=m.add((1,row),(1,{off+side:1}))
    return row

def trim_hull_row(count):
    m.need(type(count) is int and 0<=count<=30,'Trim-hull pair count')
    return ({'K':1,'Ms':-1,'Mt':-1,'ts':-1,'tt':-1,'xs':1,'xt':1},93-count,'trimmed core hull')

def diameter_source(source):
    if source=='core':return 65,{'Rs':1,'Rt':1}
    if source=='source':return 73,{'Ms':1,'Mt':1}
    m.need(source in ('trim1','trim2','trim3'),'Diameter source')
    q=int(source[-1]);off={1:'c',2:'b',3:'a'}[q]
    return 73-2*q,{'Rs':1,'Rt':1,off+'s':1,off+'t':1}

def source_maximum_overlap_rows():
    # Q=D minus the two extreme points. |2Q| <= 2R+C+13.
    # Each added maximum supplies |Q|=71 translates and the three pairs.
    # Its intersection with an old extremal translate contains a shifted E
    # intersection, and also a shifted D intersection minus at most four.
    # Both are subsets of 2Q, so these two rebates may be added.
    from itertools import product
    rows=[]
    for choices in product(('none','core','source'),repeat=2):
        if choices==('none','none'):continue
        row={'K':1,'Rs':-2,'Rt':-2,'cs':-1,'ct':-1};rhs=158
        for side,choice in zip('st',choices):
            if choice=='none':continue
            row=m.add((1,row),(-1,{'e'+side:1}),(1,{'c'+side:1}),(1,{'F' if choice=='core' else 'FD':1}))
            if choice=='source':rhs+=4
        rows.append((row,rhs,'source maximum overlap '+':'.join(choices)))
    return rows

def source_gap_inventory_rows():
    # In (2*R_v+c_v, M_v-R_o), ordinary E translates contribute nothing.
    # Only six pairs of the three smaller positive tails and four pairs of
    # M_v with opposite source tails may occur. The reflected gaps are disjoint.
    rows=[]
    for side,other in [('s','t'),('t','s')]:
        rows.append(({'K':1,'Rs':-3,'Rt':-3,'e'+other:-1,'c'+side:-1,'Bs':-1,'Bt':-1},12,'source internal tail gap '+side))
    rows.append(({'K':1,'Rs':-4,'Rt':-4,'cs':-1,'ct':-1,'Bs':-1,'Bt':-1},23,'source both internal tail gaps'))
    return rows

def alpha_pattern(st,j,positive):
    return j==5 and not positive and all(st[k+side]==(2 if k=='O' else 0)
        for k in ('P','beta','O') for side in 'st') and sorted(st['alpha'+side] for side in 'st')==[0,1]

def alpha_tail_rows(st,j,positive,e,Z):
    m.need(alpha_pattern(st,j,positive) and e>=22,'Conditional alpha tail scope')
    # Every paired gap x has 2*x >= tau+2*F-(tau+delta)+e >= e-3.
    m.need(1+3*((e-3+1)//2)>26,'Conditional alpha tail strict order')
    side=next(side for side in 'st' if st['alpha'+side]==0)
    return [(m.add((1,{'S'+side:1}),(-1,{'d'+side:1})),1,'conditional alpha one-point tail'),
            (m.add((1,{'S'+side:1}),(-1,Z['H'+side]),(-1,{'M'+side:1})),2,'conditional alpha two-point tail')]

def ownerless_rows(st,j,positive,e,Z,limits):
    m.need(j==4 and m.is_ownerless(st),'Conditional ownerless scope')
    T=lambda n:n*(n+1)//2
    for w in (range(2,15,2) if positive else [0]):
        mass=min(max(58+2*w,T(p//2)+T((p+1)//2))-4*p for p in range(66)) if w else -12
        m.need(min(1+mass+e-3*w//2,47+e-3*w//2,8+e-3*w//2,9+e-3*w//2)>0,'Conditional ownerless strict guards')
    rows=[]
    for side,other in [('s','t'),('t','s')]:
        rows.append((m.add((1,{'h'+side:1}),(-1,{'Ms':1,'Mt':1}),(-1,{'hole_W':1})),11,'conditional full ownerless '+side))
        rows.append((m.add((1,{'h'+side:1}),(-1,{'R'+side:1,'M'+other:1}),(-1,{'hole_W':1})),30,'conditional truncated ownerless '+side))
        if (limits or {}).get('uH'+side,(0,72))[1]<=68:
            rows.append((m.add((1,{'h'+side:1}),(-1,{'Rs':1,'Rt':1}),(-1,{'hole_W':1})),31,'conditional core-hit ownerless '+side))
    return rows

def alpha_compression(st,j,positive,e,edges):
    m.need(alpha_pattern(st,j,positive),'Alpha half-mass pattern')
    m.need(360-4*131+4*e>0,'Size81 alpha strict compression guard')
    names={k+s for s in 'st' for k in ('X','g','h')};indices=[];counts=Counter()
    for i,(_,_,gap) in enumerate(edges):
        clean={k:v for k,v in gap.items() if v}
        if len(clean)==1:
            name,c=next(iter(clean.items()))
            if name in names and c==1:indices.append(i);counts[name]+=1
    m.need(set(counts)==names and set(counts.values())=={2},'All twelve paired alpha edges')
    return indices


def inherited(record):
    if 'premise' not in record:return None
    parent=record['premise']
    m.need(all(parent[k]==record[k] for k in ('st','j','positive')),'Inherited root changed')
    child_limits=record.get('limits') or {}
    for name,interval in (parent.get('limits') or {}).items():
        m.need(name in child_limits,'Inherited domain was widened')
        lo,hi=child_limits[name]
        m.need(interval[0]<=lo<=hi<=interval[1],'Inherited branch domain was widened')
    return replay(parent,require_closed=False,return_state=True)


def replay(record,require_closed=True,return_state=False):
    import parametric as p
    cache_key=None
    if not require_closed and return_state:
        import hashlib
        cache_key=hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        if cache_key in PREMISE_CACHE:return PREMISE_CACHE[cache_key]
    prior=inherited(record)
    p.USE_PLANES='planes' in record;p.PLANE_GENERATOR=None;p.PLANE_TABLE=record.get('planes',{})
    p.SOURCE_TAIL_RANKS=record.get('source_tail_ranks',False)
    p.SHARP_PLANES=record.get('sharp_planes',False)
    p.SIDE_PLANES=record.get('side_planes',False)
    p.TRIM_SOURCE=record.get('trim_source',False)
    p.POINT_OVERLAP=record.get('point_overlap',False)
    st=record['st'];j=record['j'];positive=record['positive'];initial=8 if m.is_ownerless(st) else 0
    e=prior['credit'] if prior else initial
    _,rows,eqs=p.build(st,j,positive,e,record.get('limits'))
    if 'missing_leading' in record:
        side=record['missing_leading']
        m.need(side in 'st' and j==2 and all(st[k+side]==0 for k in ('P','C5','C6','C7')),'Missing-leading interface')
        rows=[r for r in rows if r[2]!='leading interval '+side]
        rows.append(({'d'+side:1,'X'+side:-2,'g'+side:-1},0,'missing leading hull below'))
        eqs.append(({'ell'+side:1,'K':-1},0,'missing leading full loss'))
    edges=p.build.last_edges;ret=p.build.last_retained;forms=m.fixed_forms()
    low=set();high=set();closed=False;constants=dict(p.build.last_compression);tail_low={'s':set(),'t':set()};tail_counts={'s':0,'t':0};tail_pairs={'s':set(),'t':set()};facts=[];point_hits={};point_groups={};extended_hits={};trim_pairs=set()
    if prior:
        low=set(prior['low']);high=set(prior['high']);facts=list(prior['facts']);rows.extend(facts)
        tail_low={s:set(prior['tail_low'][s]) for s in 'st'};tail_counts=dict(prior['tail_counts']);tail_pairs={s:set(prior['tail_pairs'][s]) for s in 'st'}
        for a,b,gap,value in prior['constants']:
            matches=[i for i,(aa,bb,gg) in enumerate(edges) if (a,b,gap)==(aa,bb,gg)]
            m.need(len(matches)==1,'Inherited compression edge changed')
            i=matches[0];constants[i]=max(constants.get(i,0),value)
    if prior:
        for a,b,gap,tags in prior.get('point_hits',[]):
            matches=[i for i,(aa,bb,gg) in enumerate(edges) if (a,b,gap)==(aa,bb,gg)]
            m.need(len(matches)==1,'Inherited point-overlap edge')
            point_hits[matches[0]]=set(tags)
    if prior:
        for a,b,gap,groups in prior.get('point_groups',[]):
            matches=[i for i,(aa,bb,gg) in enumerate(edges) if (a,b,gap)==(aa,bb,gg)]
            m.need(len(matches)==1,'Inherited point-group edge');point_groups[matches[0]]={tuple(tags):count for tags,count in groups}
    if prior:
        trim_pairs=set(tuple(x) for x in prior.get('trim_pairs',[]))
        for a,b,gap,groups in prior.get('extended_hits',[]):
            matches=[i for i,(aa,bb,gg) in enumerate(edges) if (a,b,gap)==(aa,bb,gg)]
            m.need(len(matches)==1,'Inherited extended overlap edge');extended_hits[matches[0]]={int(q):set(tags) for q,tags in groups}

    for index,step in enumerate(record['trace']):
        kind=step['kind']
        m.need(not closed,'Steps after contradiction')
        if kind=='forest':
            m.need(step['e']==e,'Unproved forest credit')
            cc={int(i):v for i,v in step.get('constants',{}).items()}
            m.need(all(constants.get(i,0)>=v for i,v in cc.items()),'Unproved compression constant')
            pc={int(i):v for i,v in step.get('point_edges',{}).items()}
            m.need(all(point_overlap_count(point_hits.get(i,set()),point_groups.get(i,{}),extended_hits.get(i,{}))>=v for i,v in pc.items()),'Unproved point overlap')
            rows.append(forest(edges,ret,step['edges'],step['roots'],e,cc,pc))
        elif kind=='extended_overlap_hit':
            i,q,tag=step['edge'],step['q'],step['tag'];m.need(record.get('point_overlap') and type(i) is int and 0<=i<len(edges),'Extended overlap edge')
            guards=extended_guards(edges[i][2],q,tag);m.need(len(step['certificates'])==2,'Two extended interval guards')
            m.need(tag not in extended_hits.get(i,{}).get(q,set()),'Repeated extended overlap hit')
            for guard,cert in zip(guards,step['certificates']):
                check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved extended interval hit');rows.append(fact);facts.append(fact)
            extended_hits.setdefault(i,{}).setdefault(q,set()).add(tag)
        elif kind=='source_trim_hull':
            m.need(record.get('point_overlap'),'Trim hull constant variable')
            rows.append(trim_hull_row(len(trim_pairs)))
        elif kind=='trim_hull_pair':
            side,pair=step['side'],tuple(step['pair']);key=(side,*pair)
            m.need(key not in trim_pairs,'Repeated trim pair')
            guard=trim_pair_guard(side,pair);check(step['certificate'],rows,eqs,guard,strict=False)
            fact=(guard,0,'proved trimmed hull pair');rows.append(fact);facts.append(fact);trim_pairs.add(key)
            fact=trim_hull_row(len(trim_pairs));rows.append(fact);facts.append(fact)
        elif kind=='point_overlap_group':
            i,tags,side,q=step['edge'],step['tags'],step['core_side'],step['q']
            m.need(record.get('point_overlap') and type(i) is int and 0<=i<len(edges),'Point group edge')
            guards=point_group_guards(edges[i][2],tags,side,q);m.need(len(step['certificates'])==3,'Three group guards')
            for index0,(guard,cert) in enumerate(zip(guards,step['certificates'])):
                check(cert,rows,eqs,guard,strict=index0==2);fact=(guard,-1 if index0==2 else 0,'proved point group');rows.append(fact);facts.append(fact)
            key=tuple(sorted(tags));count=len(tags)-q+1;point_groups.setdefault(i,{})[key]=max(point_groups.get(i,{}).get(key,0),count)
        elif kind=='point_overlap_hit':
            i,tag=step['edge'],step['tag'];m.need(record.get('point_overlap') and type(i) is int and 0<=i<len(edges) and tag not in point_hits.get(i,set()),'Point overlap fact scope')
            guards=point_overlap_guards(edges[i][2],tag);m.need(len(step['certificates'])==2,'Two point interval guards')
            for guard,certificate in zip(guards,step['certificates']):
                check(certificate,rows,eqs,guard,strict=False);fact=(guard,0,'proved point overlap interval');rows.append(fact);facts.append(fact)
            point_hits.setdefault(i,set()).add(tag)
        elif kind=='diameter':
            i,source=step['edge'],step['source'];m.need(type(i) is int and 0<=i<len(edges),'Diameter edge')
            n,span=diameter_source(source);target=m.add((1,span),(-2,edges[i][2]))
            check(step['certificate'],rows,eqs,target)
            constants[i]=max(constants.get(i,0),n)
            fact=(target,-1,'proved diameter compression');rows.append(fact);facts.append(fact)
        elif kind=='compression':
            i,k,source=step['edge'],step['k'],step['source']
            m.need(type(i) is int and 0<=i<len(edges) and type(k) is int and 0<=k<73 and source in ('core','source','trim1','trim2','trim3'),'Compression indices')
            mass={'ts':1,'tt':1} if source=='core' else {('TD' if source=='source' else 'TD'+source[-1]):1}
            target=m.add((1,mass),(-k-1,edges[i][2]))
            check(step['certificate'],rows,eqs,target)
            constants[i]=max(constants.get(i,0),{'core':65,'source':73,'trim1':71,'trim2':69,'trim3':67}[source]-k)
            fact=(target,-1,'proved compression');rows.append(fact);facts.append(fact)
        elif kind=='source_gap_inventory':
            new=source_gap_inventory_rows();rows.extend(new);facts.extend(new)
        elif kind=='source_maximum_overlap':
            new=source_maximum_overlap_rows();rows.extend(new);facts.extend(new)
        elif kind in ('conditional_alpha_tail','conditional_ownerless'):
            if kind=='conditional_alpha_tail':new=alpha_tail_rows(st,j,positive,e,p.build.last_Z)
            else:new=ownerless_rows(st,j,positive,e,p.build.last_Z,record.get('limits'))
            rows.extend(new);facts.extend(new)
        elif kind=='alpha_half_mass':
            for i in alpha_compression(st,j,positive,e,edges):constants[i]=max(constants.get(i,0),64)
        elif kind=='quartet_fringe':
            side=step['side'];m.need(side in ('s','t'),'Quartet side')
            lower=(record.get('limits') or {}).get('B'+side,(4,10))[0]
            m.need(step['lower']==lower and lower>=5,'Quartet fringe branch premise')
            new=quartet_rows(side,lower);rows.extend(new);facts.extend(new)
        elif kind in ('tail_low','tail_credit','tail_incompatible'):
            side=step['side'];m.need(side in 'st' and j>=3 and st['O'+side]!=1,'Tail interface applicability')
            if kind=='tail_incompatible':
                a,b=step['larger'],step['smaller'];pair=tuple(sorted((a,b)))
                m.need(a!=b and {a,b}<=tail_labels(side) and pair not in tail_pairs[side],'Tail pair labels')
                target=m.add((1,m.var('S'+side)),(-1,tail_endpoint(side,p.build.last_Z)),(-1,forms[a]),(1,forms[b]))
                check(step['certificate'],rows,eqs,target,strict=False)
                tail_pairs[side].add(pair);fact=(target,0,'proved tail incompatible '+a+':'+b);rows.append(fact);facts.append(fact)
            elif kind=='tail_low':
                label=step['label'];m.need(label in tail_labels(side) and label not in tail_low[side],'Tail label')
                target=m.add((1,forms[label]),(-1,tail_endpoint(side,p.build.last_Z)))
                check(step['certificate'],rows,eqs,target,strict=False)
                tail_low[side].add(label);fact=(target,0,'proved tail LOW '+label);rows.append(fact);facts.append(fact)
            else:
                removed=tail_removed(side,low|high|tail_low[side],tail_pairs[side])
                m.need(step['removed']==removed and removed>tail_counts[side],'Unproved tail capacity')
                tail_counts[side]=removed;fact=tail_row(side,p.build.last_Z,removed);rows.append(fact);facts.append(fact)
        elif kind in ('low','high'):
            label=step['label'];m.need(label in forms and label not in low|high,'Fixed label counted twice')
            form=forms[label]
            if kind=='low':
                check(step['certificate'],rows,eqs,form,strict=False);low.add(label)
                fact=(form,0,'proved LOW '+label);rows.append(fact);facts.append(fact)
            else:
                body=m.add((1,form),(-1,m.var('Ss' if '+' in label else 'St')))
                target={k:-c for k,c in body.items()}
                check(step['certificate'],rows,eqs,target);high.add(label)
                fact=(target,0 if 3 in st.values() else -1,'proved HIGH '+label);rows.append(fact);facts.append(fact)
        elif kind=='credit':
            next_e=credit(low,high,initial)
            m.need(step['e']==next_e and next_e>e,'Unjustified fixed credit')
            e=next_e;rows.extend(credit_rows(ret,e))
        elif kind=='endpoint_credit':
            m.need('planes' in record and step['e']==e,'Unproved endpoint credit')
            _,updated,_=p.build(st,j,positive,e,record.get('limits'))
            rows.extend(row for row in updated if row[2].startswith('uniform endpoint ') or row[2] in ('parameter rank range','parameter rank chord'))
        else:
            m.need(kind=='final','Unknown proof step')
            check(step['certificate'],rows,eqs);closed=True
    m.need(closed if require_closed else not closed,'No terminal contradiction' if require_closed else 'Closed inherited premise')
    if return_state:
        state=dict(credit=e,low=low,high=high,facts=facts,tail_low=tail_low,tail_counts=tail_counts,tail_pairs=tail_pairs,
                   constants=[(*edges[i],value) for i,value in constants.items()],
                   point_hits=[(*edges[i],sorted(tags)) for i,tags in point_hits.items()],
                   point_groups=[(*edges[i],[(tags,count) for tags,count in groups.items()]) for i,groups in point_groups.items()],trim_pairs=sorted(trim_pairs),extended_hits=[(*edges[i],[(q,sorted(tags)) for q,tags in groups.items()]) for i,groups in extended_hits.items()])
        if cache_key is not None:PREMISE_CACHE[cache_key]=state
        return state
    return dict(steps=len(record['trace']),credit=e)
