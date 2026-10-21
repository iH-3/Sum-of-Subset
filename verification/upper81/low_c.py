"""Standard-library replay of the uniform small-slack interface."""
from pathlib import Path
from collections import Counter
import json
import model as m
ROOT=Path(__file__).resolve().parents[2]
v=m.var;add=m.add
def build(st):
 rows=[]
 def le(a,b,label):rows.append((a,b,label))
 def ge(a,b,label):le({k:-x for k,x in a.items()},-b,label)
 Z={};anchors={}
 ge({'Ms':1,'Mt':1},73,'span')
 le({'etas':1,'etat':1},28,'holes')
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


def verify():
 packet=json.loads((ROOT/'data/upper81_low_c.json').read_text())
 m.need((packet['F_lower'],packet['delta_upper'],packet['w_upper'])==(24,76,28),'Small-slack scope')
 expected=list(m.patterns(1));m.need(len(packet['records'])==len(expected)==22,'Small-slack complete pattern census')
 margins=[]
 for record,st in zip(packet['records'],expected):
  m.need(record['st']==st,'Small-slack pattern order')
  rows,edges,ret=build(st)
  for chosen in record['forests']:
   m.need(len(set(chosen))==len(chosen),'Repeated small-slack edge')
   parent={n:n for n in ('root','Ls','Lt',*ret)};parent['Ls']=parent['Lt']='root'
   def find(n):
    while parent[n]!=n:n=parent[n]
    return n
   for i in chosen:
    m.need(type(i) is int and 0<=i<len(edges),'Small-slack edge index')
    a,b,_=edges[i];aa,bb=find(a),find(b);m.need(aa!=bb,'Small-slack forest or leading roots');parent[aa]=bb
   rows.append((add(*[(-1,edges[i][2]) for i in chosen]),76-24*len(chosen),'forest '+str(chosen)))
  lhs=Counter();rhs=0;seen=set()
  for i,w in record['certificate']:
   m.need(type(i) is int and 0<=i<len(rows) and i not in seen and type(w) is int and w>0,'Small-slack certificate multiplier');seen.add(i)
   row,b,_=rows[i]
   for k,c in row.items():lhs[k]+=w*c
   rhs+=w*b
  m.need(all(c>=0 for c in lhs.values()) and rhs<0 and -rhs==record['margin'],'Small-slack exact contradiction')
  margins.append(-rhs)
 return dict(status='PASS_UNIFORM_LOW_SLACK',patterns=22,F=24,delta=76,w=28,minimum_integer_margin=min(margins))

if __name__=='__main__':print(json.dumps(verify(),indent=2))
