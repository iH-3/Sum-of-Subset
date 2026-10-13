"""Finite base certificate for rho(X)>=|X|-5 in non-full deleted intervals."""
from itertools import combinations

def stats(r,q,H):
    h=r+q; X=[x for x in range(1,h+1) if x not in H]; bits=1
    for x in X: bits |= bits << x
    total=sum(X); holes=total+1-bits.bit_count()
    mu=bits.bit_count()-1-r*(r+1)//2
    vals=set(X)|{0}
    defects=sum(not any(2*x-y in vals for y in vals if y<x) for x in X)
    rho=mu+2-2*defects
    return holes,rho,mu,defects

def verify():
    total=nonfull=0
    for r in range(10,15):
        counts=[0,0]; minmargin=None
        for q in range(1,4):
            for H in combinations(range(1,r+q),q):
                h,rho,mu,de=stats(r,q,H); total+=1; counts[0]+=1
                if h:
                    nonfull+=1;counts[1]+=1
                    if rho<r-5:raise AssertionError((r,q,H,h,rho))
                    minmargin=min(rho-r,minmargin) if minmargin is not None else rho-r
        print('r=%d total=%d nonfull=%d min(rho-r)=%d'%(r,*counts,minmargin))
    print('PASS:',total,'complete finite cases;',nonfull,'non-full cases')
    return total,nonfull
if __name__=='__main__':verify()
