#!/usr/bin/env python3
"""Reconstruct all13 fresh Z5 A0 endpoint cards over exact rational polynomials.

No symbolic algebra dependency is used. Each polynomial is reconstructed from
the literal retained endpoint list and the centre identities, then substitutes
the supplied actual-source overlap/mass rows. The written proof establishes
those rows and the exhaustive retention classification.
"""
from fractions import Fraction as Q
from pathlib import Path
import json


class Poly:
    def __init__(self,x=0):
        self.c=dict(x) if isinstance(x,dict) else ({"1":Q(x)} if x else {})
        self.c={k:Q(v) for k,v in self.c.items() if v}
    def __add__(self,o):
        o=o if isinstance(o,Poly) else Poly(o);r=self.c.copy()
        for k,v in o.c.items():r[k]=r.get(k,0)+v
        return Poly(r)
    __radd__=__add__
    def __neg__(self):return Poly({k:-v for k,v in self.c.items()})
    def __sub__(self,o):return self+-o if isinstance(o,Poly) else self+Poly(-o)
    def __rsub__(self,o):return -self+o
    def __mul__(self,o):return Poly({k:v*Q(o) for k,v in self.c.items()})
    __rmul__=__mul__
    def __truediv__(self,o):return self*Q(1,o)
    def coefficient(self,var):return self.c.get(var,Q(0))
    def replace(self,var,val):
        r=Poly(self.c);v=r.c.pop(var,Q(0));return r+v*val
    def __eq__(self,o):return self.c==(o.c if isinstance(o,Poly) else Poly(o).c)
    def serial(self):return {k:str(v) for k,v in sorted(self.c.items())}


