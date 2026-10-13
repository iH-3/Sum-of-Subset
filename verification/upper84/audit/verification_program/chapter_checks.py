"""Standard-library exact arithmetic for the detailed P3 and Z5 appendices.
No symbolic package, solver, source configuration search or stored PASS field is used.
"""
import copy
import itertools
from fractions import Fraction
from exact_math import Poly, VerificationError, parse, equal, require, quadratic_integer_min
from checks import check_fixed_cover
from chapter_expected import EXPECTED_P3_A1_IDS, EXPECTED_Z5_LEDGER_IDS, EXPECTED_Z5_REDUCTION_IDS


def substitute(poly, replacements):
    """Simultaneous polynomial substitution, with no executable input strings."""
    output=Poly.constant(0)
    for monomial,coefficient in poly.terms.items():
        term=Poly.constant(coefficient)
        for name in monomial:
            term=term*replacements.get(name,Poly.variable(name))
        output=output+term
    return output


def resolve_substitutions(mapping):
    """Resolve a finite dependency graph, e.g. L depends on delta, delta on k."""
    raw={name:parse(value) for name,value in mapping.items()}
    resolved={}
    active=set()
    def one(name):
        if name in resolved: return resolved[name]
        require(name not in active,'Cyclic polynomial substitutions')
        active.add(name)
        dependencies={v for m in raw[name].terms for v in m if v in raw}
        result=substitute(raw[name],{v:one(v) for v in dependencies})
        active.remove(name)
        resolved[name]=result
        return result
    for name in raw: one(name)
    return resolved


def same(left,right,label):
    require(left.terms==right.terms,'Exact polynomial mismatch: '+label)


def const(expression):
    p=parse(str(expression))
    require(set(p.terms)<={()},'Expected an exact rational constant')
    return p.terms.get((),Fraction(0))


def positive_polynomial(poly,label):
    require(poly.terms.get((),0)>0,'Nonpositive terminal constant: '+label)
    require(all(c>=0 for c in poly.terms.values()),'Negative coefficient in positive terminal: '+label)
    return str(poly.terms[()])


def p3_algebra(data):
    require(len(data['identities'])==9,'P3 baseline identity omitted')
    for left,right in data['identities']: equal(left,right)
    a1=data['A1']
    rows=a1['exact_arithmetic_checks']
    require(tuple(row['id'] for row in rows)==EXPECTED_P3_A1_IDS,'P3 A1 arithmetic case omitted or changed')
    checked=[]
    for row in rows:
        if 'lhs' in row:
            same(parse(row['lhs']),parse(row['rhs']),row['id'])
        else:
            starting=row.get('base_residual',row.get('scalar_residual'))
            require(starting is not None,'Unknown P3 arithmetic record')
            result=substitute(parse(starting),resolve_substitutions(row['substitutions']))
            if 'discarded_nonnegative_loss' in row:
                loss=parse(row['discarded_nonnegative_loss'])
                require(all(c>=0 for c in loss.terms.values()),'Discarded loss has a negative coefficient')
                result=result+loss
            same(result,parse(row['result_residual']),row['id'])
        checked.append(row['id'])
    terminal=[]
    require(len(a1['strict_terminal_contradictions'])==8,'P3 A1 terminal omitted')
    for row in a1['strict_terminal_contradictions']:
        gap=const(row['left_lower'])-const(row['right_upper'])
        require(gap>0 and gap==const(row['verified_strict_gap']),'P3 A1 terminal margin changed')
        terminal.append({'case':row['case'],'margin':str(gap)})
    minimum,at=quadratic_integer_min(parse('T(r)+6*r+11*I(r)/2'))
    require(minimum==748 and at==[31],'P3 A1 m3 integer minimum mismatch')
    # The additional baseline/classifier comparisons are conditional on written deductions.
    require(len(data['classifier']['contradictions'])==5,'P3 classifier scalar row omitted')
    for row in data['classifier']['contradictions']:
        require(const(row['lhs_min'])>const(row['rhs_max']),'P3 classifier scalar comparison failed')
    require(len(data['A0']['terminal_rows'])==8,'P3 A0 terminal omitted')
    for row in data['A0']['terminal_rows']:
        require(const(row['lhs_min'])>const(row['rhs_max']),'P3 A0 comparison failed')
    return {'baseline_identities':9,'A1_exact_identities_and_substitutions':len(checked),
            'A1_case_ids':checked,'A1_strict_terminal_margins':terminal,'A1_m3_global_integer_minimum':'748',
            'A1_m3_minimizer':31,'A0_terminal_comparisons':8,'classifier_scalar_comparisons':5,
            'scope':'Conditional algebra; human proofs establish the inequality directions, actual resources and complete classifications.'}


