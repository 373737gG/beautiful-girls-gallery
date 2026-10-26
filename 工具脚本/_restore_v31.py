# -*- coding: utf-8 -*-
# 逆向修复：从"坏合并版"还原出干净的 v31 index.html
import io, re

IDX = r'D:\zhumian\工作区\项目归档\美少女图鉴\index.html'
s = io.open(IDX, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'
lines = s.split(nl)
out = []
fixed_split = 0
dropped = 0
for l in lines:
    if l.startswith('{id:'):
        m = re.match(r'\{id:(\d+)', l)
        i = int(m.group(1))
        if 244 <= i <= 283:
            dropped += 1
            continue  # 丢弃误插入的整行
        if '{id:243,' in l:
            # 拆开与 id:242 拼在一起的行
            k = l.index('{id:243,')
            assert l[k-1] == ','
            out.append(l[:k])  # id:242 原行，保留尾逗号
            out.append(l[k:])
            fixed_split += 1
            continue
    out.append(l)

s2 = nl.join(out)
s2 = s2.replace("const DATA_VERSION = '20261027-v32';", "const DATA_VERSION = '20261026-v31';", 1)
io.open(IDX, 'w', encoding='utf-8', newline='').write(s2)

# 复验
s3 = io.open(IDX, encoding='utf-8', newline='').read()
dl = [l for l in s3.split(nl) if l.startswith('{id:')]
ids = sorted(int(re.match(r'\{id:(\d+)', l).group(1)) for l in dl)
print('dropped:', dropped, 'split fixed:', fixed_split)
print('data lines:', len(dl), 'max id:', ids[-1], 'v31?', "DATA_VERSION = '20261026-v31'" in s3)
print('has 243?', 243 in ids)
assert len(dl) == 239 and ids[-1] == 242 and 243 not in ids
print('RESTORED OK')