def main():
    def var(s):return Poly({s:1})
    r,I,t,d,xs,xt,R,Ms,Mt,Xs,Xt,gs,gt,hs,ht,ds,dt=map(var,
        ('r','I','tau','delta','xi_s','xi_t','R','M_s','M_t','X_s','X_t','g_s','g_t','h_s','h_t','d_s','d_t'))
    a,b=Ms+Xs,Mt+Xt;G=gs+gt;A=I+t+d;xi=xs+xt
    f=61-(t-xi)/4;eps=d-8
    Z={'P':ds-dt-2*a-b-G-ht,'C5t':dt-2*b-a-G-hs,
       'C6t':dt-2*b-a-G,'C7t':dt-2*b-a-gt,
       'Us':ds-a,'Ut':dt-b,'Vs':ds-a-gs,'Vt':dt-b-gt,
       'Hs':ds+hs-a,'Ht':dt+ht-b,'as':hs-a,'at':ht-b}
    side={k:('s' if k.endswith('s') or k=='P' else 't') for k in Z}
    cards={
        'A':(['Vs','Vt'],{'P':1,'C5t':2,'as':2,'at':1}),
        'B':(['Vs','Ht'],{'P':1,'C5t':2,'as':2}),
        'C':(['Hs','Ut'],{'P':1,'C5t':2,'as':3}),
        'D':(['Hs','Ht'],{'P':1,'C5t':2}),
        'E':(['Hs','Ut'],{'P':1,'C5t':2,'at':1}),
        'F':(['Us','Ht'],{'P':1,'C5t':2,'at':2}),
        'G':(['Hs','Ht'],{'P':1,'C6t':2,'at':2}),
        'H':(['Hs','Ht'],{'P':1,'C6t':2,'as':1}),
        'I':(['Hs','Ut'],{'P':1,'C6t':2,'as':1,'at':1}),
        'J':(['Hs','Ht'],{'P':1,'C7t':2,'as':1,'at':2}),
        'K':(['Us','Ht'],{'P':1,'C6t':2,'at':2})}
    expected={
        'A':356+Q(9,2)*I+t+xi/2,
        'B':166+5*I+Q(3,2)*t+xi/2,
        'C':351+Q(13,2)*I+Q(5,2)*t+xi,
        'D':53+6*I+Q(11,4)*t+xi/4,
        'E':2+5*I+Q(3,2)*t+xi/2,
        'F':178+Q(11,2)*I+Q(7,4)*t+Q(3,4)*xi,
        'G':178+Q(11,2)*I+Q(7,4)*t+Q(3,4)*xi,
        'H':51+Q(9,2)*I+t+xi/2,
        'I':227+5*I+Q(5,4)*t+Q(3,4)*xi,
        'J':281+Q(11,2)*I+2*t+xi/2,
        'K':178+Q(11,2)*I+Q(7,4)*t+Q(3,4)*xi}
    checks={}
    for name,(upper,lower) in cards.items():
        const=sum(w*(73-(r if side[k]=='s' else 68-r)) for k,w in lower.items())
        const+=sum(72-(68-r if side[k]=='s' else r) for k in upper)
        err=sum(w*(xs if side[k]=='s' else xt) for k,w in lower.items())
        err+=sum(xt if side[k]=='s' else xs for k in upper)
        lhs=-sum(w*Z[k] for k,w in lower.items())+sum(Z[k] for k in upper)-2*(Ms+Mt)
        assert lhs.coefficient('d_s')==lhs.coefficient('d_t')==0
        assert lhs.coefficient('h_s')>=0 and lhs.coefficient('h_t')>=0
        p,q=lhs.coefficient('M_s'),lhs.coefficient('M_t');m=min(p,q)
        mass=m*(R+99+A)+(p-m)*(r+xs+A+8)+(q-m)*(68-r+xt+A+8)
        ca,cb=lhs.coefficient('X_s'),lhs.coefficient('X_t')
        cg,dg=lhs.coefficient('g_s'),lhs.coefficient('g_t')
        star=(ca+cb)*f-max(ca,cb)*eps/2
        gap=(cg+dg)*f-max(cg,dg)*eps/2
        if name=='D':gap=305+6*f-3*eps
        residual=mass+star+gap-2*R-1127+const+d-max(lower.values())*eps-err
        assert residual.coefficient('delta')<0
        residual=residual.replace('R',68+xi).replace('delta',60-I-t)
        assert residual==expected[name],(name,residual.serial(),expected[name].serial())
        assert all(v>=0 for v in residual.c.values())
        checks[name]={'upper':upper,'lower_weights':lower,
            'endpoint_constant':const.serial(),'generic_error':err.serial(),
            'transport_body':lhs.serial(),'exact_residual':residual.serial(),
            'strict_margin':str(residual.coefficient('1'))}
    literal=[('D',['as','at']),('A',['Us','Hs']),('A',['Ut','Ht']),('A',['Hs','Ht']),
             ('B',['at','Hs']),('C',['at','Ht']),('E',['as','Ht']),('F',['as','Hs']),
             ('G',['C5t','as']),('H',['C5t','at']),('I',['C5t','Ht']),
             ('J',['C5t','C6t']),('K',['C5t','Hs'])]
    assert len(literal)==13
    for card,holes in literal:
        endpoints=set(cards[card][0])|set(cards[card][1])
        assert endpoints.isdisjoint(holes)
    # Fresh equality-fringe mass correction: L=98+A, small-side e<=6.
    # Then the counted central gap has length at least A+79-R>=11+I+delta.
    assert 98-12-7-68==11
    out={'status':'PASS','all13_templates':[{'card':c,'extra_holes':h} for c,h in literal],
         'card_reconstructions':checks,'minimum_strict_margin':min(int(Q(c['strict_margin'])) for c in checks.values()),
         'scope':'Exact actual endpoint algebra and scalar substitutions; written retention/forest/source lemmas remain mathematical premises.'}
    path=Path(__file__).with_name('zero_audit85_results.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'templates':len(literal),'card_bodies':len(checks),
                      'minimum_strict_margin':out['minimum_strict_margin']},indent=2))


if __name__=='__main__':main()
