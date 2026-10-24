"""Cardinality of a translated subset-sum window inside the full four-sum cover.

A live component is charged its hull length or a licensed exact cardinality. An excluded
component must be strictly outside the window. Overlap only overcounts.
"""
import model as m
import full_cover as fc
from modular import INTEGER_NAMES
ONE={'ONE':1}

def core_power(node):
    m.need(node[1]>=0,'Refined core translate')
    return 4-len(fc.roots()[node[0]])-len(fc.children(node[0])[node[1]])

def mixed_gap(a,b,anchor,direction):
    p,q=core_power(a),core_power(b)
    m.need(1<=p<q<=4,'Increasing mixed core powers')
    m.need(len(anchor)==2 and all(type(i) is int and i>=0 for i in anchor) and sum(anchor)<=q-p,'Anchor is an actual (q-p)-core sum')
    m.need(type(direction) is int and direction in (-1,1),'Mixed overlap orientation')
    # A lower hull endpoint equals its centre minus power*R_t.
    gap=m.add((1,fc.interval(*b)[0]),(-1,fc.interval(*a)[0]),
              (q-p-anchor[1],{'Rt':1}),(anchor[0],{'Rs':1}))
    return m.add((direction,gap))

def core_capacity(power,first_gap_case=None):
    """Hull capacity minus the two gaps next to the extreme core sums.

    The predecessor of R_v is at most r_v-1+tau_v-xi_v.  Hence every
    qE misses at least max(0,2xi_v-tau_v) positions next to qR_v.
    The two end gaps are disjoint (the core contains zero).
    """
    m.need(type(power) is int and 2<=power<=4,'Core power for mass capacity')
    result=m.add((power,{'Rs':1,'Rt':1}),(1,ONE),(-2,{'xs':1,'xt':1}),(1,{'ts':1,'tt':1}))
    if first_gap_case is not None:
        from first_gap_core import removed_prefix_mass
        result=m.add((1,result),(-1,removed_prefix_mass(first_gap_case)))
    return result

def parameters(positive,coverage_width,bracket_width):
    return (bracket_width-1,{}) if positive and coverage_width==1 else (0,{'hole_W':2} if positive else {})

def bracket(lower,upper,mask,margin):
    for endpoint in (lower,upper):
        m.need(isinstance(endpoint,dict) and set(endpoint)<=INTEGER_NAMES and all(type(c) is int for c in endpoint.values()),'Integer complete-window endpoint')
    centre=fc.shift(mask)
    return [m.add((1,centre),(-1,{'St':1}),(margin,ONE),(-1,lower)),
            m.add((1,upper),(-1,centre),(-1,{'Ss':1}),(margin,ONE))]

def proof_bracket(proof,positive,coverage_width,bracket_width):
    margin,_=parameters(positive,coverage_width,bracket_width)
    ordinary=bracket(proof['lower'],proof['upper'],proof['mask'],margin)
    if 'outer_extension' not in proof:return ordinary
    m.need(proof['mask']==0 and (not positive or coverage_width==1),'Complete source interval for outer extension')
    order=proof['outer_extension'];m.need(len(set(order))==len(order) and all(type(i) is int and 0<=i<8 for i in order),'Distinct outer extension points')
    lower=m.add((-1,{'St':1}),(margin,ONE));upper=m.add((1,{'Ss':1}),(-margin,ONE));guards=[]
    for index in order:
        value=fc.outer()[index];magnitude={k:(1 if index<4 else -1)*v for k,v in value.items()}
        guards.append(m.add((1,magnitude),(1,lower),(-1,upper),(-1,ONE)))
        if index<4:upper=m.add((1,upper),(1,value))
        else:lower=m.add((1,lower),(1,value))
    guards.extend([m.add((1,lower),(-1,proof['lower'])),m.add((1,proof['upper']),(-1,upper))])
    return guards

def exclusion(lower,upper,node,direction):
    m.need(type(direction) is int and direction in (0,1),'Window exclusion direction')
    lo,hi=fc.interval(*node)
    return m.add((1,hi),(1,ONE),(-1,lower)) if direction==0 else m.add((1,upper),(1,ONE),(-1,lo))

