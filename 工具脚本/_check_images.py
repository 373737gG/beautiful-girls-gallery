# -*- coding: utf-8 -*-
import io, re

s = io.open('index.html', encoding='utf-8').read()
empty_str = 0
empty_arr = 0
has_img = 0
examples = []
for l in re.split(r'\r?\n', s):
    if l.startswith('{id:'):
        cid = int(re.match(r'\{id:(\d+)', l).group(1))
        m = re.search(r'images:\[(.*?)\]', l)
        if not m:
            continue
        val = m.group(1).strip()
        if val == '""':
            empty_str += 1
            if len(examples) < 8:
                examples.append(cid)
        elif val == '':
            empty_arr += 1
        else:
            has_img += 1
print('images:[""] :', empty_str, 'ids:', examples)
print('images:[]   :', empty_arr)
print('有图条目    :', has_img)
