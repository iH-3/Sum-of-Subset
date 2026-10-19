"""Exact arithmetic for proposed size83 structural reductions.
The general mathematical licenses require the companion proof; this file
alone is not a proof of the upper bound.
"""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,sys
ROOT=Path(__file__).resolve().parents[2]
T=lambda r:r*(r+1)//2

def need(ok,message):
    if not ok:raise ValueError(message)

def nonap(r):
    return r-5 if r>=17 else r-14 if r>=14 else -1 if r==13 else -8

def endpoint(r,R):
    B=R+1
    for H in range(4,2*r,2):
        for L in range(18,r+1):
            bs=[min((i-4)//2,H//2,(T(i)+i-r-7-B)//6) for i in range(L,r+1)]
            if min(bs)<2 or B>T(L-1)-r-1 or B>L-6+sum(b-1 for b in bs):continue
            need(all(2*b+4<=i and B<=T(i)+i-6*b-r-7 for i,b in zip(range(L,r+1),bs)),'Endpoint schedule')
            return dict(r=r,R=R,B=B,H=H,L=L,thresholds=bs)
    raise ValueError('No endpoint witness')

def profiles():
    path=ROOT/'verification/upper83_complete/check_structure.py'
    spec=importlib.util.spec_from_file_location('retained83_structure',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.profiles()

def verify():
    pf,pstats=profiles();inverse=[]
    need(96*67+1073-67**2==3016 and 56**2>3016 and 54**2<=3016,'Opposite pair count')
    need(1+T(67)>24*83+77 and 1+T(66)>24*75+77,'Sign survival')
    need(26**2>632 and 25**2<=632,'Bootstrap a>=8')
    for a in range(11,34):
        b=66-a;I=(33-a)**2;O=624-I;rp,rq=nonap(a),nonap(b)
        need(1+T(a)+T(b)==1123+I and 22*75+97-1123-I==O,'Source constants')
        Kmax=O-rp-rq;U=T(a)+a-2;V=T(b)+b-2
        need(Kmax<V-2,'Larger inverse test')
        margin=(a-3)+rp+rq-(O-T(a)+2)
        if a==33:
            need(margin>0,'Automatic inverse at balance');continue
        need(margin<=0,'Failed-test inventory')
        witness=endpoint(b,O-T(a)+2-(a-3)-rp);H=witness['H'];alpha=2*H+2
        diam=[V-1-Kmax,V-Kmax-2*alpha-1,V-Kmax-alpha-2,U-H-2]
        need(min(diam)>0,'Short diameter applications')
        layer=-85-2*I+2*H+(16 if a<=14 else 0)
        need(layer<0,'Repaired pre-G intersection')
        cap=O-rp-rq-T(a)-a+1-140+3*H
        need(cap<150 and 4*H<158,'Nonprimitive low-c range')
        if cap>=75:
            need(19<=a<=25,'Exceptional nonprimitive low-c rows')
            width=T(b)+b-3-2*H;maximum=b+633+4*H-I
            need(width>maximum and H<=22,'Repair localization')
        inverse.append(dict(a=a,b=b,**{k:v for k,v in witness.items() if k!='r'},diameter=diam,layer=layer,nonprimitive_cap=cap))
    need(len(inverse)==22 and max(v['nonprimitive_cap'] for v in inverse)==99,'Inverse census')
    need(T(20)+T(21)>417 and 6*27-74>(17+22)/2-2,'Localized low-c forest')
    small=[]
    for a in range(11,15):
        b=66-a;I=(33-a)**2;O=624-I;rp,rq=nonap(a),nonap(b)
        witness=endpoint(b,O-rp-47);H=witness['H']
        width=T(b)+b-3-2*H;maximum=b+633-I+4*(O-rp-rq)
        need(width>maximum,'Small-boundary localization')
        gap=(b-1)-(395-I+H);need(gap>0,'Small-boundary positive mass')
        small.append(dict(a=a,b=b,**witness,width=width,source_max=maximum,mass_margin=gap))
    need(-8+53>-1,'a8 nonAP')
    need(4<T(9)-1 and 47+52-8>48,'a9 strict inverse')
    need(52<T(10)-1 and 140-2*43+51-8>95,'a10 forces z>=44')
    basepath=ROOT/'verification/upper83_complete/check_structure.py'
    spec=importlib.util.spec_from_file_location('small83_effective',basepath)
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    effective=old.effective(56,5,132)
    need(old.rho(56,effective['mu'])==125 and 47+125-8>95,'a10 universal hole witness')
    need(all(140>624-(33-a)**2+8 for a in (8,9,10)),'Small AP post-lattice contradiction')
    # Universal profile used before the source-lattice conclusion.
    overlap=[]
    for r in range(15,52):
        s=66-r;I=(r-33)**2;h=21 if I<6 else 49
        margin=T(r-2)+2-2*r+pf[h,s]['elementary_rho']+43+I-(624-I)
        need(margin>0,'Pre-G large-hole overlap');overlap.append(margin)
    need(min(overlap)==2,'Pre-G overlap minimum')
    ap=[];triples=[];large_ap=[]
    for a in range(11,34):
        b=66-a;I=(33-a)**2;O=624-I;rp=-8 if a<=12 else -2 if a==13 else 0
        need(O-rp-(b-5)<3*T(a),'At most three residues')
        one=T(a)+T(b-2)+2-2*b+rp-O
        need(one>0,'Unique offscale smaller AP')
        two=3*T(b-2)-T(b)+4-2*b
        need(two>O-rp,'Two offscale generators')
        if O-rp-(b-5)>=2*T(a):
            need(14<=a<=19,'Three-residue census')
            need(T(b)+b-3>O-rp,'Three-residue larger side primitive')
            witness=endpoint(b,O-2*T(a)-rp);H=witness['H']
            cap=O-2*T(a)-rp-(b-5)-140+3*H
            need(cap<0 and -85-2*I+2*H<0,'Three-residue terminal')
            triples.append(dict(a=a,cap=cap,**witness))
        if a<=31:need(O-nonap(a)<T(b) and O-rp<T(b),'Larger AP one residue')
        else:
            need(O-nonap(a)<2*T(b) and O-rp<2*T(a),'Balanced AP residues')
            need(T(b)+T(a-2)+2-2*a-O>0,'Unique offscale larger AP')
            need(2*(T(a)+a-3)>O,'Smaller side primitive in cyclic two')
            witness=endpoint(a,O-T(b));H=witness['H'];cap=O-T(b)-nonap(a)-140+3*H
            need(cap<0 and -85-2*I+2*H<0,'Larger AP two-residue terminal')
            large_ap.append(dict(a=a,cap=cap,**witness))
        mass=min(T(a)+1+(b-t)*(b-t+1)+21*t+t*(t-1)-21-T(b) for t in range(2,b+1))
        need(mass>O+2*b-2-rp,'Unbounded odd W>=21')
        halfcap=O-T(a)-140+54-(b-5)-rp
        nonprim=O-140-T(a)-rp
        need(halfcap<150 and nonprim<150,'AP low-c caps')
        need(-85-2*I+36+(16 if a<=14 else 0)<0,'Halfstep pre-G')
        if halfcap>=75:
            witness_half=endpoint(b,O-T(a)-rp);HH=witness_half['H']
            need(T(b)+b-3-2*HH>b+630-I,'Halfstep endpoint localization before low-c bridge')
            need(T(a)>HH and T(b)>HH,'Halfstep zero lies in central strip')
        ap.append(dict(a=a,odd_tail_margin=mass-(O+2*b-2-rp),halfstep_cap=halfcap,nonprimitive_cap=nonprim))
    need(len(triples)==6 and len(large_ap)==2,'New AP exceptional census')
    need(18<=22 and all(x['halfstep_cap']<150 for x in ap),'Halfstep localized low-c bridge domain')
    need(max(x['halfstep_cap'] for x in ap)==125,'Halfstep cap maximum')
    # Low holes: if a whole one-side core fits in H, the opposite side
    # has at least49 holes and already consumes too much mass.
    coremargin=min(T(r)+2*(r-3)+pf[49,66-r]['mu']+(r-33)**2 for r in range(15,52))
    need(coremargin==823>526,'Individual core interval guard')
    need(772+75-56>666-75+56,'Low-hole source propagation')
    need(56<158,'Unlocalized j0 low holes')
    bands=[]
    for h,hi,mu,rho0,Hcap in [(15,16,410,282,266),(17,20,452,324,240),(21,48,492,364,312)]:
        need(min(pf[h,r]['mu']+pf[h,66-r]['mu'] for r in range(15,52))==mu,'Paired high-hole mass')
        need(min(pf[h,r]['elementary_rho']+pf[h,66-r]['elementary_rho'] for r in range(15,52))==rho0,'Paired high-hole defect')
        cap=max(624-rho0-max(47,z,140-2*z) for z in range(h,hi+1))
        need(624-rho0-140+4*hi==Hcap,'High-hole H cap')
        need(min(T(r)+(r-33)**2 for r in range(15,52))==374 and 374>Hcap,'Individual high-hole source mass')
        width=-990+Q(3,2)*(mu+rho0)-3*hi
        need(width>=0,'High-hole interval joins or abuts')
        bands.append(dict(z=[h,hi],mu=mu,rho=rho0,I_plus_c_cap=cap,H_cap=Hcap,width_margin=width))
    need(min(pf[49,r]['mu']+pf[49,66-r]['mu'] for r in range(15,52))==524,'Tail mass')
    need(min(pf[49,r]['elementary_rho']+pf[49,66-r]['elementary_rho'] for r in range(15,52))==396,'Tail defect')
    need(min(T(r)+pf[49,r]['mu']+(r-33)**2-228 for r in range(15,52))==258>0,'Tail individual core')
    need(-990+Q(3,2)*(524+396)-3*228+6*75==156>0,'Tail j>=1 width')
    need(1190>2*228-5==451,'Tail j0 propagation')
    need(410>395 and 524>470 and 48<158,'All high-hole terminals')
    return dict(status='PASS_STRUCTURAL_ARITHMETIC_ONLY',global_upper_bound_certified=False,
                inverse_rows=inverse,small_boundaries=small,AP=ap,three_residue=triples,
                larger_AP_two_residue=large_ap,pre_G_overlap_minimum=min(overlap),
                low_hole_core_minimum=coremargin,high_hole_bands=bands,profile_replay=pstats)

if __name__=='__main__':print(json.dumps(verify(),indent=2,default=str))
