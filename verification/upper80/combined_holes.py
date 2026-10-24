"""Complete merged-prefix checks for two-core low-hole mass floors.

All branches use exact integers. The finite prefix has at most two copies
of each value, with a fixed ordering of equal values from the two cores.
"""
from functools import lru_cache
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from profiles import need,tri

@lru_cache(None)
def prove(r,s,C,hole_cap):
    need(all(type(v) is int for v in (r,s,C,hole_cap)) and min(r,s)>0 and C>=0 and hole_cap>=0,'Combined prefix domain')
    stats=dict(nodes=0,pruned=0,terminals=0,max_depth=0)
    @lru_cache(None)
    def stable(p0,q0,H):
        for p in range(p0,r+1):
            for q in range(q0,s+1):
                if (p,q)==(r,s):continue
                a,b=r-p,s-q;S=tri(p)+tri(q)
                upper=(C+tri(r)+tri(s)-S-tri(a-1)-tri(b-1))//(a+b)
                if S-2*H+1<upper:return False
        return True
    def visit(p,q,ls,lt,last,side,S,bits):
        stats['nodes']+=1;stats['max_depth']=max(stats['max_depth'],p+q)
        a,b=r-p,s-q
        # For equal values, the s copy must precede the t copy.
        ns=max(ls+1,last+(side==1));nt=max(lt+1,last)
        cost=S+a*ns+tri(a-1)+b*nt+tri(b-1)-tri(r)-tri(s)
        if cost>C:stats['pruned']+=1;return
        holes=S+1-bits.bit_count()
        if holes<=hole_cap:
            H=0 if not holes else max(i for i in range(S//2+1) if not bits>>i&1)+1
            if stable(p,q,H):stats['terminals']+=1;return
        need(p+q<12,'Uncertified merged prefix')
        need(a+b>0,'Uncertified complete pair')
        upper=(C+tri(r)+tri(s)-S-tri(a-1)-tri(b-1))//(a+b)
        for physical,minimum in ((0,ns),(1,nt)):
            if (physical==0 and not a) or (physical==1 and not b):continue
            for value in range(minimum,upper+1):
                visit(p+(physical==0),q+(physical==1),value if physical==0 else ls,
                      value if physical==1 else lt,value,physical,S+value,bits|(bits<<value))
    visit(0,0,0,0,0,-1,0,1)
    return stats

def total_rows(retained=False):
    # On W in {1,2}, paired mass floors are N and 2N-2.
    row={'ts':-1,'tt':-1,'hole_W':60 if retained else 62}
    if retained:row.update(xs=1,xt=1)
    return row,-2,'combined retained hole floor' if retained else 'combined core hole floor'

def verify():
    cases=[]
    for N,ks in [(64,range(18)),(62,range(11))]:
        for k in ks:
            r,s=N//2-k,N//2+k
            for W in (1,2):
                floor=N if W==1 else 2*N-2
                stats=prove(r,s,floor-1,2*W-2)
                first=lambda rank:list(range(2,rank+2)) if W==1 else [2,*range(4,rank+3)]
                A,B=first(r),first(s);bits=1
                for value in A+B:bits|=bits<<value
                need(sum(A+B)-tri(r)-tri(s)==floor,'Sharp combined mass example')
                need(sum(A+B)+1-bits.bit_count()==2*W,'Sharp combined holes example')
                cases.append(dict(N=N,k=k,W=W,mass_floor=floor,**stats))
    rejected=False
    try:prove(32,32,126,2)
    except ValueError:rejected=True
    need(rejected,'Sharp false combined floor must be rejected')
    import itertools
    controls=0
    for r,s in ((2,3),(3,3),(3,4)):
        catalogue=[]
        for a,b in itertools.product(itertools.combinations(range(1,r+7),r),itertools.combinations(range(1,s+7),s)):
            excess=sum(a+b)-tri(r)-tri(s)
            if excess>6:continue
            bits=1
            for v in a+b:bits|=bits<<v
            catalogue.append((excess,sum(a+b)+1-bits.bit_count()))
        for C in range(7):
            for cap in (0,2):
                try:prove(r,s,C,cap)
                except ValueError:continue
                need(all(h<=cap for excess,h in catalogue if excess<=C),'Independent small-rank combined enumeration')
                controls+=1
    return dict(status='PASS_COMBINED_LOW_HOLE_MASS',global_upper_bound_certified=False,
                structural_applicability_certified=False,cases=cases,
                prefix_nodes=sum(c['nodes'] for c in cases),terminal_prefixes=sum(c['terminals'] for c in cases),
                max_prefix_length=max(c['max_depth'] for c in cases),independent_small_domains=controls,negative_controls=1)

if __name__=='__main__':print(json.dumps(verify(),indent=2))
