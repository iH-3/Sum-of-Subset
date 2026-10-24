"""Reject unsupported integer rounding and incomplete cover contradictions."""
from pathlib import Path
import copy,json,sys
root=Path(__file__).resolve().parents[3];sys.path.insert(0,str(root/'verification/upper80'))
import exact,model as m,parametric as p
from endpoint_schedule import check as schedule_check,endpoint
st=([*m.patterns(6),*m.partial_patterns(6)])[436]
record=dict(st=st,j=6,positive=False,limits={},trace=[])
exact.replay(record,require_closed=False)
rejected=[]
def reject(label,step):
    rec=copy.deepcopy(record);rec['trace'].append(step)
    try:exact.replay(rec,require_closed=False)
    except (ValueError,TypeError,KeyError,IndexError):rejected.append(label)
    else:raise ValueError('Accepted false trace: '+label)
reject('unlicensed coverage final',dict(kind='coverage_final',side='s',probe=0))
reject('unlicensed coverage force',dict(kind='coverage_force',side='s',probe=0,component=1))
reject('unlicensed complete cover final',dict(kind='full_cover_final',probe=0))
reject('unlicensed complete cover force',dict(kind='full_cover_force',probe=0,node=[0,-1]))
reject('unlicensed complete cover refinement',dict(kind='full_cover_refine',probe=0,root=0))
reject('unlicensed complete cover exclusion',dict(kind='full_cover_exclude',probe=0,node=[0,-1],direction=0,certificate={}))
reject('nonintegral complete cover target',dict(kind='full_cover_probe',target={'ONE':0.5},mask=0,certificates=[]))
reject('noninteger physical mask',dict(kind='full_cover_probe',target={},mask=True,certificates=[]))
reject('unproved complete target bracket',dict(kind='full_cover_probe',target={},mask=0,certificates=[]))
reject('zero-hole width change',dict(kind='coverage_width',hole_upper=1,certificate={}))
reject('zero-hole single-hole lemma',dict(kind='single_hole_interior',H=1,certificates=[]))
reject('unlicensed core-tail capacity',dict(kind='core_tail_capacity',side='s'))
reject('unlicensed ordered cover capacity',dict(kind='ordered_cover_capacity',selected={'s':[0]},credit=0,joint=False))
reject('empty known fixed-cover chain',dict(kind='fixed_known_cover',label=next(label for label in m.fixed_forms() if '+' in label),side='s',modes={'s':0,'t':0},chain=[],certificates=[]))
reject('unlicensed real variable rounding',dict(kind='integer_guard',guard={'unlicensed_real':1},certificate={'weights':[],'denominator':1}))
reject('rounding without strict bound',dict(kind='integer_guard',guard={'ONE':1},certificate={'weights':[],'denominator':1}))
reject('unsupported integral bound',dict(kind='integer_guard',guard={'xs':1},certificate={'weights':[],'denominator':1}))
probe=dict(kind='full_cover_probe',target={},mask=0,certificates=[dict(weights=[],denominator=1),dict(weights=[],denominator=1)])
licensed=copy.deepcopy(record);licensed['trace']=[probe]
exact.replay(licensed,require_closed=False)
for label,steps in [
    ('premature complete cover final',[dict(kind='full_cover_final',probe=0)]),
    ('premature unique complete component',[dict(kind='full_cover_force',probe=0,node=[0,-1])]),
    ('false complete component exclusion',[dict(kind='full_cover_exclude',probe=0,node=[0,-1],direction=0,certificate=dict(weights=[],denominator=1))]),
    ('duplicate complete refinement',[dict(kind='full_cover_refine',probe=0,root=0)]*2),
    ('refining a four-outer singleton',[dict(kind='full_cover_refine',probe=0,root=494)]),
]:
    rec=copy.deepcopy(licensed);rec['trace'].extend(steps)
    try:exact.replay(rec,require_closed=False)
    except (ValueError,TypeError,KeyError,IndexError):rejected.append(label)
    else:raise ValueError('Accepted false licensed trace: '+label)
bad=copy.deepcopy(endpoint(35,100));bad['thresholds'][0]=1000
try:schedule_check(bad)
except ValueError:rejected.append('unlicensed endpoint threshold')
else:raise ValueError('Accepted false endpoint threshold')
cuts=0
for value in range(-10,11):
    for cut in range(-10,11):
        if (value<=cut)+(value>=cut+1)!=1:raise ValueError('Noncomplementary integer split')
        cuts+=1
print(json.dumps(dict(status='PASS_NEW_TRACE_NEGATIVE_CONTROLS',rejected=rejected,integer_splits=cuts)))
