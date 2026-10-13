#!/usr/bin/env python3
"""Standalone finite arithmetic replay. Python stdlib only; imports no model.
All witnesses below are explicit. No construction search occurs in this checker.
"""
from hashlib import sha256
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
T=lambda r:r*(r+1)//2
n=lambda r:r-5 if r>=21 else r-14
DENSE={4:(3,55),5:(5,84),6:(6,108),7:(7,127),8:(8,143),9:(8,154),10:(8,162),11:(8,165),12:(8,167),13:(7,162),14:(7,167),15:(7,156),16:(6,140),17:(5,123),18:(4,99),19:(3,72),20:(2,40)}
ENDPOINT={4:4,5:4,6:5,7:6}
OVERLAP={1:(3,51),2:(5,79),3:(6,100),4:(7,112),5:(7,119),6:(7,119),7:(6,114),8:(5,100),9:(4,81),10:(3,55)}

def effective(r,beta,C):
 assert r>=15 and beta>=1 and C>=0
 K=3
 while (K+1)*(K-2)//2<=C+1:K+=1
 assert K*(K-3)//2<=C+1<(K+1)*(K-2)//2
 D=C+max(3,K); E=D+1
 # Equivalent to the original bridge's radical formula, using only integers.
 M=2*beta
 while T(M)-6*beta<=M+1+E:M+=1
 assert T(M)-6*beta>M+1+E
 if M>2*beta:assert T(M-1)-6*beta<=M+E
 J=max(K+1,2*beta+5,M)
 window=(r-J+1)*beta-D
 prefix=T(J-1)-1-D
 assert window>0 and prefix>0
 return {'K':K,'D':D,'E':E,'M':M,'J':J,'window_margin':window,'prefix_margin':prefix}