def derive(proof,positive,coverage_width,bracket_width,first_gap_case=None):
    shape=proof.get('core_shape')
    m.need(shape is None or type(shape) is int and shape==first_gap_case,'Licensed physical first-gap shape for core capacity')
    exact_one=proof.get('exact_one_term',False);m.need(type(exact_one) is bool,'Window exact-cardinality flag')
    mass_core=proof.get('mass_core',[]);m.need(len(set(map(tuple,mass_core)))==len(mass_core),'Unique core mass capacities')
    mass_core=set(map(tuple,mass_core))
    clipped=proof.get('clipped',[]);m.need(len({tuple(v['node']) for v in clipped})==len(clipped),'Unique clipped components')
    clipped={tuple(v['node']):v for v in clipped}
    extreme=proof.get('extreme_only',[]);m.need(len({tuple(v['node']) for v in extreme})==len(extreme),'Unique extreme-only components')
    extreme={tuple(v['node']):v for v in extreme}
    lower,upper=proof['lower'],proof['upper'];margin,holes=parameters(positive,coverage_width,bracket_width)
    guards=proof_bracket(proof,positive,coverage_width,bracket_width)
    refined=proof['refined'];m.need(len(set(refined))==len(refined),'Unique window refinements')
    inventory=fc.initial_nodes()
    for root in refined:fc.refine(inventory,root)
    seen=set()
    for item in proof['outside']:
        node=tuple(item['node']);m.need(node in inventory and node not in seen,'Complete-window exclusion inventory');seen.add(node)
        guards.append(exclusion(lower,upper,node,item['direction']))
    for item in proof.get('gap_outside',[]):
        import core_gap
        node=tuple(item['node']);m.need(node in inventory and node not in seen,'Extreme-gap window component inventory');seen.add(node)
        a,b=core_gap.gap_interval(node,item['side'],shape if node[1]>=0 else None)
        guards.extend([m.add((1,a),(-1,lower)),m.add((1,upper),(-1,b))])
    body=m.add((1,upper),(-1,lower),(1,ONE),(-1,holes))
    groups=proof.get('absorbed',[]);hull_charged={tuple(g['by']) for g in groups}
    m.need(len(hull_charged)==len(groups),'Unique absorbing hulls')
    for node in proof['inside']:
        node=tuple(node);m.need(node in inventory and node not in seen,'Complete-window retained inventory');seen.add(node)
        lo,hi=fc.interval(*node)
        remaining=4-len(fc.roots()[node[0]])
        if node[1]>=0:remaining-=len(fc.children(node[0])[node[1]])
        if node in extreme:
            import core_gap
            m.need(node not in clipped and node not in mass_core and node not in hull_charged,'Extreme-only component has its one-point charge')
            guards.append(core_gap.extreme_only_guard(lower,upper,node,extreme[node]['side'],shape if node[1]>=0 else None))
            body=m.add((1,body),(-1,ONE))
        elif node in clipped:
            spec=clipped[node]
            m.need(node not in mass_core and node not in hull_charged,'Clipping has its own hull charge')
            m.need(type(spec['left']) is int and spec['left'] in (0,1) and type(spec['right']) is int and spec['right'] in (0,1),'Window clipping selectors')
            a=lower if spec['left'] else lo;b=upper if spec['right'] else hi
            # Intersection is contained in either selected endpoint hull.
            # A nonnegative hull length is needed even for an empty set.
            guards.append(m.add((1,a),(-1,b),(-1,ONE)))
            body=m.add((1,body),(-1,b),(1,a),(-1,ONE))
        elif node in mass_core:
            m.need(node[1]>=0 and node not in hull_charged,'Refined, unabsorbed core mass capacity')
            body=m.add((1,body),(-1,core_capacity(remaining,shape)))
        elif exact_one and remaining==1 and node not in hull_charged:
            # A translate of D has 73 points; a translate of E has 65.
            body=m.add((1,body),(-(73 if node[1]==-1 else 65),ONE))
        elif exact_one and node[1]==-1 and remaining==2:
            body=m.add((1,body),(-1,{'K':1}))
        else:body=m.add((1,body),(-1,hi),(1,lo),(-1,ONE))
    retained={tuple(n) for n in proof['inside']}
    m.need(mass_core<=retained and set(clipped)<=retained and set(extreme)<=retained,'Capacity selections belong to retained components')
    for group in proof.get('equal_core',[]):
        by=tuple(group['by']);m.need(by in retained and by[1]>=0 and group['nodes'],'Retained equal-core representative')
        power=4-len(fc.roots()[by[0]])-len(fc.children(by[0])[by[1]])
        m.need(power>=1,'Nonsingleton equal-core power')
        for child in group['nodes']:
            node=tuple(child);m.need(node in inventory and node not in seen and node[1]>=0,'Equal-core component inventory');seen.add(node)
            other_power=4-len(fc.roots()[node[0]])-len(fc.children(node[0])[node[1]])
            m.need(other_power==power,'Identical core-sum powers')
            gap=m.add((1,fc.interval(*node)[0]),(-1,fc.interval(*by)[0]))
            guards.extend([gap,{k:-v for k,v in gap.items()}])
    for group in groups:
        by=tuple(group['by']);m.need(by in retained and by[1]>=0 and group['nodes'],'Retained absorbing interval hull')
        m.need(4-len(fc.roots()[by[0]])-len(fc.children(by[0])[by[1]])>=1,'Nonsingleton absorbing interval')
        for child in group['nodes']:
            node=tuple(child);m.need(node in inventory and node not in seen,'Absorbed component inventory');seen.add(node)
            guards.extend(fc.subsumption(node,by))
    m.need(seen==inventory,'Every four-sum window component accounted for')
    parent={tuple(n):tuple(n) for n in proof['inside']}
    def find(n):
        while parent[n]!=n:n=parent[n]
        return n
    for pair in proof.get('core_edges',[]):
        m.need(exact_one and len(pair)==2,'Exact core-union edge')
        a,b=map(tuple,pair);m.need(a in parent and b in parent and a!=b,'Retained core-union edge vertices')
        m.need(a not in clipped and b not in clipped and a not in extreme and b not in extreme,'Full core sets for overlap subtraction')
        powers=[]
        for node in (a,b):
            m.need(node[1]>=0,'Refined core-sum translate')
            powers.append(4-len(fc.roots()[node[0]])-len(fc.children(node[0])[node[1]]))
        m.need(powers[0]==powers[1] and 1<=powers[0]<=4,'Same core-sum translate power');power=powers[0]
        aa,bb=find(a),find(b);m.need(aa!=bb,'Acyclic core-union overlap');parent[aa]=bb
        gap=m.add((1,fc.interval(*b)[0]),(-1,fc.interval(*a)[0]));guards.append({k:-v for k,v in gap.items()})
        body=m.add((1,body),(power,{'F':1}),(1-power,ONE),(-1,gap))
    for edge in proof.get('mixed_core_edges',[]):
        a,b=tuple(edge['small']),tuple(edge['large'])
        m.need(exact_one and a in parent and b in parent and a!=b,'Retained mixed core-union vertices')
        m.need(a not in clipped and b not in clipped and a not in extreme and b not in extreme,'Full sets for mixed overlap subtraction')
        gap=mixed_gap(a,b,edge['anchor'],edge['direction']);power=core_power(a)
        aa,bb=find(a),find(b);m.need(aa!=bb,'Acyclic joint same/mixed core forest');parent[aa]=bb
        guards.append(m.add((-1,gap)))
        body=m.add((1,body),(power,{'F':1}),(1-power,ONE),(-1,gap))
    return body,guards

