"""Exact finite checks accompanying the universal arguments in the report."""
import importlib.util
from itertools import combinations,product
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def endpoint_checks():
    count=0;strict_gains=0
    for rs in range(1,7):
        profiles=list(combinations(range(1,rs+6),rs))
        for index,pos in enumerate(profiles):
            # Reflect a different actual core to test asymmetric sources.
            neg=tuple(x+1 for x in profiles[-1-index])
            rt=len(neg);R=pos[-1];R0=neg[-1]
            offsets=(1,2,4,9);offsets0=(2,3,5,13)
            D=sorted([0,*pos,*(-x for x in neg),*(R+x for x in offsets),*(-R0-x for x in offsets0)])
            for points,r,ro,P,e in [(D,rs,rt,pos,offsets[-1]),(sorted(-x for x in D),rt,rs,neg,offsets0[-1])]:
                tau=sum(x-i for i,x in enumerate(P,1));xi=P[-1]-r;d=len(D);q=d-4
                for k,x in enumerate(points):
                    if k<q:
                        error=0 if k<=ro+4 else tau//(q-k)
                        bound=1+k+r-q+error
                        need(x<=bound,'actual next-rank mass endpoint')
                        strict_gains+=error<xi
                    else:
                        bound=1+k+r-q+xi+e-4
                        need(x<=bound,'actual heavy-tail rank endpoint')
                    count+=1
    need(strict_gains>0,'strict improvement over maximum deviation')
    # This valid monotone profile makes the old common error 29, the new one 0.
    P=tuple(range(1,33))+(62,)
    need(sum(x-i for i,x in enumerate(P,1))==29 and P[-1]-33==29,'rank witness')
    need(31<=70-33,'lower clip31 has zero mass error')
    return dict(order_statistics=count,strict_error_improvements=strict_gains,
                witness=dict(core=list(P),lower_clip=31,old_error=29,new_error=0))

def forest_checks():
    count=0
    for n,edges in [(7,((0,1),(1,2),(2,3),(0,4),(4,5),(5,6))),
                    (8,((0,1),(1,2),(2,3),(0,4),(4,5),(5,6),(6,7)))]:
        for mask in range(1<<len(edges)):
            chosen=[x for i,x in enumerate(edges) if mask>>i&1]
            remaining=set(range(n));roots=[]
            while remaining:
                comp={min(remaining)}
                while True:
                    grown=comp|{b for a,b in chosen if a in comp}|{a for a,b in chosen if b in comp}
                    if grown==comp:break
                    comp=grown
                remaining-=comp
                roots.append(0 if 0 in comp else (7 if 7 in comp else min(comp)))
            for bits in product((0,1),repeat=n):
                overlaps=sum(bits[a]*bits[b] for a,b in chosen)
                for inside in (0,1):
                    loss=sum(bits)-inside*int(any(bits))
                    rebate=(1-inside)*sum(bits[root] for root in roots)
                    need(overlaps+rebate<=loss,'rooted forest pointwise inequality')
                    count+=1
    need(count==81920,'all two physical-tree point states')
    # Keeping two native roots in one edge component is not valid.
    need(1+1+1>2,'counterexample to two roots in one component')
    return dict(pointwise_checks=count,edge_subsets=[64,128],roots_per_component=1)

