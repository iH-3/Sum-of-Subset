"""New finite-tail endcaps on actual source/core powers, including shapes."""
from pathlib import Path
import sys,json,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import model as m,first_gap_core as fg,full_cover as fc,core_gap as cg,tail_caps as tc
rng=random.Random(2026102420);checks=prefix_checks=old_matches=sharp=0
for shape in [None,0,1,2,3]:
 for trial in range(8):
  k=rng.randrange(18);v={'ONE':1,'rank_k':k};E={0};tails=[];orders={}
  for side,r,sign in [('s',32-k,1),('t',32+k,-1)]:
   h=t=0
   if shape is not None:h,ps,pt=fg.CASES[shape];t=ps if side=='s' else pt
   n=r-t;phi0=rng.randrange(2,14)
   d=[max(0,phi0-n+i) for i in range(1,n+1)] if trial%2 else sorted(rng.randrange(13) for _ in range(n))
   X=([1] if t else [])+[h+i+y for i,y in enumerate(d,1)]
   phi=min([r,*[x+r-2*i for i,x in enumerate(X,1)]]);E.update(sign*x for x in X)
   v.update({'R'+side:X[-1],'x'+side:X[-1]-r,'t'+side:sum(X)-r*(r+1)//2,'phicore'+side:phi})
   offsets=sorted(rng.sample(range(1,90),4));v.update({off+side:x for off,x in zip('abce',offsets)});v['M'+side]=X[-1]+offsets[-1]
   v.update({letter+side:20 for letter in 'Xghd'});tails.extend(sign*(X[-1]+x) for x in offsets)
   ev=lambda row:sum(c*v[key] for key,c in row.items())
   for keep in range(1,5):
    order=min(13-keep,max(0,phi-h+t-keep-1));orders[side,keep]=order
    for ell in range(14-keep):
     size=r-keep-1;actual=sum(X[:size])-size*(size+1)//2
     m.need(ev(tc.core_prefix(side,keep,ell,shape))<=actual,'Actual finite-tail predecessor prefix floor');prefix_checks+=1
  D=E|set(tails);power_sets=[{0},{0}]
  for q in range(1,5):
   root=next(i for i,chosen in enumerate(fc.roots()) if len(chosen)==4-q)
   for typ,base in enumerate([E,D]):
    power_sets[typ]={a+b for a in power_sets[typ] for b in base};node=(root,0 if typ==0 else -1)
    lo,hi=fc.interval(*node);shift=ev(lo)-min(power_sets[typ]);Q={a+shift for a in power_sets[typ]}
    for keep in range(1,5):
     for side in 'st':
      order=orders[side,keep] if typ==0 else 0;case=shape if typ==0 else None;scale=keep if typ==0 else 1
      guard,count=tc.derive({}, {},node,side,keep,order,case);constant=ev(guard)
      if side=='s':L=(constant+scale-1)//scale;U=max(Q)+2
      else:L=min(Q)-2;U=(-constant)//scale
      guard,count=tc.derive({'ONE':L},{'ONE':U},node,side,keep,order,case)
      actual=sum(L<=x<=U for x in Q)
      m.need(ev(guard)<=0 and actual<=count,'Actual q-sum finite-tail cap');checks+=1;sharp+=actual==count
      if keep==1:
       old=cg.extreme_only_guard({'ONE':L},{'ONE':U},node,side,case,order)
       m.need(old==guard and count==1,('One-point rule preserved exactly',shape,typ,side,order,old,guard));old_matches+=1
bad=0
for node,side,keep,order,shape in [((0,0),'s',0,0,None),((0,0),'s',5,0,None),((0,0),'s',True,0,None),((0,0),'z',2,0,None),((0,0),'s',4,10,None),((0,-1),'s',2,1,None),((0,-1),'s',2,0,0),((0,0),'s',2,0,4),((494,-1),'s',2,0,None)]:
 try:tc.derive({}, {},node,side,keep,order,shape)
 except ValueError:bad+=1
 else:raise ValueError('Invalid finite-tail endcap accepted')
print(json.dumps(dict(status='PASS_NEW_FINITE_TAIL_CAPS',actual_core_source_pairs=40,capacities=checks,sharp_caps=sharp,prefix_floors=prefix_checks,old_one_point_rules=old_matches,invalid_recipes_rejected=bad,global_upper_bound_certified=False)))
