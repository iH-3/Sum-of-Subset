# RESEARCH PROTOTYPE: no global bound is certified by this file.
"""Standard-library integer certificates and rooted-forest reconstruction."""
from collections import Counter,OrderedDict
from math import gcd
import json
import model as m
PREMISE_CACHE=OrderedDict()


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


def fixed_pair_guards(first,second,kind):
    forms=m.fixed_forms();m.need(first in forms and second in forms and first!=second,'Fixed pair labels')
    a,b=forms[first],forms[second];sa='s' if '+' in first else 't';sb='s' if '+' in second else 't'
    if kind=='low':return [m.add((1,a),(1,b),(-1,{'ONE':1}))]
    if kind=='high':return [m.add((1,{'S'+sa:1}),(1,{'S'+sb:1}),(1,{'ONE':1}),(-1,a),(-1,b))]
    m.need(sa==sb,'Fixed pair same physical target')
    if kind=='apart':return [m.add((1,{'S'+sa:1}),(-1,a),(1,b))]
    m.need(kind=='equal','Fixed pair proof kind')
    difference=m.add((1,a),(-1,b));return [difference,{k:-v for k,v in difference.items()}]

def fixed_probe_pair_guards(first,second,resource,core_side,Z):
    forms=m.fixed_forms();m.need(first in forms and second in forms and first!=second,'Fixed source probe pair')
    side='s' if '+' in first else 't';m.need(('+' in second)==(side=='s') and resource in Z and resource[-1]==side and core_side in 'st','Fixed probe physical resource')
    sign=1 if core_side==side else -1
    probes=[m.add((sign,forms[label]),(-sign,Z[resource])) for label in (first,second)]
    # The r-1 retained core points have excess tau-xi. Omitting both
    # distinct probes in [1,r-1] costs 2(r-1)+3-probe1-probe2.
    rank={'ONE':31,'rank_k':-1 if core_side=='s' else 1}
    return [m.add((1,{'ONE':1}),(-1,forms[label])) for label in (first,second)]+[
        m.add((1,{'ONE':1}),(-1,probes[0])),m.add((1,probes[1]),(-1,rank)),
        m.add((1,{'ONE':1}),(1,probes[0]),(-1,probes[1])),
        m.add((1,{'t'+core_side:1,'x'+core_side:-1,'ONE':-2}),(-2,rank),(1,probes[0]),(1,probes[1]))]

def credit(low,high,initial=0,covered=(),covered_positive=(),pairs=()):
    removed=set(low)|set(high)|set(covered);possible_low=set(low)|(set(covered)-set(covered_positive))
    if not pairs:return max(initial,len(removed)-sum(bool(set(group)&possible_low) for group in m.GROUPS))
    labels=sorted(set(m.fixed_forms())-removed);bits={label:1<<i for i,label in enumerate(labels)};constraints=[]
    for group in m.GROUPS:
        if set(group)&possible_low:continue
        mask=sum(bits.get(label,0) for label in group)
        if not mask:return max(initial,85)
        constraints.append(mask)
    for first,second in pairs:
        m.need(first in m.LABELS and second in m.LABELS and first!=second,'Fixed conflict labels')
        if first in bits and second in bits:constraints.append(bits[first]|bits[second])
    return max(initial,len(removed)+_minimum_hitting(tuple(sorted(set(constraints))))-26)

from functools import lru_cache
@lru_cache(maxsize=200000)
def _minimum_hitting(edges):
    if not edges:return 0
    # A smaller edge makes a containing edge redundant.
    reduced=[]
    for edge in sorted(edges,key=int.bit_count):
        if not any(previous&edge==previous for previous in reduced):reduced.append(edge)
    forced=0
    for edge in reduced:
        if edge.bit_count()==1:forced|=edge
    if forced:return forced.bit_count()+_minimum_hitting(tuple(sorted(edge for edge in reduced if not edge&forced)))
    # Disjoint incidence components have additive exact optima.
    remaining=list(reduced);components=[]
    while remaining:
        component=[remaining.pop()];union=component[0]
        while True:
            attached=[edge for edge in remaining if edge&union]
            if not attached:break
            component.extend(attached)
            for edge in attached:union|=edge
            attached_set=set(attached);remaining=[edge for edge in remaining if edge not in attached_set]
        components.append(tuple(sorted(component)))
    if len(components)>1:return sum(_minimum_hitting(component) for component in components)
    def lower_bound(items):
        used=count=0
        for edge in sorted(items,key=int.bit_count):
            if not edge&used:used|=edge;count+=1
        return count
    chosen=min(reduced,key=int.bit_count);vertices=[]
    while chosen:
        bit=chosen&-chosen;chosen-=bit;vertices.append(bit)
    vertices.sort(key=lambda bit:sum(bool(edge&bit) for edge in reduced),reverse=True)
    best=len(reduced);floor=lower_bound(reduced)
    for bit in vertices:
        residual=tuple(sorted(edge for edge in reduced if not edge&bit))
        if 1+lower_bound(residual)>=best:continue
        best=min(best,1+_minimum_hitting(residual))
        if best==floor:break
    return best


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

def leading_geometry(edge):
    a,b,gap=edge
    m.need(a in ('Ls','Lt') and b[-1]==a[-1] and b[:-1] in m.CHAIN,'Leading native edge')
    side=a[-1];other='t' if side=='s' else 's';right=b[:-1] in ('V','U','H','O')
    shift=m.add((1,{'M'+side:1}),(1,gap)) if right else m.add((-1,{'M'+other:1}),(-1,gap))
    return side,other,right,shift

def signed_source_point(tag,side):
    if tag=='zero':return {}
    m.need(tag in POINT_TAGS,'Known source point tag')
    row={'R'+tag[0]:1}
    if tag[1]!='R':row=m.add((1,row),(1,{tag[1]+tag[0]:1}))
    return row if tag[0]==side else {k:-v for k,v in row.items()}

