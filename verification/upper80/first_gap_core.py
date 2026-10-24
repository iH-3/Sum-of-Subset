"""Conditional core compression after the first missing subset sum 1,2,3.

For a positive rank-r core X, phi(X)=min(r, min_i(x_i+r-2i)).
If its prescribed prefix has t points and every remaining point is at
least h+1, translate that remainder down by h. Then
phi(X)<=h-t+phi(Y), with excess mass tau(Y)=tau(X)-baseline(r,h,t).
"""
import model as m
import single_hole
ONE={'ONE':1}
CASES=((1,0,0),(2,1,0),(2,0,1),(3,1,1))

def rows(case):
    m.need(type(case) is int and 0<=case<len(CASES),'Complete first-gap core case')
    h,ps,pt=CASES[case];answer=[]
    for side,prefix,sign in [('s',ps,-1),('t',pt,1)]:
        # Baseline excess: h*r when t=0, (h-1)*(r-1) when t=1.
        weight=h-prefix;offset=0 if prefix==0 else -(h-1)
        baseline={'ONE':32*weight+offset,'rank_k':sign*weight}
        label='first missing core '+str(case)+' '+side
        answer.extend([(m.add((1,baseline),(-1,{'t'+side:1})),0,label+' mass'),
                       ({'x'+side:-1},-weight,label+' maximum lower'),
                       (m.add((1,baseline),(-1,{'t'+side:1}),(1,{'x'+side:1})),weight,label+' maximum upper')])
        for q in range(1,56):
            answer.append((m.add((q,{'phicore'+side:1}),(-1,{'t'+side:1}),(1,baseline)),q*weight+q*(q-1)//2,label+' shifted staircase '+str(q)))
            answer.append((m.add((q,{'phicore'+side:1}),(-1,{'t'+side:1}),(1,{'x'+side:1}),(1,baseline)),(q+1)*weight+q*(q+1)//2,label+' shifted maximum staircase '+str(q)))
    return answer

def guards(case):
    return [m.add((1,row),(-rhs,ONE)) for row,rhs,_ in rows(case)]

def check(step,record,prefix,rows_now,eqs,positive):
    import exact,cover_partition as cp
    m.need(positive,'First-gap core partition is positive-hole only')
    licenses=single_hole.guards(3)
    m.need(len(step['certificates'])==len(licenses),'First-gap location licenses')
    for guard,cert in zip(licenses,step['certificates']):exact.check(cert,rows_now,eqs,guard,strict=False)
    children=step['children'];m.need([c['case'] for c in children]==list(range(4)),'Every first-gap core alternative')
    for child in children:
        m.need(type(child['closed']) is bool,'First-gap child closure')
        expected=cp.branch_limits(record.get('limits'),guards(child['case']));cursor=child['record']
        while cursor!=prefix:
            m.need(isinstance(cursor,dict) and cursor.get('limits')==expected and 'premise' in cursor,'Exact first-gap conditional assumptions')
            cursor=cursor['premise']
        exact.replay(child['record'],require_closed=child['closed'])
    return all(c['closed'] for c in children)
