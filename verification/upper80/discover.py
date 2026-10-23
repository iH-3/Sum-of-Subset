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
    for eq in hull.equations:
        if eq[3]<1e-7:continue
        cs=[Fraction(float(v/eq[3])).limit_denominator(1000) for v in eq[:4]]
        den=lcm(*(c.denominator for c in cs));cs=tuple(int(c*den) for c in cs)
        rhs=max(sum(c*v for c,v in zip(cs,pt)) for pt in points)
        coeff=tuple(c*rhs.denominator for c in cs)+(rhs.numerator,)
        common=gcd(*coeff);answer.add(tuple(c//common for c in coeff))
    return sorted(answer)


class Search:
    def __init__(self,st,j,positive=False,limits=None,use_planes=False,parent=None):
        self.st=st;self.j=j;self.positive=positive;self.limits=limits
        self.parent=parent
        prior=exact.inherited(dict(st=st,j=j,positive=positive,limits=limits,premise=parent)) if parent else None
        self.initial=8 if m.is_ownerless(st) else 0
        self.e=prior['credit'] if prior else self.initial
        self.use_planes=use_planes;p.USE_PLANES=use_planes;p.PLANE_GENERATOR=planes;p.SOURCE_TAIL_RANKS=True;p.SHARP_PLANES=True;p.SIDE_PLANES=True;p.TRIM_SOURCE=True;p.POINT_OVERLAP=True
        p.USED_PLANES=set();self.plane_keys=p.USED_PLANES
        self.names,self.rows,self.eqs=p.build(st,j,positive,self.e,limits)
        self.edges=p.build.last_edges;self.ret=p.build.last_retained
        self.trace=[];self.low=set();self.high=set();self.cuts=set();self.calls=0;self.constants=dict(p.build.last_compression);self.alpha_done=False;self.alpha_tail_done=False;self.ownerless_done=False;self.point_hits={};self.point_groups={};self.extended_hits={};self.trim_pairs=set(tuple(x) for x in prior.get('trim_pairs',[])) if prior else set()
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
        for side in 'st':
            lower=(limits or {}).get('B'+side,(4,10))[0]
            if lower>=5:
                self.rows.extend(exact.quartet_rows(side,lower));self.trace.append(dict(kind='quartet_fringe',side=side,lower=lower))

        self.rows.extend(exact.source_maximum_overlap_rows());self.trace.append(dict(kind='source_maximum_overlap'))
        self.rows.extend(exact.source_gap_inventory_rows());self.trace.append(dict(kind='source_gap_inventory'))
        self.rows.append(exact.trim_hull_row(len(self.trim_pairs)));self.trace.append(dict(kind='source_trim_hull'))

    def matrices(self):
        names=self.names
        self.A=np.array([[row.get(k,0) for k in names] for row,_,_ in self.rows],float)
        self.b=np.array([b for _,b,_ in self.rows],float)
        self.E=np.array([[row.get(k,0) for k in names] for row,_,_ in self.eqs],float)
        self.f=np.array([b for _,b,_ in self.eqs],float)
        self.rsi=[max(1,*[abs(v) for v in row.values()]) for row,_,_ in self.rows]
        self.esi=[max(1,*[abs(v) for v in row.values()]) for row,_,_ in self.eqs]
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
        counts={i:exact.point_overlap_count(self.point_hits.get(i,set()),self.point_groups.get(i,{}),self.extended_hits.get(i,{})) for i in weights}
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
        if key in self.cuts or sum(c*x[k] for k,c in row[0].items())<=row[1]+1e-7:return False
        self.rows.append(row);self.cuts.add(key)
        self.trace.append(dict(kind='forest',edges=chosen,roots=roots,e=self.e,constants=constants,point_edges=point_edges))
        return True

    def lp(self,target=None):
        for iteration in range(100):
            self.matrices();self.calls+=1
            c=np.array([-target.get(k,0) for k in self.names],float) if target else np.zeros(len(self.names))
            rr=linprog(c,A_ub=self.A,b_ub=self.b,A_eq=self.E,b_eq=self.f,bounds=(0,None),method='highs')
            if rr.status!=0:return rr
            if not self.cut(dict(zip(self.names,rr.x))):return rr
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

    def run(self):
        forms=m.fixed_forms()
        for cycle in range(63):
            rr=self.lp()
            if rr.status==2:return self.final()
            if rr.status!=0:raise ValueError(rr.message)
            point=dict(zip(self.names,rr.x));changed=False
            for label,form in forms.items():
                if label in self.low|self.high:continue
                value=sum(c*point[k] for k,c in form.items())
                if value<=1e-6:target=form;kind='low'
                elif value>=point['Ss' if '+' in label else 'St']+1e-6:
                    target=m.add((-1,form),(1,m.var('Ss' if '+' in label else 'St')));kind='high'
                else:continue
                rr=self.lp(target)
                if rr.status==2:return self.final()
                if rr.status!=0:raise ValueError(rr.message)
                if rr.fun < (-1e-7 if kind=='low' else 1e-7):continue
                cert=self.reconstruct(rr,target,strict=kind=='high')
                if cert is None:continue
                self.trace.append(dict(kind=kind,label=label,certificate=cert))
                (self.low if kind=='low' else self.high).add(label)
                self.rows.append((target,0 if kind=='low' or 3 in self.st.values() else -1,'proved '+kind.upper()+' '+label))
                changed=True
            next_e=exact.credit(self.low,self.high,self.initial)
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
                    rr=self.lp(target)
                    if rr.status==2:return self.final()
                    if rr.status!=0 or rr.fun<-1e-7:continue
                    cert=self.reconstruct(rr,target,strict=False)
                    if cert is None:continue
                    self.trace.append(dict(kind='tail_low',side=side,label=label,certificate=cert))
                    self.tail_low[side].add(label);self.rows.append((target,0,'proved tail LOW '+label));changed=True
                changed=tail_credit() or changed
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
                        rr=self.lp(target)
                        if rr.status==2:return self.final()
                        if rr.status!=0 or rr.fun<-1e-7:continue
                        cert=self.reconstruct(rr,target,strict=False)
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
                        rr=self.lp(guard)
                        if rr.status==2:return self.final()
                        if rr.status!=0 or rr.fun<-1e-7:continue
                        cert=self.reconstruct(rr,guard,strict=False)
                        if cert is None:continue
                        self.trace.append(dict(kind='trim_hull_pair',side=side,pair=pair,certificate=cert))
                        self.rows.append((guard,0,'proved trimmed hull pair'));self.trim_pairs.add(key)
                        self.rows.append(exact.trim_hull_row(len(self.trim_pairs)));changed=True
            if not changed and not self.use_planes:
                self.point=point;return False
            if not changed:
                for edge,(_,_,gap) in enumerate(self.edges):
                    for q in (2,4,3,1):
                        for tag in exact.extended_tags(q):
                            if tag in self.extended_hits.get(edge,{}).get(q,set()):continue
                            guards=exact.extended_guards(gap,q,tag)
                            if any(sum(c*point[k] for k,c in guard.items())>1e-7 for guard in guards):continue
                            certificates=[]
                            for guard in guards:
                                rr=self.lp(guard)
                                if rr.status==2:return self.final()
                                if rr.status!=0 or rr.fun<-1e-7:break
                                cert=self.reconstruct(rr,guard,strict=False)
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
                            rr=self.lp(guard)
                            if rr.status==2:return self.final()
                            if rr.status!=0 or rr.fun<-1e-7:break
                            cert=self.reconstruct(rr,guard,strict=False)
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
                if not changed:self.point=point;return False
        raise ValueError('Fixed credit iteration did not settle')

    def record(self):
        rec=dict(st=self.st,j=self.j,positive=self.positive,limits=self.limits,trace=self.trace,source_tail_ranks=True,sharp_planes=True,side_planes=True,trim_source=True,point_overlap=True)
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
