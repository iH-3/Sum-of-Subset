"""Independent generic gap inventories and new size82 numerical licenses."""
from pathlib import Path
from collections import Counter
from itertools import combinations
import json,importlib.util
import model as m
ROOT=Path(__file__).resolve().parents[2]
need=m.need

def matrix(rows,eqs):
 out={};counts=Counter()
 for kind,rr in [('le',rows),('eq',eqs)]:
  for row,b,label in rr:
   key=kind+':'+label+':'+str(counts[kind+':'+label]);counts[kind+':'+label]+=1
   out[key]=(row,b,kind)
 return out

def evaluate(cert,data):
 lhs=Counter();rhs=0;seen=set()
 need(cert['denominator'] is None,'Generic gap certificate scope')
 for key,weight in cert['weights']:
  need(key in data and key not in seen and type(weight) is int and weight!=0,'Generic gap row');seen.add(key)
  row,b,kind=data[key];need(kind=='eq' or weight>0,'Generic gap sign')
  for name,c in row.items():lhs[name]+=weight*c
  rhs+=weight*b
 need(all(v>=0 for v in lhs.values()) and rhs<0,'Generic gap exact contradiction')
 return -rhs
def gap_system(kind,label):
    rows=[];eqs=[];v=m.var;add=m.add
    def ge(row,b,name):rows.append(({k:-x for k,x in row.items()},-b,name))
    for s,o in [('s','t'),('t','s')]:
        eqs.append((add((1,v('M'+s)),(-1,v('R'+s)),(-1,v('e'+s))),0,'source maximum '+s))
        for name,b in [('R',1),('e',4),('X',1),('g',1)]:ge(v(name+s),b,'positive '+name+s)
        ge(add((1,v('h'+s)),(-1,v('X'+s))),1,'active alpha '+s)
        ge(add((1,v('d'+s)),(-1,{'Ms':1,'Mt':1}),(-2,v('X'+s)),(-1,v('X'+o)),(-1,{'gs':1,'gt':1}),(-1,v('h'+o))),1,'active C5 '+s)
        ge(add((1,v('d'+s)),(-1,v('h'+s)),(-1,v('X'+s))),1,'strict ten-label guard '+s)
        ge(add((1,v('d'+o)),(-1,v('h'+s))),1,'opposite outer guard '+s)
    afull=add((1,v('ds')),(-1,v('Xs')));acore=add((1,afull),(-1,v('es')))
    bfull=add((1,afull),(1,v('hs')),(-1,{'Ms':1,'Mt':1}));bcore=add((1,bfull),(1,v('et')))
    if kind=='core_final':
        ge(add((1,v('ds')),(-1,v('hs')),(-1,v('es'))),1,'alpha peels below core gap')
        ge(add((1,acore),(-1,{'gs':1,'hs':1})),1,'U3 below core gap')
    a,b=(afull,bfull) if kind=='full' else(acore,bcore)
    value=m.fixed_forms()[label]
    rows +=[(add((1,a),(-1,value)),-1,'tested point above gap lower'),(add((1,value),(-1,b)),-1,'tested point below gap upper')]
    return matrix(rows,eqs)
def determinant(a):
    if len(a)==1:return a[0][0]
    return sum((-1)**j*a[0][j]*determinant([row[:j]+row[j+1:] for row in a[1:]]) for j in range(len(a)))

