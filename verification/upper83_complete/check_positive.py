"""Exact finite positive-hole terminals; see the accompanying geometric proofs."""
from fractions import Fraction as Q
from itertools import product, combinations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('fullrank_positive83',ROOT/'verification/upper83_fullrank/check.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
need=c.need

def z5_data():

    # Literal affine endpoint identities, coordinates Ms Mt Xs Xt gs gt hs ht ds dt.
    names=('Ms','Mt','Xs','Xt','gs','gt','hs','ht','ds','dt')
    v=lambda **kw:tuple(Q(kw.get(k,0)) for k in names)
    Z={'P':v(ds=1,dt=-1,Ms=-2,Xs=-2,Mt=-1,Xt=-1,gs=-1,gt=-1,ht=-1),
       'C5t':v(dt=1,Mt=-2,Xt=-2,Ms=-1,Xs=-1,gs=-1,gt=-1,hs=-1),
       'C6t':v(dt=1,Mt=-2,Xt=-2,Ms=-1,Xs=-1,gs=-1,gt=-1),
       'C7t':v(dt=1,Mt=-2,Xt=-2,Ms=-1,Xs=-1,gt=-1),
       'Us':v(ds=1,Ms=-1,Xs=-1),'Ut':v(dt=1,Mt=-1,Xt=-1),
       'Vs':v(ds=1,Ms=-1,Xs=-1,gs=-1),'Vt':v(dt=1,Mt=-1,Xt=-1,gt=-1),
       'Hs':v(ds=1,hs=1,Ms=-1,Xs=-1),'Ht':v(dt=1,ht=1,Mt=-1,Xt=-1),
       'as':v(hs=1,Ms=-1,Xs=-1),'at':v(ht=1,Mt=-1,Xt=-1)}
    side={k:('s' if k.endswith('s') or k=='P' else 't') for k in Z}
    cards=[('A',['Vs','Vt'],{'P':1,'C5t':2,'as':2,'at':1}),
           ('B',['Vs','Ht'],{'P':1,'C5t':2,'as':2}),
           ('C',['Hs','Ut'],{'P':1,'C5t':2,'as':3}),
           ('D',['Hs','Ht'],{'P':1,'C5t':2}),
           ('E',['Hs','Ut'],{'P':1,'C5t':2,'at':1}),
           ('F',['Us','Ht'],{'P':1,'C5t':2,'at':2}),
           ('G',['Hs','Ht'],{'P':1,'C6t':2,'at':2}),
           ('H',['Hs','Ht'],{'P':1,'C6t':2,'as':1}),
           ('I',['Hs','Ut'],{'P':1,'C6t':2,'as':1,'at':1}),
           ('J',['Hs','Ht'],{'P':1,'C7t':2,'as':1,'at':2}),
           ('K',['Us','Ht'],{'P':1,'C6t':2,'at':2})]
    return Z,side,cards

def z3():
    w=6;out=[]
    for a,ns,nt in product((0,1),(0,1),range(4)):
        e=8+2*a;clip=72*a+70*(ns+nt)
        if e+clip>228+w:continue
        p,q=2-2*a-ns,2-nt;rad=c.radial(228+w-e,12,0,-2-ns,4-nt,0,1);best=None;count=0
        for r in range(1,67):
            I=(r-33)*(r-34)
            for A in range(I+e+clip,229+w):
                peel=c.peel_min(p,q,max(4,A-156-w),393-A+w,max(8,A-76-w))
                for tau in range(A-I-e-clip+1):
                    d=A-I-tau
                    val=c.T(r)+4*r+peel[0]+816+rad[tau][0]-1026-w+2*e-d+4*(2*a+ns+nt)+70*(ns+nt)
                    count+=1
                    if best is None or val<best[0]:best=(val,(r,A,tau,d,peel,rad[tau]))
        need(best and best[0]>0,'P3 A0 terminal')
        out.append(dict(flags=[a,ns,nt],minimum=best[0],witness=best[1],states=count))
    need([x['minimum'] for x in out]==[162,224,285,330,126,266,422,88,158,313,41,220],'P3 flags complete')
    need(Q(783,2)>max(212+18,288+18,234+52+12,234+128+12),'P3 A1 all four endpoint flags')
    return out

def z4():
    w=4;out=[]
    for name,beta,cs,ct,peels,const,dc,e,endpoints,poly,ms,mt,nc,extra in c.Z4:
        rad=c.radial(152+w,beta,0,cs,ct,ms,mt);best=None;count=0;patterns=0
        for flags in product((0,1),repeat=len(endpoints)):
            h=sum(flags)
            if e+72*h>152+w:continue
            patterns+=1
            ps=sum(v for f,(side,v) in zip(flags,endpoints) if f and side=='s')
            pt=sum(v for f,(side,v) in zip(flags,endpoints) if f and side=='t')
            ex=sum(f*v for f,v in zip(flags,extra))
            for A in range(e+72*h,153+w):
                peel=c.peel_min(peels[0]-ps,peels[1]-pt,max(4,A-80-w),317-A+w,max(8,A-w))
                for r in (range(1,67) if poly else [33]):
                    I=(r-33)*(r-34)
                    for tau in range(A-I-e-72*h+1):
                        d=A-I-tau
                        val=peel[0]+beta*68+rad[tau][0]+const-w-dc*d+4*(ps+pt)+nc*72*h+ex
                        if poly:val+=c.T(r)+4*r
                        count+=1
                        if best is None or val<best[0]:best=(val,(flags,r,A,tau,d,peel,rad[tau]))
        need(best and best[0]>0,'P4 '+name)
        out.append(dict(card=name,minimum=best[0],witness=best[1],states=count,patterns=patterns))
    need([x['minimum'] for x in out]==[290,65,237,151,164,283,103],'P4 complete masters')
    return out

def z5():
    Z,side,cards=z5_data();out=[]
    for name,upper,lower in cards:
        body=tuple(sum(Z[k][i] for k in upper)-sum(w*Z[k][i] for k,w in lower.items())-(2 if i<2 else 0) for i in range(10))
        p,q,ca,cb,cg,dg,ch,dh,ds,dt=body
        need(ds==dt==0,'P5 affine cancellation')
        beta=ca+cb+cg+dg;qw=0
        loss=max(ca,cb)/2+max(cg,dg)/2+max(lower.values())
        if name=='D':
            need((cg,dg,ch,dh)==(3,3,3,2),'actual triple coefficients')
            beta=ca+cb+6;qw=5;loss=max(ca,cb)/2+3+max(lower.values())
        else:need(ch>=0 and dh>=0,'discarded positive h')
        e=11 if name=='E' else 8;best=None;count=0
        for r in range(1,67):
            ro=67-r;I=(r-33)*(r-34)
            end=sum(w*(72-(r if side[k]=='s' else ro)) for k,w in lower.items())+sum(71-(ro if side[k]=='s' else r) for k in upper)
            for sig in range(12-I-e):
                for delta in range(e,12-I-sig):
                    A=I+67+sig+delta;peel=c.peel_min(p,q,max(4,A-6),243-A,A+74)
                    for xs in range(1,2+sig):
                        for xt in range(1,3+sig-xs):
                            F=68-xs-xt
                            val=p*r+q*ro-134+peel[0]+(p-2)*xs+(q-2)*xt+beta*F+qw*68-1116+end+(1-loss)*delta+e*loss
                            count+=1
                            if best is None or val<best[0]:best=(val,(r,sig,delta,xs,xt,peel))
        need(best and best[0]>0,'P5 A0 '+name)
        out.append(dict(card=name,minimum=best[0],witness=best[1],states=count))
    need([x['minimum'] for x in out]==[608,452,723,428,344,504,504,307,515,597,504],'P5 A0 full inventory')
    native=[]
    cards=[('opposite',10,4,0,(3,1),Q(-11,2),Q(13,2),851),('same',8,-2,2,(1,1),Q(-5,2),Q(7,2),1006),('four',10,-3,1,(0,3),-3,4,1022),('branch_B',9,-1,3,(1,2),-3,4,1011)]
    for name,beta,cs,ct,peels,dc,ec,const in cards:
        best=None;count=0;e=8
        for r in range(1,67):
            I=(r-33)*(r-34)
            for sig in range(12-I-e):
                for delta in range(e,12-I-sig):
                    A=I+67+sig+delta;peel=c.peel_min(*peels,max(4,A-6),243-A,A+74)
                    for xs in range(1,2+sig):
                        for xt in range(1,3+sig-xs):
                            val=c.T(r)+4*r+peel[0]+beta*(68-xs-xt)+cs*xs+ct*xt+dc*delta+ec*e-const-2
                            count+=1
                            if best is None or val<best[0]:best=(val,(r,sig,delta,xs,xt,peel))
        need(best and best[0]>0,'P5 native '+name)
        native.append(dict(card=name,minimum=best[0],witness=best[1],states=count))
    need([x['minimum'] for x in native]==[761,326,501,461],'P5 native inventory')
    return dict(A0=out,native=native)

def seed():
    count=0
    for values in combinations(range(1,18),12):
        bits=1;total=sum(values)
        for x in values:bits|=bits<<x
        need(all(bits>>x&1 for x in range(11,total-10)),'twelve-seed interval')
        need(sum(not (bits>>x&1) for x in range(1,11))<=5,'twelve-seed low holes')
        count+=1
    need(count==6188,'all twelve-seeds')
    need(6*67+42-2*sum(range(12,18))==270>242,'twelve values exist')
    need(2*c.T(17)-21>=276 and 78+34*58>1398,'all remaining core joins')
    return count

def elementary():
    need(4*61>82 and 4*(61+2*14)>82+6*14,'P2 no two caps')
    need(26>Q(3,2)*14 and 64>Q(3,2)*14,'P2 card1 and terminal')
    need(14+32-14>12,'P2 HIGH V terminal')
    need(249-234==15>12 and 301-234==67>15,'P3 activity')
    need(min((r-33)*(r-34)+4*r+105 for r in range(1,67))==235>234,'P3 cross HIGH including ten fixed HIGH')
    need(min((r-33)*(r-34)+3*r+90 for r in range(1,67))==188>156,'P4 chain1')
    need(min((r-33)*(r-34)+2*r+95 for r in range(1,67))==161>156,'P4 chain2 with ten HIGH')
    need(min(2*c.T(r)+9*r+4*(r-33)*(r-34) for r in range(1,67))==1160>1120,'P4 double beta')
    need(100>12 and 83>66 and 144>138 and 86+65>138,'P4 ownerless statuses')
    need(100>0 and 91>62 and 144>134,'Z4 other ownerless statuses')
    # Z4 light/light bootstrap covers every r/I,tau,xi in its domain.
    cases=0
    for r in range(1,67):
        I=(r-33)*(r-34)
        for tau in range(max(0,135-I)):
            for xi in range(94+I,tau+1):
                need(44+2*I+12*xi>8*tau,'Z4 one-trim terminal')
                need(152-I-tau-18<=40-2*I<66,'Q-hit and alpha trim guard')
                cases+=1
    need(-1052+6*6+8*142==120>0,'Z6 equality excluded')
    return dict(ownerless_states=cases,Z2_P2_final_margin=43,Z6_margin=120)

def verify():
    return dict(status='PASS',seed_count=seed(),elementary=elementary(),P3=z3(),P4=z4(),P5=z5())

if __name__=='__main__':
    import json
    print(json.dumps(verify(),indent=2,default=str))
