from pathlib import Path
import sys,random,json
root=Path(__file__).resolve().parents[3];sys.path.insert(0,str(root/'verification/upper80'));import exact
rng=random.Random(24102026);tested=improvements=0;best=0
for sample in range(2501):
 k=rng.randrange(18) if sample else 0;point={'ONE':1,'rank_k':k};sides={}
 for side,r in [('s',32-k),('t',32+k)]:
  defects=[0]*(r-5)+sorted(rng.randrange(6) for _ in range(5));core=[i+1+d for i,d in enumerate(defects)]
  offsets=sorted(rng.sample(range(1,201),4))
  if sample==0:core=list(range(1,33));defects=[0]*32;offsets=[1,2,67,143] if side=='s' else [1,2,129,175]
  R=core[-1];sides[side]=core+[R+off for off in offsets]
  point.update({'R'+side:R,'M'+side:R+offsets[-1],'t'+side:sum(defects),'x'+side:defects[-1]})
  point.update({off+side:value for off,value in zip('abce',offsets)})
  point['B'+side]=len({a+b for a in offsets for b in offsets if a+b>offsets[-1]})
 D={0,*sides['s'],*(-x for x in sides['t'])};point['K']=len({a+b for a in D for b in D})
 evaluate=lambda row:sum(c*point[name] for name,c in row.items())
 u=sum(evaluate(exact.trim_pair_guard(side,pair))<=0 for side in 'st' for pair in exact.TRIM_PAIRS)
 excluded={key:{pair for pair in exact.sumset_gap_pairs(key) if any(evaluate(row)<=0 for row in exact.sumset_gap_guards(key,pair))} for key in exact.SUMSET_GAPS}
 equalities={}
 for key in exact.SUMSET_GAPS:
  side=key[0].lower();classes={}
  for pair in exact.sumset_gap_pairs(key):
   value=sum(evaluate(exact.signed_source_point(tag,side)) for tag in pair)
   classes.setdefault(value,[]).append(pair)
  equalities[key]=[(pairs[0],pair) for pairs in classes.values() for pair in pairs[1:]]
 keys=[]
 for key in [k for k in exact.SUMSET_GAPS if k[0].islower()]:
  side,other,lower,upper,qs,qo=exact.sumset_gap_data(key)
  length=evaluate(upper)-evaluate(lower)-evaluate(qs)-evaluate(qo)-1
  if length>40-len(excluded[key]):keys.append(key)
 capkeys=[]
 for key in [k for k in exact.SUMSET_GAPS if k[0].isupper()]:
  side,other,lower,upper,qs,qo=exact.sumset_gap_data(key)
  if evaluate(upper)-evaluate(lower)-evaluate(qs)-evaluate(qo)-1>40-len(excluded[key]):capkeys.append(key)
 if capkeys:
  cr,cb,_=exact.sumset_gap_capacity(capkeys,excluded,u)
  if evaluate(cr)>cb:raise ValueError(('False capped source gap bound',sample,point['K'],evaluate(cr),cb))
 row,rhs,_=exact.sumset_gap_capacity(keys,excluded,u)
 if evaluate(row)>rhs:raise ValueError(('False source gap bound',sample,point['K'],evaluate(row),rhs))
 outerrow,outerrhs,_=exact.trim_hull_row(u);old=point['K']+outerrhs-evaluate(outerrow);new=point['K']+rhs-evaluate(row)
 improvements+=new<old;best=max(best,old-new);tested+=1
 equal_bounds=[]
 for capped in (False,True):
  chosen=[]
  for key in exact.SUMSET_GAPS:
   if key[0].isupper()!=capped:continue
   side,other,lower,upper,qs,qo=exact.sumset_gap_data(key)
   if evaluate(upper)-evaluate(lower)-evaluate(qs)-evaluate(qo)-1>exact.sumset_gap_remaining(key,excluded[key],equalities[key]):chosen.append(key)
  if not chosen:continue
  er,eb,_=exact.sumset_gap_capacity(chosen,excluded,u,equalities)
  if evaluate(er)>eb:raise ValueError(('False source equality-class capacity',sample))
  equal_bounds.append(point['K']+eb-evaluate(er))
 if sample==0:example=dict(actual=point['K'],old_trim_bound=old,new_gap_bound=new,equality_class_bound=min(equal_bounds),active_gaps=keys)
print(json.dumps(dict(status='PASS_SOURCE_GAP_UPPER_BOUND',cases=tested,strict_improvements=improvements,largest_improvement=best,example=example)))
