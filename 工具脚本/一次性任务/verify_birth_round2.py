# -*- coding: utf-8 -*-
"""第2轮合并后最终自检（只读，交接文件原版逻辑 + id 定位修正抽查）"""
import re

txt = open(r'D:\zhumian\工作区\项目归档\美少女图鉴\index.html', encoding='utf-8').read()

names = re.findall(r'name:"([^"]+)"', txt)
births = re.findall(r'birth:"([^"]+)"', txt)
print('角色总数 :', len(names), '(应为 285)')
print('birth 总数:', len(births), '(应为 115)')
bad = [b for b in births if not re.fullmatch(r'\d{1,2}-\d{1,2}', b)]
print('格式异常 :', bad or '无')

# 六个抽样项（id 定位版：规避名字在他人 desc 先出现导致的错位）
checks = [(63, '帆稀', '4-17'), (65, '维尔姆', '2-5'), (188, 'HK416/可露凯', '4-16'),
          (277, '本条二亚', '2-29'), (48, '苇草', '10-16'), (291, '楪祈', '9-12')]
all_ok = True
for cid, name, exp in checks:
    m = re.search(r'\{id:%d,[^\n]*?birth:"([^"]+)"' % cid, txt)
    got = m.group(1) if m else '未写入'
    ok = got == exp
    all_ok = all_ok and ok
    print('id %-4d %-12s 期望 %-6s 实际 %-6s %s' % (cid, name, exp, got, 'OK' if ok else 'FAIL'))

# 115 条 birth 与角色行一一对应（每条 birth 都在某条数据行内、无孤儿）
row_births = 0
for ln in txt.split('\n'):
    if re.match(r'\{id:\d+,', ln):
        row_births += len(re.findall(r'birth:"\d{1,2}-\d{1,2}"', ln))
print('数据行内 birth:', row_births, '(应与总数一致 115)')
print('ALL PASS' if (len(names) == 285 and len(births) == 115 and not bad and all_ok and row_births == 115) else 'FAILED')