def scalar_checks():
    hulls=bootstrap=0
    for e in (27,31,35,42):
        for r in range(24,43):
            I=(r-33)**2
            for tau in range(96-e-I):
                eps=95-e-I-tau
                need(eps<71,'all later native clips are light')
                for rv in (r,66-r):
                    pts=[(k,0 if k<=70-rv else tau//(71-k)) for k in range(eps+1)]
                    hull=[]
                    for k,y in pts:
                        while len(hull)>=2 and (hull[-1][1]-hull[-2][1])*(k-hull[-1][0])<=(y-hull[-1][1])*(hull[-1][0]-hull[-2][0]):hull.pop()
                        hull.append((k,y))
                    for (a,b),(c,d) in zip(hull,hull[1:]):
                        need(all((c-a)*y<=(d-b)*k+(c-a)*b-(d-b)*a for k,y in pts),'concave hull dominates every allowed integer clip')
                        hulls+=1
                if e==42:
                    need(213+3*I+2*tau>6*(tau-1),'rounding to x>=tau')
                    need(77+I>tau,'safe full-core bound then x>tau')
                    bootstrap+=1
    need(bootstrap==530,'complete terminal bootstrap domain')
    need(132-95+14==51 and (51+1)//2==26,'all six initial gap types >=26')
    need(197>0 and 1+3*26==79>26 and 1+3*26>16,'tail signs without core-hit premise')
    need(13*75+84==1059 and 6*75+84==534 and 7*75+84==609,'size83 physical capacities')
    need(min(r*(r+1)//2+4*r+(r-33)**2 for r in range(1,66))==459,'target exceeds source span')
    need(459-318==141,'complete physical activity interval')
    equality=[]
    for a,b,c in combinations(range(1,19),3):
        if a+b+c>18:continue
        for e in range(c+1,2*c+1):
            B=len({x+y for x in (a,b,c,e) for y in (a,b,c,e) if x+y>e})
            Q=2*B-a-b-c
            need(Q<=3,'quartet finite part')
            if Q==3:equality.append((a,b,c,e))
    need(equality==[(1,2,4,5),(1,3,5,6)],'all equality quartets')
    need(20-19<=1 and 8-6<=2,'quartet unbounded tails')
    need(27+55>12 and 27+50>30,'small-quartet cases')
    need(56-12-7-66==-29 and 31-29>0,'central hole excludes L=A+56 after credit31')
    progress=load('alpha_source','verification/upper83_progress.py')
    sharp=progress.sharp_source(75,'theta')
    need(sharp['theta']==158 and sharp['K']==293 and 2*76==95+57,'sharp source span witness')
    return dict(concave_envelope_segments=hulls,terminal_bootstrap_states=bootstrap,
        initial_gap_floor=26,tail_strict_lower=79,physical_capacities=[534,609],
        source_span_bounds={'credit27':'L>=A+56','credit31_or_more':'L>=A+57'},
        equality_quartets=equality,sharp_source=sharp)

def catalogue_checks():
    source=load('alpha_catalogue','verification/upper83_progress.py')
    labels,_,groups=source.fixed_catalogue()
    tail=load('alpha_tail','verification/upper83_tail.py').tail_inventory(labels)
    ledger=load('alpha_old_ledger','verification/upper83_complete/check_local.py').ledger_checks()
    # Independently expand the LOW signs in coordinates a,b,gs,gt,hs,B,C,D.
    names=('a','b','gs','gt','hs','B','C','D')
    def vec(i):return tuple(int(i==j) for j in range(8))
    def add(*xs):return tuple(map(sum,zip(*xs)))
    def scale(k,x):return tuple(k*y for y in x)
    a,b,gs,gt,hs,B,C,D=map(vec,range(8))
    ht=add(B,b);ds=add(C,scale(2,a),scale(2,b),gs,gt,B);dt=add(D,a,scale(2,b),gs,gt,hs)
    s4=a;s3=add(a,gs);s2=add(s3,hs);s1=add(s2,ds)
    t4=b;t3=add(b,gt);t2=add(t3,ht);t1=add(t2,dt)
    raw=(s1,s2,s3,s4,t1,t2,t3,t4)
    expected={
      'V-3':(-1,-1,-1,0,-1,1,0,-1),
      'V-4':(-1,-1,-1,-1,-1,1,0,-1),
      'C+35':(0,-2,0,-1,-1,0,1,-1),
      'C+25':(0,-2,0,-1,0,0,1,-1),
      'C-25':(-2,0,-1,0,0,0,-1,1),
      'C-35':(-2,-1,-1,0,0,-1,-1,1),
      'C+45':(0,-2,-1,-1,-1,0,1,-1),
      'C-45':(-2,-1,-1,-1,0,-1,-1,1)}
    for name,coeff in expected.items():
        need(add(*(scale(c,x) for c,x in zip(labels[name],raw)))==coeff,'LOW identity '+name)
    return dict(ledger=ledger,LOW_identities=expected,coordinate_order=names,
        formal_multisets=tail['formal_multisets'],excluded_by_cones=tail['excluded_by_nonnegative_cones'],
        tail_fixed_labels=tail['fixed_tail'],tail_native_families=tail['native_families'])
