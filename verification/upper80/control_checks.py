"""Negative controls for the partial research packet (standard library only)."""
from pathlib import Path
import importlib.util,json,sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import replay_partial as rp
from exact import check


def verify():
    packet=rp.load_packet();rejected=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError,TypeError):rejected.append(name)
        else:raise ValueError('Invalid evidence accepted: '+name)
    original=rp.load_packet
    rp.load_packet=lambda:dict(packet,open=packet['open'][1:])
    try:reject('missing open root',rp.verify)
    finally:rp.load_packet=original
    root=dict(packet['branches'][0]);root['tree']=dict(root['tree']);root['tree'].pop('right')
    reject('missing complementary branch',lambda:rp.branch(root))
    reject('negative Farkas multiplier',lambda:check({'weights':[('r',0,-1)],'denominator':None},[({'x':1},-1,'row')],[]))
    reject('zero contradiction',lambda:check({'weights':[('r',0,1)],'denominator':None},[({'x':1},0,'row')],[]))
    return dict(status='PASS_PARTIAL_NEGATIVE_CONTROLS',global_upper_bound_certified=False,rejected=rejected)

if __name__=='__main__':print(json.dumps(verify(),indent=2))
