"""Bounded, exact mathematical checks for the consolidated upper-85 report."""
import copy
import itertools
from fractions import Fraction
from exact_math import Poly, VerificationError, parse, equal, require, quadratic_integer_min, verify_linear_certificate
from expected_cases import EXPECTED_TERMINALS, EXPECTED_POLYNOMIALS

STRATA = tuple('Z'+str(j) for j in range(6)) + tuple('P'+str(j) for j in range(6)) + ('H',)


def lower_construction():
    A = set(range(-31, 32)) | {s*n for n in (93,155,217,713) for s in (-1,1)}
    require(len(A) == 71 and A == {-a for a in A}, 'Construction cardinality/symmetry failed')
    # Subset sums via translation-aware bitset: adding a negative term moves the origin.
    bits, lo = 1, 0
    for a in sorted(A):
        if a >= 0:
            bits |= bits << a
        else:
            bits |= bits << (-a)
            lo += a
    subset_sums = {lo+i for i in range(bits.bit_length()) if bits >> i & 1}
    # Completely separate elementary set convolution for exactly four terms.
    pair_sums = {a+b for a in A for b in A}
    four_sums = {a+b for a in pair_sums for b in pair_sums}
    missing = sorted(subset_sums - four_sums)
    require(not missing, 'FS(A) has a value outside 4A: ' + str(missing[:8]))
    mass = sum(a for a in A if a > 0)
    require(mass == 1674 and lo == -1674, 'Construction mass mismatch')
    require(set(range(-mass,mass+1)) <= four_sums, '4A does not cover asserted interval')
    # Verify every printed interval in the constructive proof by exact set convolution.
    I = set(range(-31,32))
    base = {0}
    sums = [base]
    for _ in range(4):
        base = {a+b for a in base for b in I}
        sums.append(base)
    rows=[(4,[0],-124,124),(3,[217],124,310),(2,[310],248,372),
          (2,[372],310,434),(2,[434],372,496),(1,[527,589,651],496,682),
          (3,[713],620,806),(2,[806,868,930],744,992),
          (1,[1023,1085,1147],992,1178),(1,[1209,1271,1333],1178,1364),
          (2,[1426],1364,1488),(1,[1519,1581,1643],1488,1674)]
    for count, shifts, first, last in rows:
        values={a+b for a in sums[count] for b in shifts}
        require(values == set(range(first,last+1)), 'Printed interval row incorrect')
        require(values <= four_sums, 'Printed interval is not in fourfold sumset')
    return {'cardinality':len(A),'positive_mass':mass,'subset_sum_count':len(subset_sums),
            'fourfold_sumset_count':len(four_sums),'missing_values':0,'interval_rows':len(rows)}


