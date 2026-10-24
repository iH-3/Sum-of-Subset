"""Order-preserving, content-addressed storage for nested research records.

Certificate row indices depend on insertion order. Never sort record keys.
A reserved one-key reference object replaces records wherever they occur,
including conditional leaves nested inside a trace.
"""
import hashlib,json
import model as m

def canonical(value):return json.dumps(value,separators=(',',':')).encode()

def pack(value):
    pool={};identities={}
    def visit(item):
        if isinstance(item,list):return [visit(v) for v in item]
        if not isinstance(item,dict):return item
        is_record={'st','j','positive','trace'}<=set(item)
        if is_record and id(item) in identities:return {'$record':identities[id(item)]}
        body={k:visit(v) for k,v in item.items()}
        if is_record:
            key=hashlib.sha256(canonical(body)).hexdigest()
            if key in pool:m.need(pool[key]==body,'Record digest collision')
            pool[key]=body;identities[id(item)]=key;return {'$record':key}
        m.need(set(body)!={'$record'},'Reserved record reference marker')
        return body
    payload=visit(value)
    return dict(schema='upper80-nested-record-pool-v1',payload=payload,records=pool)

def unpack(packet):
    m.need(packet['schema']=='upper80-nested-record-pool-v1','Nested record pool schema')
    pool=packet['records'];memo={};visiting=set()
    def visit(item):
        if isinstance(item,list):return [visit(v) for v in item]
        if not isinstance(item,dict):return item
        if set(item)=={'$record'}:
            key=item['$record']
            if key in memo:return memo[key]
            m.need(key in pool and key not in visiting,'Acyclic nested record reference')
            body=pool[key];m.need(hashlib.sha256(canonical(body)).hexdigest()==key,'Order-preserving nested record identity')
            visiting.add(key);value={k:visit(v) for k,v in body.items()};visiting.remove(key)
            m.need({'st','j','positive','trace'}<=set(value),'Referenced research record')
            memo[key]=value;return value
        return {k:visit(v) for k,v in item.items()}
    value=visit(packet['payload']);m.need(set(memo)==set(pool),'Every pooled record referenced');return value

def read_gzip(path):
    import gzip
    value=json.loads(gzip.decompress(path.read_bytes()))
    return unpack(value) if value.get('schema')=='upper80-nested-record-pool-v1' else value

def write_gzip(path,value):
    import gzip
    packet=pack(value);temp=path.with_suffix('.tmp')
    temp.write_bytes(gzip.compress(canonical(packet),mtime=0));temp.replace(path)