def oldrho(r,mu):
 assert r>=15
 values={'nonAP':r-14,'defects':mu+2-2*r}
 for gamma in range(2,11):
  assert gamma<=r-5
  v=max(0,mu-4*gamma+2)
  # Independent literal integer inversion of t+2 floor(t/(gamma-1)).
  t=0
  while t+2*(t//(gamma-1))<v:t+=1
  q,s=divmod(v,gamma+1)
  assert t==(gamma-1)*q+min(s,gamma-1)
  values[str(gamma)]=min((gamma-1)*(r-14),t)
 result=max(values.values())
 return result,[key for key,val in values.items() if val==result]

def row(k):
 a,b=34-k,35+k;I=k*(k+1);O=587-I
 assert a+b==69 and 1+T(a)+T(b)==1226+I
 assert O==22*78+97-(1226+I)
 C=2*69+4*70+14-(1226+I)
 assert C==-794-I and C+O==-207-2*I
 rp,rq=n(a),n(b)
 return {'k':k,'a':a,'b':b,'I':I,'Omega':O,'rp':rp,'rq':rq,
 'R':O-T(a)+2-(a-3)-rp,'Kmax':O-rp-rq,
 'Umax':O-rp-rq+3,'Vmin':T(b)+b-2,'Umin':T(a)+a-2,
 'test_margin':(a-3)+rp+rq-(O-T(a)+2)}

def verify_sources():
 for ent in json.loads((HERE/'source_pins.json').read_text()):
  assert sha256((HERE/ent['path']).read_bytes()).hexdigest()==ent['sha256'],ent['path']

def verify():
 verify_sources()
 ranges=[row(k) for k in range(21)]
 assert [x['k'] for x in ranges[:20] if x['test_margin']<=0]==list(range(4,20))
 assert [x['k'] for x in ranges if x['test_margin']<=0]==list(range(4,21))
 for x in ranges:
  assert x['Omega']<T(x['b'])-1
 print('# SIZE86 inverse-gap arithmetic')
 print('\nConditional a,b>=15: failed sufficient range k4..19. Including boundary a14: k4..20.')
 print('\n|k|a|b|Omega|test margin|R|Kmax|Umax|Vmin|Umin|')
 print('|'+ '|'.join(['---']*10)+'|')
 for x in ranges:print('|'+ '|'.join(str(x[q]) for q in ('k','a','b','Omega','test_margin','R','Kmax','Umax','Vmin','Umin'))+'|')
 print('\n## Effective primitive-Q hole witnesses')
 print('\nAll 17 rows have valid witnesses; k4..7 need the endpoint repair below to obtain diameters.')
 print('\n|k|beta|C_h|K|D|M|J|window|prefix|forced rho|old gamma|H|order margin|')
 print('|'+ '|'.join(['---']*13)+'|')
 for k,(beta,C) in DENSE.items():
  x=row(k);e=effective(x['b'],beta,C);rho,gs=oldrho(x['b'],x['b']+C+1)
  assert rho>x['R']
  order=x['Vmin']-x['Umax']-x['Kmax']+1
  vals=[k,beta,C,e['K'],e['D'],e['M'],e['J'],e['window_margin'],e['prefix_margin'],rho,','.join(gs),2*beta,order]
  print('|'+ '|'.join(map(str,vals))+'|')
 print('\n## Dense diameter margins for k8..20')
 print('\nMargins: residue V−1−K; order V−U−K+1; P-diameter V−K−H−2; Q-diameter Umin−H−2.')
 print('\n|k|residue|order|P-diameter|Q-diameter|D1 upper|post-G primitive margin|')
 print('|'+ '|'.join(['---']*7)+'|')
 for k in range(8,21):
  x=row(k);H=2*DENSE[k][0]
  margins=[x['Vmin']-1-x['Kmax'],x['Vmin']-x['Umax']-x['Kmax']+1,x['Vmin']-x['Kmax']-H-2,x['Umin']-H-2]
  assert min(margins)>0
  d1=-207-2*x['I']+2*H+(16 if k==20 else 0);assert d1<0
  pm=T(x['a'])-(x['Omega']-(146-3*H)-x['rp']-x['rq'])
  print('|'+ '|'.join(map(str,[k,*margins,d1,pm]))+'|')
 print('\n## Endpoint-hole cases k4..7')
 print('\nTail margin=(beta−1)(b−14)−R; count margin=j−(2beta+5); off-scale=T_j−b−1−R; bridge=T_j−6beta−j−R−3.')
 print('\n|k|b|R|beta|j|tail|count|off-scale|bridge|H|alpha|')
 print('|'+ '|'.join(['---']*11)+'|')
 for k,beta in ENDPOINT.items():
  x=row(k);b,R=x['b'],x['R'];j=b-R//(beta-1);H=2*beta;alpha=4*beta+2
  tail=(beta-1)*(b-14)-R;count=j-(2*beta+5);off=T(j)-b-1-R;bridge=T(j)-6*beta-j-R-3
  assert tail>0 and count>=0 and off>0 and bridge>0 and j>=15 and j>2*beta
  for mm in range(j,b):assert T(mm)-6*beta>mm+R+3
  assert j>(j+beta)//2
  print('|'+ '|'.join(map(str,[k,b,R,beta,j,tail,count,off,bridge,H,alpha]))+'|')
 print('\nEndpoint residue/central-gap/diameter margins; gap margin=V−K−2alpha−1.')
 print('\n|k|residue|central gap|P-diameter|Q-diameter|D1 upper|post-G primitive margin|')
 print('|'+ '|'.join(['---']*7)+'|')
 for k,beta in ENDPOINT.items():
  x=row(k);H=2*beta;alpha=4*beta+2
  margins=[x['Vmin']-1-x['Kmax'],x['Vmin']-x['Kmax']-2*alpha-1,x['Vmin']-x['Kmax']-alpha-2,x['Umin']-H-2]
  assert min(margins)>0
  d1=-207-2*x['I']+2*H;assert d1<0
  pm=T(x['a'])-(x['Omega']-(146-3*H)-x['rp']-x['rq']);assert pm>0
  print('|'+ '|'.join(map(str,[k,*margins,d1,pm]))+'|')
 print('\n## Post-G individual P primitivity in repaired rows')
 print('\nFor gP>=2 and intrinsic nonAP hole count h0>=1, hP >= T_a+muP+2 >= T_a+a−1.')
 print('\n|k|H|coarse margin|nonprimitive margin|residual|')
 print('|---|---|---|---|---|')
 equality=[]
 for k in range(4,20):
  x=row(k);H=2*(ENDPOINT[k] if k in ENDPOINT else DENSE[k][0])
  raw=T(x['a'])-(x['Omega']-(146-3*H)-x['rp']-x['rq'])
  refined=raw+x['a']-1
  assert refined>=0
  if refined==0:equality.append(k)
  print('|'+ '|'.join(map(str,[k,H,raw,refined,'equality only' if refined==0 else 'excluded']))+'|')
 assert equality==[11,12]
 print('\nThe two equality rows have c=0, z=hQ=16, gP=2, h0=1, muP=a−3, rhoP=a−5, rhoQ=b−5, kappa=hP=T_a+a−1.')
 print('\n|k|a|b|muP|rhoP|rhoQ|kappa|T|intrinsic P span|single-hole mu floor|contradiction margin|')
 print('|'+ '|'.join(['---']*11)+'|')
 for k in equality:
  x=row(k);a,b=x['a'],x['b'];mu=a-3;kap=T(a)+a-1;budgetT=kap+146-48
  assert x['rp']+x['rq']+budgetT==x['Omega']
  assert T(a-2)>mu
  assert (T(a)+mu+1)%2==1  # A sole hole cannot be fixed by odd-span reflection.
  print('|'+ '|'.join(map(str,[k,a,b,mu,x['rp'],x['rq'],kap,budgetT,T(a)+mu+1,T(a-2),T(a-2)-mu]))+'|')
 print('Parity closure: each intrinsic span is odd, so reflection pairs distinct integer holes and h0=1 is impossible. Single-hole cross-check: the sole missing integer is central; the first coefficient breaking interval coverage must be the final coefficient and gives disjoint final supports. Thus muP>=T_(a−2), contradicting muP=a−3.')
 print('\n## Large-hole final-support overlap')
 print('\nZ=104+k(k+1); every k15..19 is excluded by Z+n(a)+n(b)>Omega. The 30 oriented cases k0..14 follow.')
 for k in range(15,20):
  x=row(k);assert 104+x['I']+x['rp']+x['rq']>x['Omega']
 print('\n|k|disjoint side|r|other s|Z|base margin|beta|C_h|K|D|M|J|window|prefix|other rho|gamma|final margin|')
 print('|'+ '|'.join(['---']*17)+'|')
 overlaps=[]
 for k in range(15):
  x=row(k);a,b,O=x['a'],x['b'],x['Omega'];Z=104+x['I']
  for side,r,s in [('P',a,b),('Q',b,a)]:
   cost=T(r-2)+2-2*r;lower=n(s);base=cost+lower+Z-O
   data=['—']*8;gam='—'
   if base<=0:
    assert side=='P' and k in OVERLAP
    beta,C=OVERLAP[k];assert Z>2*beta
    e=effective(s,beta,C);lower,gammas=oldrho(s,s+C+1);gam=','.join(gammas)
    data=[beta,C,e['K'],e['D'],e['M'],e['J'],e['window_margin'],e['prefix_margin']]
   margin=cost+lower+Z-O;assert margin>0
   overlaps.append(margin)
   print('|'+ '|'.join(map(str,[k,side,r,s,Z,base,*data,lower,gam,margin]))+'|')
 assert len(overlaps)==30 and min(overlaps)==1
 assert 1226>4*78-10+587
 print('\nPASS: 17 inverse-gap rows including a14; 4 endpoint repairs; 13 dense diameter repairs; 30 overlap cases. Minimum overlap margin1.')
 print('Scope: a>=15 is assumed for the main range. Boundary k20 is checked conditionally; repaired-row P primitivity additionally assumes the valid post-integrality G146 conclusions. No AP case, bootstrap, or endpoint exclusion is certified here.')

if __name__=='__main__':verify()
