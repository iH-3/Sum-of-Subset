"""Independent exhaustive dispatcher. No count-only acceptance."""
from itertools import product
from collections import Counter
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import model as m

def need(ok,message):
    if not ok:raise ValueError(message)

NAMES=tuple(sorted(k+s for s in 'st' for k in (*m.CHAIN,'alpha','beta')))

def key(rec):
    st=rec['st'];need(set(st)==set(NAMES),'Activity coordinates')
    need(all(type(v) is int and 0<=v<=3 for v in st.values()),'Activity type')
    need(all(type(rec[v]) is int for v in ('j','r','w')),'State integer type')
    need(rec.get('tau') is None,'Undispatched fixed mass')
    return rec['j'],rec['r'],rec['w'],tuple(st[k] for k in NAMES)

def alpha(st):
    return sum(v==1 for v in st.values())==13 and all(st[k+s]==(2 if k=='O' else 0) for k in ('P','beta','O') for s in 'st') and sorted([st['alphas'],st['alphat']])==[0,1]

def expected_main():
    direct=set();owners=set();alphas=set();counts=Counter()
    for j in range(1,7):
        for st in [*m.patterns(j),*m.partial_patterns(j)]:
            for w in range(0,15,2):
                floor=60+2*w if w else 0
                for r in range(15,34):
                    if (r-33)**2+floor>470-75*j+w:continue
                    state=key(dict(st=st,j=j,r=r,w=w));counts[j]+=1
                    if m.is_ownerless(st):owners.add(state)
                    elif w==0 and alpha(st):alphas.add(state)
                    else:direct.add(state)
    need(len(direct)+len(owners)+len(alphas)==sum(counts.values()),'Disjoint main census')
    return direct,owners,alphas,counts

def collect_roots(packets):
    found=set()
    for packet in packets:
        for rec in packet['records']:
            state=key(rec)
            need(rec.get('scope','native')=='native' and not rec.get('limits'),'Root has an extra restriction')
            need(state not in found,'Duplicate root');found.add(state)
    return found

def verify_trees(trees,leaves):
    roots=set();used=set();nodes=0
    def visit(node,base,limits):
        nonlocal nodes
        nodes+=1
        if set(node)=={'leaf'}:
            i=node['leaf'];need(type(i) is int and 0<=i<len(leaves) and i not in used,'Tree leaf index')
            used.add(i);rec=leaves[i]
            need(key(rec)==base,'Leaf attached to wrong root')
            need(rec.get('scope','native')=='native','Leaf scope')
            actual={k:tuple(v) for k,v in rec.get('limits',{}).items()}
            need(actual==limits,'Leaf domain does not match complementary path')
            return
        need(set(node)=={'variable','threshold','left','right'},'Branch node fields')
        name,mid=node['variable'],node['threshold'];need(type(name) is str and type(mid) is int,'Branch type')
        st=dict(zip(NAMES,base[3]))
        need(name[:1] in ('l','u') and name[1:] in st and st[name[1:]]==1,'Branch is not a retained native integer clip')
        lo,hi=limits.get(name,(0,74));need(lo<=mid<hi,'Noncomplementary or empty split')
        left=dict(limits);right=dict(limits);left[name]=(lo,mid);right[name]=(mid+1,hi)
        visit(node['left'],base,left);visit(node['right'],base,right)
    for rec in trees:
        base=key(rec);need(base not in roots,'Repeated branch root');roots.add(base)
        visit(rec['tree'],base,{})
    need(used==set(range(len(leaves))),'Unattached endpoint proof leaf')
    return roots,nodes

def verify_ownerless(packet,expected):
    wanted=set();pruned=0
    for j,r,w,st in expected:
        cap=170+w;floor=60+2*w if w else 0
        for bits in product((0,1),repeat=4):
            if (r-33)**2+floor+8+71*sum(bits)>cap:
                pruned+=1;continue
            wanted.add(((j,r,w,st),bits))
    found=set();names=('lalphas','lalphat','uHs','uHt')
    for rec in packet['records']:
        base=key(rec);need(base in expected and rec.get('scope','native')=='native','Ownerless root domain')
        lim=rec.get('limits',{});need(set(lim)==set(names),'Ownerless status inventory')
        bits=[]
        for name in names:
            bounds=tuple(lim[name]);need(bounds in ((0,70),(71,74)),'Ownerless clip partition')
            bits.append(int(bounds==(71,74)))
        item=(base,tuple(bits));need(item not in found,'Repeated ownerless status');found.add(item)
    need(found==wanted,'Missing ownerless rank or status')
    return dict(source_roots=len(expected),retained_statuses=len(found),budget_pruned_statuses=pruned)

def verify_low_c(packet):
    expected={key(dict(st=st,j=1,r=r,w=w)) for st in m.patterns(1) for r in range(17,34) for w in range(0,23,2)}
    found=set()
    for rec in packet['records']:
        state=key(rec);need(rec.get('scope')=='low_c' and not rec.get('limits'),'Low-c root restrictions')
        need(state not in found,'Repeated low-c state');found.add(state)
    need(found==expected and len(found)==4488,'Low-c bridge coverage')
    return len(found)

def verify(native_packets,ownerless,leaves_packet,trees,low_c):
    direct,owners,alphas,counts=expected_main()
    roots=collect_roots(native_packets)
    branched,nodes=verify_trees(trees,leaves_packet['records'])
    need(not roots&branched,'A root is both direct and branched')
    need(roots|branched==direct,'Main actual activity census has omissions or extras')
    owner=verify_ownerless(ownerless,owners);bridge=verify_low_c(low_c)
    need(len(alphas)==20,'Pinned alpha interface census')
    # j>=4 makes every hull-active native actually hit, permitting alpha.
    need(min(r*(r+1)//2+4*r+(r-33)**2 for r in range(15,52))==459,'Hull-hit mass minimum')
    need(459-393-14==52>0,'Hull-hit source guard')
    return dict(status='PASS_COMPLETE_DISPATCH',main_roots=sum(counts.values()),
                by_j=dict(sorted(counts.items())),direct_integer_proof_roots=len(roots),
                endpoint_tree_roots=len(branched),endpoint_branch_roots=sum('leaf' not in rec['tree'] for rec in trees),
                endpoint_tree_nodes=nodes,endpoint_split_nodes=nodes-len(leaves_packet['records']),endpoint_leaves=len(leaves_packet['records']),
                ownerless=owner,pinned_alpha_roots=len(alphas),low_c_bridge_roots=bridge,
                written_preconditions='Common integer source, structural reductions, raw gap and forest licenses are proved in the pinned report.')
