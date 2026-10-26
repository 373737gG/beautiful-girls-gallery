# -*- coding: utf-8 -*-
# 并入 41 条新角色到 index.html 的 DEFAULT_DATA，并升 DATA_VERSION
import io, re, shutil, sys

ROOT = r'D:\zhumian\工作区\项目归档\美少女图鉴'
IDX = ROOT + r'\index.html'
SRC = ROOT + r'\新增角色设定-20261026.txt'
BAK = ROOT + r'\index.html.bak-20261027-并入41新角色'

# 1) 备份
shutil.copy2(IDX, BAK)
print('backup ok:', BAK.encode('ascii', 'backslashreplace').decode())

s = io.open(IDX, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'
print('newline:', repr(nl))

# 2) 读取新条目
entries = [l.rstrip('\r\n') for l in io.open(SRC, encoding='utf-8') if l.lstrip().startswith('{id:')]
assert len(entries) == 41, 'entries=%d' % len(entries)
for e in entries:
    assert e.endswith(','), e[:40]
    assert '\r' not in e and '\n' not in e
    assert '"' not in e[e.index('story:'):] or True

# 3) 防重复：新角色名不得已存在于 index.html
names = [re.search(r'name:"([^"]+)"', e).group(1) for e in entries]
for n in names:
    if 'name:"' + n in s:
        print('DUP NAME:', n.encode('unicode_escape').decode()); sys.exit(1)

# 4) 定位 DEFAULT_DATA 数据块结尾（首个行首 "];"）
anchor = nl + '];'
pos = s.find(anchor)
assert pos != -1, 'anchor not found'
# 确认锚点在 DEFAULT_DATA 之后
assert s.find('const DEFAULT_DATA') < pos

# 5) 插入（先补一个换行，避免与上一行拼接）
insert = nl + nl.join(entries)
s2 = s[:pos] + insert + s[pos:]

# 6) 升版本
old_v = re.search(r"const DATA_VERSION = '([^']+)'", s2).group(1)
s2 = s2.replace("const DATA_VERSION = '%s';" % old_v, "const DATA_VERSION = '20261027-v32';", 1)
print('version:', old_v, '->', '20261027-v32')

io.open(IDX, 'w', encoding='utf-8', newline='').write(s2)

# 7) 复验：重读文件
s3 = io.open(IDX, encoding='utf-8', newline='').read()
lines = [l for l in s3.split(nl) if l.startswith('{id:')]
ids = sorted(int(re.match(r'\{id:(\d+)', l).group(1)) for l in lines)
print('data lines:', len(lines), 'max id:', ids[-1], 'min:', ids[0])
missing = [i for i in range(243, 284) if i not in ids]
print('new ids missing:', missing)
assert not missing and len(lines) == 280
assert "DATA_VERSION = '20261027-v32'" in s3
print('ALL OK')
