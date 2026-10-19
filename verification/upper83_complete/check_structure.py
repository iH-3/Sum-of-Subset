"""Finite arithmetic for the written size-84 structural and localization proof.
The general inverse, stability, cover and interval lemmas are mathematical inputs.
"""
import importlib.util
import json
from pathlib import Path
from fractions import Fraction as Q

ROOT=Path(__file__).resolve().parents[2]
T=lambda r:r*(r+1)//2

def need(p,msg):
    if not p: raise ValueError(msg)

def nonap(r):
    return r-5 if r>=21 else r-14 if r>=14 else -1 if r==13 else -8

def effective(r,beta,C):
    K=3
    while (K+1)*(K-2)//2<=C+1: K+=1
    D=C+max(3,K);M=2*beta
    while T(M)-6*beta<=M+D+2:M+=1
    J=max(K+1,2*beta+5,M)
    margins=((r-J+1)*beta-D,T(J-1)-1-D)
    need(min(margins)>0,'effective hole witness')
    return dict(r=r,beta=beta,C=C,J=J,margins=margins,mu=r+C+1)

def rho(r,mu):
    floors=[nonap(r),mu+2-2*r]
    for g in range(2,11):
        sat=(g-1)*(r-14)
        floors.append(min([v for v in range(sat) if mu<=v+4*g-2+2*(v//(g-1))]+[sat]))
    return max(floors)

ENDPOINTS=[(4,14),(5,14),(7,14),(8,14),(8,21),(9,20),(9,21),(9,21),(9,22),(9,22),(9,22),(9,22),(8,22),(8,14),(7,14),(6,20),(5,21),(5,14),(4,14),(3,14)]

def endpoint(b,R,beta,q):
    if q==14: start=0;j=b-R//(beta-1)
    else:
        need(q>=20 and T(q)-b-1>R,'nonAP starting prefix')
        start=nonap(q);j=max(q+1,21,-(-((beta-1)*b-R-5)//(beta-2)))
    margins=(start+(beta-1)*(b-q)-R,j-(2*beta+5),T(j)-b-1-R,T(j)-6*beta-j-R-3)
    need(margins[0]>0 and margins[1]>=0 and min(margins[2:])>0,'endpoint strict margins')
    need(15<=j<=b,'endpoint size')
    need(all(T(size)-6*beta>size+R+3 for size in range(j,b+1)),'extension to final size')
    return j,margins

def profiles():
    path=ROOT/'verification/upper84/audit/verification_program/foundations'
    spec=importlib.util.spec_from_file_location('retained_foundations83',path/'__init__.py',submodule_search_locations=[str(path)])
    mod=importlib.util.module_from_spec(spec)
    import sys
    sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
    stats=mod.profiles_H_only()
    data=json.loads((path/'dense/data/profiles.json').read_text())
    return {(x['h'],x['r']):x for x in data},stats

def verify():
    pf,pstats=profiles(); rows=[]
    need(96*68+1073-68**2==2977 and 55**2>2977,'opposite pairs')
    need(1+T(68)>24*84+77 and 1+T(67)>24*76+77,'both signs survive')
    need(25*26>620 and 24*25<=620,'bootstrap a>=9')
    for k in range(22):
        a,b=33-k,34+k;I=k*(k+1);O=612-I;rp,rq=nonap(a),nonap(b)
        need(1+T(a)+T(b)==1157+I and 22*76+97-1157-I==O,'new budget')
        Kmax=O-rp-rq;V=T(b)+b-2;U=T(a)+a-2
        need(Kmax<V-2,'larger-side strict inverse threshold')
        floor=(a-3)+rp+rq-(O-T(a)+2)
        if k<2:need(floor>0,'automatic small-side inverse');continue
        need(floor<=0,'complete failed sufficient test inventory')
        R=O-T(a)+2-(a-3)-rp;beta,q=ENDPOINTS[k-2];j,m=endpoint(b,R,beta,q)
        H=2*beta;alpha=4*beta+2
        diam=(V-1-Kmax,V-Kmax-2*alpha-1,V-Kmax-alpha-2,U-H-2)
        need(min(diam)>0,'short diameter applications')
        layer=-125-2*I+2*H+(16 if a<=14 else 0)
        need(layer<0,'repaired pre-G overlap')
        cap=O-rp-rq-T(a)-a+1-142+3*H
        if a>=15:need(cap<76 and 4*H<160,'nonprimitive exclusion via j0')
        else:need(O-rp-rq-142+2*H<76 and 4*H<160,'small repaired boundary j0')
        rows.append(dict(k=k,a=a,b=b,R=R,beta=beta,q=q,j=j,zcap=H,margins=m,diameter=diam,layer=layer,nonprimitive_cap=cap))
    overlap=[]
    for r in range(15,53):
        s=67-r;I=(r-33)*(r-34)
        margin=T(r-2)+2-2*r+pf[49,s]['elementary_rho']+63+I-(612-I)
        need(margin>0,'pre-G large-hole final overlap')
        overlap.append(margin)
    need(min(overlap)==77,'overlap minimum')
    # AP cases, including the balanced both-AP branch.
    aps=[]
    for a in range(12,34):
        b=67-a;I=(33-a)*(34-a);O=612-I;rp=-8 if a==12 else -2 if a==13 else 0
        need(O-nonap(a)<T(b),'ONLY larger AP one residue')
        if a<=32:need(O-rp<T(b),'both AP: larger support forces one residue')
        else:need(O-rp<2*T(a),'balanced both AP: at most two residues')
        need(O-rp-(b-5)<2*T(a),'only smaller AP: at most two residues')
        clip=T(a)+T(b-2)+2-2*b+rp-O
        need(clip>0,'clipped or unique offscale AP case')
        # For fixed t>=2 the slope in odd W is t-1>0, so W=19 covers all W>=19.
        mass=min(T(a)+1+(b-t)*(b-t+1)+19*t+t*(t-1)-19-T(b) for t in range(2,b+1))
        need(mass>O+2*b-2-rp,'unbounded odd-coefficient tail W>=19')
        cap=O-T(a)-142+48-(b-5)-rp
        nonprim=O-142-T(a)-rp
        need(cap<152 and nonprim<152,'AP low-c conclusion')
        need(-125-2*I+32+(16 if a<=14 else 0)<0,'half-step pre-G layer')
        aps.append(dict(a=a,b=b,odd_tail_margin=mass-(O+2*b-2-rp),halfstep_cap=cap,nonprimitive_cap=nonprim))
    need(max(x['halfstep_cap'] for x in aps)==93,'AP halfstep cap93')
    need(max(x['nonprimitive_cap'] for x in aps)==85,'AP nonprimitive cap85')
    need(12+64<80 and (17+64)/2-2<6*27-75,'unlocalized j1 low-c terminal')
    need(2*T(21)>444,'F>=27 with tau<=444')
    # Boundary rows and independent effective witnesses.
    eff=[effective(56,5,132),effective(55,4,119),effective(54,6,168)]
    need([rho(x['r'],x['mu']) for x in eff]==[125,113,153],'boundary defect floors')
    need(-8+53>12 and 142>20,'a9')
    need(16<T(10)-1 and 48+52-8>60,'a10')
    need(63<T(11)-1 and 142-2*39+51-8>106 and 125>114,'a11')
    need(142-12+50-8>150 and 142-32+50-8>150 and 48+113-8>150,'a12')
    need(48+153-1>192 and 192-48-142+24==26<76,'a13 strict')
    need(pf[15,53]['rho']==269>232 and 232-48-142+28==70<76,'a14 strict')
    # Uniform low-hole localization, source activity and positive rank defect.
    need(min(T(r)+(r-33)*(r-34) for r in range(1,67))==385,'mass quadratic')
    need(max(r-(r-33)*(r-34) for r in range(1,67))==34,'max rank quadratic')
    need(76-56-10==10 and 822+76-56==842>655-76+56==635,'low-hole joins')
    need(min(T(r)+7*r+2*(r-33)*(r-34) for r in range(1,67))==644,'P2 activity')
    need(min(T(r)+5*r+2*(r-33)*(r-34) for r in range(1,67))==593,'P3+ activity')
    need(T(33)>352,'prefix missing first hole')
    for n in range(1,67):
        for k in range(1,n):need((n-k)*(T(k-1)+1)>=n-1,'incomplete-prefix mass defect')
    # High-hole paired profiles and interval extension.
    bands=[]
    for h,hi,mu,rho0,cap,Hcap,cm in [(15,16,418,288,214,246,139),(17,20,461,331,179,219,166),(21,48,503,373,191,289,96)]:
        need(min(pf[h,r]['mu']+pf[h,67-r]['mu'] for r in range(15,53))==mu,'paired mass')
        need(min(pf[h,r]['elementary_rho']+pf[h,67-r]['elementary_rho'] for r in range(15,53))==rho0,'paired defect')
        actualcap=max(612-rho0-max(48,z,142-2*z) for z in range(h,hi+1))
        need(actualcap==cap,'band budget cap')
        need(612-rho0-142+4*hi==Hcap,'band H cap')
        need(385-Hcap==cm>0,'individual core mass exceeds H')
        margin=-904+Q(3,2)*(mu+rho0)-3*hi
        need(margin>0,'all source peel translates join')
        bands.append(dict(z=[h,hi],mu=mu,rho=rho0,I_plus_c_cap=cap,H_cap=Hcap,core_margin=cm,width_margin=margin))
    need(min(pf[49,r]['mu']+pf[49,67-r]['mu'] for r in range(15,53))==539,'tail mu')
    need(min(pf[49,r]['elementary_rho']+pf[49,67-r]['elementary_rho'] for r in range(15,53))==409,'tail rho')
    need(612-409==203 and 203-49==154,'tail domain')
    coremin=min(T(r)+2*(r-33)*(r-34)-406 for r in range(15,53))
    need(coremin==56>0,'tail individual mass')
    need(-904+Q(3,2)*(539+409)==518,'tail width')
    need(518-3*203+6*76==365>0,'tail j>=1 join')
    need(539+2*409-68==1289>2*203-5==401,'tail j0 join')
    need(418>380 and 539>456 and 48<160,'localized high-hole contradictions')
    return dict(status='PASS',inverse_rows=rows,pre_G_overlap_minimum=min(overlap),AP=aps,effective=eff,profile_replay=pstats,high_hole_bands=bands,tail_core_margin=coremin)

if __name__=='__main__':print(json.dumps(verify(),indent=2,default=str))
