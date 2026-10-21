"""Exact arithmetic for the written size-82 structural reduction.

The inequalities for arbitrary sets are proved in the companion report.
This module checks every discrete rank and endpoint witness used there.
"""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json
ROOT=Path(__file__).resolve().parents[2]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

old=load('retained_structure82','verification/upper82_global/structure.py')
T=old.T;nonap=old.nonap;endpoint=old.endpoint;need=old.need

def verify():
    pf,pstats=old.profiles()
    need(4*74-10-1090+635==-169 and 1089+647-168==1568 and 69+1568//2==853 and 1089-853-2*635==-1034,'Exact second-layer and width constants')
    need(96*66+1073-66**2==3053 and 55**2<=3053<57**2,'Five opposite pairs')
    need((65-55)//2==5,'Zero is not a diagonal exception')
    need(1+T(66)>24*82+77 and 1+T(65)>24*74+77,'Both signs survive')
    need(24*25<=643<25*26,'Initial smaller rank at least eight')
    inverse=[]
    for a in range(10,33):
        b=65-a;I=(32-a)*(33-a);O=635-I;rp,rq=nonap(a),nonap(b)
        need(1+T(a)+T(b)==1090+I and 22*74+97-1090-I==O,'Size82 constants')
        K=O-rp-rq;U=T(a)+a-2;V=T(b)+b-2
        need(K<V-2,'Larger-side strict inverse threshold')
        witness=endpoint(b,O-T(a)+2-(a-3)-rp);H=witness['H']
        need(-47-2*I+2*H+(16 if a<=14 else 0)<0,'Repaired pre-G layer')
        if a<=30:
            need(min(V-1-K,V-K-4*H-5,V-K-2*H-4,U-H-2)>0,'Standard repaired diameter')
        else:
            need(K<V-1 and 2*V-6*H-8>K,'At most one large subset-sum gap')
            need(K+2-T(a)<T(a-2),'Final disjoint translate contradicts failed inverse')
            need(U>H+2,'Central strip gives short diameters')
        cap=O-rp-rq-T(a)-a+1-138+3*H
        need(cap<148 and 4*H<156,'Nonprimitive failed-inverse budget')
        if cap>=74:
            need(16<=a<=27 and H<=28,'Low-slack nonprimitive range')
            need(T(b)+b-3-2*H>b+570+4*H-I,'Nonprimitive source translation propagation')
        inverse.append(dict(a=a,H=H,nonprimitive_cap=cap,witness=witness))
    need(max(x['nonprimitive_cap'] for x in inverse)==142,'Nonprimitive cap maximum')
    # The pre-G large-hole argument uses a stronger disjoint-last-step bound.
    overlap=[];exceptions=[]
    for r in range(15,51):
        s=65-r;I=(r-32)*(r-33);h=49 if I>=25 else 21
        margin=T(r-2)-2+pf[h,s]['elementary_rho']+24+I-(635-I)
        if margin<=0:
            need(r in (28,29),'Unexpected final-split exception')
            kcap=635-I-(T(r-2)-2)-pf[h,s]['elementary_rho']
            need(kcap<2*(r-1) and kcap<T(s) and kcap+1<=T(r-1)+1,'AP predecessor eliminates split')
            exceptions.append((r,kcap))
        need(margin+(r-4)+nonap(r-1)>0,'NonAP predecessor eliminates split')
        overlap.append(margin)
    need(exceptions==[(28,48),(29,38)],'Exact pre-G AP predecessor exceptions')
    # Small ranks, after the branch's own common-lattice proof.
    need(-8+52>35 and 40<T(9)-1 and 46+51-8>83,'Ranks eight and nine')
    effective=load('size82_effective','verification/upper83_complete/check_structure.py')
    witness=effective.effective(55,4,119)
    need(effective.rho(55,witness['mu'])==113 and 46+113-8>129,'Rank ten effective hole witness')
    need(138+50-8-2*25>129,'Rank ten has at least26 holes')
    small=[]
    for a in range(11,15):
        b=65-a;I=(32-a)*(33-a);O=635-I;rp,rq=nonap(a),nonap(b)
        ep=endpoint(b,O-rp-46);H=ep['H'];width=T(b)+b-3-2*H
        maximum=b+644-I+4*(O-rp-rq)
        if a<14:
            need(width>maximum and b-1>409-I+H,'Small rank localization and mass contradiction')
        else:
            need(H==20 and 4*H<156 and width>maximum-74,'Rank14 localization after j>=1')
            need(335-I+H<b-1 and 409-I+H-(b-1)==37,'Rank14 enters low-slack bridge')
        small.append(dict(a=a,H=H,width=width,source_max=maximum))
    # AP exceptions: all class counts, no-clipping licenses, and odd tails.
    ap=[];three=[];larger=[]
    for a in range(10,33):
        b=65-a;I=(32-a)*(33-a);O=635-I;rp=-8 if a<=12 else -2 if a==13 else 0
        need(O-rp-(b-5)<3*T(a),'At most three AP residue classes')
        need(2*(T(b)+b-3)>O-rp,'Parity branch reverse primitivity')
        need(T(a)+T(b-2)+2-2*b+rp>O,'Single offscale AP generator')
        need(3*T(b-2)-T(b)+4-2*b>O-rp,'Two offscale AP generators')
        if O-rp-(b-5)>=2*T(a):
            ep=endpoint(b,O-2*T(a)-rp);H=ep['H']
            need(T(b)+b-3>O-rp,'Three-class reverse primitivity')
            cap=O-2*T(a)-rp-(b-5)-138+3*H
            need(cap<0 and -47-2*I+2*H+(16 if a<=14 else 0)<0,'Three-class terminal')
            three.append(a)
            # In the two-class alternative at these same ranks, a dense
            # primitive Q prevents clipping independently of the failed
            # global condition kappa<2(u-1).
            ep2=endpoint(b,O-T(a)-rp)
            need(ep2['H']<T(a),'Parity-fiber no-clipping by dense Q')
            # The same dense-Q witness excludes a clipped gap in the
            # one-class alternative. Its putative clip already costs T_a;
            # reverse residue counting licenses Q primitivity at these ranks.
            need(T(b)+b-3>O-rp,'One-class clipped-gap reverse primitivity')
        else:need(O-rp-(b-5)<2*T(a),'Parity-fiber no-clipping by excess')
        if a<=30:
            need(O-nonap(a)<T(b) and O-rp<T(b),'Larger AP one class')
        else:
            need(O-nonap(a)<2*T(b) and O-rp<2*T(a),'Balanced AP at most two classes')
            need(T(b)+T(a-2)+2-2*a>O and 2*(T(a)+a-3)>O,'Larger AP offscale and reverse gcd')
            ep=endpoint(a,O-T(b));H=ep['H']
            need(O-T(b)-nonap(a)-138+3*H<0,'Larger AP two-class terminal')
            need(T(a)+138>O,'Both AP unequal steps')
            larger.append(a)
        mass=min(T(a)+1+(b-t)*(b-t+1)+21*t+t*(t-1)-21-T(b) for t in range(2,b+1))
        need(mass>O+2*b-2-rp,'Unbounded odd least coefficient W>=21')
        halfcap=O-T(a)-138+54-(b-5)-rp;nonprim=O-138-T(a)-rp
        need(O-rp-(b-5)-(T(b)+b-1)-138<0,'Larger nonAP side primitive after one-class no-clipping')
        need(halfcap<=150 and nonprim<148,'AP low-slack caps')
        need(-47-2*I+36+(16 if a<=14 else 0)<0,'Halfstep pre-G layer')
        need(2*T(a)+T(b)-36>b+644+72-I,'Halfstep central strip propagates through source')
        ap.append(dict(a=a,halfstep_cap=halfcap,one_class_nonprimitive_cap=nonprim))
    need(three==list(range(11,22)) and larger==[31,32],'AP exceptional rank census')
    need(min((32-a)*(33-a)+T(a) for a in range(10,33))==363>335+18,'No halfstep j>=2')
    need(T(20)+T(21)>437 and 66-40>=24,'Uniform low-slack overlap floor')
    # Low holes and the three bounded high-hole bands.
    coremin=min(T(r)+2*(r-3)+pf[49,65-r]['mu']+(r-32)*(r-33) for r in range(15,51))
    need(coremin==799>483+56,'Low-hole individual core width')
    need(724+74-56>677-74+56 and 56<156,'Low-hole source propagation')
    bands=[]
    for h,hi,mu,rho,Hcap in [(15,16,402,276,285),(17,20,443,317,260),(21,48,481,355,334)]:
        need(min(pf[h,r]['mu']+pf[h,65-r]['mu'] for r in range(15,51))==mu,'Paired high-hole mass')
        need(min(pf[h,r]['elementary_rho']+pf[h,65-r]['elementary_rho'] for r in range(15,51))==rho,'Paired high-hole defect')
        need(635-rho-138+4*hi==Hcap,'High-hole hull cap')
        need(min(T(r)+(r-32)*(r-33) for r in range(15,51))==363>Hcap,'High-hole individual core width')
        margin=-1034+3*74+Q(3,2)*(mu+rho)-3*hi
        need(margin>0 and mu+h>409,'High-hole propagation and j>=1 terminal')
        need(1089+mu-Hcap>2*hi-5 and hi<156,'High-hole j0 propagation and terminal')
        bands.append(dict(z=[h,hi],mu=mu,rho=rho,width_margin=str(margin)))
    need(min(pf[49,r]['mu']+pf[49,65-r]['mu'] for r in range(15,51))==509,'Tail paired mass')
    need(min(pf[49,r]['elementary_rho']+pf[49,65-r]['elementary_rho'] for r in range(15,51))==383,'Tail paired defect')
    need(min(T(r)+pf[49,r]['mu']+(r-32)*(r-33)-252 for r in range(15,51))==220,'Tail individual core width')
    margins=[]
    for r in range(15,51):
        s=65-r;I=(r-32)*(r-33)
        mu=pf[49,r]['mu']+pf[49,s]['mu'];rho=pf[49,r]['elementary_rho']+pf[49,s]['elementary_rho']
        zmax=635-I-74-rho
        for opposite in (r,s):
            # The expression decreases in z and increases in c.  Evaluate
            # the worst admissible z and c=74, even when this enlarges domain.
            minimum=opposite+4+(pf[49,opposite]['mu']+zmax+opposite-1)//opposite
            margins.append(-1034+4*I+3*74+Q(3,2)*(mu+rho)-3*zmax+minimum)
    need(min(margins)==42>0,'Tail propagation needs each source maximum, not their sum')
    need(1089+509-504>2*252-5 and 509>483,'Tail j0 and localized mass contradictions')
    return dict(status='PASS_SIZE82_STRUCTURAL_ARITHMETIC',inverse=inverse,pre_G_AP_predecessors=exceptions,
                small=small,AP=ap,three_class_ranks=three,larger_AP_ranks=larger,
                high_hole_bands=bands,tail_source_margin=str(min(margins)),profiles=pstats)

if __name__=='__main__':print(json.dumps(verify(),indent=2,default=str))
