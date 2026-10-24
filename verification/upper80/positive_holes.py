"""Conditional low-hole mass profiles for the size-81 main domain.

Here W=w/2 is an integer in 1..7 and both primitive core hole counts are
at least z>=w. Thus tau=mu+kappa+z>=paired_mu(2W-1)+4W.
"""
from pathlib import Path
import gzip,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import profiles as p
ROOT=Path(__file__).resolve().parents[2]
FLOORS=(62,120,176,230,282,332,380)

def row(hi):
    p.need(type(hi) is int and 1<=hi<=7,'Positive-hole profile range')
    return {'ts':-1,'tt':-1,'hole_W':60-hi},-hi-2,'positive hole mass profile '+str(hi)

def side_rows(hi):
    p.need(type(hi) is int and 1<=hi<=7,'Positive side profile range')
    answer=[]
    for side,sign,minimum_rank in [('s',-1,15),('t',1,32)]:
        slope=2*minimum_rank-hi-4
        answer.append(({'t'+side:-2,'rank_k':2*sign,'hole_W':slope},slope-62,'positive side mass profile '+str(hi)))
    return answer

def first_gap_rows(rank_hi):
    p.need(type(rank_hi) is int and 0<=rank_hi<=17,'Positive first-gap rank range')
    weight=31-rank_hi;label='positive core gap rank '+str(rank_hi)
    return [({'ts':-1,'tt':-1},-64,label),
            ({'ts':-1-weight,'tt':-1,'rank_k':-weight},-64-32*weight,label),
            ({'ts':-1,'tt':-1-weight,'rank_k':weight},-64-32*weight,label)]

def side_interval_rows(lo,hi):
    p.need(type(lo) is int and type(hi) is int and 1<=lo<=hi<=7,'Positive side interval')
    answer=[]
    for side,sign,minimum_rank in [('s',-1,15),('t',1,32)]:
        slope=2*minimum_rank-hi-lo-3
        answer.append(({'t'+side:-2,'rank_k':2*lo*sign,'hole_W':slope},-64*lo+lo*(lo+3)-2+slope*lo,'positive side interval '+str(lo)+' '+str(hi)))
    return answer

def predecessor_rows(j):
    p.need(type(j) is int and 3<=j<=6 and 510-73*j<352,'Positive predecessor mass budget')
    return [({'ts':-1,'xs':1,'rank_k':-1},-30,'positive predecessor gap s'),
            ({'tt':-1,'xt':1,'rank_k':1},-30,'positive predecessor gap t')]

def retained_predecessor_rows(lo,hi):
    p.need(type(lo) is int and type(hi) is int and 1<=lo<=hi<=7,'Retained predecessor hole range')
    label='retained positive predecessor '+str(lo)+' '+str(hi)
    answer=[({'rank_k':1},10,label),({'ts':-1,'tt':-1,'xs':1,'xt':1,'hole_W':59-lo-hi},-lo*hi-2,label)]
    for side,sign,minimum_rank in [('s',-1,21),('t',1,31)]:
        slope=2*minimum_rank-hi-lo-3
        answer.append(({'t'+side:-2,'x'+side:2,'rank_k':2*lo*sign,'hole_W':slope},-62*lo+lo*(lo+3)-2+slope*lo,label))
    return answer

