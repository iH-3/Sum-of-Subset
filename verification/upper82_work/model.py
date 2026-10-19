"""Necessary rational systems for the stated size83 C5t family only.
Geometric licenses are written in the companion proof. Standard library.
"""
from collections import Counter

def add(*args):
 z=Counter()
 for scale,row in args:
  for k,v in row.items():z[k]+=scale*v
 return dict(z)
def var(x):return {x:1}
def build(r,taueq,heavy=None,tail=True,cutoff=True,negcutoff=False,longrank=False,guard=None):
 ro=66-r;I=(r-33)**2;d=75;e=13;c=19;cap=95;rows=[];eqs=[]
 if not (24<=r<=42 and type(taueq) is int and 0<=taueq<=82-I):raise ValueError('rank/mass domain')
 def le(lhs,rhs,name):rows.append((lhs,rhs,name))
 def ge(lhs,rhs,name):le({k:-v for k,v in lhs.items()},-rhs,name)
 def eq(lhs,rhs,name):eqs.append((lhs,rhs,name))
 v=var
 tau={'ts':1,'tt':1};xi={'xs':1,'xt':1};R={'Rs':1,'Rt':1};M={'Ms':1,'Mt':1};D=v('delta');A=add((1,tau),(1,D))
 eq(add((1,v('Rs')),(-1,v('xs'))),r,'Rs');eq(add((1,v('Rt')),(-1,v('xt'))),ro,'Rt')
 for s,rv in [('s',r),('t',ro)]:
  eq(add((1,v('M'+s)),(-1,v('R'+s)),(-1,v('e'+s))),0,'max'+s)
  eq(add((1,v('S'+s)),(-1,v('t'+s)),(-4,v('R'+s)),*[(-1,v(k+s)) for k in 'abce']),rv*(rv+1)//2,'mass'+s)
  ge(v('a'+s),1,'a positive');
  for a,b in [('a','b'),('b','c'),('c','e')]:ge(add((1,v(b+s)),(-1,v(a+s))),1,'offset order')
  le(add((1,v('x'+s)),(-1,v('t'+s))),0,'xi<=tau')
  le(add((1,v('e'+s)),(1,A)),258-I,'e upper')
  ge(add((1,v('e'+s)),(-1,A)),I-24,'e lower')
  ge(v('X'+s),1,'X positive');ge(v('g'+s),1,'g positive');ge(v('h'+s),1,'h positive');ge(v('d'+s),1,'d positive')
  le(add((2,v('B'+s)),(-1,v('a'+s)),(-1,v('b'+s))),8,'quartet')
  le(add((2,v('B'+s)),*[(-1,v(k+s)) for k in 'abc']),3,'quartet triple')
  ge(v('B'+s),4,'fringe>=4');le(v('B'+s),10,'fringe<=10')
 le(A,cap-I,'budget')
 if taueq is not None:eq(tau,taueq,'fixed total mass')
 eq(add((1,v('Ss')),(1,v('St')),(-2,v('K')),(1,D)),13*d+84,'cover mass')
 U={k+s:1 for s in 'st' for k in 'ab'};C={k+s:1 for s in 'st' for k in 'c'};L={k+s:1 for s in 'st' for k in 'e'}
 eq(add((2,v('K')),(-4,R),(-1,U),(-1,C),(-1,L),(-1,A)),63+I,'Theta exact')
 le(add((1,A),(1,v('Bs')),(1,v('Bt'))),105-I,'coupled source')
 le(add((1,v('K')),(-1,M),(-1,R),(-1,v('Bs')),(-1,v('Bt'))),1,'K source fringe')
 le(add((1,v('K')),(-2,R),(-1,C)),162,'two max source')
 ge(add((1,L),(-1,A)),55+I,'L lower')
 F=v('F')
 if longrank:eq(F,67,'strict long gap full core')
 for w,b in [(1,67),(2,132),(3,195),(4,256),(6,372)]:ge(add((1,tau),(w,F)),b,'rank kernel'+str(w))
 ge(add((2,tau),(-2,xi),(7,F)),437,'rank7')
 ge(add((1,F),(1,xi)),67,'fullcore')
 ge(add((1,F),(1,tau),(-1,xi)),65,'one trim')
 ge(add((2,F),(1,tau),(-1,xi)),126,'two trim')
 le(F,67,'F cap')
 Z={};lam={};p4={}
 for s,o in [('s','t'),('t','s')]:
  a=add((1,v('M'+s)),(1,v('X'+s)));b=add((1,v('M'+o)),(1,v('X'+o)));p4[s]=a
  lam[s]=add((1,v('d'+s)),(-2,a),(-1,v('g'+s)))
  Z['U'+s]=add((1,v('d'+s)),(-1,a));Z['V'+s]=add((1,v('d'+s)),(-1,a),(-1,v('g'+s)))
  Z['H'+s]=add((1,Z['U'+s]),(1,v('h'+s)));Z['O'+s]=add((1,Z['H'+s]),(1,v('d'+s)))
  Z['alpha'+s]=add((1,v('h'+s)),(-1,a));Z['beta'+s]=add((1,Z['alpha'+s]),(-1,v('d'+s)))
  Z['C7'+s]=add((1,lam[s]),(-1,b));Z['C6'+s]=add((1,Z['C7'+s]),(-1,v('g'+o)))
  Z['C5'+s]=add((1,Z['C6'+s]),(-1,v('h'+o)));Z['P'+s]=add((1,Z['C5'+s]),(-1,v('d'+o)))
  ge(add((1,v('d'+s)),(-1,v('K')),(-2,v('X'+s)),(-1,v('g'+s)),(1,v('ell'+s))),0,'leading interval')
 for name in ['Os','Ot','Hs']:ge(add((1,Z[name]),(-1,v('S'+name[-1])),(-1,v('M'+('t' if name[-1]=='s' else 's')))),1,'empty HIGH '+name)
 for name in ['Ps','Pt','C5t','betat']:le(add((1,Z[name]),(1,v('M'+name[-1]))),0,'empty LOW '+name)
 retained=['Us','Vs','alphas','betas','C5s','C6s','C7s','Ht','Ut','Vt','alphat','C6t','C7t']
 for name in retained:
  s=name[-1];o='t' if s=='s' else 's';rv=r if s=='s' else ro;rv_o=66-rv
  lower=add((1,Z[name]),(1,v('l'+name)),(1,v('x'+s)))
  upper=add((1,Z[name]),(-1,v('S'+s)),(-1,v('u'+name)),(-1,v('x'+o)))
  if heavy==(name,'l'):lower=add((1,lower),(1,v('e'+s)));floor=71-rv+4
  else:floor=71-rv
  if heavy==(name,'u'):upper=add((1,upper),(-1,v('e'+o)));ceiling=rv_o-70-4
  else:ceiling=rv_o-70
  ge(lower,floor,'endpoint low '+name);le(upper,ceiling,'endpoint upper '+name)
  if taueq is not None:
   epsmax=cap-I-e-taueq-(71 if heavy is not None else 0)
   for typ,rv0,side in [('l',rv,s),('u',rv_o,o)]:
    if heavy==(name,typ):continue
    E=0 if min(70,epsmax)<=70-rv0 else taueq//max(1,71-min(70,epsmax))
    if typ=='l':ge(add((1,Z[name]),(1,v('l'+name))),71-rv-E,'mass endpoint lower '+name)
    else:le(add((1,Z[name]),(-1,v('S'+s)),(-1,v('u'+name))),rv_o-70+E,'mass endpoint upper '+name)
    if epsmax>=0:
     hull=[]
     for k in range(min(70,epsmax)+1):
      y=0 if k<=70-rv0 else taueq//(71-k)
      while len(hull)>=2 and (hull[-1][1]-hull[-2][1])*(k-hull[-1][0]) <= (y-hull[-1][1])*(hull[-1][0]-hull[-2][0]):hull.pop()
      hull.append((k,y))
     for (k1,y1),(k2,y2) in zip(hull,hull[1:]):
      den=k2-k1;num=y2-y1;inter=den*y1-num*k1
      if typ=='l':ge(add((den,Z[name]),(den+num,v('l'+name))),den*(71-rv)-inter,'concave mass lower '+name)
      else:le(add((den,Z[name]),(-den,v('S'+s)),(-den-num,v('u'+name))),den*(rv_o-70)+inter,'concave mass upper '+name)
  ge(add((1,v('D'+name)),(-1,v('l'+name)),(-1,v('u'+name))),0,'native loss')
  le(v('D'+name),74,'retained native')
  for typ in 'lu':
   if heavy==(name,typ):ge(v(typ+name),71,'heavy clip')
   else:le(v(typ+name),70,'light clip')
 allnative={'D'+name:1 for name in retained};roots={'ells':1,'ellt':1}
 le(add((1,allnative),(1,roots),(-1,D)),-e,'native total')
 # All subsets of the canonical two trees; an unused vertex has its native
 # loss rebated. Each leading remains a designated root of its physical tree.
 edges=[]
 for s,o in [('s','t'),('t','s')]:
  for x,y,gap in [('L'+s,'V'+s,v('X'+s)),('V'+s,'U'+s,v('g'+s)),('U'+s,'H'+s,v('h'+s)),('L'+s,'C7'+s,v('X'+o)),('C7'+s,'C6'+s,v('g'+o)),('C6'+s,'C5'+s,v('h'+o))]:
   if all(z.startswith('L') or z in retained for z in (x,y)):edges.append((x,y,gap))
 # These are genuine forest subgraphs, with one leading root per component
 # containing that leading. For a component detached from leading, no root
 # native loss is added. Native losses of both leading roots still available.
 for mask in range(1<<len(edges)):
  chosen=[edge for i,edge in enumerate(edges) if mask>>i&1]
  used=set(z for x,y,_ in chosen for z in (x,y));gap=add(*[(1,row) for _,_,row in chosen]) if chosen else {}
  unused={'D'+name:1 for name in retained if name not in used}
  le(add((len(chosen),F),(-1,gap),(1,roots),(1,unused),(-1,D)),-e,'forest '+str(mask))
 if tail:le(add((1,v('Ss')),(-1,v('ds')),(1,v('Xs')),(1,v('Dalphas'))),d+c,'tail exact')
 ge(add((1,v('ds')),(-1,v('gs')),(-1,v('Xs'))),1,'tail cone')
 if cutoff:le(add((1,Z['betas']),(1,p4['s']),(1,v('gs')),(-1,v('ds')),(1,v('Xs'))),-1,'beta cutoff')
 if negcutoff:ge(add((1,Z['betas']),(1,p4['s']),(1,v('gs')),(-1,v('ds')),(1,v('Xs'))),0,'negate beta cutoff')
 # whole physical-side group with no accidental disjointness claim
 le(add((1,v('Ss')),(-1,v('K'))),609-e,'physical s capacity')
 le(add((1,v('St')),(-1,v('K'))),534-e,'physical t capacity')
 if guard in ('Xs','Xt','gs','gt','ht'):le(v(guard),taueq,'negate strict long gap '+guard)
 names=sorted(set(k for row,_,_ in rows+eqs for k in row))
 return names,rows,eqs
