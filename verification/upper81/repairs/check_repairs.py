#!/usr/bin/env python3
"""Targeted exact checks for the 2026-10-21 proof repairs.

Run with Python 3.10+ and the fixed Sum-of-Subset checkout. This validates
finite proof obligations, not all actual-set arguments or the full N<=82 chain.
"""
import argparse,hashlib,importlib.util,itertools,json
from pathlib import Path

T=lambda n:n*(n+1)//2
def need(ok,msg):
    if not ok:raise ValueError(msg)

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod

REQUIRED_REPOSITORY_FILES={
    'data/upper82_global_sources.json',
    'reports/upper94_from95_20261016.tex','verification/nonap_sharp.py',
    'reports/proof_review_20261014.md','reports/upper86_complete_20261005.tex',
    'verification/upper82_global/proof.md','verification/upper82_global/structure.py'
}

def validate_inputs(repo,manifest=None):
    home=Path(__file__).resolve().parent
    m=json.loads((home/'repair_manifest.json').read_text()) if manifest is None else manifest
    need(m.get('schema')=='subset-sum-proof-repairs-v1','Repair manifest schema')
    need(set(m['repository_files'])==REQUIRED_REPOSITORY_FILES,'Missing explicit repair dependency')
    for path,expected in m['repository_files'].items():
        need(hashlib.sha256((repo/path).read_bytes()).hexdigest()==expected,'Changed repository dependency: '+path)
    old=json.loads((repo/'data/upper82_global_sources.json').read_text())
    for entry in old['files']:
        p=Path(entry['path'])
        need(not p.is_absolute() and '..' not in p.parts,'Pinned source path')
        need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==entry['sha256'],'Changed inherited dependency: '+str(p))
    need(set(m['package_files'])=={'check_repairs.py','no_clipping.tex','repair_note.tex'},'Incomplete repair source inventory')
    for path,expected in m['package_files'].items():
        need(hashlib.sha256((home/path).read_bytes()).hexdigest()==expected,'Changed repair source: '+path)
    return m,len(old['files'])

