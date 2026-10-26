# -*- coding: utf-8 -*-
import io, re

s = io.open(r'D:\zhumian\工作区\项目归档\美少女图鉴\index.html', encoding='utf-8').read()
blocks = re.findall(r'<script>(.*?)</script>', s, re.S)
print('script blocks:', len(blocks))
js = max(blocks, key=len)
io.open(r'D:\zhumian\工作区\项目归档\美少女图鉴\工具脚本\_extracted.js', 'w', encoding='utf-8').write(js)
print('js chars:', len(js))

# 新增条目：story/desc 内不得含未转义 ASCII 双引号（引号数成对即无内嵌）
bad = []
for l in js.split('\n'):
    ls = l.strip()
    if ls.startswith('{id:2'):
        i = int(re.match(r'\{id:(\d+)', ls).group(1))
        if 243 <= i <= 283 and ls.count('"') % 2 != 0:
            bad.append(i)
print('odd-quote lines:', bad)
