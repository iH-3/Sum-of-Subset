# RESEARCH PROTOTYPE: no global bound is certified by this file.
"""Optional exact-proof-producing endpoint branch search."""
from pathlib import Path
import json,sys,time,math,hashlib,gzip
import model as m
from discover import Search,guard_key
import exact

_RECORD_POOL={}
def intern_record(record):
    """Share repeated checkpoint premises; this is discovery-only storage."""
    parent=record.get('premise');parent_key=None
    if parent is not None:parent_key,parent=intern_record(parent)
    body={key:value for key,value in record.items() if key!='premise'}
    key=hashlib.sha256(json.dumps([body,parent_key],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if key not in _RECORD_POOL:
        if parent is not None:body['premise']=parent
        _RECORD_POOL[key]=body
    return key,_RECORD_POOL[key]

def save_checkpoint(path,record,closed):
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_bytes(gzip.compress(json.dumps(dict(closed=closed,record=record),separators=(',',':')).encode(),mtime=0))
    temporary.replace(path)


class Branch:
    def __init__(self,st,j,positive):
        self.st=st;self.j=j;self.positive=positive;self.leaves=[];self.opens=[];self.count=0;self.start=time.time()
        ident=hashlib.sha256(json.dumps([st,j,positive],sort_keys=True).encode()).hexdigest()[:16]
        self.prefix_dir=Path(__file__).resolve().parents[2]/'.work/upper80'/'prefixes'/ident
        self.prefix_dir.mkdir(parents=True,exist_ok=True)

    def visit(self,limits,depth=0,parent=None):
        self.count+=1;stamp=hashlib.sha256(json.dumps(limits,sort_keys=True).encode()).hexdigest()[:16]
        checkpoint=self.prefix_dir/(stamp+'.json.gz')
        if checkpoint.exists():
            try:cached=json.loads(gzip.decompress(checkpoint.read_bytes()))
            except (EOFError,gzip.BadGzipFile,json.JSONDecodeError):
                checkpoint.rename(checkpoint.with_suffix(checkpoint.suffix+'.unreadable'))
                print('INCOMPLETE CHECKPOINT RETAINED',checkpoint.name,flush=True)
            else:
                cached['record']=intern_record(cached['record'])[1]
                if cached['closed']:
                    rec=cached['record'];exact.replay(rec);i=len(self.leaves);self.leaves.append(rec);return {'leaf':i}
                parent=cached['record']
        s=Search(self.st,self.j,self.positive,limits,use_planes=True,parent=parent)
        numerical=None
        try:closed=s.run()
        except ValueError as exc:
            save_checkpoint(checkpoint,s.record(),False)
            if 'Exact contradiction reconstruction failed' not in str(exc) and 'HiGHS' not in str(exc):raise
            # Infeasibility is not accepted without an exact certificate.
            # Partition an integer parameter and try both actual domains.
            closed=False;numerical=str(exc)
        save_checkpoint(checkpoint,s.record(),closed)
        if closed:
            rec=s.record();exact.replay(rec);i=len(self.leaves);self.leaves.append(rec)
            return {'leaf':i}
        if numerical:
            options=[('rank_k',(0,17)),('hole_W',(1,7) if self.positive else (0,0)),('Bs',(4,10)),('Bt',(4,10))]
            options += [(typ+name,(0,72)) for name,status in self.st.items() if status==1 for typ in 'lu']
            for name,default in options:
                lo,hi=limits.get(name,default)
                if lo<hi:break
            else:raise ValueError('No integer split remains after numerical reconstruction failure')
            mid=lo if name=='rank_k' else 68 if lo<=68<hi else (lo+hi)//2
            print('NUMERICAL SPLIT',self.count,depth,name,mid,'credit',s.e,flush=True)
            left=dict(limits);left[name]=(lo,mid);right=dict(limits);right[name]=(mid+1,hi);premise=s.record()
            return dict(variable=name,threshold=mid,left=self.visit(left,depth+1,premise),right=self.visit(right,depth+1,premise))
        x=s.point;Z=m.build.last_Z;candidates=[]
        known=set(s.known_nonpositive)|{guard_key(row) for row,rhs,_ in s.rows if rhs<=0}

        for violation,guard in getattr(s,'full_cover_failures',[]):
            normalized=guard_key(guard);name='linear_cut:'+json.dumps(dict(normalized),sort_keys=True,separators=(',',':'))
            if name not in limits and normalized not in known:candidates.append((6000+min(100,violation)/100,name,0))


        for violation,guard in getattr(s,'union_failures',[]):
            normalized=guard_key(guard);name='linear_cut:'+json.dumps(dict(normalized),sort_keys=True,separators=(',',':'))
            if name not in limits and normalized not in known:candidates.append((4000+min(100,violation),name,0))
        for violation,guard in getattr(s,'core_tail_failures',[]):
            normalized=guard_key(guard);name='linear_cut:'+json.dumps(dict(normalized),sort_keys=True,separators=(',',':'))
            if name not in limits and normalized not in known:candidates.append((4500+min(100,violation),name,0))

        for violation,guard in getattr(s,'capacity_failures',[]):
            normalized=guard_key(guard);name='linear_cut:'+json.dumps(dict(normalized),sort_keys=True,separators=(',',':'))
            if name not in limits and normalized not in known:candidates.append((4300+min(100,violation),name,0))

        for length,guard in getattr(s,'fixed_known_failures',[]):
            normalized=guard_key(guard);name='linear_cut:'+json.dumps(dict(normalized),sort_keys=True,separators=(',',':'))
            if name not in limits and normalized not in known:candidates.append((1600-min(99,length),name,0))

        for guard in getattr(s,'ordered_cover_failures',[]):
            normalized=guard_key(guard);name='linear_cut:'+json.dumps(dict(normalized),sort_keys=True,separators=(',',':'))
            if name not in limits and normalized not in known:candidates.append((4700,name,0))
        for guard in getattr(s,'shifted_cover_failures',[]):
            normalized=guard_key(guard);name='linear_cut:'+json.dumps(dict(normalized),sort_keys=True,separators=(',',':'))
            if name not in limits and normalized not in known:candidates.append((4900,name,0))

        if getattr(self,'integer_first',False) and self.j>=3 and 3 not in self.st.values():
            for name in ('F','FD',*('GB'+str(i) for i in range(1,11)),'phicores','phicoret','phisources','phisourcet','ts','tt','xs','xt','as','bs','cs','es','at','bt','ct','et','Xs','Xt','gs','gt','hs','ht','ds','dt','K','delta'):
                value=x[name];cut=math.floor(value)
                key='integer_cut:'+name+':'+str(cut)
                fraction=value-cut
                if key not in limits and 1e-6<fraction<1-1e-6:candidates.append((getattr(self,'integer_priority',3000)+min(fraction,1-fraction),key,0))

        if s.coverage_probes:
            import cover_geometry as coverage
            for probe_key,state in s.coverage_probes.items():
                side,index=probe_key.split(':');index=int(index);components=coverage.catalogue(self.st,s.Z,side)
                remaining=set(range(len(components)))-state['excluded']
                if len(remaining)<=1:continue
                for component in remaining:
                    for direction in (0,1):
                        guard=coverage.exclusion(components,index,component,direction,s.coverage_width)
                        name='coverage:'+side+':'+str(index)+':'+str(component)+':'+str(direction)
                        if s.coverage_width!=(8 if self.positive else 1):
                            name='linear_cut:'+json.dumps(dict(guard_key(guard)),sort_keys=True,separators=(',',':'))
                        if name in limits or guard_key(guard) in known:continue
                        value=sum(c*x[k] for k,c in guard.items())
                        if value<=1e-7:candidates.append((2200-10*len(remaining)+min(20,-value)/100,name,0))

        if self.j==6:
            lo,hi=limits.get('tau_total',exact.integer_source_domain('tau_total',self.j,self.positive))
            if lo<hi:
                value=x['ts']+x['tt']
                mid=lo if hi-lo<=10 else min(hi-1,max(lo,int(math.floor(value+1e-7))))
                candidates.append((1500,'tau_total',mid))

        for name in ('xs','xt','ts','tt','delta','K',*(a+b for a in 'abce' for b in 'st')):
            lo,hi=limits.get(name,exact.integer_source_domain(name,self.j,self.positive));value=x[name]
            if lo<hi and abs(value-round(value))>1e-6:
                candidates.append((1200 if name[0]=='x' else 1000 if name in ('ts','tt','delta','K') else 950,name,min(hi-1,max(lo,int(math.floor(value))))))

        if self.j>=3 and 3 not in self.st.values():
            forms=m.fixed_forms()
            for label in sorted(set(forms)-s.low-s.high-s.covered):
                side='s' if '+' in label else 't'
                if sum(c*x[k] for k,c in forms[label].items())<1-1e-7:continue
                for resource in [v for v in s.ret if v[-1]==side]+['L'+side]:
                    for q in (2,4,5,3,1):
                        for witness in ((None,) if resource[0]!='L' else exact.LEADING_WITNESSES):
                            guards=exact.fixed_cover_guards(label,resource,q,witness,s.Z)
                            guards.append(m.add((1,{'ONE':1}),(-1,forms[label])))
                            values=[sum(c*x[k] for k,c in guard.items()) for guard in guards]
                            if max(values)>1e-7:continue
                            unknown=[i for i in range(len(guards)) if guard_key(guards[i]) not in known]
                            for i in sorted(unknown,key=lambda i:values[i],reverse=True):
                                name='fixed_hit:'+label+':'+resource+':'+str(q)+':'+(witness or '-')+':'+str(i)
                                if name not in limits:candidates.append((1300-120*(len(unknown)-1)-min(100,-values[i])/100,name,0))
                                break

        if self.j>=3 and 3 not in self.st.values():
            forms=m.fixed_forms();remaining=sorted(set(forms)-s.low-s.high-s.covered)
            for ai,first in enumerate(remaining):
                for second in remaining[ai+1:]:
                    pair=(first,second)
                    if pair in s.fixed_pairs or ('+' in first)!=('+' in second):continue
                    if exact.credit(s.low,s.high,s.initial,s.covered,s.covered_positive,s.fixed_pairs|{pair})<=s.e:continue
                    side='s' if '+' in first else 't'
                    for resource in (v for v in s.ret if v[-1]==side):
                        for core_side in 'st':
                            a,b=first,second
                            if (sum(c*x[k] for k,c in forms[a].items())>sum(c*x[k] for k,c in forms[b].items()))==(core_side==side):a,b=b,a
                            guards=exact.fixed_probe_pair_guards(a,b,resource,core_side,s.Z)
                            values=[sum(c*x[k] for k,c in guard.items()) for guard in guards]
                            if max(values)>1e-7:continue
                            unknown=[i for i in range(len(guards)) if guard_key(guards[i]) not in known]
                            for i in sorted(unknown,key=lambda i:values[i],reverse=True):
                                name='fixed_probe_hit:'+a+':'+b+':'+resource+':'+core_side+':'+str(i)
                                if name not in limits:candidates.append((1350-120*(len(unknown)-1)-min(100,-values[i])/100,name,0))
                                break

        for side in 'st':
            for first in ('alpha','beta'):
                for second in m.CHAIN:
                    a,b=first+side,second+side;key='order:'+first+':'+second+':'+side
                    if self.st.get(a)!=1 or self.st.get(b)!=1 or key in limits:continue
                    if any({a,b}=={aa,bb} for aa,bb,gap in s.edges):continue
                    difference=m.add((1,Z[a]),(-1,Z[b]));signed=sum(c*x[k] for k,c in difference.items());distance=abs(signed)
                    gap=difference if signed>=0 else {k:-v for k,v in difference.items()}
                    potential=0
                    for q in (2,4,3,1):
                        potential=max(potential,sum(all(sum(c*x[k] for k,c in guard.items())<=1e-7 for guard in exact.extended_guards(gap,q,tag)) for tag in exact.extended_tags(q)))
                    if potential>max(0,x['FD']-distance)+1e-7:candidates.append((1400+potential,key,0))
                    elif distance<x['FD']-1e-6:candidates.append((100+x['FD']-distance,key,0))
        for side in 'st':
            name='B'+side;lo,hi=limits.get(name,(4,10))
            if lo<=4<hi and x[name]>4+1e-6 and x['e'+side]>2*x['c'+side]-1+1e-6:
                candidates.append((1000+x['e'+side]-2*x['c'+side],name,4))
            for threshold in (6,8,9,10):
                if not lo<threshold<=hi or x[name]<=threshold-1+1e-6:continue
                violation=max((sum(c*x[k] for k,c in row.items())-rhs for row,rhs,_ in exact.quartet_rows(side,threshold)),default=0)
                if violation>1e-6:candidates.append((900+violation,name,threshold-1))
        for name,value in x.items():
            if name[:1] not in ('l','u') or self.st.get(name[1:])!=1:continue
            lo,hi=limits.get(name,(0,72))
            if lo==hi:continue
            side=name[-1];other='t' if side=='s' else 's'
            rv=32-x['rank_k'] if side=='s' else 32+x['rank_k'];ro=64-rv
            center=sum(c*x[k] for k,c in Z[name[1:]].items())
            if name[0]=='l':rank=rv;needed=69-rv-center-value;xi=x['x'+side]
            else:rank=ro;needed=center-x['S'+side]-value-ro+68;xi=x['x'+other]
            tau=x['ts']+x['tt']
            error=0 if value<=68-rank else min(xi,tau/(69-value)) if value<69 else 1e9
            violation=needed-error
            if violation>1e-6:
                mid=68 if lo<=68<hi else min(hi-1,max(lo,int(math.floor(value))))
                candidates.append((violation,name,mid))
        for side in 'st':
            for pair in exact.TRIM_PAIRS:
                key=(side,*pair);name='trim_pair:'+':'.join(key)
                if key in s.trim_pairs or name in limits:continue
                guard=exact.trim_pair_guard(side,pair);value=sum(c*x[k] for k,c in guard.items())
                if value<=1e-7 and guard_key(guard) not in known:candidates.append((1100+min(100,-value)/100,name,0))
        for gap_key in exact.SUMSET_GAPS:
            side,other,lower,upper,qs,qo=exact.sumset_gap_data(gap_key)
            length=m.add((1,upper),(-1,lower),(-1,qs),(-1,qo),(-1,{'ONE':1}))
            if sum(c*x[k] for k,c in length.items())<=0:continue
            for pair in exact.sumset_gap_pairs(gap_key):
                if pair in s.sumset_excluded.get(gap_key,set()):continue
                for index,guard in enumerate(exact.sumset_gap_guards(gap_key,pair)):
                    name='sumset_pair:'+gap_key+':'+':'.join(pair)+':'+str(index)
                    if name in limits or guard_key(guard) in known:continue
                    value=sum(c*x[k] for k,c in guard.items())
                    if value<=1e-7:candidates.append((600+min(100,-value)/100,name,0))
        for edge,(a,b,gap) in enumerate(s.edges):
            distance=sum(c*x[k] for k,c in gap.items())
            if distance<1e-7:continue
            if a in ('Ls','Lt'):
                side,other,right,_=exact.leading_geometry((a,b,gap))
                for q in (2,4,5,3,1):
                    known_hits=s.leading_hits.get(edge,set()) if q==5 else s.leading_extended.get(edge,{}).get(q,set())
                    for tag in exact.leading_tags(q):
                        if tag[0]!=(other if right else side) or tag in known_hits:continue
                        options=[]
                        for witness in exact.LEADING_WITNESSES:
                            guards=exact.leading_point_guards((a,b,gap),tag,witness,q)
                            values=[sum(c*x[k] for k,c in guard.items()) for guard in guards]
                            if max(values)>1e-7:continue
                            for guard_index in sorted(range(len(guards)),key=lambda i:values[i],reverse=True):
                                if guard_key(guards[guard_index]) in known:continue
                                name='leading_hit:'+str(q)+':'+tag+':'+witness+':'+a+':'+b+':'+str(guard_index)
                                if name in limits:continue
                                options.append((500-min(100,-values[guard_index])/100,name,0));break
                        if options:candidates.append(max(options))
            for q in (2,4,3,1):
                for tag in exact.extended_tags(q):
                    if tag in s.extended_hits.get(edge,{}).get(q,set()):continue
                    guards=exact.extended_guards(gap,q,tag);values=[sum(c*x[k] for k,c in guard.items()) for guard in guards]
                    if max(values)>1e-7:continue
                    for guard_index in sorted(range(2),key=lambda i:values[i],reverse=True):
                        if guard_key(guards[guard_index]) in known:continue
                        name='extended_hit:'+str(q)+':'+tag+':'+a+':'+b+':'+str(guard_index)
                        if name in limits:continue
                        candidates.append((90+q-min(20,-values[guard_index])/100,name,0));break
            for tag in exact.POINT_TAGS:
                if tag in s.point_hits.get(edge,set()):continue
                guards=exact.point_overlap_guards(gap,tag)
                values=[sum(c*x[k] for k,c in guard.items()) for guard in guards]
                if max(values)>1e-7:continue
                for guard_index in sorted(range(2),key=lambda i:values[i],reverse=True):
                    if guard_key(guards[guard_index]) in known:continue
                    name='hit:'+tag+':'+a+':'+b+':'+str(guard_index)
                    if name in limits:continue
                    candidates.append(((80 if tag[1]=='R' else 60)-min(20,-values[guard_index])/100,name,0));break
            for source in ('core','source','trim1','trim2','trim3'):
                n,span=exact.diameter_source(source);name='diameter:'+source+':'+a+':'+b
                if name in limits or n<=max(s.constants.get(edge,0),x['FD'])+1e-6 or distance>=n:continue
                if sum(c*x[k] for k,c in span.items())<2*distance:candidates.append((50+n-max(s.constants.get(edge,0),x['FD']),name,0))
            for source,n,mass in [('core',65,x['ts']+x['tt']),('source',73,x['TD'])]+[('trim'+str(q),73-2*q,x['TD'+str(q)]) for q in (1,2,3)]:
                k=max(0,int(math.floor(mass/distance+1e-8)))
                name='compression:'+source+':'+a+':'+b+':'+str(k)
                if name in limits or n-k<=max(s.constants.get(edge,0),x['FD'])+1e-6:continue
                candidates.append((30+n-k-max(s.constants.get(edge,0),x['FD']),name,0))
        if not candidates:
            heavy=[(typ+name,(0,72)) for name,status in self.st.items() if status==1 for typ in 'lu'
                   if (limits.get(typ+name,(0,72))[0]>=69 and limits.get(typ+name,(0,72))[0]<limits.get(typ+name,(0,72))[1])]
            for name,default in heavy+[('Bs',(4,10)),('Bt',(4,10)),('rank_k',(0,17)),('hole_W',(1,7) if self.positive else (0,0))]:
                lo,hi=limits.get(name,default)
                if lo==hi:continue
                mid=min(hi-1,max(lo,int(math.floor(x[name]))))
                candidates.append((1,name,mid));break
            else:
                i=len(self.opens);self.opens.append(dict(limits=limits,point=x,credit=s.e))
                print('OPEN LEAF',self.j,depth,'credit',s.e,flush=True)
                return {'open':i}
        _,name,mid=max(candidates)
        default=(0,1) if name.startswith(('linear_cut:','integer_cut:','order:','compression:','diameter:','hit:','trim_pair:','extended_hit:','leading_hit:','sumset_pair:','fixed_hit:','fixed_probe_hit:','coverage:')) else exact.integer_source_domain(name,self.j,self.positive) if exact.integer_source_domain(name,self.j,self.positive) is not None else (4,10) if name in ('Bs','Bt') else (0,17) if name=='rank_k' else ((1,7) if self.positive else (0,0)) if name=='hole_W' else (0,72)
        lo,hi=limits.get(name,default)
        print('split',self.count,depth,name,mid,'credit',s.e,'seconds',round(time.time()-self.start,1),flush=True)
        left=dict(limits);left[name]=(lo,mid);right=dict(limits);right[name]=(mid+1,hi)
        premise=s.record()
        return dict(variable=name,threshold=mid,left=self.visit(left,depth+1,premise),right=self.visit(right,depth+1,premise))


if __name__=='__main__':
    j=int(sys.argv[1]);i=int(sys.argv[2]);positive=len(sys.argv)>3 and sys.argv[3]=='positive'
    st=([*m.patterns(j),*m.partial_patterns(j)])[i];obj=Branch(st,j,positive);tree=obj.visit({})
    path=Path(__file__).resolve().parents[2]/'.work/upper80'/f'exact_branch_{j}_{i}_{int(positive)}.json'
    path.write_text(json.dumps(dict(st=st,j=j,positive=positive,tree=tree,leaves=obj.leaves,open=obj.opens),separators=(',',':')))
    print('DONE',j,i,'nodes',obj.count,'leaves',len(obj.leaves),'open',len(obj.opens),flush=True)
