# -*- coding: utf-8 -*-
"""全量核对：无图角色/单图角色/缺失引用/孤儿文件，并与 HEAD 对比"""
import os, re, collections, subprocess

ROOT = r'D:\zhumian\工作区\项目归档\美少女图鉴'
HTML = os.path.join(ROOT, 'index.html')
IMG_ROOT = os.path.join(ROOT, 'images')

with open(HTML, 'r', encoding='utf-8') as f:
    text = f.read()

# 解析所有角色行
pat = re.compile(r'\{id:\d+,name:"[^"]+".*?images:\[[^\]]*\]', re.S)
rows = pat.findall(text)
print('解析角色行数:', len(rows))

chars = []
for r in rows:
    name = re.search(r'name:"([^"]+)"', r).group(1)
    cid = re.search(r'\{id:(\d+)', r).group(1)
    imgs = re.findall(r'"([^"]+)"', re.search(r'images:\[([^\]]*)\]', r).group(1))
    chars.append({'id': cid, 'name': name, 'imgs': imgs})

print('角色总数:', len(chars))

print('\n===== 无图角色（images 为空）=====')
empty = [c for c in chars if not c['imgs']]
print('无图角色数:', len(empty))
for c in empty:
    print('  id:%s %s' % (c['id'], c['name']))

print('\n===== 单图角色（可能"图少了"）=====')
single = [c for c in chars if len(c['imgs']) == 1]
print('单图角色数:', len(single))
for c in single[:60]:
    print('  id:%s %s -> %s' % (c['id'], c['name'], c['imgs'][0]))
if len(single) > 60:
    print('  ... 共 %d 个' % len(single))

print('\n===== 缺失引用（引用存在但磁盘无文件）=====')
missing = []
for c in chars:
    for p in c['imgs']:
        fp = os.path.join(IMG_ROOT, p.replace('/', os.sep))
        if not os.path.exists(fp):
            missing.append((c['name'], p))
print('缺失引用数:', len(missing))
for n, p in missing:
    print('  %s -> %s' % (n, p))

print('\n===== 孤儿文件（磁盘有但未引用）=====')
all_refs = set()
for c in chars:
    all_refs.update(c['imgs'])
on_disk = set()
for dirpath, _, filenames in os.walk(IMG_ROOT):
    for fn in filenames:
        rel = os.path.relpath(os.path.join(dirpath, fn), IMG_ROOT).replace(os.sep, '/')
        on_disk.add(rel)
orphans = sorted(on_disk - all_refs)
print('磁盘文件数:', len(on_disk), ' 孤儿:', len(orphans))
for p in orphans:
    print('  ORPHAN:', p)