def candidates(point,positive,coverage_width,bracket_width,affine_only=False,internal_only=False,extreme_gaps=False,shape=None):
    import math,bisect
    ev=lambda row:sum(c*point[k] for k,c in row.items())
    margin,holes=parameters(positive,coverage_width,bracket_width);missing=ev(holes)
    intervals=[];singletons=[];bounds={};original_intervals=[]
    for node in fc.leaves():
        a,b=fc.interval(*node);lo,hi=ev(a),ev(b)
        if any(m.add((1,a),(-1,b)).values()):
            original_intervals.append((lo,hi))
            if extreme_gaps:
                import core_gap
                left=core_gap.gap_interval(node,'t',shape)[1];right=core_gap.gap_interval(node,'s',shape)[0]
                if ev(left)>lo+1e-7:singletons.append(lo);a=m.add((1,left),(1,ONE));lo=ev(a)
                if ev(right)<hi-1e-7:singletons.append(hi);b=m.add((1,right),(-1,ONE));hi=ev(b)
            bounds[node]=(a,b)
            if lo<=hi+1e-7:intervals.append((lo,hi,node))
        else:singletons.append(lo)
    if not intervals:return []
    intervals.sort();singletons.sort();gaps=[];affine_gaps=[];end=intervals[0][1];endnode=intervals[0][2]
    for lo,hi,node in intervals:
        if lo>end+1+1e-7:
            gaps.append((end+1,lo-1));affine_gaps.append((end+1,lo-1,endnode,node))
        if hi>end:end=hi;endnode=node
    affine=[];internal=[]
    if not positive or coverage_width==1:
        order=sorted(range(8),key=lambda i:abs(ev(fc.outer()[i])))
        low=m.add((-1,{'St':1}),(margin,ONE));high=m.add((1,{'Ss':1}),(-margin,ONE))
        feasible=True
        for index in order:
            if abs(ev(fc.outer()[index]))>ev(high)-ev(low)+1+1e-7:feasible=False;break
            if index<4:high=m.add((1,high),(1,fc.outer()[index]))
            else:low=m.add((1,low),(1,fc.outer()[index]))
        if feasible:
            for a,b,left,right in affine_gaps:
                if extreme_gaps and not any(c<=b+1e-7 and d>=a-1e-7 for c,d in original_intervals):continue
                lower=m.add((1,bounds[left][1]),(1,ONE));upper=m.add((1,bounds[right][0]),(-1,ONE))
                if ev(low)>a:a=ev(low);lower=low
                if ev(high)<b:b=ev(high);upper=high
                count=bisect.bisect_right(singletons,b+1e-7)-bisect.bisect_left(singletons,a-1e-7)
                if b-a+1-count<=1e-7:continue
                affine.append((b-a+1-count,dict(mask=0,lower=lower,upper=upper,outer_extension=order,exact_one_term=True,refined=[],outside=[],inside=[])))
            # A lone translate of E can have holes inside its own hull.
            # Looking only between hulls misses this cardinality deficit.
            groups={}
            for a,b,node in intervals:
                groups.setdefault((round(a,6),round(b,6)),[]).append(node)
            for (a,b),nodes in groups.items():
                if extreme_gaps:continue
                if not all(n[1]>=0 and 4-len(fc.roots()[n[0]])-len(fc.children(n[0])[n[1]])==1 for n in nodes):continue
                if a<ev(low)-1e-7 or b>ev(high)+1e-7:continue
                if any((round(c,6),round(d,6))!=(a,b) and c<=b+1e-7 and d>=a-1e-7 for c,d,n in intervals):continue
                count=bisect.bisect_right(singletons,b+1e-7)-bisect.bisect_left(singletons,a-1e-7)
                if b-a+1-65-count<=1e-7:continue
                lower,upper=fc.interval(*nodes[0]);internal.append((b-a+1-65-count,dict(mask=0,lower=lower,upper=upper,outer_extension=order,exact_one_term=True,refined=[],outside=[],inside=[])))
    affine=sorted(affine,key=lambda q:-q[0])[:3]
    internal=sorted(internal,key=lambda q:-q[0])[:3]
    if internal_only:return internal
    if affine_only:return internal+affine
    result=[];used=set()
    for mask in range(256):
        base=ev(fc.shift(mask))-point['St']
        for lo,hi in gaps:
            a=max(margin,math.ceil(lo-base-1e-7));b=min(1331-margin,math.floor(hi-base+1e-7))
            if b<a:continue
            count=bisect.bisect_right(singletons,base+b+1e-7)-bisect.bisect_left(singletons,base+a-1e-7)
            excess=b-a+1-count-missing
            if excess<1e-7 or (mask,a,b) in used:continue
            used.add((mask,a,b));lower=m.add((1,fc.shift(mask)),(-1,{'St':1}),(a,ONE));upper=m.add((1,fc.shift(mask)),(-1,{'St':1}),(b,ONE))
            result.append((excess,dict(mask=mask,lower=lower,upper=upper,exact_one_term=True,refined=[],outside=[],inside=[])))
    chosen=sorted(result,key=lambda q:-q[0])[:3]
    broad=[]
    for mask in range(256):
        centre=fc.shift(mask);start=ev(centre)-point['St']+margin;end=ev(centre)+point['Ss']-margin
        lower=m.add((1,centre),(-1,{'St':1}),(margin,ONE));upper=m.add((1,centre),(1,{'Ss':1}),(-margin,ONE))
        for a,b,left,right in [(start,end,lower,upper),(start,ev(centre),lower,centre),(ev(centre),end,centre,upper)]:
            deficit=0
            for lo,hi in gaps:
                lo=max(lo,a);hi=min(hi,b)
                if hi<lo:continue
                count=bisect.bisect_right(singletons,hi+1e-7)-bisect.bisect_left(singletons,lo-1e-7)
                deficit+=max(0,hi-lo+1-count)
            if deficit>missing+1e-7:broad.append((deficit-missing,dict(mask=mask,lower=left,upper=right,exact_one_term=True,refined=[],outside=[],inside=[])))
    # One broad source window adds genuinely different coverage constraints;
    # the three short gap windows retain the inexpensive targeted search.
    if broad:chosen.append(max(broad,key=lambda q:q[0]))
    return internal+affine+chosen