def check_partition(data):
    rows = data['strata']
    require(len(rows)==13 and {r['id'] for r in rows}==set(STRATA), 'Missing or duplicate stratum row')
    expected=[]
    for group in ('Z','P'):
        for j in range(6):
            expected.append({'id':group+str(j),'z_min':0 if group=='Z' else 1,
                             'z_max':0 if group=='Z' else 14,'j':j})
    expected.append({'id':'H','z_min':15,'z_max':None,'j':None})
    require(sorted(rows,key=lambda x:x['id'])==sorted(expected,key=lambda x:x['id']), 'Stratum domain changed')
    counts={s:0 for s in STRATA}
    largest_j={'Z':0,'P':0,'H':0}
    def floor_rho(r):
        return r-5 if r>=21 else r-14
    # This finite superset is exhaustive under the stated original scalar inequalities:
    # 15<=r<=54, 0<=z<=587 from T>=z, and 78*j+T<=587-I.
    # No finite census of source configurations is made.
    for r in range(15,55):
        imbalance=(r-34)*(r-35)
        require(imbalance == r*(r+1)//2+(69-r)*(70-r)//2-1225, 'Imbalance identity')
        for z in range(588):
            group='Z' if z==0 else ('P' if z<=14 else 'H')
            rho=0 if group=='Z' else floor_rho(r)+floor_rho(69-r)
            budget=587-imbalance-rho-max(z,49,146-2*z)
            for j in range(19):
                if 78*j > budget:
                    continue
                matches=[row['id'] for row in rows if z>=row['z_min'] and
                         (row['z_max'] is None or z<=row['z_max']) and
                         (row['j'] is None or j==row['j'])]
                require(len(matches)==1, 'Partition gap/overlap at '+str((r,z,j,matches)))
                counts[matches[0]]+=1
                largest_j[group]=max(largest_j[group],j)
    require(all(counts[s]>0 for s in STRATA), 'An expected stratum has no scalar-domain points')
    require(largest_j['Z']<=5 and largest_j['P']<=5, 'Low-hole j cap failed')
    return {'scalar_points_checked':sum(counts.values()),'counts_by_stratum':counts,
            'largest_j_in_scalar_superset':largest_j,
            'not_a_source_configuration_census':True,'z_above_587_excluded_by':'T >= z and budget <= 587'}


def check_polynomial(record):
    expr=parse(record['expression'])
    equal(record['expression'],record['factorization'])
    require(expr.univariate()==[Fraction(s) for s in record['coefficients']], 'Wrong expanded polynomial coefficients: '+record['id'])
    minimum,at=quadratic_integer_min(expr)
    require(minimum==Fraction(record['global_integer_minimum']), 'Wrong integer minimum: '+record['id'])
    require(at==record['minimizers'], 'Wrong minimizer list: '+record['id'])
    low,high=record['physical_domain']
    values=[expr.evaluate({'r':r}) for r in range(low,high+1)]
    require(min(values)>=minimum, 'Physical domain below global minimum')
    return {'minimum':str(minimum),'global_integer_minimizers':at,'physical_domain':[low,high],
            'physical_domain_minimum':str(min(values))}


def minimize_separable(expression, bounds):
    """Exact integer minimum for a sum of one-variable convex quadratics/linear terms."""
    p=parse(expression)
    require(all(len(set(m))<=1 for m in p.terms), 'Mixed term in terminal expression')
    variables={x for monomial in p.terms for x in monomial}
    require(variables==set(bounds), 'Terminal parameter mismatch: '+str(variables.symmetric_difference(bounds)))
    value=p.terms.get((),Fraction(0))
    witnesses={}
    for name in sorted(variables):
        part=Poly({m:c for m,c in p.terms.items() if m and m[0]==name})
        coeffs=part.univariate(name)
        require(len(coeffs)<=3, 'Terminal degree above two')
        low,high=bounds[name]
        require(low is None or high is None or low<=high, 'Empty terminal domain')
        if len(coeffs)==3:
            require(coeffs[2]>0, 'Nonconvex terminal')
            vertex=-coeffs[1]/(2*coeffs[2])
            floor=vertex.numerator//vertex.denominator
            candidates={floor,floor+1}
            if low is not None: candidates.add(low)
            if high is not None: candidates.add(high)
            candidates=[x for x in candidates if (low is None or x>=low) and (high is None or x<=high)]
        else:
            slope=coeffs[1]
            selected=low if slope>0 else high
            require(selected is not None, 'Terminal unbounded below: '+name)
            candidates=[selected]
        best=min((part.evaluate({name:x}),x) for x in candidates)
        value+=best[0]
        witnesses[name]=best[1]
    return value,witnesses


def check_terminal(record):
    minimum,at=minimize_separable(record['expression'],record['parameters'])
    require(minimum==Fraction(record['expected_minimum']), 'Wrong terminal minimum for '+record['id']+': '+str(minimum)+' != '+record['expected_minimum'])
    require(minimum>0, 'Nonpositive terminal contradiction margin: '+record['id'])
    return {'minimum_positive_margin':str(minimum),'attained_in_relaxed_arithmetic_domain_at':at,
            'source':record['source'],'conditional_on_analytical_derivation':True}


def check_inventory(data):
    terminals=data['terminals']
    ids=[x['id'] for x in terminals]
    require(len(ids)==len(set(ids)) and set(ids)==set(EXPECTED_TERMINALS), 'Missing, duplicate or unexpected terminal case')
    pids=[x['id'] for x in data['polynomials']]
    require(len(pids)==len(set(pids)) and set(pids)==set(EXPECTED_POLYNOMIALS), 'Missing, duplicate or unexpected polynomial case')
    touched={s for x in terminals for s in x['strata']}
    require(touched==set(STRATA), 'Arithmetic coverage must include each of the 13 strata')
    return {'strata':13,'terminal_cases':len(ids),'polynomial_cases':len(pids),
            'does_not_certify_analytical_case_completeness':True}


def check_whole_units_and_forests():
    names=('O','H','own2','own3','C4','C5','C6','C7','alpha','beta')
    components={(side,name) for side in ('p','q') for name in names}
    for branch,paired in [('A','beta'),('B','C5')]:
        units=[{('p','C4'),('q','C4')},{('p',paired),('q',paired)}]
        units += [{x} for x in sorted(components) if x[1] not in ('C4',paired)]
        require(len(units)==18 and sum(map(len,units))==20, 'Whole-unit inventory mismatch')
        require(set.union(*units)==components and sum(map(len,units))==len(components), 'Whole-unit overlap or omission')
    # Exact truth-table check of the pointwise rooted-forest counting lemma.
    # Two target-tagged trees L-own3-own2 and L-C7; at most one designated root per tree.
    edges=((0,1),(1,2),(0,3),(4,5),(5,6),(4,7))
    cases=0
    for mask in range(1<<8):
        present=[bool(mask & (1<<i)) for i in range(8)]
        for roots in ((),(0,),(4,),(0,4)):
            for in_p,in_q in itertools.product((False,True),repeat=2):
                charge=sum(present[a] and present[b] for a,b in edges)
                deficit=0
                for vertices,inside in ((range(4),in_p),(range(4,8),in_q)):
                    n=sum(present[i] for i in vertices)
                    deficit+=n-(1 if inside and n else 0)
                charge+=sum(present[r] and not (in_p if r<4 else in_q) for r in roots)
                require(charge<=deficit,'Rooted forest pointwise charge invalid')
                cases+=1
    # One missing leaf can only contribute outside its target; no capacity is restored.
    missing_cases=0
    for leading,k,empty_present,inside in itertools.product((0,1),range(4),(0,1),(0,1)):
        if inside and empty_present: continue
        edge_count=leading*(k+empty_present)
        deficiency=leading+k-(1 if inside and (leading+k)>0 else 0)
        require(edge_count<=deficiency,'One-missing-leaf pointwise license failed')
        missing_cases+=1
    return {'ordinary_whole_units_each_branch':18,'component_labels_each_branch':20,
            'rooted_forest_membership_cases':cases,'single_missing_leaf_cases':missing_cases}


def mutation_tests(data):
    outcomes=[]
    def rejected(name,fn):
        try:
            fn()
        except VerificationError as err:
            outcomes.append({'mutation':name,'rejected':True,'reason':str(err)})
            return
        raise VerificationError('Mutation was not rejected: '+name)
    bad=copy.deepcopy(data['polynomials'][0])
    bad['coefficients'][0]=str(Fraction(bad['coefficients'][0])+1)
    rejected('wrong polynomial coefficient',lambda:check_polynomial(bad))
    badrows=copy.deepcopy(data)
    badrows['strata'].pop()
    rejected('missing H partition row',lambda:check_partition(badrows))
    badcases=copy.deepcopy(data)
    badcases['terminals'].pop()
    rejected('missing terminal arithmetic case',lambda:check_inventory(badcases))
    badcert=copy.deepcopy(data['linear_certificates'][0])
    badcert['multipliers'][1]='1'
    rejected('tampered rational certificate multiplier',lambda:verify_linear_certificate(badcert))
    badmargin=copy.deepcopy(data['terminals'][0])
    badmargin['expression']='0'
    badmargin['expected_minimum']='0'
    rejected('zero contradiction margin',lambda:check_terminal(badmargin))
    return {'mutations_rejected':len(outcomes),'tests':outcomes}


def check_shared_first_gap():
    """The common P1/H1 first-gap scalar argument; no support search."""
    left='m-1+(r-kp)*m+T(r-kp)+(69-r-kq)*m+T(69-r-kq)-1225'
    right='70*m-5/4-(m+35)*(kp+kq)+(kp+kq)**2/4+(r-69/2-(kp-kq)/2)**2'
    equal(left,right)
    p=parse(right+'-5*(69+2*m-kp-kq)')
    counts=0
    best=None
    at=[]
    for m in range(1,8):
        for kp,kq in itertools.product(range(4),repeat=2):
            if kp+kq>4 or kp*(kp+1)//2+kq*(kq+1)//2>m-1:
                continue
            # The actual low entries have total m-1. In particular m>1 needs an entry.
            if m>1 and kp+kq==0:
                continue
            for r in range(15,55):
                value=p.evaluate(dict(m=m,kp=kp,kq=kq,r=r))
                require(value>=-286,'First-gap baseline lower bound fails')
                counts+=1
                if best is None or value<best:
                    best,at=value,[(m,kp,kq,r)]
                elif value==best:
                    at.append((m,kp,kq,r))
    require(best==-286,'Unexpected first-gap relaxed minimum')
    q=lambda k:-k**3+69*k**2-4*k+275
    differences=[q(k+1)-q(k) for k in range(5,40)]
    require(all(d>0 for d in differences),'Cubic is not increasing over required range')
    require(min(q(k) for k in range(5,41))==1855,'Cubic minimum mismatch')
    require(Fraction(1547,4)>375 and Fraction(1855,4)>375,'Large-first-gap contradiction failed')
    return {'lemma_ids':['G-FIRSTGAP','P1','H1'],'baseline_scalar_cases':counts,
            'baseline_minimum':str(best),'baseline_minimizers':at,
            'cubic_domain':[5,40],'cubic_minimum':1855,'small_k_margin_over_375':'47/4',
            'large_k_margin_over_375':'355/4','not_a_source_configuration_search':True}


def check_fixed_cover(certificate):
    """Expand all 110 label formulas, then check 26 disjoint signed groups."""
    require(certificate.get('schema')=='fixed-cover-symbolic-certificate-v1','Unknown fixed-cover schema')
    order=['r1','r2','r3','r4','s1','s2','s3','s4']
    require(certificate['semantics']['coefficient_order']==order,'Fixed-cover coefficient order changed')
    labels={}
    for sign,prefix,opposite in (('+','r','s'),('-','s','r')):
        p=[sum((Poly.variable(prefix+str(k)) for k in range(i,5)),Poly.constant(0)) for i in range(1,5)]
        q=[sum((Poly.variable(opposite+str(k)) for k in range(i,5)),Poly.constant(0)) for i in range(1,5)]
        lam=p[0]-p[1]-p[2]-p[3]
        alpha=p[1]-p[2]-p[3]
        beta=2*p[1]-p[0]-p[2]-p[3]
        B=p+[-v for v in q]
        for i in range(8):
            for j in range(i,8):
                labels['C'+sign+str(i+1)+str(j+1)]=lam+B[i]+B[j]
        for i in range(1,8):
            labels['U'+sign+str(i+1)]=alpha+B[i]
            labels['V'+sign+str(i+1)]=beta+B[i]
        fs=[p[2]-p[3],2*p[2]-p[1]-p[3],p[1]+p[2]-p[0]-p[3],
            2*p[2]-p[0]-p[3],3*p[2]-p[0]-p[1]-p[3]]
        for i,value in enumerate(fs,1): labels['F'+sign+str(i)]=value
    require(len(labels)==110==certificate['expected_total_labels'],'Incorrect fixed-label inventory')
    templates=certificate['templates']
    require(len(templates)==15 and [x['number'] for x in templates]==list(range(1,16)),'Missing fixed-group template')
    used=set()
    groups=[]
    for template in templates:
        require(type(template['also_reflect']) is bool,'Bad reflection flag')
        for reflected in range(2 if template['also_reflect'] else 1):
            group=template['labels']
            vector=template['coefficient_vector']
            if reflected:
                group=[s.translate(str.maketrans('+-','-+')) for s in group]
                vector=vector[4:]+vector[:4]
            require(all(s in labels for s in group),'Unknown fixed label')
            require(len(group)==len(set(group)),'Repeated label inside fixed group')
            require(not used.intersection(group),'Fixed groups reuse a label')
            total=sum((labels[s] for s in group),Poly.constant(0))
            computed=[total.terms.get((name,),0) for name in order]
            require(total.terms==Poly({(name,):c for name,c in zip(order,computed)}).terms,'Nonlinear fixed label')
            require(computed==vector,'Fixed-group coefficient mismatch: '+template['letter'])
            require(all(c<=0 for c in computed) and any(c<0 for c in computed),'Group signed sum is not strictly negative on positive increments')
            used.update(group)
            groups.append({'template':template['letter'],'reflected':bool(reflected),'labels':group,'coefficients':list(map(str,computed))})
    require(len(groups)==26==certificate['expected_groups'],'Incorrect number of disjoint deletions')
    require(110-len(groups)==84==certificate['expected_fixed_allowance'],'Incorrect fixed allowance')
    return {'total_fixed_labels':110,'disjoint_negative_sum_groups':26,'labels_in_groups':len(used),
            'maximum_usable_fixed_labels':84,'one_zero_addition_gives':85,'groups':groups,
            'human_premise':'These exact labeled resources comprise the valid original cover; a target hit needs positive signed score.'}


def fixed_cover_mutation_tests(certificate):
    bad=copy.deepcopy(certificate)
    bad['templates'][0]['coefficient_vector'][0]+=1
    try:
        check_fixed_cover(bad)
    except VerificationError as error:
        first=str(error)
    else:
        raise VerificationError('Corrupted fixed-cover coefficient accepted')
    bad=copy.deepcopy(certificate)
    bad['templates'][1]['labels'][0]=bad['templates'][0]['labels'][0]
    try:
        check_fixed_cover(bad)
    except VerificationError as error:
        second=str(error)
    else:
        raise VerificationError('Reused fixed label accepted')
    return {'mutations_rejected':2,'coefficient_reason':first,'duplicate_resource_reason':second}


def check_p4_seeds(data):
    require(data.get('schema')=='p4-propagation-seeds-v1','Unknown P4 seed schema')
    expected=((3,4,5,6),(2,4,5,6),(2,3,5,6),(2,3,4,5),(2,3,4,6),(1,3,4,5),(1,1,4,5,6))
    require(tuple(tuple(row['seed']) for row in data['seeds'])==expected,'Missing or altered P4 seed case')
    results=[]
    for row in data['seeds']:
        seed=row['seed']
        total=sum(seed)
        bits=1
        support={0}
        for x in seed:
            bits |= bits<<x
            support |= {s+x for s in support}
        require(support=={i for i in range(total+1) if bits>>i&1},'P4 seed independent supports disagree')
        omitted=set(range(total+1))-support
        predicted=set(row['holes'])|{total-h for h in row['holes']}
        require(omitted==predicted,'P4 seed omitted values mismatch')
        h=max(row['holes'])
        require(total>2*h,'P4 seed boundary strips overlap')
        require(set(range(h+1,total-h))<=support,'P4 seed central interval missing')
        candidates=[]
        for x in range(1,30):
            if x in row['forbidden_core_values']: continue
            max_multiplicity=row['maximum_multiplicity_of_one'] if x==1 else 2
            candidates.extend([x]*max_multiplicity)
        L9=sum(candidates[:9])
        require(L9==row['L9'],'P4 nine-entry minimum mismatch')
        first=total+61*(total-2*h)+sum(i//2 for i in range(61))
        second=L9+37*(L9-2*h)+sum(i//2 for i in range(37))
        require(first==row['first_fail_bound'] and second==row['second_fail_bound'],'P4 propagation arithmetic changed')
        require(min(first,second)>1364,'P4 propagation does not contradict mass cap')
        results.append({'seed':seed,'mass':total,'missing_values':sorted(omitted),'L9':L9,
                        'first_failure_lower_mass':first,'second_failure_lower_mass':second})
    require(16*17//2+17*18//2==289 and 183<289-2*4-1,'P4 long-prefix propagation bound fails')
    return {'seed_cases':7,'exact_subset_supports':results,'long_prefix_mass_minimum':289,
            'long_prefix_increment_bound':183,'selection_and_propagation_lemma_are_human_proofs':True}


def check_endpoint_rank_ranges():
    equal('k*(75-k)-216','(k-3)*(72-k)')
    equal('k*(75-k)-146','(k-2)*(73-k)')
    rows=[]
    for name,expr,lo,hi,floor in [('Z3-A0','k*(75-k)',26,72,216),
                                 ('Z3-A1','k*(149-2*k)',26,73,219),
                                 ('Z4-light','k*(75-k)',29,73,146),
                                 ('P3-A1-light','k*(75-k)',27,73,131),
                                 ('P3-A0-light','k*(75-k)',2,73,146)]:
        polynomial=parse(expr)
        values=[polynomial.evaluate({'k':k}) for k in range(lo,hi+1)]
        require(min(values)>=floor,'Endpoint rank inequality fails: '+name)
        rows.append({'case':name,'domain':[lo,hi],'actual_minimum':str(min(values)),
                     'required_floor':floor,'margin':str(min(values)-floor)})
    return {'checks':rows,'rank_values_checked':sum(r['domain'][1]-r['domain'][0]+1 for r in rows),
            'scope':'The analytical endpoint argument supplies rank and mass premises; these are exact interval inequalities.'}
