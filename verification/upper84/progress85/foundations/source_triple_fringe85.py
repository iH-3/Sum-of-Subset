#!/usr/bin/env python3
"""Exact elementary checks for the fresh size-85 source envelope T<=165.

The universal quartet inequality 2B<=a+b+8-p is an already proved dependency.
All extra exceptional small cases needed by the new P+B-a-b<=5 lemma are
exhausted here; c>=2b and e>=2c are explicitly reduced in the written proof.
"""
import json
from pathlib import Path


def fringe(xs, cutoff):
    return len({x+y for i,x in enumerate(xs) for y in xs[i:] if x+y>cutoff})


def main():
    triple_rows=[]
    for u in range(3,8):
        for a in range(1,(u-1)//2+1):
            b=u-a
            ps={c:fringe((a,b,c),c) for c in range(b+1,2*b)}
            assert all(2*p<=u+4-u%2 for p in ps.values())
            assert 2*3<=u+4-u%2  # exact P=3 for every c>=2b
            triple_rows.append({"a":a,"b":b,"P_by_c":ps,"P_at_c_ge_2b":3})

    # The complete u<=8 proof: when c>=2b, P=3 and the existing
    # quartet lemma suffices. Below 2b, inspect all e<2c; above it B=4.
    count=0
    maxima={}
    for u in range(3,9):
        best=(-1,None)
        for a in range(1,(u-1)//2+1):
            b=u-a
            assert 3+(u+8-u%2)//2-u<=5
            for c in range(b+1,2*b):
                P=fringe((a,b,c),c)
                assert P+4-u<=5
                for e in range(c+1,2*c):
                    B=fringe((a,b,c,e),e)
                    assert 2*B<=u+8-u%2
                    assert P+B-u<=5
                    count+=1
                    if P+B-u>best[0]:best=(P+B-u,(a,b,c,e,P,B))
        maxima[u]={"maximum_finite_P_plus_B_minus_u":best[0],"witness":best[1]}

    exceptional=[]
    for a,b,c in ((1,3,4),(2,4,5)):
        vals={e:fringe((a,b,c,e),e) for e in range(c+1,2*c)}
        exceptional.append({"a":a,"b":b,"c":c,"B_by_e":vals,"B_at_e_ge_2c":4})
    assert exceptional[0]["B_by_e"]=={5:5,6:5,7:4}
    assert exceptional[1]["B_by_e"]=={6:6,7:6,8:5,9:5}

    # u>=9 follows algebraically from P<=6 and the existing B bound.
    # At u>=13, even the weaker B<=10 makes the difference <=3.
    for u in range(9,13):
        assert 6+(u+8-u%2)//2-u<=5
    assert 6+10-13<=5

    # Independent wider sample, used only as a sanity check.
    sample_count=0
    for a in range(1,13):
        for b in range(a+1,17):
            for c in range(b+1,2*b+3):
                P=fringe((a,b,c),c)
                for e in range(c+1,2*c+3):
                    B=fringe((a,b,c,e),e)
                    assert P+B-a-b<=5
                    sample_count+=1

    # Constants and the endpoint algebra.
    assert 2*75+3==153
    assert (308+2)//2==155
    assert 155+5+5==165
    assert 165+280==445
    assert (350-2*165+16)//2==18
    assert 76+1==77
    assert 2*78+4+8==168
    assert (18+168)//2==93
    assert 93-4==89
    assert 105-89==16
    for a in range(1,10):
        for b in range(a+1,12):
            for c in range(b+1,15):
                assert c+(a+b)%2>=4
    out={"status":"PASS","universal_T_cap":165,"source_A_constant":445,
         "quartet_bound_dependency":"2B<=a+b+8-((a+b)%2)",
         "finite_small_quartets_checked":count,"supplementary_quartets_checked":sample_count,
         "small_triple_rows":triple_rows,"small_quartet_maxima":maxima,
         "exceptional_tables":exceptional,"T165_Bsum_cap":18,
         "universal_one_maximum_offset_floor":"e_v>=max(4,T-89)",
         "Z5_offset_floor":"e_v>=A+16"}
    path=Path(__file__).with_name("source_triple_fringe85_results.json")
    path.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:out[k] for k in ("status","universal_T_cap","source_A_constant",
                    "finite_small_quartets_checked","supplementary_quartets_checked","T165_Bsum_cap")},indent=2))


if __name__=="__main__":main()