def verify():
 packet=json.loads((ROOT/'data/upper82_global_gap_inventory.json').read_text())
 full={'C+33','C+34','C+44','C+15','C+26','C+27','C+28','U+2','U+3','V+2'}
 initial=full|{'U+4'};final=initial-{'U+3','U+4','V+2'}
 keep={'full':full,'core_initial':initial,'core_final':final}
 expected={(kind,label) for kind in keep for label in m.fixed_forms() if '+' in label and label not in keep[kind]}
 seen=set();margins=[]
 for rec in packet['records']:
  key=(rec['kind'],rec['label']);need(key in expected and key not in seen,'Gap inventory coverage');seen.add(key)
  margins.append(evaluate(rec['certificate'],gap_system(*key)))
 need(seen==expected and len(seen)==136,'Complete generic fixed gap inventory')
 T=lambda n:n*(n+1)//2
 guards=[]
 for w in range(0,15,2):
  mass=min(max(59+2*w,T(p//2)+T((p+1)//2))-4*p for p in range(67)) if w else -12
  first=30+mass-w-w//2
  guard=[first,77-w-w//2,37-w-w//2,38-w-w//2]
  need(min(guard)>0,'Size82 ownerless actual-gap licenses')
  guards.append(dict(w=w,mass_minus_four_phi=mass,strict_margins=guard))
 need(74-47==27 and 27+4>12 and 148-195+59>0,'Size82 leading hull licenses')
 need(3*74-195-14>0,'All j>=3 leadings actually hit')
 forms=[(1,0,0),(0,1,0),(0,0,1),(1,1,1),(1,-1,-1),(1,-2,-2)]
 minors=set()
 for size in range(1,4):
  for rows in combinations(range(6),size):
   for cols in combinations(range(3),size):minors.add(abs(determinant([[forms[i][j] for j in cols] for i in rows])))
 need(minors=={0,1,2,3},'Torus pattern denominator42 license')
 need(len(m.residue_patterns())==24,'Residue pattern census')
 counts=[]
 for j in range(1,7):
  integer=list(m.patterns(j));partial=list(m.partial_patterns(j))
  need(len({tuple(sorted(st.items())) for st in integer+partial})==len(integer)+len(partial),'No repeated activity pattern')
  counts.append((len(integer),len(partial)))
 need(counts==[(22,0),(66,0),(156,0),(327,30),(610,210),(1036,776)],'Complete activity census')
 need(3*4+4+10+11==37 and 2*4+4+10+8==30,'Core-gap candidate capacities')
 need(130-113+14==31 and (31+1)//2==16,'Alpha initial gap bound')
 need(1+3*16>26 and 1+3*16>16 and 5*74-195>0,'Alpha exact tail licenses')
 need(366-4*113+4*22>0,'Alpha half-mass compression')
 spec=importlib.util.spec_from_file_location('size82_generic_tail',ROOT/'verification/upper83_tail.py')
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 inventory=module.tail_inventory(m.LABELS)
 excluded={f'U+{i}' for i in range(3,9)}|{f'V+{i}' for i in range(3,9)}|{f'C+2{i}' for i in range(5,9)}
 from exact import tail_labels
 need(set(inventory['fixed_tail'])-excluded==tail_labels('s'),'Exact sixteen remaining tail slots')
 # In the generic positive cone d_s=g_s+X_s+q, the tail endpoint
 # B=H_s+M_s is g_s+h_s+q. These sixteen deleted fixed values are <=B.
 for label in excluded:
  body=m.add((1,{'gs':1,'hs':1,'q':1}),(-1,m.fixed_forms()[label]))
  ds=body.pop('ds',0)
  body=m.add((1,body),(ds,{'gs':1,'Xs':1,'q':1}))
  need(all(c>=0 for c in body.values()),'Tail deletion cone '+label)
 from exact import quartet_rows
 quartet_cases=0
 for a,b,c,e in combinations(range(1,21),4):
  values=(a,b,c,e);B=len({x+y for x in values for y in values if x+y>e})
  point=dict(zip(('as','bs','cs','es','Bs'),(a,b,c,e,B)))
  need(all(sum(v*point[k] for k,v in row.items())<=rhs for row,rhs,_ in quartet_rows('s',B)),'Quartet ordered-fringe inequality')
  quartet_cases+=1
 return dict(status='PASS_SIZE82_GEOMETRY',gap_certificates=136,minimum_integer_margin=min(margins),
             ownerless_guards=guards,activity_counts=counts,torus_minors=sorted(minors),
             tail_formal_types=inventory['formal_multisets'],tail_remaining=sorted(tail_labels('s')),quartet_regression_cases=quartet_cases)

if __name__=='__main__':print(json.dumps(verify(),indent=2))
