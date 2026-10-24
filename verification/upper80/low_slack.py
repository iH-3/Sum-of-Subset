"""Independent exact replay of conditional low-slack size-81 interfaces.

The premise is a common integer source with span >=72 and a core translation
intersection lower bound F>=24. This does not certify structural applicability.
"""
from pathlib import Path
from collections import Counter
import argparse,gzip,hashlib,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import model as m
ROOT=Path(__file__).resolve().parents[2]
v=m.var;add=m.add

def build(st,w_upper):
 rows=[]
 def le(a,b,label):rows.append((a,b,label))
 def ge(a,b,label):le({k:-x for k,x in a.items()},-b,label)
 Z={};anchors={}
 ge({'Ms':1,'Mt':1},72,'span')
 le({'etas':1,'etat':1},w_upper,'holes')
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
 path=ROOT/'data/upper80_low_slack_20261024.json.gz';raw=path.read_bytes();packet=json.loads(gzip.decompress(raw))
 m.need(packet['schema']=='upper80-conditional-low-slack-v1' and not packet['global_upper_bound_certified'] and not packet['structural_applicability_certified'],'Conditional low-slack status')
 m.need(len(packet['cases'])==2,'Low-slack case inventory');summaries=[]
 for data,(j,delta_upper) in zip(packet['cases'],[(1,110),(2,40)]):
  m.need((data['j'],data['delta_upper'],data['w_upper'],data['F_lower'])==(j,delta_upper,32,24) and not data['open'],'Low-slack premises')
  expected=list(m.patterns(j));m.need(len(data['records'])==len(expected),'Low-slack pattern coverage');margins=[]
  for record,st in zip(data['records'],expected):
   m.need(record['st']==st,'Low-slack pattern order');rows,edges,ret=build(st,32)
   for forest in record['forests']:
    m.need(len(forest)==len(set(forest)) and all(type(i) is int and 0<=i<len(edges) for i in forest),'Low-slack forest inventory')
    parent={n:n for n in ('root','Ls','Lt',*ret)};parent['Ls']=parent['Lt']='root'
    def find(n):
     while parent[n]!=n:n=parent[n]
     return n
    for i in forest:
     a,b,_=edges[i];a,b=find(a),find(b);m.need(a!=b,'Low-slack rooted forest cycle');parent[a]=b
    rows.append((add(*[(-1,edges[i][2]) for i in forest]),delta_upper-24*len(forest),'conditional loss forest'))
   coefficients=Counter();rhs=0;seen=set()
   for i,weight in record['certificate']:
    m.need(type(i) is int and 0<=i<len(rows) and i not in seen and type(weight) is int and weight>0,'Low-slack exact weights');seen.add(i)
    row,bound,_=rows[i]
    for name,value in row.items():coefficients[name]+=weight*value
    rhs+=weight*bound
   m.need(all(value>=0 for value in coefficients.values()) and rhs<0 and -rhs==record['margin'],'Low-slack exact contradiction');margins.append(-rhs)
  summaries.append(dict(j=j,delta_upper=delta_upper,w_upper=32,F_lower=24,patterns=len(expected),minimum_integer_margin=min(margins)))
 return dict(status='PASS_CONDITIONAL_LOW_SLACK_INTERFACES',global_upper_bound_certified=False,structural_applicability_certified=False,cases=summaries,packet_sha256=hashlib.sha256(raw).hexdigest())

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args();result=verify()
 if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result))
