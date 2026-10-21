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


def forest(edges,ret,chosen,roots,e,constants=None):
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
    body=m.add((len(chosen)-len(constants),m.var('FD')),*[(-1,edges[i][2]) for i in chosen],
               (1,{'ells':1,'ellt':1}),(1,{'D'+v:1 for v in roots}),(-1,m.var('delta')))
    return body,-e-sum(constants.values()),'additional forest'


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


def alpha_compression(st,j,positive,e,edges):
    m.need(j==5 and not positive and e>=22,'Alpha half-mass parameters')
    m.need(all(st[k+s]==(2 if k=='O' else 0) for k in ('P','beta','O') for s in 'st')
           and sorted(st['alpha'+s] for s in 'st')==[0,1],'Alpha half-mass pattern')
    # Each X,g,h appears twice in a legitimate two-edge forest. From
    # tau+6F>=366, delta+tau<=113-I, and fixed credit e,
    # 3*(2*x-tau)>=366-4*113+4*e+4*I>0.
    m.need(366-4*113+4*e>0,'Alpha strict compression guard')
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
    st=record['st'];j=record['j'];positive=record['positive'];initial=8 if m.is_ownerless(st) else 0
    e=prior['credit'] if prior else initial
    _,rows,eqs=p.build(st,j,positive,e,record.get('limits'))
    edges=p.build.last_edges;ret=p.build.last_retained;forms=m.fixed_forms()
    low=set();high=set();closed=False;constants=dict(p.build.last_compression);tail_low={'s':set(),'t':set()};tail_counts={'s':0,'t':0};tail_pairs={'s':set(),'t':set()};facts=[]
    if prior:
        low=set(prior['low']);high=set(prior['high']);facts=list(prior['facts']);rows.extend(facts)
        tail_low={s:set(prior['tail_low'][s]) for s in 'st'};tail_counts=dict(prior['tail_counts']);tail_pairs={s:set(prior['tail_pairs'][s]) for s in 'st'}
        for a,b,gap,value in prior['constants']:
            matches=[i for i,(aa,bb,gg) in enumerate(edges) if (a,b,gap)==(aa,bb,gg)]
            m.need(len(matches)==1,'Inherited compression edge changed')
            i=matches[0];constants[i]=max(constants.get(i,0),value)
    for index,step in enumerate(record['trace']):
        kind=step['kind']
        m.need(not closed,'Steps after contradiction')
        if kind=='forest':
            m.need(step['e']==e,'Unproved forest credit')
            cc={int(i):v for i,v in step.get('constants',{}).items()}
            m.need(all(constants.get(i,0)>=v for i,v in cc.items()),'Unproved compression constant')
            rows.append(forest(edges,ret,step['edges'],step['roots'],e,cc))
        elif kind=='compression':
            i,k,source=step['edge'],step['k'],step['source']
            m.need(type(i) is int and 0<=i<len(edges) and type(k) is int and 0<=k<74 and source in ('core','source'),'Compression indices')
            mass={'ts':1,'tt':1} if source=='core' else {'TD':1}
            target=m.add((1,mass),(-k-1,edges[i][2]))
            check(step['certificate'],rows,eqs,target)
            constants[i]=max(constants.get(i,0),(66 if source=='core' else 74)-k)
            fact=(target,-1,'proved compression');rows.append(fact);facts.append(fact)
        elif kind=='alpha_half_mass':
            for i in alpha_compression(st,j,positive,e,edges):constants[i]=max(constants.get(i,0),65)
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
                   constants=[(*edges[i],value) for i,value in constants.items()])
        if cache_key is not None:PREMISE_CACHE[cache_key]=state
        return state
    return dict(steps=len(record['trace']),credit=e)
