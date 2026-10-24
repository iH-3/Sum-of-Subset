from itertools import combinations
import json

def check(r):
 cap=2*r-3;sets=aps=0;minimum=999
 def visit(prefix,last,left):
  nonlocal sets,aps,minimum
  if len(prefix)==r:
   sets+=1;X=tuple(i+1+d for i,d in enumerate(prefix));S=sum(X);bits=1
   for x in X:bits|=bits<<x
   if bits!=(1<<(S+1))-1:return
   aps+=1;pair={a+b for a,b in combinations((0,*X),2)};delta=sum(2*x not in pair for x in X);rho=S-r*(r+1)//2+2-2*delta
   if rho<0:raise ValueError((X,rho))
   minimum=min(minimum,rho);return
  left_slots=r-len(prefix)
  for d in range(last,left//left_slots+1):visit(prefix+[d],d,left-d)
 visit([],0,cap)
 # Integer partition recurrence: partitions of weight<=cap into <=r parts.
 dp=[0]*(cap+1);dp[0]=1
 for part in range(1,r+1):
  for n in range(part,cap+1):dp[n]+=dp[n-part]
 if sets!=sum(dp):raise ValueError('Incomplete deficit enumeration')
 return dict(rank=r,deficit_cap=cap,sets=sets,AP_support_sets=aps,minimum_rho=minimum)
rows=[check(r) for r in range(2,15)]
print(json.dumps(dict(status='PASS_SMALL_AP_RHO_NONNEGATIVE',rows=rows,total_sets=sum(r['sets'] for r in rows)),indent=2))
