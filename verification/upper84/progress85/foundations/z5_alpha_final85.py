#!/usr/bin/env python3
"""Independent exact ledger and scalar replay of final Z5 A0 alpha-hole card."""
import json
from pathlib import Path


def key(label, sign):
    return label+"_"+sign


def main():
    groups=[{"C25_s","C25_t"},{"C58_s","C58_t"},
            {"U6_s","U6_t"},{"V6_s","V6_t"}]
    rows=[("C48", "F3"), ("C77", "F4"),
          ("C15", "F1", "@C55"), ("C26", "@C57", "@V4"),
          ("C35", "V3", "@C46"), ("C36", "U4", "@U5"),
          ("C44", "U8", "F5"), ("C45", "V8", "@C67"),
          ("C47", "V7", "F2"), ("C56", "V2", "@C66"),
          ("C68", "U3", "@V5")]
    for row in rows:
        for sign,opp in (("s","t"),("t","s")):
            groups.append({key(x.lstrip("@"),opp if x.startswith("@") else sign) for x in row})
    assert len(groups)==26
    assert sum(map(len,groups))==len(set().union(*groups))

    def both(labels):return {key(l,v) for l in labels for v in ("s","t")}
    H=both(("C11","C12","C13","C14"))
    L=both(("C55","C56","C57","C58","V5","V6","V7","V8","F3","F4","F5"))
    L|={key(l,"s") for l in ("U5","U6","U7","U8","V2","V3","V4")}
    records=[]
    def stage(name,expected):
        assert H.isdisjoint(L)
        assert not H.intersection(set().union(*groups))
        g=sum(bool(L&grp) for grp in groups)
        actual=(len(H),len(L),g,len(H)+len(L)-g)
        assert actual==expected,(name,actual,expected)
        records.append({"name":name,"H":actual[0],"L":actual[1],"groups":g,"credit":actual[3]})
    stage("initial",(8,29,23,14))
    H|=both(("C22","C23","C24","C16","C17","C18"))|{"C33_s"}
    stage("tail",(21,29,23,27))
    L|={key(l,"t") for l in ("U5","U6","U7","U8","V3","V4","C66","C67","C68")}
    stage("B_D_below_a",(21,38,25,34))
    L|={key(l,"s") for l in ("C66","C67","C68","C35")}
    stage("C_below_b",(21,42,25,38))
    L|={"C25_s","C25_t"}
    stage("two_C25",(21,44,26,39))
    L|={"C35_t","C45_s","C45_t"}
    stage("three_remaining_LOW",(21,47,26,42))

    # Independent exact new-label identities on representative arbitrary
    # positive outer coordinates. Both sides are linear in these coordinates;
    # checking the eight unit vectors proves the coefficient identities.
    def identities(vals):
        a,b,gs,gt,hs,ht,ds,dt=vals
        sv=(a+gs+hs+ds,a+gs+hs,a+gs,a)
        tv=(b+gt+ht+dt,b+gt+ht,b+gt,b)
        las=sv[0]-sum(sv[1:]);lat=tv[0]-sum(tv[1:])
        C=las-tv[1];D=lat-sv[1]
        C25s=las+sv[1]-tv[0];C25t=lat+tv[1]-sv[0]
        C35s=las+sv[2]-tv[0];C35t=lat+tv[2]-sv[0]
        C45s=las+sv[3]-tv[0];C45t=lat+tv[3]-sv[0]
        assert C25s==C-D-2*b-gt
        assert C25t==D-C-2*a-gs
        assert C35t==C25t-ht
        assert C45s==C35s-gs
        assert C45t==C35t-gt
    for i in range(8):identities(tuple(int(i==j) for j in range(8)))

    best=10**9;witnesses=[];count=0;max_trim=0;min_q=69
    for tau in range(19):
        for ts in range(tau+1):
            tt=tau-ts
            for xs in range(ts+1):
                for xt in range(tt+1):
                    E_s,E_t=ts-xs,tt-xt
                    choices_s=[(xs,0)]+[(j+E_s//j,j) for j in range(1,5)]
                    choices_t=[(xt,0)]+[(j+E_t//j,j) for j in range(1,5)]
                    ps,js=min(choices_s);pt,jt=min(choices_t)
                    q=69-js-jt;F=69-ps-pt
                    assert q>=61
                    residual=4*tau-2*xs+11*F-719
                    count+=1;max_trim=max(max_trim,js+jt);min_q=min(min_q,q)
                    witness={"tau":tau,"tau_s":ts,"tau_t":tt,"xi_s":xs,"xi_t":xt,
                             "trim_s":js,"trim_t":jt,"q":q,"F":F,"residual":residual}
                    if residual<best:best,witnesses=residual,[witness]
                    elif residual==best:witnesses.append(witness)
    assert count==7315
    assert best==6
    assert 2*61==122
    assert 1085+68-2*72+2*21-4*73+68==827
    assert 827+2*68-122-32==809
    assert 809+120-5*42==719
    out={"status":"PASS","ledger_stages":records,"final_HIGH":sorted(H),"final_LOW":sorted(L),
         "finite_domain_tuples":count,"minimum_residual":best,"minimizers":witnesses,
         "maximum_actual_total_trims":max_trim,"minimum_chosen_support_size":min_q,
         "final_scalar":"4I+4tau-2xi_s+11F-719<=0 is required, but minimum is 6"}
    path=Path(__file__).with_name("z5_alpha_final85_results.json")
    path.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:out[k] for k in ("status","finite_domain_tuples","minimum_residual",
             "maximum_actual_total_trims","minimum_chosen_support_size")},indent=2))


if __name__=="__main__":main()