def verify():
    new=json.loads(gzip.decompress((ROOT/'data/upper80_h3_profiles.json.gz').read_bytes()))
    p.need([(v['h'],v['r']) for v in new]==[(3,r) for r in range(15,56)],'Complete h3 profiles')
    stats=[p.replay_claim(claim,allowed_hs=(3,)) for claim in new]
    old=json.loads(gzip.decompress((ROOT/'data/upper80_profiles.json.gz').read_bytes()))
    table={(v['h'],v['r']):v['mu'] for v in old+new};paired=[58]
    paired.extend(min(table[2*W-1,r]+table[2*W-1,64-r] for r in range(15,50)) for W in range(2,8))
    floors=tuple(mu+4*W for W,mu in enumerate(paired,1));p.need(floors==FLOORS,'Exact paired low-hole mass floors')
    checks=side_checks=gap_prefixes=retained_checks=0
    minima=[]
    for r in range(15,50):
        minima.append(p.tri(r-1)+2-r+(64-r-1)+(r-32)**2)
        n=r-1
        p.need(min((n-i)*(p.tri(i)+1-i) for i in range(n))==n-1,'Noninterval predecessor mass')
    p.need(min(minima)==352 and 510-73*3<352,'A complete predecessor cannot create core holes')
    primitive_min=min(p.tri(r-1)+(64-r-1)+(r-32)**2 for r in range(15,50))
    p.need(primitive_min==372 and 218-38<primitive_min,'Positive predecessor primitivity')
    p.need(10**2<=218-38-64<11**2,'Retained predecessor rank domain')
    from endpoint_schedule import endpoint
    schedules=[]
    for r in range(22,43):
        cap=180-(r-32)**2-(64-r-1);witness=endpoint(r-1,cap)
        margin=p.tri(r-1)-2*witness['H']+1-(r+cap)
        p.need(margin>=128,'Predecessor central interval hits every maximum residue')
        schedules.append(dict(rank=r,witness=witness,propagation_margin=margin))
    for k in range(18):
        a,b=32-k,32+k;all_costs=[];nonempty=[]
        for i in range(a+1):
            for j in range(b+1):
                if (i,j)==(a,b):continue
                S=p.tri(i)+p.tri(j);cost=(a-i)*(S+1-i)+(b-j)*(S+1-j)
                all_costs.append(cost)
                if i+j:nonempty.append(cost)
                gap_prefixes+=1
        p.need(min(all_costs)==64 and min(nonempty)==95-k,'Every first-gap prefix allocation')
        for rank_hi in range(k,18):p.need(14<=31-rank_hi<=31-k,'Weighted side gap license')
    for W in range(2,8):
        for r in range(15,50):p.need(table[2*W-1,r]==W*r-W*(W+7)//2+1,'Individual affine hole profile')
    for hi in range(1,8):
        body,rhs,_=row(hi)
        for W in range(1,hi+1):
            p.need(-FLOORS[W-1]+body['hole_W']*W<=rhs,'Every integer profile chord')
            p.need(FLOORS[W-1]-(60-hi)*W-hi-2==(W-1)*(hi-W),'Profile chord identity');checks+=1
        for k in range(18):
            for W in range(1,hi+1):
                for (side,r),(body,rhs,_) in zip([('s',32-k),('t',32+k)],side_rows(hi)):
                    actual=W*r-W*(W+3)//2+1
                    p.need(-2*actual+body['rank_k']*k+body['hole_W']*W<=rhs,'Individual profile chord');side_checks+=1
        for lo in range(1,hi+1):
            for k in range(11):
                for W in range(lo,hi+1):
                    a,b=31-k,31+k
                    values={'rank_k':k,'hole_W':W,'xs':0,'xt':0,
                            'ts':W*a-W*(W+3)//2+1,
                            'tt':W*b-W*(W+3)//2+1}
                    for body,rhs,_ in retained_predecessor_rows(lo,hi):
                        p.need(sum(c*values[name] for name,c in body.items())<=rhs,
                               'Retained predecessor profile chord')
                        retained_checks+=1
            for k in range(18):
                for W in range(lo,hi+1):
                    for r,(body,rhs,_) in zip([32-k,32+k],side_interval_rows(lo,hi)):
                        actual=W*r-W*(W+3)//2+1
                        p.need(-2*actual+body['rank_k']*k+body['hole_W']*W<=rhs,'Restricted individual profile chord');side_checks+=1
    return dict(status='PASS_CONDITIONAL_POSITIVE_HOLE_PROFILES',global_upper_bound_certified=False,
                structural_applicability_certified=False,new_h3_claims=len(new),new_branches=sum(s['branches'] for s in stats),
                paired_mu=paired,tau_floors=list(FLOORS),chord_checks=checks,individual_chord_checks=side_checks,retained_predecessor_chord_checks=retained_checks,first_gap_prefixes=gap_prefixes,complete_predecessor_mass_floor=352,nonprimitive_predecessor_mass_floor=372,retained_predecessor_schedules=schedules)

if __name__=='__main__':print(json.dumps(verify(),indent=2))
