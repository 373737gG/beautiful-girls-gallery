# -*- coding: utf-8 -*-
import io, re

s = io.open('index.html', encoding='utf-8').read()
for l in re.split(r'\r?\n', s):
    if l.startswith('{id:'):
        n = re.match(r'\{id:(\d+)', l).group(1)
        if 261 <= int(n) <= 267:
            name = re.search(r'name:"([^"]+)"', l).group(1)
            tags = re.search(r'tags:\[(.*?)\]', l)
            print(name, '->', tags.group(1) if tags else 'NO TAGS')
print('plana:', 'id:284,name' in s)
print('version:', re.search(r"DATA_VERSION = '([^']+)'", s).group(1))
