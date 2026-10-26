# -*- coding: utf-8 -*-
import io, re

s = io.open('index.html', encoding='utf-8').read()
target = {'兽耳娘/images_9.jpg', '兽耳娘/images_11.jpg', '兽耳娘/118467754.jpg'}
for l in re.split(r'\r?\n', s):
    if l.startswith('{id:'):
        m = re.search(r'images:\[(.*?)\]', l)
        if m:
            imgs = re.findall(r'"([^"]+)"', m.group(1))
            hit = [i for i in imgs if i in target]
            if hit:
                name = re.search(r'name:"([^"]+)"', l).group(1)
                cid = re.match(r'\{id:(\d+)', l).group(1)
                print(f'id:{cid} {name} -> 引用: {imgs}')