def p3_seed_supports(data):
    results=[]
    for name in ('seed4','subseed4'):
        row=data['first_gap'][name]
        values=row['values']
        bits=1
        support={0}
        for value in values:
            bits |= bits<<value
            support |= {s+value for s in support}
        total=sum(values)
        require(total==row['total'],'P3 m4 seed mass mismatch')
        require(support=={i for i in range(total+1) if bits>>i&1},'P3 independent support algorithms disagree')
        holes=sorted(set(range(total+1))-support)
        require(holes==row['holes'],'P3 m4 seed holes mismatch')
        results.append({'seed':values,'mass':total,'holes':holes})
    # This is only the precise finite 13-of-17 seed statement, not Lev's full theorem.
    count=0
    least_mass=None
    for values in itertools.combinations(range(1,18),13):
        total=sum(values); bits=1
        for value in values: bits |= bits<<value
        mask=(1<<(total-17))-1
        require(((bits>>9)&mask)==mask,'A 13-of-17 seed misses its asserted central interval')
        least_mass=total if least_mass is None else min(least_mass,total)
        count+=1
    require(count==2380 and least_mass==91,'P3 finite seed domain/count mismatch')
    require(225>217 and 2866>1442 and 264<289-17,'P3 seed mass propagation scalar bounds fail')
    return {'m4_exact_seed_supports':results,'thirteen_of_seventeen_subsets':count,
            'minimum_seed_mass':91,'interval_checked':'[9,sum(seed)-9]',
            'scope':'Complete bounded seed support test only; does not prove the general Lev theorem or applicability/propagation for an arbitrary core.'}


def p3_mutations(data):
    broken=copy.deepcopy(data)
    row=next(r for r in broken['A1']['exact_arithmetic_checks'] if r['id']=='m3_mass_substitution')
    row['result_residual']='1+('+row['result_residual']+')'
    try: p3_algebra(broken)
    except VerificationError as e: reason=str(e)
    else: raise VerificationError('P3 changed m3 coefficient accepted')
    broken=copy.deepcopy(data)
    broken['A1']['exact_arithmetic_checks'].pop()
    try: p3_algebra(broken)
    except VerificationError as e: omitted=str(e)
    else: raise VerificationError('P3 omitted A1 step accepted')
    return {'mutations_rejected':2,'changed_m3_coefficient':reason,'missing_step':omitted}


def z5_expression(text):
    return substitute(parse(text),{'G':parse('gs+gt'),'k':parse('69-r')})


def z5_endpoint_cards(data):
    require(set(data['cards'])==set('ABCDEFGHIJK'),'Z5 endpoint card omitted')
    C={key:parse(value) for key,value in {
        'P':'ds-dt-2*a-b-gs-gt-ht','C5t':'dt-2*b-a-gs-gt-hs',
        'C6t':'dt-2*b-a-gs-gt','C7t':'dt-2*b-a-gt',
        'alphas':'hs-a','alphat':'ht-b','Us':'ds-a','Ut':'dt-b',
        'Vs':'ds-a-gs','Vt':'dt-b-gt','Hs':'ds+hs-a','Ht':'dt+ht-b'}.items()}
    side={key:('s' if key in ('P','alphas','Us','Vs','Hs') else 't') for key in C}
    for key,card in data['cards'].items():
        require(all(n>0 and type(n) is int for n in card['lower'].values()),'Invalid endpoint weight')
        require(sorted(side[x] for x in card['upper'])==['s','t'],'Endpoint card needs one upper endpoint on each physical side')
        body=sum((C[x] for x in card['upper']),Poly.constant(0))-sum((n*C[x] for x,n in card['lower'].items()),Poly.constant(0))
        same(body,z5_expression(card['body']),'Z5 body '+key)
        constant=Poly.constant(77)+sum((n*(parse('74-r') if side[x]=='s' else parse('5+r')) for x,n in card['lower'].items()),Poly.constant(0))
        same(constant,z5_expression(card['constant']),'Z5 endpoint constant '+key)
        if not card.get('normal',False):
            error=sum((parse('tt' if side[x]=='s' else 'ts') for x in card['upper']),Poly.constant(0))
            error+=sum((n*parse('ts' if side[x]=='s' else 'tt') for x,n in card['lower'].items()),Poly.constant(0))
            same(error,z5_expression(card['error']),'Z5 rank error '+key)
    templates=data['retained_pair1_templates']
    require(len(templates)==13 and len({tuple(sorted(t['extra_holes'])) for t in templates})==13,'Z5 retained template omitted/duplicated')
    require([t['row'] for t in templates]==list(range(1,14)),'Z5 template row inventory changed')
    for row in templates:
        card=data['cards'][row['card']]
        endpoints=set(card['upper'])|set(card['lower'])
        require(not endpoints.intersection(row['extra_holes']),'Z5 uses an empty endpoint resource')
    require({r['extra_hole'] for r in data['empty_pair1_templates']}=={'Hs','C5s','alphas'},'Z5 empty-pair templates changed')
    require(set(data['a1_empty_pair1_classifier'])=={'alphas','C5s','Us','Ht','alphat','C5t'},'Z5 A1 listed classifier changed')
    return {'endpoint_cards':11,'retained_pair1_endpoint_resource_checks':13,
            'empty_pair1_listed_cases':3,'A1_empty_pair1_listed_cases':6,
            'scope':'Checks literal endpoint arithmetic and retention within the stated templates; the human proof establishes template exhaustiveness, ownership and endpoint applicability.'}


