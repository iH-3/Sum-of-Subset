"""Add new actual subset-sum targets without restarting old probe searches.

The existing complete ten-source-block family proves each target is in
FS(A), with no interval-placement premise. Only the newly added probe is
propagated in each call. A run adds at most four distinct affine targets.
"""
import full_cover as fc,model as m

def discover(search,point):
    m.need(search.j>=3 and 3 not in search.st.values(),'Full integer known-target scope')
    if not hasattr(search,'known_target_start'):search.known_target_start=len(search.full_probes)
    if len(search.full_probes)-search.known_target_start>=4:return False,False
    used={tuple(sorted((k,c) for k,c in p['target'].items() if c)) for p in search.full_probes}
    candidates=fc.known_candidate(point,used)
    if not candidates:return False,False
    _,mask,source_mask,target=candidates[0];pid=len(search.full_probes)
    search.trace.append(dict(kind='full_cover_known_probe',mask=mask,source_mask=source_mask))
    search.full_probes.append(dict(target=target,mask=mask,width=1,margin=0,nodes=fc.initial_nodes(),forced=False))
    previous=getattr(search,'max_full_probes',4);search.max_full_probes=0
    try:changed,finished=search.full_cover_step(point,{pid})
    finally:search.max_full_probes=previous
    print('NEW_ACTUAL_TARGET',pid,'remaining_components',len(search.full_probes[pid]['nodes']),flush=True)
    # If the propagation itself proved an LP contradiction, the caller must
    # append its exact final certificate. An empty cover already has one.
    if finished:return changed,True
    return True,False
