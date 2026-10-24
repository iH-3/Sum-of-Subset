# RESEARCH PROTOTYPE: no global bound is certified by this file.
"""Optional SciPy search. Every saved step is reconstructed and checked exactly."""
from fractions import Fraction
from math import lcm,gcd
from pathlib import Path
import sys,json,time
import numpy as np
from scipy.optimize import linprog
from scipy.spatial import ConvexHull
from functools import lru_cache
import model as m
import parametric as p
import exact

@lru_cache(None)
def planes(rank,j,I,e,lo,hi,minimum_tau=0):
    cap=496-73*j-I;hi=min(hi,cap-e-minimum_tau);points=[]
    for k in range(lo,min(hi,cap-e-minimum_tau)+1):
        for delta,tau in ((e+k,minimum_tau),(cap-minimum_tau,minimum_tau),(e+k,cap-e-k)):
            error=(Fraction(0) if k<=68-rank else Fraction(tau,69-k)) if k<69 else Fraction(651-73*j-I-delta)
            points.append((k,delta,tau,error))
    if not points:return []
    if lo==hi:
        if lo>=69:return [(0,1,0,1,651-73*j-I)]
        if lo<=68-rank:return [(0,0,0,1,0)]
        return [(0,0,-1,69-lo,0)]
    hull=ConvexHull(np.array(points,float),qhull_options='QJ');answer=set()
    # Recover the exact supporting hyperplane from each simplex. Qhull's
    # perturbed floating normals otherwise create hundreds of almost equal
    # weak planes even when the exact upper face is simply error <= 0.
    def determinant(matrix):
        if len(matrix)==1:return matrix[0][0]
        return sum((-1)**i*v*determinant([row[:i]+row[i+1:] for row in matrix[1:]])
                   for i,v in enumerate(matrix[0]) if v)
    for simplex,eq in zip(hull.simplices,hull.equations):
        if eq[3]<1e-7:continue
        matrix=[]
        for index in simplex:
            values=(*points[index],-1);den=lcm(*(Fraction(v).denominator for v in values))
            matrix.append([int(v*den) for v in values])
        coeff=[(-1)**i*determinant([row[:i]+row[i+1:] for row in matrix]) for i in range(5)]
        if not coeff[3]:continue
        if coeff[3]<0:coeff=[-c for c in coeff]
        common=gcd(*coeff);coeff=tuple(c//common for c in coeff)
        if any(sum(c*v for c,v in zip(coeff[:4],pt))>coeff[4] for pt in points):continue
        answer.add(coeff)
    return sorted(answer)


def guard_key(row):
    pairs=sorted((k,int(v)) for k,v in row.items() if v)
    factor=gcd(*(abs(v) for _,v in pairs)) if pairs else 1
    return tuple((k,v//factor) for k,v in pairs)


class Search:
    def __init__(self,st,j,positive=False,limits=None,use_planes=False,parent=None):
        self.st=st;self.j=j;self.positive=positive;self.limits=limits
        self.parent=parent
        self.known_nonpositive=set()
        self.guard_certificate_cache={};self.guard_failure_cache={}
        prior=exact.inherited(dict(st=st,j=j,positive=positive,limits=limits,premise=parent)) if parent else None
        self.initial=8 if m.is_ownerless(st) else 0
        self.e=prior['credit'] if prior else self.initial
        self.use_planes=use_planes;p.USE_PLANES=use_planes;p.PLANE_GENERATOR=planes;p.SOURCE_TAIL_RANKS=True;p.SHARP_PLANES=True;p.SIDE_PLANES=True;p.TRIM_SOURCE=True;p.POINT_OVERLAP=True;p.FULL_EDGES=True
        p.PLANE_TABLE=dict(p.PLANE_TABLE)
        p.USED_PLANES=set();self.plane_keys=p.USED_PLANES
        self.names,self.rows,self.eqs=p.build(st,j,positive,self.e,limits)
        self.edges=p.build.last_edges;self.ret=p.build.last_retained
        self.trace=[];self.low=set();self.high=set();self.cuts=set();self.calls=0;self.constants=dict(p.build.last_compression);self.alpha_done=False;self.alpha_tail_done=False;self.ownerless_done=False;self.point_hits={};self.point_groups={};self.extended_hits={};self.leading_hits={};self.leading_extended={};self.sumset_excluded={key:set(tuple(pair) for pair in pairs) for key,pairs in prior.get('sumset_excluded',{}).items()} if prior else {};self.trim_pairs=set(tuple(x) for x in prior.get('trim_pairs',[])) if prior else set()
        self.sumset_equalities={key:list(values) for key,values in prior.get('sumset_equalities',{}).items()} if prior else {}
        self.covered=set(prior.get('covered',[])) if prior else set()
        self.covered_positive=set(prior.get('covered_positive',[])) if prior else set()
        self.fixed_pairs={tuple(pair) for pair in prior.get('fixed_pairs',[])} if prior else set()
        self.coverage_probes={key:dict(excluded=set(value['excluded']),forced=bool(value.get('forced'))) for key,value in prior.get('coverage_probes',{}).items()} if prior else {}
        self.coverage_width=prior.get('coverage_width',8 if positive else 1) if prior else (8 if positive else 1)
        self.coverage_bracket_width=prior.get('coverage_bracket_width',self.coverage_width) if prior else self.coverage_width
        import full_cover
        self.full_probes=full_cover.copy_probes(prior.get('full_probes',[])) if prior else []
        self.core_tail_excluded={side:set(values) for side,values in prior.get('core_tail_excluded',{}).items()} if prior else {}
        self.ordered_cover={side:dict(order=list(value['order']),excluded=set(value['excluded'])) for side,value in prior.get('ordered_cover',{}).items()} if prior else {}
        self.Z=p.build.last_Z;self.tail_low={'s':set(),'t':set()};self.tail_counts={'s':0,'t':0};self.tail_pairs={'s':set(),'t':set()}
        if prior:
            self.low=set(prior['low']);self.high=set(prior['high']);self.rows.extend(prior['facts'])
            self.tail_low={s:set(prior['tail_low'][s]) for s in 'st'};self.tail_counts=dict(prior['tail_counts']);self.tail_pairs={s:set(prior['tail_pairs'][s]) for s in 'st'}
            for a,b,gap,value in prior['constants']:
                matches=[i for i,(aa,bb,gg) in enumerate(self.edges) if (a,b,gap)==(aa,bb,gg)]
                m.need(len(matches)==1,'Inherited search edge changed');i=matches[0]
                self.constants[i]=max(self.constants.get(i,0),value)
        if prior:
            for a,b,gap,tags in prior.get('point_hits',[]):
                matches=[i for i,(aa,bb,gg) in enumerate(self.edges) if (a,b,gap)==(aa,bb,gg)]
                m.need(len(matches)==1,'Inherited point edge');self.point_hits[matches[0]]=set(tags)
        if prior:
            for a,b,gap,groups in prior.get('point_groups',[]):
                matches=[i for i,(aa,bb,gg) in enumerate(self.edges) if (a,b,gap)==(aa,bb,gg)]
                m.need(len(matches)==1,'Inherited point group edge');self.point_groups[matches[0]]={tuple(tags):count for tags,count in groups}
        if prior:
            for a,b,gap,groups in prior.get('extended_hits',[]):
                matches=[i for i,(aa,bb,gg) in enumerate(self.edges) if (a,b,gap)==(aa,bb,gg)]
                m.need(len(matches)==1,'Inherited extended search edge');self.extended_hits[matches[0]]={int(q):set(tags) for q,tags in groups}
        if prior:
            for a,b,gap,tags in prior.get('leading_hits',[]):
                matches=[i for i,(aa,bb,gg) in enumerate(self.edges) if (a,b,gap)==(aa,bb,gg)]
                m.need(len(matches)==1,'Inherited leading search edge');self.leading_hits[matches[0]]=set(tags)
        if prior:
            for a,b,gap,groups in prior.get('leading_extended',[]):
                matches=[i for i,(aa,bb,gg) in enumerate(self.edges) if (a,b,gap)==(aa,bb,gg)]
                m.need(len(matches)==1,'Inherited extended leading search edge');self.leading_extended[matches[0]]={int(q):set(tags) for q,tags in groups}
        for side in 'st':
            lower=(limits or {}).get('B'+side,(4,10))[0]
            if lower>=5:
                self.rows.extend(exact.quartet_rows(side,lower));self.trace.append(dict(kind='quartet_fringe',side=side,lower=lower))

        self.rows.extend(exact.core_mass_ceiling(self.limits));self.trace.append(dict(kind='core_mass_ceiling'))
        self.rows.extend(exact.source_maximum_overlap_rows());self.trace.append(dict(kind='source_maximum_overlap'))
        self.rows.extend(exact.source_gap_inventory_rows());self.trace.append(dict(kind='source_gap_inventory'))
        self.rows.append(exact.trim_hull_row(len(self.trim_pairs)));self.trace.append(dict(kind='source_trim_hull'))

    def matrices(self):
        names=self.names
        self.A=np.array([[row.get(k,0) for k in names] for row,_,_ in self.rows],float)
        self.b=np.array([b for _,b,_ in self.rows],float)
        self.E=np.array([[row.get(k,0) for k in names] for row,_,_ in self.eqs],float)
        self.f=np.array([b for _,b,_ in self.eqs],float)
        self.rsi=[max([1,*[abs(v) for v in row.values()]]) for row,_,_ in self.rows]
        self.esi=[max([1,*[abs(v) for v in row.values()]]) for row,_,_ in self.eqs]
        self.rs=np.array(self.rsi,float);self.es=np.array(self.esi,float)
        self.A/=self.rs[:,None];self.b/=self.rs;self.E/=self.es[:,None];self.f/=self.es

    def reconstruct(self,result,target=None,strict=True,phase=False):
        ww=[('r',i,-float(w),scale) for i,(w,scale) in enumerate(zip(result.ineqlin.marginals,self.rsi))]
        ww += [('e',i,-float(w),scale) for i,(w,scale) in enumerate(zip(result.eqlin.marginals,self.esi))]
        for bound in (1000,100000,10000000,1000000000):
            fr=[(kind,i,Fraction(w).limit_denominator(bound)/scale) for kind,i,w,scale in ww if abs(w)>1e-12]
            den=lcm(*(x.denominator for _,_,x in fr))
            weights=[(kind,i,int(x*den)) for kind,i,x in fr if x]
            divisor=gcd(*[abs(x) for _,_,x in weights],*([] if target is None else [den]))
            cert={'weights':[(kind,i,x//divisor) for kind,i,x in weights], 'denominator':None if target is None else den//divisor}
            try:exact.check(cert,self.rows,self.eqs,target,strict)
            except ValueError:continue
            return cert
        # Recover the supported dual face by exact rational elimination.
        # This path remains discovery-only: the saved integer combination is
        # subjected to the same independent standard-library check.
        support=[(kind,i) for kind,i,w,scale in ww if abs(w)>1e-10]
        coefficients=[];right=[]
        for pos,name in enumerate(self.names):
            if abs(result.lower.marginals[pos])>1e-7:continue
            coefficients.append([(self.rows if kind=='r' else self.eqs)[i][0].get(name,0) for kind,i in support])
            right.append(0 if target is None else target.get(name,0))
        if target is None:
            actual={(kind,i):w/scale for kind,i,w,scale in ww}
            first=max((i for i,(kind,_) in enumerate(support) if kind=='r'),key=lambda i:actual[support[i]],default=None)
            if first is None:return None
            coefficients.append([int(i==first) for i in range(len(support))]);right.append(1)
        try:
            nvars=len(support)
            matrix=[list(vals)+[rhs] for vals,rhs in zip(coefficients,right)]
            pivots=[];rank=0;previous=1
            # Fraction-free Bareiss elimination avoids a gcd at every inner
            # arithmetic operation. Every division is checked for exactness.
            for col in range(nvars):
                pivot=next((i for i in range(rank,len(matrix)) if matrix[i][col]),None)
                if pivot is None:continue
                matrix[rank],matrix[pivot]=matrix[pivot],matrix[rank]
                lead=matrix[rank][col]
                for i in range(rank+1,len(matrix)):
                    multiplier=matrix[i][col]
                    for jj in range(col+1,nvars+1):
                        value=lead*matrix[i][jj]-multiplier*matrix[rank][jj]
                        quotient,remainder=divmod(value,previous)
                        if remainder:raise ValueError('nonintegral Bareiss division')
                        matrix[i][jj]=quotient
                    matrix[i][col]=0
                pivots.append((rank,col));rank+=1;previous=lead
            if any(not any(row[:nvars]) and row[-1] for row in matrix):
                raise ValueError('inconsistent supported dual face')
            actual={(kind,i):w/scale for kind,i,w,scale in ww}
            normal=actual[support[first]] if target is None else 1
            pivot_cols={col for _,col in pivots}
            for precision in (1000,1000000,1000000000,None):
                solution=[Fraction(0) if col in pivot_cols or precision is None else Fraction(actual[support[col]]/normal).limit_denominator(precision) for col in range(nvars)]
                for row,col in reversed(pivots):
                    rhs=Fraction(matrix[row][-1])-sum(matrix[row][i]*solution[i] for i in range(col+1,nvars))
                    solution[col]=rhs/matrix[row][col]
                den=lcm(*(v.denominator for v in solution))
                cert={'weights':[(kind,i,int(v*den)) for (kind,i),v in zip(support,solution) if v],
                      'denominator':None if target is None else den}
                try:exact.check(cert,self.rows,self.eqs,target,strict)
                except ValueError:continue
                return cert
        except (ValueError,StopIteration,AttributeError):pass
        return None

    def cut(self,x):
        parent={v:v for v in ['root','Ls','Lt',*self.ret]};parent['Ls']=parent['Lt']='root'
        def find(v):
            while parent[v]!=v:v=parent[v]
            return v
        weights={i:max(x['FD'],self.constants.get(i,0))-sum(c*x[k] for k,c in gap.items()) for i,(_,_,gap) in enumerate(self.edges)}
        counts={i:exact.edge_point_count(self.edges[i],self.point_hits.get(i,set()),self.point_groups.get(i,{}),self.extended_hits.get(i,{}),self.leading_hits.get(i,set()),self.leading_extended.get(i,{})) for i in weights}
        point_edges={i:counts[i] for i in weights if counts[i]>max(0,weights[i])+1e-7}
        cand=[(point_edges.get(i,weights[i]),i,a,b) for i,(a,b,gap) in enumerate(self.edges)]
        cand += [(x['D'+v],-1,'root',v) for v in self.ret]
        chosen=[];roots=[]
        for weight,i,a,b in sorted(cand,reverse=True):
            aa,bb=find(a),find(b)
            if aa==bb:continue
            parent[aa]=bb
            if i<0:roots.append(b)
            else:chosen.append(i)
        chosen.sort();roots.sort();point_edges={i:n for i,n in point_edges.items() if i in chosen};constants={i:self.constants[i] for i in chosen if i not in point_edges and self.constants.get(i,0)>x['FD']+1e-7}
        key=(tuple(chosen),tuple(roots),self.e,tuple(sorted(constants.items())),tuple(sorted(point_edges.items())))
        row=exact.forest(self.edges,self.ret,chosen,roots,self.e,constants,point_edges)
        if key in self.cuts or sum(c*x[k] for k,c in row[0].items())<=row[1]+1e-7:return self.sumset_gap_cut(x)
        self.rows.append(row);self.cuts.add(key)
        self.trace.append(dict(kind='forest',edges=chosen,roots=roots,e=self.e,constants=constants,point_edges=point_edges))
        return True

    def sumset_gap_cut(self,x):
        for capped in (False,True):
            gaps=[]
            for key in exact.SUMSET_GAPS:
                if key[0].isupper()!=capped:continue
                side,other,lower,upper,qs,qo=exact.sumset_gap_data(key)
                length=m.add((1,upper),(-1,lower),(-1,qs),(-1,qo),(-1,{'ONE':1}))
                rebate=sum(c*x[k] for k,c in length.items())-exact.sumset_gap_remaining(key,self.sumset_excluded.get(key,set()),self.sumset_equalities.get(key,()))
                if rebate>1e-7:gaps.append(key)
            if not gaps:continue
            row=exact.sumset_gap_capacity(gaps,self.sumset_excluded,len(self.trim_pairs),self.sumset_equalities)
            stamp=('sumset_gaps',tuple(gaps),len(self.trim_pairs),tuple(exact.sumset_gap_remaining(key,self.sumset_excluded.get(key,set()),self.sumset_equalities.get(key,())) for key in gaps))
            if stamp in self.cuts or sum(c*x[k] for k,c in row[0].items())<=row[1]+1e-7:continue
            self.rows.append(row);self.cuts.add(stamp);self.trace.append(dict(kind='sumset_gap_capacity',gaps=gaps));return True
        return False

    def lp(self,target=None):
        for iteration in range(100):
            self.matrices();self.calls+=1
            c=np.array([-target.get(k,0) for k in self.names],float) if target else np.zeros(len(self.names))
            rr=linprog(c,A_ub=self.A,b_ub=self.b,A_eq=self.E,b_eq=self.f,bounds=(0,None),method='highs')
            if rr.status!=0:return rr
            if not self.cut(dict(zip(self.names,rr.x))):
                if target and rr.fun>=-1e-8:self.known_nonpositive.add(guard_key(target))
                return rr
        raise ValueError('Forest separation did not settle')

    def final(self):
        weights=[]
        def last(label):return max(i for i,(_,_,lab) in enumerate(self.rows) if lab==label)
        try:
            weights.append(('r',last('budget'),1))
            native=last('proved fixed credit') if any(lab=='proved fixed credit' for _,_,lab in self.rows) else last('native total')
            weights.append(('r',native,2//(-self.rows[native][0]['delta'])))
            for i,(_,_,label) in enumerate(self.rows):
                if label.startswith('native loss ') or label.startswith('clip branch lower '):weights.append(('r',i,1))
            if self.positive:
                weights += [('r',last('positive core floor'),1),('r',last('parameter positive holes'),4)]
            else:
                ei=next(i for i,(_,_,label) in enumerate(self.eqs) if label=='parameter zero holes')
                weights.append(('e',ei,4))
            cert={'weights':weights,'denominator':None};exact.check(cert,self.rows,self.eqs)
            self.trace.append(dict(kind='final',certificate=cert));return True
        except (ValueError,StopIteration,KeyError):pass
        self.matrices();n=len(self.names)
        rr=linprog(np.r_[np.zeros(n),1],A_ub=np.c_[self.A,-np.ones(len(self.rows))],b_ub=self.b,
                   A_eq=np.c_[self.E,np.zeros(len(self.eqs))],b_eq=self.f,bounds=(0,None),method='highs')
        if not rr.success or rr.fun<=1e-9:raise ValueError('Phase I failed: '+str(rr.message))
        cert=self.reconstruct(rr)
        if cert is None:
            # A second, independently optimized dual normalization often
            # avoids a numerically degenerate phase-I supported face.
            from types import SimpleNamespace
            nr,ne=len(self.rows),len(self.eqs)
            coeff=np.c_[self.A.T,self.E.T,-self.E.T]
            dual=linprog(np.r_[self.b,self.f,-self.f],A_ub=-coeff,b_ub=np.zeros(n),
                         A_eq=np.ones((1,nr+2*ne)),b_eq=[1],bounds=(0,None),method='highs')
            if dual.success and dual.fun<-1e-9:
                y=dual.x[:nr];z=dual.x[nr:nr+ne]-dual.x[nr+ne:]
                fake=SimpleNamespace(ineqlin=SimpleNamespace(marginals=-y),eqlin=SimpleNamespace(marginals=-z),
                                     lower=SimpleNamespace(marginals=coeff@dual.x))
                cert=self.reconstruct(fake)
        if cert is None:raise ValueError('Exact contradiction reconstruction failed')
        self.trace.append(dict(kind='final',certificate=cert));return True

    def guard_index(self):
        if not hasattr(self,'_guard_seen'):
            self._guard_seen=0;self._guard_epoch=0;self._guard_direct={}
            self._guard_unit=next(i for i,(row,rhs,_) in enumerate(self.eqs) if {k:v for k,v in row.items() if v}=={'ONE':1} and rhs==1)
            for i,(row,rhs,_) in enumerate(self.eqs):
                affine=m.add((1,row),(-rhs,{'ONE':1}));factor=gcd(*(abs(v) for v in affine.values())) or 1
                if not any(affine.values()):continue
                for sign in (1,-1):
                    key=guard_key({k:sign*v for k,v in affine.items()})
                    self._guard_direct.setdefault(key,('e',i,sign,factor,rhs))
        redundant={'proved core-tail license','proved core-tail exclusion','proved known-union guard','proved target probe bracket','proved target component exclusion','proved fixed conflict','proved fixed probe conflict',
                   'proved fixed source cover','proved covered fixed positive','proved trimmed hull pair','proved source gap pair outside',
                   'proved source pair equality','proved leading exterior hit','proved extended interval hit','proved point overlap interval'}
        for i in range(self._guard_seen,len(self.rows)):
            row,rhs,label=self.rows[i]
            if label not in redundant and not label.startswith(('proved LOW ','proved tail LOW ','proved tail incompatible ')):self._guard_epoch+=1
            affine=m.add((1,row),(-rhs,{'ONE':1}));factor=gcd(*(abs(v) for v in affine.values())) or 1
            if any(affine.values()):self._guard_direct.setdefault(guard_key(affine),('r',i,1,factor,rhs))
        self._guard_seen=len(self.rows)
        return self._guard_epoch

    def nonstrict_guard(self,guard):
        key=tuple(sorted((k,v) for k,v in guard.items() if v));normalized=guard_key(guard)
        if key in self.guard_certificate_cache:
            self.known_nonpositive.add(normalized);return self.guard_certificate_cache[key],False
        if all(v<=0 for v in guard.values()):
            cert={'weights':[],'denominator':1};exact.check(cert,self.rows,self.eqs,guard,strict=False)
            self.guard_certificate_cache[key]=cert;self.known_nonpositive.add(normalized);return cert,False
        epoch=self.guard_index()
        if normalized in self._guard_direct:
            kind,i,sign,factor,rhs=self._guard_direct[normalized];target_factor=gcd(*(abs(v) for v in guard.values())) or 1
            weights=[(kind,i,sign*target_factor)]
            if rhs:weights.append(('e',self._guard_unit,-rhs*sign*target_factor))
            cert={'weights':weights,'denominator':factor};exact.check(cert,self.rows,self.eqs,guard,strict=False)
            self.guard_certificate_cache[key]=cert;self.known_nonpositive.add(normalized);return cert,False
        if self.guard_failure_cache.get(key)==epoch:return None,False
        rr=self.lp(guard)
        if rr.status==2:return None,True
        epoch=self.guard_index()
        if rr.status==0 and -1+1e-7<rr.fun<-1e-7 and self.j>=3 and 3 not in self.st.values():
            from modular import INTEGER_NAMES
            if set(k for k,v in guard.items() if v)<=INTEGER_NAMES and all(type(v) is int for v in guard.values()):
                from types import SimpleNamespace
                marginal=np.array(rr.eqlin.marginals,copy=True)
                marginal[self._guard_unit]+=self.esi[self._guard_unit]
                shifted=SimpleNamespace(ineqlin=rr.ineqlin,eqlin=SimpleNamespace(marginals=marginal),lower=rr.lower)
                strict_target=m.add((1,guard),(-1,{'ONE':1}))
                strict_certificate=self.reconstruct(shifted,strict_target,strict=True)
                if strict_certificate is not None:
                    self.trace.append(dict(kind='integer_guard',guard=guard,certificate=strict_certificate))
                    index=len(self.rows);self.rows.append((guard,0,'rounded integer guard'))
                    cert={'weights':[('r',index,1)],'denominator':1}
                    self.guard_certificate_cache[key]=cert;self.known_nonpositive.add(normalized);return cert,False
        if rr.status!=0 or rr.fun<-1e-7:
            self.guard_failure_cache[key]=epoch;return None,False
        cert=self.reconstruct(rr,guard,strict=False)
        if cert is not None:self.guard_certificate_cache[key]=cert
        else:self.guard_failure_cache[key]=epoch
        return cert,False

    def coverage_gap(self,point):
        if not self.coverage_probes:return False
        import cover_geometry as coverage
        width=self.coverage_width;ev=lambda row:sum(c*point[k] for k,c in row.items())
        for key in self.coverage_probes:
            side,index=key.split(':');components=coverage.catalogue(self.st,self.Z,side);target=ev(coverage.probe(components,int(index)))
            if all(max(ev(lo)-target-width+1,target-ev(hi),0)>1e-7 for _,lo,hi in components):return True
        return False

    def coverage_step(self,point):
        if self.j<3 or 3 in self.st.values():return False,False
        import cover_geometry as coverage
        width=self.coverage_width
        catalogues={side:coverage.catalogue(self.st,self.Z,side) for side in 'st'}
        ev=lambda row:sum(c*point[k] for k,c in row.items())
        if len(self.coverage_probes)<64 and not self.coverage_gap(point):
            candidates=[]
            for side,components in catalogues.items():
                for index,(name,lo,hi) in enumerate(components):
                    key=side+':'+str(index)
                    if key in self.coverage_probes:continue
                    target=ev(coverage.probe(components,index))
                    if not 1-1e-7<=target<=point['S'+side]-self.coverage_bracket_width+1+1e-7:continue
                    distance=min(max(ev(a)-target-width+1,target-ev(b),0) for _,a,b in components)
                    if distance>1e-7:candidates.append((distance,int(lo!=hi),side,index))
            for _,_,side,index in sorted(candidates,reverse=True)[:6]:
                guards=coverage.bracket(catalogues[side],side,index,self.coverage_bracket_width);certificates=[]
                for guard in guards:
                    cert,infeasible=self.nonstrict_guard(guard)
                    if infeasible:return False,True
                    if cert is None:break
                    certificates.append(cert)
                if len(certificates)!=2:continue
                self.trace.append(dict(kind='coverage_probe',side=side,probe=index,certificates=certificates))
                for guard in guards:self.rows.append((guard,0,'proved target probe bracket'))
                self.coverage_probes[side+':'+str(index)]=dict(excluded=set(),forced=False)
                break
        changed=False
        from modular import Basis
        integer_basis=Basis(self.rows,self.eqs) if width==1 else None
        for key,state in self.coverage_probes.items():
            side,index=key.split(':');index=int(index);components=catalogues[side]
            for component in range(len(components)):
                if component in state['excluded']:continue
                _,lo,hi=components[component]
                if integer_basis is not None and lo==hi:
                    target=m.add((1,lo),(-1,coverage.probe(components,index)))
                    certificate=integer_basis.exclude(target)
                    if certificate is not None:
                        import modular
                        modular.check(certificate,self.rows,self.eqs,target)
                        self.trace.append(dict(kind='coverage_modular_exclude',side=side,probe=index,component=component,certificate=certificate))
                        state['excluded'].add(component);changed=True;continue
                options=sorted((ev(coverage.exclusion(components,index,component,direction,width)),direction) for direction in (0,1))
                for value,direction in options:
                    if value>1e-7:continue
                    guard=coverage.exclusion(components,index,component,direction,width);cert,infeasible=self.nonstrict_guard(guard)
                    if infeasible:return False,True
                    if cert is None:continue
                    self.trace.append(dict(kind='coverage_exclude',side=side,probe=index,component=component,direction=direction,certificate=cert))
                    self.rows.append((guard,0,'proved target component exclusion'));state['excluded'].add(component);changed=True;break
            remaining=set(range(len(components)))-state['excluded']
            if not remaining:
                self.trace.append(dict(kind='coverage_final',side=side,probe=index));return True,True
            if len(remaining)==1 and not state['forced']:
                component=next(iter(remaining));self.trace.append(dict(kind='coverage_force',side=side,probe=index,component=component))
                for guard in coverage.containment(components,index,component,width):self.rows.append((guard,0,'required target component'))
                state['forced']=True;changed=True
        return changed,False

    def full_cover_step(self,point):
        if self.j<3 or 3 in self.st.values():return False,False
        import full_cover as fc
        from modular import INTEGER_NAMES
        self.full_cover_failures=[]
        ev=lambda row:sum(c*point[k] for k,c in row.items())
        width,margin=fc.profile(self.positive,self.coverage_width,self.coverage_bracket_width)
        changed=False
        gap=any(all(max(ev(fc.interval(*node)[0])-ev(q['target'])-q['width']+1,
                           ev(q['target'])-ev(fc.interval(*node)[1]),0)>1e-7
                       for node in q['nodes']) for q in self.full_probes)
        if len(self.full_probes)<4 and not gap:
            used={(tuple(sorted((k,c) for k,c in q['target'].items() if c)),q['mask']) for q in self.full_probes}
            for distance,mask,target in fc.candidate(point,width,margin,used):
                m.need(set(target)<=INTEGER_NAMES,'Integer full-cover target')
                guards=fc.bracket(target,mask,width,margin);certificates=[]
                for guard in guards:
                    cert,infeasible=self.nonstrict_guard(guard)
                    if infeasible:return False,True
                    if cert is None:
                        self.full_cover_failures.append((distance,guard));break
                    certificates.append(cert)
                if len(certificates)!=2:continue
                self.trace.append(dict(kind='full_cover_probe',target=target,mask=mask,certificates=certificates))
                self.rows.extend((guard,0,'proved full target bracket') for guard in guards)
                self.full_probes.append(dict(target=target,mask=mask,width=width,margin=margin,nodes=fc.initial_nodes(),forced=False))
                changed=True;break
        for pid,state in enumerate(self.full_probes):
            nodes=state['nodes'];target=state['target'];width=state['width'];queue=sorted(nodes)
            for node in queue:
                options=sorted((ev(fc.exclusion(target,node,direction,width)),direction) for direction in (0,1))
                excluded=False
                for value,direction in options:
                    if value>1e-7:continue
                    guard=fc.exclusion(target,node,direction,width);cert,infeasible=self.nonstrict_guard(guard)
                    if infeasible:return False,True
                    if cert is None:
                        self.full_cover_failures.append((-value,guard));continue
                    self.trace.append(dict(kind='full_cover_exclude',probe=pid,node=node,direction=direction,certificate=cert))
                    self.rows.append((guard,0,'proved full component exclusion'));nodes.remove(node);changed=True;excluded=True;break
                if excluded:continue
                if node[1]==-1 and len(fc.roots()[node[0]])<4:
                    self.trace.append(dict(kind='full_cover_refine',probe=pid,root=node[0]))
                    fc.refine(nodes,node[0]);queue.extend((node[0],i) for i in range(len(fc.children(node[0]))));changed=True;state['forced']=False
            if not nodes:
                self.trace.append(dict(kind='full_cover_final',probe=pid));return True,True
            if len(nodes)==1 and not state['forced']:
                node=next(iter(nodes));self.trace.append(dict(kind='full_cover_force',probe=pid,node=node))
                self.rows.extend((guard,0,'required full target component') for guard in fc.containment(target,node,width))
                state['forced']=True;changed=True
        return changed,False

    def integral_kernel_step(self,point):
        if self.j<3 or 3 in self.st.values():return False,False
        import math
        names=['FD','F',*('GB'+str(i) for i in range(1,11)),*('phi'+source+side for source in ('core','source') for side in 'st')]
        before=len(self.trace)
        for name in names:
            value=point[name];lower=math.floor(value);upper=lower+1
            if min(value-lower,upper-value)<1e-6:continue
            for guard in ({name:1,'ONE':-lower},{name:-1,'ONE':upper}):
                _,infeasible=self.nonstrict_guard(guard)
                if infeasible:return False,True
                if len(self.trace)>before:return True,False
        return False,False

    def ordered_cover_step(self,point):
        self.ordered_cover_failures=[]
        if self.j<3 or 3 in self.st.values():return False,False
        import interval_gaps
        ev=lambda row:sum(c*point[k] for k,c in row.items());changed=False;failed=[];numeric={};selected={}
        for side in 'st':
            other='t' if side=='s' else 's';centres,points,native=interval_gaps.catalogue(self.st,self.Z,side)
            order=self.ordered_cover[side]['order'] if side in self.ordered_cover else sorted(range(len(centres)),key=lambda i:(ev(centres[i][1]),i))
            licenses=interval_gaps.licenses(self.st,self.Z,side,order)
            if any(ev(g)>1e-7 for g in licenses):continue
            if side not in self.ordered_cover:
                certificates=[]
                for guard in licenses:
                    cert,infeasible=self.nonstrict_guard(guard)
                    if infeasible:return False,True
                    if cert is None:failed.append(guard);break
                    certificates.append(cert)
                if len(certificates)!=len(licenses):continue
                self.trace.append(dict(kind='ordered_cover_license',side=side,order=order,certificates=certificates))
                self.rows.extend((guard,0,'proved ordered core cover guard') for guard in licenses)
                self.ordered_cover[side]=dict(order=order,excluded=set());changed=True
            state=self.ordered_cover[side];remaining_native=remaining_all=0
            for index,(_,form) in enumerate(points):
                value=ev(form);places=[]
                if value<=1e-7:places.append('low')
                if value>=point['S'+side]+1-1e-7:places.append('high')
                places.extend(i for i,(_,centre) in enumerate(centres) if ev(centre)-point['R'+other]-1e-7<=value<=ev(centre)+point['R'+side]+1e-7)
                if not places:
                    remaining_all+=1;remaining_native+=index<native
                if index in state['excluded']:continue
                for where in places:
                    guards=interval_gaps.exclusion(self.st,self.Z,side,index,where);certificates=[]
                    for guard in guards:
                        cert,infeasible=self.nonstrict_guard(guard)
                        if infeasible:return False,True
                        if cert is None:failed.append(guard);break
                        certificates.append(cert)
                    if len(certificates)!=len(guards):continue
                    self.trace.append(dict(kind='ordered_cover_exclude',side=side,index=index,where=where,certificates=certificates))
                    self.rows.extend((guard,0,'proved ordered core cover guard') for guard in guards);state['excluded'].add(index);changed=True;break
            forms=interval_gaps.gaps(self.st,self.Z,side,order);selected[side]=[i for i,g in enumerate(forms) if ev(g)>1e-7]
            gap=sum(ev(forms[i]) for i in selected[side])-point['hole_W'];numeric[side]=(gap,remaining_native,remaining_all)
            row=interval_gaps.capacity(self.st,self.Z,self.ordered_cover,{side:selected[side]},self.e,False)
            if ev(row[0])>row[1]+1e-7:
                self.trace.append(dict(kind='ordered_cover_capacity',selected={side:selected[side]},credit=self.e,joint=False));self.rows.append(row);changed=True
        potential=any(gap>all_points+1e-7 for gap,native,all_points in numeric.values())
        if set(selected)==set('st'):
            row=interval_gaps.capacity(self.st,self.Z,self.ordered_cover,selected,self.e,True)
            if ev(row[0])>row[1]+1e-7:
                self.trace.append(dict(kind='ordered_cover_capacity',selected=selected,credit=self.e,joint=True));self.rows.append(row);changed=True
            potential=potential or sum(v[0]-v[1] for v in numeric.values())>84-self.e+1e-7
        if potential:self.ordered_cover_failures=failed
        return changed,False

    def positive_hole_step(self,point):
        if not self.positive:return False,False
        import positive_holes,math
        used=[int(label.rsplit(' ',1)[1]) for _,_,label in self.rows if label.startswith('positive hole mass profile ')]
        for hi in range(max(1,math.ceil(point['hole_W']-1e-7)),min(used,default=8)):
            guard={'hole_W':1,'ONE':-hi};cert,infeasible=self.nonstrict_guard(guard)
            if infeasible:return False,True
            if cert is None:continue
            self.trace.append(dict(kind='positive_hole_profile',hi=hi,certificate=cert))
            self.rows.append((guard,0,'proved positive-hole profile range'));self.rows.append(positive_holes.row(hi))
            return True,False
        return False,False

    def retained_predecessor_step(self,point):
        if not self.positive or self.j!=4 or self.e<38:return False,False
        import positive_holes
        total=[int(label.rsplit(' ',1)[1]) for _,_,label in self.rows if label.startswith('positive hole mass profile ')]
        lo=(self.limits or {}).get('hole_W',(1,7))[0];hi=min(total,default=7)
        used={(int(label.split()[-2]),int(label.split()[-1])) for _,_,label in self.rows if label.startswith('retained positive predecessor ')}
        if any(a>=lo and b<=hi for a,b in used):return False,False
        guards=[{'hole_W':-1,'ONE':lo},{'hole_W':1,'ONE':-hi}];certificates=[]
        for guard in guards:
            cert,infeasible=self.nonstrict_guard(guard)
            if infeasible:return False,True
            if cert is None:return False,False
            certificates.append(cert)
        self.trace.append(dict(kind='retained_positive_predecessor',lo=lo,hi=hi,credit=self.e,certificates=certificates))
        self.rows.extend((guard,0,'proved retained predecessor range') for guard in guards);self.rows.extend(positive_holes.retained_predecessor_rows(lo,hi))
        return True,False

    def combined_hole_step(self,point):
        if not self.positive:return False,False
        import combined_holes
        used={label for _,_,label in self.rows}
        retained=self.j==4 and self.e>=38
        kinds=[False]+([True] if retained else [])
        kinds=[v for v in kinds if combined_holes.total_rows(v)[2] not in used]
        if not kinds:return False,False
        guard={'hole_W':1,'ONE':-2}
        cert,infeasible=self.nonstrict_guard(guard)
        if infeasible:return False,True
        if cert is None:return False,False
        for value in kinds:
            self.trace.append(dict(kind='combined_hole_mass',retained=value,credit=self.e,certificate=cert))
            self.rows.append((guard,0,'proved combined hole range'));self.rows.append(combined_holes.total_rows(value))
        return True,False

    def positive_kernel_step(self,point):
        if not self.positive or self.j!=4 or self.e<38:return False,False
        import positive_kernel
        lo,hi=(self.limits or {}).get('hole_W',(1,7))
        if lo!=hi or lo not in (1,2):return False,False
        used={label for _,_,label in self.rows}
        rank_hi=min([int(label.rsplit(' ',1)[1]) for _,_,label in self.rows if label.startswith('positive core gap rank ')]+[17])
        spec=positive_kernel.plan(lo,self.e,rank_hi)
        choices=[(side,q) for side,entry in spec.items() for q in range(1,entry['depth']+1) if positive_kernel.rows(lo,side,q)[0][2] not in used]
        combined=[q for q in range(1,min(v['depth'] for v in spec.values())+1) if positive_kernel.combined_rows(lo,self.e,rank_hi,q)[0][2] not in used]
        if not choices and not combined:return False,False
        guards=[{'hole_W':-1,'ONE':lo},{'hole_W':1,'ONE':-lo},{'rank_k':1,'ONE':-rank_hi}];certificates=[]
        for guard in guards:
            cert,infeasible=self.nonstrict_guard(guard)
            if infeasible:return False,True
            if cert is None:return False,False
            certificates.append(cert)
        self.trace.append(dict(kind='positive_retained_kernel',W=lo,credit=self.e,rank_hi=rank_hi,choices=choices,combined=combined,certificates=certificates))
        self.rows.extend((guard,0,'proved positive retained kernel range') for guard in guards)
        for side,q in choices:self.rows.extend(positive_kernel.rows(lo,side,q))
        for q in combined:self.rows.extend(positive_kernel.combined_rows(lo,self.e,rank_hi,q))
        return True,False

    def positive_first_gap_step(self,point):
        if not self.positive:return False,False
        import positive_holes,math
        used=[int(label.rsplit(' ',1)[1]) for _,_,label in self.rows if label.startswith('positive core gap rank ')]
        for hi in range(max(0,math.ceil(point['rank_k']-1e-7)),min(used,default=18)):
            guard={'rank_k':1,'ONE':-hi};cert,infeasible=self.nonstrict_guard(guard)
            if infeasible:return False,True
            if cert is None:continue
            self.trace.append(dict(kind='positive_core_gap',rank_hi=hi,certificate=cert))
            self.rows.append((guard,0,'proved positive first-gap rank range'));self.rows.extend(positive_holes.first_gap_rows(hi))
            return True,False
        return False,False

    def positive_hole_side_step(self,point):
        if not self.positive:return False,False
        import positive_holes
        total=[int(label.rsplit(' ',1)[1]) for _,_,label in self.rows if label.startswith('positive hole mass profile ')]
        lo=(self.limits or {}).get('hole_W',(1,7))[0];hi=min(total,default=7)
        used={(int(label.split()[-2]),int(label.split()[-1])) for _,_,label in self.rows if label.startswith('positive side interval ')}
        if any(a>=lo and b<=hi for a,b in used):return False,False
        guards=[{'hole_W':-1,'ONE':lo},{'hole_W':1,'ONE':-hi}];certificates=[]
        for guard in guards:
            cert,infeasible=self.nonstrict_guard(guard)
            if infeasible:return False,True
            if cert is None:return False,False
            certificates.append(cert)
        self.trace.append(dict(kind='positive_hole_side_interval',lo=lo,hi=hi,certificates=certificates))
        self.rows.extend((guard,0,'proved positive side interval') for guard in guards);self.rows.extend(positive_holes.side_interval_rows(lo,hi))
        return True,False

    def fixed_shifted_step(self,point):
        self.shifted_cover_failures=[]
        if not self.positive or self.j<3 or 3 in self.st.values() or point['ts']+point['tt']+point['rank_k']>94+1e-7:return False,False
        import shifted_source
        modes,data,chains=shifted_source.chains(self.st,self.Z,point);forms=m.fixed_forms()
        ev=lambda row:sum(c*point[k] for k,c in row.items());changed=False
        for label in sorted(set(forms)-self.low-self.high-self.covered):
            side='s' if '+' in label else 't';items=data[side];value=ev(forms[label])
            options=[[i] for i,(lo,hi) in enumerate(items) if ev(lo)-1e-7<=value<=ev(hi)+1e-7]
            options.extend(chain for chain in chains[side] if len(chain)>1 and ev(items[chain[0]][0])-1e-7<=value<=ev(items[chain[-1]][1])+1e-7)
            for chain in sorted(options,key=len):
                guards=shifted_source.cover_guards(self.st,self.Z,modes,side,chain,label);certificates=[]
                for guard in guards:
                    cert,infeasible=self.nonstrict_guard(guard)
                    if infeasible:return False,True
                    if cert is None:
                        self.shifted_cover_failures.append(guard);break
                    certificates.append(cert)
                if len(certificates)!=len(guards):continue
                self.trace.append(dict(kind='fixed_shifted_cover',label=label,side=side,modes=modes,chain=chain,certificates=certificates))
                self.rows.extend((guard,0,'proved shifted fixed cover') for guard in guards);self.covered.add(label);changed=True;break
        return changed,False

    def fixed_known_step(self,point):
        self.fixed_known_failures=[]
        if self.j<3 or 3 in self.st.values():return False,False
        import known_union
        modes,data,chains=known_union.cover_chains(self.st,self.Z,point);forms=m.fixed_forms()
        ev=lambda row:sum(c*point[k] for k,c in row.items());changed=False
        for label in sorted(set(forms)-self.low-self.high-self.covered):
            side='s' if '+' in label else 't';items=data[side]['components'];value=ev(forms[label])
            options=[[i] for i,(lo,hi) in enumerate(items) if ev(lo)-1e-7<=value<=ev(hi)+1e-7]
            options.extend(chain for chain in chains[side] if len(chain)>1 and ev(items[chain[0]][0])-1e-7<=value<=ev(items[chain[-1]][1])+1e-7)
            for chain in sorted(options,key=len):
                guards=known_union.cover_guards(self.st,self.Z,modes,side,chain,label);certificates=[]
                for guard in guards:
                    cert,infeasible=self.nonstrict_guard(guard)
                    if infeasible:return False,True
                    if cert is None:
                        self.fixed_known_failures.append((len(chain),guard));break
                    certificates.append(cert)
                if len(certificates)!=len(guards):continue
                self.trace.append(dict(kind='fixed_known_cover',label=label,side=side,modes=modes,chain=chain,certificates=certificates))
                self.rows.extend((guard,0,'proved known fixed cover') for guard in guards);self.covered.add(label);changed=True;break
        return changed,False

    def known_union_step(self,point):
        self.union_failures=[]
        if self.j<3 or 3 in self.st.values():return False,False
        import known_union
        proof=known_union.recipe(self.st,self.Z,point);row,guards=known_union.derive(self.st,self.Z,proof,self.e)
        violation=sum(c*point[k] for k,c in row[0].items())-row[1]
        if violation<=1e-7:return False,False
        certificates=[]
        for guard in guards:
            cert,infeasible=self.nonstrict_guard(guard)
            if infeasible:return False,True
            if cert is None:
                self.union_failures=[(violation,guard)];return False,False
            certificates.append(cert)
        self.trace.append(dict(kind='known_union',credit=self.e,recipe=proof,certificates=certificates))
        self.rows.extend((guard,0,'proved known-union guard') for guard in guards);self.rows.append(row)
        return True,False

    def cover_capacity_step(self,point):
        self.capacity_failures=[]
        if self.j<3 or 3 in self.st.values():return False,False
        import cover_capacity
        candidates=[]
        for mode,side in [('sumset',None),('native',None),('full','s'),('full','t')]:
            proof=cover_capacity.recipe(self.st,self.Z,point,mode,side)
            row,guards=cover_capacity.derive(self.st,self.Z,proof,self.e)
            violation=sum(c*point[k] for k,c in row[0].items())-row[1]
            if violation>1e-7:candidates.append((violation,proof,row,guards))
        for violation,proof,row,guards in sorted(candidates,key=lambda entry:entry[0],reverse=True):
            first_failure=True
            for attempt in range(512):
                certificates=[];failed=None
                for guard in guards:
                    cert,infeasible=self.nonstrict_guard(guard)
                    if infeasible:return False,True
                    if cert is None:
                        if first_failure:self.capacity_failures.append((violation,guard));first_failure=False
                        failed=guard;break
                    certificates.append(cert)
                if failed is None:
                    self.trace.append(dict(kind='cover_capacity',credit=self.e,recipe=proof,certificates=certificates))
                    self.rows.extend((guard,0,'proved cover capacity guard') for guard in guards);self.rows.append(row)
                    return True,False
                relaxed=cover_capacity.relax_guard(self.st,self.Z,proof,failed)
                if relaxed is None or relaxed==proof:break
                proof=relaxed;row,guards=cover_capacity.derive(self.st,self.Z,proof,self.e)
                if sum(c*point[k] for k,c in row[0].items())<=row[1]+1e-7:break
        return False,False

    def core_tail_step(self,point):
        self.core_tail_failures=[]
        if self.j<3 or 3 in self.st.values():return False,False
        import known_union
        changed=False;ev=lambda row:sum(c*point[k] for k,c in row.items())
        for side in 'st':
            if self.st.get('H'+side)!=1 or self.st.get('O'+side)==1:continue
            endpoint,guards,points=known_union.tail_catalogue(self.st,self.Z,side)
            numerical=sum(ev(endpoint)+1e-7<ev(value)<point['S'+side]+1e-7 for _,value in points)
            violation=point['S'+side]-ev(endpoint)-point['hole_W']-numerical
            if side not in self.core_tail_excluded:
                if violation<=1e-7:continue
                certificates=[]
                for guard in guards:
                    cert,infeasible=self.nonstrict_guard(guard)
                    if infeasible:return False,True
                    if cert is None:
                        self.core_tail_failures.append((violation,guard));break
                    certificates.append(cert)
                if len(certificates)!=len(guards):continue
                self.trace.append(dict(kind='core_tail_license',side=side,certificates=certificates))
                self.rows.extend((guard,0,'proved core-tail license') for guard in guards)
                self.core_tail_excluded[side]=set();changed=True
            excluded=self.core_tail_excluded[side];before=len(excluded)
            for index in range(len(points)):
                if index in excluded:continue
                for direction in sorted((0,1),key=lambda d:ev(known_union.tail_exclusion(self.st,self.Z,side,index,d))):
                    guard=known_union.tail_exclusion(self.st,self.Z,side,index,direction)
                    if ev(guard)>1e-7:continue
                    cert,infeasible=self.nonstrict_guard(guard)
                    if infeasible:return False,True
                    if cert is None:
                        if violation>0:self.core_tail_failures.append((violation,guard))
                        continue
                    self.trace.append(dict(kind='core_tail_exclude',side=side,index=index,direction=direction,certificate=cert))
                    self.rows.append((guard,0,'proved core-tail exclusion'));excluded.add(index);break
            if len(excluded)>before or changed:
                self.trace.append(dict(kind='core_tail_capacity',side=side));self.rows.append(known_union.tail_capacity(self.st,self.Z,side,excluded));changed=True
        if set(self.core_tail_excluded)==set('st'):
            row=known_union.joint_tail_capacity(self.st,self.Z,self.core_tail_excluded,self.e);stamp=(self.e,row[1])
            if stamp!=getattr(self,'joint_core_tail_stamp',None):
                self.trace.append(dict(kind='joint_core_tail_capacity',credit=self.e));self.rows.append(row);self.joint_core_tail_stamp=stamp;changed=True
        return changed,False

    def run(self):
        forms=m.fixed_forms()
        if self.positive and self.j>=3 and not any(label=='positive predecessor gap s' for _,_,label in self.rows):
            import positive_holes
            self.trace.append(dict(kind='positive_predecessor_gap'));self.rows.extend(positive_holes.predecessor_rows(self.j))
        if self.positive and self.j>=3 and 3 not in self.st.values():
            for hi in range(1,self.coverage_width-1):
                guard={'hole_W':1,'ONE':-hi}
                certificate,infeasible=self.nonstrict_guard(guard)
                if infeasible:return self.final()
                if certificate is None:continue
                self.trace.append(dict(kind='coverage_width',hole_upper=hi,certificate=certificate))
                self.rows.append((guard,0,'proved target-hole bound'))
                self.coverage_width=hi+1
                self.coverage_bracket_width=hi+1
                # Old exclusions remain valid for the shorter interval; a
                # previously forced component now gets the stronger bracket.
                for state in self.coverage_probes.values():state['forced']=False
                break
            if self.coverage_width>1 or self.coverage_bracket_width>3:
                import single_hole
                for H in (1,2,3):
                    if self.coverage_width==1 and H+2>=self.coverage_bracket_width:continue
                    certificates=[]
                    for guard in single_hole.guards(H):
                        certificate,infeasible=self.nonstrict_guard(guard)
                        if infeasible:return self.final()
                        if certificate is None:break
                        certificates.append(certificate)
                    if len(certificates)!=2:continue
                    self.trace.append(dict(kind='single_hole_interior',H=H,certificates=certificates))
                    self.rows.extend((guard,0,'proved single-hole location') for guard in single_hole.guards(H))
                    # Previously licensed probes may lie in the short top
                    # strip. Their already proved facts stay valid, while
                    # new singleton probes use the smaller interior domain.
                    self.coverage_probes={};self.coverage_width=1;self.coverage_bracket_width=H+2
                    break
        for cycle in range(512):
            rr=self.lp()
            if rr.status==2:return self.final()
            if rr.status!=0:raise ValueError(rr.message)
            point=dict(zip(self.names,rr.x));changed=False
            strengthened,infeasible=self.integral_kernel_step(point)
            if infeasible:return self.final()
            if strengthened:continue
            strengthened,infeasible=self.full_cover_step(point)
            if infeasible:return True if strengthened else self.final()
            if strengthened:continue
            for label,form in forms.items():
                if label in self.low|self.high:continue
                value=sum(c*point[k] for k,c in form.items())
                integer_scope=self.j>=3 and 3 not in self.st.values()
                if value<(1-1e-7 if integer_scope else 1e-6):target=form;kind='low'
                elif value>=point['Ss' if '+' in label else 'St']+1e-6:
                    target=m.add((-1,form),(1,m.var('Ss' if '+' in label else 'St')));kind='high'
                else:continue
                if kind=='low' or integer_scope:
                    guard=target if kind=='low' else m.add((1,target),(1,{'ONE':1}))
                    cert,infeasible=self.nonstrict_guard(guard)
                    if infeasible:return self.final()
                    if cert is not None and kind=='high':
                        weights={(a,i):v for a,i,v in cert['weights']}
                        unit=next(i for i,(row,rhs,_) in enumerate(self.eqs) if row=={'ONE':1} and rhs==1)
                        weights['e',unit]=weights.get(('e',unit),0)-cert['denominator']
                        cert={'weights':[(a,i,v) for (a,i),v in weights.items() if v],'denominator':cert['denominator']}
                        exact.check(cert,self.rows,self.eqs,target,strict=True)
                else:
                    rr=self.lp(target)
                    if rr.status==2:return self.final()
                    if rr.status!=0:raise ValueError(rr.message)
                    if rr.fun<1e-7:continue
                    cert=self.reconstruct(rr,target,strict=True)
                if cert is None:continue
                self.trace.append(dict(kind=kind,label=label,certificate=cert))
                (self.low if kind=='low' else self.high).add(label)
                self.rows.append((target,0 if kind=='low' or 3 in self.st.values() else -1,'proved '+kind.upper()+' '+label))
                changed=True
            for label in sorted(self.covered-self.covered_positive):
                guard=m.add((1,{'ONE':1}),(-1,forms[label]))
                if sum(c*point[k] for k,c in guard.items())>1e-7:continue
                cert,infeasible=self.nonstrict_guard(guard)
                if infeasible:return self.final()
                if cert is None:continue
                self.trace.append(dict(kind='fixed_cover_positive',label=label,certificate=cert))
                self.rows.append((guard,0,'proved covered fixed positive'));self.covered_positive.add(label);changed=True
            next_e=exact.credit(self.low,self.high,self.initial,self.covered,self.covered_positive,self.fixed_pairs)
            if next_e>self.e:
                self.e=next_e;self.trace.append(dict(kind='credit',e=self.e));self.rows.extend(exact.credit_rows(self.ret,self.e));changed=True
                if self.use_planes:
                    _,updated,_=p.build(self.st,self.j,self.positive,self.e,self.limits)
                    self.rows.extend(row for row in updated if row[2].startswith('uniform endpoint ') or row[2] in ('parameter rank range','parameter rank chord'))
                    self.trace.append(dict(kind='endpoint_credit',e=self.e))
            if not self.alpha_tail_done:
                try:extra=exact.alpha_tail_rows(self.st,self.j,self.positive,self.e,self.Z)
                except ValueError:extra=[]
                if extra:
                    self.trace.append(dict(kind='conditional_alpha_tail'));self.rows.extend(extra);self.alpha_tail_done=True;changed=True
            if not self.ownerless_done:
                try:extra=exact.ownerless_rows(self.st,self.j,self.positive,self.e,self.Z,self.limits)
                except ValueError:extra=[]
                if extra:
                    self.trace.append(dict(kind='conditional_ownerless'));self.rows.extend(extra);self.ownerless_done=True;changed=True
            if not self.alpha_done:
                try:indices=exact.alpha_compression(self.st,self.j,self.positive,self.e,self.edges)
                except ValueError:indices=[]
                if indices:
                    self.trace.append(dict(kind='alpha_half_mass'));self.alpha_done=True
                    for i in indices:self.constants[i]=max(self.constants.get(i,0),64)
                    changed=True
            for side in 'st':
                if self.j<3 or self.st['O'+side]==1:continue
                def tail_credit():
                    removed=exact.tail_removed(side,self.low|self.high|self.tail_low[side],self.tail_pairs[side])
                    if removed<=self.tail_counts[side]:return False
                    self.tail_counts[side]=removed;self.trace.append(dict(kind='tail_credit',side=side,removed=removed))
                    self.rows.append(exact.tail_row(side,self.Z,removed));return True
                changed=tail_credit() or changed
                end=exact.tail_endpoint(side,self.Z)
                for label in sorted(exact.tail_labels(side)-(self.low|self.high|self.tail_low[side])):
                    target=m.add((1,forms[label]),(-1,end))
                    if sum(c*point[name] for name,c in target.items())>1e-6:continue
                    cert,infeasible=self.nonstrict_guard(target)
                    if infeasible:return self.final()
                    if cert is None:continue
                    self.trace.append(dict(kind='tail_low',side=side,label=label,certificate=cert))
                    self.tail_low[side].add(label);self.rows.append((target,0,'proved tail LOW '+label));changed=True
                changed=tail_credit() or changed
            if not changed:
                extra,finished=self.positive_hole_step(point)
                if finished:return self.final()
                changed=extra
            if not changed:
                extra,finished=self.positive_hole_side_step(point)
                if finished:return self.final()
                changed=extra
            if not changed:
                extra,finished=self.positive_first_gap_step(point)
                if finished:return self.final()
                changed=extra
            if not changed:
                extra,finished=self.retained_predecessor_step(point)
                if finished:return self.final()
                changed=extra
            if not changed:
                extra,finished=self.combined_hole_step(point)
                if finished:return self.final()
                changed=extra
            if not changed:
                extra,finished=self.positive_kernel_step(point)
                if finished:return self.final()
                changed=extra
            if not changed:
                extra,finished=self.fixed_shifted_step(point)
                if finished:return self.final()
                changed=extra
            if not changed:
                extra,finished=self.fixed_known_step(point)
                if finished:return self.final()
                changed=extra
            if not changed:
                extra,finished=self.ordered_cover_step(point)
                if finished:return self.final()
                changed=extra
            if not changed:
                extra,finished=self.core_tail_step(point)
                if finished:return self.final()
                changed=extra
            if not changed:
                extra,finished=self.cover_capacity_step(point)
                if finished:return self.final()
                changed=extra
            if not changed:
                extra,finished=self.known_union_step(point)
                if finished:return self.final()
                changed=extra
            if not changed:
                extra,finished=self.coverage_step(point)
                if finished:return True if extra else self.final()
                changed=extra
                if not changed and self.coverage_gap(point):
                    current=self.lp()
                    if current.status==2:return self.final()
                    if current.status!=0:raise ValueError(current.message)
                    point=dict(zip(self.names,current.x))
                    if self.coverage_gap(point):self.point=point;return False
            if not changed and self.j>=3 and 3 not in self.st.values():
                remaining=sorted(set(forms)-self.low-self.high-self.covered)
                for ai,first in enumerate(remaining):
                    for second in remaining[ai+1:]:
                        pair=(first,second)
                        if pair in self.fixed_pairs:continue
                        if exact.credit(self.low,self.high,self.initial,self.covered,self.covered_positive,self.fixed_pairs|{pair})<=self.e:continue
                        options=[(first,second,'low'),(first,second,'high')]
                        if ('+' in first)==('+' in second):options.extend([(first,second,'apart'),(second,first,'apart'),(first,second,'equal')])
                        for a,b,mode in options:
                            guards=exact.fixed_pair_guards(a,b,mode)
                            if any(sum(c*point[k] for k,c in guard.items())>1e-7 for guard in guards):continue
                            certificates=[]
                            for guard in guards:
                                cert,infeasible=self.nonstrict_guard(guard)
                                if infeasible:return self.final()
                                if cert is None:break
                                certificates.append(cert)
                            if len(certificates)!=len(guards):continue
                            self.trace.append(dict(kind='fixed_pair',first=a,second=b,mode=mode,certificates=certificates))
                            for guard in guards:self.rows.append((guard,0,'proved fixed conflict'))
                            self.fixed_pairs.add(pair);changed=True;break
                        if pair in self.fixed_pairs or ('+' in first)!=('+' in second):continue
                        side='s' if '+' in first else 't';probe_options=[]
                        for resource in (v for v in self.ret if v[-1]==side):
                            for core_side in 'st':
                                a,b=first,second
                                if (sum(c*point[k] for k,c in forms[a].items())>sum(c*point[k] for k,c in forms[b].items()))==(core_side==side):a,b=b,a
                                guards=exact.fixed_probe_pair_guards(a,b,resource,core_side,self.Z)
                                if all(sum(c*point[k] for k,c in guard.items())<=1e-7 for guard in guards):probe_options.append((a,b,resource,core_side,guards))
                        for a,b,resource,core_side,guards in probe_options:
                            certificates=[]
                            for guard in guards:
                                cert,infeasible=self.nonstrict_guard(guard)
                                if infeasible:return self.final()
                                if cert is None:break
                                certificates.append(cert)
                            if len(certificates)!=len(guards):continue
                            self.trace.append(dict(kind='fixed_probe_pair',first=a,second=b,resource=resource,core_side=core_side,certificates=certificates))
                            for guard in guards:self.rows.append((guard,0,'proved fixed probe conflict'))
                            self.fixed_pairs.add(pair);changed=True;break
            if not changed and self.j>=3 and 3 not in self.st.values():
                for label in sorted(set(forms)-self.low-self.high-self.covered):
                    side='s' if '+' in label else 't';options=[]
                    for resource in [v for v in self.ret if v[-1]==side]+['L'+side]:
                        witnesses=(None,) if resource[0]!='L' else exact.LEADING_WITNESSES
                        for q in (2,4,5,3,1):
                            for witness in witnesses:
                                guards=exact.fixed_cover_guards(label,resource,q,witness,self.Z)
                                values=[sum(c*point[k] for k,c in guard.items()) for guard in guards]
                                if max(values)<=1e-7:options.append((len(guards),max(values),resource,q,witness,guards))
                    for _,_,resource,q,witness,guards in sorted(options,key=lambda item:item[:4]):
                        certificates=[]
                        for guard in guards:
                            cert,infeasible=self.nonstrict_guard(guard)
                            if infeasible:return self.final()
                            if cert is None:break
                            certificates.append(cert)
                        if len(certificates)!=len(guards):continue
                        self.trace.append(dict(kind='fixed_cover',label=label,resource=resource,q=q,witness=witness,certificates=certificates))
                        for guard in guards:self.rows.append((guard,0,'proved fixed source cover'))
                        self.covered.add(label);changed=True;break
            if not changed and self.use_planes:
                from itertools import combinations
                for side in 'st':
                    if self.j<3 or self.st['O'+side]==1:continue
                    end=exact.tail_endpoint(side,self.Z)
                    remaining=sorted(exact.tail_labels(side)-(self.low|self.high|self.tail_low[side]))
                    for a,b in combinations(remaining,2):
                        pair=tuple(sorted((a,b)))
                        if pair in self.tail_pairs[side]:continue
                        difference=m.add((1,forms[a]),(-1,forms[b]))
                        if sum(c*point[k] for k,c in difference.items())<0:a,b=b,a;difference={k:-c for k,c in difference.items()}
                        target=m.add((1,m.var('S'+side)),(-1,end),(-1,difference))
                        if sum(c*point[k] for k,c in target.items())>1e-6:continue
                        cert,infeasible=self.nonstrict_guard(target)
                        if infeasible:return self.final()
                        if cert is None:continue
                        self.trace.append(dict(kind='tail_incompatible',side=side,larger=a,smaller=b,certificate=cert))
                        self.tail_pairs[side].add(pair);self.rows.append((target,0,'proved tail incompatible '+a+':'+b));changed=True
                    removed=exact.tail_removed(side,self.low|self.high|self.tail_low[side],self.tail_pairs[side])
                    if removed>self.tail_counts[side]:
                        self.tail_counts[side]=removed;self.trace.append(dict(kind='tail_credit',side=side,removed=removed))
                        self.rows.append(exact.tail_row(side,self.Z,removed));changed=True
            if not changed:
                for side in 'st':
                    for pair in exact.TRIM_PAIRS:
                        key=(side,*pair)
                        if key in self.trim_pairs:continue
                        guard=exact.trim_pair_guard(side,pair)
                        if sum(c*point[k] for k,c in guard.items())>1e-7:continue
                        cert,infeasible=self.nonstrict_guard(guard)
                        if infeasible:return self.final()
                        if cert is None:continue
                        self.trace.append(dict(kind='trim_hull_pair',side=side,pair=pair,certificate=cert))
                        self.rows.append((guard,0,'proved trimmed hull pair'));self.trim_pairs.add(key)
                        self.rows.append(exact.trim_hull_row(len(self.trim_pairs)));changed=True
            if not changed:
                for key in exact.SUMSET_GAPS:
                    _,_,lower,upper,qs,qo=exact.sumset_gap_data(key)
                    length=m.add((1,upper),(-1,lower),(-1,qs),(-1,qo),(-1,{'ONE':1}))
                    if sum(c*point[k] for k,c in length.items())<=1e-7:continue
                    for pair in exact.sumset_gap_pairs(key):
                        if pair in self.sumset_excluded.get(key,set()):continue
                        guards=exact.sumset_gap_guards(key,pair)
                        options=sorted((sum(c*point[k] for k,c in guard.items()),i,guard) for i,guard in enumerate(guards))
                        for value,index,guard in options:
                            if value>1e-7:continue
                            cert,infeasible=self.nonstrict_guard(guard)
                            if infeasible:return self.final()
                            if cert is None:continue
                            self.trace.append(dict(kind='sumset_gap_exclude',gap=key,pair=pair,guard=index,certificate=cert))
                            self.rows.append((guard,0,'proved source gap pair outside'));self.sumset_excluded.setdefault(key,set()).add(pair);changed=True;break
            if not changed:
                for key in exact.SUMSET_GAPS:
                    side,_,lower,upper,qs,qo=exact.sumset_gap_data(key)
                    ev=lambda row:sum(c*point[k] for k,c in row.items())
                    left,right=ev(lower)+ev(qs),ev(upper)-ev(qo)
                    if right-left<=1:continue
                    candidates=[]
                    for pair in exact.sumset_gap_pairs(key):
                        if pair in self.sumset_excluded.get(key,set()):continue
                        value=sum(ev(exact.signed_source_point(tag,side)) for tag in pair)
                        if left<value<right:candidates.append((value,pair))
                    for ai,(value,first) in enumerate(candidates):
                        for other,second in candidates[ai+1:]:
                            if abs(value-other)>1e-7:continue
                            equalities=self.sumset_equalities.get(key,[])
                            if exact.sumset_gap_remaining(key,(),equalities)==exact.sumset_gap_remaining(key,(),[*equalities,(first,second)]):continue
                            difference=exact.sumset_pair_difference(key,first,second);certificates=[]
                            for guard in (difference,{k:-v for k,v in difference.items()}):
                                cert,infeasible=self.nonstrict_guard(guard)
                                if infeasible:return self.final()
                                if cert is None:break
                                certificates.append(cert)
                            if len(certificates)!=2:continue
                            self.trace.append(dict(kind='sumset_pair_equal',gap=key,first=first,second=second,certificates=certificates))
                            for guard in (difference,{k:-v for k,v in difference.items()}):self.rows.append((guard,0,'proved source pair equality'))
                            self.sumset_equalities.setdefault(key,[]).append((first,second));changed=True
            if not changed and not self.use_planes:
                self.point=point;return False
            if not changed:
                for edge,actual in enumerate(self.edges):
                    if actual[0] not in ('Ls','Lt'):continue
                    side,other,right,_=exact.leading_geometry(actual)
                    for q in (2,4,5,3,1):
                        known=self.leading_hits.setdefault(edge,set()) if q==5 else self.leading_extended.setdefault(edge,{}).setdefault(q,set())
                        for tag in exact.leading_tags(q):
                            if tag[0]!=(other if right else side) or tag in known:continue
                            candidates=[]
                            for witness in exact.LEADING_WITNESSES:
                                guards=exact.leading_point_guards(actual,tag,witness,q)
                                values=[sum(c*point[k] for k,c in guard.items()) for guard in guards]
                                if max(values)<=1e-7:candidates.append((max(values),witness,guards))
                            for _,witness,guards in sorted(candidates):
                                certificates=[]
                                for guard in guards:
                                    cert,infeasible=self.nonstrict_guard(guard)
                                    if infeasible:return self.final()
                                    if cert is None:break
                                    certificates.append(cert)
                                if len(certificates)!=len(guards):continue
                                self.trace.append(dict(kind='leading_overlap_hit',edge=edge,tag=tag,witness=witness,q=q,certificates=certificates))
                                for guard in guards:self.rows.append((guard,0,'proved leading exterior hit'))
                                known.add(tag);changed=True;break
            if not changed:
                for edge,(_,_,gap) in enumerate(self.edges):
                    for q in (2,4,3,1):
                        for tag in exact.extended_tags(q):
                            if tag in self.extended_hits.get(edge,{}).get(q,set()):continue
                            guards=exact.extended_guards(gap,q,tag)
                            if any(sum(c*point[k] for k,c in guard.items())>1e-7 for guard in guards):continue
                            certificates=[]
                            for guard in guards:
                                cert,infeasible=self.nonstrict_guard(guard)
                                if infeasible:return self.final()
                                if cert is None:break
                                certificates.append(cert)
                            if len(certificates)!=2:continue
                            self.trace.append(dict(kind='extended_overlap_hit',edge=edge,q=q,tag=tag,certificates=certificates))
                            for guard in guards:self.rows.append((guard,0,'proved extended interval hit'))
                            self.extended_hits.setdefault(edge,{}).setdefault(q,set()).add(tag);changed=True
            if not changed:
                for edge,(_,_,gap) in enumerate(self.edges):
                    for tag in exact.POINT_TAGS:
                        if tag in self.point_hits.get(edge,set()):continue
                        guards=exact.point_overlap_guards(gap,tag)
                        if any(sum(c*point[k] for k,c in guard.items())>1e-7 for guard in guards):continue
                        certificates=[]
                        for guard in guards:
                            cert,infeasible=self.nonstrict_guard(guard)
                            if infeasible:return self.final()
                            if cert is None:break
                            certificates.append(cert)
                            # Do not append the first row until both guards are proved;
                            # each certificate is valid without the other guard.
                        if len(certificates)!=2:continue
                        self.trace.append(dict(kind='point_overlap_hit',edge=edge,tag=tag,certificates=certificates))
                        for guard in guards:self.rows.append((guard,0,'proved point overlap interval'))
                        self.point_hits.setdefault(edge,set()).add(tag);changed=True
            if not changed:
                for edge,(_,_,gap) in enumerate(self.edges):
                    for peel_side in 'st':
                        for core_side in 'st':
                            candidates=[]
                            for tag in exact.POINT_TAGS:
                                if tag[0]!=peel_side:continue
                                lower,upper,_=exact.point_group_guards(gap,[tag],core_side,1)
                                if max(sum(c*point[k] for k,c in lower.items()),sum(c*point[k] for k,c in upper.items()))<=1e-7:candidates.append(tag)
                            if len(candidates)<2:continue
                            key=tuple(sorted(candidates))
                            for q in range(1,len(candidates)+1):
                                count=len(candidates)-q+1
                                if self.point_groups.get(edge,{}).get(key,0)>=count:break
                                guards=exact.point_group_guards(gap,candidates,core_side,q)
                                if sum(c*point[k] for k,c in guards[2].items())>=-1e-7:continue
                                certs=[]
                                for index0,guard in enumerate(guards):
                                    rr=self.lp(guard)
                                    if rr.status==2:return self.final()
                                    if rr.status!=0 or rr.fun<(1e-7 if index0==2 else -1e-7):break
                                    cert=self.reconstruct(rr,guard,strict=index0==2)
                                    if cert is None:break
                                    certs.append(cert)
                                if len(certs)!=3:continue
                                self.trace.append(dict(kind='point_overlap_group',edge=edge,tags=candidates,core_side=core_side,q=q,certificates=certs))
                                for index0,guard in enumerate(guards):self.rows.append((guard,-1 if index0==2 else 0,'proved point group'))
                                self.point_groups.setdefault(edge,{})[key]=count;changed=True;break
            if not changed:
                # A successful implication licenses the integer compression
                # bound |E intersect(E+x)| >= |E|-x-k for this actual edge.
                for edge,(_,_,gap) in enumerate(self.edges):
                    distance=sum(c*point[name] for name,c in gap.items())
                    if distance<1e-7:continue
                    for source in ('core','source','trim1','trim2','trim3'):
                        n,span=exact.diameter_source(source)
                        if n<=max(self.constants.get(edge,0),point['FD'])+1e-7 or distance>=n:continue
                        target=m.add((1,span),(-2,gap))
                        if sum(c*point[name] for name,c in target.items())>=0:continue
                        rr=self.lp(target)
                        if rr.status==2:return self.final()
                        if rr.status!=0 or rr.fun<=1e-7:continue
                        cert=self.reconstruct(rr,target)
                        if cert is None:continue
                        self.trace.append(dict(kind='diameter',edge=edge,source=source,certificate=cert))
                        self.constants[edge]=max(self.constants.get(edge,0),n);self.rows.append((target,-1,'proved diameter compression'));changed=True
                    for source,n,massvalue,mass in [('source',73,point['TD'],{'TD':1}),('core',65,point['ts']+point['tt'],{'ts':1,'tt':1})]+[('trim'+str(q),73-2*q,point['TD'+str(q)],{'TD'+str(q):1}) for q in (1,2,3)]:
                        first=max(0,int(massvalue/distance+1e-8))
                        for kk in range(first,min(first+3,n)):
                            if n-kk<=max(self.constants.get(edge,0),point['FD'])+1e-7:break
                            target=m.add((1,mass),(-kk-1,gap));rr=self.lp(target)
                            if rr.status==2:return self.final()
                            if rr.status!=0 or rr.fun<=1e-7:continue
                            cert=self.reconstruct(rr,target)
                            if cert is None:continue
                            self.trace.append(dict(kind='compression',edge=edge,k=kk,source=source,certificate=cert))
                            self.constants[edge]=max(self.constants.get(edge,0),n-kk)
                            self.rows.append((target,-1,'proved compression'));changed=True;break
                if not changed:
                    current=self.lp()
                    if current.status==2:return self.final()
                    if current.status!=0:raise ValueError(current.message)
                    self.point=dict(zip(self.names,current.x));return False
        raise ValueError('Fixed credit iteration did not settle')

    def record(self):
        rec=dict(st=self.st,j=self.j,positive=self.positive,limits=self.limits,trace=self.trace,source_tail_ranks=True,sharp_planes=True,side_planes=True,trim_source=True,point_overlap=True,leading_overlap=True,full_edges=True,sumset_gaps=True)
        if self.use_planes:rec['planes']={key:p.PLANE_TABLE[key] for key in sorted(self.plane_keys)}
        if self.parent:rec['premise']=self.parent
        return rec


def main():
    j=int(sys.argv[1]);out=Path(sys.argv[2]);start=time.time();records=[];opens=[];done=set()
    def key(rec):return rec['positive'],tuple(sorted(rec['st'].items()))
    if out.exists():
        for rec in json.loads(out.read_text())['records']:
            try:exact.replay(rec)
            except (ValueError,IndexError):continue
            records.append(rec);done.add(key(rec))
    patterns=[*m.patterns(j),*m.partial_patterns(j)]
    for positive in ((False,) if j==6 else (False,True)):
        for i,st in enumerate(patterns):
            if (positive,tuple(sorted(st.items()))) in done:continue
            search=Search(st,j,positive)
            error=None
            try:
                closed=search.run()
                if not closed:
                    search=Search(st,j,positive,use_planes=True);closed=search.run()
            except ValueError as exc:
                closed=False;error=str(exc)
            if closed:
                rec=search.record();exact.replay(rec);records.append(rec)
            else:opens.append(dict(st=st,j=j,positive=positive,i=i,point=getattr(search,'point',None),e=search.e,error=error))
            if i%25==0 or not closed:
                print(j,i,positive,'closed',closed,'credit',search.e,'seconds',round(time.time()-start,1),flush=True)
                out.write_text(json.dumps(dict(schema='upper80-uniform-exact-v1',records=records,open=opens),separators=(',',':')))
    out.write_text(json.dumps(dict(schema='upper80-uniform-exact-v1',records=records,open=opens),separators=(',',':')))
    print('DONE',j,len(records),len(opens),flush=True)


if __name__=='__main__':main()