def z5_fixed_ledgers(data,fixed_certificate):
    proven=check_fixed_cover(fixed_certificate)['groups']
    def canonical(s):
        label,side=s.split('_')
        return label[0]+('+' if side=='s' else '-')+label[1:]
    groups=[set(map(canonical,group)) for group in data['fixed_groups']]
    require(len(groups)==26 and {frozenset(g) for g in groups}=={frozenset(g['labels']) for g in proven},'Z5 baseline fixed groups differ from the checked cover certificate')
    require(tuple(row['id'] for row in data['fixed_ledgers'])==EXPECTED_Z5_LEDGER_IDS,'Z5 fixed-ledger case omitted')
    records=[]
    known={kind+sign+str(i)+str(j) for kind in ('C',) for sign in '+-' for i in range(1,9) for j in range(i,9)}
    known|={kind+sign+str(i) for kind in ('U','V') for sign in '+-' for i in range(2,9)}
    known|={'F'+sign+str(i) for sign in '+-' for i in range(1,6)}
    for row in data['fixed_ledgers']:
        high=set(map(canonical,row['HIGH'])); low=set(map(canonical,row['LOW']))
        require(len(high)==len(row['HIGH']) and len(low)==len(row['LOW']),'Duplicate fixed label in ledger')
        require(not high.intersection(low),'Z5 fixed label both HIGH and LOW')
        require(high|low<=known,'Unknown fixed label in Z5 ledger')
        require(not any(group<=high for group in groups),'Z5 ledger would spend a whole HIGH baseline group twice')
        touched=sum(bool(g&low) for g in groups)
        actual=dict(high=len(high),low=len(low),touched=touched,credit=len(high)+len(low)-touched)
        require(actual==row['counts'],'Z5 fixed-credit count mismatch: '+row['id'])
        records.append(dict(id=row['id'],**actual))
    return {'baseline_groups_matched_to_independent_certificate':26,'ledger_cases':len(records),'ledgers':records,
            'scope':'Exact labeled incidence/credit arithmetic; HIGH/LOW inequalities and applicability remain human proofs.'}


