# -*- coding: utf-8 -*-
import io, re, json

p = r'D:\zhumian\工作区\项目归档\美少女图鉴\新增角色设定-20261026.txt'
s = io.open(p, encoding='utf-8').read()
lines = [l.strip() for l in s.split('\n') if l.strip().startswith('{id:')]
print('count', len(lines))

ids = []
bad = []
req = ['id', 'name', 'source', 'type', 'race', 'desc', 'story', 'tags']
for l in lines:
    body = l.rstrip(',')
    # quote unquoted keys
    obj_txt = re.sub(r'([{,])(\w+):', r'\1"\2":', body)
    obj_txt = obj_txt.replace('""', '""')
    try:
        o = json.loads(obj_txt)
    except Exception as e:
        bad.append((body[:60], str(e)))
        continue
    ids.append(o['id'])
    for k in req:
        if k not in o:
            bad.append((o.get('name'), 'missing ' + k))
    sl = len(o.get('story', ''))
    dl = len(o.get('desc', ''))
    tl = len(o.get('tags', []))
    if not (60 <= sl <= 320):
        bad.append((o['name'], 'story len %d' % sl))
    if not (20 <= dl <= 90):
        bad.append((o['name'], 'desc len %d' % dl))
    if not (2 <= tl <= 3):
        bad.append((o['name'], 'tags n=%d' % tl))
    if o.get('images') != [""]:
        bad.append((o['name'], 'images %r' % o.get('images')))

print('id range', min(ids), max(ids), 'unique', len(set(ids)) == len(ids))
expected = list(range(243, 284))
print('id complete', sorted(ids) == expected)
print('bad:', len(bad))
for b in bad:
    print('  ', b)