def source_minus_prefix(side,q):
    m.need(side in 'st' and type(q) is int and 1<=q<=5,'Leading retained source')
    if q==5:return {'t'+side:1,'x'+side:-1,'rank_k':1 if side=='s' else -1,'ONE':-31}
    m0=4-q
    body={'ONE':-32-m0-m0*(m0+1)//2,'rank_k':1 if side=='s' else -1,'t'+side:1,'x'+side:m0}
    for off in 'abc'[:m0]:body=m.add((1,body),(1,{off+side:1}))
    return body

def leading_tags(q):return POINT_TAGS if q==5 else extended_tags(q)

LEADING_WITNESSES=('dense_core','double_core','zero',*POINT_TAGS,*('merge_'+tag for tag in POINT_TAGS))

def leading_point_guards(edge,tag,witness,q=5):
    side,other,right,shift=leading_geometry(edge)
    m.need(tag in leading_tags(q) and tag[0]==(other if right else side),'Leading exterior source point')
    m.need(witness in LEADING_WITNESSES,'Leading sumset witness')
    target=m.add((1,shift),(1,signed_source_point(tag,side)))
    return double_source_guards(side,target,witness,q)

def double_source_guards(side,target,witness,q):
    m.need(side in 'st' and witness in LEADING_WITNESSES,'Double source interval witness')
    m.need(type(q) is int and 1<=q<=5,'Double source truncation level')
    other='t' if side=='s' else 's'
    if witness=='dense_core':
        sign=-1 if side=='s' else 1
        return [{'xs':1,'xt':1,'rank_k':1,'ONE':-32},
                m.add((-1,target),(1,{'ONE':-64,'rank_k':2*sign})),
                m.add((1,target),(1,{'ONE':-64,'rank_k':-2*sign}))]
    ns,no=source_minus_prefix(side,q),source_minus_prefix(other,q)
    if witness.startswith('merge_'):
        endpoint=witness[6:];physical=endpoint[0];opposite='t' if physical=='s' else 's'
        nn,nopp=source_minus_prefix(physical,q),source_minus_prefix(opposite,q)
        # Nonempty integer core interval, followed by all consecutive joins.
        guards=[m.add((1,ns),(1,no))]
        guards.append(m.add((1,{'R'+physical:1,'ONE':-1}),(2,nn),(1,nopp)))
        last={}
        for off in 'abce':
            if endpoint[1]=='R':break
            current={off+physical:1}
            guards.append(m.add((1,current),(-1,last),(1,nn),(1,nopp),(1,{'ONE':-1})))
            last=current
            if off==endpoint[1]:break
        p=signed_source_point(endpoint,side)
        if physical==side:
            guards.extend([m.add((-1,target),(2,no)),m.add((1,target),(-1,p),(1,ns))])
        else:
            guards.extend([m.add((-1,target),(1,p),(1,no)),m.add((1,target),(2,ns))])
        return guards
    scale=2 if witness=='double_core' else 1
    if witness!='double_core':target=m.add((1,target),(-1,signed_source_point(witness,side)))
    return [m.add((-1,target),(scale,no)),m.add((1,target),(scale,ns))]

def fixed_cover_guards(label,resource,q,witness,Z):
    forms=m.fixed_forms();m.need(label in forms,'Known fixed form')
    side='s' if '+' in label else 't';other='t' if side=='s' else 's'
    m.need(resource[-1]==side,'Fixed cover physical side')
    if resource=='L'+side:
        center={'d'+side:1,'M'+side:-2,'X'+side:-2,'g'+side:-1}
        target=m.add((1,forms[label]),(-1,center))
        return double_source_guards(side,target,witness,q)
    m.need(resource in Z and witness is None,'Fixed ordinary cover resource')
    target=m.add((1,forms[label]),(-1,Z[resource]))
    return [m.add((-1,target),(1,source_minus_prefix(other,q))),
            m.add((1,target),(1,source_minus_prefix(side,q)))]

def edge_point_count(edge,hits,groups,extended,leading,leading_extended=None):
    old=point_overlap_count(hits,groups,extended)
    if not leading and not leading_extended:return old
    side,other,right,_=leading_geometry(edge);core_side=side if right else other
    core_hits={tag for tag in hits if tag[0]==core_side}
    core_groups={tags:count for tags,count in groups.items() if all(tag[0]==core_side for tag in tags)}
    result=max(old,len(leading)+point_overlap_count(core_hits,core_groups))
    for q,tags in (leading_extended or {}).items():
        core_count=sum(tag[0]==core_side for tag in extended.get(q,set()))
        result=max(result,len(tags)+core_count)
    return result

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

SUMSET_GAPS=tuple(side+str(i) for side in 'stST' for i in range(4))

def sumset_gap_data(key):
    m.need(key in SUMSET_GAPS,'Source internal gap key')
    side=key[0].lower();other='t' if side=='s' else 's';i=int(key[1]);offsets='Rabce'
    def pt(off):return {'R'+side:1} if off=='R' else {'R'+side:1,off+side:1}
    lower,upper=pt(offsets[i]),pt(offsets[i+1])
    qs={'ONE':31,'rank_k':-1 if side=='s' else 1,'t'+side:1,'x'+side:-1}
    qo={'ONE':31,'rank_k':-1 if other=='s' else 1,'t'+other:1,'x'+other:-1}
    if key[0].isupper():qs={'R'+side:1,'ONE':-1};qo={'R'+other:1,'ONE':-1}
    return side,other,lower,upper,qs,qo

def sumset_gap_pairs(key):
    side,other,*_=sumset_gap_data(key);tags=[side+x for x in 'Rabce'];opposite=[other+x for x in 'Rabce']
    return tuple([(a,b) for i,a in enumerate(tags) for b in tags[i:]]+[(a,b) for a in tags for b in opposite])

def sumset_gap_guards(key,pair):
    m.need(tuple(pair) in sumset_gap_pairs(key),'Source gap pair label')
    side,other,lower,upper,qs,qo=sumset_gap_data(key)
    value=m.add(*[(1,signed_source_point(tag,side)) for tag in pair])
    return [m.add((1,value),(-1,lower),(-1,qs)),m.add((1,upper),(-1,qo),(-1,value))]

def sumset_pair_difference(key,first,second):
    pairs=sumset_gap_pairs(key)
    m.need(tuple(first) in pairs and tuple(second) in pairs and tuple(first)!=tuple(second),'Distinct source pair labels')
    side=key[0].lower()
    return m.add(*[(1,signed_source_point(tag,side)) for tag in first],
                 *[(-1,signed_source_point(tag,side)) for tag in second])

def sumset_gap_remaining(key,excluded,equalities=()):
    pairs=sumset_gap_pairs(key);parent={pair:pair for pair in pairs}
    def find(pair):
        while parent[pair]!=pair:pair=parent[pair]
        return pair
    for first,second in equalities:
        first,second=tuple(first),tuple(second)
        m.need(first in parent and second in parent,'Source pair equality labels')
        parent[find(first)]=find(second)
    forbidden={find(tuple(pair)) for pair in excluded}
    return len({find(pair) for pair in pairs}-forbidden)

def sumset_gap_capacity(keys,excluded,outer_count,equalities=None):
    m.need(len(keys)==len(set(keys)) and set(keys)<=set(SUMSET_GAPS),'Disjoint source gap capacity')
    capped=bool(keys) and keys[0][0].isupper()
    m.need(all(k[0].isupper()==capped for k in keys),'Single nonoverlapping source gap family')
    row=({'K':1,'Ms':-1,'Mt':-1,'Rs':-1-len(keys),'Rt':-1-len(keys),'Bs':-1,'Bt':-1} if capped else
         {'K':1,'Ms':-1,'Mt':-1,'ts':-1-len(keys),'tt':-1-len(keys),'xs':1+len(keys),'xt':1+len(keys)})
    for key in keys:
        side,other,lower,upper,qs,qo=sumset_gap_data(key)
        row=m.add((1,row),(1,upper),(-1,lower))
        m.need(set(excluded.get(key,set()))<=set(sumset_gap_pairs(key)),'Source gap exclusions scope')
    rhs=1+39*len(keys) if capped else 93+103*len(keys)-outer_count
    return row,rhs-sum(40-sumset_gap_remaining(key,excluded.get(key,set()),(equalities or {}).get(key,())) for key in keys),'source internal gaps'

def integer_source_domain(name,j,positive):
    if name in ('xs','xt','ts','tt','delta','tau_total'):return 0,496-73*j+(14 if positive else 0)
    if name in tuple(a+b for a in 'abce' for b in 'st'):return 0,655-73*j+(14 if positive else 0)
    if name=='K':return 145,4096
    return None

def core_mass_ceiling(limits):
    lo,hi=(limits or {}).get('rank_k',(0,17))
    m.need(type(lo) is int and type(hi) is int and 0<=lo<=hi<=17,'Core mass rank interval')
    return [({'ts':1,'xs':-(32-lo)},0,'core maximum mass s'),
            ({'tt':1,'xt':-(32+hi)},0,'core maximum mass t')]

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
    # A nested branch/import must not replace its caller's endpoint planes
    # or geometry. In particular an ensuing endpoint_credit uses THIS
    # record's saved planes, not those of the most recently replayed child.
    import parametric as p
    names=('USE_PLANES','PLANE_GENERATOR','PLANE_TABLE','USED_PLANES',
           'SOURCE_TAIL_RANKS','SHARP_PLANES','SIDE_PLANES','TRIM_SOURCE',
           'POINT_OVERLAP','FULL_EDGES')
    saved={name:getattr(p,name) for name in names}
    geometry=dict(p.build.__dict__);model_geometry=dict(m.build.__dict__)
    p.USED_PLANES=set()
    try:return _replay(record,require_closed,return_state)
    finally:
        for name,value in saved.items():setattr(p,name,value)
        p.build.__dict__.clear();p.build.__dict__.update(geometry)
        m.build.__dict__.clear();m.build.__dict__.update(model_geometry)


def _replay(record,require_closed=True,return_state=False):
    import parametric as p
    cache_key=None
    if not require_closed and return_state:
        import record_pool
        # Base row indices depend on dictionary insertion order (notably
        # limits). Reordered records must never share a verification cache.
        # A content-addressed record commits to all descendant records while
        # preserving dictionary order. Shared ancestors need not be expanded
        # repeatedly into potentially exponential unpooled JSON strings.
        cache_key=record_pool.record_digest(record)
        if cache_key in PREMISE_CACHE:
            PREMISE_CACHE.move_to_end(cache_key);return PREMISE_CACHE[cache_key]
    prior=inherited(record)
    import first_gap_core
    core_shape=first_gap_core.shape_case(record)
    if core_shape is None and prior:core_shape=prior.get('core_shape')
    p.USE_PLANES='planes' in record;p.PLANE_GENERATOR=None;p.PLANE_TABLE=record.get('planes',{})
    p.SOURCE_TAIL_RANKS=record.get('source_tail_ranks',False)
    p.SHARP_PLANES=record.get('sharp_planes',False)
    p.SIDE_PLANES=record.get('side_planes',False)
    p.TRIM_SOURCE=record.get('trim_source',False)
    p.POINT_OVERLAP=record.get('point_overlap',False)
    p.FULL_EDGES=record.get('full_edges',False)
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
    low=set();high=set();covered=set();covered_positive=set();fixed_pairs=set();coverage_probes={};closed=False;constants=dict(p.build.last_compression);tail_low={'s':set(),'t':set()};tail_counts={'s':0,'t':0};tail_pairs={'s':set(),'t':set()};facts=[];point_hits={};point_groups={};extended_hits={};leading_hits={};leading_extended={};trim_pairs=set();sumset_excluded={};sumset_equalities={}
    if prior:
        low=set(prior['low']);high=set(prior['high']);covered=set(prior.get('covered',[]));covered_positive=set(prior.get('covered_positive',[]));fixed_pairs={tuple(pair) for pair in prior.get('fixed_pairs',[])};facts=list(prior['facts']);rows.extend(facts)
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

    if prior:
        for a,b,gap,tags in prior.get('leading_hits',[]):
            matches=[i for i,(aa,bb,gg) in enumerate(edges) if (a,b,gap)==(aa,bb,gg)]
            m.need(len(matches)==1,'Inherited leading overlap edge');leading_hits[matches[0]]=set(tags)
    if prior:
        for a,b,gap,groups in prior.get('leading_extended',[]):
            matches=[i for i,(aa,bb,gg) in enumerate(edges) if (a,b,gap)==(aa,bb,gg)]
            m.need(len(matches)==1,'Inherited extended leading edge');leading_extended[matches[0]]={int(q):set(tags) for q,tags in groups}
    if prior:sumset_excluded={key:set(tuple(pair) for pair in pairs) for key,pairs in prior.get('sumset_excluded',{}).items()}
    if prior:coverage_probes={key:dict(excluded=set(value['excluded']),forced=bool(value.get('forced'))) for key,value in prior.get('coverage_probes',{}).items()}
    if prior:sumset_equalities={key:list(values) for key,values in prior.get('sumset_equalities',{}).items()}
    coverage_width=prior.get('coverage_width',8 if positive else 1) if prior else (8 if positive else 1)
    coverage_bracket_width=prior.get('coverage_bracket_width',coverage_width) if prior else coverage_width
    import full_cover
    full_probes=full_cover.copy_probes(prior.get('full_probes',[])) if prior else []
    core_tail_excluded={side:set(values) for side,values in prior.get('core_tail_excluded',{}).items()} if prior else {}
    ordered_cover={side:dict(order=list(value['order']),excluded=set(value['excluded'])) for side,value in prior.get('ordered_cover',{}).items()} if prior else {}
    for index,step in enumerate(record['trace']):
        kind=step['kind']
        m.need(not closed,'Steps after contradiction')
        if kind=='core_mass_ceiling':
            extra=core_mass_ceiling(record.get('limits'));rows.extend(extra);facts.extend(extra)
        elif kind=='coverage_width':
            hi=step['hole_upper']
            m.need(positive and j>=3 and 3 not in st.values() and type(hi) is int and 1<=hi<coverage_width-1,'Strict target-cover width improvement')
            guard={'hole_W':1,'ONE':-hi};check(step['certificate'],rows,eqs,guard,strict=False)
            fact=(guard,0,'proved target-hole bound');rows.append(fact);facts.append(fact)
            coverage_width=hi+1
            coverage_bracket_width=hi+1
            for state in coverage_probes.values():state['forced']=False
        elif kind=='first_gap_shape_interior':
            import first_gap_core
            case=core_shape
            m.need(case is not None and (record.get('limits') or {}).get('hole_W')==[1,1],'Actual first-gap shape with exactly one target hole')
            h=first_gap_core.CASES[case][0]
            m.need(coverage_width>1 or h+2<coverage_bracket_width,'Strict shape-based interior improvement')
            coverage_probes={};coverage_width=1;coverage_bracket_width=h+2
        elif kind=='single_hole_interior':
            import single_hole
            m.need(positive and j>=3 and 3 not in st.values() and (coverage_width>1 or step['H']+2<coverage_bracket_width),'Single-hole main domain or strict interior improvement')
            guards=single_hole.guards(step['H'])
            m.need(len(step['certificates'])==2,'Complete single-hole location guards')
            for guard,cert in zip(guards,step['certificates']):
                check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved single-hole location');rows.append(fact);facts.append(fact)
            coverage_probes={};coverage_width=1;coverage_bracket_width=step['H']+2
        elif kind in ('ordered_cover_license','ordered_cover_exclude','ordered_cover_capacity'):
            import interval_gaps
            m.need(j>=3 and 3 not in st.values(),'Ordered core cover scope')
            if kind=='ordered_cover_capacity':
                m.need(step['credit']==e and type(step['joint']) is bool,'Ordered cover fixed credit')
                fact=interval_gaps.capacity(st,p.build.last_Z,ordered_cover,step['selected'],e,step['joint']);rows.append(fact);facts.append(fact)
            else:
                side=step['side']
                if kind=='ordered_cover_license':
                    m.need(side not in ordered_cover,'New ordered cover license')
                    guards=interval_gaps.licenses(st,p.build.last_Z,side,step['order'])
                else:
                    m.need(side in ordered_cover and step['index'] not in ordered_cover[side]['excluded'],'Licensed new gap singleton exclusion')
                    guards=interval_gaps.exclusion(st,p.build.last_Z,side,step['index'],step['where'])
                m.need(len(guards)==len(step['certificates']),'Ordered cover guard inventory')
                for guard,cert in zip(guards,step['certificates']):
                    check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved ordered core cover guard');rows.append(fact);facts.append(fact)
                if kind=='ordered_cover_license':ordered_cover[side]=dict(order=step['order'],excluded=set())
                else:ordered_cover[side]['excluded'].add(step['index'])
        elif kind=='combined_hole_mass':
            import combined_holes
            m.need(positive and type(step['retained']) is bool,'Combined hole domain')
            if step['retained']:m.need(j==4 and step['credit']==e and e>=38,'Combined predecessor propagation domain')
            guard={'hole_W':1,'ONE':-2};check(step['certificate'],rows,eqs,guard,strict=False)
            extra=[(guard,0,'proved combined hole range'),combined_holes.total_rows(step['retained'])]
            rows.extend(extra);facts.extend(extra)
        elif kind=='positive_retained_kernel':
            import positive_kernel
            m.need(j==4 and positive and step['credit']==e and e>=38,'Retained positive kernel scope')
            W,rank_hi=step['W'],step['rank_hi'];spec=positive_kernel.plan(W,e,rank_hi)
            guards=[{'hole_W':-1,'ONE':W},{'hole_W':1,'ONE':-W},{'rank_k':1,'ONE':-rank_hi}]
            m.need(len(step['certificates'])==3,'Positive kernel guard inventory')
            for guard,cert in zip(guards,step['certificates']):
                check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved positive retained kernel range');rows.append(fact);facts.append(fact)
            for side,q in step['choices']:
                m.need(side in spec and type(q) is int and 1<=q<=spec[side]['depth'],'Licensed positive kernel depth')
                extra=positive_kernel.rows(W,side,q);rows.extend(extra);facts.extend(extra)
            for q in step.get('combined',[]):
                extra=positive_kernel.combined_rows(W,e,rank_hi,q);rows.extend(extra);facts.extend(extra)
        elif kind=='retained_positive_predecessor':
            import positive_holes
            m.need(j==4 and positive and step['credit']==e and e>=38,'Retained positive predecessor scope and credit')
            lo,hi=step['lo'],step['hi'];extra=positive_holes.retained_predecessor_rows(lo,hi)
            guards=[{'hole_W':-1,'ONE':lo},{'hole_W':1,'ONE':-hi}]
            m.need(len(step['certificates'])==2,'Retained predecessor range guards')
            for guard,cert in zip(guards,step['certificates']):
                check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved retained predecessor range');rows.append(fact);facts.append(fact)
            rows.extend(extra);facts.extend(extra)
        elif kind=='positive_predecessor_gap':
            import positive_holes
            m.need(positive,'Positive predecessor hole scope')
            extra=positive_holes.predecessor_rows(j);rows.extend(extra);facts.extend(extra)
        elif kind=='positive_core_gap':
            import positive_holes
            hi=step['rank_hi'];m.need(positive and type(hi) is int and 0<=hi<=17,'Positive first-gap main domain')
            guard={'rank_k':1,'ONE':-hi};check(step['certificate'],rows,eqs,guard,strict=False)
            fact=(guard,0,'proved positive first-gap rank range');rows.append(fact);facts.append(fact)
            extra=positive_holes.first_gap_rows(hi);rows.extend(extra);facts.extend(extra)
        elif kind=='positive_hole_side_interval':
            import positive_holes
            lo,hi=step['lo'],step['hi'];extra=positive_holes.side_interval_rows(lo,hi)
            m.need(positive and len(step['certificates'])==2,'Restricted positive side profile')
            guards=[{'hole_W':-1,'ONE':lo},{'hole_W':1,'ONE':-hi}]
            for guard,cert in zip(guards,step['certificates']):
                check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved positive side interval');rows.append(fact);facts.append(fact)
            rows.extend(extra);facts.extend(extra)
        elif kind in ('positive_hole_profile','positive_hole_sides'):
            import positive_holes
            hi=step['hi'];m.need(positive and type(hi) is int and 1<=hi<=7,'Positive-hole main-domain profile')
            guard={'hole_W':1,'ONE':-hi};check(step['certificate'],rows,eqs,guard,strict=False)
            fact=(guard,0,'proved positive-hole profile range');rows.append(fact);facts.append(fact)
            extra=[positive_holes.row(hi)] if kind=='positive_hole_profile' else positive_holes.side_rows(hi)
            rows.extend(extra);facts.extend(extra)
        elif kind=='integer_guard':
            from modular import INTEGER_NAMES
            guard=step['guard']
            m.need(j>=3 and 3 not in st.values() and set(guard)<=INTEGER_NAMES and all(type(v) is int for v in guard.values()),'Rounded physical integer guard scope')
            check(step['certificate'],rows,eqs,m.add((1,guard),(-1,{'ONE':1})),strict=True)
            fact=(guard,0,'rounded integer guard');rows.append(fact);facts.append(fact)
        elif kind=='joint_core_tail_capacity':
            import known_union
            m.need(j>=3 and 3 not in st.values() and step['credit']==e,'Joint core-tail integer scope and credit')
            row=known_union.joint_tail_capacity(st,p.build.last_Z,core_tail_excluded,e);rows.append(row);facts.append(row)
        elif kind in ('core_tail_license','core_tail_exclude','core_tail_capacity'):
            import known_union
            m.need(j>=3 and 3 not in st.values(),'Core-tail integer pattern scope');side=step['side']
            end,guards,points=known_union.tail_catalogue(st,p.build.last_Z,side)
            if kind=='core_tail_license':
                m.need(side not in core_tail_excluded and len(step['certificates'])==len(guards),'New core-tail license')
                for guard,cert in zip(guards,step['certificates']):
                    check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved core-tail license');rows.append(fact);facts.append(fact)
                core_tail_excluded[side]=set()
            else:
                m.need(side in core_tail_excluded,'Missing core-tail license')
                if kind=='core_tail_exclude':
                    i=step['index'];m.need(i not in core_tail_excluded[side],'New core-tail exclusion')
                    guard=known_union.tail_exclusion(st,p.build.last_Z,side,i,step['direction'])
                    check(step['certificate'],rows,eqs,guard,strict=False);fact=(guard,0,'proved core-tail exclusion');rows.append(fact);facts.append(fact);core_tail_excluded[side].add(i)
                else:
                    row=known_union.tail_capacity(st,p.build.last_Z,side,core_tail_excluded[side]);rows.append(row);facts.append(row)
        elif kind=='cover_capacity':
            import cover_capacity
            m.need(j>=3 and 3 not in st.values() and step['credit']==e,'Cover capacity physical scope and credit')
            row,guards=cover_capacity.derive(st,p.build.last_Z,step['recipe'],e)
            m.need(len(guards)==len(step['certificates']),'Cover capacity guard certificates')
            for guard,cert in zip(guards,step['certificates']):
                check(cert,rows,eqs,guard,strict=False)
                fact=(guard,0,'proved cover capacity guard');rows.append(fact);facts.append(fact)
            rows.append(row);facts.append(row)
        elif kind=='known_union':
            import known_union
            m.need(j>=3 and 3 not in st.values() and step['credit']==e,'Known-union physical scope and credit')
            row,guards=known_union.derive(st,p.build.last_Z,step['recipe'],e)
            m.need(len(guards)==len(step['certificates']),'Known-union guard certificates')
            for guard,cert in zip(guards,step['certificates']):
                check(cert,rows,eqs,guard,strict=False)
                fact=(guard,0,'proved known-union guard');rows.append(fact);facts.append(fact)
            rows.append(row);facts.append(row)
        elif kind=='forest':
            m.need(step['e']==e,'Unproved forest credit')
            cc={int(i):v for i,v in step.get('constants',{}).items()}
            m.need(all(constants.get(i,0)>=v for i,v in cc.items()),'Unproved compression constant')
            pc={int(i):v for i,v in step.get('point_edges',{}).items()}
            m.need(all(edge_point_count(edges[i],point_hits.get(i,set()),point_groups.get(i,{}),extended_hits.get(i,{}),leading_hits.get(i,set()),leading_extended.get(i,{}))>=v for i,v in pc.items()),'Unproved point overlap')
            rows.append(forest(edges,ret,step['edges'],step['roots'],e,cc,pc))
        elif kind=='record_consequences':
            import record_consequences
            imported=record_consequences.derive(step,record);rows.extend(imported);facts.extend(imported)
            if 'credit' in step:
                m.need(step['credit']>e,'Strict imported fixed-credit improvement')
                e=step['credit'];rows.extend(credit_rows(ret,e))
        elif kind=='domain_contradiction':
            import record_consequences
            source=step['record'];m.need(all(source.get(k)==record.get(k) for k in ('st','j','positive')),'Contradiction in the same physical pattern')
            record_consequences.domain_contains(source,record)
            replay(source,require_closed=True);closed=True
        elif kind=='first_gap_core_partition':
            import first_gap_core
            m.need(j>=3 and 3 not in st.values(),'Integer first-gap partition scope')
            prefix=dict(record,trace=record['trace'][:index])
            closed=first_gap_core.check(step,record,prefix,rows,eqs,positive)
            if not closed and step.get('inherit_remaining',False):
                survivors=[c for c in step['children'] if not c['closed']]
                m.need(len(survivors)==1,'Exactly one surviving physical first-gap case')
                child=survivors[0];state=replay(child['record'],require_closed=False,return_state=True)
                core_shape=child['case'];extra=first_gap_core.rows(core_shape)+state['facts'];rows.extend(extra);facts.extend(extra)
                if state['credit']>e:e=state['credit'];rows.extend(credit_rows(ret,e))
            if not closed and 'credit' in step:
                minimum=step['credit'];m.need(type(minimum) is int and minimum>e,'Strict common first-gap credit improvement')
                e=minimum;rows.extend(credit_rows(ret,e))
            if not closed and 'hole_upper' in step:
                bound=step['hole_upper'];m.need(type(bound) is int and 1<=bound<=3,'First-gap interior bound')
                coverage_width=1;coverage_bracket_width=bound+2;coverage_probes={}
        elif kind=='full_cover_partition_credit':
            import cover_partition
            m.need(j>=3 and 3 not in st.values(),'Integer target credit partition scope')
            minimum=step['credit'];m.need(type(minimum) is int and minimum>e,'Strict common credit improvement')
            prefix=dict(record,trace=record['trace'][:index])
            closed=cover_partition.check(step['tree'],full_probes,rows,eqs,base_record=prefix,minimum_credit=minimum)['closed']
            cover_partition.remove_closed_top(step['tree'],full_probes)
            if not closed:
                e=minimum;rows.extend(credit_rows(ret,e))
        elif kind=='full_cover_partition':
            import cover_partition
            m.need(j>=3 and 3 not in st.values(),'Integer target partition scope')
            prefix=dict(record,trace=record['trace'][:index])
            closed=cover_partition.check(step['tree'],full_probes,rows,eqs,base_record=prefix)['closed']
            cover_partition.remove_closed_top(step['tree'],full_probes)
        elif kind=='integer_cg':
            import cg_cut
            m.need(j>=3 and 3 not in st.values(),'Integer CG domain')
            fact=cg_cut.derive(step['proof'],rows,eqs);rows.append(fact);facts.append(fact)
        elif kind=='canonical_tail_mass':
            import canonical_phi
            m.need(j>=3 and 3 not in st.values(),'Canonical nonlast integer core minimum scope')
            fact,guards=canonical_phi.tail_derive(step['side'],step['cap'],step.get('core_shape'),core_shape)
            m.need(len(step['certificates'])==len(guards),'Canonical nonlast minimum licenses')
            for cert,guard in zip(step['certificates'],guards):check(cert,rows,eqs,guard,strict=False)
            rows.append(fact);facts.append(fact)
        elif kind=='shifted_canonical_phi_mass':
            import canonical_phi
            m.need(j>=3 and 3 not in st.values(),'Shifted canonical integer core minimum scope')
            fact,guards=canonical_phi.shifted_derive(step['side'],step['cap'],step['core_shape'],core_shape)
            m.need(len(step['certificates'])==len(guards),'Shifted core mass cap licenses')
            for cert,guard in zip(step['certificates'],guards):check(cert,rows,eqs,guard,strict=False)
            rows.append(fact);facts.append(fact)
        elif kind=='canonical_phi_mass':
            import canonical_phi
            m.need(j>=3 and 3 not in st.values(),'Canonical integer core minimum scope')
            fact,guards=canonical_phi.derive(step['side'],step['cap'])
            m.need(len(step['certificates'])==2,'Canonical core mass cap licenses')
            for cert,guard in zip(step['certificates'],guards):check(cert,rows,eqs,guard,strict=False)
            rows.append(fact);facts.append(fact)
        elif kind=='averaged_source_capacity':
            import averaged_source
            m.need(not positive and j>=3 and 3 not in st.values(),'Zero-hole averaged-source capacity scope')
            fact,guards=averaged_source.derive(step['proof'])
            m.need(len(step['certificates'])==len(guards),'Every averaged-source hull guard')
            for cert,guard in zip(step['certificates'],guards):check(cert,rows,eqs,guard,strict=False)
            rows.append(fact);facts.append(fact)
        elif kind=='trimmed_source_capacity':
            import trimmed_source
            m.need(not positive and j>=3 and 3 not in st.values(),'Zero-hole trimmed-source capacity scope')
            fact,guards=trimmed_source.derive(step['proof'])
            m.need(len(step['certificates'])==len(guards),'Every trimmed-source hull guard')
            for cert,guard in zip(step['certificates'],guards):check(cert,rows,eqs,guard,strict=False)
            rows.append(fact);facts.append(fact)
        elif kind=='source_envelope_capacity':
            import source_envelope
            m.need(j>=3 and 3 not in st.values(),'Integer source-envelope capacity scope')
            fact,guards=source_envelope.derive(step['proof'],core_shape)
            m.need(len(step['certificates'])==len(guards),'Every source-envelope hull guard')
            for cert,guard in zip(step['certificates'],guards):check(cert,rows,eqs,guard,strict=False)
            rows.append(fact);facts.append(fact)
        elif kind=='source_hull_capacity':
            import source_hulls
            m.need(j>=3 and 3 not in st.values(),'Integer source-hull capacity scope')
            fact,guards=source_hulls.derive(step['proof'],core_shape)
            m.need(len(step['certificates'])==len(guards),'Every source hull membership guard')
            for cert,guard in zip(step['certificates'],guards):check(cert,rows,eqs,guard,strict=False)
            rows.append(fact);facts.append(fact)
        elif kind=='source_union_capacity':
            import source_union,first_gap_core
            m.need(j>=3 and 3 not in st.values(),'Integer source-union capacity scope')
            body,guards=source_union.derive(step['proof'],core_shape)
            m.need(len(step['certificates'])==len(guards),'Every source membership guard certified')
            for cert,guard in zip(step['certificates'],guards):check(cert,rows,eqs,guard,strict=False)
            fact=(body,0,'complete double-source union capacity');rows.append(fact);facts.append(fact)
        elif kind=='full_window_capacity':
            import full_window,first_gap_core
            m.need(j>=3 and 3 not in st.values(),'Integer full-window capacity scope')
            body,guards=full_window.derive(step['proof'],positive,coverage_width,coverage_bracket_width,core_shape)
            m.need(len(step['certificates'])==len(guards),'Every full-window guard certified')
            for cert,guard in zip(step['certificates'],guards):check(cert,rows,eqs,guard,strict=False)
            fact=(body,0,'complete four-sum window capacity');rows.append(fact);facts.append(fact)
        elif kind in ('full_cover_probe','full_cover_extended_probe','full_cover_known_probe','full_cover_refine','full_cover_exclude','full_cover_gap_exclude','full_cover_modular_exclude','full_cover_subsume','full_cover_bound','full_cover_force','full_cover_final'):
            m.need(j>=3 and 3 not in st.values(),'Complete integer four-sum cover scope')
            if kind=='full_cover_extended_probe':
                import full_window
                proof=step['proof'];m.need(proof['lower']==proof['upper'] and 'outer_extension' in proof,'One extended-interval target')
                guards=full_window.proof_bracket(proof,positive,coverage_width,coverage_bracket_width)
                m.need(len(step['certificates'])==len(guards),'Every extended target guard')
                for guard,cert in zip(guards,step['certificates']):
                    check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved full target bracket');rows.append(fact);facts.append(fact)
                full_probes.append(dict(target=proof['lower'],mask=0,width=1,margin=0,nodes=full_cover.initial_nodes(),forced=False))
            elif kind=='full_cover_known_probe':
                target=full_cover.known_target(step['mask'],step['source_mask'])
                full_probes.append(dict(target=target,mask=step['mask'],width=1,margin=0,nodes=full_cover.initial_nodes(),forced=False))
            elif kind=='full_cover_probe':
                from modular import INTEGER_NAMES
                target=step['target'];mask=step['mask']
                m.need(isinstance(target,dict) and set(target)<=INTEGER_NAMES and all(type(v) is int for v in target.values()),'Integral affine target')
                width,margin=full_cover.profile(positive,coverage_width,coverage_bracket_width)
                guards=full_cover.bracket(target,mask,width,margin)
                m.need(len(step['certificates'])==2,'Complete full target bracket')
                for guard,cert in zip(guards,step['certificates']):
                    check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved full target bracket');rows.append(fact);facts.append(fact)
                full_probes.append(dict(target=target,mask=mask,width=width,margin=margin,nodes=full_cover.initial_nodes(),forced=False))
            else:
                pid=step['probe'];m.need(type(pid) is int and 0<=pid<len(full_probes),'Licensed full target probe')
                state=full_probes[pid];nodes=state['nodes'];width=state['width'];target=state['target']
                if kind=='full_cover_refine':
                    full_cover.refine(nodes,step['root']);state['forced']=False
                elif kind=='full_cover_bound':
                    from modular import INTEGER_NAMES
                    guard=step['guard'];m.need(set(guard)<=INTEGER_NAMES and all(type(v) is int for v in guard.values()),'Integer complete-cover consequence')
                    cases=step['cases'];inventory=[tuple(case['node']) for case in cases]
                    m.need(set(inventory)==nodes and len(inventory)==len(nodes),'Every live cover alternative has a consequence')
                    for case in cases:
                        augmented=rows+[(g,0,'case target containment') for g in full_cover.containment(target,tuple(case['node']),width)]
                        m.need(type(case['infeasible']) is bool,'Exact alternative consequence kind')
                        rounded=case.get('rounded',False);m.need(type(rounded) is bool,'Integer alternative rounding flag')
                        m.need(not case['infeasible'] or not rounded,'Infeasible case needs no rounding')
                        consequence=m.add((1,guard),(-1,{'ONE':1})) if rounded else guard
                        check(case['certificate'],augmented,eqs,None if case['infeasible'] else consequence,strict=rounded)
                    fact=(guard,0,'complete target-cover consequence');rows.append(fact);facts.append(fact)
                elif kind=='full_cover_exclude':
                    node=tuple(step['node']);m.need(node in nodes,'Live full target component')
                    guard=full_cover.exclusion(target,node,step['direction'],width);check(step['certificate'],rows,eqs,guard,strict=False)
                    fact=(guard,0,'proved full component exclusion');rows.append(fact);facts.append(fact);nodes.remove(node)
                elif kind=='full_cover_gap_exclude':
                    import core_gap
                    node=tuple(step['node']);m.need(node in nodes,'Live component for extreme-gap exclusion')
                    shape=step.get('core_shape');m.need(shape is None or type(shape) is int and shape==core_shape,'Licensed first-gap extreme interval')
                    guards=core_gap.guards(target,node,width,step['side'],shape,step.get('prefix',0))
                    m.need(len(step['certificates'])==2,'Both extreme-gap containment guards')
                    for guard,cert in zip(guards,step['certificates']):
                        check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved empty extreme-sum interval');rows.append(fact);facts.append(fact)
                    nodes.remove(node);state['forced']=False
                elif kind=='full_cover_modular_exclude':
                    import modular
                    node=tuple(step['node']);m.need(node in nodes and width==1,'Live singleton full target component')
                    lo,hi=full_cover.interval(*node);m.need(not any(m.add((1,lo),(-1,hi)).values()),'Full-cover modular singleton')
                    modular.check(step['certificate'],rows,eqs,m.add((1,lo),(-1,target)));nodes.remove(node)
                elif kind=='full_cover_subsume':
                    node,by=tuple(step['node']),tuple(step['by']);m.need(node in nodes and by in nodes,'Live final cover containment')
                    guards=full_cover.subsumption(node,by);m.need(len(step['certificates'])==2,'Complete final containment guards')
                    for guard,cert in zip(guards,step['certificates']):
                        check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved final component containment');rows.append(fact);facts.append(fact)
                    nodes.remove(node)
                elif kind=='full_cover_force':
                    node=tuple(step['node']);m.need(nodes=={node} and not state['forced'],'Unique full target component')
                    for guard in full_cover.containment(target,node,width):
                        fact=(guard,0,'required full target component');rows.append(fact);facts.append(fact)
                    state['forced']=True
                else:
                    m.need(not nodes,'Every full target component excluded');closed=True
        elif kind in ('coverage_probe','coverage_exclude','coverage_modular_exclude','coverage_force','coverage_final'):
            import cover_geometry as coverage
            m.need(j>=3 and 3 not in st.values(),'Bounded-hole integer target cover scope');width=coverage_width
            side,probe_index=step['side'],step['probe'];components=coverage.catalogue(st,p.build.last_Z,side);key=side+':'+str(probe_index)
            if kind=='coverage_probe':
                m.need(key not in coverage_probes,'New target probe')
                guards=coverage.bracket(components,side,probe_index,coverage_bracket_width);m.need(len(step['certificates'])==2,'Target probe bracket')
                for guard,cert in zip(guards,step['certificates']):
                    check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved target probe bracket');rows.append(fact);facts.append(fact)
                coverage_probes[key]=dict(excluded=set(),forced=False)
            else:
                m.need(key in coverage_probes,'Unlicensed target probe');state=coverage_probes[key]
                if kind=='coverage_exclude':
                    component=step['component'];m.need(component not in state['excluded'],'New cover exclusion')
                    guard=coverage.exclusion(components,probe_index,component,step['direction'],width);check(step['certificate'],rows,eqs,guard,strict=False)
                    fact=(guard,0,'proved target component exclusion');rows.append(fact);facts.append(fact);state['excluded'].add(component)
                elif kind=='coverage_modular_exclude':
                    import modular
                    component=step['component']
                    m.need(width==1 and type(component) is int and 0<=component<len(components) and component not in state['excluded'],'New zero-hole modular exclusion')
                    _,lo,hi=components[component];m.need(lo==hi,'Modular exclusion singleton scope')
                    target=m.add((1,lo),(-1,coverage.probe(components,probe_index)))
                    modular.check(step['certificate'],rows,eqs,target);state['excluded'].add(component)
                elif kind=='coverage_force':
                    component=step['component'];m.need(set(range(len(components)))-state['excluded']=={component} and not state['forced'],'Unique remaining cover component')
                    for guard in coverage.containment(components,probe_index,component,width):
                        fact=(guard,0,'required target component');rows.append(fact);facts.append(fact)
                    state['forced']=True
                else:
                    m.need(state['excluded']==set(range(len(components))),'Every cover component excluded');closed=True
        elif kind=='fixed_probe_pair':
            m.need(j>=3 and 3 not in st.values() and step['resource'] in ret,'Integer retained fixed probe pair')
            first,second=step['first'],step['second'];pair=tuple(sorted((first,second)));m.need(pair not in fixed_pairs,'New fixed probe conflict')
            guards=fixed_probe_pair_guards(first,second,step['resource'],step['core_side'],p.build.last_Z)
            m.need(len(guards)==len(step['certificates']),'Fixed probe guard count')
            for guard,cert in zip(guards,step['certificates']):
                check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved fixed probe conflict');rows.append(fact);facts.append(fact)
            fixed_pairs.add(pair)
        elif kind=='fixed_pair':
            m.need(j>=3 and 3 not in st.values(),'Integer fixed conflict scope')
            first,second=step['first'],step['second'];pair=tuple(sorted((first,second)));m.need(pair not in fixed_pairs,'New fixed conflict')
            guards=fixed_pair_guards(first,second,step['mode']);m.need(len(guards)==len(step['certificates']),'Fixed conflict guard count')
            for guard,cert in zip(guards,step['certificates']):
                check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved fixed conflict');rows.append(fact);facts.append(fact)
            fixed_pairs.add(pair)
        elif kind=='fixed_cover_positive':
            label=step['label'];m.need(label in covered and label not in covered_positive,'Positive covered fixed label')
            guard=m.add((1,{'ONE':1}),(-1,forms[label]));check(step['certificate'],rows,eqs,guard,strict=False)
            fact=(guard,0,'proved covered fixed positive');rows.append(fact);facts.append(fact);covered_positive.add(label)
        elif kind=='fixed_shifted_cover':
            import shifted_source
            m.need(positive and j>=3 and 3 not in st.values(),'Shifted known-cover domain')
            label=step['label'];m.need(label not in covered,'New shifted known cover')
            guards=shifted_source.cover_guards(st,p.build.last_Z,step['modes'],step['side'],step['chain'],label)
            m.need(len(guards)==len(step['certificates']),'Shifted known-cover guards')
            for guard,cert in zip(guards,step['certificates']):
                check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved shifted fixed cover');rows.append(fact);facts.append(fact)
            covered.add(label)
        elif kind=='fixed_known_cover':
            import known_union
            m.need(j>=3 and 3 not in st.values(),'Known fixed-cover scope')
            label=step['label'];m.need(label not in covered,'New known fixed cover')
            guards=known_union.cover_guards(st,p.build.last_Z,step['modes'],step['side'],step['chain'],label)
            m.need(len(guards)==len(step['certificates']),'Known fixed-cover guard count')
            for guard,cert in zip(guards,step['certificates']):
                check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved known fixed cover');rows.append(fact);facts.append(fact)
            covered.add(label)
        elif kind=='fixed_cover':
            m.need(j>=3 and 3 not in st.values(),'Integer fixed cover scope')
            label,resource=step['label'],step['resource'];m.need(label not in covered and (resource in ret or resource in ('Ls','Lt')),'New retained fixed cover')
            guards=fixed_cover_guards(label,resource,step['q'],step.get('witness'),p.build.last_Z)
            m.need(len(guards)==len(step['certificates']),'Fixed cover guard count')
            for guard,cert in zip(guards,step['certificates']):
                check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved fixed source cover');rows.append(fact);facts.append(fact)
            covered.add(label)
        elif kind=='sumset_pair_equal':
            key,first,second=step['gap'],step['first'],step['second']
            difference=sumset_pair_difference(key,first,second);m.need(len(step['certificates'])==2,'Two source equality proofs')
            for guard,cert in zip((difference,{k:-v for k,v in difference.items()}),step['certificates']):
                check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved source pair equality');rows.append(fact);facts.append(fact)
            sumset_equalities.setdefault(key,[]).append((tuple(first),tuple(second)))
        elif kind=='sumset_gap_exclude':
            m.need(record.get('sumset_gaps') and record.get('point_overlap'),'Source gap proof scope')
            key,pair,index=step['gap'],tuple(step['pair']),step['guard']
            m.need(type(index) is int and index in (0,1) and pair not in sumset_excluded.get(key,set()),'New source gap pair exclusion')
            guard=sumset_gap_guards(key,pair)[index];check(step['certificate'],rows,eqs,guard,strict=False)
            fact=(guard,0,'proved source gap pair outside');rows.append(fact);facts.append(fact)
            sumset_excluded.setdefault(key,set()).add(pair)
        elif kind=='sumset_gap_capacity':
            m.need(record.get('sumset_gaps'),'Source gap capacity scope')
            fact=sumset_gap_capacity(step['gaps'],sumset_excluded,len(trim_pairs),sumset_equalities);rows.append(fact);facts.append(fact)
        elif kind=='leading_overlap_hit':
            i,tag,witness,q=step['edge'],step['tag'],step['witness'],step.get('q',5)
            m.need(record.get('leading_overlap') and record.get('point_overlap') and type(i) is int and 0<=i<len(edges),'Leading overlap scope')
            known=leading_hits.setdefault(i,set()) if q==5 else leading_extended.setdefault(i,{}).setdefault(q,set())
            m.need(tag not in known,'Repeated leading exterior point')
            guards=leading_point_guards(edges[i],tag,witness,q);m.need(len(step['certificates'])==len(guards),'All leading containment guards')
            for guard,cert in zip(guards,step['certificates']):
                check(cert,rows,eqs,guard,strict=False);fact=(guard,0,'proved leading exterior hit');rows.append(fact);facts.append(fact)
            known.add(tag)
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
        elif kind=='ownerless_core_hit':
            import ownerless_hit
            row,guard=ownerless_hit.derive(st,j,positive,e,step['side'])
            check(step['certificate'],rows,eqs,guard,strict=False)
            rows.append(row);facts.append(row)
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
            next_e=credit(low,high,initial,covered,covered_positive,fixed_pairs)
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
        state=dict(credit=e,low=low,high=high,covered=covered,covered_positive=covered_positive,fixed_pairs=sorted(fixed_pairs),coverage_probes={key:dict(excluded=sorted(value['excluded']),forced=value['forced']) for key,value in coverage_probes.items()},core_tail_excluded={side:sorted(values) for side,values in core_tail_excluded.items()},ordered_cover={side:dict(order=value['order'],excluded=sorted(value['excluded'])) for side,value in ordered_cover.items()},facts=facts,tail_low=tail_low,tail_counts=tail_counts,tail_pairs=tail_pairs,
                   constants=[(*edges[i],value) for i,value in constants.items()],
                   point_hits=[(*edges[i],sorted(tags)) for i,tags in point_hits.items()],
                   point_groups=[(*edges[i],[(tags,count) for tags,count in groups.items()]) for i,groups in point_groups.items()],trim_pairs=sorted(trim_pairs),sumset_excluded={key:sorted(pairs) for key,pairs in sumset_excluded.items()},sumset_equalities=sumset_equalities,leading_hits=[(*edges[i],sorted(tags)) for i,tags in leading_hits.items()],leading_extended=[(*edges[i],[(q,sorted(tags)) for q,tags in groups.items()]) for i,groups in leading_extended.items()],extended_hits=[(*edges[i],[(q,sorted(tags)) for q,tags in groups.items()]) for i,groups in extended_hits.items()])
        state['coverage_width']=coverage_width
        state['core_shape']=core_shape
        state['coverage_bracket_width']=coverage_bracket_width
        state['full_probes']=full_cover.export_probes(full_probes)
        if cache_key is not None:
            PREMISE_CACHE[cache_key]=state;PREMISE_CACHE.move_to_end(cache_key)
            if len(PREMISE_CACHE)>64:PREMISE_CACHE.popitem(last=False)
        return state
    return dict(steps=len(record['trace']),credit=e)