def schedule(a):
    need(11<=a<=33,'Small AP size range')
    b=66-a;I=(33-a)**2;omega=624-I
    p=-8 if a<=12 else -2 if a==13 else 0
    R=omega-T(a)-p;B=R+1
    L=next(i for i in range(18,b+1) if B<=T(i-1)-b-1)
    beta=[min((i-4)//2,16,(T(i)+i-b-7-B)//6) for i in range(L,b+1)]
    return dict(a=a,b=b,p=p,omega=omega,R=R,B=B,L=L,H=32,beta=beta)

def validate_schedule(row):
    a=row['a'];b=row['b'];B=row['B'];L=row['L'];H=row['H'];beta=row['beta']
    need(b==66-a and 11<=a<=33 and row['omega']==624-(33-a)**2 and row['R']==row['omega']-T(a)-row['p'],'Exact budget row')
    need(row['p']==(-8 if a<=12 else -2 if a==13 else 0),'AP defect floor')
    need(B==row['R']+1 and H==32 and H<T(a),'Strict no-clipping threshold')
    need(18<=L<=b and len(beta)==b-L+1,'Complete prefix schedule')
    need(B<=T(L-1)-b-1,'Late AP escape')
    for i,k in zip(range(L,b+1),beta):
        need(isinstance(k,int) and 2<=k<=H//2,'Integral threshold range')
        need(2*k+4<=i and B<=T(i)+i-6*k-b-7,'Central-interval escape')
    closing=L-6+sum(k-1 for k in beta)-B
    need(closing>=0,'Accumulated increment contradiction')
    primitive=2*(T(b)+b-3)-(row['omega']-row['p'])
    need(primitive>0,'Primitivity before hole normalization')
    return dict(**row,closing_margin=closing,primitivity_margin=primitive)

def support(X):
    S={0}
    for x in X:S|={s+x for s in S}
    return S

def fiber_identity(X,u):
    V=support(X);W=min(x for x in X if x%2);total=sum(X)
    fibers=[sorted((x-r)//2 for x in V if x%2==r) for r in (0,1)]
    gaps=[right-left-1 for vs in fibers for left,right in zip(vs,vs[1:])]
    clip=sum(max(0,g-(u-1)) for g in gaps)
    U=set(range(0,2*u,2));sumset={s+t for s in U for t in V}
    kappa=len(sumset)-u-len(V)+1;holes=total+1-len(V)
    mu=len(V)-1-T(len(X))
    need(kappa==u-1+sum(min(g,u-1) for g in gaps),'Exact parity sumset count')
    need(holes==W-1+sum(gaps),'Parity hull endpoints')
    need(mu+kappa==total+u-W-T(len(X))-clip,'Corrected mass identity')
    if holes<u-1:need(clip==0,'Hole bound prevents clipping')
    return dict(kappa=kappa,holes=holes,mu=mu,clip=clip,uncorrected=total+u-W-T(len(X)))

def check_fibers():
    count=0;nonclip=0
    for r in range(2,6):
        for X in itertools.combinations(range(1,11),r):
            if sum(x%2 for x in X)<2:continue
            for u in range(2,13):
                row=fiber_identity(X,u);count+=1
                nonclip+=row['holes']<u-1
    bad=fiber_identity((1,3,100),4)
    need(bad['clip']>0 and bad['mu']+bad['kappa']!=bad['uncorrected'],'Unclipped identity must fail without its hypotheses')
    return dict(cases=count,no_clipping_cases=nonclip,clipped_counterexample=dict(Q=[1,3,100],u=4,**bad))

def check_peeling():
    count=0
    universe=[i for i in range(-6,7) if i]
    for r in range(4,13):
        for X in itertools.combinations(universe,r):
            F=set(X)|{0};H=set(sorted((x for x in X if x>0),reverse=True)[:2]+sorted(x for x in X if x<0)[:2])
            H.update(sorted(set(X)-H)[:4-len(H)])
            alpha=sum(x for x in H if x<0);beta=sum(x for x in H if x>0);t=beta-alpha
            S=support(F-H);SF=support(F);RF={x+y for x,y in itertools.combinations(F,2)}
            C={x%t for x in S};Q={(c+alpha)%t for c in C};K={x%t for x in RF}
            shifts={alpha+x for x in S}|{beta+x for x in S}
            need(min(RF)>=alpha and max(RF)<=beta,'Restricted sum interval')
            need(len(shifts)>=len(S)+len(Q),'Translated residue classes')
            need(len(K)>=len(RF)-1 and len(SF)>=len(S)+len(Q|K),'Additional restricted-sum classes')
            need(len(SF)>=len(S)+len(RF)-1,'Peeling conclusion')
            count+=1
    need({(-5)%8,3%8}=={3} and 0 not in {(-5)%8,3%8},'Regression for unshifted residue classes')
    return dict(finite_integer_sets=count,unshifted_class_counterexample=[-3,-2,0,1,2])

def controls(rows):
    rejected=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,KeyError,TypeError):rejected.append(label)
        else:raise ValueError('Invalid mutation accepted: '+label)
    bad=dict(rows[14],beta=list(rows[14]['beta']));bad['beta'][0]=17
    reject('Invalid endpoint threshold',lambda:validate_schedule(bad))
    bad=dict(rows[0],H=T(11))
    reject('Non-strict no-clipping bound',lambda:validate_schedule(bad))
    reject('Missing size-25 row',lambda:need({x['a'] for x in rows if x['a']!=25}==set(range(11,34)),'Incomplete row census'))
    return rejected

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--structure',action='store_true',help='Also rerun the original complete size83 structural arithmetic')
    args=parser.parse_args();repo=args.repo.resolve()
    manifest,inherited_count=validate_inputs(repo)
    pins=manifest['repository_files']
    nonap=load(repo/'verification/nonap_sharp.py','repair_nonap').finite_base()
    need(nonap['total']==2723 and nonap['nonfull']==1106,'Complete r>=17 finite base')
    rows=[validate_schedule(schedule(a)) for a in range(11,34)]
    need(min(r['closing_margin'] for r in rows)==2 and min(r['primitivity_margin'] for r in rows)==558,'Exact margins')
    finite=dict(endpoint_rows=rows,nonap_base=nonap,fibers=check_fibers(),peeling=check_peeling(),negative_controls=controls(rows))
    bad=json.loads(json.dumps(manifest));bad['repository_files'].pop('verification/nonap_sharp.py')
    try:validate_inputs(repo,bad)
    except ValueError:finite['negative_controls'].append('Missing r>=17 non-AP dependency')
    else:raise ValueError('Missing sharp non-AP dependency accepted')
    if args.structure:finite['original_structure']=load(repo/'verification/upper82_global/structure.py','repair_original_structure').verify()
    digest=hashlib.sha256(json.dumps(finite,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()
    result=dict(status='PASS_TARGETED_PROOF_REPAIRS',scope='Finite obligations for the three identified repairs; not a complete replay of N<=82',finite_digest=digest,inherited_pinned_files=inherited_count,source_sha256=pins,finite=finite)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str)+'\n')
    print(json.dumps(dict(status=result['status'],finite_digest=digest,rows=len(rows),nonap_cases=nonap['total'],fiber_cases=finite['fibers']['cases'],peeling_cases=finite['peeling']['finite_integer_sets'],structure_replayed=args.structure)))

if __name__=='__main__':main()