def z5_algebra(data):
    require(len(data['polynomials'])==6,'Z5 polynomial case omitted')
    polynomials=[]
    for row in data['polynomials']:
        lhs=z5_expression(row['lhs'])
        if 'rhs' in row:
            same(lhs,z5_expression(row['rhs']),'Z5 factorization '+row['id'])
            global_min,at=quadratic_integer_min(lhs)
            physical_min=min(lhs.evaluate({'r':r}) for r in range(28,42))
            require(global_min==physical_min==const(row['integer_min']),'Z5 exact integer minimum mismatch')
            bound=row.get('upper_bound',row.get('strict_upper_bound'))
            require(global_min>const(bound),'Z5 polynomial does not contradict supplied upper bound')
            polynomials.append({'id':row['id'],'integer_minimum':str(global_min),'minimizers':at,'margin':str(global_min-const(bound))})
        else:
            c,b,a=lhs.univariate()
            require(a>0,'Z5 polynomial is not convex')
            minimum=c-b*b/(4*a)
            require(minimum==const(row['real_min']) and minimum>0,'Z5 real quadratic minimum mismatch')
            polynomials.append({'id':row['id'],'exact_global_real_minimum':str(minimum)})
    require(len(data['linear_eliminations'])==3,'Z5 elimination omitted')
    for row in data['linear_eliminations']:
        multipliers=[const(x) for x in row['multipliers']]
        require(all(x>=0 for x in multipliers),'Negative elimination multiplier')
        result=multipliers[0]*z5_expression(row['row1'])+multipliers[1]*z5_expression(row['row2'])
        same(result,z5_expression(row['result']),'Z5 linear elimination '+row['id'])
        positive_polynomial(result,'Z5 elimination '+row['id'])
    require(tuple(row['id'] for row in data['affine_reductions'])==EXPECTED_Z5_REDUCTION_IDS,'Z5 affine reduction omitted')
    for row in data['affine_reductions']:
        replacements={k:z5_expression(v) for k,v in row['substitutions'].items()}
        original=z5_expression(row['row'])
        require(set(row['substitution_directions'])==set(replacements),'Missing substitution direction')
        for variable,direction in row['substitution_directions'].items():
            coefficient=original.terms.get((variable,),0)
            require(all(variable not in monomial or monomial==(variable,) for monomial in original.terms),'Expected affine substitution variable')
            require(direction in ('upper','lower','equality'),'Unknown substitution direction')
            if direction=='upper': require(coefficient<=0,'Upper bound used with wrong residual coefficient sign')
            if direction=='lower': require(coefficient>=0,'Lower bound used with wrong residual coefficient sign')
        result=substitute(z5_expression(row['row']),replacements)*const(row['scale'])
        same(result,z5_expression(row['result']),'Z5 affine reduction '+row['id'])
        require(const(row['scale'])>0,'Z5 affine scale must be positive')
    guards=data.get('arithmetic_guards',[])
    require([r['id'] for r in guards]==['C5_zero_loss_constant'],'Mandatory corrected C5 constant guard omitted')
    for guard in guards:
        constructed=const(guard['lhs'])
        require(constructed==const(guard['rhs']),'Corrected C5 source constant arithmetic fails')
        row=next(r for r in data['affine_reductions'] if r['id']==guard['affine_id'])
        require(z5_expression(row['row']).terms.get((),0)==constructed,'C5 affine row does not use its independently constructed constant')
    minima={}
    for key,card in data['cards'].items():
        if key=='K': continue
        minima[key]=positive_polynomial(z5_expression(card['terminal']),'Z5 card '+key)
    require(len(data['terminal_margin_checks'])==4,'Z5 terminal margin case omitted')
    for row in data['terminal_margin_checks']:
        require(const(row['lower_lhs'])>const(row['rhs']),'Z5 constant margin is not strict')
    return {'polynomials':polynomials,'nonnegative_linear_eliminations':3,
            'exact_affine_substitutions':len(data['affine_reductions']),'bound_substitution_coefficient_directions_checked':19,'positive_card_minima':minima,
            'strict_terminal_comparisons':4,'mandatory_corrected_C5_guard':'999 -> 7; coupled to independent constant construction',
            'scope':'Algebraic identities and positivity only; analytical rows, substitution directions and actual-set hypotheses are supplied by the report.'}


def z5_mutations(data,fixed_certificate):
    results=[]
    for name,mutate,checker in [
        ('endpoint coefficient',lambda d:d['cards']['A'].__setitem__('body','1+('+d['cards']['A']['body']+')'),lambda d:z5_endpoint_cards(d)),
        ('missing fixed-ledger case',lambda d:d['fixed_ledgers'].pop(),lambda d:z5_fixed_ledgers(d,fixed_certificate)),
        ('wrong fixed credit',lambda d:d['fixed_ledgers'][0]['counts'].__setitem__('credit',999),lambda d:z5_fixed_ledgers(d,fixed_certificate)),
        ('wrong affine result',lambda d:d['affine_reductions'][0].__setitem__('result','1+('+d['affine_reductions'][0]['result']+')'),lambda d:z5_algebra(d))]:
        broken=copy.deepcopy(data); mutate(broken)
        try: checker(broken)
        except VerificationError as error: results.append({'mutation':name,'rejected':str(error)})
        else: raise VerificationError('Z5 mutation accepted: '+name)
    broken=copy.deepcopy(data)
    row=next(r for r in broken['affine_reductions'] if r['id']=='C5_zero_loss')
    row['row']=row['row'].replace('999','1039')
    row['result']=row['result'].replace('7+','47+',1)
    try: z5_algebra(broken)
    except VerificationError as error: results.append({'mutation':'coupled obsolete C5 constants 1039/47','rejected':str(error)})
    else: raise VerificationError('Obsolete C5 1039/47 constants accepted')
    return {'mutations_rejected':len(results),'controls':results}
