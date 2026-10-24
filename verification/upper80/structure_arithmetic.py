"""Size-81 structural arithmetic, conditional on the written geometry.

This is deliberately not an assertion of completed structural applicability
or of N <= 80. Profiles are supplied by the separately checked packet.
"""
from pathlib import Path
from fractions import Fraction
import gzip,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from endpoint_schedule import endpoint,tri as T,need
ROOT=Path(__file__).resolve().parents[2]
HS=(5,7,9,11,13,15,17,21,31,49)
def f(r):return r-5 if r>=17 else r-14 if r>=14 else -1 if r==13 else -8

def verify():
    pf={(row['h'],row['r']):row for row in json.loads(gzip.decompress((ROOT/'data/upper80_profiles.json.gz').read_bytes()))}
    schedules={}
    def ep(r,R):
        w=endpoint(r,R);schedules[r,R]=w;return w['H']
    need(96*65+1073-65**2==3088,'Opposite-pair quadratic constant')
    need(54**2<=3088<56**2 and (64-54)//2==5,'At least five opposite pairs')
    inverse=[];nonprimitive=[];high=[]
    for a in range(9,33):
        b=64-a;I=(32-a)**2;O=646-I;K=O-f(a)-f(b);U=T(a)+a-2;V=T(b)+b-2
        H=ep(b,O-T(a)+1-(a-3)-f(a));threshold=V-4*H-5
        if K>=threshold:
            RP=O-threshold-f(b);RQ=O-threshold-f(a);HP=ep(a,RP);HQ=ep(b,RQ)
            need(max(RP-T(a-2)+2,RQ-T(b-2)+2)<0,'High-kappa predecessors nonAP')
            need(HP+HQ<threshold,'High-kappa equal-unit exclusion')
            need(min(U-2*HP-2,V-2*HQ-2)>2*max(HP,HQ)+2,'High-kappa ratio-two gap filling')
            need(-9-2*I+2*max(HP,HQ)-2*(f(a-1)+f(b-1))<0,'High-kappa pre-G')
            need(f(a)+f(b)+threshold+136-3*max(HP,HQ)-O>0,'High-kappa terminal')
            high.append(dict(a=a,threshold=threshold,HP=HP,HQ=HQ));K=threshold-1
        need(K<V-2,'Larger strict inverse in repaired standard range')
        need(min(V-1-K,V-K-4*H-5,V-K-2*H-4,U-H-2)>0,'Standard repaired diameter')
        if a<=27:need(-9-2*I+2*H+(16 if a<=14 else 0)<0,'Standard pre-G')
        else:
            need(K+1-T(a)<T(a-2) and O-T(a)+1-(a-3)-f(a)<T(b-2)-2,'Standard nonAP predecessors')
            need(-9-2*I+2*H-2*(f(a-1)+f(b-1))<0,'Retained predecessor pre-G')
        inverse.append(dict(a=a,H=H))
        caps=[];allowed=[]
        for z in range(H+1):
            rq=max([f(b),*[pf[h,b]['rho'] for h in HS if h<=z]])
            cap=O-f(a)-rq-(T(a)+a-3)-136+3*z;caps.append(cap)
            if cap>=73:allowed.append(z)
        need(max(caps)<146 and 4*H<154,'Nonprimitive low-slack domain')
        if allowed:
            margin=T(b)+b-3-2*H-(b+582+4*max(allowed)-I)
            need(margin>0 and max(allowed)<=6 and max(caps)<=98,'Nonprimitive localization')
            nonprimitive.append(dict(a=a,zmax=max(allowed),capacity=max(caps),margin=margin))
    need([r['a'] for r in high]==[29,30,31,32],'High-kappa census')
    need([r['a'] for r in nonprimitive]==list(range(17,25)),'Nonprimitive census')
    predecessor=[]
    for r in range(15,50):
        s=64-r;I=(r-32)**2;O=646-I
        need(pf[49,r]['rho']+pf[49,s]['rho']+49>O,'Pre-G high holes')
        need(-9-2*I+96-2*(f(r-1)+f(s-1))<0,'Two nonAP predecessors')
        need(T(r-2)+T(s-2)-4>O,'Two AP predecessors')
        Z=5+I+f(s-1)
        if Z<=48:
            h=max(h for h in HS if h<=Z);margin=T(r-2)-2+pf[h,s]['rho']+Z-O
            need(margin>0,'One AP predecessor');predecessor.append(dict(r=r,Z=Z,margin=margin))
    small=[]
    for a in range(8,15):
        b=64-a;I=(32-a)**2;O=646-I;allowed=[]
        for z in range(max(0,O+17)):
            rq=max([f(b),*[pf[h,b]['rho'] for h in HS if h<=z and (h,b) in pf]])
            if f(a)+rq+max(46,z,136-2*z)<=O:allowed.append(z)
        if not allowed:small.append(dict(a=a,excluded=True));continue
        H=ep(b,O-f(a)-46);z=min(H,max(allowed));width=T(b)+b-3-2*H
        need(width>b+655+4*z-I and 4*z<154,'Small-rank propagation')
        need(423+z-I-(b-3)<=110 and 350+z-I-(b-3)<=40 and 277+z-I-(b-3)<0,'Small-rank bridge budgets')
        small.append(dict(a=a,H=H,zmax=z,j1_delta=423+z-I-(b-3),j2_delta=350+z-I-(b-3)))
    ap=[];three=[]
    for a in range(9,33):
        b=64-a;I=(32-a)**2;O=646-I;rp=-8 if a<=12 else -2 if a==13 else 0
        need(O-rp-f(b)<3*T(a),'At most three AP classes')
        need(2*(T(b)+b-3)>O-rp,'Parity reverse primitivity')
        need(T(a)+T(b-2)+2-2*b+rp>O and 3*T(b-2)-T(b)+4-2*b>O-rp,'AP offscale exclusions')
        if O-rp-f(b)>=2*T(a):
            H=ep(b,O-2*T(a)-rp)
            need(T(b)+b-3>O-rp and O-2*T(a)-rp-f(b)-136+3*H<0,'Three-class terminal')
            need(ep(b,O-T(a)-rp)<T(a),'No-clipping schedule');three.append(a)
        for W in range(1,64,2):
            mass=min(T(a)+1+(b-t)*(b-t+1)+W*t+t*(t-1)-W-T(b) for t in range(2,b+1))
            if mass>O+2*b-2-rp:break
        need(W<=23,'Odd least coefficient finite cap');z=W-3
        H=ep(b,O-T(a)-rp);predecessor_floor=f(b-1) if O-T(a)-rp<T(b-2)-2 else 0
        need(-9-2*I+2*min(z,H)-2*predecessor_floor+(16 if a<=14 else 0)<0,'Halfstep pre-G')
        need(2*T(a)+T(b)-2*z>b+655+4*z-I,'Halfstep source propagation')
        cap=O-T(a)-136+3*z-f(b)-rp
        need(cap<=180 and 423+z-I-(T(a)+f(b)+rp)<=110,'AP j1 bridge')
        need(350+z-I-(T(a)+f(b)+rp)<=40,'AP j2 bridge')
        ap.append(dict(a=a,Wmax=W-2,zmax=z,capacity=cap))
    need(three==list(range(10,23)),'AP three-class census')
    need(52-8>21 and 29<T(57) and 78<T(56) and 19<T(8),'Small AP boundary arithmetic')
    for a in (30,31):
        b=64-a;I=(32-a)**2;O=646-I;H=ep(a,O-T(b))
        need(O-T(b)-f(a)-136+3*H<0,'Larger AP terminal')
    need(ap[-1]['capacity']==-9,'Balanced AP reflected terminal')
    coremin=min(T(r)+2*(r-3)+pf[49,64-r]['mu']+(r-32)**2 for r in range(15,50))
    need(coremin==972 and coremin>496+56,'Low-hole individual core width')
    need(676+73-56>687-73+56 and 56<154,'Low-hole propagation')
    bands=[]
    for h,hi,mu,rho,Hcap in [(15,16,394,270,304),(17,20,434,310,280),(21,30,508,384,246),(31,48,658,534,168)]:
        need(min(pf[h,r]['mu']+pf[h,64-r]['mu'] for r in range(15,50))==mu,'Paired mass profile')
        need(min(pf[h,r]['rho']+pf[h,64-r]['rho'] for r in range(15,50))==rho,'Paired defect profile')
        need(646-rho-136+4*hi==Hcap and Hcap<352,'High-hole individual width')
        margin=-1097+3*73+Fraction(3,2)*(mu+rho)-3*hi
        need(margin>0 and 1056+mu-Hcap>2*hi-5,'High-hole propagation')
        if h>=17:need(mu+h>423,'Localized high-hole mass contradiction')
        else:need(423+16-mu<=110 and 350+16-mu<0,'High-hole small-slack bridge')
        bands.append(dict(z=[h,hi],mu=mu,rho=rho,Hcap=Hcap,margin=str(margin)))
    return dict(status='PASS_CONDITIONAL_SIZE81_STRUCTURAL_ARITHMETIC',global_upper_bound_certified=False,
                structural_applicability_certified=False,inverse=inverse,high_kappa=high,nonprimitive=nonprimitive,
                pre_G=predecessor,small=small,AP=ap,high_holes=bands,schedules=list(schedules.values()))

if __name__=='__main__':print(json.dumps(verify(),indent=2))
