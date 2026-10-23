# RESEARCH PROTOTYPE
"""Discover generic j=1 low-slack certificates (no primitive-core premise)."""
import sys,json,importlib.util
from pathlib import Path
from collections import Counter
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction
from math import lcm,gcd
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('m80',ROOT/'verification/upper80/model.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
v=m.var;add=m.add

def build(st):
 rows=[]
 def le(a,b,label):rows.append((a,b,label))
 def ge(a,b,label):le({k:-x for k,x in a.items()},-b,label)
 Z={};anchors={}
 ge({'Ms':1,'Mt':1},72,'span')
 le({'etas':1,'etat':1},WMAX,'holes')
 for s,o in [('s','t'),('t','s')]:
  for k in ('M','X','g','h','d'):ge(v(k+s),1,'positive '+k+s)
  p=add((1,v('M'+s)),(1,v('X'+s)));po=add((1,v('M'+o)),(1,v('X'+o)))
  lam=add((1,v('d'+s)),(-2,p),(-1,v('g'+s)))
  Z['V'+s]=add((1,lam),(1,p));Z['U'+s]=add((1,Z['V'+s]),(1,v('g'+s)))
  Z['H'+s]=add((1,Z['U'+s]),(1,v('h'+s)));Z['O'+s]=add((1,Z['H'+s]),(1,v('d'+s)))
  Z['alpha'+s]=add((1,v('h'+s)),(-1,p));Z['beta'+s]=add((1,Z['alpha'+s]),(-1,v('d'+s)))
  Z['C7'+s]=add((1,lam),(-1,po));Z['C6'+s]=add((1,Z['C7'+s]),(-1,v('g'+o)))
  Z['C5'+s]=add((1,Z['C6'+s]),(-1,v('h'+o)));Z['P'+s]=add((1,Z['C5'+s]),(-1,v('d'+o)))
  anchors[s]=[add((1,lam),(1,v('M'+s))),add((1,lam),(-1,v('M'+o)))]
  t=add((1,v('d'+s)),(-1,{'Ms':1,'Mt':1}))
  if st['O'+s]==1:le(add((1,t),(-1,v('eta'+s))),12,'raw O '+s)
  if st['beta'+s]==st['H'+s]==1:le(add((1,t),(-1,v('eta'+s))),9,'raw beta H '+s)
  if st['beta'+s]==st['O'+s]==1:le(add((2,t),(-1,v('eta'+s))),17,'raw beta O '+s)
 for name,status in st.items():
  s=name[-1];o='t' if s=='s' else 's'
  if status==0:le(add((1,Z[name]),(1,v('M'+s))),0,'LOW '+name)
  elif status==2:ge(add((1,Z[name]),(-1,v('S'+s)),(-1,v('M'+o))),1,'HIGH '+name)
  else:
   ge(add((1,Z[name]),(1,v('M'+s))),1,'retained lower '+name)
   le(add((1,Z[name]),(-1,v('S'+s)),(-1,v('M'+o))),0,'retained upper '+name)
 retained=[k for k,st0 in st.items() if st0==1];edges=[]
 for s in 'st':
  last='L'+s;pos=anchors[s][0]
  for k in ('V','U','H','O'):
   name=k+s
   if name in retained:edges.append((last,name,add((1,Z[name]),(-1,pos))));last=name;pos=Z[name]
  last='L'+s;pos=anchors[s][1]
  for k in ('C7','C6','C5','P'):
   name=k+s
   if name in retained:edges.append((last,name,add((1,pos),(-1,Z[name]))));last=name;pos=Z[name]
  for k1,k2 in [('beta','alpha'),('alpha','H')]:
   if k1+s in retained and k2+s in retained:edges.append((k1+s,k2+s,v('d'+s)))
 return rows,edges,retained

def ray(rows):
 names=sorted({k for a,b,l in rows for k in a});A=np.array([[a.get(k,0) for k in names] for a,b,l in rows],float);b=np.array([b for a,b,l in rows],float)
 rr=linprog(np.r_[np.zeros(len(names)),1],A_ub=np.c_[A,-np.ones(len(rows))],b_ub=b,bounds=(0,None),method='highs')
 if not rr.success or rr.fun<1e-8:return None
 for lim in (1000,1000000,1000000000):
  weights=[Fraction(-float(w)).limit_denominator(lim) for w in rr.ineqlin.marginals];den=lcm(*(w.denominator for w in weights));ww=[int(w*den) for w in weights];gg=gcd(*ww);ww=[w//gg for w in ww]
  lhs=Counter();rhs=0
  for w,(a,b,l) in zip(ww,rows):
   for k,c in a.items():lhs[k]+=w*c
   rhs+=w*b
  if min(lhs.values())>=0 and rhs<0:return [(i,w) for i,w in enumerate(ww) if w],-rhs
 raise ValueError('No exact ray')

J=int(sys.argv[1]);DCAP=int(sys.argv[2]);WMAX=int(sys.argv[3]);FMIN=int(sys.argv[4]);out=[];opens=[]
for index,st in enumerate(m.patterns(J)):
 rows,edges,ret=build(st);forests=[]
 for iteration in range(100):
  names=sorted({k for a,b,l in rows for k in a});A=np.array([[a.get(k,0) for k in names] for a,b,l in rows],float);b=np.array([b for a,b,l in rows],float)
  rr=linprog(np.zeros(len(names)),A_ub=A,b_ub=b,bounds=(0,None),method='highs')
  if rr.status==2:break
  if not rr.success:raise ValueError(rr.message)
  x=dict(zip(names,rr.x));parent={n:n for n in ('root','Ls','Lt',*ret)};parent['Ls']=parent['Lt']='root'
  def find(n):
   while parent[n]!=n:n=parent[n]
   return n
  chosen=[]
  for value,i,a,b in sorted([(FMIN-sum(c*x[k] for k,c in g.items()),i,a,b) for i,(a,b,g) in enumerate(edges)],reverse=True):
   if value<=0:continue
   aa,bb=find(a),find(b)
   if aa!=bb:parent[aa]=bb;chosen.append(i)
  if sum(FMIN-sum(c*x[k] for k,c in edges[i][2].items()) for i in chosen)<=DCAP+1e-7:
   opens.append(dict(i=index,point=x));break
  forests.append(chosen);rows.append((add(*[(-1,edges[i][2]) for i in chosen]),DCAP-FMIN*len(chosen),'forest '+str(chosen)))
 if opens and opens[-1]['i']==index:
  print('OPEN',index,flush=True);continue
 cert=ray(rows);out.append(dict(st=st,forests=forests,certificate=cert[0],margin=cert[1]));print(index,len(forests),cert[1],flush=True)
(ROOT/f'.work/upper80/low_c_j{J}_{DCAP}_{WMAX}_{FMIN}.json').write_text(json.dumps(dict(j=J,delta_upper=DCAP,w_upper=WMAX,F_lower=FMIN,records=out,open=opens),separators=(',',':'))+'\n')
print('COMPLETE',len(out),len(opens))
