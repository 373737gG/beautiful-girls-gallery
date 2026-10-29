# -*- coding: utf-8 -*-
"""校正/查验/补全：09总表(109) + 10第8批(6) 双向核对 index.html 的 115 条 birth
方向A 表→文件：清单每条在 index.html 中 birth 一致（查漏/错值）
方向B 文件→表：index.html 每条 birth 能在清单中找到（抓未经查证的孤儿数据）
"""
import re

BASE = r'D:\zhumian\工作区\项目归档\美少女图鉴'
txt = open(BASE + r'\index.html', encoding='utf-8').read()
t09 = open(BASE + r'\生日数据查证\09-生日合并总表-109项.md', encoding='utf-8').read()
t10 = open(BASE + r'\生日数据查证\10-第8批-缺race角色生日查证.md', encoding='utf-8').read()

# ===== 清单侧（09 表格行：| 文件角色名 | ... | birth | 状态 |） =====
expect = {}  # name -> birth
for m in re.finditer(r'^\| ([^|]+) \| ([^|]+) \| [^|]+ \| \*\*([\d-]+)\*\* \| (✅|❌|⬜|⚠)', t09, re.M):
    name, alias, birth = m.group(1).strip(), m.group(2).strip(), m.group(3)
    if name == '（未匹配）':  # HK416 行：角色名在"清单写法"列
        name = alias
    expect[name] = birth
n09 = len(expect)

# 10 文件确认清单（表格：| # | 角色 | 出处 | birth | ...）
for m in re.finditer(r'^\| \d+ \| ([^|]+) \| [^|]* \| \*\*([\d-]+)\*\* \|', t10, re.M):
    expect[m.group(1).strip()] = m.group(2)
print('清单侧条目: 09表 %d + 10第8批 %d = %d' % (n09, len(expect) - n09, len(expect)))

# ===== 文件侧（index.html 数据行：id/name/birth） =====
actual = {}
for ln in txt.split('\n'):
    m = re.match(r'\{id:(\d+),', ln)
    if not m:
        continue
    nm = re.search(r'name:"([^"]+)"', ln)
    bt = re.search(r'birth:"(\d{1,2}-\d{1,2})"', ln)
    if nm:
        actual[nm.group(1)] = (int(m.group(1)), bt.group(1) if bt else None)

# 名字写法差异映射（清单写法 -> index.html 写法）
ALIAS = {'可露凯 / HK416': 'HK416/可露凯'}

# ===== 方向A：表→文件 =====
print('\n== 方向A：清单 -> index.html ==')
errs = []
for name, birth in expect.items():
    aname = ALIAS.get(name, name)
    if aname not in actual:
        errs.append('清单有但文件无此角色: %s (%s)' % (name, birth))
        continue
    aid, abirth = actual[aname]
    if abirth is None:
        errs.append('缺写入: %s(id%d) 应为 %s' % (aname, aid, birth))
    elif abirth != birth:
        errs.append('值冲突: %s(id%d) 文件=%s 清单=%s' % (aname, aid, abirth, birth))
if errs:
    for e in errs:
        print('  ' + e)
else:
    print('  %d 条全部一致' % len(expect))

# ===== 方向B：文件→表（抓孤儿/未查证数据） =====
print('\n== 方向B：index.html -> 清单（孤儿检测） ==')
norm = lambda s: s.replace(' ', '')
parts = lambda s: frozenset(norm(s).split('/'))  # "可露凯 / HK416" 与 "HK416/可露凯" → 同一名字集合
rev = {}
for name, birth in expect.items():
    rev.setdefault(birth, []).append(parts(name))
orphans = []
for aname, (aid, abirth) in actual.items():
    if abirth is None:
        continue
    cands = rev.get(abirth, [])
    ap = parts(aname)
    if ap in cands or any(ap <= c or c <= ap for c in cands):
        continue
    orphans.append('id%d %s birth=%s 不在清单' % (aid, aname, abirth))
if orphans:
    for o in orphans:
        print('  ' + o)
else:
    print('  无孤儿：115 条全部有清单依据')

print('\n文件侧 birth 总数:', sum(1 for _, (_, b) in actual.items() if b))
print('VERDICT:', 'PASS' if not errs and not orphans else 'NEED FIX')