def discover(search,point):
    from first_gap_core import shape_case
    shape=getattr(search,'core_shape',None)
    if shape is None:shape=shape_case(dict(j=search.j,positive=search.positive,limits=search.limits))
    ev=lambda row:sum(c*point[k] for k,c in row.items());margin,_=parameters(search.positive,search.coverage_width,search.coverage_bracket_width)
    extreme_gaps=getattr(search,'window_extreme_gaps',False)
    for score,proof in candidates(point,search.positive,search.coverage_width,search.coverage_bracket_width,getattr(search,'window_affine_only',False),getattr(search,'window_internal_only',False),extreme_gaps,shape):
        if shape is not None:proof['core_shape']=shape
        certificates=[]
        bracket_guards=proof_bracket(proof,search.positive,search.coverage_width,search.coverage_bracket_width)
        for guard in bracket_guards:
            cert,finished=search.nonstrict_guard(guard)
            if finished:return False,True
            if cert is None:break
            certificates.append(cert)
        if len(certificates)!=len(bracket_guards):continue
        queue=sorted(fc.initial_nodes());proof['gap_outside']=[];gap_certs=[];extreme_certs={};extreme_sides={}
        for node in queue:
            removed=False
            for direction in (0,1):
                guard=exclusion(proof['lower'],proof['upper'],node,direction)
                if ev(guard)>1e-7:continue
                cert,finished=search.nonstrict_guard(guard)
                if finished:return False,True
                if cert is None:continue
                proof['outside'].append(dict(node=node,direction=direction));certificates.append(cert);removed=True;break
            if removed:continue
            power=4-len(fc.roots()[node[0]])-(len(fc.children(node[0])[node[1]]) if node[1]>=0 else 0)
            if extreme_gaps and power>=1:
                import core_gap
                for side in 'st':
                    a,b=core_gap.gap_interval(node,side,shape if node[1]>=0 else None)
                    conditions=[m.add((1,a),(-1,proof['lower'])),m.add((1,proof['upper']),(-1,b))]
                    if any(ev(g)>1e-7 for g in conditions):continue
                    local=[]
                    for guard in conditions:
                        cert,finished=search.nonstrict_guard(guard)
                        if finished:return False,True
                        if cert is None:break
                        local.append(cert)
                    if len(local)==2:
                        proof['gap_outside'].append(dict(node=node,side=side));gap_certs.extend(local);removed=True;break
            if removed:continue
            if extreme_gaps and power>=1:
                for side in 'st':
                    guard=core_gap.extreme_only_guard(proof['lower'],proof['upper'],node,side,shape if node[1]>=0 else None)
                    if ev(guard)>1e-7:continue
                    cert,finished=search.nonstrict_guard(guard)
                    if finished:return False,True
                    if cert is None:continue
                    proof['inside'].append(node);extreme_certs[node]=cert;extreme_sides[node]=side;removed=True;break
            if removed:continue
            if node[1]==-1 and len(fc.roots()[node[0]])<4:
                proof['refined'].append(node[0]);queue.extend((node[0],i) for i in range(len(fc.children(node[0]))))
            else:proof['inside'].append(node)
        certificates.extend(gap_certs)
        # A charged interval hull may also cover other components. Mark
        # every absorbing core translate for full hull charge, rather than
        # incorrectly retaining its 65-point cardinality charge.
        live=set(map(tuple,proof['inside']));protected=set();proof['absorbed']=[];proof['equal_core']=[];equal_certs=[]
        groups={}
        for node in sorted(live):
            if node[1]<0:continue
            power=4-len(fc.roots()[node[0]])-len(fc.children(node[0])[node[1]])
            if power>=1:groups.setdefault((power,round(ev(fc.interval(*node)[0]),6)),[]).append(node)
        for nodes in groups.values():
            if len(nodes)<2:continue
            nodes.sort(key=lambda n:(n not in extreme_certs,n))
            by=nodes[0];chosen=[]
            for node in nodes[1:]:
                gap=m.add((1,fc.interval(*node)[0]),(-1,fc.interval(*by)[0]));local=[]
                for guard in (gap,{k:-v for k,v in gap.items()}):
                    cert,finished=search.nonstrict_guard(guard)
                    if finished:return False,True
                    if cert is None:break
                    local.append(cert)
                if len(local)==2:chosen.append(node);equal_certs.extend(local)
            if chosen:live.difference_update(chosen);protected.add(by);proof['equal_core'].append(dict(by=by,nodes=chosen))
        mass_core=set()
        for node in live:
            power=4-len(fc.roots()[node[0]])-(len(fc.children(node[0])[node[1]]) if node[1]>=0 else 0)
            lo,hi=fc.interval(*node)
            if node not in extreme_certs and node[1]>=0 and 2<=power<=4 and ev(core_capacity(power,shape))<ev(hi)-ev(lo)+1-1e-7:mass_core.add(node)
        def charge(node):
            if node in extreme_certs:return 1
            lo,hi=fc.interval(*node)
            power=4-len(fc.roots()[node[0]])-(len(fc.children(node[0])[node[1]]) if node[1]>=0 else 0)
            if node in mass_core:return ev(core_capacity(power,shape))
            return 65 if node[1]>=0 and power==1 else ev(hi)-ev(lo)+1
        absorbed_certs=[]
        absorbers=sorted((n for n in live if n not in extreme_certs and n[1]>=0 and ev(fc.interval(*n)[1])-ev(fc.interval(*n)[0])>1e-7),key=lambda n:ev(fc.interval(*n)[0])-ev(fc.interval(*n)[1]))
        for by in absorbers:
            if by not in live:continue
            lo,hi=fc.interval(*by);penalty=ev(hi)-ev(lo)+1-charge(by)
            possible=[n for n in live-protected-{by} if fc.terminal(n) and all(ev(g)<=1e-7 for g in fc.subsumption(n,by))]
            if sum(charge(n) for n in possible)<=penalty+1e-7:continue
            chosen=[];local=[]
            for node in sorted(possible):
                certs=[]
                for guard in fc.subsumption(node,by):
                    cert,finished=search.nonstrict_guard(guard)
                    if finished:return False,True
                    if cert is None:break
                    certs.append(cert)
                if len(certs)==2:chosen.append(node);local.extend(certs)
            if sum(charge(n) for n in chosen)<=penalty+1e-7:continue
            live.difference_update(chosen);protected.add(by);proof['absorbed'].append(dict(by=by,nodes=chosen));absorbed_certs.extend(local)
            mass_core.difference_update([by,*chosen])
        proof['inside']=sorted(live)
        proof['extreme_only']=[dict(node=n,side=extreme_sides[n]) for n in proof['inside'] if n in extreme_certs]
        proof['clipped']=[];clipped=set()
        for node in proof['inside']:
            if node in extreme_certs:certificates.append(extreme_certs[node]);continue
            if node in protected:continue
            lo,hi=fc.interval(*node);left=int(ev(proof['lower'])>ev(lo));right=int(ev(proof['upper'])<ev(hi))
            a=proof['lower'] if left else lo;b=proof['upper'] if right else hi
            if ev(b)-ev(a)+1>=charge(node)-1e-7:continue
            guard=m.add((1,a),(-1,b),(-1,ONE));cert,finished=search.nonstrict_guard(guard)
            if finished:return False,True
            if cert is None:continue
            proof['clipped'].append(dict(node=node,left=left,right=right));clipped.add(node);certificates.append(cert);mass_core.discard(node)
        proof['mass_core']=sorted(mass_core);certificates.extend(equal_certs);certificates.extend(absorbed_certs)
        proof['core_edges']=[]
        for power in range(1,5):
            core_nodes=sorted((tuple(n) for n in proof['inside'] if tuple(n) not in clipped and tuple(n) not in extreme_certs and n[1]>=0 and 4-len(fc.roots()[n[0]])-len(fc.children(n[0])[n[1]])==power),key=lambda n:ev(fc.interval(*n)[0]))
            for a,b in zip(core_nodes,core_nodes[1:]):
                gap=m.add((1,fc.interval(*b)[0]),(-1,fc.interval(*a)[0]))
                if ev(gap)>=power*point['F']-power+1-1e-7:continue
                cert,finished=search.nonstrict_guard({k:-v for k,v in gap.items()})
                if finished:return False,True
                if cert is None:continue
                proof['core_edges'].append((a,b));certificates.append(cert)
        # A pE translate overlaps a qE translate through any of the latter's
        # contained pE translates (p<q), using actual endpoint/zero anchors.
        parent={tuple(n):tuple(n) for n in proof['inside']}
        def find(node):
            while parent[node]!=node:node=parent[node]
            return node
        for a,b in proof['core_edges']:parent[find(a)]=find(b)
        eligible=[n for n in sorted(parent) if n not in clipped and n not in extreme_certs and n[1]>=0 and core_power(n)>=1]
        options=[]
        for a in eligible:
            p=core_power(a)
            for b in eligible:
                q=core_power(b)
                if q<=p:continue
                choices=[]
                for i in range(q-p+1):
                    for j in range(q-p+1-i):
                        gap=mixed_gap(a,b,(i,j),1);distance=ev(gap);direction=1 if distance>=0 else -1
                        rebate=p*point['F']-p+1-abs(distance)
                        if rebate>1e-7:choices.append((rebate,i,j,direction))
                if choices:
                    rebate,i,j,direction=max(choices);options.append((rebate,a,b,i,j,direction))
        proof['mixed_core_edges']=[]
        for rebate,a,b,i,j,direction in sorted(options,reverse=True):
            if find(a)==find(b):continue
            gap=mixed_gap(a,b,(i,j),direction);cert,finished=search.nonstrict_guard(m.add((-1,gap)))
            if finished:return False,True
            if cert is None:continue
            parent[find(a)]=find(b)
            proof['mixed_core_edges'].append(dict(small=a,large=b,anchor=[i,j],direction=direction));certificates.append(cert)
        row,guards=derive(proof,search.positive,search.coverage_width,search.coverage_bracket_width,shape)
        if ev(row)<=1e-7:continue
        from math import gcd
        def row_key(body,bound=0):
            body=m.add((1,body),(-bound,ONE));factor=gcd(*(abs(v) for v in body.values())) or 1
            return tuple(sorted((k,v//factor) for k,v in body.items() if v))
        key=row_key(row)
        if any(row_key(body,bound)==key for body,bound,_ in search.rows):continue
        # The search may add other consequences while proving the guards;
        # all certificate row indices refer to their unchanged row prefixes.
        for cert,guard in zip(certificates,guards):
            import exact
            exact.check(cert,search.rows,search.eqs,guard,strict=False)
        search.trace.append(dict(kind='full_window_capacity',proof=proof,certificates=certificates))
        search.rows.append((row,0,'complete four-sum window capacity'))
        return True,False
    return False,False


def add_probe(search,point):
    """Use a new affine window endpoint as an exact integer subset-sum target."""
    used={tuple(sorted((k,v) for k,v in p['target'].items() if v)) for p in search.full_probes}
    for _,window in candidates(point,search.positive,search.coverage_width,search.coverage_bracket_width,True):
        for target in (window['lower'],window['upper']):
            key=tuple(sorted((k,v) for k,v in target.items() if v))
            if key in used:continue
            proof=dict(mask=0,lower=target,upper=target,outer_extension=window['outer_extension'])
            guards=proof_bracket(proof,search.positive,search.coverage_width,search.coverage_bracket_width);certificates=[]
            for guard in guards:
                cert,finished=search.nonstrict_guard(guard)
                if finished:return False,True
                if cert is None:break
                certificates.append(cert)
            if len(certificates)!=len(guards):continue
            search.trace.append(dict(kind='full_cover_extended_probe',proof=proof,certificates=certificates))
            search.rows.extend((g,0,'proved full target bracket') for g in guards)
            search.full_probes.append(dict(target=target,mask=0,width=1,margin=0,nodes=fc.initial_nodes(),forced=False))
            return True,False
    return False,False
