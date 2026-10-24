# RESEARCH PROTOTYPE: no global bound is certified by this file.
"""Necessary systems for the size81 exclusion. The written proof supplies structural applicability.
All arithmetic and verification paths in this module use the standard library.
"""
from collections import Counter
from itertools import product
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
from math import lcm
import importlib.util
import sys,json
ROOT=Path(__file__).resolve().parents[2]
def add(*args):
    result=Counter()
    for scale,row in args:
        for key,value in row.items():result[key]+=scale*value
    return dict(result)
def var(key):return {key:1}
spec=importlib.util.spec_from_file_location('catalogue82',ROOT/'verification/upper83_progress.py')
catalogue=importlib.util.module_from_spec(spec);spec.loader.exec_module(catalogue)
LABELS,_,GROUPS=catalogue.fixed_catalogue()
CHAIN=('P','C5','C6','C7','V','U','H','O')
PLANE_TABLE={}
DISABLE_PLANES=False

def need(ok,message):
    if not ok:raise ValueError(message)

def configure_planes(table):
    global PLANE_TABLE
    PLANE_TABLE=table
    free_planes.cache_clear();fixed_planes2.cache_clear()

def check_planes(kind,args):
    if DISABLE_PLANES:return ()
    key=kind+':'+','.join(map(str,args))
    need(key in PLANE_TABLE,'Missing endpoint planes '+key)
    planes=PLANE_TABLE[key]
    if kind=='free':
        r,j,I,e,lo,hi=args;cap=496-73*j-I;points=[]
        for k in range(lo,min(hi,cap-e)+1):
            for delta,tau in ((e+k,0),(cap,0),(e+k,cap-e-k)):
                error=(Fraction(0) if k<=68-r else Fraction(tau,69-k)) if k<69 else Fraction(651-73*j-I-delta)
                points.append((k,delta,tau,error))
    else:
        r,tau,j,I,e,lo,hi=args;cap=496-73*j-I-tau;points=[]
        for k in range(lo,hi+1):
            for delta in (e+k,cap):
                error=(0 if k<=68-r else tau//(69-k)) if k<69 else 651-73*j-I-delta
                points.append((k,delta,tau,error))
    for plane in planes:
        need(len(plane)==5 and all(type(v) is int for v in plane),'Plane type')
        need(plane[3]>0,'Plane error coefficient')
        need(all(sum(a*b for a,b in zip(plane[:4],point))<=plane[4] for point in points),'Invalid endpoint majorant')
    return tuple(tuple(p) for p in planes)

@lru_cache(None)
def free_planes(*args):return check_planes('free',args)
@lru_cache(None)
def fixed_planes2(*args):return check_planes('fixed',args)

def is_ownerless(st):
    return all(st[k+s]==(2 if k=='O' else 0) for s in 'st' for k in ('P','beta','O')) and sum(v==1 for v in st.values())==14

def patterns(j):
    sides=[]
    for a in range(9):
      for b in range(a,9):
        chain={k:(0 if i<a else 1 if i<b else 2) for i,k in enumerate(CHAIN)}
        for be in range(3):
          for al in range(be,3):
            if al>chain['H']:continue
            x=dict(chain,beta=be,alpha=al)
            sides.append(x)
    for s,t in product(sides,repeat=2):
      if sum(x==1 for x in [*s.values(),*t.values()])!=18-j:continue
      if s['P']==t['P']==1:continue
      if all(x[k]==1 for x in (s,t) for k in ('beta','C5')):continue
      if any(x['P']==x['beta']==y['C5']==1 for x,y in ((s,t),(t,s))):continue
      yield {k+side:v for side,x in [('s',s),('t',t)] for k,v in x.items()}

def residue_patterns():
    pats=set()
    for x,y,z in product(range(42),repeat=3):
      pat=tuple(t%42==0 for t in (x,y,z,x+y+z,x-y-z,x-2*y-2*z))
      if sum(w for w,ok in zip((2,2,2,2,1,1),pat) if not ok)<=8:pats.add(pat)
    return sorted(pats)

def partial_patterns(j):
    full=(True,)*6;pats=residue_patterns()
    side_patterns=[]
    for p,q in product(pats,repeat=2):
      if p==q==full:continue
      if sum(w for a in (p,q) for w,ok in zip((2,2,2,2,1,1),a) if not ok)>j+2:continue
      aligned={}
      for v,o,pat in [('s','t',p),('t','s',q)]:
        for ok,names0 in zip(pat,[(('H',v),('C5',o)),(('U',v),('C6',o)),(('V',v),('C7',o)),(('O',v),('P',o)),(('alpha',v),),(('beta',v),)]):
          for name,side in names0:aligned[name+side]=ok
      choices=[]
      for v in 'st':
        chain=[k for k in CHAIN if aligned[k+v]];allrows=[]
        for a in range(len(chain)+1):
          for b in range(a,len(chain)+1):
            row={k+v:3 for k in [*CHAIN,'alpha','beta']}
            row.update({k+v:(0 if i<a else 1 if i<b else 2) for i,k in enumerate(chain)})
            for be,al in product(range(3) if aligned['beta'+v] else [3],range(3) if aligned['alpha'+v] else [3]):
              rr=dict(row,**{'beta'+v:be,'alpha'+v:al})
              kk=[rr[k+v] for k in ('beta','alpha','H') if rr[k+v]!=3]
              if kk!=sorted(kk):continue
              allrows.append(rr)
        choices.append(allrows)
      for s,t in product(*choices):
        st=dict(s,**t)
        if sum(v==1 for v in st.values())!=18-j:continue
        if st['Ps']==st['Pt']==1:continue
        if all(st[k+v]==1 for v in 'st' for k in ('beta','C5')):continue
        if any(st['P'+v]==st['beta'+v]==st['C5'+o]==1 for v,o in [('s','t'),('t','s')]):continue
        yield st

def base_build(st,j,r=32,tau=0,e=0,clip_limits=None,long_gaps=(),short_gaps=(),core_gaps=(),core_short=(),kernels=(),w=0,forest_masks=None):
    global CURRENT_J,CURRENT_I
    CURRENT_J=j;CURRENT_I=I=(r-32)**2
    cap=496-73*j+w;th=73*j-342-w;ro=64-r
    rows=[];eqs=[];v=var
    def le(row,rhs,label):rows.append((row,rhs,label))
    def ge(row,rhs,label):le({k:-x for k,x in row.items()},-rhs,label)
    def eq(row,rhs,label):eqs.append((row,rhs,label))
    T={'ts':1,'tt':1};xi={'xs':1,'xt':1};R={'Rs':1,'Rt':1};M={'Ms':1,'Mt':1};D=v('delta');A=add((1,T),(1,D))
    for s,rv in [('s',r),('t',ro)]:
      eq(add((1,v('Rs'.replace('s',s))),(-1,v('x'+s))),rv,'core max '+s)
      eq(add((1,v('M'+s)),(-1,v('R'+s)),(-1,v('e'+s))),0,'source max '+s)
      eq(add((1,v('S'+s)),(-1,v('t'+s)),(-4,v('R'+s)),*[(-1,v(k+s)) for k in 'abce']),rv*(rv+1)//2,'source mass '+s)
      ge(v('a'+s),1,'first offset '+s)
      for a,b in [('a','b'),('b','c'),('c','e')]:ge(add((1,v(b+s)),(-1,v(a+s))),1,'offset order '+s+a)
      le(add((1,v('x'+s)),(-1,v('t'+s))),0,'xi <= tau '+s)
      le(add((1,v('e'+s)),(1,A)),655-73*j+w-I,'max offset '+s)
      ge(add((1,v('e'+s)),(-1,A)),th-85+I,'min offset '+s)
      for k in ('X','g','h','d'):ge(v(k+s),0 if 3 in st.values() else 1,'outer gap '+k+s)
      le(add((2,v('B'+s)),(-1,v('a'+s)),(-1,v('b'+s))),8,'quartet '+s)
      le(add((2,v('B'+s)),*[(-1,v(k+s)) for k in 'abc']),3,'quartet triple '+s)
      ge(v('B'+s),4,'fringe lower '+s);le(v('B'+s),10,'fringe upper '+s)
    le(A,cap-I,'budget')
    if tau is not None:eq(T,tau,'mass fixed')
    if w:ge(T,58+2*w,'positive core floor')
    eq(add((1,v('Ss')),(1,v('St')),(-2,v('K')),(1,D)),(18-j)*73+84+w,'cover mass')
    U={k+s:1 for s in 'st' for k in 'ab'};C={k+s:1 for s in 'st' for k in 'c'};L={k+s:1 for s in 'st' for k in 'e'}
    eq(add((2,v('K')),(-4,R),(-1,U),(-1,C),(-1,L),(-1,A)),th+I,'Theta exact')
    le(add((1,A),(1,v('Bs')),(1,v('Bt'))),164-th-I,'coupled source')
    le(add((1,v('K')),(-1,M),(-1,R),(-1,v('Bs')),(-1,v('Bt'))),1,'K source fringe')
    le(add((1,v('K')),(-2,R),(-1,C)),158,'two max source')
    ge(v('K'),145,'sumset cardinality')
    ge(add((1,L),(-1,A)),th-8+I,'L lower')
    F=v('F')
    for rank_weight,b in [(q,q*(66-q)) for q in range(1,20)]:ge(add((1,T),(rank_weight,F)),b,'rank kernel '+str(rank_weight))
    ge(add((2,T),(-2,xi),(7,F)),423,'rank7')
    ge(add((1,F),(1,xi)),65,'full core')
    ge(add((1,F),(1,T),(-1,xi)),63,'one trim')
    ge(add((2,F),(1,T),(-1,xi)),122,'two trim');le(F,65,'F cap')
    FD=v('FD');TD=v('TD')
    eq(add((1,TD),(-1,v('Ss')),(-1,v('St'))),-1332-I,'full source mass excess')
    ge(add((1,FD),(-1,F)),0,'source contains core')
    le(FD,73,'FD cap')
    for q in range(1,13):ge(add((1,TD),(q,FD)),q*(74-q),'source rank '+str(q))
    ge(add((1,FD),(1,M)),145,'source full span')
    ge(add((2,TD),(-2,M),(7,FD)),335,'source rank seven')
    Z={};lam={};anchors={}
    for s,o in [('s','t'),('t','s')]:
      a=add((1,v('M'+s)),(1,v('X'+s)));b=add((1,v('M'+o)),(1,v('X'+o)))
      lam[s]=add((1,v('d'+s)),(-2,a),(-1,v('g'+s)))
      Z['U'+s]=add((1,v('d'+s)),(-1,a));Z['V'+s]=add((1,Z['U'+s]),(-1,v('g'+s)))
      Z['H'+s]=add((1,Z['U'+s]),(1,v('h'+s)));Z['O'+s]=add((1,Z['H'+s]),(1,v('d'+s)))
      Z['alpha'+s]=add((1,v('h'+s)),(-1,a));Z['beta'+s]=add((1,Z['alpha'+s]),(-1,v('d'+s)))
      Z['C7'+s]=add((1,lam[s]),(-1,b));Z['C6'+s]=add((1,Z['C7'+s]),(-1,v('g'+o)))
      Z['C5'+s]=add((1,Z['C6'+s]),(-1,v('h'+o)));Z['P'+s]=add((1,Z['C5'+s]),(-1,v('d'+o)))
      anchors[s]=[add((1,lam[s]),(1,v('M'+s))),add((1,lam[s]),(-1,v('M'+o)))]
      ge(add((1,v('d'+s)),(-1,v('K')),(-2,v('X'+s)),(-1,v('g'+s)),(1,v('ell'+s))),0,'leading interval '+s)
      le(add((1,lam[s]),(1,v('K')),(-1,v('S'+s)),(-2,v('M'+o)),(-1,v('ell'+s))),1,'leading upper '+s)
      le(add((1,v('K')),(-1,v('S'+s)),(-1,v('ell'+s))),0,'leading cardinality '+s)
      if st['O'+s]==1:le(add((1,v('d'+s)),(-1,M)),12+w//2,'raw O cap '+s)
      if st['beta'+s]==st['H'+s]==1:le(add((1,v('d'+s)),(-1,M)),9+w//2,'raw beta H cap '+s)
      if st['beta'+s]==st['O'+s]==1:le(add((2,v('d'+s)),(-2,M)),17+w//2,'raw beta O cap '+s)
      # K-delta>0 for j>=3 licenses d_v>g_v+X_v. The universal
      # 495-type tail inventory leaves 16 fixed values beyond H_v+M_v.
      if j>=3 and st['O'+s]!=1:
        le(add((1,v('S'+s)),(-1,Z['H'+s]),(-1,v('M'+s))),16+w//2,'sixteen-slot tail '+s)
    alpha_family=(False and j==5 and w==0 and all(st[k+s]==(2 if k=='O' else 0)
                   for k in ('P','beta','O') for s in 'st')
                   and sorted(st['alpha'+s] for s in 'st')==[0,1])
    if alpha_family:
      side=next(s for s in 'st' if st['alpha'+s]==0)
      le(add((1,v('S'+side)),(-1,v('d'+side))),1,'alpha one-point tail')
      le(add((1,v('S'+side)),(-1,Z['H'+side]),(-1,v('M'+side))),2,'alpha two-point tail')
    retained=[k for k,x in st.items() if x==1]
    for name,status in st.items():
      s=name[-1];o='t' if s=='s' else 's';rv=r if s=='s' else ro;rv0=64-rv
      if status==0:le(add((1,Z[name]),(1,v('M'+s))),0,'LOW '+name);continue
      if status==2:ge(add((1,Z[name]),(-1,v('S'+s)),(-1,v('M'+o))),1,'HIGH '+name);continue
      if status==3:continue
      ge(add((1,Z[name]),(1,v('M'+s))),1,'active lower '+name)
      le(add((1,Z[name]),(-1,v('S'+s)),(-1,v('M'+o))),0,'active upper '+name)
      for typ,rank in [('l',rv),('u',rv0)]:
        lo,hi=(clip_limits or {}).get(typ+name,(0,72))
        # The budget already bounds each clip; keep the row inventory uniform.
        ge(v(typ+name),lo,'clip branch lower '+typ+name);le(v(typ+name),hi,'clip branch upper '+typ+name)
        if hi<=68:
          if typ=='l':ge(add((1,Z[name]),(1,v(typ+name)),(1,v('x'+s))),69-rv,'light radial lower '+name)
          else:le(add((1,Z[name]),(-1,v('S'+s)),(-1,v(typ+name)),(-1,v('x'+o))),rv0-68,'light radial upper '+name)
        if lo>=69 and hi>=lo:
          offset='abce'[hi-69]
          if typ=='l':ge(add((1,Z[name]),(1,v('R'+s)),(1,v(offset+s))),1,'exact upper tail lower '+name)
          else:le(add((1,Z[name]),(-1,v('S'+s)),(-1,v('R'+o)),(-1,v(offset+o))),0,'exact lower tail upper '+name)
        pp=free_planes(rank,j,I-w,e,lo,hi) if tau is None else fixed_planes2(rank,tau,j,I-w,e,lo,hi)
        for kcoef,dcoef,tcoef,ecoef,rhs in pp:
          if typ=='l':ge(add((ecoef,Z[name]),(ecoef-kcoef,v(typ+name)),(-dcoef,D),(-tcoef,T)),ecoef*(69-rv)-rhs,'mass lower '+name)
          else:le(add((ecoef,Z[name]),(-ecoef,v('S'+s)),(kcoef-ecoef,v(typ+name)),(dcoef,D),(tcoef,T)),ecoef*(rv0-68)+rhs,'mass upper '+name)
      ge(add((1,v('D'+name)),(-1,v('l'+name)),(-1,v('u'+name))),0,'native loss '+name)
      le(v('D'+name),73,'native hull resource '+name)
      for typ in 'lu':le(v(typ+name),72,'hull clip '+typ+name)
      # Exact physical source mass can use all fixed slots conservatively.
    roots={'ells':1,'ellt':1};allnative={'D'+name:1 for name in retained}
    le(add((1,roots),(1,allnative),(-1,D)),-e,'native total')
    for s in 'st':
      le(add((1,v('S'+s)),(-1,v('K'))),73*sum(k[-1]==s for k in retained)+84-e+w//2,'physical capacity '+s)
    # Ordered native chain and two embedded anchors in each full leading.
    edges=[]
    for s,o in [('s','t'),('t','s')]:
      arm=[k+s for k in ('V','U','H','O') if k+s in retained]
      last='L'+s;pos=anchors[s][0]
      for k in arm:edges.append((last,k,add((1,Z[k]),(-1,pos))));last=k;pos=Z[k]
      arm=[k+s for k in ('C7','C6','C5','P') if k+s in retained]
      last='L'+s;pos=anchors[s][1]
      for k in arm:edges.append((last,k,add((1,pos),(-1,Z[k]))));last=k;pos=Z[k]
      if 'beta'+s in retained and 'alpha'+s in retained:edges.append(('beta'+s,'alpha'+s,v('d'+s)))
      if 'alpha'+s in retained and 'H'+s in retained:edges.append(('alpha'+s,'H'+s,v('d'+s)))
    # Every cycle-free subset of these graph edges is a licensed inequality.
    for i,(_,_,gap) in enumerate(edges):ge(gap,1,'integer native gap '+str(i))
    long=set(long_gaps)
    for i in long:ge(add((1,edges[i][2]),(-1,TD)),1,'long source gap '+str(i))
    for i in short_gaps:le(add((1,edges[i][2]),(-1,TD)),0,'short source gap '+str(i))
    for i in core_gaps:ge(add((1,edges[i][2]),(-1,T)),1,'long core gap '+str(i))
    for i in core_short:le(add((1,edges[i][2]),(-1,T)),0,'short core gap '+str(i))
    for kind,i,k,yes in kernels:
      body=add((k+1,edges[i][2]),(-1,TD if kind=='D' else T))
      if yes:ge(body,1,'compression '+str((kind,i,k,yes)))
      else:le(body,0,'compression '+str((kind,i,k,yes)))
    masks={0,(1<<len(edges))-1}|{1<<i for i in range(len(edges))}
    masks|={(1<<i)|(1<<j0) for i in range(len(edges)) for j0 in range(i)}
    if forest_masks is not None:
      need(set(forest_masks)<=masks,'Unlicensed built-in forest mask')
      masks=set(forest_masks)
    for mask in sorted(masks):
      chosen=[x for i,x in enumerate(edges) if mask>>i&1]
      parent={x:x for edge in chosen for x in edge[:2]}
      def find(x):
        while parent[x]!=x:x=parent[x]
        return x
      bad=False
      for x,y,_ in chosen:
        a,b=find(x),find(y)
        if a==b:bad=True;break
        parent[a]=b
      if bad:continue
      used=set(parent);comp={}
      for x in used:comp.setdefault(find(x),[]).append(x)
      rebate={'D'+x:1 for x in retained if x not in used}
      for cc in comp.values():
        if not any(x.startswith('L') for x in cc):rebate['D'+min(cc)]=1
      gap=add(*[(1,g) for _,_,g in chosen]) if chosen else {}
      nlong=sum(i in long for i in range(len(edges)) if mask>>i&1)
      le(add((len(chosen)-nlong,FD),(-1,gap),(1,roots),(1,rebate),(-1,D)),-e-73*nlong,'forest '+str(mask))
    names=sorted(set(k for row,_,_ in rows+eqs for k in row))
    base_build.last_edges=edges
    base_build.last_retained=retained
    base_build.last_Z=Z
    base_build.last_long=long
    return names,rows,eqs

@lru_cache(None)
def fixed_forms():
    raw=[]
    for s in 'st':
      a={'M'+s:1,'X'+s:1};b=add((1,a),(1,var('g'+s)));c=add((1,b),(1,var('h'+s)));d=add((1,c),(1,var('d'+s)))
      raw.extend((d,c,b,a))
    return {k:add(*[(v,w) for v,w in zip(row,raw)]) for k,row in LABELS.items()}

V=var
@lru_cache(maxsize=None)
def static_rank_rows(r,blocks):
 """Immutable row templates; their values depend only on rank and block use."""
 rows=[];eqs=[]
 for tag,rank,maxtag,mass,base in [('core',64,'x','t',0),('source',72,'M','S',4)]:
  phi={}
  for side,rv in [('s',r),('t',64-r)]:
   rv+=base;p='phi'+tag+side;phi[side]=p
   massbase=rv*(rv+1)//2 if tag=='source' else 0
   maxbase=rv if tag=='source' else 0
   rows.append((V(p),rv,'side phi rank '+tag+side))
   rows.append((add((1,V(p)),(-1,V(maxtag+side))),-maxbase,'side phi span '+tag+side))
   for q in range(1,56):
    rows.append((add((q,V(p)),(-1,V(mass+side))),q*(q-1)//2-massbase,'side staircase '+tag+side+str(q)))
    rows.append((add((q,V(p)),(-1,V(mass+side)),(1,V(maxtag+side))),q*(q+1)//2-massbase+maxbase,'side staircase max '+tag+side+str(q)))
  eqs.append((add((1,V('F' if tag=='core' else 'FD')),(1,V(phi['s'])),(1,V(phi['t']))),rank+1,'side phi definition '+tag))
 if blocks:
  for weight in range(1,11):
   chis=[]
   for side,rv in [('s',r+4),('t',68-r)]:
    key='chi'+str(weight)+side;chis.append(key)
    rows.append((V(key),weight*rv,'side block rank '+key))
    rows.append((add((1,V(key)),(-1,V('M'+side))),-rv,'side block span '+key))
    for q in range(1,56):
     rows.append((add((q,V(key)),(-1,V('S'+side))),weight*q*(q-1)//2-rv*(rv+1)//2,'side block mass '+key+':'+str(q)))
     rows.append((add((q,V(key)),(-1,V('S'+side)),(1,V('M'+side))),weight*q*(q+1)//2-rv*(rv+1)//2+rv,'side block max '+key+':'+str(q)))
   eqs.append((add((1,V('GB'+str(weight))),*[(1,V(key)) for key in chis]),weight*73,'side block definition '+str(weight)))
  for side in 'st':
   eqs.append((add((1,V('chi1'+side)),(-1,V('phisource'+side))),0,'same one-weight truncation '+side))
   rows.append((add((1,V('phicore'+side)),(-1,V('phisource'+side))),0,'source phi monotone '+side))
   rows.append((add((1,V('phisource'+side)),(-1,V('phicore'+side))),4,'source phi four appended '+side))
   for weight in range(2,11):
    rows.append((add((1,V('chi'+str(weight-1)+side)),(-1,V('chi'+str(weight)+side))),0,'weighted phi monotone '+side+str(weight)))
    rows.append((add((1,V('chi'+str(weight)+side)),(-weight,V('phisource'+side))),0,'weighted phi scale '+side+str(weight)))
    if weight<10:
     rows.append((add((1,V('chi'+str(weight-1)+side)),(1,V('chi'+str(weight+1)+side)),(-2,V('chi'+str(weight)+side))),0,'weighted phi concavity '+side+str(weight)))
 return tuple(rows),tuple(eqs)

def build(st,j,r=32,tau=None,e=0,clip_limits=None,w=0,blocks=True,forest_masks=None):
 names,rows,eqs=base_build(st,j,r,tau,e,clip_limits=clip_limits,w=w,forest_masks=forest_masks)
 if blocks:
  G={};d=73
  # G_b = max over actual inward truncations [b*|Q| - holes(Q)].
  for b in range(1,11):
   key='GB'+str(b);G[b]=V(key)
   rows.append((V(key),b*d,'block cap'))
   # chi_b <= zeta_D = M-(d-1)
   rows.append((add((-1,V(key)),(-1,{'Ms':1,'Mt':1})), -b*d-(d-1),'block full span'))
   # tau >= q*chi_b - b*q(q-1) (both sides).
   for q in range(1,20):
    rows.append((add((-q,V(key)),(-1,V('TD'))),-q*b*d+b*q*(q-1),'block mass'))
   # remove the maximum dev on both sides before staircase bound.
   for q in range(1,20):
    rows.append((add((-q,V(key)),(-1,V('TD')),(1,{'Ms':1,'Mt':1})), -q*b*d+b*q*(q+1)+(d-1),'block max removed'))
  Z=base_build.last_Z;ret=base_build.last_retained
  rows.append((add((1,V('LS')),(1,V('LT')),(-1,V('delta'))),-e,'block total'))
  for s,o in [('s','t'),('t','s')]:
   side=[k for k in ret if k.endswith(s)];loss=V('L'+s.upper())
   root=V('ell'+s)
   chain=[k+s for k in CHAIN if k+s in ret]
   lam=add((1,V('d'+s)),(-2,V('M'+s)),(-2,V('X'+s)),(-1,V('g'+s)))
   am=add((1,lam),(-1,V('M'+o)));ap=add((1,lam),(1,V('M'+s)))
   rows.append((add((1,root),(1,{'D'+k:1 for k in side}),(-1,loss)),0,'block native'))
   for i in range(len(chain)):
    for stop in range(i+1,len(chain)+1):
     group=chain[i:stop];k=len(group)
     # two disjoint-up-to-one D anchors in the single leading resource
     lo=Z[group[0]] if CHAIN.index(group[0][:-1])<4 else am
     hi=Z[group[-1]] if CHAIN.index(group[-1][:-1])>=4 else ap
     span=add((1,hi),(-1,lo))
     rows.append((add((1,G[k+1]),(-1,span),(1,root),(1,{'D'+x:1 for x in side if x not in group}),(-1,loss)),1,'two-anchor block '+s+str((i,stop))))
     if k>=2:
      span=add((1,Z[group[-1]]),(-1,Z[group[0]]))
      for root0 in group:
       rows.append((add((1,G[k-1]),(-1,span),(1,root),(1,V('D'+root0)),(1,{'D'+x:1 for x in side if x not in group}),(-1,loss)),0,'ordinary block'))
  names=sorted(set(k for row,_,_ in rows+eqs for k in row))
 tail_rows,tail_eqs=static_rank_rows(r,blocks)
 rows.extend(tail_rows);eqs.extend(tail_eqs)
 for attr in ('edges','retained','Z','long'):setattr(build,'last_'+attr,getattr(base_build,'last_'+attr))
 names=sorted(set(k for row,_,_ in rows+eqs for k in row))
 return names,rows,eqs
