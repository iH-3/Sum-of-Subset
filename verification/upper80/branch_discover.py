# RESEARCH PROTOTYPE: no global bound is certified by this file.
"""Optional exact-proof-producing endpoint branch search."""
from pathlib import Path
import json,sys,time,math,hashlib,gzip
import model as m
from discover import Search
import exact


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
            cached=json.loads(gzip.decompress(checkpoint.read_bytes()))
            if cached['closed']:
                rec=cached['record'];exact.replay(rec);i=len(self.leaves);self.leaves.append(rec);return {'leaf':i}
            parent=cached['record']
        s=Search(self.st,self.j,self.positive,limits,use_planes=True,parent=parent)
        numerical=None
        try:closed=s.run()
        except ValueError as exc:
            checkpoint.write_bytes(gzip.compress(json.dumps(dict(closed=False,record=s.record()),separators=(',',':')).encode(),mtime=0))
            if 'Exact contradiction reconstruction failed' not in str(exc) and 'HiGHS' not in str(exc):raise
            # Infeasibility is not accepted without an exact certificate.
            # Partition an integer parameter and try both actual domains.
            closed=False;numerical=str(exc)
        checkpoint.write_bytes(gzip.compress(json.dumps(dict(closed=closed,record=s.record()),separators=(',',':')).encode(),mtime=0))
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
        for side in 'st':
            for first in ('alpha','beta'):
                for second in m.CHAIN:
                    a,b=first+side,second+side;key='order:'+first+':'+second+':'+side
                    if self.st.get(a)!=1 or self.st.get(b)!=1 or key in limits:continue
                    if any({a,b}=={aa,bb} for aa,bb,gap in s.edges):continue
                    difference=m.add((1,Z[a]),(-1,Z[b]));distance=abs(sum(c*x[k] for k,c in difference.items()))
                    if distance<x['FD']-1e-6:candidates.append((100+x['FD']-distance,key,0))
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
                if value<=1e-7:candidates.append((1100+min(100,-value)/100,name,0))
        for edge,(a,b,gap) in enumerate(s.edges):
            distance=sum(c*x[k] for k,c in gap.items())
            if distance<1e-7:continue
            for q in (2,4,3,1):
                for tag in exact.extended_tags(q):
                    if tag in s.extended_hits.get(edge,{}).get(q,set()):continue
                    guards=exact.extended_guards(gap,q,tag);values=[sum(c*x[k] for k,c in guard.items()) for guard in guards]
                    if max(values)>1e-7:continue
                    for guard_index in sorted(range(2),key=lambda i:values[i],reverse=True):
                        name='extended_hit:'+str(q)+':'+tag+':'+a+':'+b+':'+str(guard_index)
                        if name in limits:continue
                        candidates.append((90+q-min(20,-values[guard_index])/100,name,0));break
            for tag in exact.POINT_TAGS:
                if tag in s.point_hits.get(edge,set()):continue
                guards=exact.point_overlap_guards(gap,tag)
                values=[sum(c*x[k] for k,c in guard.items()) for guard in guards]
                if max(values)>1e-7:continue
                for guard_index in sorted(range(2),key=lambda i:values[i],reverse=True):
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
        default=(0,1) if name.startswith(('order:','compression:','diameter:','hit:','trim_pair:','extended_hit:')) else (4,10) if name in ('Bs','Bt') else (0,17) if name=='rank_k' else ((1,7) if self.positive else (0,0)) if name=='hole_W' else (0,72)
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
